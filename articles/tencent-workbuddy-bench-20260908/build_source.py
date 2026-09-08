#!/usr/bin/env python3
"""Assemble immutable source.md from the cleaned arXiv markdown dump."""
import re
from pathlib import Path

SRC = Path("/Users/ajaxhe/.cursor/projects/Users-ajaxhe-CodeBuddy/uploads/2607.20911-0.md")
OUT = Path(__file__).resolve().parent / "source.md"

FIG = {
    "Figure 1.": "images/fig01.png",
    "Figure 2.": "images/fig02.png",
    "Figure 3.": "images/fig03.png",
    "Figure 4.": "images/fig04.png",
    "Figure 5.": "images/fig05.png",
    "Figure 6.": "images/fig06.png",
    "Figure 7.": "images/fig07.png",
    "Figure 8.": "images/fig08.png",
    "Figure 9.": "images/fig09.png",
}

SKIP_EXACT = {
    "TENCENT WORKBUDDY BENCH",
    "Technical Report · 2026",
    "---",
    "Project page",
    "Code",
    "Dataset",
    "Report",
    "(a) Code usage domains",
    "(b) Web task categories",
    "(c) Web lifecycle modes",
    "(a) Construction route",
    "(b) Calibrated difficulty",
    "(a) Difficulty trend",
    "(b) Performance by task type",
}

HEADER_SKIP = {
    "Source URL:",
    "Title:",
}


def clean_inline(s: str) -> str:
    s = s.replace("\\(", "").replace("\\)", "")
    s = s.replace("CSV/J-SON", "CSV/JSON")
    s = re.sub(r" +", " ", s)
    return s.rstrip()


def main() -> None:
    raw = SRC.read_text()
    lines = raw.splitlines()
    out: list[str] = []
    inserted: set[str] = set()
    pending_figs: list[tuple[str, str]] = []
    started = False

    for line in lines:
        stripped = line.strip()
        if not started:
            if any(stripped.startswith(p) for p in HEADER_SKIP):
                continue
            if stripped.startswith("arXiv:"):
                continue
            if stripped == "# Tencent WorkBuddy Bench":
                started = True
            else:
                continue

        if stripped in SKIP_EXACT:
            continue
        if re.fullmatch(r"\d{1,2}", stripped):
            continue

        text = clean_inline(line)
        if not text and out and out[-1] == "":
            continue

        fig_hit = next((p for p in FIG if text.startswith(p)), None)
        if fig_hit:
            pending_figs.append((fig_hit, text))
            continue

        if (
            out
            and out[-1]
            and not re.search(r'[.!?:”"”)\]]$', out[-1])
            and not out[-1].startswith(("#", "|", "-", "*", ">", "!", "[", "tasks/"))
            and text
            and (text[0].islower() or text.startswith(("modes,", "workspace", "nesses")))
        ):
            out[-1] = out[-1] + " " + text
        else:
            out.append(text)

        while pending_figs:
            prefix, caption = pending_figs.pop(0)
            if prefix in inserted:
                continue
            if out and out[-1]:
                out.append("")
            out.append(caption)
            out.append("")
            out.append(f"![{prefix.rstrip('.')}]({FIG[prefix]})")
            out.append("")
            inserted.add(prefix)

    # collapse 3+ blanks
    cleaned: list[str] = []
    blank = 0
    for line in out:
        if line == "":
            blank += 1
            if blank <= 2:
                cleaned.append(line)
        else:
            blank = 0
            cleaned.append(line)

    text_joined = "\n".join(cleaned)
    text_joined = text_joined.replace(
        "tasks/<task-name>/\n"
        "task.toml\n"
        "instruction.md\n"
        "environment/\n"
        "Dockerfile\n"
        "workspace/\n"
        "tests/\n"
        "test.sh\n"
        "grading/\n"
        "gold.patch (optional; Code diagnostic reference)</task-name>",
        "```\n"
        "tasks/<task-name>/\n"
        "  task.toml\n"
        "  instruction.md\n"
        "  environment/\n"
        "    Dockerfile\n"
        "  workspace/\n"
        "  tests/\n"
        "    test.sh\n"
        "    grading/\n"
        "    gold.patch (optional; Code diagnostic reference)\n"
        "```",
    )
    cleaned = text_joined.splitlines()

    text = "\n".join(cleaned).strip() + "\n"
    OUT.write_text(text)
    imgs = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", text)
    print(f"wrote {OUT} chars={len(text)} lines={text.count(chr(10))+1} figs={imgs}")


if __name__ == "__main__":
    main()
