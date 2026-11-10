import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const expected = {
  "research.md": "8a1db1dc2a9441a7b16683c70067203ddc7be6c0070560f32c02d91b5e32de34",
  "brief.md": "7b44818f6b681a4ee786c00a32359b4181772aeaa1b5cd897bcd13871b1ad016",
  "claims.md": "73f9ea7122ec728357b7eb3c8487b9657b4bbe0e6d140c4b0514a7deddc2d471",
  "video.json": "d69ce07f441aeabddc231d4d98fe4437ffea4e7c763198d2a61be1161bebe0cb",
  "script.md": "9d590c8c3e6f93628d87d4618276ee967364aa36e0b54c7008c9266b6daae0ac",
};
const ballotHashes = {
  a: "9ad26823d4360c49212f14d5b2f05c7ba7783269dd03ab6f893e43a209d29bc9",
  b: "9ed2f8a7d5d2f35def56aedf04da388c9fdf1c02f4555c59d7c710e541ab18a4",
};
const chosen = {
  a: ["s58001", "s58005", "s58041", "s58104", "s58083", "s58070", "s58049", "s58041", "s58114", "s58156", "s58008", "s58030", "s58071"],
  b: ["s58001", "s58005", "s58041", "s58034", "s58083", "s58016", "s58049", "s58041", "s58114", "s58156", "s58008", "s58155", "s58105"],
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R2 creative SHA drift before transcription");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r2-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  const rows = [...raw.toString("utf8").matchAll(/^\| (?:\d+ )?`([a-z_]+)` \| \*\*?(YES|NO)\*\*? \| (.*?) \|$/gm)];
  // A uses bold judgments; B uses plain judgments. Accept both explicitly.
  const plainRows = [...raw.toString("utf8").matchAll(/^\| (?:\d+ )?`([a-z_]+)` \| (YES|NO) \| (.*?) \|$/gm)];
  const parsed = rows.length === 13 ? rows : plainRows;
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
  ballots.push({ reader, original_path: `../r2-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((a) => a.yes).length, no: answers.filter((a) => !a.yes).map((a) => a.id), citations: parsed.map((row, i) => ({ id: row[1], vote: row[2], quoted_id: chosen[reader][i], quoted_line: lines.get(chosen[reader][i]), original_reason_mentions_id: row[3].includes(chosen[reader][i]), original_reason: row[3] })) });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R2", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((a) => a.yes).length, failed: merged.failed.map((a) => a.id), advisory: merged.advisory.map((a) => a.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 8 || audit.merged.failed.join(",") !== "no_spoiler,one_line,payoffs,no_recap,no_detour") throw new Error("unexpected R2 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
