### 微信公众号文章处理（mp.weixin.qq.com）

**强制方案：乐享 MCP `file_create_hyperlink`**

乐享后端原生支持微信公众号文章的抓取与解析，**一步到位**，无需本地抓取和手动上传图片。
URL host 一旦识别为 `mp.weixin.qq.com`，必须直接进入此分支；禁止先用 WebFetch、
Playwright/CDP、浏览器或 `fetch_article.py` 侦察/抓取正文。

```
file_create_hyperlink(
  url = "https://mp.weixin.qq.com/s/...",
  parent_entry_id = "<目标目录 entry_id>",
  name = "<文章标题>"  // 可选；仅在已可靠获知时传，不得为取标题而抓取
)
```

当前 MCP schema 只要求 `url` 与目标 `parent_entry_id`；不要编造或额外传入 schema
中不存在的 `space_id`。调用前仍须按主流程完成目标目录定位和 URL/标题去重。

**返回值**：
- `entry.id` — 必须存在，作为导入成功的硬条件
- 若响应暴露相关字段，再确认 `entry_type: "flink"`、`extension: "wechat"`
- 若响应含 `finished`，其值必须为 `true`

**后端自动完成的事情**：
1. 抓取微信文章全文（正文 + 图片）
2. 图片保存到乐享 COS（`/assets/xxx` 格式）
3. OCR 识别图片中的文字（用于全文检索和 AI 解析）
4. 自动提取标题、作者、发布时间等元信息

**优势**：
- 一步完成，省去 fetch_article.py + 分块导入 + 逐张上传图片的复杂流程
- Token 消耗从 ~50K 降到 <1K
- 图片质量由乐享后端保证，无需本地下载和上传
- 支持乐享的全文检索和 AI 解析（RAG）

**如需附加用户评价/评论**：
- 优先使用乐享评论能力。
- 不得把原生微信条目改造成 Markdown page，也不得再用 block/uploader 覆盖正文。

**失败处理**：
- 工具不可用、返回错误、`finished: false` 或缺少 `entry.id` 时，报告错误并停止。
- 禁止静默回退到 `fetch_article.py`、WebFetch、Playwright/CDP、通用 Markdown 导入或
  uploader；某些已删除、受限或需付费的文章可能无法导入，应保留失败事实。

**注意事项**：
- 产出的 entry_type 是 `flink`（外部链接），而非 `page`（在线文档）
- flink 类型在乐享中以原始文章格式展示，支持全文检索和 AI 解析
- 微信公众号归档请求统一保留原生 `flink/wechat` 形态；即使提到在线查看或后续检索，
  也不能误判为需要 Markdown page
- 此分支不生成 `source.md`、`images/`、`meta.json`，不调用 `trans-doc-to-md` 或
  `upload-markdown-to-lexiang`

### 得到 APP 文章抓取（dedao.cn）

**核心问题**：得到 APP（`www.dedao.cn`）的文章内容是**付费内容 + SPA 动态渲染**，`web_fetch` 和 `fetch_article.py` 的通用提取逻辑都无法直接获取正文。

**技术原因**：
1. **SPA 架构**：得到网页版是 React SPA，文章正文通过 JS 异步渲染，`web_fetch` 只能拿到空白壳页面
2. **付费墙**：文章属于付费专栏内容，必须有已登录且已订阅的账号才能查看全文
3. **DOM 结构特殊**：课程页正文容器可能是 `.iget-articles`；分享包页（`/share/packet`）登录后的正文容器是 `.article-body`，外层 `.article` / `.main-content` 会混入标题栏和评论。`fetch_article.py` 对得到来源优先锁 `.article-body`，再回退 `.iget-articles`。标题、作者、发布日期取 `window.__INITIAL_STATE__.packetInfo` / `articleInfo.article.PublishTime`，不要用文内第一个 h1（那是小节标题）。未登录时 `packetInfo.has_authority=false`，正文只有约 20%，必须停下来等登录，不能把预览当全文。
4. **内容区混杂**：正文容器中混入了标题重复、音频时长、"划重点"、用户评论等非正文内容，需要清理

**抓取方案**：使用 **CDP 模式**连接 CDP Chrome（9222 端口）：

