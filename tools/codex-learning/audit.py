"""Audit the generated series using the real API schemas and editorial checks."""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
from app.guides.pack_ingest import lint_all  # noqa: E402

catalog = json.loads((ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8"))
findings = lint_all(ROOT / "apps/api/app/guides/content", ROOT / "apps/web/public",
                    slugs={row["slug"] for row in catalog if row["ready"]} | {"codex-learning-hub"})
report = {slug: [{"level": p.level, "code": p.code, "message": p.message} for p in problems]
          for slug, problems in findings.items() if problems}
out = ROOT / "docs/codex-learning/evidence/content-audit.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
counts = Counter(p["level"] for problems in report.values() for p in problems)
print(json.dumps(dict(counts)))
sys.exit(1 if counts["error"] else 0)
