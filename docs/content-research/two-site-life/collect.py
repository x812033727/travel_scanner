"""Collect only public article identities/titles, and cross-check archive pagination.

Run from the repository root with Python 3.13. Never requests article bodies.
"""
import concurrent.futures
import datetime
import html
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SITES = [
    ("frankknow", "https://frankknow.com", "/category/content/", "categories=20&"),
    ("notesstartup", "https://notesstartup.com", "/", ""),
]


def get(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mokaair-title-inventory/1.0"})
            with urllib.request.urlopen(req, timeout=40) as response:
                return response.read().decode("utf-8"), dict(response.headers)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def clean(text):
    return re.sub(r"\s+", " ", re.sub(r"[\x00-\x1f\x7f]", "", html.unescape(re.sub(r"<[^>]+>", "", text)))).strip()


def archive(url):
    body, _ = get(url)
    entries = []
    for heading in re.findall(r'<h[23][^>]*class="[^"]*(?:entry-title|elementor-post__title)[^"]*"[^>]*>([\s\S]*?)</h[23]>', body):
        link = re.search(r'<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)</a>', heading)
        if link:
            entries.append({"url": html.unescape(link[1]), "title": clean(link[2])})
    pages = [int(n) for n in re.findall(r'/page/(\d+)/', body)]
    return {"url": url, "count": len(entries), "entries": entries, "last_page": max(pages, default=1)}


def main():
    checked = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records, verification = [], []
    for site, origin, listing, query in SITES:
        api = origin + "/wp-json/wp/v2/posts?" + query + "per_page=100&_fields=id,title,link"
        body, headers = get(api + "&page=1")
        lower_headers = {key.lower(): value for key, value in headers.items()}
        total, pages = int(lower_headers["x-wp-total"]), int(lower_headers["x-wp-totalpages"])
        posts = json.loads(body)
        for page in range(2, pages + 1):
            posts.extend(json.loads(get(api + f"&page={page}")[0]))
        assert len(posts) == total and len({p["link"] for p in posts}) == total
        first = archive(origin + listing)
        urls = [origin + listing + f"page/{n}/" for n in range(2, first["last_page"] + 1)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            listings = [first, *pool.map(archive, urls)]
        listed = {row["url"] for page in listings for row in page["entries"]}
        indexed = {post["link"] for post in posts}
        missing, extras = sorted(indexed - listed), sorted(listed - indexed)
        verification.append({"site": site, "api": api, "api_total": total, "api_pages": pages,
                             "archive_pages": len(listings), "archive_unique": len(listed),
                             "api_not_in_archive": missing, "archive_not_in_api": extras,
                             "archives": [{k: v for k, v in page.items() if k != "entries"} for page in listings]})
        if extras:
            raise ValueError(f"{site}: archive contains entries absent from public posts: {extras}")
        for post in posts:
            records.append({"key": f"{site}:{post['id']}", "source": site, "source_id": post["id"],
                            "original_title": post["title"]["rendered"], "title": clean(post["title"]["rendered"]),
                            "url": post["link"], "archive_listed": post["link"] in listed, "checked_on": checked[:10]})
        print(f"{site}: {total} public titles; {len(listings)} archive pages, {len(listed)} listed; {len(missing)} public API-only entries retained", flush=True)
    data = {"checked_at": checked, "collection_policy": "Titles and links only; no article bodies or source images requested.",
            "count": len(records), "verification": verification, "articles": records}
    OUT.joinpath("titles.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# 兩站完整文章標題清單", "", f"查閱日期：{checked[:10]}。共 {len(records)} 筆；已逐頁核對公開文章索引。", "",
             "僅使用標題作為選題靈感。原始標題（含 HTML entities）保存在 titles.json；此處為清理後顯示文字。", "",
             "分頁差異也保存在 JSON 的 verification。諾特斯有公開 API 已列出、首頁分頁沒有列出的文章，仍完整保留，沒有用首頁數量取代全站公開篇數。", ""]
    for site, _, _, _ in SITES:
        rows = [row for row in records if row["source"] == site]
        lines.extend([f"## {site}（{len(rows)} 筆）", "", "| ID | 標題 |", "| --- | --- |"])
        lines.extend(f"| {row['source_id']} | [{row['title'].replace('|', '&#124;')}]({row['url']}) |" for row in rows)
        lines.append("")
    OUT.joinpath("titles.md").write_text("\n".join(lines), encoding="utf-8")
    existing = []
    for path in sorted(ROOT.joinpath("apps/api/app/guides/content").glob("*.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        existing.append({"slug": pack["slug"], "kind": pack["kind"], "title": pack["locales"].get("zh-TW", {}).get("title", "")})
    planned = []
    for line in ROOT.joinpath("docs/life-ai-series.md").read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) > 4 and re.fullmatch(r"\d+", cells[1]) and re.fullmatch(r"`[a-z0-9-]+`", cells[2]):
            planned.append({"slug": cells[2].strip("`"), "title": cells[3]})
    tasks = []
    for path in ROOT.joinpath("tasks/open").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        matches = re.findall(r"apps/api/app/guides/content/([a-z0-9-]+)\.json", text)
        if matches:
            tasks.append({"task": path.stem, "article_slugs": sorted(set(matches))})
    OUT.joinpath("existing-snapshot.json").write_text(json.dumps({"checked_at": checked, "existing": existing, "planned_ai": planned, "tasks": tasks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Baseline: {len(existing)} existing packs; {len(planned)} planned AI articles", flush=True)


if __name__ == "__main__":
    main()
