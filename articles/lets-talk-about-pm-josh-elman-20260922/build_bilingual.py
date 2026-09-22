#!/usr/bin/env python3
"""Assemble bilingual Markdown from immutable source.md + zh_paragraphs.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

WORKDIR = Path(__file__).resolve().parent
SOURCE = WORKDIR / "source.md"
ZH_FILE = WORKDIR / "zh_paragraphs.json"
TITLE = '"Let\'s Talk about Product Managers" by Josh Elman at Lean Product & Lean UX Meetup'
OUT = WORKDIR / f"{TITLE.replace('/', '-')}.md"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def split_blocks(markdown: str) -> list[tuple[str, str]]:
    blocks = []
    for block in re.split(r"\n\s*\n", markdown):
        block = block.strip()
        if not block:
            continue
        match = HEADING_RE.match(block.splitlines()[0]) if "\n" not in block else HEADING_RE.match(block)
        if match and "\n" not in block:
            blocks.append(("heading", block))
        else:
            blocks.append(("para", block))
    return blocks


def heading_bilingual(block: str) -> str | None:
    match = HEADING_RE.match(block)
    if not match:
        return block
    level, title = match.group(1), match.group(2).strip()
    if level == "#" and title.startswith('"Let\'s Talk about Product Managers"'):
        return None
    mapping = {
        "视频介绍": "Video introduction / 视频介绍",
        "逐字稿": "Transcript / 逐字稿",
    }
    rendered = mapping.get(title, title)
    return f"{level} {rendered}"


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    zh_map: dict[str, str] = json.loads(ZH_FILE.read_text(encoding="utf-8"))
    parts: list[str] = []
    para_index = 0
    missing = []
    for kind, block in split_blocks(source):
        if kind == "heading":
            rendered = heading_bilingual(block)
            if rendered:
                parts.append(rendered)
            continue
        key = str(para_index)
        zh = zh_map.get(key)
        if zh is None:
            missing.append(para_index)
            zh = ""
        if block.startswith("#") and not block.startswith("# "):
            # Hashtag line must not become a document heading.
            block = block.replace("#", r"\#", 1)
        if zh.strip():
            parts.append(f"{block}\n\n{zh.strip()}")
        else:
            parts.append(block)
        para_index += 1
    if missing:
        raise SystemExit(f"missing translations for paragraphs: {missing}")
    OUT.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {OUT.name} ({OUT.stat().st_size} bytes), {para_index} paragraphs")


if __name__ == "__main__":
    main()
