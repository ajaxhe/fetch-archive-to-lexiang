---
name: fetch-archive-to-lexiang
description: 通用文章抓取与归档工具。抓取任意 URL（免费/付费/登录墙）的文章全文，转换为结构化 Markdown，并可选转存到乐享知识库。支持 Substack、Medium、知识星球等付费平台的登录态管理。支持 YouTube 视频下载（yt-dlp）、播客音频下载（小宇宙FM等）、音频转录（Whisper）、翻译（中英对照格式），并将音视频和文字稿上传乐享知识库（文字稿使用在线文档格式，支持按块编辑）。支持 PDF 文件/链接：自动提取文本+精确裁剪图形，非中文内容默认翻译为中英对照后转存乐享。支持微博帖子抓取（CDP 模式绕过登录墙）。关键词触发：抓取文章、获取全文、付费文章、转存知识库、乐享、保存原文、fetch article、归档、YouTube、视频转录、字幕提取、视频下载、播客、podcast、小宇宙、xiaoyuzhou、PDF、论文、arxiv、微博、weibo。
---

# 抓取链接内容 & 转存知识库

## 核心规则

1. **文件命名**：必须用原文标题命名（`<标题>.md`），不用 `article.md`
2. **乐享链接格式**：`https://lexiangla.com/pages/{entry_id}?company_from=e6c565d6d16811efac17768586f8a025`（禁止 `mcp.lexiang-app.com`）
3. **非中文内容必须翻译**：中英对照格式（每段英文后紧跟中文翻译）
4. **图片不可丢失**：有图片的文章必须用 `fetch_article.py` 抓取 + `md_to_page.py` 导入

## 工作流程总览

```
Step 1: 素材收集（抓取原文+图片）
Step 2: 语言检测 → 非中文则翻译为中英对照
Step 3: 转存到乐享知识库（日期目录 + 图文导入）
```

## Step 1：素材收集（抓取方式决策树）

根据 URL 类型选择抓取方式（按优先级）：

| 优先级 | URL 类型 | 抓取方式 | 详细参考 |
|--------|----------|----------|----------|
| 1 | 微信公众号 `mp.weixin.qq.com` | 乐享 MCP `file_create_hyperlink` 一步到位 | [platform-specific.md](references/platform-specific.md) |
| 2 | YouTube 视频 | `scripts/yt_download_transcribe.py` | [youtube-video.md](references/youtube-video.md) |
| 2b | 含嵌入视频/播客的文章（Substack/Newsletter 等） | 提取 YouTube 链接 → `yt_download_transcribe.py` | [youtube-video.md](references/youtube-video.md) |
| 3 | 播客音频（小宇宙等）| `scripts/podcast_to_lexiang.py`（转录） + 标题文件夹归档 | [podcast-audio.md](references/podcast-audio.md) |
| 4 | PDF 文件/链接 | pymupdf 提取+裁剪 | [pdf-processing.md](references/pdf-processing.md) |
| 5 | 付费/登录墙文章 | `scripts/fetch_article.py`（Cookie/CDP） | 见下方 |
| 6 | 免费图文文章 | `scripts/fetch_article.py` | 见下方 |
| 7 | 得到 APP | `fetch_article.py --cdp` | [platform-specific.md](references/platform-specific.md) |
| 8 | SPA 动态网站 | Playwright 生成 PDF | [platform-specific.md](references/platform-specific.md) |

### fetch_article.py 用法

```bash
# 标准模式（Cookie 注入）
python3 scripts/fetch_article.py fetch "<URL>" --output-dir <项目子目录>

# CDP 模式（Substack/微博/Cloudflare 等需要完整登录态的站点）
python3 scripts/fetch_article.py fetch "<URL>" --output-dir <项目子目录> --cdp
```

**CDP 前置条件**：Chrome 已开启 `--remote-debugging-port=9222`

**产出物**：
- `<项目子目录>/<标题>.md` — Markdown 正文
- `<项目子目录>/<标题>_meta.json` — 元信息
- `<项目子目录>/images/` — 配图

> ⚠️ `web_fetch` 无法下载图片。有图片的文章**必须**用 `fetch_article.py`。

## Step 2：语言检测与翻译

读取抓取内容前 500 字符，统计中文字符占比：
- ≥ 30% → 中文，跳过翻译
- < 30% → 非中文，**必须翻译为中英对照格式**

中英对照格式：每段先英文原文，紧跟中文翻译，标题用 `## English Title / 中文标题`。

## Step 3：转存乐享知识库

> 详细的上传步骤、降级方案、图片处理见 [lexiang-upload.md](references/lexiang-upload.md)

### 操作流程（严格按顺序，不可跳步）

**步骤 0：读取配置**
- 读取 `config.json`，提取 `space_id`、`company_from`

**步骤 1：获取知识库根节点**
- `space_describe_space(space_id)` → 提取 `root_entry_id`

**步骤 2：检查/创建日期目录（🚨 先查再建）**

```
2a. entry_list_children(parent_id=root_entry_id, sort_by="sort_id", limit=5)
    → 遍历找 name=="今天日期" 且 entry_type=="folder"
    → 找到 → 复用其 ID
    → 没找到 → 步骤 2b

2b. entry_create_entry(entry_type="folder", parent_entry_id=root_entry_id, name="今天日期")
    
    🚨 创建后必须置顶：
    → entry_list_children(parent_id=root_entry_id, sort_by="sort_id", limit=1) 获取当前第一个条目 ID
    → entry_move_entry(entry_id=新目录, parent_id=root_entry_id, before=第一个条目ID)
    
    ⚠️ after="" 是排末尾（API 文档有误），禁止使用！
    ⚠️ 必须用 before=<第一个条目ID> 才能真正置顶
```

