// The policy item: Jev reads the narration against the channel's rules (docs/videos/HANDS-OFF.md
// §自動品管): written to the channel stance and the owner's viewpoint, with a demonstration or a
// worked example, without investment, medical, legal or electoral advice, and not sponsored. The
// judgement is the site's (`POST /video/automation/judge/policy`, apps/api/app/video_automation/
// judge.py, whose request model refuses any field it does not know); this module only shapes the
// request and reads the answer, so both sides are tested without Jev.
import { briefSections } from "../core/lint.mjs";

// The endpoint's limits (judge.py JudgePolicyIn): a 10-minute narration is about 2,500 characters.
export const SCRIPT_MAX_CHARS = 60_000;
export const VIEWPOINT_MAX_CHARS = 8_000;
// The brief section the planner writes the owner's viewpoint in (core/lint.mjs BRIEF_SECTIONS).
export const VIEWPOINT_SECTION = "站主觀點";

const clip = (text, max) => [...text].slice(0, max).join("");

/** The narration as one text: every line in order, a blank line between scenes. */
export function narrationScript(doc) {
  return doc.scenes.map((scene) => scene.lines.map((line) => line.text).join("\n")).join("\n\n");
}

/** The owner's viewpoint: the text of brief.md's `## 站主觀點` section, or "" without one. */
export function ownerViewpoint(brief) {
  if (typeof brief !== "string") return "";
  return (briefSections(brief)[VIEWPOINT_SECTION] ?? "").trim();
}

/** The body the judge endpoint receives: exactly { slug, script, viewpoint }. */
export function policyRequest({ doc, brief }) {
  return { slug: doc.slug, script: clip(narrationScript(doc), SCRIPT_MAX_CHARS), viewpoint: clip(ownerViewpoint(brief), VIEWPOINT_MAX_CHARS) };
}

const SCORES = ["stance", "demo", "advice", "sponsored"];

/**
 * The judge's answer as an item verdict: { ok, detail }. The endpoint answers
 * { stance, demo, advice, sponsored, passed, note }: `passed` is the verdict and `note` is Jev's
 * sentence for the review card, passed or not. An answer without a verdict is a failure, never
 * a pass. `demo` is null for a video that is not asked for a demonstration (an explainer, a
 * story, a cut Short): the site's note says so (「有示範：不適用（解說）」), and the line
 * written here when there is no note says it was not asked instead of leaving it out.
 */
export function policyVerdict(answer) {
  if (typeof answer?.passed !== "boolean") return { ok: false, detail: "the judge answered without a verdict" };
  const note = typeof answer.note === "string" && answer.note.trim() ? answer.note.trim() : null;
  const scores = SCORES.filter((name) => typeof answer[name] === "number" || (name === "demo" && answer.demo === null))
    .map((name) => (answer[name] === null ? "demo not asked" : `${name} ${answer[name].toFixed(2)}`))
    .join(", ");
  const detail = note ?? `${answer.passed ? "Jev passed the narration" : "Jev did not pass the narration"}${scores ? `: ${scores}` : ""}`;
  return { ok: answer.passed, detail };
}
