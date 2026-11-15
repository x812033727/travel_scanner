# F01 格林初版灰姑娘：製作紀錄與備忘

## 企劃與查核紀錄

- **主題**：1812 年格林兄弟初版《灰姑娘》（Aschenputtel）——為什麼沒有神仙教母與玻璃鞋，姊姊要切掉腳跟？為什麼第二版非但沒改溫和，反而越改越狠？
- **查核依據**：5 個 HTTP 200 一手歷史文獻與權威機構典藏：
  1. *Aschenputtel* (Kinder- und Haus-Märchen Band 1, 1812, Nr. 21, S. 88–101, Anhang S. XVI) — Wikisource
  2. *Aschenputtel* (Kinder- und Haus-Märchen Band 1, 2. Auflage, 1819, S. 114–123) — Wikisource
  3. *Aschenputtel* (Kinder- und Haus-Märchen Band 1, 7. Auflage, 1857, S. 119–126) — Wikisource
  4. *Cendrillon, ou la petite pantoufle de verre* (Charles Perrault, 1697) — Wikisource
  5. *Cinderella (film, 1950)* — D23 華特迪士尼官方百科 Disney A to Z
- **事實查核結果**：詳見 [`claims.md`](claims.md) 與 [`verify-1.md`](verify-1.md)，所有初版細節（生母墳前小樹、白鳥投衣、金拖鞋、母親遞刀、大姊削跟、二姊削趾、城門白鴿叫喊揭穿、初版結尾無啄眼、格林批評佩羅）、第二版改動（榛樹枝由來、順序對調、冷酷台詞、婚禮雙目被啄瞎私刑）、佩羅宮廷版確立（仙女教母、南瓜馬車、老鼠侍從、玻璃鞋、善良寬恕）及闢謠（玻璃鞋通篇印為 `verre`，毛皮 `vair` 誤譯說純屬近代假說）均獲獨立核實無誤。

## 盲評（`narrative`，14 題）

- 兩位盲測讀者獨立審查，14 題全數通過（14/14 PASS），附帶引用台詞 ID 與時間碼 `[line_id mm:ss]`，評審記錄寫入工作目錄 `review/narrative.json`。
- 開場 44 秒完成鉤子、懸念與承諾句，每 30–45 秒設置開放式懸念與反轉，節奏緊湊。

## 語音與配樂

- **中文（`zh-TW`）**：Gemini TTS 雙角色對話演繹（所長 `Sulafat`、小問 `Leda`），語速目標 $\ge 4.4$ 字／秒。
- **八語配音（`en,ja,ko,es,pt,id,vi,th`）**：全數使用 MiniMax Speech（`dub --provider minimax`），依各語言精選男女雙發音人演繹所長與小問。
- **配樂**：`light, curious, a little mysterious, no vocals`，音量曲線設定 `gain_db: -20, duck_db: -10`。

## 畫面風格升級：劇場級動畫光影 × 厚塗水粉質感

站主 2026-11-14 指定之全新畫風規格：
1. **生圖工具**：100% 使用內建 `generate_image`（`AspectRatio: "16:9"`），以 `keyframes import --provider external --usd 0` 匯入，嚴禁 MiniMax 生圖。
2. **角色鎖定**：所長鏡頭傳入 `characters/chief/`，小問鏡頭傳入 `characters/kid/` 鎖定五官特徵與服裝色系。
3. **質感配方**：
   - 暖深褐色手繪墨線（warm-sepia tapered linework，無粗黑死板向量框線）。
   - 窗邊斜射暖金陽光（warm golden directional sunlight）、髮絲／眼鏡／連帽金色輪廓光（rim light）、空氣光塵（volumetric dust motes）。
   - 奶油感淺景深散景（creamy shallow DOF painterly bokeh）。
   - 多層次布料摺皺、木桌紋理與材質反射，滿版 16:9 無邊框。
   - 乾淨空白介面（clean blank surfaces），畫面上 0 亂碼字、0 假文字。
4. **配額冷卻守則**：遇到 `gemini-3.1-flash-image` 配額冷卻時，先執行翻譯、配音、字幕等步驟，不退回 MiniMax。
5. **零出錯硬規則**：
   - 純物件與機制鏡頭標記 `nobody: true`，提示詞嚴格寫明 `zero humans`。
   - 歷史場景群像解除 `nobody`，杜絕假人與殘肢。
   - 縮圖字卡採用強烈好奇衝突問句（`**切腳跟**\n誰當后？`），拒絕劇透。

## 觀眾觀影體驗與完播率評審（`audience_review`，評分 93.5/100，Grade A）

- **評審報告**：詳見 [`review/audience_review.md`](review/audience_review.md)。
- **五大維度表現**：
  - 開場鉤子（18.5/20）：44 秒內完成世界童話破題、削腳衝擊與文獻翻開承諾句。
  - 敘事階梯（19.0/20）：五重反轉層層遞進（無教母 -> 無處罰 -> 佩羅發明 -> 格林越改越狠 -> 闢謠毛皮誤譯），每 30-45 秒設置開放式迴路。
  - 謎底回收（19.5/20）：基督教道德嚴明因果昇華至「童話是時代心靈的鏡子」。
  - 視聽節奏（17.0/20）：已即時修復 29 處重複景別前綴、84 處 motion 與 speaker 脫鉤、以及 2 處古籍具體文字生圖風險。
  - 防離場設計（19.5/20）：結案章精準鎖定在第 166 景，後續僅 6.5 秒互動提問與訂閱 CTA，徹底杜絕完播率斷崖。
