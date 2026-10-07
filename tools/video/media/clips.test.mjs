import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { LEASE_FILE } from "../core/project-lease.mjs";
import { approve } from "../core/approvals.mjs";
import { clipsHash, lookHash, mixHash } from "../core/drama.mjs";
import { dramaFixture, fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { pipelineStatus } from "../core/state.mjs";
import { buildTimeline, estimatedSamples, FPS, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from "../core/timeline.mjs";
import { readJobs } from "./cache.mjs";
import { clipPrompt, clipRubric, clipSeconds, lastFrameArgs, MAX_CLIP_TAKES, proxyArgs } from "./clips.mjs";
import { FIX_ARROW } from "./keyframes.mjs";
import { importedTotals, readLedger, reserve, savedTotals } from "./ledger.mjs";
import { MIN_TRACK_SECONDS, trackSeconds } from "./music.mjs";
import { chosenModel, clipSecondPrice, statusProblem, trackPrice } from "./stages.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

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

/**
 * A media server whose clips need one poll, and whose judge answers from `verdicts(request, count)`.
 * `refuse(request)` returning `{ code, detail }` makes that clip job end failed when it is polled,
 * as the server reports a provider's refusal.
 */
function mediaSite({ verdicts = () => ({ overall: 8, passed: true }), tooLargeOnce = null, status = STATUS, refuse = () => null } = {}) {
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
      state.jobs.set(id, { bytes, seconds: request.seconds, refusal: refuse(request) });
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
      if (job.refusal) return Response.json({ id, status: "failed", file: null, error: job.refusal, retry_after_seconds: 0, usd_estimate: job.seconds * 0.15 });
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

/**
 * A drama work directory after tts, look (chosen and approved) and keyframes (approved).
 * `mutate(doc)` changes the script first and writes it back, so the hashes match what the
 * stages read from disk.
 */
function prepared(mutate = null) {
  const box = sandbox("fixture-drama", "drama");
  const doc = dramaFixture();
  if (mutate) {
    mutate(doc);
    writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);
  }
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

const shortDialogue = (doc) => {
  for (const scene of doc.scenes) {
    delete scene.data.fit;
    for (const line of scene.lines) {
      line.text = "走。";
      delete line.say;
      delete line.say_for;
    }
  }
};

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

test("a production model or resolution mismatch stops before any paid clip submission", async () => {
  const required = { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p" };
  for (const choice of [{ ...required, model: "gemini-omni-1.1-flash" }, { ...required, resolution: "720p" }]) {
    const { box } = prepared(shortDialogue);
    writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: { profile: { video: required } } }));
    await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
    await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
    const site = mediaSite({ status: { ...STATUS, clip: { ...STATUS.clip, ...choice } } });
    const run = context(box, site.fetchImpl);
    assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.owner, run.out.stderr || run.out.stdout);
    assert.match(run.out.stderr, /approved production profile requires/);
    assert.equal(site.state.clips.length, 0);
    assert.equal(site.state.uploads.length, 0);
  }
});

test("named-look clip questions fit the judge limit for E1 Zhitang and maximum appearances", () => {
  const episode = JSON.parse(readFileSync(new URL("../../../docs/videos/series-plans/competition-20261002/episodes/episode-01-voice.video.json", import.meta.url), "utf8"));
  const zhitang = { ...episode.characters.find((character) => character.id === "zhitang"), shot_look: "zhitang--base" };
  const boundary = { id: "a".repeat(24), name: "Long display name ".repeat(50), shot_look: "b".repeat(24), appearance: "requested appearance ".repeat(40).slice(0, 800) };
  assert.equal(boundary.appearance.length, 800);
  for (const character of [zhitang, boundary]) {
    const rubric = clipRubric([character]);
    assert.ok(rubric.every((criterion) => criterion.question.length <= 400), `${character.id}: ${rubric[0].question.length}`);
    assert.ok(rubric[0].question.includes(character.id));
    assert.ok(rubric[0].question.includes(character.shot_look));
    assert.match(rubric[0].question, /facial identity.*bone structure/);
    assert.match(rubric[0].question, /full requested appearance.*context/);
    assert.match(rubric[0].question, /clothing, hair and age override/);
    assert.match(rubric[0].question, /no morphing back to the base outfit/);
  }
  assert.equal(clipRubric([{ id: "jingwei", name: "精衛" }])[0].question, 'In the clip\'s last frame, is 精衛 still the same person as in the reference sheet labelled "精衛": face, hair, clothing, build?');
});

test("named-look clip judging retains the complete appearance and identity in context", async () => {
  const appearance = "adult woman wearing a navy business suit; ".repeat(20).slice(0, 793) + " TAIL!!";
  assert.equal(appearance.length, 800);
  const { box, doc } = prepared((doc) => {
    doc.characters[0].shot_looks = [{ id: "present", appearance }];
    doc.scenes[1].data.character_looks = { jingwei: "present" };
  });
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
  const judge = site.state.judges.find((entry) => entry.context.shot?.id === "farewell");
  assert.ok(judge.rubric.every((criterion) => criterion.question.length <= 400));
  assert.deepEqual(judge.context.characters[0], { id: "jingwei", shot_look: "present", name: doc.characters[0].name, description: appearance });
  assert.match(judge.files.find((file) => file.label === `sheet ${doc.characters[0].name}`).sha256, /^[a-f0-9]{64}$/);
  const other = judge.context.characters[1];
  const original = doc.characters.find((character) => character.name === other.name);
  assert.deepEqual(other, { name: original.name, description: original.appearance }, "ordinary character context stays unchanged");
  assert.ok(site.state.clips.find((entry) => entry.shot_id === "farewell").prompt.includes(appearance));
});

test("ordinary clip questions with long display names stay bounded and preserve full context", async () => {
  for (const name of ["界".repeat(74), "界".repeat(75), "Long display name ".repeat(30)]) {
    const { box, doc } = prepared((doc) => { doc.characters[0].name = name; });
    assert.ok(clipRubric([doc.characters[0]]).every((criterion) => criterion.question.length <= 400));
    await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
    await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
    const site = mediaSite();
    const run = context(box, site.fetchImpl);
    assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
    const judge = site.state.judges.find((entry) => entry.context.shot?.id === "farewell");
    assert.ok(judge.files.every((file) => file.label.length <= 80), "all file labels satisfy JudgeFile's 80-character maximum");
    const longLabel = `sheet ${name}`.length > 80;
    const originalQuestion = `In the clip's last frame, is ${name} still the same person as in the reference sheet labelled "${name}": face, hair, clothing, build?`;
    if (originalQuestion.length > 400 || longLabel) {
      assert.ok(judge.rubric[0].question.includes(doc.characters[0].id));
      assert.match(judge.rubric[0].question, /full name in context.*face, hair, clothing, build/);
      assert.ok(!judge.rubric[0].question.includes(`labelled "${name}"`), "the question must not name a sheet label absent from the files");
    } else assert.equal(judge.rubric[0].question, originalQuestion);
    assert.ok(judge.files.some((file) => file.label === `sheet ${longLabel ? doc.characters[0].id : name}`));
    assert.deepEqual(judge.context.characters[0], { ...(longLabel ? { id: doc.characters[0].id } : {}), name, description: doc.characters[0].appearance });
  }
});

test("a production child's visual shots stop before uploads or paid Veo Lite calls", async () => {
  const { box } = prepared(shortDialogue);
  const video = { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p" };
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: {
    profile: { video },
    characters: [{ id: "jingwei", video_constraints: { min_visual_age_years: 12, veo_lite_i2v: "not-verified-under-18" } }],
  } }));
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite({ status: { ...STATUS, clip: { ...STATUS.clip, ...video } } });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.owner, run.out.stderr || run.out.stdout);
  assert.match(run.out.stderr, /allow_adult.*jingwei \(12\)/);
  assert.match(run.out.stderr, /preserve the approved ages/);
  assert.equal(site.state.uploads.length, 0);
  assert.equal(site.state.clips.length, 0);
  assert.equal(site.state.judges.length, 0);
});

