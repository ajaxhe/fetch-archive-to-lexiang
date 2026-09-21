#!/usr/bin/env python3
"""追踪换算过程：列出每个被识别的公式及其绝对偏移，定位误配对点。"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402

path = Path(sys.argv[1])
t = path.read_text(encoding="utf-8")
chunk = t  # 第一个分块（无围栏代码）

out, formulas = [], []
index = 0
broken = False
while index < len(chunk):
    if chunk.startswith(r"\$", index):
        out.append(r"\$")
        index += 2
        continue
    if chunk[index] != "$":
        out.append(chunk[index])
        index += 1
        continue
    if index + 1 < len(chunk) and (
        chunk[index + 1].isdigit()
        or (chunk[index + 1] in {"≈", "~"} and index + 2 < len(chunk) and chunk[index + 2].isdigit())
    ):
        out.append("$")
        index += 1
        continue
    display = chunk.startswith("$$", index)
    width = 2 if display else 1
    end = core._find_closing_dollar(chunk, index + width, display)
    if end < 0:
        print(f"!! 未闭合 @ {index} (行 {chunk.count(chr(10), 0, index) + 1}) display={display}")
        print("   上下文:", repr(chunk[max(0, index - 120):index + 120]))
        broken = True
        break
    latex = chunk[index + width:end].strip()
    formulas.append((index, end + width, display, latex))
    index = end + width

print("识别公式数:", len(formulas), "| 未闭合:", broken)
print("=== 最后 8 个公式 ===")
for start, stop, display, latex in formulas[-8:]:
    line = chunk.count("\n", 0, start) + 1
    span = stop - start
    print(f"L{line:5d} off={start:7d} len={span:6d} display={display} | {latex[:100]}")