```bash
# 前提：CDP Chrome 在运行，且用户已在 CDP Chrome 窗口（非日常 Chrome）登录得到
curl -s http://127.0.0.1:9222/json/version   # 预检
~/.fetch_article/start-cdp-chrome.sh          # 若未运行
python scripts/fetch_article.py fetch "https://www.dedao.cn/course/article?id=<ID>" --output-dir <目录> --cdp
```

**付费墙时的做法**（与 SKILL「付费墙：停等登录」一致）：

页面出现「剩余 N%，继续学习」，或 `packetInfo.has_authority === false`，就停。登录框留在当前 CDP Chrome。等用户说登录完成，再对**原来的 URL** 抓一次。`fetch_article.py` 在墙还在时会以 `PAYWALL_LOGIN_REQUIRED` 退出，并且不写 `source.md`。

**已知限制**：
- **CDP 零标签页陷阱**（2026-07-07 修复）：CDP Chrome 所有 tab 关闭时 `connect_over_cdp` 失败；v2.8.3 起自动创建种子 tab。旧版会静默回退到 `Google Chrome for Testing`（无登录态）
- **CDP 连接失败**：`--cdp` 模式下 v2.8.3 起禁止回退到 Testing Chrome，应修复 CDP 环境（见 SKILL.md Step 0d）后重试
- 正文容器优先 `.article-body`，没有时再回退 `.iget-articles`。不要用更长的 `.main-content`，那里混有评论和页面外壳。

**内容清理要点**：
- 去掉正文开头的标题重复、日期、音频时长等元信息（通常在 `凡哥杂谈，你好` 或类似开场白之前）
- 去掉正文末尾的"划重点"、"添加到笔记"、"首次发布"、"用户留言"等非正文内容
- 如果是多篇系列文章（如上/下篇），合并时用 `## 上篇` / `## 下篇` 分隔
- 作者信息需要手动确认（通用提取器可能抓错）

**得到文章现行流程**：

1. 先看登录态。墙还在就停等，不要抓预览。用户确认登录后，再跑
   `fetch_article.py ... --cdp` 生成标准 `source.md`、`images/`、`meta.json`。
2. 不在抓取层删除图片或清洗正文；非中文或需复杂清洗时，将整个工作包交给
   `trans-doc-to-md` Prepared Markdown Package 模式。
3. 最终标题 Markdown 只交给 `upload-markdown-to-lexiang`，由 uploader 保持图片位置并
   渲染富元素。

**适用场景**：得到 APP 专栏文章（`www.dedao.cn/course/article?id=xxx`）和知识红包分享页（`www.dedao.cn/share/packet?packetId=...`）。分享页必须在 CDP Chrome 登录且 `has_authority=true` 后再抓。

### SPA 网站 Playwright 直接出 PDF（正文隔离方案）

**适用场景**：
- `fetch_article.py` 抓取后正文为空或极少（< 200 字符），说明网站是 SPA 动态渲染，通用 Markdown 提取器无法工作
- 批量抓取帮助中心/文档站（如 Guru help.getguru.com、readme.io 托管站、GitBook 等）
- 已知案例：`vcsmemo.com`（Nuxt.js SPA）、`help.getguru.com`（readme.io）

**核心方案**：用 Playwright 无头浏览器直接访问页面 → 等待 SPA 渲染完成 → 隔离正文区域 → `page.pdf()` 生成 PDF。

**关键步骤**：

#### 1. 加载与等待
```javascript
await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
await page.waitForTimeout(5000); // SPA 需要额外等待 JS 渲染
```

#### 2. 滚动触发懒加载图片
```javascript
await page.evaluate(async () => {
  const delay = (ms) => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < document.body.scrollHeight; i += 300) {
    window.scrollBy(0, 300);
    await delay(200);
  }
  window.scrollTo(0, 0);
});
await page.waitForTimeout(3000);
```

#### 3. 正文隔离（⚠️ 最关键的一步）

**问题**：直接 `page.pdf()` 会把整个页面打进 PDF，包括导航栏、侧边栏、相关推荐、页脚等非正文内容。**必须在生成 PDF 前隔离正文区域**。

