import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";

import { canonical, CHAPTER_KEYS, claimSupported, compile, compiledCurrent, DEFAULT_PLAN, loadPlan, order, planProblems, reviewProblems, scheduleMarkdown, scheduleProblems, serialize, seriesProblems, storyHash, storyProblems, STORY_KEYS } from "./plan.mjs";
import { fetchSources, main, USER_AGENT } from "./validate.mjs";

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

test("fetchSources asks for every source under the worker's name", async () => {
  const asked = [];
  const fetchImpl = async (url, options) => {
    asked.push([url, options.headers["User-Agent"]]);
    if (url.includes("wikipedia")) throw new Error("socket hang up");
    return { status: url.includes("news") ? 403 : 200 };
  };
  const results = await fetchSources({ stories: [{ id: "A01", story: story() }] }, { fetchImpl, gap: 0 });
  assert.deepEqual(results.map((each) => each.status ?? each.error), [200, 403, "socket hang up"]);
  assert.ok(asked.every(([, agent]) => agent === USER_AGENT));
  assert.doesNotMatch(USER_AGENT, /gmail|@(?!mokaair\.com)/);
});

test("the repository's plan is complete, sound and compiled", () => {
  const plan = loadPlan(DEFAULT_PLAN);
  assert.deepEqual(planProblems(plan), []);
  assert.equal(plan.stories.length, 100);
  assert.ok(compiledCurrent(plan), "stories.json is older than its sources: run node tools/video/story-plans/validate.mjs --write");
});
