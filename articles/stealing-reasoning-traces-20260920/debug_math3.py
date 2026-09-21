#!/usr/bin/env python3
"""列出全部识别出的公式，找出第一处误配对。"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402

t = Path(sys.argv[1]).read_text(encoding="utf-8")
chunk = t

formulas = []
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
        print(f"!! 未闭合 @ {index}")
        break
    latex = chunk[index + width:end].strip()
    formulas.append((index, end + width, display, latex))
    index = end + width

limit = int(sys.argv[2]) if len(sys.argv) > 2 else 45
for n, (start, stop, display, latex) in enumerate(formulas[:limit]):
    line = chunk.count("\n", 0, start) + 1
    flag = ""
    if len(latex) > 400 or "\n##" in latex or "RESPONSE" in latex:
        flag = "  <== 可疑"
    print(f"#{n:3d} L{line:5d} off={start:7d} len={stop-start:6d} d={int(display)} | {latex[:90]!r}{flag}")
