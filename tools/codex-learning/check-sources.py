"""Read-only source URL health check; does not replace the article's factual review."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
sources = json.loads((ROOT / "docs/codex-learning/deep/sources.json").read_text(encoding="utf-8"))
urls = sorted({source["url"] for entries in sources.values() for source in entries})


def check(url):
    record = {"url": url, "attempts": []}
    # Some documentation hosts reject HEAD while serving the actual page normally.
    # Preserve both responses instead of treating a HEAD-only failure as a dead link.
    for method in ("HEAD", "GET"):
        attempt = {"method": method}
        request = urllib.request.Request(url, method=method, headers={"User-Agent": "CodexLearningSourceCheck/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                attempt.update(status=response.status, resolvedUrl=response.url)
        except urllib.error.HTTPError as error:
            attempt.update(status=error.code, resolvedUrl=error.url)
        except (OSError, urllib.error.URLError) as error:
            attempt.update(error=type(error).__name__)
        record["attempts"].append(attempt)
        if 200 <= attempt.get("status", 0) < 400:
            break
    record.update(record["attempts"][-1])
    return record


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, urls))
report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "scope": "Public source URL response only; not factual or authenticated-surface verification", "sources": results}
(ROOT / "docs/codex-learning/evidence/source-health.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
attention = [result for result in results if result.get("status", 0) >= 400 or "error" in result]
print(json.dumps({"checked": len(results), "needsReview": attention}, indent=2))
