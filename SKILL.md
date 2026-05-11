---
name: fetch-archive-to-lexiang
description: 通用文章抓取与归档工具。抓取任意 URL（免费/付费/登录墙）的文章全文，转换为结构化 Markdown，并可选转存到乐享知识库。支持 Substack、Medium、知识星球等付费平台的登录态管理。支持 YouTube 视频下载（yt-dlp）、播客音频下载（小宇宙FM等）、音频转录（Whisper）、翻译（中英对照格式），并将音视频和文字稿上传乐享知识库（文字稿使用在线文档格式，支持按块编辑）。关键词触发：抓取文章、获取全文、付费文章、转存知识库、乐享、保存原文、fetch article、归档、YouTube、视频转录、字幕提取、视频下载、播客、podcast、小宇宙、xiaoyuzhou。
---

# 抓取链接内容 & 转存知识库

> **🎬 视频/音频上传到乐享**：必须用 `scripts/upload_video_via_openapi.py`（走 OpenAPI `/cgi-bin/v1/kb/files/upload-params`）。**不要**用 MCP 的 `file_apply_upload` 或 `docs/cos-param`——它们产出 `entry_type=file` 的条目，不触发 VOD 转码，视频无法播放。详见下方「YouTube 视频处理 → Step 2：上传到乐享知识库」章节。凭证存放于 `~/.lexiang/openapi.json`（不进 git）。

## 概述

将文章 URL（免费/付费/登录墙）抓取为结构化 Markdown，并自动转存到乐享知识库，实现素材归档和可追溯。

### 最终产出物
1. `<项目子目录>/<原文标题>.md` — 完整文章 Markdown（含图片引用）
2. `<项目子目录>/<原文标题>_meta.json` — 结构化元信息（原文链接、作者、发布时间、抓取时间等）
3. `<项目子目录>/images/` — 所有文章配图
4. 乐享知识库中的文档副本（按天维度归档）

### 文件命名规则（重要）

- **必须使用原文标题命名**，不要用 `article.md` 等通用名称
- 文件名格式：`<原文标题>.md`、`<原文标题>_meta.json`
- 示例：`How Notion uses Custom Agents.md`、`How Notion uses Custom Agents_meta.json`
- 如果标题中包含文件名不合法字符（`/`、`\`、`:`等），替换为 `-`
- 乐享知识库转存时也使用原文标题作为文档标题

## 工作流程

### Step 1：素材收集

#### 抓取方式决策树

根据 URL 类型选择抓取方式（按优先级排列）：

1. **微信公众号文章**（`mp.weixin.qq.com`）→ **优先使用乐享 MCP `file_create_hyperlink`**（一步到位，后端自动抓取图文+OCR），详见下方「微信公众号文章处理」章节。降级方案：`fetch_article.py`
2. **YouTube 视频** → 使用 `yt_download_transcribe.py`（yt-dlp 下载 + Whisper 转录 + AI 翻译），详见下方「YouTube 视频处理」章节
3. **播客音频**（小宇宙 `xiaoyuzhoufm.com`、Apple Podcasts 等）→ yt-dlp 下载音频 + Whisper 转录，详见下方「播客音频处理」章节
4. **付费/登录墙文章** → 用 `fetch_article.py`（Cookie 注入或 CDP 模式）
5. **免费图文文章**（正文含图片/截图/图表）→ **必须**用 `fetch_article.py`（`web_fetch` 只能返回文本，无法提取和下载页面中的图片）
6. **免费纯文字文章**（正文无配图）→ 可用 `web_fetch`，内容不完整时切换 `fetch_article.py`
7. **SPA 动态渲染网站**（`fetch_article.py` 抓取正文为空或极少）→ **Playwright 直接生成 PDF**，详见下方「SPA 网站 Playwright 直接出 PDF」章节
8. **批量抓取帮助中心/文档站**（如 readme.io、GitBook、Guru 等）→ Playwright 直接生成 PDF，详见下方「SPA 网站 Playwright 直接出 PDF」章节
9. **文字观点** → 直接整理
10. **图片素材** → 分析图片内容

> **⚠️ 关键原则**：`web_fetch` 工具**只能返回文本内容，无法提取和下载页面中的图片**。任何包含图片、截图、图表的文章，都**必须**使用 `fetch_article.py` 抓取，否则图片信息会完全丢失。当不确定文章是否含图时，**默认用 `fetch_article.py`**。
>
> **⚠️ SPA 降级原则**：如果 `fetch_article.py` 抓取后正文内容极少（< 200 字符），说明该网站是 SPA 动态渲染，通用内容提取器无法工作。此时应切换到 **Playwright 直接生成 PDF** 方案。

#### 付费/登录墙文章获取

适用于**所有需要登录态才能查看全文的网站**（Substack 付费订阅、Medium 会员、知识星球、财新网、The Information 等），使用 `fetch_article.py` 脚本：

```bash
# Cookie 注入模式（默认，适用于大部分站点）
python scripts/fetch_article.py fetch <URL> --output-dir <项目子目录>

# CDP 模式（适用于 Cloudflare 保护站点、需要 Google 账号登录的站点）
python scripts/fetch_article.py fetch <URL> --output-dir <项目子目录> --cdp
```

**两种浏览器模式**：

| 模式 | 参数 | 原理 | 适用场景 |
|------|------|------|----------|
| Cookie 注入 | （默认） | 从 Chrome Cookie DB 提取 cookies → 注入 Playwright 浏览器 | Medium 等大部分站点 |
| **CDP** | `--cdp` | 通过 Chrome DevTools Protocol 连接用户真实 Chrome（port 9222），复用完整登录态 | **Substack（自动启用）**、OpenAI、Cloudflare 保护站点、LinkedIn、Google 系网站等 |

> **自动升级到 CDP 模式的场景**：
> 1. **Substack 站点**（所有 `*.substack.com` 及已知自定义域名）：自动使用 CDP 模式，并在抓取前**校验登录态**。未登录时会暂停提示用户在 Chrome 中登录，验证通过后才继续抓取。
> 2. **Cloudflare 保护站点**（如 openai.com）：自动切换 CDP 模式，等待 JS challenge 通过。
> 3. 手动指定 `--cdp` 参数。

**CDP 模式前置条件**：确保 Chrome 浏览器已开启 CDP 远程调试端口：
```bash
# 方式1（推荐）：直接用带 CDP 的方式启动 Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

# 方式2：如果 Chrome 已在运行，需要先关闭再以 CDP 模式重启
# 脚本会自动尝试此操作，但可能需要用户手动确认
```

> **⚠️ CDP 独立 profile 的已知限制**：
> 
> 脚本会使用独立的 CDP profile 目录（`~/.fetch_article/chrome_cdp_profile`），虽然会自动复制 Cookies 文件，但**以下登录态信息不会被同步**：
> - `localStorage`（Substack 等 SPA 站点的会话 token）
> - `Service Worker` 缓存
> - `sessionStorage`
>
> **实际影响**：对于 Substack 等依赖 localStorage 的站点，仅靠 Cookies 复制可能无法完全还原登录态。脚本已通过 **Substack 登录态缓存**机制（`~/.substack/storage_state.json`）弥补此限制——首次登录后会保存完整的 Playwright storage state（含 Cookies + localStorage），后续抓取直接复用。
>
> **最佳实践**：
> 1. **首次使用 Substack 前**，先运行 `python scripts/fetch_article.py login` 完成登录并缓存
> 2. 如果 CDP 模式下登录态校验失败，脚本会自动暂停并引导用户在弹出的 Chrome 窗口中登录
> 3. 登录成功后会自动刷新缓存，后续抓取无需重复登录

**工作原理**：
1. 自动从 Chrome 浏览器的 Cookie 数据库提取目标域名的登录 cookies
2. 将 cookies 注入 Playwright 浏览器上下文
3. 加载页面，自动检测并等待 Cloudflare challenge 通过（如有）
4. 滚动加载懒加载内容、下载所有图片
5. **自动格式转换**：检测下载图片的真实格式（WebP/SVG 伪装成 .png/.jpg 很常见），自动转为真正的 PNG 以确保 PDF 生成和文档嵌入兼容
6. 将正文转换为 Markdown（`article.md`），图片保存到 `images/` 子目录
7. 内容提取时自动选择**最长的内容容器**（避免只抓到免费预览区域）

**标题提取增强**（多策略回退）：
1. CSS 选择器优先级：`h1.post-title` > `article h1` > `[class*="title"] h1` > `h1`
2. 回退到 `<meta property="og:title">` → `<meta name="title">` → `document.title`
3. 自动清理标题中的网站后缀（如 `" - Cursor"`、`" | Substack"`）
4. 正文中与已提取标题相同的第一个 `<h1>` 会被自动去重，避免 MD 中标题重复

**作者提取增强**：
- CSS 选择器 + `meta[name="author"]` + `[rel="author"]` + `meta[property="article:author"]` 多策略回退

**微信公众号文章（mp.weixin.qq.com）专项优化**：
脚本对微信公众号文章有专门的检测和处理策略：

1. **自动检测**：识别 `mp.weixin.qq.com` 域名，自动启用微信模式
2. **无需登录**：微信公众号文章是公开可读的，跳过登录检测和 Cookie 注入流程
3. **专用内容选择器**：使用 `#js_content` / `.rich_media_content` 精准定位正文区域（而非通用选择器可能匹配到页面其他内容）
4. **标题提取**：`#activity-name` > `h1.rich_media_title` > 通用 h1 > meta 标签回退
5. **作者提取**：`#js_name`（公众号名称）> `.rich_media_meta_nickname` > 通用选择器回退
6. **日期提取**：`#publish_time` > 通用 time/date 选择器回退
7. **图片懒加载增强**：
   - 微信图片使用 `data-src` + IntersectionObserver 懒加载
   - 滚动速度放慢（300px 步长、200ms 间隔）以确保触发所有 IntersectionObserver
   - 强制将未触发的 `data-src` 复制到 `src`（兜底策略）
   - 图片下载时优先使用 `data-src` 的高清原图 URL
8. **图片格式识别**：微信图片 URL 格式特殊（`mmbiz.qpic.cn/...?wx_fmt=png`），从 `wx_fmt` 查询参数推断文件扩展名
9. **Referer 防盗链**：通过 Playwright 页面上下文的 `page.request.get()` 下载图片，自动携带正确的 Referer 头

**Substack 站点（如 www.lennysnewsletter.com）专项优化**：
脚本对 Substack 托管的站点（`*.substack.com`、`lennysnewsletter.com` 等）有专门的登录检测和**登录态缓存**机制：

1. **登录态缓存**：登录成功后自动保存 Playwright `storage_state` 到 `~/.substack/storage_state.json`，后续抓取直接复用，**无需重复登录和邮箱验证**
2. **优先级**：缓存 `storage_state` > Chrome cookies > 引导登录
3. **自动检测登录状态**：加载页面后检查右上角是否有用户头像（已登录）还是 "Sign in" 按钮（未登录）
4. **已登录** → 直接抓取全文，并刷新缓存延长有效期
5. **缓存过期** → 自动清理旧缓存，进入引导登录流程
6. **未登录** → 打开可见浏览器窗口引导登录，用户在终端输入 `y` 确认后二次验证，通过后自动缓存

**独立登录命令**（推荐首次使用时先执行）：
```bash
python scripts/fetch_article.py login
```
此命令单独完成 Substack 登录并缓存，不需要指定文章 URL。后续所有 Substack 文章抓取都会自动复用此登录态。

