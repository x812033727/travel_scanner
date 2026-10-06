import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { approvalState, approve, readApprovals } from "../core/approvals.mjs";
import { lookHash } from "../core/drama.mjs";
import { dramaFixture, explainerFixture, sandbox } from "../core/fixtures/load.mjs";
import { readLedger } from "./ledger.mjs";
import { keepSheets } from "./series-store.mjs";
import { readCache, readJobs } from "./cache.mjs";
import { bestTake, chosenSheets, CONTACT_SHEET_TILES, contactSheetPages, entryStands, FIX_ARROW, fixClauses, fixesBefore, keyframeChecks, keyframeRubric, MAX_KEYFRAME_TAKES, PLACEHOLDER_FIX, retakePrompt, shotPrompt, STYLE_PLATE_ID, STYLE_PLATE_PROMPT } from "./keyframes.mjs";
import { DEFAULT_SHEET_PROMPT, MAX_LOOK_ROUNDS, optionKey, parseChoice, sheetPrompt, suggestedOf } from "./look.mjs";
import { imagePrice, statusProblem } from "./stages.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"m".repeat(43)}`;
const SHA = (data) => createHash("sha256").update(data).digest("hex");
const PNG = (text) => Buffer.concat([Buffer.from("\x89PNG\r\n\x1a\n", "binary"), Buffer.from(text)]);
const PRO_MODEL = "gemini-3-pro-image";
const FLASH_MODEL = "gemini-3.1-flash-image";

const STATUS = {
  enabled: true,
  music_enabled: true,
  image: { provider: "gemini", model: "gemini-3-pro-image", configured: true },
  clip: { provider: "gemini", model: "omni", configured: true, resolution: "1080p", seconds: 8 },
  music: { provider: "gemini", model: "lyria", configured: true },
  models: { images: { gemini: [
    { value: PRO_MODEL, label: "Pro", description: null, status: "stable", resolutions: [], durations: [], reference_images: 14, native_audio: false, usd_per_second: null, usd_per_image: 0.134, usd_per_track: null },
    { value: FLASH_MODEL, label: "Flash", description: null, status: "stable", resolutions: [], durations: [], reference_images: 14, native_audio: false, usd_per_second: null, usd_per_image: 0.067, usd_per_track: null },
  ] }, clips: {}, music: {} },
  budgets: {},
  estimated_usd: 0,
  max_usd_per_video: 200,
  max_clips_per_video: 40,
  max_retakes_per_shot: 2,
  judge_min_score: 7,
  style_preset: "cinematic-3d",
  store: { used_bytes: 0, max_file_bytes: 1, max_total_bytes: 1, writable: true },
  limits: {},
};

/**
 * A media server that draws a picture per request (its bytes depend on the prompt and seed) and
 * answers the judge from `verdicts`: a function of (kind, context, count so far) → { overall, passed, problems }.
 * `refuse(request)` returning `{ code, detail }` makes that image request a failed job instead,
 * as the server reports a provider's refusal.
 */
function mediaSite({ verdicts, status = STATUS, actualImageModel = () => status.image.model, refuse = () => null }) {
  const state = { images: [], judges: [], uploads: [], files: new Map() };
  const fetchImpl = async (url, init = {}) => {
    const { pathname, search } = new URL(url);
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const route = pathname.replace("/api/video/media/", "");
    if (init.method === "GET" && route === "status") return Response.json(status);
    if (init.method === "POST" && route === "images") {
      const request = JSON.parse(init.body);
      state.images.push(request);
      const refusal = refuse(request);
      if (refusal) return Response.json({ id: `img${state.images.length}`, status: "failed", file: null, usd_estimate: 0, error: refusal, retry_after_seconds: 0 }, { status: 200 });
      // Like the server, choose from the series, independently of the global status response,
      // and price a 2K picture with the slides choice's 2K price.
      const model = actualImageModel();
      const price = request.size === "2K" ? status.slides_image.usd_per_image_2k : status.models.images.gemini.find((entry) => entry.value === model).usd_per_image;
      const bytes = PNG(`${model}|${request.prompt}|${request.seed ?? ""}|${(request.references ?? []).map((reference) => reference.sha256).join(",")}`);
      state.files.set(SHA(bytes), bytes);
      return Response.json({ id: `img${state.images.length}`, status: "ready", file: { sha256: SHA(bytes), size: bytes.length, content_type: "image/png" }, usd_estimate: price, error: null, retry_after_seconds: 0 }, { status: 200 });
    }
    if (init.method === "GET" && route.startsWith("files/")) {
      const bytes = state.files.get(route.split("/")[2]);
      return bytes ? new Response(bytes, { headers: { "Content-Type": "image/png", "Content-Length": String(bytes.length) } }) : Response.json({ code: "video_media_file_not_found", detail: "gone" }, { status: 404 });
    }
    if (init.method === "PUT" && route.startsWith("files/")) {
      const bytes = Buffer.from(init.body);
      state.uploads.push({ route: `${route}${search}`, sha256: SHA(bytes) });
      state.files.set(route.split("/")[2], bytes);
      return Response.json({ received: [0], complete: true });
    }
    if (init.method === "POST" && route === "judge") {
      const request = JSON.parse(init.body);
      state.judges.push(request);
      const verdict = verdicts(request.kind, request, state.judges.length);
      return Response.json({ scores: {}, overall: verdict.overall, passed: verdict.passed, problems: verdict.problems ?? [], notes: "", model: "gemini-judge" });
    }
    return Response.json({ code: "video_media_route_unknown", detail: route }, { status: 404 });
  };
  return { state, fetchImpl };
}

function context(box, fetchImpl, extra = {}) {
  const out = { stdout: "", stderr: "" };
  const fakeRenderer = async () => ({ sheet: async () => PNG("sheet"), close: async () => {} });
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" },
      home: box.base,
      fetch: fetchImpl,
      openRenderer: fakeRenderer,
      hashImage: async (file) => SHA(readFileSync(file)).slice(0, 16),
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-26T08:00:00Z"),
      sleep: async () => {},
      ...extra,
    },
  };
}

const manifestOf = (box, name) => JSON.parse(readFileSync(path.join(box.workdir, name, "manifest.json"), "utf8"));
const readJson = (file) => JSON.parse(readFileSync(file, "utf8"));

test("sheet prompts, choices and suggestions", () => {
  const doc = dramaFixture();
  const prompt = sheetPrompt(doc.characters[0], { style: "ink" });
  assert.ok(prompt.startsWith(DEFAULT_SHEET_PROMPT) && prompt.includes("精衛, a girl") && prompt.endsWith("Style: ink"));
  assert.equal(sheetPrompt({ name: "x", appearance: "y", sheet_prompt: "custom sheet" }, { style: "s" }), "custom sheet. Character: x, y. Style: s");
  assert.equal(optionKey(1), "A");
  assert.equal(optionKey(3), "C");
  const candidates = [{ n: 1, judge: { overall: 8, passed: true } }, { n: 2, judge: { overall: 9.5, passed: true } }, { n: 3, judge: { overall: 9.9, passed: false } }];
  assert.equal(suggestedOf(candidates), 2, "the best of the passed ones");
  assert.equal(suggestedOf([candidates[2]]), null);
  const manifest = { characters: { jingwei: { candidates: [{ n: 1 }, { n: 2 }] }, yandi: { candidates: [{ n: 1 }] } } };
  assert.deepEqual(parseChoice("jingwei=2, yandi=1", manifest), { jingwei: 2, yandi: 1 });
  assert.throws(() => parseChoice("nobody=1", manifest), /not a character/);
  assert.throws(() => parseChoice("jingwei=9", manifest), /has no candidate 9/);
  assert.equal(imagePrice(STATUS), 0.134);
  assert.equal(statusProblem(STATUS), null);
  assert.match(statusProblem({ ...STATUS, enabled: false }), /drama route is off/);
  assert.match(statusProblem({ ...STATUS, image: { ...STATUS.image, configured: false } }), /no gemini key/);
});

test("keyframe prompts carry the style, camera and cast; the rubric asks one identity question per character", () => {
  const doc = dramaFixture();
  const farewell = doc.scenes.find((scene) => scene.id === "farewell");
  const prompt = shotPrompt(farewell, { style: "cinematic" }, doc.characters);
  assert.match(prompt, /^medium shot, the emperor.*\. Style: cinematic\. Camera: static, slight handheld drift\. Characters: 精衛: a girl of about twelve.*; 炎帝: a tall/);
  const rubric = keyframeRubric([{ id: "jing-wei", name: "精衛" }]);
  assert.deepEqual(rubric.map((item) => item.key), ["identity_jing_wei", "prompt", "style", "clean", "no_text", "subtitle_band"]);
  assert.ok(rubric.every((item) => /^[a-z][a-z0-9_]{0,39}$/.test(item.key)));
  const sheets = chosenSheets({ characters: { jingwei: { candidates: [{ n: 1, file: "a.png", sha256: "1" }, { n: 2, file: "b.png", sha256: "2" }] } } }, { jingwei: 2, yandi: 1 });
  assert.deepEqual(sheets, { jingwei: { file: "b.png", sha256: "2" } });
});

test("look draws candidates per character, has them judged, suggests the best and reuses everything on a rerun", async () => {
  const box = sandbox("fixture-drama", "drama");
  // Every sheet passes but jingwei's first; the best score wins.
  const site = mediaSite({
    verdicts: (kind, request, count) => {
      assert.equal(kind, "look");
      const first = request.context.character.name === "精衛" && request.files[0].label === "candidate A";
      return first ? { overall: 5, passed: false, problems: ["six fingers"] } : { overall: 7 + (count % 3), passed: true };
    },
  });
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  assert.match(dry.out.stdout, /2 characters × 3 candidates = 6 images/);
  assert.match(dry.out.stdout, /gemini gemini-3-pro-image ready; about US\$0\.86 for one round/);
  assert.equal(site.state.images.length, 0);

  const run = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.equal(site.state.images.length, 6);
  assert.deepEqual([...new Set(site.state.images.map((request) => request.purpose))], ["character_sheet"]);
  assert.deepEqual(site.state.images.slice(0, 3).map((request) => request.seed), [1, 2, 3]);
  assert.match(site.state.images[0].prompt, /Character: 精衛/);
  assert.match(site.state.images[0].negative_prompt, /extra fingers/);
  assert.equal(site.state.judges.length, 6);
  const manifest = manifestOf(box, "characters");
  assert.equal(manifest.look_hash, lookHash(dramaFixture()));
  assert.equal(manifest.characters.jingwei.candidates.length, 3);
  assert.equal(manifest.characters.jingwei.candidates[0].judge.passed, false);
  assert.notEqual(manifest.characters.jingwei.suggested, 1, "a failed sheet is never suggested");
  assert.ok(manifest.characters.yandi.suggested >= 1);
  for (const entry of Object.values(manifest.characters)) for (const candidate of entry.candidates) assert.ok(existsSync(path.join(box.workdir, candidate.file)), candidate.file);
  assert.equal(manifest.contact_sheet, "characters/contact-sheet.png");
  assert.ok(existsSync(path.join(box.workdir, "characters", "contact-sheet.png")));
  const ledger = readLedger(box.workdir);
  assert.equal(ledger.totals.images, 6);
  assert.equal(ledger.totals.judge_calls, 6);
  assert.equal(ledger.totals.usd, 0.864, "six sheets at 0.134 and six judge calls at 0.01");
  assert.match(run.out.stdout, /next: node tools\/video\/cli\.mjs review-push --slug fixture-drama --gate look/);

  const again = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(site.state.images.length, 6, "nothing is generated twice");
  assert.equal(site.state.judges.length, 6, "nothing is judged twice");

  const choose = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug, "--choose", "jingwei=2,yandi=1"], choose.ctx), EXIT.ok, choose.out.stderr);
  const choice = JSON.parse(readFileSync(path.join(box.workdir, "characters", "choice.json"), "utf8"));
  assert.deepEqual(choice, { look_hash: manifest.look_hash, chosen: { jingwei: 2, yandi: 1 }, chosen_at: "2026-09-26T08:00:00.000Z" });

  const page = context(box, site.fetchImpl);
  assert.equal(await main(["review", "--slug", box.slug], page.ctx), EXIT.ok, page.out.stderr);
  const html = readFileSync(path.join(box.workdir, "review", "look.html"), "utf8");
  assert.match(html, /精衛（jingwei）/);
  assert.match(html, /six fingers/);
});

