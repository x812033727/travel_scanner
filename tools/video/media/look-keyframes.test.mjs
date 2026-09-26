import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { approve, readApprovals } from "../core/approvals.mjs";
import { lookHash } from "../core/drama.mjs";
import { dramaFixture, sandbox } from "../core/fixtures/load.mjs";
import { readLedger } from "./ledger.mjs";
import { chosenSheets, keyframeRubric, MAX_KEYFRAME_TAKES, shotPrompt } from "./keyframes.mjs";
import { DEFAULT_SHEET_PROMPT, MAX_LOOK_ROUNDS, optionKey, parseChoice, sheetPrompt, suggestedOf } from "./look.mjs";
import { imagePrice, statusProblem } from "./stages.mjs";

const TOKEN = `mkv_${"m".repeat(43)}`;
const SHA = (data) => createHash("sha256").update(data).digest("hex");
const PNG = (text) => Buffer.concat([Buffer.from("\x89PNG\r\n\x1a\n", "binary"), Buffer.from(text)]);

const STATUS = {
  enabled: true,
  music_enabled: true,
  image: { provider: "gemini", model: "gemini-3-pro-image", configured: true },
  clip: { provider: "gemini", model: "omni", configured: true, resolution: "1080p", seconds: 8 },
  music: { provider: "gemini", model: "lyria", configured: true },
  models: { images: { gemini: [{ value: "gemini-3-pro-image", label: "Pro", description: null, status: "stable", resolutions: [], durations: [], reference_images: 14, native_audio: false, usd_per_second: null, usd_per_image: 0.134, usd_per_track: null }] }, clips: {}, music: {} },
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
 */
function mediaSite({ verdicts, status = STATUS }) {
  const state = { images: [], judges: [], uploads: [], files: new Map() };
  const fetchImpl = async (url, init = {}) => {
    const { pathname, search } = new URL(url);
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const route = pathname.replace("/api/video/media/", "");
    if (init.method === "GET" && route === "status") return Response.json(status);
    if (init.method === "POST" && route === "images") {
      const request = JSON.parse(init.body);
      state.images.push(request);
      const bytes = PNG(`${request.prompt}|${request.seed ?? ""}|${(request.references ?? []).map((reference) => reference.sha256).join(",")}`);
      state.files.set(SHA(bytes), bytes);
      return Response.json({ id: `img${state.images.length}`, status: "ready", file: { sha256: SHA(bytes), size: bytes.length, content_type: "image/png" }, usd_estimate: 0.134, error: null, retry_after_seconds: 0 }, { status: 200 });
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

test("a character no sheet passes gets a second round, then the owner is told", async () => {
  const box = sandbox("fixture-drama", "drama");
  const site = mediaSite({ verdicts: (kind, request) => (request.context.character.name === "炎帝" ? { overall: 4, passed: false, problems: ["wrong crown"] } : { overall: 8, passed: true }) });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug], run.ctx), EXIT.lint, run.out.stderr);
  const manifest = manifestOf(box, "characters");
  assert.equal(manifest.characters.yandi.candidates.length, 3 * MAX_LOOK_ROUNDS);
  assert.deepEqual(manifest.characters.yandi.candidates.map((candidate) => candidate.seed), [1, 2, 3, 101, 102, 103]);
  assert.equal(manifest.characters.yandi.needs_review, true);
  assert.equal(manifest.characters.jingwei.candidates.length, 3, "a character with a passed sheet gets no second round");
  assert.match(run.out.stdout, /ERROR yandi: no candidate passed the judge: wrong crown/);
});

test("keyframes need the approved look, draw each shot from the chosen sheets, retake failures and warn on look-alikes", async () => {
  const box = sandbox("fixture-drama", "drama");
  let sheets = 0;
  const site = mediaSite({
    verdicts: (kind, request) => {
      if (kind === "look") return { overall: 8 + ((sheets += 1) % 2), passed: true };
      // The storm's first take fails; everything else passes.
      const stormTakes = site.state.judges.filter((each) => each.kind === "keyframe" && each.context.shot.id === "sea-storm").length;
      return request.context.shot.id === "sea-storm" && stormTakes === 1 ? { overall: 5, passed: false, problems: ["the girl faces the wrong way"] } : { overall: 8, passed: true };
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
  assert.equal(manifest.shots["sea-storm"].needs_review, false);
  assert.equal(manifest.shots["sea-storm"].file, "keyframes/sea-storm-2.png");
  assert.equal(manifest.thumbnail_source, "keyframes/sea-storm-2.png");
  assert.deepEqual(manifest.duplicates, []);
  assert.ok(existsSync(path.join(box.workdir, "keyframes", "contact-sheet.png")));
  assert.match(run.out.stdout, /next: node tools\/video\/cli\.mjs review-push --slug fixture-drama --gate storyboard/);

  const again = context(box, site.fetchImpl, { hashImage: async () => "0".repeat(16) });
  assert.equal(await main(["keyframes", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(site.state.images.length, imagesBefore + 5, "drawn shots are kept");
  assert.equal(manifestOf(box, "keyframes").duplicates.length, 3, "four identical hashes are three look-alike pairs");
  assert.match(again.out.stdout, /WARN shots opening and farewell look alike/);
});

test("a shot that never passes is left for a prompt fix after the last take", async () => {
  const box = sandbox("fixture-drama", "drama");
  const site = mediaSite({ verdicts: (kind, request) => (kind === "keyframe" && request.context.shot.id === "bird" ? { overall: 3, passed: false, problems: ["no bird"] } : { overall: 9, passed: true }) });
  await main(["look", "--slug", box.slug], context(box, site.fetchImpl).ctx);
  await main(["look", "--slug", box.slug, "--choose", "jingwei=1,yandi=1"], context(box, site.fetchImpl).ctx);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--shot", "bird,opening"], run.ctx), EXIT.lint, run.out.stderr);
  const manifest = manifestOf(box, "keyframes");
  assert.equal(manifest.shots.bird.takes.length, MAX_KEYFRAME_TAKES);
  assert.equal(manifest.shots.bird.needs_review, true);
  assert.deepEqual(manifest.shots.bird.problems, ["no bird"]);
  assert.equal(manifest.shots.opening.needs_review, false);
  assert.equal(manifest.shots.farewell, undefined, "only the named shots were drawn");
  assert.match(run.out.stdout, /ERROR bird: no take passed the judge: no bird/);
  assert.equal(readApprovals(box.workdir).approvals.at(-1).gate, "look");
  assert.ok(existsSync(path.join(box.workdir, "keyframes", "bird-3.png")), "every take stays on disk for the prompt fix");

  // The STOP file ends a run between remote calls and keeps what was drawn.
  writeFileSync(path.join(box.workdir, "STOP"), "");
  const stopped = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "--slug", box.slug, "--shot", "farewell"], stopped.ctx), EXIT.ok, stopped.out.stderr);
  assert.match(stopped.out.stdout, /stopped by the STOP file/);
  assert.equal(manifestOf(box, "keyframes").shots.farewell, undefined);
});
