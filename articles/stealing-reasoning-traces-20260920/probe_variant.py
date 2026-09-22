#!/usr/bin/env python3
"""探针：判断 WAF 对哪一类变体放行。

对同一行文本的多种改写做 block_convert_content_to_blocks（无副作用），
找出「内容相同但写法不同」时 WAF 的判定差异。
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/helufan/.workbuddy/skills/upload-markdown-to-lexiang/scripts")
import lexiang_upload as up  # noqa: E402

DELAY = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0

credential = up.load_credential(up.resolve_credential_selector())
client = up.MCPClient(credential)

ZWSP = "\u200b"

VARIANTS = [
    ("A 原句", "Let’s fetch captcha.js."),
    ("B 单词 captcha", "captcha"),
    ("C captcha.js", "captcha.js"),
    ("D 改述", "Let’s fetch the captcha script."),
    ("E 零宽-单词", f"Let’s fetch capt{ZWSP}cha.js."),
    ("F 零宽-captcha", f"capt{ZWSP}cha"),
    ("G 对照", "an ordinary sentence about nothing in particular"),
]


def probe(label: str, content: str) -> bool:
    try:
        client.json(
            "block_convert_content_to_blocks",
            {"content": content, "content_type": "markdown"},
        )
        print(f"{label:16s} OK", flush=True)
        return True
    except Exception as error:  # noqa: BLE001
        msg = str(error)
        if "403" in msg:
            print(f"{label:16s} BLOCKED(403)", flush=True)
        else:
            print(f"{label:16s} ERR {msg[:90]}", flush=True)
        return False


for label, text in VARIANTS:
    probe(label, text)
    time.sleep(DELAY)
