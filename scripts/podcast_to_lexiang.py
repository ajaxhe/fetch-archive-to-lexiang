#!/usr/bin/env python3
"""播客音频处理脚本：抓取 Show Notes → 下载 → ASR 转录 → 生成标准工作包。

核心设计原则：
- 所有操作固化在脚本中，Agent 只需准备 JSON 配置文件 + 一行命令调用
- 长音频预切片 → 逐片段转录 → 说话人分离与连续发言合并 → 章节对齐
- 热词通过 generate(hotword="词1 词2") 传入，提升专有名词准确率
- 本脚本不上传 Markdown 或媒体；归档编排分别调用 uploader 和 VOD 专用脚本

用法：
  # 完整流程（下载 + 转录 + 生成 Markdown）
  python3 podcast_to_lexiang.py "<播客链接>" \\
      --output-dir ./output \\
      --language zh \\
      --metadata-json metadata.json \\
      --chapters-json chapters.json \\
      --hotwords-json hotwords.json

依赖安装（首次使用）：
  pip install funasr torch torchaudio modelscope yt-dlp opencc-python-reimplemented

已知经验和踩坑记录：
  1. FunASR 热词必须通过 generate(hotword="词1 词2") 传入，不能放 AutoModel 构造函数
  2. 长音频（>10分钟）必须预切片再逐片段转录，否则 FunASR 会合并为一整段
  3. 切片大小建议 600s（10分钟），ffmpeg -f segment -segment_time 600
  4. 有 sentence_info 时以说话人切换为主边界；无说话人信息时才按标点切分
  5. 系统 Python (/usr/bin/python3) 可用，managed Python 的 torch 有 code signing 问题
  6. 脚本执行时间较长（139分钟音频约10分钟），建议 nohup 后台运行
"""
from __future__ import annotations

import argparse
import html as html_module
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


# 节目级 boilerplate，shownotes 中截断点（保留介绍 + 本期剧透，去掉重复 footer）
_SHOWNOTES_CUT_MARKERS = (
    "听友来信", "收听渠道", "新节目指路", "关于我们",
    "展开Show Notes", "打开小宇宙查看更多精彩评论",
)
_SHOWNOTES_SECTION_HEADERS = ("本期剧透", "时间线", "章节", "Shownotes", "Show Notes")


# ============================================================
# 0. 抓取 Show Notes / 元信息
# ============================================================
def _http_get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_xiaoyuzhou_metadata(url: str) -> dict:
    """从小宇宙 episode 页 __NEXT_DATA__ 提取 shownotes 与元信息。"""
    page = _http_get(url)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.DOTALL)
    if not m:
        return {}
    data = json.loads(m.group(1))
    ep = data.get("props", {}).get("pageProps", {}).get("episode") or {}
    if not ep:
        return {}

    pod = ep.get("podcast") or {}
    duration_sec = ep.get("duration") or 0
    pub = (ep.get("pubDate") or "")[:10]
    shownotes = (ep.get("description") or "").strip()
    if not shownotes and ep.get("shownotes"):
        shownotes = html_module.unescape(re.sub(r"<[^>]+>", "\n", ep["shownotes"]))
        shownotes = re.sub(r"\n{3,}", "\n\n", shownotes).strip()

    return {
        "title": ep.get("title"),
        "show_name": pod.get("title"),
        "shownotes": shownotes,
        "description": shownotes,
        "date": pub,
        "duration": f"{duration_sec // 60}分钟" if duration_sec else "",
        "platform": "小宇宙FM",
        "url": url,
    }


