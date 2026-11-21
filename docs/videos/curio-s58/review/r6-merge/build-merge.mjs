import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const expected = {
  "research.md": "b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e",
  "brief.md": "5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f",
  "claims.md": "f69dace9c1bc7434564da46fbcd74146a453a3bf253781dacfd86bec254f3ccd",
  "video.json": "0ece21cb763b15b9ce2d2cc96d363c789c5f1021bd9a52856d17c0119b51b37b",
  "script.md": "c1e6e201108663a6c3af9c7c96e56ad07e3fe73b60e4f13f017c8d044aeaec10",
};
const ballotHashes = {
  a: "2e4379e20da083aac73cac486463095ec97cbd098af798094c61a8f58b50e004",
  b: "ab83968096b5f23ed805ad690538454c5a7658ee33efcb09bfb3da2d3ac90cd2",
};
const chosen = {
  a: ["s58001", "s58005", "s58031", "s58005", "s58108", "s58013", "s58140", "s58068", "s58056", "s58146", "s58005", "s58021", "s58057"],
  b: ["s58001", "s58005", "s58031", "s58055", "s58108", "s58013", "s58143", "s58124", "s58056", "s58146", "s58005", "s58021", "s58057"],
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R6 creative SHA drift before transcription");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r6-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  // Reader B uses a numbered column and bold verdicts.
  const parsed = [...raw.toString("utf8").matchAll(/^\|\s*(?:\d+\s*\|\s*)?`([a-z_]+)`\s*\|\s*\*{0,2}(YES|NO)\*{0,2}\s*\|\s*(.*?)\s*\|$/gm)];
  if (parsed.length !== 13 || parsed.some((row, i) => row[1] !== NARRATIVE_PANEL[i].id)) throw new Error(`reader ${reader} panel row/order mismatch: ${parsed.length}`);
  const answers = parsed.map((row, i) => {
    const id = chosen[reader][i];
    if (!lines.has(id)) throw new Error(`unknown line ${id}`);
    const evidence = row[1] === "no_recap" ? (reader === "a" ? `[s58067] ${lines.get("s58067")}；[s58068] ${lines.get("s58068")}` : `[s58087] ${lines.get("s58087")}；[s58124] ${lines.get("s58124")}`) : `[${id}] ${lines.get(id)}`;
    return { id: row[1], yes: row[2] === "YES", evidence };
  });
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r6-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((a) => a.yes).length, no: answers.filter((a) => !a.yes).map((a) => a.id), citations: parsed.map((row, i) => ({ id: row[1], vote: row[2], quoted_id: chosen[reader][i], quoted_line: lines.get(chosen[reader][i]), original_reason_mentions_id: row[3].includes(chosen[reader][i]), original_reason: row[3] })) });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R6", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((a) => a.yes).length, failed: merged.failed.map((a) => a.id), advisory: merged.advisory.map((a) => a.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 12 || audit.merged.failed.join(",") !== "no_recap" || audit.merged.advisory.length !== 0) throw new Error("unexpected R6 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
