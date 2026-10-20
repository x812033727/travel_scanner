// Technical QA for an UNAPPROVED X05 local concept. Never an upload approval.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { sha256File } from "../../../../tools/video/core/approvals.mjs";
import { audioEvidenceProblems } from "../../../../tools/video/core/audio-evidence.mjs";
import { buildCues, checkCues, toSrt, toVtt } from "../../../../tools/video/core/captions.mjs";
import { lookHash, mixHash } from "../../../../tools/video/core/drama.mjs";
import { isInside, resolveWorkdir, ROOT } from "../../../../tools/video/core/paths.mjs";
import { lintProject, loadProject } from "../../../../tools/video/core/state.mjs";
import { speechHash, visualHash } from "../../../../tools/video/core/timeline.mjs";
import { readLedger, totalsOf } from "../../../../tools/video/media/ledger.mjs";
import { themeHash } from "../../../../tools/video/render/plan.mjs";
import { INTRO_FRAMES, OUTRO_FRAMES } from "../local-preview-bookends.mjs";
import { previewDurations, renderedCardEvidence, shiftPreviewCues, unsafeSelectedPicture } from "../local-preview.mjs";

const SLUG = "story-everyday-meta-x05";
const FPS = 30;
const CAP_USD = 25;
const read = (file) => JSON.parse(readFileSync(file, "utf8"));
const inside = (workdir, name) => {
  const file = path.resolve(workdir, name);
  assert.ok(isInside(file, workdir), `media path escapes workdir: ${name}`);
  return file;
};
const run = (tool, args) => {
  const done = spawnSync(tool, args, { encoding: "utf8", maxBuffer: 20 * 1024 * 1024, timeout: 20 * 60_000 });
  if (done.error || done.status !== 0) throw new Error(`${tool}: ${done.error?.message ?? done.stderr?.trim() ?? done.status}`);
  return done;
};

