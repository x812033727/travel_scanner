---
id: 2026-09-27-ai-shorts-owner-review-studio-launch
title: AI Shorts: owner review, Studio launch and 90-day measurement
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-27T18:47:02Z
completed_at:
branch: codex/shorts-backend-audit
depends_on:
  - 2026-09-27-ai-shorts-pilot
scope:
  - docs/videos/ai-shorts/releases
---

# AI Shorts: owner review, Studio launch and 90-day measurement

## Why

The local Shorts implementation provides three evidence-bound pilots and fifteen detailed briefs. Real audience performance and the 90-day goal require owner-reviewed publication and actual YouTube Studio exports. Local rendering does not establish public release, audience retention, or ten million views.

## Definition of done

- [ ] Owner listens to all three pilots and checks typography/captions on a phone; approve the local Hanhan voice or provide approved replacement narration.
- [ ] Export the existing channel's last 90 days of Shorts analytics, or record that no historical Shorts exist. Preserve raw files outside Git.
- [ ] Owner privately uploads the pilots in Studio, verifies playback/CC/cover and disclosure/audience settings, and explicitly chooses public release times.
- [ ] Record actual video IDs and public timestamps; initialize tracking from the first public date, not the illustrative calendar date.
- [ ] Capture actual 24h/72h/7d snapshots, costs and status changes. Review five mature samples per series before applying the editorial rules.
- [ ] Run weekly topic selection and budget review for 90 days; report the real outcome and missing observations without inventing retrospective snapshots.

## Steps

- [ ] Read docs/videos/ai-shorts/README.md and the delivery receipt; inspect the local artifact paths and manifests.
- [ ] Complete owner review and channel baseline before expanding production.
- [ ] Keep releases/ receipts for reviewed, uploaded and published states separately; private metrics/media remain outside Git.
- [ ] Produce subsequent topics from the campaign briefs and weekly evidence. Preserve existing original experiment outputs.

## How to verify

Use YouTube Studio Analytics → Advanced mode → Shorts → Export, preserving export time, filters and units. Run `node tools/video/shorts/cli.mjs track-init --dir <outside-repo-empty-dir> --start <actual-first-public-date>` and `report --dir <same-dir>`. Verify public playback and captions only after owner-authorized publication. An empty report must stay `no_metrics`; incomplete raw rows go to staging, never zero-fill.

## Notes

- Scope is release receipts; new scripts/tool changes need their own task and scope check.
- This ticket is not authorization to publish, buy subscriptions, alter production settings, or change the YouTube API quota.
- Targets: 120 slots over 90 days (30/45/45); 10,000,000 cumulative public views is a stretch goal. First three pilots <= NT$300; each 30-day period <= NT$3,000, soft stop at NT$2,400; total <= NT$9,000.
- Existing tests used the same session model in two fresh contexts, one bundled response each. They do not establish a model-brand ranking or general accuracy.

### 2026-09-29 live pilot review

- The three pilots are now in the production Shorts tab, all pending final approval. Current runtime: receipt 38.30s, poster 36.20s, prompt 35.80s. Exact downloaded review media was fully decoded and remeasured: all three are 1080x1920/30fps/H.264/AAC 48kHz and meet loudness/peak requirements (-14.14/-0.99, -14.01/-2.05, -13.90/-1.11 LUFS/dBTP respectively). This is not the old local-pilot acceptance receipt.
- Each still lacks a script-hash-bound `verify.json` and has a policy failure. Receipt phrase 4 and prompt phrase 6 are flagged by the submitted narration check; poster's 14 phrases passed the submitted automated check. Real listening was not performed, so no narration flag was waived.
- Rechecked 11 evidence references against the repository's experiment files; hashes match and both poster HTML files match the preserved JSON outputs. Receipt 275/25 and quiz 162/270/11:20, 3-versus-3 are supported. Backend evidence bytes were not independently downloaded; distinguish repository evidence validation from backend file identity.
- Required wording fix for `shorts-prompt-check`: the title says only one phrase was added, but the B request adds several requirements, and arithmetic/receipt/poster tasks share one bundled request per condition. Change the framing to stronger checking requirements, disclose bundling and one-run-per-condition limits, or run a genuinely single-variable experiment before preserving the current causal framing. Do not rewrite original experiment records.
- Improve receipt A/B wording: A already asks to check the total. Poster remains a preference comparison, not an objective B win; increase small-print legibility and make the bundled-method limit clear. Captured key content and captions fit the safe area; phone playback still needs acceptance.
- Live settings show Gemini/Sulafat, only Traditional Chinese, 25-55s, automatic production off, no campaign start date or autopublish consent. These settings do not prove which voice generated an existing file. The tab displays library 0, pending 15 and recorded cost NT$0; this does not prove production was free.
- Findings and per-video suggested return notes are retained outside Git in the dated `shorts-audit-20260929` audit package. All production review decisions, settings and YouTube states were left unchanged. Complete fixes, listening, current hash-bound facts/policy checks and owner acceptance before using the pilot launch workflow.

### 2026-09-29 owner-authorized corrections

- After the audit, the owner requested corrections. Revised scripts are in `docs/videos/ai-shorts/corrections-20260929/labs/`; original pilots, experiment protocol and outputs are preserved.
- All three were rebuilt with synchronized narration/captions. Automated narration passed 41/41 phrases; independent facts passed 32 claims; final files fully decoded and passed format, loudness, layout and caption checks. Added Gemini TTS usage across the correction runs was 18 calls / 209 characters, not a claim of zero cost.
- All three final reviews were resubmitted to their existing backend projects. Current video, QA and attachment hashes were reloaded and compared. The dated release receipt in this ticket's scope records exact video/script hashes; all remain pending, with 11/12 QA items passed and policy blocked by the empty channel stance.
- No publish review, YouTube upload, schedule, channel stance or other shared setting was changed. Owner listening/phone playback, channel stance approval, private-upload acceptance and actual analytics remain open. Source changes remain local on `codex/shorts-backend-audit`; no PR was created by this correction.
