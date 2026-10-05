/**
 * The three scripts the animation-preproduction skill ships
 * (.agents/skills/animation-preproduction/scripts/): the shot list and spec sheet, the lock and
 * change order, and the animatic.
 *
 * Pinned here: the risk table in references/shot-risk.md is the script's RISK_RULES row by row
 * (id, grade, what it applies to); each rule fires on the case it was written for and not on the
 * false friends found while writing it (a hair cord, an arc that leaves the frame, an eyes-only
 * close-up); the seconds bought per route follow the route's own range plus the tail handle and
 * a master shot covers the cuts taken from it; the web prompt uses Hailuo's bracket commands and
 * Kling's camera phrases with the pan direction kept; a production profile refuses a web route;
 * the lock notices a one-word change of motion (which the image model never reads but visualHash
 * covers) and names the approvals it stales; the animatic keeps the timeline's length and cannot
 * be broken out of its script block by a line of dialogue.
 */
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { DRAMA_FIXTURE_FILE, dramaFixture } from "./video/core/fixtures/load.mjs";
import { clipPrompt } from "./video/media/clips.mjs";
import { resolveLook, shotCast } from "./video/core/drama.mjs";
import { estimateTimeline, FPS } from "./video/core/timeline.mjs";
import { PLANS, secondsBought } from "../.agents/skills/animation-production/scripts/episode_estimate.mjs";
import {
  continuityTerms,
  DEFAULT_HANDLE_S,
  EXPECTED_TAKES,
  HAILUO_CLIP_SECONDS,
  planEpisode,
  renderCsv,
  renderMarkdown,
  RISK_RULES,
  shotRisk,
  webMove,
  webPrompt,
  H3_FIRST_LINE,
  HAILUO_MODELS,
  expectedTakesFlag,
} from "../.agents/skills/animation-preproduction/scripts/shot_plan.mjs";
import { changeOrderLine, compareLock, continuityBreaks, coveringOrder, lockOf, promiseBreaks, renderChangeOrder, shotPrints } from "../.agents/skills/animation-preproduction/scripts/plan_lock.mjs";
import { animaticFfmpegArgs, animaticHtml, animaticShots, animaticStats } from "../.agents/skills/animation-preproduction/scripts/animatic.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const SKILL = path.join(ROOT, ".agents", "skills", "animation-preproduction");
const SCRIPTS = path.join(SKILL, "scripts");
const EXAMPLE = path.join(ROOT, ".agents", "skills", "animation-camera", "references", "budaimiao-example.json");
const example = () => JSON.parse(readFileSync(EXAMPLE, "utf8"));
const run = (script, ...args) => spawnSync(process.execPath, [path.join(SCRIPTS, script), ...args], { encoding: "utf8" });
const box = () => mkdtempSync(path.join(tmpdir(), "preproduction-"));

const ctxOf = (change = {}) => ({ characters: 1, names: ["ayu", "chen", "ye", "yue", "shen", "lu"], face: false, speakerVisible: false, camera: "", moves: 0, buySeconds: 4, clipTakes: 2, ...change });
const ids = (risk) => risk.reasons.map((reason) => reason.id);

test("the risk table in shot-risk.md is RISK_RULES, row by row", () => {
  const text = readFileSync(path.join(SKILL, "references", "shot-risk.md"), "utf8");
  const table = text.slice(text.indexOf("## 風險表"));
  const rows = [...table.matchAll(/^\| `([a-z.-]+)` \| ([ABC]) \| (clip|image) \|/gm)].map((match) => [match[1], match[2], match[3]]);
  assert.deepEqual(rows, RISK_RULES.map((rule) => [rule.id, rule.grade, rule.applies]));
  for (const rule of RISK_RULES) assert.ok(rule.why && rule.redesign, `${rule.id} explains itself and how to design around it`);
  assert.deepEqual(EXPECTED_TAKES, { A: 1.2, B: 1.5, C: 2 });
});

test("each risk fires on the case it was written for and not on its false friends", () => {
  const pen = shotRisk({ prompt: "Insert of her right hand over the contract", motion: "Her right hand lifts the pen off the paper" }, "clip", ctxOf());
  assert.equal(pen.grade, "C");
  assert.deepEqual(ids(pen), ["hands.small-prop"]);
  assert.equal(pen.expected_takes, EXPECTED_TAKES.C);
  assert.deepEqual(ids(shotRisk({ prompt: "Extreme close-up of Shen's open eyes, one jade hair cord at the upper left edge", motion: "Shen narrows her eyes, then steadies her gaze" }, "clip", ctxOf())), [], "a hair cord with no hand is not a small prop in a hand");
  assert.deepEqual(ids(shotRisk({ prompt: "Medium close-up of Shen", motion: "One cyan arc travels toward screen right and leaves the frame" }, "clip", ctxOf())), [], "an arc leaving the frame is not a person entering");
  assert.deepEqual(ids(shotRisk({ prompt: "Wide shot of the hall", motion: "Ayu enters through the door on screen left" }, "clip", ctxOf())), ["entrance"]);
  assert.deepEqual(ids(shotRisk({ prompt: "Insert of the staff band, a narrow cyan arc entering from frame left", motion: "The arc strikes the band once" }, "clip", ctxOf({ characters: 0 }))), [], "an arc entering the frame is not a person");
  assert.deepEqual(ids(shotRisk({ prompt: "Two-shot", motion: "Chen grabs Ayu's wrist" }, "clip", ctxOf({ characters: 2 }))), ["contact.two-person"]);
  assert.deepEqual(ids(shotRisk({ prompt: "Medium close-up", motion: "Chen grabs the rail" }, "clip", ctxOf({ characters: 1 }))), [], "one person grabbing a rail is not two people touching");
  assert.deepEqual(ids(shotRisk({ prompt: "Medium close-up of Lu", motion: "Lu lowers his staff" }, "clip", ctxOf({ face: true, speakerVisible: true }))), ["speech.visible-mouth"]);
  assert.deepEqual(ids(shotRisk({ prompt: "A signboard reads \"Open\" above the door", motion: "Wind moves the sign" }, "still", ctxOf())), ["text.readable"], "a still is checked for what the picture model has to draw");
  assert.deepEqual(ids(shotRisk({ prompt: "Wide", motion: "Guests turn" }, "clip", ctxOf({ buySeconds: 9 }))), ["long.take"]);
  assert.deepEqual(ids(shotRisk({ prompt: "Wide", motion: "She waits" }, "clip", ctxOf({ camera: "wide shot, slow orbit" }))), ["camera.complex"]);
  assert.deepEqual(shotRisk({ prompt: "x", motion: "y" }, "cut", ctxOf()), { grade: "A", reasons: [], expected_takes: 0 }, "a cut buys nothing");
});

