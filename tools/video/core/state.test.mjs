import assert from "node:assert/strict";
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { approvalState, approve } from "./approvals.mjs";
import { runtimePolicyHash } from "./anime-policy.mjs";
import { bindAudioEvidence } from "./audio-evidence.mjs";
import { brandingHash, pinBranding } from "./branding.mjs";
import { parseSrt } from "./captions.mjs";
import { lookHash, mixHash, subtitlesHash } from "./drama.mjs";
import { animeRuntimeProof } from "./duration.mjs";
import { dramaFixture, fixture, fixtureLexicon, sandbox, storyFixture, writeAudioFixture } from "./fixtures/load.mjs";
import { atomicWrite, isInside, resolveWorkdir, stopRequested, UsageError } from "./paths.mjs";
import { eachLine, textHash } from "./schema.mjs";
import { localeTexts, runCaptions, StageError } from "./stages.mjs";
import { compilationHash } from "./compilation.mjs";
import { approvedEpisodes, COMPILATION_STEPS, lintProject, loadProject, LOOK_STEPS, narratorOnly, pipelineStatus, recordStage, stepsFor, translationComplete } from "./state.mjs";
import { buildTimeline, estimateTimeline, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from "./timeline.mjs";
import { compilationSandbox, EPISODES, sha, writeEpisode, writeTranslations } from "../compile/fixture.mjs";
import { planRequests } from "../tts/requests.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

/** What the TTS stage will write: a timeline with the hash of the script it was built from. */
function writeTimeline(box) {
  const project = loadProject({ slug: box.slug, root: box.root });
  const timeline = { ...estimateTimeline(project.doc), speech_hash: speechHash(project.doc, project.lexicon) };
  writeAudioFixture(timeline, box.workdir);
  return timeline;
}

function writeAnimePolicy(box, doc) {
  atomicWrite(path.join(box.dir, "video.json"), JSON.stringify(doc));
  atomicWrite(path.join(box.dir, "series.json"), JSON.stringify({
    ...doc.series, category: doc.category, production_policy: doc.production_policy, runtime_spec: doc.runtime_spec,
    target_minutes: doc.target_minutes[0], style_preset: doc.look.preset, characters: doc.characters,
  }));
}

function measuredAnimeTimeline(doc) {
  // Synthetic WAV sample counts exercise status evidence; no real speech or film is generated.
  const samples = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, 5 * SAMPLE_RATE]));
  const last = [...eachLine(doc)].at(-1).line.id;
  samples[last] += (39_600 - buildTimeline(doc, samples).total_frames) * SAMPLES_PER_FRAME;
  return { ...buildTimeline(doc, samples), speech_hash: speechHash(doc, fixtureLexicon()) };
}

function animeStateChecks(doc, timeline, final) {
  const shots = doc.scenes.filter((scene) => scene.template === "shot").map((scene) => {
    const timing = timeline.scenes.find((placed) => placed.id === scene.id);
    const frames = timing.end_frame - timing.start_frame;
    return { shot: scene.id, kind: "clip", fit: { available: frames, mode: "auto", speed: 1, source_frames: frames, stretched: frames, pad: 0, trim: 0 } };
  });
  return {
    ok: true, speech_hash: timeline.speech_hash, visual_hash: visualHash(doc),
    runtime_policy_hash: runtimePolicyHash(doc), final_sha256: sha(final), narration_sha256: timeline.audio_evidence?.narration_sha256,
    look_hash: lookHash(doc), subtitles_hash: subtitlesHash(doc), mix_hash: mixHash(doc), clips_hash: "fixture-clips",
    metrics: { fps: 30, frames: timeline.total_frames, shots },
  };
}

function writeAnimePackage(box, doc, timeline, checks, final) {
  const proof = animeRuntimeProof({ doc, timeline, checks, timelineCurrent: true, finalSha256: sha(final) });
  const metadata = { final_sha256: sha(final), production_policy: doc.production_policy, runtime_spec: doc.runtime_spec, runtime_proof: proof };
  atomicWrite(path.join(box.workdir, "upload", "metadata.json"), JSON.stringify(metadata));
  return metadata;
}

