// Read-only checks for the approved C14 source projection. No paid or media calls.
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { textHash } from "../../../tools/video/core/schema.mjs";
import { lintProject, loadProject } from "../../../tools/video/core/state.mjs";
import { factsChecks } from "../../../tools/video/qa/facts.mjs";

const dir = dirname(fileURLToPath(import.meta.url));
const check = spawnSync(process.execPath, [join(dir, "build-canonical.mjs"), "--check"], { encoding: "utf8" });
if (check.status !== 0) throw new Error(`Approved-source projection failed: ${check.stderr || check.stdout}`);
const script = readFileSync(join(dir, "script.md"), "utf8");
const plan = JSON.parse(readFileSync(join(dir, "visual-plan.json"), "utf8"));
const rows = [...script.matchAll(/^- \*\*([HOIETN]\d{2})\*\* (.+?)〔(.+?)〕$/gm)];
const project = loadProject({ slug: "story-everyday-camelbak-c14" });
const doc = project.doc;
const lint = lintProject(project);
if (lint.errors.length) throw new Error(`C14 lint errors: ${JSON.stringify(lint.errors)}`);
const facts = factsChecks({ report: { name: "verify-1.md",
  markdown: readFileSync(join(dir, "verify-1.md"), "utf8") }, doc });
if (!facts.ok) throw new Error(`C14 existing-source QA bridge failed: ${facts.detail}`);
if (rows.length !== 70 || doc.scenes.length !== 70) throw new Error("C14 needs 70 approved lines and scenes");
let images = 0;
let cards = 0;
let consecutiveCards = 0;
let maxConsecutiveCards = 0;
let paperTotal = 0;
let paperColdOpen = 0;
let paperBodyImages = 0;
for (const [index, match] of rows.entries()) {
  const [, sourceId, approvedText] = match;
  const visual = plan.shots[index];
  const scene = doc.scenes[index];
  const line = scene.lines?.[0];
  if (visual.line !== sourceId || line?.id !== `c14${sourceId.toLowerCase()}` ||
      line?.text !== approvedText || scene.id !== `c14-sc-${line.id}` ||
      scene.claims?.length !== 1 || scene.claims[0] !== sourceId ||
      (line.say !== undefined && line.say_for !== textHash(line.text))) {
    throw new Error(`C14 approved line or ID mismatch: ${sourceId}`);
  }
  if (visual.kind === "illustration") {
    images += 1;
    consecutiveCards = 0;
    if (scene.template !== "shot" || scene.data.prompt !== visual.prompt ||
        scene.data.camera !== visual.motion.replaceAll("_", " ") || scene.data.visual !== "still") {
      throw new Error(`C14 approved illustration changed: ${sourceId}`);
    }
    if (sourceId[0] !== "H") paperBodyImages += visual.planned_duration_s;
  } else if (visual.kind === "card") {
    cards += 1;
    consecutiveCards += 1;
    maxConsecutiveCards = Math.max(maxConsecutiveCards, consecutiveCards);
    if (scene.template !== "big" || scene.data.text !== visual.post_text) {
      throw new Error(`C14 approved card changed: ${sourceId}`);
    }
  } else {
    throw new Error(`Unexpected C14 visual kind: ${sourceId}`);
  }
  paperTotal += visual.planned_duration_s;
  if (sourceId[0] === "H") paperColdOpen += visual.planned_duration_s;
}
const round = (value) => Math.round(value * 10) / 10;
const paperPostIntro = round(paperTotal - paperColdOpen);
if (images !== 54 || cards !== 16 || maxConsecutiveCards !== 3 ||
    round(paperTotal) !== 496.5 || round(paperColdOpen) !== 40.3 ||
    paperPostIntro !== 456.2 || round(paperBodyImages) !== 333.0) {
  throw new Error("C14 paper timing or illustration/card mix changed");
}
console.log(JSON.stringify({
  status: "nonpaid-preflight-pass-with-production-hold", source_lines: 70, scenes: 70,
  illustrations: images, cards, max_consecutive_cards: maxConsecutiveCards,
  paper_all_narration_s: round(paperTotal), paper_cold_open_s: round(paperColdOpen),
  paper_postintro_body_s: paperPostIntro, paper_body_illustration_s: round(paperBodyImages),
  paper_body_illustration_percent: round((paperBodyImages / paperPostIntro) * 100),
  measured_body_floor_s: 480, paper_body_shortfall_s: round(480 - paperPostIntro),
  lint_errors: lint.errors.length, lint_warnings: lint.warnings.length,
  existing_source_qa_bridge: facts.ok,
  paid_authorized: false, measured_audio_available: false,
}));
