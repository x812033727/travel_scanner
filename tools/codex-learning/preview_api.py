"""Read-only localhost fixture. All publication states below are synthetic for UI QA.

Never point production at this server. Run with Python; it binds only 127.0.0.1:8123.
"""
import json
import asyncio
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
from app.guides import series as series_service  # noqa: E402
from app.guides.schemas import ArticleReference, GuideDocument  # noqa: E402
PACKS = {p.stem: json.loads(p.read_text(encoding="utf-8"))
         for p in (ROOT / "apps/api/app/guides/content").glob("codex-*.json")}
STAMP = "2026-09-14T00:00:00Z"
DOCUMENTS = {(slug, locale): GuideDocument.model_validate(document)
             for slug, pack in PACKS.items() for locale, document in pack["locales"].items()}


async def fixture_documents(_session, locale, targets):
    return {slug: (ArticleReference(kind="life", slug=slug, title=PACKS[slug]["locales"][locale]["title"]),
                   DOCUMENTS[(slug, locale)])
            for kind, slug in targets if kind == "life" and slug in PACKS and locale in PACKS[slug]["locales"]}


# This standalone fixture replaces only the database lookup, exercising real catalogue
# and navigation logic against explicitly synthetic published documents.
series_service.published_documents = fixture_documents


def summary(pack, locale):
    doc = pack["locales"][locale]
    return {"slug": pack["slug"], "kind": "life", "destination_id": None,
            "destination_label": None, "topics": [], "title": doc["title"],
            "description": doc["description"], "hero": doc["hero"],
            "published_at": STAMP, "valid_until": None, "featured": False}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        locale = query.get("locale", ["zh-TW"])[0]
        body = {}
        status = 200
        if url.path == "/api/v1/guides":
            rows = [] if query.get("section") == ["travel"] else [summary(p, locale) for p in PACKS.values() if locale in p["locales"]]
            offset = int(query.get("cursor", ["0"])[0])
            limit = int(query.get("limit", ["12"])[0])
            body = {"articles": rows[offset:offset + limit], "next_cursor": str(offset + limit) if offset + limit < len(rows) else None}
        elif url.path.startswith("/api/v1/guides/series/"):
            series = asyncio.run(series_service.public_series(None, url.path.rsplit("/", 1)[-1], locale))
            if series is None:
                status = 404
            else:
                body = series.model_dump(mode="json")
        elif url.path.startswith("/api/v1/guides/life/"):
            slug = url.path.rsplit("/", 1)[-1]
            pack = PACKS.get(slug)
            if pack and locale in pack["locales"]:
                document = DOCUMENTS[(slug, locale)]
                navigation = asyncio.run(series_service.article_navigation(None, "life", slug, locale))
                links = asyncio.run(series_service.resolve_article_links(None, locale, document))
                body = {**summary(pack, locale), "locale": locale, "status": "published", "expired": False,
                        "published_locales": list(pack["locales"]),
                        "series": navigation.model_dump(mode="json") if navigation else None,
                        "article_links": [link.model_dump(mode="json") for link in links],
                        "document": {**pack["locales"][locale], "version": 1, "published_at": STAMP, "modified_at": STAMP}}
            else:
                status = 404
        elif url.path == "/api/v1/guides/topics":
            body = {"topics": []}
        else:
            status = 404
        payload = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    print("Synthetic publication fixture at http://127.0.0.1:8123", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8123), Handler).serve_forever()
