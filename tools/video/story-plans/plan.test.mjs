import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";

import { canonical, CHAPTER_KEYS, claimSupported, compile, compiledCurrent, DEFAULT_PLAN, hostOf, loadPlan, order, planProblems, reviewProblems, scheduleMarkdown, scheduleProblems, serialize, seriesProblems, siteGuides, storyHash, storyProblems, STORY_KEYS } from "./plan.mjs";
import { fetchProblems, fetchSources, main, reviewerOnlyFacts, USER_AGENT } from "./validate.mjs";

const point = (text) => text.repeat(Math.ceil(80 / [...text].length));

/** A sound story; each test breaks one thing. */
function story(overrides = {}) {
  return {
    id: "A01",
    slug: "story-example",
    category: "everyday",
    region: "global",
    subject: "範例",
    title: "一個範例的標題",
    logline: "一句話說明這支影片。",
    question: "為什麼會這樣？",
    chapters: CHAPTER_KEYS.map((key) => ({ key, point: point(`這一段講 ${key} 的具體事實。`) })),
    takeaway: "留給觀眾的一句觀察。",
    must_verify: [
      { claim: "第一個事實", sources: [0], core: true },
      { claim: "第二個事實", sources: [1, 2] },
      { claim: "第三個事實", sources: [2], attributed: true },
      { claim: "第四個事實", sources: [0] },
    ],
    sources: [
      { url: "https://example.com/history", publisher: "Example Corp", kind: "official", supports: "公司沿革", checked: "2026-09-28" },
      { url: "https://news.example.org/a", publisher: "Example News", kind: "news", supports: "報導", checked: "2026-09-28" },
      { url: "https://en.wikipedia.org/wiki/Example", publisher: "Wikipedia", kind: "reference", supports: "概述", checked: "2026-09-28" },
    ],
    names: ["Example Corp", "John Example"],
    cast: [{ id: "founder", role: "創辦人", appearance: "a middle-aged man in a grey 1950s suit, short hair, round glasses" }],
    image_notes: "不畫商標與文字。",
    sensitivity: "none",
    related_guide: null,
    thumbnail: { headline: "範例標題", idea: "一個箱子" },
    ...overrides,
  };
}

const schedule = (pairs) => ({ days: pairs.map(([noon, evening], index) => ({ day: index + 1, slots: { "12:00": noon, "20:00": evening } })) });
const series = (overrides = {}) => ({
  slug: "brand-stories",
  title: "品牌故事",
  kind: "story",
  target_minutes: 13,
  episodes_per_day: 2,
  hands_off: true,
  visual_tier: "stills",
  image_model: "gemini-3.1-flash-image",
  look: { style: "flat cartoon", negative: "text, logo" },
  ...overrides,
});

test("a sound story has no problems", () => {
  assert.deepEqual(storyProblems(story()), []);
});

test("the id decides the category and, for the Asian brands, the region", () => {
  assert.match(storyProblems(story({ category: "tech" })).join("\n"), /category "tech" does not fit id A01/);
  assert.match(storyProblems(story({ id: "B02", region: "kr", category: "asia-brand" }), "B02").join("\n"), /region "kr" does not fit id B02 \(jp\)/);
  assert.deepEqual(storyProblems(story({ id: "K03", region: "kr", category: "asia-brand" }), "K03"), []);
  assert.match(storyProblems(story({ id: "A02" }), "A01").join("\n"), /does not match the file name A01\.json/);
});

test("the six chapters come in order and say something", () => {
  const swapped = story();
  [swapped.chapters[0], swapped.chapters[1]] = [swapped.chapters[1], swapped.chapters[0]];
  assert.match(storyProblems(swapped).join("\n"), /chapters\[0\]\.key is "origin", expected "hook"/);
  assert.match(storyProblems(story({ chapters: story().chapters.slice(0, 5) })).join("\n"), /chapters must be the 6 parts/);
  const thin = story();
  thin.chapters[3].point = "介紹背景。";
  assert.match(storyProblems(thin).join("\n"), /chapters\[3\] \(engine\) is 5 characters/);
});

