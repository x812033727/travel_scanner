import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const expected = {
  "research.md": "27bebfb771aa8a901cf69528fb23401d351dcc35bdf584ab5e70c2163bfa0ea7",
  "brief.md": "49a1bd7cf68e2db074cc128bd08f60739da9ce85f63aa1ba4f7abab9f044e0d4",
  "claims.md": "73dcedbcbf30d5abd2db92fd34b789718e61938e8b4a86fe528d109851d332ec",
  "video.json": "7283ea2a7e444e2e58e83bb52a40da9548a1dddc1c2d74740971100f33936c48",
  "script.md": "6fd7c0585ebb1a47f518d70d769a1094deb54dc90404362df0ce0ed821ef1816",
};
const ballotHashes = {
  a: "568b28a0e0501f02420d5d83c1a00c93c6019a66858ab10e4629dfd7fba3ee9a",
  b: "91c1f5019202cb827291bf1522764a455c8a57defae3011de64ee5041693efbc",
};
const chosen = {
  a: ["s58001", "s58005", "s58031", "s58005", "s58033", "s58013", "s58025", "s58131", "s58080", "s58142", "s58005", "s58021", "s58055"],
  b: ["s58001", "s58005", "s58031", "s58033", "s58033", "s58013", "s58025", "s58042", "s58080", "s58146", "s58005", "s58021", "s58055"],
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R3 creative SHA drift before transcription");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r3-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  // The two raw ballots differ only in whether they include a numbered column.
  const parsed = [...raw.toString("utf8").matchAll(/^\|\s*(?:\d+\s*\|\s*)?`([a-z_]+)`\s*\|\s*(YES|NO)\s*\|\s*(.*?)\s*\|$/gm)];
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
  ballots.push({ reader, original_path: `../r3-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((a) => a.yes).length, no: answers.filter((a) => !a.yes).map((a) => a.id), citations: parsed.map((row, i) => ({ id: row[1], vote: row[2], quoted_id: chosen[reader][i], quoted_line: lines.get(chosen[reader][i]), original_reason_mentions_id: row[3].includes(chosen[reader][i]), original_reason: row[3] })) });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R3", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((a) => a.yes).length, failed: merged.failed.map((a) => a.id), advisory: merged.advisory.map((a) => a.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 11 || audit.merged.failed.join(",") !== "no_recap,no_detour") throw new Error("unexpected R3 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
