---
id: 2026-10-25-final-review-dub-downloads
title: Expose checked dub attachments on final review downloads
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-25T16:33:17Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
---

# Expose checked dub attachments on final review downloads

## Why

The native final submission already attaches current checked `dub_<locale>` M4A
files, but `FinalBody` renders no download links for them. `LanguagesBody` only
renders tracks on languages/dubs reviews, which cannot be submitted until the
source final is approved. The owner explicitly requested direct backend audio
delivery and delegated production decisions, so stored blobs must be accessible
without confusing them with formal batch readiness or YouTube upload.

## Definition of done

- [ ] A final-review card displays each attached checked dub with a human locale label and an exact `<locale>.m4a` download name, including while that review is pending.
- [ ] Source-final approval, language batch binding and YouTube upload states remain unchanged by the download UI.
- [ ] Existing final cards without dub attachments retain their behavior.

## Steps

- [ ] Read existing final submission/dub roles and generic file download routes.
- [ ] Add the download UI for final `dub_*` attachments without changing producer permissions or auto-approval.
- [ ] Add regression coverage for pending final cards with eight dub files, filename/route correctness and no state changes.

## How to verify

Use a native-shaped pending final review with eight `dub_<locale>` files and
verify all eight authenticated download links. Run the affected web tests,
typecheck and i18n checks if new labels are necessary.

## Notes

- Observed in `openai-dns-containment` on 2026-10-25: all eight actual encoded tracks passed80/80 checks, native final submission stored all eight `dub_*` roles, but the existing final card does not render them.
- Concrete temporary delivery uses additional `evidence_<locale>_m4a` aliases for the same checked blobs in the existing generic final evidence download list. The original QA and pending approval are preserved; no languages/dubs gate is used as a bypass. The proper UI should make those aliases unnecessary.
- This ticket is unclaimed. Do not alter another active task's component scope without the normal collision check.
