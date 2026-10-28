// `keyframes import`: a picture drawn outside the pipeline becomes a shot's keyframe, gated,
// named, judged on request and booked (ticket 2026-10-28-keyframes-import-keyframes-manifest-judge).
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { lookHash } from "../core/drama.mjs";
import { dramaFixture, sandbox } from "../core/fixtures/load.mjs";
import { visualHash } from "../core/timeline.mjs";
import { KEYFRAME_IMPORT_PROVIDERS, pictureSize } from "./keyframes-import.mjs";
import { importedTotals, readLedger } from "./ledger.mjs";

process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const TOKEN = `mkv_${"m".repeat(43)}`;
const SHA = (data) => createHash("sha256").update(data).digest("hex");

/** A PNG whose IHDR says width×height (the pixel data is not read by anything here). */
function png(width, height, text = "") {
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; ihdr[9] = 2;
  const length = Buffer.alloc(4);
  length.writeUInt32BE(13, 0);
  return Buffer.concat([Buffer.from("\x89PNG\r\n\x1a\n", "binary"), length, Buffer.from("IHDR"), ihdr, Buffer.alloc(4), Buffer.from(text)]);
}
/** A JPEG with one SOF0 frame header saying width×height. */
function jpeg(width, height) {
  const sof = Buffer.alloc(19);
  sof[0] = 0xff; sof[1] = 0xc0; sof.writeUInt16BE(17, 2); sof[4] = 8; sof.writeUInt16BE(height, 5); sof.writeUInt16BE(width, 7); sof[9] = 3;
  return Buffer.concat([Buffer.from([0xff, 0xd8, 0xff, 0xe0, 0x00, 0x10]), Buffer.alloc(14), sof, Buffer.from([0xff, 0xd9])]);
}

const STATUS = {
  enabled: true,
  music_enabled: true,
  image: { provider: "gemini", model: "gemini-3-pro-image", configured: true },
  clip: { provider: "gemini", model: "omni", configured: true, resolution: "1080p", seconds: 8 },
  music: { provider: "gemini", model: "lyria", configured: true },
  models: { images: { gemini: [{ value: "gemini-3-pro-image", label: "Pro", description: null, status: "stable", resolutions: [], durations: [], reference_images: 14, native_audio: false, usd_per_second: null, usd_per_image: 0.134, usd_per_image_2k: 0.24 }] }, clips: {}, music: {} },
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

/** A media server for `look` (pictures and judge) and for the import's uploads and judge. */
function mediaSite({ verdicts = () => ({ overall: 8, passed: true }) } = {}) {
  const state = { images: [], judges: [], uploads: [], files: new Map() };
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const route = pathname.replace("/api/video/media/", "");
    if (init.method === "GET" && route === "status") return Response.json(STATUS);
    if (init.method === "POST" && route === "images") {
      const request = JSON.parse(init.body);
      state.images.push(request);
      const bytes = png(1376, 768, `${request.prompt}|${request.seed ?? ""}`);
      state.files.set(SHA(bytes), bytes);
      return Response.json({ id: `img${state.images.length}`, status: "ready", file: { sha256: SHA(bytes), size: bytes.length, content_type: "image/png" }, usd_estimate: 0.134, error: null, retry_after_seconds: 0 });
    }
    if (init.method === "GET" && route.startsWith("files/")) {
      const bytes = state.files.get(route.split("/")[2]);
      return bytes ? new Response(bytes, { headers: { "Content-Type": "image/png", "Content-Length": String(bytes.length) } }) : Response.json({ code: "video_media_file_not_found", detail: "gone" }, { status: 404 });
    }
    if (init.method === "PUT" && route.startsWith("files/")) {
      const bytes = Buffer.from(init.body);
      state.uploads.push({ sha256: SHA(bytes) });
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

function context(box, fetchImpl) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" },
      home: box.base,
      fetch: fetchImpl,
      openRenderer: async () => ({ sheet: async () => png(800, 600, "sheet"), close: async () => {} }),
      hashImage: async (file) => SHA(readFileSync(file)).slice(0, 16),
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-10-28T08:00:00Z"),
      sleep: async () => {},
    },
  };
}

const manifestOf = (box) => JSON.parse(readFileSync(path.join(box.workdir, "keyframes", "manifest.json"), "utf8"));
const outside = (box, name, bytes) => {
  const file = path.join(box.base, name);
  writeFileSync(file, bytes);
  return file;
};

