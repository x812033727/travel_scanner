---
id: 2026-10-26-distinguish-pending-narration-in-manual-progress
title: Distinguish pending narration from synthesized progress in manual review reports
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-26T02:02:07Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# Distinguish pending narration from synthesized progress in manual review reports

## Why

The manual review reporter writes the *next unfinished step's* completion-style
ID into the project's raw `stage`. After a script has a legitimate local adopt,
that next ID is `narration synthesized` even when no synthesis artifact exists.
The resulting backend label can be mistaken for completed narration.

The fifth episode's preserved normal `tts --dry-run` output is
`111 requests, 111 to synthesize; about 2508 billable characters now`.
Its saved normal project GET at 2026-10-26T01:51:27.193Z nevertheless records
`project_stage: "narration synthesized"`, while `paid_tts_started: false` and the
script review is genuinely `pending`. The local script adopt is a separate
record, not a remote/user-UI approval. At read-only inspection the work tree's
only regular file was `approvals.json`: there was no audio directory,
`timeline.json`, `narration.wav` or M4A.

This is not evidence that dry-run secretly synthesized audio or itself made a
progress PUT. `tts/cli.mjs:418-434` prints the estimate, optionally reads service
status and returns exit0. `cli.mjs:351-362` merely delegates. The relevant native
write is `reviewPush` in `review/sync.mjs:1322-1332`, which unconditionally uses
`stage: status.next ? status.next.id.slice(0, 40) : "done"` before submitting the
selected gate or returning from `--report-only`. The core narration step is
correctly incomplete when its current timeline/audio evidence is absent. Fix
the narrow reporting distinction without weakening that artifact test.

## Definition of done

- [ ] With a valid locally adopted script but no current narration artifacts,
      manual progress/report-only or script-review reporting does not write
      `narration synthesized` as if synthesis were complete. The user can tell
      pending narration/next action from an actually completed synthesis.
- [ ] Running only TTS dry-run and obtaining exit0 never qualifies as synthesis
      completion. Actual synthesized reporting uses the existing successful,
      current artifact/evidence determination; missing, stale or incomplete
      artifacts remain uncompleted.
- [ ] Already legitimate completed narration and later progress labels remain
      correct. The fix is narrowly scoped; do not globally reinterpret every
      existing valid stage or downgrade a genuinely completed stage.
- [ ] True remote script `pending`, source binding and local delegated adoption
      remain distinguishable. No fabricated approval, owner click or completed
      TTS receipt is created to make the label consistent.
- [ ] Focused offline native routing/report tests capture the normal project PUT
      and prove the distinction without network/provider requests or server
      state repair. Existing core gates, thresholds and success criteria stay
      unchanged.

## Steps

- [ ] Refresh the shared sync-file ownership/branch checks before claiming;
      coordinate the separate fitted-dub audio-readiness ticket on this file.
- [ ] Separate prospective narration work from completed synthesis in the
      manual progress payload, reusing the existing native status evidence.
- [ ] Add fake-transport report-only/script-gate cases after a dry-run-like
      zero-artifact state, plus valid completed/stale/partial artifact controls.
- [ ] Preserve the original observed label and dry-run proof; document the
      reporting fix without rewriting that old failure or the real approvals.

## How to verify

Use the native sandbox and fake `request`/provider fixtures in
`tools/video/review/sync.test.mjs`. Make a valid locally adopted script with no
audio/timeline, perform a stubbed `tts --dry-run`, and inspect the subsequent
normal manual report PUT. Its stage must remain explicitly pending rather than
claim narration was synthesized. Test both `--report-only` and an explicit
script gate, preserving the actual pending review and local adopt separately.

Use the existing synthetic-narration/current-evidence fixtures for a successful
completed-synthesis control, then remove/stale/interrupt those artifacts and
verify that reporting does not promote them. Retain existing valid later-stage
report behavior. The focused command after implementation is:

```bash
node --test tools/video/review/sync.test.mjs
```

All transports must be fake. Do not rerun a production dry-run, push a review,
reset backend stage, invoke paid TTS or alter core completion checks to verify
this ticket.

## Notes

- Filed only, **open and unclaimed**. Scope is exactly the native manual review
  routing/report file and its native tests. No core/TTS/provider/API/server
  implementation, progress repair, paid/retry behavior or settings change here.
- Safe preserved proof references under the external `work/ai-tech-next`:
  - `fifth-script-pending-readback.script-gate.json`, SHA256
    `f862a2d74fd12a3c69c6c0a6af4cd6c7eaefa020b6fef0437b412296b1cbe791`.
    Only the raw stage label, `pending` review and `paid_tts_started:false`
    excerpt is used here; sensitive project metadata is not copied.
  - `fifth-tts-initial-dry-run.log`, SHA256
    `cf8052a0fa5c0213503cb576f97cc7d413daa856e74d598c85f3d4c58cfa90c5`.
    The 111 pending requests/2508 characters are estimates, not synthesis or
    completed artifact receipts; quota/readiness details are not copied.
  - Source SHA256
    `ca1ef60f4e9fd98f7c2e336a7fc8ab339c58b94f557ba0a7f6b8fb7cc279e1bf`;
    native script SHA256
    `7aac2017419c82a4b81fb40050f067c9e021312600e5d66ec70846b58946107b`.
- Inspected `tools/video/review/sync.mjs` SHA256
  `8a25b2ce9e6eac14e32d789461f35d758504e5b4547ab3600f0c8e9985d3b4c9`.
  The native core `narration synthesized` predicate at `core/state.mjs:537`
  requires current speech/timeline/runtime/audio evidence; it must not be
  relaxed or patched for a misleading manual stage string.
- Local duplicate check covered open/done files, including uncommitted tasks,
  in all five worktrees and task trees of all six local branches. No equivalent
  pending-versus-synthesized manual-report ticket was found. No network or
  remote/PR query was used for this explicitly local-only filing.
- `2026-10-07-count-targeted-dub-retakes-in-dry` is about cached redo request and
  character estimates, not stage reporting. The imageStatus dry-run task is
  about a media provider key. `2026-10-25-a-final-review-calls-fitted-dubs`
  shares `sync.mjs` but concerns attaching a fitted foreign track before its
  audio check passes; coordinate ownership, do not merge the two defects.
- No original failure label, backend stage, source/script approval record,
  diagnostic or dry-run log was edited. No production command, network/paid
  request, commit or stage occurred while filing this ticket.
