// node sb.mjs <ep> <header.md> <footer.md>: writes docs/videos/zhong-tian-qu-qi-e0<ep>/storyboard.md
import { readFileSync, writeFileSync } from "node:fs";
const REPO = "/home/user/travel_scanner";
const SCR = decodeURIComponent(new URL('.', import.meta.url).pathname).replace(/\/$/, '');
const { normalize } = await import(`${REPO}/tools/video/core/craft.mjs`);
const [ep, headerFile, footerFile] = process.argv.slice(2);
const dir = `${REPO}/docs/videos/zhong-tian-qu-qi-e0${ep}`;
const v = JSON.parse(readFileSync(`${dir}/video.json`, "utf8"));
const ov = JSON.parse(readFileSync(`${dir}/overlays.json`, "utf8"));
const zh = Object.fromEntries(JSON.parse(readFileSync(`${SCR}/zh-e0${ep}.json`, "utf8")).map((r) => [r.id, r]));
const names = Object.fromEntries(v.characters.map((c) => [c.id, c.name]));
const shots = normalize(v).shots;
let t = 0;
const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
const rows = [];
v.scenes.forEach((sc, i) => {
  const sec = shots[i].seconds;
  if (sc.chapter) rows.push(`| **${sc.chapter}** |||||||`);
  const lines = sc.lines.length ? sc.lines.map((l) => `${names[l.speaker]}${sc.data.characters.includes(l.speaker) ? "" : "（畫外）"}：${l.text}`).join("<br>") : "—";
  const panel = ov[sc.id] ? ov[sc.id].map((o) => `${o.text}（${o.kind}）`).join("<br>") : "—";
  const desc = zh[sc.id].zh + (sc.lines.length ? "" : (zh[sc.id].zh.includes("無台詞") ? "" : "（無台詞）"));
  rows.push(`| ${sc.id} | ${mmss(t)} | ${sec.toFixed(1)} | ${zh[sc.id].kind} | ${sc.data.camera} | ${desc} | ${lines} | ${panel} |`);
  t += sec;
});
const head = readFileSync(headerFile, "utf8").trimEnd();
const foot = readFileSync(footerFile, "utf8").trimEnd();
const out = `${head}\n\n| 鏡 | 開始 | 秒 | 種類 | 景別、運鏡 | 畫面 | 台詞 | 面板（overlays） |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n${rows.join("\n")}\n\n${foot}\n`;
writeFileSync(`${dir}/storyboard.md`, out);
console.log("total", t.toFixed(1), "s");
// print starts for writing brief
v.scenes.forEach((sc, i) => {});
let a = 0; console.log(v.scenes.map((sc, i) => { const r = `${sc.id}@${mmss(a)}`; a += shots[i].seconds; return r; }).join(" "));