/** A drama whose look is drawn, chosen and approved: what `keyframes` and `keyframes import` both wait for. */
async function approvedLook(site) {
  const box = sandbox("fixture-drama", "drama");
  const look = context(box, site.fetchImpl);
  assert.equal(await main(["look", "--slug", box.slug], look.ctx), EXIT.ok, look.out.stderr);
  const choose = context(box, site.fetchImpl);
  await main(["look", "--slug", box.slug, "--choose", "jingwei=2,yandi=1"], choose.ctx);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  return box;
}

test("pictureSize reads a PNG's IHDR and a JPEG's frame header, and nothing else", () => {
  assert.deepEqual(pictureSize(png(1312, 736)), { width: 1312, height: 736, ext: "png" });
  assert.deepEqual(pictureSize(jpeg(1920, 1080)), { width: 1920, height: 1080, ext: "jpg" });
  assert.equal(pictureSize(Buffer.from("not a picture at all")), null);
  assert.equal(pictureSize(Buffer.from("\x89PNG\r\n\x1a\n", "binary")), null, "a signature with no IHDR");
});

test("keyframes import refuses what it cannot take, and waits for the approved look like keyframes does", async () => {
  const site = mediaSite();
  const box = sandbox("fixture-drama", "drama");
  const picture = outside(box, "opening.png", png(1312, 736, "colab opening"));
  const bring = ["keyframes", "import", "--slug", box.slug, "--shot", "opening", "--file", picture, "--provider", "colab"];
  const usage = async (args, pattern) => {
    const run = context(box, site.fetchImpl);
    assert.equal(await main(args, run.ctx), EXIT.usage, run.out.stderr || run.out.stdout);
    assert.match(run.out.stderr, pattern);
  };
  assert.deepEqual(KEYFRAME_IMPORT_PROVIDERS, ["colab", "hailuo-web", "external"]);
  await usage(bring.slice(0, 8), /--provider must be one of colab, hailuo-web, external/);
  await usage(["keyframes", "import", "--slug", box.slug, "--file", picture, "--provider", "colab"], /needs --slug, --shot and --file/);
  await usage(bring.map((each) => (each === "opening" ? "nowhere" : each)), /--shot nowhere names no shot/);
  await usage(bring.map((each) => (each === picture ? path.join(box.base, "missing.png") : each)), /missing\.png does not exist/);
  await usage(bring.map((each) => (each === picture ? outside(box, "words.png", Buffer.from("hello")) : each)), /is not a PNG or JPEG/);
  await usage([...bring, "--usd", "lots"], /--usd must be a number, zero or more/);
  // The look is not approved yet: the owner's gate, as for a drawn keyframe.
  const early = context(box, site.fetchImpl);
  assert.equal(await main(bring, early.ctx), EXIT.owner, early.out.stderr);
  assert.match(early.out.stderr, /the look is not generated yet/);
  assert.ok(!existsSync(path.join(box.workdir, "keyframes", "manifest.json")), "nothing was written");
});

