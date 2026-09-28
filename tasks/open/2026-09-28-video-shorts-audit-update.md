---
id: 2026-09-28-video-shorts-audit-update
title: Video shorts O1: bring the YouTube API audit application in line with automatic Shorts publishing
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T04:10:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/YOUTUBE-API-AUDIT.md
---

# Video shorts O1: bring the YouTube API audit application in line with automatic Shorts publishing

## Why

未通過稽核的專案用 API 上傳的影片一律鎖成私人，所以 Shorts 要做到「連上傳都自動」，非過稽核不可。申請書的草稿（`docs/videos/YOUTUBE-API-AUDIT.md`，2026-09-27）是照長片的做法寫的，裡面有幾句話在 Shorts 全自動之後不再成立：

- 「站主看過成片、決定上架時間，沒有這個決定，影片不會進頻道」——全自動之後站主是事前授權、照月曆排程，不是逐支決定。
- 「每週幾支、一天最多幾支」——Shorts 是一天一到兩支、90 天 120 支。
- 沒有提到讀取統計數字；隱私權政策的段落寫的是「只存取影片、字幕與影片資訊」。

申請書寫的必須是實際的做法。送件之後才改用途，依政策要重新申報。

設計全文在 `docs/videos/SHORTS.md`（§上架、§成效與每週報告、§政策與依據、§還要站主決定的事 第 4 項）。

## Definition of done

- [ ] 第 3 段的組織說明（英文照抄版與中文對照）改寫：Shorts 的製作方式、事前授權的內容與範圍、月曆排程、站主隨時可以改、抽掉、暫停與撤回、網站永遠不把影片直接設成公開。
- [ ] 第 5 段的用量：每天的請求數與配額重算（一天兩支 Shorts 加原本的長片），仍然不申請高於預設的配額。
- [ ] 端點清單補上讀取統計數字用到的方法與 YouTube Analytics API。
- [ ] 第 5 段的用途加選「Analytics & Reporting」，並說明要算的指標（同系列影片之間的比較，用來決定下週做什麼）；這是接受衍生指標增修條款的方式（`developers.google.com/youtube/terms/derived-metrics-policy`）。站主不想要這個用途的話就不選，後台照樣只顯示原值。
- [ ] 隱私權政策的段落（五種語言）補上：網站會讀取自己頻道影片的統計數字、保存多久、怎麼刪除。
- [ ] §五「送出之後要一直守的規則」補上兩條：不得用 API 的數字算衍生指標（成效區只顯示原值）；自動上傳要有事前、具體、明示的同意（授權卡）。
- [ ] 附件清單補上：自動上架授權卡的截圖、月曆的截圖、成效區的截圖。
- [ ] 文件開頭寫清楚兩種送法的取捨，讓站主選：照全自動的做法送；或先照原稿送、通過之後再申報用途變更（那樣在變更之前 Shorts 不能自動上傳）。

## Steps

- [ ] 重讀開發人員政策與稽核表單（頁面可能改版；記下讀取日期）。
- [ ] 改寫上面各段；個資一律留【站主填】，repo 是公開的。
- [ ] 站主選定送法之後，把決定記在文件的送出紀錄與這張票。

## How to verify

站主讀過改寫後的申請書，確認每一句都跟後台實際的做法一樣。

## Notes

- 同一份文件也是開著的票 `2026-09-26-video-hands-off-api-audit` 的 scope（那張票在等站主送件）。兩張票不要同時有人做；先做這張的人在那張票的 Notes 留一句。
- 截圖要等 W1 與 Y1 上線才截得到。
- 這張票不送件、不代替站主做任何決定。
