---
id: 2026-09-28-drama-plan-continuity-handoff
title: Carry drama plan continuity rules into production review documents
status: review
priority: P2
area: docs
owner: codex-ten-drama
claimed_at: 2026-09-28T15:03:39Z
created_at: 2026-09-28T14:15:23Z
completed_at:
branch: codex/ten-drama-audit-fixes
depends_on: []
scope:
  - docs/videos/series-plans/binge-five-20260928
  - docs/videos/series-plans/claude-binge-five-20260928
---

# Carry drama plan continuity rules into production review documents

## Why

Both ten-drama builders write source.continuity_notes only to continuity.md,
outside the six documents imported for review. The episode worker consumes the
approved setting/chapter Markdown, structured cast/beats and recaps; it does not
load these local continuity files. Global visual/continuity instructions can
therefore be available to a human reviewer but absent from production inputs.

Current inventory: Codex has 60 notes and Claude has 35, across ten works. None
of those 95 complete note strings occurs verbatim in the 60 imported document
bodies, and none has a continuity_notes key. Some facts are repeated in settings
or episode beats, so this is NOT a claim that 95 unique facts were lost.

## Definition of done

- [x] After editorial corrections, required global continuity instructions are
  present in the actual review and writer/verifier payloads, with source-bound
  evidence. Merely retaining continuity.md in Git is insufficient.
- [x] Keep human-readable and structured review representations consistent.
  Reuse existing setting Markdown if appropriate; adding an ignored JSON key
  alone does not establish that the writer receives the instructions.
- [x] Add focused builder regression coverage for propagation and generated-file
  drift, and regenerate affected artifacts/manifests/review receipts correctly.
- [x] Document a separate authorized import/update step and do not overwrite
  production review history or claim that local regeneration updated production.

## Steps

- [x] Review Codex build.mjs:31-33,47 and Claude build.mjs:138-152,438-441.
  Continuity notes are emitted as a standalone file rather than part of setting.
- [x] Trace tools/video/automation/flow.mjs:799,844-859 and :1147-1160, plus
  prompts.mjs:747 onward. Production uses setting_md/chapter_md and structured
  cast/beats; neither the importer nor the worker reads continuity.md.
- [x] Select mandatory instructions after resolving contradictory notes in
  2026-09-28-ten-drama-plan-audit-findings. Do not blindly copy known-bad rules.
  Examples of global instructions to preserve/reconcile: Throne source.mjs:1439
  requires writing the handkerchief fold count at every covered-mouth action;
  Before the Hammer :1506 requires the repaired gold seam to remain visible
  after E27, and :1508 limits the master's post-stroke full-length speech.
  Individual beats show some of these facts but do not replace the global rule.

## How to verify

Audit used dynamic imports of all ten source.mjs files and parsed documents.json
structurally. Count source.continuity_notes and compare against concatenated
body_md plus JSON.stringify(body_json), then inspect the builder/worker path.

```text
city 12; rival 9; empress 14; train 14; wedding 11
hammer 8; ghost 8; reload 6; throne 7; three-needles 6
documents 60; notes 95; complete notes present verbatim 0
```

Verify a representative late-episode payload actually includes the applicable
global instruction after the fix. Run both batch validators and existing test
suites; renew changed review receipts rather than reusing stale content hashes.

## Notes

- Another explicit manual handoff remains for all ten: packaging requires
  chapter_cards=false and outro=false in the generated compilation video.json.
  automation/compilation.mjs:123 does not pass either option; the constructor
  in core/compilation.mjs:120 defaults both true. For forty episodes this creates
  forty chapter-card scenes and one outro. Both batch READMEs already explain
  the manual edit, so this is a tracked manual production step, not evidence
  that the intended card-free compilation is impossible. Confirm those flags
  and the resulting timeline at compilation acceptance. The current series
  request/import alone does not apply them.
- Do not confuse these missing payload instructions with finished-video defects;
  the audited ten had no generated episodes at the recorded production snapshot.
- This task only records the handoff gap. No source, production review document,
  generation setting, upload or publication was changed by the audit.

## Repair implementation, 2026-09-28

- Implemented in isolated branch `codex/ten-drama-audit-fixes` under the claimed
  ten-drama content / preloaded-approval / listener tasks. The owner explicitly
  approved parallel backend repairs despite other task claims; no other branch
  or owner claim was changed.
- Report: `docs/videos/series-plans/binge-five-20260928/AUDIT-REPAIR-20260928.md`.
- Local source/documents and code are revised; historical production/import
  receipts are unchanged. No deployment, production update, approval, generation
  or publication has been performed by this repair.

### Verification and handoff

- Content: both ten-work validators pass; 34 generator/continuity tests pass;
  independent revised-source receipts and all 60 current document hashes checked.
- API: 80 focused tests pass, including SQLite transaction coverage; 5 PostgreSQL
  integration tests remain skipped locally. Ruff and touched-file mypy pass.
- Worker/tool suite: 578 pass, 1 existing Windows/Bash environment skip.
- The branch is ready for code review; it has not been merged or deployed. The
  independent production/browser follow-up remains with its existing owner.
