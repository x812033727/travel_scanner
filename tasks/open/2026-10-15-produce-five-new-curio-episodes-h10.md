---
id: 2026-10-15-produce-five-new-curio-episodes-h10
title: Produce five new Curio episodes H10 H11 H12 M09 U09
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-five
claimed_at: 2026-10-15T23:52:59Z
created_at: 2026-10-15T16:31:58Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-next-five-20261016
---

# Produce five new Curio episodes H10 H11 H12 M09 U09

## Why

On 2026-10-16 (Asia/Taipei), the owner expanded the next Curio episode request to five new episodes. H09 remains a separate owner-operated Studio handoff. This batch covers H10 Franklin, H11 Voynich, H12 Flannan, M09 Antikythera and U09 pulsars under the current Curio series rules.

## Definition of done

- [x] Select five non-duplicate topics from existing checked research and isolate their work from H09.
- [x] Refresh primary evidence and independently review five concrete outline packages.
- [x] Present all five outlines and a bounded production estimate for the owner's decisions.
- [ ] Produce the selected scripts, narration, illustrations and final cuts through the actual review gates after the required decisions.
- [ ] Deliver approved upload packages; track languages and Studio delivery separately.

## Steps

- [x] Read current main and series/narrative rules; create the batch branch at a77a9416d.
- [x] Check local worktrees, Git refs, open PRs and 192 live non-Shorts videos for duplicates; the five exact slugs returned 404.
- [x] Complete each episode's research, claims and A/B outline under its own narrow task.
- [x] Cross-review evidence and narrative shape, assemble a single owner review index and production budget.
- [x] Read back owner outline and spending decisions before paid production.

## How to verify

Use the existing outlineOptions parser to confirm A/B options are complete. Check primary source retrieval and claim boundaries; independent reviewers must identify blocked sources. Validate task metadata and repository hygiene. Subsequent scripts must pass lint and narrative review; synthesis, audio acceptance, storyboard, final cut, package, languages and actual upload/playback retain distinct receipts.

## Notes

Source research is read-only from origin/claude/curio-topic-bank-second-batch at 949bb91fc85d41a53633d056062b27d87651e9d5. Do not edit the shared topic bank owned by its original task. This task owns only the batch index; episode researchers own their episode directories.

At 2026-10-16 01:01 Taipei, the five exact slugs were manually reported and submitted as outline reviews using the existing review API, without a Jev pick or paid call. All five read back pending with exact payloads and brief hashes; review IDs and hashes are in docs/videos/curio-next-five-20261016/submission.json. No worker-start request was issued. The immutable local bundle and incremental receipt are under the ordinary media work base at curio-next-five-20261016/review. Do not blindly resubmit; read the existing IDs first.

Owner review index: docs/videos/curio-next-five-20261016/README.md. Recommend A for each episode; proposed estimated stop limit USD6 per episode / USD30 total covers Mandarin synthesis, targeted retakes, transcription, images, image judging and text/audio/final QA through Gemini, MiniMax image-01 and TypeSafe Jev. Neither outline choice nor spending is approved yet. Episode task claims are released while awaiting decisions; claim the relevant scope before the next edits. Existing approvals for H09 do not apply.

On 2026-10-16 at 07:53 Taipei, the owner answered the bundled decision: all five A outlines selected in /admin/videos and the proposed zh-TW production scope authorized at USD6 per episode / USD30 total. Readback of each original outline review ID returned approved/A and its original brief SHA256. The source submission remains a historical pending receipt; decision-20261016.json records the later live approvals and the exact budget/data scope. The root task was reclaimed; each episode author reclaims its own narrow task. No paid call or worker start had been made at this readback. The script approval gate remains separate.

Cross-review fixes and test limits are recorded in outline-review.md. The docs-videos suite produced 214 passes and one known Windows Node24.13.0 native-copy crash; the exact failing test passed with the existing bundled Node24.19.0. Runtime/test sources match origin/main; no production tool code was changed.

Final handoff checks: check:tasks validated 1895 files (pre-existing stale/overlap warnings only), repo-hygiene passed 3/3, and the staged diff whitespace check passed. A separate read-only reviewer recomputed all five brief hashes and found no state/budget inconsistency across the batch documents. Local branches, remote refs and open PR file paths were checked again before preparing the draft PR; no competing five-episode change was found. The owner received one bundled request for backend outline choices and the proposed budget. Release this task while those decisions are pending; do not mark the production batch complete.

Live 2026-10-16 Taipei readback: image-01 is configured, series_script_gate=true, auto_pick_look=true, auto_approve_storyboard=true, shared max_usd_per_video=200. The one-off request schema has no individual dollar cap. The shared ceiling does not authorize spending on these five episodes. Existing H09 dollar approvals do not carry to this batch. No new paid requests or worker-start requests have been issued.

At 2026-10-16 08:04 Taipei, the five updated briefs were submitted as new manual outline reviews because the current lint requires four exact section headers and owner approval is tied to the whole-file SHA. The A/B option bodies and parsed summaries/hooks matched the originally approved payloads byte-for-byte. The new cards all read back pending, with IDs and hashes in docs/videos/curio-next-five-20261016/format-resubmission.json. Owner reconfirmation of A on these new cards is required before submitting scripts. The five scripts are being drafted and independently checked in parallel; no paid calls, worker starts, or script submissions have occurred.

The owner then reconfirmed all five revised A briefs in /admin/videos. At 2026-10-16 08:07 Taipei, every new review ID read back approved/A with its matching whole-file SHA-256; exact decisions are in format-decision-20261016.json. This clears the revised-outline gate, but not the independent script review or owner script approval gate. No paid calls or worker starts have occurred.

H09 PR #1503 head bff1f1a65 has no new CI run because main conflicts in docs/videos/long-form/review.md and review.json. A live task owned by codex-story-budget-cap still claims both files; no takeover or merge was performed. This is separate from the five-episode production branch and from H09's pending owner Studio URL.

## 2026-10-17 批次接續快照

本批總覽與原規劃保留在 `docs/videos/curio-next-five-20261016/README.md`、`production-plan.md`；兩份新增 2026-10-17 狀態節，避免把 10／16「零成片／零付費」的啟動基線讀成現況。五集 A 及正式劇本關卡均已通過；H10、H11、M09、U09 的繁中成片由站主核准，H12 最新分鏡 manifest `F61238CD…6A475AB` 已讀回核准並進入本機組裝，仍待最終 QA 與成片核准。五集尚不可結案。

站主已逐集追加 H10／H11 各 US$2、M09／U09 各 US$2.50 多語停手上限；原五集繁中 US$30 加增額 US$9，批次估算停手上限 US$39。此為授權上限，不是已花或供應商實際帳單；最新估算及預留只以外部共用帳本當時讀回為準。H11 的修正版繁中成片和最新上傳包／語言卡已核准、英日韓配音已經站主試聽接受；站主決定自行操作 Studio，尚待其提供影片網址及音軌完成讀回。H10 英韓已試聽接受、日語待站主提供錯句 ID；M09 英語已接受、日韓待試聽；U09 日語 102／102 機械 QA 已補齊，`724570c6` 由站主確認聽到核准詞，但其餘日語及英語旗標仍待試聽，韓語配音完成而 QA 進行中。不要把本機成片、後台卡片核准或逐句試聽當成 Studio 上傳及播放驗收。
