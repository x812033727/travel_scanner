// The policy item: Jev reads the narration against the channel's rules (docs/videos/HANDS-OFF.md
// §自動品管): written to the channel stance, with a demonstration or a worked example, without
// investment, medical, legal or political advice, and without sponsorship. The judgement is the
// site's (`POST /video/automation/judge/policy`, ticket 2026-09-26-video-hands-off-judge); this
// module only shapes the request and reads the answer, so both sides can be tested without Jev.
import { eachLine } from "../core/schema.mjs";

/** The body the judge endpoint receives: the script as spoken, the brief, and the YouTube text. */
export function policyRequest({ doc, brief, description }) {
  return {
    slug: doc.slug,
    format: doc.format,
    title: doc.youtube.title,
    description,
    brief: brief ?? "",
    lines: [...eachLine(doc)].map(({ scene, line }) => ({ id: line.id, scene: scene.id, text: line.text })),
  };
}

/**
 * The judge's answer as an item verdict: { ok, detail }. The endpoint answers
 * { passed: boolean, scores?: { <name>: number }, reasons?: string[] }; an answer without a
 * verdict is a failure, never a pass.
 */
export function policyVerdict(answer) {
  const passed = typeof answer?.passed === "boolean" ? answer.passed : typeof answer?.ok === "boolean" ? answer.ok : null;
  if (passed === null) return { ok: false, detail: "the judge answered without a verdict" };
  const scores = answer.scores && typeof answer.scores === "object" ? Object.entries(answer.scores).map(([name, score]) => `${name} ${Number(score).toFixed(2)}`).join(", ") : "";
  const reasons = Array.isArray(answer.reasons) ? answer.reasons.map(String).filter(Boolean) : [];
  const detail = [passed ? "Jev passed the narration" : "Jev did not pass the narration", ...(reasons.length ? [reasons.join("; ")] : []), ...(scores ? [scores] : [])].join(": ");
  return { ok: passed, detail };
}
