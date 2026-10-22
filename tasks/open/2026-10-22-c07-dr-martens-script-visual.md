---
id: 2026-10-22-c07-dr-martens-script-visual
title: Write and independently review C07 Dr. Martens script and visual plan
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-c07-script
claimed_at: 2026-10-22T05:29:15Z
created_at: 2026-10-22T05:29:06Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/script.md
  - docs/videos/story-everyday-dr-martens-c07/visual-plan.md
  - docs/videos/story-everyday-dr-martens-c07/script-source-notes.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/narrative-reader-1.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/narrative-reader-2.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-review-summary.md
---

# Write and independently review C07 Dr. Martens script and visual plan

## Why

站主已採用 C07 六章企劃（Treatment 原檔雜湊見 owner-treatment-approval.md）。須在同一證據界線內寫出可朗讀的連續故事與奇聞檔案局風格逐鏡稿，先補可直接讀取的獨立博物館文化來源，再進逐句查核與兩位盲讀。

## Definition of done

- [ ] 六章逐句稿、每句依據與一對一逐鏡方案完成；青年文化轉向有可直接讀的獨立館藏或研究來源。
- [ ] 另一代理逐句核查，兩位真正盲讀；各審查收據與本版 SHA-256 綁定。
- [ ] 相關檢查通過，草稿 PR 貼 `no-auto-merge`；未付費生成、上傳或發布，劇本仍待站主另審。

## Steps

- [x] 從已核准 Treatment `68c8c8766` 開獨立工作樹與窄票。
- [x] 補直接可讀倫敦博物館館藏與獨立研究來源，寫 77 句逐句稿與 77 鏡方案。
- [ ] 交獨立來源審查和兩位盲讀，修改並重綁收據。
- [ ] 執行文件／看板檢查並開草稿 PR。

## How to verify

`npm run check:tasks`、`git diff --check`；來源逐句可讀性及檔案 SHA-256；稿件句數與分鏡行數一致、插圖占比至少七成、連續文字卡最多三張。正式正文 ≥480 秒仍須以核准後 TTS 實測，字數估時不充數。

## Notes

2026-10-22：倫敦博物館 1995 年館藏物件頁可直接讀，明確寫 Dr. Martens 於 1960 年代末被 skinheads 採用、後有其他次文化；Arthur Crucq 的 2021 年獨立研究可直接讀，分開晚 1960s、晚 1970s punk 與後來極右挪用。V&A 品牌專頁直取仍 403，不作逐句唯一依據。出廠日與未知零售日嚴格分開。舊 Treatment 任務 `done` 曾寫出 done 副本但 open 檔刪除受政策拒絕，詳見舊工作樹，**勿以改寫命令繞過**。

2026-10-22：初稿凍結雜湊見 `reviews/script-review-summary.md`。77 句與 77 鏡 ID 一對一、63 插圖／14 卡、最長兩連卡；仍待另一代理逐句查核、兩位真正盲讀、時長與時間占比實測，不能宣稱 PASS。`npm run check:tasks` 通過（全庫舊票警告）；首輪 `npm run test:docs-videos` 因此新工作樹缺 `pinyin-pro` 中止，正在 `npm ci` 補依賴後重跑。