**正文隔离策略（三步法）**：

**Step A：定位正文容器** — 找到包含文章核心段落的最小公共祖先节点
```javascript
// 用文章中的关键句子定位正文 <p> 标签
const articleParagraphs = [];
document.querySelectorAll("p").forEach(p => {
  if (p.textContent.includes("文章中的某段独特文字")) {
    articleParagraphs.push(p);
  }
});

// 计算所有正文段落的最小公共祖先
let commonAncestor = articleParagraphs[0];
for (let i = 1; i < articleParagraphs.length; i++) {
  // ... 向上遍历 DOM 树找公共祖先
}
```

**Step B：替换 body** — 将整个 `document.body` 的内容替换为正文容器的克隆
```javascript
const articleContent = commonAncestor.cloneNode(true);
document.body.innerHTML = "";
document.body.appendChild(articleContent);
```

**Step C：清理残余** — 从正文容器内部移除混入的非正文元素
```javascript
// 移除正文容器内可能混入的非内容元素
articleContent.querySelectorAll(
  '[class*="related"], [class*="sidebar"], [class*="comment"], ' +
  '[class*="share"], [class*="subscribe"], nav, header, footer'
).forEach(el => el.remove());

// 按文本内容移除（如"相关文章"、"登录"等中文导航项）
articleContent.querySelectorAll("*").forEach(el => {
  const t = el.textContent.trim();
  if (t === "相关文章" || t === "登录" || t.startsWith("Signal, not noise")) {
    const wrapper = el.closest("section, div, aside");
    wrapper ? wrapper.remove() : el.remove();
  }
});
```

#### 4. 样式优化
```javascript
articleContent.style.maxWidth = "750px";
articleContent.style.margin = "0 auto";
articleContent.style.padding = "30px 20px";
articleContent.style.fontSize = "15px";
articleContent.style.lineHeight = "1.8";

articleContent.querySelectorAll("img").forEach(img => {
  img.style.maxWidth = "100%";
  img.style.height = "auto";
});
```

#### 5. 生成 PDF
```javascript
await page.pdf({
  path: outputPath,
  format: "A4",
  printBackground: true,
  margin: { top: "15mm", bottom: "15mm", left: "15mm", right: "15mm" },
});
```

**常见需要移除的非正文元素**：

| 元素类型 | 典型选择器/文本 | 说明 |
|---------|---------------|------|
| 左侧导航 | `nav`, `[class*="sidebar"]`, 包含"首页/快讯/登录"等文本 | 网站主导航 |
| 右侧推荐 | `[class*="related"]`, 包含"相关文章"文本 | 相关文章推荐 |
| 顶部搜索 | `[class*="search"]`, `header` | 搜索栏和网站 header |
| 底部页脚 | `footer`, `[class*="footer"]` | 版权信息等 |
| 作者卡片 | `[class*="author-card"]`, 包含头像+简介的独立区块 | 如果在正文外部 |
| 订阅入口 | `[class*="subscribe"]`, `[class*="newsletter"]` | CTA 按钮 |

**调试技巧**：
- 在 `page.pdf()` 之前先 `page.screenshot({ path: "debug.png", fullPage: true })` 截图确认隔离效果
- 如果首次隔离不干净，根据截图调整选择器，迭代优化

**已验证的 SPA 网站**：

| 网站 | 框架 | 正文定位方式 |
|------|------|-------------|
| `vcsmemo.com` | Nuxt.js | 通过文章段落文本找公共祖先，class `left` 内的 `section` |
| `help.getguru.com` | readme.io | 移除 `.rm-Sidebar` + `nav` + `header` + `footer` |
| `dedao.cn` | React SPA | CDP 模式 + `.iget-articles` 专用选择器 |

### Substack 站点（如 lennysnewsletter.com）

`fetch_article.py` 对 Substack 托管站（`*.substack.com`、`a16z.news`、
`lennysnewsletter.com` 等）默认复用 **CDP Chrome profile**：
1. 每次先连接已配置端口（默认 9222，端口写在 `~/.fetch_article/cdp_port`）的现有
   Google Chrome 上下文；没有 page target 时创建种子 tab，再连接并复用。若 9222 被
   Ardot 等非 Google Chrome 进程占用，启动脚本自动选择 9223–9232 的空闲端口。
