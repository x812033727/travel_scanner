// Stand-ins for what the paid stages make, so the smoke test and a local dry run of the assembly
// need neither the narration server, a video tool token nor any media vendor.
//
// The narration is a soft tone per line, as long as the line would take to say, laid on the
// frame grid exactly as the tts stage lays real speech. A drama also gets a keyframe per shot
// (ffmpeg's test pattern, a different hue per shot), a clip per shot that opens on that very
// frame (one clip runs short of its lines and one long, so the fit is exercised both ways) and
// a twenty-second two-tone music track.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

import { clipsHash, isShot, lookHash, mixHash } from "../core/drama.mjs";
import { buildTimeline, estimatedSamples, FPS, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from "../core/timeline.mjs";

export const MUSIC_SECONDS = 20;
// The second shot's clip is this much shorter than its lines, the third this much longer.
export const SHORT_BY_SECONDS = 2;
export const LONG_BY_SECONDS = 3;

function wav(samples) {
  const header = Buffer.alloc(44);
  header.write("RIFF", 0, "ascii");
  header.writeUInt32LE(36 + samples.length * 2, 4);
  header.write("WAVEfmt ", 8, "ascii");
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(1, 22);
  header.writeUInt32LE(SAMPLE_RATE, 24);
  header.writeUInt32LE(SAMPLE_RATE * 2, 28);
  header.writeUInt16LE(2, 32);
  header.writeUInt16LE(16, 34);
  header.write("data", 36, "ascii");
  header.writeUInt32LE(samples.length * 2, 40);
  return Buffer.concat([header, Buffer.from(samples.buffer, samples.byteOffset, samples.byteLength)]);
}

/** Write timeline.json and narration.wav for `doc` into `workdir`, as the tts stage would. */
export function writeSyntheticNarration(doc, lexicon, workdir) {
  const samplesById = estimatedSamples(doc);
  const timeline = { ...buildTimeline(doc, samplesById), speech_hash: speechHash(doc, lexicon) };
  const narration = new Int16Array(timeline.total_frames * SAMPLES_PER_FRAME);
  timeline.lines.forEach((placed, index) => {
    const start = placed.start_frame * SAMPLES_PER_FRAME;
    const pitch = 180 + (index % 5) * 40;
    for (let sample = 0; sample < placed.audio_samples; sample++) {
      const envelope = Math.min(1, sample / 2400, (placed.audio_samples - sample) / 2400);
      narration[start + sample] = Math.round(6000 * envelope * Math.sin((2 * Math.PI * pitch * sample) / SAMPLE_RATE));
    }
  });
  writeFileSync(path.join(workdir, "narration.wav"), wav(narration));
  writeFileSync(path.join(workdir, "timeline.json"), `${JSON.stringify(timeline, null, 2)}\n`);
  return timeline;
}

const hue = (index) => (index * 47) % 360;
const fileSha256 = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");
const ffmpeg = (binary, args) => execFileSync(binary, ["-hide_banner", "-y", "-loglevel", "error", ...args], { stdio: ["ignore", "ignore", "inherit"], windowsHide: true });
const writeManifest = (workdir, dir, manifest) => writeFileSync(path.join(workdir, dir, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);

/** The seconds the clips stage would ask for: whole seconds covering the lines, 4 to 10. */
export const clipSeconds = (frames) => Math.min(10, Math.max(4, Math.ceil(frames / FPS)));

/** One 1920x1080 keyframe per shot, and keyframes/manifest.json as the keyframes stage writes it. */
export function writeSyntheticKeyframes(doc, workdir, binary) {
  mkdirSync(path.join(workdir, "keyframes"), { recursive: true });
  const shots = {};
  doc.scenes.filter(isShot).forEach((scene, index) => {
    const file = `keyframes/${scene.id}-synthetic.png`;
    ffmpeg(binary, ["-f", "lavfi", "-i", `testsrc2=size=1920x1080:rate=${FPS},hue=h=${hue(index)}`, "-frames:v", "1", path.join(workdir, file)]);
    shots[scene.id] = { file, sha256: fileSha256(path.join(workdir, file)) };
  });
  const manifest = { look_hash: lookHash(doc), visual_hash: visualHash(doc), shots };
  writeManifest(workdir, "keyframes", manifest);
  return manifest;
}

/**
 * One clip per shot that opens on the shot's keyframe, and clips/manifest.json as the clips
 * stage writes it. The second shot's clip is SHORT_BY_SECONDS shorter than its lines and the
 * third LONG_BY_SECONDS longer.
 */
export function writeSyntheticClips(doc, timeline, lexicon, workdir, binary) {
  mkdirSync(path.join(workdir, "clips"), { recursive: true });
  const shots = {};
  const order = [];
  let index = 0;
  for (const scene of timeline.scenes) {
    const source = doc.scenes.find((each) => each.id === scene.id);
    if (!isShot(source)) continue;
    let seconds = clipSeconds(scene.end_frame - scene.start_frame);
    if (index === 1) seconds = Math.max(1, seconds - SHORT_BY_SECONDS);
    if (index === 2) seconds += LONG_BY_SECONDS;
    const file = `clips/${scene.id}-synthetic.mp4`;
    ffmpeg(binary, [
      "-f", "lavfi", "-i", `testsrc2=size=1920x1080:rate=${FPS}:duration=${seconds},hue=h=${hue(index)}`,
      "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", String(FPS), path.join(workdir, file),
    ]);
    shots[scene.id] = { file, sha256: fileSha256(path.join(workdir, file)), seconds };
    order.push({ id: scene.id, sha256: shots[scene.id].sha256 });
    index += 1;
  }
  const manifest = { speech_hash: speechHash(doc, lexicon), visual_hash: visualHash(doc), look_hash: lookHash(doc), clips_hash: clipsHash(order), shots };
  writeManifest(workdir, "clips", manifest);
  return manifest;
}

/** A twenty-second two-tone track and music/manifest.json as the music stage writes it. */
export function writeSyntheticMusic(doc, workdir, binary) {
  mkdirSync(path.join(workdir, "music"), { recursive: true });
  const file = "music/synthetic.wav";
  ffmpeg(binary, [
    "-f", "lavfi", "-i", `sine=frequency=220:sample_rate=${SAMPLE_RATE}:duration=${MUSIC_SECONDS}`,
    "-f", "lavfi", "-i", `sine=frequency=330:sample_rate=${SAMPLE_RATE}:duration=${MUSIC_SECONDS}`,
    "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0,volume=-6dB[a]",
    "-map", "[a]", "-c:a", "pcm_s16le", path.join(workdir, file),
  ]);
  const manifest = { mix_hash: mixHash(doc), file, sha256: fileSha256(path.join(workdir, file)), seconds: MUSIC_SECONDS };
  writeManifest(workdir, "music", manifest);
  return manifest;
}