// A judge problem as the server shapes it: the criterion's key, the fault and where, and after
// the arrow the words to put in the prompt (apps/api/app/video_media/judge.py).
const CROWN_FIX = "a crown of bronze leaves, as the appearance says";
const CROWN_PROBLEM = `appearance: the crown is a plain gold band${FIX_ARROW}${CROWN_FIX}`;

test("a character no sheet passes gets a second round, asked with the judge's fix, then the owner is told", async () => {
  const box = sandbox("fixture-drama", "drama");
  const site = mediaSite({ verdicts: (kind, request) => (request.context.character.name === "炎帝" ? { overall: 4, passed: false, problems: [CROWN_PROBLEM] } : { overall: 8, passed: true }) });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug], run.ctx), EXIT.lint, run.out.stderr);
  const manifest = manifestOf(box, "characters");
  assert.equal(manifest.characters.yandi.candidates.length, 3 * MAX_LOOK_ROUNDS);
  assert.deepEqual(manifest.characters.yandi.candidates.map((candidate) => candidate.seed), [1, 2, 3, 101, 102, 103]);
  assert.equal(manifest.characters.yandi.needs_review, true);
  assert.equal(manifest.characters.jingwei.candidates.length, 3, "a character with a passed sheet gets no second round");
  // Every candidate after the first, and the whole second round, is asked with the fix; the
  // character whose sheets pass is asked as written.
  const yandi = site.state.images.filter((request) => request.prompt.includes("Character: 炎帝"));
  assert.equal(yandi.length, 3 * MAX_LOOK_ROUNDS);
  assert.doesNotMatch(yandi[0].prompt, /Corrections/);
  assert.ok(yandi.slice(1).every((request) => request.prompt.endsWith(`. Corrections: ${CROWN_FIX}`)), yandi[1].prompt);
  assert.ok(site.state.images.filter((request) => request.prompt.includes("Character: 精衛")).every((request) => !request.prompt.includes("Corrections")));
  assert.deepEqual(manifest.characters.yandi.candidates.map((candidate) => candidate.fixes), [undefined, [CROWN_FIX], [CROWN_FIX], [CROWN_FIX], [CROWN_FIX], [CROWN_FIX]]);
  assert.deepEqual(manifest.characters.yandi.fixes, [CROWN_FIX], "the hint for the rewrite of the appearance");
  assert.equal(manifest.characters.jingwei.fixes, undefined);
  assert.match(run.out.stdout, /yandi seed 2: asked with the corrections of the candidates before: a crown of bronze leaves, as the appearance says\n/);
  assert.match(run.out.stdout, /ERROR yandi: no candidate passed the judge: appearance: the crown is a plain gold band → a crown of bronze leaves, as the appearance says\n  fixes for yandi: a crown of bronze leaves, as the appearance says\nrewrite the appearance or sheet_prompt of yandi and run look again/);
});

const STORM_FIX = "the girl facing the sea, in the middle third of the frame";
const STORM_PROBLEM = `prompt: the girl faces away from the sea, at the left edge${FIX_ARROW}${STORM_FIX}`;

test("keyframes need the approved look, draw each shot from the chosen sheets, retake failures with the judge's fix and warn on look-alikes", async () => {
  const box = sandbox("fixture-drama", "drama");
  let sheets = 0;
  const site = mediaSite({
    verdicts: (kind, request) => {
      if (kind === "look") return { overall: 8 + ((sheets += 1) % 2), passed: true };
      // The storm's first take fails; everything else passes.
      const stormTakes = site.state.judges.filter((each) => each.kind === "keyframe" && each.context.shot.id === "sea-storm").length;
      return request.context.shot.id === "sea-storm" && stormTakes === 1 ? { overall: 5, passed: false, problems: [STORM_PROBLEM] } : { overall: 8, passed: true };
    },
  });
  const look = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug], look.ctx), EXIT.ok, look.out.stderr);
  const early = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], early.ctx), EXIT.owner);
  assert.match(early.out.stderr, /the look is not approved yet/);

  const choose = context(box, site.fetchImpl);
  await main(["look", "--slug", box.slug, "--choose", "jingwei=2,yandi=1"], choose.ctx);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  const imagesBefore = site.state.images.length;
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  assert.match(dry.out.stdout, /keyframes for 4 shots \(0 end frames\), up to 3 takes each/);
  assert.match(dry.out.stdout, /farewell: medium shot.*\n  references: jingwei=B, yandi=A/);

  const run = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  const requests = site.state.images.slice(imagesBefore);
  assert.equal(requests.length, 5, "four shots, the storm twice");
  assert.deepEqual(requests.map((request) => [request.shot_id, request.seed]), [["opening", 1], ["farewell", 1], ["sea-storm", 1], ["sea-storm", 2], ["bird", 1]]);
  // The retake is asked with the judge's fix for the take before it; the first take as written.
  assert.doesNotMatch(requests[2].prompt, /Corrections/);
  assert.equal(requests[3].prompt, `${requests[2].prompt}. Corrections: ${STORM_FIX}`);
  assert.match(run.out.stdout, /sea-storm take 2: asked with the corrections of the takes before: the girl facing the sea, in the middle third of the frame\n/);
  const chosen = manifestOf(box, "characters").characters;
  const jingweiSheet = chosen.jingwei.candidates.find((candidate) => candidate.n === 2).sha256;
  const yandiSheet = chosen.yandi.candidates.find((candidate) => candidate.n === 1).sha256;
  assert.deepEqual(requests[1].references, [{ sha256: jingweiSheet, role: "character" }, { sha256: yandiSheet, role: "character" }]);
  assert.deepEqual(requests[4].references, [], "the bird's shot names no character");
  assert.ok(site.state.uploads.some((upload) => upload.sha256 === jingweiSheet), "the chosen sheets go to the store first");
  const storm = site.state.judges.filter((each) => each.kind === "keyframe" && each.context.shot.id === "sea-storm");
  assert.equal(storm.length, 2);
  assert.deepEqual(storm[0].files.map((file) => file.label), ["keyframe", "sheet 精衛"]);
  assert.deepEqual(storm[0].rubric.map((item) => item.key).slice(0, 2), ["identity_jingwei", "prompt"]);
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.look_hash, lookHash(dramaFixture()));
  assert.equal(manifest.shots["sea-storm"].seed, 2);
  assert.equal(manifest.shots["sea-storm"].takes.length, 2);
  assert.equal(manifest.shots["sea-storm"].takes[0].fixes, undefined);
  assert.deepEqual(manifest.shots["sea-storm"].takes[1].fixes, [STORM_FIX], "what the take was asked with is on record");
  assert.notEqual(manifest.shots["sea-storm"].takes[0].key, manifest.shots["sea-storm"].takes[1].key);
  assert.equal(manifest.shots["sea-storm"].needs_review, false);
  assert.equal(manifest.shots["sea-storm"].fixes, undefined, "a shot that passed leaves no hint");
  assert.equal(manifest.shots["sea-storm"].file, "keyframes/sea-storm-2.png");
  assert.equal(manifest.thumbnail_source, "keyframes/sea-storm-2.png");
  assert.deepEqual(manifest.duplicates, []);
  assert.ok(existsSync(path.join(box.workdir, "keyframes", "contact-sheet.png")));
  assert.equal(manifest.contact_sheet, "keyframes/contact-sheet.png");
  assert.deepEqual(manifest.contact_sheets, ["keyframes/contact-sheet.png"], "four shots fit on one page");
  assert.match(run.out.stdout, /next: node tools\/video\/cli\.mjs review-push --slug fixture-drama --gate storyboard/);

  const again = context(box, site.fetchImpl, { hashImage: async () => "0".repeat(16) });
  assert.equal(await main(["keyframes", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(site.state.images.length, imagesBefore + 5, "drawn shots are kept");
  assert.equal(manifestOf(box, "keyframes").duplicates.length, 3, "four identical hashes are three look-alike pairs");
  assert.match(again.out.stdout, /WARN shots opening and farewell look alike/);
});

test("two looks in one episode share the approved face sheet and carry appearance into image judging", async () => {
  const box = sandbox("fixture-drama", "drama");
  const doc = dramaFixture();
  doc.characters[0].shot_looks = [
    { id: "present", appearance: "adult woman in a navy business suit with short hair" },
    { id: "past", appearance: "young woman in a white ancient robe with braided hair" },
  ];
  doc.scenes[1].data.character_looks = { jingwei: "past" };
  doc.scenes[2].data.character_looks = { jingwei: "present" };
  doc.scenes[1].data.end_frame = { prompt: "the woman turns away" };
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const site = mediaSite({ verdicts: () => ({ overall: 9, passed: true, problems: [] }) });
  assert.equal(await main(["look", "--slug", box.slug], context(box, site.fetchImpl).ctx), EXIT.ok);
  const sheets = manifestOf(box, "characters");
  assert.deepEqual(Object.keys(sheets.characters), ["jingwei", "yandi"], "no duplicate cast or per-shot faces");
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
  const images = site.state.images.filter((request) => request.purpose === "keyframe");
  const past = images.find((request) => request.shot_id === "farewell");
  const present = images.find((request) => request.shot_id === "sea-storm");
  assert.equal(past.references[0].sha256, present.references[0].sha256, "both ages use the same approved identity anchor");
  assert.match(past.prompt, /white ancient robe/);
  assert.match(present.prompt, /navy business suit/);
  assert.match(present.prompt, /same facial identity/);
  assert.ok(images.some((request) => request.prompt.includes("the woman turns away") && request.prompt.includes("white ancient robe")), "end frame uses the same selected look");
  const verdict = site.state.judges.find((request) => request.kind === "keyframe" && request.context.shot.id === "sea-storm");
  assert.match(verdict.rubric[0].question, /override the sheet/);
  assert.equal(verdict.context.characters[0].description, doc.characters[0].shot_looks[0].appearance);
  assert.equal((await approvalState({ gate: "look", docDir: box.dir, workdir: box.workdir })).status, "approved");
});

const BIRD_FIX = "a white gull in the middle third of the frame";
const BIRD_PROBLEM = `subject: no bird anywhere in the frame${FIX_ARROW}${BIRD_FIX}`;

test("a shot that never passes is left for a prompt fix after the last take, with the judge's fixes as the hint", async () => {
  const box = sandbox("fixture-drama", "drama");
  const site = mediaSite({ verdicts: (kind, request) => (kind === "keyframe" && request.context.shot.id === "bird" ? { overall: 3, passed: false, problems: [BIRD_PROBLEM] } : { overall: 9, passed: true }) });
  await main(["look", "--slug", box.slug], context(box, site.fetchImpl).ctx);
  await main(["look", "--slug", box.slug, "--choose", "jingwei=1,yandi=1"], context(box, site.fetchImpl).ctx);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--shot", "bird,opening"], run.ctx), EXIT.lint, run.out.stderr);
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.shots.bird.takes.length, MAX_KEYFRAME_TAKES);
  assert.equal(manifest.shots.bird.needs_review, true);
  assert.deepEqual(manifest.shots.bird.problems, [BIRD_PROBLEM], "the same line from every take, once");
  assert.deepEqual(manifest.shots.bird.fixes, [BIRD_FIX]);
  assert.deepEqual(site.state.images.filter((request) => request.shot_id === "bird").map((request) => request.prompt.endsWith(`. Corrections: ${BIRD_FIX}`)), [false, true, true], "the second and third takes were asked with the fix");
  assert.equal(manifest.shots.opening.needs_review, false);
  assert.equal(manifest.shots.opening.fixes, undefined);
  assert.equal(manifest.shots.farewell, undefined, "only the named shots were drawn");
  assert.match(run.out.stdout, /ERROR bird: no take passed the judge: subject: no bird anywhere in the frame → a white gull in the middle third of the frame\n  fixes for bird: a white gull in the middle third of the frame\nfix the prompts of bird and run keyframes again/);
  assert.equal(readApprovals(box.workdir).approvals.at(-1).gate, "look");
  assert.ok(existsSync(path.join(box.workdir, "keyframes", "bird-3.png")), "every take stays on disk for the prompt fix");

  // The STOP file ends a run between remote calls and keeps what was drawn.
  writeFileSync(path.join(box.workdir, "STOP"), "");
  const stopped = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--shot", "farewell"], stopped.ctx), EXIT.ok, stopped.out.stderr);
  assert.match(stopped.out.stdout, /stopped by the STOP file/);
  assert.equal(manifestOf(box, "keyframes").shots.farewell, undefined);
});