test("sources are https, distinct, described and dated", () => {
  const bad = story();
  bad.sources[0].url = "http://example.com/history";
  bad.sources[1].url = bad.sources[2].url;
  bad.sources[2].checked = "yesterday";
  const problems = storyProblems(bad).join("\n");
  assert.match(problems, /sources\[0\]\.url must be an https URL/);
  assert.match(problems, /sources\[2\]\.checked must be the date/);
  assert.match(storyProblems(story({ sources: story().sources.slice(0, 2), must_verify: story().must_verify.map((claim) => ({ ...claim, sources: [0] })) })).join("\n"), /sources has 2 entries, at least 3/);
  const repeated = story();
  repeated.sources[2] = { ...repeated.sources[1] };
  assert.match(storyProblems(repeated).join("\n"), /sources\[2\]\.url repeats an earlier source/);
});

test("a claim needs a primary source, two independent ones, or to be told as somebody's account", () => {
  const { sources } = story();
  assert.equal(claimSupported({ sources: [0] }, sources), true);
  assert.equal(claimSupported({ sources: [1] }, sources), false);
  assert.equal(claimSupported({ sources: [1, 2] }, sources), true);
  assert.equal(claimSupported({ sources: [1], attributed: true }, sources), true);
  assert.equal(claimSupported({ sources: [] }, sources), false);
  // Two pages of one publisher are one voice, and so are two publishers' names on one host.
  const sameVoice = [...sources, { url: "https://news.example.org/b", publisher: "Example News", kind: "news", supports: "x", checked: "2026-09-28" }];
  assert.equal(claimSupported({ sources: [1, 3] }, sameVoice), false);
  const sameHost = [...sources, { url: "https://www.news.example.org/c", publisher: "Another Name", kind: "news", supports: "x", checked: "2026-09-28" }];
  assert.equal(claimSupported({ sources: [1, 3] }, sameHost), false);
  // Two language editions of one encyclopedia are one voice, whatever the publisher field says.
  const editions = [...sources, { url: "https://ja.wikipedia.org/wiki/Example", publisher: "維基百科（日文）", kind: "reference", supports: "x", checked: "2026-09-28" }];
  assert.equal(claimSupported({ sources: [2, 3] }, editions), false);
  assert.equal(claimSupported({ sources: [1, 3] }, editions), true, "an encyclopedia and a newspaper are two voices");
  // A page read through the Wayback Machine is its publisher's page: two publishers kept there
  // are two voices, and the copy of an article beside the article itself is one.
  const kept = (url, publisher) => ({ url: `https://web.archive.org/web/20251226124930/${url}`, publisher, kind: "news", supports: "x", checked: "2026-09-28" });
  const archived = [kept("https://www.daily.example.com/a", "Daily Example"), kept("http://weekly.example.net/b", "Weekly Example"), kept("https://news.example.org/a", "Example News（存檔）"), sources[1]];
  assert.equal(hostOf(archived[0].url), "daily.example.com");
  assert.equal(claimSupported({ sources: [0, 1] }, archived), true);
  assert.equal(claimSupported({ sources: [2, 3] }, archived), false);
  assert.match(storyProblems(story({ sources: [...sources, kept("https://news.example.org/a/", "Example News（存檔）")] })).join("\n"), /sources\[3\]\.url repeats an earlier source/);

  const weak = story();
  weak.must_verify[1] = { claim: "只有一個新聞來源", sources: [1] };
  assert.match(storyProblems(weak).join("\n"), /must_verify\[1\] rests on one secondary source/);
  const noCore = story();
  for (const claim of noCore.must_verify) delete claim.core;
  assert.match(storyProblems(noCore).join("\n"), /no must_verify claim is marked core/);
  const outOfRange = story();
  outOfRange.must_verify[0].sources = [7];
  assert.match(storyProblems(outOfRange).join("\n"), /must_verify\[0\]\.sources must list indexes into sources/);
});