**非 Substack 站点的登录确认机制**：
- 无 Chrome cookies 时自动切换到非无头模式，打开可见浏览器窗口
- 终端提示用户完成登录操作后**按回车键**继续
- 收到确认信号后重新加载页面并检测付费墙状态

**付费墙检测**：脚本同时检测以下信号：
- DOM 元素：`[data-testid="paywall"]`、`.paywall`
- 文本关键词：`This post is for paid subscribers`、`Subscribe to read`、`Upgrade to paid` 等
- 注意：不同网站的付费墙 DOM 结构和关键词不同，如遇新网站抓取不完整，需检查页面实际的付费墙标识并更新检测逻辑

**判断内容是否完整的方法**：
- 先用 `web_fetch` 尝试获取，如果明显被截断（内容不完整、出现付费提示），则切换到 `fetch_article.py`
- 抓取完成后**必须**告知用户查看 `article.md` 确认内容完整性
- 关注文章末尾是否有作者署名/总结段落作为完整性标志
- 如果用户反馈内容不完整，检查：(1) 登录账号是否有付费权限 (2) 页面是否有懒加载内容未触发 (3) 内容选择器是否匹配到了免费预览区而非全文区

**产出物**：
- `<项目子目录>/<原文标题>.md` — 完整文章 Markdown（含图片引用）
- `<项目子目录>/<原文标题>_meta.json` — 结构化元信息（原文链接、作者、发布时间、抓取时间等）
- `<项目子目录>/images/` — 所有文章配图

`<原文标题>_meta.json` 格式：
```json
{
  "url": "原文链接",
  "title": "文章标题",
  "subtitle": "副标题",
  "author": "作者",
  "date": "发布时间",
  "content_length": 12345,
  "image_count": 5,
  "images": ["images/img_01_xxx.png", ...],
  "fetched_at": "2026-02-25T10:30:00"
}
```

#### X.com / Twitter 帖子抓取（必须用 CDP 模式）

**X.com 是登录墙网站的典型代表**，`web_fetch` 和普通 Cookie 注入模式都无法抓取，**必须使用 CDP 模式**：

```bash
# CDP 模式（必须）
python scripts/fetch_article.py fetch "https://x.com/<username>/status/<id>" --output-dir <项目子目录> --cdp
```

**CDP 模式工作原理**：
1. 通过 Chrome DevTools Protocol (port 9222) 连接用户真实 Chrome 浏览器
2. 复用浏览器中已登录的 X 账号会话
3. 绕过自动化浏览器检测（X 会检测并阻止 Playwright/Selenium）

**CDP 模式前置条件**：
```bash
# 启动 Chrome 并开启 CDP 端口
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

# 验证
curl -s http://localhost:9222/json/version
```

**X.com 抓取的特殊处理**：
1. 帖子内容会转换为 Markdown 格式
2. 图片（帖子中的媒体）会下载到 `images/` 目录
3. 帖子中的链接会转换为 Markdown 链接格式
4. 转发数、点赞数等元信息会保留

**产出物**：
- `<项目子目录>/<原文标题>.md` — 帖子 Markdown
- `<项目子目录>/<原文标题>_meta.json` — 元信息
- `<项目子目录>/images/` — 帖子中的媒体图片

#### 英文文章翻译为中英对照

对于英文文章（如 X 帖子、英文博客等），可以使用 OpenAI API 翻译为中英对照格式：

**翻译脚本** (`scripts/translate_article.py`)：

```bash
python scripts/translate_article.py <原文.md> <输出.md> --model gpt-4o-mini
```

**翻译格式**：
```markdown
## 英文标题

[英文原文段落]

[中文翻译]

## 第二节英文标题

[英文原文...]

[中文翻译...]
```

**翻译工作流**：
1. 先用 `fetch_article.py` 抓取原文
2. 用 `translate_article.py` 翻译为中英对照
3. 将翻译后的 Markdown 上传到乐享知识库

**依赖**：
- `OPENAI_API_KEY` 环境变量

#### 使用 `web_fetch` 获取的免费文章

对于通过 `web_fetch` 获取到完整内容的免费文章，**同样需要保存原文**：
1. **保存原文全文**：将 `web_fetch` 返回的内容直接保存为 Markdown，**不做总结、不做摘要、不做改写**，保持原文的完整结构和措辞
2. 文件名使用原文标题：`<项目子目录>/<原文标题>.md`
3. 手动构建 `<原文标题>_meta.json`，包含 URL、标题、作者、日期等元信息
4. 如果文章包含图片，尽量下载保存到 `<项目子目录>/images/`

> **关键区分**：`web_fetch` 工具可能会返回总结/摘要版本而非原文全文。如果返回的内容明显是总结（缺少原始段落、引用、细节），需要在 `web_fetch` 调用时明确要求"返回完整原始全文内容，不要总结或缩写"。保存到本地的**必须是原文全文**，而不是经过 AI 总结的摘要。

#### YouTube 视频处理（yt-dlp + Whisper + 翻译 + 乐享）

**当用户提供 YouTube 视频链接时**，使用 `yt_download_transcribe.py` 脚本完成完整的下载-转录-翻译-归档工作流。

**⚠️ 重要**：**不要**使用 `web_fetch`（无法获取视频内容），**不要**使用 NotebookLM（已替换为本地 Whisper 方案，速度更快、无外部依赖）。

**工作流概述**：
1. **yt-dlp 下载视频** → 本地 `.mp4` 文件
2. **ffmpeg 提取音频** → WAV 格式（16kHz 单声道）
3. **Whisper 转录** → 带时间戳的文字稿
4. **AI 翻译**（如果是英文）→ 中英对照格式的 Markdown
5. **上传乐享知识库**：
   - 文字稿：**以在线文档（page）格式上传**，支持后续按块维度编辑更新
   - 视频文件：以文件（file）格式上传
6. **清理**：上传成功后删除本地视频文件

**Step 1：下载 + 转录 + 翻译**

```bash
cd <项目子目录>

# 完整流程（下载 + 转录 + 翻译）
python3 scripts/yt_download_transcribe.py "<YouTube URL>" \
  --output-dir . \
  --whisper-model base

# 常用参数：
#   --whisper-model tiny|base|small|medium|large  转录模型（越大越准但越慢）
#   --skip-download    跳过下载（用于重新转录已下载的视频）
#   --skip-translate   跳过翻译步骤
#   --keep-audio       保留提取的音频文件
```

**产出物**：
- `<视频标题>.mp4` — 下载的视频文件
- `<视频标题>.md` — 文字稿 Markdown（英文视频为中英对照格式）
- `<视频标题>_meta.json` — 视频元信息

**文字稿格式**（英文视频，中英对照）：

```markdown
# 视频标题

**频道**: xxx
**发布日期**: 2026-03-10
**时长**: 15:30
**原始链接**: https://www.youtube.com/watch?v=xxx
**转录语言**: en

---

## 文字稿（中英对照）

> 以下内容采用「英文原文 + 中文翻译」对照排列。

**[00:00]**

This is the original English text from the video...

这是视频中的中文翻译文本...

**[01:23]**

Next paragraph of English text...

下一段中文翻译...
```

**Whisper 模型选择建议**：

| 模型 | 速度 | 精度 | 适用场景 |
|------|------|------|---------|
| `tiny` | 最快 | 较低 | 快速预览、非关键内容 |
| `base` | 快 | 中等 | **默认推荐**，适合大部分场景 |
| `small` | 中等 | 较高 | 口音较重、背景噪音较多 |
| `medium` | 慢 | 高 | 重要内容、需要高精度 |
| `large` | 最慢 | 最高 | 专业内容、学术演讲 |

**Step 2：上传到乐享知识库**

> 通过 lexiang MCP 工具完成上传，流程与 Step 2（普通文章转存乐享）一致。**前提是 lexiang MCP 已连接**（参见 Step 2 的「乐享 MCP 工具的调用方式」章节）。

**文字稿上传**（在线文档 page 类型）：
1. 获取知识库根节点 → 检查/创建日期目录（同上述步骤 1-3）
2. 调用 `entry_import_content`（参数：`space_id`, `parent_id=<日期目录ID>`, `name="<视频标题>"`, `content=<文字稿Markdown内容>`, `content_type="markdown"`）
3. 在线文档支持后续在乐享中按块维度编辑更新（如修正翻译）

**视频文件上传**（🚨 推荐使用 OpenAPI 路径，MCP 的 `file_apply_upload` 产生不可播放的 file 条目）：

```bash
# ✅ 推荐：通过 OpenAPI 上传，产生 entry_type=video，乐享会 VOD 转码，真能播放
python3 scripts/upload_video_via_openapi.py "<视频路径>.mp4" \
    --space-id <space_id> \
    --parent-entry-id <父节点 entry_id> \
    --media-type video
```

需要在 `~/.lexiang/openapi.json` 配置 AppKey/AppSecret/StaffID（**不入 git**）。

OpenAPI 正确流程（脚本已封装）：
1. `POST /cgi-bin/v1/kb/files/upload-params`（body: `{"name":"xxx.mp4","media_type":"video"}`）→ 获取 VOD 上传签名 + state
2. `PUT <bucket>.cos.<region>.myqcloud.com/<key>` → 上传到 VOD COS
3. `POST /cgi-bin/v1/kb/entries?space_id=xxx&state=xxx`（body: `entry_type=video, name=xxx.mp4`）→ 创建可播放视频节点

**🚨 关键踩坑（2026-05-03 实战总结）**：
- ❌ 不要用 MCP 的 `file_apply_upload`——产物是 `entry_type=file + extension=video`，不触发 VOD 转码，**视频无法播放**
- ❌ 不要用 `/cgi-bin/v1/docs/cos-param` 签名接口——它只支持 `attachment/file`，签发的 state 不能用于创建 entry_type=video
- ✅ **必须用 `/cgi-bin/v1/kb/files/upload-params`**——支持 `media_type=video/audio/file`，签发的 state 可用于 `kb/entries`
- ✅ `name` 参数**必须带文件后缀**（`.mp4` 等），否则报"name 需指定文件后缀"
- ✅ `kb/entries` 接口用 **`x-staff-id`**（小写带连字符），不是 `StaffID`

**备用：MCP 三步流程（仅适用于非视频文件，如 PDF）**：
1. `file_apply_upload`（参数：`parent_entry_id=<日期目录ID>`, `name="<文件名>.pdf"`, `size=<文件字节数>`, `mime_type="application/pdf"`, `upload_type="PRE_SIGNED_URL"`）
2. `curl -X PUT "<upload_url>" -H "Content-Type: application/pdf" --data-binary "@<文件路径>"`
3. `file_commit_upload`（参数：`session_id=<上一步返回的session_id>`）

**上传成功后**：自动删除本地视频文件（`rm -f <视频文件路径>`），节省磁盘空间。

**依赖**：
- `yt-dlp`（**推荐 `brew install yt-dlp`**，不要用 `pip3 install`）— YouTube 视频下载。必须用 brew 安装以获取最新版本，pip 版本受限于系统 Python 版本（如 Python 3.9 无法安装 nightly 版），而 brew 版自带独立 Python 环境
- `openai-whisper`（`pip3 install openai-whisper`）— 音频转录
- `ffmpeg`（`brew install ffmpeg`）— 音频提取
- `openai`（`pip3 install openai`）— 翻译（需要 `OPENAI_API_KEY` 环境变量）。**如果没有 API Key，可以跳过翻译步骤，由 AI 助手直接在对话中翻译后更新文档**

#### 播客音频处理（yt-dlp + Whisper + 乐享）

**当用户提供播客链接时**（小宇宙FM `xiaoyuzhoufm.com`、Apple Podcasts 等），使用 yt-dlp 下载音频 + Whisper 转录的方式处理。

