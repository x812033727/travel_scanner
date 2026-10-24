// Deterministic, offline C09 v8 promotion check. This is not a host-worker guard:
// the series must stay paused until a separately reviewed worker handoff exists.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { parseScript } from "../../../tools/video/review/script-intake.mjs";
import { textHash } from "../../../tools/video/core/schema.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const SHA = Object.freeze({
  script: "4445ad74bcafbac1dfca65392199fec89700c17ab8c01e665ac79dfffc1aa3f7",
  visual: "2235ea304c240e78f6473183e45a63502500ee20f931107843c6af3c5ad0bf5a",
  narration: "0e813642e36e7524d55f982bf26d646a1361658deffa5310fe6991c7a0a258ad",
});
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const file = (name) => path.join(dir, name);
const read = (name) => readFileSync(file(name));
const parse = (name) => JSON.parse(read(name).toString("utf8"));

function frozenInputs() {
  const scriptBytes = read("script.md");
  const candidateBytes = read("reviews/visual-plan-v8-candidate-2235ea30.json");
  const visualBytes = read("visual-plan.json");
  const narratorBytes = read("reviews/narrator-only-v8-0e813642.txt");
  assert.equal(sha(scriptBytes), SHA.script, "canonical script differs from owner-approved bytes");
  assert.equal(sha(candidateBytes), SHA.visual, "reviewed visual candidate changed");
  assert.equal(sha(visualBytes), SHA.visual, "canonical visual plan differs from reviewed candidate");
  assert.equal(sha(narratorBytes), SHA.narration, "narration-only blind input changed");

  const script = parseScript(scriptBytes.toString("utf8"), "C09");
  const visual = JSON.parse(candidateBytes.toString("utf8"));
  const series = parse("series.json");
  assert.equal(script.length, 77);
  assert.equal(visual.scenes.length, 77);
  assert.equal(visual.chapters.length, 6);
  assert.equal(visual.script_sha256.toLowerCase(), SHA.script);
  assert.equal(visual.narration_projection_sha256.toLowerCase(), SHA.narration);
  assert.deepEqual(visual.look, { preset: "cute-mystery" });
  assert.equal(series.kind, "story");
  assert.equal(series.slug, "brand-stories-everyday-reversals");
  assert.equal(series.episode, 9);
  assert.deepEqual(series.look, { preset: "cute-mystery" });

  const ids = new Set();
  const sceneIds = new Set();
  const firstIds = new Set(visual.chapters.map(({ first_id }) => first_id));
  assert.equal(firstIds.size, 6);
  let shots = 0;
  let cards = 0;
  let cardRun = 0;
  let maxCardRun = 0;
  for (let index = 0; index < script.length; index++) {
    const narration = script[index].lines[0];
    const scene = visual.scenes[index];
    assert.equal(scene.lines.length, 1, `scene ${index + 1} has multiple lines`);
    assert.equal(scene.lines[0].id, narration.id, `line ID drift at scene ${index + 1}`);
    assert.equal(scene.lines[0].text, narration.text, `narration text drift at ${narration.id}`);
    assert.ok(!ids.has(narration.id) && !sceneIds.has(scene.id), `duplicate scene or line ${narration.id}`);
    ids.add(narration.id);
    sceneIds.add(scene.id);
    if (scene.template === "shot") {
      assert.ok(typeof scene.data.prompt === "string" && scene.data.prompt.trim(), `empty prompt at ${narration.id}`);
      assert.equal(scene.data.visual, "still");
      shots++;
      cardRun = 0;
    } else {
      assert.equal(scene.template, "stats", `unsupported card at ${narration.id}`);
      assert.equal(scene.data.stats.length, 1, `stats card has multiple claims at ${narration.id}`);
      cards++;
      cardRun++;
      maxCardRun = Math.max(maxCardRun, cardRun);
    }
  }
  assert.equal(shots, 67);
  assert.equal(cards, 10);
  assert.ok(maxCardRun <= 2);
  for (const { first_id, title } of visual.chapters) {
    const index = script.findIndex((scene) => scene.lines[0].id === first_id);
    assert.ok(index >= 0 && script[index].chapter.endsWith(title), `chapter drift at ${first_id}`);
  }
  return { visual, series, firstIds, shots, cards, maxCardRun };
}

