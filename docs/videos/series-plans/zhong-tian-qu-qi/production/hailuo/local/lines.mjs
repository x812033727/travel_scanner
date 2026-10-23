// Records the given line ids of a drama video.json with each speaker's voice (style + emotion,
// the way tools/video/tts/requests.mjs voiceFor folds them) into <out>/<line id>.wav.
//   node lines.mjs <repo root> <video.json> <out dir> <id,id,...>
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
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
    console.log(`${line.id} ${line.speaker} ${line.text}: ok`);
  }
}
