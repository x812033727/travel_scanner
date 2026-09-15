"""Generate five API catalogues from the same stable IDs used by the directory."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
from app.guides.series import Catalogue  # noqa: E402

rows = sorted(json.loads((ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8")), key=lambda row: row["order"])
units = json.loads((ROOT / "apps/web/lib/codex-learning/units.json").read_text(encoding="utf-8"))
sources = json.loads((ROOT / "docs/codex-learning/deep/sources.json").read_text(encoding="utf-8"))
by_id = {row["id"]: row for row in rows}
platforms = ["desktop", "mobile", "cli", "ide", "cloud"]
path_titles = {
    "zh-TW": ["桌面版", "手機", "CLI", "IDE", "雲端"],
    "zh-CN": ["桌面版", "手机", "CLI", "IDE", "云端"],
    "en": ["Desktop", "Mobile", "CLI", "IDE", "Cloud"],
    "ja": ["デスクトップ", "モバイル", "CLI", "IDE", "クラウド"],
    "ko": ["데스크톱", "모바일", "CLI", "IDE", "클라우드"],
}
pending = []
for locale, titles in units.items():
    data = {"slug": "codex", "locale": locale, "hub": "codex-learning-hub", "navigation_by_group": True,
            "groups": [{"id": chr(65 + i), "title": title} for i, title in enumerate(titles)],
            "paths": [{"id": name, "title": path_titles[locale][i], "slugs": [row["slug"] for row in rows if i in row["platforms"]]} for i, name in enumerate(platforms)],
            "entries": [{"slug": row["slug"], "title": row["locales"][locale]["title"],
                         "outcome": row["locales"][locale]["description"],
                         "sources": [source["url"] for source in sources.get(f'{row["id"]:02d}', [])],
                         "number": row["order"], "group": row["unit"],
                         "level": ["beginner", "intermediate", "advanced"][row["level"]],
                         "platforms": [platforms[i] for i in row["platforms"]],
                         "aliases": row["aliases"].split(), "reading_minutes": row["minutes"],
                         "operation_minutes": row.get("operationMinutes"),
                         "prerequisites": [by_id[i]["slug"] for i in row["prerequisites"]],
                         "related": [by_id[i]["slug"] for i in row["related"]]} for row in rows]}
    Catalogue.model_validate(data)
    pending.append((ROOT / f"apps/api/app/guides/series_data/codex-{locale}.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n"))
for path, encoded in pending:
    if "--check" in sys.argv:
        if not path.exists() or path.read_text(encoding="utf-8") != encoded:
            raise SystemExit(f"Stale generated catalogue: {path.name}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encoded, encoding="utf-8")
print("Five Codex API catalogues match the shared lesson manifest")