// The review of 2026-10-04 (forward use on an original fight scene) found the first rules misread fight wording.
test("fight wording: thrusts and slashes at the other person are contact, a weapon in a hand is a weapon, anchors and effects are not props", () => {
  const two = ctxOf({ characters: 2 });
  assert.deepEqual(ids(shotRisk({ prompt: "Two-shot", motion: "Yue thrusts the spear toward Ye's chest and she twists her torso aside" }, "clip", two)), ["contact.two-person"]);
  assert.deepEqual(ids(shotRisk({ prompt: "Two-shot", motion: "Ye's saber slashes down onto the spear shaft once" }, "clip", two)), ["contact.two-person"]);
  assert.deepEqual(ids(shotRisk({ prompt: "Two-shot", motion: "The single cyan arc strikes the central bronze band of Lu's horizontal staff once" }, "clip", two)), ["contact.two-person"], "an energy strike on the other person's weapon still touches them");
  assert.deepEqual(ids(shotRisk({ prompt: "Two-shot", motion: "Shen lowers her sword twenty centimetres; Lu holds his guard" }, "clip", two)), [], "two people in frame without touching");
  assert.deepEqual(ids(shotRisk({ prompt: "Insert of the hilt", motion: "The right hand raises the single sword hilt twenty centimetres and stops" }, "clip", ctxOf({ characters: 0 }))), ["hands.weapon"]);
  assert.deepEqual(ids(shotRisk({ prompt: "Medium shot of Ye, one jade hair cord, her right hand at her side", motion: "Ye lifts her chin toward screen right and stops" }, "clip", ctxOf())), [], "the anchors the style asks for (hair cords, cuffs) are not props in a hand");
  assert.deepEqual(ids(shotRisk({ prompt: "Medium shot", motion: "She pours tea into the cup" }, "clip", ctxOf())), ["hands.small-prop", "physics.fluid"], "pouring tea needs no hand word");
  for (const motion of ["The horse stands stable in the stable", "He leans on the drawer under pressure", "A panoramic chasm opens below", "Lightning strikes the far peak", "Fire and smoke roll across the plain"]) {
    assert.deepEqual(ids(shotRisk({ prompt: "Wide", motion }, "clip", ctxOf())), [], motion);
  }
  assert.deepEqual(ids(shotRisk({ prompt: "Wide", motion: "Ayu enters through the door on screen left" }, "clip", ctxOf())), ["entrance"]);
  assert.deepEqual(ids(shotRisk({ prompt: "Wide", motion: "The spear head enters from frame right" }, "clip", ctxOf())), [], "a spear head entering is not a person");
  const capped = shotRisk({ prompt: "Insert", motion: "Her right hand lifts the pen off the paper" }, "clip", ctxOf({ clipTakes: 1 }));
  assert.equal(capped.expected_takes, 1, "the expected takes never exceed the take limit");
});

