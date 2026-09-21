#!/usr/bin/env python3
"""按附录小节测试公式可解析性，输出哪些区块需要降级处理。"""
import re
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
lines = text.split("\n")

starts = [i for i, l in enumerate(lines) if re.match(r"^#{2,5} ", l)]
starts.append(len(lines))

print(f"{'小节':<62} {'$':>6} {'结果'}")
print("-" * 90)
for k in range(len(starts) - 1):
    head = lines[starts[k]].strip()
    body = "\n".join(lines[starts[k]:starts[k + 1]])
    dollars = body.count("$")
    if dollars == 0:
        continue
    try:
        core.convert_math(body)
        status = "ok"
    except core.PreflightError as error:
        status = "FAIL: " + str(error)[:40]
    print(f"{head[:60]:<62} {dollars:>6} {status}")
