# YouTube / 嵌入视频

## 职责边界

`yt_download_transcribe.py` 只负责：

1. yt-dlp 获取元信息和下载视频。
2. ffmpeg 提取音频。
3. Whisper 转录；访谈类视频默认用 SenseVoiceSmall + CAM++ 提供说话人区间。
4. 保留 YouTube description 作为视频介绍。
5. 生成标准 `source.md` 和 `meta.json`。

它不翻译、不生成最终双语稿、不上传 Markdown。旧 `--skip-translate` 仅兼容旧命令，
会提示 deprecated。

## 命令

```bash
python3 scripts/yt_download_transcribe.py "<YouTube URL>" \
  --output-dir <work-dir> \
  --whisper-model base \
  --host "主持人姓名" \
  --guest "嘉宾姓名"
```

常用参数：

- `--whisper-model tiny|base|small|medium|large`
- `--skip-download`
- `--keep-audio`
- `--cookies-from-browser chrome`
- `--host` / `--guest`：可选姓名；缺省仍显示“主持人”/“嘉宾”
- `--no-speakers`：仅非访谈内容或明确接受无角色文字稿时使用

## 输出

```text
<work-dir>/
├── source.md
├── meta.json
└── <视频标题>.mp4
```

`source.md` 结构为元信息、`## 视频介绍`、`## 逐字稿`。转录段落含时间戳，不插入翻译
emoji，也不在每段之间插入分隔线。访谈默认格式：

```markdown
> 说明：下文按说话人分段。**主持人** 为主持人，**嘉宾** 为嘉宾。

**[00:00] 主持人：** 开场白……

**[03:10] 嘉宾：** 连续回答……
```

Whisper 负责高质量文本，SenseVoiceSmall + CAM++ 只提供说话人时间区间。脚本按时间
重叠把 `spk` 映射到 Whisper segment，再以说话人切换为首要边界合并：

- 同一 `spk` 跨 ≤15 秒停顿继续合并。
- 开场白最多 1400 字符或 180 秒；对话段最多 1800 字符或 360 秒。
- 多位嘉宾即使角色都为 `guest`，不同 `spk` 也不能合并。
- CAM++ 不可用或没有 `sentence_info` 时直接失败，不静默退化；显式
  `--no-speakers` 才允许生成无角色文字稿。

`meta.json` 包含标准字段：

- `title`
- `source_url`
- `source_title`
- `source_type: youtube`
- `language`

以及频道、发布日期、时长、缩略图、媒体路径等扩展字段。

如果目标目录已有内容不同的 `source.md`，脚本报错，要求使用新目录。

## 内容加工

- 中文转录：编排流程确认完整后复制为 `<原文标题>.md`。
- 非中文转录：把整个工作包交给 `trans-doc-to-md` 的
  Prepared Markdown Package 模式，生成最终 `<原文标题>.md`。

## 乐享归档

```text
日期目录/
└── <视频原文标题>/
    ├── <视频原文标题>（在线 Markdown 页面）
    └── <视频文件>（video entry）
```

1. 查询并复用日期目录和标题目录。
2. 按标题、来源 URL 和类型去重。
3. 最终 Markdown 只交给 `upload-markdown-to-lexiang`。
4. 视频独立调用 VOD 脚本：

```bash
python3 scripts/upload_video_via_openapi.py "<视频路径>.mp4" \
  --space-id <space_id> \
  --parent-entry-id <标题目录ID> \
  --media-type video
```

VOD 必须使用 `/cgi-bin/v1/kb/files/upload-params` 签名并创建 `entry_type=video`；
普通文件上传不会触发转码。

## 依赖

- `yt-dlp`
- `openai-whisper`（仅本地 Whisper 包名，不使用 OpenAI 翻译 API）
- `funasr>=1.3.2`（SenseVoiceSmall + CAM++ 说话人分离）
- `ffmpeg`

沙箱中若 torch/native 库签名失败，应申请允许的沙箱外执行；不得用 Show Notes 冒充转录。