// What the server reports when the provider refuses a request outright, as MiniMax did a prompt
// over its length limit on 2026-10-04: a failed job, refused again for every seed of that prompt.
const TOO_LONG = { code: "video_media_upstream_invalid", detail: "prompt length must be less than 1500" };

test("a shot every seed is refused for waits for a prompt fix with the refusal, while the drawn shots go on to the sheet and the look-alike check", async () => {
  const box = sandbox("fixture-story", "story");
  let refusing = true;
  const site = mediaSite({
    verdicts: () => ({ overall: 8, passed: true }),
    // The thumbnail's shot is refused every time, the shot before it on its first seed only.
    refuse: (request) => (refusing && (request.shot_id === "sand-lines" || (request.shot_id === "number-owner" && request.seed === 1)) ? TOO_LONG : null),
  });
  const sheets = [];
  const hashed = [];
  const extra = {
    openRenderer: async () => ({ sheet: async (html) => (sheets.push(html), PNG(`sheet ${sheets.length}`)), close: async () => {} }),
    hashImage: async (file) => (hashed.push(path.basename(file)), SHA(readFileSync(file)).slice(0, 16)),
  };
  const shots = ["--shot", "checkout-beep,number-owner,sand-lines"];
  const run = context(box, site.fetchImpl, extra);
  assert.equal(await main(["keyframes", "--slug", box.slug, ...shots], run.ctx), EXIT.lint, run.out.stderr);
  assert.doesNotMatch(run.out.stderr, /TypeError|argument must be/, "the refusal is the result, not an exception");
  assert.deepEqual(site.state.images.map((request) => [request.shot_id, request.seed]), [["checkout-beep", 1], ["number-owner", 1], ["number-owner", 2], ["sand-lines", 1], ["sand-lines", 2], ["sand-lines", 3]]);
  assert.equal(site.state.judges.length, 2, "a refused seed has no picture to judge");
  const manifest = manifestOf(box, "keyframes");
  assert.deepEqual(manifest.shots["sand-lines"], { takes: [], needs_review: true, problems: [`no take could be generated: ${TOO_LONG.detail}`] });
  assert.equal(manifest.shots["checkout-beep"].file, "keyframes/checkout-beep-1.png");
  assert.equal(manifest.shots["checkout-beep"].needs_review, false);
  assert.equal(manifest.shots["number-owner"].file, "keyframes/number-owner-2.png", "a refused seed is followed by the next");
  assert.deepEqual(manifest.shots["number-owner"].takes.map((take) => take.seed), [2]);
  assert.equal(manifest.shots["number-owner"].needs_review, false);
  assert.equal(manifest.thumbnail_source, null, "the thumbnail's shot has no picture yet");
  assert.deepEqual(hashed, ["checkout-beep-1.png", "number-owner-2.png"], "only pictures are compared");
  assert.deepEqual(manifest.contact_sheets, ["keyframes/contact-sheet.png"]);
  assert.equal(sheets.length, 1);
  assert.equal(sheets[0].match(/<figure>/g).length, 2);
  assert.match(sheets[0], /fixture-story：分鏡 2 鏡/);
  assert.doesNotMatch(sheets[0], /sand-lines/);
  assert.match(run.out.stdout, /2 keyframes generated in \d+ s; 2 shots drawn;/);
  assert.match(run.out.stdout, /sand-lines seed 3: sand-lines: prompt length must be less than 1500; trying another seed\n/);
  assert.match(run.out.stdout, /ERROR sand-lines: no take could be generated: prompt length must be less than 1500\n/);
  assert.match(run.out.stdout, /fix the prompts of sand-lines and run keyframes again/);
  // Each refusal is booked as a failed job at no cost, and none is left waiting to be picked up.
  const images = readLedger(box.workdir).entries.filter((entry) => entry.kind === "image");
  assert.deepEqual(images.map((entry) => [entry.id, entry.status, entry.error ?? null]), [
    ["checkout-beep", "ready", null],
    ["number-owner", "failed", TOO_LONG.code],
    ["number-owner", "ready", null],
    ["sand-lines", "failed", TOO_LONG.code],
    ["sand-lines", "failed", TOO_LONG.code],
    ["sand-lines", "failed", TOO_LONG.code],
  ]);
  assert.ok(images.filter((entry) => entry.status === "failed").every((entry) => entry.cost_usd === 0));
  assert.deepEqual(readJobs(box.workdir).jobs, {});

  // Once the prompt is one the provider takes, the rerun draws that shot alone and keeps the rest.
  refusing = false;
  const fixed = context(box, site.fetchImpl, extra);
  assert.equal(await main(["keyframes", "--slug", box.slug, ...shots], fixed.ctx), EXIT.ok, fixed.out.stderr);
  assert.match(fixed.out.stdout, /checkout-beep: kept \(judge 8\/10\)\n/);
  assert.match(fixed.out.stdout, /number-owner: kept \(judge 8\/10\)\n/);
  assert.deepEqual(site.state.images.slice(6).map((request) => [request.shot_id, request.seed]), [["sand-lines", 1]]);
  const after = manifestOf(box, "keyframes");
  assert.equal(after.shots["sand-lines"].file, "keyframes/sand-lines-1.png");
  assert.equal(after.shots["sand-lines"].needs_review, false);
  assert.equal(after.shots["sand-lines"].problems, undefined);
  assert.equal(after.shots["number-owner"].sha256, manifest.shots["number-owner"].sha256);
  assert.equal(after.thumbnail_source, "keyframes/sand-lines-1.png");
  assert.equal(sheets.at(-1).match(/<figure>/g).length, 3);
});

test("a run where every seed of every shot is refused ends on the refusals, with no picture checked and no contact sheet", async () => {
  const box = sandbox("fixture-story", "story");
  // A sheet left by an earlier storyboard shows pictures that are not this manifest's.
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  writeFileSync(path.join(box.workdir, "keyframes", "contact-sheet.png"), PNG("an earlier storyboard"));
  const BLOCKED = { code: "video_media_rejected", detail: "output blocked by the content filter" };
  const site = mediaSite({
    verdicts: () => ({ overall: 8, passed: true }),
    refuse: (request) => (request.shot_id === "first-scan" && request.seed > 1 ? BLOCKED : TOO_LONG),
  });
  let renderers = 0;
  let hashes = 0;
  const run = context(box, site.fetchImpl, {
    openRenderer: async () => {
      renderers += 1;
      return { sheet: async () => PNG("sheet"), close: async () => {} };
    },
    hashImage: async () => {
      hashes += 1;
      return "0".repeat(16);
    },
  });
  assert.equal(await main(["keyframes", "--slug", box.slug, "--shot", "sand-lines,first-scan"], run.ctx), EXIT.lint, run.out.stderr);
  assert.doesNotMatch(run.out.stderr, /TypeError|argument must be/);
  const manifest = manifestOf(box, "keyframes");
  assert.deepEqual(manifest.shots, {
    "sand-lines": { takes: [], needs_review: true, problems: [`no take could be generated: ${TOO_LONG.detail}`] },
    "first-scan": { takes: [], needs_review: true, problems: [`no take could be generated: ${TOO_LONG.detail}`, `no take could be generated: ${BLOCKED.detail}`] },
  });
  assert.equal(site.state.images.length, 6);
  assert.equal(site.state.judges.length, 0);
  assert.equal(hashes, 0, "no picture to compare");
  assert.equal(renderers, 0, "no sheet is drawn for a storyboard with no picture");
  assert.deepEqual(manifest.duplicates, []);
  assert.equal(manifest.thumbnail_source, null);
  assert.equal(manifest.contact_sheet, null);
  assert.deepEqual(manifest.contact_sheets, []);
  assert.ok(!existsSync(path.join(box.workdir, "keyframes", "contact-sheet.png")), "the earlier storyboard's sheet is gone");
  const ledger = readLedger(box.workdir);
  assert.deepEqual(ledger.entries.map((entry) => [entry.id, entry.status, entry.error]), [
    ["sand-lines", "failed", TOO_LONG.code],
    ["sand-lines", "failed", TOO_LONG.code],
    ["sand-lines", "failed", TOO_LONG.code],
    ["first-scan", "failed", TOO_LONG.code],
    ["first-scan", "failed", BLOCKED.code],
    ["first-scan", "failed", BLOCKED.code],
  ]);
  assert.equal(ledger.totals.usd, 0, "a refused job costs nothing");
  assert.deepEqual(readJobs(box.workdir).jobs, {});
  assert.match(run.out.stdout, /0 keyframes generated in \d+ s; 0 shots drawn;/);
  assert.match(run.out.stdout, /ERROR sand-lines: no take could be generated: prompt length must be less than 1500\n/);
  assert.match(run.out.stdout, /ERROR first-scan: no take could be generated: prompt length must be less than 1500; no take could be generated: output blocked by the content filter\n/);
  assert.match(run.out.stdout, /fix the prompts of sand-lines, first-scan and run keyframes again/);
  assert.deepEqual(contactSheetPages([]), [], "a storyboard with no picture has no page");
});

