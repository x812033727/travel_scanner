import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { lookHash, mixHash } from "../core/drama.mjs";
import { dramaFixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { FPS, visualHash } from "../core/timeline.mjs";
import { clipPrompt, clipRubric, clipSeconds, lastFrameArgs, MAX_CLIP_TAKES, proxyArgs } from "./clips.mjs";
import { readLedger } from "./ledger.mjs";
import { MIN_TRACK_SECONDS, trackSeconds } from "./music.mjs";
import { chosenModel, clipSecondPrice, statusProblem, trackPrice } from "./stages.mjs";

const TOKEN = `mkv_${"c".repeat(43)}`;
const SHA = (data) => createHash("sha256").update(data).digest("hex");
const PNG = (text) => Buffer.concat([Buffer.from("\x89PNG\r\n\x1a\n", "binary"), Buffer.from(text)]);
const MP4 = (text) => Buffer.concat([Buffer.from("\x00\x00\x00\x18ftypisom", "binary"), Buffer.from(text)]);

const STATUS = {
  enabled: true,
  music_enabled: true,
  image: { provider: "gemini", model: "gemini-3-pro-image", configured: true },
  clip: { provider: "gemini", model: "gemini-omni-1.1-flash", configured: true, resolution: "1080p", seconds: 8 },
  music: { provider: "gemini", model: "lyria-3.5", configured: true },
  models: {
    images: { gemini: [{ value: "gemini-3-pro-image", usd_per_image: 0.134, durations: [], resolutions: [], reference_images: 14, native_audio: false, usd_per_second: null, usd_per_track: null, label: "", description: null, status: "stable" }] },
    clips: { gemini: [{ value: "gemini-omni-1.1-flash", usd_per_second: 0.15, durations: [4, 5, 6, 7, 8, 9, 10], resolutions: ["720p", "1080p"], reference_images: 3, native_audio: true, usd_per_image: null, usd_per_track: null, label: "", description: null, status: "stable" }] },
    music: { gemini: [{ value: "lyria-3.5", usd_per_track: 0.08, durations: [], resolutions: [], reference_images: 0, native_audio: false, usd_per_second: null, usd_per_image: null, label: "", description: null, status: "stable" }] },
  },
  budgets: { clip_seconds: { unit: "seconds", limit: 3000, used: 12, remaining: 2988 } },
  estimated_usd: 1.8,
  max_usd_per_video: 200,
  max_clips_per_video: 40,
  max_retakes_per_shot: 2,
  judge_min_score: 7,
  style_preset: "cinematic-3d",
  store: { used_bytes: 0, max_file_bytes: 1, max_total_bytes: 1, writable: true },
  limits: {},
};

/** A media server whose clips need one poll, and whose judge answers from `verdicts(request, count)`. */
function mediaSite({ verdicts = () => ({ overall: 8, passed: true }), tooLargeOnce = null, status = STATUS } = {}) {
  const state = { clips: [], music: [], polls: {}, judges: [], uploads: [], files: new Map(), jobs: new Map() };
  let large = tooLargeOnce;
  const fetchImpl = async (url, init = {}) => {
    const { pathname, search } = new URL(url);
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const route = pathname.replace("/api/video/media/", "");
    if (init.method === "GET" && route === "status") return Response.json(status);
    if (init.method === "POST" && route === "clips") {
      const request = JSON.parse(init.body);
      state.clips.push(request);
      const id = `clip${state.clips.length}`;
      const bytes = MP4(`${request.shot_id}|${request.prompt}|${request.seed}|${request.first_frame}|${request.seconds}`);
      state.jobs.set(id, { bytes, seconds: request.seconds });
      return Response.json({ id, status: "queued", file: null, error: null, retry_after_seconds: 1, usd_estimate: request.seconds * 0.15 }, { status: 202 });
    }
    if (init.method === "POST" && route === "music") {
      const request = JSON.parse(init.body);
      state.music.push(request);
      const bytes = Buffer.from(`ID3music|${request.prompt}|${request.seconds}`);
      state.files.set(SHA(bytes), bytes);
      return Response.json({ id: `music${state.music.length}`, status: "ready", file: { sha256: SHA(bytes), size: bytes.length, content_type: "audio/mpeg" }, error: null, retry_after_seconds: 0, usd_estimate: 0.08 });
    }
    if (init.method === "GET" && route.startsWith("jobs/")) {
      const id = route.slice(5);
      state.polls[id] = (state.polls[id] ?? 0) + 1;
      const job = state.jobs.get(id);
      if (state.polls[id] < 2) return Response.json({ id, status: "submitted", file: null, error: null, retry_after_seconds: 1, usd_estimate: job.seconds * 0.15 });
      state.files.set(SHA(job.bytes), job.bytes);
      return Response.json({ id, status: "ready", file: { sha256: SHA(job.bytes), size: job.bytes.length, content_type: "video/mp4" }, error: null, retry_after_seconds: 0, usd_estimate: job.seconds * 0.15 });
    }
    if (init.method === "GET" && route.startsWith("files/")) {
      const bytes = state.files.get(route.split("/")[2]);
      return bytes ? new Response(bytes, { headers: { "Content-Type": "video/mp4", "Content-Length": String(bytes.length) } }) : Response.json({ code: "video_media_file_not_found", detail: "gone" }, { status: 404 });
    }
    if (init.method === "PUT" && route.startsWith("files/")) {
      const bytes = Buffer.from(init.body);
      state.uploads.push({ sha256: SHA(bytes), route: `${route}${search}` });
      state.files.set(route.split("/")[2], bytes);
      return Response.json({ received: [0], complete: true });
    }
    if (init.method === "POST" && route === "judge") {
      const request = JSON.parse(init.body);
      state.judges.push(request);
      if (large && request.context.shot?.id === large) {
        large = null;
        return Response.json({ code: "video_media_judge_too_large", detail: "too big" }, { status: 413 });
      }
      const verdict = verdicts(request, state.judges.length);
      return Response.json({ scores: {}, overall: verdict.overall, passed: verdict.passed, problems: verdict.problems ?? [], notes: "", model: "gemini-judge" });
    }
    return Response.json({ code: "video_media_route_unknown", detail: route }, { status: 404 });
  };
  return { state, fetchImpl };
}

/** A drama work directory after tts, look (chosen and approved) and keyframes (approved). */
function prepared() {
  const box = sandbox("fixture-drama", "drama");
  const doc = dramaFixture();
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  mkdirSync(path.join(box.workdir, "characters", "jingwei"), { recursive: true });
  mkdirSync(path.join(box.workdir, "characters", "yandi"), { recursive: true });
  const timeline = writeSyntheticNarration(doc, fixtureLexicon(), box.workdir);
  const shots = {};
  for (const scene of doc.scenes.filter((each) => each.template === "shot")) {
    const file = `keyframes/${scene.id}-1.png`;
    writeFileSync(path.join(box.workdir, file), PNG(`key ${scene.id}`));
    shots[scene.id] = { file, sha256: SHA(PNG(`key ${scene.id}`)), seed: 1, judge: { overall: 8, passed: true, problems: [] }, needs_review: false };
  }
  writeFileSync(path.join(box.workdir, "keyframes", "farewell-end.png"), PNG("end farewell"));
  shots.farewell.end_frame = { file: "keyframes/farewell-end.png", sha256: SHA(PNG("end farewell")) };
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

const goodProbe = (seconds) => ({ codec: "h264", width: 1920, height: 1080, fps: 30, frames: seconds * FPS, duration: seconds });

function context(box, fetchImpl, extra = {}) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" },
      home: box.base,
      fetch: fetchImpl,
      clipQc: async (file, wanted) => ({ probe: goodProbe(wanted.requested), black: [], freezes: [], cuts: [], keyframe_psnr: 40, rival_psnr: 20 }),
      extractFrame: async (clip, target) => writeFileSync(target, PNG(`last of ${path.basename(clip)}`)),
      makeProxy: async (clip, target) => writeFileSync(target, MP4(`proxy of ${path.basename(clip)}`)),
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-26T09:00:00Z"),
      sleep: async () => {},
      ...extra,
    },
  };
}

