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
  "claims.md": "35c33785728e092c6f4d4a22c9076f05cee92b7bdde36ca2563cad2db0fb142b",
  "video.json": "b392e57b9056df90ccda3242b95ca659aaa0395348b8c0c2210984fe885e3924",
  "script.md": "d9bd044c1261ab76f3ad32a098e8c50aadfc05473d223aac3d61a621223afd6d",
};
const ballotHashes = {
  a: "24f1d8da3305f6d977a33f7a2bf6936f791a666f9ba1e1b30e8458fefddf3c2e",
  b: "1d765c9032bd9fa0186e65db5ae4958eb382fda679ac296601cf42a9f6e7be0a",
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R9 creative SHA drift before transcription");
const script = readFileSync(join(episode, "script.md"), "utf8");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r9-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  const parsed = reader === "a"
    ? [...raw.toString("utf8").matchAll(/^\|\s*`([a-z_]+)`\s*\|\s*(YES|NO)\s*\|\s*(.*?)\s*\|$/gm)]
    : [...raw.toString("utf8").matchAll(/^\d+\.\s+\*\*`([a-z_]+)`\s+—\s+(YES|NO)\.\*\*\s*(.*)$/gm)];
  if (parsed.length !== 13 || parsed.some((row, i) => row[1] !== NARRATIVE_PANEL[i].id)) throw new Error(`reader ${reader} panel mismatch: ${parsed.length}`);
  const answers = parsed.map((row) => {
    const cited = [...row[3].matchAll(/\b(s\d{5})\b/g)].map((match) => match[1]);
    if (!cited.length || cited.some((id) => !lines.has(id) || !script.includes(lines.get(id)))) throw new Error(`reader ${reader} evidence missing or invalid for ${row[1]}`);
    let evidence = `[${cited[0]}] ${lines.get(cited[0])}`;
    if (row[1] === "no_recap") {
      const pair = reader === "a" ? ["s58061", "s58062"] : ["s58088", "s58089"];
      evidence = pair.map((id) => `[${id}] ${lines.get(id)}`).join("；");
    }
    return { id: row[1], yes: row[2] === "YES", evidence };
  });
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r9-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((answer) => answer.yes).length, no: answers.filter((answer) => !answer.yes).map((answer) => answer.id), answers });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R9", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((answer) => answer.yes).length, failed: merged.failed.map((answer) => answer.id), advisory: merged.advisory.map((answer) => answer.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 12 || audit.merged.failed.join(",") !== "no_recap" || audit.merged.advisory.length) throw new Error("unexpected R9 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
