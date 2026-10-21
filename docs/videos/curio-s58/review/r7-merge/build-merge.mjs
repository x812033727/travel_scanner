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
  "claims.md": "fbb902e05bede6a4a88b108aae725667b41058c979ff7a69dea339a188c19e87",
  "video.json": "ad330abbe8f0919987c01de2c3227e025af8d1d93cc7f2e3557875d5d7b629ec",
  "script.md": "d32bea9d5cc33125cf9b41f1288a8faf78765d96dcd3ed2002abe4ad97f20957",
};
const ballotHashes = {
  a: "ec1a47dda76f6606c0fce4fc2b49861ed9254a6015587f84b15633f562c015cc",
  b: "37a697113f8e29558498e4b6e41e5019254668b7f05eb739f697db9d618cb610",
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R7 creative SHA drift before transcription");
const script = readFileSync(join(episode, "script.md"), "utf8");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r7-blind-${reader}.md`);
  const raw = readFileSync(source);
  if (sha(raw) !== ballotHashes[reader]) throw new Error(`reader ${reader} ballot SHA drift`);
  writeFileSync(join(here, `raw-ballot-${reader}.md`), raw);
  let answers;
  if (reader === "a") {
    const parsed = [...raw.toString("utf8").matchAll(/^\|\s*`([a-z_]+)`\s*\|\s*(YES|NO)\s*\|\s*(.*?)\s*\|$/gm)];
    if (parsed.length !== 13 || parsed.some((row, i) => row[1] !== NARRATIVE_PANEL[i].id)) throw new Error(`reader A panel mismatch: ${parsed.length}`);
    answers = parsed.map((row) => {
      const cited = [...row[3].matchAll(/\[\s*(s\d{5})\b/g)].map((match) => match[1]);
      if (!cited.length || cited.some((id) => !lines.has(id) || !script.includes(lines.get(id)))) throw new Error(`reader A evidence missing or invalid for ${row[1]}`);
      return { id: row[1], yes: row[2] === "YES", evidence: `[${cited[0]}] ${row[3]}` };
    });
  } else {
    const parsed = JSON.parse(raw.toString("utf8"));
    if (parsed.script_sha256 !== expected["script.md"] || parsed.answers?.length !== 13 || parsed.answers.some((row, i) => row.id !== NARRATIVE_PANEL[i].id)) throw new Error("reader B frozen script or panel mismatch");
    answers = parsed.answers.map(({ id, yes, evidence }) => {
      if (typeof yes !== "boolean" || typeof evidence !== "string") throw new Error(`reader B malformed ${id}`);
      const cited = [...evidence.matchAll(/\[\s*(s\d{5})\s*\]/g)].map((match) => match[1]);
      if (!cited.length || cited.some((sid) => !lines.has(sid))) throw new Error(`reader B evidence missing scene citation for ${id}`);
      return { id, yes, evidence };
    });
  }
  const answerFile = join(here, `ballot-${reader}.json`);
  writeFileSync(answerFile, `${JSON.stringify({ answers }, null, 2)}\n`);
  const verdict = panelVerdict({ answers });
  if (verdict.answers.some((answer, i) => answer.yes !== answers[i].yes)) throw new Error(`reader ${reader} official verdict changed a vote`);
  ballots.push({ reader, original_path: `../r7-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((answer) => answer.yes).length, no: answers.filter((answer) => !answer.yes).map((answer) => answer.id), answers });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R7", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((answer) => answer.yes).length, failed: merged.failed.map((answer) => answer.id), advisory: merged.advisory.map((answer) => answer.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 12 || audit.merged.failed.join(",") !== "no_recap" || audit.merged.advisory.length) throw new Error("unexpected R7 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