test("a cap interruption before the end frame retains the judged start picture and resumes only the missing end", async () => {
  const box = sandbox("fixture-drama", "drama");
  const doc = dramaFixture();
  doc.scenes[0].data.end_frame = { prompt: "the sun rises above the mountain" };
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const status = { ...STATUS };
  const site = mediaSite({ status, verdicts: () => ({ overall: 9, passed: true, problems: [] }) });
  await main(["look", "--slug", box.slug], context(box, site.fetchImpl).ctx);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  status.max_usd_per_video = readLedger(box.workdir).totals.usd + 0.15;
  const capped = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--shot", "opening"], capped.ctx), EXIT.owner, capped.out.stderr);
  assert.match(capped.out.stderr, /per-video cap/);
  const partial = manifestOf(box, "keyframes").shots.opening;
  assert.equal(partial.incomplete, true);
  assert.equal(partial.judge.passed, true);
  assert.equal(partial.end_frame, undefined);
  const images = site.state.images.length;
  const judges = site.state.judges.length;
  status.max_usd_per_video = 200;
  const resumed = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--shot", "opening"], resumed.ctx), EXIT.ok, resumed.out.stderr);
  const completed = manifestOf(box, "keyframes").shots.opening;
  assert.equal(completed.sha256, partial.sha256);
  assert.ok(completed.end_frame.file);
  assert.equal(completed.incomplete, undefined);
  assert.equal(site.state.images.length, images + 1, "only the missing end frame is bought");
  assert.equal(site.state.judges.length, judges, "the accepted start picture keeps its verdict");
});

test("an explainer has no look: look refuses it, and keyframes draw every still with no sheet and no identity question", async () => {
  const box = sandbox("fixture-explainer", "explainer");
  const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }) });
  const look = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug], look.ctx), EXIT.usage);
  assert.match(look.out.stderr, /a drama with none has no look stage: run keyframes/);

  const run = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  const shots = explainerFixture().scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id);
  assert.deepEqual(site.state.images.map((request) => request.shot_id), shots);
  assert.ok(site.state.images.every((request) => request.references.length === 0), "no character sheet to reference");
  assert.match(site.state.images[0].prompt, /Style: flat editorial illustration/);
  assert.ok(site.state.judges.every((request) => !request.rubric.some((item) => item.key.startsWith("identity_"))));
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.look_hash, lookHash(explainerFixture()));
  assert.deepEqual(Object.keys(manifest.shots).sort(), [...shots].sort());
});

