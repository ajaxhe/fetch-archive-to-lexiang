#!/usr/bin/env python3
"""复刻上传器的完整预处理（公式物化 + 分段），导出指定段落内容以便排查。"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload_core as core  # noqa: E402
import lexiang_upload as up  # noqa: E402

md = Path(sys.argv[1]).resolve()
target = int(sys.argv[2])
markdown = md.read_text(encoding="utf-8")
markdown, formula_count = up.materialize_formula_fallback(markdown, md.parent, render_images=False)
plan = core.build_plan(markdown, md.parent)

print("公式数:", formula_count, "| 段落数:", len(plan.segments))
seg = plan.segments[target - 1]
value = str(seg.value)
out = Path(f"/tmp/segment_{target}.txt")
out.write_text(value, encoding="utf-8")
print("段落", target, seg.kind, "长度", len(value), "-> ", out)

lines = value.split("\n")
print("行数:", len(lines), "| 最长行:", max((len(l) for l in lines), default=0))
print("=== 前 1200 字符 ===")
print(value[:1200])