async function animeStateFixture(t) {
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = dramaFixture();
  Object.assign(doc, {
    category: "anime", production_policy: "long-anime-v1", target_minutes: [22, 22],
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { slug: "fantasy", episode: 7, chapter: 1, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false, closed_ending: false },
  });
  doc.look.preset = "anime-2d";
  delete doc.music;
  for (const scene of doc.scenes) delete scene.data.fit;
  writeAnimePolicy(box, doc);
  assert.deepEqual(lintProject(loadProject({ slug: box.slug, root: box.root })).errors, []);
  // Silent takes and narration of the measured lengths carry the timeline's audio evidence.
  const timeline = writeAudioFixture(measuredAnimeTimeline(doc), box.workdir);
  const final = Buffer.from("local anime status fixture, not real media");
  const checks = animeStateChecks(doc, timeline, final);
  atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify(checks));
  atomicWrite(path.join(box.workdir, "final.mp4"), final);
  atomicWrite(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visualHash(doc), speech_hash: timeline.speech_hash, subtitles_hash: subtitlesHash(doc) }));
  atomicWrite(path.join(box.workdir, "clips", "manifest.json"), JSON.stringify({ speech_hash: timeline.speech_hash, visual_hash: visualHash(doc), look_hash: lookHash(doc), clips_hash: "fixture-clips", shots: {} }));
  atomicWrite(path.join(box.dir, "script.md"), "# Local screenplay fixture\n");
  const lineKeys = Object.fromEntries(planRequests(doc, fixtureLexicon()).flatMap((request) => request.lines).map((line) => [line.id, line.key]));
  atomicWrite(path.join(box.workdir, "audio", "cache.json"), JSON.stringify({ lines: lineKeys }));
  const metadata = writeAnimePackage(box, doc, timeline, checks, final);
  const places = { docDir: box.dir, workdir: box.workdir };
  for (const gate of ["script", "audio", "final", "publish"]) await approve({ gate, ...places });
  return { ...box, doc, timeline, final, checks, metadata, places, lineKeys };
}

const stepOf = (state, id) => state.steps.find((step) => step.id === id);
const DELIVERY_STEPS = ["video assembled", "final video approved", "upload package"];

test("anime budget changes invalidate measured timing and delivery approvals while reusing unchanged voice clips", async (t) => {
  const box = await animeStateFixture(t);
  const status = () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  const initial = await status();
  for (const id of ["script approved", "narration synthesized", "narration approved", ...DELIVERY_STEPS]) assert.equal(stepOf(initial, id).done, true, id);
  const audioBytes = Object.fromEntries(Object.keys(box.lineKeys).map((id) => [id, readFileSync(path.join(box.workdir, "audio", `${id}.wav`))]));
  const changed = { ...box.doc, runtime_spec: { ...box.doc.runtime_spec, op_ed_budget_seconds: 120, slot_reserve_seconds: 360 } };
  writeAnimePolicy(box, changed);
  assert.equal(speechHash(changed, fixtureLexicon()), box.timeline.speech_hash);
  assert.equal(visualHash(changed), box.checks.visual_hash);
  assert.notEqual(runtimePolicyHash(changed), box.checks.runtime_policy_hash);
  assert.deepEqual(Object.fromEntries(planRequests(changed, fixtureLexicon()).flatMap((request) => request.lines).map((line) => [line.id, line.key])), box.lineKeys);
  const stale = await status();
  for (const id of ["script approved", "narration synthesized", "narration approved", ...DELIVERY_STEPS]) assert.equal(stepOf(stale, id).done, false, id);
  assert.match(stepOf(stale, "narration synthesized").note, /current measured runtime policy/);
  assert.equal(stepOf(stale, "frames rendered").done, true, "unchanged visual frames remain reusable");
  for (const gate of ["script", "audio", "final", "publish"]) assert.equal((await approvalState({ gate, ...box.places })).status, "stale", gate);

  // tts reuses the unchanged takes and binds them to the refreshed timeline.
  const timeline = bindAudioEvidence(measuredAnimeTimeline(changed), box.workdir);
  atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  assert.equal(stepOf(await status(), "narration synthesized").done, true);
  assert.equal(stepOf(await status(), "narration approved").done, false);
  await approve({ gate: "audio", ...box.places });
  assert.equal(stepOf(await status(), "narration approved").done, true);
  assert.equal(stepOf(await status(), "video assembled").done, false, "a refreshed timeline alone cannot refresh the cut receipt");
  const checks = animeStateChecks(changed, timeline, box.final);
  atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify(checks));
  assert.equal(stepOf(await status(), "video assembled").done, true);
  assert.equal(stepOf(await status(), "final video approved").done, false, "unchanged final bytes still need approval for the new runtime policy");
  await approve({ gate: "final", ...box.places });
  assert.equal(stepOf(await status(), "final video approved").done, true);
  assert.equal(stepOf(await status(), "upload package").done, false);
  writeAnimePackage(box, changed, timeline, checks, box.final);
  assert.equal(stepOf(await status(), "upload package").done, true);
  await approve({ gate: "script", ...box.places });
  await approve({ gate: "publish", ...box.places });
  for (const gate of ["script", "audio", "final", "publish"]) assert.equal((await approvalState({ gate, ...box.places })).status, "approved", gate);
  for (const [id, bytes] of Object.entries(audioBytes)) assert.deepEqual(readFileSync(path.join(box.workdir, "audio", `${id}.wav`)), bytes);
  assert.deepEqual(JSON.parse(readFileSync(path.join(box.workdir, "audio", "cache.json"), "utf8")).lines, box.lineKeys);
});

