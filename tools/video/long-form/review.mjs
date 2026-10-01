import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { DIRECTORY, ROOT } from "./plans.mjs";

const sha = (value) => createHash("sha256").update(value).digest("hex");
export const REVIEW_FILES = [
  "tools/video/long-form/plans.mjs", "tools/video/long-form/cli.mjs", "tools/video/long-form/review.mjs",
  "docs/videos/long-form/policy.json", "docs/videos/long-form/plans.json",
  "tools/video/core/duration.mjs", "tools/video/qa/checks.mjs", "tools/video/qa/cli.mjs",
  "apps/api/app/video_automation/schemas.py", "apps/api/app/video_automation/series.py",
  "apps/web/components/admin-video-series.tsx", "docs/videos/long-form/README.md",
  "docs/videos/so-thats-why/README.md", "docs/videos/so-thats-why/season2/README.md", "docs/videos/KNOWLEDGE-STORIES.md",
  "tools/video/long-form/plans.test.mjs", "tools/video/long-form/review.test.mjs", "tools/video/core/duration.test.mjs", "tools/video/qa/duration.test.mjs",
  "apps/api/tests/test_video_explainer_duration.py", "apps/web/components/admin-video-explainer-duration.test.tsx",
];

export function durationReviewProblems(receipt, report, hashFile) {
  const problems = [];
  if (receipt?.status !== "PASS" || receipt?.review_scope !== "DURATION_ONLY" || !receipt?.author_agent || !receipt?.reviewer_agent || receipt.author_agent === receipt.reviewer_agent) problems.push("independent passing duration-only review required");
  if (receipt?.report !== `${DIRECTORY}/review.md` || receipt?.report_sha256 !== sha(report)) problems.push("duration review report is stale");
  const bindings = Object.fromEntries([...report.matchAll(/\| `([^`]+)` \| `([a-f0-9]{64})` \|/g)].map((match) => [match[1], match[2]]));
  if (JSON.stringify(Object.keys(receipt?.reviewed_files ?? {}).sort()) !== JSON.stringify([...REVIEW_FILES].sort())) problems.push("duration review must cover every implementation, plan, document and regression test");
  for (const file of REVIEW_FILES) {
    const expected = receipt?.reviewed_files?.[file];
    if (!expected || expected !== bindings[file] || expected !== hashFile(file)) problems.push(`stale duration review binding: ${file}`);
  }
  return problems;
}

export function checkDurationReview(root = ROOT) {
  const bytes = (file) => readFileSync(path.join(root, file));
  const receipt = JSON.parse(bytes(`${DIRECTORY}/review.json`));
  const report = bytes(`${DIRECTORY}/review.md`).toString("utf8");
  return durationReviewProblems(receipt, report, (file) => sha(bytes(file)));
}
