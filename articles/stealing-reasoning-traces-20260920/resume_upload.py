#!/usr/bin/env python3
"""带节流与断点续传的乐享上传（应对 WAF 403 频率限制）。

复用 upload-markdown-to-lexiang 的内部实现，只在写入片段之间加入延迟并记录断点：
  - 首次运行：清空页面后逐段写入
  - 后续运行：从断点续写，不再清空
  - 每段失败（WAF 403 等）退避重试

用法：resume_upload.py [延迟秒数]
"""
import json
import sys
import time
from pathlib import Path

UPLOADER = "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts"
sys.path.insert(0, UPLOADER)
import lexiang_upload as up  # noqa: E402
import lexiang_upload_core as core  # noqa: E402

BASE = Path(__file__).resolve().parent
MD = BASE / "Stealing Reasoning Traces from Proprietary LLM APIs.md"
ENTRY_ID = "9ca5b3ef4b174a06a7cfa31438d32bcd"
PARENT_ID = "34a3f7f1f2fe4e33a8e7e91c49f15476"
CKPT = BASE / ".upload_checkpoint.json"

DELAY = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
BACKOFF = 45.0
MAX_TRIES = 8

markdown = MD.read_text(encoding="utf-8")
meta = up.load_meta("meta.json", MD.parent)
credential = up.load_credential(up.resolve_credential_selector())
source_url, source_title = up.resolve_source(
    "", "", meta, True, credential_loader=lambda: credential
)
markdown = up.prepend_source_link(markdown, source_url, source_title)
markdown, formula_count = up.materialize_formula_fallback(
    markdown, MD.parent, render_images=False
)
plan = core.build_plan(markdown, MD.parent)
segments = plan.segments
total = len(segments)
print(f"公式 {formula_count} | 片段 {total} | 节流 {DELAY}s", flush=True)

state = {"entry_id": ENTRY_ID, "total": total, "cleared": False, "done": 0}
if CKPT.is_file():
    saved = json.loads(CKPT.read_text(encoding="utf-8"))
    if saved.get("entry_id") == ENTRY_ID and saved.get("total") == total:
        state = saved
        print(f"从断点恢复：已完成 {state['done']}/{total}", flush=True)

client = up.MCPClient(credential)

if not state["cleared"]:
    print("清空页面既有内容…", flush=True)
    up.clear_existing_page(client, ENTRY_ID)
    state["cleared"] = True
    CKPT.write_text(json.dumps(state), encoding="utf-8")
    time.sleep(DELAY)


def write_segment(index: int) -> None:
    segment = segments[index]
    if segment.kind == "text":
        up.append_page_text(client, ENTRY_ID, segment.value)
    elif segment.kind == "image":
        up.upload_image(client, ENTRY_ID, Path(segment.value))
    else:
        up.append_callout(client, ENTRY_ID, segment.value, segment.icon)


for index in range(state["done"], total):
    label = f"[{index + 1}/{total}] {segments[index].kind}"
    for attempt in range(1, MAX_TRIES + 1):
        try:
            write_segment(index)
            print(f"{label} ok", flush=True)
            break
        except Exception as error:  # noqa: BLE001
            message = str(error)[:160]
            print(f"{label} 第 {attempt} 次失败：{message}", flush=True)
            if attempt == MAX_TRIES:
                raise
            time.sleep(BACKOFF)
    state["done"] = index + 1
    CKPT.write_text(json.dumps(state), encoding="utf-8")
    time.sleep(DELAY)

print("全部片段写入完成，置顶…", flush=True)
try:
    up.pin_page(client, ENTRY_ID, PARENT_ID)
except Exception as error:  # noqa: BLE001
    print("置顶失败（不影响正文）：", str(error)[:120], flush=True)

print(json.dumps({"ok": True, "entry_id": ENTRY_ID, "segments": total}, ensure_ascii=False))
