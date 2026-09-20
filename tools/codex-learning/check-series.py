"""Verify all authored references and locale code against the final draft packs."""
from collections import Counter
from datetime import date, datetime, timezone
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("depth_compiler", Path(__file__).with_name("build-depth.py"))
depth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(depth)
catalog = json.loads((ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8"))
build = json.loads((ROOT / "docs/codex-learning/deep/build-report.json").read_text(encoding="utf-8"))
build_by_id = {row["id"]: row for row in build["lessons"]}
assert len(catalog) == 60 and {row["id"] for row in catalog} == set(range(1, 61))
assert all(row["ready"] for row in catalog)
assert len(build_by_id) == 60 and all(row["compiled"] and row["fullFiveLocales"] for row in build_by_id.values())
locales = ["zh-TW", "zh-CN", "en", "ja", "ko"]
known = {row["slug"] for row in catalog} | {"codex-learning-hub"}
report = []


def authored_links(nodes):
    for node in nodes:
        if node["type"] == "link":
            yield node["attrs"]["url"]
        yield from authored_links(node.get("children", []))


for row in sorted(catalog, key=lambda item: item["order"]):
    pack_path = ROOT / f'apps/api/app/guides/content/{row["slug"]}.json'
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    assert set(pack["locales"]) == set(locales)
    expected_hash = build_by_id[row["id"]]["packHash"]
    # Match the compiler's canonical UTF-8/LF hash on Windows and Unix checkouts.
    assert sha256(pack_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest() == expected_hash, row["slug"]
    code_reference = None
    link_counts = {}
    image_counts = {}
    for locale in locales:
        if locale == "zh-CN":
            source = depth.simplified((ROOT / f'docs/codex-learning/deep/zh-TW/{row["id"]:02d}.md').read_text(encoding="utf-8"))
        else:
            source = (ROOT / f'docs/codex-learning/deep/{locale}/{row["id"]:02d}.md').read_text(encoding="utf-8")
        expected_links = Counter(authored_links(depth.parse(source)))
        document = pack["locales"][locale]
        blocks = document["blocks"]
        actual_links = Counter()
        for block in blocks:
            if block["type"] == "link":
                actual_links[block["url"]] += 1
            for node in block.get("inlines", []):
                if node["type"] == "article":
                    assert node["slug"] in known
                    actual_links["article:" + node["slug"]] += 1
                elif node["type"] == "link":
                    actual_links[node["url"]] += 1
        assert actual_links == expected_links, (row["id"], locale, expected_links - actual_links, actual_links - expected_links)
        assert actual_links["article:codex-learning-hub"] >= 2
        code_blocks = [(block["language"], block["code"]) for block in blocks if block["type"] == "code"]
        if code_reference is None:
            code_reference = code_blocks
        assert code_blocks == code_reference
        assert all(block["label"].strip() for block in blocks if block["type"] == "code")
        assert document["sources"]
        for source in document["sources"]:
            checked_on = date.fromisoformat(source["checked_on"])
            assert date(2026, 9, 14) <= checked_on <= datetime.now(timezone.utc).date(), source
        images = [block for block in blocks if block["type"] == "image"]
        assert images and all(image.get("alt") and image.get("caption") and image.get("credit") for image in images)
        assert all((ROOT / "apps/web/public" / image["src"].lstrip("/")).is_file() for image in images)
        link_counts[locale] = sum(actual_links.values())
        image_counts[locale] = len(images)
    report.append({"id": row["id"], "order": row["order"], "slug": row["slug"], "stage": "drafted",
                   "packHash": expected_hash, "fiveLocaleCodeEqual": True,
                   "allAuthoredLinksPreserved": True, "linksByLocale": link_counts,
                   "imagesByLocale": image_counts,
                   "previewAccepted": False, "published": False})

summary = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "passed",
           "scope": "Static draft integrity; not editorial acceptance, browser acceptance or publication",
           "lessons": report, "lessonCount": len(report), "languageDocumentCountIncludingHub": 305,
           "limitations": ["Product UI and platform evidence remains separately labeled",
                           "Final integrated browser run is pending after preview startup was blocked",
                           "Published visibility is verified by runtime API tests, not inferred from ready"]}
(ROOT / "docs/codex-learning/evidence/series-integrity.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("60 lessons / 300 lesson documents: every authored link retained, five-locale code identical, images and sources present")
