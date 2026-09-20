"""Check the Korea specials batch's cross-pack editorial invariants.

Run from any directory: python docs/korea-food-specials/verification/check_batch.py
The pack CLI remains the authority for each pack's schema and assets.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "docs/korea-food-specials/README.md"
CONTENT = ROOT / "apps/api/app/guides/content"
ASSETS = ROOT / "apps/web/public/guides"
REPORTS = ROOT / "docs/korea-food-specials/verification"
ALLOWED_CAFE_TYPES = {"網美", "咖啡品質", "韓屋", "海景"}


def main() -> int:
    slugs = re.findall(r"^\|[^|]+\|\s*`([a-z0-9-]+-guide)`\s*\|", DOC.read_text(encoding="utf-8"), re.M)
    problems: list[str] = []
    if len(slugs) != 22 or len(set(slugs)) != 22:
        problems.append(f"README inventory has {len(slugs)} rows and {len(set(slugs))} unique slugs; expected 22")
    heroes: dict[str, str] = {}
    aliases: dict[str, str] = {}
    for slug in slugs:
        path = CONTENT / f"{slug}.json"
        if not path.is_file():
            problems.append(f"{slug}: missing pack")
            continue
        pack = json.loads(path.read_text(encoding="utf-8"))
        doc = pack["locales"].get("zh-TW", {})
        if pack["slug"] != slug or pack["kind"] != "howto" or len(pack["topics"]) != 1:
            problems.append(f"{slug}: slug, kind or one-topic invariant failed")
        if set(pack["locales"]) != {"zh-TW"}:
            problems.append(f"{slug}: batch should contain only zh-TW")
        asset_dir = ASSETS / slug
        hero = asset_dir / Path(doc.get("hero", {}).get("src", "")).name
        if not hero.is_file():
            problems.append(f"{slug}: missing hero")
        else:
            digest = hashlib.sha256(hero.read_bytes()).hexdigest()
            if digest in heroes:
                problems.append(f"{slug}: hero duplicates {heroes[digest]}")
            heroes[digest] = slug
        if not (asset_dir / "diagram-1.svg").is_file() or not list(asset_dir.glob("photo-*")):
            problems.append(f"{slug}: diagram or inline photo missing")
        for alias in pack.get("aliases", {}).get("zh-TW", []):
            key = alias.casefold()
            if key in aliases and aliases[key] != slug:
                problems.append(f"{slug}: alias {alias!r} duplicates {aliases[key]}")
            aliases[key] = slug
        for n in (1, 2):
            if not (REPORTS / slug / f"verify-{n}.md").is_file():
                problems.append(f"{slug}: missing verify-{n} report")
        for source in doc.get("sources", []):
            title = source.get("title", "")
            if not title or title.count("（") != title.count("）"):
                problems.append(f"{slug}: malformed source title {title!r}")
            if not source.get("url") or not source.get("checked_on"):
                problems.append(f"{slug}: source missing URL or check date")
        if pack["topics"] == ["cafe"]:
            tables = [b for b in doc.get("blocks", []) if b.get("type") == "table" and "類型" in b.get("header", [])]
            if len(tables) != 1:
                problems.append(f"{slug}: expected one cafe type table")
            for table in tables:
                col = table["header"].index("類型")
                for row in table.get("rows", []):
                    types = {part.strip() for part in re.split(r"[、/／]", row[col]) if part.strip()}
                    if not types or not types <= ALLOWED_CAFE_TYPES:
                        problems.append(f"{slug}: {row[0]} lacks a supported type: {row[col]}")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"{len(slugs)} packs, {len(slugs) * 2} reviews; topics, cafe types, assets, aliases and hero uniqueness checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
