#!/bin/sh
# Rebuild pack.json from build_pack.py and ingest it into apps/api/app/guides/content/.
# pack_cli ingest accepts the ai-plans sub-topic since tasks/done/2026-09-16-pack-cli-ingest-805.md,
# so the old remove-and-restore step around ingest is gone.
# Ingest also re-renders hero.jpg from hero.svg. When only the text changed, pass a scratch
# folder as PUBLIC_DIR so the committed pictures stay byte-identical (done on 2026-10-06).
set -e
cd "$(dirname "$0")"
python3 build_pack.py
cd ../../../apps/api
if [ -n "$PUBLIC_DIR" ]; then
  uv run python -m app.guides.pack_cli --public-dir "$PUBLIC_DIR" ingest --from ../../docs/content-research --slug ai-model-comparison-table-2026
else
  uv run python -m app.guides.pack_cli ingest --from ../../docs/content-research --slug ai-model-comparison-table-2026
fi
