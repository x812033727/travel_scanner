// Read-only, repeatable technical QA of the local concept preview.
// Run --inputs-only while media is in progress; omit it only after the final
// MP4, captions and sidecar have been atomically published.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
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

const SLUG = "story-everyday-dominos-pizza-x02";
const INTRO = 150;
const OUTRO = 630;
const FPS = 30;
const CAP_USD = 25;
const names = {
  mp4: "preview-review-needed.mp4",
  srt: "preview-review-needed.zh-TW.srt",
  vtt: "preview-review-needed.zh-TW.vtt",
  sidecar: "preview-review-needed.json",
};
const read = (file) => JSON.parse(readFileSync(file, "utf8"));
const digest = (data) => createHash("sha256").update(data).digest("hex");
const within = (workdir, name) => {
  const file = path.resolve(workdir, name);
  assert.ok(isInside(file, workdir), "media path escapes workdir: " + name);
  return file;
};

function run(tool, args) {
  const done = spawnSync(tool, args, { encoding: "utf8", maxBuffer: 16 * 1024 * 1024, timeout: 20 * 60_000 });
  if (done.error || done.status !== 0) throw new Error(tool + " failed: " + (done.error?.message ?? done.stderr?.trim() ?? "status " + done.status));
  return done;
}

async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: { workdir: { type: "string" }, "inputs-only": { type: "boolean" } },
    strict: true,
  });
  assert.ok(values.workdir, "pass --workdir <media base outside the repository>");
  const workdir = resolveWorkdir({ flag: values.workdir, slug: SLUG, root: ROOT });
  const docFile = path.join(ROOT, "docs", "videos", SLUG, "video.json");
  const project = loadProject({ slug: SLUG, root: ROOT });
  assert.deepEqual(lintProject(project).errors, [], "the current project must lint cleanly");
  const { doc, lexicon } = project;
  const timelineFile = within(workdir, "timeline.json");
  const timeline = read(timelineFile);
  assert.equal(timeline.speech_hash, speechHash(doc, lexicon), "speech hash drift");
  assert.deepEqual(audioEvidenceProblems(timeline, workdir), [], "TTS evidence drift");
  const introAt = timeline.chapters[1].start_frame;
  assert.ok(Number.isSafeInteger(introAt) && introAt > 0 && introAt < timeline.total_frames);
  assert.ok(timeline.scenes.some((scene) => scene.start_frame === introAt), "intro is not on a scene boundary");
  const expectedFrames = timeline.total_frames + INTRO + OUTRO;

  const keyframeFile = within(workdir, "keyframes/manifest.json");
  const keyframes = read(keyframeFile);
  assert.equal(keyframes.look_hash, lookHash(doc), "look hash drift");
  assert.equal(keyframes.visual_hash, visualHash(doc), "keyframe visual hash drift");
  const shotScenes = doc.scenes.filter((scene) => scene.template === "shot" && !scene.data?.source);
  assert.equal(Object.keys(keyframes.shots).length, shotScenes.length, "keyframe shot count");
  const flagged = [];
  for (const scene of shotScenes) {
    const shot = keyframes.shots[scene.id];
    assert.ok(shot && !shot.incomplete && shot.file && /^[a-f0-9]{64}$/.test(shot.sha256 ?? ""), "incomplete selected picture: " + scene.id);
    assert.equal(await sha256File(within(workdir, shot.file)), shot.sha256, "picture hash drift: " + scene.id);
    if (shot.needs_review || (shot.judge?.passed === false && !Array.isArray(shot.accepted_with_problems))) flagged.push(scene.id);
  }
  assert.ok(flagged.length, "this checker expects an explicitly unapproved review-needed concept");

  const framesFile = within(workdir, "frames/manifest.json");
  const frames = read(framesFile);
  assert.equal(frames.visual_hash, visualHash(doc), "card visual hash drift");
  assert.equal(frames.theme_hash, themeHash(), "card render theme drift");
  assert.equal(frames.scenes?.length, doc.scenes.length, "rendered scene count");
  const cardNames = [];
  for (const scene of frames.scenes ?? []) for (const state of scene.states ?? []) {
    for (const name of [state.still, ...(state.transition ?? [])]) {
      assert.ok(typeof name === "string" && name && existsSync(within(workdir, name)), "missing rendered card: " + name);
      cardNames.push(name);
    }
  }
  const cardFiles = [];
  for (const name of [...new Set(cardNames)].sort()) cardFiles.push({ file: name, sha256: await sha256File(within(workdir, name)) });
  const thumbnailFile = within(workdir, "thumbnail.jpg");
  assert.ok(existsSync(thumbnailFile), "rendered thumbnail is missing");
  const musicFile = within(workdir, "music/manifest.json");
  const music = read(musicFile);
  assert.equal(music.mix_hash, mixHash(doc), "music mix hash drift");
  assert.equal(await sha256File(within(workdir, music.file)), music.sha256, "music hash drift");
  const ledger = readLedger(workdir);
  const totals = totalsOf(ledger.entries);
  assert.deepEqual(totals, ledger.totals, "ledger total does not equal its rows");
  assert.equal(totals.reservations, 0, "media ledger has unresolved reservations");
  assert.ok(totals.usd <= CAP_USD, "visible media ledger is over the per-video cap");
  const jobs = ledger.entries.map((entry) => entry.job_id).filter(Boolean);
  assert.equal(new Set(jobs).size, jobs.length, "duplicate media job ID");

  const texts = Object.fromEntries(doc.scenes.flatMap((scene) => (scene.lines ?? []).map((line) => [line.id, line.text])));
  const built = buildCues(timeline, texts, "zh-TW");
  assert.deepEqual(built.missing, [], "caption lines missing");
  const lineStarts = new Map(timeline.lines.map((line) => [line.id, line.start_frame]));
  const cues = built.cues.map((cue) => {
    const start = lineStarts.get(cue.line);
    assert.ok(Number.isSafeInteger(start), "caption has no measured line: " + cue.line);
    const by = start >= introAt ? 1000 * INTRO / FPS : 0;
    return { ...cue, start_ms: Math.round(cue.start_ms + by), end_ms: Math.round(cue.end_ms + by) };
  });
  const cueProblems = checkCues(cues, "zh-TW");
  assert.deepEqual(cueProblems, [], "caption timing or reading speed");
  const introMs = Math.round(introAt * 1000 / FPS);
  const introEndMs = introMs + 1000 * INTRO / FPS;
  assert.equal(cues.filter((cue) => cue.start_ms < introEndMs && cue.end_ms > introMs).length, 0, "caption overlays concept intro");
  assert.ok(cues.at(-1).end_ms <= Math.round((timeline.total_frames + INTRO) * 1000 / FPS), "caption overlays concept outro");
  const expectedCaptions = { srt: Buffer.from(toSrt(cues)), vtt: Buffer.from(toVtt(cues)) };
  const byScene = new Map(timeline.scenes.map((scene) => [scene.id, scene]));
  const reviewSpots = flagged.map((id) => {
    const scene = byScene.get(id);
    assert.ok(scene, "flagged scene missing from timeline: " + id);
    const frame = scene.start_frame + (scene.start_frame >= introAt ? INTRO : 0);
    return { id, frame, seconds: Number((frame / FPS).toFixed(3)) };
  });
  const summary = {
    technical: values["inputs-only"] ? "INPUTS_READY" : "PASS",
    workdir,
    source: { video_json_sha256: await sha256File(docFile), timeline_sha256: await sha256File(timelineFile), keyframes_manifest_sha256: await sha256File(keyframeFile), frames_manifest_sha256: await sha256File(framesFile), music_manifest_sha256: await sha256File(musicFile), rendered_card_files: cardFiles, thumbnail_sha256: await sha256File(thumbnailFile) },
    expected: { body_frames: timeline.total_frames, output_frames: expectedFrames, seconds: Number((expectedFrames / FPS).toFixed(3)), intro: [introAt, introAt + INTRO], outro: [timeline.total_frames + INTRO, expectedFrames], chapters: timeline.chapters.map((chapter, index) => chapter.start_frame + (index ? INTRO : 0)), cues: cues.length, caption_sha256: Object.fromEntries(Object.entries(expectedCaptions).map(([name, bytes]) => [name, digest(bytes)])) },
    media: { selected_pictures: shotScenes.length, review_needed: flagged, review_spots: reviewSpots, ledger: totals, caveat: "Ledger covers visible media jobs, not unlisted TTS, transcription, tax or provider charges." },
  };
  if (values["inputs-only"]) {
    process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
    return;
  }

  const previewDir = within(workdir, "review/local-preview");
  const files = Object.fromEntries(Object.entries(names).map(([name, file]) => [name, path.join(previewDir, file)]));
  for (const file of Object.values(files)) assert.ok(existsSync(file), "preview output missing: " + file);
  const sidecar = read(files.sidecar);
  assert.equal(sidecar.kind, "unapproved-local-concept-preview");
  assert.equal(sidecar.approved, false);
  assert.equal(sidecar.slug, SLUG);
  assert.equal(sidecar.video_json_sha256, summary.source.video_json_sha256);
  assert.equal(sidecar.timeline_sha256, summary.source.timeline_sha256);
  assert.equal(sidecar.keyframes_manifest_sha256, summary.source.keyframes_manifest_sha256);
  assert.equal(sidecar.frames_manifest_sha256, summary.source.frames_manifest_sha256);
  assert.equal(sidecar.music_manifest_sha256, summary.source.music_manifest_sha256);
  assert.deepEqual(sidecar.rendered_card_files, cardFiles, "rendered card file hashes");
  assert.equal(sidecar.look_hash, lookHash(doc));
  assert.equal(sidecar.visual_hash, visualHash(doc));
  assert.deepEqual(sidecar.review_needed.map((shot) => shot.id), flagged, "sidecar review-needed IDs");
  for (const record of sidecar.review_needed) {
    const shot = keyframes.shots[record.id];
    assert.equal(record.file, shot.file, "sidecar selected file drift: " + record.id);
    assert.equal(record.sha256, shot.sha256, "sidecar selected SHA drift: " + record.id);
    const problems = [...new Set([...(Array.isArray(shot.problems) ? shot.problems : []), ...(Array.isArray(shot.judge?.problems) ? shot.judge.problems : [])])];
    assert.deepEqual(record.problems, problems, "sidecar problems drift: " + record.id);
  }
  const hashes = {};
  for (const name of ["mp4", "srt", "vtt"]) {
    assert.equal(sidecar.outputs[name].file, names[name], "sidecar output filename");
    hashes[name] = await sha256File(files[name]);
    assert.equal(sidecar.outputs[name].sha256, hashes[name], "sidecar output hash drift: " + name);
  }
  for (const name of ["srt", "vtt"]) {
    assert.ok(readFileSync(files[name]).equals(expectedCaptions[name]), "caption bytes differ from current script: " + name);
  }

  const probe = readProbe(files.mp4);
  const streams = probe.streams ?? [];
  const videos = streams.filter((stream) => stream.codec_type === "video");
  const audios = streams.filter((stream) => stream.codec_type === "audio");
  assert.equal(videos.length, 1, "expected one video stream");
  assert.equal(audios.length, 1, "expected one audio stream");
  const video = videos[0];
  const audio = audios[0];
  assert.equal(video.codec_name, "h264");
  assert.match(video.profile, /High/i);
  assert.equal(video.width, 1920);
  assert.equal(video.height, 1080);
  assert.equal(video.r_frame_rate, "30/1");
  assert.equal(video.pix_fmt, "yuv420p");
  assert.equal(video.color_range, "tv");
  for (const field of ["color_space", "color_primaries", "color_transfer"]) assert.equal(video[field], "bt709", field);
  assert.equal(Number(video.nb_read_packets), expectedFrames, "video packet count");
  assert.equal(Number(video.nb_read_frames), expectedFrames, "decoded frame count");
  assert.equal(audio.codec_name, "aac");
  assert.equal(Number(audio.sample_rate), 48000);
  assert.equal(audio.channels, 2);
  assert.ok(Math.abs(Number(audio.duration) - expectedFrames / FPS) < 0.11, "audio/video duration drift");

  // The full independent decode catches damaged frames or AAC packets. FFprobe's decoded
  // frame timestamps then catches holes/duplication that a packet count could miss.
  run("ffmpeg", ["-hide_banner", "-v", "error", "-xerror", "-err_detect", "explode", "-i", files.mp4, "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"]);
  const ptsOutput = run("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries", "frame=best_effort_timestamp", "-of", "csv=p=0", files.mp4]).stdout;
  const pts = ptsOutput.trim().split(/\r?\n/).map((line) => {
    const value = /^-?\d+/.exec(line)?.[0];
    assert.ok(value !== undefined, "missing decoded frame PTS");
    return Number(value);
  });
  assert.equal(pts.length, expectedFrames, "PTS frame count");
  assert.equal(pts[0], 0, "first decoded video PTS");
  const [timeNum, timeDen] = video.time_base.split("/").map(Number);
  const step = timeDen / (FPS * timeNum);
  assert.ok(Number.isSafeInteger(step), "video time base does not fit 30 fps");
  for (let index = 1; index < pts.length; index++) assert.equal(pts[index] - pts[index - 1], step, "video PTS gap at frame " + index);
  const loudnessLog = run("ffmpeg", ["-hide_banner", "-nostats", "-i", files.mp4, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr;
  const finalSummary = loudnessLog.slice(loudnessLog.lastIndexOf("Summary:"));
  const integrated = Number(/I:\s*(-?[\d.]+)\s*LUFS/.exec(finalSummary)?.[1]);
  const truePeak = Number(/Peak:\s*(-?[\d.]+)\s*dBFS/.exec(finalSummary)?.[1]);
  assert.ok(Number.isFinite(integrated) && Number.isFinite(truePeak), "missing EBU R128 summary");
  assert.ok(Math.abs(integrated + 14) <= 1, "full-preview integrated loudness is outside -14 ±1 LUFS");
  assert.ok(truePeak <= -0.5, "full-preview true peak is above -0.5 dBFS");
  summary.output = { bytes: statSync(files.mp4).size, hashes, probe: { video: { codec: video.codec_name, profile: video.profile, width: video.width, height: video.height, fps: video.r_frame_rate, pixel: video.pix_fmt, color_range: video.color_range, color_space: video.color_space, color_primaries: video.color_primaries, color_transfer: video.color_transfer, packet_frames: Number(video.nb_read_packets), decoded_frames: Number(video.nb_read_frames), pts_step: step }, audio: { codec: audio.codec_name, sample_rate: Number(audio.sample_rate), channels: audio.channels, duration: Number(audio.duration), integrated_lufs: integrated, true_peak_dbfs: truePeak } }, full_decode: "PASS", exact_caption_bytes: "PASS", sidecar_hashes: "PASS" };
  process.stdout.write(JSON.stringify(summary, null, 2) + "\n");
}

function readProbe(file) {
  return JSON.parse(run("ffprobe", ["-v", "error", "-count_frames", "-count_packets", "-show_entries", "stream=codec_type,codec_name,profile,width,height,r_frame_rate,time_base,pix_fmt,color_range,color_space,color_primaries,color_transfer,nb_read_frames,nb_read_packets,sample_rate,channels,duration", "-of", "json", file]).stdout);
}

main().catch((error) => {
  process.stderr.write("LOCAL PREVIEW QA FAILED: " + error.stack + "\n");
  process.exitCode = 1;
});
