"""ICU argument contracts, matching FormatJS with ``ignoreTag: true``.

This parser validates message syntax; it does not format translated text. Its semantic
signature omits literal copy and formatting styles, but keeps argument roles, branch
selectors, plural offsets and pound references. Each scope is a set, so repeating an
argument is allowed without hiding a removed reference in a different branch.

The grammar follows the installed @formatjs/icu-messageformat-parser and skeleton
parser. Shared fixtures in docs/ui-text-icu-cases.json also run against the web's real
IntlMessageFormat parser. Keep those fixtures in step when FormatJS changes its syntax.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import cast

# FormatJS's identifier excludes Unicode White_Space and Pattern_Syntax. This is its
# generated fallback character class, rather than Python's different \w / \s rules.
IDENTIFIER = re.compile(
    r"[^\t-\r -/:-@\[-\^`\{-~\x85\xa0-\xa7\xa9\xab\xac\xae\xb0\xb1\xb6"
    r"\xbb\xbf\xd7\xf7\u1680\u2000-\u200a\u2010-\u2029\u202f-\u203e"
    r"\u2041-\u2053\u2055-\u205f\u2190-\u245f\u2500-\u2775\u2794-\u2bff"
    r"\u2e00-\u2e7f\u3000-\u3003\u3008-\u3020\u3030\ufd3e\ufd3f\ufe45\ufe46]*"
)
LITERAL_PARAMETER = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
SPACE = "\t\n\v\f\r \x85\u200e\u200f\u2028\u2029"
JS_TRIM = (
    "\t\n\v\f\r \xa0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006"
    "\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
)
DATE_PATTERN = re.compile(
    r"(?:[Eec]{1,6}|G{1,5}|[Qq]{1,5}|(?:[yYur]+|U{1,5})|[ML]{1,5}|d{1,2}|"
    r"D{1,3}|F|[abB]{1,5}|[hkHK]{1,2}|w{1,2}|W|m{1,2}|s{1,2}|[zZOvVxX]{1,4})"
    r"(?=([^']*'[^']*')*[^']*$)"
)
FRACTION_PRECISION = re.compile(r"\.(?:0+\*?|#+|0+#+)")
SIGNIFICANT_PRECISION = re.compile(r"(@+)?(\+|#+)?[rs]?")
INTEGER_WIDTH = re.compile(r"(\*)(0+)|(#+)(0+)|(0+)")

type SemanticNode = tuple[object, ...]
type Signature = frozenset[SemanticNode]


class IcuSyntaxError(ValueError):
    """An invalid ICU message, with a one-based source position."""


@dataclass(frozen=True)
class IcuContract:
    arguments: Signature
    literal_parameters: frozenset[str]


def describe_argument(node: SemanticNode) -> str:
    """Explain a contract difference using the ICU notation the editor can change."""
    kind = cast(int, node[0])
    if kind == 7:
        return "#"
    role = {1: "argument", 2: "number", 3: "date", 4: "time", 5: "select", 6: "plural"}[kind]
    if kind == 6 and node[2] == "ordinal":
        role = "selectordinal"
    label = f"{{{node[1]}}} ({role}"
    if kind == 6:
        label += f", offset:{node[3]}"
    label += ")"
    if kind not in {5, 6}:
        return label
    branches = cast(tuple[tuple[str, Signature], ...], node[2] if kind == 5 else node[4])
    descriptions = [
        f"{selector}: {', '.join(sorted(map(describe_argument, children))) or '純文字'}"
        for selector, children in branches
    ]
    return f"{label} [{'；'.join(descriptions)}]"


class _Parser:
    def __init__(self, message: str) -> None:
        self.message = message
        self.position = 0
        self.literals: set[str] = set()

    def fail(self, problem: str) -> None:
        raise IcuSyntaxError(f"第 {self.position + 1} 個字元：{problem}")

    def peek(self) -> str:
        return self.message[self.position : self.position + 1]

    def take(self, text: str) -> bool:
        if self.message.startswith(text, self.position):
            self.position += len(text)
            return True
        return False

    def space(self) -> None:
        while self.peek() and self.peek() in SPACE:
            self.position += 1

    def identifier(self) -> str:
        found = IDENTIFIER.match(self.message, self.position)
        assert found is not None
        self.position = found.end()
        return found[0]

    def close(self) -> None:
        if not self.take("}"):
            self.fail("參數或分支缺少結尾大括號 }")

    def quoted(self, parent: str) -> str | None:
        if self.peek() != "'":
            return None
        following = self.message[self.position + 1 : self.position + 2]
        if following == "'":
            self.position += 2
            return "'"
        if following not in {"{", "}", "<", ">"} and not (
            following == "#" and parent in {"plural", "selectordinal"}
        ):
            return None
        self.position += 1
        literal: list[str] = []
        while self.peek():
            if self.take("''"):
                literal.append("'")
            elif self.take("'"):
                break
            else:
                literal.append(self.peek())
                self.position += 1
        # ICU closes an unterminated message quote at the end of the message.
        return "".join(literal)

    def message_scope(self, parent: str = "", *, nested: bool = False) -> Signature:
        nodes: set[SemanticNode] = set()
        literal: list[str] = []

        def flush_literal() -> None:
            self.literals.update(LITERAL_PARAMETER.findall("".join(literal)))
            literal.clear()

        while self.peek():
            if self.peek() == "}" and nested:
                break
            quote = self.quoted(parent)
            if quote is not None:
                literal.append(quote)
            elif self.peek() == "{":
                flush_literal()
                nodes.add(self.argument())
            elif self.peek() == "#" and parent in {"plural", "selectordinal"}:
                flush_literal()
                self.position += 1
                nodes.add((7,))
            else:
                literal.append(self.peek())
                self.position += 1
        flush_literal()
        return frozenset(nodes)

    def integer(self) -> int:
        sign = -1 if self.take("-") else 1
        if sign == 1:
            self.take("+")
        start = self.position
        while self.peek() and "0" <= self.peek() <= "9":
            self.position += 1
        if start == self.position:
            self.fail("plural offset 或 = 選項後必須是整數")
        value = int(self.message[start : self.position]) * sign
        if abs(value) > 9_007_199_254_740_991:
            self.fail("plural 整數超過可安全表示的範圍")
        return value

    def style(self, kind: str) -> None:
        if not self.take(","):
            return
        self.space()
        start = self.position
        while self.peek():
            if self.take("'"):
                end = self.message.find("'", self.position)
                if end < 0:
                    self.fail("格式樣式的單引號沒有結尾")
                self.position = end + 1
            elif self.peek() == "}":
                # Installed FormatJS ends a named style at its first unquoted close,
                # including after a literal opening brace in the style itself.
                break
            else:
                self.position += 1
        style = self.message[start : self.position].rstrip(JS_TRIM)
        if not style:
            self.fail("number/date/time 的格式樣式不能留空")
        if style.startswith("::"):
            self.skeleton(style[2:].lstrip(JS_TRIM), kind)

    def skeleton(self, text: str, kind: str) -> None:
        if not text:
            self.fail("格式 skeleton 不能留空")
        if kind in {"date", "time"}:
            for match in DATE_PATTERN.finditer(text):
                token = match[0]
                if token[0] in "YuUrQqwWDFbBZOvVXx" or (token[0] in "ec" and len(token) < 4):
                    self.fail(f"FormatJS 不支援日期時間 skeleton {token}")
            return
        for token in re.split(f"[{SPACE}]", text):
            if not token:
                continue
            stem, *options = token.split("/")
            if any(not option for option in options):
                self.fail("number skeleton 的 / 後缺少選項")
            if stem in {"unit", "measure-unit", "integer-width"} and not options:
                self.fail(f"number skeleton {stem} 缺少選項")
            if stem == "integer-width":
                if len(options) > 1:
                    self.fail("integer-width 只能有一個選項")
                for match in INTEGER_WIDTH.finditer(options[0]):
                    if match[3] or match[5]:
                        self.fail("FormatJS 不支援最大或固定整數位數")
            if FRACTION_PRECISION.fullmatch(stem) and len(options) > 1:
                self.fail("小數精度只能有一個選項")
            significant = SIGNIFICANT_PRECISION.fullmatch(stem)
            if FRACTION_PRECISION.fullmatch(stem) and options and options[0] != "w":
                significant = SIGNIFICANT_PRECISION.fullmatch(options[0])
            if significant is not None and not significant[1]:
                self.fail("有效位數 skeleton 必須包含 @")
            if stem.startswith("E") and not re.fullmatch(r"EE?(?:\+!|\+\?)?0+", stem):
                self.fail("科學記號 skeleton 必須指定整數位數")

    def argument(self) -> SemanticNode:
        self.position += 1
        self.space()
        name = self.identifier()
        if not name:
            self.fail("大括號內缺少有效參數名稱")
        self.space()
        if self.take("}"):
            return (1, name)
        if not self.take(","):
            self.fail(f"參數 {name} 後應為逗號或結尾大括號")
        self.space()
        kind = self.identifier()
        self.space()
        if kind in {"number", "date", "time"}:
            self.style(kind)
            self.close()
            return ({"number": 2, "date": 3, "time": 4}[kind], name)
        if kind not in {"select", "plural", "selectordinal"}:
            self.fail(f"參數 {name} 的 ICU 類型 {kind!r} 不受支援")
        if not self.take(","):
            self.fail(f"{kind} 後缺少分隔逗號")
        self.space()
        selector = self.identifier()
        offset = 0
        if kind != "select" and selector == "offset":
            if not self.take(":"):
                self.fail("offset 後缺少冒號")
            self.space()
            offset = self.integer()
            self.space()
            selector = self.identifier()
        options: dict[str, Signature] = {}
        while True:
            if not selector and kind != "select" and self.take("="):
                start = self.position - 1
                self.integer()
                selector = self.message[start : self.position]
            if not selector:
                break
            if selector in options:
                self.fail(f"{kind} 重複選項 {selector}")
            self.space()
            if not self.take("{"):
                self.fail(f"{kind} 選項 {selector} 缺少大括號內容")
            options[selector] = self.message_scope(kind, nested=True)
            self.close()
            self.space()
            selector = self.identifier()
        if "other" not in options:
            self.fail(f"{kind} 必須包含 other 分支")
        self.close()
        branches = tuple(sorted(options.items()))
        if kind == "select":
            return (5, name, branches)
        return (6, name, "cardinal" if kind == "plural" else "ordinal", offset, branches)


def parse_icu(message: str) -> IcuContract:
    parser = _Parser(message)
    try:
        arguments = parser.message_scope()
    except RecursionError as error:
        raise IcuSyntaxError("ICU 分支巢狀層級過深，請簡化文案") from error
    return IcuContract(arguments, frozenset(parser.literals))