test("anime episode context changes invalidate timing and final evidence even when text and media bytes stay the same", async (t) => {
  const box = await animeStateFixture(t);
  for (const [key, value] of [["slug", "other-fantasy"], ["episode", 8], ["chapter", 2], ["planned_episodes", 121], ["open_ended", true]]) {
    const changed = { ...box.doc, series: { ...box.doc.series, [key]: value } };
    writeAnimePolicy(box, changed);
    assert.equal(speechHash(changed, fixtureLexicon()), box.timeline.speech_hash, key);
    assert.notEqual(runtimePolicyHash(changed), box.checks.runtime_policy_hash, key);
    const state = await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
    assert.deepEqual(state.lint.errors, [], key);
    for (const id of ["narration synthesized", "narration approved", ...DELIVERY_STEPS]) assert.equal(stepOf(state, id).done, false, `${key}: ${id}`);
    assert.equal(stepOf(state, "frames rendered").done, true, key);
  }
  writeAnimePolicy(box, box.doc);
  const restored = await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  for (const id of ["narration synthesized", "narration approved", ...DELIVERY_STEPS]) assert.equal(stepOf(restored, id).done, true, id);
});

test("anime status refuses estimated timing, replaced final bytes and incomplete current package proofs", async (t) => {
  const box = await animeStateFixture(t);
  const status = () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  for (const [name, timeline, checks] of [
    ["estimate", { ...box.timeline, timing_basis: "estimated" }, box.checks],
    ["missing policy", { ...box.timeline, runtime_policy_hash: undefined }, box.checks],
    ["short body", { ...box.timeline, total_frames: 3_600 }, { ...box.checks, metrics: { ...box.checks.metrics, frames: 3_600 } }],
    ["stale final receipt", box.timeline, { ...box.checks, final_sha256: "f".repeat(64) }],
    ["missing shot receipts", box.timeline, { ...box.checks, metrics: { ...box.checks.metrics, shots: [] } }],
    ["slowed clip", box.timeline, { ...box.checks, metrics: { ...box.checks.metrics, shots: box.checks.metrics.shots.map((shot, index) => index === 0 ? { ...shot, fit: { ...shot.fit, speed: 0.85 } } : shot) } }],
    ["held clip tail", box.timeline, { ...box.checks, metrics: { ...box.checks.metrics, shots: box.checks.metrics.shots.map((shot, index) => index === 0 ? { ...shot, fit: { ...shot.fit, pad: 1 } } : shot) } }],
  ]) {
    atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
    atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify(checks));
    const state = await status();
    for (const id of DELIVERY_STEPS) assert.equal(stepOf(state, id).done, false, `${name}: ${id}`);
    if (name === "estimate" || name === "missing policy") assert.equal(stepOf(state, "narration synthesized").done, false, name);
  }
  atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(box.timeline));
  atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify(box.checks));
  atomicWrite(path.join(box.workdir, "final.mp4"), "replacement local anime fixture, not real media");
  for (const id of DELIVERY_STEPS) assert.equal(stepOf(await status(), id).done, false, id);
  atomicWrite(path.join(box.workdir, "final.mp4"), box.final);
  for (const [name, proof] of [
    ["missing proof", undefined],
    ["estimated proof", { ...box.metadata.runtime_proof, basis: "estimated" }],
    ["wrong body", { ...box.metadata.runtime_proof, body_frames: 39_601 }],
    ["wrong presentation", { ...box.metadata.runtime_proof, presentation_frames: 39_601 }],
    ["wrong episode", { ...box.metadata.runtime_proof, runtime_context: { ...box.metadata.runtime_proof.runtime_context, episode: 8 } }],
    ["unknown field", { ...box.metadata.runtime_proof, unverified: true }],
  ]) {
    atomicWrite(path.join(box.workdir, "upload", "metadata.json"), JSON.stringify({ ...box.metadata, runtime_proof: proof }));
    const state = await status();
    assert.equal(stepOf(state, "video assembled").done, true, name);
    assert.equal(stepOf(state, "final video approved").done, true, name);
    assert.equal(stepOf(state, "upload package").done, false, name);
  }
  atomicWrite(path.join(box.workdir, "upload", "metadata.json"), JSON.stringify(box.metadata));
  for (const id of DELIVERY_STEPS) assert.equal(stepOf(await status(), id).done, true, id);
});

