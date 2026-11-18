# 05 AI 製作系統：把現有產線對應到兩個頻道

對應提示詞 5「AI 驅動的 YouTube 製作系統」。產線早就有了（`tools/video`、各個 skill、主機工人），**這份不新增工具**，
只回答三件事：每個系列走哪條路線、品管怎麼做、改編到其他平台怎麼做，最後列出支援第二個頻道要改的地方。

## 1. 路線表

| 階段 | A 奇聞檔案局 | A 原來如此事務所 | B AI 劇（3D） | B 真人版 | B AI 寵物短劇 | B AI 製作解說／教學 |
| --- | --- | --- | --- | --- | --- | --- |
| 先讀 | `curio-episode` | `so-thats-why/CURRENT.md`、`look.md`、`lessons/sothatswhy.md` | `youtube-video` 的 `drama.md`、`animation-production` | 同左＋`lessons/zhong-tian-qu-qi-r2.md` | `producer` 的 `micro-drama.md` | `youtube-video` 全自動路線 |
| 選題與研究 | 題庫 `history-curiosity/topics*.json`、`pool/` | `node tools/video/so-thats-why/cli.mjs list` | `series-plans/zhong-tian-qu-qi/` 逐集細綱 | 同一份細綱 | 一句話企劃 | 站上文章、`producer` §3 |
| 腳本與查核 | 撰稿 → 另一個代理逐來源查核 → 十步架構盲評 | 同左 | 劇本關卡、`drama_craft_check.mjs` | 同左 | 笑點盲評（三位評審） | 撰稿 → 換人查核 → 聽眾審稿 |
| 開拍前鎖定 | — | — | `animation-preproduction`：分鏡、三鏡小樣、估價，**站主核准** | 同左（成本更高，一定要過） | 同左 | — |
| 畫面 | 內建 `generate_image` → `keyframes import --provider external --usd 0`；Ada 設定圖鎖定 | 同左；所長與小孩的設定圖 | Hailuo／Kling 瀏覽器或 RunPod H3（`minimax-h3-runpod`） | 同左，寫實風提示詞 | Colab 或 RunPod 的 H3 | 投影片版型、`screencast` |
| 聲音 | 中文 Gemini `Sulafat`（≥ 4.4 字／秒），八語 MiniMax 配音 | 中文 Gemini `Sulafat`＋`Leda`，八語 MiniMax | 多角色配音（`drama.md`） | 同左 | 內心獨白或零台詞 | Gemini 旁白 |
| 組片與品管 | `assemble` → `qa` 11 項 → 2 倍放大獨立審圖 → **獨立觀眾評分並修完** | 同左（`review/audience-review.md`） | `qa`、成片評分 ≥ 42 | 同左 | 同左 | `qa` |
| 備份 | Google Drive（`todrive.sh`），不推 `transfer/*` 分支 | 同左 | 同左 | 同左 | 同左 | 同左 |
| 上架 | `review-push --gate final` → 站台上傳到 **A** | 同左 | Studio 手動上傳到 **B**（多頻道做好前） | 同左；**必勾**合成內容 | 同左 | 同左 |
| 檢討 | 7／28 天看報表（`07-analytics-review.md`），教訓寫進 `docs/videos/lessons/` | 同左 | 同左 | 同左 | 同左 | 同左 |

**每支大概的成本**：
- 奇聞與原來如此的關鍵影格用內建生圖，記 US$0（`--usd 0`）；配音與主機的費用照 `animation-production` 的估價。
- AI 劇與真人版的片段要付點數，**每一批都先估價、等站主核准**，數字寫在那一集的 preproduction 鎖定包裡。這份文件不預估金額，因為報價依路線與秒數而定。

## 2. 品管清單（上架前，每支都過）

**技術**（只分過與不過）：
- [ ] `node tools/video/cli.mjs qa` 11 項全過（長度、音量、字幕、雜湊……）
- [ ] Shorts：9:16、主體在中間三分之一、第一秒就有主角

**內容**（照 `scorecards.md`）：
- [ ] 企劃與稿子評分過門檻（奇聞與品牌故事總分 70；其他 50）
- [ ] 成片評分：總分 ≥ 42（奇聞 ≥ 56），沒有任何一項低於 5；評分的代理不能是做這支片的那一個
- [ ] 標題答應的事在前 30 秒開始兌現
- [ ] 奇聞、原來如此：由獨立代理做觀眾評分，全部修完後重跑 `qa`，才備份和推送

