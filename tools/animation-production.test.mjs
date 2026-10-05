/**
 * The three production scripts the animation-production skill ships
 * (.agents/skills/animation-production/scripts/): the estimate, the offline preflight and the
 * run report.
 *
 * What is pinned here is that their numbers are the tools' own: the PRICES table is compared
 * with apps/api/app/video_media/catalog.py model by model (a price changed there goes red here),
 * the take, round and exit constants with the stage modules, the seconds-bought rule with
 * clips.mjs clipSeconds, and the current estimator/preflight behavior for preserved avoidance
 * constraints and bounded clip identity questions. Provider payload behavior is covered by the
 * API provider tests. The scripts then run on the drama fixture and on a
 * sandbox work directory prepared the way tools/video/media/clips.test.mjs prepares one.
 */
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { writeSyntheticNarration } from "./video/assemble/synthetic.mjs";
import { approve } from "./video/core/approvals.mjs";
import { lookHash, resolveLook } from "./video/core/drama.mjs";
import { DRAMA_FIXTURE_FILE, dramaFixture, fixtureLexicon, sandbox } from "./video/core/fixtures/load.mjs";
import { estimateTimeline, FPS, visualHash } from "./video/core/timeline.mjs";
import {
  estimateEpisode,
  hailuoSeconds,
  KLING_CREDITS_PER_SECOND,
  klingSeconds,
  MAX_CLIP_TAKES,
  MAX_KEYFRAME_TAKES,
  MAX_LOOK_ROUNDS,
  MIN_CLIP_SECONDS,
  MAX_CLIP_SECONDS,
  PLANS,
  PRICES,
  secondsBought,
} from "../.agents/skills/animation-production/scripts/episode_estimate.mjs";
import { EXIT, JUDGE_CALLS_PER_HOUR, JUDGE_MONTHLY_BUDGET, KEYFRAME_MIN_PSNR, MAX_RUBRIC_QUESTION, preflight } from "../.agents/skills/animation-production/scripts/drama_preflight.mjs";
import { renderMarkdown, renderReport, runReport } from "../.agents/skills/animation-production/scripts/run_report.mjs";
import { lockOf } from "../.agents/skills/animation-preproduction/scripts/plan_lock.mjs";
import { planEpisode } from "../.agents/skills/animation-preproduction/scripts/shot_plan.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const SCRIPTS = path.join(ROOT, ".agents", "skills", "animation-production", "scripts");
const SHA = (data) => createHash("sha256").update(data).digest("hex");
const PNG = (text) => Buffer.concat([Buffer.from("\x89PNG\r\n\x1a\n", "binary"), Buffer.from(text)]);
const MP4 = (text) => Buffer.concat([Buffer.from("\x00\x00\x00\x18ftypisom", "binary"), Buffer.from(text)]);
const SHOT_IDS = ["opening", "farewell", "sea-storm", "bird"];
const sum = (items) => items.reduce((total, item) => total + item, 0);
const near = (actual, expected, message) => assert.ok(Math.abs(actual - expected) < 1e-6, `${message ?? ""}: ${actual} vs ${expected}`);
// The scripts round money and ratios to four decimals before printing.
const near4 = (actual, expected, message) => assert.ok(Math.abs(actual - expected) < 5e-5 + 1e-9, `${message ?? ""}: ${actual} vs ${expected}`);
const run = (script, ...args) => spawnSync(process.execPath, [path.join(SCRIPTS, script), ...args], { encoding: "utf8", env: { ...process.env, VIDEO_MIN_EPISODE_MINUTES: "0" } });
const framesOf = (doc) => {
  const timeline = estimateTimeline(doc);
  return (id) => {
    const scene = timeline.scenes.find((each) => each.id === id);
    return scene.end_frame - scene.start_frame;
  };
};

/** catalog.py read with a regex per MediaModel block: id, the three prices and the durations. */
function catalogModels() {
  const text = readFileSync(path.join(ROOT, "apps", "api", "app", "video_media", "catalog.py"), "utf8");
  const models = {};
  for (const block of text.split(/\bMediaModel\(\s*\n/).slice(1)) {
    const id = /^\s*"([^"]+)"/.exec(block)?.[1];
    if (!id) continue;
    const num = (name) => {
      const match = new RegExp(`\\b${name}=([0-9.]+)`).exec(block);
      return match ? Number(match[1]) : null;
    };
    let durations = [];
    if (/durations=_SECONDS_4_TO_10/.test(block)) durations = [4, 5, 6, 7, 8, 9, 10];
    else {
      const match = /durations=\(([0-9, ]+)\)/.exec(block);
      if (match) durations = match[1].split(",").map((each) => Number(each.trim())).filter(Number.isFinite);
    }
    models[id] = { usd_per_second: num("usd_per_second"), usd_per_image: num("usd_per_image"), usd_per_image_2k: num("usd_per_image_2k"), usd_per_track: num("usd_per_track"), durations };
  }
  return { text, models };
}

/**
 * A drama work directory after tts, look (chosen) and keyframes, as tools/video/media/clips.test.mjs
 * prepares one; `mutate(doc)` changes the script first and writes it back so the hashes match.
 */
function prepared(mutate = null) {
  const box = sandbox("fixture-drama", "drama");
  const doc = dramaFixture();
  if (mutate) {
    mutate(doc);
    writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);
  }
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  mkdirSync(path.join(box.workdir, "clips"), { recursive: true });
  mkdirSync(path.join(box.workdir, "characters", "jingwei"), { recursive: true });
  mkdirSync(path.join(box.workdir, "characters", "yandi"), { recursive: true });
  const timeline = writeSyntheticNarration(doc, fixtureLexicon(), box.workdir);
  const shots = {};
  for (const scene of doc.scenes.filter((each) => each.template === "shot")) {
    const file = `keyframes/${scene.id}-1.png`;
    writeFileSync(path.join(box.workdir, file), PNG(`key ${scene.id}`));
    shots[scene.id] = { file, sha256: SHA(PNG(`key ${scene.id}`)), seed: 1, judge: { overall: 8, passed: true, problems: [] }, needs_review: false };
  }
  writeFileSync(path.join(box.workdir, "keyframes", "manifest.json"), JSON.stringify({ look_hash: lookHash(doc), visual_hash: visualHash(doc), shots }));
  const characters = {};
  for (const id of ["jingwei", "yandi"]) {
    const file = `characters/${id}/001.png`;
    writeFileSync(path.join(box.workdir, file), PNG(`sheet ${id}`));
    characters[id] = { name: id, candidates: [{ n: 1, seed: 1, file, sha256: SHA(PNG(`sheet ${id}`)), judge: { overall: 9, passed: true } }], suggested: 1 };
  }
  writeFileSync(path.join(box.workdir, "characters", "manifest.json"), JSON.stringify({ look_hash: lookHash(doc), characters }));
  writeFileSync(path.join(box.workdir, "characters", "choice.json"), JSON.stringify({ look_hash: lookHash(doc), chosen: { jingwei: 1, yandi: 1 } }));
  return { box, doc, timeline, shots, characters };
}

const approveBoth = async (box) => {
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
};
const writeClips = (box, doc, timeline, shots) => writeFileSync(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify({ speech_hash: timeline.speech_hash, visual_hash: visualHash(doc), look_hash: lookHash(doc), clips_hash: "0".repeat(16), shots }));
// The lock package animation-preproduction writes before any money is spent: the server route, on the recorded timeline.
const PLAN_LOCK = path.join(ROOT, ".agents", "skills", "animation-preproduction", "scripts", "plan_lock.mjs");
const lockShots = (box, doc, timeline, created = "2026-10-05T00:00:00.000Z") => {
  const lock = { ...lockOf(doc, fixtureLexicon(), planEpisode(doc, { route: "server", timeline })), created_at: created, note: "test" };
  mkdirSync(path.join(box.workdir, "plan"), { recursive: true });
  writeFileSync(path.join(box.workdir, "plan", "lock.json"), JSON.stringify(lock));
  return lock;
};

test("PRICES carries the catalog's API prices, model by model, and the judge price", () => {
  const { text, models } = catalogModels();
  assert.ok(Object.keys(models).length >= 6, "catalog.py was parsed");
  for (const id of ["gemini-omni-1.1-flash", "veo-3.1-lite-generate-preview", "veo-3.1-generate-001", "veo-3.1-fast-generate-001", "MiniMax-H3"]) assert.equal(PRICES[id]?.kind, "clip", `${id} is priced: the references name it`);
  for (const [id, entry] of Object.entries(PRICES)) {
    if (id === "judge") {
      assert.match(text, /\bJUDGE_USD_PER_CALL = 0\.01\b/);
      assert.equal(entry.usd_per_call, 0.01);
      continue;
    }
    const model = models[id];
    assert.ok(model, `${id} is not a MediaModel in catalog.py`);
    if (entry.kind === "clip") {
      assert.equal(entry.usd_per_second, model.usd_per_second, `${id} usd_per_second`);
      assert.deepEqual(entry.durations, model.durations, `${id} durations`);
    } else if (entry.kind === "image") {
      assert.equal(entry.usd_per_image, model.usd_per_image, `${id} usd_per_image`);
      assert.equal(entry.usd_per_image_2k, model.usd_per_image_2k, `${id} usd_per_image_2k`);
    } else if (entry.kind === "music") {
      assert.equal(entry.usd_per_track, model.usd_per_track, `${id} usd_per_track`);
    } else assert.fail(`${id}: unknown kind ${entry.kind}`);
  }
});

