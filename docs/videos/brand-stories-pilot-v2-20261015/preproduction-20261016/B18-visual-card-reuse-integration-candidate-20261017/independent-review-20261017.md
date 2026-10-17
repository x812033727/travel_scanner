# B18 字卡與共圖意圖整合：獨立限定覆核

2026-10-17（台北）。結論：**PASS_EXACT_INTEGRATION_AND_STATIC_CARD_ONLY；整片 HOLD**。本覆核只處理畫面版字卡副標與舊共圖映射的衝突；不重審 93 行完整故事或 65 項來源主張，也不是 worker 審稿收據、圖片驗收或成片驗收。

## 精確輸入與輸出

| 檔案 | 本次重算 SHA-256 |
| --- | --- |
| 基底 `B18-visual-direction-candidate-20261016/sha256.json` | `1fa55f086c06a402d8d8ca501b35bf427e8a2093c66ed84c6ce274171e0f1f2c` |
| 舊單卡 `B18-mobile-card-revision-candidate/variant.json` | `6dda79642d299c933fa56c63d74ac95b97f947918764ad56b9705ff02cb96a24` |
| 舊作者映射 `B18-authored-chapters-candidate/mapping.json` | `46f8a6c27e79c42e733fda1e91a57e07144094907e3184d6e59d5af43cddedbc` |
| 本包 `sha256.json` | `d950454ac96598ec59c1391731e4e0c0f9eae54c702123b4d9b3b3afb1675d1f` |
| 本包 `chapters/idea.json` | `9afd40486ba804e38e8aa12b11a298275eb96cc4a651671baf46925516c15301` |
| 本包 `reuse-intent.json` | `7c900da1deadc32bb666aaed73878e08c3fa92202dea2430b0f52363dd88404c` |

我獨立重算 `sha256.json` 所列所有產物的檔案雜湊，零不符；另與基底逐檔比對七份輸入：`series.json` 及 `hook`、`origin`、`engine`、`turn`、`now` 五章逐位元組相同。`idea.json` 的純文字差異只有 `idea-s027.data.subtitle`，從三行「兩份沿革記載／J-Net21 記載／發明協會記載」改為單行「兩份資料，兩種說法」。標題 `J-Net21 · 發明協會` 和標籤 `J-Net21／發明協會` 不變。由於其餘 JSON 位元組相同，93 行旁白、65 項主張及判定、71 個插畫提示詞、鏡位與 `series.json` 都沒有改動。`node build.mjs --check` 退出碼 0，回報 90 景、93 行、0 lint error、22 warning、0 cute-story error、0 外部呼叫；這是離線結構檢查。

## 正式版型的手機字卡

以專案 `slideHtml`／`openRenderer.capture`、已驗證的 Node v24.19.0 與 `msedge` 渲染本包 `idea-s027`，將 1920×1080 still 真正縮至 320×180；命令退出碼 0、`sceneProblems` 和渲染器 `problems` 均為空。`theme.css` SHA-256 為 `ae26b5b6c920b2d2cfffa45bdc0c181a996c7cd3689cc9769d6186875df360c5`。完整版型 PNG SHA-256 為 `67dd10c38773016eca8a626a7e31ff9d7b79ad3be9941b00f0b2878b3be6c00b`；保存的 [320×180 獨立重渲染](idea-s027-independent-320x180.png)為 26,050 bytes，SHA-256 `2c777428a427d93fb1bde88461c732bb5854d96e951d51c6c05a7ec3e7bc3dd5`，與舊單卡審查保存的小圖逐位元組相同。

我以原始 320×180 檢視：徽章、主標和單行副標可辨識，沒有裁切或文字重疊。這只支持**靜態字卡**可讀；成片停留秒數、動態轉場、繁中 CC 遮擋及手機播放仍待媒體檢查。兩種來源說法須由相鄰旁白分別歸屬，不能把這張卡當成史料裁決。

## 共圖意圖與採用界線

舊 `mapping.json` 的三組開場／回收列仍寫 `same_prompt_camera_key: true`，同檔媒體驗證為 `null`。本版的 `hook-s004→idea-s023`、`hook-s005→engine-s055`、`hook-s006→turn-s077` 各有**不同**提示詞、相同鏡位，章檔沒有 `image_asset_key`；片尾 `now-s101`、`now-s101b`、`now-s102`、`now-s103` 是四個不同提示詞。`reuse-intent.json` 因此將三組定為敘事主題回呼、片尾定為四個獨立畫面，明寫 `same_file_required_by_this_candidate: false`、`production_alias_installed: false`、`accepted_asset_sha256: null` 與採用時須明確消除舊映射衝突。這個決定與章檔現狀一致，**只是一份離線編輯意圖**，不會被正式 worker 自動套用，也不證明已有任何相同或不同圖片檔。

此限定 PASS 不解除 65 項 `UNCHECKED`、舊作者章採用路徑的阻擋、來源與整稿敘事審查、真圖與 TTS、成片和站主看片關卡。採用前須明確決定並更新舊映射／實際媒體處理，再做獨立覆核；本報告不授權主機寫入、付費製作、匯入或 YouTube 上傳。

本包 `README.md` 的「獨立覆核下一步」保留候選凍結時的待辦狀態；上述限定覆核由本報告補記。`README.md` 已被 `sha256.json` 固定，本次未改其內容或候選產物。
