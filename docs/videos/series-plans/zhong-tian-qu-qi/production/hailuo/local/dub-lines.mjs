// Checks an episode's dub.<locale>.json and records its lines with each speaker's own Gemini voice
// into <out>/<line id>.wav. The style is the glossary's native-speaker lead for the locale, the
// character's persona and the line's emotion (still in Chinese, marked as direction only); the
// zh-TW accent wording never goes in. <id>.json beside each wav records the text and style it was
// made from, so a re-translated line is recorded again and an unchanged one is kept.
//   node dub-lines.mjs <repo root> <video.json> <locale> <out dir> [--check]
// A line's value is its text, or { "text": subtitle, "say": what the voice reads } when they differ.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const [root, file, locale, out, flag] = process.argv.slice(2);
const H = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const glossary = JSON.parse(readFileSync(path.join(H, "dub-glossary.json"), "utf8"));
const video = JSON.parse(readFileSync(file, "utf8"));
const dubFile = path.join(path.dirname(file), `dub.${locale}.json`);
if (!glossary.lead[locale]) throw new Error(`no glossary lead for ${locale}`);
if (!existsSync(dubFile)) throw new Error(`${dubFile} is missing: translate the episode first`);
const dub = JSON.parse(readFileSync(dubFile, "utf8"));
const lines = video.scenes.flatMap((s) => s.lines ?? []);

// The check: every line translated, nothing extra, the right script, a rough length budget.
// CJK = kana and han, HANGUL, THAI: no line may carry another language's script.
const CJK = /[぀-ヿ㐀-鿿]/u, HANGUL = /[가-힯]/u, THAI = /[฀-๿]/u;
const any = (...res) => ({ test: (s) => res.some((re) => re.test(s)) });
const LATIN = { bad: any(CJK, HANGUL, THAI) };
const SCRIPT = { en: LATIN, es: LATIN, pt: LATIN, id: LATIN, vi: LATIN, ja: { bad: any(HANGUL, THAI), need: CJK }, ko: { bad: any(CJK, THAI), need: HANGUL }, th: { bad: any(CJK, HANGUL), need: THAI } };
// Spoken characters per second (spaces and punctuation not counted): en/ja/ko from
// tools/video/dubs/plan.mjs; es/pt/id/vi/th are the medians the e001–e005 dubs measured (raw take
// minus 0.4 s, 2026-10-18). The acted lines here run slower than narration: en measured 11.6.
const RATE = { en: 15, ja: 7.8, ko: 6.7, es: 11, pt: 9.5, id: 11, vi: 13, th: 12 };
const textOf = (v) => (typeof v === "string" ? v : v?.text);
const sayOf = (v) => (typeof v === "string" ? v : v?.say ?? v?.text);
const problems = [], warnings = [];
for (const l of lines) {
  const v = dub[l.id];
  if (!textOf(v)?.trim() || !sayOf(v)?.trim()) { problems.push(`${l.id}: not translated`); continue; }
  const rule = SCRIPT[locale];
  if (rule && (rule.bad.test(sayOf(v)) || rule.bad.test(textOf(v)) || (rule.need && !rule.need.test(sayOf(v))))) problems.push(`${l.id}: wrong script for ${locale}: ${sayOf(v)}`);
  if (!glossary.characters[l.speaker]) problems.push(`${l.id}: speaker ${l.speaker} is not in dub-glossary.json`);
  // The zh line as the cut speaks it (segments-v4/lines, trimmed and sped), when the cut exists.
  const fast = path.join(path.dirname(out), "segments-v4", "lines", `${l.id}.wav`);
  if (existsSync(fast) && RATE[locale]) {
    const zh = (readFileSync(fast).length - 44) / (48000 * 2 * 2);
    const est = 0.4 + [...sayOf(v).replace(/[\s…—,.!?;:'"、。！？「」]/g, "")].length / RATE[locale];
    if (est > zh * 1.3 + 0.35) warnings.push(`${l.id}: about ${est.toFixed(1)} s against ${zh.toFixed(1)} s of Chinese: ${sayOf(v)}`);
  }
}
for (const id of Object.keys(dub)) if (!lines.some((l) => l.id === id)) problems.push(`${id}: no such line in video.json`);
for (const w of warnings) console.log(`long? ${w}`);
if (problems.length) { console.error(problems.join("\n")); process.exit(2); }
console.log(`${path.basename(dubFile)}: ${lines.length} lines checked, ${warnings.length} possibly long`);
if (flag === "--check") process.exit(0);

const mod = (p) => import(pathToFileURL(path.join(root, "tools/video", p)).href);
const { voiceFields, spokenParts } = await mod("tts/requests.mjs");
const { emptyLexicon } = await mod("core/lexicon.mjs");
const { synthesize } = await mod("tts/client.mjs");
const { readCredentials } = await mod("tts/credentials.mjs");
const voices = Object.fromEntries(video.characters.map((c) => [c.id, c.voice]));
const { site, token } = readCredentials();
mkdirSync(out, { recursive: true });
const styleOf = (l) => [glossary.lead[locale], glossary.characters[l.speaker].persona, l.emotion ? `${glossary.direction[locale]} ${l.emotion}` : null].filter(Boolean).join(" ").slice(0, 400);
const jobs = lines.filter((l) => {
  const side = path.join(out, `${l.id}.json`);
  const want = { text: sayOf(dub[l.id]), style: styleOf(l), voice: voices[l.speaker].name };
  if (existsSync(path.join(out, `${l.id}.wav`)) && existsSync(side) && JSON.stringify(JSON.parse(readFileSync(side, "utf8"))) === JSON.stringify(want)) return false;
  l.want = want;
  return true;
});
let billable = 0, seconds = 0, done = 0;
const t0 = Date.now();
const one = async (l) => {
  const body = { ...voiceFields({ provider: "gemini", name: l.want.voice, style: l.want.style }), segments: [{ parts: spokenParts(l.want.text, emptyLexicon()), break_after_ms: 0 }] };
  const result = await synthesize({ site, token, fetchImpl: globalThis.fetch, body });
  writeFileSync(path.join(out, `${l.id}.wav`), result.wav);
  writeFileSync(path.join(out, `${l.id}.json`), `${JSON.stringify(l.want)}\n`);
  billable += result.billable;
  seconds += (result.wav.length - 44) / (48000 * 2);
  console.log(`${l.id} ${l.speaker} ${l.want.text}: ok (${++done}/${jobs.length})`);
};
const queue = [...jobs];
await Promise.all(Array.from({ length: Math.min(4, queue.length) }, async () => { while (queue.length) await one(queue.shift()); }));
// gemini-3.8-flash-tts: 25 audio tokens a second at US$9 per million (docs/videos/DUBS.md §成本).
console.log(`recorded ${jobs.length} of ${lines.length} (${lines.length - jobs.length} kept); ${billable} billable characters, ${seconds.toFixed(1)} s of audio ≈ US$${(seconds * 25 * 9e-6).toFixed(4)}; ${((Date.now() - t0) / 1000).toFixed(0)} s`);
