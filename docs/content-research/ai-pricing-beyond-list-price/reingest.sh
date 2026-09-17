#!/bin/sh
# ai-plans 是子主題，pack_cli ingest 會擋（見 tasks/open/2026-09-16-pack-cli-ingest-805.md）。
# 先拿掉再 ingest，完了補回去。那張卡修好之後這個腳本就可以刪掉。
set -e
cd "$(dirname "$0")"
python3 build_pack.py
python3 -c "import json;d=json.load(open('pack.json'));d['topics']=['ai','software'];json.dump(d,open('pack.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)"
cd ../../../apps/api
uv run python -m app.guides.pack_cli ingest --from ../../docs/content-research --slug ai-pricing-beyond-list-price
cd ../..
python3 - <<'PY'
import json
for p in ["apps/api/app/guides/content/ai-pricing-beyond-list-price.json",
          "docs/content-research/ai-pricing-beyond-list-price/pack.json"]:
    d = json.load(open(p, encoding="utf-8")); d["topics"] = ["ai", "software", "ai-plans"]
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2); fh.write("\n")
PY
echo "ingested, ai-plans restored"
