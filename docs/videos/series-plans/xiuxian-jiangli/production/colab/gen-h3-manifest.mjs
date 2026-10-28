// 從鎖定檔產生 Colab H3 的工作清單：h3/prompts/<id>.txt（定稿正文原封不動）、h3/manifest.json（每個 clip 鏡頭一支）、
// h3/manifest-pilot.json（鎖定檔的小樣鏡頭）。畫布 1312×736（16:9 首格不拉伸，minimax-h3-colab/references/motion-quality.md
// 第三節），秒數照鎖定檔的 buy_s，prompt_sha256 等於鎖定檔的正文雜湊（h3.sh check 會對）。
//
//   node docs/videos/series-plans/xiuxian-jiangli/production/colab/gen-h3-manifest.mjs [<lock.json>]
//
// 預設讀 ../e001-plan-lock.json（鎖定檔從 <VIDEO_WORKDIR>/<slug>/plan/lock.json 抄來）。離線、不花錢。
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const lockFile = process.argv[2] ?? path.join(here, "..", "e001-plan-lock.json");
const lock = JSON.parse(readFileSync(lockFile, "utf8"));
const episode = lock.slug ?? "xiuxian-jiangli-e001";
const WIDTH = 1312, HEIGHT = 736;
const outDir = path.join(here, "h3");
mkdirSync(path.join(outDir, "prompts"), { recursive: true });

const jobs = [];
for (const [id, shot] of Object.entries(lock.shots)) {
  if (shot.visual_kind !== "clip" || !shot.prompt?.text) continue;
  const text = shot.prompt.text;
  const sha = createHash("sha256").update(text).digest("hex");
  if (shot.prompt.sha256 && shot.prompt.sha256 !== sha) throw new Error(`${id}: the lock's sha256 does not match its own text`);
  writeFileSync(path.join(outDir, "prompts", `${id}.txt`), text);
  jobs.push({
    id, title: `${episode} ${id}`, inference_mode: "first_frame", reference_images: [`first-frames/${id}.png`],
    prompt_file: `prompts/${id}.txt`, duration_seconds: shot.buy_s, width: WIDTH, height: HEIGHT, output_name: `${id}-t1.mp4`, prompt_sha256: sha,
  });
}
const note = (which) => `manifest 給 .agents/skills/minimax-h3-colab 的 h3.sh batch（在 h3/ 目錄裡跑）：reference_images 的 first-frames/<id>.png 要先放好（通過 judge 的關鍵影格經 fit_first_frame.sh 裁成 ${WIDTH}×${HEIGHT}），prompts/<id>.txt 是鎖定檔的定稿正文原封不動（prompt_sha256 等於鎖定檔）；秒數照鎖定檔（H3 最少 5 秒、說話鏡 6 秒）；取樣 profile smooth。${which}`;
const write = (name, list, which) => writeFileSync(path.join(outDir, name), `${JSON.stringify({ episode, generated_from: path.basename(lockFile), locked_at: lock.locked_at ?? null, note: note(which), jobs: list }, null, 1)}\n`);
write("manifest.json", jobs, `整集 ${jobs.length} 支（靜圖與切素材不買）。`);
const pilot = new Set(lock.pilot ?? []);
write("manifest-pilot.json", jobs.filter((job) => pilot.has(job.id)), `小樣 ${[...pilot].join("、")}。`);
const seconds = jobs.reduce((a, j) => a + j.duration_seconds, 0);
console.log(`${jobs.length} jobs, ${seconds} s; pilot ${[...pilot].join(", ")}; prompts ${Math.max(...jobs.map((j) => readFileSync(path.join(outDir, j.prompt_file), "utf8").length))} chars max`);