test("the work directory is <base>/<slug> and never inside the repository", () => {
  const box = sandbox();
  assert.equal(resolveWorkdir({ flag: box.work, slug: "a", root: box.root }), path.join(box.work, "a"));
  assert.equal(resolveWorkdir({ env: { VIDEO_WORKDIR: box.work }, slug: "a", root: box.root }), path.join(box.work, "a"));
  // With neither, videos go under the home directory, so nobody has to set a variable first.
  assert.equal(resolveWorkdir({ env: {}, slug: "a", root: box.root, home: box.base }), path.join(box.base, "mokaair-work", "videos", "a"));
  assert.throws(() => resolveWorkdir({ env: {}, slug: "a", root: box.root, home: box.root }), UsageError);
  assert.throws(() => resolveWorkdir({ flag: path.join(box.root, "tmp"), slug: "a", root: box.root }), /inside the repository/);
  assert.ok(isInside(path.join(box.root, "x", "y"), box.root));
  assert.ok(!isInside(box.work, box.root));
});

test("atomicWrite leaves the finished file and no temporary", () => {
  const box = sandbox();
  const file = path.join(box.workdir, "deep", "a.json");
  atomicWrite(file, "{}");
  atomicWrite(file, '{"b":1}');
  assert.equal(readFileSync(file, "utf8"), '{"b":1}');
  assert.deepEqual(readdirSync(path.dirname(file)), ["a.json"]);
});

test("a STOP file in the video's directory or the base above it asks stages to stop", () => {
  const box = sandbox();
  mkdirSync(box.workdir);
  assert.ok(!stopRequested(box.workdir));
  writeFileSync(path.join(box.work, "STOP"), "");
  assert.ok(stopRequested(box.workdir));
});

test("an approval binds the exact file and goes stale when the file changes", async () => {
  const box = sandbox();
  const places = { docDir: box.dir, workdir: box.workdir };
  assert.equal((await approvalState({ gate: "outline", ...places })).status, "missing");
  assert.equal((await approvalState({ gate: "final", ...places })).status, "absent");
  const entry = await approve({ gate: "outline", ...places, now: new Date("2026-09-24T01:00:00Z"), note: "owner chose outline B" });
  assert.equal(entry.file, "brief.md");
  assert.equal((await approvalState({ gate: "outline", ...places })).status, "approved");
  appendFileSync(path.join(box.dir, "brief.md"), "\n一行新增的字\n");
  assert.equal((await approvalState({ gate: "outline", ...places })).status, "stale");
  await assert.rejects(approve({ gate: "final", ...places }), /does not exist yet/);
});

