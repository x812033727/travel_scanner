"""Option (d): real Jev decisions the site recorded, pulled from the repository with the line each
comes from, so a card can be checked against its source. Reads files only."""
import json
import re

from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[4]) + "/"  # the repository root


def line(path, needle):
    for no, text in enumerate(open(ROOT + path, encoding="utf-8"), 1):
        if needle in text:
            return {"file": path, "line": no, "text": text.strip()[:400]}
    raise SystemExit(f"not found: {needle} in {path}")


audio = json.load(open(ROOT + "docs/videos/series-plans/competition-20261002/episodes/audio-check-summary.json", encoding="utf-8"))
flagged = [
    {"episode": ep["episode"], "check_at": ep["latest_check_run"]["at"], **{k: f[k] for k in ("line_id", "intended")},
     "heard": f["first_recognizer"]["heard"], "jev_noul": f["first_recognizer"]["noul"],
     "second_heard": f["second_recognizer"]["heard"], "second_jev_noul": f["second_recognizer"]["noul"]}
    for ep in audio["episodes"] for f in ep["flagged_lines"]
]

records = {
    "outline_pick_t27": line("docs/videos/sothatswhy-t27/production-record.md", "choice 0.99"),
    "outline_thresholds": line("apps/api/app/video_automation/judge.py", "PICK_MIN_DEMO = "),
    "policy_demo_siri_fail_then_pass": line("tasks/open/2026-09-28-video-1m-siri-ai.md", "有示範 0.26"),
    "policy_demo_siri_near_threshold": line("tasks/open/2026-09-28-video-1m-siri-ai.md", "0.62 與 0.58"),
    "policy_demo_google_vids_owner_override": line("tasks/open/2026-09-28-video-1m-google-vids-free.md", "有示範」0.52"),
    "narration_threshold": line("tools/video/tts/check.mjs", "DEFAULT_THRESHOLD = 0.5"),
    "narration_L002_accepted": line("docs/videos/series-plans/competition-20261002/pilot/review.md", "Jev 記錄 0.66"),
    "narration_flagged_lines_from_receipt": flagged,
    "news_duplicate_band": line("apps/api/app/news_automation/ai.py", "0.25 < probability < 0.85"),
    "news_budget_ran_out_0926": line("tasks/done/2026-09-26-pause-news-candidates-when-the-jev.md", "207 of 243"),
    "news_budget_ran_out_0927": line("tasks/done/2026-09-27-resume-jev-paused-news-candidates-as.md", "99 news candidates"),
    "news_budget_raised": line("tasks/done/2026-09-27-resume-jev-paused-news-candidates-as.md", "raised the budget to 5,000"),
    "generating_model_reply_failures_0924": [
        line("tasks/done/2026-09-24-let-news-model-replies-be-repaired.md", "three of the first five"),
        line("tasks/done/2026-09-24-let-news-model-replies-be-repaired.md", "missing comma at column 3363"),
        line("tasks/done/2026-09-24-let-news-model-replies-be-repaired.md", "326-character summary"),
        line("tasks/done/2026-09-24-let-news-model-replies-be-repaired.md", "extra_forbidden"),
    ],
    "cjk_never_acts_alone": line("apps/api/app/ai/jev.py", "if tier == \"act\" and locale != \"en\" and not cjk_autopilot"),
    "where_we_chose_not_to_use_jev": [
        line("docs/catchtable-ranking-discovery.md", "不做 skill、不接 Jev。"),
        line("tasks/done/2026-09-21-jev-typesafe-system-one-decision-provider.md", "Withdrawn after"),
    ],
    "no_accuracy_measurement_on_our_content_yet": [
        line("tasks/open/2026-09-22-jev-review-advisory-tool.md", "- [ ] The measurement below has been run"),
        line("tasks/open/2026-09-22-jev-review-advisory-tool.md", "runs_with_shadow_rows: 0"),
    ],
}
print(json.dumps(records, ensure_ascii=False, indent=1))