test("estimating Lite and non-Lite with avoidance constraints preserves the script and look hash", () => {
  const doc = dramaFixture();
  const before = structuredClone(doc);
  const hash = lookHash(doc);
  const negative = resolveLook(doc.look).negative;
  assert.ok(negative.length > 0, "the preset has real avoidance constraints");
  for (const model of ["veo-3.1-lite-generate-preview", "gemini-omni-1.1-flash"]) {
    const estimate = estimateEpisode(doc, { model });
    assert.equal(estimate.verdict.ok, true, JSON.stringify(estimate.verdict.problems));
    assert.deepEqual(doc, before);
    assert.equal(resolveLook(doc.look).negative, negative);
    assert.equal(lookHash(doc), hash);
  }
});

test("the take, round, clip-second and exit constants mirror the tools, and secondsBought is clips.mjs clipSeconds", async () => {
  const [keyframes, clips, look, cli] = await Promise.all([import("./video/media/keyframes.mjs"), import("./video/media/clips.mjs"), import("./video/media/look.mjs"), import("./video/cli.mjs")]);
  assert.equal(MAX_KEYFRAME_TAKES, keyframes.MAX_KEYFRAME_TAKES);
  assert.equal(MAX_CLIP_TAKES, clips.MAX_CLIP_TAKES);
  assert.equal(MIN_CLIP_SECONDS, clips.MIN_CLIP_SECONDS);
  assert.equal(MAX_CLIP_SECONDS, clips.MAX_CLIP_SECONDS);
  assert.equal(MAX_LOOK_ROUNDS, look.MAX_LOOK_ROUNDS);
  assert.deepEqual(EXIT, cli.EXIT);
  const { KEYFRAME_MIN_PSNR: psnr } = await import("./video/assemble/drama.mjs");
  assert.equal(KEYFRAME_MIN_PSNR, psnr);
  for (const model of Object.keys(PRICES).filter((id) => PRICES[id].kind === "clip")) {
    for (const resolution of PRICES[model].resolutions) {
      for (const frames of [1, 30, 95, 150, 241, 300, 400, 3000]) {
        assert.equal(secondsBought(frames, model, resolution), clips.clipSeconds(frames, PRICES[model].durations, { model, resolution }), `${model} ${resolution} ${frames} frames`);
      }
    }
  }
  assert.equal(secondsBought(30, "veo-3.1-lite-generate-preview", "1080p"), 8, "Lite at 1080p buys eight seconds whatever the need");
  assert.equal(secondsBought(30, "veo-3.1-lite-generate-preview", "720p"), 4);
  assert.deepEqual([hailuoSeconds(30), hailuoSeconds(95), hailuoSeconds(300), hailuoSeconds(900)], [4, 4, 10, 15]);
  assert.deepEqual([klingSeconds(30), klingSeconds(95), klingSeconds(300), klingSeconds(900)], [3, 4, 10, 15], "Kling VIDEO 3.0 sells 3 to 15 whole seconds");
  const admin = readFileSync(path.join(ROOT, "apps", "api", "app", "video_media", "admin_api.py"), "utf8");
  assert.match(admin, new RegExp(`\\bJUDGES_PER_HOUR = ${JUDGE_CALLS_PER_HOUR}\\b`), "the media route's judge rate limit");
  const models = readFileSync(path.join(ROOT, "apps", "api", "app", "video_automation", "models.py"), "utf8");
  assert.match(models, new RegExp(`"monthly_judge_calls_budget": ${JUDGE_MONTHLY_BUDGET}\\b`));
  const schemas = readFileSync(path.join(ROOT, "apps", "api", "app", "video_media", "schemas.py"), "utf8");
  assert.match(schemas, new RegExp(`question: str = Field\\(min_length=1, max_length=${MAX_RUBRIC_QUESTION}\\)`));
});

test("the drama fixture is priced from the constants: per stage, one take and the take caps, per clip model", () => {
  const doc = dramaFixture();
  const frames = framesOf(doc);
  const report = estimateEpisode(doc);
  const image = PRICES["gemini-3-pro-image"].usd_per_image;
  const judge = PRICES.judge.usd_per_call;
  const price = PRICES["gemini-omni-1.1-flash"].usd_per_second;
  const bought = SHOT_IDS.map((id) => secondsBought(frames(id), "gemini-omni-1.1-flash", "1080p"));
  const sheets = 2 * 3;
  assert.deepEqual(report.shots.map((shot) => shot.id), SHOT_IDS, "the outro card is not a shot");
  assert.deepEqual(report.shots.map((shot) => shot.bought_s), bought);
  assert.deepEqual(report.shots.map((shot) => shot.visual), ["clip", "clip", "clip", "clip"]);
  assert.equal(report.counts.characters, 2);
  assert.equal(report.stages.look.images_one, sheets);
  assert.equal(report.stages.look.images_cap, sheets * MAX_LOOK_ROUNDS);
  assert.equal(report.stages.keyframes.images_one, 4);
  assert.equal(report.stages.keyframes.images_cap, 4 * MAX_KEYFRAME_TAKES);
  assert.equal(report.stages.keyframes.end_frames, 0);
  assert.equal(report.stages.clips.clip_seconds_one, sum(bought));
  assert.equal(report.stages.clips.clip_seconds_cap, sum(bought) * MAX_CLIP_TAKES);
  assert.equal(report.stages.judge.calls_one, sheets + 4 + 4);
  assert.equal(report.stages.judge.calls_cap, sheets * MAX_LOOK_ROUNDS + 4 * MAX_KEYFRAME_TAKES + 4 * MAX_CLIP_TAKES);
  assert.equal(report.stages.music.usd, PRICES["lyria-3.5"].usd_per_track, "music.prompt buys one track");
  near(report.totals.usd_one, sheets * image + 4 * image + sum(bought) * price + (sheets + 8) * judge + 0.08, "one take");
  near(report.totals.usd_cap, sheets * MAX_LOOK_ROUNDS * image + 4 * MAX_KEYFRAME_TAKES * image + sum(bought) * MAX_CLIP_TAKES * price + (sheets * MAX_LOOK_ROUNDS + 4 * MAX_KEYFRAME_TAKES + 4 * MAX_CLIP_TAKES) * judge + 0.08, "worst case");
  const opening = report.shots[0];
  near(opening.usd_one, image + 2 * judge + opening.bought_s * price);
  near(opening.usd_cap, MAX_KEYFRAME_TAKES * (image + judge) + MAX_CLIP_TAKES * (opening.bought_s * price + judge));
  assert.equal(report.verdict.ok, true);
  assert.equal(report.plan, null);

  const lite = estimateEpisode(doc, { model: "veo-3.1-lite-generate-preview" });
  assert.deepEqual(lite.shots.map((shot) => shot.bought_s), [8, 8, 8, 8], "Lite at 1080p: eight seconds each");
  near(lite.stages.clips.usd_one, 32 * PRICES["veo-3.1-lite-generate-preview"].usd_per_second);
  assert.equal(lite.verdict.ok, true, JSON.stringify(lite.verdict.problems));
  assert.ok(resolveLook(doc.look).negative.length > 0, "Lite keeps the preset's avoidance constraints");
  const fast = estimateEpisode(doc, { model: "veo-3.1-fast-generate-001" });
  assert.deepEqual(fast.shots.map((shot) => shot.bought_s), [8, 8, 8, 8], "Fast at 1080p is a Veo 3.1 too");
  near(fast.stages.clips.usd_one, 32 * 0.12);
  const lite720 = estimateEpisode(doc, { model: "veo-3.1-lite-generate-preview", resolution: "720p" });
  assert.deepEqual(lite720.shots.map((shot) => shot.bought_s), SHOT_IDS.map((id) => secondsBought(frames(id), "veo-3.1-lite-generate-preview", "720p")));
  const h3 = estimateEpisode(doc, { model: "MiniMax-H3" });
  assert.equal(h3.resolution, "2k");
  near(h3.stages.clips.usd_one, sum(SHOT_IDS.map((id) => secondsBought(frames(id), "MiniMax-H3", "2k"))) * 0.13);
  const custom = estimateEpisode(doc, { model: "something-new", pricePerSecond: 0.5, imagePrice: 0.1 });
  near(custom.stages.clips.usd_one, sum(SHOT_IDS.map((id) => secondsBought(frames(id), "something-new"))) * 0.5);
  near(custom.stages.keyframes.usd_one, 0.4);
  assert.throws(() => estimateEpisode(doc, { model: "something-new" }), /unknown clip model/);

  // A still buys no clip and one judge less; a cut buys nothing; an end frame is one more image, judged never.
  const mixed = dramaFixture();
  mixed.scenes[1].data.visual = "still";
  mixed.scenes[3].data.source = { shot: "sea-storm", from_s: 1 };
  delete mixed.scenes[3].data.start_frame;
  mixed.scenes[0].data.end_frame = { prompt: "the girl has turned toward the sea" };
  const mixedReport = estimateEpisode(mixed);
  assert.deepEqual(mixedReport.shots.map((shot) => shot.visual), ["clip", "still", "clip", "cut"]);
  assert.deepEqual(mixedReport.shots.map((shot) => [shot.images_one, shot.judge_one, shot.bought_s]), [[2, 2, bought[0]], [1, 1, 0], [1, 2, bought[2]], [0, 0, 0]]);
  assert.equal(mixedReport.stages.keyframes.end_frames, 1);
  assert.equal(mixedReport.stages.keyframes.images_one, 4);
  assert.equal(mixedReport.stages.clips.clip_seconds_one, bought[0] + bought[2]);
  assert.equal(mixedReport.counts.cuts, 1);
  // An existing cut is checked against what its source buys under this model, not against lint's ten seconds.
  const room = Math.min(bought[2], MAX_CLIP_SECONDS);
  assert.equal(mixedReport.shots[3].source_room_s, room);
  assert.equal(mixedReport.shots[3].source_fits, 1 + frames("bird") / FPS <= room);
  const late = dramaFixture();
  late.scenes[3].data.source = { shot: "sea-storm", from_s: 9 };
  delete late.scenes[3].data.start_frame;
  const lateReport = estimateEpisode(late);
  assert.equal(lateReport.shots[3].source_fits, false);
  assert.equal(lateReport.verdict.ok, false);
  assert.match(lateReport.verdict.problems.join("\n"), /bird 從 sea-storm 的 9 s 切.*只買/);
  const orphan = dramaFixture();
  orphan.scenes[3].data.source = { shot: "nowhere", from_s: 0 };
  delete orphan.scenes[3].data.start_frame;
  assert.match(estimateEpisode(orphan).verdict.problems.join("\n"), /不是 clip 鏡/);
});