test("the production age guard permits offscreen voices and leaves legacy projects unchanged", async () => {
  const video = { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p" };
  const status = { ...STATUS, clip: { ...STATUS.clip, ...video }, models: { ...STATUS.models, clips: { gemini: [{ ...STATUS.models.clips.gemini[0], value: video.model, durations: [4, 6, 8], reference_images: 0 }] } } };
  for (const legacy of [false, true]) {
    const { box, doc } = prepared((doc) => {
      shortDialogue(doc);
      if (!legacy) for (const scene of doc.scenes) scene.data.characters = (scene.data.characters ?? []).filter((id) => id !== "jingwei");
    });
    assert.ok(doc.scenes.some((scene) => scene.lines.some((line) => line.speaker === "jingwei")), "the child still has a spoken line");
    writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: {
      ...(legacy ? {} : { profile: { video } }),
      characters: [{ id: "jingwei", video_constraints: { min_visual_age_years: 12, veo_lite_i2v: "not-verified-under-18" } }],
    } }));
    await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
    await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
    const site = mediaSite({ status });
    const run = context(box, site.fetchImpl);
    assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, `${legacy ? "legacy" : "offscreen"}: ${run.out.stderr || run.out.stdout}`);
    assert.equal(site.state.clips.length, doc.scenes.filter((scene) => scene.template === "shot").length);
  }
});

test("an episode's unnamed child in the picture stops Veo Lite even without a child cast id", async () => {
  const { box } = prepared(shortDialogue);
  const video = { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p" };
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: {
    profile: { video }, characters: [],
    episode: { video_constraints: { veo_lite_i2v: "unverified-minor-on-screen", reason: "a child stands in the opening crowd" } },
  } }));
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite({ status: { ...STATUS, clip: { ...STATUS.clip, ...video } } });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.owner, run.out.stderr || run.out.stdout);
  assert.match(run.out.stderr, /child stands in the opening crowd/);
  assert.equal(site.state.uploads.length, 0);
  assert.equal(site.state.clips.length, 0);
  assert.equal(site.state.judges.length, 0);
});

test("a short written shot whose recorded dialogue exceeds eight seconds stops before media submission", async () => {
  const { box, doc } = prepared(shortDialogue);
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: { profile: {} } }));
  const measured = estimatedSamples(doc);
  measured[doc.scenes[0].lines[0].id] = 8 * SAMPLE_RATE;
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify({ ...buildTimeline(doc, measured), speech_hash: speechHash(doc, fixtureLexicon()) }));
  const site = mediaSite();
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.owner, run.out.stderr || run.out.stdout);
  assert.match(run.out.stderr, /measured production timeline needs a script revision/);
  assert.match(run.out.stderr, /8 seconds including pauses/);
  assert.equal(site.state.clips.length, 0);
  assert.equal(site.state.uploads.length, 0);
});

test("the production profile refuses a slightly short source take instead of padding the last frame", async () => {
  const { box, doc } = prepared(shortDialogue);
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: { profile: {} } }));
  const measured = estimatedSamples(doc);
  measured[doc.scenes[0].lines[0].id] = 101 * SAMPLES_PER_FRAME;
  measured[doc.scenes[0].lines[1].id] = 100 * SAMPLES_PER_FRAME;
  const timeline = buildTimeline(doc, measured);
  assert.equal(timeline.scenes[0].end_frame, 240);
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify({ ...timeline, speech_hash: speechHash(doc, fixtureLexicon()) }));
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const run = context(box, site.fetchImpl, { clipQc: async (file, wanted) => ({ probe: goodProbe(path.basename(file).startsWith("opening-") ? 7.9 : wanted.requested), black: [], freezes: [], cuts: [], keyframe_psnr: 40, rival_psnr: 20 }) });
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.lint, run.out.stderr || run.out.stdout);
  const opening = manifestOf(box, "clips").shots.opening;
  assert.equal(opening.needs_review, true);
  assert.match(opening.problems.join("; "), /would need padding or slowing/);
  assert.equal(site.state.clips.filter((request) => request.shot_id === "opening").length, MAX_CLIP_TAKES, "the existing paid-retake bound remains in force");
});

test("1080p production rejects a native 720p take with bounded retakes while legacy QC stays unchanged", async () => {
  for (const production of [true, false]) {
    const { box } = prepared(shortDialogue);
    if (production) writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: { profile: { video: { ...STATUS.clip, aspect: "16:9" } } } }));
    await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
    await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
    const site = mediaSite();
    const run = context(box, site.fetchImpl, { clipQc: async (file, wanted) => ({
      probe: { ...goodProbe(wanted.requested), ...(path.basename(file).startsWith("opening-") ? { width: 1280, height: 720 } : {}) },
      black: [], freezes: [], cuts: [], keyframe_psnr: 40, rival_psnr: 20,
    }) });
    assert.equal(await main(["clips", "--slug", box.slug], run.ctx), production ? EXIT.lint : EXIT.ok, run.out.stderr || run.out.stdout);
    const opening = manifestOf(box, "clips").shots.opening;
    assert.equal(opening.needs_review, production);
    if (production) assert.match(opening.problems.join("; "), /native 1920x1080.*1280x720/);
    assert.equal(site.state.clips.filter((request) => request.shot_id === "opening").length, production ? MAX_CLIP_TAKES : 1);
  }
});

test("resuming a production checks cached model, native size and motion evidence rather than trusting old clip hashes", async () => {
  const { box } = prepared(shortDialogue);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const first = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
  const status = async () => (await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir })).steps.find((step) => step.id === "clips generated");
  const select = (model) => writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ production: { profile: { video: { ...STATUS.clip, model } } } }));
  select("veo-3.1-lite-generate-preview");
  assert.equal((await status()).done, false);
  assert.match((await status()).note, /do not match the approved production/);
  select(STATUS.clip.model);
  assert.equal((await status()).done, true);
  const original = manifestOf(box, "clips");
  for (const fault of ["duration", "dimensions"]) {
    const clips = structuredClone(original);
    if (fault === "duration") clips.shots.opening.qc.metrics.duration = 0.1;
    else Object.assign(clips.shots.opening.qc.metrics, { width: 1280, height: 720 });
    writeFileSync(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify(clips));
    assert.equal((await status()).done, false);
    assert.match((await status()).note, fault === "duration" ? /whole dialogue/ : /native 1920x1080/);
    const paidBefore = site.state.clips.length;
    const resumed = context(box, site.fetchImpl);
    assert.equal(await main(["clips", "--slug", box.slug], resumed.ctx), EXIT.owner, resumed.out.stderr);
    assert.match(resumed.out.stderr, /cached clip opening/);
    assert.equal(site.state.clips.length, paidBefore, "a resume never silently replaces untrusted evidence with a paid retry");
  }
});

test("Veo 3.1 Lite 1080p requests eight seconds and first frames, with sheets only for the judge", async () => {
  const { box, shots } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const model = "veo-3.1-lite-generate-preview";
  const status = { ...STATUS, clip: { ...STATUS.clip, model }, models: { ...STATUS.models, clips: { gemini: [{ ...STATUS.models.clips.gemini[0], value: model, durations: [4, 6, 8], reference_images: 0 }] } } };
  const site = mediaSite({ status });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
  assert.ok(site.state.clips.every((request) => request.seconds === 8 && request.references.length === 0 && request.native_audio === false));
  assert.equal(site.state.clips.find((request) => request.shot_id === "farewell").first_frame, shots.farewell.sha256);
  assert.ok(site.state.judges.find((request) => request.context.shot?.id === "farewell").files.some((file) => file.label === "sheet 精衛"));
  assert.equal(clipSeconds(30, [4, 6, 8], { model, resolution: "720p" }), 4);
  assert.equal(clipSeconds(30, [4, 6, 8], { model: "veo-3.1-fast-generate-preview", resolution: "1080p" }), 8);
});

