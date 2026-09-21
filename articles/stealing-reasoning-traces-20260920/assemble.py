#!/usr/bin/env python3
"""装配最终双语 Markdown：正文双语（drafts/part_*.md）+ 参考文献/附录保留英文原文。"""
import re
from pathlib import Path

base = Path(__file__).resolve().parent
src_lines = (base / "source.md").read_text(encoding="utf-8").splitlines()

parts = sorted((base / "drafts").glob("part_*.md"))
if not parts:
    raise SystemExit("drafts/ 下没有 part_*.md")
head = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in parts)

out, note_done = [], False
for line in src_lines[581:]:  # 第 582 行起 = 参考文献 + 附录
    s = line.strip()
    if s == "### References":
        out.append("## References / 参考文献")
        continue
    if s == "## Appendix" and not note_done:
        out.append("## Appendix / 附录")
        out.append("")
        out.append(
            "> 归档说明：按本次归档范围要求，参考文献与附录 A–E 保留英文原文，未作逐字对照翻译。"
            "/ Archive note: the References and Appendices A–E are kept in their original English, "
            "per the requested archive scope."
        )
        note_done = True
        continue
    m = re.match(r"^(#{3,5}) (Appendix [A-E])([A-Z].*)$", line)
    out.append(f"{m.group(1)} {m.group(2)}. {m.group(3)}" if m else line)

final = head.rstrip() + "\n\n" + "\n".join(out).lstrip("\n").rstrip() + "\n"
target = base / "Stealing Reasoning Traces from Proprietary LLM APIs.md"
target.write_text(final, encoding="utf-8")
print(f"assembled: {target.name} | {len(final)} chars | {final.count(chr(10)) + 1} lines")
print(f"appendix note inserted: {note_done}")
