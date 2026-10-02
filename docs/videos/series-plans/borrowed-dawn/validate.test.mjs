import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import test from "node:test";
import { validatePlan, workerCompatibility } from "./validate.mjs";

const read = (name) => JSON.parse(readFileSync(new URL(name, import.meta.url), "utf8"));
const copy = (value) => structuredClone(value);

// Deliberately synthetic schema fixture: not story text and never written to the plan.
function fixture() {
  const plan = read("plan.json");
  const setting = read("setting.json");
  const contract = read("authoring-contract.json");
  const endingTypes = ["danger", "reveal", "choice", "reversal", "emotion"];
  const seasons = Array.from({ length: 10 }, (_, seasonIndex) => ({
    number: seasonIndex + 1,
    title: `Test season ${seasonIndex + 1}`,
    theme: "Synthetic test theme",
    core_conflict: "Synthetic test conflict",
    time_span: "Synthetic test time",
    season_resolution: "Synthetic test resolution",
    season_hook: "Synthetic test hook",
    episodes: Array.from({ length: 12 }, (_, index) => {
      const number = seasonIndex * 12 + index + 1;
      const text = `Synthetic episode ${number}`;
      return {
        number, title: text, logline: text, hook: text, conflict: text, turn: text,
        cliffhanger: { type: endingTypes[(number - 1) % endingTypes.length], text: number === 120 ? "Resolved ordinary life" : text },
        tension: [2, 4, 3, 5, number === 120 ? plan.production_support.gaps.find((gap) => gap.code === "closed-finale").planned_last_tension : 4],
        setups: setting.mysteries.filter((thread) => thread.introduced_in === number).map((thread) => thread.id),
        payoffs: setting.mysteries.filter((thread) => thread.resolved_in === number).map((thread) => thread.id),
        general_payoffs: number % 4 === 0 ? ["A specific synthetic task is completed"] : [],
        characters: ["shen-che"], locations: ["Test location"], theme: text,
        high_tension: ["first_half", "second_half"].map((beat) => ({ beat, event: text, stakes: "Test loss", consequence: "Test lasting result" })),
        consequence: text,
        state: { time: text, knowledge: text, character_state: text, evidence: text, carry_forward: text },
        closed_ending: number === 120,
      };
    }),
  }));
  return { plan, setting, seasons, contract };
}

const episode = (data, number) => data.seasons[Math.floor((number - 1) / 12)].episodes[(number - 1) % 12];
function artifactFixture() {
  const data = fixture();
  const encode = (value) => `${JSON.stringify(value, null, 2)}\n`;
  const hash = (value) => createHash("sha256").update(value).digest("hex");
  data.outline = { chapters: data.seasons.map((season) => ({ number: season.number, title: season.title, theme: season.theme, episodes: season.episodes.map(({ number, title, logline }) => ({ number, title, logline })) })) };
  data.files = {
    "authoring-contract.json": encode(data.contract), "plan.json": encode(data.plan), "setting.json": encode(data.setting),
    ...Object.fromEntries(data.seasons.map((season) => [`season-${String(season.number).padStart(2, "0")}.json`, encode(season)])),
  };
  const sourceNames = Object.keys(data.files);
  const supportNames = ["README.md", "review.md", "build.mjs", "validate.mjs", "validate.test.mjs"];
  for (const name of supportNames) data.files[name] = `Synthetic support file: ${name}\n`;
  data.files["setting.md"] = "# Synthetic setting\n";
  data.files["outline.md"] = "# Synthetic outline\n";
  for (const season of data.seasons) data.files[`season-${String(season.number).padStart(2, "0")}.md`] = `# Synthetic chapter ${season.number}\n`;
  data.files["outline.json"] = encode(data.outline);
  data.documents = {
    schema_version: 1, stage: "planning", ready_for_import: false, category: "anime",
    documents: [
      { kind: "setting", body_md: data.files["setting.md"], body_json: copy(data.setting) },
      { kind: "outline", body_md: data.files["outline.md"], body_json: copy(data.outline) },
      ...data.seasons.map((season) => ({ kind: "chapter", chapter_number: season.number, body_md: data.files[`season-${String(season.number).padStart(2, "0")}.md`], body_json: copy(season) })),
    ],
  };
  data.files["documents.json"] = encode(data.documents);
  data.files["continuity.md"] = "# Synthetic continuity\n";
  data.files["continuity.csv"] = "episode,title\n";
  const generatedNames = Object.keys(data.files).filter((name) => !sourceNames.includes(name) && !supportNames.includes(name));
  data.manifest = {
    schema_version: 1, artifact_kind: data.plan.artifact_kind, slug: data.plan.slug, category: "anime",
    episode_count: 120, season_count: 10, ready_for_import: false, admin_series_created: false, media_generated: false, published: false,
    source_files: Object.fromEntries(sourceNames.map((name) => [name, hash(data.files[name])])),
    support_files: Object.fromEntries(supportNames.map((name) => [name, hash(data.files[name])])),
    generated_files: Object.fromEntries(generatedNames.map((name) => [name, hash(data.files[name])])),
  };
  data.files["manifest.json"] = encode(data.manifest);
  return data;
}

