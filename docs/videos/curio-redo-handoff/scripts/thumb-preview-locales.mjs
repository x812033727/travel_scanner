import { readFileSync, writeFileSync } from "node:fs";
import { openRenderer } from "./tools/video/render/browser.mjs";
import { thumbnailHtml, THUMB_SIZE } from "./tools/video/templates/templates.mjs";
const [slug, out, layout] = process.argv.slice(2);
const W = `/root/mokaair-work/videos/${slug}`;
const doc = JSON.parse(readFileSync(`docs/videos/${slug}/video.json`, "utf8"));
const m = JSON.parse(readFileSync(W + "/keyframes/manifest.json", "utf8"));
const shot = doc.thumbnail.data.shot;
const r = await openRenderer({ root: process.cwd(), workdir: W });
let i = 0;
for (const loc of ["en","ja","ko","es","pt","id","th","vi"]) {
  const t = JSON.parse(readFileSync(`docs/videos/${slug}/i18n/${loc}.json`, "utf8")).thumbnail;
  const data = { ...doc.thumbnail.data, ...t, layout };
  const html = thumbnailHtml({ template: "thumb", data }, { background: "/work/" + m.shots[shot].file, subject: "shot", slug, locale: loc });
  const res = await r.capture((++i).toString(16).padStart(4, "0"), html, { size: THUMB_SIZE, type: "png" });
  writeFileSync(`${out}-${loc}.png`, res.still);
  if (res.problems?.length) console.log(loc, res.problems.join(" | "));
}
await r.close?.();