2. 不启动 `Google Chrome for Testing`，不另存一套 Playwright `storage_state`。
3. 公开且正文完整的文章无需登录；仅检测到付费墙或正文过短时才引导用户在 CDP Chrome 登录。
4. 转 Markdown 时过滤 `Discover more`、订阅组件、相关推荐、newsletter disclaimer
   及其图片；作者、发布日期优先读取 canonical meta、`time[datetime]` 和 JSON-LD。

```bash
python scripts/fetch_article.py login   # 首次在 CDP Chrome 登录，后续直接复用
```

**付费墙检测信号**：DOM `[data-testid="paywall"]` 或正文 `This post is for paid subscribers` / `This post is for paying subscribers` 时立刻停，即使预览已经超过 2000 字；较弱的 `Subscribe to read` / `Upgrade to paid` 只在正文过短时拦截，避免把免费文页脚订阅组件当成墙。不同站点结构不同，抓取不全时检查实际付费墙标识并更新检测逻辑。

### X.com / Twitter 帖子

分两种形态，**先判形态再选工具**：

**A. 普通推文 / 图文帖** —— 用通用抓取器 + CDP：

```bash
python scripts/fetch_article.py fetch "https://x.com/<user>/status/<id>" --output-dir <目录> --cdp
```

**B. 长文（Article / Long-form post）** —— 必须用专用抓取器：

```bash
python scripts/x_article_fetch.py "https://x.com/<user>/status/<id>" --output-dir <目录> --cdp-port <端口>
```

判断信号：页面存在 `[data-testid="twitter-article-title"]` 或 `[data-testid="longformRichTextComponent"]`。
`fetch_article.py` 对长文无效——它取到的 innerText 会把 85 个 Draft.js 块压成一行、标题退化成
`Conversation`、并混入 `Want to publish your own Article?` / `Upgrade to Premium` /
`Post your reply` 等按钮文案（详见 lessons-learned L052）。

`x_article_fetch.py` 直接解析 Draft.js 结构：

| DOM | 含义 |
|---|---|
| `[data-testid="twitter-article-title"]` | 文章标题 |
| `[data-testid="longformRichTextComponent"]` | 正文容器 |
| `div[data-block="true"].longform-unstyled` | 段落（整段加粗且 ≤80 字符 ⇒ `##` 小标题） |
| `…longform-unordered-list-item` | 无序列表项 |
| `[data-testid="twitterArticleReadView"] img[src*=pbs.twimg.com/media]` | 封面图（长文无正文插图） |

两种形态的共同前提：**CDP Chrome 必须带 X 登录态**（`auth_token` cookie）。X 对匿名/无登录
上下文会返回 `net::ERR_HTTP_RESPONSE_CODE_FAILURE`；脚本检测不到 `auth_token` 直接失败退出，
**禁止**改用匿名兜底或 WebFetch 取正文。

启动带登录态的 CDP Chrome（沿用 L051 做法，勿用 `~/.fetch_article/chrome_cdp_profile`，它没有登录态）：

```bash
SRC="$HOME/Library/Application Support/Google/Chrome"; DST="/tmp/cdp_profile_x"
rm -rf "$DST"; mkdir -p "$DST/Default"
cp "$SRC/Local State" "$DST/Local State"
for f in Cookies Cookies-journal Preferences "Login Data" "Web Data" "Secure Preferences"; do
  cp "$SRC/Default/$f" "$DST/Default/$f"; done
for d in "Local Storage" "Session Storage"; do cp -R "$SRC/Default/$d" "$DST/Default/$d"; done
nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9233 --user-data-dir="$DST" --no-first-run --no-default-browser-check \
  --headless=new --disable-gpu --disable-extensions --no-sandbox --disable-dev-shm-usage \
  --disable-software-rasterizer --in-process-gpu >/tmp/chrome_cdp_x.log 2>&1 & disown
# 轮询 http://127.0.0.1:9233/json/version 就绪后再抓取，两者必须在同一次命令里
```

