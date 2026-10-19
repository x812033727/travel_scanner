// redo-gen.mjs <repo> <redo-dh-scan-list.json> <redo-dh-scan.json> [--patch]
// The 2026-10-19 scan of episodes 1-24 (costume, blood-like dye, legible text, strangers, hands).
// Builds first-frame and clip jobs for the scan's fix list. With --patch it first copies Tang
// Xiaotang's high-collar appearance from cast.json into e001-e024 video.json.
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [repo, listFile, outFile, flag] = process.argv.slice(2);
const H = join(repo, "docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo");
const cast = JSON.parse(readFileSync(join(H, "../cast.json"), "utf8"));
const T = (Array.isArray(cast) ? cast : cast.characters ?? Object.values(cast)).find((c) => c.id === "tangxiaotang");
const list = JSON.parse(readFileSync(listFile, "utf8"));
const tmp = mkdtempSync(join(tmpdir(), "redo-"));
const TAKE = "t6";

const FF = {
  tang: "Tang Xiaotang's high stand-up mandarin collar is fastened at her throat and her thick opaque peach-pink brocade covers her collarbones and chest completely; no skin below her neck shows, nothing sheer",
  text: "every paper, page, card and notice shows only soft blurred grey smudges that cannot be read, no characters or letters anywhere, and any red seal is a plain solid red square or circle with nothing inside it",
  red: "the dye on the hands is a flat dry matte bright orange like freshly dyed cloth, clearly dye and not blood: nothing wet, glossy, dripping or dark red",
  seal: "only the pad of the thumb carries a small dry matte vermilion paste mark, the rest of the hand is clean, nothing wet, glossy or dripping, nothing that looks like blood",
  scar: "the mark on her wrist is a faint thin pale silvery old scar, long healed, the same colour as her skin, no redness, no wound",
  hand: "every person has exactly two arms and two hands; hands never pass through or merge with another arm, a hand that grips a wrist wraps around it from the outside",
  strangers: "the three young women behind Xu Yan are exactly Qin Shuang, A-ling and Tang Xiaotang from their reference portraits, nobody else",
  drift: "Tang Xiaotang keeps her own face, her two looped buns with pink ribbons and pearl pins, exactly as in her reference portrait",
};
const CLIP = {
  tang: "",
  text: "The papers stay blank with no readable writing. ",
  red: "The dye on the hands stays a flat dry matte orange, never wet, glossy or dark red. ",
  seal: "The paste on the thumb stays a small dry matte vermilion mark, nothing wet. ",
  scar: "The wrist scar stays a faint pale old line. ",
  hand: "Every hand stays whole and separate, exactly two hands per person. ",
  strangers: "The three young women stay Qin Shuang, A-ling and Tang Xiaotang. ",
  drift: "Tang Xiaotang's face and hair stay exactly the same. ",
};
const P = "[Shot 1] ";
const jobs = [];
for (const [ep, shots] of Object.entries(list)) {
  if (ep.startsWith("_")) continue;
  const e3 = String(ep).padStart(3, "0");
  const vf = join(repo, `docs/videos/zhong-tian-qu-qi-e${e3}/video.json`);
  if (flag === "--patch") {
    const v = JSON.parse(readFileSync(vf, "utf8"));
    const t = v.characters.find((c) => c.id === "tangxiaotang");
    if (t && t.appearance !== T.appearance) { t.appearance = T.appearance; writeFileSync(vf, JSON.stringify(v, null, 2) + "\n"); }
  }
  const ffo = join(tmp, `ff${e3}.json`), clo = join(tmp, `cl${e3}.json`);
  execFileSync("node", [join(H, "gen-dh.mjs"), vf, join(H, "local/empty-lock.json"), String(ep), ffo, clo]);
  const ff = JSON.parse(readFileSync(ffo, "utf8"));
  const cl = JSON.parse(readFileSync(clo, "utf8"));
  for (const [id, kind] of Object.entries(shots)) {
    const f = ff.find((j) => j.id === id);
    const c = cl[`a${ep}-${id}`];
    if (!f) { console.error(`e${e3} ${id}: no first frame of its own (fixed through its source shot)`); continue; }
    const extra = FF[kind] + (kind !== "tang" && f.refs.some((r) => r.includes("tangxiaotang")) ? "; " + FF.tang : "");
    let base = f.prompt;
    if (kind === "red") base = base.replace(/red-stained/g, "orange-dyed").replace(/red (hand|hands|palm|palms)/g, "orange-dyed $1").replace(/bright orange-red dye/g, "flat bright orange dye");
    if (kind === "seal") base = base.replace("a right thumb red with seal ink", "a right thumb with a small dry vermilion paste mark on its pad").replace("with a thumb dipped in the vermilion paste", "with a small dry vermilion paste mark on the pad of the thumb");
    const prompt = base.replace(", 16:9 frame.", `, ${extra}, 16:9 frame.`);
    let text = c ? c[0] : null;
    const add = CLIP[kind];
    if (add && text) text = text.replace(P, P + add);
    if (text && kind === "red") text = text.replace(/the red hand/g, "the orange-dyed hand").replace(/the red hands/g, "the orange-dyed hands").replace(/bright orange-red dye/g, "flat bright orange dye").replace(/stained the very same orange-red/g, "dyed the very same flat orange");
    jobs.push({ e: Number(ep), id, kind, label: `a${ep}-${id}-${TAKE}`, refs: f.refs, names: f.refs.map((r) => r.replace(/\.png$/, "")), prompt, clip: text ? [text, createHash("sha256").update(text).digest("hex").slice(0, 16), c[2]] : null });
  }
}
writeFileSync(outFile, JSON.stringify(jobs, null, 1));
console.log(jobs.length, "jobs;", jobs.filter((j) => !j.prompt.includes(FF[j.kind])).length, "without their fix sentence");
