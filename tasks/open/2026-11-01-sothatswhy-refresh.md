---
id: 2026-11-01-sothatswhy-refresh
title: So Thats Why refresh: current rules and curated topic catalog
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-7ba3
claimed_at: 2026-11-01T05:14:36Z
created_at: 2026-11-01T05:14:34Z
completed_at:
branch: codex/sothatswhy-refresh-20261101
depends_on: []
scope:
  - docs/videos/so-thats-why/refresh-20261101
  - docs/videos/so-thats-why/CURRENT.md
  - docs/videos/so-thats-why/playlists.md
  - docs/videos/so-thats-why/thumbnails.md
  - tools/video/so-thats-why
---

# So Thats Why refresh: current rules and curated topic catalog

## Why

站主要求原來如此事務所用奇聞檔案局最新規則優化、整理並剔除不好的題目，參考十萬個為什麼補更好的題目。舊三季各 100 題混有品牌史、AI 舊失誤、政策與偏薄冷知識，系列規格仍有舊三秒片頭與下一集預告等歷史內容。

本票完成編輯規格、逐題處置、來源可追溯的新題與可查詢的本機清單；不承包另一位持有者的共用工人／後台變更。正式產線同步有明確後續票，不能把本票完成說成已部署。

## Definition of done

- [x] 三季 300 原題逐題有保留／改題／短片／併題／轉線／暫緩／剔除理由，8 個舊判重不復活。
- [x] 補 13 個具有核心機制來源、三段因果線、舊題區隔與限制的新題，經不同代理研究來源。
- [x] 新規格採最新 13 分鐘、五步開場、45 秒鉤子、11 loops、MiniMax 可愛插圖、配樂、繁中燒錄與濃縮後片頭／v4 片尾，保留本系列畫風。
- [x] 首批 24 題與有效 100 題可直接閱讀；新入口拒絕退下長片的題目，保留所有原稿／查核／既有素材與核准。
- [x] 獨立編輯審閱已完成，修正 8 個只共用分類的硬併題，以及 T14 標題的新主張；記錄於 REVIEW.md。
- [ ] 相關測試與來源綁定檢查完成，整理成可審閱 PR；共用產線未同步的差異有接續票。

## Steps

- [x] 從新抓取的 origin/main b1ee20b8e 建分支，核對最新 10-31 字幕決定與所有活躍 scope，認領隔離範圍。
- [x] 寫 CURRENT、SPEC、逐題 editorial 資料、新題來源與 README／TOPICS／AUDIT，保留原三季 JSON。
- [x] 加本機 build/check/list/show/brief，綁來源與原查核包 SHA-256、輸出 merged_topics，題庫與表格漂移即拒用。
- [x] 不同代理覆核並套修；新增產線同步接續票。
- [ ] 完成檢查、結案與 PR。

## How to verify

`node tools/video/so-thats-why/cli.mjs check`；`node --test tools/video/so-thats-why/catalog.test.mjs`；`node tools/video/long-form/cli.mjs check`；`npm run check:tasks`；完整 tools/docs-videos 測試。

## Notes

- 最終：87 舊題換角度 + 13 新題 = 100 長片候選；62 短片、11 可選併題、102 轉其他系列候選、20 暫緩、18 剔除。每個原 id 完整保留。
- 不動 B26／T26／T27 舊影片資料；改題不代表重新核准或重製。未讀正式片單，正式製作前仍須按 id／slug 查重。
- REVIEW.md 為獨立代理實際審閱紀錄，不是作者自行簽核；新增題核心來源已查，不代表完整逐字稿通過或 300 舊題已全數重新查核。
- 原 README／look／operations 仍有其他任務持有，KNOWLEDGE-STORIES 又受共用時長收據綁定；本票沒有改它們。入口從 CURRENT 與 playlists／thumbnails 導向新版，後續 `2026-11-01-sothatswhy-production-rules-sync` 處理共享產線、主索引與舊入口。
- 無付費生成、正式設定、後台匯入、刪除、排程或發布。`production_synced:false`、`production_ready:false` 保持明確。
