#!/usr/bin/env node
// Story-plan review for comedy shorts and dramas (.agents/skills/animation-preproduction/references/comedy-review.md).
// Offline: it never calls a model. `packet` writes what a blind judge reads (the shots, the lines,
// the sound cues; no brief, no intent); `score` reads the judges' JSON and decides whether the plan
// may go on to the script gate. Exit codes: 0 passed, 1 failed (revise and judge again), 2 usage
// or a judge file that does not follow the schema.
import { readFileSync, writeFileSync } from "node:fs";

/** The rubric: key → [maximum, what the judge scores]. Totals 100. */
export const RUBRIC = {
  hook: [15, "前 2 秒：第一格就有衝突或怪事，讓人不想滑走"],
  premise: [10, "一句話說得出的設定，一般人一看就有共鳴"],
  laughs: [20, "笑點密度：平均每 8–10 秒一個真的會笑的點，不是只有可愛"],
  escalation: [10, "情況一次比一次糟或荒謬，不是同一個笑點重複"],
  surprise: [15, "至少一個觀眾猜不到、但回頭看合理的反轉"],
  character: [10, "角色的反應與台詞有個性、具體，不是空泛的形容"],
  payoff: [10, "結尾收得有力，有重看或追下一集的理由"],
  share: [10, "看完會想轉給某個具體的人"],
};

/** Every gate must hold. Medians across judges; the strong-beat rule counts a beat a judge did not list as 1. */
export const GATES = {
  minJudges: 3,
  medianTotal: 80,
  everyJudgeTotal: 65,
  medianLaughs: 14,
  medianSurprise: 10,
  strongBeats: 3,
  strongBeatScore: 4,
};

export const MAX_ROUNDS = 3;

const median = (values) => {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};

/** Problems with one judge's answer; empty when it follows the schema. */
export function judgeProblems(judge, shotIds = null) {
  const problems = [];
  if (!judge || typeof judge !== "object") return ["must be a JSON object"];
  if (typeof judge.judge !== "string" || !judge.judge) problems.push("judge: a name for this reviewer");
  for (const [key, [max]] of Object.entries(RUBRIC)) {
    const value = judge.scores?.[key];
    if (!(Number.isInteger(value) && value >= 0 && value <= max)) problems.push(`scores.${key}: a whole number 0–${max}`);
  }
  if (!Array.isArray(judge.beats) || judge.beats.length === 0) problems.push("beats: the joke beats this judge found, [{shot, joke, funny 1–5}]");
  else
    judge.beats.forEach((beat, index) => {
      if (typeof beat?.shot !== "string" || (shotIds && !shotIds.has(beat.shot))) problems.push(`beats[${index}].shot: a shot id of the packet`);
      if (typeof beat?.joke !== "string" || !beat.joke) problems.push(`beats[${index}].joke: what the joke is`);
      if (!(Number.isInteger(beat?.funny) && beat.funny >= 1 && beat.funny <= 5)) problems.push(`beats[${index}].funny: 1–5`);
    });
  if (!Array.isArray(judge.fixes)) problems.push("fixes: concrete rewrites for the weakest parts (may be empty)");
  return problems;
}

const total = (judge) => Object.keys(RUBRIC).reduce((sum, key) => sum + judge.scores[key], 0);

/** The verdict over a round of judges. */
export function decide(judges) {
  const reasons = [];
  if (judges.length < GATES.minJudges) reasons.push(`needs at least ${GATES.minJudges} independent judges, got ${judges.length}`);
  const totals = judges.map(total);
  const axis = Object.fromEntries(Object.keys(RUBRIC).map((key) => [key, median(judges.map((j) => j.scores[key]))]));
  const medianTotal = median(totals);
  if (medianTotal < GATES.medianTotal) reasons.push(`median total ${medianTotal} < ${GATES.medianTotal}`);
  const low = judges.filter((j) => total(j) < GATES.everyJudgeTotal).map((j) => `${j.judge} ${total(j)}`);
  if (low.length) reasons.push(`a judge scored under ${GATES.everyJudgeTotal}: ${low.join(", ")}`);
  if (axis.laughs < GATES.medianLaughs) reasons.push(`laughs median ${axis.laughs}/20 < ${GATES.medianLaughs}: not enough real jokes`);
  if (axis.surprise < GATES.medianSurprise) reasons.push(`surprise median ${axis.surprise}/15 < ${GATES.medianSurprise}: the turn is predictable`);
  const shots = new Set(judges.flatMap((j) => j.beats.map((b) => b.shot)));
  const beats = [...shots]
    .map((shot) => {
      const scores = judges.map((j) => Math.max(1, ...j.beats.filter((b) => b.shot === shot).map((b) => b.funny)));
      const jokes = judges.flatMap((j) => j.beats.filter((b) => b.shot === shot).map((b) => b.joke));
      return { shot, median: median(scores), scores, joke: jokes[0] };
    })
    .sort((a, b) => b.median - a.median);
  const strong = beats.filter((b) => b.median >= GATES.strongBeatScore);
  if (strong.length < GATES.strongBeats) reasons.push(`${strong.length} beat(s) with a median of ${GATES.strongBeatScore}+ out of 5; needs ${GATES.strongBeats}`);
  const fixes = judges.flatMap((j) => j.fixes.map((fix) => `${j.judge}: ${fix}`));
  return { pass: reasons.length === 0, reasons, medianTotal, totals: Object.fromEntries(judges.map((j, i) => [j.judge, totals[i]])), axis, beats, fixes };
}