抓取后清理 `pkill -f "user-data-dir=/tmp/cdp_profile_x"` + `rm -rf /tmp/cdp_profile_x`（约 57MB）。

X 长文只有 1 张封面图：正文里 `Caption: “…”` 这类图注可能指向 X 未渲染的插图，
抓不到就是抓不到，**不要**用封面图冒充插图或伪造图片。

X 的 `[[` 内联图片、转赞数等元信息由脚本写入 `meta.json`（`author` / `author_handle` /
`date` / `views`）。

### 微博帖子（必须 CDP）

微博强制登录（PC/移动/API 端口均是），`web_fetch` 和普通 Playwright 都会被重定向到 `Sina Visitor System`。**必须 CDP**：

```bash
python scripts/fetch_article.py fetch "https://weibo.com/<uid>/<mid>" --output-dir <目录> --cdp
```

| 坑 | 说明 |
|---|---|
| `web_fetch` 失败 | 被重定向到 `passport.weibo.com/visitor/visitor` |
| Playwright 失败 | 检测 HeadlessChrome UA，`--browser=chrome` 也被拦 |
| 内容整理 | 原始 HTML 含导航/按钮噪音，需清理为结构化 markdown |
| 标题 | 默认「微博正文 - 微博」，转存改为 `<作者>：<主题关键词>`（如 `唐杰THU：最近的一些想法`） |
| 图片 | `sinaimg.cn` CDN，部分需 Referer |

转存时生成标准工作包，最终 Markdown 统一交给 uploader；`file_create_hyperlink` 仅用于
支持的微信链接场景。

### web_fetch 获取的免费文章

通过 `web_fetch` 拿到完整内容的免费文章，**同样保存原文全文**（不总结/不摘要/不改写）：
生成标准 `source.md`、`meta.json` 和可选 `images/`，最终标题文件由编排流程生成。

> ⚠️ `web_fetch` 可能返回**总结版**而非全文。若内容明显被缩写（缺段落/引用/细节），调用时明确要求「返回完整原始全文，不要总结或缩写」。保存的必须是原文全文。

### Python 兼容性

脚本使用 `from __future__ import annotations` 以兼容 Python 3.9（`str | None` 联合类型语法在 3.9 中不可用）。

### Mintlify 文档站（docs.glean.com 等）

公开文档站，无需登录态，直连可达。用 CDP `fetch_article.py` 抓取即可，但抓取稿**必须**做清洗版工作包（详见 lessons-learned L065）：

| 现象 | 处理 |
|---|---|
| FAQ 折叠面板的问题标题被拍平，只剩答案 | 从 `curl -sL` 原始 HTML 按问题关键词恢复问题文本，写成 `####` 标题并与答案顺序对齐 |
| `noteUse these times...` / `warningUsage of Glean...` 标签粘连 | 还原成 `> [!note] Note / 注` / `> [!note] Warning / 警告`，英文行与中文行分开 |
| 标题尾部零宽字符 `\u200b`、章节间 `---` | 全部清除（L024） |
| 页尾 `© <年份> ...Was this page helpful?On this page- [...]` | 整段删除；同时删除与图片 alt 重复的图注行 |
| 首张图 alt=`banner` 的渐变装饰横幅 | 删除；正文截图保留 |
| 图片扩展名 `.webp` 但实际是 PNG 编码 | 用 `file` 核实后改名 `.png`，同步 `meta.json.verification.image_references` |
| 正文链接是 `/get-started/...` 相对路径 | 补全为 `https://docs.glean.com/...`，链接留在原句内（L057） |

页面日期取抓取器 `meta.json.date`（如 `2026-11-04`），文档站通常没有作者，不要编造。清洗版放新目录 `<slug>-YYYYMMDD-final`，随后 `bilingual_validate.py --profile generic --json` 必须 `ok=true` 才能上传。

### Glean 官方博客（www.glean.com/blog，Webflow）

公开博客，无需登录态，CDP 抓取即可。抓取稿必须做 `-final` 清洗版工作包（完整判据见 lessons-learned L067）：

