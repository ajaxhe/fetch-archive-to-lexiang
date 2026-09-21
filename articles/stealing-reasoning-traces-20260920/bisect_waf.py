#!/usr/bin/env python3
"""二分定位第 N 段中触发 WAF 的内容。

按行二分：找出最小的、仍然触发 403 的行区间。
"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload as up  # noqa: E402

BASE = Path(__file__).resolve().parent
segment_index = int(sys.argv[1]) if len(sys.argv) > 1 else 26
text = (BASE / "Stealing Reasoning Traces from Proprietary LLM APIs.md").read_text(encoding="utf-8")
text, _ = up.materialize_formula_fallback(text, BASE, render_images=False)
lines = (Path("/tmp") / f"seg{segment_index}.md").read_text(encoding="utf-8").split("\n")

credential = up.load_credential(up.resolve_credential_selector())
client = up.MCPClient(credential)
probes = 0


def blocked(content: str) -> bool:
    global probes
    probes += 1
    if not content.strip():
        return False
    try:
        client.json("block_convert_content_to_blocks", {"content": content, "content_type": "markdown"})
        return False
    except Exception as error:  # noqa: BLE001
        if "403" in str(error):
            return True
        print("  非 403 错误:", str(error)[:120])
        return False


lo, hi = 0, len(lines)
assert blocked("\n".join(lines)), "整段未触发，无法二分"
while lo + 1 < hi:
    mid = (lo + hi) // 2
    if blocked("\n".join(lines[lo:mid])):
        hi = mid
    else:
        lo = mid

print(f"探测次数: {probes}")
print(f"最小触发行区间: {lo + 1} .. {hi}（段内 1-based）")
print("=== 该区间内容 ===")
print("\n".join(lines[lo:hi])[:2000])
