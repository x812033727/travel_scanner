---
id: 2026-10-05-life-ai-head-to-head-office
title: "Life batch: AI office productivity (6 articles)"
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-05T08:44:15Z
created_at: 2026-10-05T02:52:28Z
completed_at: 2026-10-06T13:35:08Z
branch: claude/determined-clarke-1laipc
depends_on: []
scope:
  - apps/api/app/guides/content/ai-official-documents-taiwan.json
  - apps/api/app/guides/content/ai-proposal-writing.json
  - apps/api/app/guides/content/ai-proofreading-terminology.json
  - apps/api/app/guides/content/ai-sop-manual-writing.json
  - apps/api/app/guides/content/ai-survey-design-analysis.json
  - apps/api/app/guides/content/ai-interview-preparation.json
  - apps/web/public/guides/ai-official-documents-taiwan
  - apps/web/public/guides/ai-proposal-writing
  - apps/web/public/guides/ai-proofreading-terminology
  - apps/web/public/guides/ai-sop-manual-writing
  - apps/web/public/guides/ai-survey-design-analysis
  - apps/web/public/guides/ai-interview-preparation
  - docs/life-ai-office-productivity
---

# Life batch: AI office productivity (6 articles)

## Why

The owner asked for office-productivity subjects like the reference site's. The six first
planned (Excel, email, meeting notes to tasks, weekly reports, slides, document rewriting)
are already on the site (`chatgpt-for-excel-formulas`, `ai-spreadsheet-automation`,
`ai-email-management`, `chatgpt-for-email-writing`, `ai-meeting-notes-tools`,
`gemini-workspace-meeting-handoff`, `ai-weekly-review-templates`, `ai-slides-generation-tools`,
`gemini-in-gmail-docs-sheets`), so this batch takes six real gaps instead. The six hands-on
head-to-heads this ticket also named moved to `2026-10-05-ai-head-to-head-hands-on`: they need
real accounts to test honestly. Spec: `docs/life-ai-office-productivity/README.md`.

## Definition of done

- [x] Six zh-TW packs: official documents (公文、簽呈), proposals, proofreading and terminology,
      SOPs, survey design and open answers, interview preparation. Each has a self-drawn hero, a
      diagram, at least 3 h2s, a table, sources checked 2026-10-05 and internal links.
- [x] No hands-on test results or scores; legal points (公文程式條例, 文書處理手冊, 個資法,
      就業服務法) cite the law database or the authority.
- [x] `intake_check.py --from-content` 0 FAIL x 6; `pack_cli lint --kind life` no finding for
      these slugs; `tests/test_guides_content_pack.py` green.
- [ ] Published on mokaair.com (needs the owner's go-ahead, with the twelve of the AI income
      batch: same `guides-import --slug ... --locale zh-TW` steps).

## Notes

- Same workflow as the AI income batch: writer, two independent fact-check rounds (3-10 then
  0-3 factual corrections), mechanical and visual gate, cross-check. The cross-check caught
  Microsoft's rename of Microsoft 365 Copilot to Microsoft Copilot (confirmed by the
  coordinator on learn.microsoft.com) and redrew one hero that echoed a previous batch's.
- Records per article in `docs/life-ai-office-productivity/records/<slug>/`, and
  `CROSS-CHECK.md`.

- Closed by claude-opus-5-5-train-1323-1324-1268 in the train for #1323, #1324 and #1268
  (the claim was over 24 hours stale and the branch work is complete). The unticked production
  step moved to `2026-10-06-publish-the-eighteen-life-ai-articles`.
