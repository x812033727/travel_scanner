---
id: 2026-10-02-create-borrowed-dawn-in-the-production
title: Create Borrowed Dawn in the production admin
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-02T08:42:04Z
completed_at:
branch:
depends_on:
  - 2026-10-02-import-long-anime-plans-as-paused
scope:
  - docs/videos/import-receipts/borrowed-dawn.json
---

# Create Borrowed Dawn in the production admin

## Why

The owner requested a real admin work after the planning package was merged in PR #1113. The paused anime import implementation is prepared in a separate PR, but nothing has been written to the production database. Cloud SSH to 187.127.118.6:7788 was refused; the owner is testing access locally. Keep the operational completion visible until it is proved by production readback.

## Definition of done

- [ ] After the import-support PR is merged and deployed, the authenticated admin can read borrowed-dawn as an anime planning series with a 22-minute body, ensemble, twelve review documents and 120 planned episodes.
- [ ] The exact source bundle is preflighted and atomically applied by an active administrator, with one audit record and no production requests, videos or worker job.
- [ ] A sanitized receipt outside the source package records the deployed revision, bundle SHA, preflight/apply/readback results and admin route; it contains no credentials, private keys or administrator email.

## Steps

- [ ] Confirm the imported support and migration are deployed through the existing release workflow.
- [ ] Follow docs/videos/ANIME-PLANNING-IMPORT.md: prepare, preflight, apply the exact hash and read back unchanged records.
- [ ] Verify the authenticated admin page and record the sanitized production evidence.

## How to verify

Use the exact CLI commands in docs/videos/ANIME-PLANNING-IMPORT.md. After apply, repeat the read-only preflight and require action=unchanged, category=anime, status=paused, planning_only=true, documents=12 and episodes=120. Open /zh-TW/admin/videos?tab=drama&series=borrowed-dawn. Confirm the source specification and both tension events per episode remain available and no production actions are enabled.

## Notes

The current owner instruction is to open the support PR. This ticket records the remaining host action, not permission to merge or deploy the PR. Local isolated PostgreSQL evidence is not production evidence. Keep any receipt outside docs/videos/series-plans/borrowed-dawn so the validated flat source package remains unchanged.

Full 22-minute screenplay/media production remains tracked separately by 2026-10-02-anime-long-episode-support.