const manifestOf = (box, name) => JSON.parse(readFileSync(path.join(box.workdir, name, "manifest.json"), "utf8"));

test("clip seconds, prompts, rubric and ffmpeg arguments", () => {
  assert.equal(clipSeconds(30, [4, 6, 8]), 4);
  assert.equal(clipSeconds(150, [4, 6, 8]), 6, "5 s of lines takes the next offered duration");
  assert.equal(clipSeconds(400, [4, 6, 8]), 8, "capped at the longest offered; the fit holds the rest");
  assert.equal(clipSeconds(285, []), 10, "no catalog: whole seconds up to ten");
  assert.equal(clipSeconds(3000, [4, 5, 6, 7, 8, 9, 10]), 10);
  const doc = dramaFixture();
  const opening = doc.scenes[0];
  assert.equal(clipPrompt(opening, { motion: "no cuts" }), "mist drifting through the pines, birds crossing the sky. slow push in. no cuts");
  assert.equal(clipPrompt({ data: {} }, { motion: "" }), "");
  assert.deepEqual(clipRubric([{ id: "jing-wei", name: "精衛" }]).map((item) => item.key), ["identity_jing_wei", "motion", "prompt", "clean", "no_text"]);
  assert.match(proxyArgs("a.mp4", "p.mp4").join(" "), /scale=1280:720.*-crf 28.*-an/);
  assert.deepEqual(lastFrameArgs("a.mp4", 240, "last.png").slice(-5), ["-fps_mode", "passthrough", "-frames:v", "1", "last.png"]);
  assert.match(lastFrameArgs("a.mp4", 240, "last.png").join(" "), /select=eq\(n\\,239\)/);
  assert.equal(clipSecondPrice(STATUS), 0.15);
  assert.equal(trackPrice(STATUS), 0.08);
  assert.equal(chosenModel(STATUS, "clip").value, "gemini-omni-1.1-flash");
  assert.match(statusProblem({ ...STATUS, music_enabled: false }, "music"), /music generation is off/);
  assert.equal(statusProblem(STATUS, "clip"), null);
  assert.equal(trackSeconds(1275), 48, "42.5 s of video plus the tail");
  assert.equal(trackSeconds(30), MIN_TRACK_SECONDS);
});

