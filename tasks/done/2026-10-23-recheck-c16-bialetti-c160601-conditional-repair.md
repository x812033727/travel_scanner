---
id: 2026-10-23-recheck-c16-bialetti-c160601-conditional-repair
title: Recheck C16 Bialetti c160601 conditional repair
status: done
priority: P1
area: docs
owner: codex-c16-v4-delta-review
claimed_at: 2026-10-23T05:39:23Z
created_at: 2026-10-23T05:39:17Z
completed_at: 2026-10-23T05:40:40Z
branch: codex/c16-bialetti-v4-delta-review
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/c16-v4-delta-review.md
---

# Recheck C16 Bialetti c160601 conditional repair

## Why

作者在獨立 PR #1733 對 `c160601` 的 HOLD 後，只改旁白為再次使用的條件句。需以新 head 原始 bytes 重核這句與 M06 館方來源、前後章節及未變配鏡；舊 PASS/HOLD 都不可直接套用。

## Definition of done

- [x] 留下綁定新 head 與四份 SHA-256 的非作者差異 PASS／HOLD 收據。
- [x] 確認新句來源安全、接住 c160519，且 81 句／鏡及兩種視覺檔逐欄相符。

## Steps

- [x] 在作者工作樹只讀比較 `09e24dc` 與 `a285312`，重開 M06 國立 Museo Omero 原頁。
- [x] 核對旁白、來源註記、原配鏡與全套 ID；寫獨立差異收據。

## How to verify

收據 `docs/videos/story-everyday-bialetti-c16/reviews/c16-v4-delta-review.md`。`git show a285312:<path>` bytes 的 SHA-256、Python 81/81 ID／Markdown／JSON 斷言；`npm run check:tasks` 與 `git diff --cached --check`。

## Notes

新 head `a2853124dce795df65d2a42b522084bb72144438`：`c160601` 條件句及原配鏡 PASS，合併前輪精確未變部分，81/81 來源與配鏡文字 PASS。原 Museo Omero 頁 HTTP 200，確認旋合開閉、下水室、咖啡粉漏斗及加熱水路；不提供具體家庭隔日紀錄。兩位新版旁白盲讀與站主／付費關卡仍開。作者工作樹和舊審查工作樹的政策阻擋重複任務均未觸碰。

`npm run check:tasks` 在 `done` 前 exit 0（2,082 檔，既有警告）。`done` 留下本工作樹新建的未追蹤 `tasks/open` 副本；前輪同型精確刪除被政策擋下，本輪不重試。PR 只提交此 `tasks/done` 檔及收據。
