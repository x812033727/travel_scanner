"""Mechanical checks on translations that a schema cannot see: ``translation_checks.py <prefix>``.

Batch 4.2 had its drafts translated by a smaller model, and one Japanese article came back with whole
runs of mistyped kanji (北竹 for 北竿), Korean had syllables that do not exist (겑), and the Chinese
names quoted inside English and Korean text had typos (海翆 for 海纜). The per-language reviewers caught
them, but these three detectors are cheap and catch the same class before a reviewer reads a word:

* ja: kanji Shift_JIS cannot encode -- a corrupted character, or a Chinese form that was never converted
* ko: Hangul syllables outside KS X 1001 (EUC-KR) -- almost always a typo
* en/ko: runs of CJK quoted in the translation that do not occur in the zh-TW original

Legitimate hits remain (a Taiwanese place name such as 莒光, a quoted Chinese title); read the list.
It only reads the packs, so any Python will do.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "apps/api/app/guides/content"
RUN = re.compile(r"[㐀-䶿一-鿿]{2,}")


def unencodable(text: str, pattern: str, codec: str) -> list[str]:
    found = []
    for match in re.finditer(pattern, text):
        try:
            match.group(0).encode(codec)
        except UnicodeEncodeError:
            found.append(text[max(0, match.start() - 6):match.end() + 5].replace("\n", " "))
    return found


def main() -> int:
    prefix = sys.argv[1] if len(sys.argv) > 1 else "tech-news-"
    hits = 0
    for path in sorted(CONTENT.glob(prefix + "*.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        locales = pack["locales"]
        zh = json.dumps(locales["zh-TW"], ensure_ascii=False)
        zh_all = zh + zh.replace("臺", "台") + zh.replace("台", "臺")
        for locale, doc in locales.items():
            text = json.dumps(doc, ensure_ascii=False)
            found = []
            if locale == "ja":
                found = unencodable(text, r"[㐀-鿿]", "cp932")
            elif locale == "ko":
                found = unencodable(text, r"[가-힣]", "euc_kr")
            if locale in ("en", "ko"):
                found += sorted({run for run in RUN.findall(text) if run not in zh_all})
            if found:
                hits += len(found)
                print(pack["slug"], locale, found[:12])
    print(hits, "hit(s) to read")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
