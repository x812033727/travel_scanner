import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { DIRECTORY, ROOT } from "./plans.mjs";

const sha = (value) => createHash("sha256").update(value).digest("hex");
export const REVIEW_FILES = [
  ".agents/skills/youtube-video/SKILL.md",
  ".agents/skills/youtube-video/references/automated.md",
  ".agents/skills/youtube-video/references/formats.md",
  ".claude/skills/youtube-video/SKILL.md",
  "apps/api/app/video_automation/anime_policy.py",
  "apps/api/app/video_automation/judge.py",
  "apps/api/app/video_automation/models.py",
  "apps/api/app/video_automation/schemas.py",
  "apps/api/app/video_automation/series.py",
  "apps/api/app/video_automation/settings.py",
  "apps/api/app/video_reviews/admin_service.py",
  "apps/api/app/video_reviews/schemas.py",
  "apps/api/migrations/versions/0118_video_min_8_minutes.py",
  "apps/api/migrations/versions/0122_video_anime_production_policy.py",
  "apps/api/tests/test_migration_0118_video_min_8_minutes.py",
  "apps/api/tests/test_migration_0121_video_series_planning.py",
  "apps/api/tests/test_migration_0122_video_anime_production_policy.py",
  "apps/api/tests/test_video_anime_production_policy.py",
  "apps/api/tests/test_video_anime_review_policy.py",
  "apps/api/tests/test_video_automation_settings.py",
  "apps/api/tests/test_video_drama_requests.py",
  "apps/api/tests/test_video_explainer_duration.py",
  "apps/api/tests/test_video_series.py",
  "apps/web/components/admin-video-explainer-duration.test.tsx",
  "apps/web/components/admin-video-review-card.tsx",
  "apps/web/components/admin-video-reviews.test.tsx",
  "apps/web/components/admin-video-series.test.tsx",
  "apps/web/components/admin-video-series.tsx",
  "apps/web/components/admin-video-settings-tutorial.tsx",
  "apps/web/messages/en/admin.json",
  "apps/web/messages/ja/admin.json",
  "apps/web/messages/ko/admin.json",
  "apps/web/messages/zh-CN/admin.json",
  "apps/web/messages/zh-TW/admin.json",
  "docs/videos/DESIGN.md",
  "docs/videos/KNOWLEDGE-STORIES.md",
  "docs/videos/LONG-ANIME-PRODUCTION.md",
  "docs/videos/README.md",
  "docs/videos/long-form/README.md",
  "docs/videos/long-form/plans.json",
  "docs/videos/long-form/policy.json",
  "docs/videos/series-plans/borrowed-dawn/authoring-contract.json",
  "docs/videos/series-plans/borrowed-dawn/validate.mjs",
  "docs/videos/so-thats-why/README.md",
  "docs/videos/so-thats-why/season2/README.md",
  "tools/video/assemble/assemble.test.mjs",
  "tools/video/assemble/cli.mjs",
  "tools/video/assemble/smoke.mjs",
  "tools/video/automation/anime-write.mjs",
  "tools/video/automation/anime-write.test.mjs",
  "tools/video/automation/automation.test.mjs",
  "tools/video/automation/discuss.mjs",
  "tools/video/automation/flow.mjs",
  "tools/video/automation/prompts.mjs",
  "tools/video/automation/series.mjs",
  "tools/video/automation/series.test.mjs",
  "tools/video/cli.test.mjs",
  "tools/video/core/anime-policy.mjs",
  "tools/video/core/anime-policy.test.mjs",
  "tools/video/core/approvals.mjs",
  "tools/video/core/approvals.test.mjs",
  "tools/video/core/branding.mjs",
  "tools/video/core/branding.test.mjs",
  "tools/video/core/drama.mjs",
  "tools/video/core/drama.test.mjs",
  "tools/video/core/duration.mjs",
  "tools/video/core/duration.test.mjs",
  "tools/video/core/explainer.test.mjs",
  "tools/video/core/lint.mjs",
  "tools/video/core/lint.test.mjs",
  "tools/video/core/narration-locale.test.mjs",
  "tools/video/core/schema.mjs",
  "tools/video/core/screenplay.mjs",
  "tools/video/core/screenplay.test.mjs",
  "tools/video/core/stages.test.mjs",
  "tools/video/core/state.mjs",
  "tools/video/core/state.test.mjs",
  "tools/video/core/timeline.mjs",
  "tools/video/core/timeline.test.mjs",
  "tools/video/dubs/captions-package.test.mjs",
  "tools/video/dubs/dubs.test.mjs",
  "tools/video/dubs/freshness.test.mjs",
  "tools/video/dubs/plan.test.mjs",
  "tools/video/long-form/cli.mjs",
  "tools/video/long-form/integration.test.mjs",
  "tools/video/long-form/plans.mjs",
  "tools/video/long-form/plans.test.mjs",
  "tools/video/long-form/review.mjs",
  "tools/video/long-form/review.test.mjs",
  "tools/video/media/clips.test.mjs",
  "tools/video/media/look-keyframes.test.mjs",
  "tools/video/package/cli.mjs",
  "tools/video/package/package.test.mjs",
  "tools/video/production/anime-input.mjs",
  "tools/video/production/anime-input.test.mjs",
  "tools/video/qa/checks.mjs",
  "tools/video/qa/checks.test.mjs",
  "tools/video/qa/cli.mjs",
  "tools/video/qa/duration.test.mjs",
  "tools/video/qa/qa.test.mjs",
  "tools/video/review/sync.mjs",
  "tools/video/review/sync.test.mjs",
  "tools/video/screencast/screencast.test.mjs",
  "tools/video/templates/terminal/terminal.test.mjs",
  "tools/video/tts/batch-recovery.test.mjs",
  "tools/video/tts/check.test.mjs",
  "tools/video/tts/synthesis.mjs",
  "tools/video/tts/tts.test.mjs",
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
