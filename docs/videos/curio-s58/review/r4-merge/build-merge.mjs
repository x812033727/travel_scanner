import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256, panelVerdict, mergePanelVerdicts } from "../../../../../tools/video/core/narrative.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const expected = {
  "research.md": "0adab42902bd00393a4b7c945a4b37a9eae4f61e79cbbd2710085713f8643132",
  "brief.md": "8d0d42c6c5cf1de97ee8b497db3d298540b9fc21e1fe3bcee024b749c8960e08",
  "claims.md": "f0e340870fa7389224932ca732950fb990b4bdebcf4baaabf2d93fa3d994edc1",
  "video.json": "78960f72a00a5fcc245896d680bc18f9481cef6c472dd9fc94d82ad80ae7e547",
  "script.md": "b9451d33643dccd8ffc84f4a6f93074f4500adb50855f7a5529d9620eeaa8d0c",
};
const ballotHashes = {
  a: "965de7b59b68e381db7486aa3d79071de7a058d34f4b05ce5c59aa0190e071b1",
  b: "f0380deb62cd71f4ea66d1ac11d9c7fd1f11c049dfbe98b34139f2337a7f4be0",
};
const chosen = {
  a: ["s58001", "s58005", "s58031", "s58099", "s58108", "s58013", "s58111", "s58080", "s58080", "s58146", "s58005", "s58021", "s58057"],
  b: ["s58001", "s58005", "s58031", "s58099", "s58108", "s58013", "s58111", "s58080", "s58080", "s58146", "s58005", "s58021", "s58057"],
};

const creative = Object.fromEntries(Object.keys(expected).map((name) => [name, sha(readFileSync(join(episode, name)))]));
if (Object.entries(expected).some(([name, value]) => creative[name] !== value)) throw new Error("R4 creative SHA drift before transcription");
const lines = new Map(JSON.parse(readFileSync(join(episode, "video.json"), "utf8")).scenes.map((scene) => [scene.id, scene.lines[0].text]));
const ballots = [];
const verdicts = [];
for (const reader of ["a", "b"]) {
  const source = join(here, `../r4-blind-${reader}.md`);
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
  ballots.push({ reader, original_path: `../r4-blind-${reader}.md`, original_sha256: sha(raw), raw_copy_sha256: sha(readFileSync(join(here, `raw-ballot-${reader}.md`))), answer_sha256: sha(readFileSync(answerFile)), yes: answers.filter((a) => a.yes).length, no: answers.filter((a) => !a.yes).map((a) => a.id), citations: parsed.map((row, i) => ({ id: row[1], vote: row[2], quoted_id: chosen[reader][i], quoted_line: lines.get(chosen[reader][i]), original_reason_mentions_id: row[3].includes(chosen[reader][i]), original_reason: row[3] })) });
  verdicts.push(verdict);
}
const merged = mergePanelVerdicts(verdicts);
const mergedAnswers = { answers: merged.answers.map(({ id, yes, evidence }) => ({ id, yes, evidence })) };
const mergedFile = join(here, "merged-answers.json");
writeFileSync(mergedFile, `${JSON.stringify(mergedAnswers, null, 2)}\n`);
const audit = { slug: "curio-s58", round: "R4", rule: "official fixed OR: a cited YES from either reader passes a criterion", creative_sha256: creative, creative_matches_at_transcription: true, panel_rules_sha256: PANEL_RULES_SHA256, ballots, merged_answer_sha256: sha(readFileSync(mergedFile)), merged: { passed: merged.passed, yes: merged.answers.filter((a) => a.yes).length, failed: merged.failed.map((a) => a.id), advisory: merged.advisory.map((a) => a.id), answers: merged.answers.map(({ id, yes, evidence, yes_readers }) => ({ id, yes, evidence, yes_readers })) } };
writeFileSync(join(here, "merge-audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
if (merged.passed || audit.merged.yes !== 11 || audit.merged.failed.join(",") !== "chapters_link,no_recap") throw new Error("unexpected R4 OR result");
process.stdout.write(`${JSON.stringify({ ballots: ballots.map(({ reader, yes, no }) => ({ reader, yes, no })), merged: audit.merged, panel_rules_sha256: PANEL_RULES_SHA256 }, null, 2)}\n`);
