# H36 卡迪夫巨人騙局：製作紀錄與備忘

## 企劃與查核紀錄

- **主題**：1869 年卡迪夫巨人騙局（The Cardiff Giant）——被拆穿是石膏像後，為什麼紐約百老匯反而有「兩個巨人」同時收門票？
- **查核依據**：5 個 HTTP 200 一手歷史文獻與機構典藏：
  1. *The Cardiff Giant Humbug* (1870, P.T. Barnum)
  2. The Cardiff Giant: A Chapter in the History of Human Folly (1898, William A. Newell)
  3. The Cardiff Giant Hoax (Library of Congress)
  4. Farmers' Museum Cardiff Giant Permanent Exhibition
  5. Mark Twain: *A Ghost Story* (1870)
- **事實查核結果**：詳見 [`claims.md`](claims.md) 與 [`verify-1.md`](verify-1.md)，所有時間（1869 年 10 月 16 日）、尺寸（10 英尺 4.5 英吋）、地名（紐約州卡迪夫、雪城、愛荷華石膏採石場、芝加哥彫刻工坊、百老匯阿波羅大廳與伍德博物館）、票價（25 美分至 50 美分）與法官判決（Nelson 法官裁定）均獲獨立核實無誤。

## 盲評（`narrative`，14 題）

- 兩位盲測讀者獨立審查，14 題全數通過（14/14 PASS），附帶引用台詞 ID 與時間碼 `[line_id mm:ss]`，評審記錄寫入工作目錄 `review/narrative.json`。
- 鉤子與承諾句節奏符合黑貓研究院十步架構，每 30–45 秒一個懸念與資訊遞進，雙巨人百老匯打對台的荒謬反轉精準收束於新聞識讀教訓。

## 語音與配樂

- **中文（`zh-TW`）**：Gemini TTS 雙角色對話演繹（所長 `Sulafat`、小問 `Leda`），總時長 7 分 39 秒（459.9 秒），實測語速達 **4.53 字／秒**（超越站主要求的 $\ge 4.4$ 字／秒門檻），`audio` gate 已正式核准。
- **八語配音（`en,ja,ko,es,pt,id,vi,th`）**：全數使用 MiniMax Speech（`dub --provider minimax`），依各語言精選男女雙發音人演繹所長與小問。
- **配樂**：`light, curious, a little mysterious, no vocals`，音量曲線設定 `gain_db: -20, duck_db: -10`。

## 畫面風格升級：劇場級動畫光影 × 厚塗水粉質感

站主 2026-11-14 指定之全新畫風規格：
1. **生圖工具**：100% 使用內建 `generate_image`（`AspectRatio: "16:9"`），以 `keyframes import --provider external --usd 0` 匯入，嚴禁 MiniMax 生圖。
2. **角色鎖定**：所長鏡頭傳入 `docs/videos/so-thats-why/series-sheets/characters/chief/0c3a400c8e981d84.png`，小問鏡頭傳入 `kid/f8dac008f296a6a3.png` 鎖定五官特徵與服裝色系。
3. **質感配方**：
   - 暖深褐色手繪墨線（warm-sepia tapered linework，無粗黑死板向量框線）。
   - 窗邊斜射暖金陽光（warm golden directional sunlight）、髮絲／眼鏡／連帽金色輪廓光（rim light）、空氣光塵（volumetric dust motes）。
   - 奶油感淺景深散景（creamy shallow DOF painterly bokeh）。
   - 多層次布料摺皺、木桌紋理與材質反射，滿版 16:9 無邊框。
   - 乾淨空白介面（clean blank surfaces），畫面上 0 亂碼字、0 假文字。
4. **配額冷卻守則**：遇到 `gemini-3.1-flash-image` 配額冷卻時，先執行翻譯、配音、字幕等步驟，不退回 MiniMax。

## 觀眾評分與深度品檢（Audience Review，評分：86.0 / 100，A-）

2026-11-14 依站主指示由獨立影評顧問進行全片深度評審，各維度得分如下：
- **內容劇情與節奏**：28.0 / 30（A+，開場 28 秒三記重拳打破認知，雙角色對談生動自然、無說教感）。
- **視覺與畫面感覺**：24.0 / 30（B+，劇場級水粉光影質感驚艷，但抓出 21 處 `nobody: true` 提示詞矛盾）。
- **聲音與聽覺氛圍**：18.0 / 20（A-，4.53 字/秒緊湊俐落，建議在荒謬笑點後留白發酵）。
- **全球化與多語包裝**：16.0 / 20（B，八語翻譯傳神，但縮圖原設辦公室 Shot 0 為 CTR 災難且字卡劇透）。

### 依評審建議完成之具體改善：
1. **縮圖重構（CTR 與懸念最大化）**：
   - 鏡頭由辦公室 `7jnm` 改為泥坑巨石腳趾出土震撼特寫 `xd9z`。
   - 字卡由劇透的 `**雙巨人**\n全是假` 改為強烈衝突問句 `**假告假**\n誰是真？`，八國語言縮圖同步更新。
2. **徹底消除 21 處 Prompt Negation Clash**：
   - 修正 `video.json` 與 `prompts/keyframes.md`，純物件/環境機制鏡頭（工具、金幣、報紙、票根）保留 `nobody: true` 與無人提示詞；1869 年歷史群像與工人鏡頭解除 `nobody`，改為 19 世紀復古匿名剪影描述，杜絕殘肢與畸形假人。
3. **規則與教訓沉澱**：
   - 片尾離場標誌（結案章）排他鎖定規則、`nobody: true` 提示詞人物衝突檢測門檻、縮圖嚴禁指定辦公室 Shot 0 等教訓已正式寫入 `docs/videos/lessons/curio.md`。
4. **正式流程整合**：
   - 已將「觀眾評分與深度品檢（Audience Review）」正式增訂至 `.agents/skills/curio-episode/SKILL.md` 與 `.claude/skills/curio-episode/SKILL.md` 製作流程中。
