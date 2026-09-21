#!/usr/bin/env python3
"""扫描：省略标记是否落在未闭合的公式内部；并报告全文公式闭合状态。"""
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

# 去掉围栏代码，避免误判
text = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", text)

OPENERS = [("$$", "$$"), ("\\[", "\\]"), ("\\(", "\\)"), ("$", "$")]

state = None          # 当前打开的定界符
state_pos = 0
problems = []
i = 0
n = len(text)
while i < n:
    if text.startswith(r"\$", i):
        i += 2
        continue
    if state is None:
        # 找下一个开符号
        matched = None
        for opener, closer in OPENERS:
            if text.startswith(opener, i):
                matched = (opener, closer)
                break
        if matched:
            opener, closer = matched
            # 便宜处理：$ 后面跟数字视为货币
            if opener == "$" and not text.startswith("$$", i):
                nxt = text[i + 1] if i + 1 < n else ""
                if nxt.isdigit() or nxt in {"≈", "~"}:
                    i += 1
                    continue
            state, state_pos = matched, i
            i += len(opener)
            continue
        i += 1
        continue
    # 在公式内部：找闭合符
    closer = state[1]
    if text.startswith(closer, i):
        # 检查转义
        slashes = 0
        j = i - 1
        while j >= 0 and text[j] == "\\":
            slashes += 1
            j -= 1
        if slashes % 2 == 0:
            state = None
        i += len(closer)
        continue
    if text.startswith("[ ⋯", i):
        line = text.count("\n", 0, i) + 1
        problems.append((line, state, state_pos))
        i += 1
        continue
    i += 1

print("=== 省略标记落在公式内部 ===")
for line, st, spos in problems:
    open_line = text.count("\n", 0, spos) + 1
    print(f"标记行 {line} | 处于 {st!r} 内（开于第 {open_line} 行）")
if not problems:
    print("（无）")
print("=== 文件结束时未闭合 ===", state)