test("a clip model the catalog gives no reference images (MiniMax-H3) gets its frames alone, and its sheets go to the judge", async () => {
  const { box, shots } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const model = "MiniMax-H3";
  const status = { ...STATUS, clip: { ...STATUS.clip, provider: "minimax", model, resolution: "2k" }, models: { ...STATUS.models, clips: { minimax: [{ ...STATUS.models.clips.gemini[0], value: model, resolutions: ["768p", "2k"], reference_images: 0 }] } } };
  const site = mediaSite({ status });
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
  assert.ok(site.state.clips.length > 0 && site.state.clips.every((request) => request.references.length === 0), "no sheet and no previous frame: the server refuses them for H3");
  const farewell = site.state.clips.find((request) => request.shot_id === "farewell");
  assert.equal(farewell.first_frame, shots.farewell.sha256);
  assert.equal(farewell.last_frame, shots.farewell.end_frame.sha256);
  assert.ok(site.state.judges.find((request) => request.context.shot?.id === "farewell").files.some((file) => file.label === "sheet 精衛"));
});

test("clips keep the face reference while using the shot's named outfit in generation and judging", async () => {
  const { box, characters } = prepared((doc) => {
    doc.characters[0].shot_looks = [{ id: "present", appearance: "adult woman wearing a navy business suit" }];
    doc.scenes[1].data.character_looks = { jingwei: "present" };
  });
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
  const request = site.state.clips.find((entry) => entry.shot_id === "farewell");
  assert.match(request.prompt, /navy business suit/);
  assert.match(request.prompt, /same facial identity/);
  assert.equal(request.references[0].sha256, characters.jingwei.candidates[0].sha256);
  const judge = site.state.judges.find((entry) => entry.context.shot?.id === "farewell");
  assert.match(judge.rubric[0].question, /no morphing back to the base outfit/);
  assert.match(judge.context.characters[0].description, /navy business suit/);
});

// A judge problem as the server shapes it: the criterion's key, the fault and where, and after
// the arrow the words to put in the prompt (apps/api/app/video_media/judge.py).
const BEARD_FIX = "the beard still, resting on the collar";
const BEARD_PROBLEM = `motion: the emperor's beard morphs into the collar in the last second${FIX_ARROW}${BEARD_FIX}`;

test("clips need an approved storyboard, then each shot gets a clip from its keyframe, checked and retaken with the judge's fix", async () => {
  const { box, doc, timeline, shots } = prepared();
  const site = mediaSite({
    verdicts: (request) => (request.context.shot.id === "farewell" && site.state.judges.filter((each) => each.context.shot?.id === "farewell").length === 1 ? { overall: 4, passed: false, problems: [BEARD_PROBLEM] } : { overall: 8, passed: true }),
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
  assert.match(dry.out.stdout, new RegExp(`4 shots: 0 stills \\(animated keyframes, nothing to buy\\) and 4 clips priced, ${expected.reduce((a, b) => a + b, 0)} clip seconds for one take each`));
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
  // The retake is asked with the judge's fix for the take before it; the first take as written.
  assert.doesNotMatch(requests[1].prompt, /Corrections/);
  assert.equal(requests[2].prompt, `${requests[1].prompt}. Corrections: ${BEARD_FIX}`);
  assert.notEqual(requests[2].idempotency_key, requests[1].idempotency_key, "another prompt, another request");
  assert.match(run.out.stdout, /farewell take 2: asked with the corrections of the takes before: the beard still, resting on the collar\n/);
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
  assert.match(manifest.shots.farewell.takes[0].qc.problems[0], /judge 4\/10: motion: the emperor's beard morphs into the collar in the last second → the beard still/);
  assert.equal(manifest.shots.farewell.takes[0].fixes, undefined);
  assert.deepEqual(manifest.shots.farewell.takes[1].fixes, [BEARD_FIX], "what the take was asked with is on record");
  assert.equal(manifest.shots.farewell.needs_review, false);
  assert.equal(manifest.shots.farewell.fixes, undefined, "a shot that passed leaves no hint");
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

test("a shot that fails every take is left for a prompt fix with the judge's fixes as the hint, and the STOP file ends a run cleanly", async () => {
  const { box } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  // The storm fails the black-frame check every time, and the judge has a fix for it too.
  const WAVES_FIX = "the waves rolling through the whole clip";
  const site = mediaSite({ verdicts: (request) => (request.context.shot.id === "sea-storm" ? { overall: 5, passed: false, problems: [`motion: the waves freeze mid-roll${FIX_ARROW}${WAVES_FIX}`] } : { overall: 8, passed: true }) });
  const black = context(box, site.fetchImpl, {
    clipQc: async (file, wanted) => ({ probe: goodProbe(wanted.requested), black: file.includes("sea-storm") ? [{ start: 0.5, end: 1.2 }] : [], freezes: [], cuts: [], keyframe_psnr: 40, rival_psnr: 20 }),
  });
  assert.equal(await main(["clips", "--slug", box.slug, "--shot", "sea-storm,opening"], black.ctx), EXIT.lint, black.out.stderr);
  const manifest = manifestOf(box, "clips");
  assert.equal(manifest.shots["sea-storm"].takes.length, MAX_CLIP_TAKES);
  assert.equal(manifest.shots["sea-storm"].needs_review, true);
  assert.match(manifest.shots["sea-storm"].problems[0], /black from 0\.50 s to 1\.20 s/);
  assert.match(manifest.shots["sea-storm"].problems[1], /judge 5\/10: motion: the waves freeze mid-roll → the waves rolling/);
  assert.deepEqual(manifest.shots["sea-storm"].fixes, [WAVES_FIX], "the judge's fix, from under the check's line");
  assert.deepEqual(site.state.clips.filter((request) => request.shot_id === "sea-storm").map((request) => request.prompt.endsWith(`. Corrections: ${WAVES_FIX}`)), [false, true], "the second take was asked with it");
  assert.equal(manifest.shots.opening.needs_review, false);
  assert.equal(manifest.shots.opening.fixes, undefined);
  assert.equal(manifest.shots.bird, undefined);
  assert.match(black.out.stdout, /ERROR sea-storm: no take passed: black from/);
  assert.match(black.out.stdout, /\n  fixes for sea-storm: the waves rolling through the whole clip\nfix the prompts of sea-storm and run clips again/);

  writeFileSync(path.join(box.workdir, "STOP"), "");
  const stopped = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--shot", "farewell"], stopped.ctx), EXIT.incomplete, stopped.out.stderr);
  assert.match(stopped.out.stdout, /stopped by the STOP file/);
  assert.equal(manifestOf(box, "clips").shots.farewell, undefined);
});

// What the server reports when the provider refuses a job outright (MiniMax refused keyframe prompts
// over its length limit this way on 2026-10-04): a failed job, refused again for every seed.
const TOO_LONG = { code: "video_media_upstream_invalid", detail: "prompt length must be less than 1500" };
const BLOCKED = { code: "video_media_rejected", detail: "output blocked by the content filter" };

test("a shot every seed is refused for waits for a prompt fix with the provider's refusal, and a rerun once it is taken buys that shot alone", async () => {
  const { box, doc, timeline } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  let refusing = true;
  // sea-storm is refused on every seed, twice for its length and then by the filter; opening on its first seed only.
  const site = mediaSite({
    refuse: (request) => (!refusing ? null : request.shot_id === "sea-storm" ? (request.seed < 3 ? TOO_LONG : BLOCKED) : request.shot_id === "opening" && request.seed === 1 ? TOO_LONG : null),
  });
  // A record for sea-storm that names a clip no longer on disk and no take: nothing of it may
  // stand in the new record, or the clips hash and a shot continuing from it would read that clip.
  mkdirSync(path.join(box.workdir, "clips"), { recursive: true });
  const stale = { file: "clips/sea-storm-9.mp4", sha256: "9".repeat(64), seed: 9, seconds: 6, judge: { overall: 4, passed: false, problems: ["the waves freeze"] }, takes: [], needs_review: true, problems: ["judge 4/10: the waves freeze"] };
  writeFileSync(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify({ speech_hash: timeline.speech_hash, visual_hash: visualHash(doc), look_hash: lookHash(doc), shots: { "sea-storm": stale } }));
  const shots = ["--shot", "opening,sea-storm", "--takes", "3"];

  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, ...shots], run.ctx), EXIT.lint, run.out.stderr);
  assert.deepEqual(site.state.clips.map((request) => [request.shot_id, request.seed]), [["opening", 1], ["opening", 2], ["sea-storm", 1], ["sea-storm", 2], ["sea-storm", 3]]);
  assert.equal(site.state.judges.length, 1, "a refused seed has no clip to judge");
  const manifest = manifestOf(box, "clips");
  assert.deepEqual(manifest.shots["sea-storm"], { takes: [], needs_review: true, problems: [`no take could be generated: ${TOO_LONG.detail}`, `no take could be generated: ${BLOCKED.detail}`] }, "one problem per distinct refusal, nothing of the earlier record");
  assert.equal(manifest.shots.opening.file, "clips/opening-2.mp4", "a refused seed is followed by the next");
  assert.deepEqual(manifest.shots.opening.takes.map((take) => take.seed), [2]);
  assert.equal(manifest.shots.opening.needs_review, false);
  assert.equal(manifest.clips_hash, clipsHash([{ id: "opening", sha256: manifest.shots.opening.sha256 }]), "the refused shot has no clip to hash");
  assert.match(run.out.stdout, /sea-storm seed 3: sea-storm: output blocked by the content filter; trying another seed\n/);
  assert.match(run.out.stdout, /ERROR sea-storm: no take could be generated: prompt length must be less than 1500; no take could be generated: output blocked by the content filter\n/);
  assert.match(run.out.stdout, /fix the prompts of sea-storm and run clips again/);
  // Each refusal is booked as a failed job at no cost, and none is left waiting to be picked up.
  const clips = readLedger(box.workdir).entries.filter((entry) => entry.kind === "clip");
  assert.deepEqual(clips.map((entry) => [entry.id, entry.status, entry.error ?? null]), [
    ["opening", "failed", TOO_LONG.code],
    ["opening", "ready", null],
    ["sea-storm", "failed", TOO_LONG.code],
    ["sea-storm", "failed", TOO_LONG.code],
    ["sea-storm", "failed", BLOCKED.code],
  ]);
  assert.ok(clips.filter((entry) => entry.status === "failed").every((entry) => entry.cost_usd === 0));
  assert.deepEqual(readJobs(box.workdir).jobs, {});

  // Once the provider takes the prompt, the rerun buys that shot alone and keeps the other.
  refusing = false;
  const fixed = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, ...shots], fixed.ctx), EXIT.ok, fixed.out.stderr);
  assert.match(fixed.out.stdout, /opening: kept \(/);
  assert.deepEqual(site.state.clips.slice(5).map((request) => [request.shot_id, request.seed]), [["sea-storm", 1]]);
  const after = manifestOf(box, "clips");
  assert.equal(after.shots["sea-storm"].file, "clips/sea-storm-1.mp4");
  assert.equal(after.shots["sea-storm"].needs_review, false);
  assert.equal(after.shots["sea-storm"].problems, undefined);
  assert.equal(after.shots.opening.sha256, manifest.shots.opening.sha256);
});