function fails(mutator, pattern) {
  const data = fixture();
  mutator(data);
  const result = validatePlan(data);
  assert.ok(result.errors.some((error) => pattern.test(error)), `Expected ${pattern}; got ${JSON.stringify(result.errors)}`);
}

test("complete planning fixture passes while keeping production warnings", () => {
  const result = validatePlan(fixture());
  assert.deepEqual(result.errors, []);
  assert.equal(result.episode_count, 120);
  assert.equal(result.season_count, 10);
  assert.ok(result.warnings.some((warning) => warning.includes("不等於可匯入")));
  assert.ok(result.warnings.some((warning) => warning.includes("尚未提供或量測")));
});

test("missing and duplicate episodes are rejected", () => {
  fails((data) => data.seasons[3].episodes.pop(), /必須恰好 12 集|必須有 120 集/);
  fails((data) => { episode(data, 37).number = 36; }, /全劇集號含重複值/);
});

test("season order and cross-season episode numbering cannot be changed", () => {
  fails((data) => { data.seasons[2].number = 7; }, /number 必須是 3/);
  fails((data) => { const rows = data.seasons[2].episodes; [rows[0], rows[1]] = [rows[1], rows[0]]; }, /全劇集號必須是 25/);
});

test("each episode has exactly two complete, ordered tension events", () => {
  fails((data) => episode(data, 38).high_tension.pop(), /high_tension 必須恰好兩段/);
  fails((data) => { episode(data, 38).high_tension[1].stakes = "  "; }, /stakes 必須非空/);
  fails((data) => episode(data, 38).high_tension.reverse(), /先 first_half 後 second_half/);
});

test("cast and thread references must exist", () => {
  fails((data) => episode(data, 41).characters.push("missing-person"), /未知 ID "missing-person"/);
  fails((data) => episode(data, 41).setups.push("m99"), /未知 ID "m99"/);
  fails((data) => data.setting.characters.pop(), /缺少約定角色/);
});

test("payoff cannot precede its introduction or its actual setup", () => {
  fails((data) => episode(data, 59).payoffs.push("m06"), /早於 introduced_in=60/);
  fails((data) => {
    episode(data, 1).setups = episode(data, 1).setups.filter((id) => id !== "m05");
    episode(data, 1).payoffs.push("m05");
    episode(data, 2).setups.push("m05");
  }, /先 payoff 後 setup/);
});

test("setup cannot precede this package's declared earliest seed", () => {
  fails((data) => episode(data, 59).setups.push("m06"), /早於 introduced_in=60/);
});

test("declared final resolution must appear in its episode's payoff list", () => {
  fails((data) => { episode(data, 107).payoffs = episode(data, 107).payoffs.filter((id) => id !== "m09"); }, /resolved_in=107 當集沒有對應 payoff/);
});

test("a long mystery may stay open while concrete general payoffs keep the four-episode rhythm", () => {
  const data = fixture();
  assert.deepEqual(episode(data, 2).payoffs, []);
  assert.deepEqual(episode(data, 3).payoffs, []);
  assert.deepEqual(validatePlan(data).errors, []);
  fails((next) => { episode(next, 4).general_payoffs = []; }, /E1–E4 四集窗口缺少/);
});

test("duration, anime category, and anime 2D look cannot be quietly changed", () => {
  fails((data) => { data.plan.runtime.story_minutes = 3; }, /story_minutes 必須是 22/);
  fails((data) => { data.plan.runtime.broadcast_slot_minutes = 22; }, /broadcast_slot_minutes 必須是 30/);
  fails((data) => { data.plan.video_defaults.category = "story"; }, /video_defaults.category 必須是 anime/);
  fails((data) => { data.plan.video_defaults.look.preset = "flat-explainer"; }, /look.preset 必須是 anime-2d/);
  fails((data) => { data.contract.story_minutes = 8; }, /authoring contract 必須維持正文 22/);
});

