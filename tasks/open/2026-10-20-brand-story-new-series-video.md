---
id: 2026-10-20-brand-story-new-series-video
title: 新增品牌故事系列與首集影片
status: blocked
priority: P1
area: docs
owner: codex-gpt6-new-brand-video
claimed_at: 2026-10-20T00:46:46Z
created_at: 2026-10-20T00:46:43Z
completed_at:
branch: codex/brand-stories-new-series-20261020
depends_on: []
scope:
  - docs/videos/brand-stories-everyday-reversals-20261020
---

# 新增品牌故事系列與首集影片

## Why

站主在已交付 A01 進度 PR 後，要求另開全新題材的品牌故事系列並實際製作影片。既有 100 題、五集新包與五集改編各有自己的製作順序；新工作需要獨立系列代號、來源查核與預算，不能沿用既有影片審核或重複購買素材。

## Definition of done

- [ ] 三集系列題材與首集正式來源獨立查核完成，首集逐字稿、分鏡、製作成本與審核收據可追溯。
- [ ] 首集經台灣口音旁白、MiniMax `image-01` 插畫、合成、繁中 CC 與 QA，產生可看片的 1080p／30fps 影片；正文實測至少 8 分鐘。
- [ ] 正式 `kind: story` 系列／集數及影片狀態與本地收據一致；成片由站主看過，才進入語言及上傳。

## Steps

- [x] 對照既有題庫與正式專案，選出不重複的 Crocs、Tupperware、Moleskine 候選與獨立系列 slug。
- [x] 在 onboarding 設定草稿保存 Crocs／SEC 官方來源的最小網域；等待發布後逐頁查核。
- [ ] 讀 Crocs 一手資料、完成首集 Treatment／企劃列及另一代理的 hash 綁定查核。
- [ ] 逐章撰稿、逐句查核、聽眾及敘事審稿；量實際配音長度。
- [ ] 取得品牌片頭片尾與正式工人工作區，核對佇列、現有支出、供應商餘額、價格及可重試上限。
- [ ] 按整批張數及全項目 US$25 上限取得站主核定，再生成、合成、檢查首集影片。

## How to verify

`node tools/video/story-plans/validate.mjs` 驗證獨立查核後的企劃包。建立 `video.json` **之前**先依工具流程初始化故事發音字典；成稿後由 CLI 逐一執行 `lint`、`tts --dry-run`、`tts`、`check-audio`、`keyframes --dry-run`、`keyframes`、`render`、`clips`、`assemble`、`captions`、`qa`、`package`，每步帶本集 `--slug` 與獨立媒體工作區並保存真實輸出。依賴站主審核的關卡先取得其實際決定，不寫入替代收據。實片以 ffprobe 驗證 1920×1080、30fps、正文時長及聲畫 hash；看片與正式站審核另有各自收據。企劃候選目前只檢查 `seriesProblems`，不能當影片完成證明。

## Notes

2026-10-20：新系列 `brand-stories-everyday-reversals` 只在本機草案，三題來自 `reserve.json` 且未獨立查核。Crocs 首集官方入口 `investors.crocs.com`、`www.crocs.com`、`www.sec.gov`、`data.sec.gov` 遭目前雲端 HTTP allowlist 擋下；已保存設定草稿，`requires_publish=true`，尚未生效。不得以網路失敗當來源不存在，也不得從備選題目的角度倒推成已證實財務事實。

已配對影片工具可讀正式狀態，但不能下載工人章稿、時間軸、審核預覽或品牌包。此 checkout 沒有新系列影片媒體，正式 `story-*` 工作是否存在須獨立查。新 slug 不在現有全片預算保護清單，全域媒體 US$200 上限不等於每片 US$25 全項目約束。未做正式匯入、付費呼叫或上傳。