test("the camera line becomes H3's camera sentence, Hailuo 2.3's bracket command and Kling's phrase, with the pan direction of the camera", () => {
  assert.deepEqual(webMove("Two-shot, eye level, locked"), { group: "locked", slow: false, unsupported: null, h3: "The camera is a static shot and stays completely still", hailuo: "[Static shot]", kling: "locked-off camera, no camera movement" });
  assert.equal(webMove("Wide shot, pan left").h3, "The camera pans left at a steady speed", "a move always carries a speed in the H3 sentence");
  assert.deepEqual([webMove("Wide shot, slow pan").group, webMove("Wide shot, slow pan").unsupported], [null, "pan"], "a pan with no direction is not guessed as a drift");
  assert.deepEqual([webMove("Wide shot, orbit").group, webMove("Wide shot, orbit").unsupported], [null, "orbit"]);
  assert.equal(webMove("Wide shot, drift").group, "drift");
  assert.equal(webMove("Medium close-up, low angle, slow push in").h3, "The camera pushes in with small amplitude at slow speed", "type + amplitude + speed, as the official H3 guide writes it");
  assert.equal(webMove("Medium close-up, low angle, slow push in").hailuo, "[Push in]");
  assert.equal(webMove("Medium close-up, low angle, slow push in").slow, true);
  assert.equal(webMove("Medium close-up, pan left").hailuo, "[Pan left]", "our pan left is the camera turning left, as Hailuo's is");
  assert.equal(webMove("Wide shot, pan right").kling, "the camera pans right");
  assert.equal(webMove("Medium shot, tracking").hailuo, "[Tracking shot]");
  assert.equal(webMove("Close-up").group, null, "no move word: the web text says nothing about the camera");
  const doc = example();
  const look = resolveLook(doc.look);
  const s01 = doc.scenes.find((scene) => scene.id === "s01");
  const hailuo = webPrompt("hailuo", s01, look, shotCast(doc, s01));
  assert.equal(hailuo.model, "h3", "H3 is the default Hailuo model");
  assert.ok(hailuo.text.startsWith(H3_FIRST_LINE + "\n\nintegrated_multimodal_description: [Shot 1] "), "the official H3 image-to-video layout");
  assert.match(hailuo.text, /The camera is a static shot and stays completely still\./);
  assert.match(hailuo.text, /\noverall_soundscape: N\/A\nnon_diegetic_music: N\/A$/, "silence asked for; the pipeline drops the track anyway");
  assert.ok(!/Avoid:/.test(hailuo.text), "the negative stays out of the text");
  assert.equal(hailuo.negative, look.negative.replace(/[.\s]+$/, ""), "and is listed for a negative field");
  assert.ok(!/\.\./.test(hailuo.text), "fields that end in a full stop are not doubled");
  const asks = webPrompt("kling", { ...s01, data: { ...s01.data, motion: "Shen asks why?" } }, look, shotCast(doc, s01));
  assert.ok(asks.text.includes("Shen asks why? ") && !asks.text.includes("why?."), "a question mark is not followed by a full stop");
  assert.equal(hailuo.sha256.length, 64);
  const legacy = webPrompt("hailuo", s01, look, shotCast(doc, s01), { hailuoModel: "2.3" });
  assert.match(legacy.text, /^\[Static shot\] /, "Hailuo 2.3 reads the bracket commands");
  assert.match(legacy.text, /The camera stays completely still\./);
  const s02 = doc.scenes.find((scene) => scene.id === "s02");
  assert.match(webPrompt("kling", s02, look, shotCast(doc, s02)).text, /^Single continuous shot, the camera slowly pushes in\. /);
  assert.equal(webPrompt("server", s02, look, shotCast(doc, s02)).text, clipPrompt(s02, look, shotCast(doc, s02)), "the server route sends what clips.mjs composes");
});

test("seconds bought per route: the route's range plus the tail handle, the server's clipSeconds, a master covering its cuts", () => {
  const doc = example();
  const timeline = estimateTimeline(doc);
  const need = (id) => { const scene = timeline.scenes.find((each) => each.id === id); return (scene.end_frame - scene.start_frame) / FPS; };
  const hailuo = planEpisode(doc, { route: "hailuo" });
  assert.equal(hailuo.plan.id, "hailuo:pro", "the Pro plan is the default for a Hailuo route");
  assert.equal(hailuo.handle_s, DEFAULT_HANDLE_S);
  for (const shot of hailuo.shots) assert.equal(shot.buy_s, Math.min(HAILUO_CLIP_SECONDS[1], Math.max(HAILUO_CLIP_SECONDS[0], Math.ceil(need(shot.id) + DEFAULT_HANDLE_S - 1e-9))), shot.id);
  const kling = planEpisode(doc, { route: "kling" });
  for (const shot of kling.shots) assert.equal(shot.buy_s, Math.min(15, Math.max(3, Math.ceil(need(shot.id) + DEFAULT_HANDLE_S - 1e-9))), shot.id);
  assert.equal(kling.plan.credits_per_second, PLANS["kling:pro"].credits_per_second["1080p"]);
  const server = planEpisode(doc, { route: "server" });
  assert.equal(server.handle_s, 0);
  for (const shot of server.shots) assert.equal(shot.buy_s, secondsBought(Math.round(need(shot.id) * FPS), "gemini-omni-1.1-flash", "1080p"), shot.id);
  for (const shot of hailuo.shots) {
    assert.equal(shot.cost.one, shot.buy_s * 12);
    assert.equal(shot.cost.expected, Math.round(shot.buy_s * 12 * shot.risk.expected_takes * 100) / 100);
    assert.equal(shot.cost.cap, shot.buy_s * 12 * 2);
  }

  // s08 returns to s01's setup and is cut from it: the master has to be bought long enough.
  const cut = example();
  const s08 = cut.scenes.find((scene) => scene.id === "s08");
  s08.data = { ...cut.scenes.find((scene) => scene.id === "s01").data, source: { shot: "s01", from_s: 3 } };
  const master = planEpisode(cut, { route: "hailuo" });
  const s01 = master.shots.find((shot) => shot.id === "s01");
  const s08Need = master.shots.find((shot) => shot.id === "s08").need_s;
  assert.deepEqual(s01.cuts, ["s08"]);
  assert.equal(s01.buy_s, Math.ceil(3 + s08Need + DEFAULT_HANDLE_S - 1e-9), "bought to cover the cut taken from it");
  assert.equal(master.shots.find((shot) => shot.id === "s08").buy_s, 0);
  assert.equal(master.shots.find((shot) => shot.id === "s08").first_frame.kind, "source");
  const serverCut = planEpisode(cut, { route: "server" });
  assert.ok(serverCut.problems.some((problem) => problem.shot === "s01" && /切鏡 s08/.test(problem.what)), "the server buys clipSeconds of s01's own length, too short for the cut");
});