test("status walks the checklist and names the next command", async () => {
  const box = sandbox();
  const status = async () => (await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir })).next;
  assert.match((await status()).todo, /approve --slug fixture-minimal --gate outline/);
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir });
  assert.equal((await status()).id, "fact-checked");
  writeFileSync(path.join(box.dir, "verify-1.md"), "# 查核\n");
  assert.equal((await status()).id, "narration synthesized");
  writeTimeline(box);
  assert.equal((await status()).id, "narration approved");
  await approve({ gate: "audio", docDir: box.dir, workdir: box.workdir });
  const next = await status();
  assert.equal(next.id, "frames rendered");
  assert.match(next.todo, /cli\.mjs render --slug fixture-minimal/);
});

test("editing the script after synthesis makes the narration stale again", async () => {
  const box = sandbox();
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir });
  writeFileSync(path.join(box.dir, "verify-1.md"), "ok");
  writeTimeline(box);
  const file = path.join(box.dir, "video.json");
  writeFileSync(file, readFileSync(file, "utf8").replace("今天用三個問題", "今天只用三個問題"));
  const status = await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.equal(status.next.id, "narration synthesized");
  assert.equal(status.next.note, "timeline.json was built for an older script");
});

test("branding pins invalidate presentation artifacts without invalidating narration or following a new channel default", async () => {
  const box = sandbox();
  const timeline = writeTimeline(box);
  const project = loadProject({ slug: box.slug, root: box.root });
  const brand = { schema_version: 1, id: "first", intro: { file: "intro.mp4", sha256: "a".repeat(64), frames: 150 }, outro: { file: "outro.mp4", sha256: "b".repeat(64), frames: 90 } };
  pinBranding(box.workdir, brand);
  const hash = brandingHash(brand);
  atomicWrite(path.join(box.workdir, "checks.json"), JSON.stringify({ ok: true, narration_sha256: timeline.audio_evidence.narration_sha256, speech_hash: timeline.speech_hash, visual_hash: visualHash(project.doc), branding: { hash, body_frames: timeline.total_frames } }));
  atomicWrite(path.join(box.workdir, "captions", "manifest.json"), JSON.stringify({ speech_hash: timeline.speech_hash, branding_hash: hash }));
  atomicWrite(path.join(box.workdir, "final.mp4"), "approved branded bytes");
  const final = await approve({ gate: "final", docDir: box.dir, workdir: box.workdir });
  await approve({ gate: "audio", docDir: box.dir, workdir: box.workdir });
  atomicWrite(path.join(box.workdir, "upload", "metadata.json"), JSON.stringify({ final_sha256: final.sha256, branding_hash: hash }));
  const status = async () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  const done = (state, id) => state.steps.find((step) => step.id === id).done;
  for (const id of ["video assembled", "captions written", "final video approved", "upload package"]) assert.equal(done(await status(), id), true, id);
  const nextBrand = { ...brand, intro: { ...brand.intro, sha256: "c".repeat(64) } };
  atomicWrite(path.join(box.work, "_branding", "current.json"), JSON.stringify(nextBrand));
  assert.equal(done(await status(), "video assembled"), true, "changing the default never changes an old pin");
  pinBranding(box.workdir, nextBrand);
  for (const id of ["video assembled", "captions written", "final video approved", "upload package"]) assert.equal(done(await status(), id), false, id);
  assert.equal(done(await status(), "narration approved"), true, "body TTS timing and approval are unchanged");
});

test("captions: zh-TW always, a translated locale only when every line is current", () => {
  const box = sandbox();
  assert.throws(() => runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir }), StageError);
  writeTimeline(box);
  const project = loadProject({ slug: box.slug, root: box.root });
  const lines = Object.fromEntries([...eachLine(project.doc)].map(({ line }) => [line.id, { source_hash: textHash(line.text), text: `English for ${line.id}.` }]));
  mkdirSync(path.join(box.dir, "i18n"));
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify({ lines }));
  writeFileSync(path.join(box.dir, "i18n", "ja.json"), JSON.stringify({ lines: { ...lines, k7p2: { source_hash: "stale0000000", text: "古い" } } }));

  const manifest = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir, now: new Date("2026-09-24T02:00:00Z") });
  assert.deepEqual(Object.keys(manifest.locales).sort(), ["en", "zh-TW"]);
  assert.deepEqual(manifest.skipped, { ja: ["k7p2"] });
  assert.deepEqual(manifest.chapters, []);
  const zh = parseSrt(readFileSync(path.join(box.workdir, "captions", "zh-TW.srt"), "utf8"));
  // 32 characters: one cue, two lines of at most 16. No comma lets both halves fit, so the break
  // falls at the middle.
  assert.equal(zh[0].text, "每次有新模型出來，排行榜就換一次\n第一名，你真的每次都要跟著換嗎？");
  assert.ok(existsSync(path.join(box.workdir, "captions", "en.vtt")));
  assert.ok(!existsSync(path.join(box.workdir, "captions", "ja.srt")));
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.deepEqual(state.runs.map((run) => run.stage), ["captions"]);
});