test("encyclopedia mirrors cannot independently corroborate the original or each other", () => {
  const encyclopedia = { url: "https://en.wikipedia.org/wiki/Example", publisher: "Wikipedia", kind: "reference" };
  const newspaper = { url: "https://news.example.org/a", publisher: "Independent News", kind: "news" };
  const mirrors = [
    "https://www.wikiwand.com/en/articles/Example",
    "https://www.wikimili.com/en/Example",
    "https://commons.wikimedia.org/wiki/Example",
    "https://web.archive.org/web/20251226124930/http://m.wikiwand.com/en/Example",
  ].map((url, index) => ({ url, publisher: `Mirror ${index}`, kind: "reference" }));
  for (const mirror of mirrors) {
    assert.equal(hostOf(mirror.url), "wikipedia.org");
    assert.equal(claimSupported({ sources: [0, 1] }, [encyclopedia, mirror]), false);
    assert.equal(claimSupported({ sources: [0, 1] }, [newspaper, mirror]), true);
  }
  assert.equal(claimSupported({ sources: [0, 1] }, mirrors), false);
  assert.equal(hostOf("https://wikiwand.com.example.org/a"), "wikiwand.com.example.org", "only the actual domain and its subdomains belong to the family");
});

test("a figure is generic: English, and never named after a real person or brand", () => {
  const named = story();
  named.cast[0].appearance = "John Example in a grey suit";
  assert.match(storyProblems(named).join("\n"), /cast\[0\]\.appearance names "John Example"/);
  const chinese = story();
  chinese.cast[0].appearance = "穿灰色西裝的男人";
  assert.match(storyProblems(chinese).join("\n"), /cast\[0\]\.appearance must be English/);
  assert.match(storyProblems(story({ cast: [1, 2, 3, 4].map((n) => ({ id: `figure-${n}`, role: "人物", appearance: "a person in a coat" })) })).join("\n"), /cast has 4 figures, at most 3/);
  assert.deepEqual(storyProblems(story({ cast: [] })), []);
  assert.match(storyProblems(story({ cast: [{ id: "narrator", role: "旁白", appearance: "a person" }] })).join("\n"), /not "narrator"/);
});

test("the rest of a story's fields", () => {
  assert.match(storyProblems(story({ extra: true })).join("\n"), /unknown field "extra"/);
  assert.match(storyProblems(story({ slug: "rolling-suitcase" })).join("\n"), /slug "rolling-suitcase" must be story-/);
  assert.match(storyProblems(story({ title: "標題 <b>" })).join("\n"), /angle bracket/);
  assert.match(storyProblems(story({ thumbnail: { headline: "這個縮圖標題實在是太長了超過十二個字", idea: "x" } })).join("\n"), /thumbnail\.headline is \d+ characters, at most 12/);
  assert.match(storyProblems(story({ sensitivity: "high" })).join("\n"), /sensitivity must be one of none, care/);
  assert.match(storyProblems(story({ related_guide: "Not A Slug" })).join("\n"), /related_guide must be/);
  assert.deepEqual(storyProblems(story({ related_guide: "japan-suica-guide" })), []);
  assert.match(storyProblems(story({ names: [] })).join("\n"), /names must list/);
  assert.deepEqual(storyProblems([]), ["the file is not a JSON object"]);
});

test("canonical keeps a story's fields in the order the files are written in", () => {
  const shuffled = Object.fromEntries(Object.entries(story()).reverse());
  assert.deepEqual(Object.keys(canonical(shuffled)), STORY_KEYS);
});

test("the schedule places every story once, two a day", () => {
  assert.deepEqual(scheduleProblems(schedule([["A01", "B01"], ["A02", "C01"]])), []);
  assert.match(scheduleProblems(schedule([["A01", "B01"], ["A01", "C01"]])).join("\n"), /A01 is scheduled on day 1 and day 2/);
  assert.match(scheduleProblems({ days: [{ day: 1, slots: { "12:00": "A01" } }] }).join("\n"), /day 1 has no story at 20:00/);
  assert.match(scheduleProblems({ days: [{ day: 2, slots: { "12:00": "A01", "20:00": "B01" } }] }).join("\n"), /days\[0\]\.day is 2, expected 1/);
  const placed = order(schedule([["A01", "B01"], ["A02", "C01"]]));
  assert.deepEqual(placed.get("A01"), { number: 1, day: 1, slot: "12:00" });
  assert.deepEqual(placed.get("C01"), { number: 4, day: 2, slot: "20:00" });
});