async function main() {
  const { values } = parseArgs({ args: process.argv.slice(2), options: {
    workdir: { type: "string" }, "inputs-only": { type: "boolean" },
  }, strict: true });
  assert.ok(values.workdir, "pass --workdir <media base>");
  const workdir = resolveWorkdir({ flag: values.workdir, slug: SLUG, root: ROOT });
  const project = loadProject({ slug: SLUG, root: ROOT });
  const { doc, lexicon, dir } = project;
  assert.deepEqual(lintProject(project).errors, [], "current project lint");
  const scriptSha = await sha256File(path.join(dir, "video.json"));
  for (const receipt of ["source-review-v14-visual-timing.md", "blind-o-v14-final.md", "blind-p-v14-final.md"]) {
    assert.ok(readFileSync(path.join(dir, "reviews", receipt), "utf8").includes(scriptSha), `review receipt is not bound to current video.json: ${receipt}`);
  }
  const timelineFile = inside(workdir, "timeline.json");
  const timeline = read(timelineFile);
  assert.equal(timeline.fps, FPS);
  assert.equal(timeline.speech_hash, speechHash(doc, lexicon), "speech hash drift");
  assert.deepEqual(audioEvidenceProblems(timeline, workdir), [], "audio evidence drift");
  const measured = previewDurations(timeline, doc);
  assert.ok(measured.hookFrames >= 30 * FPS && measured.hookFrames <= 60 * FPS, "hook outside 30–60s");
  assert.ok(measured.substantiveBodyFrames >= 8 * 60 * FPS, "strict body under eight minutes");
  assert.ok(measured.closingStartFrame < timeline.total_frames, "closing boundary after native end");
  const expectedFrames = timeline.total_frames + INTRO_FRAMES + OUTRO_FRAMES;

  const checkFile = inside(workdir, "review/check.json");
  const flagsFile = inside(workdir, "review/check-flags.json");
  assert.ok(existsSync(checkFile) && existsSync(flagsFile), "check-audio evidence missing");
  const checked = read(checkFile);
  const flags = read(flagsFile);
  assert.deepEqual(Object.keys(checked.lines ?? {}).sort(), timeline.lines.map((line) => line.id).sort(), "not every current narrated line was checked");
  assert.equal(flags.speech_hash, timeline.speech_hash, "spoken-line verdict belongs to another script");
  assert.ok(Array.isArray(flags.flags), "check-audio flags are missing");
  assert.ok(flags.flags.every((id) => checked.lines[id]), "audio flag is not one of the current lines");

  const keyframeFile = inside(workdir, "keyframes/manifest.json");
  const keyframes = read(keyframeFile);
  assert.equal(keyframes.look_hash, lookHash(doc));
  assert.equal(keyframes.visual_hash, visualHash(doc));
  assert.deepEqual(keyframes.image, { provider: "minimax", model: "image-01" }, "illustration model changed");
  const shots = doc.scenes.filter((scene) => scene.template === "shot" && !scene.data?.source);
  assert.equal(Object.keys(keyframes.shots ?? {}).length, shots.length);
  assert.ok(shots.length / doc.scenes.length >= 0.70, "genuine MiniMax scene share under 70%");
  let cardRun = 0;
  let maxCardRun = 0;
  for (const scene of doc.scenes) {
    cardRun = scene.template === "stats" ? cardRun + 1 : 0;
    maxCardRun = Math.max(maxCardRun, cardRun);
    assert.ok(cardRun <= 3, "more than three native cards consecutively");
  }
  const generationCache = read(inside(workdir, "media/cache.json"));
  const mediaLedger = readLedger(workdir);
  const reviewNeeded = [];
  for (const scene of shots) {
    const shot = keyframes.shots[scene.id];
    assert.ok(shot?.file && /^[a-f0-9]{64}$/.test(shot.sha256 ?? ""), `incomplete picture: ${scene.id}`);
    assert.equal(await sha256File(inside(workdir, shot.file)), shot.sha256, `picture bytes drift: ${scene.id}`);
    assert.deepEqual(unsafeSelectedPicture(shot), [], `selected picture has a hard redraw fault: ${scene.id}`);
    assert.ok(shot.takes?.some((take) => take.file === shot.file && take.sha256 === shot.sha256 && take.key === shot.key && take.judge?.passed === true),
      `selected picture is not a passed take: ${scene.id}`);
    const cached = generationCache.entries?.[shot.key];
    assert.equal(cached?.provider, "minimax", `image origin changed: ${scene.id}`);
    assert.equal(cached?.model, "image-01", `image model changed: ${scene.id}`);
    assert.equal(await sha256File(inside(workdir, cached.file)), cached.sha256, `raw MiniMax picture bytes drift: ${scene.id}`);
    assert.ok(mediaLedger.entries.some((entry) => entry.stage === "keyframes" && entry.kind === "image" && entry.id === scene.id
      && entry.key === shot.key && entry.provider === "minimax" && entry.model === "image-01" && entry.status === "ready"),
    `no paid MiniMax image receipt: ${scene.id}`);
    if (shot.needs_review || shot.judge?.passed === false) reviewNeeded.push(scene.id);
  }

  const framesFile = inside(workdir, "frames/manifest.json");
  const frames = read(framesFile);
  assert.equal(frames.visual_hash, visualHash(doc));
  assert.equal(frames.theme_hash, themeHash());
  assert.equal(frames.scenes.length, doc.scenes.length);
  const cardEvidence = await renderedCardEvidence(frames, workdir);
  assert.deepEqual(cardEvidence.issues, []);
  const thumbnailFile = inside(workdir, "thumbnail.jpg");
  assert.ok(existsSync(thumbnailFile), "thumbnail missing");

  const officialMusicFile = inside(workdir, "music/manifest.json");
  const musicManifestFile = existsSync(officialMusicFile) ? officialMusicFile : inside(workdir, "review/local-preview/reused-music.json");
  const music = read(musicManifestFile);
  assert.equal(music.mix_hash, mixHash(doc), "music mix drift");
  assert.equal(await sha256File(inside(workdir, music.file)), music.sha256, "music bytes drift");
  if (music.source === "local-concept-reuse") {
    assert.equal(music.reused_from?.source, "generated");
    assert.equal(music.reused_from?.sha256, music.sha256);
    const sourceDir = path.join(path.dirname(workdir), music.reused_from.slug);
    const originalManifest = path.join(sourceDir, "music/manifest.json");
    assert.equal(await sha256File(originalManifest), music.reused_from.original_manifest_sha256, "original track manifest drift");
    assert.equal(await sha256File(path.join(sourceDir, music.reused_from.file)), music.sha256, "original track bytes drift");
  }
  const ledger = mediaLedger;
  const totals = totalsOf(ledger.entries);
  assert.deepEqual(totals, ledger.totals, "ledger total drift");
  assert.equal(totals.reservations, 0, "unresolved paid media reservation");
  assert.ok(totals.usd <= CAP_USD, "visible media ledger exceeds US$25");

  const texts = Object.fromEntries(doc.scenes.flatMap((scene) => (scene.lines ?? []).map((line) => [line.id, line.text])));
  const { cues, missing } = buildCues(timeline, texts, "zh-TW");
  assert.deepEqual(missing, [], "captions missing line text");
  const shifted = shiftPreviewCues(cues, timeline, measured.hookFrames);
  assert.deepEqual(checkCues(shifted, "zh-TW"), [], "caption timing/reading speed");
  const expectedCaptions = { srt: Buffer.from(toSrt(shifted)), vtt: Buffer.from(toVtt(shifted)) };
  const stem = reviewNeeded.length || flags.flags.length ? "preview-review-needed" : "preview";
  const previewDir = inside(workdir, "review/local-preview");
  const output = {
    mp4: path.join(previewDir, `${stem}.mp4`),
    srt: path.join(previewDir, `${stem}.zh-TW.srt`),
    vtt: path.join(previewDir, `${stem}.zh-TW.vtt`),
    sidecar: path.join(previewDir, `${stem}.json`),
    narrationReview: path.join(previewDir, "narration-review.mp3"),
  };
  const summary = {
    technical: values["inputs-only"] ? "INPUTS_READY" : "PASS",
    quality_review: flags.flags.length || reviewNeeded.length ? "REVIEW_NEEDED" : "HUMAN_REVIEW_PENDING",
    approval: "UNAPPROVED_CONCEPT", official_branding: false, slug: SLUG,
    source: { video_json_sha256: scriptSha, timeline_sha256: await sha256File(timelineFile),
      keyframes_manifest_sha256: await sha256File(keyframeFile), frames_manifest_sha256: await sha256File(framesFile),
      music_manifest_sha256: await sha256File(musicManifestFile), music_source: music.source,
      music_provenance: music.reused_from ?? null, thumbnail_sha256: await sha256File(thumbnailFile) },
    timing: { ...measured, hook_seconds: measured.hookFrames / FPS,
      after_hook_seconds: measured.afterHookFrames / FPS,
      substantive_body_seconds: measured.substantiveBodyFrames / FPS,
      expected_frames: expectedFrames, expected_seconds: expectedFrames / FPS,
      intro_frames: INTRO_FRAMES, outro_frames: OUTRO_FRAMES },
    media: { shots: shots.length, minimax_share: shots.length / doc.scenes.length, max_consecutive_cards: maxCardRun, review_needed: reviewNeeded, card_files: cardEvidence.files,
      checked_lines: Object.keys(checked.lines).length, audio_review_needed: flags.flags, ledger: totals,
      caveat: "Visible media ledger omits unquoted TTS, transcription, external review and taxes; US$25 all-in final cost requires separate accounting." },
    captions: { cues: shifted.length },
  };
  if (values["inputs-only"]) { process.stdout.write(JSON.stringify(summary, null, 2) + "\n"); return; }

  for (const file of Object.values(output)) assert.ok(existsSync(file), `preview output missing: ${file}`);
  const sidecar = read(output.sidecar);
  assert.equal(sidecar.kind, "unapproved-local-concept-preview");
  assert.equal(sidecar.approved, false);
  assert.equal(sidecar.official_branding, false);
  assert.equal(sidecar.video_json_sha256, scriptSha);
  assert.equal(sidecar.timeline_sha256, summary.source.timeline_sha256);
  assert.equal(sidecar.audio_check_sha256, await sha256File(checkFile));
  assert.equal(sidecar.audio_flags_sha256, await sha256File(flagsFile));
  assert.deepEqual(sidecar.audio_review_needed, flags.flags);
  assert.equal(sidecar.narration_review.file, "narration-review.mp3");
  assert.equal(sidecar.narration_review.sha256, await sha256File(output.narrationReview));
  assert.equal(sidecar.narration_review.source_narration_sha256, await sha256File(inside(workdir, "narration.wav")));
  assert.deepEqual(sidecar.narration_review.spots, flags.flags.map((id) => {
    const line = timeline.lines.find((entry) => entry.id === id);
    return { id, start_seconds: Number((line.start_frame / FPS).toFixed(3)), end_seconds: Number((line.end_frame / FPS).toFixed(3)) };
  }));
  assert.equal(sidecar.keyframes_manifest_sha256, summary.source.keyframes_manifest_sha256);
  assert.equal(sidecar.frames_manifest_sha256, summary.source.frames_manifest_sha256);
  assert.equal(sidecar.music_manifest_sha256, summary.source.music_manifest_sha256);
  assert.deepEqual(sidecar.music_provenance, music.reused_from ?? null);
  assert.deepEqual(sidecar.rendered_card_files, cardEvidence.files);
  assert.deepEqual(sidecar.review_needed.map((item) => item.id), reviewNeeded);
  const hashes = {};
  for (const kind of ["mp4", "srt", "vtt"]) {
    hashes[kind] = await sha256File(output[kind]);
    assert.equal(sidecar.outputs[kind].sha256, hashes[kind], `sidecar ${kind} SHA drift`);
  }
  assert.ok(readFileSync(output.srt).equals(expectedCaptions.srt), "SRT differs from current timeline");
  assert.ok(readFileSync(output.vtt).equals(expectedCaptions.vtt), "VTT differs from current timeline");
  const probe = JSON.parse(run("ffprobe", ["-v", "error", "-count_frames", "-count_packets", "-show_entries",
    "stream=codec_type,codec_name,profile,width,height,r_frame_rate,nb_read_frames,nb_read_packets,sample_rate,channels,duration", "-of", "json", output.mp4]).stdout);
  const video = probe.streams.find((stream) => stream.codec_type === "video");
  const audio = probe.streams.find((stream) => stream.codec_type === "audio");
  assert.equal(video.codec_name, "h264");
  assert.equal(video.width, 1920);
  assert.equal(video.height, 1080);
  assert.equal(video.r_frame_rate, "30/1");
  assert.equal(Number(video.nb_read_frames), expectedFrames, "decoded frame count");
  assert.equal(Number(video.nb_read_packets), expectedFrames, "video packet count");
  assert.equal(audio.codec_name, "aac");
  assert.equal(Number(audio.sample_rate), 48000);
  assert.equal(audio.channels, 2);
  assert.ok(Math.abs(Number(audio.duration) - expectedFrames / FPS) < 0.11, "audio duration drift");
  run("ffmpeg", ["-hide_banner", "-v", "error", "-xerror", "-err_detect", "explode", "-i", output.mp4,
    "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"]);
  const loud = run("ffmpeg", ["-hide_banner", "-nostats", "-i", output.mp4, "-map", "0:a:0",
    "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr;
  const final = loud.slice(loud.lastIndexOf("Summary:"));
  const integrated = Number(/I:\s*(-?[\d.]+)\s*LUFS/.exec(final)?.[1]);
  const peak = Number(/Peak:\s*(-?[\d.]+)\s*dBFS/.exec(final)?.[1]);
  assert.ok(Number.isFinite(integrated) && Math.abs(integrated + 14) <= 1, "integrated loudness outside -14 ±1 LUFS");
  assert.ok(Number.isFinite(peak) && peak <= -0.5, "true peak above -0.5 dBFS");
  summary.output = { bytes: statSync(output.mp4).size, hashes, decoded: "PASS", loudness_lufs: integrated, true_peak_dbfs: peak };
  process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
}

main().catch((error) => { process.stderr.write(`LOCAL PREVIEW QA FAILED: ${error.stack}\n`); process.exitCode = 1; });