**步骤 3：去重检查**
- `entry_list_children(parent_id=日期目录ID)` → 按名称+类型检查是否已存在

**步骤 4：上传文档**

| 情况 | 方式 |
|------|------|
| 微信公众号 | `file_create_hyperlink`（一步到位，后端自动抓图文） |
| 有图片的文章（✅ 首选） | MCP connector "先全文后补图"（见 [lexiang-upload.md](references/lexiang-upload.md)） |
| 有图片的文章（备选） | `scripts/md_to_page.py --parent-id <日期目录ID> --name "标题"`（需 LEXIANG_TOKEN） |
| 纯文本 ≤30K 字符 | `entry_import_content(parent_id, name, content, content_type="markdown")` |
| **纯文本 >30K 字符（大文档）** | **`scripts/upload_doc_to_lexiang.py`**（见下方） |
| 视频/音频（仅上传文件） | `scripts/upload_video_via_openapi.py --media-type video/audio` |
| **视频转录归档（文字稿+视频）** | 创建标题文件夹 → 文字稿上传为 file → 视频作为子文档（见 [youtube-video.md](references/youtube-video.md)） |
| **播客转录归档（文字稿+音频）** | 创建标题文件夹 → 文字稿上传为 file → 音频作为子文档（见 [podcast-audio.md](references/podcast-audio.md)） |

**🚨 大文档上传策略（>30K字符）**：

Agent **禁止**通过 MCP 工具参数直接传入大段 content（会超限失败 + 上下文腐化）。

```bash
# 有 LEXIANG_TOKEN 时（最佳，创建在线文档）：
python3 scripts/upload_doc_to_lexiang.py <文件.md> \
    --parent-id <目录ID> --name "标题" --space-id <SPACE_ID>

# 无 LEXIANG_TOKEN 时（Agent 执行 3 步操作）：
python3 scripts/upload_doc_to_lexiang.py <文件.md> \
    --parent-id <目录ID> --name "标题" --mode instructions
# → 输出 JSON 指令，Agent 按指令执行 file_apply_upload → curl PUT → file_commit_upload
```

> ⚠️ **LEXIANG_TOKEN 有效期约 2 小时**，过期后 `md_to_page.py` 的图片上传全部失败（401）。MCP connector 不受 token 过期影响，因此有图片的文章**首选 MCP connector 方式**。`md_to_page.py` 仅在 token 新鲜时作为更便捷的备选。

## 脚本文件

| 脚本 | 用途 |
|------|------|
| `scripts/upload_doc_to_lexiang.py` | **通用大文档上传**：绕过 MCP 参数限制，支持在线文档/文件两种模式 |
| `scripts/podcast_to_lexiang.py` | **播客全流程**：下载→FunASR转录→Markdown→上传（一键执行） |
| `scripts/fetch_article.py` | 抓取文章（Cookie/CDP/Substack） |
| `scripts/md_to_page.py` | Markdown + 图片 → 乐享在线文档（需 LEXIANG_TOKEN） |
| `scripts/yt_download_transcribe.py` | YouTube 下载 + Whisper 转录 + 翻译 |
| `scripts/upload_video_via_openapi.py` | 视频/音频上传到乐享（VOD 路径） |
| `scripts/md_to_pdf.py` | Markdown → PDF（最终降级方案） |

## 关键约束

- 🚨 **沙箱权限与转录降级**：Whisper/torch/faster-whisper 等含 native 库的 Python 包在沙箱环境可能因 code signing 失败。**禁止静默降级**（如用 shownotes 代替逐字转录）！必须先向用户申请沙箱外执行权限（`dangerouslyDisableSandbox: true`），用户同意后再执行；仅当用户明确拒绝时才可降级处理
- 🚨 **视频/音频上传**必须用 `upload_video_via_openapi.py`（走 VOD），不用 MCP 的 `file_apply_upload`
- 🚨 **日期目录**必须先查再建，创建后必须用 `before` 置顶
- 🚨 **图片处理**贯穿全流程，`entry_import_content` / `entry_import_content_to_entry` **不会上传任何图片**。在 content 中写 `![alt](url)` 或 `<image src="url"/>` 会产生**空图片 block**（有 image 标签但无 file_id，页面显示空白），而不是跳过图片。图片只能通过 `block_apply_block_attachment_upload` → `curl PUT` → `block_create_block_descendant(image.session_id)` 三步流程上传
- 🚨 **`after=""`** 是排末尾不是置顶，禁止使用
- 🚨 **LEXIANG_TOKEN 有效期约 2 小时**，过期后 `md_to_page.py` 图片上传全部 401。有图片文章首选 MCP connector 方式

## 参考文档（按需加载）

| 文件 | 何时加载 |
|------|----------|
| [references/lexiang-upload.md](references/lexiang-upload.md) | 上传到乐享时遇到问题、需要降级方案 |
| [references/pdf-processing.md](references/pdf-processing.md) | 处理 PDF 文件（提取文字+裁剪图形） |
| [references/youtube-video.md](references/youtube-video.md) | 处理 YouTube 视频（下载+转录+翻译） |
| [references/podcast-audio.md](references/podcast-audio.md) | 处理播客音频（下载+转录） |
| [references/platform-specific.md](references/platform-specific.md) | 微信公众号/得到/SPA/微博等特定平台 |
| [references/tips-experience.md](references/tips-experience.md) | 经验总结、平台适配思路 |
| [references/troubleshooting.md](references/troubleshooting.md) | 常见问题排查 |