| 现象 | 处理 |
|---|---|
| `.png` 文件头是 `<!DOCTYPE ht`、字节数等于 `curl` 的 HTML | 「HTML 假 png」，删；用 `file` 判定，不看扩展名 |
| alt=`CTA Section Background Shape` 的 AVIF 大图 | CTA 装饰，删；alt=`Product Illustration` 的正文示意图保留并逐张读图确认 |
| `.webp` 名但内容是 PNG | 统一改 `.png`，同步 `meta.json.verification.image_references` |
| `og:title` / `<title>` 是 SEO 标题，与正文 H1 不同 | `meta.title`、文件名、`display_title` 一律用正文 H1 |
| `5minutes read[作者\n\n职位](/authors/...)`、残缺 `Table of contents`、页尾 `Back to all stories` / `Get The Resource` / 空 `##` / `Work AI for all` | 全部删除；作者/日期改用 `<meta name="author">`、页面 `Last updated` + `og:publish_date` |
| `**Scholastic **serves` 粗体尾随空格 | 修成 `**Scholastic** serves`，否则乐享粗体序列化异常 |
| 同一引导段出现两份措辞略异的变体 | 先用原始 HTML 去标签计数确认是 CMS 自身重复；确认后**两份都保留**，不擅自删减 |
| 斜体图注与通用 alt 不重复、有信息量 | 保留并翻译（区别于 Mintlify 的重复图注） |

正文相对链接补 `https://www.glean.com` 前缀，链接留在原句内（L057）。

补充规律（2026-11-15 `waldo-launch`，详见 L068）：

| 现象 | 处理 |
|---|---|
| `Listen to article` 音频播放器 UI（常成对出现） | 整块删，不进正文 |
| byline 有多位作者（本次 4 位），`<meta name="author">` 只有第一位 | 取 byline 全量写入元信息行 |
| 图表 `alt` 与下方斜体图注逐字重复且很长 | 清洗版简化 alt，保留斜体图注原文并翻译 |
| 正文 H1 超长（136 字符） | `meta.title` / 文件名保留完整原题；只缩短 `display_title` 与 `--name`（L035） |
| 原文含 `~50%` / `~250 ms` 等近似值 | `source.md` 保留 `~`，双语稿统一改 `≈`，否则 `validate_no_unsafe_tildes` 失败 |

`Availability: ... will be deployed to customers soon.` 这类上线状态句属正文末句，必须保留。

### Glean Perspectives（www.glean.com/perspectives，Webflow 新模板）

与 `/blog/` 模板**不同**（详见 lessons-learned L069）。公开页面、CDP 抓取即可，但必须做 `-final` 清洗版工作包：

| 现象 | 处理 |
|---|---|
| 抓取稿出现 2 个 H1：首行是缺撇号的 SEO title，约第 20 行才是正文 H1 | 只保留正文 H1 作 `meta.title` / 文件名 / `display_title`；`og:title` 与 `<title>` 是 SEO 版，不采信 |
| 残缺且含 `#anchor` 的 `Table of contents`、`See how Glean works`、`11minutes read` | 整块删 |
| 页尾 `Back to Perspectives home` / `## Recent posts` 六张推荐卡（含多次 `No items found.`）/ `## Work AI that works.` / `Get a demo` / `Request a demo` | 全部删除 |
| 8 张下载图仅 2 张落盘，均为 PNG 编码的 `.webp` | hero 保留并改 `.png`；`CTA BG` 装饰图删除；同步 `meta.json.verification.image_references` |
| 正文 3 列 5 行表格 | 每单元格写成 `English<br>中文`（列数 ≤10），行数不超过乐享上限 |
| 5 个 FAQ 问题标题 | 保留，写成 `### English / 中文` |
| 原文用 `approximately` / `roughly` 表述数值，无裸 `~` | 不要套用 `/blog/` 的 `~`→`≈` 规则，`source.md` 与双语稿都保持原词 |

作者取 `<meta name="author">`（如 `The Glean Team`），日期取 `Last updated` + `og:publish_date`。`entry_list_children` 查重后上传；双语稿里英文源段**禁止混入 CJK**，否则 `bilingual_validate.py` 会报「缺少源文段落」（L069）。线上对账自检项见 L069。

补充规律（2026-11-15 `live-fall-25-agentic-engine2-performance`，`/blog/` 模板第三次复现，详见 L070）：