test("a still shot buys no clip: its keyframe goes into the manifest, a clip may continue from it, and it needs a passed keyframe", async () => {
  // sea-storm becomes a still; bird continues from it, so bird's previous frame is that keyframe.
  const { box, timeline, shots } = prepared((doc) => {
    doc.scenes.find((scene) => scene.id === "sea-storm").data.visual = "still";
  });
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  const frames = (id) => timeline.scenes.find((scene) => scene.id === id).end_frame - timeline.scenes.find((scene) => scene.id === id).start_frame;
  const expected = ["opening", "farewell", "bird"].map((id) => clipSeconds(frames(id), [4, 5, 6, 7, 8, 9, 10]));
  assert.match(dry.out.stdout, /sea-storm: [\d.]+ s of lines → still, its keyframe under a camera move \(no clip to buy\)/);
  assert.match(dry.out.stdout, new RegExp(`4 shots: 1 stills \\(animated keyframes, nothing to buy\\) and 3 clips priced, ${expected.reduce((a, b) => a + b, 0)} clip seconds for one take each`));
  assert.match(dry.out.stdout, new RegExp(`about US\\$${(expected.reduce((a, b) => a + b, 0) * 0.15 + 3 * 0.01).toFixed(2)}`), "only the three clips are priced");

  let extracted = 0;
  const run = context(box, site.fetchImpl, { extractFrame: async () => { extracted += 1; } });
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.deepEqual(site.state.clips.map((request) => request.shot_id), ["opening", "farewell", "bird"], "no clip is asked for the still");
  const bird = site.state.clips[2];
  assert.deepEqual(bird.references.at(-1), { sha256: shots["sea-storm"].sha256, role: "previous_frame" }, "a clip after a still continues from the keyframe itself");
  assert.equal(extracted, 0, "there is no clip to take a last frame of");
  const manifest = manifestOf(box, "clips");
  assert.deepEqual(Object.keys(manifest.shots), ["sea-storm", "opening", "farewell", "bird"], "stills are recorded first, then the clips in order");
  assert.deepEqual(manifest.shots["sea-storm"], { still: true, file: "keyframes/sea-storm-1.png", sha256: shots["sea-storm"].sha256 });
  assert.equal(manifest.shots.bird.continues.file, "keyframes/sea-storm-1.png");
  const order = ["opening", "farewell", "sea-storm", "bird"].map((id) => ({ id, sha256: manifest.shots[id].sha256 }));
  assert.equal(manifest.clips_hash, clipsHash(order), "the clips hash covers the still's keyframe in script order");
  assert.notEqual(manifest.clips_hash, clipsHash(order.map((shot) => (shot.id === "sea-storm" ? { ...shot, sha256: "0".repeat(64) } : shot))), "a redrawn keyframe changes it");
  assert.match(run.out.stdout, /3 clips generated in \d+ s; 4 shots in the manifest \(1 stills\)/);
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  const last = state.runs.filter((each) => each.stage === "clips").at(-1);
  assert.equal(last.shots, 4);
  assert.equal(last.stills, 1);
  assert.equal(last.generated, 3);

  // A still whose keyframe failed its checks stops the stage like any undrawn shot.
  const keyframes = manifestOf(box, "keyframes");
  keyframes.shots["sea-storm"].needs_review = true;
  writeFileSync(path.join(box.workdir, "keyframes", "manifest.json"), JSON.stringify(keyframes));
  const flagged = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--shot", "sea-storm"], flagged.ctx), EXIT.usage);
  assert.match(flagged.out.stderr, /shots sea-storm have no passed keyframe; run keyframes first/);
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

test("music under illustrated slides comes from the owner's track, with no drama guard", async () => {
  const box = sandbox("fixture-illustrated", "illustrated");
  const site = mediaSite();
  const missing = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug], missing.ctx), EXIT.owner);
  assert.match(missing.out.stderr, /bed\.mp3 is not in/);
  mkdirSync(path.join(box.work, "_music"), { recursive: true });
  writeFileSync(path.join(box.work, "_music", "bed.mp3"), "bed bytes");
  const track = context(box, site.fetchImpl);
  assert.equal(await main(["music", "--slug", box.slug], track.ctx), EXIT.ok, track.out.stderr);
  const manifest = manifestOf(box, "music");
  assert.equal(manifest.source, "track");
  assert.equal(manifest.track, "bed.mp3");
  assert.equal(site.state.music.length, 0, "a licensed file buys nothing");
  const { capFor } = await import("./stages.mjs");
  assert.equal(capFor({ max_usd_per_video: 200, slides_max_usd_per_video: 20 }, "slides"), 20);
  assert.equal(capFor({ max_usd_per_video: 200, slides_max_usd_per_video: 20 }), 200);
  assert.equal(capFor({ max_usd_per_video: 200 }, "slides"), 200);
});

