---
name: fetch-archive-to-lexiang
version: "4.6.0"
author: ajaxhe
license: MIT
category: research
description: Import WeChat Official Account articles through Lexiang's native MCP interface; discover and fetch other articles, videos, podcasts, and PDFs into standardized source packages, then orchestrate deduplicated archival. 微信公众号文章使用乐享 MCP 原生导入；其他来源经侦察、抓取和标准工作包编排归档。
tags: fetch, archive, wechat, youtube, podcast, pdf, transcribe, lexiang, paywall, substack, medium, arxiv
disable-model-invocation: false
requires:
  skills:
    - name: trans-doc-to-md
      version: ">=3.0.0,<4.0.0"
    - name: upload-markdown-to-lexiang
      version: ">=1.1.0,<2.0.0"
  binaries:
    - python3
    - yt-dlp
  python:
    - playwright
    - pymupdf
    - openai-whisper
    - funasr>=1.3.2
---

# 抓取来源并编排乐享归档

本 Skill 只负责：

1. 来源侦察和抓取方式选择。
2. 网页抓取、视频/播客下载与转录。
3. 生成统一工作包。
4. 乐享目录、去重和视频/音频 VOD 编排。

本 Skill 不负责：

- 非中文 Markdown 的清洗、翻译和完整性验证：统一委托
  `trans-doc-to-md` 的 **Prepared Markdown Package** 模式。
- 任何 Markdown 页面写入：统一委托 `upload-markdown-to-lexiang`。
- 在上传后用 MCP 二次渲染正常富元素：uploader 直接渲染
  `trans-doc-to-md` 标注。

## 强制边界

1. `source.md` 是不可变原文；若同目录已有不同内容，必须换工作目录，禁止覆盖。
2. 禁止摘要替代原文，禁止丢失图片、Show Notes 或转录内容。
3. 最终 Markdown 文件名必须是原文标题；文件名非法字符可安全替换，但 `meta.json`
   中的 `title` 和 `source_title` 必须保留原始标题。
4. 中文来源可由编排流程把 `source.md` 复制为 `<原文标题>.md`；抓取脚本不自行决定。
5. 非中文来源必须先交给 `trans-doc-to-md`，不得在本 Skill 或当前 Agent
   内实现翻译。
6. Markdown 页面只用 uploader 写入，不得恢复任何旧导入、文件上传或本地上传器副本。
7. 视频和音频继续使用 `scripts/upload_video_via_openapi.py` 的 VOD 路径。
8. 上传后少量人工增量修复仅是异常维护路径；每次修复必须同步本地最终 Markdown。
9. `mp.weixin.qq.com` 文章是强制例外：只调用乐享 MCP
   `file_create_hyperlink` 原生导入，禁止浏览器/WebFetch/脚本抓取，禁止生成工作包，
   禁止调用 Markdown uploader；接口失败时报告错误并停止，不得静默回退抓取。

## 统一工作包

```text
<work-dir>/
├── source.md               # 不可变原文
├── images/                 # 可选，引用路径保持相对
├── meta.json
└── <原文标题>.md           # 编排完成后的最终 Markdown
```

`meta.json` 标准字段：

```json
{
  "title": "归档标题",
  "display_title": "原文标题 / 中文标题",
  "source_url": "https://...",
  "source_title": "原文标题",
  "source_type": "article|youtube|podcast|pdf",
  "language": "zh|en|...",
  "parent_id": "可选的目标目录 ID"
}
```

允许保留作者、日期、时长、媒体文件等扩展字段。

## Step 0：预检与来源侦察

1. 阅读 `references/lessons-learned.md` 中全部 P0 教训。
2. **先按 URL 路由**：host 为 `mp.weixin.qq.com` 时直接进入 Step 1 的
   “微信公众号强制分支”；不得打开页面侦察正文或进入任何抓取逻辑。
3. 非微信来源才侦察标题、作者、日期、语言、长度、图片数、媒体时长、付费墙和登录墙。
4. 非微信网页有图片必须用抓取脚本下载，不能只依赖 WebFetch。
5. 网页抓取默认使用 CDP：先检查已配置端口（默认 9222，实际端口记录在
   `~/.fetch_article/cdp_port`）和有效 page target，复用已有浏览器上下文与登录态，
   并在其中新开任务标签页；端口未启动时主动启动 CDP Chrome。CDP 连接失败
   必须退出，禁止静默回退到无登录态的 Testing Chrome。只有用户明确要求隔离浏览器时
   才使用 `--no-cdp`。
6. 非微信来源确定新的独立工作目录，避免覆盖已有 `source.md`。

平台细节见 `references/platform-specific.md`。

## Step 1：抓取并生成工作包

