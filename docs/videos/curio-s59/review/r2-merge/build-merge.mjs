import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const expected = {
  "research.md": "ad5baec33ae786da9d103eecadca9f16c9f23f00d4041bde158e1e2697958efb",
  "brief.md": "90024cd567cb540e92fe9d58815cb36a0d05ade7a6739ec6851a54d6d5d10b80",
  "claims.md": "b84f891c58a937cd9fd2cfffc2aab0f14c0c652fee838f6a79bfca2b40e99bc5",
  "video.json": "26844c8610bd399077be2f349b3c548168c5021d6c143a88610ca8138d16a435",
  "script.md": "c74ea14ea53d7442b59d2232fd867b1ce7794aae4b2878337b693fe25a3e78a3",
};
const ballotHashes = {
  a: "5dcb6fc982e4658d52f0105dd2c1230c6f6ea0c291d0075be843b2521c1e5e02",
  b: "e9d86cef82821b11e8a1830614efabc7428eedf562190cc627800b2dd9212bd1",
};
const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R2 creative SHA drift before transcription");
const scenes = JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes;
const find = (prefix) => {
  const hits = scenes.filter((scene) => scene.lines[0].text.startsWith(prefix));
  if (hits.length !== 1) throw new Error(`expected one line for ${prefix}; got ${hits.length}`);
  return hits[0];
};
const chosenPrefixes = [
  "一八七八年三月十一日", "一個沒有練過的人", "開場那天，杜蒙塞爾", "電報紙盤轉過壓針",
  "開場那張草圖", "可那個接點只會", "他寫這聲音略顯細弱", "但「他試失敗」",
  "開場輪到杜蒙塞爾", "原始資料和頻道連結", "愛迪生後來提到一張十八美元",
  "這隻手轉出的人聲", "他說回放聲傳遍編輯室",
];
if (chosenPrefixes.length !== NARRATIVE_PANEL.length) throw new Error("scene choice count mismatch");
const chosen = chosenPrefixes.map(find);
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r2-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  const regex = /^\|\s*(?:\d+\s*\|\s*)?`([a-z_]+)`\s*\|\s*(?:\*\*)?(YES|NO)(?:\*\*)?\s*\|\s*(.*?)\s*\|$/gm;
  const parsed = [...raw.toString("utf8").matchAll(regex)];
  if (parsed.length !== 13 || parsed.some((row, i) => row[1] !== NARRATIVE_PANEL[i].id)) throw new Error(`reader ${reader} panel row/order mismatch: ${parsed.length}`);
  const selected = chosen.map((scene, i) => reader === "b" && NARRATIVE_PANEL[i].id === "no_recap" ? find("紙盤留下的是點和劃") : scene);
  const answers = parsed.map((row, i) => ({ id: row[1], yes: row[2] === "YES", evidence: `[${selected[i].id}] ${selected[i].lines[0].text}` }));
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r2-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((a) => a.yes).length, no: answers.filter((a) => !a.yes).map((a) => a.id), citations: parsed.map((row, i) => ({ id: row[1], vote: row[2], quoted_id: selected[i].id, quoted_line: selected[i].lines[0].text, original_reason: row[3] })) });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
writeFileSync(join(here, "merged-answers.json"), `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s59", round: "R2", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(join(here, "merged-answers.json"))), merged: { passed: merged.passed, yes: merged.answers.filter((a) => a.yes).length, failed: merged.failed.map((a) => a.id), advisory: merged.advisory.map((a) => a.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 12 || audit.merged.failed.join(",") !== "no_recap") throw new Error("unexpected R2 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
