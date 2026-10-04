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
import { compareLock, lockOf, shotPrints } from "../.agents/skills/animation-preproduction/scripts/plan_lock.mjs";
import { animaticFfmpegArgs, animaticHtml, animaticShots, animaticStats } from "../.agents/skills/animation-preproduction/scripts/animatic.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const SKILL = path.join(ROOT, ".agents", "skills", "animation-preproduction");
const SCRIPTS = path.join(SKILL, "scripts");
const EXAMPLE = path.join(ROOT, ".agents", "skills", "animation-camera", "references", "budaimiao-example.json");
const example = () => JSON.parse(readFileSync(EXAMPLE, "utf8"));
const run = (script, ...args) => spawnSync(process.execPath, [path.join(SCRIPTS, script), ...args], { encoding: "utf8" });
const box = () => mkdtempSync(path.join(tmpdir(), "preproduction-"));

const ctxOf = (change = {}) => ({ characters: 1, face: false, speakerVisible: false, camera: "", moves: 0, buySeconds: 4, ...change });
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

test("the camera line becomes H3's camera sentence, Hailuo 2.3's bracket command and Kling's phrase, with the pan direction of the camera", () => {
  assert.deepEqual(webMove("Two-shot, eye level, locked"), { group: "locked", slow: false, h3: "The camera is a static shot and stays completely still", hailuo: "[Static shot]", kling: "locked-off camera, no camera movement" });
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
  assert.deepEqual(result.shots.map((shot) => [shot.id, shot.visual, shot.speech, shot.prompt]), [["s05", true, false, true], ["s07", false, true, false]]);
  assert.deepEqual(result.impact.approvals, ["storyboard", "audio"]);
  assert.ok(result.impact.rebuy.some((line) => /^s05：關鍵影格（已畫）、素材（已買）/.test(line)));
  assert.equal(result.impact.judge_calls, doc.scenes.length + 2, "every drawn picture and every bought clip is judged again");
  assert.deepEqual(result.impact.imported_need_reimport, ["s01"]);

  const looked = example();
  looked.look.style += " softer";
  const lookResult = compareLock(lock, lockOf(looked, null, planEpisode(looked, { route: "hailuo" })));
  assert.equal(lookResult.look, true);
  assert.deepEqual(lookResult.impact.approvals, ["look", "storyboard"]);
  const moved = compareLock(lock, lockOf(doc, null, planEpisode(doc, { route: "kling" })));
  assert.ok(moved.route.includes("route"));
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
    const written = lock("--write", "--route", "hailuo", "--note", "owner said yes");
    assert.equal(written.status, 0, written.stderr);
    assert.ok(existsSync(path.join(work, "plan", "lock.json")));
    assert.equal(lock("--check").status, 0);
    assert.equal(lock("--write").status, 2, "an existing lock is not overwritten by accident");
    const doc = JSON.parse(readFileSync(file, "utf8"));
    doc.scenes.find((scene) => scene.id === "s03").data.motion = "Shen closes her eyes once";
    writeFileSync(file, JSON.stringify(doc));
    const checked = lock("--check");
    assert.equal(checked.status, 1);
    assert.match(checked.stdout, /變更單/);
    assert.match(checked.stdout, /s03/);
    assert.equal(lock("--write", "--force", "--route", "hailuo").status, 0);
    assert.equal(readdirSync(path.join(work, "plan")).filter((name) => /^lock-.*\.json$/.test(name)).length, 1, "the old lock is kept beside the new one");
    const log = readFileSync(path.join(work, "plan", "changes.jsonl"), "utf8").trim().split("\n").map((line) => JSON.parse(line));
    assert.equal(log.length, 1, "the re-lock records the change order it settled");
    assert.ok(log[0].changes.some((line) => line.startsWith("s03")));
    const ready = lock("--ready");
    assert.equal(ready.status, 1, "nothing drawn yet");
    assert.match(ready.stdout, /first_frame\.s01/);
    assert.match(ready.stdout, /無水印下載/);
    assert.equal(run("plan_lock.mjs", "--file", file, "--check").status, 2, "--file needs --workdir");
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