test("a shot cut from another shot's clip buys nothing: priced at zero, recorded with its source frame and its saving, and left for a fix when it runs past the clip", async () => {
  const cutFrom = (from_s) => (doc) => {
    shortDialogue(doc);
    const bird = doc.scenes.find((scene) => scene.id === "bird");
    delete bird.data.start_frame;
    bird.data.source = { shot: "sea-storm", from_s };
  };
  const { box, timeline } = prepared(cutFrom(1));
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  const frames = (id) => timeline.scenes.find((scene) => scene.id === id).end_frame - timeline.scenes.find((scene) => scene.id === id).start_frame;
  const expected = ["opening", "farewell", "sea-storm"].map((id) => clipSeconds(frames(id), [4, 5, 6, 7, 8, 9, 10]));
  const bought = expected.reduce((a, b) => a + b, 0);
  const notBought = clipSeconds(frames("bird"), [4, 5, 6, 7, 8, 9, 10]);
  assert.match(dry.out.stdout, new RegExp(`bird: [\\d.]+ s of lines → cut from sea-storm's clip at 1 s \\(no clip to buy; ${notBought} clip seconds not bought\\)`));
  assert.match(dry.out.stdout, new RegExp(`4 shots: 0 stills \\(animated keyframes, nothing to buy\\), 1 cuts from another shot's clip \\(nothing to buy, ${notBought} clip seconds saved\\) and 3 clips priced, ${bought} clip seconds for one take each`));
  assert.match(dry.out.stdout, new RegExp(`about US\\$${(bought * 0.15 + 3 * 0.01).toFixed(2)}`), "the cut is not priced");

  const run = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], run.ctx), EXIT.ok, run.out.stderr);
  assert.deepEqual(site.state.clips.map((request) => request.shot_id), ["opening", "farewell", "sea-storm"], "no clip is asked for the cut");
  const manifest = manifestOf(box, "clips");
  const storm = manifest.shots["sea-storm"];
  assert.deepEqual(manifest.shots.bird, { source: { shot: "sea-storm", from_s: 1, from_frame: 30 }, file: storm.file, sha256: storm.sha256, seconds: storm.seconds, frames: storm.frames, needed_s: Number((frames("bird") / FPS).toFixed(3)), needs_review: false });
  assert.deepEqual(Object.keys(manifest.shots), ["opening", "farewell", "sea-storm", "bird"], "the cut is recorded after the clips it needs");
  assert.match(run.out.stdout, new RegExp(`bird: cut from sea-storm's clip at 1 s \\(${notBought} clip seconds not bought\\)`));
  assert.match(run.out.stdout, new RegExp(`3 clips generated in \\d+ s; 4 shots in the manifest \\(0 stills, 1 cuts from another shot's clip, ${notBought} clip seconds not bought\\)`));
  const ledger = readLedger(box.workdir);
  const cut = ledger.entries.find((entry) => entry.status === "cut");
  assert.deepEqual([cut.id, cut.kind, cut.stage, cut.seconds, cut.cost_usd, cut.saved_seconds, cut.saved_usd, cut.source], ["bird", "clip", "clips", 0, 0, notBought, Number((notBought * 0.15).toFixed(4)), { shot: "sea-storm", from_s: 1 }]);
  assert.equal(ledger.totals.clip_seconds, bought, "a saving is not spending");
  assert.deepEqual(savedTotals(ledger.entries), { clip_seconds: notBought, usd: Number((notBought * 0.15).toFixed(4)), cuts: 1 });
  const again = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(readLedger(box.workdir).entries.filter((entry) => entry.status === "cut").length, 1, "a rerun replaces the cut's entry instead of counting it twice");
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  const last = state.runs.filter((each) => each.stage === "clips").at(-1);
  assert.equal(last.cuts, 1);
  assert.equal(last.saved_clip_seconds, notBought);
  assert.ok((await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir })).steps.find((step) => step.id === "clips generated").done, "the cut counts as generated");

  // A cut that runs past the source clip's end is left for the writer, like a take that failed.
  const late = prepared(cutFrom(3.5));
  await approve({ gate: "look", docDir: late.box.dir, workdir: late.box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: late.box.dir, workdir: late.box.workdir, note: "test" });
  const flagged = context(late.box, mediaSite().fetchImpl);
  assert.equal(await main(["clips", "--slug", late.box.slug], flagged.ctx), EXIT.lint, flagged.out.stderr);
  const bird = manifestOf(late.box, "clips").shots.bird;
  assert.equal(bird.needs_review, true);
  assert.match(bird.problems[0], /sea-storm's clip runs 4\.0 s; a cut starting at 3\.5 s needs [\d.]+ s: start earlier or shorten the lines/);
  assert.match(flagged.out.stdout, /ERROR bird: no take passed: sea-storm's clip runs 4\.0 s/);
  assert.equal(readLedger(late.box.workdir).entries.some((entry) => entry.status === "cut"), false, "nothing was saved");
});

// A clip made outside the pipeline, as ffmpeg would measure it: `seconds` long, starting `psnr` dB from the keyframe.
const outsideQc = (seconds = 8, psnr = 40) => ({ clipQc: async () => ({ probe: goodProbe(seconds), black: [], freezes: [], cuts: [], keyframe_psnr: psnr, rival_psnr: 20 }) });
const outsideFile = (box, name, text) => {
  const file = path.join(box.base, name);
  writeFileSync(file, MP4(text));
  return file;
};
const clipsStep = async (box) => (await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir })).steps.find((step) => step.id === "clips generated");

