---
id: 2026-10-22-record-c10-oxo-owner-paid-pilot
title: Record C10 OXO owner paid pilot approval
status: review
priority: P1
area: docs
owner: codex-root-c10-paid-gate
claimed_at: 2026-10-22T17:23:06Z
created_at: 2026-10-22T17:22:48Z
completed_at:
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/reviews/owner-paid-pilot-approval.md
---

# Record C10 OXO owner paid pilot approval

## Why

站主已核准 C10 整支本機試片 US$25 上限；此決定需要與已核准稿件、逐鏡、報價及仍未解除的帳本／TTS 停線綁定，避免把費用核准誤作可立即生成。

## Definition of done

- [x] 對精確稿件、逐鏡與報價雜湊記錄站主決定、最大張數／重試與全費用上限。
- [x] 收據明列預算路由、舊費用歸因、正文 480 秒與 70% 畫面停線；不宣稱已花費或已成片。
- [ ] 草稿 PR 已含收據且遠端讀回。

## Steps

- [x] 讀回站主答案與三份核准稿、報價雜湊。
- [x] 寫入 `reviews/owner-paid-pilot-approval.md`。
- [ ] 提交、推送並更新 PR body；只在遠端讀回後結束本票。

## How to verify

`Get-FileHash` 對稿件、逐鏡及報價；`git diff --check`；`gh pr view 1689 --json body,headRefOid,isDraft`。本收據不觸發媒體 API。

## Notes

C03–C06 舊費用仍未歸因，C10 獨立預算路由仍待實證。US$25 核准只是一個上限，不是可花餘額。
