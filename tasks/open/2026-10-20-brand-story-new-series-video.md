---
id: 2026-10-20-brand-story-new-series-video
title: 新增品牌故事系列與首集影片
status: in-progress
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
  - docs/videos/story-everyday-crocs-c01
---

# 新增品牌故事系列與首集影片

## Why

站主在已交付 A01 進度 PR 後，要求另開全新題材的品牌故事系列並實際製作影片。既有 100 題、五集新包與五集改編各有自己的製作順序；新工作需要獨立系列代號、來源查核與預算，不能沿用既有影片審核或重複購買素材。

## Definition of done

- [x] 二十集新系列的題材、順序與查核入口完成；首集正式來源獨立查核、逐字稿、分鏡、製作成本與審核收據可追溯。
- [x] 首集經台灣口音旁白、MiniMax `image-01` 插畫、合成、繁中 CC 與 QA，產生可看片的 1080p／30fps 影片；正文實測至少 8 分鐘。
- [ ] 正式 `kind: story` 系列／集數及影片狀態與本地收據一致；成片由站主看過，才進入語言及上傳。

## Steps

- [x] 對照既有題庫與正式專案，擴成不重複的二十集企劃與獨立系列 slug。
- [x] 雲端環境來源設定已發布；實測 SEC 原始申報可讀。
- [x] 讀 Crocs 一手 SEC 申報，完成 C01 Treatment、20 段旁白與 100 景本機分鏡；另一代理對旁白和 `video.json` 分別做 hash 綁定來源查核。
- [x] 逐章撰稿、逐句查核、兩位獨立讀者敘事審稿；`lint` 零錯誤。
- [x] 實測台灣口音配音時長，若超出規格則修稿並重新查核。
- [ ] 建立正式 `episodes/C01.json` 企劃列及其獨立 hash 查核，匯入前唯讀試跑。
- [ ] 取得品牌片頭片尾與正式工人工作區，核對佇列、現有支出、供應商餘額、價格及可重試上限。
- [x] 對 C01 整批 93 張插畫、七張資料卡及全項目 US$25 硬上限乾跑並寫報價。
- [x] 取得站主整批 US$25 核定，生成、合成本機試看片並檢查；正式成片仍須品牌素材與審核。
- [x] 依參考頻道歷史紀錄盤點缺口、修正與 A40 重複的題目，另外增補不冒稱出自頻道的獨立品牌候選。

## How to verify

`node tools/video/story-plans/validate.mjs` 驗證獨立查核後的企劃包。建立 `video.json` **之前**先依工具流程初始化故事發音字典；成稿後由 CLI 逐一執行 `lint`、`tts --dry-run`、`tts`、`check-audio`、`keyframes --dry-run`、`keyframes`、`render`、`clips`、`assemble`、`captions`、`qa`、`package`，每步帶本集 `--slug` 與獨立媒體工作區並保存真實輸出。依賴站主審核的關卡先取得其實際決定，不寫入替代收據。實片以 ffprobe 驗證 1920×1080、30fps、正文時長及聲畫 hash；看片與正式站審核另有各自收據。企劃候選目前只檢查 `seriesProblems`，不能當影片完成證明。

## Notes

2026-10-20：新系列 `brand-stories-everyday-reversals` 擴為二十集編輯企劃；八題（C01／C02／C03／C05／C08／C11／C15／C19）取自 `reserve.json`，十二題是本批新提案。站主回覆雲端網路設定已發布後，已實測 SEC／Crocs 官方頁面 200，下載並閱讀 Crocs 2008／2009／2010／2025 年報與 2026 Q2 季報。C01 旁白與分鏡核心財務事實已有另一代理分別按內容雜湊獨立核查；C02–C20 不得把取證入口當已查核事實。

本次雲端已用站主核對代碼的裝置流程重新配對影片工具；權杖保存在工作區外於 repo 的 `/workspace/.video-tool-home/.mokaair/video-tool.json`（目錄 700、檔案 600），不進 Git。使用 `node --use-env-proxy /workspace/video-tool-cli.mjs media-status --slug story-everyday-crocs-c01 --workdir /workspace/.brand-video-workdir` 唯讀通過，讀回本機媒體帳目 US$2.29。工具仍不能下載正式工人的章稿、時間軸、審核預覽或品牌包；全域媒體 US$200 上限不等於每片 US$25 全項目約束。C01 已做核准範圍內的本機付費生成，但**未正式匯入、未上傳**。

上段為付費生成前的歷史紀錄，已由下列實際結果取代：C01 現為 97 句、90 張插畫與七張字卡，台灣口音旁白逐句音訊檢查 97／97 通過，兩位敘事盲審 13／13 通過。`/workspace/.brand-video-workdir/story-everyday-crocs-c01/review/local-preview/preview.mp4` 是 1920×1080、30 fps、10:51.77 的本機試看片，SHA-256 `5ba761f9cb0b68cdaa96da4855b6c66e35cb0414f57c26a49a15bb1f1b432322`；109 則繁中 CC 及首尾畫面 QA 已通過。含 45 秒濃縮開場、5 秒明標概念片頭、21 秒明標概念片尾；正式站主品牌素材與 YouTube Studio 可點片尾仍未接入。媒體工具記錄的圖片／評審／音樂費為 US$2.29，語音、轉錄、模型及稅費沒有完整可核帳單，不能宣稱全片最終花費已核定。

2026-10-20 補充選題：`channel-gap-candidates-20261020.md` 列出六個能從 10 月 7／17 日頻道快照辨識且無同核心的缺口；先前列入的金氏世界紀錄其實已有 A40 及獨立查核，已剔除。`additional-brand-candidates-20261020.md` 再列六個**獨立編輯候選**，不得稱為參考頻道影片。Beats、Meta、WD-40 的 SEC 原件及 Adobe 訂閱轉型的四份年報已初查；其餘仍待來源。雲端代理對 YouTube 即時頁回 `CONNECT 403`，無法宣稱已盤點其最新完整清單。新增網域 `www.youtube.com`、`youtube.com` 的設定草稿因 `stale_base` 衝突而未存成；完整交接見 `docs/videos/brand-stories-everyday-reversals-20261020/research-access-handoff.md`。