test("an imported keyframe is copied under its route's name, bound to the look and script, booked, and the same bytes keep their name", async () => {
  const site = mediaSite();
  const box = await approvedLook(site);
  const picture = outside(box, "opening.png", png(1312, 736, "colab opening"));
  const bring = ["keyframes", "import", "--slug", box.slug, "--shot", "opening", "--file", picture, "--provider", "colab", "--credits", "0.4", "--note", "qwen-image-edit seed 7"];
  const run = context(box, site.fetchImpl);
  assert.equal(await main(bring, run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
  assert.match(run.out.stdout, /opening: keyframes\/opening-import-1\.png from colab \(0\.4 credits\): 1312x736, not judged \(--judge asks\)/);
  assert.match(run.out.stdout, /next: .*review-push .*--gate storyboard/);
  const manifest = manifestOf(box);
  assert.equal(manifest.look_hash, lookHash(dramaFixture()));
  assert.equal(manifest.visual_hash, visualHash(dramaFixture()));
  const shot = manifest.shots.opening;
  assert.equal(shot.file, "keyframes/opening-import-1.png");
  assert.equal(shot.sha256, SHA(readFileSync(picture)));
  assert.equal(shot.needs_review, false, "without --judge the picture is the owner's choice");
  assert.equal(shot.judge, null);
  assert.deepEqual([shot.provider, shot.credits, shot.note, shot.width, shot.height], ["colab", 0.4, "qwen-image-edit seed 7", 1312, 736]);
  assert.equal(shot.takes.length, 1);
  assert.ok(existsSync(path.join(box.workdir, shot.file)));
  assert.equal(site.state.judges.filter((each) => each.kind === "keyframe").length, 0, "no judge was asked");
  const ledger = readLedger(box.workdir).entries.filter((entry) => entry.status === "imported");
  assert.equal(ledger.length, 1);
  assert.deepEqual([ledger[0].stage, ledger[0].kind, ledger[0].id, ledger[0].credits, ledger[0].cost_usd], ["keyframes", "image", "opening", 0.4, 0]);
  assert.deepEqual(importedTotals(readLedger(box.workdir).entries), { clips: 0, clip_seconds: 0, credits: 0.4, usd: 0 }, "a keyframe is not a clip");

  // The same bytes again: the same name, one take; other bytes: the next number, replacing the shot's picture.
  const again = context(box, site.fetchImpl);
  assert.equal(await main(bring, again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(manifestOf(box).shots.opening.takes.length, 1);
  assert.equal(readLedger(box.workdir).entries.filter((entry) => entry.status === "imported").length, 1, "one row per shot and file");
  const other = outside(box, "opening-2.jpg", jpeg(1920, 1080));
  const next = context(box, site.fetchImpl);
  assert.equal(await main(bring.map((each) => (each === picture ? other : each)), next.ctx), EXIT.ok, next.out.stderr);
  const replaced = manifestOf(box).shots.opening;
  assert.equal(replaced.file, "keyframes/opening-import-2.jpg");
  assert.equal(replaced.takes.length, 2);
  assert.match(next.out.stdout, /replaces keyframes\/opening-import-1\.png/);
});

test("--judge asks the site's judge on the keyframes rubric with the chosen sheets; a failing verdict leaves the shot needs_review with the fixes, --force keeps it, --usd is booked", async () => {
  let fail = true;
  const site = mediaSite({ verdicts: (kind) => (kind === "keyframe" && fail ? { overall: 5, passed: false, problems: ["identity_jingwei: another face → the girl of the sheet"] } : { overall: 8, passed: true }) });
  const box = await approvedLook(site);
  const picture = outside(box, "farewell.png", png(1312, 736, "colab farewell"));
  const bring = ["keyframes", "import", "--slug", box.slug, "--shot", "farewell", "--file", picture, "--provider", "colab", "--judge", "--usd", "0.05"];
  const run = context(box, site.fetchImpl);
  assert.equal(await main(bring, run.ctx), EXIT.lint, run.out.stderr || run.out.stdout);
  const asked = site.state.judges.filter((each) => each.kind === "keyframe");
  assert.equal(asked.length, 1);
  assert.deepEqual(asked[0].files.map((file) => file.label), ["keyframe", "sheet 精衛", "sheet 炎帝"]);
  assert.equal(asked[0].files[0].sha256, SHA(readFileSync(picture)), "the picture itself goes to the judge");
  assert.deepEqual(asked[0].rubric.map((item) => item.key).slice(0, 3), ["identity_jingwei", "identity_yandi", "prompt"]);
  assert.equal(asked[0].context.shot.id, "farewell");
  const shot = manifestOf(box).shots.farewell;
  assert.equal(shot.needs_review, true);
  assert.equal(shot.judge.overall, 5);
  assert.deepEqual(shot.fixes, ["the girl of the sheet"]);
  assert.match(run.out.stdout, /ERROR farewell: judge 5\/10/);
  assert.match(run.out.stdout, /keep this one with --force/);
  const money = readLedger(box.workdir).entries.filter((entry) => entry.status === "imported");
  assert.equal(money.length, 1);
  assert.equal(money[0].cost_usd, 0.05, "the dollars are booked in place of the hold");
  assert.equal(readLedger(box.workdir).entries.filter((entry) => entry.status === "reserved").length, 0, "nothing stays reserved");

  const forced = context(box, site.fetchImpl);
  assert.equal(await main([...bring, "--force"], forced.ctx), EXIT.ok, forced.out.stderr);
  assert.match(forced.out.stdout, /kept by --force although judge 5\/10/);
  assert.deepEqual([manifestOf(box).shots.farewell.needs_review, manifestOf(box).shots.farewell.forced], [false, true]);

  // A passing verdict needs no force; a picture under 1280x720 fails the size check whatever the judge says.
  fail = false;
  const pass = context(box, site.fetchImpl);
  assert.equal(await main(bring, pass.ctx), EXIT.ok, pass.out.stderr);
  assert.equal(manifestOf(box).shots.farewell.needs_review, false);
  const small = outside(box, "small.png", png(1000, 560, "small"));
  const tiny = context(box, site.fetchImpl);
  assert.equal(await main(["keyframes", "import", "--slug", box.slug, "--shot", "bird", "--file", small, "--provider", "external"], tiny.ctx), EXIT.lint);
  assert.match(tiny.out.stdout, /the picture is 1000x560; at least 1280x720 is needed/);
  assert.equal(manifestOf(box).shots.bird.needs_review, true);
});