**包裝**：
- [ ] 縮圖五項評分；大字 ≤ 6 字；不破梗
- [ ] 標題：認得的名字放前面，系列後綴照 `CAPTION_TAGS`
- [ ] 準備 2–3 組縮圖做 A/B 測試（長片）

**政策**：
- [ ] 寫實 AI 內容勾選「經過修改或合成的內容」；`contains_synthetic_media` 照實填
- [ ] 沒有在世的人，或 1956 年後過世的人入畫（奇聞）
- [ ] 改編作品有「參考劇與原創聲明」，不搬原劇的情節與台詞
- [ ] 音樂與素材的授權有記錄

## 3. 改編到 Shorts 與 Instagram Reels

| 來源 | Shorts | Reels | 工具 |
| --- | --- | --- | --- |
| 奇聞、原來如此長片 | 每支切 1–2 段：選「最反常的那一句」加上答案前的懸念，25–55 秒 | 同一支 9:16 檔案 | `node tools/video/shorts/cli.mjs`（`docs/videos/SHORTS.md`），長度範圍在後台 Shorts 設定 |
| AI 劇 | 單集本身就是 Shorts（50–180 秒的集數，超過 60 秒的要剪短或用合輯切片） | 同一支 | `shorts from-drama` 裁切 |
| 寵物短劇 | 原生 15 秒或 50–55 秒 | 同一支，這類最適合 Reels | 同上 |

**跨平台的規則**：
- 上傳**沒有浮水印**的原始檔，不要轉載 YouTube 下載的版本。
- 字幕燒進畫面（Reels 很多人靜音看）；YouTube 版用 CC。
- 站主 2026-11-18 決定**經營 Reels**，TikTok 先不做（[`../DECISIONS.md`](../DECISIONS.md)）。Reels 目前**沒有自動上傳工具**，由站主手動上傳。

**Reels 規劃**：

| 項目 | 做法 |
| --- | --- |
| 帳號 | 跟兩個 YouTube 頻道各配一個 Instagram 帳號，名稱一致（Mokaair、摩卡劇場 Mokaair），站主開 |
| 頻率 | 跟著 Shorts 走：@Mokaair 每週 4–8 支，摩卡劇場每天 1 支 |
| 檔案 | 同一支 9:16、無浮水印的原始檔；字幕燒進畫面 |
| 時段 | 和 YouTube Shorts 同一天，晚 2–3 小時上，先讓 Shorts 吃第一波 |
| 導流 | 個人檔案的連結放 YouTube 頻道；每支說明第一行寫系列名，結尾說「完整版在 YouTube 搜尋○○」 |
| 先試什麼 | 摩卡劇場的寵物短劇和《種田》最有爽點的單集；4 週後看哪一類分享數最高，再調整比例 |
| 數字 | 每週檢視加一行：Reels 觀看、分享、個人檔案點擊（Instagram 洞察報告手抄） |
- 每支結尾都導回 YouTube 的系列名稱（說「搜尋○○」，不要只放連結）。

## 4. 第二個頻道要改的地方（開工程票）

查過的現況：站台的 YouTube 連線是**單一頻道**。`apps/api/app/models.py` 的 `VideoYoutubeConnection` 註明「The one YouTube channel the site publishes to」，
資料表有 `CHECK (id = 1)`。上傳、公開同步（`video_reviews/admin_service.py` 的 `_linked_youtube`）、報表（`youtube-channel-reports`）全都綁在這一筆。

| 項目 | 現在 | 要改成 | 在那之前怎麼辦 |
| --- | --- | --- | --- |
| OAuth 連線 | 一筆（`id = 1`） | 每個頻道一筆，影片／系列記錄要上哪個頻道 | B 用 Studio 手動上傳（`MANUAL-UPLOAD.md`） |
| 報表 | 只下載 A 的 | 依頻道分開下載與查詢（`cli.mjs --channel`） | B 的數字從 Studio 手抄進每週檢視 |
| VPS Studio 上傳器 | 一個瀏覽器設定檔，還沒驗收 | 每個頻道一個設定檔 | 不用 |
| 系列預設 | 沒有頻道欄 | `curio`、`sothatswhy` → A；`zhong-tian-qu-qi*`、漫劇、寵物短劇 → B | 人工確認 |

這是一張 migration 加上 API 加上後台的工程票，要照 `backend-conventions` 做（migration 編號、整合測試、後台頁登記）。
**這份文件只開票，不實作。**