**⚠️ 重要**：yt-dlp 的 generic extractor 可以从播客页面中自动提取音频 URL（m4a/mp3），**不需要** cookies，也**不需要**专门的播客 extractor。

**工作流概述**：
1. **yt-dlp 下载音频** → 本地 `.m4a` 或 `.mp3` 文件（播客没有视频，直接是音频）
2. **ffmpeg 提取/转换音频** → WAV 格式（16kHz 单声道，Whisper 推荐）
3. **Whisper 转录** → 带时间戳的文字稿
4. **繁简转换**（如需要）→ Whisper base 模型对中文会输出繁体，需用 `opencc` 转为简体
5. **上传乐享知识库**（通过 lexiang MCP 工具）：
   - 文字稿：`entry_import_content` 创建为在线文档（page）格式
   - 音频文件：`file_apply_upload` → `curl PUT` → `file_commit_upload` 三步上传

**Step 1：下载音频**

```bash
cd <项目子目录>

# yt-dlp 直接下载播客音频（不需要 cookies）
yt-dlp --no-playlist -o "%(title)s.%(ext)s" "<播客链接>"
```

> **小宇宙链接格式**：`https://www.xiaoyuzhoufm.com/episode/<episode_id>`
> yt-dlp 会通过 generic extractor 自动从页面中提取 `media.xyzcdn.net` 的音频直链。

**Step 2：提取 WAV + Whisper 转录**

```bash
# 提取 WAV（16kHz 单声道）
ffmpeg -i "<音频文件>.m4a" -vn -acodec pcm_s16le -ar 16000 -ac 1 -y "<音频文件>.wav"

# Whisper 转录（中文播客指定 language=zh）
python3 -c "
import whisper, json, time
model = whisper.load_model('base')
result = model.transcribe('<音频文件>.wav', language='zh', verbose=False)
with open('whisper_segments.json', 'w', encoding='utf-8') as f:
    json.dump(result['segments'], f, ensure_ascii=False, indent=2)
print(f'Done: {len(result[\"segments\"])} segments')
"
```

**Step 3：合并段落 + 繁简转换 + 生成 Markdown**

使用与 YouTube 视频相同的段落合并逻辑（max_gap=1.5s, max_duration=30s，遇句末标点+gap>0.8s 断开）。

**关键**：Whisper base 模型对中文普通话倾向输出繁体字，必须用 `opencc` 进行繁简转换：
```bash
pip3 install opencc-python-reimplemented
```

```python
import opencc
converter = opencc.OpenCC("t2s")
simplified_text = converter.convert(traditional_text)
```

**文字稿 Markdown 格式**（中文播客）：
```markdown
# 播客标题

> 播客：节目名 | 平台：小宇宙FM
> 嘉宾：xxx | 主播：xxx
> 发布日期：YYYY-MM-DD | 时长：xx分xx秒
> 原始链接：https://www.xiaoyuzhoufm.com/episode/xxx
> 转录工具：Whisper base + OpenCC 繁简转换

---

## Part 1：章节标题

**[00:00]** 第一段转录文本，由多个 Whisper segment 合并而成...

**[01:23]** 第二段转录文本...

## Part 2：章节标题

**[15:30]** 第三段转录文本...
```

**文字稿整理规范（🚨 必须遵守，避免格式混乱）**：

> **核心原则**：Whisper 输出的 segments 是细碎的短句（通常每条1-5秒），必须**先合并为自然段落**，再插入章节标题和时间戳。直接按 segment 粒度插入标题会导致同一个标题在每个短句前重复出现。

**段落合并策略**：

> **🚨 关键 bug 修复（2026-05-08）**：Whisper base 对中文输出几乎没有句号等标点，因此"句末标点断开"条件基本不会触发。**唯一有效的断开条件是 duration 和 gap**。必须确保 duration 计算正确：`duration = 当前 segment 的 end - 段落起始 cur_start`。

1. 相邻 segment 间隔 > 1.0s → **强制断开**
2. 累计时长 > 15s（`seg.end - cur_start > 15`）→ **强制断开**
3. 遇到句号、问号等句末标点 + gap > 0.5s → 断开为新段落
4. 合并后的段落开头标注时间戳 `**[MM:SS]**`

**⚠️ 参数选择依据**：
- `max_duration=15s` 而非 30s/60s：因为中文 Whisper 没有标点输出，只能靠 duration 强制切割。15s 约 200 字/段，阅读体验较好
- `max_gap=1.0s`：对话中的自然停顿通常 > 1s
- 目标：48 分钟播客应产出 150-200 段（平均 90-100 字/段）

**合并代码参考**：
```python
paragraphs = []
cur_text = ""
cur_start = 0
cur_end = 0

for seg in segments:
    start, end, text = seg["start"], seg["end"], seg["text"].strip()
    if not text:
        continue
    if cur_text:
        gap = start - cur_end
        duration = end - cur_start  # ⚠️ 必须用 end 而非 cur_end
        if duration > 15 or gap > 1.0:
            paragraphs.append({"start": cur_start, "end": cur_end, "text": cur_text.strip()})
            cur_text, cur_start, cur_end = text, start, end
        else:
            cur_text += text
            cur_end = end
    else:
        cur_text, cur_start, cur_end = text, start, end
if cur_text:
    paragraphs.append({"start": cur_start, "end": cur_end, "text": cur_text.strip()})
```

**章节标题插入策略（🚨 关键，避免重复）**：
1. 从播客简介/shownotes 中提取章节时间线
2. 将章节时间点转换为秒数，建立映射
3. **每个标题只插入一次**：用 `inserted_headers = set()` 跟踪已插入的标题
4. 在段落合并**完成后**，根据段落起始时间匹配最近的章节标题
5. 匹配条件：`段落起始时间 >= 章节时间点` 且 `该标题尚未插入`

**常见错误（必须避免）**：
- ❌ 在每个 Whisper segment 级别插入章节标题 → 同一标题重复几十次
- ❌ 用宽松时间容差匹配（如 `abs(start - ts) < 5`）→ 多个 segment 命中同一标题
- ❌ 不跟踪已插入状态 → 标题被重复插入
- ✅ 先合并 segments 为段落，再在段落级别插入标题，每个标题只插入一次

**Step 4：上传到乐享知识库**

与 YouTube 视频处理相同的流程（通过 lexiang MCP 工具完成，**前提是 MCP 已连接**）：
1. 获取知识库根节点 → 检查/创建日期目录
2. 文字稿使用 `entry_import_content_to_entry` 创建为**在线文档（page 类型）**，**不要**直接上传 .md 文件（排版会乱，用户无法正常阅读）
3. 音频文件**必须**使用 `upload_video_via_openapi.py --media-type audio`（走 OpenAPI VOD 路径），**不要**用 MCP 的 `file_apply_upload`（产生 entry_type=file，无法在线播放）

**文字稿在线文档导入方法（🚨 分块导入，避免内容丢失）**：

> **核心问题**：播客文字稿通常 15-25K chars，无法在单次 MCP 工具调用中传入全部内容。**必须分块导入**。

**分块导入流程**：
1. 先用 `entry_create_entry`（`entry_type="page"`）创建空白 page，获取 `entry_id`
2. 将 markdown 内容按行分块，每块 ≤ 4000 chars（确保没有超长单行）
3. **第一块**：`entry_import_content_to_entry`（`entry_id=<page_id>`, `force_write=true`, `content=<第一块>`）
4. **后续块**：`entry_import_content_to_entry`（`entry_id=<page_id>`, `force_write=false`, `content=<后续块>`）— 追加到末尾
5. 验证：调用 `entry_describe_ai_parse_content` 确认内容完整（检查最后一个时间戳是否接近播客总时长）

**⚠️ 关键注意事项**：
- 每块内容必须是完整的 markdown 结构（不要在标题或段落中间切断）
- 如果文字稿中有单行超过 4000 chars 的情况（说明合并策略有 bug），需要回到 Step 3 修复合并逻辑
- 48 分钟播客（~200 段 × ~100 字/段 = ~20K chars）通常需要分 5-6 块导入

```bash
# ✅ 正确：通过 OpenAPI 上传音频（产生 entry_type=audio，触发 VOD 转码可播放）
python3 scripts/upload_video_via_openapi.py "<音频文件>.m4a" \
    --space-id <space_id> \
    --parent-entry-id <日期目录 entry_id> \
    --media-type audio
```

> **🚨 关键踩坑（2026-05-08 实战验证）**：
> - ❌ `file_apply_upload` + curl PUT + `file_commit_upload` → 产出 `entry_type=file`，音频**无法播放**
> - ✅ `upload_video_via_openapi.py --media-type audio` → 产出 `entry_type=audio`，乐享自动 VOD 转码，**可在线播放**

**播客 vs YouTube 的关键区别**：

| 维度 | YouTube 视频 | 播客音频 |
|------|-------------|---------|
| 文件格式 | `.mp4`（视频） | `.m4a`/`.mp3`（纯音频） |
| 文件大小 | 较大（HLS 720p ~500MB） | 较小（~60MB/小时） |
| 下载方式 | 需要 HLS 格式避免 403 | 直接下载，无反爬 |
| cookies | 通常需要 | 不需要 |
| Whisper 语言 | 通常是英文（需翻译） | 通常是中文（需繁简转换） |
| 上传 MIME | `video/mp4` | `audio/mp4` 或 `audio/mpeg` |

**依赖**（额外）：
- `opencc-python-reimplemented`（`pip3 install opencc-python-reimplemented`）— 繁体转简体（Whisper base 模型中文输出为繁体时需要）

#### 结构化分析

输出结构化分析：
```
【文章主题】一句话概括
【核心论点】3-5 个关键观点
【关键数据】文章中的重要数据/图表
【利益相关】作者/机构的立场与潜在倾向（如有）
【原文出处】完整标题 + URL
```

规划图表：第 1 张为总览图，第 2-N 张各聚焦 1 个核心论点。向用户确认图表数量和主题划分。

### Step 2：原文保存到乐享知识库

**在进入信息图生成流程之前，先将原文完整保存到乐享知识库**，确保素材归档和可追溯。

#### 配置文件与初始化

本 skill 的目标知识库等信息通过配置文件管理，**不在 SKILL.md 中硬编码**。

配置文件路径：**`config.json`**（位于 skill 根目录，即与本 SKILL.md 同级）

##### 对话式配置初始化（首次使用时自动触发）

当 `config.json` 中 `_initialized` 为 `false` 或 `space_id` 为空时，**在执行任何乐享操作前**，必须先通过对话引导用户完成配置。

**核心设计**：用户只需要粘贴一个乐享知识库链接，Agent 自动完成所有配置。

**链接格式**：`https://<domain>/spaces/<space_id>?company_from=<company_from>`
- 示例：`https://lexiangla.com/spaces/b6013f6492894a29abbd89d5f2e636c6?company_from=e6c565d6d16811efac17768586f8a025`
- 从链接中可解析出三个关键信息：**域名**（`lexiangla.com`）、**space_id**、**company_from**

---

**流程如下**：