def fetch_ytdlp_metadata(url: str) -> dict:
    """yt-dlp JSON 作为通用 fallback（description 常为节目级简介，信息量有限）。"""
    cmd = ["yt-dlp", "--dump-json", "--no-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {}
    try:
        info = json.loads(result.stdout.strip().split("\n")[0])
    except (json.JSONDecodeError, IndexError):
        return {}

    desc = (info.get("description") or "").strip()
    upload_date = info.get("upload_date") or ""
    if len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    duration = info.get("duration") or 0
    return {
        "title": info.get("title") or info.get("fulltitle"),
        "show_name": info.get("uploader") or info.get("channel"),
        "shownotes": desc,
        "description": desc,
        "date": upload_date,
        "duration": f"{duration // 60}分钟" if duration else "",
        "platform": info.get("extractor_key", ""),
        "url": info.get("webpage_url") or url,
    }


def fetch_episode_metadata(url: str) -> dict:
    """按平台抓取 episode 元信息与 shownotes。"""
    if "xiaoyuzhoufm.com" in url:
        meta = fetch_xiaoyuzhou_metadata(url)
        if meta.get("shownotes"):
            return meta
    return fetch_ytdlp_metadata(url)


def merge_metadata(base: dict, fetched: dict) -> dict:
    """页面抓取结果填空白；metadata.json / Agent 手工字段优先。"""
    merged = dict(fetched)
    merged.update({k: v for k, v in base.items() if v not in (None, "", [], {})})
    if not merged.get("shownotes") and base.get("description"):
        merged["shownotes"] = base["description"]
    elif not merged.get("shownotes") and fetched.get("description"):
        merged["shownotes"] = fetched["description"]
    return merged


def trim_shownotes_boilerplate(text: str) -> str:
    """去掉节目级 footer（听友来信、关于我们等），保留介绍与本期剧透。"""
    if not text:
        return ""
    cut_at = len(text)
    for marker in _SHOWNOTES_CUT_MARKERS:
        idx = text.find(marker)
        if 0 < idx < cut_at:
            cut_at = idx
    return text[:cut_at].strip()


def parse_time_to_seconds(time_str: str) -> int:
    parts = time_str.strip().split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0


def extract_chapters_from_shownotes(text: str) -> list[tuple[int, str]]:
    """从 shownotes 时间线提取章节，如「1、09:36 标题」。"""
    chapters: list[tuple[int, str]] = []
    for line in text.split("\n"):
        line = line.strip()
        m = re.match(
            r"^\d+[、.]?\s*(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$",
            line,
        )
        if m:
            chapters.append((parse_time_to_seconds(m.group(1)), m.group(2).strip()))
    return chapters


def format_shownotes_markdown(shownotes: str) -> str:
    """将 shownotes 格式化为「节目介绍」区块（位于逐字稿之前）。"""
    text = trim_shownotes_boilerplate(shownotes)
    if not text:
        return ""

    lines = ["## 节目介绍", ""]
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        if para in _SHOWNOTES_SECTION_HEADERS:
            lines.extend(["", f"### {para}", ""])
        else:
            lines.extend([para, ""])

    return "\n".join(lines).strip()


# ============================================================
# 1. 下载音频
# ============================================================
def download_audio(url: str, output_dir: Path) -> Path:
    """使用 yt-dlp 下载播客音频。已存在则跳过。"""
    print(f"\n{'='*60}")
    print(f"[1/4] 下载音频: {url}")
    print(f"{'='*60}", flush=True)

    output_dir.mkdir(parents=True, exist_ok=True)

    # 检查已有文件（避免重复下载）
    existing = list(output_dir.glob("*.m4a")) + list(output_dir.glob("*.mp3")) + list(output_dir.glob("*.opus"))
    if existing:
        audio_path = max(existing, key=lambda f: f.stat().st_mtime)
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        print(f"📌 已存在音频文件，跳过下载: {audio_path.name} ({size_mb:.1f} MB)")
        return audio_path

    cmd = ["yt-dlp", "--no-playlist", "-o", str(output_dir / "%(title)s.%(ext)s"), url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 下载失败: {result.stderr[-500:]}")
        sys.exit(1)

    audio_files = list(output_dir.glob("*.m4a")) + list(output_dir.glob("*.mp3")) + list(output_dir.glob("*.opus"))
    if not audio_files:
        print("❌ 未找到下载的音频文件")
        sys.exit(1)

    audio_path = max(audio_files, key=lambda f: f.stat().st_mtime)
    size_mb = audio_path.stat().st_size / (1024 * 1024)
    print(f"✅ 下载完成: {audio_path.name} ({size_mb:.1f} MB)")
    return audio_path


# ============================================================
# 2. 音频预处理（转WAV + 切片）
# ============================================================
def prepare_audio(audio_path: Path, output_dir: Path, chunk_seconds: int = 600) -> tuple[Path, list[Path]]:
    """转换为 WAV 16kHz 单声道，并切成固定时长的片段。"""
    print(f"\n{'='*60}")
    print(f"[2/4] 音频预处理: WAV转换 + 切片({chunk_seconds}s/片)")
    print(f"{'='*60}", flush=True)

    wav_path = output_dir / "audio_16k.wav"
    chunks_dir = output_dir / "chunks"

    # 转 WAV（如已存在则跳过）
    if not wav_path.exists():
        cmd = ["ffmpeg", "-i", str(audio_path), "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "-y", str(wav_path)]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"✅ WAV 转换完成: {wav_path.stat().st_size / (1024*1024):.1f} MB")
    else:
        print(f"📌 WAV 已存在，跳过转换")

    # 切片（如已存在则跳过）
    if not chunks_dir.exists() or not list(chunks_dir.glob("*.wav")):
        chunks_dir.mkdir(exist_ok=True)
        cmd = ["ffmpeg", "-i", str(wav_path), "-f", "segment", "-segment_time", str(chunk_seconds), "-c", "copy", str(chunks_dir / "chunk_%03d.wav")]
        subprocess.run(cmd, capture_output=True, check=True)

    chunk_files = sorted(chunks_dir.glob("chunk_*.wav"))
    print(f"✅ 切片完成: {len(chunk_files)} 个片段 (每片 {chunk_seconds}s)")
    return wav_path, chunk_files


# ============================================================
# 3. ASR 转录（FunASR 分片 + 热词 + 标点切分）
# ============================================================
def _host_score(text: str) -> float:
    t = (text or "").strip()
    if not t:
        return 0.0
    score = 0.0
    for m in ("你们", "你觉得", "你怎么", "你说的", "能不能", "为什么要",
              "为什么没有", "我想问", "欢迎收听", "正式进入", "今天的主播"):
        if m in t:
            score += 2.0
    t_wo = t.replace("对吧？", "").replace("对吧?", "")
    if t_wo.endswith("？") or t_wo.endswith("?"):
        score += 1.5 if len(t) < 40 else 0.5
    return score


def _guest_score(text: str) -> float:
    t = (text or "").strip()
    if not t:
        return 0.0
    score = 0.0
    for m in ("我们公司", "我们模型", "我们团队", "我们发了", "我们做",
              "对我们来说", "我们内部", "我们意识到", "坦白说"):
        if m in t:
            score += 2.0
    if len(t) > 40:
        score += 0.5
    return score


def remap_speaker_roles(sentences: list[dict], chunk_seconds: int = 600,
                        intro_end: float | None = None) -> list[dict]:
    """将 cam++ 本地 spk id 映射为 host/guest。

    访谈播客跨 chunk 时 spk 编号会重置，需按口吻打分；开场白强制为主播。
    """
    if not sentences:
        return sentences

    if intro_end is None:
        # 默认：含「正式进入」的句子结束处；否则取前 2 分钟
        intro_end = 120.0
        for s in sentences:
            if "正式进入" in (s.get("text") or "") or "欢迎收听" in (s.get("text") or ""):
                intro_end = max(intro_end, float(s.get("end") or 0))
        intro_end = min(intro_end + 1.0, 180.0)

    from collections import defaultdict
    by_chunk: dict[int, list[dict]] = defaultdict(list)
    for s in sentences:
        by_chunk[int(float(s["start"]) // chunk_seconds)].append(s)

    first_chunk_index = min(by_chunk)
    first_chunk = by_chunk[first_chunk_index]
    intro_seed_end = min(intro_end, 45.0)
    intro_durations: dict[int, float] = defaultdict(float)
    for s in first_chunk:
        if float(s["start"]) >= intro_seed_end:
            continue
        sid = int(s.get("spk", 0))
        intro_durations[sid] += max(0.0, float(s["end"]) - float(s["start"]))
    intro_host_sid = (
        max(intro_durations, key=intro_durations.get)
        if intro_durations
        else int(first_chunk[0].get("spk", 0))
    )

    for ci, chunk in sorted(by_chunk.items()):
        spk_ids = sorted({int(s.get("spk", 0)) for s in chunk})
        if len(spk_ids) == 1:
            text = "".join(x["text"] for x in chunk)
            role = (
                "host"
                if ci == first_chunk_index and spk_ids[0] == intro_host_sid
                else ("host" if _host_score(text) > _guest_score(text) else "guest")
            )
            for s in chunk:
                s["role"] = role
            continue
        scores = {}
        for sid in spk_ids:
            segs = [x for x in chunk if int(x.get("spk", 0)) == sid]
            hs = sum(_host_score(x["text"]) for x in segs)
            gs = sum(_guest_score(x["text"]) for x in segs)
            q_short = sum(
                1 for x in segs
                if ("？" in x["text"] or "?" in x["text"])
                and "对吧" not in x["text"]
                and len(x["text"]) < 40
            )
            scores[sid] = hs - gs + q_short * 1.5
        if ci == first_chunk_index:
            scores[intro_host_sid] += 100.0
        ranked = sorted(spk_ids, key=lambda sid: scores[sid], reverse=True)
        host_sid = ranked[0]
        host_spks = {host_sid}
        if ci == first_chunk_index:
            if len(ranked) > 1 and scores[ranked[1]] > scores[ranked[0]] * 0.5:
                t1 = "".join(x["text"] for x in chunk if int(x.get("spk", 0)) == ranked[1])
                if _host_score(t1) > _guest_score(t1):
                    host_spks.add(ranked[1])
        for s in chunk:
            s["role"] = "host" if int(s.get("spk", 0)) in host_spks else "guest"

    # 把 intro_end 挂到首段，供合并时强制断段
    if sentences:
        sentences[0]["_intro_end"] = intro_end
    return sentences


def merge_by_speaker(sentences: list[dict], max_chars: int = 1500,
                     max_gap: float = 15.0, max_duration: float = 360.0,
                     intro_max_chars: int = 1200,
                     intro_max_duration: float = 180.0) -> list[dict]:
    """同一说话人连续发言合并为一段；说话人切换或跨开场/对话边界则新开段。"""
    if not sentences:
        return []
    intro_end = float(sentences[0].get("_intro_end") or 0)
    merged: list[dict] = []
    cur = None
    for s in sentences:
        text = (s.get("text") or "").strip()
        if not text or text in {"law，", "law,", "law"}:
            continue
        role = s.get("role") or "unknown"
        start, end = float(s["start"]), float(s["end"])
        if cur is None:
            cur = {"role": role, "text": text, "start": start, "end": end,
                   "spk": s.get("spk")}
            continue
        gap = start - cur["end"]
        cross_intro = bool(intro_end) and cur["start"] < intro_end <= start
        in_intro = bool(intro_end) and cur["start"] < intro_end
        char_limit = intro_max_chars if in_intro else max_chars
        duration_limit = intro_max_duration if in_intro else max_duration
        same_speaker = (
            s.get("spk") == cur.get("spk")
            if s.get("spk") is not None and cur.get("spk") is not None
            else role == cur["role"]
        )
        can_merge = (
            same_speaker
            and gap <= max_gap
            and len(cur["text"]) + len(text) <= char_limit
            and end - cur["start"] <= duration_limit
            and not cross_intro
        )
        if can_merge:
            needs_space = (
                bool(cur["text"])
                and bool(text)
                and cur["text"][-1].isascii()
                and cur["text"][-1].isalnum()
                and text[0].isascii()
                and text[0].isalnum()
            )
            cur["text"] += (" " if needs_space else "") + text
            cur["end"] = end
        else:
            merged.append(cur)
            cur = {"role": role, "text": text, "start": start, "end": end,
                   "spk": s.get("spk")}
    if cur:
        merged.append(cur)
    return merged


def transcribe(chunk_files: list[Path], hotwords: str = "", chunk_seconds: int = 600,
               with_speakers: bool = True) -> list[dict]:
    """逐片段转录，带热词增强；默认启用 cam++ 说话人分离。

    关键经验：
    - 热词通过 generate(hotword="词1 词2") 传入（空格分隔）
    - 不能放在 AutoModel(hotword=file) 构造函数中（那是 contextual 模型专用）
    - merge_vad=True + merge_length_s=15 避免段落过碎
    - 有 sentence_info 时优先用说话人句级结果，再按同说话人合并
    """
    print(f"\n{'='*60}")
    mode = "Paraformer + CT-Punc + cam++" if with_speakers else "Paraformer + CT-Punc"
    print(f"[3/4] ASR 转录 (FunASR {mode} + 热词)")
    print(f"{'='*60}", flush=True)

    from funasr import AutoModel

    model_kwargs = dict(
        model="paraformer-zh",
        model_revision="v2.0.4",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        punc_model="ct-punc",
        device="cpu",
        disable_update=True,
    )
    if with_speakers:
        model_kwargs["spk_model"] = "cam++"

    model = AutoModel(**model_kwargs)

    if hotwords:
        print(f"📌 热词: {hotwords[:80]}...")

    all_segments = []
    total_offset = 0.0
    start_time = time.time()

    for i, chunk_file in enumerate(chunk_files):
        print(f"[{i+1}/{len(chunk_files)}] {chunk_file.name}...", end=" ", flush=True)
        t0 = time.time()

        gen_kwargs = {
            "input": str(chunk_file),
            "cache": {},
            "language": "auto",
            "use_itn": True,
            "batch_size_s": 300,
            "merge_vad": True,
            "merge_length_s": 15,
        }
        if hotwords:
            gen_kwargs["hotword"] = hotwords

        res = model.generate(**gen_kwargs)

        chunk_segs = []
        for item in res:
            info = item.get("sentence_info") or []
            if with_speakers and info:
                for sent in info:
                    text = (sent.get("text") or sent.get("sentence") or "").strip()
                    if not text:
                        continue
                    start = sent.get("start", 0)
                    end = sent.get("end", 0)
                    if start > 1000 or end > 1000:
                        start, end = start / 1000.0, end / 1000.0
                    chunk_segs.append({
                        "text": text,
                        "start": float(start),
                        "end": float(end),
                        "spk": int(sent.get("spk", 0)),
                    })
                continue
            text = item.get("text", "")
            timestamps = item.get("timestamp", [])
            if not text.strip():
                continue
            if timestamps:
                chunk_segs.extend(split_by_punctuation(text, timestamps))
            else:
                chunk_segs.append({"text": text, "start": 0, "end": 0})

        for seg in chunk_segs:
            seg["start"] += total_offset
            seg["end"] += total_offset

        all_segments.extend(chunk_segs)
        total_offset += chunk_seconds
        print(f"{len(chunk_segs)} 段, {time.time()-t0:.1f}s", flush=True)

    elapsed = time.time() - start_time
    print(f"\n✅ 转录完成: {len(all_segments)} 段, 总用时 {elapsed:.0f}s")

    if with_speakers and any("spk" in s for s in all_segments):
        before = len(all_segments)
        remap_speaker_roles(all_segments, chunk_seconds=chunk_seconds)
        all_segments = merge_by_speaker(all_segments)
        print(f"📌 同说话人合并: {before} → {len(all_segments)} 段")

    return all_segments


def split_by_punctuation(text: str, timestamps: list[list[int]]) -> list[dict]:
    """将 FunASR 的整段 text + 逐字 timestamp 按句末标点切分为自然段落。

    切分策略：
    - 遇到句号/问号/感叹号 → 断句
    - 累计超过 200 字 → 在最近的逗号处断句
    - 超过 300 字无论如何断
    - 最终每段 30-200 字，带起止时间戳
    """
    if not text or not timestamps:
        return [{"text": text, "start": 0, "end": 0}]

    sentence_ends = set("。！？!?")
    soft_breaks = set("，,；;：:")

    segments = []
    chars = list(text)

    # 建立字符到时间戳映射
    ts_idx = 0
    char_ts_map = []
    for ch in chars:
        if ts_idx < len(timestamps):
            char_ts_map.append((ch, timestamps[ts_idx][0], timestamps[ts_idx][1]))
            if ch not in sentence_ends and ch not in soft_breaks and ch not in "，,。！？!?；;：:、\"\"''""（）()【】《》":
                ts_idx += 1
        else:
            last_end = timestamps[-1][1] if timestamps else 0
            char_ts_map.append((ch, last_end, last_end))

    cur_text = ""
    cur_start = char_ts_map[0][1] if char_ts_map else 0
    cur_end = 0
    last_soft_break_pos = -1

    for i, (ch, start_ms, end_ms) in enumerate(char_ts_map):
        cur_text += ch
        cur_end = end_ms

        if ch in soft_breaks:
            last_soft_break_pos = len(cur_text)

        should_break = False
        if ch in sentence_ends:
            should_break = True
        elif len(cur_text) > 200 and last_soft_break_pos > 50:
            overflow = cur_text[last_soft_break_pos:]
            cur_text = cur_text[:last_soft_break_pos]
            segments.append({"text": cur_text.strip(), "start": cur_start / 1000.0, "end": cur_end / 1000.0})
            cur_text = overflow
            cur_start = start_ms
            last_soft_break_pos = -1
            continue
        elif len(cur_text) > 300:
            should_break = True

        if should_break and ch in sentence_ends:
            segments.append({"text": cur_text.strip(), "start": cur_start / 1000.0, "end": cur_end / 1000.0})
            cur_text = ""
            cur_start = end_ms
            last_soft_break_pos = -1

    if cur_text.strip():
        segments.append({"text": cur_text.strip(), "start": cur_start / 1000.0, "end": cur_end / 1000.0})

    return segments


# ============================================================
# 4. 生成 Markdown 文字稿
# ============================================================
def generate_markdown(segments: list[dict], title: str, metadata: dict,
                      chapters: list[tuple[int, str]] | None = None, language: str = "zh") -> str:
    """将分段结果生成带 shownotes、章节和时间戳的 Markdown。"""
    print(f"\n{'='*60}")
    print(f"[4/4] 生成 Markdown 文字稿")
    print(f"{'='*60}", flush=True)

    # 繁简转换
    if language in ("zh", "auto"):
        try:
            import opencc
            converter = opencc.OpenCC("t2s")
            for seg in segments:
                seg["text"] = converter.convert(seg["text"])
            print("📌 已完成繁简转换")
        except ImportError:
            pass

    def fmt_time(seconds: float) -> str:
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m:02d}:{s:02d}"

    lines = []
    lines.append(f"# {title}\n")
    if metadata.get("show_name"):
        lines.append(f"> 播客：{metadata['show_name']} | 平台：{metadata.get('platform', '小宇宙FM')}")
    if metadata.get("guest"):
        lines.append(f"> 嘉宾：{metadata['guest']} | 主播：{metadata.get('host', '')}")
    if metadata.get("date"):
        lines.append(f"> 发布日期：{metadata['date']} | 时长：{metadata.get('duration', '')}")
    if metadata.get("url"):
        lines.append(f"> 原始链接：{metadata['url']}")
    has_roles = any(seg.get("role") in ("host", "guest") for seg in segments)
    if has_roles:
        lines.append("> 转录工具：FunASR (Paraformer + CT-Punc + cam++ 说话人分离) | 同说话人段落已合并\n")
    else:
        lines.append("> 转录工具：FunASR (Paraformer + CT-Punc) | 标点自动恢复\n")
    lines.append("---\n")

    shownotes = metadata.get("shownotes") or metadata.get("description") or ""
    shownotes_md = format_shownotes_markdown(shownotes)
    if shownotes_md:
        lines.append(shownotes_md)
        lines.append("\n---\n")
        print(f"📌 已插入节目介绍 ({len(trim_shownotes_boilerplate(shownotes))} 字符)")

    lines.append("## 逐字稿\n")

    host_name = (metadata.get("host") or "").split("，")[0].split(",")[0].strip()
    guest_name = (metadata.get("guest") or "").split("，")[0].split(",")[0].strip()
    host_label = host_name or "主持人"
    guest_label = guest_name or "嘉宾"
    if has_roles:
        lines.append(
            f"> 说明：下文按说话人分段。"
            f"**{host_label}** 为主持人，**{guest_label}** 为嘉宾。"
            " 同一人连续发言（包括跨越短暂停顿）已合并为较大的自然段。\n"
        )

    def format_seg_line(seg: dict) -> str:
        ts = fmt_time(seg["start"])
        role = seg.get("role")
        if role == "host":
            return f"**[{ts}] {host_label}：** {seg['text']}\n"
        if role == "guest":
            return f"**[{ts}] {guest_label}：** {seg['text']}\n"
        return f"**[{ts}]** {seg['text']}\n"

    # 插入章节标题
    if chapters:
        chapter_idx = 0
        inserted = set()
        for seg in segments:
            while chapter_idx < len(chapters):
                ch_time, ch_title = chapters[chapter_idx]
                if seg["start"] >= ch_time and chapter_idx not in inserted:
                    lines.append(f"\n## {ch_title}\n")
                    inserted.add(chapter_idx)
                    chapter_idx += 1
                else:
                    break
            lines.append(format_seg_line(seg))
    else:
        for seg in segments:
            lines.append(format_seg_line(seg))

    content = "\n".join(lines)
    print(f"✅ Markdown 生成完成: {len(segments)} 段, {len(content)} 字符")
    return content


# ============================================================
# 热词构建
# ============================================================
def build_hotwords(args, metadata: dict, chapters: list | None) -> str:
    """从多个来源构建热词列表（空格分隔的词列表）。"""
    # 来源1: --hotwords 直接指定
    if hasattr(args, 'hotwords') and args.hotwords:
        if os.path.isfile(args.hotwords):
            with open(args.hotwords) as f:
                return " ".join(line.split()[0] for line in f if line.strip())
        return args.hotwords

    # 来源2: --hotwords-json（支持 list / {"hotwords": [...]}）
    if hasattr(args, 'hotwords_json') and args.hotwords_json and Path(args.hotwords_json).exists():
        with open(args.hotwords_json) as f:
            hw_data = json.load(f)
        if isinstance(hw_data, dict):
            hw_list = hw_data.get("hotwords") or hw_data.get("words") or []
        else:
            hw_list = hw_data
        words = []
        for item in hw_list:
            words.append(item["word"] if isinstance(item, dict) else str(item))
        return " ".join(words)

    # 来源3: 自动从 metadata + chapters 提取
    words = set()
    if metadata.get("guest"):
        name = re.split(r'[（(]', metadata["guest"])[0].strip()
        words.add(name)
        if 2 <= len(name) <= 4:
            words.add(name[1:])
    if metadata.get("host"):
        name = re.split(r'[（(]', metadata["host"])[0].strip()
        words.add(name)
    if chapters:
        for _, ch_title in chapters:
            for term in re.findall(r'\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*\b', ch_title):
                if len(term) > 2:
                    words.add(term)

    return " ".join(words) if words else ""


# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="播客下载→转录→标准工作包")
    parser.add_argument("url", help="播客链接")
    parser.add_argument("--output-dir", "-o", default="./podcast_output", help="输出目录")
    parser.add_argument("--language", "-l", default="auto", choices=["zh", "en", "auto"])
    parser.add_argument("--title", help="自定义标题")
    parser.add_argument("--metadata-json", help="元信息 JSON")
    parser.add_argument("--chapters-json", help="章节时间线 JSON")
    parser.add_argument("--hotwords", help="热词文件或字符串")
    parser.add_argument("--hotwords-json", help="热词 JSON")
    parser.add_argument("--shownotes-json", help="Show Notes JSON（含 shownotes 字段）或纯文本 .md")
    parser.add_argument("--skip-shownotes-fetch", action="store_true", help="跳过自动抓取 shownotes")
    parser.add_argument("--chunk-seconds", type=int, default=600, help="切片时长(秒)")
    parser.add_argument("--no-speakers", action="store_true",
                        help="禁用 cam++ 说话人分离与同说话人合并（默认开启）")

    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载配置
    metadata = {}
    if args.metadata_json and Path(args.metadata_json).exists():
        with open(args.metadata_json) as f:
            metadata = json.load(f)

    if args.shownotes_json and Path(args.shownotes_json).exists():
        p = Path(args.shownotes_json)
        if p.suffix == ".json":
            with open(p) as f:
                sn = json.load(f)
            metadata["shownotes"] = sn.get("shownotes") or sn.get("description") or ""
        else:
            metadata["shownotes"] = p.read_text(encoding="utf-8")

    # 自动抓取 shownotes（小宇宙等平台信息量远高于 yt-dlp description）
    if not args.skip_shownotes_fetch and not metadata.get("shownotes"):
        print(f"\n{'='*60}")
        print(f"[0/4] 抓取 Show Notes")
        print(f"{'='*60}", flush=True)
        fetched = fetch_episode_metadata(args.url)
        metadata = merge_metadata(metadata, fetched)
        if metadata.get("shownotes"):
            print(f"✅ Show Notes: {len(metadata['shownotes'])} 字符")
        else:
            print("⚠️ 未获取到 Show Notes，将仅输出逐字稿")

    chapters = None
    if args.chapters_json and Path(args.chapters_json).exists():
        with open(args.chapters_json) as f:
            chapters = [(c["time"], c["title"]) for c in json.load(f)]
    elif metadata.get("shownotes"):
        chapters = extract_chapters_from_shownotes(metadata["shownotes"])
        if chapters:
            print(f"📌 从 Show Notes 提取 {len(chapters)} 个章节时间点")

    title = args.title or metadata.get("title", "播客转录")
    hotwords = build_hotwords(args, metadata, chapters)

    # Step 1: 下载
    audio_path = download_audio(args.url, output_dir)

    # Step 2: WAV + 切片
    wav_path, chunk_files = prepare_audio(audio_path, output_dir, args.chunk_seconds)

    # Step 3: 转录（默认说话人分离 + 同说话人合并）
    segments = transcribe(
        chunk_files, hotwords, args.chunk_seconds,
        with_speakers=not args.no_speakers,
    )

    # 保存 segments
    segments_path = output_dir / "segments.json"
    with open(segments_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    # Step 4: 生成 Markdown
    md_content = generate_markdown(segments, title, metadata, chapters, args.language)
    md_path = output_dir / "source.md"
    if md_path.exists() and md_path.read_text(encoding="utf-8") != md_content:
        raise FileExistsError(f"{md_path} 已存在且内容不同；请使用新的输出目录，避免覆盖不可变原文")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    detected_language = "zh" if args.language == "auto" else args.language
    standard_meta = {
        "title": title,
        "source_url": metadata.get("url") or args.url,
        "source_title": metadata.get("title") or title,
        "source_type": "podcast",
        "language": detected_language,
    }
    if metadata.get("parent_id"):
        standard_meta["parent_id"] = metadata["parent_id"]
    standard_meta.update({
        key: value for key, value in metadata.items()
        if key not in standard_meta and key not in {"url"}
    })
    meta_path = output_dir / "meta.json"
    meta_path.write_text(
        json.dumps(standard_meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{'='*60}")
    print("转录与工作包生成完成")
    print(f"{'='*60}")
    print(f"  音频: {audio_path}")
    print(f"  原文: {md_path}")
    print(f"  元信息: {meta_path}")
    print(f"  segments: {segments_path}")

    # 输出 result.json
    result = {"status": "success", "segments_count": len(segments), "content_length": len(md_content),
              "source_path": str(md_path), "meta_path": str(meta_path),
              "audio_path": str(audio_path), "title": title}
    with open(output_dir / "result.json", "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
