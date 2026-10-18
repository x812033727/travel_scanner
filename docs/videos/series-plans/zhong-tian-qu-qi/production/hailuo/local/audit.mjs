// node audit.mjs [from] [to] : audit the 3D donghua episodes: storyboard vs clip jobs, first frames, clips, audio, cut.
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";

import { fileURLToPath } from "node:url";
const R = fileURLToPath(new URL("../../../../../../../", import.meta.url)).replace(/[\/]$/, "");
const V = process.env.VIDEO_WORKDIR ?? `${process.env.HOME ?? process.env.USERPROFILE}/mokaair-work/videos`;
const H = R + "/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo";
const cast = JSON.parse(readFileSync(R + "/docs/videos/series-plans/zhong-tian-qu-qi/production/cast.json", "utf8"));
const probe = (f) => { try { const o = execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height", "-of", "json", f]).toString(); const j = JSON.parse(o); const v = j.streams.find((s) => s.codec_type === "video"); return { d: +j.format.duration, w: v?.width, h: v?.height }; } catch { return null; } };
const castVoices = Object.fromEntries((cast.characters ?? Object.entries(cast).map(([id, c]) => ({ id, ...c }))).map((c) => [c.id, c.voice?.name ?? c.voice]));

const [from = 1, to = 20] = process.argv.slice(2).map(Number);
for (let n = from; n <= to; n++) {
  const e = String(n).padStart(3, "0");
  const out = [];
  const vf = `${R}/docs/videos/zhong-tian-qu-qi-e${e}/video.json`;
  if (!existsSync(vf)) { console.log(`e${e}: NO video.json`); continue; }
  const v = JSON.parse(readFileSync(vf, "utf8"));
  const W = `${V}/zhong-tian-qu-qi-e${e}-dh`;
  const shots = v.scenes.filter((s) => s.template === "shot" && !s.data.source).map((s) => s.id);
  const jobs = Object.keys(JSON.parse(readFileSync(`${H}/clips-dh-e${e}.json`, "utf8"))).map((k) => k.split("-")[1]);
  const ff = JSON.parse(readFileSync(`${H}/ff-dh-e${e}.json`, "utf8")).map((j) => j.id);
  const miss = (a, b) => a.filter((x) => !b.includes(x));
  if (miss(shots, jobs).length) out.push("shots without clip job: " + miss(shots, jobs));
  if (miss(shots, ff).length) out.push("shots without ff job: " + miss(shots, ff));
  const clips = existsSync(W + "/clips") ? readdirSync(W + "/clips") : [];
  const ffs = existsSync(W + "/first-frames") ? readdirSync(W + "/first-frames") : [];
  const noClip = jobs.filter((id) => !clips.some((f) => f.startsWith(id + "-t") && f.endsWith(".mp4")));
  const noFf = ff.filter((id) => !ffs.some((f) => f.startsWith(id + "-t")));
  if (noFf.length) out.push("first frames missing: " + noFf.join(","));
  if (noClip.length) out.push(`clips missing (${noClip.length}): ` + noClip.join(","));
  const bad = [];
  for (const f of clips.filter((f) => f.endsWith(".mp4"))) { const p = probe(`${W}/clips/${f}`); if (!p || !(p.d >= 3.5) || !p.w) bad.push(`${f}:${p ? p.d.toFixed(2) + "s " + p.w + "x" + p.h : "unreadable"}`); }
  if (bad.length) out.push("bad clips: " + bad.join(" "));
  // Audio: every line has a wav, recorded after its speaker's current voice was set.
  const lines = v.scenes.flatMap((s) => (s.lines ?? []).map((l) => ({ ...l, scene: s.id })));
  const aud = existsSync(W + "/audio") ? readdirSync(W + "/audio") : [];
  const noAud = lines.filter((l) => !aud.includes(l.id + ".wav")).map((l) => l.id);
  if (noAud.length) out.push(`audio missing (${noAud.length}): ` + noAud.join(","));
  const vv = Object.fromEntries((v.characters ?? []).map((c) => [c.id, c.voice?.name ?? c.voice]));
  const vdiff = Object.entries(castVoices).filter(([id, name]) => vv[id] && JSON.stringify(vv[id]) !== JSON.stringify(name)).map(([id]) => id);
  if (vdiff.length) out.push("voice differs from cast.json: " + vdiff.join(","));
  const empty = lines.filter((l) => !l.text?.trim()).map((l) => l.id);
  if (empty.length) out.push("empty lines: " + empty);
  // Cut: exists, newer than every clip and wav it uses.
  const cut = `${W}/cut/e${e}-dh-phone.mp4`;
  if (!existsSync(cut)) out.push("NO cut yet");
  else {
    const ct = statSync(cut).mtimeMs;
    const newer = [...clips.map((f) => `${W}/clips/${f}`), ...aud.map((f) => `${W}/audio/${f}`)].filter((f) => statSync(f).mtimeMs > ct).map((f) => f.split("/").pop());
    if (newer.length) out.push(`cut older than ${newer.length} inputs: ` + newer.slice(0, 8).join(","));
    const log = readFileSync(`${W}/cut/final.log`, "utf8");
    const warn = log.split("\n").filter((l) => /missing|warn|error|not found|fallback|held [1-9]/i.test(l));
    if (warn.length) out.push("log: " + warn.slice(0, 6).join(" / "));
    if (!/exit 0/.test(log)) out.push("assembly did not exit 0");
    const p = probe(cut); out.push(`cut ${p?.d?.toFixed(1)}s`);
  }
  if (!existsSync(`${H}/edit-dh-e${e}.json`)) out.push("NO edit config");
  console.log(`e${e} [${shots.length} shots, ${lines.length} lines]: ` + (out.join(" | ") || "ok"));
}
