import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const expected = {
  "research.md": "f3ab0acd1e0bbf4124b7897b07604897d38068095a72530a2e2071e4b968f566",
  "brief.md": "c03bd176667ff1ca5180f5f9591869f1e8e58ca7e7454fa8d723913c7a3ed133",
  "claims.md": "e221beb8befe971381ef306aa89433f37021cbb88e3692f6c51409568211083a",
  "video.json": "e780262318e4b6860637a173c07258d7b3019e0d077200aabc35d8b6b1fc0e54",
  "script.md": "c61844a2e079285b8ad98a150e7ac49fa03dca9939dab10a81748fabcf4336d5",
};
const ballotHashes = {
  a: "9b8e1af4a52a29355ab248537a21963c9882cf32707543bdad0b98335e5c854b",
  b: "635aa75586d59e743e0c0490f384f60b66d3cdccb90f11fcbbbe4a8f38904280",
};
const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R1 creative SHA drift before transcription");
const scenes = JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes;
const find = (prefix) => {
  const hits = scenes.filter((scene) => scene.lines[0].text.startsWith(prefix));
  if (hits.length !== 1) throw new Error(`expected one line for ${prefix}; got ${hits.length}`);
  return hits[0];
};
const chosenPrefixes = [
  "一八七八年三月十一日", "一個沒有練過的人", "開場那天，杜蒙塞爾", "會場那個難題",
  "開場那張草圖", "那時重播的是點和劃", "他寫這聲音略顯細弱", "手搖的速度若變了",
  "開場輪到杜蒙塞爾", "原始資料和頻道連結", "愛迪生後來提到一張十八美元",
  "這隻手轉出的人聲", "人愈來愈多",
];
if (chosenPrefixes.length !== NARRATIVE_PANEL.length) throw new Error("scene choice count mismatch");
const chosen = chosenPrefixes.map(find);
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r1-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  const regex = reader === "a"
    ? /^\| `([a-z_]+)` \| (YES|NO) \| (.*?) \|$/gm
    : /^\| \d+ \| `([a-z_]+)` \| \*\*(YES|NO)\*\* \| (.*?) \|$/gm;
  const parsed = [...raw.toString("utf8").matchAll(regex)];
  if (parsed.length !== 13 || parsed.some((row, i) => row[1] !== NARRATIVE_PANEL[i].id)) throw new Error(`reader ${reader} panel row/order mismatch: ${parsed.length}`);
  const answers = parsed.map((row, i) => ({ id: row[1], yes: row[2] === "YES", evidence: `[${chosen[i].id}] ${chosen[i].lines[0].text}` }));
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r1-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((a) => a.yes).length, no: answers.filter((a) => !a.yes).map((a) => a.id), citations: parsed.map((row, i) => ({ id: row[1], vote: row[2], quoted_id: chosen[i].id, quoted_line: chosen[i].lines[0].text, original_reason: row[3] })) });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
writeFileSync(join(here, "merged-answers.json"), `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s59", round: "R1", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(join(here, "merged-answers.json"))), merged: { passed: merged.passed, yes: merged.answers.filter((a) => a.yes).length, failed: merged.failed.map((a) => a.id), advisory: merged.advisory.map((a) => a.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 11 || audit.merged.failed.join(",") !== "payoffs,no_recap") throw new Error("unexpected R1 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
