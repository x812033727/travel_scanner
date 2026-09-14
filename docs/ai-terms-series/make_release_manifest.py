"""Pin the accepted article and asset bytes; no production connection."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
catalogue = json.loads((HERE / "catalogue.json").read_text(encoding="utf-8"))
validation = json.loads((HERE / "validation.json").read_text(encoding="utf-8"))
assert not validation["errors"] and not validation["missing"]
assert validation["database"]["published_reads"] == 83
slugs = [t["slug"] for t in catalogue["terms"]] + ["ai-glossary-50-terms", "ai-terms-index"]
files = {}
for slug in slugs:
    path = ROOT / "apps/api/app/guides/content" / f"{slug}.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    doc = pack["locales"]["zh-TW"]
    assets = [doc["hero"]["src"]] + [b["src"] for b in doc["blocks"] if b["type"] == "image"]
    for file in [path] + [ROOT / "apps/web/public" / s.lstrip("/") for s in assets]:
        data = file.read_bytes()
        if file.suffix in {".json", ".svg"}:
            # Match the repository's * text=auto eol=lf contract before pinning bytes.
            normalized = data.replace(b"\r\n", b"\n")
            if normalized != data:
                file.write_bytes(normalized)
            data = normalized
        files[str(file.relative_to(ROOT)).replace("\\", "/")] = hashlib.sha256(data).hexdigest()
manifest = {
    "locale": "zh-TW", "slugs": slugs, "index_last": "ai-terms-index", "files": files,
    "text_line_endings": "LF, matching .gitattributes and deployed git archive bytes",
    "new_slugs": [t["slug"] for t in catalogue["terms"] if t["action"] == "new"] + ["ai-terms-index"],
    "updated_slugs": [t["slug"] for t in catalogue["terms"] if t["action"] != "new"] + ["ai-glossary-50-terms"],
}
(HERE / "release-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"Pinned {len(slugs)} article packs and {len(files)-len(slugs)} assets.")
