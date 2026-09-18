"""What a per-language reviewer reads: ``review_dumps.py <crypto|tech|ai> <out-dir>``.

Writes ``<out-dir>/<slug>.<locale>.txt`` for every pack of the vertical and every translated
locale: each reader-visible string as a pair -- ``ZH:`` the zh-TW original, then the
translation -- in reading order, followed by the closing links (read-only, they are the
target's title) and the words drawn on the artwork from the research record.

Batch 4.1's reviewers were first pointed at the pack JSON itself. A pack holds five locales, so
a reviewer of one language read four it had no use for, and lining a sentence up with its
original meant counting blocks by hand; twelve reviewers each reading four articles came to
about half the tokens once they read these files instead. The strings printed here are the
parsed JSON values, which is what ``apply_corrections.py`` matches ``old`` against, so a
reviewer can copy ``old`` straight out of a dump.

Run from ``apps/api`` with the API virtualenv, before or after ``pack_cli relink``: a
``rich_paragraph`` is printed one text inline at a time, because a correction may not span
inlines either.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verticals import BY_NAME, CONTENT, LOCALES, ROOT, block_kind, link_of  # noqa: E402


def strings(document: dict) -> list[tuple[str, str]]:
    """``(where, text)`` for every translatable string, in reading order. Closing links are
    left out: their text is the target's title in that locale, not the translator's."""
    found = [("title", document["title"]), ("description", document["description"]),
             ("hero.alt", document["hero"]["alt"])]
    for n, block in enumerate(document["blocks"]):
        kind, where = block["type"], f"block{n}.{block['type']}"
        if kind in ("paragraph", "heading"):
            found.append((where, block["text"]))
        elif kind == "rich_paragraph":
            if block_kind(block) == "link":
                continue
            found.extend((f"{where}.inline{i}", node["text"])
                         for i, node in enumerate(block["inlines"]) if node["type"] == "text")
        elif kind == "summary":
            found.extend((f"{where}[{i}]", item) for i, item in enumerate(block["items"]))
        elif kind == "table":
            found.extend((f"{where}.header[{i}]", cell) for i, cell in enumerate(block["header"]))
            for r, row in enumerate(block["rows"]):
                found.extend((f"{where}.row{r}[{i}]", cell) for i, cell in enumerate(row))
            found.append((f"{where}.caption", block.get("caption", "")))
        elif kind == "image":
            found.extend([(f"{where}.alt", block["alt"]), (f"{where}.caption", block.get("caption", ""))])
        elif kind == "faq":
            for q, item in enumerate(block["items"]):
                found.extend([(f"{where}{q}.question", item["question"]), (f"{where}{q}.answer", item["answer"])])
        elif kind == "callout":
            found.extend([(f"{where}.title", block.get("title", "")), (f"{where}.text", block["text"])])
        elif kind != "link":
            raise SystemExit(f"unhandled block type {kind}")
    found.extend((f"source{i}.title", source["title"]) for i, source in enumerate(document["sources"]))
    return found


def dump(pack: dict, record: dict, locale: str) -> str:
    zh, doc = pack["locales"]["zh-TW"], pack["locales"][locale]
    pairs = list(zip(strings(zh), strings(doc), strict=False))
    lines = [f"# {pack['slug']}  ({locale})", '# PACK -- file: "pack". ZH is the verified original; never edit it.', ""]
    if len(strings(zh)) != len(strings(doc)):
        # relink and autolink run per locale, so the inline split can differ; the pairs are
        # still printed, and the reviewer is told they may not line up after this point.
        lines.insert(2, "# NOTE: zh-TW and this locale split their paragraphs differently; pairs may drift.")
    for n, ((_, original), (where, text)) in enumerate(pairs):
        lines += [f"[{n}] {where}", f"ZH: {original}", f"{locale}: {text}", ""]
    lines.append("# CLOSING LINKS (read-only: the text is the target article's title in this locale)")
    for block in doc["blocks"]:
        if block_kind(block) == "link":
            target, text = link_of(block, locale)
            lines.append(f"- {text}  <{target}>")
    drawn = record.get("translations", {}).get(locale, {})
    lines += ["", f'# ARTWORK TEXT -- file: "research" (translations.{locale}); the diagram caption equals the image caption above',
              f"ZH hero_label: {record.get('hero_label')}",
              f"ZH diagram title: {(record.get('diagram') or {}).get('title')}",
              f"ZH nodes: {json.dumps((record.get('diagram') or {}).get('nodes'), ensure_ascii=False)}",
              f"{locale} hero_label: {drawn.get('hero_label')}",
              f"{locale} diagram title: {(drawn.get('diagram') or {}).get('title')}",
              f"{locale} nodes: {json.dumps((drawn.get('diagram') or {}).get('nodes'), ensure_ascii=False)}"]
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) < 3 or sys.argv[1] not in BY_NAME:
        print("usage: review_dumps.py <" + "|".join(BY_NAME) + "> <out-dir> [slug...]")
        return 2
    vertical, out = BY_NAME[sys.argv[1]], Path(sys.argv[2])
    # Only the articles named, when a later batch adds a few to a vertical whose earlier
    # packs were reviewed already (and whose research records may live in another workspace).
    only = set(sys.argv[3:])
    out.mkdir(parents=True, exist_ok=True)
    written = 0
    for path in sorted(CONTENT.glob(f"{vertical.prefix}*.json")):
        if only and path.stem not in only:
            continue
        pack = json.loads(path.read_text(encoding="utf-8"))
        research = ROOT / vertical.workspace / "research" / f"{pack['slug']}.json"
        record = json.loads(research.read_text(encoding="utf-8")) if research.is_file() else {}
        for locale in LOCALES[1:]:
            if locale not in pack["locales"]:
                print(f"skipped {pack['slug']} {locale}: not merged yet")
                continue
            (out / f"{pack['slug']}.{locale}.txt").write_bytes(dump(pack, record, locale).encode("utf-8"))
            written += 1
    print(f"wrote {written} files to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