/** The sandbox's video.json, changed by `edit` and written back. */
function rewrite(box, edit) {
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  edit(doc);
  writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`);
  return doc;
}

/** The story example stretched to `count` shots: its own ten, then later moments of them under new ids. */
function stretch(doc, count) {
  const shots = doc.scenes.filter((scene) => scene.template === "shot");
  const cards = doc.scenes.filter((scene) => scene.template !== "shot");
  const more = Array.from({ length: count - shots.length }, (_, index) => {
    const copy = structuredClone(shots[index % shots.length]);
    delete copy.chapter;
    copy.data.prompt = `${copy.data.prompt}, a later moment ${index + 1}`;
    return { ...copy, id: `more-${index + 1}`, lines: copy.lines.map((line, n) => ({ ...line, id: `m${String(index).padStart(3, "0")}${n}` })) };
  });
  doc.scenes = [...shots, ...more, ...cards];
}

test("a narrator-only drama draws its keyframes without a look gate, from the style frames alone", async () => {
  const box = sandbox("fixture-story", "story");
  // The style anchor every story of the series shares (docs/videos/STORY.md), beside the script.
  const anchor = PNG("style anchor");
  writeFileSync(path.join(box.dir, "style-anchor.png"), anchor);
  const doc = rewrite(box, (each) => {
    each.look.style_frames = ["style-anchor.png"];
  });
  const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }) });
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  assert.match(dry.out.stdout, /keyframes for 10 shots \(0 end frames\), up to 3 takes each/);

  const run = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.equal(site.state.images.length, 10, "one keyframe a shot, and not one character sheet");
  assert.deepEqual([...new Set(site.state.images.map((request) => request.purpose))], ["keyframe"]);
  for (const request of site.state.images) assert.deepEqual(request.references, [{ sha256: SHA(anchor), role: "style" }], request.shot_id);
  assert.deepEqual(site.state.uploads.map((upload) => upload.sha256), [SHA(anchor)], "only the style frame goes to the store");
  assert.equal(site.state.judges.length, 10);
  for (const judged of site.state.judges) {
    assert.deepEqual(judged.rubric.map((item) => item.key), ["prompt", "style", "clean", "no_text", "subtitle_band"], "no identity question without a character, and no craft question: that is for illustrated slides alone");
    assert.deepEqual(judged.files.map((file) => file.label), ["keyframe"]);
  }
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.look_hash, lookHash(doc));
  assert.deepEqual(Object.keys(manifest.shots), doc.scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id));
  assert.equal(manifest.thumbnail_source, manifest.shots["sand-lines"].file);
  assert.equal(manifest.contact_sheet, "keyframes/contact-sheet.png");
  assert.deepEqual(manifest.contact_sheets, ["keyframes/contact-sheet.png"]);
  assert.ok(!existsSync(path.join(box.workdir, "characters")), "no character sheet is read or written");
  assert.deepEqual(readApprovals(box.workdir).approvals, [], "nothing waited on a gate");
  assert.match(run.out.stdout, /next: node tools\/video\/cli\.mjs review-push --slug fixture-story --gate storyboard/);
});

test("the storyboard's contact sheet is one page up to 24 shots, then pages of 24 in shot order", () => {
  const tiles = (count) => Array.from({ length: count }, (_, index) => ({ file: `keyframes/shot-${index + 1}-1.png`, label: `shot-${index + 1}` }));
  const pages = (count) => contactSheetPages(tiles(count)).map((page) => [page.file, page.tiles.length]);
  assert.equal(CONTACT_SHEET_TILES, 24);
  assert.deepEqual(pages(24), [["keyframes/contact-sheet.png", 24]], "a storyboard that fits keeps the one sheet its readers know");
  assert.deepEqual(pages(25), [["keyframes/contact-sheet-01.png", 24], ["keyframes/contact-sheet-02.png", 1]]);
  assert.deepEqual(pages(95), [["keyframes/contact-sheet-01.png", 24], ["keyframes/contact-sheet-02.png", 24], ["keyframes/contact-sheet-03.png", 24], ["keyframes/contact-sheet-04.png", 23]]);
  assert.deepEqual(contactSheetPages(tiles(95)).flatMap((page) => page.tiles), tiles(95), "every shot once, in order");
});

test("keyframes of a long story draw every page, keep contact_sheet on the first and clear an older storyboard's sheet", async () => {
  const box = sandbox("fixture-story", "story");
  rewrite(box, (doc) => stretch(doc, 25));
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  writeFileSync(path.join(box.workdir, "keyframes", "contact-sheet.png"), PNG("a shorter storyboard"));
  const drawn = [];
  const openRenderer = async () => ({
    sheet: async (html) => {
      drawn.push(html);
      return PNG(`page ${drawn.length}`);
    },
    close: async () => {},
  });
  const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }) });
  const run = context(box, site.fetchImpl, { openRenderer });
  assert.equal(await main(["keyframes", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.equal(site.state.images.length, 25);
  const manifest = manifestOf(box, "keyframes");
  assert.deepEqual(manifest.contact_sheets, ["keyframes/contact-sheet-01.png", "keyframes/contact-sheet-02.png"]);
  assert.equal(manifest.contact_sheet, "keyframes/contact-sheet-01.png", "the first page, for the readers written before there were pages");
  assert.deepEqual(drawn.map((html) => html.match(/<figure>/g).length), [24, 1]);
  assert.match(drawn[0], /fixture-story：分鏡 25 鏡（第 1／2 頁）/);
  assert.match(drawn[1], /more-15 · 8\/10/);
  for (const file of manifest.contact_sheets) assert.ok(existsSync(path.join(box.workdir, file)), file);
  assert.ok(!existsSync(path.join(box.workdir, "keyframes", "contact-sheet.png")), "the shorter storyboard's sheet is gone");
});

function seriesImageModel(box, model) {
  const file = path.join(box.dir, "series.json");
  const series = JSON.parse(readFileSync(file, "utf8"));
  series.image_model = model;
  writeFileSync(file, `${JSON.stringify(series, null, 2)}\n`);
}

// One sheet or one narrator-only shot isolates the image model from character approval and
// multi-shot retry behavior, which the preceding tests already cover.
const modelStages = [
  {
    command: "look",
    manifest: "characters",
    args: ["--candidates", "1"],
    prepare(box) {
      const character = dramaFixture().characters[0];
      rewrite(box, (doc) => { doc.characters = [character]; });
      const file = path.join(box.dir, "series.json");
      const series = JSON.parse(readFileSync(file, "utf8"));
      series.characters = [character];
      writeFileSync(file, `${JSON.stringify(series, null, 2)}\n`);
    },
    picture: (manifest) => manifest.characters.jingwei.candidates[0],
  },
  {
    command: "keyframes",
    manifest: "keyframes",
    args: ["--shot", "checkout-beep"],
    prepare() {},
    picture: (manifest) => manifest.shots["checkout-beep"],
  },
];

test("clearing a story override cannot reuse an unknown legacy series sheet", async () => {
  const box = sandbox("fixture-story", "story");
  modelStages[0].prepare(box);
  let actual = FLASH_MODEL;
  const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }), actualImageModel: () => actual });
  const oldRun = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug, "--candidates", "1"], oldRun.ctx), EXIT.ok);
  const legacy = manifestOf(box, "characters");
  delete legacy.image_selection_version;
  writeFileSync(path.join(box.workdir, "characters", "manifest.json"), `${JSON.stringify(legacy)}\n`);
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  assert.equal(keepSheets({ workBase: box.work, workdir: box.workdir, seriesSlug: doc.series.slug, doc, manifest: legacy, chosen: { jingwei: 1 } }), 1);

  seriesImageModel(box, null);
  actual = PRO_MODEL;
  const corrected = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug, "--candidates", "1"], corrected.ctx), EXIT.ok, corrected.out.stderr);
  assert.equal(site.state.images.length, 2, "a cleared override still requires trustworthy series-store provenance");
  assert.equal(site.state.judges.length, 2);
  const manifest = manifestOf(box, "characters");
  assert.equal(manifest.image.model, PRO_MODEL);
  assert.equal(manifest.image_selection_version, 1);
  assert.equal(manifest.characters.jingwei.reused, undefined);
});

test("media-status resolves the named series image model without changing the unscoped default", async () => {
  const box = sandbox("fixture-story", "story");
  seriesImageModel(box, FLASH_MODEL);
  const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }) });
  const scoped = context(box, site.fetchImpl);
  assert.equal(await main(["media-status", "--slug", box.slug, "--json"], scoped.ctx), EXIT.ok, scoped.out.stderr);
  const scopedStatus = JSON.parse(scoped.out.stdout);
  assert.equal(scopedStatus.status.image.model, FLASH_MODEL);
  assert.equal(imagePrice(scopedStatus.status), 0.067);
  const global = context(box, site.fetchImpl);
  assert.equal(await main(["media-status", "--json"], global.ctx), EXIT.ok, global.out.stderr);
  assert.equal(JSON.parse(global.out.stdout).status.image.model, PRO_MODEL);
  assert.equal(site.state.images.length, 0);
  assert.equal(site.state.judges.length, 0);
});

for (const stage of modelStages) {
  test(`${stage.command} dry-run prices the series Flash model while the global model remains Pro`, async () => {
    const box = sandbox("fixture-story", "story");
    stage.prepare(box);
    seriesImageModel(box, FLASH_MODEL);
    const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }), actualImageModel: () => FLASH_MODEL });
    const dry = context(box, site.fetchImpl);
    assert.equal(await main([stage.command, "--slug", box.slug, ...stage.args, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr || dry.out.stdout);
    // keyframes also says what size the pictures come at; look (character sheets) stays at 1K.
    assert.match(dry.out.stdout, /gemini gemini-3\.1-flash-image ready; (?:pictures at 1K; )?about US\$0\.08/);
    assert.equal(site.state.images.length, 0);
    assert.equal(site.state.judges.length, 0);
    assert.equal(STATUS.image.model, PRO_MODEL, "resolving one series never mutates the shared default");
  });

  test(`${stage.command} uses the series price for the cap and records its model in the ledger, cache and manifest`, async () => {
    const box = sandbox("fixture-story", "story");
    stage.prepare(box);
    seriesImageModel(box, FLASH_MODEL);
    const status = { ...STATUS, max_usd_per_video: 0.08 };
    const site = mediaSite({ status, verdicts: () => ({ overall: 8, passed: true }), actualImageModel: () => FLASH_MODEL });
    const run = context(box, site.fetchImpl);
    assert.equal(await main([stage.command, "--slug", box.slug, ...stage.args], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
    assert.equal(site.state.images.length, 1, "Flash plus its judge fits the cap; the Pro estimate would refuse it");
    assert.equal(site.state.images[0].model, undefined, "the server still owns the model choice");
    const manifest = manifestOf(box, stage.manifest);
    assert.deepEqual(manifest.image, { provider: "gemini", model: FLASH_MODEL });
    const picture = stage.picture(manifest);
    const ledger = readLedger(box.workdir);
    const image = ledger.entries.find((entry) => entry.kind === "image");
    assert.equal(image.model, FLASH_MODEL);
    assert.equal(image.provider, "gemini");
    assert.equal(image.cost_usd, 0.067);
    assert.equal(ledger.totals.usd, 0.077);
    const cached = readCache(box.workdir).entries[picture.key];
    assert.equal(cached.model, FLASH_MODEL);
    assert.equal(cached.cost_usd, 0.067);
    assert.equal(SHA(readFileSync(path.join(box.workdir, picture.file))), picture.sha256);

    const tooSmall = sandbox("fixture-story", "story");
    stage.prepare(tooSmall);
    seriesImageModel(tooSmall, FLASH_MODEL);
    const blockedSite = mediaSite({ status: { ...STATUS, max_usd_per_video: 0.06 }, verdicts: () => ({ overall: 8, passed: true }), actualImageModel: () => FLASH_MODEL });
    const blocked = context(tooSmall, blockedSite.fetchImpl);
    assert.equal(await main([stage.command, "--slug", tooSmall.slug, ...stage.args], blocked.ctx), EXIT.owner);
    assert.match(blocked.out.stderr, /next generation costs about US\$0\.07.*per-video cap/);
    assert.equal(blockedSite.state.images.length, 0, "the actual override price still enforces a smaller cap before submission");
    assert.equal(blockedSite.state.judges.length, 0);
  });

  test(`${stage.command} redraws and rejudges after Pro to Flash to Pro changes, then reuses the stable model`, async () => {
    const box = sandbox("fixture-story", "story");
    stage.prepare(box);
    let actual = PRO_MODEL;
    const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }), actualImageModel: () => actual });
    const pictures = [];
    for (const [index, model] of [PRO_MODEL, FLASH_MODEL, PRO_MODEL].entries()) {
      actual = model;
      seriesImageModel(box, model);
      const run = context(box, site.fetchImpl);
      assert.equal(await main([stage.command, "--slug", box.slug, ...stage.args], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
      assert.equal(site.state.images.length, index + 1, "a changed model must not keep an old judged manifest or an overwritten cached file");
      assert.equal(site.state.judges.length, index + 1, "each replacement image is judged");
      const manifest = manifestOf(box, stage.manifest);
      assert.deepEqual(manifest.image, { provider: "gemini", model });
      const picture = stage.picture(manifest);
      pictures.push(picture);
      assert.equal(SHA(readFileSync(path.join(box.workdir, picture.file))), picture.sha256, "a cache record must describe the bytes now at its fixed target path");
      const cached = readCache(box.workdir).entries[picture.key];
      assert.equal(cached.model, model);
      assert.equal(cached.sha256, picture.sha256);
      if (stage.command === "look" && index === 0) {
        await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "approved Pro sheet" });
      } else if (stage.command === "look" && index === 1) {
        assert.equal((await approvalState({ gate: "look", docDir: box.dir, workdir: box.workdir })).status, "stale", "the earlier Pro approval does not authorize the new Flash sheet");
      }
    }
    assert.notEqual(pictures[0].key, pictures[1].key, "model participates in the cache key");
    assert.equal(pictures[0].key, pictures[2].key, "identical Pro request has the same key, but its overwritten file had to be redrawn");
    assert.notEqual(pictures[0].sha256, pictures[1].sha256);
    assert.equal(pictures[0].sha256, pictures[2].sha256);
    assert.deepEqual(readLedger(box.workdir).entries.filter((entry) => entry.kind === "image").map((entry) => [entry.model, entry.cost_usd]), [[PRO_MODEL, 0.134], [FLASH_MODEL, 0.067], [PRO_MODEL, 0.134]]);
    const stable = context(box, site.fetchImpl);
    assert.equal(await main([stage.command, "--slug", box.slug, ...stage.args], stable.ctx), EXIT.ok, stable.out.stderr || stable.out.stdout);
    assert.equal(site.state.images.length, 3);
    assert.equal(site.state.judges.length, 3);
    assert.equal(readLedger(box.workdir).totals.images, 3, "a stable-model rerun incurs no second charge");
  });

  for (const selection of [PRO_MODEL, null]) {
    test(`${stage.command} replaces a legacy mislabeled manifest and cache when the series selection is ${selection ?? "cleared"}`, async () => {
      const box = sandbox("fixture-story", "story");
      stage.prepare(box);
      // Before the selection fix, the server could draw Flash while the worker booked Pro.
      // No image_model field keeps the legacy cache key; remove the new receipt below
      // to model a saved pre-fix manifest, whose model label was not trustworthy.
      let actual = FLASH_MODEL;
      const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }), actualImageModel: () => actual });
      const oldRun = context(box, site.fetchImpl);
      assert.equal(await main([stage.command, "--slug", box.slug, ...stage.args], oldRun.ctx), EXIT.ok, oldRun.out.stderr || oldRun.out.stdout);
      const legacy = manifestOf(box, stage.manifest);
      delete legacy.image_selection_version;
      writeFileSync(path.join(box.workdir, stage.manifest, "manifest.json"), `${JSON.stringify(legacy, null, 2)}\n`);
      const oldPicture = stage.picture(legacy);
      const oldCache = readCache(box.workdir).entries[oldPicture.key];
      assert.equal(legacy.image_selection_version, undefined);
      assert.equal(legacy.image.model, PRO_MODEL);
      assert.equal(oldCache.model, PRO_MODEL);
      assert.equal(oldCache.cost_usd, 0.067, "the mock server actually produced Flash");
      assert.equal(SHA(readFileSync(path.join(box.workdir, oldPicture.file))), oldPicture.sha256);
      assert.equal(oldCache.sha256, oldPicture.sha256, "legacy metadata and bytes agree; a file hash check alone cannot detect the wrong model label");

      seriesImageModel(box, selection);
      actual = PRO_MODEL;
      const corrected = context(box, site.fetchImpl);
      assert.equal(await main([stage.command, "--slug", box.slug, ...stage.args], corrected.ctx), EXIT.ok, corrected.out.stderr || corrected.out.stdout);
      assert.equal(site.state.images.length, 2, "matching Pro labels must not preserve the old actual-Flash image");
      assert.equal(site.state.judges.length, 2);
      const manifest = manifestOf(box, stage.manifest);
      const picture = stage.picture(manifest);
      assert.equal(manifest.image_selection_version, 1);
      assert.equal(manifest.image.model, PRO_MODEL);
      assert.notEqual(picture.key, oldPicture.key, "the corrected model-selection namespace cannot hit the legacy image cache");
      assert.notEqual(picture.sha256, oldPicture.sha256, "the replacement is a real Pro image");
      assert.equal(SHA(readFileSync(path.join(box.workdir, picture.file))), picture.sha256);
      const cached = readCache(box.workdir).entries[picture.key];
      assert.equal(cached.model, PRO_MODEL);
      assert.equal(cached.cost_usd, 0.134);
      const images = readLedger(box.workdir).entries.filter((entry) => entry.kind === "image");
      assert.equal(images.length, 2, "the old charge remains in history");
      assert.equal(images[1].model, PRO_MODEL);
      assert.equal(images[1].cost_usd, 0.134);

      const stable = context(box, site.fetchImpl);
      assert.equal(await main([stage.command, "--slug", box.slug, ...stage.args], stable.ctx), EXIT.ok, stable.out.stderr || stable.out.stdout);
      assert.equal(site.state.images.length, 2, "a corrected stable-model rerun keeps the new image");
      assert.equal(site.state.judges.length, 2);
    });
  }
}

test("illustrated slides draw their stills with no look gate, bound to the shots rather than the cards, and judged without a subtitle band", async () => {
  const { illustratedFixture } = await import("../core/fixtures/load.mjs");
  const { picturesHash } = await import("../core/drama.mjs");
  const box = sandbox("fixture-illustrated", "illustrated");
  // The site draws slides pictures under their own switch and model once it has them; the drama route may be off.
  const status = { ...STATUS, enabled: false, slides_enabled: true, slides_image: { provider: "gemini", model: "gemini-3.1-flash-image", configured: true }, slides_max_usd_per_video: 20, models: { ...STATUS.models, images: { gemini: [...STATUS.models.images.gemini, { value: "gemini-3.1-flash-image", label: "Flash", description: null, status: "stable", resolutions: [], durations: [], reference_images: 5, native_audio: false, usd_per_second: null, usd_per_image: 0.067, usd_per_track: null }] } } };
  const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }), status });
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  // One style plate before the five shots (docs/videos/ILLUSTRATED.md §第二輪): 6 × (0.067 + 0.01).
  assert.match(dry.out.stdout, /keyframes for 5 shots \(0 end frames\), up to 3 takes each, after one style plate\n/);
  assert.match(dry.out.stdout, /references: style plate\n/);
  assert.match(dry.out.stdout, /gemini gemini-3\.1-flash-image ready; pictures at 1K; about US\$0\.46 for one take of everything, up to US\$1\.39 at 3 takes; this video so far US\$0\.00 of the US\$20 cap/);
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  const doc = illustratedFixture();
  const shots = doc.scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id);
  assert.deepEqual(site.state.images.map((request) => request.shot_id), [STYLE_PLATE_ID, ...shots]);
  // The plate is the look on a neutral daylight scene, drawn with no reference; every shot is then
  // drawn with the plate as its style reference and judged beside it.
  assert.match(site.state.images[0].prompt, new RegExp(`^${STYLE_PLATE_PROMPT.slice(0, 40)}.*Style: hand-drawn editorial illustration for a printed magazine feature`));
  assert.equal(site.state.images[0].purpose, "style_frame");
  assert.deepEqual(site.state.images[0].references, []);
  const plate = readJson(path.join(box.workdir, "keyframes", "plate.json"));
  assert.equal(plate.look_hash, lookHash(doc));
  assert.equal(plate.file, "keyframes/plate-1.png");
  assert.ok(existsSync(path.join(box.workdir, plate.file)));
  assert.match(run.out.stdout, /style plate take 1: judge 8\/10\n/);
  assert.ok(site.state.uploads.some((upload) => upload.sha256 === plate.sha256), "the plate is put in the store before the shots use it");
  for (const request of site.state.images.slice(1)) assert.deepEqual(request.references, [{ sha256: plate.sha256, role: "style" }]);
  assert.match(site.state.images[1].prompt, /Style: hand-drawn editorial illustration for a printed magazine feature/);
  assert.ok(site.state.images.every((request) => request.size === undefined), "a choice priced at 1K only is drawn at 1K");
  assert.ok(site.state.judges.every((request) => !request.rubric.some((item) => item.key === "subtitle_band" || item.key.startsWith("identity_"))), "CC only: no subtitle band; no cast: no identity question");
  assert.ok(site.state.judges.every((request) => request.rubric.some((item) => item.key === "craft")), "no cast: the picture is judged as craft, drawn by a hand rather than rendered");
  assert.match(site.state.judges[0].rubric.find((item) => item.key === "style").question, /style description in the context/);
  for (const request of site.state.judges.slice(1)) {
    assert.deepEqual(request.files.map((each) => each.label), ["keyframe", "style plate"]);
    assert.match(request.rubric.find((item) => item.key === "style").question, /labelled "style plate", as if by the same hand/);
  }
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.look_hash, lookHash(doc));
  assert.equal(manifest.pictures_hash, picturesHash(doc));
  assert.equal(manifest.visual_hash, undefined);
  assert.deepEqual(manifest.image, { provider: "gemini", model: "gemini-3.1-flash-image" });
  assert.deepEqual(manifest.plate, { file: plate.file, sha256: plate.sha256, seed: 1, judge: plate.judge });
  assert.equal(readLedger(box.workdir).totals.images, shots.length + 1);
  assert.match(run.out.stdout, new RegExp(`${shots.length + 1} keyframes generated in`));
  // A card edit keeps every picture; a camera edit redraws that shot alone, from the same plate.
  const file = path.join(box.dir, "video.json");
  const edited = JSON.parse(readFileSync(file, "utf8"));
  edited.scenes[0].data.title = "另一個標題";
  writeFileSync(file, JSON.stringify(edited));
  const kept = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], kept.ctx), EXIT.ok, kept.out.stderr);
  assert.equal(site.state.images.length, shots.length + 1, "nothing redrawn for a card's text");
  assert.match(kept.out.stdout, /style plate: kept \(judge 8\/10\)\n/);
  edited.scenes[1].data.camera = "pan left";
  writeFileSync(file, JSON.stringify(edited));
  const redrawn = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], redrawn.ctx), EXIT.ok, redrawn.out.stderr);
  assert.equal(site.state.images.length, shots.length + 2, "a new binding walks every shot again; the cache answers the unchanged ones without the server");
  assert.deepEqual(site.state.images.at(-1).references, [{ sha256: plate.sha256, role: "style" }], "the plate outlives a prompt edit: it is bound to the look, not to the pictures");
  assert.equal(readLedger(box.workdir).totals.images, shots.length + 2, "only the shot with the new camera is paid for");
  // A new look draws a new plate, and with it every picture.
  edited.look = { preset: "flat-explainer" };
  writeFileSync(file, JSON.stringify(edited));
  const relooked = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], relooked.ctx), EXIT.ok, relooked.out.stderr);
  assert.equal(site.state.images.length, shots.length + 2 + 1 + shots.length);
  const second = readJson(path.join(box.workdir, "keyframes", "plate.json"));
  assert.notEqual(second.sha256, plate.sha256);
  assert.equal(second.look_hash, lookHash(edited));
  // An owner's own style frames stand in for the plate.
  const framed = sandbox("fixture-illustrated-framed", "illustrated");
  const framedDoc = JSON.parse(readFileSync(path.join(framed.dir, "video.json"), "utf8"));
  writeFileSync(path.join(framed.dir, "frame.png"), PNG("owner's frame"));
  framedDoc.look = { preset: "tech-story", style_frames: ["frame.png"] };
  writeFileSync(path.join(framed.dir, "video.json"), JSON.stringify(framedDoc));
  const framedSite = mediaSite({ verdicts: () => ({ overall: 8, passed: true }), status });
  const framedRun = context(framed, framedSite.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", framed.slug], framedRun.ctx), EXIT.ok, framedRun.out.stderr);
  assert.deepEqual(framedSite.state.images.map((request) => request.shot_id), shots, "no plate when the look has frames");
  assert.ok(framedSite.state.images.every((request) => request.references.length === 1 && request.references[0].role === "style"));
  assert.ok(!existsSync(path.join(framed.workdir, "keyframes", "plate.json")));
  // The drama keeps its subtitle band and its binding to the whole picture.
  assert.ok(keyframeRubric([]).some((item) => item.key === "subtitle_band"));
  assert.ok(!keyframeRubric([], { subtitleBand: false }).some((item) => item.key === "subtitle_band"));
  assert.match(keyframeRubric([]).find((item) => item.key === "style").question, /style description in the context/);
  assert.match(keyframeRubric([{ id: "a", name: "A" }]).find((item) => item.key === "style").question, /reference sheets/);
  // Craft is the caller's word about the video, never inferred from a shot having no cast: an
  // empty establishing shot of a 3D drama is not judged as a print illustration.
  assert.ok(!keyframeRubric([]).some((item) => item.key === "craft"));
  assert.ok(!keyframeRubric([{ id: "a", name: "A" }]).some((item) => item.key === "craft"));
  assert.deepEqual(keyframeRubric([], { subtitleBand: false, craft: true }).map((item) => item.key), ["prompt", "style", "craft", "clean", "no_text"]);
  assert.match(keyframeRubric([], { craft: true }).find((item) => item.key === "craft").question, /made by a person for print, not generated.*no glossy, airbrushed, glowing or rendered finish/);
  assert.match(keyframeRubric([], { craft: true }).find((item) => item.key === "clean").question, /filling the whole frame with no bars, borders, margins or blurred side panels/);
  // The server takes a rubric question of at most 400 characters (schemas.py RubricItem).
  for (const item of keyframeRubric([{ id: "a", name: "A", shot_look: "wet", appearance: "x".repeat(120) }], { craft: true, plate: true })) assert.ok(item.question.length <= 400, `${item.key}: ${item.question.length} characters`);
  // With the drama route on and no slides fields, slides draw as a drama does.
  assert.equal(statusProblem({ ...STATUS }, "image", "slides"), null);
  assert.match(statusProblem({ ...STATUS, enabled: false }, "image", "slides"), /pictures for slides videos are off/);
  assert.equal(imagePrice(status, "slides"), 0.067);
  assert.equal(imagePrice(status), 0.134, "a drama keeps the global model");
});

test("a paper margin is cut off a still: the manifest, the plate's reference and the next shots use the trimmed copy, the judge saw the picture whole", async () => {
  const box = sandbox("fixture-illustrated", "illustrated");
  const status = { ...STATUS, enabled: false, slides_enabled: true, slides_image: { provider: "gemini", model: "gemini-3.1-flash-image", configured: true }, slides_max_usd_per_video: 20, models: { ...STATUS.models, images: { gemini: [...STATUS.models.images.gemini, { value: "gemini-3.1-flash-image", label: "Flash", description: null, status: "stable", resolutions: [], durations: [], reference_images: 5, native_audio: false, usd_per_second: null, usd_per_image: 0.067, usd_per_track: null }] } } };
  const site = mediaSite({ verdicts: () => ({ overall: 8, passed: true }), status });
  const trimmed = [];
  const trimImage = async (file) => {
    // Only the plate and the first shot came back with a margin.
    if (!/plate-1|podium-1/.test(file)) return null;
    const out = file.replace(/\.png$/, "-trim.png");
    writeFileSync(path.join(box.workdir, out), PNG(`trimmed ${file}`));
    trimmed.push(file);
    return { file: out, sha256: SHA(PNG(`trimmed ${file}`)), margins: { top: 2.1, bottom: 2.1, left: 1.6, right: 1.6 } };
  };
  const run = context(box, site.fetchImpl, { trimImage });
  assert.equal(await main(["keyframes", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.deepEqual(trimmed, ["keyframes/plate-1.png", "keyframes/podium-1.png"]);
  assert.match(run.out.stdout, /style-plate: trimmed a 2\.1% paper margin\n/);
  assert.match(run.out.stdout, /podium: trimmed a 2\.1% paper margin\n/);
  const plate = readJson(path.join(box.workdir, "keyframes", "plate.json"));
  assert.equal(plate.file, "keyframes/plate-1-trim.png");
  assert.equal(plate.sha256, SHA(PNG("trimmed keyframes/plate-1.png")));
  assert.deepEqual(plate.takes[0].margins, { top: 2.1, bottom: 2.1, left: 1.6, right: 1.6 });
  // The judge was sent the picture as the server drew it; the shots reference the trimmed plate.
  assert.notEqual(site.state.judges[0].files[0].sha256, plate.sha256);
  assert.ok(site.state.uploads.some((upload) => upload.sha256 === plate.sha256), "the trimmed plate is put in the store");
  for (const request of site.state.images.slice(1)) assert.deepEqual(request.references, [{ sha256: plate.sha256, role: "style" }]);
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.shots.podium.file, "keyframes/podium-1-trim.png");
  assert.equal(manifest.shots.podium.sha256, SHA(PNG("trimmed keyframes/podium-1.png")));
  assert.deepEqual(manifest.shots.podium.margins, { top: 2.1, bottom: 2.1, left: 1.6, right: 1.6 });
  assert.equal(manifest.shots.desk.file, "keyframes/desk-1.png", "a picture with no margin is used as it came");
  assert.equal(manifest.shots.desk.margins, undefined);
  assert.deepEqual(manifest.plate, { file: plate.file, sha256: plate.sha256, seed: 1, judge: plate.judge });
  // A rerun keeps the trimmed copies without asking the server or the trimmer again.
  const again = context(box, site.fetchImpl, { trimImage });
  assert.equal(await main(["keyframes", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(trimmed.length, 2);
  assert.match(again.out.stdout, /podium: kept \(judge 8\/10\)\n/);
});

// The site as it serves illustrated slides: their own switch and model, the drama route off.
const SLIDES_STATUS = { ...STATUS, enabled: false, slides_enabled: true, slides_image: { provider: "gemini", model: FLASH_MODEL, configured: true }, slides_max_usd_per_video: 20 };

test("a shot keeps its best take, and an entry stands only while its requests and its question are the same", () => {
  const take = (seed, overall, passed = false) => ({ seed, key: `k${seed}`, judge: { overall, passed }, judged: "q1" });
  assert.equal(bestTake([take(1, 6.5), take(2, 6.9), take(3, 6.2)]).seed, 2, "none passed: the highest score, not the last seed");
  assert.equal(bestTake([take(1, 6.9), take(2, 6.9)]).seed, 1, "a tie goes to the earlier seed");
  assert.equal(bestTake([take(1, 7.4, true), take(2, 9.9), take(3, 7.1, true)]).seed, 3, "a take that passed beats a higher score that did not, the latest of them first");
  assert.equal(bestTake([]), null);

  const keys = { take: (seed) => `k${seed}`, end: null };
  const failed = { needs_review: true, takes: [take(1, 6.5), take(2, 6.9)] };
  const passed = { needs_review: false, takes: [take(1, 6.5), take(2, 8, true)] };
  assert.ok(entryStands(failed, { keys, stamp: "q1" }), "a shot that has not passed keeps its verdicts too: the same pictures are not asked about twice");
  assert.ok(entryStands(passed, { keys, stamp: "q1" }));
  assert.ok(!entryStands(passed, { keys, stamp: "q2" }), "another rubric, another context or another bar is another question");
  assert.ok(!entryStands(passed, { keys: { ...keys, take: (seed) => `other${seed}` }, stamp: "q1" }), "another prompt, camera, look or reference is another picture");
  assert.ok(!entryStands(passed, { keys: { ...keys, end: "e1" }, stamp: "q1" }), "an end frame the shot now asks for is still to draw");
  assert.ok(!entryStands({ ...passed, end_frame: { key: "e0" } }, { keys: { ...keys, end: "e1" }, stamp: "q1" }), "a changed end frame");
  assert.ok(entryStands({ ...passed, end_frame: { key: "e1" } }, { keys: { ...keys, end: "e1" }, stamp: "q1" }));
  assert.ok(!entryStands({ takes: [] }, { keys, stamp: "q1" }));
  assert.ok(!entryStands(undefined, { keys, stamp: "q1" }));
  // Takes from before verdicts carried a stamp: a pass stands, a failure is asked about again.
  const unstamped = (entry) => ({ ...entry, takes: entry.takes.map(({ judged: _judged, ...rest }) => rest) });
  assert.ok(entryStands(unstamped(passed), { keys, stamp: "q1" }));
  assert.ok(!entryStands(unstamped(failed), { keys, stamp: "q1" }));
});

test("the fix clauses of the judge's problems: after the arrow, each once, the server's placeholder left out; the next take is asked with the ones before it", () => {
  assert.equal(PLACEHOLDER_FIX, "write the correction into the prompt", "spelled as apps/api/app/video_media/judge.py spells it");
  const problems = [
    `clean: six fingers on the left hand${FIX_ARROW}the left hand with five fingers`,
    `subject: no bird in the frame${FIX_ARROW}a white gull in the middle third of the frame`,
    `text: the sign reads CAFE${FIX_ARROW}${PLACEHOLDER_FIX}`,
    "a line with no arrow",
    `clean: six fingers on the left hand${FIX_ARROW}the left hand with five fingers`,
  ];
  assert.deepEqual(fixClauses(problems), ["the left hand with five fingers", "a white gull in the middle third of the frame"]);
  assert.deepEqual(fixClauses([]), []);
  assert.deepEqual(fixClauses(undefined), []);
  assert.equal(retakePrompt("a gull over the sea. Style: ink", []), "a gull over the sea. Style: ink", "no fix, the prompt as written");
  assert.equal(retakePrompt("a gull over the sea. Style: ink", ["a white gull", "no lettering"]), "a gull over the sea. Style: ink. Corrections: a white gull; no lettering");
  assert.equal(retakePrompt("x".repeat(3990), ["y".repeat(50)]).length, 4000, "the server's prompt limit");
  const takes = [
    { seed: 2, judge: { problems: [`clean: a${FIX_ARROW}fix two`] } },
    { seed: 1, judge: { problems: [`clean: b${FIX_ARROW}fix one`] } },
    { seed: 3, judge: { problems: [`clean: c${FIX_ARROW}fix three`] } },
    { seed: 4 },
  ];
  assert.deepEqual(fixesBefore(takes, 1), []);
  assert.deepEqual(fixesBefore(takes, 3), ["fix one", "fix two"], "in seed order, whatever the order recorded");
  assert.deepEqual(fixesBefore(takes, 5), ["fix one", "fix two", "fix three"], "a take with no verdict has no fix");
  assert.deepEqual(fixesBefore(undefined, 2), []);
});

test("a failed take's fixes go into the next take's prompt, stand with the shot over a prompt edit elsewhere, and are the hint left for the prompt fix", async () => {
  const box = sandbox("fixture-illustrated", "illustrated");
  // The desk never passes. Each picture gets a fix named after it (a judge asked twice about the
  // same picture says the same thing), beside one line the judge gave no fix for.
  const site = mediaSite({
    status: SLIDES_STATUS,
    verdicts: (kind, request) => {
      if (request.context.shot.id !== "desk") return { overall: 9, passed: true };
      const picture = request.files[0].sha256.slice(0, 6);
      return { overall: 6.5, passed: false, problems: [`subject: the desk is bare in ${picture}${FIX_ARROW}a ledger open on the desk (${picture})`, `text: a label on the drawer reads TEA${FIX_ARROW}${PLACEHOLDER_FIX}`] };
    },
  });
  const first = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], first.ctx), EXIT.lint, first.out.stderr);
  const asked = site.state.images.filter((request) => request.shot_id === "desk");
  assert.equal(asked.length, 3);
  const fixes = site.state.judges.filter((request) => request.context.shot.id === "desk").map((request) => `a ledger open on the desk (${request.files[0].sha256.slice(0, 6)})`);
  assert.equal(new Set(fixes).size, 3, "three pictures, three fixes");
  assert.doesNotMatch(asked[0].prompt, /Corrections/);
  assert.equal(asked[1].prompt, `${asked[0].prompt}. Corrections: ${fixes[0]}`);
  assert.equal(asked[2].prompt, `${asked[0].prompt}. Corrections: ${fixes[0]}; ${fixes[1]}`, "each take carries the fixes of every take before it");
  assert.ok(asked.every((request) => !request.prompt.includes(PLACEHOLDER_FIX)), "the server's placeholder is a note to the writer, not prompt text");
  const manifest = manifestOf(box, "keyframes");
  assert.deepEqual(manifest.shots.desk.takes.map((take) => take.fixes), [undefined, [fixes[0]], [fixes[0], fixes[1]]]);
  assert.deepEqual(manifest.shots.desk.fixes, fixes, "the hint for the prompt fix: every fix the judge gave");
  assert.equal(manifest.shots.desk.problems.length, 4, "three lines with a fix of their own, and the one without, once");
  assert.ok(first.out.stdout.includes(`desk take 2: asked with the corrections of the takes before: ${fixes[0]}\n`), first.out.stdout);
  assert.ok(first.out.stdout.includes(`desk take 3: asked with the corrections of the takes before: ${fixes[0]}; ${fixes[1]}\n`));
  assert.match(first.out.stdout, /ERROR desk: no take passed the judge: subject: the desk is bare/);
  assert.ok(first.out.stdout.includes(`  fixes for desk: ${fixes.join("; ")}\nfix the prompts of desk and run keyframes again`));

  // Another shot's prompt changes: the desk's takes, asked with their corrections, stand as they
  // were (their keys are recomputed with the same fixes), and nothing of the desk is asked again.
  const drawn = site.state.images.length;
  const judged = site.state.judges.length;
  rewrite(box, (each) => {
    each.scenes.find((scene) => scene.id === "race").data.prompt += ", a groundskeeper raking the pit";
  });
  const edited = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], edited.ctx), EXIT.lint, edited.out.stderr);
  assert.match(edited.out.stdout, /4 of 5 drawn shots are unchanged and keep their verdicts\n/);
  assert.equal(site.state.images.length, drawn + 1, "the race alone is drawn");
  assert.equal(site.state.judges.length, judged + 1);
  assert.deepEqual(manifestOf(box, "keyframes").shots.desk.fixes, fixes);
  // Nothing changed: nothing is drawn or judged.
  const again = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], again.ctx), EXIT.lint, again.out.stderr);
  assert.equal(site.state.images.length, drawn + 1);
  assert.equal(site.state.judges.length, judged + 1);
});

test("a prompt edit sends that shot alone back to the judge: the others keep their takes and verdicts, and a shot that never passed keeps its best take", async () => {
  const { picturesHash } = await import("../core/drama.mjs");
  const box = sandbox("fixture-illustrated", "illustrated");
  // The desk never passes: 6.5, then 6.9, then 6.2, each time it is asked about.
  const desk = [6.5, 6.9, 6.2];
  const site = mediaSite({
    status: SLIDES_STATUS,
    verdicts: (kind, request) => {
      if (request.context.shot.id !== "desk") return { overall: 9, passed: true };
      const nth = site.state.judges.filter((each) => each.context.shot.id === "desk").length;
      return { overall: desk[(nth - 1) % desk.length], passed: false, problems: [`desk fault ${nth}`] };
    },
  });
  const first = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], first.ctx), EXIT.lint, first.out.stderr);
  let manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.shots.desk.needs_review, true);
  assert.equal(manifest.shots.desk.seed, 2, "the best-scoring take is the one kept, not the last");
  assert.equal(manifest.shots.desk.file, "keyframes/desk-2.png");
  assert.equal(manifest.shots.desk.judge.overall, 6.9);
  assert.deepEqual(manifest.shots.desk.problems, ["desk fault 1", "desk fault 2", "desk fault 3"]);
  const drawn = site.state.images.length;
  const judged = site.state.judges.length;
  assert.equal(judged, 8, "the plate, four shots once and the desk three times");
  assert.ok(site.state.judges.every((request) => request.min_score === undefined), "the bar is the owner's setting; the tool never sends one of its own");
  assert.ok(Object.values(manifest.shots).every((shot) => shot.takes.every((each) => /^[0-9a-f]{16}$/.test(each.judged))), "every verdict records the question it answered");

  // One prompt changes: one picture and one judge call. Before, every cached take went back to
  // the judge (US$0.01 each, and a passed picture could fail on the second asking).
  const doc = rewrite(box, (each) => {
    each.scenes.find((scene) => scene.id === "race").data.prompt += ", a groundskeeper raking the long-jump pit behind them";
  });
  const edited = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], edited.ctx), EXIT.lint, edited.out.stderr);
  assert.match(edited.out.stdout, /4 of 5 drawn shots are unchanged and keep their verdicts\n/);
  assert.match(edited.out.stdout, /podium: kept \(judge 9\/10\)\n/);
  assert.equal(site.state.images.length, drawn + 1);
  assert.equal(site.state.judges.length, judged + 1, "the four unchanged shots are not judged again, the one that failed included");
  assert.equal(site.state.judges.at(-1).context.shot.id, "race");
  assert.equal(readLedger(box.workdir).totals.judge_calls, judged + 1);
  manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.pictures_hash, picturesHash(doc));
  assert.equal(manifest.shots.desk.takes.length, 3);
  assert.equal(manifest.shots.desk.seed, 2);
  assert.equal(manifest.shots.desk.needs_review, true, "a failed shot is still waiting for its prompt fix");

  // A manifest written before verdicts were stamped: a shot that passed keeps its verdict over a
  // prompt edit, a shot that had not is asked about again (its pictures come from the cache).
  const file = path.join(box.workdir, "keyframes", "manifest.json");
  for (const shot of Object.values(manifest.shots)) for (const take of shot.takes) delete take.judged;
  writeFileSync(file, JSON.stringify(manifest));
  rewrite(box, (each) => {
    each.scenes.find((scene) => scene.id === "door").data.prompt += ", a bicycle leaning under the stairs";
  });
  const legacy = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], legacy.ctx), EXIT.lint, legacy.out.stderr);
  assert.match(legacy.out.stdout, /3 of 5 drawn shots are unchanged and keep their verdicts\n/);
  assert.equal(site.state.images.length, drawn + 2, "only the door is drawn; the desk's three pictures are in the cache");
  assert.equal(site.state.judges.length, judged + 1 + 1 + 3);
  assert.ok(manifestOf(box, "keyframes").shots.desk.takes.every((take) => take.judged), "asked again, the desk's verdicts are stamped");

  // --force is the owner asking for every verdict again.
  const forced = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--force"], forced.ctx), EXIT.lint, forced.out.stderr);
  assert.doesNotMatch(forced.out.stdout, /keep their verdicts/);
  assert.equal(site.state.judges.length, judged + 1 + 1 + 3 + 8, "the plate and every take of every shot");
});

test("illustrated slides are judged by yes/no fault checks once the server takes them, and a shot that failed on the old question is asked again", async () => {
  const REDRAW = ["text", "anatomy", "detached", "subject", "frame", "style"];
  const checks = keyframeChecks({ plate: true });
  assert.deepEqual(checks.map((item) => item.key), [...REDRAW, "details", "awkward", "generated"]);
  assert.deepEqual(checks.filter((item) => item.cost === 10).map((item) => item.key), REDRAW, "these faults leave the criterion at 0, under the server's floor of 4");
  assert.ok(checks.every((item) => item.cost > 0 && item.cost <= 10 && item.question.length <= 400 && /^[a-z][a-z0-9_]{0,39}$/.test(item.key)));
  assert.ok(checks.filter((item) => item.cost < 10).every((item) => 10 - item.cost >= 4), "a second-look flaw alone never fails a take");
  assert.match(checks.find((item) => item.key === "style").question, /labelled "style plate"/);
  assert.match(keyframeChecks().find((item) => item.key === "style").question, /the style the context describes/);
  assert.match(checks.find((item) => item.key === "anatomy").question, /more than five.*hidden or left out by the style does not count/);
  // What the server computes from the answers (apps/api/app/video_media/judge.py), so the bar keeps its meaning.
  const total = checks.reduce((sum, item) => sum + item.weight, 0);
  const overall = (...faults) => Math.round((checks.reduce((sum, item) => sum + (faults.includes(item.key) ? 10 - item.cost : 10) * item.weight, 0) / total) * 100) / 100;
  assert.equal(overall(), 10, "nothing found is the top of the scale");
  assert.deepEqual([overall("details"), overall("generated"), overall("awkward")], [9.29, 8.59, 7.88]);
  assert.deepEqual([overall("awkward", "details"), overall("generated", "details")], [7.18, 7.88], "at a bar of 7 one flaw beside a missed detail passes");
  assert.equal(overall("awkward", "generated"), 6.47, "awkward and generated-looking together do not");

  // A server that does not take checks yet is asked for scores, as before.
  const box = sandbox("fixture-illustrated", "illustrated");
  const status = { ...SLIDES_STATUS, limits: {} };
  let verdicts = (kind, request) => (request.context.shot.id === "desk" ? { overall: 6.9, passed: false, problems: ["a remark"] } : { overall: 7, passed: true });
  const site = mediaSite({ status, verdicts: (...args) => verdicts(...args) });
  const scored = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], scored.ctx), EXIT.lint, scored.out.stderr);
  assert.ok(site.state.judges.every((request) => request.rubric.every((item) => item.cost === undefined) && request.rubric.some((item) => item.key === "craft")));
  const drawn = site.state.images.length;
  const judged = site.state.judges.length;
  assert.equal(judged, 8, "the plate, four shots once and the desk three times");

  // The server now takes checks. The shots that passed keep their verdicts; the desk failed on a
  // question that is no longer the one asked, so its first take is asked about again from the
  // cached picture, with stamped verdicts and with ones from before the stamps alike.
  status.limits = { judge_checks: 1 };
  verdicts = () => ({ overall: 9.29, passed: true, problems: ["the lamp is on the left"] });
  const file = path.join(box.workdir, "keyframes", "manifest.json");
  const before = readJson(file);
  delete before.shots.desk.takes[1].judged;
  writeFileSync(file, JSON.stringify(before));
  const checked = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug], checked.ctx), EXIT.ok, checked.out.stderr);
  assert.equal(site.state.images.length, drawn, "nothing is drawn again");
  assert.equal(site.state.judges.length, judged + 1, "one call: the desk's first take passes on the question as it is asked now");
  assert.match(checked.out.stdout, /desk take 1: judge 9\.29\/10 \(reused\)\n/);
  const asked = site.state.judges.at(-1);
  assert.equal(asked.context.shot.id, "desk");
  assert.deepEqual(asked.rubric, keyframeChecks({ plate: true }));
  assert.deepEqual(asked.files.map((each) => each.label), ["keyframe", "style plate"]);
  assert.equal(asked.min_score, undefined);
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.shots.desk.needs_review, false);
  assert.equal(manifest.shots.desk.seed, 1);
  assert.deepEqual(manifest.shots.desk.takes.map((take) => [take.seed, take.judge.overall]), [[1, 9.29], [2, 6.9], [3, 6.9]], "one entry a seed, in seed order");
  assert.notEqual(manifest.shots.desk.takes[0].judged, before.shots.desk.takes[0].judged, "the stamp is of the question asked");
  assert.equal(manifest.shots.podium.judge.overall, 7, "a shot that passed is kept as it was");

  // From the start on such a server the plate is checked too, against the look's description.
  const fresh = sandbox("fixture-illustrated", "illustrated");
  const freshSite = mediaSite({ status, verdicts: () => ({ overall: 10, passed: true }) });
  const run = context(fresh, freshSite.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", fresh.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.deepEqual(freshSite.state.judges[0].rubric, keyframeChecks());
  assert.equal(freshSite.state.judges[0].context.shot.id, STYLE_PLATE_ID);
  for (const request of freshSite.state.judges.slice(1)) assert.deepEqual(request.rubric, keyframeChecks({ plate: true }));

  // A drama's pictures are scored on the rubric whatever the server can do: only illustrated slides were measured.
  const story = sandbox("fixture-story", "story");
  writeFileSync(path.join(story.dir, "style-anchor.png"), PNG("style anchor"));
  rewrite(story, (doc) => {
    doc.look.style_frames = ["style-anchor.png"];
  });
  const storySite = mediaSite({ status: { ...STATUS, limits: { judge_checks: 1 } }, verdicts: () => ({ overall: 8, passed: true }) });
  const told = context(story, storySite.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", story.slug], told.ctx), EXIT.ok, told.out.stderr);
  assert.ok(storySite.state.judges.length > 0 && storySite.state.judges.every((request) => request.rubric.every((item) => item.cost === undefined)));
});