test("the series row is a hands-off stills story series", () => {
  assert.deepEqual(seriesProblems(series()), []);
  const problems = seriesProblems(series({ kind: "series", visual_tier: "clips", hands_off: false, target_minutes: 3, episodes_per_day: 0 })).join("\n");
  for (const expected of [/kind must be "story"/, /visual_tier must be "stills"/, /hands_off must be true/, /target_minutes must be 12 to 15/, /episodes_per_day must be 1 to 12/]) assert.match(problems, expected);
});

test("compile lists the stories in production order with their slots", () => {
  const plan = {
    series: series(),
    schedule: schedule([["A01", "B01"]]),
    stories: [
      { id: "B01", story: story({ id: "B01", slug: "story-b", title: "B", category: "asia-brand", region: "jp" }) },
      { id: "A01", story: story() },
    ],
  };
  const compiled = compile(plan);
  assert.deepEqual(compiled.stories.map((each) => [each.number, each.id, each.publish]), [[1, "A01", { day: 1, slot: "12:00" }], [2, "B01", { day: 1, slot: "20:00" }]]);
  assert.equal(compiled.series.slug, "brand-stories");
  assert.deepEqual(planProblems(plan, { expected: null }), []);
  // What the fact checker left for the writer travels with the story; without a review it is empty.
  assert.deepEqual(compiled.stories.map((each) => each.caveats), ["", ""]);
  plan.stories[1].review = review(story(), { notes: " 專利被同業繞過的說法查不到出處，不要提。 " });
  assert.deepEqual(compile(plan).stories.map((each) => each.caveats), ["專利被同業繞過的說法查不到出處，不要提。", ""]);
  assert.deepEqual(Object.keys(compile(plan).stories[0]).slice(-3), ["thumbnail", "caveats", "publish"]);
  assert.match(planProblems(plan).join("\n"), /1 stories are everyday, expected 40/);
});