test("clips need an approved storyboard, then each shot gets a clip from its keyframe, checked and retaken", async () => {
  const { box, doc, timeline, shots } = prepared();
  const site = mediaSite({
    verdicts: (request) => (request.context.shot.id === "farewell" && site.state.judges.filter((each) => each.context.shot?.id === "farewell").length === 1 ? { overall: 4, passed: false, problems: ["the emperor's beard morphs"] } : { overall: 8, passed: true }),
    tooLargeOnce: "opening",
  });
  const early = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], early.ctx), EXIT.owner);
  assert.match(early.out.stderr, /the storyboard is not approved yet/);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });

  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  const frames = (id) => timeline.scenes.find((scene) => scene.id === id).end_frame - timeline.scenes.find((scene) => scene.id === id).start_frame;
  const expected = ["opening", "farewell", "sea-storm", "bird"].map((id) => clipSeconds(frames(id), [4, 5, 6, 7, 8, 9, 10]));
  assert.match(dry.out.stdout, new RegExp(`4 shots, ${expected.reduce((a, b) => a + b, 0)} clip seconds for one take each`));
  assert.match(dry.out.stdout, /2988 of 3000 clip seconds left this month/);
  assert.equal(site.state.clips.length, 0);

  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  const requests = site.state.clips;
  assert.deepEqual(requests.map((request) => [request.shot_id, request.seed, request.seconds]), [["opening", 1, expected[0]], ["farewell", 1, expected[1]], ["farewell", 2, expected[1]], ["sea-storm", 1, expected[2]], ["bird", 1, expected[3]]]);
  assert.equal(requests[0].first_frame, shots.opening.sha256, "a clip starts on its keyframe");
  assert.equal(requests[1].last_frame, shots.farewell.end_frame.sha256, "an end frame guides the last picture");
  assert.equal(requests[0].last_frame, undefined);
  assert.deepEqual(requests[1].references.map((reference) => reference.role), ["character", "character"]);
  assert.equal(requests[0].resolution, "1080p");
  assert.equal(requests[0].native_audio, false);
  assert.match(requests[0].prompt, /^mist drifting through the pines.*slow push in\. slow cinematic camera move/);
  assert.match(requests[0].negative_prompt, /watermark/);
  const bird = requests[4];
  assert.equal(bird.references.at(-1).role, "previous_frame", "a continued shot carries the previous clip's last frame");
  assert.equal(bird.references.at(-1).sha256, SHA(PNG("last of sea-storm-1.mp4")));
  assert.ok(site.state.uploads.some((upload) => upload.sha256 === shots.opening.sha256), "keyframes go back to the store");
  // The opening's clip was too large for the judge inline: a proxy went up and was judged instead.
  const openingJudges = site.state.judges.filter((each) => each.context.shot.id === "opening");
  assert.equal(openingJudges.length, 2);
  assert.equal(openingJudges[1].files[0].sha256, SHA(MP4("proxy of opening-1.mp4")));
  assert.deepEqual(openingJudges[0].files.map((file) => file.label), ["clip", "sheet 精衛"], "sheets are labelled by the character's name");
  const manifest = manifestOf(box, "clips");
  assert.equal(manifest.speech_hash, timeline.speech_hash);
  assert.equal(manifest.look_hash, lookHash(doc));
  assert.match(manifest.clips_hash, /^[0-9a-f]{16}$/);
  assert.deepEqual(Object.keys(manifest.shots), ["opening", "farewell", "sea-storm", "bird"]);
  assert.equal(manifest.shots.farewell.seed, 2);
  assert.equal(manifest.shots.farewell.takes.length, 2);
  assert.match(manifest.shots.farewell.takes[0].qc.problems[0], /judge 4\/10: the emperor's beard morphs/);
  assert.equal(manifest.shots.farewell.needs_review, false);
  assert.equal(manifest.shots.farewell.file, "clips/farewell-2.mp4");
  assert.equal(manifest.shots.bird.continues.shot, "sea-storm");
  assert.equal(manifest.shots.opening.first_frame.sha256, shots.opening.sha256);
  assert.ok(manifest.shots.opening.qc.ok && manifest.shots.opening.qc.metrics.keyframe_psnr === 40);
  for (const shot of Object.values(manifest.shots)) assert.ok(existsSync(path.join(box.workdir, shot.file)), shot.file);
  const ledger = readLedger(box.workdir);
  assert.equal(ledger.totals.clip_seconds, expected.reduce((a, b) => a + b, 0) + expected[1], "the retake counts too");
  assert.equal(ledger.totals.judge_calls, 5, "the refused oversized call is not booked; the proxy's is");
  assert.match(run.out.stdout, /next: node tools\/video\/cli\.mjs music --slug fixture-drama/);

  const again = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(site.state.clips.length, 5, "clips that passed are kept");
  assert.match(again.out.stdout, /opening: kept/);
  const before = manifestOf(box, "clips").clips_hash;
  assert.equal(before, manifest.clips_hash);
});