| 来源 | 处理方式 |
|---|---|
| 微信公众号 (`mp.weixin.qq.com`) | 强制调用乐享 MCP `file_create_hyperlink`；不抓取、不建工作包、不上传 Markdown |
| 免费/付费网页 | `scripts/fetch_article.py fetch "<URL>" --output-dir <DIR>`（默认 CDP） |
| YouTube | `scripts/yt_download_transcribe.py "<URL>" --output-dir <DIR>` |
| 播客 | `scripts/podcast_to_lexiang.py "<URL>" --output-dir <DIR>` |
| PDF / 乐享 PDF | 准备 PDF/解析原文后交给 `trans-doc-to-md` |

### 微信公众号强制分支

1. 按 Step 3 的目标规则获取知识库根目录，查询并复用当天 `YYYY-MM-DD` folder。
2. 在当天目录内按来源 URL 和规范化标题去重；同一 URL 已存在时复用现有条目，
   不重复导入。
3. 调用乐享 MCP `file_create_hyperlink`：

```text
url = "https://mp.weixin.qq.com/s/..."
parent_entry_id = "<当天目录 entry_id>"
name = "<可选；已可靠获知标题时才传，禁止为取标题而抓取正文>"
```

4. 必须验证调用成功且返回 `entry.id`；可见响应字段允许时，同时确认
   `entry_type == "flink"`、`extension == "wechat"`。
5. 该分支到此结束，直接执行 Step 4 的微信自检。**跳过工作包生成、Step 2 内容加工、
   uploader 和 block 二次写入。** 接口不可用、返回失败或验证不通过时，报告错误并停止；
   不得调用 `fetch_article.py`、WebFetch、Playwright/CDP 或通用网页导入作为降级。

三个抓取/转录脚本均以 `source.md` + `meta.json` 为标准输出。YouTube 和播客同时保留
下载媒体、ASR 中间产物；它们不翻译、不上传 Markdown。

网页抓取默认使用快速保真模式：Substack 以 `domcontentloaded` + 正文条件等待替代固定
等待，图片并行下载，调试截图默认关闭（排障时显式加 `--debug-screenshot`）。
`meta.json.verification` 必须满足 `ok=true`、图片引用/本地文件对账一致且
`platform_noise_hits=[]`；Agent 优先读取该紧凑报告，校验通过时不要为重复确认而读取整篇
`source.md`，以减少 Token 消耗。

## Step 2：内容加工

微信公众号强制分支跳过本步骤。

读取 `meta.json.language`：

- 中文：验证 `source.md` 完整后，由编排流程复制为 `<原文标题>.md`。
- 非中文或语言不确定：调用 `trans-doc-to-md` 的
  **Prepared Markdown Package** 模式，输入整个工作包。该 Skill 负责清洗、双语翻译、
  图片/富元素保真和完整性验证，并输出 `<原文标题>.md`。

不得修改 `source.md`。最终 Markdown 必须继续使用相对图片路径。

## Step 3：乐享目录、去重与上传

目标优先级：用户指定 > 工作区规则 > 本 Skill 的 gitignored `config.json` > 初始化。

微信公众号只执行本步骤的目录定位与导入前去重，随后使用 Step 1 的
`file_create_hyperlink`；不得进入下方 Markdown uploader 流程。

1. 获取目标知识库 `root_entry_id`。
2. 查询并复用当天 `YYYY-MM-DD` folder；不存在才创建，使用
   `before=<当前第一条目 ID>` 置顶。
3. 视频/播客在日期目录下查询并复用 `<原文标题>` 文件夹。
4. 在目标目录内按规范化标题、来源 URL 和条目类型去重；确认是同一来源后才覆盖。
5. 上传前记录目标目录子条目快照；本次任务只允许新增或更新“最终 Markdown 页面 +
   VOD 媒体”各一条。诊断上传必须使用 `--dry-run`，禁止创建 `upload test`、`v2`、
   `中英对照`等试验条目。
6. 调用 uploader：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" upload \
  "<work-dir>/<原文标题>.md" \
  --parent-id "<目标目录ID>" \
  --name "<meta.display_title；中文来源回退 meta.title>" \
  --pin \
  --json
```

uploader 版本必须满足 `>=1.1.0,<2.0.0`。它直接渲染
`trans-doc-to-md` 的 callout、表格和图片标注，并完成线上对账。

非中文来源发布时禁止追加“中英对照”“双语版”等机械后缀。页面名称必须直接使用
`trans-doc-to-md` 生成的 `meta.json.display_title`，格式为
`Original Title / 中文标题`；最终 Markdown 不得保留与页面名称重复的文档级 H1。

视频/音频在 Markdown 上传成功后独立归档：

```bash
python3 scripts/upload_video_via_openapi.py "<媒体文件>" \
  --space-id "<SPACE_ID>" \
  --parent-entry-id "<标题目录ID>" \
  --media-type video
