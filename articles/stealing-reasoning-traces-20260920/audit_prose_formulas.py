#!/usr/bin/env python3
"""列出被解析成「散文化公式」的项——公式里出现空行或英文散文，说明 `$` 配对仍错位。"""
import re
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402

t = Path(sys.argv[1]).read_text(encoding="utf-8")
fence = core.FENCE_RE.search(t)
chunk = t[:fence.start()] if fence else t

spans = []
index = 0
while index < len(chunk):
    if chunk.startswith("\\$", index):
        index += 2
        continue
    if chunk[index] != "$":
        index += 1
        continue
    if index + 1 < len(chunk) and (
        chunk[index + 1].isdigit() or (chunk[index + 1] in {"≈", "~"} and index + 2 < len(chunk) and chunk[index + 2].isdigit())
    ):
        index += 1
        continue
    display = chunk.startswith("$$", index)
    width = 2 if display else 1
    end = core._find_closing_dollar(chunk, index + width, display)
    latex = chunk[index + width:end].strip() if end >= 0 else ""
    if end < 0 or not latex:
        print(f"!! 解析中断 @ 行 {chunk.count(chr(10), 0, index) + 1}")
        break
    spans.append((index, end + width, display, latex))
    index = end + width

PROSE_RE = re.compile(r"\b(the|and|is|of|to|we|if|then|so|that|with|for|are)\b", re.I)


def is_prose(s: str) -> bool:
    if "\n" in s:
        return True
    if "\\" in s or "ˆ" in s or "=" in s:
        return False
    return len(PROSE_RE.findall(s)) >= 2


bad = [s for s in spans if is_prose(s[3])]
print(f"公式总数: {len(spans)} | 散文化公式: {len(bad)}")
for start, _stop, display, latex in bad[:15]:
    line = chunk.count("\n", 0, start) + 1
    print(f"  L{line:5d} d={int(display)} | {latex[:110]!r}")
