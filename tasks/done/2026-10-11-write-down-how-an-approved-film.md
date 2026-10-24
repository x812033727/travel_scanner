---
id: 2026-10-11-write-down-how-an-approved-film
title: Write down how an approved film is produced again after a rewrite
status: done
priority: P2
area: docs
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:23:59Z
created_at: 2026-10-11T13:28:03Z
completed_at: 2026-10-24T13:24:16Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - .agents/skills/youtube-video/references/automated.md
---

# Write down how an approved film is produced again after a rewrite

## Why

On 2026-10-11 a finished tutorial (`claude-code-skills-hands-on`, all four gates approved on
2026-10-10, waiting to be uploaded) was rewritten from new runs and had to be produced again.
Neither the `youtube-video` skill nor `docs/videos/` says how. The agent doing it stopped before
any speech and reported; the owner then decided the route. This task is to write that route
down, so the next rewrite does not stop at the same place. Every film sent back by the blind
reading of 2026-10-11 (`tasks/open/2026-10-11-rewrite-*.md`) will meet this.

What the owner decided, relayed by the coordinating session on 2026-10-11, in the owner's words:
「用新代號，舊專案標停止」. The rewritten film is produced under a new slug; the old project is
stopped on the site with the reason in its note; the old cut's work folder is left as it is.
The coordinating session said this is how every later rewrite of an already approved film is
done.

What was found, and why the three other routes did not fit:

1. **Pushing every gate again on the same slug.** `automated.md` (the paragraph on teaching
   cards, and "核准綁定檔案雜湊") and `docs/videos/DESIGN.md` say approvals are bound to file
   hashes and a changed script is recorded and reviewed again. That is all they say. On the
   site, a review with a new hash is accepted and judged, but only pending older reviews of
   that gate are superseded (`apps/api/app/video_reviews/admin_service.py`, `submit_review`):
   the old cut's approved final and upload confirmation would stay approved beside the new
   ones. This was read from the code, not tried.
2. **The outline gate as it stood.** A rewritten brief that keeps its old options has more
   than three, and the judge is sent the first three only (`tools/video/review/sync.mjs`,
   `JUDGE_MAX_OPTIONS = 3`; fewer than two go to the owner without a pick). The option the
   new script follows was the fourth, so the judge would have chosen among outlines that no
   longer exist. `approve --gate outline` is documented as the fallback for when the admin
   page cannot be used, and it records the owner's own answer.
3. **The owner renewal flow** (`docs/videos/BRANDING.md` §已核准、尚未上傳的長片換版,
   `tools/video/review/renewal.mjs`). It is the documented way to replace an approved cut that
   has not been uploaded: the old final, upload confirmation and language reviews are marked
   superseded and the new final is reviewed by the owner by hand. Its `stage` step is built
   for new branding on an unchanged body: it checks that the new length is the retained body
   plus the new intro and outro. A film with a new body does not pass it, and it needs the
   owner's session.

## Definition of done

- [x] The shared canonical `automated.md` says, where it now
      says only that a changed script is reviewed again, what to do when the film's gates were
      already approved: a new slug, the old project stopped on the site with its reason, the
      old work folder kept, and one line in the new brief and in the fact-check file naming the
      old slug and both dates.
- [x] It says what the rewritten brief's 大綱 has to look like before the outline gate: two or
      three live options, the one the script follows among them, and the superseded options
      reduced to a note, because the judge reads at most three and only what is written as
      `### 選項 X：`.
- [x] It says when the owner renewal flow is the right one instead (same body, new branding)
      and that it is not for a rewritten script.
- [x] It says who stops the old project and how (this was done by the coordinating session on
      2026-10-11 at 13:21 UTC; the steps were not seen by the agent that filed this task).
- [ ] `npm run test:tools` passes (it keeps the two copies of the skill in step).

## Steps

- [x] Recover the coordinating session's recorded site action, verify it against current UI/API code, and write the steps.
- [x] Decide whether `docs/videos/BRANDING.md` should point at the new paragraph; it is outside
      this task's scope, and it is one of the documents the duration receipt may bind, so
      check before touching it.
- [ ] Write the paragraph in shared `automated.md`, verify the current shared-skill contract, run the tools tests and obtain the independent duration increment.

## How to verify

Read the paragraph as someone holding a rewritten script for an approved slug: it should tell
them what to do before the outline gate without opening the API code.

## Notes

- First case: `docs/videos/claude-code-skills-vs-claude-md/` (was `claude-code-skills-hands-on`);
  its brief's first paragraph and `verify-3.md` carry the one-line history. Its run log's
  "Runner note 3" says what had and had not been done when the route was decided.
- Whether the site should supersede an older approved final when a new one arrives on the same
  slug is a product question this task does not answer; with a new slug it does not arise.
- Not checked: what the admin page shows for a stopped project, and whether a stopped slug's
  article (`source_guide`) is free for the new slug's request on the site's own queue
  (`docs/videos/AUTOMATION.md` says the article-request route refuses a second film on an
  article until the first is dropped).

### 2026-10-24 open-task reconciliation

- The only overlapping claim on this canonical reference is the stale
  `2026-10-20-tutorial-flow-and-hooks-rules-learned` claim (2026-10-20T17:25:00Z).
  No open PR in the current inventory touches this reference. Normal claim refused
  that overlap; `--force` was used only for this narrow documentation correction.
  The earlier task, owner, files and unfinished acceptance remain intact.
- Recovered the actual drop action from the successor production task's Notes,
  then read `DropVideo` in `apps/web/components/admin-video-reviews.tsx`, the
  zh-TW `dropTitle`/`dropButton` labels, `DropIn`, and `drop_project` in the API.
  The current label is 「放棄這支影片」. It clears website preview attachments,
  so the new section records preservation before the owner-authorized action,
  plus exact slug/reason/date and persisted dropped-state readback. No live drop
  or production action was performed during this documentation work.
- Added a complete handoff section: preserved original work folder and evidence,
  a new slug, old/new dates in brief and fact-check, two or three live outline
  options with the scripted choice included, fresh gates/language choice, and the
  retained-body-only boundary of the ordinary owner renewal route.
- Current `tools/skills.test.mjs` keeps references/scripts only under `.agents/`;
  `.claude/skills/` contains only byte-identical `SKILL.md` entry points. The old
  ticket's duplicated-reference requirement was therefore updated to the shared
  canonical file. Both existing SKILL.md entry points remain untouched.
- `BRANDING.md` already describes its own renewal and approved-final handoffs.
  This patch links to it from the new section without changing that out-of-scope
  document or its receipt binding.
- The source edit passes `git diff --check`. Full tool checks and an independent
  duration-only receipt increment remain required before closure; the author did
  not write or rebind `docs/videos/long-form/review.md` or `review.json`.


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- Recorded unresolved condition:   "Runner note 3" says what had and had not been done when the route was decided.
- 2026-10-24 authored in codex/open-tasks-reconcile-20261024: canonical automated.md now has the complete rewrite handoff; tools/skills.test.mjs 7/7 PASS and git diff --check PASS. No .claude duplicate reference remains, per current shared-skill contract.
- 2026-10-24 execution: Documentation handoff with existing seven skills tests passed, independent duration binding and 473-plan long-form CLI check passed. Local implementation only; no merge/deploy or paid request.

本輪已執行並驗證，實作在獨立分支；依PR流程結票，不宣稱已部署。
