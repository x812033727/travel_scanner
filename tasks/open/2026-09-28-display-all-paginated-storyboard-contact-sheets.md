---
id: 2026-09-28-display-all-paginated-storyboard-contact-sheets
title: Display all paginated storyboard contact sheets in review
status: in-progress
priority: P1
area: web
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T07:31:27Z
created_at: 2026-09-28T07:28:37Z
completed_at:
branch: codex/pr895-storyboard-pages
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-storyboard-pages.test.tsx
---

# Display all paginated storyboard contact sheets in review

## Why

PR #895 sends long storyboards as several contact sheets and keeps every shot in the
payload, but StoryboardBody only displays the old contact_sheet role. A 95-shot story
can therefore reach its approval screen with almost every image invisible.

## Definition of done

- [ ] Every uploaded contact sheet can be inspected in page order before deciding.
- [ ] A shot without its individual image points to its sheet when that mapping exists.
- [ ] Legacy one-sheet reviews and existing decisions keep working; malformed metadata
      cannot render an unuploaded file or duplicate a page.

## Steps

- [ ] Add failing review-card coverage for the paged tool payload and legacy payload.
- [ ] Render uploaded sheets and shot-to-page navigation with existing translated labels.
- [ ] Verify scoped tests, lint, task integrity and the final PR CI.

## How to verify

Run the new storyboard page component tests with admin-video-reviews.test.tsx,
scoped ESLint, npm run check:i18n, npm run check:tasks and git diff --check.

## Notes

- The collision survey found no open PR touching this component and no checked-out
  video-review-manga-workflow/video-languages branch. The claim tool still sees the
  old review-status tickets video-drama-room-web and video-languages-web. Their work
  landed in PR #870 (main 79e26fcd, confirmed merged at 06:38:47Z); the current main
  component is that implementation. Claim only this narrow follow-up with --force
  under task-board rule 2; do not release, edit or close the other owner's tickets.
- Merged main 210e6fdb locally before editing. No remote push or CI restart yet.