| 现象 | 处理 |
|---|---|
| 3 个 `.png` 字节数恰好等于 `curl` 原始 HTML（本次 624236），文件头 `<!DOCTYPE ht` | 按「字节数 == 原始 HTML」批量识别 HTML 假 png；同一假图常有多个序号且被引用多次，全部删净 |
| `<title>` 与正文 H1 相同（129 字符，含弯撇号） | 先比对再决定，不要机械套用「SEO title ≠ H1」；仍按 L035 只缩短展示名 |
| `<meta name="author">` 1 位 / 拍平 byline 4 位 / 文末 `Authors:` 行 8 位 | 三处都看，取最完整的一份（本次文末 8 位）；文末 Authors 行按原文保留并翻译 |
| `**Label: **` 粗体尾随空格（本次 12 处） | 用精确字符串替换，替换模板别多加冒号；修完 grep `::**` 复核（L070） |
| 7/8 张正文图 alt 为空，hero 的 alt 是完整 H1 | 清洗版补简短英文 alt；用 2×4 缩略拼图一次目视确认全部为正文图 |

### Glean 新闻稿（www.glean.com/press，第 4 种模板）

与 `/blog/`、`/perspectives/`、`docs.glean.com` 都不同（详见 lessons-learned L071）。公开页面、CDP 抓取即可，必须做 `-final` 清洗版：

| 现象 | 处理 |
|---|---|
| 原始 HTML 里 `Get The Resource` / `Listen to article` / `Recent posts` / `Table of contents` / `Work AI for all` 全为 0 | 据此判定是 `/press/` 模板，不要套用 `/blog/` 的噪音表；只需删 `See how Glean works`、抓取器元信息行、段首 `---`、零宽字符 |
| 双 H1：首行是带 `\| Glean Press` 后缀的 `<title>`，第 12 行才是正文 H1 | 去站点后缀，只保留正文 H1 作 `meta.title` / `source_title` / 文件名 / `display_title` |
| 无 byline、无 `<meta name="author">` | `author` 留空，双语稿元信息行不写作者，**不编造**；日期取 `Published ...` + 正文 dateline |
| `Learn More` / `About Glean` / `Connect with Us!` / `Contact` 固定尾部 | 属新闻稿正文，**保留并逐段翻译**，不要当 CTA 噪音删 |
| 8 个章节名是加粗伪标题（`**From Search to Agentic Action...**`） | 按 L011 提升为 `##`，双语稿写 `## English / 中文`；`Learn More:` 去掉尾部冒号 |
| `**About Glean\n\u200d**...` / `**Contact\n\u200d**...` 跨行粗体 | 先删 `\u200d`，再拆成 `## 标题` + 独立正文段 |
| `**Connect with Us!\xa0**[Blog](...)[LinkedIn](...)[Twitter X](...)` | 含 U+00A0 且链接粘连，精确拆成 `**Connect with Us!** [Blog](...) [LinkedIn](...) [Twitter X](...)` |
| `**Label: **` 粗体尾随空格（本次 8 处，含 dateline） | 按 L070 精确字符串替换，替换模板别多加冒号，修完 grep `::**` |
| 只有 2 张图：圆形品牌 logo + `Years from 1 to 200M ARR` 数据曲线图 | logo 连同下方单独一行 `Glean` 文字一起删；数据图保留、改 `.png`、简化 alt。图片少也要逐张目视 |

金额 `$200M` 等普通 `$` 不需要转义（dry-run `formulas: 0`），写 `\$` 反而会被双语校验拒绝。用户给「推算类洞察」（如 ARR 人效）时按 L071 的编排：标「笔记作者推算」+ 逐字引用原始数值 + 核对时点 + 给出数值边界（`more than 1,000` 是下界 ⇒ 20 万是上限）。


### Foundation Capital / Framer 生成站（foundationcapital.com/ideas/…）

2026-11-16 首次遇到（`context-graphs-ais-trillion-dollar-opportunity`），详见 lessons-learned **L072**。公开页面，CDP 抓取即可，但必须做 `-final` 清洗版；抓取器需已带 L072 的 `data-fetch-article-root` 两阶段锁定修复，否则正文为 0 字符。

