// First-frame jobs for a 種田娶妻 episode (adapted from 長燈村 gen-ff-jobs2): one job per clip or
// still shot (source cuts reuse their source), refs = each on-screen character's portrait and
// turnaround (or the modern portrait for a shot_look "modern") plus a set reference picked from
// the prompt, prompt = shot prompt + look style + camera + verbatim character appearance.
//   node gen-ff-zt.mjs <video.json> <out.json>
import { readFileSync, writeFileSync } from "node:fs";

const [file, out] = process.argv.slice(2);
const video = JSON.parse(readFileSync(file, "utf8"));
const C = Object.fromEntries(video.characters.map((c) => [c.id, c]));
const SET = [
  [/dirt yard|farmhouse yard|in the yard|courtyard/i, "set-xujia-yuan-t1"],
  [/inside (the|a) (poor )?(thatched )?(farmhouse|room|hut)|thatched room|farmhouse interior|inside the house/i, "set-xujia-wu-t1"],
  [/stream|riverbank|river bank|willow/i, "set-liuxi-he-t1"],
];
const jobs = [];
for (const scene of video.scenes) {
  if (scene.template !== "shot" || scene.data.source) continue;
  const d = scene.data;
  const looks = d.character_looks ?? scene.character_looks ?? {};
  const refs = [];
  const people = [];
  const cast = [];
  for (const id of d.characters ?? []) {
    const c = C[id];
    if (!c) continue;
    const lookId = looks[id];
    const named = lookId ? (c.shot_looks ?? []).find((l) => l.id === lookId) : null;
    if (lookId === "modern") refs.push("xuyan-modern-t1", "xuyan-portrait-t1");
    else if (["mianshiguan", "zhaobutou", "laisan"].includes(id)) refs.push(`${id}-portrait-t1`);
    else refs.push(`${id}-portrait-t1`, `${id}-turnaround-t1`);
    people.push(c.name);
    cast.push(`${c.name}: ${named?.appearance ?? c.appearance}`);
  }
  const set = SET.find(([re]) => re.test(d.prompt))?.[1];
  if (set) refs.push(set);
  const unique = [...new Set(refs)];
  const notes = [];
  if (people.length) notes.push(`${people.join(" and ")} must be the same people as in their reference portraits and character sheets (same faces, hair and costumes)`);
  if (set) notes.push("the location matches the set reference image (same buildings and layout)");
  const modern = /meeting room|office|city street|modern|wastebasket|neon|asphalt|umbrella|power line|electric|street light|streetlight|city/i.test(d.prompt);
  const style = modern ? "photorealistic live-action modern-day drama, film still, cinematic light, realistic skin and fabric texture, shallow depth of field" : video.look.style;
  const prompt = `${d.prompt}, 16:9 film frame. Style: ${style}. Camera: ${d.camera}.${cast.length ? ` Characters: ${cast.join("; ")}.` : ""}${notes.length ? ` Reference images: ${notes.join("; ")}.` : ""} No text, no letters, no watermark, no UI.`;
  jobs.push({ id: scene.id, kind: d.visual === "still" ? "still" : "clip", refs: unique.map((n) => `${n}.png`), want: `1 ${20 + unique.length} 創建`, prompt });
}
writeFileSync(out, JSON.stringify(jobs, null, 1));
console.log(jobs.length, "jobs; refs", jobs.reduce((a, j) => a + j.refs.length, 0), "; points ≈", jobs.reduce((a, j) => a + 20 + j.refs.length, 0), "; max prompt", Math.max(...jobs.map((j) => j.prompt.length)));
