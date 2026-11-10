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
  "claims.md": "4dc0fdf5c0ee1ce70d78e77e125a83afaf2b3f52fb5d474bb5e3594aa887b503",
  "video.json": "f5ffe0868a570ab86b993cbdbe69014922b7447f078626e2c7294d531c21bbef",
  "script.md": "37dbc104268814e5cc9db7ac72f13a537b2007e9e71c4c219c1252c4a2d7d3f0",
};
const ballotHashes = {
  a: "f1468b81333b1605a0b37f53f13936ab6f0a12863f4eba95ff88730393d3754f",
  b: "fe89c2808e611069e6d7ea5adcc039a7f964964234c76b471daffa1b52cd4592",
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R10 creative SHA drift before transcription");
const script = readFileSync(join(episode, "script.md"), "utf8");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r10-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  const parsed = reader === "a"
    ? [...raw.toString("utf8").matchAll(/^\d+\.\s+\*\*`([a-z_]+)`\s+—\s+(YES|NO)\.\*\*\s*(.*)$/gm)]
    : [...raw.toString("utf8").matchAll(/^\|\s*`([a-z_]+)`\s*\|\s*\*{0,2}(YES|NO)\*{0,2}\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$/gm)];
  if (parsed.length !== 13 || parsed.some((row, i) => row[1] !== NARRATIVE_PANEL[i].id)) throw new Error(`reader ${reader} panel mismatch: ${parsed.length}`);
  const answers = parsed.map((row) => {
    const reason = reader === "a" ? row[3] : `${row[3]} ${row[4]}`;
    const cited = [...reason.matchAll(/\b(s\d{5})\b/g)].map((match) => match[1]);
    if (!cited.length || cited.some((id) => !lines.has(id) || !script.includes(lines.get(id)))) throw new Error(`reader ${reader} evidence missing or invalid for ${row[1]}`);
    let evidence = `[${cited[0]}] ${lines.get(cited[0])}`;
    if (row[1] === "no_recap") evidence = ["s58053", "s58055"].map((id) => `[${id}] ${lines.get(id)}`).join("；");
    if (reader === "b" && row[1] === "one_line") evidence = ["s58143", "s58144"].map((id) => `[${id}] ${lines.get(id)}`).join("；");
    return { id: row[1], yes: row[2] === "YES", evidence };
  });
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r10-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((answer) => answer.yes).length, no: answers.filter((answer) => !answer.yes).map((answer) => answer.id), answers });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R10", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((answer) => answer.yes).length, failed: merged.failed.map((answer) => answer.id), advisory: merged.advisory.map((answer) => answer.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 12 || audit.merged.failed.join(",") !== "no_recap" || audit.merged.advisory.length) throw new Error("unexpected R10 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