test("Hailuo 2.3 sells fixed lengths per clip and has no end frame; --expected-takes moves the expected budget", () => {
  const doc = example();
  doc.scenes.find((scene) => scene.id === "s08").data.end_frame = { prompt: "Shen with her sword lowered at her waist" };
  const legacy = planEpisode(doc, { route: "hailuo", hailuoModel: "2.3" });
  assert.equal(legacy.resolution, "1080p");
  for (const shot of legacy.shots) {
    assert.equal(shot.buy_s, 6, "1080p is sold as six seconds only");
    assert.equal(shot.cost.one, HAILUO_MODELS["2.3"].per_clip["1080p"][6]);
  }
  assert.ok(legacy.problems.some((problem) => problem.shot === "s08" && /沒有首尾格/.test(problem.what)));
  assert.ok(legacy.notes.some((note) => /relax/.test(note)), "the Max plan's unlimited relax queue is named");
  const at768 = planEpisode(example(), { route: "hailuo", hailuoModel: "2.3", resolution: "768p" });
  assert.ok(at768.shots.every((shot) => [6, 10].includes(shot.buy_s)));
  assert.throws(() => planEpisode(example(), { route: "hailuo", hailuoModel: "1.0" }), /--hailuo-model/);
  const cautious = planEpisode(example(), { route: "kling", expectedTakes: expectedTakesFlag("2,3,4") });
  const base = planEpisode(example(), { route: "kling" });
  assert.ok(cautious.totals.clip.expected > base.totals.clip.expected);
  assert.equal(cautious.totals.clip.cap, base.totals.clip.cap, "the cap is the take limit either way");
  assert.throws(() => expectedTakesFlag("1,2"), /three numbers/);
});

test("batches: a three-shot pilot inside one scene with the riskiest clips, then masters and high risk first", () => {
  const plan = planEpisode(example(), { route: "hailuo" });
  const pilot = plan.batches[0];
  assert.equal(pilot.name, "小樣");
  assert.equal(pilot.shots.length, 3);
  const order = plan.shots.map((shot) => shot.id);
  const at = pilot.shots.map((id) => order.indexOf(id));
  assert.deepEqual(at, [at[0], at[0] + 1, at[0] + 2], "three consecutive shots");
  assert.ok(pilot.shots.some((id) => plan.shots.find((shot) => shot.id === id).risk.grade === "C"), "the pilot holds the hardest kind of shot");
  const rest = plan.batches[1];
  assert.equal(rest.checkpoint, true, "the first scene ends at a checkpoint");
  const grades = rest.buys.map((id) => plan.shots.find((shot) => shot.id === id).risk.grade);
  assert.deepEqual(grades, [...grades].sort((a, b) => b.localeCompare(a)), "C before B before A");
  assert.deepEqual(new Set([...pilot.shots, ...rest.shots]), new Set(order), "every shot is in a batch once");
});

