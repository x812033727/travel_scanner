---
id: 2026-10-23-record-c14-camelbak-owner-script-approval
title: Record C14 CamelBak owner script approval
status: in-progress
priority: P1
area: docs
owner: codex-root-c14-approval
claimed_at: 2026-10-23T03:22:11Z
created_at: 2026-10-23T03:22:02Z
completed_at:
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/reviews/owner-script-approval.md
---

# Record C14 CamelBak owner script approval

## Why

站主已核准 C14《CamelBak》v8 的 70 句劇本與 70 鏡方向；收據須綁定同一份完成獨立來源／配鏡查核及雙盲讀的作者檔，並保留 TTS 和付費關卡。

## Definition of done

- [x] 站主決定以四份作者檔 SHA-256 固定，與付費、時長、成圖及發布權限分開。

## Steps

- [x] 讀回 PR #1695、v8 作者檔及獨立／盲讀收據。
- [x] 記錄核准內容、版號與未完成關卡。

## How to verify

`Get-FileHash` 核對四份作者檔；`git diff --cached --check`；`gh pr view 1695 --json headRefOid,isDraft,labels` 讀回。

## Notes

正文 496.5 秒與插圖 75.19% 都只是紙上規劃；正常語速 TTS、成片畫面時間及整支報價尚未完成。本票不付費。
