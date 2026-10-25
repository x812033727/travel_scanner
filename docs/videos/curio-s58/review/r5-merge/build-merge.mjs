import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const expected = {
  "research.md": "1f6adc58345a10655a0bfdf66c87d5337cbd87c8271f41cb4878204bf4e5d5d0",
  "brief.md": "fbffce22c2eff5052a4050b06b121e3fc8a62b7ab350ecfd6a150f5788214362",
  "claims.md": "67ed990038429d6186487e1f16504ebf3e982d2b8d7c591c75b7c58faf8cceef",
  "video.json": "1be17b85b1b41cb1f5e0f9fe21d18c758ef096447cb4c776c5dcba1ba79dda22",
  "script.md": "ce03aeae00241c3e178897ea35a4469c697abaddbb268061fd0574eed0dc35e0",
};
const ballotHashes = {
  a: "19746ef5547ffb2de58f2ddb0ed522e5305b7b4fd8e976d43a95a2996361c097",
  b: "bd368236f51c2f4052c4eacd3598dae9f577dab474abfeca3971904cfc492c41",
};
const chosen = {
  a: ["s58001", "s58005", "s58031", "s58005", "s58108", "s58013", "s58140", "s58123", "s58056", "s58146", "s58005", "s58021", "s58057"],
  b: ["s58001", "s58005", "s58031", "s58055", "s58108", "s58013", "s58143", "s58146", "s58056", "s58146", "s58005", "s58021", "s58057"],
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R5 creative SHA drift before transcription");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r5-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  // Reader B uses a numbered column and bold verdicts.
  const parsed = [...raw.toString("utf8").matchAll(/^\|\s*(?:\d+\s*\|\s*)?`([a-z_]+)`\s*\|\s*\*{0,2}(YES|NO)\*{0,2}\s*\|\s*(.*?)\s*\|$/gm)];
  if (parsed.length !== 13 || parsed.some((row, i) => row[1] !== NARRATIVE_PANEL[i].id)) throw new Error(`reader ${reader} panel row/order mismatch: ${parsed.length}`);
  const answers = parsed.map((row, i) => {
    const id = chosen[reader][i];
    if (!lines.has(id)) throw new Error(`unknown line ${id}`);
    return { id: row[1], yes: row[2] === "YES", evidence: `[${id}] ${lines.get(id)}` };
  });
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r5-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((a) => a.yes).length, no: answers.filter((a) => !a.yes).map((a) => a.id), citations: parsed.map((row, i) => ({ id: row[1], vote: row[2], quoted_id: chosen[reader][i], quoted_line: lines.get(chosen[reader][i]), original_reason_mentions_id: row[3].includes(chosen[reader][i]), original_reason: row[3] })) });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R5", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((a) => a.yes).length, failed: merged.failed.map((a) => a.id), advisory: merged.advisory.map((a) => a.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (!merged.passed || audit.merged.yes !== 13 || audit.merged.failed.length !== 0 || audit.merged.advisory.length !== 0) throw new Error("unexpected R5 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