/** What a blind judge reads: the shots in order, their picture and action, lines and cues; no intent. */
export function packet(doc) {
  const names = Object.fromEntries((doc.characters ?? []).map((c) => [c.id, c.name]));
  const cues = new Map();
  for (const cue of doc.sfx?.cues ?? []) if (cue.scene) cues.set(cue.scene, [...(cues.get(cue.scene) ?? []), cue.sound]);
  const out = [`# ${doc.youtube?.title ?? doc.slug}`, "", "每一鏡依序：畫面（英文是給繪圖模型的描述）、畫面裡發生的事、台詞、音效。", ""];
  (doc.scenes ?? []).forEach((scene, index) => {
    const data = scene.data ?? {};
    out.push(`## ${index + 1}. ${scene.id}`);
    if (data.camera) out.push(`- 鏡頭：${data.camera}`);
    if (data.prompt) out.push(`- 畫面：${data.prompt}`);
    if (data.motion) out.push(`- 動作：${data.motion}`);
    if (scene.action_seconds) out.push(`- 無台詞，${scene.action_seconds} 秒`);
    for (const line of scene.lines ?? []) out.push(`- 【${names[line.speaker] ?? "旁白"}】${line.emotion ? `（${line.emotion}）` : ""}${line.text}`);
    if (cues.has(scene.id)) out.push(`- 音效（這一鏡開始時）：${cues.get(scene.id).join("、")}`);
    out.push("");
  });
  return out.join("\n");
}

function usage() {
  console.error(`usage:
  node comedy_review.mjs packet <video.json> [--out packet.md]
  node comedy_review.mjs score <video.json> <judge-a.json> <judge-b.json> <judge-c.json> ... [--out summary.json]`);
  return 2;
}

function main(argv) {
  const [command, file, ...rest] = argv;
  const outAt = rest.indexOf("--out");
  const out = outAt >= 0 ? rest[outAt + 1] : null;
  const files = outAt >= 0 ? rest.filter((_, i) => i !== outAt && i !== outAt + 1) : rest;
  if (!file || !["packet", "score"].includes(command)) return usage();
  const doc = JSON.parse(readFileSync(file, "utf8"));
  if (command === "packet") {
    const text = packet(doc);
    if (out) writeFileSync(out, text);
    else process.stdout.write(text);
    return 0;
  }
  const shotIds = new Set((doc.scenes ?? []).map((s) => s.id));
  const judges = [];
  for (const path of files) {
    const judge = JSON.parse(readFileSync(path, "utf8"));
    const problems = judgeProblems(judge, shotIds);
    if (problems.length) {
      console.error(`${path}:\n  ${problems.join("\n  ")}`);
      return 2;
    }
    judges.push(judge);
  }
  const verdict = decide(judges);
  console.log(`${verdict.pass ? "PASS" : "FAIL"}  median ${verdict.medianTotal}/100  (${Object.entries(verdict.totals).map(([k, v]) => `${k} ${v}`).join(", ")})`);
  for (const [key, [max, what]] of Object.entries(RUBRIC)) console.log(`  ${key.padEnd(10)} ${String(verdict.axis[key]).padStart(4)}/${max}  ${what}`);
  console.log("beats (median of 5):");
  for (const beat of verdict.beats) console.log(`  ${String(beat.median).padStart(3)}  ${beat.shot}  ${beat.joke}`);
  for (const reason of verdict.reasons) console.log(`FAIL ${reason}`);
  if (out) writeFileSync(out, `${JSON.stringify({ ...verdict, gates: GATES, judges: files }, null, 2)}\n`);
  return verdict.pass ? 0 : 1;
}

if (import.meta.url === `file://${process.argv[1]}`) process.exitCode = main(process.argv.slice(2));
