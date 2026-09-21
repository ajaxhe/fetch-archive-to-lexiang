#!/usr/bin/env python3
"""用上传器的真实解析逻辑列出公式，标出可疑（跨行 / 过长 / 含 markdown）的项。"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402

t = Path(sys.argv[1]).read_text(encoding="utf-8")
chunk = t

found = []
index = 0
while index < len(chunk):
    if chunk.startswith(r"\$", index):
        index += 2
        continue
    if chunk[index] != "$":
        index += 1
        continue
    if index + 1 < len(chunk) and (
        chunk[index + 1].isdigit()
        or (chunk[index + 1] in {"≈", "~"} and index + 2 < len(chunk) and chunk[index + 2].isdigit())
    ):
        index += 1
        continue
    display = chunk.startswith("$$", index)
    width = 2 if display else 1
    end = core._find_closing_dollar(chunk, index + width, display)
    if end < 0:
        print(f"!! 未闭合 @ 行 {chunk.count(chr(10), 0, index) + 1}")
        break
    latex = chunk[index + width:end].strip()
    if not latex:
        print(f"!! 空公式 @ 行 {chunk.count(chr(10), 0, index) + 1} off={index}")
        print("   上下文:", repr(chunk[max(0, index - 150):index + 150]))
        break
    found.append((index, end + width, display, latex))
    index = end + width

bad = [f for f in found if len(f[3]) > 250 or "\n\n" in f[3] or "**" in f[3] or f[3].startswith("#")]
print("公式总数:", len(found), "| 可疑:", len(bad))
for start, stop, display, latex in bad[:15]:
    line = chunk.count("\n", 0, start) + 1
    print(f"  L{line:5d} len={stop-start:6d} d={int(display)} | {latex[:110]!r}")
