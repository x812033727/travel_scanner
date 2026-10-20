// Import folders for /admin/videos (tools/video/cli.mjs import): final.mp4 (hard link), meta.json,
// zh-TW.srt, thumbnail.png (the season key art, one for every episode and language). A compilation's
// folder also gets, for every locale compile-dh.mjs made, dub.<l>.m4a, <l>.srt and description.<l>.txt
// (its translated title and description), ready for `import --languages`.
//   node prep-import.mjs <n|first-last> ...
import { existsSync, linkSync, mkdirSync, readFileSync, rmSync, writeFileSync, copyFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
const R = fileURLToPath(new URL("../../../../../../../", import.meta.url)).replace(/[\/]$/, "");
const V = process.env.VIDEO_WORKDIR ?? `${process.env.HOME ?? process.env.USERPROFILE}/mokaair-work/videos`;
const OUT = `${V}/zhong-tian-qu-qi-import`;
const THUMB = `${V}/zhong-tian-qu-qi-compilations/season1-thumb.png`;
const pad = (n) => String(n).padStart(3, "0");
const link = (a, b) => { if (existsSync(b)) rmSync(b); linkSync(a, b); };
for (const arg of process.argv.slice(2)) {
  const [a, b] = arg.split("-").map(Number);
  let dir, mp4, srt, meta, langs = [];
  if (b) {
    const C = `${V}/zhong-tian-qu-qi-compilations/e${pad(a)}-${pad(b)}`;
    const yt = JSON.parse(readFileSync(`${C}.youtube.json`, "utf8"));
    dir = `${OUT}/zhong-tian-qu-qi-e${pad(a)}-${pad(b)}`; mp4 = `${C}.mp4`; srt = `${C}.zh-TW.srt`;
    meta = { slug: `zhong-tian-qu-qi-e${pad(a)}-${pad(b)}`, title: yt.title, description: yt.description, category: "drama", note: `種田娶妻打天下 第${a}–${b}集合集（3D 國漫版，海螺手工製作）` };
    langs = Object.entries(yt.localizations ?? {}).map(([l, t]) => ({ l, t, m4a: `${C}.${l}.m4a`, srt: `${C}.${l}.srt` }));
  } else {
    const v = JSON.parse(readFileSync(`${R}/docs/videos/zhong-tian-qu-qi-e${pad(a)}/video.json`, "utf8"));
    const W = `${V}/zhong-tian-qu-qi-e${pad(a)}-dh/cut`;
    dir = `${OUT}/zhong-tian-qu-qi-e${pad(a)}`; mp4 = `${W}/e${pad(a)}-dh.mp4`; srt = `${W}/e${pad(a)}-dh.zh-TW.srt`;
    meta = { slug: `zhong-tian-qu-qi-e${pad(a)}`, title: `種田娶妻打天下 第${a}集 | CC字幕`, description: v.youtube.description, category: "drama", note: `種田娶妻打天下 第${a}集（3D 國漫版，海螺手工製作）` };
  }
  mkdirSync(dir, { recursive: true });
  link(mp4, `${dir}/final.mp4`);
  copyFileSync(srt, `${dir}/zh-TW.srt`);
  copyFileSync(THUMB, `${dir}/thumbnail.png`);
  writeFileSync(`${dir}/meta.json`, JSON.stringify(meta, null, 1));
  for (const { l, t, m4a, srt: cc } of langs) {
    writeFileSync(`${dir}/description.${l}.txt`, `${t.title}\n\n${t.description}\n`);
    if (existsSync(m4a) && existsSync(cc)) { link(m4a, `${dir}/dub.${l}.m4a`); copyFileSync(cc, `${dir}/${l}.srt`); } else console.log(`  ${l}: no dub or CC beside the compilation, title and description only`);
  }
  if (langs.length) console.log(`  languages: ${langs.map(({ l }) => l).join(", ")}`);
  console.log(meta.slug, "|", meta.title);
}
