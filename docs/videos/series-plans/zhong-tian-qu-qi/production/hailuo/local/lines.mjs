// Records the given line ids of a drama video.json with each speaker's voice (style + emotion,
// the way tools/video/tts/requests.mjs voiceFor folds them) into <out>/<line id>.wav.
// A speaker listed in voice-post.json (next to this file) is post-processed right after recording:
// sped up (atempo) and filtered (the system voice, owner 2026-11-05); the raw take stays as <id>.raw-tts.wav.
//   node lines.mjs <repo root> <video.json> <out dir> <id,id,...>
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { pathToFileURL } from "node:url";

const [root, file, out, ids] = process.argv.slice(2);
const mod = (p) => import(pathToFileURL(path.join(root, "tools/video", p)).href);
const { voiceFields, spokenParts } = await mod("tts/requests.mjs");
const { emptyLexicon } = await mod("core/lexicon.mjs");
const { synthesize } = await mod("tts/client.mjs");
const { readCredentials } = await mod("tts/credentials.mjs");
const { voiceFor } = await mod("core/drama.mjs");
const video = JSON.parse(readFileSync(file, "utf8"));
const voices = Object.fromEntries(video.characters.map((c) => [c.id, c.voice]));
const want = new Set(ids.split(","));
const postFile = path.join(path.dirname(new URL(import.meta.url).pathname), "voice-post.json");
const POST = existsSync(postFile) ? JSON.parse(readFileSync(postFile, "utf8")) : {};
const { site, token } = readCredentials();
mkdirSync(out, { recursive: true });
for (const scene of video.scenes) {
  for (const line of scene.lines ?? []) {
    if (!want.has(line.id)) continue;
    const target = path.join(out, `${line.id}.wav`);
    if (existsSync(target)) { console.log(`${line.id}: kept`); continue; }
    const voice = voiceFor(video, line);
    const style = voice.style;
    const body = { ...voiceFields({ provider: "gemini", name: voice.name, style }), segments: [{ parts: spokenParts(line.text, emptyLexicon()), break_after_ms: 0 }] };
    const result = await synthesize({ site, token, fetchImpl: globalThis.fetch, body });
    writeFileSync(target, result.wav);
    const post = POST[line.speaker];
    if (post) {
      const raw = path.join(out, `${line.id}.raw-tts.wav`);
      renameSync(target, raw);
      const af = [post.atempo ? `atempo=${post.atempo}` : null, post.filter].filter(Boolean).join(",");
      execFileSync("ffmpeg", ["-v", "error", "-y", "-i", raw, "-af", af, "-ar", "24000", "-ac", "1", target]);
    }
    console.log(`${line.id} ${line.speaker} ${line.text}: ok`);
  }
}