test("clips import brings a clip made elsewhere into a shot: gated like a bought clip, checked, named by its route and booked", async () => {
  const { box, doc, timeline, shots } = prepared();
  const site = mediaSite();
  const made = outsideFile(box, "hailuo-opening.mp4", "hailuo opening");
  const bring = ["clips", "import", "--slug", box.slug, "--shot", "opening", "--file", made, "--provider", "hailuo-web", "--plan", "pro", "--credits", "60"];
  const usage = async (args, pattern) => {
    const run = context(box, site.fetchImpl, outsideQc());
    assert.equal(await main(args, run.ctx), EXIT.usage, run.out.stderr || run.out.stdout);
    assert.match(run.out.stderr, pattern);
  };
  await usage(bring.slice(0, 8), /--provider must be one of hailuo-web, kling-mcp, external/);
  await usage(["clips", "import", "--slug", box.slug, "--file", made, "--provider", "external"], /needs --slug, --shot and --file/);
  await usage(bring.map((each) => (each === "opening" ? "nowhere" : each)), /--shot nowhere names no shot/);
  await usage(bring.map((each) => (each === made ? path.join(box.base, "missing.mp4") : each)), /missing\.mp4 does not exist/);
  await usage(bring.map((each) => (each === "60" ? "many" : each)), /--credits must be a number, zero or more/);

  const early = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(bring, early.ctx), EXIT.owner);
  assert.match(early.out.stderr, /the storyboard is not approved yet/);
  assert.equal(existsSync(path.join(box.workdir, "clips", "opening-import-1.mp4")), false, "nothing is copied before the gate");
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });

  const run = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(bring, run.ctx), EXIT.ok, run.out.stderr || run.out.stdout);
  assert.deepEqual([site.state.clips.length, site.state.uploads.length, site.state.judges.length], [0, 0, 0], "an import without --judge never calls the site");
  const frames = (id) => timeline.scenes.find((scene) => scene.id === id).end_frame - timeline.scenes.find((scene) => scene.id === id).start_frame;
  const manifest = manifestOf(box, "clips");
  const opening = manifest.shots.opening;
  assert.deepEqual([manifest.speech_hash, manifest.visual_hash, manifest.look_hash], [timeline.speech_hash, visualHash(doc), lookHash(doc)]);
  assert.equal(manifest.clips_hash, clipsHash([{ id: "opening", sha256: SHA(MP4("hailuo opening")) }]));
  assert.deepEqual(
    [opening.file, opening.sha256, opening.seconds, opening.frames, opening.needed_s, opening.first_frame, opening.judge, opening.needs_review],
    ["clips/opening-import-1.mp4", SHA(MP4("hailuo opening")), 8, 8 * FPS, Number((frames("opening") / FPS).toFixed(3)), { file: shots.opening.file, sha256: shots.opening.sha256 }, null, false],
  );
  assert.deepEqual([opening.provider, opening.plan, opening.credits, opening.imported_at], ["hailuo-web", "pro", 60, "2026-09-26T09:00:00.000Z"]);
  assert.ok(opening.qc.ok && opening.qc.metrics.keyframe_psnr === 40 && opening.qc.metrics.width === 1920);
  assert.deepEqual(opening.takes.map((take) => [take.import, take.file, take.provider]), [[1, "clips/opening-import-1.mp4", "hailuo-web"]]);
  assert.deepEqual(readFileSync(path.join(box.workdir, opening.file)), MP4("hailuo opening"));
  assert.match(run.out.stdout, /opening: clips\/opening-import-1\.mp4 from hailuo-web, pro, 60 credits: 8\.0 s for [\d.]+ s of lines, 1920x1080, not judged/);
  assert.match(run.out.stdout, /next: node tools\/video\/cli\.mjs status --slug fixture-drama/);
  const booked = readLedger(box.workdir);
  const { at, ...entry } = booked.entries[0];
  assert.deepEqual(entry, { stage: "clips", id: "opening", provider: "hailuo-web", plan: "pro", credits: 60, seconds: 8, cost_usd: 0, file: opening.file, sha256: opening.sha256, kind: "clip", status: "imported" });
  assert.deepEqual(booked.totals, { usd: 0, images: 0, clip_seconds: 8, music: 0, judge_calls: 0, reserved: 0, reservations: 0 }, "the ledger counts its seconds");
  assert.deepEqual(importedTotals(booked.entries), { clips: 1, clip_seconds: 8, credits: 60, usd: 0 });
  const recorded = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8")).runs.filter((each) => each.stage === "clips").at(-1);
  assert.deepEqual([recorded.shots, recorded.imported, recorded.generated], [1, 1, 0]);

  // The same file again keeps its name and its one ledger entry.
  const again = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(bring, again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(manifestOf(box, "clips").shots.opening.takes.length, 1);
  assert.equal(readLedger(box.workdir).entries.length, 1);
  assert.equal(existsSync(path.join(box.workdir, "clips", "opening-import-2.mp4")), false);

  // status and the dry run tell it from a clip the pipeline buys.
  assert.equal((await clipsStep(box)).detail, "1 of 1 clips imported: hailuo-web 1");
  const status = context(box, site.fetchImpl);
  assert.equal(await main(["status", "--slug", box.slug], status.ctx), EXIT.ok, status.out.stderr);
  assert.match(status.out.stdout, /clips generated \(1 of 1 clips imported: hailuo-web 1\)/);
  const dry = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, dry.out.stderr);
  const bought = ["farewell", "sea-storm", "bird"].map((id) => clipSeconds(frames(id), [4, 5, 6, 7, 8, 9, 10]));
  const boughtSeconds = bought.reduce((a, b) => a + b, 0);
  assert.match(dry.out.stdout, /opening: [\d.]+ s of lines → imported \(hailuo-web, pro, 60 credits; no clip to buy\)/);
  assert.match(dry.out.stdout, new RegExp(`4 shots: 0 stills \\(animated keyframes, nothing to buy\\), 1 imported from outside the pipeline \\(nothing to buy\\) and 3 clips priced, ${boughtSeconds} clip seconds for one take each`));
  assert.match(dry.out.stdout, new RegExp(`about US\\$${(boughtSeconds * 0.15 + 3 * 0.01).toFixed(2)}`), "the imported shot is not priced");
  const forced = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug, "--dry-run", "--force"], forced.ctx), EXIT.ok, forced.out.stderr);
  assert.match(forced.out.stdout, /and 4 clips priced/, "--force buys the shot again, so it is priced");

  // The stage keeps the imported clip and buys only the others.
  const rest = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], rest.ctx), EXIT.ok, rest.out.stderr || rest.out.stdout);
  assert.deepEqual(site.state.clips.map((request) => request.shot_id), ["farewell", "sea-storm", "bird"]);
  assert.match(rest.out.stdout, /opening: kept \(imported from hailuo-web, 8 s, judge \?\/10\)/);
  assert.match(rest.out.stdout, /3 clips generated in \d+ s; 4 shots in the manifest \(0 stills, 1 imported from outside the pipeline\)/);
  const after = manifestOf(box, "clips");
  assert.equal(after.shots.opening.provider, "hailuo-web");
  assert.equal(after.clip.provider, "gemini", "the top-level choice is still the server's");
  const ledger = readLedger(box.workdir);
  assert.equal(ledger.totals.clip_seconds, 8 + boughtSeconds);
  assert.deepEqual(importedTotals(ledger.entries), { clips: 1, clip_seconds: 8, credits: 60, usd: 0 });
  assert.equal((await clipsStep(box)).detail, "1 of 4 clips imported: hailuo-web 1");
});

test("an imported clip that fails its checks is left for review, --force keeps it with the reason, and --judge asks the judge", async () => {
  const { box } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite({ verdicts: (request) => (request.context.shot.id === "bird" ? { overall: 4, passed: false, problems: [`clean: the wings melt into the tail${FIX_ARROW}the wings beating clear of the tail`] } : { overall: 8, passed: true }) });
  const made = outsideFile(box, "kling-opening.mp4", "kling opening");
  const bring = ["clips", "import", "--slug", box.slug, "--shot", "opening", "--file", made, "--provider", "kling-mcp", "--credits", "40"];

  // Its first frame is not the shot's keyframe: needs_review like a failed take, and still booked (the credits are spent).
  const off = context(box, site.fetchImpl, outsideQc(5, 15));
  assert.equal(await main(bring, off.ctx), EXIT.lint, off.out.stderr || off.out.stdout);
  const failed = manifestOf(box, "clips").shots.opening;
  assert.equal(failed.needs_review, true);
  assert.match(failed.problems[0], /the first frame does not show the keyframe \(PSNR 15\.0 dB\)/);
  assert.match(off.out.stdout, /ERROR opening: the first frame does not show the keyframe/);
  assert.match(off.out.stdout, /make opening again from its keyframe \(keyframes\/opening-1\.png\) and import that, or keep this one with --force/);
  assert.equal(readLedger(box.workdir).entries.filter((entry) => entry.status === "imported").length, 1);
  const step = await clipsStep(box);
  assert.equal(step.done, false);
  assert.match(step.note, /some shots failed the clip checks/);

  const kept = context(box, site.fetchImpl, outsideQc(5, 15));
  assert.equal(await main([...bring, "--force", "--note", "the owner accepted the reframing"], kept.ctx), EXIT.ok, kept.out.stderr || kept.out.stdout);
  const forced = manifestOf(box, "clips").shots.opening;
  assert.deepEqual([forced.needs_review, forced.forced, forced.note, forced.qc.ok, forced.problems, forced.takes.length], [false, true, "the owner accepted the reframing", false, undefined, 1]);
  assert.match(forced.qc.problems[0], /PSNR 15\.0 dB/, "the measurement stays on record");
  assert.match(kept.out.stdout, /opening: kept by --force although the first frame does not show the keyframe/);
  assert.equal(readLedger(box.workdir).entries.filter((entry) => entry.status === "imported").length, 1, "the same file is booked once");
  assert.equal((await clipsStep(box)).done, true);

  // --judge sends the clip and the cast's sheets to the store and asks the clip rubric; --usd prices the credits.
  const farewell = outsideFile(box, "kling-farewell.mp4", "kling farewell");
  const judged = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(["clips", "import", "--slug", box.slug, "--shot", "farewell", "--file", farewell, "--provider", "kling-mcp", "--plan", "pro", "--credits", "80", "--usd", "0.99", "--judge"], judged.ctx), EXIT.ok, judged.out.stderr || judged.out.stdout);
  assert.equal(site.state.clips.length, 0, "nothing is bought");
  assert.ok(site.state.uploads.some((upload) => upload.sha256 === SHA(MP4("kling farewell"))), "the clip goes to the store for the judge");
  assert.equal(site.state.judges.length, 1);
  assert.deepEqual(site.state.judges[0].files.map((file) => file.label), ["clip", "sheet 精衛", "sheet 炎帝"]);
  assert.equal(site.state.judges[0].files[0].sha256, SHA(MP4("kling farewell")));
  assert.deepEqual(site.state.judges[0].rubric.map((item) => item.key).slice(-4), ["motion", "prompt", "clean", "no_text"]);
  assert.equal(manifestOf(box, "clips").shots.farewell.judge.overall, 8);
  assert.match(judged.out.stdout, /farewell: clips\/farewell-import-1\.mp4 from kling-mcp, pro, 80 credits, US\$0\.99: .* judge 8\/10/);
  const ledger = readLedger(box.workdir);
  assert.deepEqual([ledger.totals.judge_calls, ledger.totals.usd], [1, 1], "the judge call and the priced credits are both money");
  assert.deepEqual(importedTotals(ledger.entries), { clips: 2, clip_seconds: 13, credits: 120, usd: 0.99 });

  // A judge that refuses the clip leaves it for review like any failed take.
  const bird = outsideFile(box, "kling-bird.mp4", "kling bird");
  const refused = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(["clips", "import", "--slug", box.slug, "--shot", "bird", "--file", bird, "--provider", "kling-mcp", "--judge"], refused.ctx), EXIT.lint, refused.out.stderr || refused.out.stdout);
  assert.match(manifestOf(box, "clips").shots.bird.problems[0], /judge 4\/10: clean: the wings melt into the tail/);
  assert.deepEqual(manifestOf(box, "clips").shots.bird.fixes, ["the wings beating clear of the tail"], "the judge's fix is the hint for the next attempt outside");
  assert.match(refused.out.stdout, /\n  fixes for bird: the wings beating clear of the tail\nmake bird again from its keyframe/);
  assert.equal(manifestOf(box, "clips").shots.bird.credits, null, "credits that were not given are not invented");
  assert.equal((await clipsStep(box)).detail, "3 of 3 clips imported: kling-mcp 3");
});