test("false production readiness and hidden gaps are rejected", () => {
  fails((data) => { data.plan.production_support.ready_for_import = true; }, /ready_for_import 必須保持 false/);
  fails((data) => { data.plan.production_support.gaps = []; }, /gaps 必須誠實保留/);
  fails((data) => { data.plan.production_support.media_generated = true; }, /media_generated 必須保持 false/);
  fails((data) => { data.plan.production_support.gaps = data.plan.production_support.gaps.filter((gap) => gap.code !== "ensemble-retention"); }, /ensemble-retention gap 必須保留/);
  fails((data) => { data.plan.genre = "xianxia"; }, /不得改題材繞過工人限制/);
});

test("the ending stays closed, honest and low tension instead of inventing a cliffhanger", () => {
  fails((data) => { data.setting.finale.new_crisis_or_sequel_hook = true; }, /不得宣稱新增危機/);
  fails((data) => { episode(data, 120).closed_ending = false; }, /E120 必須 closed_ending=true/);
  fails((data) => { episode(data, 120).cliffhanger.type = "danger"; }, /E120 type=emotion/);
  fails((data) => { episode(data, 120).tension[4] = 4; }, /E120 末段必須為 1–3/);
  fails((data) => { episode(data, 119).tension[4] = 2; }, /末段張力必須 >=4/);
});

test("adjacent ending types and necessary continuity state are checked", () => {
  fails((data) => { episode(data, 13).cliffhanger.type = episode(data, 12).cliffhanger.type; }, /相鄰 ending type 不得相同/);
  fails((data) => { episode(data, 60).state.evidence = ""; }, /state.evidence 必須是非空字串/);
});

test("derived outline cannot drift from its source episode titles", () => {
  const data = fixture();
  data.outline = { chapters: data.seasons.map((season) => ({ number: season.number, title: season.title, theme: season.theme, episodes: copy(season.episodes) })) };
  assert.deepEqual(validatePlan(data).errors, []);
  data.outline.chapters[4].episodes[0].title = "Changed downstream title";
  assert.ok(validatePlan(data).errors.some((error) => /outline 第 5 季集號／標題／logline 偏離 source/.test(error)));
});

test("derived documents and hashes match their real local source bytes", () => {
  assert.deepEqual(validatePlan(artifactFixture()).errors, []);
  const data = artifactFixture();
  data.files["season-05.json"] += " \n";
  assert.ok(validatePlan(data).errors.some((error) => /雜湊不符：season-05.json/.test(error)));
});

test("documents cannot substitute drifted body_json or an unrelated body_md", () => {
  const data = artifactFixture();
  data.documents.documents[2].body_json.episodes[0].title = "Changed only in downstream document";
  data.documents.documents[3].body_md = "# Placeholder instead of the actual chapter";
  const errors = validatePlan(data).errors;
  assert.ok(errors.some((error) => /documents\[2\].body_json 偏離來源/.test(error)));
  assert.ok(errors.some((error) => /documents\[3\].body_md 不等於實際/.test(error)));
});

test("manifest lists, counts and production declarations cannot overstate the artifact", () => {
  const data = artifactFixture();
  data.manifest.episode_count = 121;
  data.manifest.ready_for_import = true;
  delete data.manifest.generated_files["continuity.csv"];
  const errors = validatePlan(data).errors;
  assert.ok(errors.some((error) => /manifest 必須宣告 anime、120 集、10 季/.test(error)));
  assert.ok(errors.some((error) => /manifest.ready_for_import 必須保持 false/.test(error)));
  assert.ok(errors.some((error) => /manifest.generated_files 清單缺失/.test(error)));
});

test("real worker checks distinguish structural-only documents from custom retention and the closed finale", async () => {
  const report = await workerCompatibility(artifactFixture());
  assert.equal(report.results.length, 12);
  const chapters = report.results.filter((row) => row.kind === "chapter");
  assert.ok(chapters.slice(0, 9).every((row) => row.structural_only_problem === null));
  assert.match(chapters[9].structural_only_problem, /episode 120 must end tense/);
  assert.ok(chapters.slice(0, 9).every((row) => /needs hook_type/.test(row.actual_worker_problem)));
  assert.match(chapters[9].actual_worker_problem, /episode 120 must end tense/);
});

test("invalid top-level inputs return errors instead of throwing", () => {
  assert.ok(validatePlan({}).errors.length > 0);
  assert.ok(validatePlan({ plan: null, setting: null, seasons: [null] }).errors.length > 0);
  const data = fixture();
  episode(data, 4).general_payoffs = {};
  episode(data, 120).tension = {};
  data.outline = { chapters: {} };
  assert.ok(validatePlan(data).errors.length > 0);
});
