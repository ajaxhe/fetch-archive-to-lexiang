#!/usr/bin/env python3
"""修复 `source.md` 里会让上传器公式预检失败的问题。

背景：arXiv HTML 抓取的产物在附录（原始推理轨迹）里混入了大量非公式的 `$`
与「省略标记截断公式」的情况，导致上传器的 `$...$` 配对整体错位。

处理顺序（顺序重要）：
  1. 规范化省略标记 `[ ⋯\\cdots ]` → `[ ⋯ ]`
  2. 转义代码语境里的字面 `$`（Svelte runes / shell 变量 / JS 模板字面量）
  3. 附录区里 `$` 个数为奇数的行，整行按字面转义（落单定界符）
  4. 给「以数字开头的行内公式」开符号后补空格，绕开上传器的货币启发式
  5. 状态机扫描：省略标记落在公式内部时，补上应有的闭合符

只补定界符与转义，不改动任何实质内容。
"""
import re
import sys
from pathlib import Path

OPENERS = (("$$", "$$"), ("\\[", "\\]"), ("\\(", "\\)"), ("$", "$"))
MARKER = "[ ⋯"
LITERAL_DOLLAR_RE = re.compile(r"(?<!\\)\$(?=\{|props|state|derived|effect|bindable|DBURL)")
DIGIT_MATH_RE = re.compile(r"\$(?=[0-9])([^$\n]{0,200}?)\$")


def _escaped(text: str, index: int) -> bool:
    slashes = 0
    k = index - 1
    while k >= 0 and text[k] == "\\":
        slashes += 1
        k -= 1
    return slashes % 2 == 1


def scan(state, env_stack, s):
    """返回扫描后的 (state, env_stack)。"""
    i = 0
    while i < len(s):
        if s.startswith("\\$", i):
            i += 2
            continue
        if state is None:
            matched = None
            for opener, closer in OPENERS:
                if s.startswith(opener, i):
                    matched = (opener, closer)
                    break
            if matched:
                if matched[0] == "$":
                    nxt = s[i + 1] if i + 1 < len(s) else ""
                    if nxt.isdigit() or nxt in {"≈", "~"}:
                        i += 1
                        continue
                state = matched
                i += len(matched[0])
                continue
            i += 1
            continue
        closer = state[1]
        if s.startswith(closer, i):
            if not _escaped(s, i):
                state = None
            i += len(closer)
            continue
        if state[0] == "\\[":
            for name in ("aligned", "array", "cases", "matrix", "pmatrix", "bmatrix"):
                if s.startswith("\\begin{" + name + "}", i):
                    env_stack.append(name)
                    i += len(name) + 8
                    break
                if s.startswith("\\end{" + name + "}", i):
                    if env_stack and env_stack[-1] == name:
                        env_stack.pop()
                    i += len(name) + 6
                    break
            else:
                i += 1
                continue
            continue
        i += 1
    return state, env_stack


def close_truncated_formulas(text: str) -> tuple[str, list[str]]:
    """省略标记落在公式内部时，补上应有的闭合符。"""
    lines = text.split("\n")
    state = None
    env_stack: list[str] = []
    repairs = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if state is not None and line.strip().startswith(MARKER):
            prev = i - 1
            while prev >= 0 and not lines[prev].strip():
                prev -= 1
            if state[0] in ("$", "$$", "\\(", "\\)"):
                body = lines[prev].rstrip()
                if body.endswith("\\") and not body.endswith("\\\\"):
                    body = body[:-1].rstrip()
                lines[prev] = body + state[1]
                repairs.append(f"第 {prev + 1} 行补 {state[1]}（{state[0]}… 被省略标记截断）")
                state = None
            else:
                inserts = []
                while env_stack:
                    inserts.append("\\end{" + env_stack.pop() + "}")
                inserts.append("\\]")
                lines[prev + 1:prev + 1] = inserts
                repairs.append(f"第 {prev + 1} 行后补 {'、'.join(inserts)}（\\[…\\] 被省略标记截断）")
                state = None
                i += len(inserts)
            i += 1
            continue
        state, env_stack = scan(state, env_stack, line)
        i += 1
    return "\n".join(lines), repairs


