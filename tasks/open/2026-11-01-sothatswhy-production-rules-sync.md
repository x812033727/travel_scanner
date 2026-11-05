---
id: 2026-11-01-sothatswhy-production-rules-sync
title: So Thats Why: sync curated topics and new rules into shared production entrypoints
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-11-01T05:22:21Z
completed_at:
branch:
depends_on:
  - 2026-11-01-sothatswhy-refresh
scope:
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/long-form
  - docs/videos/long-form
  - docs/videos/so-thats-why/README.md
  - docs/videos/so-thats-why/operations.md
  - docs/videos/so-thats-why/look.md
  - docs/videos/KNOWLEDGE-STORIES.md
---

# So Thats Why: sync curated topics and new rules into shared production entrypoints

## Why

站主 2026-11-01 要原來如此事務所採奇聞最新規則並重整題目。編輯規格與 300 舊題處置、13 新題已在 `docs/videos/so-thats-why/CURRENT.md` 和 `refresh-20261101/`，本機選題入口為 `tools/video/so-thats-why/cli.mjs`。共用工人與舊 long-form inputs 尚未讀此新清單；CARTOON 仍有舊開場預告數與分原因結構。文件完成不代表主機已套用。

2026-11-01 查到 `automation`／`narrative`／templates／long-form review 多個 scope 已由其他任務持有（daily-brief-on-the-host-worker、daily-ai-news-brief-video-format、story-thumbnail-brand 等），所以整理題庫的票只動隔離目錄與未持有的索引。本票在重新查碰撞、確認相關工作落地後執行，不釋出別人的 claim。

## Definition of done

- [ ] 所有原來如此的新選題入口套用逐題處置，剔除／暫緩／轉線／短片／併題不再被當新長片選出；舊 journal 續跑與既有影片不被破壞。
- [ ] cute-cartoon 新稿採五步開場、最多兩預告、同一因果主線、45 秒內鉤子、13 分鐘至少 11 個 loops；writer、verifier、blind panel 和 lint 一致。
- [ ] 新單集有效輸入以 13 分鐘、cute-cartoon、image-01、配樂、繁中 burn_in=true、開場後片頭與 v4 片尾產生；不更動其他系列的預設。
- [ ] 原來如此的縮圖套用明亮 bold 方向、6 字主標／12 字副標，保留本系列色盤；實際渲染驗證手機縮圖。
- [ ] README／operations／look／KNOWLEDGE-STORIES／舊有效輸入入口明確導向 CURRENT；重建舊時長資料若需要，必須獨立審查代理更新收據，不能作者自己重綁。
- [ ] 回歸與 docs 檢查通過，舊包／來源／核准／媒體沒有被抹掉，PR 記錄是否部署；不能只因合併就宣稱正式生效。

## Steps

- [ ] 重新查當前 worktrees／遠端 PR／持有 scope、主機進行中 journal；避免提示詞變更重開付費請求。
- [ ] 採用 `refresh-20261101/SPEC.md`，把 authoring-only 規則接入共用產線，補不影響其他系列的測試。
- [ ] 逐路徑核對原來如此題號與 slug，驗證舊入口無法繞過退題；後台資料匯入若需另有 API scope，先把精確範圍列入票。
- [ ] 獨立時長覆核與 PR，正式部署按 action-time 範圍處理；部署後用新單集只讀／dry-run 確認實際設定。

## How to verify

`node tools/video/so-thats-why/cli.mjs check`、相關 explainer/narrative/templates/automation 測試、`node tools/video/long-form/cli.mjs check`、`npm run test:tools`、`npm run test:docs-videos`、`npm run check:tasks`。針對其他系列的 prompt/hash 與既有 journal 做回歸；正式站狀態須另有部署與 readback 證據。

## Notes

- 本票保持 open，沒有 claim，也沒有部署、付費生成、刪影片或搬移其他系列的授權執行紀錄。
- 最新奇聞字幕決定是 2026-10-31：奇聞燒繁中、品牌不燒。原來如此新版採前者，不可照較早的「全部不燒」快照。
- 編輯分類不是事實核准；`source_references`、`merged_topics` 的限制要跟著交給撰稿者。新題與第三季仍需完整製作包。
