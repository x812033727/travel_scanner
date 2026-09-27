import assert from "node:assert/strict";
import test from "node:test";

import { checkLinks, descriptionUrls, HOST_GAP_MS, linkChecker, linksDetail, TIMEOUT_MS, USER_AGENT } from "./links.mjs";

test("the description's URLs come out once each, without the punctuation around them", () => {
  const zh = "🔗 完整文章：https://mokaair.com/zh-TW/guides/ai/x?utm_source=youtube&utm_campaign=x\n\n📚 參考資料\n來源一：https://openai.com/a。\n來源二（https://help.openai.com/b）";
  const en = "🔗 Full article: https://mokaair.com/en/guides/ai/x?utm_source=youtube&utm_campaign=x\n\nSources\nOne: https://openai.com/a.\nhttp://old.example.com/page,";
  assert.deepEqual(descriptionUrls([zh, en]), [
    "https://mokaair.com/zh-TW/guides/ai/x?utm_source=youtube&utm_campaign=x",
    "https://openai.com/a",
    "https://help.openai.com/b",
    "https://mokaair.com/en/guides/ai/x?utm_source=youtube&utm_campaign=x",
    "http://old.example.com/page",
  ]);
  assert.deepEqual(descriptionUrls(["no links here", null]), []);
});

test("links are fetched with GET, redirects followed, the editorial agent, a second apart per host", async () => {
  let clock = 1_000_000;
  const waits = [];
  const seen = [];
  const check = linkChecker({
    now: () => clock,
    sleep: async (ms) => {
      waits.push(ms);
      clock += ms;
    },
    fetchImpl: async (url, init) => {
      seen.push({ url, method: init.method, redirect: init.redirect, agent: init.headers["User-Agent"], signal: init.signal });
      if (url.endsWith("/gone")) return new Response("missing", { status: 404 });
      // Response.url is read-only, so the redirected answer is a stand-in with the fields the checker reads.
      if (url.endsWith("/moved")) return { ok: true, status: 200, url: "https://openai.com/final", body: null };
      return new Response("<p>ok</p>", { status: 200 });
    },
  });
  const results = await checkLinks(["https://openai.com/a", "https://openai.com/gone", "https://help.openai.com/c", "https://openai.com/moved", "not a url"], check);
  assert.deepEqual(results.map((result) => [result.ok, result.status]), [[true, 200], [false, 404], [true, 200], [true, 200], [false, 0]]);
  assert.equal(results[1].error, "HTTP 404");
  assert.equal(results[3].final_url, "https://openai.com/final");
  assert.equal(results[4].error, "not a URL");
  assert.equal(seen.length, 4, "a string that is not a URL is never requested");
  assert.ok(seen.every((request) => request.method === "GET" && request.redirect === "follow" && request.signal instanceof AbortSignal));
  assert.ok(seen.every((request) => request.agent === "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"));
  assert.equal(USER_AGENT, "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)");
  assert.deepEqual(waits, [HOST_GAP_MS, HOST_GAP_MS], "the second and third requests to openai.com waited; help.openai.com is another host");
  assert.equal(HOST_GAP_MS, 1000);
  assert.equal(linksDetail(results), "2 of 5 links do not open: https://openai.com/gone (HTTP 404), not a url (not a URL)");
  assert.equal(linksDetail(results.filter((result) => result.ok)), "3 links open");
  assert.equal(linksDetail([]), "the description has no links");
});

test("a link that does not answer in time is listed as timed out; a refused connection with its reason", async () => {
  const check = linkChecker({
    timeoutMs: 20,
    gapMs: 0,
    fetchImpl: (url, init) =>
      url.endsWith("/slow")
        ? new Promise((_, reject) => init.signal.addEventListener("abort", () => reject(Object.assign(new Error("aborted"), { name: "AbortError" }))))
        : Promise.reject(new TypeError("fetch failed")),
  });
  const [slow, refused] = await checkLinks(["https://example.com/slow", "https://example.com/down"], check);
  assert.deepEqual([slow.ok, slow.error], [false, "timed out after 0 s"]);
  assert.deepEqual([refused.ok, refused.error], [false, "fetch failed"]);
  assert.equal(TIMEOUT_MS, 15_000);
});
