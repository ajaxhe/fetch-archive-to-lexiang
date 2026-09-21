#!/usr/bin/env python3
"""按本次归档范围校验双语文档。

范围约定（用户 2026-09-20 选定）：
  - 正文范围：source.md 第 1–581 行（题名/作者/摘要 + §1–6 + 结论）→ 中英对照
  - 参考文献与附录 A–E（582 行起）→ 保留英文原文

因此：
  1) 段落保全检查跑「全文」——附录英文原文也必须逐段仍在，不得丢失；
  2) 中文覆盖率检查只跑「已翻译范围」——否则英文附录会把分母撑大而误报；
  3) 「转义美元」检查只跑「已翻译范围」——附录里那些 `$` 是上传器公式解析所需的结构性转义，
     不是被误转义的金额；图片提取元数据则仍对全文检查。
"""
import json
import re
import sys
from pathlib import Path

SKILL_SCRIPTS = "/Users/helufan/.workbuddy/skills/trans-doc-to-md/scripts"
sys.path.insert(0, SKILL_SCRIPTS)
import bilingual_validation_core as c  # noqa: E402

TRANSLATED_SCOPE_END = 581  # 1-based，含

base = Path(__file__).resolve().parent
source = (base / "source.md").read_text(encoding="utf-8")
bilingual = (base / "Stealing Reasoning Traces from Proprietary LLM APIs.md").read_text(encoding="utf-8")
source_lines = source.splitlines()
source_body = "\n".join(source_lines[:TRANSLATED_SCOPE_END])
head = "\n\n".join(
    p.read_text(encoding="utf-8").strip() for p in sorted((base / "drafts").glob("part_*.md"))
)

METADATA_RE = re.compile(
    r"\[/?IMAGE\]|</?image_ocr>|(?:图片链接|图片标题|图片描述|图片OCR结果|图像 OCR)\s*[：:]",
    re.IGNORECASE,
)


def check_image_metadata(markdown: str) -> None:
    problems = [
        f"L{n}"
        for n, line in enumerate(markdown.splitlines(), start=1)
        if METADATA_RE.search(line)
    ]
    if problems:
        raise c.ValidationError("文档残留图片提取元数据：" + "；".join(problems[:5]))


checks = []
ok = True


def run(name, fn):
    global ok
    try:
        fn()
        checks.append({"check": name, "status": "pass"})
    except Exception as error:  # ValidationError 或 OSError
        ok = False
        checks.append({"check": name, "status": "fail", "detail": str(error)})


run("paragraph-preservation@full-document",
    lambda: c.validate_bilingual_source(c._without_trailing_subscription_chrome(source), bilingual))
run("translation-coverage@translated-scope",
    lambda: c.validate_translation_coverage(source_body, head))
run("local-images-preserved@full-document",
    lambda: c.validate_local_images_preserved(source, bilingual))
run("no-image-metadata@full-document", lambda: check_image_metadata(bilingual))
run("no-escaped-dollars@translated-scope",
    lambda: c.validate_no_image_metadata_or_escaped_dollars(head))

print(json.dumps({
    "ok": ok,
    "translated_scope": f"source.md lines 1-{TRANSLATED_SCOPE_END}",
    "english_only_scope": f"source.md lines {TRANSLATED_SCOPE_END + 1}-{len(source_lines)}",
    "checks": checks,
}, ensure_ascii=False, indent=2, sort_keys=True))
sys.exit(0 if ok else 1)
