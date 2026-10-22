// C04's paid-media gate: measure delivered chapter 02–06 WAVs, excluding hook and branding.
// Usage: node docs/videos/story-everyday-bubble-wrap-c04-pilot/measure-body.mjs <exact C04 workdir>
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadProject } from "../../../tools/video/core/state.mjs";
import { FPS, SAMPLE_RATE, speechHash } from "../../../tools/video/core/timeline.mjs";
import { parseWav, requireNarrationFormat } from "../../../tools/video/tts/wav.mjs";

const slug = "story-everyday-bubble-wrap-c04";
const root = fileURLToPath(new URL("../../../", import.meta.url));
const workdir = process.argv[2];
if (!workdir || !path.isAbsolute(workdir) || path.basename(path.normalize(workdir)) !== slug) {
  throw new Error(`Pass the absolute ${slug} media workdir`);
}

const { doc, lexicon } = loadProject({ slug, root });
const timeline = JSON.parse(readFileSync(path.join(workdir, "timeline.json"), "utf8"));
const cache = JSON.parse(readFileSync(path.join(workdir, "audio", "cache.json"), "utf8"));
if (timeline.speech_hash !== speechHash(doc, lexicon)) throw new Error("Timeline is stale for the current C04 script/lexicon");
if (timeline.fps !== FPS || timeline.sample_rate !== SAMPLE_RATE) throw new Error("Unexpected timeline frame/audio rate");
const chapters = timeline.chapters;
if (chapters.length !== 6 || chapters[0].scene !== "c04-h01" || chapters[1].scene !== "c04-o01" || chapters.at(-1).scene !== "c04-n01") {
  throw new Error("C04 chapter boundaries differ from the approved six-chapter script");
}

const approvedBodyScenes = doc.scenes.slice(doc.scenes.findIndex((scene) => scene.id === "c04-o01"));
const bodyIds = approvedBodyScenes.flatMap((scene) => (scene.lines ?? []).map((line) => line.id));
const timelineLines = new Map(timeline.lines.map((line) => [line.id, line]));
if (timeline.lines.length !== doc.scenes.reduce((sum, scene) => sum + (scene.lines?.length ?? 0), 0) || new Set(bodyIds).size !== bodyIds.length) {
  throw new Error("Line count or IDs differ from the approved script");
}

let samples = 0;
for (const id of bodyIds) {
  const line = timelineLines.get(id);
  if (!line || !cache.lines?.[id] || !cache.sha256?.[id]) throw new Error(`Missing current take/cache for ${id}`);
  const wav = readFileSync(path.join(workdir, "audio", `${id}.wav`));
  const hash = createHash("sha256").update(wav).digest("hex");
  if (hash !== cache.sha256[id]) throw new Error(`Take hash mismatch for ${id}`);
  const decoded = requireNarrationFormat(parseWav(wav));
  if (decoded.length !== line.audio_samples) throw new Error(`Timeline/WAV sample mismatch for ${id}`);
  samples += decoded.length;
}

const pureSeconds = samples / SAMPLE_RATE;
const timelineSeconds = (timeline.total_frames - chapters[1].start_frame) / FPS;
const pass = pureSeconds >= 480;
process.stdout.write(JSON.stringify({ slug, body_lines: bodyIds.length, pure_wav_seconds: Number(pureSeconds.toFixed(3)), body_timeline_seconds: Number(timelineSeconds.toFixed(3)), minimum_pure_seconds: 480, pass }, null, 2) + "\n");
if (!pass) process.exitCode = 1;