test("a shot that fails every take is left for a prompt fix, and the STOP file ends a run cleanly", async () => {
  const { box } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const black = context(box, site.fetchImpl, {
    clipQc: async (file, wanted) => ({ probe: goodProbe(wanted.requested), black: file.includes("sea-storm") ? [{ start: 0.5, end: 1.2 }] : [], freezes: [], cuts: [], keyframe_psnr: 40, rival_psnr: 20 }),
  });
  assert.equal(await main(["clips", "--slug", box.slug, "--shot", "sea-storm,opening"], black.ctx), EXIT.lint, black.out.stderr);
  const manifest = manifestOf(box, "clips");
  assert.equal(manifest.shots["sea-storm"].takes.length, MAX_CLIP_TAKES);
  assert.equal(manifest.shots["sea-storm"].needs_review, true);
  assert.match(manifest.shots["sea-storm"].problems[0], /black from 0\.50 s to 1\.20 s/);
  assert.equal(manifest.shots.opening.needs_review, false);
  assert.equal(manifest.shots.bird, undefined);
  assert.match(black.out.stdout, /ERROR sea-storm: no take passed: black from/);
  assert.match(black.out.stdout, /fix the prompts of sea-storm and run clips again/);

  writeFileSync(path.join(box.workdir, "STOP"), "");
  const stopped = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--shot", "farewell"], stopped.ctx), EXIT.ok, stopped.out.stderr);
  assert.match(stopped.out.stdout, /stopped by the STOP file/);
  assert.equal(manifestOf(box, "clips").shots.farewell, undefined);
});

test("music is generated a little longer than the video and cached, or the owner's own track is checked", async () => {
  const { box, doc, timeline } = prepared();
  const site = mediaSite();
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  assert.match(dry.out.stdout, new RegExp(`music: ${trackSeconds(timeline.total_frames)} s for a`));
  assert.match(dry.out.stdout, /gemini lyria-3\.5 ready; about US\$0\.08/);
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.equal(site.state.music.length, 1);
  assert.deepEqual(site.state.music[0], { slug: "fixture-drama", prompt: doc.music.prompt, seconds: trackSeconds(timeline.total_frames) });
  const manifest = manifestOf(box, "music");
  assert.equal(manifest.mix_hash, mixHash(doc));
  assert.equal(manifest.source, "generated");
  assert.match(manifest.file, /^music\/[0-9a-f]{16}\.mp3$/);
  assert.ok(existsSync(path.join(box.workdir, manifest.file)));
  assert.equal(readLedger(box.workdir).totals.music, 1);
  const again = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(site.state.music.length, 1, "the same prompt and length are not paid for twice");
  assert.match(again.out.stdout, /reused/);

  // The owner's own file: checked against music.sha256 when given, refused when missing.
  const file = path.join(box.dir, "video.json");
  const own = JSON.parse(readFileSync(file, "utf8"));
  own.music = { track: "guqin.mp3", sha256: SHA("guqin bytes") };
  writeFileSync(file, JSON.stringify(own));
  const missing = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug], missing.ctx), EXIT.owner);
  assert.match(missing.out.stderr, /guqin\.mp3 is not in/);
  mkdirSync(path.join(box.work, "_music"), { recursive: true });
  writeFileSync(path.join(box.work, "_music", "guqin.mp3"), "guqin bytes");
  const track = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug], track.ctx), EXIT.ok, track.out.stderr);
  const checked = manifestOf(box, "music");
  assert.equal(checked.source, "track");
  assert.equal(checked.track, "guqin.mp3");
  assert.equal(checked.mix_hash, mixHash(own));
  own.music.sha256 = "0".repeat(64);
  writeFileSync(file, JSON.stringify(own));
  const wrong = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug], wrong.ctx), EXIT.owner);
  assert.match(wrong.out.stderr, /not music\.sha256/);
});
