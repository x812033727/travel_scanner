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
  "claims.md": "db0457996d4a99337e56c5b763986e1621286b258eeec1bbac9c0d1668b47aa9",
  "video.json": "c3464296eea71e0e65d93dc52340bec4720a8c4c9eb55e5db10e837070955d8b",
  "script.md": "eff9457c6d99f680b4dc5d17b10f2ec5f68504f905631590bfb0e333b3e548b9",
};
const ballotHashes = {
  a: "3c1dff64fbb86ac35caac8b8461604857acf13ca2b3b2a16dff76689ac956113",
  b: "6624b76182f9931e8849276994299cf388e77d76a1ac31f7b309e92ff64487f8",
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R11 creative SHA drift before transcription");
const script = readFileSync(join(episode, "script.md"), "utf8");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r11-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  const answers = reader === "a"
    ? JSON.parse(raw.toString("utf8")).answers
    : [...raw.toString("utf8").matchAll(/^\|\s*\d+\s*\|\s*`([a-z_]+)`\s*\|\s*\*{0,2}(YES|NO)\*{0,2}\s*\|\s*(.*?)\s*\|$/gm)].map((row) => {
      const cited = [...row[3].matchAll(/\b(s\d{5})\b/g)].map((match) => match[1]);
      if (!cited.length || cited.some((id) => !lines.has(id))) throw new Error(`reader b evidence missing/invalid for ${row[1]}`);
      const ids = row[1] === "no_recap" ? ["s58090", "s58108"] : [cited[0]];
      return { id: row[1], yes: row[2] === "YES", evidence: ids.map((id) => `[${id}] ${lines.get(id)}`).join("；") };
    });
  if (answers.length !== 13 || answers.some((answer, i) => answer.id !== NARRATIVE_PANEL[i].id || typeof answer.yes !== "boolean")) throw new Error(`reader ${reader} panel mismatch: ${answers.length}`);
  for (const answer of answers) {
    const cited = [...answer.evidence.matchAll(/\b(s\d{5})\b/g)].map((match) => match[1]);
    if (!cited.length || cited.some((id) => !lines.has(id) || !answer.evidence.includes(lines.get(id)) || !script.includes(lines.get(id)))) throw new Error(`reader ${reader} exact spoken evidence missing/invalid for ${answer.id}`);
  }
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r11-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((answer) => answer.yes).length, no: answers.filter((answer) => !answer.yes).map((answer) => answer.id), answers });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R11", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((answer) => answer.yes).length, failed: merged.failed.map((answer) => answer.id), advisory: merged.advisory.map((answer) => answer.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (!merged.passed || audit.merged.yes !== 13 || audit.merged.failed.length || audit.merged.advisory.length) throw new Error("unexpected R11 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
