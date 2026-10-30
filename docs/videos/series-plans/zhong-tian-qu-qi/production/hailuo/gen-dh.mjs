// 3D donghua (國漫 CG) version of an episode: first-frame jobs and clip prompts in one pass.
// Every shot that is not a source cut gets its own first frame and its own clip (no stills: the
// reference donghua never holds a frame), characters come from the dh- portraits, sets from the
// dh- set pictures. A shot whose speaker is on screen gets the speaking clause first.
//   node gen-dh.mjs <video.json> <lock.json> <ep> <ff-out.json> <clips-out.json>
//
// Clip body since 2026-10-28 (.agents/skills/minimax-h3-colab/references/motion-quality.md §2):
// `[Shot 1]` opens with the official style word and an anchor sentence that cites <Picture 1>, the
// speaking clause and the shot's own motion follow, the camera line is the storyboard's own move in
// the official "type + amplitude + speed" sentence (`locked` stays `holds a static shot`; it used to
// be rewritten into a push-in), and the fixed "camera keeps moving slowly the whole time" tail is
// gone. Seconds: 5 by default (4 s = 107 frames, under the 124 frames H3 was trained on), 6 when
// someone on screen speaks for about 3 s or the motion has two beats; `data.buy_seconds` overrides.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";

const [file, lockFile, ep, ffOut, clipOut] = process.argv.slice(2);
const video = JSON.parse(readFileSync(file, "utf8"));
const lock = JSON.parse(readFileSync(lockFile, "utf8"));
const C = Object.fromEntries(video.characters.map((c) => [c.id, c]));
const STYLE = "3D Chinese donghua CG animation still, like a high-end Chinese 3D animated series or game cinematic, Unreal Engine 5 cinematic render: stylized semi-realistic characters with refined faces and slightly larger expressive eyes, detailed skin that is clearly CG and not a photograph, individually rendered hair strands, physically simulated cloth with wear, dust and grime; cool desaturated grey-blue palette with warm accents, volumetric light and haze, strong rim light, shallow depth of field, dramatic cinematic composition";
const MODERN = "3D Chinese donghua CG animation still of a present-day city, Unreal Engine 5 cinematic render, stylized semi-realistic characters, cool desaturated palette with neon or daylight accents, volumetric light, strong rim light, shallow depth of field";
const SET = [
  [/well pit|half-dug well/i, "dh-set-jingkeng-t1"],
  [/ancestral hall/i, "dh-set-citang-t1"],
  [/deep pool|dark pool/i, "dh-set-shentan-t1"],
  [/irrigation channel|new channel|head of the channel|sluice/i, "dh-set-xinqu-t1"],
  [/granary/i, "dh-set-gucang-t1"],
  [/official road/i, "dh-set-guandao-t1"],
  [/city gate|gatehouse/i, "dh-set-chengmen-t1"],
  [/physician's hall|medicine hall|clinic/i, "dh-set-yiguan-t1"],
  [/back gate of the (Xu )?farmhouse|farmhouse back gate/i, "dh-set-houmen-t1"],
  [/back alley|narrow alley/i, "dh-set-xiaoxiang-t1"],
  [/county jail|jail cell|prison cell/i, "dh-set-dalao-t1"],
  [/town square|county square/i, "dh-set-guangchang-t1"],
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
const DH = new Set(["diaoqi", "baidaifu", "xuyan", "aling", "qinshuang", "tangxiaotang", "xiaohe", "erniu", "qianyuanwai", "zhaobutou", "mianshiguan", "laisan", "sunzhanggui", "huxianling", "shimujiang", "hanbo", "weijihuoji", "weishaoqing", "zhengbo", "tangwanjin"]);
const EN = { diaoqi: "Diao Qi", baidaifu: "Doctor Bai", zhengbo: "Steward Zheng", tangwanjin: "Tang Wanjin", weijihuoji: "the Wei shop clerk", hanbo: "Elder Han", weishaoqing: "Wei Shaoqing", shimujiang: "Carpenter Shi", sunzhanggui: "Sun Zhanggui", huxianling: "Magistrate Hu", xuyan: "Xu Yan", aling: "A-ling", qinshuang: "Qin Shuang", tangxiaotang: "Tang Xiaotang", xiaohe: "little Xiaohe", erniu: "Wang Erniu", qianyuanwai: "Qian Yuanwai", zhaobutou: "Zhao Butou", mianshiguan: "the interviewer", laisan: "Lai San" };
// Portraits redrawn after the first takes: Tang Xiaotang's t2 has the high stand-up collar (2026-10-19).
const PORTRAIT = { tangxiaotang: "dh-tangxiaotang-portrait-t2" };
const portrait = (id) => PORTRAIT[id] ?? `dh-${id}-portrait-t1`;
const HER = new Set(["aling", "qinshuang", "tangxiaotang", "xiaohe", "mianshiguan"]);
const P = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] 3D CG. ";
const S = " One continuous shot. Smooth, weighty 3D CG character animation; faces, hair and costumes stay as in the first frame.\noverall_soundscape: N/A\nnon_diegetic_music: N/A";
// Seconds to buy at 12 points a second (H3 2K): 5 s = 124 frames is the trained minimum; a line
// that fills the shot or a two-beat motion gets 6 s (158 frames). Estimated speech: ~4.3 zh
// characters a second at the cut's 1.07x tempo, plus the cut's lead, gap and tail.
const SECONDS_DEFAULT = 5, SECONDS_TALK = 6, POINTS_PER_SECOND = 12, TALK_THRESHOLD = 3.0;
const speechSeconds = (lines) => (lines.length ? 0.12 + 0.22 + 0.12 * (lines.length - 1) + lines.reduce((a, l) => a + l.text.replace(/[，。！？、…「」\s]/g, "").length / 4.3, 0) : 0);
const twoBeats = (motion) => /\b(then|after that|and then)\b|;/.test(motion);
// The storyboard's camera line in the official H3 sentence (type + amplitude + speed; medium is
// omitted). `locked` is a real choice, not a gap: H3 drifts unless told to hold.
function cameraSentence(camera) {
  const c = String(camera ?? "").toLowerCase();
  const slow = /\b(slow|slowly|gentle|gently|subtle)\b/.test(c);
  const fast = /\b(fast|quick|quickly|whip|snap)\b/.test(c);
  const speed = slow ? " with small amplitude at slow speed" : fast ? " at fast speed" : "";
  if (/\b(locked|static|held still|stays still)\b/.test(c)) return "The camera holds a static shot.";
  if (/\b(track|tracking|follow|follows|following)\b/.test(c)) return `The camera is a tracking shot that follows the subject${slow ? " at slow speed" : ""}.`;
  if (/\b(orbit|arc)\b/.test(c)) return `The camera is an arc shot around the subject${speed}.`;
  if (/\b(push in|dolly in|move in|pushes in)\b/.test(c)) return `The camera pushes in${speed}.`;
  if (/\b(pull out|pull back|dolly out|pulls out)\b/.test(c)) return `The camera pulls out${speed}.`;
  if (/\bpan (left|right)\b/.test(c)) return `The camera pans ${/pan left/.test(c) ? "left" : "right"}${speed}.`;
  if (/\btilt (up|down)\b/.test(c)) return `The camera tilts ${/tilt up/.test(c) ? "up" : "down"}${speed}.`;
  if (/\btruck (left|right)\b/.test(c)) return `The camera trucks ${/truck left/.test(c) ? "left" : "right"}${speed}.`;
  if (/\b(zoom in)\b/.test(c)) return `The camera zooms in${speed}.`;
  if (/\b(zoom out)\b/.test(c)) return `The camera zooms out${speed}.`;
  return ""; // no camera word: the model decides (write `locked` to hold)
}
const ff = [];
const clips = {};
const cameraInMotion = [];
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
    refs.push(looks[id] === "modern" ? "dh-xuyan-modern-t1" : portrait(id));
    people.push(c.name);
    cast.push(`${c.name}: ${named?.appearance ?? c.appearance}`);
  }
  // Characters named in the prompt but missing from the list (the three brides behind Xu Yan in e1-s47) get their portraits too.
  const NAMED = { diaoqi: /Diao Qi/, baidaifu: /Doctor Bai/, zhengbo: /Steward Zheng/, tangwanjin: /Tang Wanjin/, weijihuoji: /Wei shop clerk/i, hanbo: /Elder Han/, weishaoqing: /Wei Shaoqing/, shimujiang: /Carpenter Shi/, sunzhanggui: /Sun Zhanggui/, huxianling: /Magistrate Hu/, xuyan: /Xu Yan/, aling: /A[- ]?[Ll]ing/, qinshuang: /Qin Shuang/, tangxiaotang: /Tang Xiaotang/, xiaohe: /Xiao ?[Hh]e/, erniu: /Wang Erniu|Erniu/, qianyuanwai: /Qian Yuanwai/, zhaobutou: /Zhao Butou/, laisan: /Lai San/ };
  for (const [id, re] of Object.entries(NAMED)) {
    if ((d.characters ?? []).includes(id) || !C[id]) continue;
    const m = d.prompt.match(re);
    if (!m || /^.{0,25}off (screen|frame)/.test(d.prompt.slice(m.index + m[0].length))) continue;
    refs.push(portrait(id));
    people.push(C[id].name);
    cast.push(`${C[id].name}: ${C[id].appearance}`);
  }
  if (/three (young )?(women|brides)|the three (women|brides)/i.test(d.prompt)) for (const id of ["qinshuang", "aling", "tangxiaotang"]) if (!refs.includes(portrait(id))) { refs.push(portrait(id)); people.push(C[id].name); cast.push(`${C[id].name}: ${C[id].appearance}`); }
  const modern = /meeting room|office building|city street|modern|wastebasket|neon|asphalt|streetlight/i.test(d.prompt);
  const set = modern ? null : SET.find(([re]) => re.test(d.prompt))?.[1];
  if (set) refs.push(set);
  const unique = [...new Set(refs)];
  const notes = [];
  if (people.length) notes.push(`${people.join(" and ")} must be the same characters as in their reference portraits (same faces, hair, costumes and the same 3D donghua art style)`);
  if (set) notes.push("the location matches the set reference picture");
  const prompt = `${d.prompt}, 16:9 frame. Style: ${modern ? MODERN : STYLE}. Camera: ${d.camera}.${cast.length ? ` Characters: ${cast.join("; ")}.` : ""}${notes.length ? ` Reference images: ${notes.join("; ")}.` : ""} Not a photograph, not live action. No text, no letters, no watermark, no UI.`;
  ff.push({ id: scene.id, kind: "clip", refs: unique.map((n) => `${n}.png`), want: `1 ${20 + unique.length} 創建`, prompt });

  // Clip: anchor on the first frame, then the speaking clause, the shot's own motion and its own camera move.
  const english = (d.characters ?? []).filter((id) => DH.has(id)).map((id) => EN[id] ?? C[id]?.name).concat(people.filter((n) => !(d.characters ?? []).some((id) => C[id]?.name === n)).map((n) => EN[Object.keys(C).find((id) => C[id].name === n)] ?? n));
  const who = [...new Set(english)];
  const named = who.length ? `${who.join(" and ")} shown in <Picture 1> ${who.length > 1 ? "keep" : "keeps"} the same face, hair, costume and props as the first frame; the set layout stays as it is.` : "The scene shown in <Picture 1> keeps the first frame's set layout and props.";
  const locked = lock.shots[scene.id]?.prompt?.text?.split("[Shot 1] ")[1]?.split(" Natural, realistic human motion")[0];
  // A trailing ", the camera panning left toward him" in motion duplicates data.camera: the clip
  // gets one camera sentence, from data.camera, so the clause is dropped and the shot is listed.
  let motion = String(d.motion ?? "").trim().replace(/[.。]+$/, "");
  if (/\bcamera\b/i.test(motion)) {
    cameraInMotion.push(scene.id);
    motion = motion.replace(/,?\s*(?:the|with the|as the|while the)\s+camera\b[^.;]*$/i, "").trim();
  }
  const camera = cameraSentence(d.camera);
  const orig = locked ?? `${motion}. ${camera}`.trim();
  const on = (scene.lines ?? []).filter((l) => l.speaker !== "xitong" && (d.characters ?? []).includes(l.speaker));
  const by = {};
  for (const l of on) (by[l.speaker] ??= []).push(`「${l.text.replace(/[。]$/, "")}」`);
  const talk = Object.entries(by).map(([id, ls]) => `${EN[id] ?? id} speaks ${ls.length > 1 ? `${ls.length} short Mandarin lines, ${ls.join(" then ")}` : `a short Mandarin line, ${ls[0]}`}, ${HER.has(id) ? "her" : "his"} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes`).join("; ");
  // Her collar sentence opens the clip (e25 on): a fixed look the clip must keep, and it keeps a re-shot
  // clip from matching the card of the one it replaces.
  const collar = (d.characters ?? []).includes("tangxiaotang") && /stand-up mandarin collar/.test(C.tangxiaotang?.appearance ?? "") ? "Tang Xiaotang's high stand-up collar stays closed at her throat. " : "";
  const text = `${P}${named} ${collar}${talk && !/ speaks /.test(orig) ? `${talk}, while: ` : ""}${orig}${S}`;
  const seconds = Number(d.buy_seconds) || (speechSeconds(on) > TALK_THRESHOLD || twoBeats(motion) ? SECONDS_TALK : SECONDS_DEFAULT);
  if (d.visual !== "still") clips[`a${ep}-${scene.id}`] = [text, createHash("sha256").update(text).digest("hex").slice(0, 16), seconds];
}
writeFileSync(ffOut, JSON.stringify(ff, null, 1));
writeFileSync(clipOut, JSON.stringify(clips));
const pts = ff.reduce((a, j) => a + 20 + j.refs.length, 0);
const clipList = Object.values(clips);
const clipPts = clipList.reduce((a, c) => a + c[2] * POINTS_PER_SECOND, 0);
const bySeconds = clipList.reduce((a, c) => ((a[c[2]] = (a[c[2]] ?? 0) + 1), a), {});
console.log(`${ff.length} first frames ≈ ${pts} points; ${clipList.length} clips (${Object.entries(bySeconds).map(([s, n]) => `${n} × ${s} s`).join(", ")}) ≈ ${clipPts} points; total ≈ ${pts + clipPts}`);
console.log("max ff prompt", Math.max(...ff.map((j) => j.prompt.length)), "max clip prompt", Math.max(...clipList.map((c) => c[0].length)));
if (cameraInMotion.length) console.log(`motion mentioned the camera in ${cameraInMotion.join(", ")}: a trailing camera clause was dropped (the clip gets its one camera sentence from data.camera); keep camera words out of motion in the storyboard`);
