---
id: 2026-10-15-curio-h10-research-outline
title: Prepare Curio H10 Franklin source refresh and outline choices
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-15T16:33:45Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-h10
---

# Prepare Curio H10 Franklin source refresh and outline choices

## Why

使用者要求接續製作五集奇聞檔案局。H10 富蘭克林遠征需要更新來源、兩個可選的完整大綱及主張邊界，交站主與獨立審核員一起檢視；本任務只處理 H10 前製。

## Definition of done

- [x] research.md 登錄 2026-10-16 實際打開的來源與限制。
- [x] claims.md 可將兩案重要敘述對回來源，修正 4 月 25 日所記「明日 26 日」南行計畫。
- [x] brief.md 提供 A／B、可朗讀 30–60 秒開場、六章、3–5 轉折、loops 與結尾新資訊。
- [x] 獨立審核員讀回修正版；大綱層級通過，非正式劇本十三題通過。
- [x] 完成獨立覆核與手動 outline 送審交接，後台讀回 pending。
- [ ] 站主選定 A／B，並明確核准本批 US$30 費用提案後，再接續正式製作。

## Steps

- [x] 閱讀現行 curio-episode／youtube-video／script-writing，參考 H01-v2 前 30 景與 H09 brief。
- [x] 唯讀參考 949bb91fc 題庫，重開 Parks Canada、加拿大歷史博物館、Waterloo 與原始研究來源。
- [x] 補入 2024 Fitzjames 身分研究與 2024–2025 官方成果背景。
- [x] 按獨立覆核意見，把開場物件清單改成可朗讀場景和三個未揭曉行動時刻。
- [x] 送審後釋出本票認領供後續接手；未建立 video.json、未啟動付費工人。

## How to verify

`git diff --check`；`npm run check:tasks`；逐一讀 research.md、claims.md、brief.md 的交叉引用、六章時長和 loops；核對開場朗讀量為 30–60 秒。沒有劇本 JSON，因此不宣稱正式劇本 lint 或旁白 QA 已通過。

## Notes

工作樹為 curio-next-five，base a77a9416d。此 task 的 UTC 產生日期為 10/15，文件查核日採 Asia/Taipei 10/16。H10 九個採用來源均取得正文或指定專節；主線不加入血腥遺骸、食人畫面或死因排行榜。共同預算為每集 US$6／五集 US$30 估算停手提案，尚未授權；本任務實際外部付費 US$0，未啟動付費工人、未推送。獨立覆核者 curio_h12_m09_planning 已確認主要史實並讀回開場修訂，無剩餘阻擋項。凍結 brief SHA-256：725991c44d9129668377c291efd0aa8edfc9306635abe551c6fc2616397e45ff。git diff --check 與 check:tasks 通過（1895 票；既有長期認領／scope 警告保留）。

2026-10-16 01:01（Asia/Taipei），主代理完成五集手動 outline 送審並讀回 pending；H10 review ID：`72a82580-0901-476f-b0b6-e7ddfa30e7c5`，對應上述最新 brief SHA。獨立覆核與送審交接完成，釋出認領但不標 done。下一位接手者須先讀回站主 A／B 選擇及本批 US$30 明確授權；目前兩者均未核准。送審卡未啟動付費製作。已送審 brief 維持原樣，由主代理統一 commit／PR。