def escape_literal_dollars(text: str) -> tuple[str, int]:
    """代码语境里的字面 `$` → `\\$`（Svelte runes / shell 变量 / JS 模板字面量）。"""
    return LITERAL_DOLLAR_RE.subn(lambda _: "\\$", text)


def escape_odd_lines(text: str, start_line: int) -> tuple[str, list[int]]:
    """`$` 个数为奇数的行说明有落单定界符，按字面转义。"""
    lines = text.split("\n")
    touched = []
    for i in range(start_line - 1, len(lines)):
        if lines[i].count("$") % 2 == 1:
            lines[i] = lines[i].replace("$", "\\$")
            touched.append(i + 1)
    return "\n".join(lines), touched


MATH_SIGNALS = ("\\", "ˆ", "^", "_", "=", "{", "}")
NUMERIC_ONLY_RE = re.compile(r"^[\d.,%+\-/]+[a-zA-Z]?$")


def _looks_like_math(content: str) -> bool:
    """判断 `$<数字>...$` 是数学公式还是货币金额。

    单 token（`41.32`、`2d`、`3`）算公式；含 LaTeX 特征字符的算公式；
    其余（如 `30,000 on API credits`）按货币处理，保持不变。
    """
    stripped = content.strip()
    if not stripped:
        return False
    if any(ch in stripped for ch in MATH_SIGNALS):
        return True
    if not re.search(r"\s", stripped):
        return bool(NUMERIC_ONLY_RE.match(stripped))
    return False


def guard_digit_leading_math(text: str) -> tuple[str, list[str]]:
    """给「以数字开头的行内公式」开符号后补空格。

    上传器把 `$` 紧跟数字视为货币，会跳过真正的公式起始符，使 `$60ˆ\\circ$` 这类整体错位。
    补空格即可绕过该启发式，公式内容会被 `.strip()` 去掉空格，渲染不受影响。
    """
    out = []
    cursor = 0
    samples = []
    while True:
        match = DIGIT_MATH_RE.search(text, cursor)
        if not match:
            out.append(text[cursor:])
            break
        if _looks_like_math(match.group(1)):
            out.append(text[cursor:match.start()])
            out.append("$ " + match.group(1) + "$")
            samples.append(match.group(0)[:60])
            cursor = match.end()
        else:
            out.append(text[cursor:match.start() + 1])
            cursor = match.start() + 1
    return ("".join(out), samples) if samples else (text, [])


def repair(path: Path) -> None:
    before = path.read_text(encoding="utf-8")
    text = before

    marker_count = text.count("[ ⋯\\cdots ]")
    text = text.replace("[ ⋯\\cdots ]", "[ ⋯ ]")

    text, literal_count = escape_literal_dollars(text)

    appendix_start = next(
        (n for n, line in enumerate(text.split("\n"), start=1) if line.strip() == "## Appendix"),
        1,
    )
    text, odd_lines = escape_odd_lines(text, appendix_start)

    text, samples = guard_digit_leading_math(text)

    text, repairs = close_truncated_formulas(text)

    path.write_text(text, encoding="utf-8")

    print(f"1) 省略标记规范化 [ ⋯\\cdots ] → [ ⋯ ]：{marker_count} 处")
    print(f"2) 代码语境字面 $ 转义：{literal_count} 处")
    print(f"3) 附录落单 $ 整行转义：{len(odd_lines)} 行 {odd_lines}")
    print(f"4) 数字开头行内公式补空格：{len(samples)} 处")
    print("5) 截断公式补闭合符：")
    for r in repairs:
        print("   -", r)

    stripped = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", text)
    print("   全文公式状态:", scan(None, [], stripped))


if __name__ == "__main__":
    repair(Path(sys.argv[1]))
