import { createHash } from "node:crypto";
import { copyFileSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { PANEL_RULES_SHA256, NARRATIVE_PANEL, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");
const expected = {
  "research.md": "ad5baec33ae786da9d103eecadca9f16c9f23f00d4041bde158e1e2697958efb",
  "brief.md": "f2086e64ffd56c5c2d8ea072d7122ffd7d7a2c2290c3413cf54a8ea2a8e35b4f",
  "claims.md": "75f3c81a1cfba0250c8fe2d291765acdeb098dd6f37e8fc34bb17632e62356e9",
  "video.json": "542c5d17330d2344fd588bfe839b636642f37da80c97a9f34d29ace013c75ec5",
  "script.md": "86d6b9883dc24ba55b2c4c66ad390755610999a84dd354e1c02aa8c0f8cbc1f3",
};
const originals = {
  a: { ballot: "../r3-blind-a.md", answer: "../r3-blind-a-answers.json", ballot_sha: "5ab3e4a99ca0df9ec139e352a19b147ca1a2d8040aaf14734090450ce9744e36", answer_sha: "74e45ae2000bb9628a53c121dcd06f8deaca21a570bd7db3ecde5f8db2d87801" },
  b: { ballot: "../r3-blind-b.md", answer: "../r3-blind-b/answers.json", ballot_sha: "958183170d8470b0c8d9302c040d5ebec187bb6ae05bb7b78a42a9c11e45b23e", answer_sha: "5c8d149b111d66cd1daa433151d0cbf356839afdf0e338bcf9b31637fb8a7a15" },
};
const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(join(episode, name))]));
if (Object.entries(expected).some(([name, hash]) => creative[name] !== hash)) throw new Error("R3 creative SHA drift");
const sceneLines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.lines[0].id, scene.lines[0].text]));
const verdicts = [];
const ballots = [];
for (const [reader, source] of Object.entries(originals)) {
  const ballotPath = join(here, source.ballot);
  const answerPath = join(here, source.answer);
  if (sha(ballotPath) !== source.ballot_sha || sha(answerPath) !== source.answer_sha) throw new Error(`R3 reader ${reader} receipt SHA drift`);
  copyFileSync(ballotPath, join(here, `raw-ballot-${reader}.md`));
  copyFileSync(answerPath, join(here, `ballot-${reader}.json`));
  const answers = JSON.parse(readFileSync(answerPath, "utf8"));
  if (answers.answers.length !== NARRATIVE_PANEL.length || answers.answers.some((a, i) => a.id !== NARRATIVE_PANEL[i].id)) throw new Error(`reader ${reader} panel order`);
  for (const answer of answers.answers) {
    const cited = [...answer.evidence.matchAll(/\[(s\d{5})\]/g)].map((hit) => hit[1]);
    if (cited.length === 0 || cited.some((id) => !sceneLines.has(id))) throw new Error(`reader ${reader} unknown evidence ID for ${answer.id}`);
  }
  const verdict = panelVerdict(answers);
  if (verdict.answers.filter((a) => a.yes).length !== 12 || verdict.failed.map((a) => a.id).join(",") !== "no_recap") throw new Error(`reader ${reader} unexpected ballot`);
  verdicts.push(verdict);
  ballots.push({ reader, original_ballot_path: source.ballot, original_ballot_sha256: source.ballot_sha, original_answer_path: source.answer, original_answer_sha256: source.answer_sha, raw_copy_sha256: sha(join(here, `raw-ballot-${reader}.md`)), answer_copy_sha256: sha(join(here, `ballot-${reader}.json`)), yes: 12, failed: ["no_recap"], no_recap_evidence: verdict.failed[0].evidence });
}
const merged = mergePanelVerdicts(verdicts);
if (merged.passed || merged.answers.filter((a) => a.yes).length !== 12 || merged.failed.map((a) => a.id).join(",") !== "no_recap" || merged.advisory.length) throw new Error("unexpected fixed-OR result");
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
writeFileSync(join(here, "merged-answers.json"), `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s59", round: "R3", rule: "official fixed OR: one cited YES from either reader passes a criterion", creative_sha256: creative, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(join(here, "merged-answers.json")), merged: { passed: merged.passed, yes: 12, failed: ["no_recap"], advisory: [], answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) }, policy_gate: "NOT_RUN because required narrative criterion no_recap failed" };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, failed }) => ({ reader, yes, failed })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
