#!/usr/bin/env python3
"""诊断 WAF 403：是内容触发还是频率限制。

用 `block_convert_content_to_blocks`（纯转换、无写入副作用）分别试：
  A. 一段普通文本（对照组）
  B. 第 N 段真实内容
若 A 通 B 挂 → 内容触发；A/B 都挂 → 频率或临时封禁。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload as up  # noqa: E402
import lexiang_upload_core as core  # noqa: E402

BASE = Path(__file__).resolve().parent
segment_index = int(sys.argv[1]) if len(sys.argv) > 1 else 26

markdown = (BASE / "Stealing Reasoning Traces from Proprietary LLM APIs.md").read_text(encoding="utf-8")
markdown, _ = up.materialize_formula_fallback(markdown, BASE, render_images=False)
plan = core.build_plan(markdown, BASE)
value = str(plan.segments[segment_index - 1].value)
(Path("/tmp") / f"seg{segment_index}.md").write_text(value, encoding="utf-8")

credential = up.load_credential(up.resolve_credential_selector())
client = up.MCPClient(credential)


def probe(label: str, content: str) -> None:
    try:
        client.json("block_convert_content_to_blocks", {"content": content, "content_type": "markdown"})
        print(f"{label}: OK")
    except Exception as error:  # noqa: BLE001
        print(f"{label}: FAIL {str(error)[:100]}")


probe("对照-短文本", "hello world\n\n这是一段普通测试文本。")
probe(f"第 {segment_index} 段", value)
probe("对照-短文本(again)", "second control probe")
