"""Fill the Simplified Chinese label of every hotspot seed from its Traditional one.

Wikidata is the source for the English, Japanese and Korean labels, but its
``zh-cn`` label is not dependable for this: of the 239 it had, 26 were still
written in Traditional characters and several pointed at a different place
entirely (Lumphini Park came back as「是樂園」). A label that is not actually
Simplified is worse than none, because it silently replaces the fallback.

So Simplified is derived from the Traditional name instead, with OpenCC's
``t2s`` table. Traditional to Simplified is a character conversion, so the input
fully determines the output: no vendor call, no cost, and no chance of a rename
(鄭王廟 becomes 郑王庙, never 黎明寺). Japanese character forms in the seed names are
first mapped to Traditional (``SHINJITAI_TO_TRADITIONAL``), because ``t2s`` does not
know them. Every result is still checked before it is kept:

* the same number of characters — a phrase-table entry that changed the length
  would be a rewrite, not a conversion;
* only Han characters replaced, and only by other Han characters, so Latin,
  digits, spacing and punctuation survive exactly as given.

Anything that fails is dropped, and the seed keeps falling back to Traditional.
The output is written into the checked-in bootstrap files, so the whole change is
reviewed in the diff like every other seed edit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

from opencc import OpenCC

BOOTSTRAP_DIR = Path(__file__).resolve().parent

# Japanese shinjitai → Traditional, applied before ``t2s``. Seed names of Japanese
# places keep their Japanese spelling (楽水園, 円頓寺商店街, 天神／薬院), and OpenCC has
# no mapping for Japanese forms, so without this they pass through untouched and the
# zh-CN label mixes Japanese characters into Simplified. Each entry was checked to
# simplify to the standard character through ``t2s``. Left out on purpose: forms
# ``t2s`` already handles (国, 将, 横), and 浜, which is also a Chinese character in
# its own right (沙家浜) and must not become 滨. Kana are never mapped.
SHINJITAI_TO_TRADITIONAL = str.maketrans(
    {
        "楽": "樂",
        "桜": "櫻",
        "円": "圓",
        "薬": "藥",
        "沢": "澤",
        "関": "關",
        "駅": "驛",
        "広": "廣",
        "県": "縣",
        "竜": "龍",
        "恵": "惠",
        "栄": "榮",
        "売": "賣",
        "両": "兩",
        "乗": "乘",
        "鉄": "鐵",
        "塩": "鹽",
        "蔵": "藏",
        "稲": "稻",
        "歩": "步",
        "渓": "溪",
        "滝": "瀧",
        "豊": "豐",
        "戸": "戶",
    }
)


@cache
def _converter() -> OpenCC:
    # Loading the dictionaries reads several files; one instance serves every call.
    return OpenCC("t2s")


def to_simplified(traditional: str) -> str:
    return str(_converter().convert(traditional.translate(SHINJITAI_TO_TRADITIONAL)))


def acceptable(traditional: str, simplified: str) -> bool:
    """True when ``simplified`` has the shape of a conversion of ``traditional``.

    Shape only: this cannot tell a conversion from a same-length rename into
    different Han characters. With OpenCC doing the conversion there is no rename
    to catch; the check stays for a mapping file applied with ``--from-mapping``,
    which may have been produced or edited elsewhere, and as a guard on OpenCC's
    phrase table.

    Deliberately list-free. An earlier attempt screened the result against a
    hand-written set of Traditional-only characters and kept mis-classifying
    characters written the same in both scripts (高, 首, 秘), rejecting correct
    conversions.
    """
    if len(simplified) != len(traditional):
        return False
    for original, converted in zip(traditional, simplified, strict=True):
        if original == converted:
            continue
        # A character may only be replaced by another Han character.
        if not ("一" <= original <= "鿿" and "一" <= converted <= "鿿"):
            return False
    return True


@dataclass
class ConversionReport:
    converted: dict[str, str] = field(default_factory=dict)
    unchanged: list[str] = field(default_factory=list)
    rejected: list[tuple[str, str]] = field(default_factory=list)


def convert_names(names: list[str]) -> ConversionReport:
    """Convert each Traditional name, keeping only results that pass ``acceptable``."""
    report = ConversionReport()
    for name in dict.fromkeys(names):
        if not name.strip():
            continue
        simplified = to_simplified(name)
        if simplified == name:
            # Plenty of names are written identically in both scripts.
            report.unchanged.append(name)
        elif acceptable(name, simplified):
            report.converted[name] = simplified
        else:
            report.rejected.append((name, simplified))
    return report


def seed_rows(paths: list[Path]) -> list[tuple[Path, list[dict[str, Any]]]]:
    loaded: list[tuple[Path, list[dict[str, Any]]]] = []
    for path in paths:
        rows = json.loads(path.read_text(encoding="utf-8"))
        loaded.append((path, rows if isinstance(rows, list) else []))
    return loaded


def stored_label_count(rows: list[dict[str, Any]]) -> int:
    """How many rows currently carry a zh-CN label, for the run to report."""
    return sum(
        1
        for row in rows
        if isinstance(row.get("names"), dict) and isinstance(row["names"].get("zh-CN"), str)
    )


def apply_conversions(rows: list[dict[str, Any]], converted: dict[str, str]) -> int:
    """Write each conversion onto its row, and clear a label with no conversion.

    Clearing happens here, per row, rather than in a separate pass beforehand.
    That earlier shape was the bug: it emptied every zh-CN label first, so a run
    whose conversions all failed still wrote the stripped rows out and reported
    success. A row now only loses its label in the same step that could replace it.
    """
    written = 0
    for row in rows:
        names = row.get("names")
        if not isinstance(names, dict):
            continue
        simplified = converted.get(str(row.get("name")))
        current = names.get("zh-CN")
        if simplified:
            if current != simplified:
                names["zh-CN"] = simplified
                written += 1
        elif isinstance(current, str):
            names.pop("zh-CN")
            written += 1
    return written


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
