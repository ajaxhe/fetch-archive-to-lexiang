#!/usr/bin/env python3
"""Pin a Lexiang entry before the first sibling under its parent.

OpenAPI POST ?before= does not reorder folders. Use the same MCP
entry_move_entry path as upload-markdown-to-lexiang --pin.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _uploader_scripts() -> Path:
    env = os.environ.get("LEXIANG_UPLOADER_ROOT")
    if env:
        scripts = Path(env) / "scripts"
        if (scripts / "lexiang_upload.py").is_file():
            return scripts
    search_roots = [Path.cwd(), *Path.cwd().parents, Path(__file__).resolve()]
    for root in search_roots:
        for rel in (
            Path(".codebuddy/skills/upload-markdown-to-lexiang/scripts"),
            Path("upload-markdown-to-lexiang/scripts"),
        ):
            cand = root / rel
            if (cand / "lexiang_upload.py").is_file():
                return cand
    home = Path.home() / ".agents/skills/upload-markdown-to-lexiang/scripts"
    if (home / "lexiang_upload.py").is_file():
        return home
    raise FileNotFoundError(
        "找不到 upload-markdown-to-lexiang；请设置 LEXIANG_UPLOADER_ROOT"
    )


def pin_entry(entry_id: str, parent_id: str) -> dict:
    scripts = _uploader_scripts()
    sys.path.insert(0, str(scripts))
    from lexiang_upload import MCPClient, load_credential  # type: ignore

    client = MCPClient(load_credential())
    listed = client.json(
        "entry_list_children",
        {"parent_id": parent_id, "limit": 8, "_mcp_fields": "-html_content,-staffs"},
    )
    siblings = listed.get("data", {}).get("entries", [])
    first = next(
        (item.get("id") for item in siblings if item.get("id") and item.get("id") != entry_id),
        None,
    )
    if not first:
        return {"ok": True, "moved": False, "reason": "no sibling", "first": entry_id}

    client.json(
        "entry_move_entry",
        {"entry_id": entry_id, "parent_id": parent_id, "before": first},
    )
    after = client.json(
        "entry_list_children",
        {"parent_id": parent_id, "limit": 3, "_mcp_fields": "-html_content,-staffs"},
    )
    names = [item.get("name") for item in after.get("data", {}).get("entries", [])]
    first_id = (after.get("data", {}).get("entries") or [{}])[0].get("id")
    if first_id != entry_id:
        raise RuntimeError(f"置顶失败，当前首位是 {names[:3]}")
    return {"ok": True, "moved": True, "before": first, "order": names}


def main() -> int:
    parser = argparse.ArgumentParser(description="将乐享条目移到父目录首位")
    parser.add_argument("--entry-id", required=True)
    parser.add_argument("--parent-id", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = pin_entry(args.entry_id, args.parent_id)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("pinned" if result.get("moved") else result.get("reason"), result.get("order"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
