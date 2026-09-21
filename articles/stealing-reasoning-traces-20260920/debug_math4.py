#!/usr/bin/env python3
"""复刻上传器语义（含 `$` 后接数字视为货币的启发式），报告首个 / 末尾未闭合的定界符。"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fix_math as fm  # noqa: E402

t = Path(sys.argv[1]).read_text(encoding="utf-8")
t = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", t)

state = None
open_pos = None
opened = []
i = 0
while i < len(t):
    if t.startswith("\\$", i):
        i += 2
        continue
    if state is None:
        matched = None
        for opener, closer in fm.OPENERS:
            if t.startswith(opener, i):
                matched = (opener, closer)
                break
        if matched:
            if matched[0] == "$":
                nxt = t[i + 1] if i + 1 < len(t) else ""
                if nxt.isdigit() or nxt in {"≈", "~"}:
                    i += 1
                    continue
            state, open_pos = matched, i
            opened.append(open_pos)
            i += len(matched[0])
            continue
        i += 1
        continue
    closer = state[1]
    if t.startswith(closer, i):
        if not fm._escaped(t, i):
            state = None
        i += len(closer)
        continue
    i += 1

print("结束时状态:", state)
if state:
    line = t.count("\n", 0, open_pos) + 1
    print("未闭合开符号行:", line)
    print("上下文:", repr(t[max(0, open_pos - 260):open_pos + 260]))
print("累计开符号数:", len(opened))