test("clips import refuses a production profile, a still, a cut and a stale timeline, and a cut from the imported shot follows it", async () => {
  const cutBird = (doc) => {
    shortDialogue(doc);
    const bird = doc.scenes.find((scene) => scene.id === "bird");
    delete bird.data.start_frame;
    bird.data.source = { shot: "sea-storm", from_s: 1 };
  };
  const { box } = prepared(cutBird);
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const bring = (shot, file) => ["clips", "import", "--slug", box.slug, "--shot", shot, "--file", file, "--provider", "hailuo-web"];
  const storm = outsideFile(box, "storm.mp4", "hailuo storm");

  const cut = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(bring("bird", storm), cut.ctx), EXIT.usage);
  assert.match(cut.out.stderr, /bird is cut from sea-storm's clip; import a clip for sea-storm instead/);

  // The stage buys the three clips and records the cut; importing the cut's source moves the cut to the new file.
  const stage = context(box, site.fetchImpl);
  assert.equal(await main(["clips", "--slug", box.slug], stage.ctx), EXIT.ok, stage.out.stderr || stage.out.stdout);
  assert.equal(manifestOf(box, "clips").shots.bird.file, "clips/sea-storm-1.mp4");
  const moved = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(bring("sea-storm", storm), moved.ctx), EXIT.ok, moved.out.stderr || moved.out.stdout);
  const manifest = manifestOf(box, "clips");
  assert.deepEqual([manifest.shots.bird.file, manifest.shots.bird.sha256, manifest.shots.bird.source.from_frame, manifest.shots.bird.needs_review], ["clips/sea-storm-import-1.mp4", SHA(MP4("hailuo storm")), 30, false]);
  assert.equal(manifest.shots["sea-storm"].takes.length, 2, "the bought take stays on record beside the imported one");
  assert.match(moved.out.stdout, /replaces clips\/sea-storm-1\.mp4/);
  assert.match(moved.out.stdout, /bird: cut from sea-storm's clip, now from the imported one/);
  assert.equal(manifest.clips_hash, clipsHash(["opening", "farewell", "sea-storm", "bird"].map((id) => ({ id, sha256: manifest.shots[id].sha256 }))));

  // A second, shorter import gets the next number, and the cut it is too short for is left for a fix.
  const brief = context(box, site.fetchImpl, outsideQc(1));
  assert.equal(await main(bring("sea-storm", outsideFile(box, "storm-short.mp4", "hailuo storm, short")), brief.ctx), EXIT.lint, brief.out.stderr || brief.out.stdout);
  assert.equal(manifestOf(box, "clips").shots["sea-storm"].file, "clips/sea-storm-import-2.mp4");
  assert.match(brief.out.stdout, /sea-storm: the clip is shorter than its lines/);
  assert.match(brief.out.stdout, /ERROR bird: sea-storm's clip runs 1\.0 s; a cut starting at 1 s needs/);
  assert.equal(manifestOf(box, "clips").shots.bird.needs_review, true);

  // A script changed since the narration was made: the timeline is stale, exit 2 like `clips`.
  const timeline = JSON.parse(readFileSync(path.join(box.workdir, "timeline.json"), "utf8"));
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify({ ...timeline, speech_hash: "0".repeat(16) }));
  const stale = context(box, site.fetchImpl, outsideQc());
  assert.equal(await main(bring("opening", storm), stale.ctx), EXIT.usage);
  assert.match(stale.out.stderr, /timeline\.json is missing or was built for an older script/);

  const still = prepared((doc) => {
    doc.scenes.find((scene) => scene.id === "sea-storm").data.visual = "still";
  });
  const stillRun = context(still.box, site.fetchImpl, outsideQc());
  assert.equal(await main(["clips", "import", "--slug", still.box.slug, "--shot", "sea-storm", "--file", outsideFile(still.box, "storm.mp4", "storm"), "--provider", "external"], stillRun.ctx), EXIT.usage);
  assert.match(stillRun.out.stderr, /sea-storm is a still: assemble animates its keyframe/);

  // A production profile names its own model; another route is the owner's decision (exit 3), and nothing is copied.
  const profiled = prepared(shortDialogue);
  writeFileSync(path.join(profiled.box.dir, "series.json"), JSON.stringify({ production: { profile: { video: { provider: "gemini", model: "veo-3.1-lite-generate-preview", resolution: "1080p" } } } }));
  await approve({ gate: "look", docDir: profiled.box.dir, workdir: profiled.box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: profiled.box.dir, workdir: profiled.box.workdir, note: "test" });
  const refused = context(profiled.box, site.fetchImpl, outsideQc());
  assert.equal(await main(["clips", "import", "--slug", profiled.box.slug, "--shot", "opening", "--file", outsideFile(profiled.box, "opening.mp4", "opening"), "--provider", "hailuo-web"], refused.ctx), EXIT.owner);
  assert.match(refused.out.stderr, /approved production profile, which accepts only clips bought with its own model/);
  assert.equal(existsSync(path.join(profiled.box.workdir, "clips")), false);
});