function machineProject({ visual, series, firstIds }) {
  // These are pronunciation-only candidates. Visible text, CC and source-bound
  // narration stay exactly as approved; actual audio remains a separate gate.
  const spokenNames = new Map([
    ["c090102", ["Patagonia", "巴塔哥尼亞"]],
    ["c090609", ["Patagonia", "巴塔哥尼亞"]],
    ["c090214", ["Ventura", "文圖拉"]],
    ["c090601", ["Ventura", "文圖拉"]],
  ]);
  // Visible, postproduction-only copy. The reviewed candidate and its factual
  // value/label remain frozen; source codes and editorial notes stay in the
  // source matrix and this mapping's review receipt, not on screen.
  const cardCopy = new Map([
    ["c09-p01-s02", ["當時的器材公司", "1972 年型錄前言、品牌回顧"]],
    ["c09-p02-s06", ["從鐵砧開始", "1977 年刊出採訪中的本人回憶"]],
    ["c09-p02-s09", ["最初的鍛造速度", "1977 年刊出採訪中的本人回憶"]],
    ["c09-p02-s10", ["本人回憶的售價", "1977 年刊出採訪中的本人回憶"]],
    ["c09-p03-s02", ["反覆敲拔的例子", "1967 年器材文章的例子"]],
    ["c09-p03-s17", ["型錄改寫建議", "1972 年型錄前言（後來重刊）"]],
    ["c09-p04-s03", ["仍有必要例外", "1972 年型錄前言（後來重刊）"]],
    ["c09-p04-s04", ["固定岩釘留紀錄", "1972 年型錄前言（後來重刊）"]],
    ["c09-p05-s10", ["一次攀登的回顧", "1977 年刊出報導的事後回顧"]],
    ["c09-p06-s01", ["報導發表年", "1977 年刊出報導"]],
  ]);
  assert.equal(cardCopy.size, 10);
  const loops = [
    ["c090103", "c090316", "為何勸顧客少用岩釘"],
    ["c090105", "c090611", "自家岩釘如何從首選變例外"],
    ["c090216", "c090304", "反覆敲拔的岩縫留下什麼"],
    ["c090310", "c090312", "有沒有少用錘子的替代器材"],
    ["c090322", "c090408", "型錄如何教顧客換器材"],
    ["c090416", "c090507", "賣岩釘者勸人克制是否可信"],
    ["c090503", "c090511", "不帶岩釘能否完成長路線"],
    ["c090515", "c090603", "岩釘後來是否仍在工廠生產"],
  ].map(([setup, payoff, what]) => ({ setup, payoff, what }));
  const sources = [
    ["Chouinard／Frost，1967 年器材文章", "https://publications.americanalpineclub.org/articles/12196733400/On-New-Rock-Climbing-Equipment-and-Its-Use"],
    ["Chouinard／Frost，1972 年型錄前言全文重刊", "https://www.patagonia.com/stories/sports/climbing/a-word/story-116598.html"],
    ["Rowell，1973 年型錄書評", "https://publications.americanalpineclub.org/articles/12197352200/Chouinard-Equipment"],
    ["Bernstein，1977 年刊出採訪", "https://www.newyorker.com/magazine/1977/01/31/ascending"],
    ["Patagonia，2012 年公司史回顧", "https://www.patagonia.com/stories/culture/community/patagonia-surf-stores-the-wave-riding-collective/story-18439.html"],
  ].map(([title, url]) => ({ title, url, checked_on: "2026-10-24" }));
  return {
    schema_version: 1,
    slug: "story-everyday-patagonia-c09",
    format: "drama",
    category: "explainer",
    narration_locale: "zh-TW",
    target_minutes: [9, 11],
    voice: { provider: "gemini", name: "Sulafat", style: "標準國語，咬字清楚，台北日常說話語調。像對朋友講一樁真實品牌奇聞；日期、器材限制與來源歸因放慢，章末問題留半拍。" },
    subtitles: { burn_in: false },
    look: { preset: "cute-mystery" },
    characters: [],
    series: { slug: series.slug, episode: series.episode, chapter: 1 },
    music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 },
    loops,
    youtube: {
      category_id: 27, made_for_kids: false, default_language: "zh-TW",
      title: "Patagonia 創辦人，為何勸人少用自家岩釘？｜品牌故事",
      description: "1972 年的 Chouinard Equipment 型錄，勸攀岩者在合適路線優先考慮可拆式楔塊，但保留必要時岩釘的例外。沿著早期鍛造、岩縫傷痕、型錄爭論與後來的工廠報導，看這個建議改變了什麼。1977 年只指採訪刊年；插圖是匿名概念示意，不重建真人、真實路線或型錄原頁。資料查核日期：2026-10-24。",
      tags: ["Patagonia", "岩釘", "攀岩", "品牌故事", "日用品的意外轉身"],
      video_id: null,
    },
    thumbnail: { template: "thumb", data: { headline: "岩釘\n變例外？", tag: "品牌故事", brand: "PATAGONIA", shot: visual.scenes.find((scene) => scene.template === "shot").id } },
    sources,
    assets: [],
    scenes: visual.scenes.map((scene) => {
      const line = scene.lines[0];
      const pronunciation = spokenNames.get(line.id);
      if (pronunciation) assert.ok(line.text.includes(pronunciation[0]), `pronunciation input changed at ${line.id}`);
      const machineLine = pronunciation ? { ...line, say: line.text.replace(pronunciation[0], pronunciation[1]), say_for: textHash(line.text) } : line;
      const visibleCopy = cardCopy.get(scene.id);
      assert.equal(Boolean(visibleCopy), scene.template === "stats", `postproduction card copy drift at ${scene.id}`);
      const data = visibleCopy ? { ...scene.data, title: visibleCopy[0], source: visibleCopy[1] } : scene.data;
      return {
        id: scene.id,
        ...(firstIds.has(line.id) ? { chapter: scene.chapter } : {}),
        template: scene.template,
        data,
        lines: [machineLine],
      };
    }),
  };
}

const inputs = frozenInputs();
const project = machineProject(inputs);
const projectPath = file("video.json");
if (process.argv.length === 3 && process.argv[2] === "--write") {
  writeFileSync(projectPath, `${JSON.stringify(project, null, 2)}\n`);
} else {
  assert.equal(process.argv.length, 2, "usage: node preflight-v8.mjs [--write]");
  assert.deepEqual(parse("video.json"), project, "video.json differs from frozen v8 project");
}
console.log(JSON.stringify({ slug: project.slug, lines: project.scenes.length, shots: inputs.shots, cards: inputs.cards, maxCardRun: inputs.maxCardRun, script_sha256: SHA.script, visual_sha256: SHA.visual, project_sha256: sha(readFileSync(projectPath)) }));
