#!/usr/bin/env python3
"""X.com 长文（Article / Long-form post）专用抓取器。

背景：`fetch_article.py` 的通用提取对 X 长文无效——它取到的 innerText 会把
85 个 Draft.js 块压成一行，并且混入 "Want to publish your own Article?"
"Upgrade to Premium" "Post your reply" 等按钮文案；标题还会退化成 "Conversation"。

本脚本改为直接解析 X 长文的 Draft.js 结构：
  [data-testid="twitter-article-title"]            → 文章标题
  [data-testid="longformRichTextComponent"]        → 正文容器
    div[data-block="true"].longform-unstyled       → 段落（整段加粗且短 ⇒ 小标题）
    div[data-block="true"].longform-unordered-list-item → 无序列表项
  [data-testid="twitterArticleReadView"] img       → 封面图（长文只有封面，无正文插图）

前置条件：CDP Chrome 必须带 X 登录态（auth_token）。
见 references/platform-specific.md「X.com / Twitter 帖子」。

用法：
  python3 scripts/x_article_fetch.py "<x.com 链接>" --output-dir <目录>
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

_CDP_PORT_FILE = Path.home() / ".fetch_article" / "cdp_port"
try:
    _saved = _CDP_PORT_FILE.read_text(encoding="utf-8").strip()
except OSError:
    _saved = ""
CDP_PORT = int(os.environ.get("FETCH_ARTICLE_CDP_PORT") or _saved or "9222")

NOISE_MARKERS = [
    "want to publish your own article",
    "upgrade to premium",
    "post your reply",
    "view quotes",
    "discover more",
    "relevant people",
]

_EXTRACT_JS = r"""
() => {
  const rv = document.querySelector('[data-testid="twitterArticleReadView"]');
  if (!rv) return {error: 'no twitterArticleReadView'};
  const titleEl = document.querySelector('[data-testid="twitter-article-title"]');
  const rt = document.querySelector('[data-testid="longformRichTextComponent"]');
  if (!rt) return {error: 'no longformRichTextComponent'};

  function inlineMd(node) {
    let out = '';
    node.childNodes.forEach(n => {
      if (n.nodeType === 3) { out += n.textContent; return; }
      if (n.nodeType !== 1) return;
      const tag = n.tagName.toLowerCase();
      if (tag === 'br') { out += '\n'; return; }
      const inner = inlineMd(n);
      if (!inner) return;
      const st = n.getAttribute('style') || '';
      if (tag === 'a') {
        const href = n.getAttribute('href') || '';
        if (href && !href.startsWith('#')) {
          const abs = href.startsWith('http') ? href : 'https://x.com' + href;
          out += '[' + inner.trim() + '](' + abs + ')';
        } else { out += inner; }
        return;
      }
      const lead = inner.match(/^\s+/);
      const trail = inner.match(/\s+$/);
      const core = inner.trim();
      if (!core) { out += inner; return; }
      let s = core;
      if (/font-weight:\s*(bold|[6-9]00)/.test(st) || tag === 'b' || tag === 'strong') {
        s = '**' + s + '**';
      }
      if (/font-style:\s*italic/.test(st) || tag === 'i' || tag === 'em') {
        s = '*' + s + '*';
      }
      // 标记符号不能吞掉边界空格，否则 "*I*think" 这类粘连会破坏阅读与分词
      out += (lead ? lead[0] : '') + s + (trail ? trail[0] : '');
    });
    return out;
  }

  const blocks = Array.from(rt.querySelectorAll('[data-block="true"]')).map(bl => {
    const cls = (bl.className || '').toString();
    let kind = 'p';
    if (/unordered-list-item/.test(cls)) kind = 'li';
    else if (/ordered-list-item/.test(cls)) kind = 'oli';
    else if (/blockquote/.test(cls)) kind = 'quote';
    else if (/header-(one|1)/.test(cls)) kind = 'h1';
    else if (/header-(two|2)/.test(cls)) kind = 'h2';
    else if (/header-(three|3)/.test(cls)) kind = 'h3';
    else if (/code-block/.test(cls)) kind = 'code';
    return {kind: kind, md: inlineMd(bl).replace(/\u00a0/g, ' ').trim()};
  }).filter(b => b.md.length > 0);

  // 封面图：长文正文内没有插图，媒体图在 ReadView 层
  const cover = Array.from(rv.querySelectorAll('img'))
    .map(i => i.src || '')
    .filter(s => s.includes('pbs.twimg.com/media/'));

  const timeEl = document.querySelector('article time[datetime]');
  const userName = document.querySelector('[data-testid="User-Name"]');
  const analytics = document.querySelector('a[href*="/analytics"]');

  return {
    title: titleEl ? titleEl.innerText.trim() : '',
    blocks: blocks,
    cover: cover,
    date: timeEl ? (timeEl.getAttribute('datetime') || '') : '',
    date_text: timeEl ? timeEl.innerText.trim() : '',
    author_block: userName ? userName.innerText : '',
    views: analytics ? analytics.innerText.replace(/\s+/g, ' ').trim() : '',
    text_len: rt.innerText.length
  };
}
"""


def _norm_cover(url: str) -> str:
    base = url.split("?")[0]
    return f"{base}?format=jpg&name=large"


def _download(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                dest.write_bytes(r.read())
            return dest.stat().st_size > 1024
        except Exception:
            continue
    return False


def build_markdown(title: str, author: str, handle: str, date: str, url: str,
                   blocks: list, image_rel: str | None) -> str:
    lines = [f"# {title}", ""]
    if image_rel:
        lines += [f"![{title}]({image_rel})", ""]
    meta = []
    if author:
        meta.append(f"> 作者: {author}" + (f" (@{handle})" if handle else ""))
    if date:
        meta.append(f"> 发布时间: {date}")
    meta.append(f"> 原文链接: {url}")
    lines += meta + ["", "---", ""]

    for i, b in enumerate(blocks):
        kind, md = b["kind"], b["md"]
        if kind == "li":
            lines.append(f"- {md}")
            nxt = blocks[i + 1]["kind"] if i + 1 < len(blocks) else None
            if nxt != "li":
                lines.append("")
        elif kind == "oli":
            lines.append(f"1. {md}")
            nxt = blocks[i + 1]["kind"] if i + 1 < len(blocks) else None
            if nxt != "oli":
                lines.append("")
        elif kind in ("h1", "h2", "h3"):
            lines += [f"## {md}", ""]
        elif kind == "quote":
            lines += [f"> {md}", ""]
        elif kind == "code":
            lines += ["```", md, "```", ""]
        else:
            # 整段加粗且较短 ⇒ 作者用作小标题
            m = re.fullmatch(r"\*\*(.+?)\*\*", md, re.S)
            if m and len(m.group(1)) <= 80 and "\n" not in m.group(1):
                lines += [f"## {m.group(1).strip()}", ""]
            else:
                lines += [md, ""]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


async def run(url: str, out_dir: Path, port: int) -> int:
    from playwright.async_api import async_playwright

    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / "images"
    images_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        except Exception as e:
            print(f"❌ 无法连接 CDP Chrome（端口 {port}）：{e}", file=sys.stderr)
            print("   先按 references/platform-specific.md 启动带 X 登录态的 CDP Chrome。",
                  file=sys.stderr)
            return 2
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        cookies = await ctx.cookies("https://x.com")
        if not any(c.get("name") == "auth_token" for c in cookies):
            print("❌ CDP Chrome 未登录 X（缺少 auth_token cookie）。", file=sys.stderr)
            print("   X 长文必须用带登录态的 CDP Chrome，禁止匿名回退。", file=sys.stderr)
            return 3

        page = await ctx.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            await page.wait_for_selector('[data-testid="longformRichTextComponent"]',
                                         timeout=45000)
        except Exception:
            print("❌ 未渲染出长文正文（longformRichTextComponent 超时）。", file=sys.stderr)
            await page.close()
            return 4
        await page.wait_for_timeout(2000)
        data = await page.evaluate(_EXTRACT_JS)
        await page.close()

    if data.get("error"):
        print(f"❌ 提取失败：{data['error']}", file=sys.stderr)
        return 5

    blocks = data["blocks"]
    title = (data["title"] or "").strip()
    if not title:
        print("❌ 未取到文章标题。", file=sys.stderr)
        return 6
    if len(blocks) < 5 or data["text_len"] < 500:
        print(f"❌ 正文过短（{len(blocks)} 块 / {data['text_len']} 字符），判定抓取失败。",
              file=sys.stderr)
        return 7

    author, handle = "", ""
    ab = data.get("author_block") or ""
    lines = [x for x in ab.split("\n") if x.strip()]
    if lines:
        author = lines[0].strip()
    m = re.search(r"@([A-Za-z0-9_]+)", ab)
    if m:
        handle = m.group(1)

    image_rel = None
    downloaded = 0
    if data.get("cover"):
        cu = _norm_cover(data["cover"][0])
        digest = hashlib.sha1(cu.encode()).hexdigest()[:8]
        dest = images_dir / f"img_01_{digest}.jpg"
        if dest.exists() or _download(cu, dest):
            image_rel = f"images/{dest.name}"
            downloaded = 1
        else:
            print("⚠️  封面图下载失败", file=sys.stderr)

    md = build_markdown(title, author, handle, data.get("date", ""), url, blocks, image_rel)
    (out_dir / "source.md").write_text(md, encoding="utf-8")

    refs = re.findall(r"\((images/[^)\s]+)\)", md)
    local_files = sorted(p.name for p in images_dir.glob("*") if p.is_file())
    missing = [r for r in refs if not (out_dir / r).exists()]
    noise = [n for n in NOISE_MARKERS if n in md.lower()]

    meta = {
        "title": title,
        "display_title": title,
        "source_url": url,
        "source_title": title,
        "source_type": "article",
        "platform": "x.com",
        "language": "en",
        "author": author,
        "author_handle": handle,
        "date": data.get("date", ""),
        "date_text": data.get("date_text", ""),
        "views": data.get("views", ""),
        "content_length": len(md),
        "image_count": downloaded,
        "images": [image_rel] if image_rel else [],
        "fetched_at": datetime.now().isoformat(),
        "verification": {
            "ok": not missing and not noise,
            "source_sha256": hashlib.sha256(md.encode()).hexdigest(),
            "block_count": len(blocks),
            "markdown_image_references": len(refs),
            "unique_local_images": len(local_files),
            "missing_local_images": len(missing),
            "platform_noise_hits": noise,
        },
    }
    (out_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"📖 标题: {title}")
    print(f"👤 作者: {author} (@{handle})   日期: {data.get('date','')[:10]}   浏览: {data.get('views','')}")
    print(f"📏 正文: {len(md)} 字符 / {len(blocks)} 块")
    print(f"🖼️  图片: {downloaded} 张")
    print(f"✅ 工作包: {out_dir}")
    print(f"   校验: ok={meta['verification']['ok']} 缺图={len(missing)} 噪音={noise}")
    return 0 if meta["verification"]["ok"] else 8


def main() -> int:
    ap = argparse.ArgumentParser(description="X.com 长文专用抓取器")
    ap.add_argument("url")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--cdp-port", type=int, default=CDP_PORT)
    a = ap.parse_args()
    return asyncio.run(run(a.url, Path(a.output_dir), a.cdp_port))


if __name__ == "__main__":
    raise SystemExit(main())
