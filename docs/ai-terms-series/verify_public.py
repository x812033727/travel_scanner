"""Read-only checks of every reviewed public article, asset, canonical and sitemap."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "apps/api"))
from app.guides.schemas import GuideDocument
from app.guides.service import document_hash

BASE = "https://mokaair.com"
manifest = json.loads((HERE / "release-manifest.json").read_text(encoding="utf-8"))


def get(path):
    request = urllib.request.Request(BASE + path, headers={
        "User-Agent": "Mozilla/5.0 (compatible; MokaairPublicationCheck/1.0)",
        "Cache-Control": "no-cache",
    })
    with urllib.request.urlopen(request, timeout=45) as response:
        assert response.status == 200
        return response.read(), dict(response.headers), response.url


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.robots = []
        self.images = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "link" and attributes.get("rel") == "canonical":
            self.canonical.append(attributes.get("href"))
        if tag == "meta" and attributes.get("name") in {"robots", "googlebot"}:
            self.robots.append(attributes.get("content", ""))
        if tag == "img":
            self.images.append(attributes.get("src", ""))
        if tag == "a":
            self.links.append(attributes.get("href", ""))


def article(slug):
    pack = json.loads((ROOT / "apps/api/app/guides/content" / (slug + ".json")).read_text(encoding="utf-8"))
    desired = GuideDocument.model_validate(pack["locales"]["zh-TW"])
    payload, _, _ = get("/api/travel/guides/life/" + slug + "?locale=zh-TW")
    result = json.loads(payload)
    assert result["status"] == "published" and result["locale"] == "zh-TW", slug
    public = GuideDocument.model_validate({key: result["document"][key] for key in GuideDocument.model_fields})
    wanted_hash = document_hash(desired.model_dump(mode="json"))
    assert document_hash(public.model_dump(mode="json")) == wanted_hash, slug + " content differs"
    path = "/zh-TW/life/" + slug
    raw, headers, url = get(path)
    html = raw.decode("utf-8")
    metadata = Metadata()
    metadata.feed(html)
    assert url == BASE + path, (slug, "redirect")
    assert metadata.canonical == [BASE + path], (slug, metadata.canonical)
    assert all("noindex" not in value.lower() for value in metadata.robots), slug
    assert "noindex" not in next((v for k, v in headers.items() if k.lower() == "x-robots-tag"), "").lower(), slug
    assert desired.title in html and metadata.images, (slug, "missing rendered article")
    if slug != "ai-terms-index":
        assert any(link.endswith("/life/ai-terms-index") for link in metadata.links), slug + " missing index link"
    return {"slug": slug, "url": url, "document_sha256": wanted_hash,
            "version": result["document"]["version"], "canonical": metadata.canonical[0],
            "robots": metadata.robots or ["index, follow (default; no restrictive meta tag)"], "status": "pass"}


def asset(item):
    relative, expected = item
    path = "/" + relative.removeprefix("apps/web/public/")
    data, headers, _ = get(path)
    assert hashlib.sha256(data).hexdigest() == expected, path + " bytes differ"
    return {"path": path, "sha256": expected, "bytes": len(data), "status": "pass"}


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        articles = list(pool.map(article, manifest["slugs"]))
        assets = list(pool.map(asset, [(p, h) for p, h in manifest["files"].items() if p.startswith("apps/web/public/")]))
    xml, _, _ = get("/sitemap.xml")
    locations = {element.text for element in ET.fromstring(xml).iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    expected = {entry["url"] for entry in articles}
    assert expected <= locations, "Missing sitemap pages: " + repr(sorted(expected - locations))
    result = {"checked_at": datetime.now(timezone.utc).isoformat(), "status": "passed",
              "articles": articles, "assets": assets, "sitemap_present": len(expected),
              "search_engine_indexing": "Not measured; sitemap presence and index directives are not proof of search-engine indexing."}
    (HERE / "public-verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"articles": len(articles), "assets": len(assets), "sitemap_present": len(expected), "status": "passed"}))


if __name__ == "__main__":
    main()