```

音频使用 `--media-type audio`。不得用普通文件上传替代 VOD。

访谈类 YouTube 和播客默认启用说话人分离。YouTube 使用 Whisper 保留文本质量，
同时用 SenseVoiceSmall + CAM++ 提供说话人时间区间，再按时间重叠映射并合并：

- 说话人切换是首要段落边界；同一人跨不超过 15 秒的停顿继续合并。
- 开场白按最多 1400 字符或 180 秒形成少数大段；对话段最多 1800 字符或 360 秒。
- 有姓名显示姓名；缺少姓名也必须显示“主持人”/“嘉宾”。
- 多位嘉宾不能仅因都属于 `guest` 就合并；合并必须同时保持同一 `spk`。
- 只有非访谈内容或用户明确接受无角色文字稿时才使用 `--no-speakers`。

## Step 4：交付自检

```text
□ source.md 未被修改，且不是摘要
□ meta.json 标准字段完整，原文标题与来源 URL 可追溯
□ meta.json.verification.ok == true；优先依据紧凑报告完成抓取自检，避免重复通读全文
□ 作者与发布日期来自 canonical meta/time/JSON-LD，并在最终文档顶部只展示一次
□ images/ 中引用文件完整，图文顺序保留
□ 订阅引导、相关推荐、newsletter disclaimer、页脚图片等平台噪音已在抓取转 MD 时过滤
□ 非中文包已通过 trans-doc-to-md 完整性验证
□ 最终文件名为原文标题
□ 非中文页面名为“原文标题 / 中文标题”，没有“中英对照”等机械后缀
□ 最终 Markdown 与线上正文均不含和页面名称重复的首个文档级 H1
□ uploader verified == true，local_images == remote_images
□ 富元素由 uploader 直接渲染，无常规 MCP 二次渲染
□ 文档目录、去重结果和 VOD 媒体目录正确
□ 人工增量修复已同步本地最终 Markdown
□ 浏览器抓取复用了 CDP 上下文；未启动 Google Chrome for Testing
□ 播客：同说话人连续发言与短暂停顿已合并为大段；开场白只有少数大段
□ 播客：每段明确标注“主持人/嘉宾”（有姓名则用姓名）；开场白未与第一问粘连
□ 访谈视频：CAM++ 说话人区间已映射到 Whisper 文本；连续同一 spk 已合并
□ 访谈视频：主持人/嘉宾标签完整；多位嘉宾没有因同属 guest 被误合并
□ 新建页面上传失败时已自动回滚，不在日期目录或知识库留下临时空页面
□ 上传后目标目录与上传前快照对账，仅保留最终页面和 VOD；无 test/v2/空白/重复条目
□ 微信公众号：只调用 file_create_hyperlink，未启动浏览器/WebFetch/抓取脚本
□ 微信公众号：未生成工作包、未调用 trans-doc-to-md 或 Markdown uploader
□ 微信公众号：返回 entry.id；可见字段允许时 entry_type=flink、extension=wechat
□ 微信公众号：当天目录内来源 URL 唯一；失败时已停止且未回退抓取
□ Substack：正文提取、图片枚举和 Markdown 转换都锁定 `.available-content`，未因 `article`/`main` 更长而混入评论、Recent Episodes 或页脚
□ Substack：标题优先取带 `datePublished` 的 JSON-LD `headline`，未把嘉宾名或正文小标题误作文章标题
□ 页面展示名不超过乐享 150 字符限制；超长双语标题只缩短展示名，`meta.title`、`source_title` 和最终 Markdown 文件名仍保留完整原题
```

## Step 5：自省

用户指出错误、自检失败、发现新平台规律或同类问题再次出现时，更新
`references/lessons-learned.md`。历史根因可保留，但必须明确其旧方案已废弃。

问题归属：

- 抓取、转录、工作包、目录/去重/VOD：本 Skill。
- 微信公众号 MCP 原生导入、目录与去重：本 Skill。
- 清洗、翻译、富元素识别、完整性：`trans-doc-to-md`。
- Markdown 渲染、页面写入和线上对账：`upload-markdown-to-lexiang`。

## 脚本边界

| 脚本 | 职责 |
|---|---|
| `fetch_article.py` | 网页抓取，生成 `source.md`、`images/`、`meta.json` |
| `yt_download_transcribe.py` | YouTube 下载、转录、Show Notes、标准工作包 |
| `podcast_to_lexiang.py` | 播客下载、转录、Show Notes、标准工作包 |
| `lexiang_pdf_parse.py` | 乐享 PDF 来源解析桥接 |
| `upload_video_via_openapi.py` | 视频/音频 VOD 上传 |
| `md_to_pdf.py` | 用户明确要求时生成 PDF |

本 Skill 不包含翻译脚本或 Markdown → 乐享 page 上传脚本。

## 参考文档

- `references/lexiang-upload.md`
- `references/pdf-processing.md`
- `references/youtube-video.md`
- `references/podcast-audio.md`
- `references/platform-specific.md`
- `references/troubleshooting.md`
- `references/lessons-learned.md`