**第一步：检测 MCP 连接**
1. 尝试调用任意一个 lexiang MCP 工具（如 `whoami`）检测 MCP 是否已连接
2. 如果调用成功 → MCP 已连接，进入第二步
3. 如果调用失败（MCP 未连接）→ 引导用户完成 MCP 鉴权：
   ```
   ⚠️ 乐享 MCP 尚未连接。请先完成鉴权配置：

   1. 访问 https://lexiangla.com/mcp 登录后获取 COMPANY_FROM 和 LEXIANG_TOKEN
   2. 按照你使用的 Agent 配置 MCP 连接：
      - CodeBuddy：在 MCP 管理面板中添加 lexiang server
      - OpenClaw：运行 claw install https://github.com/tencent-lexiang/lexiang-mcp-skill
      - 其他 Agent：在 MCP 配置文件中添加 lexiang server
   3. 完成后告诉我，我会继续配置流程。
   ```
   **不要继续后续步骤**，等待用户完成 MCP 连接后重试。

**第二步：请求用户提供知识库链接**
1. 向用户发送引导消息：
   ```
   🔧 首次使用，需要配置目标知识库。

   请粘贴你想用来归档文章的乐享知识库链接，格式如：
   https://lexiangla.com/spaces/xxxxx?company_from=yyyyy

   💡 获取方式：在乐享中打开目标知识库，复制浏览器地址栏中的链接即可。
   ```
2. **等待用户输入**，不要自行猜测或列举知识库

**第三步：解析链接并验证**
1. 从用户提供的链接中用正则解析出三个字段：
   - **domain**：链接的域名部分（如 `lexiangla.com`），用于生成后续访问链接
   - **space_id**：`/spaces/` 后面的路径段（如 `b6013f6492894a29abbd89d5f2e636c6`）
   - **company_from**：`company_from=` 参数值（如 `e6c565d6d16811efac17768586f8a025`）
2. 如果链接格式不正确（缺少 `space_id` 或 `company_from`）→ 提示用户重新粘贴正确的链接
3. 调用 `space_describe_space`（参数：`space_id=<解析出的 space_id>`）验证知识库是否存在
4. 如果验证失败 → 提示用户检查链接是否正确或是否有该知识库的访问权限

**第四步：写入配置并确认**
1. 将解析和验证得到的信息写入 `config.json`：
   - `lexiang.target_space.space_id` = 解析出的 space_id
   - `lexiang.target_space.space_name` = 从 `space_describe_space` 返回值获取的知识库名称
   - `lexiang.target_space.company_from` = 解析出的 company_from
   - `lexiang.access_domain.domain` = 解析出的域名
   - `lexiang.access_domain.page_url_template` = `https://<domain>/pages/{entry_id}?company_from={company_from}`
   - `lexiang.access_domain.space_url_template` = `https://<domain>/spaces/{space_id}?company_from={company_from}`
   - `_initialized` = `true`
2. 向用户确认配置结果：
   ```
   ✅ 配置完成！

   📚 目标知识库：<知识库名称>
   🔗 访问链接：https://<domain>/spaces/<space_id>?company_from=<company_from>

   后续抓取的文章将自动归档到此知识库。如需更换，告诉我「重新配置知识库」即可。
   ```

##### 重新配置

当用户说「重新配置知识库」、「切换知识库」、「更换目标知识库」等类似意图时：
1. 将 `config.json` 中 `_initialized` 设为 `false`
2. 重新执行上述对话式初始化流程（从第一步开始）

##### 用户输入容错

用户可能不会粘贴完美的链接，需要处理以下情况：

| 用户输入 | 处理方式 |
|---------|---------|
| 完整链接 `https://lexiangla.com/spaces/xxx?company_from=yyy` | 直接解析 ✅ |
| 不带 company_from 的链接 `https://lexiangla.com/spaces/xxx` | 提示：「链接中缺少 company_from 参数。请在乐享中重新复制完整链接（地址栏中通常会包含 ?company_from=xxx），或者访问 https://lexiangla.com/mcp 获取你的 COMPANY_FROM 值告诉我。」|
| 纯 space_id `b6013f6492894a29abbd89d5f2e636c6` | 提示：「请提供完整的知识库链接（包含 company_from 参数），我需要从链接中同时获取知识库 ID 和企业标识。」|
| 页面链接 `https://lexiangla.com/pages/xxx` | 提示：「这是一个页面链接，请提供知识库链接（格式：https://lexiangla.com/spaces/xxx?company_from=yyy）。你可以在乐享中进入目标知识库首页，复制地址栏链接。」|
| 返回的文档链接打不开/无权限 | 链接中缺少 `company_from` 参数。页面链接必须带 `?company_from=xxx`，格式：`https://lexiangla.com/pages/<entry_id>?company_from=<company_from>` |

##### 配置结构

```json
{
  "_initialized": false,
  "lexiang": {
    "target_space": {
      "space_id": "",
      "space_name": "",
      "company_from": ""
    },
    "access_domain": {
      "domain": "lexiangla.com",
      "page_url_template": "https://lexiangla.com/pages/{entry_id}?company_from={company_from}",
      "space_url_template": "https://lexiangla.com/spaces/{space_id}?company_from={company_from}"
    }
  }
}
```

> **`access_domain` 会从用户粘贴的链接中自动提取域名**，无需手动配置。适配自定义域名的乐享部署。

后续文档中所有 `<SPACE_ID>`、`<COMPANY_FROM>`、`<ACCESS_DOMAIN>` 等占位符，均指从 `config.json` 中读取的实际值。

#### 乐享 MCP 工具的调用方式（重要 — 多 Agent 适配）

本 skill 需要服务多个 Agent 产品（OpenClaw、CodeBuddy、Claude Desktop 等）。不同 Agent 连接乐享 MCP 的方式不同，但**暴露的工具名称和参数完全一致**（都是 lexiang MCP server 提供的标准工具）。

> **核心原则**：本 skill 只描述「调用哪个工具 + 传什么参数」，**不规定具体的 MCP 调用语法**。每个 Agent 按自己的方式调用即可。

**各 Agent 产品的 MCP 连接方式**：

| Agent 产品 | lexiang MCP 连接方式 | 工具调用方式 |
|-----------|---------------------|-------------|
| **CodeBuddy** | 在 `~/.codebuddy/mcp.json` 中配置 lexiang server，通过 IDE 的 MCP 管理面板启用连接 | 直接调用 `space_describe_space`、`file_apply_upload` 等 lexiang MCP 工具 |
| **OpenClaw** | `claw install https://github.com/tencent-lexiang/lexiang-mcp-skill`，加载 skill 时自动连接 MCP | 同上，通过 skill 暴露的 MCP 工具调用 |
| **Claude Desktop / 其他 MCP 兼容 Agent** | 在 Agent 的 MCP 配置文件中添加 lexiang server URL | 同上 |

**MCP 连接检测与降级**：

在执行乐享操作前，**必须先检测 lexiang MCP 是否已连接**：
1. 读取 `config.json`，检查 `_initialized` 和 `lexiang.target_space.space_id`
2. 如果未初始化 → 先触发对话式配置初始化（参见上方「对话式配置初始化」），初始化流程中会自动完成 MCP 连接检测
3. 如果已初始化，尝试调用 `space_describe_space`（参数：`space_id=<config 中的 space_id>`）验证 MCP 连接
4. 如果调用成功 → MCP 已连接，继续后续流程
5. 如果调用失败（MCP 未连接）→ **提示用户检查 MCP 连接**，给出对应 Agent 的操作指引：
   - CodeBuddy：「请在 MCP 管理面板中确认 lexiang server 已启用并显示为已连接状态」
   - OpenClaw：「请确认已安装 lexiang skill（`claw install https://github.com/tencent-lexiang/lexiang-mcp-skill`）」
   - 其他 Agent：「请确认 MCP 配置中已添加 lexiang server」

> **⚠️ 禁止降级为 curl 调用 REST API**：即使 MCP 未连接，也**不要**自行编写 curl 调用乐享 REST API，因为：(1) 认证信息硬编码在 curl 中不安全；(2) 不同 Agent 的执行环境差异大，curl 方式不通用；(3) REST API 的 URL 格式和鉴权方式可能变化。应该引导用户修复 MCP 连接。

**认证配置**（首次使用时需要）：

