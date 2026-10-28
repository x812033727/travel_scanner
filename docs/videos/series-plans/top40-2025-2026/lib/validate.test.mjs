// node --test docs/videos/series-plans/top40-2025-2026/lib/validate.test.mjs
import assert from "node:assert/strict";
import { test } from "node:test";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { limitsOf, loadPlan, outlineProblems, planProblems, seasonProblems } from "./validate.mjs";
import { render } from "./build.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const reference = join(here, "..", "..", "zhong-tian-qu-qi");

const setting = {
  title: "測試劇",
  tones: [{ id: "shuang", name: "爽" }, { id: "xiju", name: "喜" }],
  characters: [{ id: "lead", name: "主角" }],
  beasts: [],
  mysteries: [{ id: "m01", question: "?", setup_season: 1, reveal_season: 1, answer: "a" }],
};
const outline = {
  seasons: [{ number: 1, title: "一", theme: "t", start_state: "s", end_state: "e", episodes: [1, 2], chapters: [{ number: 1, episodes: [1, 2], title: "c", beats: "b", end: "e", spectacle: "s", threads: ["x"], tones: ["shuang"] }] }],
};
const plan = { episodes_per_chapter: 2, episode_seconds: { min: 90, max: 180, chapter_finale_min: 120 }, hooks_per_episode: { min: 3, max: 5 } };

function episode(number, extra = {}) {
  return {
    number, season_episode: number, chapter: 1, title: `第${number}`, youtube_title: "標題", duration_s: 120, logline: "l",
    hook: `開頭${number}`, hook_type: "image", mid_hook: `中段${number}`, conflict: "c", turn: "t",
    satisfaction: [{ beat: "first_half", type: "face_slap" }, { beat: "ending", type: "reversal" }],
    cliffhanger: { type: number === 2 ? "reversal" : "danger", text: `結尾${number}`, question: "然後？" },
    lead_arc: "wins", tension: [3, 3, 4, 4, 5], tones: ["shuang"], spectacle: "s", glamour_shot: "g",
    setups: number === 1 ? ["m01"] : [], payoffs: number === 2 ? ["m01"] : [], reveals: number === 2 ? ["m01"] : [], general_payoffs: [],
    characters: ["lead"], locations: ["家"], state: { time: "t", knowledge: "k", carry_forward: "c" },
    ...extra,
  };
}
const season = (episodes) => ({ number: 1, title: "一", theme: "t", start_state: "s", end_state: "e", threads: [], episodes });

test("limits default to the 種田娶妻 rules and read plan.json otherwise", () => {
  assert.deepEqual(limitsOf({}), { minSeconds: 50, maxSeconds: 180, finaleMinSeconds: 120, minHooks: 3, maxHooks: 3, episodesPerChapter: 10 });
  assert.equal(limitsOf(plan).minSeconds, 90);
  assert.equal(limitsOf(plan).maxHooks, 5);
});

test("a clean two-episode season passes", () => {
  assert.deepEqual(planProblems({ setting, outline, plan, seasons: [season([episode(1), episode(2)])] }), []);
  assert.deepEqual(outlineProblems({ setting, outline, plan }), []);
});

test("episode length follows plan.json", () => {
  const problems = seasonProblems(season([episode(1, { duration_s: 60 }), episode(2)]), { setting, outline, plan });
  assert.ok(problems.some((p) => p.includes("duration_s must be 90–180")));
});

test("extra hooks must be distinct and within the plan's count", () => {
  const ok = seasonProblems(season([episode(1, { extra_hooks: ["第四鉤", "第五鉤"] }), episode(2)]), { setting, outline, plan });
  assert.deepEqual(ok, []);
  const dup = seasonProblems(season([episode(1, { extra_hooks: ["開頭1"] }), episode(2)]), { setting, outline, plan });
  assert.ok(dup.some((p) => p.includes("must all be different beats")));
  const many = seasonProblems(season([episode(1, { extra_hooks: ["a", "b", "c"] }), episode(2)]), { setting, outline, plan });
  assert.ok(many.some((p) => p.includes("3–5 hooks")));
  const strict = seasonProblems(season([episode(1, { extra_hooks: ["a"] }), episode(2)]), { setting, outline, plan: {} });
  assert.ok(strict.some((p) => p.includes("3–3 hooks")));
});

test("outline chapters must tile the season's episode range", () => {
  const broken = { seasons: [{ ...outline.seasons[0], chapters: [] }] };
  assert.ok(outlineProblems({ setting, outline: broken, plan }).some((p) => p.includes("do not cover")));
});

test("the shared checker accepts the 種田娶妻 plan unchanged and renders the same season text", () => {
  const loaded = loadPlan(reference);
  assert.deepEqual(outlineProblems(loaded), []);
  assert.deepEqual(planProblems(loaded), []);
  const out = render(loaded);
  assert.match(out["season-01.md"], /^<!-- 由 lib\/build\.mjs/);
  assert.ok(out["season-01.md"].includes("### 第 1 集（本季第 1 集）"));
});
