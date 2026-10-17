// Speaking re-shoot jobs: for every shot of an episode whose line is spoken by a character who is
// on screen (and the shot has its own first frame), a 4 s clip prompt that keeps the shot's action
// and adds the speaker saying the line with clearly moving lips.
//   node gen-speak.mjs <video.json> <lock.json> <receipts.jsonl> <episode> <out.json>
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";

const [vf, lf, rf, ep, out] = process.argv.slice(2);
const video = JSON.parse(readFileSync(vf, "utf8"));
const lock = JSON.parse(readFileSync(lf, "utf8"));
const urls = {};
for (const line of readFileSync(rf, "utf8").trim().split("\n")) {
  const r = JSON.parse(line);
  if (r.label?.startsWith(`e${ep}-`) && /-t\d$/.test(r.label)) urls[r.label.replace(/-t\d$/, "")] = r.url.split("/moss/prod/")[1];
}
const EN = { xuyan: "Xu Yan", aling: "A-ling", qinshuang: "Qin Shuang", tangxiaotang: "Tang Xiaotang", xiaohe: "little Xiaohe", erniu: "Wang Erniu", qianyuanwai: "Qian Yuanwai", zhaobutou: "Zhao Butou", mianshiguan: "the interviewer", laisan: "Lai San" };
const P = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] ";
const S = " Natural, realistic human motion; faces and costumes stay the same; no morphing, no cuts. Keep the supplied first frame's composition, character identities, costumes and props; one continuous shot with no cuts and no on-screen text.\noverall_soundscape: N/A\nnon_diegetic_music: N/A";
const jobs = {};
for (const s of video.scenes) {
  if (s.data.source) continue;
  const on = (s.lines ?? []).filter((l) => l.speaker !== "xitong" && (s.data.characters ?? []).includes(l.speaker));
  if (!on.length) continue;
  const url = urls[`e${ep}-${s.id}`];
  if (!url) { console.error("no first frame", s.id); continue; }
  const bySpeaker = {};
  for (const l of on) (bySpeaker[l.speaker] ??= []).push(`「${l.text.replace(/[。]$/, "")}」`);
  const talk = Object.entries(bySpeaker).map(([id, ls]) => `${EN[id] ?? id} speaks ${ls.length > 1 ? `${ls.length} short Mandarin lines, ${ls.join(" then ")}` : `a short Mandarin line, ${ls[0]}`}, ${id === "aling" ? "her" : ["qinshuang", "tangxiaotang", "xiaohe", "mianshiguan"].includes(id) ? "her" : "his"} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes`).join("; ");
  const orig = lock.shots[s.id]?.prompt?.text?.split("[Shot 1] ")[1]?.split(" Natural, realistic human motion")[0] ?? `${s.data.motion} The camera stays still.`;
  const text = `${P}${talk}, while: ${orig}${S}`;
  const sha = createHash("sha256").update(text).digest("hex").slice(0, 16);
  jobs[`${s.id}sp`] = [text, sha, 4, url];
}
writeFileSync(out, JSON.stringify(jobs));
console.log(ep, Object.keys(jobs).length, Object.keys(jobs).join(","), "max", Math.max(...Object.values(jobs).map((j) => j[0].length)));