1. 访问 [https://lexiangla.com/mcp](https://lexiangla.com/mcp) 登录后获取 **`LEXIANG_TOKEN`**（访问令牌，格式：`lxmcp_xxx`）
   > `COMPANY_FROM` 无需手动获取 — 会从用户粘贴的知识库链接中自动解析

2. 配置方式（二选一）：
   - **环境变量**（推荐）：`export LEXIANG_TOKEN="lxmcp_xxx"`
   - **直接修改 MCP 配置**：将 MCP server URL 中的 `${LEXIANG_TOKEN}` 占位符替换为实际值

3. 详细配置步骤参见：[lexiang-mcp-skill setup.md](https://github.com/tencent-lexiang/lexiang-mcp-skill/blob/main/setup.md)

#### 目标知识库

从 `config.json` 的 `lexiang.target_space` 中读取：

- **知识库名称**：`config.lexiang.target_space.space_name`
- **知识库访问链接**：按 `config.lexiang.access_domain.space_url_template` 格式拼接
- **Space ID**：`config.lexiang.target_space.space_id`

> **⚠️ 访问链接域名**：用户可访问的乐享前端域名从 `config.lexiang.access_domain.domain` 读取（默认为 `lexiangla.com`），**不是** `mcp.lexiang-app.com`（后者是 MCP API 服务端域名，浏览器无法直接访问）。所有展示给用户的链接必须按 `config.lexiang.access_domain.page_url_template` 格式生成。

#### 目录组织方式

按**天维度**组织目录：
```
知识库根目录/
  2026-02-25/
    文章标题A      (图文文章，在线文档 page 类型，图片内嵌)
    文章标题B      (纯文本文章，在线文档 page 类型)
  2026-02-26/
    文章标题C      (在线文档 page 类型)
```

> **⚠️ 默认格式**：所有文章（无论是否含图片）**统一使用在线文档（page）格式上传**。在线文档支持在乐享中直接编辑、划词评论、全文检索，体验远优于 PDF。PDF 仅作为降级方案（`md_to_page.py` 失败时）或用户明确要求时使用。

#### 操作流程

> **⚠️ 严格按步骤顺序执行，不得跳步！** 必须完成步骤 0→1→2→3→4 的完整流程。尤其是**步骤 2（创建日期目录）不可跳过**——文档必须上传到当天日期命名的文件夹中，而不是直接上传到知识库根目录。如果跳过步骤 2 直接用 `root_entry_id` 作为上传目标，文档将错误地出现在根目录下。

通过 lexiang MCP 工具，按以下步骤完成转存：

**步骤 0：读取配置（含初始化检测）**
- 读取 skill 目录下的 `config.json` 文件
- 检查 `_initialized` 是否为 `true` 且 `lexiang.target_space.space_id` 非空
- 如果**未初始化**（`_initialized` 为 `false` 或 `space_id` 为空）→ **触发对话式配置初始化流程**（参见上方「对话式配置初始化」），完成后再继续
- 提取 `lexiang.target_space.space_id`、`lexiang.access_domain.page_url_template` 等配置项

**步骤 1：获取知识库根节点**
- 调用 `space_describe_space`（参数：`space_id=<config 中的 SPACE_ID>`）
- 从返回结果中提取 `root_entry_id`

**步骤 2：检查/创建当天日期目录（🚨 必须先查再建，禁止直接创建）**

> **🚨 这是本 skill 最常见的错误！** 2026-05-11 实战中，Agent 未查询直接创建了同名目录。每次执行到此步骤，**必须**严格按照下方决策树执行，绝对禁止跳过查询直接调用创建工具。

---

**🚨 执行前必读：三种常见错误**

| # | 错误做法 ❌ | 正确做法 ✅ |
|---|---|---|
| 1 | 直接调用 `mcp__lexiang__entry_create_entry` 创建文件夹 | 先调用 `mcp__lexiang__entry_list_children` 查询根目录 |
| 2 | 只查第一页，看到没有就创建（忽略 `next_page_token`） | 只要返回有 `next_page_token`，就继续查下一页，直到取完所有条目 |
| 3 | 只匹配 `name=="2026-05-11"`，不检查 `entry_type` | 必须同时匹配 `name=="2026-05-11"` **且** `entry_type=="folder"` |

---

**决策树（必须逐条执行，不可跳步）：**

```
步骤 2a：首次查询根目录
  工具：mcp__lexiang__entry_list_children
  参数：{"parent_id": "<root_entry_id>"}
  
  遍历返回的 entries[] 数组：
    查找是否有 entry_type=="folder" 且 name=="当天日期" 的条目
    例如今天 2026-05-11 → 查找 name=="2026-05-11" 且 entry_type=="folder"
  
  如果找到 → 记录其 id → 【跳到步骤 3，不创建】

步骤 2b：处理分页（重要！）
  检查首次返回结果中是否有 next_page_token：
    如果有 → 用 page_token 参数再次调用 entry_list_children
    重复此过程，直到 next_page_token 为空
    【每次查询都要检查 entries[] 中是否有目标文件夹】

步骤 2c：确认不存在后，才能创建
  只有满足以下所有条件，才能调用创建工具：
    ✅ 已检查第一页 entries（确认不存在）
    ✅ 已检查所有分页（如果 next_page_token 存在）
    ✅ 确认不存在任何 name=="当天日期" 且 entry_type=="folder" 的条目
  
  调用：mcp__lexiang__entry_create_entry
  参数：{"entry_type": "folder", "parent_entry_id": "<root_entry_id>", "name": "当天日期"}
```

---

**❌ 错误示例（禁止这样做）：**

```
# 错误：直接创建，不查询
→ 调用 mcp__lexiang__entry_create_entry，参数 name="2026-05-11"
→ 结果：知识库中出现多个同名 "2026-05-11" 文件夹
```

**✅ 正确示例（必须这样做）：**

```
# 正确：先查询所有分页，确认不存在才创建
→ 调用 mcp__lexiang__entry_list_children，参数 parent_id="<root_entry_id>"
→ 遍历 entries，检查是否有 name=="2026-05-11" 且 entry_type=="folder"
→ 检查 next_page_token，若存在则继续查询下一页（重复直至为空）
→ 确认不存在 → 才调用 mcp__lexiang__entry_create_entry
→ 若已存在 → 直接使用已有文件夹的 id，跳过创建
```

**步骤 3：去重检查**
- 调用 `entry_list_children`（参数：`parent_id=<日期目录ID>`）查询该日期目录下已有的条目
- 按「名称 + 类型」检查是否已存在同名文档，如果已存在则跳过上传并告知用户

**步骤 3.5：非中文文章翻译（🚨 强制检查，不可跳过）**

> **⚠️ 重要**：无论文章是通过 `fetch_article.py`、`web_fetch` 还是其他方式获取，在上传到乐享之前**都必须经过语言检测和翻译步骤**。这是一个**强制检查点**，不存在任何可以跳过的"简化路径"。
>
> **常见遗漏场景**：
> 1. ❌ 用 `web_fetch` 抓取后直接转 PDF 上传 → 英文原文未翻译
> 2. ❌ 觉得文章"看起来不长"就跳过翻译 → 知识库中留下纯英文文档
> 3. ❌ 翻译脚本不可用就放弃翻译 → 应该由 Agent 直接在对话中翻译
>
> **正确做法**：每篇文章上传前，**必须先执行语言检测**，非中文则翻译后再上传。

在上传到乐享之前，**必须检测原文语言**。如果原文不是中文，则需要先翻译为**中英对照格式**后再归档。

**语言检测规则**：
- 读取 `<原文标题>.md` 的前 500 个字符，统计中文字符（Unicode 范围 `\u4e00-\u9fff`）占比
- 中文字符占比 **≥ 30%** → 判定为中文文章，**跳过翻译**，直接进入步骤 4
- 中文字符占比 **< 30%** → 判定为非中文文章，**执行翻译**

**翻译排版格式（中英对照）**：
- 按段落逐段翻译，每段原文紧跟对应中文翻译
- **段落之间不加分隔线 `---`**，仅通过空行分隔
- **中文翻译段落开头不加国旗 emoji（🇨🇳）**，直接以中文开始
- 标题也需要翻译，保留原文标题 + 中文翻译标题
- 列表项、引用块等结构元素同样逐条翻译
- **保留原文中的图片引用**（`![](images/xxx.png)`），图片引用放在对应段落的上方或下方，确保图文对应关系不丢失

```markdown
# Original English Title
# 中文翻译标题

Original first paragraph text...

第一段的中文翻译...

![](images/img_01_xxx.png)

Original second paragraph text...

第二段的中文翻译...
```

**翻译方式（按优先级）**：
1. **translate_article.py 脚本**（如果 `OPENAI_API_KEY` 可用）：
   ```bash
   python3 scripts/translate_article.py "<原文标题>.md" "<原文标题>_translated.md" --model gpt-4o-mini
   ```
2. **AI 助手直接翻译**（如果无 API Key）：由 Agent 在对话中逐段翻译全文，生成 `<原文标题>_translated.md`

**翻译完成后**：
- 本地保存两个文件：`<原文标题>.md`（原文）和 `<原文标题>_translated.md`（中英对照版）
- **归档到乐享知识库的必须是翻译后的中英对照版本**（`_translated.md`），确保知识库中的内容对中文读者友好
- 乐享文档标题使用：`<原文标题中文翻译>（<原文标题>）`，如：`AI 原型精通阶梯（The AI Prototyping Mastery Ladder）`

**步骤 3.7：评价信息处理（可选）**

如果在转存前用户提供了对文章的评价（例如："这篇文章好在：1）... 2）..."），需要在上传时自动添加评价信息：

1. **检测评价信息**：在对话中识别用户是否提供了评价内容（关键词：好在、评价、优点、建议等）
2. **保存评价内容**：将评价信息保存到临时文件（如 `/tmp/evaluation.txt`）
3. **传入脚本参数**：调用 `md_to_page.py` 时，添加 `--evaluation-file /tmp/evaluation.txt` 参数
4. **脚本自动处理**：`md_to_page.py` 会自动在文档顶部插入评价信息（格式为 blockquote，乐享可能自动转换为 callout 组件）

**对于非在线文档格式（如视频）**：
- 由于 lexiang MCP 工具中**没有创建评论的 API**（只有查询评论的 `comment_list_comments` 和 `comment_describe_comment`），暂时无法自动添加评论到视频文件
- **建议**：转存完成后，手动在乐享中添加评论

**示例：用户提供评价后的处理流程**
```bash
# 1. 将用户评价保存到临时文件
cat > /tmp/evaluation.txt << 'EOF'
这篇文章好在：
1）把智能体Agent做了分类，每个分类定义了对应是适用场景；
2）列举了详实的案例说明；
3）通过构建的复杂度、技术架构、实现时长、运行成本、衡量成功等几个维度来系统化地综合判断Agent落地的优先级
4）未来关于Agent选型上，能够提供系统性的参考建议
EOF

# 2. 调用 md_to_page.py，传入评价文件
python3 scripts/md_to_page.py "<原文标题>_translated.md" \
  --parent-id <日期目录ID> --name "<文档标题>" \
  --evaluation-file /tmp/evaluation.txt \
  --token "$LEXIANG_TOKEN" --company-from "$COMPANY_FROM"
```

**评价信息格式说明**：
- 脚本会将评价信息格式化为 blockquote（以 `>` 开头的 Markdown 格式）
- 在乐享在线文档中，blockquote 可能被自动渲染为 callout 组件（带有左侧竖线或背景色）
- 如果需要真正的 callout 组件（特殊 block 类型），需要通过 `block_create_block_descendant` API 创建，但需要先了解 callout 的 block 结构

**步骤 3.8：页面内嵌视频检测与链接附加（⚠️ 不可跳过）**

在生成 PDF 或上传之前，**必须检测页面中是否包含嵌入视频**。嵌入视频（如 Wistia、YouTube、Vimeo、Loom 等 iframe 嵌入）在转为 PDF 时会完全丢失，因此需要将视频链接以文本形式附加到文档末尾，确保知识库读者能找到并观看原始视频。

**检测范围**（按优先级扫描）：
1. `<iframe>` 嵌入 — 匹配 `src` 中包含 `youtube`、`youtu.be`、`vimeo`、`loom`、`wistia`、`vidyard`、`player` 的 iframe
2. `<video>` 标签 — 提取 `src` 或内部 `<source>` 的 `src`
3. `<a>` 链接 — 匹配 `href` 指向 `youtube.com/watch`、`youtu.be/`、`vimeo.com/`、`loom.com/share` 等视频平台
4. 平台特定容器 — 如 readme.io 的 `rdmd-embed` 组件、`[class*="video"]` 容器等

**视频链接还原规则**：
- Wistia embed（`fast.wistia.net/embed/iframe/<id>`）→ 附加可观看链接 `https://fast.wistia.net/embed/iframe/<id>`
- YouTube embed（`youtube.com/embed/<id>`）→ 还原为 `https://www.youtube.com/watch?v=<id>`
- Vimeo embed（`player.vimeo.com/video/<id>`）→ 还原为 `https://vimeo.com/<id>`
- Loom embed（`loom.com/embed/<id>`）→ 还原为 `https://www.loom.com/share/<id>`
- 其他视频 URL → 原样保留

**附加格式**：在 Markdown 文档末尾（PDF 生成前）追加一个独立章节：

```markdown

---

## 📹 页面内嵌视频

本页面包含以下嵌入视频，PDF 中无法播放，请通过链接观看：

1. [视频] https://fast.wistia.net/embed/iframe/xxxxx
2. [视频] https://www.youtube.com/watch?v=yyyyy
```

如果使用 Playwright 直接生成 PDF（非 `fetch_article.py` 抓取），应在 `page.pdf()` 之前通过 `page.evaluate()` 在页面底部注入视频链接信息块。

**步骤 4：上传到乐享（统一使用在线文档格式）**

> **🚨 核心原则：所有文章默认使用在线文档（page）格式上传，不再默认转 PDF。**
> 在线文档的优势：支持编辑、划词评论、全文检索、移动端阅读体验好。
> PDF 仅在以下情况使用：(1) `md_to_page.py` 和 `entry_import_content` 都失败时的最终降级；(2) 用户明确要求 PDF 格式。

检查 `<原文标题>.md` 文件同目录下是否存在 `images/` 目录且包含图片文件：

- **有图片（图文文章）** → 使用 `scripts/md_to_page.py` 将 Markdown 图文导入为在线文档（图片内嵌到正文对应位置）：
  ```bash
  python3 scripts/md_to_page.py "<原文标题>.md" \
    --parent-id <日期目录ID> --name "<原文标题>" \
    --token "$LEXIANG_TOKEN" --company-from "$COMPANY_FROM"
  ```
  脚本会自动：按图片位置拆分 markdown → 分段导入文字（直传原始 markdown，不做 base64 编码）→ 逐张上传图片到 COS → 在正确位置插入 image block。
  
  **降级方案 A（脚本无 token 时 — 通过 MCP connector 分块导入图文）**：
  
  当 `md_to_page.py` 因缺少 LEXIANG_TOKEN 无法运行时（如 mcp.json 中无 lexiang 配置，只有 connector 模式），改用以下流程：
  1. `entry_create_entry`（`entry_type="page"`）创建空白 page
  2. 将 markdown **去除本地图片引用**（`![](images/xxx)`）后，分块（≤4000 chars/块）用 `entry_import_content_to_entry` 导入文字（第一块 force_write=true，后续 force_write=false 追加）
  3. **逐张上传关键图片**（>50KB 的图表/概念图/配图）到文档对应位置：
     - `block_apply_block_attachment_upload`（传 entry_id + name + size + mime_type）→ 获得 `session_id` + `upload_url`
     - `curl -X PUT "<upload_url>" -H "Content-Type: <mime>" -H "Content-Length: <size>" --data-binary @<文件路径>` → 上传到 COS
     - `block_create_block_descendant`（传 entry_id + parent_block_id + index + image block with session_id）→ 在指定位置插入图片
  4. 小装饰图/公式图（<50KB 的 icon/分隔线/SVG）可跳过
  
  > **⚠️ 图片位置确定方法**：
  > - 先用 `block_list_block_children`（entry_id, with_descendants=false）获取当前文档全部一级 block 及其 block_id
  > - 根据原文中 `![](images/xxx)` 出现的位置（在哪段文字之后），找到对应的 block_id
  > - 用 `index` 参数指定插入位置（0-based，-1 表示末尾）
  > - 如果文字已分块导入完毕再补图，可以按顺序从前往后插入（注意每插入一张图，后续 block 的 index 会 +1）
  > - **⚠️ 严禁对所有图片统一使用 `index=-1`（追加到末尾）**：这会导致所有图片堆积在文档底部，破坏图文混排效果。必须逐张计算正确位置插入
  
  > **⚠️ 得到 APP 文章特殊情况**：得到文章通常有 80-100+ 张图片，其中大部分是公式渲染图（3-10KB），真正有信息量的数据图表约 5-10 张（>50KB）。对得到文章，**必须**上传 >50KB 的关键图片（概念图、流程图、案例配图等），不需要逐张上传所有小图。
  
  > **⚠️ 得到文章完整转存流程（2026-05-09 实战验证）**：
  > 1. `fetch_article.py --cdp` 抓取全文 → 本地 article.md + images/
  > 2. 提取纯文字版（去掉 `![](images/...)` 引用 + 去掉得到APP UI噪声如"展开"、"分享"、点赞数、用户留言等）
  > 3. 创建 page → 分块导入纯文字（每块 ≤4000 chars）
  > 4. 筛选 >50KB 的关键图片（用 `find images/ -size +50k`）
  > 5. 排除 SVG 格式的 UI 图标（查看文件头是否为 `<?xml`）
  > 6. 逐张上传关键图片并插入文档对应位置
  
  **降级方案 B（最终降级）**：如果以上都失败 → 调用 `scripts/md_to_pdf.py` 转为 PDF，再通过三步上传流程上传：
  1. `file_apply_upload`（参数：`parent_entry_id=<日期目录ID>`, `name="<原文标题>.pdf"`, `size=<文件字节数>`, `mime_type="application/pdf"`, `upload_type="PRE_SIGNED_URL"`）
  2. 使用 `curl -X PUT` 将 PDF 文件上传到返回的 `upload_url`
  3. `file_commit_upload`（参数：`session_id=<上一步返回的session_id>`）
  
  > **🚨 绝对禁止**：不要用 `file_apply_upload` 直接上传 .md 文件！.md 上传后在乐享中会丢失所有图片信息，用户看到的只是含 `![](images/xxx)` 引用的纯文本，毫无可读性。

- **无图片（纯文本文章）** → 使用 `entry_import_content` 创建为**在线文档（page 类型）**：
  - 参数：`space_id=<config 中的 SPACE_ID>`, `parent_id=<日期目录ID>`, `name="<原文标题>"`, `content=<Markdown文件内容>`, `content_type="markdown"`
  - 在线文档支持在乐享中直接编辑

- **通过 `web_fetch` 抓取的文章（无本地图片文件）** → 直接使用 `entry_import_content` 创建在线文档，Markdown 内容中的外链图片在乐享中可能无法显示，但文字内容完整可编辑、可检索。

**步骤 5：输出结果**
- 按 `config.json` 中的 `lexiang.access_domain.page_url_template` 格式拼接文档链接，告知用户
- 示例：`https://lexiangla.com/pages/<entry_id>?company_from=<company_from>`（域名和 company_from 从配置读取，**不要**硬编码）
- **⚠️ 链接必须包含 `company_from` 参数**，否则用户打开页面会跳转到登录页或显示无权限

#### 注意事项

- **配置初始化是前置条件**：首次使用时会自动通过对话引导完成知识库配置，无需手动编辑文件
- **MCP 连接是前置条件**：必须先确认 lexiang MCP 已连接才能执行操作。不同 Agent 的连接方式不同，参见上方「乐享 MCP 工具的调用方式」
- **访问链接域名**：展示给用户的链接一律按 `config.json` 中 `page_url_template` 格式生成（含 `company_from` 参数），**不要**使用 `mcp.lexiang-app.com`，**不要**省略 `company_from`
- **上传前自动去重**：按「文档名称 + 文档类型」在目标日期目录下查重，避免重复上传
- **默认使用在线文档（page）格式**：所有文章（含图文）统一以在线文档格式上传，支持编辑、检索、评论。PDF 仅作为最终降级方案
- 纯文本文章直接用 `entry_import_content`，图文文章优先用 `md_to_page.py`（图片内嵌），降级用 `entry_import_content`（图片不内嵌但文字完整）
- PDF 转换依赖 `pymupdf` 库（`pip3 install pymupdf`），仅在前两种方式都失败时使用
- 如果同一天多次处理不同文章，它们会归入同一个日期目录下
- 使用 `_mcp_fields` 参数可以减少返回数据量，如 `_mcp_fields=["id", "root_entry_id", "name"]`

## 脚本文件

| 文件 | 用途 |
|------|------|
| `scripts/fetch_article.py` | 付费/登录墙文章全文抓取脚本（Chrome cookies + Playwright，Substack 登录态缓存，输出 Markdown + 图片 + 元信息 JSON） |
| `scripts/md_to_pdf.py` | Markdown 转 PDF 脚本（使用 pymupdf，嵌入本地图片，正确渲染中文，支持标题回退和拆行标题修复） |
| `scripts/md_to_page.py` | **【推荐】** Markdown 图文导入乐享在线文档脚本。按图片位置将 markdown 拆分为 text/image 交替段落，分段导入到乐享 page（文字用 entry_import_content_to_entry 直传原始 markdown，图片用 block_apply_block_attachment_upload + curl PUT + block_create_block_descendant 三步上传）。⚠️ 脚本通过 HTTP JSON-RPC 直连乐享 MCP API，content 字段**不需要 base64 编码**（直传原始 markdown 字符串）。支持任意长度文章，图片内嵌到正文对应位置，生成可编辑、可划词评论的在线文档。用法：`python3 scripts/md_to_page.py <md_file> --entry-id <ID> --token <TOKEN> --company-from <CF>` 或 `--parent-id <PID> --name "标题"` 创建新页面 |
| `scripts/yt_download_transcribe.py` | YouTube 视频下载 + Whisper 转录 + AI 翻译脚本（yt-dlp 下载、ffmpeg 提取音频、Whisper 转录、OpenAI 翻译为中英对照 Markdown）。也可用于播客音频转录（跳过视频下载步骤） |
| `scripts/translate_gemini.py` | 使用 Gemini API 将英文 Markdown 翻译为中英对照格式。按 ~4K 字符分段翻译，每段间隔 2 秒避免限频。模型：`gemini-2.5-flash`。需要 `GEMINI_API_KEY` 环境变量。用法：`python3 scripts/translate_gemini.py`（翻译后生成 `_translated.md` 文件） |

> **注意**：乐享知识库操作不再通过独立脚本（`save_to_lexiang.sh`/`upload_yt_to_lexiang.sh`）完成，而是由大模型通过 **lexiang MCP 工具**直接执行。不同 Agent 产品（OpenClaw、CodeBuddy、Claude Desktop 等）各自管理 MCP 连接，但调用的工具名称和参数完全一致。

## 经验总结

### 在线文档图文导入（md_to_page.py）

**核心方案**：Python 脚本通过 HTTP JSON-RPC 直连乐享 MCP API，按图片位置将 markdown 拆分为 text/image 交替段落，逐段导入。

**为什么不走 IDE 的 MCP 工具调用**：
- IDE MCP 工具调用有参数长度限制，45K 字符的 markdown base64 编码后 62K，无法一次性传递
- Python 脚本直连 HTTP JSON-RPC 没有此限制，按 ~15K 字符分段传输即可

**关键踩坑（⚠️ 重要）**：
1. **不要做 base64 编码**：通过 HTTP JSON-RPC 直连时，`entry_import_content_to_entry` 的 content 字段直传原始 markdown 字符串。如果做了 base64 编码，乐享会把 base64 字符串当成纯文本存储，页面显示为乱码。只有通过 IDE MCP 协议调用时才需要 base64
2. **图片需逐张插入**：`block_create_block_descendant` 一次传多张图片的 block 会失败，必须一张一张来
3. **文字分段追加**：第一段用 `force_write=true` 覆盖，后续段用 `force_write=false` 追加到末尾
4. **图片位置要正确**：先按原文中 `![](images/xxx.jpg)` 的位置拆分 markdown，确保文字和图片按原文顺序交替插入
5. **乐享文档名称**：要与文章原标题一致，创建时通过 `--name` 指定，或创建后用 `entry_rename_entry` 修改

**翻译注意事项**：
- **所有英文文章默认必须翻译为中英对照格式再归档**，不可跳过
- 翻译脚本 `translate_gemini.py` 使用 Gemini API（模型：`gemini-2.5-flash`），按 ~4K 字符分段翻译
- Gemini API `gemini-2.0-flash` 已下线，务必使用 `gemini-2.5-flash` 或更新的模型
- 翻译完成后用 `md_to_page.py --entry-id <ID>` 覆盖更新在线文档
- 如果没有 Gemini API Key 也没有 OpenAI API Key，由 AI 助手在对话中翻译后写入文件

**自测清单**（发布前必须完成）：
- [ ] 通过 `entry_describe_ai_parse_content` 验证文字内容可读（非 base64 乱码）
- [ ] 通过 `block_list_block_children` 验证图片 block 存在且有 file_id
- [ ] 验证文档名称与文章标题一致
- [ ] 验证中英对照格式（英文在前，中文翻译紧跟其后）

### YouTube 视频下载与转录

**核心方案**：yt-dlp 下载 → ffmpeg 提取音频 → Whisper 本地转录 → OpenAI API 翻译

**为什么不用 NotebookLM / summarize.sh**：
1. NotebookLM 需要 Google 账号且有额度限制，部分视频可能因版权限制无法提取
2. summarize.sh 依赖外部 API（Apify/YouTube 字幕 API），部分视频无字幕时无法工作
3. Whisper 本地转录**不依赖字幕**，直接从音频波形识别语音，覆盖率 100%

**yt-dlp 版本与安装（关键！）**：
- **必须使用 `brew install yt-dlp`** 安装，不要用 `pip3 install yt-dlp`
- 原因：pip 版本受限于系统 Python 版本（macOS 自带 Python 3.9），无法安装 yt-dlp 的 nightly 版本（需要 Python 3.10+）。而 YouTube 频繁更新反爬策略，旧版 yt-dlp 会遇到 HTTP 403 Forbidden 错误
- brew 安装的 yt-dlp 自带独立 Python 环境，始终能获取最新版本
- 脚本中调用方式：直接用 `yt-dlp` 命令，**不要**用 `python3 -m yt_dlp`

**YouTube DASH 格式 403 错误（重要！）**：
- YouTube 正在强制使用 SABR（Streaming ABR）流媒体协议，传统 DASH 分片下载（`bestvideo+bestaudio`）会触发 HTTP 403 Forbidden
- **解决方案**：优先使用 HLS（m3u8）格式下载，不会被 SABR 拦截
- 脚本中的格式选择顺序：`95-1/94-1/93-1/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best`
  - `95-1`: 720p HLS（推荐，画质和文件大小的最佳平衡）
  - `94-1`: 480p HLS
  - `93-1`: 360p HLS
  - 后面是传统 DASH 格式作为回退
- HLS 格式下载的视频文件会比 DASH 大一些（720p HLS 约 500-600MB vs DASH 约 200-300MB）
- **注意**：`--extractor-args "youtube:player_client=android"` 不支持 cookies，不是可靠的 403 解决方案

**Whisper 转录最佳实践**：
- 音频预处理：16kHz 采样率、单声道 WAV（`ffmpeg -ar 16000 -ac 1`），减少文件大小且是 Whisper 推荐格式
- 段落合并策略：相邻 segment 间隔 <2s 且总时长 <60s 则合并，句号/问号结尾时倾向断开
- 模型选择：默认用 `base`（速度和精度的最佳平衡），重要内容用 `small` 或 `medium`

**翻译策略**：
- 使用 OpenAI `gpt-4o-mini`，分批翻译（每批 10 段），避免 token 超限
- 翻译 prompt 要求"自然流畅的中文表达，专业术语保留英文并附中文注释"
- 中英对照格式：每段先展示英文原文，紧跟中文翻译，段间用空行分隔（不加分隔线和国旗 emoji）
- **如果没有 OPENAI_API_KEY**：脚本会跳过翻译步骤，输出纯英文文字稿。此时可以由 AI 助手在对话中直接翻译全文，然后用 `md_to_page.py --entry-id` 更新乐享文档

**上传乐享的关键决策**：
- 文字稿使用 **在线文档（page）格式**而非文件上传，原因：支持在乐享中按块维度编辑更新，可以逐段修正翻译或补充注释
- 视频使用 **文件（file）格式**上传，因为视频不需要在线编辑
- 上传成功后自动删除本地视频文件，避免占用磁盘空间

**视频上传到乐享的正确方式（重要！）**：
- 通过 lexiang MCP 工具完成，使用三步上传流程：
  1. `file_apply_upload`：申请上传凭证（传入 `parent_entry_id`=日期目录 ID、`upload_type`=PRE_SIGNED_URL、`mime_type`=video/mp4、`size`=文件字节数）
  2. `curl -X PUT` 上传文件到返回的 `upload_url`（预签名 URL，直传 COS）
  3. `file_commit_upload`：确认上传完成（传入 `session_id`）
- 518MB 视频的 PUT 上传约需 30-60 秒

### 播客音频转录

**核心方案**：yt-dlp（generic extractor）下载音频 → ffmpeg 转 WAV → Whisper 转录 → opencc 繁简转换

**yt-dlp 对小宇宙的支持**：
- yt-dlp 没有小宇宙专用 extractor，但 **generic extractor 完全够用**
- 小宇宙页面中嵌入了 `<audio>` 标签，音频直链在 `media.xyzcdn.net`
- 下载不需要 cookies，直接用 `yt-dlp --no-playlist -o "%(title)s.%(ext)s" <URL>` 即可
- 下载速度约 7MB/s，63 分钟播客（59MB）仅需 8 秒

**Whisper 中文转录的繁体问题（重要！）**：
- Whisper base 模型对中文普通话**倾向输出繁体字**（如「歡迎」→ 应为「欢迎」）
- 这是 Whisper 的已知行为，因为训练数据中繁体中文比重较大
- **解决方案**：转录后用 `opencc-python-reimplemented` 的 `t2s`（Traditional to Simplified）模式批量转换
- 安装：`pip3 install opencc-python-reimplemented`
- 用法：`opencc.OpenCC("t2s").convert(text)`

**中文播客 vs 英文 YouTube 的流程差异**：
- 中文播客**不需要翻译**，但**需要繁简转换**
- 播客音频是直接的 m4a/mp3 文件，**不需要从视频中提取音频**（但仍需 ffmpeg 转为 WAV 格式给 Whisper）
- Whisper 转录时**指定 `language='zh'`** 可以提高中文识别准确率
- 上传乐享时 MIME 类型用 `audio/mp4`（m4a）或 `audio/mpeg`（mp3），不是 `video/mp4`

**转录性能参考**：
- 63 分钟中文播客 → Whisper base 模型在 CPU 上转录耗时约 115 秒
- 产出 2496 个 segments，合并后 65 个段落

### 微信公众号图文抓取

**核心问题**：`web_fetch` 工具无法获取微信公众号文章的图片（懒加载 + 防盗链），**必须**使用 `fetch_article.py`。

**技术原理**：
1. **懒加载机制**：微信图片的真实 URL 存放在 `data-src` 而非 `src`，依赖 `IntersectionObserver` 在元素进入视口时才加载。Playwright 无头浏览器通过 `window.scrollBy(0, 300)` 配合 `asyncio.sleep(0.2)` 模拟慢速滚动，逐步触发所有图片的懒加载观察器
2. **兜底策略**：滚动完成后，通过 `page.evaluate()` 遍历所有 `img[data-src]`，将未被触发的 `data-src` 强制复制到 `src`
3. **高清图优先**：提取图片 URL 时优先使用 `data-src`（高清原图），而非 `src`（可能是低分辨率占位图）
4. **格式识别**：微信图片 URL 无常规扩展名（如 `mmbiz.qpic.cn/...?wx_fmt=png`），需解析 `wx_fmt` 查询参数推断文件格式
5. **防盗链绕过**：通过 Playwright 页面上下文的 `page.request.get()` 下载图片，自动携带正确的 Referer 头
6. **专用选择器**：微信文章有固定 DOM 结构（`#js_content`、`#activity-name`、`#js_name`、`#publish_time`），使用专用选择器比通用选择器更精准可靠

**关键决策**：
- 微信文章是公开可读的，跳过登录检测和 Cookie 注入流程
- 滚动参数（300px 步长、200ms 间隔）经实测可平衡速度与懒加载触发成功率
- Markdown 转换时 `imageMap` 同时匹配 `src` 和 `data-src`，确保无论 HTML 中引用哪个属性都能正确替换

**验证标准**：抓取完成后检查 `article_meta.json` 中的 `image_count` 字段，与原文图片数量比对，确认无遗漏。

### 新平台适配思路

适配新平台时，需依次识别和处理以下 4 个维度：
1. **懒加载机制** — 图片是否用 `data-src`、`data-lazy` 等延迟加载？需要怎样的滚动策略触发？
2. **专用 DOM 结构** — 正文、标题、作者、日期的选择器是什么？
3. **图片 URL 格式** — 扩展名是否在路径中？是否需要从查询参数推断？
4. **防盗链策略** — 是否需要正确的 Referer？是否有其他鉴权机制？

### 微信公众号文章处理（mp.weixin.qq.com）

**首选方案：乐享 MCP `file_create_hyperlink`（2026-05-09 验证 ✅）**

乐享后端原生支持微信公众号文章的抓取与解析，**一步到位**，无需本地抓取和手动上传图片。

```
mcp__lexiang__file_create_hyperlink(
  url = "https://mp.weixin.qq.com/s/...",
  parent_entry_id = "<目标目录 entry_id>",
  name = "<文章标题>"  // 可选，不传会自动从微信提取
)
```

**返回值**：
- `finished: true` — 后端抓取完成
- `entry.id` — 新创建的知识条目 ID
- `entry_type: "flink"` — 外部链接类型
- `extension: "wechat"` — 自动识别微信来源

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
- 创建 hyperlink 后，可用 `entry_import_content_to_entry`（force_write=false）追加评价内容
- 或用 `block_create_block_descendant` 在文档末尾插入评价 block

**降级方案（当 `file_create_hyperlink` 失败时）**：
- 如果返回 `finished: false` 或错误码，改用 `fetch_article.py` 本地抓取 + 降级方案 A 导入
- 某些被限制的微信文章（如已删除、需付费等）可能无法通过此接口抓取

**注意事项**：
- 产出的 entry_type 是 `flink`（外部链接），而非 `page`（在线文档）
- flink 类型在乐享中以原始文章格式展示，支持全文检索和 AI 解析
- 如果用户明确要求以「在线文档/page」格式存储（需要后续编辑），才使用 fetch_article.py 降级方案

### 得到 APP 文章抓取（dedao.cn）

**核心问题**：得到 APP（`www.dedao.cn`）的文章内容是**付费内容 + SPA 动态渲染**，`web_fetch` 和 `fetch_article.py` 的通用提取逻辑都无法直接获取正文。

**技术原因**：
1. **SPA 架构**：得到网页版是 React SPA，文章正文通过 JS 异步渲染，`web_fetch` 只能拿到空白壳页面
2. **付费墙**：文章属于付费专栏内容，必须有已登录且已订阅的账号才能查看全文
3. **DOM 结构特殊**：正文容器使用 `.iget-articles` 类名，不在 `fetch_article.py` 的默认选择器列表（`article`、`.post-content` 等）中。通用 `article` 选择器只匹配到极少内容（~167 字符），而真正的正文在 `.iget-articles` 中有 6000+ 字符
4. **内容区混杂**：正文容器中混入了标题重复、音频时长、"划重点"、用户评论等非正文内容，需要清理

**抓取方案**：使用 **CDP 模式**连接已登录得到的 Chrome 浏览器：

```bash
# 前提：用户已在 Chrome 中登录得到 APP 且有文章阅读权限
python scripts/fetch_article.py fetch "https://www.dedao.cn/course/article?id=<ID>" --output-dir <目录> --cdp
```

**已知限制**：
- `fetch_article.py` 的通用内容提取逻辑对得到 DOM 结构匹配不佳，**抓取结果可能不完整**
- 正确做法是通过 Playwright CDP 连接后，**手动指定 `.iget-articles` 选择器**提取正文：

```python
# 通过 CDP 连接后，用专用选择器提取得到文章正文
content_el = await page.query_selector('.iget-articles')
if content_el:
    text = await content_el.inner_text()  # 完整正文
```

**内容清理要点**：
- 去掉正文开头的标题重复、日期、音频时长等元信息（通常在 `凡哥杂谈，你好` 或类似开场白之前）
- 去掉正文末尾的"划重点"、"添加到笔记"、"首次发布"、"用户留言"等非正文内容
- 如果是多篇系列文章（如上/下篇），合并时用 `## 上篇` / `## 下篇` 分隔
- 作者信息需要手动确认（通用提取器可能抓错）

**得到文章转存乐享完整流程（2026-05-09 实战验证 ✅）**：

> 以下流程已在实际操作中验证通过，确保图文完整转存。

1. **抓取**：`python scripts/fetch_article.py fetch "<URL>" --output-dir articles/dedao_<ID短码> --cdp`
   - 产出：`article.md` + `images/` 目录（通常 80-100+ 张图，大部分是小于 10KB 的公式/icon 图）

2. **提取纯文字版**（去除图片引用和得到 UI 噪声）：
   ```bash
   # 去除图片引用 ![](images/...)
   # 去除得到 APP 特有 UI 噪声：
   #   - "展开"/"收起" 按钮文字
   #   - 点赞数、评论数、分享按钮（如 "25"、"8"、"218"、"分享"）
   #   - "关注" 按钮
   #   - 用户昵称 + 日期行（如 "Christy\n05-05"）
   #   - "划重点" / "添加到笔记" / "写笔记划线删除划线复制" 等功能按钮
   #   - "首次发布: ..." 行
   #   - "我的留言" / "用户留言" / "全部 精选 筛选" 等区域标记
   # 保留正文 + 注释引用
   ```
   
3. **创建在线文档 + 分块导入文字**：
   - `entry_create_entry`（entry_type="page", parent_entry_id=日期目录, name="<文章标题>（来源描述）"）
   - 将纯文字版分块（≤4000 chars/块），第一块 force_write=true，后续 force_write=false 追加
   - 验证导入结果（spot check 关键段落）

4. **筛选并上传关键图片**：
   ```bash
   # 找出 >50KB 的关键图片
   find images/ -size +50k -type f | sort
   
   # 排除 SVG/UI 图标（检查文件头）
   file images/img_04_*.png  # 如果是 SVG XML 则跳过
   
   # 查看图片内容（确认哪些有信息价值）
   # 典型有价值的：概念图、流程图、人物照片、数据图表
   # 典型无价值的：SVG 格式的得到 APP logo/icon
   ```

5. **逐张上传图片到文档对应位置**（每张图3步）：
   ```
   ① block_apply_block_attachment_upload(entry_id, name, size, mime_type) → session_id + upload_url
   ② curl -X PUT "<upload_url>" -H "Content-Type: <mime>" -H "Content-Length: <size>" --data-binary @<file>
   ③ block_create_block_descendant(entry_id, parent_block_id=page_block_id, index=<位置>, descendant=[{block_type:"image", image:{session_id, caption, align:"center"}}])
   ```
   
   **图片位置确定**：
   - 先用 `block_list_block_children`（entry_id, with_descendants=false）获取所有一级 block
   - 根据原文 article.md 中 `![](images/xxx)` 的位置，找到对应文字段落的 block_id
   - 用 index 参数插入（注意：每插入一张图，后面的 block index 都会 +1）
   - 如果精确位置难以确定，也可以用 index=-1 追加到末尾（所有图集中放在文末也可接受）

**适用场景**：得到 APP 专栏文章（`www.dedao.cn/course/article?id=xxx`）

**TODO**：考虑在 `fetch_article.py` 中增加得到专用检测和选择器（类似微信公众号的 `_is_wechat_article` 机制），自动使用 `.iget-articles` 提取正文。

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

### Python 兼容性

脚本使用 `from __future__ import annotations` 以兼容 Python 3.9（`str | None` 联合类型语法在 3.9 中不可用）。

## 常见问题

| 问题 | 原因 | 修复方法 |
|------|------|----------|
| YouTube 视频下载 HTTP 403 Forbidden | yt-dlp 版本过旧 + YouTube 强制 SABR 流媒体协议，传统 DASH 分片下载被拦截 | ① `brew install yt-dlp` 升级到最新版（不要用 pip）；② 脚本已配置优先使用 HLS(m3u8) 格式（`95-1/94-1/93-1`），自动回退 |
| `pip3 install --upgrade yt-dlp` 无法安装最新版 | macOS 自带 Python 3.9，yt-dlp nightly 版需要 Python 3.10+ | 改用 `brew install yt-dlp`，brew 版自带独立 Python 环境 |
| 脚本中 `python3 -m yt_dlp` 调用失败 | pip 安装的旧版 yt-dlp 与 brew 安装的新版不一致 | 脚本已修改为直接调用 `yt-dlp` 命令（brew 安装的版本） |
| 视频上传乐享报"不支持的文件格式" | 旧版 COS API（`/kb/files/upload-params`）不识别视频格式 | 通过 lexiang MCP 工具使用三步上传流程：`file_apply_upload` → `curl PUT` → `file_commit_upload` |
| Whisper 转录速度极慢 | 模型太大或音频太长 | 换用 `tiny` 或 `base` 模型；对于长视频（>1h），考虑用 `--whisper-model tiny` 先快速预览 |
| 翻译结果为空 | 未设置 `OPENAI_API_KEY` 环境变量 | `export OPENAI_API_KEY=sk-xxx`；或使用 `--skip-translate` 跳过翻译，由 AI 助手在对话中直接翻译全文后用 `md_to_page.py --entry-id` 更新乐享文档 |
| 中英对照格式段落错位 | AI 翻译返回的段落数与原文不匹配 | 脚本已有容错处理（缺少翻译的段落会跳过），可手动补充翻译 |
| 视频上传乐享超时 | 视频文件过大（>500MB）| 使用 MCP 的 `file_apply_upload` 预签名 URL 方式上传，518MB 文件约 30-60 秒即可完成 |
| Whisper 中文转录输出繁体字 | Whisper base 模型对中文普通话倾向输出繁体 | 用 `opencc-python-reimplemented` 的 `t2s` 模式进行繁简转换：`opencc.OpenCC("t2s").convert(text)` |
| 小宇宙播客下载提示 generic extractor | yt-dlp 没有小宇宙专用 extractor | 正常现象，generic extractor 能自动从页面提取音频直链（`media.xyzcdn.net`），下载完全正常 |
| 微信文章图片丢失 | `web_fetch` 无法触发懒加载和绕过防盗链 | **首选**：使用 `file_create_hyperlink` 直接导入（乐享后端自动处理图文）。**降级**：使用 `fetch_article.py`（脚本自动检测微信域名并启用专用处理策略） |
| 乐享知识库操作失败 | MCP 连接异常或 Token 过期 | ① 确认当前 Agent 的 lexiang MCP 已连接（CodeBuddy 检查 MCP 面板、OpenClaw 检查 skill 安装状态）；② Token 过期时访问 https://lexiangla.com/mcp 获取新 Token 并更新 MCP 配置 |
| 文件上传到了知识库根目录而非日期目录 | 跳过了步骤 2（创建日期目录）和步骤 3（去重检查），直接以 `root_entry_id` 作为 `parent_entry_id` 上传 | 严格按照步骤 1→2→3→4 顺序执行，步骤 2 中先 `entry_list_children` 检查日期目录是否存在，不存在则创建 |
| 展示给用户的乐享链接无法访问 | 使用了 MCP API 域名 `mcp.lexiang-app.com` 或缺少 `company_from` 参数 | 所有展示给用户的链接必须按 `config.json` 中 `page_url_template` 格式生成：`https://lexiangla.com/pages/<entry_id>?company_from=<company_from>`。**company_from 不可省略**，否则用户无法访问 |
| PDF 中缺少标题 | `fetch_article.py` 的 `processNode` 将正文 `<h1>` 转为 `# 标题`，与手动拼接的元信息头标题重复；某些网站（如 Lenny's Newsletter）标题在 `articleEl` 外部导致 MD 文件第一行 `# ` 为空 | 已修复：(1) `processNode` 中自动去重正文中与已提取 title 相同的第一个 h1 (2) 标题提取增加 `og:title`、`meta[name="title"]`、`document.title` 多策略回退 (3) `md_to_pdf.py` 增加标题回退——当 MD 中无有效 h1 时从 `article_meta.json` 补充 |
| PDF 中缺少子标题 | 某些网站的 HTML 结构导致 `### # 从 Tab 到 Agents` 被拆为两行：`### #` 和 `从 Tab 到 Agents`，`parse_markdown` 将 `#` 视为无效标题丢弃 | 已修复：`parse_markdown` 增加拆行标题检测——当标题文字为 `#` 或空时，检查下一行是否为实际标题文字并合并 |
| md_to_page.py 导入后文字显示为 base64 乱码 | 脚本通过 HTTP JSON-RPC 直连乐享 MCP API 时，对 content 做了多余的 base64 编码。乐享 MCP 的 base64 要求仅针对 IDE 侧 MCP 协议 | 已修复：去掉 `import_content` 函数中的 `base64.b64encode()`，直传原始 markdown。⚠️ 通过 HTTP JSON-RPC 直连时**永远不要做 base64 编码** |
| md_to_page.py 批量插入图片 block 失败 | `block_create_block_descendant` 一次传多张图片的 descendant 数组会超时或报错 | 改为逐张插入，每次只传一个 image block 的 descendant + children |
| Gemini API 调用报 404 模型不存在 | `gemini-2.0-flash` 模型已下线 | 使用 `gemini-2.5-flash` 替代。可通过 `curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"` 查看当前可用模型 |
| 英文文章未翻译就归档 | 跳过了步骤 3.5 的语言检测和翻译 | **所有英文文章必须翻译为中英对照后再归档**，这是强制步骤不可跳过。使用 `translate_gemini.py`（Gemini API）或 `translate_article.py`（OpenAI API）翻译，翻译完用 `md_to_page.py --entry-id` 覆盖更新 |
| `translate_gemini.py` 报错 FileNotFoundError | 脚本硬编码了源文件路径，不读取命令行参数 | 已修复：改用 `sys.argv[1]` 读取输入文件，`sys.argv[2]` 读取输出文件，默认输出 `_translated.md` |
| `md_to_page.py` 执行报错 IndentationError | 添加 `--evaluation`/`--evaluation-file` 参数时缩进不一致 | 已修复：参数定义须与上方 `--base-url` 对齐；Python 严禁混用 tab 和空格 |
| `fetch_article.py` 下载的图片在 `md_to_page.py` 中提示 NOT FOUND | 下载保存的文件名与写入 Markdown 的引用不一致（如 `img_06_1c1cfc4c.gif` vs `img_06_1c1cfc42.gif`）| `fetch_article.py` 的 `process_images` 函数中，保存到 `images/` 的文件名与替换 Markdown `src` 时的文件名必须完全一致；建议统一使用 `hash[:8]` + 原始扩展名，并在替换后打印映射表方便排查 |
| 乐享 MCP 更新 token 后工具仍报 "not found" | `mcp.json` 配置已更新，但 MCP 服务未重新加载 | **必须重启 WorkBuddy**（或禁用再重新启用 MCP 服务），新的 token 才能生效 |
| `md_to_page.py` 新增评价信息功能 | 需要在文档顶部插入用户评价（callout 组件）| 已添加 `--evaluation`（短文本）和 `--evaluation-file`（文件路径）两个参数；评价内容会以 blockquote 格式插入文档顶部，乐享会自动渲染为 callout 组件 |
| 播客文字稿章节标题重复出现几十次 | 在 Whisper segment 级别（1-5秒粒度）插入章节标题，且用宽松时间容差匹配 `abs(start - ts) < 5`，导致多个 segment 都命中同一标题 | **必须先合并 segments 为段落（gap<2s, duration<60s），再在段落级别插入标题**。用 `inserted_headers = set()` 跟踪已插入标题，每个标题只插入一次 |
| 日期目录重复创建 | 直接调用 `entry_create_entry` 而不先查询目录是否已存在 | **必须先用 `entry_list_children` 查询根目录**，匹配到同名 folder 则复用其 ID，不存在才创建。已在步骤 2 中加强约束 |
| 得到文章转存后无图片 | 只导入了纯文字，未执行图片上传步骤 | 得到文章**必须**在文字导入后，逐张上传 >50KB 的关键图片（概念图/流程图/配图），流程：`block_apply_block_attachment_upload` → `curl PUT` → `block_create_block_descendant`(image block)。详见"得到 APP 文章抓取"章节 |
| 图片上传后显示不出来 | `block_create_block_descendant` 的 image block 未正确传入 session_id | image block 的 `session_id` 必须来自同一个 `block_apply_block_attachment_upload` 返回值，且 curl PUT 必须返回 HTTP 200 才表示文件上传成功 |
