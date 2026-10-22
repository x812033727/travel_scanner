---
id: 2026-10-22-independently-review-c17-nalgene-treatment-sources
title: Independently review C17 Nalgene treatment sources
status: review
priority: P2
area: docs
owner: codex-c17-independent-sources
claimed_at: 2026-10-22T18:57:55Z
created_at: 2026-10-22T18:57:49Z
completed_at:
branch: codex/brand-story-nalgene-c17
depends_on: []
scope:
  - docs/videos/brand-story-independent-reviews/C17-nalgene-20261023.md
  - tasks/open/2026-10-22-independently-review-c17-nalgene-treatment-sources.md
---

# Independently review C17 Nalgene treatment sources

## Why

站主尚未採用 C17《Nalgene》企劃。作者稿需要由不同代理重開一手材料，逐項確認實驗器皿、戶外用途和材料更替的時間線，並把結果綁在當前 Treatment／來源矩陣雜湊。審查只寫獨立收據，不修改作者稿。

## Definition of done

- [x] S1–S7 可讀原件重開，M01–M12 逐項列出來源、適用邊界和精確問題。
- [x] 收據綁定作者兩檔 SHA-256，清楚區分來源 PASS 與待修 HOLD；不冒稱站主企劃核准。
- [x] 收據與票提交至草稿 PR #1699，讀回 head、draft 和 no-auto-merge。
- [x] 作者窄修後以新兩檔 SHA-256 覆核五處來源定位替換；PASS 附記提交至同一草稿 PR。

## Steps

- [x] 核對作者稿與現有認領；只認領獨立審查檔及本票。
- [x] 逐一重開公司／供應商原件及轉刊公司公告，核對 1949、1960s、mid-1970s、2008、2020 與現行 FAQ。
- [x] 寫雜湊綁定的 M01–M12 審查收據，標明 2019 年公司稿「標題」定位的錯誤。
- [x] 跑 task／diff 檢查、提交推送並讀回草稿 PR。

## How to verify

重算 `docs/videos/story-everyday-nalgene-c17/treatment.md` 與 `source-matrix.md` 的 SHA-256；對照審查收據與 S1–S7 原件；跑 `npm run check:tasks`、`git diff --check`；`gh pr view 1699 --json headRefOid,isDraft,labels,body` 讀回。來源問題修正後須以新 SHA 做窄幅獨立覆核，不能把舊 PASS 當新稿 PASS。

## Notes

2026-10-23：來源主線已核對；Treatment 與矩陣把 2019 原廠稿「水瓶 1949 debut」說成**標題**，實際在開頭導語，正式標題不含 1949。這是精確來源定位問題，見審查收據；其餘 M 項按收據界線可用。沒有編修 Treatment、付費、匯入、合併、上傳或發布。

2026-10-23：作者 head `2f3fbcd500f5e0cc345b286739addd6943f5eeab` 把三處實質定位與兩處審稿提示的「標題」改為「開頭導語」。新 Treatment SHA-256 `0451192DAA6EDF85CFD8721674511B6DBDBC671A73AC720B0BCEDFB9E14C1E07`，矩陣 SHA-256 `892041F854DCF4FBFFF37BFE90AC6B1AA02647CBD146CB2262F7A2E47FAC316E`；與舊版逐位元組比對只見這五處，S2 重新讀取證實位置正確。差異覆核 PASS，見收據附記。站主企劃採用仍另待核准；PR body 編輯遭自動審查 `blocked by policy`，不改走其他方式重試。
