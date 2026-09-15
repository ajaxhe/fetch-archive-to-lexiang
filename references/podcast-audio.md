# 播客音频处理

## 职责边界

`podcast_to_lexiang.py` 只负责 Show Notes 抓取、音频下载、FunASR 转录和标准工作包生成。
它不上传 Markdown，也不调用媒体 VOD。归档编排在脚本完成后分别调用 uploader 和 VOD
专用脚本。

## 命令

```bash
python3 scripts/podcast_to_lexiang.py "<播客链接>" \
  --output-dir <work-dir> \
  --language zh \
  --metadata-json metadata.json \
  --chapters-json chapters.json \
  --hotwords-json hotwords.json
```

脚本不再接受 `--space-id`、`--parent-entry-id` 或 `--no-upload`。

## 依赖（转录前必须先自检，见 L046）

FunASR 链路比脚本顶部注释列出的要多，缺一个就会在 import 阶段崩。启动转录前先跑：

```bash
python -c "import funasr, torchaudio, torchaudio.compliance.kaldi, omegaconf, jieba, editdistance, kaldiio, oss2, scipy, librosa"
```

全绿再启动，否则会白等一次 183MB 下载 + 14 片切分。两个已知坑：

- `torchaudio` 是 cam++ 说话人分离的硬依赖（`torchaudio.compliance.kaldi`），不能省。
  PyPI 上 torchaudio 版本低于 torch 时，用 `pip install --no-deps torchaudio==2.11.0`
  即可，无需降级 torch。
- 本机 pip 解包 sdist 会报 `EEXIST ... pip-install-*`，**不要反复重试 pip**；
  jieba / oss2 / antlr4-python3-runtime / editdistance 需手工下载解包落地（详见 L046）。

转录会拉起 torch，**必须在沙箱外执行**；沙箱内会被 SIGKILL(137)。

## Show Notes

Show Notes 必须在逐字稿之前：

```markdown
# 播客标题

> 原始链接：…

## 节目介绍

节目摘要、嘉宾介绍和时间线。

## 逐字稿

> 说明：下文按说话人分段。**主播名** 为主播，**嘉宾名** 为嘉宾。

**[00:00] 主播名：** …
**[01:20] 嘉宾名：** …
```

- 小宇宙优先从 `__NEXT_DATA__.episode.description` 提取。
- 外部 `metadata.json.shownotes` 优先于自动抓取。
- 无 `chapters.json` 时，从 Show Notes 的时间线提取章节。
- 节目级 footer 会被截断。
- 默认启用 FunASR `cam++` 说话人分离；同一说话人连续发言以及不超过 15 秒的短暂停顿
  合并为较大的自然段。开场白按最多 1200 字或 180 秒分成少数大段；对话段按最多
  1500 字或 360 秒控制，角色切换时立即断段。
- 合并同时要求 `spk` 相同；多位嘉宾不能因为都映射为 `guest` 而合并成同一段。
- **角色判定优先级（L047，2026-09-12 起）**：
  1. **开场白文本锚点**——首切片中含 `欢迎收听` / `我是主持人` / `今天的主播` 的句子，
     其说话人即主播（冷开场时嘉宾先说话，45 秒时长锚点会判反，故文本锚点优先）；
  2. **累计字数主导者 = 嘉宾**——仅当主导者字数 ≥ 次席 1.3 倍时采纳；
  3. 前两条都不成立时才退回口吻打分（`_host_score` / `_guest_score`）。
  − 少于 2 句的孤立 spk 不参与判定，跟随前一段落角色。
- 交付前必检：`guest` 平均段长应显著大于 `host`（参考量级 2–3 倍）；若接近或倒挂即为判定失败。
- **ASR 已跑完但角色判错时不要重跑转录**：`segments.json` 保留 `spk`，
  直接调用 `remap_speaker_roles` → `merge_by_speaker` → `generate_markdown` 重新生成 `source.md`；
  记得补 `meta["url"] = meta["source_url"]`，否则「原始链接」行会丢。
- `metadata.json` 提供 `host` / `guest` 时写入姓名；缺少姓名时也必须显示
  “主持人”/“嘉宾”角色标签。可用 `--no-speakers` 关闭。

## 输出

```text
<work-dir>/
├── source.md
├── meta.json
├── segments.json
├── result.json
├── <标题>.m4a|mp3|opus
├── audio_16k.wav
└── chunks/
```

`meta.json` 包含 `title/source_url/source_title/source_type/language` 和可选 `parent_id`，
并保留节目名、嘉宾、主播、日期、时长、Show Notes 等扩展字段。

`source.md` 为不可变原文。已有不同内容时脚本报错，防止覆盖。

## 内容加工与归档

- 中文：编排流程复制 `source.md` 为 `<原文标题>.md`。
- 非中文：交给 `trans-doc-to-md` Prepared Markdown Package 模式。
- 最终 Markdown：只交给 `upload-markdown-to-lexiang`。
- 音频：独立调用 VOD 脚本。

```bash
python3 scripts/upload_video_via_openapi.py "<音频路径>" \
  --space-id <SPACE_ID> \
  --parent-entry-id <标题目录ID> \
  --media-type audio
```

目标结构：

```text
日期目录/
└── <播客原文标题>/
    ├── <播客原文标题>（在线 Markdown 页面）
    └── <音频>（audio entry）
```

上传前按标题、来源 URL 和条目类型去重。

## ASR 经验

- 长音频先切为 600 秒片段。
- FunASR 热词传给 `generate(hotword="...")`。
- 无说话人信息时才从逐字 timestamp 按标点切自然段；有 `sentence_info` 时以说话人
  切换为主边界，并合并连续发言。
- 转录任务可后台执行，但完成标志是 `source.md` 和 `meta.json` 同时存在。
- torch code signing 失败时申请允许的沙箱外执行，不得静默降级为 Show Notes。