| 现象 | 处理 |
|---|---|
| `curl` 原始 HTML 首行 `Made in Framer`，`data-framer-component-type` 出现 200+ 次；`article` / `main` / `.entry-content` / `[class*="body"]` 全不命中 | 提取阶段会回退 `document.body`；**必须**给回退节点也打 `data-fetch-article-root="1"`，转换阶段优先复用该节点。别用 `--no-cdp` 或反复重抓来绕过 |
| 双 H1：首行是带 ` - Foundation Capital` 后缀的 `<title>`（与 `og:title` 相同），约第 16 行才是正文 H1 | 去站点后缀，只保留正文 H1 作 `meta.title` / `source_title` / 文件名 / `display_title`（本次 45 字符，加中文 67 < 150，无需按 L035 缩短） |
| 无 `<meta name="author">`；byline 是两个 `../team-members/...` 链接，页面另有重复作者卡 | 作者取 byline（Jaya Gupta, Ashu Garg）；日期取 `<time datetime="...">Dec 22, 2025</time>` + `Posted`；`12 MIN READ` 是 JS 估算，原始 HTML 为 `0 MIN READ` 占位，不要当权威元数据 |
| `AIENTERPRISEThe last generation...` 分类标签粘在首段段首 | 剥掉标签，写入顶部元信息行（`分类: AI · Enterprise`），正文首段从 `The last generation` 起 |
| `#### About Ashu` 作者卡（`Secondary Content / Content` + 头像）、`### Get insights directly to your inbox.`、`## Get insights directly to your inbox.` | 都是 Framer 侧栏 / newsletter CTA，整块删除；**不要**套用 L071「About Glean 属新闻稿正文」的结论 |
| `#### The compounding asset enterprise software never had` + `Ashu Garg, Jaya Gupta` + 摘要 + `Read the article` + 一张飞轮图 | 是 `Get the full report / Text & CTA` 相关文章导流卡（另一篇文章的推广），整块删除；缩略图虽与本文主题相关，也不是正文配图 |
| 页脚两处办公地址（含 U+00A0）、`Work at our companies`、`Terms of Use`、`Privacy Policy`、`© Foundation Capital 2026`、`Cookie Settings`、reCAPTCHA 链接、`framer.com/edit?framerSiteId=...` | 全部删除；抓取器元信息行与段首 `---` 按 L024 一并删 |
| 3 张图：hero 真 JPEG 2560×1440（alt 只是署名 `Trey Holterman…`）、作者头像 443×443、导流卡缩略图 439×439 | 逐张目视；只留 hero 并补描述性 alt（保留原署名作 credit）；另两张随卡片删除，同步 `meta.json.verification.image_references` |
| `**the decision traces **-`、`**Incumbents will fight back. **` 粗体尾随空格 | 按 L070 用精确字符串替换；修完 grep `::**` 复核 |
| 6 个独立成段的加粗伪标题 | 按 L011 提升为 `###`，**清洗版 `source.md` 与双语稿同步提升**，双语写 `### English / 中文`；否则 `_paragraphs` 会误报源文段落缺失 |
| 正文链接带长串广告追踪参数（如 PlayerZero 的 `?matchtype=&utm_...&gad_...`） | URL 简化为站点根地址；`_normalize` 只取链接锚文本，不影响双语对账 |
| 用户未给「核心洞察」 | 按 L066 不编造 `Key Takeaways`，只做逐段中英对照归档 |

**装配与对账（本次新增硬规则）**：双语 bullet 必须写成 `- English / 中文`（保留 `- ` 前缀）；装配脚本写成 `en[2:] + " / " + cjk` 会丢前缀，导致线上 4 个 bullet 合并成一个 `p` 块，而 `bilingual_validate.py` 与 `--dry-run` 都会**假阴性通过**（校验器只检查匹配 `- ` 的行，一行都没有就当通过）。上传前后必须额外对账 `grep -c '^- ' 本地` == 线上 `bulleted_list` 块数。已上传页面要修复时用 `upload ... --entry-id <entry_id>` 原地清空重写（返回 `action: updated`），不要 create 出重复条目。
