---
id: 2026-09-28-display-all-paginated-storyboard-contact-sheets
title: Display all paginated storyboard contact sheets in review
status: done
priority: P1
area: web
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T07:31:27Z
created_at: 2026-09-28T07:28:37Z
completed_at: 2026-09-28T07:45:19Z
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

- [x] Every uploaded contact sheet can be inspected in page order before deciding.
- [x] A shot without its individual image points to its sheet when that mapping exists.
- [x] Legacy one-sheet reviews and existing decisions keep working; malformed metadata
      cannot render an unuploaded file or duplicate a page.

## Steps

- [x] Add failing review-card coverage for the paged tool payload and legacy payload.
- [x] Render uploaded sheets and shot-to-page navigation with existing translated labels.
- [x] Verify scoped tests, lint, translations and diff integrity; require latest PR CI before merge.

## How to verify

Run the new storyboard page component tests with admin-video-reviews.test.tsx,
scoped ESLint, npm run check:i18n, npm run check:tasks and git diff --check.

## Notes

- Before the fix: three paged-file cases failed because there were no displayed page
  images; the legacy single-sheet case passed. After the fix: all four pass, plus all
  25 existing review-page tests (29 total). The 95-shot fixture verifies four sheets
  in page order, the retained individual keyframe, all 23 final-page links and read-only
  approval permissions. Other cases cover missing metadata, missing files and duplicates.
- Scoped ESLint, five-locale i18n validation and diff checks passed. Logs are retained
  under test-results/pr895-ui-before-forks.log, pr895-ui-after.log and pr895-i18n.log.
  The first threads run timed out starting its worker, before any tests; local fork
  workers then executed both the negative and corrected runs. No timeout, assertion,
  retry or repository runner setting was weakened. Full typecheck/browser CI and the
  synchronized final head remain merge gates, not claims made by these component tests.

- The collision survey found no open PR touching this component and no checked-out
  video-review-manga-workflow/video-languages branch. The claim tool still sees the
  old review-status tickets video-drama-room-web and video-languages-web. Their work
  landed in PR #870 (main 79e26fcd, confirmed merged at 06:38:47Z); the current main
  component is that implementation. Claim only this narrow follow-up with --force
  under task-board rule 2; do not release, edit or close the other owner's tickets.
- Merged main 210e6fdb locally before editing, then main 55e75518 without conflicts.
  The latter merge did not change either validated component file. A scoped TypeScript
  check of the component, new tests and their imported dependencies passed using the
  repository's strict compiler options; the integrated task check validated 1,016 files.
  Evidence: test-results/pr895-typecheck.log and pr895-main55-tasks.log. The full-project
  CI checks still gate merge. Remote push waits for a slot in the three-PR CI batch and
  the parent design PR #888 to land.
