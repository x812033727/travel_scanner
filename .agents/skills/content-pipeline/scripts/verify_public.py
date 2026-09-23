"""Verify published article pages the way a logged-out reader sees them, one request at a time.

    <PY> verify_public.py --slug <S1> --slug <S2> --kind howto --locale zh-TW [--sitemap]
    <PY> verify_public.py --url-list urls.txt [--sitemap]
    <PY> verify_public.py --from-report report.json [--kind howto] [--locale zh-TW]
    ... [--base https://mokaair.com] [--content-dir DIR] [--interval 1.3]

URL shape: life articles live at ``/<locale>/life/<slug>``, everything else at
``/<locale>/guides/<kind>/<slug>``. ``--kind`` may be omitted when the pack can be read from the
content directory, which also supplies the expected title. ``--from-report`` takes the JSON a
``guides-import`` run printed (a dry run's ``articles[]`` or a publish's ``created``,
``updated`` and ``published`` lists) and derives slug and locale from it.

Per page: HTTP 200; the ``<h1>`` equals the pack's title for that locale when the pack is
readable; ``<link rel="canonical">`` equals the URL; no ``noindex`` in the robots meta or the
``X-Robots-Tag`` header; every ``/guides/<slug>/...`` image the page references (hero, photos,
diagrams) answers 200. ``--sitemap`` also walks the sitemap index and requires every URL to be
listed.

Requests go out sequentially with at least ``--interval`` seconds between them: the site
rate-limits public reads, and a parallel run trips the limit and reports false failures. The
User-Agent is the editorial one and nothing personal is sent. Exit 1 on any problem.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONTENT_DIR = SKILL_ROOT / "apps" / "api" / "app" / "guides" / "content"
USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"

H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
CANONICAL = re.compile(
    r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"|<link[^>]+href="([^"]+)"[^>]+rel="canonical"',
    re.I,
)
ROBOTS = re.compile(
    r'<meta[^>]+name="robots"[^>]+content="([^"]*)"|<meta[^>]+content="([^"]*)"[^>]+name="robots"',
    re.I,
)
LOC = re.compile(r"<loc>([^<]+)</loc>")


class Fetcher:
    """Sequential HTTP GET with a fixed pause between requests."""

    def __init__(self, interval: float) -> None:
        self.interval = interval
        self._last = 0.0

    def get(self, url: str) -> tuple[int, str, dict[str, str]]:
        wait = self.interval - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})  # noqa: S310
        try:
            with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
                body = response.read().decode("utf-8", "replace")
                return response.status, body, {k.lower(): v for k, v in response.headers.items()}
        except urllib.error.HTTPError as error:
            return error.code, "", {}
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            return 0, str(error), {}
        finally:
            self._last = time.monotonic()


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG.sub("", text))).strip()


def read_pack(content_dir: Path, slug: str) -> dict[str, Any] | None:
    path = content_dir / f"{slug}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def article_url(base: str, locale: str, kind: str, slug: str) -> str:
    if kind == "life":
        return f"{base}/{locale}/life/{slug}"
    return f"{base}/{locale}/guides/{kind}/{slug}"


def targets_from_report(report: dict[str, Any], default_locale: str) -> list[tuple[str, str]]:
    """(slug, locale) pairs from a guides-import dry run or publish report."""
    pairs: list[tuple[str, str]] = []
    for article in report.get("articles", []):
        for entry in article.get("locales", []):
            pairs.append((article["slug"], entry.get("locale", default_locale)))
    for key in ("created", "updated", "published"):
        for item in report.get(key, []) or []:
            if isinstance(item, str):
                slug, _, locale = item.partition(":")
                pairs.append((slug, locale or default_locale))
            elif isinstance(item, dict) and "slug" in item:
                pairs.append((item["slug"], item.get("locale", default_locale)))
    seen: set[tuple[str, str]] = set()
    unique = []
    for pair in pairs:
        if pair not in seen:
            seen.add(pair)
            unique.append(pair)
    return unique


def check_page(
    fetcher: Fetcher, url: str, base: str, slug: str | None, expected_title: str | None
) -> list[str]:
    status, body, headers = fetcher.get(url)
    if status != 200:
        return [f"status {status}"]
    problems = []
    robots = ROBOTS.search(body)
    robots_value = (robots.group(1) or robots.group(2) or "") if robots else ""
    if "noindex" in robots_value.lower() or "noindex" in headers.get("x-robots-tag", "").lower():
        problems.append("noindex")
    canonical = CANONICAL.search(body)
    canonical_value = (canonical.group(1) or canonical.group(2)) if canonical else None
    if canonical_value is None or canonical_value.rstrip("/") != url.rstrip("/"):
        problems.append(f"canonical {canonical_value!r}")
    h1 = H1.search(body)
    title = clean(h1.group(1)) if h1 else ""
    if not title:
        problems.append("no h1")
    elif expected_title is not None and title != clean(expected_title):
        problems.append(f"h1 {title!r} != pack title {clean(expected_title)!r}")
    if slug:
        images = sorted(
            set(re.findall(rf"/guides/{re.escape(slug)}/[\w.-]+\.(?:jpg|jpeg|webp|png|svg)", body))
        )
        if not images:
            problems.append("no /guides/<slug>/ image referenced")
        for image in images:
            code, _, _ = fetcher.get(f"{base}{image}")
            if code != 200:
                problems.append(f"{image} -> {code}")
    return problems


def sitemap_membership(fetcher: Fetcher, base: str, urls: list[str]) -> list[str]:
    status, index, _ = fetcher.get(f"{base}/sitemap.xml")
    if status != 200:
        return [f"sitemap index -> {status}"]
    children = LOC.findall(index)
    print(f"info sitemap index lists {len(children)} sitemaps")
    wanted = set(urls)
    found: set[str] = set()
    for child in children:
        if wanted <= found:
            break
        code, xml, _ = fetcher.get(child)
        if code != 200:
            print(f"WARN sitemap {child} -> {code}")
            continue
        found.update(u for u in wanted if f"<loc>{u}</loc>" in xml)
    return [f"not in sitemap: {u}" for u in urls if u not in found]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--base", default="https://mokaair.com")
    parser.add_argument("--slug", action="append", default=[], help="Repeatable")
    parser.add_argument("--kind", choices=("howto", "intel", "life"))
    parser.add_argument("--locale", action="append", default=[], help="Repeatable; default zh-TW")
    parser.add_argument("--url-list", type=Path, help="One URL per line")
    parser.add_argument("--from-report", type=Path, help="JSON printed by guides-import")
    parser.add_argument("--content-dir", type=Path, default=DEFAULT_CONTENT_DIR)
    parser.add_argument("--sitemap", action="store_true", help="Also require sitemap membership")
    parser.add_argument("--interval", type=float, default=1.3, help="Seconds between requests")
    args = parser.parse_args()

    base = args.base.rstrip("/")
    locales = args.locale or ["zh-TW"]
    targets: list[tuple[str, str | None, str | None]] = []  # (url, slug, expected title)

    if args.url_list:
        for line in args.url_list.read_text(encoding="utf-8").splitlines():
            url = line.strip()
            if url and not url.startswith("#"):
                slug = url.rstrip("/").rsplit("/", 1)[-1]
                targets.append((url, slug, None))

    pairs: list[tuple[str, str]] = []
    if args.from_report:
        report = json.loads(args.from_report.read_text(encoding="utf-8"))
        pairs.extend(targets_from_report(report, locales[0]))
    for slug in args.slug:
        for locale in locales:
            pairs.append((slug, locale))
    for slug, locale in pairs:
        pack = read_pack(args.content_dir, slug)
        kind = args.kind or (pack or {}).get("kind")
        if kind is None:
            print(f"FAIL {slug}: kind unknown; pass --kind or make the pack readable")
            return 1
        expected = ((pack or {}).get("locales", {}).get(locale) or {}).get("title")
        targets.append((article_url(base, locale, kind, slug), slug, expected))

    if not targets:
        parser.error("nothing to check: pass --slug, --url-list or --from-report")

    fetcher = Fetcher(args.interval)
    failures = 0
    for url, slug, expected in targets:
        problems = check_page(fetcher, url, base, slug, expected)
        if problems:
            failures += 1
            print(f"FAIL {url}: {'; '.join(problems)}")
        else:
            print(f"ok   {url}")
    if args.sitemap:
        for problem in sitemap_membership(fetcher, base, [t[0] for t in targets]):
            failures += 1
            print(f"FAIL {problem}")
    print(f"RESULT {'FAIL' if failures else 'PASS'} ({failures} problems, {len(targets)} pages)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
