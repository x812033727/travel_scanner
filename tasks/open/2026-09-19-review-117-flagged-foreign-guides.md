---
id: 2026-09-19-review-117-flagged-foreign-guides
title: Review the 117 introductions the foreign-place rule flagged beyond the vetted 52
status: review
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-19T08:32:20Z
created_at: 2026-09-19T08:01:09Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - docs/catalog-content-reviews/2026-09-19-foreign-guides-unreviewed.json
  - docs/catalog-content-reviews/2026-09-19-foreign-guides-keep-ids.txt
  - docs/catalog-content-reviews/2026-09-19-foreign-guides-review.md
---

# Review the 117 introductions the foreign-place rule flagged beyond the vetted 52

## Why

On 2026-09-19 `guides-foreign-place-scan` (PR #559) read all 6,061 approved hotspot introductions
and flagged 165 as describing another country. The owner chose to reject only the 52 that
`2026-09-13-reject-public-guides-about-another-country` had checked by hand; the other **117 are still
approved and public**. They were never read one by one.

A glance says most are genuinely misplaced: Busan's 國際市場 carries JNTO statistics about the
"Japan market", Huế's 孝陵 and 场钱桥 carry Taiwan travel blogs, Sapporo's 圓山公園 carries Taipei's
Yuanshan. But the rule also misfires: `6da32c2d` is NAVITIME's page for the Shibuya MEGA Don Quijote
itself, flagged as Thailand. Rejecting all 117 blind would remove good content with the bad.

By country of the hotspot: 韓國 50, 越南 41, 台灣 15, 日本 11. The full list, with title, URL, locale
and the rule's reason, is `docs/catalog-content-reviews/2026-09-19-foreign-guides-unreviewed.json`.

## Definition of done

- [x] Every one of the 117 is marked in the JSON as `reject` or `keep`, with a one-line reason for each `keep`.
- [ ] The `reject` rows are rejected on the host and no longer public; the `keep` rows stay approved.
- [x] Rule misfires that repeat (a shape, not a single row) are written down for whoever tunes `foreign_place`. （2026-09-19：見 `2026-09-19-foreign-guides-review.md` 的三種誤判形狀，另開票 `2026-09-19-foreign-place-reason`。）

## Steps

- [x] Read each row: open the URL when the title is not conclusive; judge against the hotspot, not the city.
- [x] Put the `keep` ids in a skip list and run the scan with `--skip-ids-file`, list only, to confirm the
      remaining findings are exactly the `reject` rows. (Skip list written; the confirmation run itself is the
      owner's, on the host — commands in `2026-09-19-foreign-guides-review.md`.)
- [ ] With the owner's go-ahead, run the same command with `--apply --actor-email` (see the host commands in
      `docs/catalog-content-reviews/2026-09-13-misplaced-guides.md`), then re-run list-only and expect 0.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-foreign-place-scan --skip-ids-file <keep-list>
```

After the apply this lists nothing.

## Notes

- `eff4dc8f-6ea0-4392-abed-f7bf7d6e0e72` (Funliday's 西公園 page under Fukuoka) was already skipped on
  2026-09-13 and is not among the 117.
- The scan counts each (guide, locale) once; the same article can appear under two hotspots.

### 2026-09-19 逐筆判讀（claude-fable-5-1）

- 117 筆全部看過：**reject 115、keep 2**。依景點所在國：韓國 50/0、越南 40/1、台灣 15/0、日本 10/1（reject/keep）。
- 寫回 `docs/catalog-content-reviews/2026-09-19-foreign-guides-unreviewed.json`：每列加 `verdict` 與 `verdict_reason`
  （規則原本的 `reason` 沒動，所以是新欄位而不是覆寫）。
- 新檔：`docs/catalog-content-reviews/2026-09-19-foreign-guides-keep-ids.txt`（`--skip-ids-file` 用；2 筆 keep +
  `eff4dc8f`）與 `docs/catalog-content-reviews/2026-09-19-foreign-guides-review.md`（計數、三種規則誤判的形狀、
  主機指令：list-only 預期 115 → `--apply --actor-email` → list-only 預期 0）。
- keep：`6da32c2d`（NAVITIME 的澀谷店頁，摘要的「タイ」誤判為泰國）、`c4706b00`（hoiana 的會安古鎮文章，因「日本橋」
  誤判為日本）。後者原網址已 404、同文搬到英文 slug，死連結另開票處理，不在本票範圍。
- 開頁 8 次（UA `Mokaair-editorial/1.0`、間隔 1.5 秒）：NAVITIME 403、hoiana 原網址 404，其餘 200；影片依標題判。
- 沒把握、靠開頁才定的 reject：`e588910e`（韓國觀光數據實驗室的泰國市場動向報告）、`d469749d`／`c7aac200`（觀光署的
  台北指南宮頁）、`c039721a`（觀光署景點總覽）、`94f810a9`（JETRO 觀光市場分析）——理由都在 `verdict_reason`。
- 第 2 個 Step 的確認跑（`--skip-ids-file` list-only = 115 筆）與第 3 個 Step 的 `--apply` 都在主機上，由站主執行；
  這台機器沒有正式站。