test("localeTexts leaves out translations older than their line", () => {
  const box = sandbox();
  const { doc } = loadProject({ slug: box.slug, root: box.root });
  const { texts, skipped } = localeTexts(doc, { ko: { lines: { k7p2: { source_hash: textHash(doc.scenes[0].lines[0].text), text: "안녕" } } } });
  assert.equal(texts.ko.k7p2, "안녕");
  assert.equal(skipped.ko.length, 6);
});

test("a drama with no characters walks no look steps, and its status never reads the character files", async () => {
  const doc = storyFixture();
  assert.equal(narratorOnly(doc), true);
  assert.equal(narratorOnly(dramaFixture()), false);
  assert.equal(narratorOnly(fixture()), false, "a slides video has no look at all");
  const cast = { ...doc, characters: dramaFixture().characters.slice(0, 1) };
  assert.deepEqual(stepsFor(doc), stepsFor(cast).filter((id) => !LOOK_STEPS.includes(id)), "only the look steps go");
  for (const drama of [cast, dramaFixture()]) assert.ok(LOOK_STEPS.every((id) => stepsFor(drama).includes(id)), "a drama with characters keeps its look steps");

  const box = sandbox("fixture-story", "story");
  const status = async () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.deepEqual((await status()).steps.map((step) => step.id), stepsFor(doc));
  // Character files nobody can parse: a status that read them would throw.
  mkdirSync(path.join(box.workdir, "characters"), { recursive: true });
  writeFileSync(path.join(box.workdir, "characters", "manifest.json"), "{ not json");
  writeFileSync(path.join(box.workdir, "characters", "choice.json"), "{ not json");
  const places = { docDir: box.dir, workdir: box.workdir };
  await approve({ gate: "outline", ...places });
  writeFileSync(path.join(box.dir, "verify-1.md"), "# 查核\n");
  // The script gate, which an episode of a series has, is settled whatever the look does.
  writeFileSync(path.join(box.dir, "script.md"), "# 劇本\n");
  await approve({ gate: "script", ...places });
  assert.equal((await status()).next.id, "narration synthesized", "nothing to draw or choose before the narration");
  writeTimeline(box);
  await approve({ gate: "audio", ...places });
  assert.equal((await status()).next.id, "keyframes drawn");

  const project = loadProject({ slug: box.slug, root: box.root });
  const visual = visualHash(project.doc);
  const shots = Object.fromEntries(project.doc.scenes.filter((scene) => scene.template === "shot").map((scene) => [scene.id, { file: `keyframes/${scene.id}-1.png` }]));
  atomicWrite(path.join(box.workdir, "keyframes", "manifest.json"), JSON.stringify({ look_hash: lookHash(project.doc), visual_hash: visual, shots }));
  assert.equal((await status()).next.id, "storyboard approved");
  await approve({ gate: "storyboard", ...places });
  assert.equal((await status()).next.id, "frames rendered");
  atomicWrite(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visual, speech_hash: speechHash(project.doc, project.lexicon), subtitles_hash: subtitlesHash(project.doc) }));
  assert.equal((await status()).next.id, "clips generated");
});

test("recordStage appends runs for the handover", () => {
  const box = sandbox();
  recordStage(box.workdir, "tts", { lines: 7 }, new Date("2026-09-24T03:00:00Z"));
  recordStage(box.workdir, "render", {}, new Date("2026-09-24T03:05:00Z"));
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.deepEqual(state.runs, [
    { stage: "tts", at: "2026-09-24T03:00:00.000Z", lines: 7 },
    { stage: "render", at: "2026-09-24T03:05:00.000Z" },
  ]);
});