test("--tier caps the clips and names the stills to make; --cap and --month-clip-seconds give the verdict", () => {
  const doc = dramaFixture();
  const price = PRICES["gemini-omni-1.1-flash"].usd_per_second;
  const stills = estimateEpisode(doc, { tier: "stills" });
  assert.equal(stills.levers.stills.allowed_clips, 1, "a tenth of four shots, rounded up");
  assert.equal(stills.levers.stills.over_by, 3);
  assert.equal(stills.levers.stills.candidates.length, 3);
  near(stills.levers.stills.saving_usd, sum(stills.levers.stills.candidates.map((shot) => stills.shots.find((each) => each.id === shot.id).bought_s * price + 0.01)));
  near(stills.levers.stills.total_one_tiered, stills.totals.usd_one - stills.levers.stills.saving_usd);
  assert.equal(stills.verdict.ok, false);
  assert.match(stills.verdict.problems.join("\n"), /stills tier 最多 1 支片段/);
  const hybrid = estimateEpisode(doc, { tier: "hybrid" });
  assert.equal(hybrid.levers.stills.allowed_clips, 2);
  assert.equal(hybrid.levers.stills.over_by, 2);
  const clips = estimateEpisode(doc, { tier: "clips" });
  assert.equal(clips.levers.stills.over_by, 0);
  assert.equal(clips.verdict.ok, true);
  assert.throws(() => estimateEpisode(doc, { tier: "gold" }), /--tier must be one of/);
  // A look-only shot is the first candidate for a still.
  const looks = dramaFixture();
  looks.scenes[2].data.motion = "Her eyes close.";
  assert.equal(estimateEpisode(looks, { tier: "stills" }).levers.stills.candidates[0].id, "sea-storm");
  assert.equal(estimateEpisode(doc, { tier: "stills", production: true }).levers.stills.candidates, undefined, "the production profile allows no stills");

  const capped = estimateEpisode(doc, { cap: 1 });
  assert.equal(capped.verdict.ok, false);
  assert.match(capped.verdict.problems[0], /超過每影片上限 US\$1\.00/);
  const month = estimateEpisode(doc, { monthClipSeconds: 10 });
  assert.equal(month.verdict.ok, false);
  assert.match(month.verdict.problems[0], /每月額度 10 秒/);
});

test("--plan prices the same clips in Hailuo credits (2K or 768P, per plan) and in Kling credits (official per-second price, overridable)", () => {
  const doc = dramaFixture();
  const frames = framesOf(doc);
  const seconds = SHOT_IDS.map((id) => hailuoSeconds(frames(id)));
  const pro = estimateEpisode(doc, { plan: "hailuo:pro" });
  assert.equal(pro.plan.vendor, "hailuo");
  assert.equal(pro.plan.resolution, "2k", "1080p is not a Hailuo H3 resolution; the plan prices 2K");
  assert.equal(pro.plan.credits_per_second, 12);
  assert.equal(pro.plan.credits_basis, "實測 2026-10-04", "12 credits a second at 2K was measured on the owner's account: a 5 s clip cost 60");
  assert.ok(pro.plan.notes.some((note) => /2560×1440/.test(note) && /無水印下載/.test(note)), "the measured output size and the watermark-free download are named");
  assert.deepEqual(pro.plan.shots.map((shot) => shot.seconds), seconds);
  assert.equal(pro.plan.credits_one, sum(seconds) * 12);
  assert.equal(pro.plan.credits_cap, sum(seconds) * 12 * MAX_CLIP_TAKES);
  near4(pro.plan.share_cap, (sum(seconds) * 12 * MAX_CLIP_TAKES) / PLANS["hailuo:pro"].credits);
  near4(pro.plan.usd_page_one, sum(seconds) * 0.081);
  near4(pro.plan.usd_fee_one, (sum(seconds) * 12 * 54.99) / 4500);
  near4(pro.plan.usd_fee_cap, (sum(seconds) * 12 * 54.99 * MAX_CLIP_TAKES) / 4500);
  assert.equal(pro.plan.rounds_one, Math.ceil(4 / 2), "Pro runs two tasks at a time");
  assert.equal(pro.plan.unverified, false);
  assert.ok(pro.plan.notes.some((note) => /clips import/.test(note)));
  // The plan is set beside the server route: the same clips in US$, and the seconds a month that make the fee worth it.
  assert.equal(pro.plan.server_model, "gemini-omni-1.1-flash");
  near4(pro.plan.server_clip_usd_one, pro.stages.clips.usd_one);
  assert.equal(pro.plan.plan_seconds_per_month, Math.floor(4500 / 12));
  assert.equal(pro.plan.breakeven_seconds_monthly, Math.ceil(54.99 / 0.15));
  assert.equal(pro.plan.breakeven_seconds_annual, Math.ceil(30.40 / 0.15));
  assert.equal(estimateEpisode(doc, { plan: "hailuo:pro", model: "veo-3.1-lite-generate-preview" }).plan.breakeven_seconds_monthly, Math.ceil(54.99 / 0.08));
  const pro768 = estimateEpisode(doc, { plan: "hailuo:pro", resolution: "768p" });
  assert.equal(pro768.plan.credits_one, sum(seconds) * 7);
  assert.equal(pro768.plan.credits_basis, "推算", "768P was not measured: its 7 credits a second is still inferred from the plan page");
  near4(pro768.plan.usd_page_one, sum(seconds) * 0.047);
  assert.equal(pro768.resolution, "1080p", "768p is a Hailuo tier, not an Omni resolution: the server side keeps its default");
  assert.equal(estimateEpisode(doc, { plan: "hailuo:pro", model: "MiniMax-H3", resolution: "768p" }).resolution, "768p", "H3 does offer 768p");
  const standard = estimateEpisode(doc, { plan: "hailuo:standard" });
  assert.equal(standard.plan.credits_one, pro.plan.credits_one, "the credits per second are the same on every plan; the fee per credit differs");
  near4(standard.plan.usd_page_one, sum(seconds) * 0.101);
  assert.equal(standard.plan.rounds_one, 4, "Standard runs one task at a time");
  for (const [id, plan] of Object.entries(PLANS)) {
    if (plan.vendor === "hailuo") assert.ok(plan.fee_usd > 0 && plan.credits > 0 && plan.running >= 1, id);
    else assert.ok(plan.fee_usd > 0 && plan.credits > 0 && plan.credits_per_second === KLING_CREDITS_PER_SECOND, id);
  }

  const klingSecs = SHOT_IDS.map((id) => klingSeconds(frames(id)));
  const kling = estimateEpisode(doc, { plan: "kling:pro" });
  assert.equal(kling.plan.vendor, "kling");
  assert.equal(kling.plan.unverified, false, "the per-second price is the official user guide's");
  assert.equal(kling.plan.resolution, "1080p");
  assert.equal(kling.plan.credits_per_second, 8, "VIDEO 3.0 at 1080p without native audio");
  assert.match(kling.plan.credits_basis, /官方價目 2026-10-04（未實扣）/, "official, but no clip has been charged on the owner's account yet");
  assert.ok(kling.plan.notes.some((note) => /enable_audio false/.test(note) && /prefer_multi_shots false/.test(note)), "both Kling CLI defaults a shot must turn off are named");
  assert.ok(kling.plan.notes.some((note) => /輸出數/.test(note) && /設 1/.test(note)), "the outputs-per-generation setting multiplies credits and is named");
  assert.deepEqual(kling.plan.shots.map((shot) => shot.seconds), klingSecs);
  assert.equal(kling.plan.credits_one, sum(klingSecs) * 8);
  assert.equal(kling.plan.credits_cap, sum(klingSecs) * 8 * MAX_CLIP_TAKES);
  near4(kling.plan.share_one, (sum(klingSecs) * 8) / 3000);
  near4(kling.plan.usd_fee_one, (sum(klingSecs) * 8 * 37) / 3000);
  assert.equal(kling.plan.breakeven_seconds_monthly, Math.ceil(37 / 0.15));
  assert.equal(kling.plan.breakeven_seconds_first_month, Math.ceil(25.99 / 0.15));
  assert.equal(kling.plan.plan_seconds_per_month, Math.floor(3000 / 8));
  const kling720 = estimateEpisode(doc, { plan: "kling:pro", resolution: "720p" });
  assert.equal(kling720.plan.credits_one, sum(klingSecs) * 6);
  assert.equal(kling720.resolution, "720p", "720p is also an Omni resolution on the server side");
  assert.equal(estimateEpisode(doc, { plan: "kling:pro", creditsPerSecond: 10 }).plan.credits_one, sum(klingSecs) * 10);
  assert.equal(estimateEpisode(doc, { plan: "kling:pro", creditsPerSecond: 10 }).plan.credits_basis, "旗標");
  assert.throws(() => estimateEpisode(doc, { plan: "kling:gold" }), /unknown plan/);
});

