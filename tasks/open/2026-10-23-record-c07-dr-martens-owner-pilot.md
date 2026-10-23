---
id: 2026-10-23-record-c07-dr-martens-owner-pilot
title: Record C07 Dr Martens owner pilot approval
status: in-progress
priority: P1
area: docs
owner: codex-root-c07-approval
claimed_at: 2026-10-23T03:20:57Z
created_at: 2026-10-23T03:20:51Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/owner-paid-pilot-approval.md
---

# Record C07 Dr Martens owner pilot approval

## Why

站主已另行核准 C07 本機試片的整支 US$25 上限；須把決定綁定現有稿件、逐鏡與整支報價，並明確保留預算歸因、實測時長及上傳發布的不同關卡。

## Definition of done

- [x] 獨立於劇本核准的站主付費上限決定有精確雜湊收據，且未把核准當作可立即支出的餘額。

## Steps

- [x] 讀回 PR #1680、已核准稿件與整支報價的內容雜湊。
- [x] 記錄站主決定及未解除的付費前停線，保留草稿與 no-auto-merge。

## How to verify

`Get-FileHash` 核對 `script.md`、`visual-plan.md`、`production-quote.md`；`git diff --cached --check`；`gh pr view 1680 --json headRefOid,isDraft,labels` 讀回。

## Notes

現行 C07 單集預算路由仍缺，`tasks/open/2026-10-22-guard-c07-dr-martens-paid-pilot.md` 未完成；舊費用歸因與實際 TTS 正文 ≥480 秒亦未驗證。本票只記錄授權，不發出付費請求。
