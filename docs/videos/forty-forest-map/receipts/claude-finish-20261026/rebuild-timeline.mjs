// Rebuild forty-forest-map's body timeline from the delivered zh-TW captions (real timing).
// Each line's start comes from its first cue, its audio end from its last cue; buildTimeline then
// lays the frames out. Proved only if every line start lands on its cue and the total and speech
// hash match what was approved.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
const [F] = process.argv.slice(2);
const W = `${F}/wt`;
const { loadProject } = await import(`${W}/tools/video/core/state.mjs`);
const { buildTimeline, speechHash, FPS } = await import(`${W}/tools/video/core/timeline.mjs`);
const project = loadProject({ slug: "forty-forest-map", root: W });
const { doc, lexicon } = project;
const INTRO_AT = 682, INTRO = 150, BODY = 15383, SR = 48000;
const ms = (t) => { const [h, m, s] = t.replace(",", ".").split(":"); return Math.round((Number(h) * 3600 + Number(m) * 60 + Number(s)) * 1000); };
const cues = readFileSync(`${F}/site/final/captions_zh-TW.txt`, "utf8").trim().split(/\n\s*\n/).map((block) => {
  const rows = block.split("\n"); const [a, b] = rows[1].split(" --> ");
  return { start: ms(a), end: ms(b), text: rows.slice(2).join("") };
});
// Presented -> body milliseconds: anything after the intro moves back by its length.
const introStartMs = INTRO_AT * 1000 / FPS, introMs = INTRO * 1000 / FPS;
const body = (t) => (t >= introStartMs + introMs - 1 ? t - introMs : t);
const lines = doc.scenes.flatMap((s) => s.lines ?? []);
const norm = (s) => s.replace(/[\s，。、；：！？「」『』（）,.!?;:"'“”‘’—…-]/g, "");
// Assign cues to lines in order by consuming each line's text.
const spans = []; let c = 0;
for (const line of lines) {
  const want = norm(line.subtitle ?? line.caption ?? line.text);
  let got = "", first = c;
  while (c < cues.length && got.length < want.length) got += norm(cues[c++].text);
  spans.push({ id: line.id, start: body(cues[first].start), end: body(cues[c - 1].end), cues: c - first, match: got === want, want, got });
}
const bad = spans.filter((s) => !s.match);
console.log("cues", cues.length, "consumed", c, "| text mismatches", bad.length);
for (const s of bad.slice(0, 5)) console.log(" ", s.id, "want:", s.want.slice(0, 30), "got:", s.got.slice(0, 30));
const T = await import(`${W}/tools/video/core/timeline.mjs`);
const startFrame = (s) => Math.round(s.start * FPS / 1000);
const sceneOf = new Map(doc.scenes.flatMap((sc) => (sc.lines ?? []).map((l, i) => [l.id, { last: i === sc.lines.length - 1, final: sc === doc.scenes.at(-1) }])));
const samplesById = {};
spans.forEach((s, i) => {
  const next = i + 1 < spans.length ? startFrame(spans[i + 1]) : BODY;
  const frames = next - startFrame(s), where = sceneOf.get(s.id), line = lines[i];
  const pauseMs = (line.pause_after_ms ?? T.DEFAULT_PAUSE_MS) + (where.last ? (where.final ? T.TAIL_MS : T.SCENE_GAP_MS) : 0);
  samplesById[s.id] = frames * T.SAMPLES_PER_FRAME - Math.round(pauseMs * T.SAMPLE_RATE / 1000);
});
const timeline = { ...buildTimeline(doc, samplesById), speech_hash: speechHash(doc, lexicon) };
const misplaced = timeline.lines.filter((l, i) => Math.abs(l.start_frame * 1000 / FPS - spans[i].start) > 1);
console.log("total_frames", timeline.total_frames, "(want", BODY + ")", "| speech_hash", timeline.speech_hash, "| line starts off the cues:", misplaced.length);
for (const l of misplaced.slice(0, 5)) console.log("  ", l.id, l.start_frame, spans.find((s) => s.id === l.id).start);
mkdirSync(`${F}/rebuilt`, { recursive: true });
writeFileSync(`${F}/rebuilt/timeline.json`, `${JSON.stringify(timeline, null, 2)}\n`);