test("levers: a later shot in an earlier clip's setup that fits is a cut, two short neighbours in one setup merge, a long shot is flagged", () => {
  const doc = dramaFixture();
  const farewell = doc.scenes.find((scene) => scene.id === "farewell");
  const storm = doc.scenes.find((scene) => scene.id === "sea-storm");
  const bird = doc.scenes.find((scene) => scene.id === "bird");
  const short = (scene) => { scene.lines = [{ id: scene.lines[0].id, text: "走。", speaker: "jingwei" }]; };
  short(farewell);
  short(bird);
  bird.data.camera = farewell.data.camera;
  bird.data.prompt = `${farewell.data.prompt.split(",")[0]}, later that day`;
  delete bird.data.start_frame;
  let report = estimateEpisode(doc);
  const cut = report.levers.cuts.find((each) => each.shot === "bird");
  assert.ok(cut, "bird is a cut candidate");
  assert.equal(cut.from_shot, "farewell");
  assert.equal(cut.from_s, Math.ceil(report.shots.find((shot) => shot.id === "farewell").frames / FPS), "the cut starts after the source shot's own lines");
  assert.equal(cut.repeats_frames, false);
  assert.ok(cut.from_s + cut.needed_s <= cut.room_s);
  assert.equal(cut.saving_usd, report.shots.find((shot) => shot.id === "bird").usd_one, "a cut buys nothing: the whole shot is saved");
  assert.equal(typeof cut.prompt_similarity, "number");
  assert.equal(cut.picture_differs, cut.prompt_similarity < 0.5, "the candidate compares only the setup; a different picture is flagged for a person to look at");
  assert.deepEqual(report.levers.merges, [], "farewell and bird are not neighbours");

  // sea-storm in farewell's setup and cast, both short: the two merge into one clip (and sea-storm could be cut too).
  short(storm);
  storm.data.camera = farewell.data.camera;
  storm.data.prompt = `${farewell.data.prompt.split(",")[0]}, the gate behind her`;
  storm.data.characters = [...farewell.data.characters];
  report = estimateEpisode(doc);
  const merge = report.levers.merges.find((each) => each.shots.join("+") === "farewell+sea-storm");
  assert.ok(merge, "farewell and sea-storm merge");
  assert.equal(merge.bought_separately_s, 8);
  assert.equal(merge.bought_merged_s, secondsBought(report.shots[1].frames + report.shots[2].frames, "gemini-omni-1.1-flash", "1080p"));
  near(merge.saving_usd, (8 - merge.bought_merged_s) * 0.15 + 0.134 + 0.02);
  assert.ok(report.levers.cuts.some((each) => each.shot === "sea-storm" && each.from_shot === "farewell"));

  // Under the production profile a cut must end inside eight seconds, and a long shot is a lint error.
  const long = dramaFixture();
  long.scenes[0].lines[0].text = "一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五";
  const flagged = estimateEpisode(long, { production: true });
  const entry = flagged.levers.long.find((each) => each.id === "opening");
  assert.ok(entry && entry.over_production && entry.over_clip, JSON.stringify(flagged.levers.long));
  assert.equal(flagged.verdict.ok, false);
  assert.match(flagged.verdict.problems.join("\n"), /opening 約 [\d.]+ 秒：production profile 一鏡最多 8 秒/);
  // The fixture as it is: two shots run past the 8 s craft target but inside the models' 10 s; without a profile that is a lever, not a verdict.
  const plain = estimateEpisode(dramaFixture());
  assert.deepEqual(plain.levers.long.map((each) => [each.id, each.over_production, each.over_clip]), [["opening", true, false], ["bird", true, false]]);
  assert.equal(plain.verdict.ok, true);
});

test("episode_estimate.mjs exits 0, 1 with --strict on a failed verdict, 2 on a file it cannot read, and prints JSON on request", () => {
  assert.equal(run("episode_estimate.mjs", DRAMA_FIXTURE_FILE).status, 0);
  const text = run("episode_estimate.mjs", DRAMA_FIXTURE_FILE, "--plan", "hailuo:pro");
  assert.equal(text.status, 0, text.stderr);
  assert.match(text.stdout, /方案 hailuo:pro/);
  assert.match(text.stdout, /H3 2k 12 credits\/s（實測 2026-10-04）/);
  assert.match(text.stdout, /損益平衡/);
  assert.match(text.stdout, /裁定：過/);
  const strict = run("episode_estimate.mjs", DRAMA_FIXTURE_FILE, "--strict", "--cap", "1");
  assert.equal(strict.status, 1);
  assert.match(strict.stdout, /裁定：不過/);
  const lite = run("episode_estimate.mjs", DRAMA_FIXTURE_FILE, "--strict", "--model", "veo-3.1-lite-generate-preview");
  assert.equal(lite.status, 0, "Lite with the preset's negative is supported by the adapter");
  assert.match(lite.stdout, /裁定：過/);
  assert.equal(run("episode_estimate.mjs", DRAMA_FIXTURE_FILE, "--cap", "1").status, 0, "without --strict a failed verdict is only printed");
  const json = run("episode_estimate.mjs", DRAMA_FIXTURE_FILE, "--json", "--plan", "kling:pro", "--credits-per-second", "10");
  assert.equal(json.status, 0, json.stderr);
  const parsed = JSON.parse(json.stdout);
  assert.equal(parsed.shots.length, 4);
  assert.equal(parsed.plan.vendor, "kling", "--plan kling:pro reaches the estimator through argv");
  assert.equal(parsed.plan.credits_per_second, 10);
  const hailuo = run("episode_estimate.mjs", DRAMA_FIXTURE_FILE, "--json", "--plan", "hailuo:pro");
  assert.equal(hailuo.status, 0, hailuo.stderr);
  assert.equal(JSON.parse(hailuo.stdout).plan.vendor, "hailuo", "--plan hailuo:pro reaches the estimator through argv");
  assert.equal(run("episode_estimate.mjs", path.join(ROOT, "nowhere.json")).status, 2);
  assert.equal(run("episode_estimate.mjs").status, 2);
  assert.equal(run("episode_estimate.mjs", DRAMA_FIXTURE_FILE, "--tier", "gold").status, 2);
});

