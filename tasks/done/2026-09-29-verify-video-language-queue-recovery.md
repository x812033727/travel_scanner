---
id: 2026-09-29-verify-video-language-queue-recovery
title: Verify video language queue recovery after deployment
status: done
priority: P1
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-29T10:56:13Z
created_at: 2026-09-29T00:57:26Z
completed_at: 2026-09-29T10:58:37Z
branch: claude/verify-language-queue-recovery
depends_on:
  - 2026-09-29-video-language-summary-stalls-worker
scope:
  - docs/videos/validation/language-queue-recovery.md
---

# Verify video language queue recovery after deployment

## Why

The language submission fix needs production acceptance after the owner separately
authorizes deployment. The 2026-09-29 read-only diagnosis found a 673-character
Academy language summary rejected by the 500-character API limit every five
minutes, starving later videos. Local regression tests cannot establish recovery
of those production files and review records.

## Definition of done

- [x] The owner authorizes a specific reviewed revision for production deployment;
  deploy preflight and health/revision checks pass.
- [x] The Academy language batch submits successfully with full skip reasons still
  visible in the payload, without changing approvals or the existing YouTube ID.
- [x] Logs and persisted state prove another previously stalled video advances.
- [ ] Any remaining per-video validation failure appears as blocked and no longer
  prevents another video from advancing; retries require the owner's request.
- [x] Record timestamps, revision, affected slugs and before/after evidence in
  `docs/videos/validation/language-queue-recovery.md`, without secrets or media.

## Steps

- [x] Read the parent fix ticket and inspect fresh production state.
- [x] Follow the deploy skill only after explicit owner deployment authorization.
- [x] Observe worker rounds and compare review/project state and language payloads.
- [x] Record acceptance and file any unresolved defects separately.

## How to verify

Use read-only worker logs, `auto.json`, project/review queries, and the review UI.
Check actual successful language delivery plus a later video's progress. Uptime,
HTTP 200, or an accepted retry click alone does not prove recovery.

## Notes

- This ticket is not production deployment, retry, approval, upload or publication
  authorization. The user approved implementation and a draft PR only.
- The parent diagnosis also found 15 Shorts with incomplete QA and local/imported
  videos whose approved reviews have not been pulled by their producing tools.
  Those need their content workflows; deploying this fix does not complete them.
- 2026-09-29 (claude-opus-5-5): the owner asked in chat to redeploy; `716bd5dc`
  (contains #964) went live at 10:08:40 UTC. Within 20 s the Academy language
  batch was accepted (summary 74 characters, full dub reasons still in the
  payload), then ENISA reached its language batch and GPT-6 Sol/Luna assembled
  its video. Evidence: `docs/videos/validation/language-queue-recovery.md`.
- Not observed live: no video hit an invalid language submission after the
  deploy, so the "blocked and the queue keeps moving" path is covered only by
  #964's regression tests (item left unticked for that reason).
- The pre-deploy logs went with the recreated container; before-evidence is the
  parent ticket's 00:44 UTC diagnosis. The Academy YouTube ID is still set, but
  its earlier value was never recorded, so "unchanged" is not provable.
