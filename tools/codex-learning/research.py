"""Fetch official Markdown into an untracked cache for editorial verification."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
import json

root = Path(__file__).resolve().parents[2]
PAGES = sorted({page for path in (root / "docs/codex-learning/lessons").glob("*.json")
                for page in json.loads(path.read_text(encoding="utf-8"))["sources"]})
cache = root / ".codex" / "codex-learning-research"
cache.mkdir(parents=True, exist_ok=True)

def fetch(page):
    url = f"https://learn.chatgpt.com/docs/{page}.md"
    try:
        with urlopen(url, timeout=35) as response:
            body = response.read().decode()
        if body.lstrip().startswith("<!DOCTYPE"):
            return {"page": page, "error": "HTML fallback"}
        (cache / (page.replace("/", "--") + ".md")).write_text(body, encoding="utf-8")
        return {"page": page, "bytes": len(body), "headings": [s for s in body.splitlines() if s.startswith("##")][:12]}
    except Exception as exc:
        return {"page": page, "error": str(exc)}

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(fetch, PAGES):
            print(json.dumps(result, ensure_ascii=False))
