#!/usr/bin/env python3
"""定位上传器公式预检失败的真实偏移（错误偏移是相对分块的，不是全文件）。"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402

path = Path(sys.argv[1])
t = path.read_text(encoding="utf-8")

cursor = 0
found = False
for fence in core.FENCE_RE.finditer(t):
    chunk = t[cursor:fence.start()]
    try:
        core._convert_inline_code_aware(chunk)
    except core.PreflightError as error:
        rel = int(str(error).split("字符偏移 ")[1])
        abso = cursor + rel
        found = True
        print("分块起点:", cursor, "| 相对偏移:", rel, "| 绝对偏移:", abso)
        print("绝对行号:", t.count("\n", 0, abso) + 1)
        start = t.rfind("\n", 0, abso) + 1
        end = t.find("\n", abso)
        print("所在行:", repr(t[start:end]))
        print("上下文:", repr(t[max(0, abso - 200):abso + 200]))
        break
    cursor = fence.end()

if not found:
    tail = t[cursor:]
    try:
        core._convert_inline_code_aware(tail)
        print("全文公式预检通过")
    except core.PreflightError as error:
        rel = int(str(error).split("字符偏移 ")[1])
        abso = cursor + rel
        print("尾部块失败 | 绝对偏移:", abso, "| 行号:", t.count("\n", 0, abso) + 1)
        start = t.rfind("\n", 0, abso) + 1
        end = t.find("\n", abso)
        print("所在行:", repr(t[start:end]))
        print("上下文:", repr(t[max(0, abso - 200):abso + 200]))