test("a compilation walks its own steps: planned metadata, cards, the join, the translations, then the shared gates", async () => {
  const box = compilationSandbox({ rendered: false, planned: false });
  const status = async () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  const project = loadProject({ slug: box.slug, root: box.root });
  assert.equal(stepsFor(project.doc), COMPILATION_STEPS);
  assert.deepEqual(lintProject(project).errors, [], "the placeholder document passes lint");
  let state = await status();
  assert.deepEqual(state.steps.map((step) => step.id), COMPILATION_STEPS);
  assert.equal(state.next.id, "metadata planned");
  assert.match(state.next.note, /placeholder/);
  assert.match(state.next.todo, /plans the compilation's title/);
  assert.deepEqual(state.dubs, {});

  // The planner's work, and the thumbnail's source keyframe the worker copies in.
  const planned = compilationSandbox({ rendered: false });
  const plannedStatus = async () => pipelineStatus({ slug: planned.slug, root: planned.root, workdir: planned.workdir });
  state = await plannedStatus();
  assert.equal(state.steps[0].done, true);
  assert.equal(state.next.id, "cards rendered");
  assert.match(state.next.todo, /render --slug wuxia-full/);

  // The cards drawn: the join is next, and it wants every episode cleared.
  const drawn = compilationSandbox();
  const drawnStatus = async () => pipelineStatus({ slug: drawn.slug, root: drawn.root, workdir: drawn.workdir });
  state = await drawnStatus();
  assert.equal(state.steps[1].done, true);
  assert.equal(state.next.id, "video compiled");
  assert.match(state.next.todo, /compile --slug wuxia-full/);
  writeEpisode(drawn.work, "wuxia-ep-2", { approved: false });
  state = await drawnStatus();
  assert.equal(state.next.note, "episodes not cleared for upload: wuxia-ep-2");
  const cleared = writeEpisode(drawn.work, "wuxia-ep-2");
  const episodes = approvedEpisodes(drawn.doc, drawn.work);
  assert.deepEqual(episodes.map((episode) => episode.slug), EPISODES);
  assert.equal(episodes[1].sha256, cleared.sha256);
  // What compile leaves behind, for these very cuts and cards.
  const hash = compilationHash(drawn.doc, episodes);
  atomicWrite(path.join(drawn.workdir, "checks.json"), JSON.stringify({ ok: true, compilation_hash: hash, visual_hash: visualHash(drawn.doc), problems: [] }));
  atomicWrite(path.join(drawn.workdir, "captions", "manifest.json"), JSON.stringify({ compilation_hash: hash, locales: {}, skipped: {} }));
  writeFileSync(path.join(drawn.workdir, "final.mp4"), "joined");
  state = await drawnStatus();
  assert.equal(state.steps[2].done, true);
  assert.equal(state.next.id, "metadata translated");
  assert.match(state.next.todo, /i18n\/<locale>\.json with title, description, tags and chapters for en, ja, ko, zh-CN/);
  // A re-cut episode voids the join.
  writeEpisode(drawn.work, "wuxia-ep-3");
  state = await drawnStatus();
  assert.equal(state.next.id, "video compiled");
  assert.equal(state.next.note, "checks.json was written for other cuts or cards");
  atomicWrite(path.join(drawn.workdir, "checks.json"), JSON.stringify({ ok: true, compilation_hash: compilationHash(drawn.doc, approvedEpisodes(drawn.doc, drawn.work)), visual_hash: visualHash(drawn.doc), problems: [] }));
  atomicWrite(path.join(drawn.workdir, "captions", "manifest.json"), JSON.stringify({ compilation_hash: compilationHash(drawn.doc, approvedEpisodes(drawn.doc, drawn.work)), locales: {}, skipped: {} }));
  writeTranslations(drawn, drawn.doc);
  state = await drawnStatus();
  assert.equal(state.next.id, "final video approved");
  assert.match(state.next.todo, /approve --slug wuxia-full --gate final/);
  assert.equal(translationComplete({ title: "t", description: "d", tags: ["t"], chapters: {} }), true);
  assert.equal(translationComplete({ title: "t", description: "d", tags: [], chapters: {} }), false, "an empty tags list reads as untranslated in lint, so it is not complete");
  assert.equal(translationComplete({ title: "t", description: "d", tags: ["t"] }), false);
  assert.equal(translationComplete(null), false);
  assert.equal(sha("x").length, 64);
});

test("illustrated slides walk the picture and music steps, bound to the shots rather than the cards", async () => {
  const { illustratedFixture } = await import("./fixtures/load.mjs");
  const { ARTIFACTS, ILLUSTRATED_STEPS, SLIDES_STEPS } = await import("./state.mjs");
  const { keyframesHash, lookHash, mixHash, picturesHash, sfxHash } = await import("./drama.mjs");
  const { visualHash } = await import("./timeline.mjs");
  const doc = illustratedFixture();
  assert.deepEqual(stepsFor(doc), ILLUSTRATED_STEPS);
  assert.deepEqual(stepsFor({ ...doc, music: undefined }), ILLUSTRATED_STEPS.filter((id) => id !== "music generated"));
  assert.equal(stepsFor(fixture()), SLIDES_STEPS, "plain slides keep their twelve steps");
  const box = sandbox("fixture-illustrated", "illustrated");
  mkdirSync(box.workdir, { recursive: true });
  const write = (name, value) => {
    mkdirSync(path.dirname(path.join(box.workdir, name)), { recursive: true });
    writeFileSync(path.join(box.workdir, name), JSON.stringify(value));
  };
  const status = () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  const ids = (state) => state.steps.map((step) => step.id);
  const done = (state, id) => state.steps.find((step) => step.id === id).done;
  assert.deepEqual(ids(await status()), ILLUSTRATED_STEPS);
  // Keyframes bound to the look and the shots: a card edit does not undo them, a camera edit does.
  const shots = Object.fromEntries(doc.scenes.filter((scene) => scene.template === "shot").map((scene) => [scene.id, { file: `keyframes/${scene.id}.png`, sha256: "a".repeat(64) }]));
  write(ARTIFACTS.keyframes, { look_hash: lookHash(doc), pictures_hash: picturesHash(doc), shots });
  assert.equal(done(await status(), "keyframes drawn"), true);
  const edited = illustratedFixture();
  edited.scenes[0].data.title = "改了標題";
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(edited));
  assert.equal(done(await status(), "keyframes drawn"), true, "a card edit leaves the pictures drawn");
  edited.scenes[1].data.camera = "pan left";
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(edited));
  assert.equal(done(await status(), "keyframes drawn"), false, "a camera edit asks for the picture again");
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  // The cut is current only when it was made from these pictures, this music and these effects.
  const timeline = writeTimeline(box);
  const checks = { ok: true, narration_sha256: timeline.audio_evidence.narration_sha256, speech_hash: (await status()).steps && null, visual_hash: visualHash(doc), look_hash: lookHash(doc), pictures_hash: keyframesHash(doc, { shots }), mix_hash: mixHash(doc), sfx_hash: sfxHash(doc) };
  write(ARTIFACTS.music, { mix_hash: mixHash(doc), file: "music/bed.mp3" });
  assert.equal(done(await status(), "music generated"), true);
  const { speechHash } = await import("./timeline.mjs");
  const project = loadProject({ slug: box.slug, root: box.root });
  checks.speech_hash = speechHash(project.doc, project.lexicon);
  write(ARTIFACTS.checks, checks);
  writeFileSync(path.join(box.workdir, ARTIFACTS.video), "");
  assert.equal(done(await status(), "video assembled"), true);
  write(ARTIFACTS.checks, { ...checks, pictures_hash: keyframesHash(doc, { shots: { ...shots, podium: { ...shots.podium, sha256: "b".repeat(64) } } }) });
  assert.equal(done(await status(), "video assembled"), false, "a redrawn picture asks for the cut again");
  write(ARTIFACTS.checks, { ...checks, sfx_hash: "0000000000000000" });
  assert.equal(done(await status(), "video assembled"), false, "other sound effects ask for the cut again");
});
