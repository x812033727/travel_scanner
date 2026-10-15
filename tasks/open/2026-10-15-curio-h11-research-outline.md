---
id: 2026-10-15-curio-h11-research-outline
title: Prepare Curio H11 Voynich source refresh and outline choices
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-15T16:34:00Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-h11
---

# Prepare Curio H11 Voynich source refresh and outline choices

## Why

使用者要求接續製作五集奇聞檔案局。H11 伏尼契手稿需要把新研究與仍未知的內容分清，產出可讓站主直接選 A／B 的大綱包；本任務只處理 H11 前製。

## Definition of done

- [x] research.md 列實際取得、僅摘要與無法開啟的來源。
- [x] claims.md 分清材料定年、文字統計、頁邊註記及全文解讀。
- [x] brief.md 提供 A／B、可朗讀 30–60 秒開場、六章、3–5 轉折、loops 與結尾新資訊。
- [x] 獨立審核員讀回修正版；大綱層級通過，非正式劇本十三題通過。
- [x] 完成獨立覆核與手動 outline 送審交接，後台讀回 pending。
- [ ] 站主選定 A／B，並明確核准本批 US$30 費用提案後，再接續正式製作。

## Steps

- [x] 閱讀現行系列規則及腳本故事、開場、結尾和十三題規則。
- [x] 唯讀參考 949bb91fc 題庫，重開館方、原始論文、校方聲明及研究者來源。
- [x] 納入 2024 多光譜、2025 Yale 筆跡介紹及 Naibbe 作者 README 的有限結論。
- [x] 按獨立覆核意見修正「2009 年定年工作」、開場不先揭露撤下新聞，以及模型圖僅為提案示意。
- [x] 送審後釋出本票認領供後續接手；未建立 video.json、未啟動付費工人。

## How to verify

`git diff --check`；`npm run check:tasks`；逐讀三份文件，確認每個大綱主張有來源、每案六章時長與 loops、開場文字可朗讀 30–60 秒。Naibbe 完整論文、原始 Yale 掃描與 NSA PDF 本輪未取得，不可宣稱已讀。

## Notes

工作樹 curio-next-five，base a77a9416d；查核日 2026-10-16 Asia/Taipei。Arizona 原站 404，以大學供稿的 Phys.org 刊載版替代並明示；Naibbe 論文正文 403，但 raw README 已讀。多光譜筆跡歸屬是研究者判讀，不是解密完成。共同預算每集 US$6／五集 US$30 仍是尚未授權提案。本任務付費 US$0，未啟動付費工人、未推送。獨立覆核者 curio_h12_m09_planning 重開八個可讀來源，讀回定年、開場及模型示意修訂後無剩餘阻擋項。凍結 brief SHA-256：4cc10a9506a997a0beca7f102e277fdcd6b45edfa488b204fcc39b3e61b50b6d。git diff --check 與 check:tasks 通過（1895 票；既有長期認領／scope 警告保留）。

2026-10-16 01:01（Asia/Taipei），主代理完成五集手動 outline 送審並讀回 pending；H11 review ID：`83bac5e3-c59b-417e-8060-0b14b4381f60`，對應上述最新 brief SHA。獨立覆核與送審交接完成，釋出認領但不標 done。下一位接手者須先讀回站主 A／B 選擇及本批 US$30 明確授權；目前兩者均未核准。送審卡未啟動付費製作。已送審 brief 維持原樣，由主代理統一 commit／PR。
