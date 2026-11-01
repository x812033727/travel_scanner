// The lead picture of a daily brief whose script cites only the site's own articles
// (ticket 2026-11-01-daily-brief-lead-picture-finds-no).
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { articleCitation, findLeadPicture, leadArticle } from "./lead-picture.mjs";

const ARTICLE = "https://mokaair.com/zh-TW/life/ai-news-gpt6-luna-update-20261029";
const OFFICIAL = "https://deploymentsafety.openai.com/gpt-6-luna-october-28-2026-addendum";
const ld = (data) => `<script type="application/ld+json">${JSON.stringify(data)}</script>`;
const articleHtml = ld({ "@type": "NewsArticle", citation: [{ "@type": "CreativeWork", name: "Addendum", url: OFFICIAL }, { "@type": "CreativeWork", url: "https://example.com/second" }] });

test("an article's first official citation is read from its JSON-LD", () => {
  assert.equal(articleCitation(`<html>${ld({ "@type": "BreadcrumbList" })}${articleHtml}</html>`, ARTICLE), OFFICIAL);
  assert.equal(articleCitation(ld({ "@graph": [{ "@type": "WebPage" }, { "@type": "Article", citation: { url: "https://blog.google/a" } }] }), ARTICLE), "https://blog.google/a", "a single citation inside @graph");
  assert.equal(articleCitation(ld({ citation: [{ url: "https://mokaair.com/zh-TW/life/other" }, { url: "http://insecure.example.com/" }, "https://example.org/b"] }), ARTICLE), "https://example.org/b", "the site's own pages and plain http are skipped");
  assert.equal(articleCitation(`<script type="application/ld+json">{broken</script>${articleHtml}`, ARTICLE), OFFICIAL, "a broken block is skipped");
  assert.equal(articleCitation("<html><a href=\"https://example.com\">x</a></html>", ARTICLE), null);
});

test("the lead article is the first https source on this site", () => {
  assert.equal(leadArticle({ sources: [{ url: "not a url" }, { url: "https://blog.example.com/" }, { title: "主文", url: ARTICLE }] }).url, ARTICLE);
  assert.equal(leadArticle({ sources: [{ url: "https://blog.example.com/" }] }), null);
});

function fetcher(pages) {
  const asked = [];
  const fetchImpl = async (url) => {
    asked.push(String(url));
    const page = pages[url];
    if (!page) return new Response("", { status: 404 });
    return new Response(page.body, { headers: { "content-type": page.type } });
  };
  return { asked, fetchImpl };
}

test("a brief citing only the site's articles takes the picture of the page its lead article cites", async () => {
  const video = { sources: [{ title: "GPT-6 Luna", url: ARTICLE }, { url: "https://mokaair.com/zh-TW/life/second" }] };
  const { asked, fetchImpl } = fetcher({
    [ARTICLE]: { type: "text/html; charset=utf-8", body: articleHtml },
    [OFFICIAL]: { type: "text/html", body: `<meta property="og:image" content="/assets/social.png">` },
    "https://deploymentsafety.openai.com/assets/social.png": { type: "image/png", body: new Uint8Array([137, 80, 78, 71]) },
  });
  const found = await findLeadPicture(fetchImpl, video);
  assert.equal(found.page, OFFICIAL);
  assert.equal(found.image, "https://deploymentsafety.openai.com/assets/social.png");
  assert.deepEqual([...found.bytes], [137, 80, 78, 71]);
  assert.deepEqual(asked, [ARTICLE, OFFICIAL, found.image], "the article, its official page, the picture");
});

test("an official source in the script is used directly, without reading the article", async () => {
  const video = { sources: [{ url: ARTICLE }, { url: OFFICIAL }] };
  const { asked, fetchImpl } = fetcher({
    [OFFICIAL]: { type: "text/html", body: `<meta property="og:image" content="https://cdn.example.com/a.jpg">` },
    "https://cdn.example.com/a.jpg": { type: "image/jpeg", body: new Uint8Array([255, 216]) },
  });
  assert.equal((await findLeadPicture(fetchImpl, video)).page, OFFICIAL);
  assert.deepEqual(asked, [OFFICIAL, "https://cdn.example.com/a.jpg"]);
});

test("an article that cites nothing official says so", async () => {
  const { fetchImpl } = fetcher({ [ARTICLE]: { type: "text/html", body: "<html></html>" } });
  await assert.rejects(findLeadPicture(fetchImpl, { sources: [{ url: ARTICLE }] }), /names no official source, and .* cites none/);
  await assert.rejects(findLeadPicture(fetchImpl, { sources: [] }), /^Error: the script names no official source$/);
});

test("the site's article page still writes its sources as JSON-LD citations", () => {
  // articleCitation reads what the article page renders; if the page stops writing citation,
  // every brief's thumbnail loses its picture again.
  const page = readFileSync(new URL("../../../apps/web/lib/structured-data.ts", import.meta.url), "utf8");
  assert.match(page, /citation:/);
});
