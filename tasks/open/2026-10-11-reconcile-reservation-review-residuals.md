---
id: 2026-10-11-reconcile-reservation-review-residuals
title: 核對訂位審核殘項：店家編輯身分競態與 TABLES／沁園春來源事實
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T13:46:06Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-reservation-review-residuals.md
---

## Why

原分支 `codex/food-reservation-platforms` HEAD `59f4b994533554509ec2dd90d0f7139acf8030a9` 的產品功能已由 PR #392 合併。後續 PR #408 完成原 296 家未連結店的 311 列查核，PR #397 修正 dot-ID，#428/#434 完成後續平台拓展；舊 309/296 研究數、SevenRooms/inline canonical link 和 priority-entry holds 已有具體替代結果，不應再列未完成研究。本票只保留原 `2026-09-11-merchant-reservation-enrichment`／收據中沒有對應結案證據的三項：Maisen 搜尋列曾開出 Thipsamai 對話框（存檔前發現）、TABLES 日期性停業通知與後續營運來源，以及沁園春原店 129→137 Taiwan Boulevard 臨時搬遷的 merchant/source 事實。原觀察不等於現在仍有 bug 或仍停業。

## Done when

- [ ] 在目前 editor 查找已修正收據，或以無正式寫入 fixture 重現 rapid-search 的 row/dialog identity；Maisen、Thipsamai、dialog merchant ID 与選中列應全程一致。記錄是否重現、序列與 SHA；若可重現另開最小 source/test 票，本票不代改 editor。
- [ ] 逐來源比較 TABLES Coffee Bakery&Diner 原平台的 `2026-07-31` closure notice 與目前官方 exact branch 名稱、地址、營運公告，記錄日期與結論／仍缺資訊。預約平台頁目前可讀或有按鈕，不能單獨證明商家營運事實已核定。
- [ ] 核對沁園春創始店原 `129` 與臨時 `137` 地址的公告有效時段、exact branch 身分及目前 merchant/source 記錄，明確區別已驗證的訂位網址和未核定的商家／地址事實。
- [ ] 原報告／原票三項各有可追溯 disposition，已被後續證據解決的項目不重開；確需事實或程式修正者另立窄 scope 票並引用，正式資料／地圖／座標／啟用不變。

## Steps

- [ ] 讀取 `git show 59f4b994533554509ec2dd90d0f7139acf8030a9:docs/catalog-content-reviews/2026-09-11-reservation-enrichment.md` 及同 HEAD 的 `tasks/open/2026-09-11-merchant-reservation-enrichment.md`；先引用主線 PR #392/#397/#408/#428/#434 的完成收據，劃掉已被替代的完整目錄研究與網址 parser 舊 holds。
- [ ] 以目前 source 和既有 fix/tests 檢查 dialog identity；無寫入 fixture 依穩定 filter、快速切換及延遲 search response 三種序列觀察。禁止真實 admin save，原 report 已證明當時錯誤在存檔前發現，沒有 Thipsamai 誤寫證據。
- [ ] 只讀原 closure／relocation 頁與目前 exact branch 官方資料，記錄原文來源網址、讀取日期、門市名稱地址與時效，與商家／source readback 逐欄比對；網站受限就記具體限制，不繞過，也不猜最新地址。
- [ ] 在本票記錄三項結果與需另票的工作；不要把訂位網址 `verified` 當作商家營運／搬遷事實自動核定，也不要重播原已套用平台資料。

## Verification

editor 重現必須記錄 row ID、dialog ID、search response order 及 source SHA，並證明零正式寫入；「沒有重現」須列測過的序列，不冒充 source fix。TABLES／沁園春逐筆具日期來源與目前 exact branch 只讀比對，正面證據才能關閉殘項。正式 merchant facts、map identity、coordinates、approval/active、platform records 和既有 audit 不變。

## Notes

最終證據 `<home>/.codex/scratch/uncertain-branches-followup-20261011/catalog-audit.json`；後續 exact merchant successor 記錄在同目錄 `catalog-extra-proofs.json`，完整原收據在 `catalog-evidence.json`。原平台資料本來已 live，不需要新 PR／部署來發布歷史已套用資料。TABLES／沁園春此次只是缺少明確事實 adjudication 的收據，不宣稱目前仍待審或原地址必錯。Naver booking 既有票是另一 cohort，不擴大本票。

2026-10-11 分支續查；共享票比對基線為 main `73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b` 的全部 389 張 open 票，未找到同義任務（詳 `<home>/.codex/scratch/uncertain-branches-followup-20261011/catalog-open-task-check.json`）。本票只追蹤唯讀對帳與保全，初始 scope 僅含本票檔案，結果直接記在本票。任何程式、資料或其他證據檔修改須另開窄 scope 票並先核對所有者；不釋放或覆寫任何原 claims、owner、scope。未發布、未公開、舊票仍在 open、當前主線較新，均不能單獨證明現在仍 pending。這次開票不授權正式資料寫入、重播舊 batch、付費呼叫、部署或發布。

本票保持 open、未認領；建票只恢復待辦，不釋出原分支 owner 或授權接管現有工作目錄。續作時依 task-board 核對認領、main 與本票 scope；正式站寫入、合併／部署與付費生成維持各自原有授權。

本票 scope 僅含這份對帳紀錄：以唯讀調查及可查核結論完成交接。需要產品、資料或原工作目錄修改時另開並認領窄 scope 票，不以本票直接處置。
