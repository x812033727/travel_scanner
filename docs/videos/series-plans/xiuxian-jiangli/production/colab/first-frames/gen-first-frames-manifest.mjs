// 從 video.json、鎖定檔與工作目錄的設定圖選擇，產生 Colab 畫首格的工作清單（票 2026-10-28-1-colab-qwen-image-edit-2509）：
// 每個要畫的鏡頭一筆 { id, prompt, negative, references[], seed, width, height }。prompt 用產線 keyframes 同一個
// 組法（shotPrompt：場景、look.style、camera、角色外觀），參照圖＝該鏡角色選定的設定圖（<VIDEO_WORKDIR>/<slug>/characters/…）
// 加同一場已經通過 judge 的關鍵影格當場景參照（最多三張，Qwen-Image-Edit-2509 一到三張最準）。
//
//   VIDEO_WORKDIR=<dir> node gen-first-frames-manifest.mjs [--shots s25,s26,s32] [--out manifest-pilot.json] [--set-ref s34]
//
// 離線、不花錢。參照圖的路徑是絕對路徑（工作目錄不進 git），runner 打包時再複製。
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../../../../../..");
const { shotPrompt, chosenSheets } = await import(path.join(root, "tools/video/media/keyframes.mjs"));
const { resolveLook, shotCast, drawnShotScenes, lookHash } = await import(path.join(root, "tools/video/core/drama.mjs"));
const { loadProject, lookChosen, ARTIFACTS } = await import(path.join(root, "tools/video/core/state.mjs"));

const SLUG = "xiuxian-jiangli-e001";
const WIDTH = 1312, HEIGHT = 736;
const values = parseArgs({ options: { shots: { type: "string" }, out: { type: "string" }, "set-ref": { type: "string" }, seed: { type: "string" } }, strict: true }).values;
const workBase = process.env.VIDEO_WORKDIR;
if (!workBase) throw new Error("VIDEO_WORKDIR is not set");
const workdir = path.join(workBase, SLUG);
const project = loadProject({ slug: SLUG, root });
const { doc } = project;
const look = resolveLook(doc.look);
const hash = lookHash(doc);
const lookManifest = JSON.parse(readFileSync(path.join(workdir, ARTIFACTS.characters), "utf8"));
const chosen = lookChosen(lookManifest, existsSync(path.join(workdir, ARTIFACTS.characterChoice)) ? JSON.parse(readFileSync(path.join(workdir, ARTIFACTS.characterChoice), "utf8")) : null, hash);
if (!chosen) throw new Error("the look has no chosen sheet for every character; run look --choose first");
const sheets = chosenSheets(lookManifest, chosen);
const keyframes = existsSync(path.join(workdir, ARTIFACTS.keyframes)) ? JSON.parse(readFileSync(path.join(workdir, ARTIFACTS.keyframes), "utf8")) : { shots: {} };
const wanted = values.shots ? new Set(values.shots.split(",").map((s) => s.trim()).filter(Boolean)) : null;
const setRef = values["set-ref"] ? keyframes.shots?.[values["set-ref"]]?.file : null;
if (values["set-ref"] && !setRef) throw new Error(`--set-ref ${values["set-ref"]} has no keyframe in ${ARTIFACTS.keyframes}`);
const seedBase = values.seed ? Number(values.seed) : 1;

// 場：chapter 開一場，之後的鏡頭都屬它（同 shot_plan.mjs）。
const chapters = new Map();
let chapter = null;
for (const scene of doc.scenes) {
  if (typeof scene.chapter === "string" && scene.chapter.trim()) chapter = scene.chapter.trim();
  chapters.set(scene.id, chapter);
}
const chapterOf = (scene) => chapters.get(scene.id) ?? null;

const jobs = [];
for (const scene of drawnShotScenes(doc)) {
  if (wanted && !wanted.has(scene.id)) continue;
  const cast = shotCast(doc, scene);
  const references = [];
  for (const character of cast) if (sheets[character.id]) references.push({ role: "character", name: character.name, file: path.join(workdir, sheets[character.id].file) });
  // The judged keyframe named by --set-ref is the set reference for its own chapter; a shot with no
  // reference at all (an insert with no cast) gets it as a style reference, since the edit model
  // wants at least one picture.
  const setScene = values["set-ref"] ? doc.scenes.find((each) => each.id === values["set-ref"]) : null;
  const sameChapter = setScene && chapterOf(scene) === chapterOf(setScene);
  if (setRef && (sameChapter || references.length === 0)) references.push({ role: sameChapter ? "set" : "style", name: values["set-ref"], file: path.join(workdir, setRef) });
  jobs.push({
    id: scene.id,
    prompt: shotPrompt(scene, look, cast, 4000),
    negative: look.negative || "",
    references: references.slice(0, 3),
    seed: seedBase,
    width: WIDTH,
    height: HEIGHT,
    output_name: `${scene.id}.png`,
  });
}
const out = path.join(here, values.out ?? "manifest.json");
writeFileSync(out, `${JSON.stringify({ episode: SLUG, look_hash: hash, note: "Colab first frames: Qwen-Image-Edit-2509 with the chosen character sheets (and a judged keyframe of the same set) as references; width/height are the H3 first-frame canvas. References are absolute paths in the work directory; ff_runner.py bundles them.", jobs }, null, 1)}\n`);
console.log(`${jobs.length} jobs → ${out}; references per job: ${jobs.map((j) => `${j.id}=${j.references.length}`).join(" ")}`);