test("preflight names the gate the next stage will refuse on, with the stage's exit code, and exits 1", async () => {
  const { box } = prepared();
  const result = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(result.next_paid, "clips", "look and keyframes are done in the prepared work directory");
  assert.equal(result.stage, "clips");
  assert.equal(result.gates.storyboard, "missing");
  assert.equal(result.gates.look, "missing");
  assert.ok(result.bindings.timeline.bound && result.bindings.keyframes.bound && result.bindings.characters.bound && !result.bindings.clips.present);
  const storyboard = result.findings.find((finding) => /storyboard/.test(finding.what));
  assert.ok(storyboard, JSON.stringify(result.findings));
  assert.equal(storyboard.level, "refuse");
  assert.equal(storyboard.exit, EXIT.owner);
  assert.deepEqual(result.new.clips, SHOT_IDS, "nothing is bought yet");
  assert.deepEqual(result.kept.keyframes, SHOT_IDS);
  assert.equal(result.judge.calls_one, 4);
  assert.equal(result.judge.calls_cap, 4 * MAX_CLIP_TAKES);
  assert.ok(result.findings.some((finding) => finding.level === "note" && /看不出伺服器會用哪個片段模型/.test(finding.what)));
  assert.equal(result.exit_code, 1);

  const keyframes = await preflight({ slug: box.slug, root: box.root, workdir: box.work, stage: "keyframes" });
  const look = keyframes.findings.find((finding) => /look 關卡/.test(finding.what));
  assert.equal(look?.level, "refuse");
  assert.equal(look?.exit, EXIT.owner);
  assert.deepEqual(keyframes.new.keyframes, [], "every keyframe is kept: a rerun buys nothing");

  // With both gates approved and nothing else wrong, clips would run: exit 0.
  await approveBoth(box);
  const clear = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(clear.exit_code, 0, JSON.stringify(clear.findings));
  assert.ok(clear.findings.every((finding) => finding.level === "note"));
  // A keyframes rerun now would only void the storyboard approval.
  const rerun = await preflight({ slug: box.slug, root: box.root, workdir: box.work, stage: "keyframes" });
  assert.equal(rerun.exit_code, 1);
  assert.ok(rerun.findings.some((finding) => finding.level === "waste" && /storyboard 核准作廢/.test(finding.fix)));
  // An edit to the script voids the keyframes binding: the preflight says what it re-buys.
  const file = path.join(box.dir, "video.json");
  const edited = JSON.parse(readFileSync(file, "utf8"));
  edited.scenes[0].data.prompt = `${edited.scenes[0].data.prompt}, a hawk overhead`;
  writeFileSync(file, JSON.stringify(edited));
  const after = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(after.stage, "keyframes");
  assert.equal(after.bindings.keyframes.bound, false);
  assert.deepEqual(after.new.keyframes, SHOT_IDS, "visual_hash covers every shot: the whole storyboard is redrawn");
  assert.ok(after.findings.some((finding) => /全部重買/.test(finding.what)));
  const cli = run("drama_preflight.mjs", "--slug", box.slug, "--root", box.root, "--workdir", box.work, "--stage", "clips");
  assert.equal(cli.status, 1, cli.stderr);
  assert.match(cli.stdout, /\[拒絕 exit 2\]/);
  assert.equal(run("drama_preflight.mjs", "--slug", "nowhere", "--root", box.root, "--workdir", box.work).status, 2);
  assert.equal(run("drama_preflight.mjs").status, 2);
});

