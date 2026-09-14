"""Check the catalogue's primary sources; keep full fetches in a temporary cache only."""
import hashlib
import json
import re
import html
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "apps/api/app/guides/series_data/claude-code.json"
CACHE = Path(tempfile.gettempdir()) / "mokaair-claude-code-sources"
CACHE.mkdir(exist_ok=True)
checked = datetime.now(ZoneInfo("Asia/Taipei")).date().isoformat()


def fetch(url):
    with httpx.Client(follow_redirects=True, timeout=40) as client:
        response = client.get(url + ".md" if url.startswith("https://code.claude.com/") else url)
        body = response.text
        # Several documentation sections have a quickstart page. Keep their cached
        # documents distinct when a future research pass retrieves them in parallel.
        path = CACHE / (hashlib.sha256(url.encode()).hexdigest()[:16] + "-" + url.rsplit("/", 1)[1] + ".md")
        path.write_text(body, encoding="utf-8")
        title = next((line.lstrip("# ") for line in body.splitlines() if line.startswith("# ")), "")
        if not title:
            match = re.search(r"<title[^>]*>(.*?)</title>", body, re.S)
            title = html.unescape(match.group(1)) if match else ""
        return {"url": url, "fetched_url": str(response.url), "status": response.status_code,
                "checked_on": checked, "title": title, "sha256": hashlib.sha256(response.content).hexdigest(),
                "bytes": len(response.content), "verification": "official-documentation",
                "product_operation_tested": False}


if __name__ == "__main__":
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    urls = sorted({url for entry in manifest["entries"] for url in entry["sources"]})
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch, urls))
    output = ROOT / "docs/claude-code-series/source-checks.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checked": len(results), "cache": str(CACHE),
                      "failures": [entry for entry in results if entry["status"] != 200 or not entry["title"]]}, ensure_ascii=False))
