---
id: 2026-10-01-vps-db-settings-runbook
title: Align VPS uploader setup and rollback docs with database settings
status: done
priority: P2
area: docs
owner: codex-b10e-vps-docs
claimed_at: 2026-10-01T01:31:13Z
created_at: 2026-10-01T01:26:57Z
completed_at: 2026-10-01T01:41:01Z
branch: codex/vps-settings-browser-acceptance-20261001
depends_on: []
scope:
  - docs/videos/VPS-UPLOADER.md
---

# Align VPS uploader setup and rollback docs with database settings

## Why

Main `76b39a25` adds database-backed VPS connection settings, but the same
runbook still describes environment removal as disabling the website uploader
and stopping the old service before clearing its configuration. A saved DB row
takes precedence, and normal disable/connection changes must authenticate with
the existing service and verify an empty queue. Following the old instructions
can leave the website enabled or make the guarded settings update impossible.

## Definition of done

- [x] Environment settings are explicitly a fallback before a DB setting is saved;
      saved settings apply immediately and an explicit DB disable does not fall back.
- [x] Normal disable/switch steps keep the original service available until its
      authenticated `active_jobs == 0` check and settings save succeed. Stop the old
      instance only when disabling or switching to another service; for same-service
      channel/secret corrections, test the saved connection under the approved plan.
      Preserve volumes and the existing approval gate.
- [x] Emergency stop explains the subsequent empty-queue verification limitation,
      without bypassing the guard, editing the DB directly or risking a second upload.
- [x] Same-host operations consistently retain both Compose files and the existing
      owner approval, login and real upload acceptance requirements.

## Steps

- [x] Audit scope collisions before claiming the documentation file.
- [x] Reconcile deployment, activation, legacy environment and rollback sections
      against the merged settings service.
- [x] Review the final runbook and validate task records.

## How to verify

Read `apps/api/app/video_youtube/vps_settings.py`: DB precedence at lines 150–159,
disabled handling at 181–183, old-service empty-queue guard at 282–295 and DB save
at 298–299. Check all setup/rollback paragraphs for contradictions, keep shell
commands as unexecuted templates, and run `npm run check:tasks`. No production
operation is needed or authorized by this documentation task.

## Notes

- Found during the approved offline refresh of the VPS live acceptance plan.
  The existing live acceptance and local browser acceptance tasks did not record
  this documentation defect, so it is filed separately with one-file scope.
- 2026-10-01: The coordinating agent confirmed the single-file collision check
  before the normal claim. Read the full runbook and current `vps_settings.py`;
  the relevant runbook blob is unchanged between `76b39a25` and main `5e65606c`.
  Reconciled initial activation, legacy fallback, normal versus emergency stop,
  same-host Compose commands and secret handling with the merged implementation.
  A connection test writes diagnostics; it is not presented as a read-only check.
- Independent review correction: the stop step now applies only to disabling or
  moving to another service. Same-service channel correction or secret rotation
  instead verifies the saved connection under the approved plan. Re-read the guard
  in `vps_settings.py` and the mistyped-channel correction regression at
  `tests/test_video_youtube_vps_settings.py:196`; no service action or test was run.
- Only documentation and this task's handoff were edited. No production access,
  configuration save, login, upload, tests or service operations were performed.
  Independent review and the coordinating agent's source reconciliation passed
  after limiting the old-service stop to disable or service switches. Same-service
  channel correction or secret rotation now retains the active service and follows
  its approved connection verification plan. `check:tasks` validated 1,227 records
  and `git diff --check` passed. This documentation correction is complete in the
  draft change; merge, production configuration and live acceptance are separate.
