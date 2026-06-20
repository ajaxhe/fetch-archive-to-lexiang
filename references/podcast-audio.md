#### 播客音频处理（转录脚本 + 标题文件夹归档）

**当用户提供播客链接时**（小宇宙FM `xiaoyuzhoufm.com`、Apple Podcasts 等），**直接调用脚本完成转录**，然后按标题文件夹结构归档到乐享。

**⚠️ 核心原则**：
- 所有转录逻辑已固化在 `scripts/podcast_to_lexiang.py` 中
- Agent 只做 4 件事：WebFetch 获取元信息 → 准备 JSON 配置 → 调用脚本转录 → 按标题文件夹结构上传乐享
- **禁止**在 Agent 对话中内联转录代码或逐步推理 ASR 逻辑

**🚨 乐享目录结构（与视频转录一致）**：

```
贾维斯知识库/
└── 2026-06-03/                        ← 日期目录
    └── <播客标题>/                     ← 标题文件夹
        ├── 文字稿.md（file entry）     ← 主内容：转录文字稿（预签名 URL 上传）
        └── 音频.m4a（audio entry）     ← 原始音频文件（VOD 路径上传）
```

---

## Agent 操作步骤

### Step 1: WebFetch 获取播客元信息

从播客页面提取：标题、节目名、嘉宾、主播、发布日期、时长、章节时间线

### Step 2: 准备 3 个 JSON 文件

**metadata.json**（必须）:
```json
{
  "title": "播客标题",
  "show_name": "节目名",
  "guest": "嘉宾",
  "host": "主播",
  "date": "2026-05-26",
  "duration": "139分钟",
  "platform": "小宇宙FM",
  "url": "https://..."
}
```

**chapters.json**（推荐，有则章节对齐）:
```json
[
  {"time": 120, "title": "章节标题1"},
  {"time": 410, "title": "章节标题2"}
]
```

**hotwords.json**（推荐，提升专有名词准确率）:
```json
[
  {"word": "雨森", "weight": 25},
  {"word": "戴雨森", "weight": 25},
  {"word": "张小珺", "weight": 20},
  {"word": "Anthropic", "weight": 20},
  {"word": "Claude Code", "weight": 18}
]
```

热词来源：
- **人名**（权重 20-25）：嘉宾、主播、被提及的人
- **产品/公司名**（权重 15-20）：shownotes 中的专有名词
- **核心概念**（权重 10-15）：章节标题中的关键术语

### Step 3: 调用脚本（nohup 后台执行）

```bash
# 因为转录耗时长（139分钟音频约10分钟），必须 nohup 后台运行
cd <工作目录> && nohup /usr/bin/python3 \
  <skill_dir>/scripts/podcast_to_lexiang.py \
  "<播客链接>" \
  --output-dir ./output \
  --language zh \
  --metadata-json ./metadata.json \
  --chapters-json ./chapters.json \
  --hotwords-json ./hotwords.json \
  --no-upload \
  > transcribe_log.txt 2>&1 &
```

### Step 4: 等待完成后上传（标题文件夹结构）

**🚨 乐享目录结构（与视频转录一致）**：

```
贾维斯知识库/
└── 2026-06-03/                        ← 日期目录
    └── <播客标题>/                     ← 标题文件夹
        ├── 文字稿.md（file entry）     ← 主内容：转录文字稿
        └── 音频.m4a（audio entry）     ← 原始音频文件
```

**上传流程**：

```bash
# 1. 检查是否完成
grep "全部完成\|✅ 转录完成" transcribe_log.txt

# 2. 获取/创建日期目录（先查再建，创建后 before 置顶）
#    → entry_list_children(root_entry_id) 查找今日目录
#    → 找不到则 entry_create_entry(folder) + entry_move_entry(before=第一个)

# 3. 在日期目录下创建「标题文件夹」
#    → entry_create_entry(entry_type="folder", parent_entry_id=<日期目录ID>, name="<播客标题>")

# 4. 上传文字稿到标题文件夹（大文档预签名 URL 方式）
#    → file_apply_upload(parent_entry_id=<标题文件夹ID>, name="<标题>.md", ...)
#    → curl PUT 上传 .md 文件
#    → file_commit_upload 确认

# 5. 上传音频到标题文件夹（VOD 路径）
python3 scripts/upload_video_via_openapi.py <音频.m4a> \
    --space-id <SPACE_ID> --parent-entry-id <标题文件夹ID> --media-type audio
```

**要点**：
- 文字稿和音频放在同一个标题文件夹下，逻辑绑定
- 文字稿用预签名 URL 上传（file entry），支持全文搜索
- 音频用 OpenAPI VOD 路径上传（audio entry），乐享可在线播放

---

## 技术架构和已知经验

### ASR 模型
- **FunASR Paraformer-zh + CT-Punc**（中文准确率 95.7%，标点正确率 92.3%）
- 降级方案：Whisper base（准确率较低，无标点）

### 关键技术决策

| 问题 | 解决方案 | 踩坑记录 |
|------|----------|----------|
| 长音频合并为1段 | 预切片 600s/片 → 逐片转录 | FunASR merge_vad=True 对整段音频会合并全部 |
| 热词不生效 | `generate(hotword="词1 词2")` | `AutoModel(hotword=file)` 是 contextual 模型专用，paraformer-zh 不支持 |
| 无分段/时间戳 | 从逐字 timestamp 按标点切分 | FunASR 返回 `timestamp: [[start_ms, end_ms], ...]` 逐字 |
| torch code signing | 用系统 Python `/usr/bin/python3` | managed Python 的 torch.dylib 签名不匹配 |
| 脚本超时 | `nohup ... &` 后台运行 | WorkBuddy Bash 超时约 2min，139min 音频需 ~10min |
| 大文档上传失败 | 预签名 URL 上传 .md 文件 | MCP content 参数限制约 30K 字符 |
| 标点丢失 | FunASR 内置 ct-punc 模型 | Whisper base 中文几乎无标点输出 |
| 专有名词错误 | 热词偏置 + 后处理替换（可选） | "雨森"→"宇森" 等同音字 |

### 依赖

```bash
# 系统 Python (/usr/bin/python3) 已安装:
# funasr 1.3.9, torch 2.8.0, torchaudio, modelscope, opencc, yt-dlp, ffmpeg
```

### 输出文件

| 文件 | 说明 |
|------|------|
| `output/<标题>.m4a` | 原始音频 |
| `output/audio_16k.wav` | WAV 转换 |
| `output/chunks/chunk_*.wav` | 切片文件 |
| `output/segments.json` | ASR 分段结果（带时间戳） |
| `output/<标题>.md` | 最终 Markdown 文字稿 |
| `output/result.json` | 执行结果摘要 |
