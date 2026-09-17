"""Coordinator-side translation helper.

  l10n.py dump <slug>                      -- print the zh-TW strings, numbered, in document order
  l10n.py build <slug> <locale> <strings.json>
        -- rebuild the zh-TW document with the numbered strings replaced, fix hero/diagram src
           and link urls/texts for the locale, and write <slug>.<locale>.json into $L10N_OUT (default: the current directory)
           (merge it with docs/news-2026-batch-4/merge_locale.py afterwards).

Walking the zh-TW document keeps block types, order, table shape, summary and faq counts
identical by construction, so a translation cannot drift structurally.
"""
import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "apps/api/app/guides/content"
OUT = Path(os.environ.get("L10N_OUT", Path.cwd()))


def slots(doc):
    """(container, key) for every translatable string, in reading order. Link texts are not
    slots: they are the target's title in that locale."""
    found = [(doc, "title"), (doc, "description"), (doc["hero"], "alt")]
    for block in doc["blocks"]:
        kind = block["type"]
        if kind in ("paragraph", "heading"):
            found.append((block, "text"))
        elif kind == "summary":
            found.extend((block["items"], i) for i in range(len(block["items"])))
        elif kind == "table":
            found.extend((block["header"], i) for i in range(len(block["header"])))
            for row in block["rows"]:
                found.extend((row, i) for i in range(len(row)))
            found.append((block, "caption"))
        elif kind == "image":
            found.extend([(block, "alt"), (block, "caption")])
        elif kind == "faq":
            for item in block["items"]:
                found.extend([(item, "question"), (item, "answer")])
        elif kind == "callout":
            found.extend([(block, "title"), (block, "text")])
        elif kind == "link":
            pass
        else:
            raise SystemExit(f"unhandled block type {kind}")
    found.extend((source, "title") for source in doc["sources"])
    return found


def main():
    mode, slug = sys.argv[1], sys.argv[2]
    pack = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))
    zh = pack["locales"]["zh-TW"]
    if mode == "dump":
        for n, (holder, key) in enumerate(slots(zh)):
            print(f"[{n}] {holder[key]}")
        return
    locale, strings_path = sys.argv[3], Path(sys.argv[4])
    strings = json.loads(strings_path.read_text(encoding="utf-8"))
    doc = copy.deepcopy(zh)
    targets = slots(doc)
    if len(strings) != len(targets):
        raise SystemExit(f"{len(strings)} strings for {len(targets)} slots")
    for (holder, key), value in zip(targets, strings):
        if not isinstance(value, str) or not value.strip():
            raise SystemExit(f"empty string at slot for {key}")
        holder[key] = value
    suffix = "-" + locale.lower()
    doc["hero"]["src"] = f"/guides/{slug}/hero{suffix}.jpg"
    for block in doc["blocks"]:
        if block["type"] == "image":
            block["src"] = f"/guides/{slug}/diagram-1{suffix}.svg"
        if block["type"] == "link":
            prefix = "https://mokaair.com/zh-TW/life/"
            assert block["url"].startswith(prefix), block["url"]
            target = block["url"][len(prefix):]
            block["url"] = f"https://mokaair.com/{locale}/life/{target}"
            other = json.loads((CONTENT / f"{target}.json").read_text(encoding="utf-8"))["locales"].get(locale, {})
            block["text"] = other.get("title") or block["text"]
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{slug}.{locale}.json"
    out.write_bytes((json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print("wrote", out)


if __name__ == "__main__":
    main()
