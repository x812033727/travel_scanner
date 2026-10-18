// 3D donghua (國漫 CG) version of an episode: first-frame jobs and clip prompts in one pass.
// Every shot that is not a source cut gets its own first frame and its own clip (no stills: the
// reference donghua never holds a frame), characters come from the dh- portraits, sets from the
// dh- set pictures. A shot whose speaker is on screen gets the speaking clause first.
//   node gen-dh.mjs <video.json> <lock.json> <ep> <ff-out.json> <clips-out.json>
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";

const [file, lockFile, ep, ffOut, clipOut] = process.argv.slice(2);
const video = JSON.parse(readFileSync(file, "utf8"));
const lock = JSON.parse(readFileSync(lockFile, "utf8"));
const C = Object.fromEntries(video.characters.map((c) => [c.id, c]));
const STYLE = "3D Chinese donghua CG animation still, like a high-end Chinese 3D animated series or game cinematic, Unreal Engine 5 cinematic render: stylized semi-realistic characters with refined faces and slightly larger expressive eyes, detailed skin that is clearly CG and not a photograph, individually rendered hair strands, physically simulated cloth with wear, dust and grime; cool desaturated grey-blue palette with warm accents, volumetric light and haze, strong rim light, shallow depth of field, dramatic cinematic composition";
const MODERN = "3D Chinese donghua CG animation still of a present-day city, Unreal Engine 5 cinematic render, stylized semi-realistic characters, cool desaturated palette with neon or daylight accents, volumetric light, strong rim light, shallow depth of field";
const SET = [
  [/county academy gate|academy gate/i, "dh-set-shuyuan-t1"],
  [/Xu family shop/i, "dh-set-xuji-pu-t1"],
  [/county inn guest room/i, "dh-set-kezhan-t1"],
  [/small ferry boat/i, "dh-set-chuan-t1"],
  [/sugar workshop/i, "dh-set-tangfang-t1"],
  [/ferry landing/i, "dh-set-dukou-t1"],
  [/roof of the farmhouse|farmhouse roof/i, "dh-set-wuding-t1"],
  [/county yamen|yamen gate|yamen hall/i, "dh-set-xianya-t1"],
  [/teahouse/i, "dh-set-chalou-t1"],
  [/market street|county town market/i, "dh-set-shiji-t1"],
  [/silk shop/i, "dh-set-chouduan-t1"],
  [/escort agency/i, "dh-set-biaoju-t1"],
  [/Qian manor gate/i, "dh-set-qianfu-men-t1"],
  [/Qian manor hall|Qian manor/i, "dh-set-qianfu-ting-t1"],
  [/village entrance/i, "dh-set-cunkou-t1"],
  [/bamboo grove|nameless grave/i, "dh-set-zhulin-fen-t1"],
  [/carpenter's workshop/i, "dh-set-mujiang-fang-t1"],
  [/threshing ground/i, "dh-set-dagu-chang-t1"],
  [/spring field|muddy field|ploughed field|plowed field/i, "dh-set-chuntian-t1"],
  [/stone bridge/i, "dh-set-shiqiao-t1"],
  [/work shed|workshop|lean-to/i, "dh-set-gongpeng-t1"],
  [/kitchen/i, "dh-set-xujia-zao-t1"],
  [/dirt yard|farmhouse yard|in the yard|morning yard|courtyard|yard gate|mud wall|woodpile|wooden gate|broken gate/i, "dh-set-xujia-yuan-t1"],
  [/inside (the|a) (poor )?(thatched )?(farmhouse|room|hut)|thatched room|farmhouse interior|inside the house|in the farmhouse/i, "dh-set-xujia-wu-t1"],
  [/stream|riverbank|river bank|willow|reeds/i, "dh-set-liuxi-he-t1"],
];
// Characters with a 3D portrait (refs-dh-jobs*.json); others are described in the prompt only.
const DH = new Set(["xuyan", "aling", "qinshuang", "tangxiaotang", "xiaohe", "erniu", "qianyuanwai", "zhaobutou", "mianshiguan", "laisan", "sunzhanggui", "huxianling", "shimujiang", "hanbo", "weijihuoji", "weishaoqing"]);
const EN = { weijihuoji: "the Wei shop clerk", hanbo: "Elder Han", weishaoqing: "Wei Shaoqing", shimujiang: "Carpenter Shi", sunzhanggui: "Sun Zhanggui", huxianling: "Magistrate Hu", xuyan: "Xu Yan", aling: "A-ling", qinshuang: "Qin Shuang", tangxiaotang: "Tang Xiaotang", xiaohe: "little Xiaohe", erniu: "Wang Erniu", qianyuanwai: "Qian Yuanwai", zhaobutou: "Zhao Butou", mianshiguan: "the interviewer", laisan: "Lai San" };
const HER = new Set(["aling", "qinshuang", "tangxiaotang", "xiaohe", "mianshiguan"]);
const P = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] ";
const S = " 3D Chinese donghua CG animation with smooth, weighty, expressive character animation; the camera keeps moving slowly the whole time; faces, hair and costumes stay the same; no morphing, no cuts. Keep the supplied first frame's composition, art style, character identities, costumes and props; one continuous shot with no cuts and no on-screen text.\noverall_soundscape: N/A\nnon_diegetic_music: N/A";
const ff = [];
const clips = {};
for (const scene of video.scenes) {
  if (scene.template !== "shot" || scene.data.source) continue;
  const d = scene.data;
  const looks = d.character_looks ?? {};
  const refs = [];
  const people = [];
  const cast = [];
  for (const id of d.characters ?? []) {
    const c = C[id];
    if (!c) continue;
    if (!DH.has(id)) { cast.push(`${c.name}: ${c.appearance}`); continue; }
    const named = looks[id] ? (c.shot_looks ?? []).find((l) => l.id === looks[id]) : null;
    refs.push(looks[id] === "modern" ? "dh-xuyan-modern-t1" : `dh-${id}-portrait-t1`);
    people.push(c.name);
    cast.push(`${c.name}: ${named?.appearance ?? c.appearance}`);
  }
  // Characters named in the prompt but missing from the list (the three brides behind Xu Yan in e1-s47) get their portraits too.
  const NAMED = { weijihuoji: /Wei shop clerk/i, hanbo: /Elder Han/, weishaoqing: /Wei Shaoqing/, shimujiang: /Carpenter Shi/, sunzhanggui: /Sun Zhanggui/, huxianling: /Magistrate Hu/, xuyan: /Xu Yan/, aling: /A[- ]?[Ll]ing/, qinshuang: /Qin Shuang/, tangxiaotang: /Tang Xiaotang/, xiaohe: /Xiao ?[Hh]e/, erniu: /Wang Erniu|Erniu/, qianyuanwai: /Qian Yuanwai/, zhaobutou: /Zhao Butou/, laisan: /Lai San/ };
  for (const [id, re] of Object.entries(NAMED)) {
    if ((d.characters ?? []).includes(id) || !C[id]) continue;
    const m = d.prompt.match(re);
    if (!m || /^.{0,25}off (screen|frame)/.test(d.prompt.slice(m.index + m[0].length))) continue;
    refs.push(`dh-${id}-portrait-t1`);
    people.push(C[id].name);
    cast.push(`${C[id].name}: ${C[id].appearance}`);
  }
  if (/three (young )?(women|brides)|the three (women|brides)/i.test(d.prompt)) for (const id of ["qinshuang", "aling", "tangxiaotang"]) if (!refs.includes(`dh-${id}-portrait-t1`)) { refs.push(`dh-${id}-portrait-t1`); people.push(C[id].name); cast.push(`${C[id].name}: ${C[id].appearance}`); }
  const modern = /meeting room|office building|city street|modern|wastebasket|neon|asphalt|streetlight/i.test(d.prompt);
  const set = modern ? null : SET.find(([re]) => re.test(d.prompt))?.[1];
  if (set) refs.push(set);
  const unique = [...new Set(refs)];
  const notes = [];
  if (people.length) notes.push(`${people.join(" and ")} must be the same characters as in their reference portraits (same faces, hair, costumes and the same 3D donghua art style)`);
  if (set) notes.push("the location matches the set reference picture");
  const prompt = `${d.prompt}, 16:9 frame. Style: ${modern ? MODERN : STYLE}. Camera: ${d.camera}.${cast.length ? ` Characters: ${cast.join("; ")}.` : ""}${notes.length ? ` Reference images: ${notes.join("; ")}.` : ""} Not a photograph, not live action. No text, no letters, no watermark, no UI.`;
  ff.push({ id: scene.id, kind: "clip", refs: unique.map((n) => `${n}.png`), want: `1 ${20 + unique.length} 創建`, prompt });

  // Clip: the shot's own motion from the plan lock (or the storyboard), with the speaking clause first.
  let orig = lock.shots[scene.id]?.prompt?.text?.split("[Shot 1] ")[1]?.split(" Natural, realistic human motion")[0] ?? `${d.motion}. ${/push|pull|dolly|track|orbit|pan|tilt/i.test(d.camera) ? `Camera: ${d.camera}.` : "The camera pushes in slowly."}`;
  orig = orig.replace(/The camera is a static shot[^.]*.|The camera (stays|is held) [^.]*still[^.]*./g, "The camera pushes in slowly.");
  const on = (scene.lines ?? []).filter((l) => l.speaker !== "xitong" && (d.characters ?? []).includes(l.speaker));
  const by = {};
  for (const l of on) (by[l.speaker] ??= []).push(`「${l.text.replace(/[。]$/, "")}」`);
  const talk = Object.entries(by).map(([id, ls]) => `${EN[id] ?? id} speaks ${ls.length > 1 ? `${ls.length} short Mandarin lines, ${ls.join(" then ")}` : `a short Mandarin line, ${ls[0]}`}, ${HER.has(id) ? "her" : "his"} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes`).join("; ");
  const text = `${P}${talk && !/ speaks /.test(orig) ? `${talk}, while: ` : ""}${orig}${S}`;
  if (d.visual !== "still") clips[`a${ep}-${scene.id}`] = [text, createHash("sha256").update(text).digest("hex").slice(0, 16), 4];
}
writeFileSync(ffOut, JSON.stringify(ff, null, 1));
writeFileSync(clipOut, JSON.stringify(clips));
const pts = ff.reduce((a, j) => a + 20 + j.refs.length, 0);
console.log(`${ff.length} first frames ≈ ${pts} points; ${Object.keys(clips).length} clips ≈ ${Object.keys(clips).length * 48} points; total ≈ ${pts + Object.keys(clips).length * 48}`);
console.log("max ff prompt", Math.max(...ff.map((j) => j.prompt.length)), "max clip prompt", Math.max(...Object.values(clips).map((c) => c[0].length)));