test("preflight preserves Lite avoidance and approvals, flags real timing/keyframe limits and identifies external clips", async () => {
  const { box } = prepared();
  await approveBoth(box);
  const scriptBefore = readFileSync(path.join(box.dir, "video.json"));
  const approvalsBefore = readFileSync(path.join(box.workdir, "approvals.json"));
  const hashBefore = lookHash(JSON.parse(scriptBefore));
  assert.ok(resolveLook(JSON.parse(scriptBefore).look).negative.length > 0);
  const lite = await preflight({ slug: box.slug, root: box.root, workdir: box.work, model: "veo-3.1-lite-generate-preview" });
  assert.ok(!lite.findings.some((finding) => /HTTP 400/.test(finding.what)));
  assert.equal(lite.exit_code, 0, JSON.stringify(lite.findings));
  assert.equal(lite.gates.look, "approved");
  assert.equal(lite.gates.storyboard, "approved");
  assert.equal(lite.hashes.look, hashBefore);
  assert.deepEqual(readFileSync(path.join(box.dir, "video.json")), scriptBefore);
  assert.deepEqual(readFileSync(path.join(box.workdir, "approvals.json")), approvalsBefore);
  assert.equal(lite.clip_model, "veo-3.1-lite-generate-preview");
  const omni = await preflight({ slug: box.slug, root: box.root, workdir: box.work, model: "gemini-omni-1.1-flash" });
  assert.ok(!omni.findings.some((finding) => /HTTP 400/.test(finding.what)));
  assert.equal(omni.exit_code, 0);
  assert.ok(omni.findings.some((finding) => /gemini-omni-1\.1-flash/.test(finding.fix)), "the new clips are priced with the model");

  // The production profile: the fixture's freeze fit and long shots are lint errors (exit 1) and, past lint, refused by clips before any submission (exit 3).
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: { profile: { video: { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p" } } } }));
  const profile = await preflight({ slug: box.slug, root: box.root, workdir: box.work, stage: "clips" });
  const timing = profile.findings.find((finding) => /production profile 的時長規則/.test(finding.what));
  assert.equal(timing?.exit, EXIT.owner, JSON.stringify(profile.findings));
  assert.match(timing.what, /freeze/);
  assert.equal(profile.findings.find((finding) => /lint 錯誤/.test(finding.what))?.exit, EXIT.lint);
  assert.equal(profile.clip_model, "veo-3.1-lite-generate-preview", "the model comes from the profile");
  assert.ok(!profile.findings.some((finding) => /HTTP 400/.test(finding.what)), "the profile does not revive the resolved Lite failure");
  const picked = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(picked.stage, "clips", "with lint errors the next paid stage is still read from the manifests, not from status");

  // Clips use bounded questions with full appearance in context; keyframes still need a real length guard.
  const long = prepared((doc) => {
    doc.characters[0].shot_looks = [{ id: "present", appearance: `adult woman in a navy suit, ${"x".repeat(600)}` }];
    doc.scenes[1].data.character_looks = { jingwei: "present" };
  });
  await approveBoth(long.box);
  const longApprovals = readFileSync(path.join(long.box.workdir, "approvals.json"));
  const clips = await preflight({ slug: long.box.slug, root: long.box.root, workdir: long.box.work });
  assert.equal(clips.exit_code, 0, JSON.stringify(clips.findings));
  assert.ok(!clips.findings.some((finding) => new RegExp(`超過 ${MAX_RUBRIC_QUESTION} 字`).test(finding.what)));
  assert.equal(clips.gates.look, "approved");
  assert.equal(clips.gates.storyboard, "approved");
  assert.equal(clips.hashes.look, lookHash(long.doc));
  assert.deepEqual(readFileSync(path.join(long.box.workdir, "approvals.json")), longApprovals);
  // Only a keyframe that will actually be bought is checked. Make farewell genuinely missing.
  const manifestPath = path.join(long.box.workdir, "keyframes", "manifest.json");
  const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  delete manifest.shots.farewell;
  writeFileSync(manifestPath, JSON.stringify(manifest));
  const rubric = await preflight({ slug: long.box.slug, root: long.box.root, workdir: long.box.work, stage: "keyframes" });
  assert.deepEqual(rubric.new.keyframes, ["farewell"]);
  const question = rubric.findings.find((finding) => new RegExp(`超過 ${MAX_RUBRIC_QUESTION} 字`).test(finding.what));
  assert.ok(question, JSON.stringify(rubric.findings));
  assert.equal(question.level, "waste");
  assert.equal(question.exit, EXIT.external);
  assert.equal(rubric.exit_code, 1);
  assert.match(question.what, /farewell\/identity_jingwei/);

  // An mp4 put into clips/ by hand, with a manifest entry and no ledger job: kept, and named as external.
  const external = prepared();
  await approveBoth(external.box);
  writeFileSync(path.join(external.box.workdir, "clips", "opening-1.mp4"), MP4("hailuo clip"));
  writeClips(external.box, external.doc, external.timeline, { opening: { file: "clips/opening-1.mp4", sha256: SHA(MP4("hailuo clip")), seconds: 4, frames: 120, needed_s: 2.5, qc: { ok: true, metrics: {} }, judge: { overall: 8, passed: true }, needs_review: false } });
  const kept = await preflight({ slug: external.box.slug, root: external.box.root, workdir: external.box.work });
  assert.deepEqual(kept.external, ["opening"]);
  assert.deepEqual(kept.kept.clips, ["opening"]);
  assert.deepEqual(kept.new.clips, ["farewell", "sea-storm", "bird"]);
  const note = kept.findings.find((finding) => /不是這條線買的片段/.test(finding.what));
  assert.ok(note && note.level === "note" && /opening/.test(note.what));
  assert.match(note.fix, /qc\.mjs/, "assemble does not run the black, freeze and cut filters: the note says to run them by hand");
  assert.equal(kept.exit_code, 0);
  const assemble = await preflight({ slug: external.box.slug, root: external.box.root, workdir: external.box.work, stage: "assemble" });
  const assembleNote = assemble.findings.find((finding) => new RegExp(`PSNR（≥ ${KEYFRAME_MIN_PSNR}`).test(finding.what));
  assert.ok(assembleNote);
  assert.match(assembleNote.what, /assemble 不查/);
  assert.ok(assemble.findings.some((finding) => finding.level === "refuse" && /frames\/manifest\.json/.test(finding.what)), "render has not run");

  // The same clip brought in by `clips import` is named as imported, and nothing asks for its checks to be run by hand.
  assert.deepEqual(kept.imported, []);
  const clipsFile = path.join(external.box.workdir, "clips", "manifest.json");
  const saved = JSON.parse(readFileSync(clipsFile, "utf8"));
  Object.assign(saved.shots.opening, { provider: "hailuo-web", plan: "pro", credits: 60, imported_at: "2026-10-04T00:00:00.000Z" });
  writeFileSync(clipsFile, JSON.stringify(saved));
  const brought = await preflight({ slug: external.box.slug, root: external.box.root, workdir: external.box.work });
  assert.deepEqual([brought.external, brought.imported, brought.kept.clips], [["opening"], ["opening"], ["opening"]]);
  assert.ok(brought.findings.some((finding) => finding.level === "note" && /clips import 匯入的片段：opening/.test(finding.what)));
  assert.ok(!brought.findings.some((finding) => /不是這條線買的片段/.test(finding.what)));
});

test("the run report adds the ledger up by kind and stage, reads takes and utilisation, and counts the five statuses apart", async () => {
  const { box, doc, timeline } = prepared();
  const at = "2026-10-03T09:00:00.000Z";
  const image = (id) => ({ at, stage: "keyframes", kind: "image", id, provider: "gemini", model: "gemini-3-pro-image", key: `k-${id}`, job_id: `img-${id}`, seconds: 0, cost_usd: 0.134, status: "ready" });
  const judge = (stage, id) => ({ at, stage, kind: "judge", id, provider: "gemini", model: "gemini-judge", key: null, cost_usd: 0.01, status: "judged" });
  const clip = (id, job, seconds) => ({ at, stage: "clips", kind: "clip", id, provider: "gemini", model: "gemini-omni-1.1-flash", key: `c-${job}`, job_id: job, seconds, cost_usd: seconds * 0.15, status: "ready" });
  const entries = [
    ...SHOT_IDS.map(image),
    ...SHOT_IDS.map((id) => judge("keyframes", id)),
    clip("farewell", "jc1", 8), clip("farewell", "jc2", 8), clip("sea-storm", "jc3", 6), clip("sea-storm", "jc4", 6),
    judge("clips", "farewell"), judge("clips", "farewell"), judge("clips", "sea-storm"), judge("clips", "sea-storm"),
    { at, stage: "clips", kind: "clip", id: "bird", provider: "gemini", model: "gemini-omni-1.1-flash", source: { shot: "sea-storm", from_s: 1 }, saved_seconds: 4, saved_usd: 0.6, status: "cut", seconds: 0, cost_usd: 0 },
    { at, stage: "music", kind: "music", id: "music", provider: "gemini", model: "lyria-3.5", key: "m1", job_id: "mu1", seconds: 30, cost_usd: 0.08, status: "ready" },
  ];
  mkdirSync(path.join(box.workdir, "media"), { recursive: true });
  writeFileSync(path.join(box.workdir, "media", "ledger.json"), JSON.stringify({ entries, totals: {} }));
  writeFileSync(path.join(box.workdir, "clips", "opening-ext.mp4"), MP4("external"));
  writeClips(box, doc, timeline, {
    opening: { file: "clips/opening-ext.mp4", sha256: SHA(MP4("external")), seconds: 4, frames: 120, needed_s: 2, provider: "external", qc: { ok: true }, needs_review: false },
    farewell: { file: "clips/farewell-2.mp4", sha256: "f".repeat(64), seconds: 8, frames: 240, needed_s: 6.4, qc: { ok: true }, judge: { overall: 8, passed: true }, takes: [{ seed: 1, qc: { ok: false, problems: ["judge 4/10: the beard morphs"] }, judge: { overall: 4, passed: false } }, { seed: 2, qc: { ok: true }, judge: { overall: 8, passed: true } }], needs_review: false },
    "sea-storm": { file: "clips/sea-storm-2.mp4", sha256: "e".repeat(64), seconds: 6, frames: 180, needed_s: 3, qc: { ok: false }, judge: { overall: 8, passed: true }, takes: [{ seed: 1, qc: { ok: false, problems: ["black from 0.50 s to 1.20 s"] }, judge: { overall: 8, passed: true } }, { seed: 2, qc: { ok: false, problems: ["black from 0.50 s to 1.20 s"] }, judge: { overall: 8, passed: true } }], needs_review: true, problems: ["black from 0.50 s to 1.20 s"] },
    bird: { source: { shot: "sea-storm", from_s: 1, from_frame: 30 }, file: "clips/sea-storm-2.mp4", sha256: "e".repeat(64), seconds: 6, frames: 180, needed_s: 4, needs_review: false },
  });
  writeFileSync(path.join(box.workdir, "state.json"), JSON.stringify({ runs: [{ stage: "keyframes", at, shots: 4, generated: 4, seconds: 120 }, { stage: "clips", at, generated: 3, seconds: 500 }, { stage: "clips", at, generated: 1, seconds: 100 }] }));
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });

  const report = await runReport({ slug: box.slug, root: box.root, workdir: box.work });
  near(report.totals.usd, 4 * 0.134 + 8 * 0.01 + 28 * 0.15 + 0.08);
  assert.equal(report.totals.clip_seconds, 28, "every take bought counts, the cut does not");
  assert.equal(report.totals.judge_calls, 8);
  assert.deepEqual(report.spend.by_kind.clip, { count: 4, usd: 4.2, seconds: 28 });
  assert.equal(report.spend.by_kind.image.count, 4);
  near(report.spend.by_stage.keyframes.usd, 4 * 0.134 + 4 * 0.01);
  assert.equal(report.spend.by_stage.clips.judge_calls, 4);
  near(report.spend.by_stage.music.usd, 0.08);
  assert.equal(report.spend.failed.count, 0);
  const takes = Object.fromEntries(report.takes.map((take) => [`${take.stage}/${take.id}`, take]));
  assert.deepEqual([takes["clips/farewell"].takes, takes["clips/farewell"].passed], [2, 1]);
  assert.deepEqual([takes["clips/sea-storm"].takes, takes["clips/sea-storm"].passed, takes["clips/sea-storm"].needs_review], [2, 0, true]);
  assert.deepEqual([takes["keyframes/opening"].takes, takes["keyframes/opening"].passed], [1, 1]);
  assert.equal(takes["clips/bird"], undefined, "a cut has no takes of its own");
  const use = Object.fromEntries(report.utilisation.shots.map((shot) => [shot.id, shot]));
  assert.deepEqual([use.opening.utilisation, use.farewell.utilisation, use["sea-storm"].utilisation], [0.5, 0.8, 0.5]);
  assert.equal(use.opening.external, true);
  near(report.utilisation.needed_s, 11.4);
  assert.equal(report.utilisation.adopted_s, 18);
  near4(report.utilisation.overall_adopted, 11.4 / 18);
  near4(report.utilisation.needed_booked_s, 9.4, "the external clip's need is outside the ledger ratio");
  near4(report.utilisation.overall_bought, 9.4 / 28);
  assert.deepEqual(report.waste, { images_bought: 4, images_used: 4, clip_seconds_bought: 28, clip_seconds_used: 14 });
  assert.deepEqual([report.cuts.cuts, report.cuts.clip_seconds, report.cuts.usd], [1, 4, 0.6]);
  assert.deepEqual(report.external.map((each) => each.id), ["opening"]);
  assert.equal(report.judge.calls, 8);
  assert.deepEqual(report.judge.by_stage, { keyframes: 4, clips: 4 });
  assert.deepEqual(report.bought.clips, { count: 4, seconds: 28, usd: 4.2 });
  assert.deepEqual(report.bought.keyframes, { count: 4, end_frames: 0, usd: 0.536 });
  assert.deepEqual(report.status.clips, { shots: 3, job_ready: 2, qc_ok: 2, judge_passed: 2, needs_review: 1, owner_accepted: 0 });
  assert.deepEqual(report.status.keyframes, { shots: 4, job_ready: 4, qc_ok: null, judge_passed: 4, needs_review: 0, owner_accepted: 4 });
  assert.deepEqual(report.status.characters, { shots: 2, job_ready: 0, qc_ok: null, judge_passed: 2, needs_review: 0, owner_accepted: 0 }, "the sheets were never booked in this ledger; the look gate is not approved");
  assert.deepEqual(report.retakes.map((retake) => [retake.stage, retake.id, retake.take]), [["clips", "farewell", 1], ["clips", "sea-storm", 1], ["clips", "sea-storm", 2]]);
  assert.deepEqual(report.stale, []);
  assert.deepEqual(report.wallclock.clips, { runs: 2, seconds: 600, first_at: at, last_at: at, generated: 4 });
  assert.equal(report.wallclock.keyframes.seconds, 120);
  assert.deepEqual(report.needs_review.map((take) => take.id), ["sea-storm"]);

  const markdown = renderMarkdown(report, new Date(at));
  assert.match(markdown, /^# fixture-drama post-mortem（2026-10-03）/);
  assert.match(markdown, /\| 素材 \| 4 \| 28 秒 \| 4\.20 \| not_available \| not_available \|/);
  assert.match(markdown, /\| judge \| 8 \| 次 \| 0\.01 × 8 = 0\.08 \|/);
  assert.match(markdown, /\| 外部片段 \| 1 \| 1 支／4 秒 \|/);
  assert.match(markdown, /\| job ready \| 0 \| 4 \| 2 \|/);
  assert.match(markdown, /\| QC ok（ffmpeg） \| — \| — \| 2 \|/);
  assert.match(markdown, /\| needs_review \| 0 \| 0 \| 1 \|/);
  assert.match(markdown, /\| 站主 accepted（關卡） \| look: missing 0 \| storyboard: approved 4 \| final: absent 0 \|/);
  assert.match(markdown, /整集 63%（採用的 take）／34%（全部買到，不含外部）；切鏡省下 4 秒／US\$0\.60/);
  assert.match(markdown, /- 買了沒用的：圖 4 買、4 用；素材 28 秒買、14 秒採用/);
  assert.match(markdown, /\| clips\/sea-storm \| 1 \| black from 0\.50 s to 1\.20 s \| \| \| \|/);
  assert.match(markdown, /\| clips\/farewell \| 1 \| judge 4\/10: the beard morphs \| \| \| \|/);
  assert.match(markdown, /\| storyboard \| approved \|\s+\|/);
  assert.match(markdown, /\| clips \| 2 \| 600 \| not_available \|/);
  assert.match(markdown, /- clips sea-storm（2 take）：black from 0\.50 s to 1\.20 s/);
  assert.match(markdown, /## 下次改什麼（可驗證的，一條一個變數）/);

  // The storyboard approval goes stale once the manifest is rewritten: the accepted count drops to zero.
  const manifest = JSON.parse(readFileSync(path.join(box.workdir, "keyframes", "manifest.json"), "utf8"));
  manifest.generated_at = at;
  writeFileSync(path.join(box.workdir, "keyframes", "manifest.json"), JSON.stringify(manifest));
  const stale = await runReport({ slug: box.slug, root: box.root, workdir: box.work });
  assert.deepEqual(stale.stale, ["storyboard"]);
  assert.equal(stale.status.keyframes.owner_accepted, 0);
  assert.match(renderMarkdown(stale), /\| storyboard \| stale \| （人填：核准後改了什麼） \|/);

  const cli = run("run_report.mjs", "--slug", box.slug, "--root", box.root, "--workdir", box.work, "--markdown");
  assert.equal(cli.status, 0, cli.stderr);
  assert.match(cli.stdout, /# fixture-drama post-mortem（/);
  const text = run("run_report.mjs", "--slug", box.slug, "--root", box.root, "--workdir", box.work);
  assert.equal(text.status, 0, text.stderr);
  assert.match(text.stdout, /外部片段（clips import 匯入的，或手放、ledger 沒有它的 job）：opening（clips\/opening-ext\.mp4，4 s，手放）/);
  const json = run("run_report.mjs", "--slug", box.slug, "--root", box.root, "--workdir", box.work, "--json");
  assert.equal(JSON.parse(json.stdout).status.clips.needs_review, 1);
  assert.equal(run("run_report.mjs", "--slug", "nowhere", "--root", box.root, "--workdir", box.work).status, 2);
  assert.equal(run("run_report.mjs").status, 2);

  // The same clip brought in by `clips import`: the ledger books it, apart from what the line bought.
  const clipsFile = path.join(box.workdir, "clips", "manifest.json");
  const saved = JSON.parse(readFileSync(clipsFile, "utf8"));
  Object.assign(saved.shots.opening, { provider: "hailuo-web", plan: "pro", credits: 60, imported_at: at });
  writeFileSync(clipsFile, JSON.stringify(saved));
  writeFileSync(path.join(box.workdir, "media", "ledger.json"), JSON.stringify({ entries: [...entries, { at, stage: "clips", kind: "clip", id: "opening", provider: "hailuo-web", plan: "pro", credits: 60, seconds: 4, cost_usd: 0.5, file: "clips/opening-ext.mp4", sha256: SHA(MP4("external")), status: "imported" }], totals: {} }));
  const brought = await runReport({ slug: box.slug, root: box.root, workdir: box.work });
  assert.deepEqual(brought.imported, { clips: 1, clip_seconds: 4, credits: 60, usd: 0.5 });
  assert.equal(brought.totals.clip_seconds, 32, "the ledger's total counts the imported seconds");
  assert.deepEqual(brought.bought.clips, { count: 4, seconds: 28, usd: 4.2 }, "what the line bought does not");
  assert.deepEqual(brought.spend.by_kind.clip, { count: 4, usd: 4.2, seconds: 28 });
  assert.deepEqual([brought.utilisation.ledger_s, brought.waste.clip_seconds_bought], [28, 28]);
  assert.deepEqual(brought.external, [{ id: "opening", file: "clips/opening-ext.mp4", seconds: 4, provider: "hailuo-web", route: "hailuo-web", plan: "pro", credits: 60, imported: true }]);
  assert.match(renderMarkdown(brought, new Date(at)), /\| 外部片段 \| 1 \| 1 支／4 秒 \| 0\.50（方案點數：60 點，方案 pro） \| — \| — \|/);
});

// Delivery promise and continuity locks (OpenMontage's and the drama-skills / shuohao-skills packs' names; the idea only).
test("preflight refuses a promised clip that quietly became a still, a cut or a freeze, and a locked string that left the prompt, until a change order against the lock names it", async () => {
  const { box, doc, timeline } = prepared();
  await approveBoth(box);
  const file = path.join(box.dir, "video.json");
  const lock = lockShots(box, doc, timeline);
  assert.equal(lock.shots["sea-storm"].promise.fit, "freeze", "the fixture's sea-storm was promised with its freeze fit");
  assert.deepEqual(lock.shots.bird.continuity.depends_on, ["sea-storm"], "bird continues from sea-storm's last frame");
  assert.deepEqual(lock.shots.opening.continuity.locks.time_of_day, ["dawn"]);
  const clear = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(clear.exit_code, 0, JSON.stringify(clear.findings));
  assert.deepEqual(clear.lock.broken, { promise: [], continuity: [] });
  assert.ok(!clear.findings.some((finding) => finding.id), "a kept promise says nothing");

  // farewell becomes a still: refused with the lint code at whatever stage comes next.
  const edit = (change) => { const current = JSON.parse(readFileSync(file, "utf8")); change(current); writeFileSync(file, JSON.stringify(current)); };
  edit((current) => { current.scenes[1].data.visual = "still"; });
  const still = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  const broken = still.findings.find((finding) => finding.id === "promise.broken");
  assert.ok(broken, JSON.stringify(still.findings));
  assert.equal(broken.level, "refuse");
  assert.equal(broken.exit, EXIT.lint);
  assert.match(broken.what, /^farewell 鎖定時答應的是 clip（買 \d+ s，server），現在是 still，沒有變更單$/);
  assert.match(broken.fix, /--accept --note/);
  assert.deepEqual(still.lock.broken.promise, ["farewell"]);
  assert.equal(still.exit_code, 1);
  const cli = run("drama_preflight.mjs", "--slug", box.slug, "--root", box.root, "--workdir", box.work);
  assert.equal(cli.status, 1, cli.stderr);
  assert.match(cli.stdout, /開拍鎖定 2026-10-05T00:00:00\.000Z：承諾改小 沒變更單 1／有 0；連戲字少了 沒變更單 0／有 0/);
  assert.match(cli.stdout, /\[拒絕 exit 1\] farewell 鎖定時答應的是 clip/);

  // The owner's word, recorded by plan_lock --accept against this lock, lets it through as a note.
  const accepted = spawnSync(process.execPath, [PLAN_LOCK, "--slug", box.slug, "--root", box.root, "--workdir", box.work, "--accept", "--note", "站主：farewell 改 still"], { encoding: "utf8", env: { ...process.env, VIDEO_MIN_EPISODE_MINUTES: "0" } });
  assert.equal(accepted.status, 0, accepted.stderr);
  const signed = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(signed.exit_code, 0, JSON.stringify(signed.findings));
  assert.deepEqual([signed.lock.broken.promise, signed.lock.signed.promise], [[], ["farewell"]]);
  assert.match(signed.findings.find((finding) => finding.id === "promise.signed").what, /有站主點頭的變更單（.*：站主：farewell 改 still）/);

  // A freeze fit on a clip promised without one, and a time of day that left the prompt, are each refused on their own; the order above covers neither.
  edit((current) => { current.scenes[1].data.visual = "clip"; current.scenes[0].data.fit = "freeze"; current.scenes[0].data.prompt = current.scenes[0].data.prompt.replace("at dawn", "at dusk"); });
  const twice = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.deepEqual(twice.findings.filter((finding) => finding.level === "refuse").map((finding) => finding.id), ["promise.broken", "continuity.broken"], JSON.stringify(twice.findings));
  assert.match(twice.findings.find((finding) => finding.id === "promise.broken").what, /^opening .*現在 fit 是 freeze（鎖定時 auto），沒有變更單$/);
  assert.match(twice.findings.find((finding) => finding.id === "continuity.broken").what, /^opening 鎖住的連戲字不在 prompt 裡了：時刻「dawn」，沒有變更單$/);
  assert.equal(twice.exit_code, 1);
  assert.deepEqual(twice.lock.broken, { promise: ["opening"], continuity: ["opening"] });

  // A cut from another shot is a kind change too; an old lock is only a note and checks nothing.
  edit((current) => { current.scenes[0].data.fit = "auto"; current.scenes[0].data.prompt = current.scenes[0].data.prompt.replace("at dusk", "at dawn"); current.scenes[3].data = { ...current.scenes[2].data, source: { shot: "sea-storm", from_s: 1 } }; delete current.scenes[3].data.fit; });
  const cut = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.match(cut.findings.find((finding) => finding.id === "promise.broken")?.what ?? "", /^bird .*現在是切素材（source），沒有變更單$/);
  writeFileSync(path.join(box.workdir, "plan", "lock.json"), JSON.stringify({ ...lock, version: 2 }));
  const old = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.ok(old.findings.some((finding) => finding.level === "note" && /lock\.json.*version 2/.test(finding.what)), JSON.stringify(old.findings));
  assert.ok(!old.findings.some((finding) => finding.id));
  assert.equal(old.lock.problem !== null, true);
});

test("the run report sets each shot's promise against what was delivered and what the ledger spent, and marks a downgrade nobody signed", async () => {
  const { box, doc, timeline } = prepared();
  const lock = lockShots(box, doc, timeline);
  const at = "2026-10-05T02:00:00.000Z";
  const bought = lock.shots.farewell.buy_s;
  const price = (seconds) => Math.round(seconds * 0.15 * 100) / 100;
  const clip = (id, job, seconds) => ({ at, stage: "clips", kind: "clip", id, provider: "gemini", model: "gemini-omni-1.1-flash", key: `c-${job}`, job_id: job, seconds, cost_usd: price(seconds), status: "ready" });
  mkdirSync(path.join(box.workdir, "media"), { recursive: true });
  writeFileSync(path.join(box.workdir, "media", "ledger.json"), JSON.stringify({ entries: [clip("farewell", "j1", bought), clip("farewell", "j2", bought)], totals: {} }));
  writeClips(box, doc, timeline, {
    farewell: { file: "clips/farewell-2.mp4", sha256: "f".repeat(64), seconds: bought, frames: bought * 30, needed_s: 6, qc: { ok: true }, needs_review: false },
    "sea-storm": { still: true, file: "keyframes/sea-storm-1.png", sha256: "e".repeat(64) },
  });
  const report = await runReport({ slug: box.slug, root: box.root, workdir: box.work });
  const shots = Object.fromEntries(report.promises.shots.map((shot) => [shot.id, shot]));
  assert.deepEqual([report.promises.unit, report.promises.lock, report.promises.route], ["usd", lock.created_at, "server"]);
  assert.deepEqual([shots.farewell.kept, shots.farewell.change, shots.farewell.delivered.kind, shots.farewell.delivered.external, shots.farewell.spent.jobs], [true, null, "clip", false, 2]);
  near4(shots.farewell.delta, 2 * price(bought) - lock.shots.farewell.cost.one, "two takes against the one promised");
  assert.deepEqual([shots["sea-storm"].kept, shots["sea-storm"].change, shots["sea-storm"].signed, shots["sea-storm"].delivered.kind], [false, "downgrade", false, "still"], "a still delivered on a promised clip, and nobody signed");
  near4(shots["sea-storm"].delta, -lock.shots["sea-storm"].cost.one, "the promised clip's price was saved");
  assert.deepEqual([shots.bird.delivered, shots.bird.kept, shots.bird.change], [null, true, null], "not made yet: the promise stands as the script stands");
  assert.deepEqual([report.promises.totals.kept, report.promises.totals.downgraded, report.promises.totals.unsigned, report.promises.totals.upgraded, report.promises.totals.pending], [3, 1, 1, 0, 2]);
  near4(report.promises.totals.promised_one, lock.totals.clip.one);
  near4(report.promises.totals.spent, 2 * price(bought));
  near4(report.promises.totals.delta, 2 * price(bought) - lock.totals.clip.one);
  assert.deepEqual(report.promises.orders, { accepted: 0, settled: 0 });
  const text = renderReport(report);
  assert.ok(text.includes(`sea-storm    承諾 clip ${lock.shots["sea-storm"].buy_s} s fit freeze → still；花 0（0 筆），差 -${lock.shots["sea-storm"].cost.one}；改小（沒簽變更單）`), text);
  assert.ok(text.includes(`farewell     承諾 clip ${bought} s → clip ${bought} s；花 ${2 * price(bought)}（2 筆），差 +${price(bought)}；守住`), text);
  const markdown = renderMarkdown(report, new Date(at));
  assert.match(markdown, /## 承諾與交付（plan\/lock\.json）/);
  assert.ok(markdown.includes(`| farewell | clip ${bought} s（server） | clip ${bought} s | ${2 * price(bought)} | +${price(bought)} | 守住 |`), markdown);
  assert.ok(markdown.includes("| bird | clip"), "a shot not made yet is still a row");
  const cli = run("run_report.mjs", "--slug", box.slug, "--root", box.root, "--workdir", box.work, "--json");
  assert.equal(cli.status, 0, cli.stderr);
  assert.equal(JSON.parse(cli.stdout).promises.totals.unsigned, 1);
  const empty = sandbox("fixture-drama", "drama");
  mkdirSync(empty.workdir, { recursive: true });
  assert.equal((await runReport({ slug: empty.slug, root: empty.root, workdir: empty.work })).promises, null, "no lock package: nothing was promised");
});

test("an empty work directory reports zero spend and no takes instead of failing", async () => {
  const box = sandbox("fixture-drama", "drama");
  mkdirSync(box.workdir, { recursive: true });
  const report = await runReport({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(report.totals.usd, 0);
  assert.deepEqual(report.takes, []);
  assert.equal(report.utilisation.overall_adopted, null);
  assert.deepEqual(report.status.clips, { shots: 0, job_ready: 0, qc_ok: 0, judge_passed: 0, needs_review: 0, owner_accepted: 0 });
  assert.deepEqual(report.status.characters, { shots: 0, job_ready: 0, qc_ok: null, judge_passed: 0, needs_review: 0, owner_accepted: 0 });
  assert.deepEqual(report.retakes, []);
  assert.match(renderMarkdown(report), /\| （沒有退回的 take） \|/);
  assert.match(renderMarkdown(report), /\| 全部 \| — \| not_available \| not_available \|/);
  const result = await preflight({ slug: box.slug, root: box.root, workdir: box.work });
  assert.equal(result.stage, "look", "nothing is made yet: the look comes first");
  assert.equal(result.exit_code, 0, JSON.stringify(result.findings));
  assert.deepEqual(result.new.characters, ["jingwei", "yandi"]);
  assert.equal(result.judge.calls_one, 6);
});
