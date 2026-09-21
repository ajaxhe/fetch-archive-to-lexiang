#!/usr/bin/env python3
"""精确定位上传器公式预检失败的位置（错误偏移是相对分块的，需做偏移映射）。"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402

t = Path(sys.argv[1]).read_text(encoding="utf-8")


def probe(chunk: str, base: int) -> tuple[int, str] | None:
    """在 chunk 内复刻 _convert_inline_code_aware 的顺序，返回 (绝对偏移, 错误信息)。"""
    cursor = 0
    for match in core.re.finditer(r"`[^`\n]*`", chunk):
        before = chunk[cursor:match.start()]
        try:
            core._convert_math_outside_code(before)
        except core.PreflightError as error:
            rel = int(str(error).split("字符偏移 ")[1])
            return base + cursor + rel, str(error)
        cursor = match.end()
    tail = chunk[cursor:]
    try:
        core._convert_math_outside_code(tail)
    except core.PreflightError as error:
        rel = int(str(error).split("字符偏移 ")[1])
        return base + cursor + rel, str(error)
    return None


cursor = 0
found = None
for fence in core.FENCE_RE.finditer(t):
    result = probe(t[cursor:fence.start()], cursor)
    if result:
        found = result
        break
    cursor = fence.end()
if not found:
    found = probe(t[cursor:], cursor)

if not found:
    print("公式预检通过")
    sys.exit(0)

off, message = found
line = t.count("\n", 0, off) + 1
print("错误:", message)
print("绝对偏移:", off, "行:", line)
print("字符:", repr(t[off]))
print("上下文:", repr(t[max(0, off - 220):off + 220]))
