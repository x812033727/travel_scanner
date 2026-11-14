# sothatswhy-p12-qr-code 製作紀錄

企劃：[`brief.md`](brief.md)（對話形式規範：[`../so-thats-why/dialogue-pilot-20261103/README.md`](../so-thats-why/dialogue-pilot-20261103/README.md)、評分表 [`SCORECARD.md`](../so-thats-why/dialogue-pilot-20261103/SCORECARD.md)、系列畫風 [`../so-thats-why/look.md`](../so-thats-why/look.md)、V2 標準人物設定圖 [`../so-thats-why/series-sheets/README.md`](../so-thats-why/series-sheets/README.md)）。查核來源：[`claims.md`](claims.md)、獨立逐句查核：[`verify-1.md`](verify-1.md)。分鏡 2 倍放大審核：[`review/scorecard-2-storyboard.md`](review/scorecard-2-storyboard.md)。成片獨立觀眾視角評分：[`review/audience-review.md`](review/audience-review.md)。

## 稿子怎麼產生

整份 [`video.json`](video.json)（scenes、loops、角色、聲音、youtube、縮圖、sources）與 [`build_scenes.py`](build_scenes.py) 完全逐位元對應（`sha256 e9a536d794df`）：

- **角色與聲音**：`chief`（Gemini `Sulafat`）與 `kid`（Gemini `Leda`）沿用系列已核准的設定圖快取（`look` 0 次生圖呼叫），實錄平均語速 **`5.11 字／秒`**（高於系列下限 `4.4 字／秒`）；[`docs/videos/lexicon.json`](../lexicon.json) 新增 `"QR Code": "Q R Code"`、`"QR": "Q R"`、`"CD": "C D"`、`"Reed-Solomon": "Reed Solomon"`，避免共用詞表把 `"Code"` 念成 `"扣德"`。
- **V2 標準人物造型與無人機制鏡比例**：
  - 全片 80 鏡全數透過內建生圖搭配 `keyframes import --provider external --usd 0` 匯入（MiniMax 生圖呼叫 `0` 次、圖片 API 費用 `US$0`），採舞台聚光厚塗不透明水彩（`theatrical-light rich gouache`）。
  - 43 鏡（`53.75%`）為《原來如此事務所》專屬 **2.5 頭身 Q 版**角色鏡（對齊 [`chief-canon-v2.png`](../so-thats-why/series-sheets/characters/chief-canon-v2.png) 雙耳無鉛筆、[`kid-canon-v2.png`](../so-thats-why/series-sheets/characters/kid-canon-v2.png) 圓亮大眼，與《奇聞檔案局》3.5 頭身修長 `Ada` 完全區隔）；37 鏡（`46.25%`）為 `nobody: true` 無人機制與實物特寫（落於系列 `45%–65%` 區間）。
- **運鏡凍結在 [`cameras.json`](cameras.json)**：80 鏡全數無連續三鏡重複運鏡，搭配 `pauses: {line_ms: 0, scene_ms: 150}` 與 `still_motion: "beat"`。

## 2026-11-14 完製與審核紀錄

- **撰稿、查核與盲評**：
  - 6 章、80 鏡、159 句、0 張字卡（100% 插圖）、`loops` 19 個全數回收；片頭後 15 秒內拋出飲料店沾冰咖啡照樣嗶 vs 花邊貼太近掃不過的核心問題。
  - 獨立代理逐句查核 [`verify-1.md`](verify-1.md) 通過（嚴守 DENSO WAVE `qrcode.com` 與 CMU Reed-Solomon 教材一手範圍，不引用未讀 ISO 原文細節）；盲評 14 題敘事審核（含 `no_orphans`）通過；`lint` `0 errors`。
- **語音與八語配音**：
  - `zh-TW` Gemini `Sulafat`＋`Leda` 合成並通過 `check-audio`（157／159 句自動放行，2 處同音轉寫 `靜區／禁區`、`幾盒碼字／幾何碼子` 人工核對語音正確）。
  - `en, ja, ko, es, pt, id, vi, th` 八語翻譯經獨立母語審稿，MiniMax 八語配音合成並全數通過 `check-audio --locale`，且與 `mokaair-sothatswhy-bookends-v3-endscreen`（`82263266d425`）及 `sothatswhy-bed-r2.m4a` 對齊混音。
- **分鏡 2 倍放大審核（[`review/scorecard-2-storyboard.md`](review/scorecard-2-storyboard.md)）**：
  - 獨立代理逐鏡四象限 2 倍放大檢查 80 張關鍵影格與全部縮圖：**`68 / 70` 分通過**（最低單項 `9/10`；零懸空耳鉛筆、零偽文字亂碼、零與奇聞系列撞臉）。
- **成片組裝、觀眾視角獨立評分（[`review/audience-review.md`](review/audience-review.md)）與修正**：
  - `final.mp4`（`sha256 b9a7b1839d315c74ebfa28d2850403a01e0c7e4b3bdaa0ad32336e6f991140fc`，`18,187 frames`，`606.26 s`，`-14.0 LUFS`）組裝完成後，交由全新獨立代理以一般 YouTube 觀眾視角檢視 21 張成片抽格總表、9 語字幕與 11 張縮圖。
  - 80 鏡正片與音訊 **0 處待修瑕疵**；初審抓出 `thumbnail-c.jpg` 副標單行與 `en/es/pt/id` 外語縮圖主標單行壓邊共 2 項零成本排版問題，已全數改為雙行斷行重繪並複驗左側文字安全區（`< 794px`），最終六維度平均 **`9.13 / 10`**、技術七項 **`64.3 / 70`**，並通過 **`qa` 11／11**。
- **Google Drive 完整備份與後台送審**：
  - 完整製作目錄（含 `_raw_keyframes/`、`_repo_docs/`、`final.mp4`、8 語 `dubs/`、9 語 `captions/`、`review/`、`SHA256SUMS`，排除任何權杖密鑰）已備份至 `AI/備份/AI劇/原來如此事務所/數位科技與通訊工程/P12/製作檔/sothatswhy-p12-qr-code/`（資料夾 ID：`1kMdSO7TbqNqoTayAhSlB5c7Xo_Kln7EO`），並經獨立代理涵蓋核對 `0` 差異。
  - 已執行 `review-push --slug sothatswhy-p12-qr-code --gate final` 送交 `/admin/videos` 待站主核准 `final` 關卡（後續站主核准後再跑 `review-pull` 與 `package`）。