test("the schedule table names each day's two stories and counts the categories", () => {
  const plan = {
    series: series(),
    schedule: schedule([["A01", "B01"], ["A02", "K01"]]),
    stories: [
      { id: "A01", story: story({ title: "有 | 直線的標題" }) },
      { id: "B01", story: story({ id: "B01", slug: "story-b", title: "日本的故事", category: "asia-brand", region: "jp" }) },
      { id: "K01", story: story({ id: "K01", slug: "story-k", title: "韓國的故事", category: "asia-brand", region: "kr" }) },
    ],
  };
  const table = scheduleMarkdown(plan);
  assert.match(table, /\| 1 \| A01 有 ｜ 直線的標題 \| B01 日本的故事 \|/);
  assert.match(table, /\| 2 \| A02（還沒寫） \| K01 韓國的故事 \|/);
  assert.match(table, /\| 日韓台旅途品牌 \| 2（日本 1、韓國 1） \|/);
  assert.match(table, /\| 日常用品與隱形標準 \| 1 \|/);
  assert.doesNotMatch(table, /跟核准時不一樣的標題/);
  // What the owner approved beside what the fact check left.
  const seeds = [
    { id: "B01", subject: "範例", title: "日本的故事" },
    { id: "K01", subject: "範例", title: "核准時的標題" },
    { id: "A02", subject: "還沒寫", title: "還沒寫的標題" },
  ];
  const compared = scheduleMarkdown({ ...plan, seeds });
  assert.match(compared, /## 跟核准時不一樣的標題/);
  assert.match(compared, /\| K01 \| 核准時的標題 \| 韓國的故事 \|/);
  assert.doesNotMatch(compared, /\| B01 \| 日本的故事 \| 日本的故事/);
  assert.doesNotMatch(compared, /還沒寫的標題/);
  // The facts only the reviewer could read the evidence for are listed, with the title's marked.
  assert.doesNotMatch(compared, /只有查核的人讀得到證據的事實/);
  plan.stories[2].review = review(plan.stories[2].story, { reviewer_only: [0, 3] });
  const listed = scheduleMarkdown(plan);
  assert.match(listed, /## 只有查核的人讀得到證據的事實/);
  assert.match(listed, /\| K01 \| 第一個事實 \| 是 \|\n\| K01 \| 第四個事實 \|  \|/);
});

test("a plan's stories have distinct slugs and titles, and each has a slot", () => {
  const plan = {
    series: series(),
    schedule: schedule([["A01", "B01"]]),
    stories: [
      { id: "A01", story: story() },
      { id: "A02", story: story({ id: "A02" }) },
      { id: "A03", error: "Unexpected token" },
    ],
  };
  const problems = planProblems(plan, { expected: null }).join("\n");
  assert.match(problems, /A02: slug "story-example" is also A01's/);
  assert.match(problems, /A02: title "一個範例的標題" is also A01's/);
  assert.match(problems, /A02: not in schedule\.json/);
  assert.match(problems, /A03: not valid JSON/);
});

test("a story's related article is one the site has", () => {
  const plan = {
    series: series(),
    schedule: schedule([["A01", "B01"]]),
    stories: [
      { id: "A01", story: story({ related_guide: "overseas-atm-withdrawal" }) },
      { id: "B01", story: story({ id: "B01", slug: "story-b", title: "B", category: "asia-brand", region: "jp", related_guide: "overseas-atm-withdrawl" }) },
    ],
    guides: new Set(["overseas-atm-withdrawal"]),
  };
  assert.deepEqual(planProblems(plan, { expected: null }), ['B01: related_guide "overseas-atm-withdrawl" is not an article of the site (apps/api/app/guides/content/overseas-atm-withdrawl.json)']);
  // Where the articles are not there to read, the slug's shape is all that is checked.
  assert.deepEqual(planProblems({ ...plan, guides: null }, { expected: null }), []);
  // The repository's own articles are read from the content packs.
  assert.ok(siteGuides().has("overseas-atm-withdrawal"));
  assert.equal(siteGuides(path.join(os.tmpdir(), "no-such-directory-of-guides")), null);
});

const review = (read, overrides = {}) => ({ id: read.id, reviewed: "2026-09-28", reviewer: "a second reader", story_sha256: storyHash(read), verdict: "pass", sources_opened: 3, changes: [], notes: "", ...overrides });

test("a review is bound to the text it read", () => {
  const read = story();
  assert.deepEqual(reviewProblems(review(read), read), []);
  // Reformatting the file is not an edit; changing a word is.
  assert.equal(storyHash(Object.fromEntries(Object.entries(read).reverse())), storyHash(read));
  assert.match(reviewProblems(review(read), story({ title: "改過的標題" })).join("\n"), /the story changed after this review/);
  assert.match(reviewProblems(review(read, { verdict: "fixed" }), read).join("\n"), /verdict "fixed" needs the changes it made/);
  assert.match(reviewProblems(review(read, { changes: ["改了年份"] }), read).join("\n"), /verdict "pass" has changes/);
  assert.deepEqual(reviewProblems(review(read, { verdict: "fixed", changes: ["改了年份"] }), read), []);
  assert.match(reviewProblems(review(read, { sources_opened: 1 }), read).join("\n"), /the reviewer opens at least 3 sources/);
  assert.match(reviewProblems(review(read, { verdict: "replace" }), read).join("\n"), /verdict must be one of pass, fixed/);
  assert.match(reviewProblems(review(read, { story_sha256: "abc" }), read).join("\n"), /story_sha256 must be the story's hash/);
  assert.match(reviewProblems(review(read, { reviewer: "" }), read).join("\n"), /reviewer is missing/);
  assert.match(reviewProblems(review(read, { notes: "字".repeat(801) }), read).join("\n"), /notes is 801 characters, at most 800/);
  assert.match(reviewProblems(review(read), read, "A02").join("\n"), /does not match the file name A02\.json/);
});

test("a finished plan has a current review for every story; a plan being written need not", () => {
  const read = story();
  const plan = { series: series(), schedule: schedule([["A01", "B01"]]), stories: [{ id: "A01", story: read }], orphans: [] };
  assert.deepEqual(planProblems(plan, { expected: null }), []);
  assert.match(planProblems(plan).join("\n"), /A01: no review yet/);
  plan.stories[0].review = review(read);
  assert.doesNotMatch(planProblems(plan).join("\n"), /review/);
  plan.stories[0].review = review(story({ takeaway: "另一句觀察。" }));
  assert.match(planProblems(plan, { expected: null }).join("\n"), /A01: review: the story changed after this review/);
  plan.orphans = ["C09"];
  assert.match(planProblems(plan, { expected: null }).join("\n"), /C09: reviews\/C09\.json has no story/);
});

test("validate --write compiles a plan directory and the check then passes", async () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "story-plan-"));
  try {
    mkdirSync(path.join(dir, "stories"));
    writeFileSync(path.join(dir, "series.json"), JSON.stringify(series()));
    writeFileSync(path.join(dir, "schedule.json"), JSON.stringify(schedule([["A01", "B01"]])));
    writeFileSync(path.join(dir, "stories", "A01.json"), JSON.stringify(story()));
    writeFileSync(path.join(dir, "stories", "B01.json"), JSON.stringify(story({ id: "B01", slug: "story-b", title: "B", category: "asia-brand", region: "jp" })));
    const out = { text: "", write(chunk) { this.text += chunk; } };
    assert.equal(compiledCurrent(loadPlan(dir)), false);
    assert.equal(await main(["--plan", dir, "--partial", "--write"], { stdout: out, stderr: out }), 0);
    assert.equal(compiledCurrent(loadPlan(dir)), true);
    assert.equal(readFileSync(path.join(dir, "stories.json"), "utf8"), serialize(compile(loadPlan(dir))));
    assert.match(out.text, /2 stories \(everyday 1, asia-brand 1\); 1 days scheduled\n0 problems/);
    // The full check holds a plan to the hundred stories.
    assert.equal(await main(["--plan", dir], { stdout: out, stderr: out }), 1);
    // --hash prints what a review records; a review of that text is then current.
    const hashed = { text: "", write(chunk) { this.text += chunk; } };
    assert.equal(await main(["--plan", dir, "--hash", "A01"], { stdout: hashed, stderr: hashed }), 0);
    assert.equal(hashed.text.trim(), storyHash(story()));
    assert.equal(await main(["--plan", dir, "--hash", "Z99"], { stdout: hashed, stderr: hashed }), 1);
    mkdirSync(path.join(dir, "reviews"));
    writeFileSync(path.join(dir, "reviews", "A01.json"), JSON.stringify(review(story({ title: "舊的標題" }))));
    const only = { text: "", write(chunk) { this.text += chunk; } };
    assert.equal(await main(["--plan", dir, "--only", "B01"], { stdout: only, stderr: only }), 0);
    assert.equal(await main(["--plan", dir, "--only", "A01"], { stdout: only, stderr: only }), 1);
    assert.match(only.text, /PROBLEM A01: review: the story changed after this review/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

const page = (body, { status = 200, type = "text/html; charset=utf-8" } = {}) => new Response(body, { status, headers: { "content-type": type } });
const prose = `<html><head><title>Example</title></head><body><p>${"A sentence the page says. ".repeat(40)}</p></body></html>`;
const noWait = async () => {};

test("fetchSources reads every source with the worker's reader, under the worker's name", async () => {
  const asked = [];
  const fetchImpl = async (url, options) => {
    asked.push([new URL(url).hostname, options.headers["User-Agent"]]);
    if (url.includes("wikipedia")) throw new Error("socket hang up");
    return url.includes("news") ? page("no", { status: 403 }) : page(prose);
  };
  const lines = [];
  const results = await fetchSources({ stories: [{ id: "A01", story: story() }] }, { fetchImpl, sleep: noWait, log: (line) => lines.push(line) });
  assert.deepEqual(
    results.map((each) => [each.id, each.index, each.status, each.readable, each.error]),
    [
      ["A01", 0, 200, true, undefined],
      ["A01", 1, 403, false, "HTTP 403"],
      ["A01", 2, 0, false, "socket hang up"],
    ],
  );
  // A page that could not be reached is asked for once more, and then the way the finished
  // video's link check asks; one that answered is asked for once.
  assert.deepEqual(asked.map(([host]) => host).sort(), ["en.wikipedia.org", "en.wikipedia.org", "en.wikipedia.org", "example.com", "news.example.org"]);
  assert.ok(asked.every(([, agent]) => agent === USER_AGENT));
  assert.doesNotMatch(USER_AGENT, /gmail|@(?!mokaair\.com)/);
  assert.ok(lines.includes("A01 200 text https://example.com/history"));
  assert.ok(lines.includes("A01 0 no text (socket hang up) again https://en.wikipedia.org/wiki/Example"));
});

test("a report too large to arrive in the reader's time is there, and unreadable", async () => {
  // The reader waits for the whole page and gives up; the link check waits for the status only.
  const asksForThePage = (options) => !String(options.headers.Accept).includes("application/pdf");
  const fetchImpl = async (url, options) => {
    if (!url.endsWith("/big-report.pdf")) return page(prose);
    if (asksForThePage(options)) throw Object.assign(new Error("This operation was aborted"), { name: "AbortError" });
    return page("%PDF-1.7", { type: "application/pdf" });
  };
  const source = (url, publisher, kind = "news") => ({ url, publisher, kind, supports: "報告", checked: "2026-09-28" });
  const read = story({
    sources: [source("https://example.com/big-report.pdf", "Example Institute", "official"), source("https://news.example.org/a", "Example News"), source("https://en.wikipedia.org/wiki/Example", "Wikipedia", "reference")],
    must_verify: [
      { claim: "只寫在大報告裡", sources: [0], core: true },
      { claim: "大報告與報導都有", sources: [0, 1] },
      { claim: "兩家都有", sources: [1, 2] },
      { claim: "百科的說法", sources: [2], attributed: true },
    ],
  });
  assert.deepEqual(storyProblems(read), []);
  const plan = { stories: [{ id: "A01", story: read }] };
  const lines = [];
  const results = await fetchSources(plan, { fetchImpl, sleep: noWait, log: (line) => lines.push(line) });
  assert.deepEqual(results.map((each) => [each.status, each.readable, each.error]), [
    [200, false, "the link opens, the reader gave up: timed out"],
    [200, true, undefined],
    [200, true, undefined],
  ]);
  assert.ok(lines.includes("A01 200 no text (the link opens, the reader gave up: timed out) https://example.com/big-report.pdf"));
  // So it is no dead link: the one fact that rests on it alone is the reviewer's to vouch for.
  assert.deepEqual(fetchProblems(plan, results).map((problem) => problem.split(" cites ")[0]), ["A01: must_verify[0]"]);
  plan.stories[0].review = review(read, { reviewer_only: [0] });
  assert.deepEqual(fetchProblems(plan, results), []);
});

test("a page that answers without text is there, and no use to the worker's fact check", async () => {
  const source = (url, publisher, kind = "news") => ({ url, publisher, kind, supports: "報導", checked: "2026-09-28" });
  const read = story({
    sources: [source("https://example.com/report.pdf", "Example Corp", "official"), source("https://app.example.net/page", "Example App"), source("https://news.example.org/a", "Example News"), source("https://gone.example.org/b", "Gone News")],
    must_verify: [
      { claim: "只有 PDF", sources: [0], core: true },
      { claim: "PDF 加上讀得到的報導", sources: [0, 2] },
      { claim: "兩頁都讀不到", sources: [0, 1] },
      { claim: "一頁讀得到，一頁不見了", sources: [2, 3] },
    ],
  });
  assert.deepEqual(storyProblems(read), []);
  const fetchImpl = async (url) => {
    if (url.endsWith(".pdf")) return page("%PDF-1.7", { type: "application/pdf" });
    if (url.includes("app.example.net")) return page('<html><body><div id="root"></div><script>render()</script></body></html>');
    if (url.includes("gone")) return page("gone", { status: 404 });
    return page(prose);
  };
  const plan = { stories: [{ id: "A01", story: read }] };
  const results = await fetchSources(plan, { fetchImpl, sleep: noWait });
  assert.deepEqual(results.map((each) => [each.status, each.readable]), [[200, false], [200, false], [200, true], [404, false]]);
  assert.match(results[0].error, /not a text page \(application\/pdf\)/);
  assert.equal(results[1].error, "only 0 characters of text");
  const hint = "cite one it can read as well, or list the fact in the review's reviewer_only when there is none";
  assert.deepEqual(fetchProblems(plan, results), [
    "A01: sources[3] https://gone.example.org/b answered 404",
    `A01: must_verify[0] cites only pages the worker cannot read (sources[0]: not a text page (application/pdf)): ${hint}`,
    `A01: must_verify[2] cites only pages the worker cannot read (sources[0]: not a text page (application/pdf); sources[1]: only 0 characters of text): ${hint}`,
  ]);

  // The reviewer looked and found no page the worker can read: the review says so, the check
  // accepts it, and the compiled story tells the worker which facts to take on the plan's word.
  plan.stories[0].review = review(read, { reviewer_only: [0, 2] });
  assert.deepEqual(reviewProblems(plan.stories[0].review, read), []);
  assert.deepEqual(fetchProblems(plan, results), ["A01: sources[3] https://gone.example.org/b answered 404"]);
  assert.deepEqual(reviewerOnlyFacts(plan), [
    { id: "A01", index: 0, core: true, claim: "只有 PDF" },
    { id: "A01", index: 2, core: false, claim: "兩頁都讀不到" },
  ]);
  const compiled = compile({ series: series(), schedule: schedule([["A01", "B01"]]), stories: plan.stories });
  assert.deepEqual(compiled.stories[0].must_verify.map((claim) => claim.reviewer_only === true), [true, false, true, false]);
  assert.equal(read.must_verify[0].reviewer_only, undefined, "compile leaves the story itself alone");

  // The list is held to what the reader gets: a fact with a readable page comes off it.
  plan.stories[0].review = review(read, { reviewer_only: [1] });
  assert.match(fetchProblems(plan, results).join("\n"), /A01: must_verify\[1\] is in the review's reviewer_only, but the worker can read sources\[2\]: take it off the list/);
  for (const bad of [[4], [0, 0], [-1], ["0"], "0"]) {
    assert.match(reviewProblems(review(read, { reviewer_only: bad }), read).join("\n"), /reviewer_only must list, once each, the indexes of the must_verify facts/);
  }
});

test("validate --fetch reports what it read and keeps it when asked", async () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "story-plan-"));
  try {
    mkdirSync(path.join(dir, "stories"));
    writeFileSync(path.join(dir, "series.json"), JSON.stringify(series()));
    writeFileSync(path.join(dir, "schedule.json"), JSON.stringify(schedule([["A01", "B01"]])));
    writeFileSync(path.join(dir, "stories", "A01.json"), JSON.stringify(story()));
    writeFileSync(path.join(dir, "stories", "B01.json"), JSON.stringify(story({ id: "B01", slug: "story-b", title: "B", category: "asia-brand", region: "jp" })));
    const report = path.join(dir, "read.json");
    const out = { text: "", write(chunk) { this.text += chunk; } };
    const fetchImpl = async (url) => (url.includes("news") ? page("gone", { status: 410 }) : page(prose));
    assert.equal(await main(["--plan", dir, "--only", "B01", "--fetch", "--report", report], { stdout: out, stderr: out, fetchImpl }), 1);
    assert.match(out.text, /3 sources read: 2 give the worker text, 0 answer without text, 1 do not answer/);
    assert.match(out.text, /PROBLEM B01: sources\[1\] https:\/\/news\.example\.org\/a answered 410\n1 problems/);
    assert.deepEqual(JSON.parse(readFileSync(report, "utf8")).map((each) => [each.id, each.status]), [["B01", 200], ["B01", 410], ["B01", 200]]);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("the repository's plan is complete, sound and compiled", () => {
  const plan = loadPlan(DEFAULT_PLAN);
  assert.deepEqual(planProblems(plan), []);
  assert.equal(plan.stories.length, 100);
  assert.ok(compiledCurrent(plan), "stories.json is older than its sources: run node tools/video/story-plans/validate.mjs --write");
});
