// The dialogue of a dub (assemble-v4.mjs with DUB=<locale>): every dubbed line starts where its
// Chinese line starts in the zh-TW cut and must end before the next line starts, so the picture,
// its timing and every later line stay where they are. A line longer than its slot is sped up
// (atempo up to MAX_TEMPO); one that still does not fit stops the build with the lines to
// shorten, unless dub-force.json lists it for the locale or FORCE=1 is set, which cuts it at the
// slot's end with a short fade.
//   slot end = min(next line's start - 0.06 s, its own shot's end + SPILL, the cut's end)
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const MAX_TEMPO = Number(process.env.DUB_MAX_TEMPO ?? 1.3);
const BEFORE_NEXT = 0.06, SPILL = 0.5, END = 0.05;
const TRIM = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse";

/**
 * Builds <segDir>/dub-<locale>/dialogue.wav (`total` seconds) and returns
 * { dialogue, srt: [{ start, end, text }], fit: [...] }. `lineAt` is assemble-v4's list of placed
 * zh lines ({ id, shot, speaker, start, len }), `starts` its shots ({ start, dur }).
 */
export function dubDialogue({ locale, videoFile, work, segDir, lineAt, starts, total, probe, zhSrt }) {
  const dub = JSON.parse(readFileSync(path.join(path.dirname(videoFile), `dub.${locale}.json`), "utf8"));
  const dir = path.join(segDir, `dub-${locale}`);
  mkdirSync(dir, { recursive: true });
  // The zh timing must be the timing of the cut that is on the site: compare with its subtitles.
  if (zhSrt && existsSync(zhSrt)) {
    const cues = readFileSync(zhSrt, "utf8").split(/\r?\n\r?\n/).map((b) => /(\d+):(\d+):(\d+),(\d+) -->/.exec(b)).filter(Boolean).map((m) => +m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000);
    const spoken = lineAt.filter((l) => l.subtitled).map((l) => l.start);
    const off = spoken.length !== cues.length ? Infinity : Math.max(0, ...spoken.map((s, i) => Math.abs(s - cues[i])));
    if (off > 0.02) throw new Error(`the zh timing differs from ${path.basename(zhSrt)} (${spoken.length} lines vs ${cues.length} cues, off ${off}); re-cut the zh episode first`);
  }
  const fit = [], over = [], srt = [], placed = [];
  lineAt.forEach((l, k) => {
    const v = dub[l.id];
    const text = typeof v === "string" ? v : v?.text;
    if (!text) throw new Error(`${l.id}: no ${locale} translation`);
    const src = path.join(work, `audio-${locale}`, `${l.id}.wav`);
    if (!existsSync(src)) throw new Error(`${l.id}: no ${locale} recording (${src})`);
    const shotEnd = starts[l.shot].start + starts[l.shot].dur;
    const next = lineAt[k + 1]?.start ?? total;
    const slot = Math.min(next - BEFORE_NEXT, shotEnd + SPILL, total - END) - l.start;
    const trimmed = path.join(dir, `${l.id}.raw.wav`);
    execFileSync("ffmpeg", ["-v", "error", "-y", "-i", src, "-af", TRIM, "-ar", "48000", "-ac", "2", trimmed]);
    const raw = probe(trimmed);
    // atempo comes out ~1% long: aim a little inside the slot.
    let tempo = raw > slot ? raw / (slot * 0.99) : 1;
    let status = tempo > 1 ? "atempo" : "fits";
    if (tempo > MAX_TEMPO) { over.push({ id: l.id, speaker: l.speaker, text, zh: l.len, slot, raw, tempo, chars: [...text].length }); tempo = MAX_TEMPO; status = "cut"; }
    const fast = path.join(dir, `${l.id}.wav`);
    const af = [tempo > 1 ? `atempo=${tempo.toFixed(4)}` : null, status === "cut" ? `atrim=duration=${slot.toFixed(3)},afade=t=out:st=${Math.max(0, slot - 0.08).toFixed(3)}:d=0.08` : null].filter(Boolean);
    execFileSync("ffmpeg", ["-v", "error", "-y", "-i", trimmed, ...(af.length ? ["-af", af.join(",")] : ["-c", "copy"]), fast]);
    const len = probe(fast);
    placed.push({ wav: fast, at: l.start });
    srt.push({ start: l.start, end: l.start + len, text });
    fit.push({ id: l.id, speaker: l.speaker, start: +l.start.toFixed(3), zh: +l.len.toFixed(3), slot: +slot.toFixed(3), raw: +raw.toFixed(3), tempo: +tempo.toFixed(3), len: +len.toFixed(3), status, text });
  });
  // dub-force.json: { "<locale>": ["<line id>", ...] } — lines whose take only loses a trailing
  // laugh or breath when cut, so a rebuild (or a compilation) needs no FORCE=1.
  const forceFile = path.join(path.dirname(fileURLToPath(import.meta.url)), "dub-force.json");
  const forced = existsSync(forceFile) ? JSON.parse(readFileSync(forceFile, "utf8"))[locale] ?? [] : [];
  const stop = over.filter((o) => !forced.includes(o.id));
  if (stop.length && process.env.FORCE !== "1") {
    const say = stop.map((o) => `${o.id} ${o.speaker}: ${o.raw.toFixed(2)} s in a ${o.slot.toFixed(2)} s slot (zh ${o.zh.toFixed(2)} s) needs ${o.tempo.toFixed(2)}x; shorten to about ${Math.floor(o.chars * MAX_TEMPO * o.slot / o.raw)} characters: ${o.text}`);
    throw new Error(`${stop.length} ${locale} line(s) do not fit even at ${MAX_TEMPO}x:\n${say.join("\n")}`);
  }
  // One pass: every line delayed to its start on a silent bed exactly as long as the cut.
  const dialogue = path.join(dir, "dialogue.wav");
  const args = ["-v", "error", "-y"];
  const graph = [];
  placed.forEach((p, i) => {
    args.push("-i", p.wav);
    const ms = Math.round(p.at * 1000);
    graph.push(`[${i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=${ms}|${ms}[a${i}]`);
  });
  args.push("-f", "lavfi", "-t", total.toFixed(3), "-i", "anullsrc=r=48000:cl=stereo");
  graph.push(`${placed.map((_, i) => `[a${i}]`).join("")}[${placed.length}:a]amix=inputs=${placed.length + 1}:normalize=0:duration=longest,atrim=duration=${total.toFixed(3)}[a]`);
  args.push("-filter_complex", graph.join(";"), "-map", "[a]", "-c:a", "pcm_s16le", dialogue);
  execFileSync("ffmpeg", args, { stdio: "inherit" });
  writeFileSync(path.join(dir, "fit.json"), `${JSON.stringify(fit, null, 1)}\n`);
  return { dialogue, srt, fit, over };
}
