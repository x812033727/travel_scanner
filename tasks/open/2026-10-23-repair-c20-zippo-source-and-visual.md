---
id: 2026-10-23-repair-c20-zippo-source-and-visual
title: Repair C20 Zippo source and visual holds
status: in-progress
priority: P1
area: docs
owner: codex-root-c20-script
claimed_at: 2026-10-23T05:30:28Z
created_at: 2026-10-23T05:30:23Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/script.md
  - docs/videos/story-everyday-zippo-c20/script-source-notes.md
  - docs/videos/story-everyday-zippo-c20/visual-plan.md
  - docs/videos/story-everyday-zippo-c20/visual-plan.json
  - docs/videos/story-everyday-zippo-c20/reviews/author-script-receipt.md
---

# Repair C20 Zippo source and visual holds

## Why

第一輪獨立來源／配鏡審查 [PR #1732](https://github.com/x812033727/travel_scanner/pull/1732) 對 C20 作者稿 68 句判 65 PASS／3 HOLD：`c200207` 未在聲音和字卡說清 1933 售價／承諾是後來公司回顧；`c200310` 暗示看過 1933 同期銷售文件；`c200410` 把只可定年的 1997 博物館開幕錯接到今日 Repair Clinic 展示。本票只修這三個 ID，不擴大到付費或匯入。

## Definition of done

- [x] 三句旁白、來源註記及相配的兩張後製字卡／一個概念插圖都回到可說證據範圍。
- [x] 68 句／68 鏡同 ID、同序，58 張概念插圖／10 張字卡不變；四檔新 Git blob SHA-256 記入作者收據。
- [ ] 作者修改推送到原 draft PR #1728，實際 `no-auto-merge` label 保留；後續獨立差異重核與兩位新版純旁白盲讀各留收據。

## Steps

- [x] 按 PR #1732 原始 Zippo 公司史及博物館頁的可見敘述窄修 `c200207`、`c200310`、`c200410`。
- [x] 同步 `script.md`、逐句註記、分鏡 Markdown／JSON 及作者收據，重算四檔 Git blob SHA-256。
- [ ] 跑結構及 task/diff 檢查，提交／推送；另請非作者獨立重核，兩位讀者只看新版 68 句旁白。

## How to verify

以 `git show :<path>` 的位元組算 SHA-256；比對 68 個旁白 ID、來源註記、Markdown 鏡頭和 JSON 的 ID／旁白／提示詞同序相同。執行 `npm run check:tasks`、`git diff --cached --check`；在 GitHub 讀回 PR #1728 的 draft、head、`no-auto-merge` label 與未啟用 auto-merge。三句的差異另由非作者重開公司史、博物館頁與專利原件確認。稿件變動後舊盲讀不適用。

## Notes

此次避免把公司多年後回顧的 1933 售價及保證說成同期商品卡，也不把現今 Repair Clinic 倒定年到 1997。主線、句數和圖卡數不變；正文紙上估約 571.4 秒，不是實際 TTS。