test("clips import --usd is money: refused past the per-video cap before anything is copied, held while the clip is checked and booked in place of the hold; the judge's call counts too", async () => {
  const { box } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  let heldAtJudge = null;
  const site = mediaSite({
    status: { ...STATUS, max_usd_per_video: 2 },
    verdicts: () => {
      heldAtJudge = readLedger(box.workdir).entries.filter((entry) => entry.status === "reserved");
      return { overall: 8, passed: true };
    },
  });
  let statusReads = 0;
  const fetchImpl = async (url, init) => {
    if (new URL(url).pathname.endsWith("/status")) statusReads += 1;
    return site.fetchImpl(url, init);
  };
  const bring = (shot, file, ...extra) => ["clips", "import", "--slug", box.slug, "--shot", shot, "--file", file, "--provider", "hailuo-web", "--plan", "pro", "--credits", "60", ...extra];
  const opening = outsideFile(box, "paid-opening.mp4", "paid opening");

  // Past the cap: the owner's call (exit 3), nothing copied, nothing held, nothing booked.
  const over = context(box, fetchImpl, outsideQc());
  assert.equal(await main(bring("opening", opening, "--usd", "2.5"), over.ctx), EXIT.owner, over.out.stderr || over.out.stdout);
  assert.match(over.out.stderr, /this video has spent US\$0\.00 and the next import costs about US\$2\.50, past the per-video cap of US\$2/);
  assert.equal(existsSync(path.join(box.workdir, "clips", "opening-import-1.mp4")), false);
  assert.deepEqual(readLedger(box.workdir).entries, []);
  assert.equal(statusReads, 1, "the cap comes from the site: one status read");
  // Free of charge and unjudged, the import never calls the site.
  const free = context(box, fetchImpl, outsideQc());
  assert.equal(await main(bring("opening", opening, "--usd", "0"), free.ctx), EXIT.ok, free.out.stderr || free.out.stdout);
  assert.equal(statusReads, 1);
  // Under the cap: booked at the price given, the hold gone with the booking.
  const paid = context(box, fetchImpl, outsideQc());
  assert.equal(await main(bring("opening", opening, "--usd", "0.5"), paid.ctx), EXIT.ok, paid.out.stderr || paid.out.stdout);
  assert.equal(statusReads, 2);
  let ledger = readLedger(box.workdir);
  assert.deepEqual(ledger.entries.map((entry) => [entry.id, entry.status, entry.cost_usd, entry.key]), [["opening", "imported", 0.5, undefined]], "the same file again replaces its row; the booked row carries no key");
  assert.deepEqual([ledger.totals.usd, ledger.totals.reserved, ledger.totals.reservations], [0.5, 0, 0]);

  // With --judge the hold is in the ledger while the judge looks, and the judge's own call passes the cap.
  const farewell = outsideFile(box, "paid-farewell.mp4", "paid farewell");
  const judged = context(box, fetchImpl, outsideQc());
  assert.equal(await main(bring("farewell", farewell, "--usd", "0.25", "--judge"), judged.ctx), EXIT.ok, judged.out.stderr || judged.out.stdout);
  assert.equal(statusReads, 3, "one status read serves the cap check and the judge");
  assert.deepEqual(heldAtJudge.map((entry) => [entry.id, entry.cost_usd, entry.key, entry.provider, entry.plan, entry.credits, entry.seconds]), [["farewell", 0.25, `import:farewell:${SHA(MP4("paid farewell"))}`, "hailuo-web", "pro", 60, 0]]);
  ledger = readLedger(box.workdir);
  assert.deepEqual([ledger.totals.usd, ledger.totals.judge_calls, ledger.totals.reservations], [0.76, 1, 0]);
  assert.deepEqual(importedTotals(ledger.entries), { clips: 2, clip_seconds: 16, credits: 120, usd: 0.75 });

  // The judge refused past the cap, with the hold counted: the clip is checked but not recorded, and its hold is let go.
  const bird = outsideFile(box, "paid-bird.mp4", "paid bird");
  const refused = context(box, fetchImpl, outsideQc());
  assert.equal(await main(bring("bird", bird, "--usd", "1.24", "--judge"), refused.ctx), EXIT.owner, refused.out.stderr || refused.out.stdout);
  assert.match(refused.out.stderr, /this video has spent US\$2\.00 \(US\$1\.24 of it reserved for 1 request not yet reconciled\) and the next judge call costs about US\$0\.01, past the per-video cap of US\$2/);
  assert.equal(site.state.judges.length, 1, "the judge was not asked");
  assert.equal(manifestOf(box, "clips").shots.bird, undefined);
  ledger = readLedger(box.workdir);
  assert.deepEqual([ledger.totals.usd, ledger.totals.reservations, ledger.entries.length], [0.76, 0, 3]);

  // The STOP file before the import: nothing copied, recorded or held (one that comes later
  // stops it before the judge, with nothing recorded either).
  writeFileSync(path.join(box.workdir, "STOP"), "");
  const stopped = context(box, fetchImpl, outsideQc());
  assert.equal(await main(bring("bird", bird, "--usd", "0.5", "--judge"), stopped.ctx), EXIT.incomplete, stopped.out.stderr || stopped.out.stdout);
  assert.match(stopped.out.stdout, /stopped by the STOP file before anything was drawn or written/);
  assert.deepEqual([readLedger(box.workdir).totals.reservations, readLedger(box.workdir).entries.length], [0, 3]);
  rmSync(path.join(box.workdir, "STOP"));

  // A hold left by a run that died is money the next import sees.
  reserve(box.workdir, { stage: "clips", kind: "clip", id: "sea-storm", provider: "gemini", model: "gemini-omni-1.1-flash", key: "k-dead", seconds: 4, cost_usd: 1 }, new Date("2026-09-26T09:00:00Z"));
  const crowded = context(box, fetchImpl, outsideQc());
  assert.equal(await main(bring("bird", bird, "--usd", "0.3"), crowded.ctx), EXIT.owner, crowded.out.stderr || crowded.out.stdout);
  assert.match(crowded.out.stderr, /spent US\$1\.76 \(US\$1\.00 of it reserved for 1 request not yet reconciled\) and the next import costs about US\$0\.30/);
});

test("clips and music run by hand under the project's STOP file, or while another producer holds it, buy and write nothing", async () => {
  const { box } = prepared();
  await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
  await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
  const site = mediaSite();
  const files = () => ["clips/manifest.json", "music/manifest.json"].map((name) => (existsSync(path.join(box.workdir, name)) ? readFileSync(path.join(box.workdir, name), "utf8") : null));
  const before = files();
  writeFileSync(path.join(box.workdir, "STOP"), "owner hold");
  for (const command of ["clips", "music"]) {
    const run = context(box, site.fetchImpl);
    assert.equal(await main([command, "--slug", box.slug], run.ctx), EXIT.incomplete, command);
    assert.match(run.out.stdout, /stopped by the STOP file before anything was drawn or written/);
  }
  rmSync(path.join(box.workdir, "STOP"));
  writeFileSync(path.join(box.workdir, LEASE_FILE), JSON.stringify({ schema_version: 1, token: "11111111-2222-3333-4444-555555555555", owner: "auto", pid: 4242, host: "video-worker-elsewhere", boot_id: null, start_ticks: null, acquired_at: "2026-10-07T00:00:00.000Z" }));
  for (const command of ["clips", "music"]) {
    const run = context(box, site.fetchImpl);
    assert.equal(await main([command, "--slug", box.slug], run.ctx), EXIT.owner, command);
    assert.match(run.out.stderr + run.out.stdout, /auto \(pid 4242 on video-worker-elsewhere.*nothing was sent or written/);
  }
  assert.deepEqual([site.state.clips.length, site.state.music.length], [0, 0], "nothing was bought");
  assert.deepEqual(files(), before, "nothing was written");
});

test("a selected keyframe or end frame whose bytes changed under an unchanged, approved manifest stops clips and clips import before the site is asked anything", async () => {
  for (const [label, file, args] of [
    ["start", "keyframes/sea-storm-1.png", ["--shot", "sea-storm"]],
    ["end", "keyframes/farewell-end.png", ["--shot", "farewell"]],
    ["import", "keyframes/opening-1.png", null],
  ]) {
    const { box } = prepared();
    await approve({ gate: "look", docDir: box.dir, workdir: box.workdir, note: "test" });
    await approve({ gate: "storyboard", docDir: box.dir, workdir: box.workdir, note: "test" });
    const site = mediaSite();
    let requests = 0;
    const fetchImpl = async (url, init) => {
      requests += 1;
      return site.fetchImpl(url, init);
    };
    const manifest = readFileSync(path.join(box.workdir, "keyframes", "manifest.json"), "utf8");
    // A later take drew over the selected file name; the manifest and its approval did not change.
    writeFileSync(path.join(box.workdir, file), PNG(`redrawn ${label}`));
    const command = args ? ["clips", "--slug", box.slug, ...args] : ["clips", "import", "--slug", box.slug, "--shot", "opening", "--file", outsideFile(box, "made.mp4", "made"), "--provider", "hailuo-web", "--plan", "pro", "--credits", "60", "--usd", "0.5"];
    const run = context(box, fetchImpl, args ? {} : outsideQc());
    assert.equal(await main(command, run.ctx), EXIT.usage, label);
    assert.match(run.out.stderr, new RegExp(`selected picture has changed: ${file.replace(".", "\\.")}`), label);
    assert.equal(requests, 0, `${label}: no status read, upload or submission`);
    assert.deepEqual([site.state.clips.length, site.state.uploads.length], [0, 0]);
    assert.equal(readFileSync(path.join(box.workdir, "keyframes", "manifest.json"), "utf8"), manifest, "the manifest is not rewritten to make it pass");
    assert.equal(existsSync(path.join(box.workdir, "clips", "manifest.json")), false);
    assert.deepEqual(readLedger(box.workdir).entries, [], "nothing held or booked");
  }
});