test("a production profile refuses the web routes; the server route plans it", () => {
  const doc = example();
  const series = { production: { profile: { video: { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p" } } } };
  const web = planEpisode(doc, { route: "kling", series });
  assert.equal(web.conditions.import_ok, false);
  assert.ok(web.problems.some((problem) => problem.level === "refuse" && /clips import/.test(problem.what)));
  const server = planEpisode(doc, { route: "server", series });
  assert.equal(server.conditions.import_ok, true);
  assert.equal(server.model, "veo-3.1-lite-generate-preview", "the profile's model");
  assert.ok(server.shots.every((shot) => shot.buy_s === 8), "Lite at 1080p buys eight seconds");
});

test("the markdown and CSV carry the shot list, the final web text and the batches", () => {
  const plan = planEpisode(example(), { route: "hailuo" });
  const markdown = renderMarkdown(plan, "example.json");
  for (const heading of ["## 分鏡表", "## 風險與重設計", "## 定稿正文", "## 批次順序"]) assert.ok(markdown.includes(heading), heading);
  assert.match(markdown, /fully referenced/);
  assert.match(markdown, /負面欄（網頁真的有負面欄才貼/);
  const csv = renderCsv(plan).split("\n");
  assert.equal(csv.length, plan.shots.length + 1);
  assert.match(csv[0], /^id,chapter,setup,camera/);
});

test("shot_plan from the command line: exit 0, 1 with --strict on a problem, 2 on bad input", () => {
  const ok = run("shot_plan.mjs", EXAMPLE, "--route", "kling", "--json");
  assert.equal(ok.status, 0, ok.stderr);
  assert.equal(JSON.parse(ok.stdout).route, "kling");
  assert.equal(run("shot_plan.mjs").status, 2);
  assert.equal(run("shot_plan.mjs", EXAMPLE, "--route", "vimeo").status, 2);
  assert.equal(run("shot_plan.mjs", EXAMPLE, "--route", "hailuo", "--plan", "kling:pro").status, 2, "a Kling plan on a Hailuo route");
  const dir = box();
  try {
    const doc = example();
    const s08 = doc.scenes.find((scene) => scene.id === "s08");
    s08.data = { ...doc.scenes.find((scene) => scene.id === "s01").data, source: { shot: "s01", from_s: 7 } };
    writeFileSync(path.join(dir, "video.json"), JSON.stringify(doc));
    assert.equal(run("shot_plan.mjs", path.join(dir, "video.json"), "--strict").status, 1, "a cut past what the server buys");
    assert.equal(run("shot_plan.mjs", DRAMA_FIXTURE_FILE).status, 0, "the repository's drama fixture plans");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("the lock notices a one-word change of motion and a changed line, and names what it re-buys", () => {
  const doc = example();
  const plan = planEpisode(doc, { route: "hailuo" });
  const lock = { ...lockOf(doc, null, plan), created_at: "2026-10-04T00:00:00Z", note: null };
  assert.equal(compareLock(lock, lockOf(doc, null, planEpisode(doc, { route: "hailuo" }))).changed, false);

  const edited = example();
  edited.scenes.find((scene) => scene.id === "s05").data.motion += " quickly";
  edited.scenes.find((scene) => scene.id === "s07").lines[0].text = "你守得住幾人？";
  const keyframes = { shots: Object.fromEntries(doc.scenes.map((scene) => [scene.id, { file: `keyframes/${scene.id}-1.png` }])) };
  const clips = { shots: { s05: { file: "clips/s05-1.mp4" }, s01: { file: "clips/s01-import-1.mp4", imported_at: "2026-10-04T01:00:00Z" } } };
  const result = compareLock(lock, lockOf(edited, null, planEpisode(edited, { route: "hailuo" })), { keyframes, clips });
  assert.equal(result.changed, true);
  assert.deepEqual(result.shots.map((shot) => [shot.id, shot.visual, shot.keyframe, shot.speech, shot.prompt]), [["s05", true, false, false, true], ["s07", false, false, true, false]]);
  assert.deepEqual(result.impact.approvals, ["script", "storyboard", "audio"], "a changed line changes script.md too");
  assert.ok(result.impact.rebuy.some((line) => line === "s05：素材（已買）"), "motion is not in the keyframe request: no redraw since #1193");
  assert.equal(result.impact.judge_keyframes, 0);
  assert.equal(result.impact.judge_clips, 1, "the one server clip is judged again; the imported one is re-imported");
  assert.deepEqual(result.impact.imported_need_reimport, ["s01"]);
  const onlyStoryboard = compareLock(lock, lockOf(edited, null, planEpisode(edited, { route: "hailuo" })), { keyframes, clips, approved: ["storyboard"] });
  assert.deepEqual(onlyStoryboard.impact.approvals, ["storyboard"], "only approvals that exist are listed as stale");
  const reprompted = example();
  reprompted.scenes.find((scene) => scene.id === "s03").data.prompt += ", rain on her lashes";
  const redraw = compareLock(lock, lockOf(reprompted, null, planEpisode(reprompted, { route: "hailuo" })), { keyframes, clips });
  assert.ok(redraw.impact.rebuy.some((line) => /^s03：關鍵影格（已畫，重畫並 judge）/.test(line)));
  assert.equal(redraw.impact.judge_keyframes, 1);
  const voiced = example();
  voiced.characters[0].voice = { ...voiced.characters[0].voice, name: "Puck" };
  const voice = compareLock(lock, lockOf(voiced, null, planEpisode(voiced, { route: "hailuo" })));
  assert.equal(voice.changed, true, "a character's voice moves the speech and script hashes even though no shot changed");
  assert.ok(voice.impact.approvals.includes("audio"));

  const looked = example();
  looked.look.style += " softer";
  const lookResult = compareLock(lock, lockOf(looked, null, planEpisode(looked, { route: "hailuo" })));
  assert.equal(lookResult.look, true);
  assert.deepEqual(lookResult.impact.approvals, ["look", "storyboard"]);
  const moved = compareLock(lock, lockOf(doc, null, planEpisode(doc, { route: "kling" })));
  assert.ok(moved.settings.includes("route"));
  assert.deepEqual(shotPrints(doc.scenes[0]), shotPrints(JSON.parse(JSON.stringify(doc.scenes[0]))));
});

test("plan_lock from the command line: write, check, refuse to overwrite, force keeps the old lock, ready lists what is missing", () => {
  const dir = box();
  try {
    const file = path.join(dir, "doc", "video.json");
    const work = path.join(dir, "work");
    mkdirSync(path.dirname(file), { recursive: true });
    copyFileSync(EXAMPLE, file);
    const lock = (...args) => run("plan_lock.mjs", "--file", file, "--workdir", work, ...args);
    assert.equal(lock("--check").status, 2, "no lock yet");
    const early = lock("--ready", "--route", "hailuo");
    assert.equal(early.status, 1, "--ready runs before the lock, for the lock package");
    assert.match(early.stdout, /還沒有鎖定檔/);
    assert.equal(lock("--write", "--route", "hailuo", "--resolution", "1080p").status, 2, "H3 does not sell 1080p: refused, not silently 2K");
    const written = lock("--write", "--route", "hailuo", "--hailuo-model", "h3", "--resolution", "768p", "--assist", "off", "--note", "owner said yes");
    assert.equal(written.status, 0, written.stderr);
    assert.ok(existsSync(path.join(work, "plan", "lock.json")));
    const locked = JSON.parse(readFileSync(path.join(work, "plan", "lock.json"), "utf8"));
    assert.deepEqual([locked.route, locked.hailuo_model, locked.resolution, locked.web_assist], ["hailuo", "h3", "768p", "off"]);
    assert.equal(lock("--check").status, 0, "no flags: the lock's own settings");
    assert.equal(lock("--check", "--route", "kling").status, 1, "another route is a change");
    assert.equal(lock("--write").status, 2, "an existing lock is not overwritten by accident");
    const doc = JSON.parse(readFileSync(file, "utf8"));
    doc.scenes.find((scene) => scene.id === "s03").data.motion = "Shen closes her eyes once";
    writeFileSync(file, JSON.stringify(doc));
    const checked = lock("--check");
    assert.equal(checked.status, 1);
    assert.match(checked.stdout, /變更單/);
    assert.match(checked.stdout, /s03/);
    assert.equal(lock("--write", "--force").status, 0, "a re-lock keeps the locked settings");
    assert.equal(JSON.parse(readFileSync(path.join(work, "plan", "lock.json"), "utf8")).resolution, "768p");
    assert.equal(readdirSync(path.join(work, "plan")).filter((name) => /^lock-.*\.json$/.test(name)).length, 1, "the old lock is kept beside the new one");
    const log = readFileSync(path.join(work, "plan", "changes.jsonl"), "utf8").trim().split("\n").map((line) => JSON.parse(line));
    assert.equal(log.length, 1, "the re-lock records the change order it settled");
    assert.ok(log[0].changes.some((line) => line.startsWith("s03")));
    const ready = lock("--ready");
    assert.equal(ready.status, 1, "nothing drawn yet");
    assert.match(ready.stdout, /first_frame\.s01/);
    assert.match(ready.stdout, /無水印下載/);
    assert.equal(run("plan_lock.mjs", "--file", file, "--check").status, 2, "--file needs --workdir");
    writeFileSync(path.join(work, "plan", "lock.json"), JSON.stringify({ version: 1, route: "hailuo", created_at: "x", shots: {} }));
    const broken = lock("--check");
    assert.equal(broken.status, 2, "an old or broken lock is a read error, not a change");
    assert.match(broken.stderr, /version/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("the animatic keeps the timeline's length, uses keyframes when they exist and cannot be broken out of its script", () => {
  const doc = example();
  const plan = planEpisode(doc, { route: "hailuo" });
  const timeline = estimateTimeline(doc);
  const cards = animaticShots(doc, plan, {});
  assert.equal(cards.length, plan.shots.length);
  assert.equal(cards.at(-1).end, Math.round((timeline.scenes.at(-1).end_frame / FPS) * 1000) / 1000);
  assert.ok(cards.every((shot) => shot.image === null), "nothing drawn: text cards");
  const stats = animaticStats(cards);
  assert.equal(stats.shots, cards.length);
  assert.equal(stats.opening_10s, cards.filter((shot) => shot.start < 10).length);
  const dir = box();
  try {
    mkdirSync(path.join(dir, "keyframes"));
    writeFileSync(path.join(dir, "keyframes", "s01-1.png"), "png");
    const manifest = { shots: { s01: { file: "keyframes/s01-1.png" } } };
    const drawn = animaticShots(doc, plan, { manifest, workdir: dir, outDir: path.join(dir, "plan") });
    assert.equal(drawn[0].image, "../keyframes/s01-1.png", "a relative path from the page, not an embedded picture");
    assert.equal(drawn[1].image, null);
    const html = animaticHtml({ title: "t", shots: [{ ...drawn[0], lines: [{ speaker: "x", text: "</script><img src=x onerror=alert(1)>" }] }], stats, basis: "b" });
    assert.equal(html.match(/<\/script>/g).length, 1, "only the page's own closing tag");
    assert.ok(html.includes('case"pan left":return"scale(1.08) translateX("+(-3+6*p)'), "camera pan left: the picture runs right, as assemble moves it");
    assert.ok(html.includes('case"tilt up":return"scale(1.08) translateY("+(-3+6*p)'), "camera tilt up: the picture runs down");
    const { list, args } = animaticFfmpegArgs([{ ...drawn[0], image_file: path.join(dir, "keyframes", "s01-1.png") }], { list: "x.ffconcat", out: "x.mp4" });
    assert.match(list, /^ffconcat version 1\.0\n/);
    assert.equal(args[args.indexOf("-t") + 1], drawn[0].end.toFixed(3));
    const out = run("animatic.mjs", "--file", EXAMPLE, "--out", path.join(dir, "a.html"));
    assert.equal(out.status, 0, out.stderr);
    assert.ok(readFileSync(path.join(dir, "a.html"), "utf8").includes("動態分鏡"));
    assert.equal(run("animatic.mjs", "--file", EXAMPLE, "--out", path.join(dir, "b.html"), "--mp4", path.join(dir, "b.mp4")).status, 1, "--mp4 needs a picture for every shot");
    assert.equal(run("animatic.mjs", "--file", EXAMPLE).status, 2, "a file without a work directory needs --out");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

// Delivery promise and continuity locks (the names are OpenMontage's and the drama-skills / shuohao-skills packs'; the idea only).
test("continuity terms are the prompt's own words: nouns from the three lists with the adjective in front, a time of day on every mention", () => {
  const terms = continuityTerms("Wide shot at dusk, Shen in her ivory robe, one jade hair cord, Shen's sword low, a right hand in a narrow silver cuff");
  assert.deepEqual(terms.time_of_day, ["dusk"]);
  assert.deepEqual(terms.costume, ["robe", "ivory robe", "hair cord", "jade hair cord", "cuff", "silver cuff"]);
  assert.deepEqual(terms.prop, ["sword"], "a possessive (Shen's) is not an adjective, nor are `one` and `a`");
  const friends = continuityTerms("the girl bowing to him, a swordsman at the gate at nightfall");
  assert.deepEqual(friends.prop, [], "bowing is not a bow and a swordsman is not a sword");
  assert.deepEqual(friends.time_of_day, ["nightfall"]);
  assert.deepEqual(continuityTerms(undefined), { prop: [], costume: [], time_of_day: [] });
});

test("the plan carries each shot's promise and continuity locks: a shared anchor locks both ends, a time of day locks on one mention, a cut and a start_frame depend on their source", () => {
  const doc = example();
  const plan = planEpisode(doc, { route: "hailuo" });
  const byId = Object.fromEntries(plan.shots.map((shot) => [shot.id, shot]));
  for (const shot of plan.shots) assert.deepEqual(shot.promise, { visual_kind: "clip", buy_s: shot.buy_s, route: "hailuo", fit: "auto" }, shot.id);
  assert.deepEqual(byId.s05.continuity.depends_on, ["s01", "s03", "s04"], "the sword from s01, the jade hair cord from s03, the silver cuff from s04");
  assert.deepEqual(byId.s05.continuity.locks, { prop: ["sword"], costume: ["cuff", "silver cuff", "hair cord", "jade hair cord"], time_of_day: [] });
  assert.deepEqual(byId.s03.continuity, { depends_on: [], locks: { prop: [], costume: ["hair cord", "jade hair cord"], time_of_day: [] } }, "the first end of a thread has nothing before it but holds the string");
  assert.ok(!byId.s04.continuity.locks.prop.includes("steel sword"), "a phrase only one shot writes is not a thread");
  assert.deepEqual(byId.s07.continuity.locks.costume, ["shoulder clasp", "bronze shoulder clasp"], "Lu's anchor, shared with s02");
  const linked = example();
  linked.scenes.find((scene) => scene.id === "s08").data.start_frame = { shot: "s07", at: "last" };
  linked.scenes.find((scene) => scene.id === "s06").data = { ...linked.scenes.find((scene) => scene.id === "s01").data, source: { shot: "s01", from_s: 2 } };
  const chained = planEpisode(linked, { route: "hailuo" });
  assert.ok(chained.shots.find((shot) => shot.id === "s08").continuity.depends_on.includes("s07"), "a clip that continues from another's last frame depends on it");
  const cut = chained.shots.find((shot) => shot.id === "s06");
  assert.equal(cut.promise.visual_kind, "cut");
  assert.ok(cut.continuity.depends_on.includes("s01"), "a cut depends on the shot it is cut from");
  const timed = example();
  timed.scenes.find((scene) => scene.id === "s01").data.prompt += ", at dusk";
  assert.deepEqual(planEpisode(timed, { route: "hailuo" }).shots[0].continuity.locks.time_of_day, ["dusk"], "a time of day locks on its only mention");
  const markdown = renderMarkdown(plan, "example.json");
  assert.match(markdown, /## 承諾與連戲鎖/);
  assert.ok(markdown.includes("- s05：接 s01、s03、s04；道具 「sword」、服裝 「cuff」「silver cuff」「hair cord」「jade hair cord」"), markdown);
  const csv = renderCsv(plan).split("\n");
  assert.match(csv[0], /,fit,depends_on,locks$/);
  assert.ok(csv.find((row) => row.startsWith("s05,")).endsWith(",auto,s01 s03 s04,prop:sword; costume:cuff; costume:silver cuff; costume:hair cord; costume:jade hair cord"));
});

test("the lock holds each promise and continuity lock; --check names a promise made smaller and a missing string; a change-order line covers exactly the change it recorded", () => {
  const doc = example();
  const lock = { ...lockOf(doc, null, planEpisode(doc, { route: "hailuo" })), created_at: "2026-10-05T00:00:00Z", note: null };
  assert.equal(lock.version, 3);
  assert.deepEqual(lock.shots.s05.promise, { visual_kind: "clip", buy_s: lock.shots.s05.buy_s, route: "hailuo", fit: "auto" });
  assert.deepEqual(lock.shots.s05.continuity.depends_on, ["s01", "s03", "s04"]);
  const edited = example();
  edited.scenes.find((scene) => scene.id === "s03").data.visual = "still";
  edited.scenes.find((scene) => scene.id === "s02").data.fit = "freeze";
  const s05 = edited.scenes.find((scene) => scene.id === "s05");
  s05.data.prompt = s05.data.prompt.replace("jade hair cord", "red hair cord");
  const result = compareLock(lock, lockOf(edited, null, planEpisode(edited, { route: "hailuo" })), { doc: edited });
  const entry = Object.fromEntries(result.shots.map((shot) => [shot.id, shot]));
  assert.deepEqual(entry.s03.kind, ["clip", "still"]);
  assert.deepEqual(entry.s02.fit, ["auto", "freeze"]);
  assert.deepEqual(entry.s05.continuity, { missing: [{ category: "costume", text: "jade hair cord" }], depends_on: ["s01", "s03", "s04"] });
  assert.deepEqual(result.promises, [{ id: "s02", kind: null, fit: ["auto", "freeze"] }, { id: "s03", kind: ["clip", "still"], fit: null }]);
  assert.ok(result.lines.includes("s05：畫面欄位（prompt／camera／characters／末格…）、連戲鎖少了 服裝「jade hair cord」（接 s01、s03、s04 的字）"), result.lines.join("\n"));
  assert.match(renderChangeOrder(result, lock), /承諾改小的（鎖定時答應的 clip）：s02 fit auto → freeze、s03 clip → still/);
  assert.deepEqual(promiseBreaks(lock, edited).map((broken) => [broken.id, broken.kind, broken.fit]), [["s02", null, ["auto", "freeze"]], ["s03", ["clip", "still"], null]]);
  assert.deepEqual(continuityBreaks(lock, edited).map((broken) => broken.id), ["s05"]);
  assert.equal(compareLock(lock, lockOf(edited, null, planEpisode(edited, { route: "hailuo" }))).shots.find((shot) => shot.id === "s05").continuity, null, "without the document the prompt cannot be read: no continuity line");
  const removed = example();
  removed.scenes = removed.scenes.filter((scene) => scene.id !== "s04");
  assert.deepEqual(compareLock(lock, lockOf(removed, null, planEpisode(removed, { route: "hailuo" }))).promises, [{ id: "s04", kind: ["clip", "removed"], fit: null }], "a promised clip that is deleted is a promise made smaller too");

  const line = changeOrderLine(result, { at: "2026-10-05T01:00:00Z", previous_lock: lock.created_at, note: "站主說可以", status: "accepted" });
  assert.deepEqual(line.shots.map((shot) => shot.id), ["s02", "s03", "s05"]);
  assert.deepEqual([line.status, line.previous_lock, line.note, line.changes], ["accepted", lock.created_at, "站主說可以", result.lines]);
  assert.ok(coveringOrder([line], lock, "s03", { kind: ["clip", "still"] }));
  assert.equal(coveringOrder([line], lock, "s03", { kind: ["clip", "cut"] }), null, "the order covers the change it recorded, not another");
  assert.ok(coveringOrder([line], lock, "s02", { fit: ["auto", "freeze"] }));
  assert.ok(coveringOrder([line], lock, "s05", { continuity: { missing: [{ category: "costume", text: "jade hair cord" }] } }));
  assert.equal(coveringOrder([line], lock, "s05", { continuity: { missing: [{ category: "costume", text: "jade hair cord" }, { category: "prop", text: "sword" }] } }), null, "a string that went missing after the order is not covered");
  assert.equal(coveringOrder([line], { ...lock, created_at: "2026-10-06T00:00:00Z" }, "s03", { kind: ["clip", "still"] }), null, "an order against another lock covers nothing");
  assert.equal(coveringOrder([{ ...line, previous_lock: undefined }], { ...lock, created_at: undefined }, "s03", { kind: ["clip", "still"] }), null);
});

test("plan_lock --accept records the owner's decision against the lock in force; a re-lock settles it and promises the new kind", () => {
  const dir = box();
  try {
    const file = path.join(dir, "doc", "video.json");
    const work = path.join(dir, "work");
    mkdirSync(path.dirname(file), { recursive: true });
    copyFileSync(EXAMPLE, file);
    const lock = (...args) => run("plan_lock.mjs", "--file", file, "--workdir", work, ...args);
    assert.equal(lock("--accept", "--note", "x").status, 2, "nothing to accept against before a lock");
    assert.equal(lock("--write", "--route", "kling", "--note", "yes").status, 0);
    const written = JSON.parse(readFileSync(path.join(work, "plan", "lock.json"), "utf8"));
    assert.equal(written.version, 3);
    assert.equal(lock("--accept").status, 2, "the owner's words are the point of a change order");
    assert.equal(lock("--accept", "--note", "x").status, 1, "nothing changed: nothing to record");
    const doc = JSON.parse(readFileSync(file, "utf8"));
    doc.scenes.find((scene) => scene.id === "s03").data.visual = "still";
    writeFileSync(file, JSON.stringify(doc));
    const checked = lock("--check");
    assert.equal(checked.status, 1);
    assert.match(checked.stdout, /承諾改小的（鎖定時答應的 clip）：s03 clip → still/);
    const accepted = lock("--accept", "--note", "站主：s03 改成 still，省點數");
    assert.equal(accepted.status, 0, accepted.stderr);
    assert.match(accepted.stdout, /記下變更單（\d+ 項/);
    let log = readFileSync(path.join(work, "plan", "changes.jsonl"), "utf8").trim().split("\n").map((line) => JSON.parse(line));
    assert.equal(log.length, 1);
    assert.deepEqual([log[0].status, log[0].previous_lock, log[0].note], ["accepted", written.created_at, "站主：s03 改成 still，省點數"]);
    assert.deepEqual(log[0].shots.find((shot) => shot.id === "s03").kind, ["clip", "still"]);
    assert.equal(lock("--write", "--force", "--note", "重鎖").status, 0);
    log = readFileSync(path.join(work, "plan", "changes.jsonl"), "utf8").trim().split("\n").map((line) => JSON.parse(line));
    assert.equal(log.length, 2);
    assert.deepEqual([log[1].status, log[1].previous_lock], ["settled", written.created_at]);
    assert.equal(JSON.parse(readFileSync(path.join(work, "plan", "lock.json"), "utf8")).shots.s03.promise.visual_kind, "still", "the new lock promises what was settled");
    assert.equal(lock("--check").status, 0);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
