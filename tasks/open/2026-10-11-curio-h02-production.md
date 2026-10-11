---
id: 2026-10-11-curio-h02-production
title: Produce Curio H02 Roanoke episode from the checked topic
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T16:47:36Z
completed_at:
branch: codex/curio-h02-production-20261012
depends_on: []
scope:
  - docs/videos/curio-h02
---

# Produce Curio H02 Roanoke episode from the checked topic

## Why

Owner requested continuation of 奇聞檔案局 on 2026-10-12 (Asia/Taipei). The three existing pilots have current approved upload packages; H02 is the first independently checked unproduced topic. Produce Roanoke from the existing dossier rather than repeat the pilots.

## Definition of done

- [x] Source-backed brief, script and claims; independent fact and listener reviews.
- [x] Narration and MiniMax image-01 illustrations produced within existing effective limits, with no uncertain paid retries.
- [ ] 1080p final with at least eight minutes of substantive narration, Traditional Chinese CC and verified upload package.
- [x] Current backend review readback and delivery hashes; owner gates and YouTube state reported separately.

## Steps

- [x] Check local worktrees, remote branches, open PRs and existing pilot receipts; claim narrow episode scope.
- [x] Refresh core sources and acquire clearly licensed photographs.
- [x] Write three outline options, submit outline and independently review script.
- [x] Dry-run and produce narration; resolve audio flags, submit and pull audio review.
- [x] Dry-run and produce illustrations, submit/pull storyboard; render and inspect the selected stills.
- [x] Assemble and caption the current source.
- [ ] Obtain the current storyboard and final decisions.
- [ ] Final QA, upload package, backend readback and receipt-bound delivery.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-h02`, `status --slug curio-h02`, final QA and package checks with the explicit repository-external video workdir. Verify actual media duration, decode, approval source hashes and saved attachments; run repository video-doc and task checks before delivery.

## Notes

- 2026-10-12: no curio production branch/PR, H02 docs or H02 workdir existed. H01/U02/L08 final and publish approvals match saved media. All three pilot language records are Traditional Chinese only; none has a YouTube ID. Their archived QA reports retain policy failures subsequently owner-approved, so they are not described as automatic 11/11 passes.
- H02 uses the agreed mystery cartoon palette, local slides route and ~10 minute target. CROATOAN is the agreed relocation message in White's own account; archaeological claims remain attributed and unresolved. The 2025 NPS page precedes the 2026 foundation announcement and cannot be presented as its response.
- Skip the two British Museum digital-image candidates awaiting owner licence choice; use independently verified public-domain photographs and label later imaginative depictions or reconstructed 1585 works.
- The task tool's UTC date generated the 2026-10-11 identifier; user-facing work date is 2026-10-12 Asia/Taipei.
- 2026-10-12: outline submitted once. Jev chose A with pick 1.00, stance 0.89 and advice 0.01, but demo 0.18 < 0.6 left the review pending. Existing tracking ticket `2026-10-10-outline-pick-demo-exempts-explainers` covers this known outline policy mismatch. Requested the owner's concrete outline decision while continuing independent script and source work; do not repeat paid outline judging.
- 2026-10-12: owner replied explicitly 「採用 A，繼續製作」. Record that decision against the frozen brief hash locally; distinguish this chat approval from the original backend pending outline review. Production may continue after independent script review without asking the same permission again.
- 2026-10-12: full script is 109 scenes / 134 lines / 91 shots. First fact review and listener text review pass; second independent fact review is completing. Current lint has zero errors and three prompt-word repetition warnings; 199 video-document tests passed using bundled Node v24.19.0. Dry-runs: 120 fresh speech requests / 2797 Gemini characters; illustrations estimated US$1.23 for one take or US$3.69 at three takes, within the existing US$80 limit. No paid synthesis has started yet.
- 2026-10-12: independent second fact review passed at video hash `7b8d066cbb42ad7ee621171fcaedcda7c5eeafb9acf9bf8dc6c7d287b08c482d`, claims hash `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`. TTS launched once after both reviews; running stage and exit receipt are held in the external `_audit/` directory. No audio, picture or final approval is implied by launch.
- 2026-10-12: TTS completed exit 0, 134 WAVs, 11:09 timeline / 9:10 substantive clips. All WAV/timeline/current speech hashes read back equal. check-audio interrupted on Windows EPERM after a confirmed answer reached the temporary journal receipt; exact 16 kHz request-body and answer hashes independently verified, both receipts backed up, original confirmed bytes restored and offline journal reuse proven with zero POSTs. Official check-audio resumed from cache; no uncertain request forgotten or resent. Illustration pilot previously refused by the active audio project lock, with no request sent.
- 2026-10-12: after two bounded retake rounds and one independently reviewed wording rewrite of five lines, check-audio passed 134/134 with zero flags; final narration 672.5 seconds, substantive clips 553.175 seconds. Audio review auto-approved on backend and pulled locally. Current video hash aa6a6155da421683bdb9a2bf16532d1460e78d15a17cd5505d14748efa9c917e is bound by original verify-2 plus audio-rewrite-review; claims unchanged. Three image pilots cost US$0.05; actual visual inspection requested two faithful prompt corrections despite passed judge scores, preserving old takes and manifest.
- 2026-10-12: after actual inspection of the complete batch, 18 faulty historical illustrations were replaced by native source-labelled cards. Current source `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e` retains all 134 spoken line objects and WAVs; 394 independent source/snapshot checks passed. Current 68 selected images and all 99 retained image files match the snapshot; four exact takes are retained with their original judge remarks. Illustration/judge ledger is USD 1.9915, with no reservations or pending jobs, excluding other production costs. Current audio `4c9de49b…` is backend-approved; storyboard `92961cfc…` is pending. The official checker fails because 52 otherwise passed pictures retain soft remarks; evidence is preserved and shared-code repair is tracked in `2026-10-11-align-storyboard-approval-with-retained-soft`. Render exited 0; the two actual still inspections cover 29/60 unique native states plus the thumbnail, without blocking issues.
- 2026-10-12: assembly and captions completed exit 0. 1080p final is 680.5 seconds / 20415 frames, SHA `d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6`; 134 Traditional Chinese cues include the five-second intro offset. Current final review `a3f6b386-f6ec-41ce-a5e2-9ded114a605b` is pending/manual, with all four retained takes listed. QA is 9/11: additional locales await owner selection and two Smithsonian automated GETs return 403, despite actual browser bodies being readable. All seven backend attachment metadata hashes/sizes match local files; actual remote playback/bytes remain unverified. YouTube ID is null, no upload package or publish approval exists.
- 2026-10-12: one full independent audit returned 290/299 PASS, eight known language/QA/review/package failures and one strict body avg-frame-rate mismatch (30.001103668 versus exact 30). Narration, body and final complete decode all exit 0; null-mux DTS warnings retained. Final probe is exact 30fps / 680.5 seconds. Nineteen unique final sample images were actually viewed, 175 checks PASS, no blocking visual issue. This is not full playback/listening or CC-player acceptance. Full evidence is in repository-external `_audit/`, summarized in `docs/videos/curio-h02/delivery.md` and `production.md`. Await owner storyboard/final and per-episode language decisions before packaging; do not restart or repurchase existing media.
- 2026-10-12: packet-only readback reproduced the null-mux warnings after rounding distinct PTS to a 30 Hz time base; original body/final PTS and DTS have no duplicates and DTS is monotonic. Original audit failures and media bytes remain unchanged; strict CFR and owner playback are not claimed. Claim will be released while awaiting the owner. Resume this branch and existing external receipts/media instead of starting a competing production; a draft PR preserves this work without merge or deployment.
