# B18 成本刷新獨立覆核（2026-10-17）

**結論：離線估價的版本、公開單價及算式 PASS；付費製作 HOLD。** 覆核對象是本目錄 `README.md` SHA-256 `f2bd5c8dd1371e89ce86ba00863eeaac27297b70c6b3a797bac677f1044cc06d`。本覆核沒有登入供應商帳戶、讀取正式帳本、呼叫付費 API 或碰正式主機；公開價不能證明帳戶實際權益或最終帳單。

## 釘選與數量

- B18 父版 `B18-claim-granularity-candidate-20261017/sha256.json` 實測 SHA-256 `1016d3de91236af487eec891e256f43214d71a06ba806409084831f47584e198`；其 `base_manifest_sha256` 與上一版 manifest 實測 `cb28ae7bb6aed7a30c639318504e8e11386aee8de1404e9b71b1c372c1e40953` 相同。父版 manifest 列出的 12 個檔案逐一重新雜湊，0 筆不符。
- `series.json` 實測 `218d1bb500701380f505f5c3da37638de7cbffce95db23f8c06aa45b6546c807`，確為 `image-01`、`cute-mystery`、1 個 cast。`verification.json` 實測 `7daf65fe0e13b228f0c5d207334803b14123122afb62f4f13aac8a2d195811a1`。另外直接加總六個章檔，得到 **85 景＝66 個 shot＋19 張 title 卡、88 行旁白**；`estimated_body_seconds` 為 560.966666… 秒，`measured_body_seconds` 為 null。這些是規劃數，不是已生成圖片、已錄音訊或正式 QA。
- v3 報價 JSON 實測 `08686ceef4bea59cfc87de8c1028e8671c931ee0267a14daa80f7b345699a816`；MD 實測 `4e0c47d6fd78159aae82ccce7d25bd39c19e6132d4a8549c1fa17292aeb23a83`，均與刷新筆記釘選一致。v3 的 B18 為 91 張、3 張 cast 候選、46 張重試，共 140 次圖片生成，模型合計 US$2.60098；刷新筆記改用新分鏡數量，沒有重估後五片。

## 官方公開價與算式

- [MiniMax 官方價目](https://platform.minimax.io/docs/pricing/overview)列 `image-01` 為 **US$0.0035／張**；同頁訂閱／套包涵蓋語音或 Hailuo 影片，沒有把 `image-01` 列入。筆記不把圖片當成已由訂閱抵扣，正確。
- [Google Gemini API 官方價目](https://ai.google.dev/gemini-api/docs/pricing)列標準層 `gemini-3.8-flash` 至 2026-12-31 輸入／輸出為 **US$0.75／3.75 每百萬 token**；`gemini-3.8-flash-tts` 為 **US$0.50 文字輸入／US$9 音訊輸出每百萬 token**，音訊輸出按每秒 25 token；Lyria 3.5 完整歌曲 **US$0.08／次**。這些與筆記一致，2027 價格須另算。
- [TypeSafe 官方 Jev 介紹](https://typesafe.ai/blog/introducing-system-one-models-and-jev)列 **US$0.042／百萬輸入 token、輸出免費**；[2026-10-07 官方案例](https://typesafe.ai/blog/jack-jill-jev-case-study)也使用同一公開表價。這不核實該帳戶的合約價格。
- 以筆記的有限次數假設重算：圖片與審圖規劃額首輪 `(66+3)×(0.0035+0.01)=0.93150`，重試 `ceil(0.5×66)×0.0135=0.44550`；TTS `0.15500+0.07750`；轉錄 `0.19440+0.09720`；Jev `0.02688`；音樂 `0.08+0.08`。首輪 **US$1.38778**，正常重試 **US$0.70020**，總額 **US$2.08798**；比 v3 少 **US$0.51300**，與提案 US$5 差 **US$2.91202**。逐項算式 PASS。

## 限制與一項文字問題

- 筆記所寫「圖片生成及其逐張 judge 合計 102 次」容易被讀成**兩種請求合計只有 102 次**。依其公式是 **102 次 MiniMax 圖片生成，另有 102 次逐張 Gemini judge 的規劃配額**；若一圖一審，兩種請求共 204 次。金額已將兩種單價各算 102 次，**金額無需因此改動**；對外或執行清單應修正呼叫數措辭。
- `US$0.01／judge` 只是內部規劃值，不是官方固定收費或最壞單次價格。`apps/api/app/video_media/admin_api.py` 的 Gemini judge 單次保守預留上限為 US$1.032192；應按實際已結算、未結／不確定與下一次最高預留檢查。US$5 僅是**未核准且尚未正式落地的逐片停損提案**，並不承諾以 US$2.08798 做完整片。
- 未計入真實稅率、外語配音／CC、Shorts、額外縮圖圖像、上傳、訂閱和主機固定成本。只有已接受關鍵圖組的縮圖、本地文字卡、既有片頭片尾以及可選兩版配樂在本模型內。600 秒、120 句、重試比例及 token 用量皆為估算；沒有 TTS 實測、圖片 SHA、成片、正式 worker/來源資料列覆核或站主觀看。**此 PASS 僅認可本地估價算術；不放行匯入、購買、合併、部署或發布。**
