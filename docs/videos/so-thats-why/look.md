# 原來如此事務所：畫面識別與片頭

2026-09-28 起草。

**2026-11-14 定案（現行標準）**：站主對比 P21 與 P12 樣張後指定全系列改採**「劇場級動畫光影 × 厚塗水粉質感」**，並固定由代理內建 `generate_image`（`16:9` 滿版）生圖後以 `keyframes import --provider external --usd 0` 匯入，**嚴禁用 MiniMax 生圖**（對話版雙角色分工與完整製作流程見 [`dialogue-pilot-20261103/README.md`](dialogue-pilot-20261103/README.md)）：

- **角色造型與頭身比鎖死（與《奇聞檔案局》嚴格分家）**：本系列雙角色固定為 **2.5 頭身圓頭大眼 Q 版比例（`2.5-head chibi`）**——與《奇聞檔案局》的 3.5 頭身修長比例研究員 `Ada`（暗紅細圓框眼鏡＋褪色青風衣）完全不同，嚴禁混用或漏寫 `2.5-head chibi` 導致漂成寫實長腿大人。有角色的鏡頭，`ImagePaths` **必傳 Repo 內正式 V2 標準設定圖**（所長傳 `docs/videos/so-thats-why/series-sheets/characters/chief/chief-canon-v2.png`：深棕黑低馬尾帶銀灰挑染、粗黑圓框眼鏡、**雙耳乾淨無耳環且已移除舊版耳後鉛筆**、芥末黃針織外套配白襯衫；小問傳 `docs/videos/so-thats-why/series-sheets/characters/kid/kid-canon-v2.png`：亮黑平瀏海短鮑伯頭＋頭頂一撮呆毛、**圓亮大眼有高光**、深墨藍牛角釦雨衣配亮黃垂領帽兜、空手無筆記本；禁用同資料夾早期 `0c3a400c8e981d84.png`／`f8dac008f296a6a3.png` 舊版 MiniMax 失敗檔，詳見 [`series-sheets/README.md`](series-sheets/README.md)）。重繪既有分鏡時一併傳入原構圖圖檔鎖定骨架與道具位置；遇到 `gemini-3.1-flash-image` 配額冷卻時先跑八語翻譯與配音或分批等待，絕不退回 MiniMax。
- **畫面不必每鏡都有人（`nobody: true` 純物件／機制鏡佔 45%–65%）**：內建 `generate_image` 畫無人場景不會像早期 MiniMax 在物件上亂畫人臉，**嚴禁把整集做成滿滿的大頭站樁講話**。全集約 **45%–65%** 鏡頭應設為 `"nobody": true`（`characters: []`），直接呈現純機制剖面、日常物件微距、數量比例對照與實驗特寫；角色鏡頭控制在約 **35%–55%**，只留給開場怪事反應、小問提問猜測、所長關鍵點破與片尾收束。
- **五大質感配方**：
  1. **線條**：前景主體改用暖深褐色（warm-sepia）有粗細收尖變化的手繪墨線，不用粗黑死板向量框線；背景完全不畫黑框線。
  2. **光影**：窗邊斜射暖金陽光（warm golden directional window sunlight），在髮絲、眼鏡框、連帽邊緣與道具倒角打出明亮金邊輪廓光（glowing rim light），空氣帶微細光塵（subtle volumetric dust motes）。
  3. **景深**：前景角色與桌面道具銳利聚焦，背景做奶油感淺景深散景虛化（creamy shallow depth-of-field painterly bokeh）。
  4. **材質、色溫呼吸與圖解對比**：保留系列色盤（暖奶油底、墨藍、芥末黃、印章紅），畫出厚塗水粉（rich gouache）筆觸、針織外套與雨衣的多層次布料摺皺陰影、木桌紋理、玻璃／壓克力透光折射、金屬高光與液體光澤，不做單色平塗色塊。**防暖棕視覺疲勞**：室內對話每 6–8 鏡穿插明亮冷調藍天窗景、淺薄荷工作牆或深藍太空／工廠冷色場景讓眼睛換氣；**純機制／數量對比鏡改鋪淺奶油白或冷調日光灰桌面**，搭配墨藍、天藍、薄荷綠、珊瑚紅高對比道具（避免棕色污漬、金色小盒與暖黃橡木桌在手機小螢幕糊成一團）。
  5. **零出錯與無字圖解連續性硬規則**：全圖 100% 滿版無黑邊；嚴禁任何中英文字母、數字、招牌字或背景黑板粉筆亂碼；單人正反打不同框，`nobody: true` 純機制鏡頭零路人或殘肢；手指數（5 指）、眼神對焦與旁白提到的道具數量／比例 100% 精準吻合；**所長雙耳乾淨無耳後鉛筆，手勢維持在胸前或桌面高度**；同一個抽象單位（如「一盒 8 位元碼字」）全集鎖死同一種幾何外觀，截面比例採上下垂直投影對齊、非重量關係禁用翹翹板、反直覺損壞對比必加發光薄荷綠 `✓` 與珊瑚紅 `✕` 標記；匯入後必切 2 倍放大檢視圖由獨立子代理逐張審過。
- **每鏡 Prompt 英文畫風基底句**：
  ```text
  High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces with zero text or symbols.
  ```
- `video.json` 頂層仍寫 `"look": { "preset": "cute-cartoon" }` 以綁定系列身分（縮圖版型、卡片與不燒字幕檢查），實際關鍵影格一律用上方升級基底句經 `generate_image` 生圖後 `keyframes import --provider external --usd 0` 匯入。

---

以下為早期歷史版本紀錄（2026-09-28 無角色草案、2026-10-10 MiniMax 平塗版，已被上方 2026-11-14 定案取代）：

2026-09-28 原始起草紀錄：當時決定**不用吉祥物**（2026-09-28）：這個系列沒有任何固定角色，辨識度由畫風、色盤與「蓋章」這個動作承擔。這份寫全系列共用的 `look`、片頭 3 秒、結尾蓋章與章節卡；片頭三張關鍵影格做一次、每集重用，選定後雜湊記在最後一節。

**2026-10-10 更新（歷史紀錄，已停用 MiniMax 生圖）**：插圖曾改由 MiniMax `image-01` 生成，畫風改成可愛卡通家族（候選與 MiniMax 的限制在 [`../history-curiosity/look.md`](../history-curiosity/look.md)）。站主同日選了候選 A「大頭卡通」。下面是 2026-10-10 版的 `look`（`negative` 對 MiniMax 無效，留空；第 1 版的 flat-explainer 文字保留在 `tools/video/core/drama.mjs` 的預設裡）；色盤、印章、片頭、章節卡的規則不變。

```json
{
  "preset": "custom",
  "style": "cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, bright flat colours with soft cel shading on a warm cream paper ground, ink navy, mustard yellow, stamp red only on the answer, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9",
  "negative": "",
  "motion": "slow push in or gentle drift, no morphing, no cuts",
  "candidates": 3
}
```

第 1 版（2026-09-28，已被取代）：

## 系列畫風

每集 `video.json` 的 `look`：

```json
{
  "preset": "custom",
  "style": "flat editorial illustration, bold clean outlines, limited palette of warm cream #F6EFE3, ink navy #1F2A44, stamp red #D8452F and mustard #E8B64C, soft paper grain, simple shapes, generous negative space, friendly and clear, 16:9 composition, no gradients heavier than two tones",
  "negative": "photorealistic, 3d render, cinematic lighting, text, letters, watermark, logo, brand marks, mascot, recurring cartoon character, extra fingers, deformed hands, cluttered background",
  "candidates": 3
}
```

- 色盤：奶油紙底、墨藍、印章紅、芥末黃。**印章紅只給答案與蓋章**，觀眾看到紅色就知道答案要來了。
- 人物：需要人的畫面用簡化的無臉或極簡五官人物、剪影，不做跨集重複出現的角色，也就不需要設定圖（`characters` 留空，只有旁白）。
- 手：盡量不畫手指特寫；要拿東西時用手部剪影或只畫物件。
- 真實人物、公司 logo、產品外觀：不用 AI 生成相似的臉或 logo，改用剪影、泛稱物件與文字卡；需要真實圖片時走 `screenshot` 模板並標出處。
- 文字一律由卡片場景或合成疊字，不讓圖片模型寫字（`negative` 擋文字）。

2026-10-10 樣張：借站上的投影片代號用上面的 `look` 畫了 4 張超市場景（走道、補貨推車、拿鮮奶的手、門口的店長），MiniMax `image-01` 4／4 一次過、各 9.29，`look_hash` `a5910f9c047dbeff`；圖在 repo 外 `mokaair-work/videos/_audition/look-20261010-curio/stw-a/`。

**片頭**：站主 2026-10-02 核准了系列的 6.9 秒片頭（[`../branding-release/2026-10-02-sothatswhy-intro-approval.md`](../branding-release/2026-10-02-sothatswhy-intro-approval.md)），下面 2026-09-28 的三張關鍵影格片頭是當時的草案，已被取代，不重畫。

## 片頭 3 秒（2026-09-28 草案，已被 2026-10-02 核准的片頭取代）

| 時間 | 畫面 | 運鏡（`camera`） | 聲音 |
| --- | --- | --- | --- |
| 0.0–1.0 秒 | 事務所木門，門上毛玻璃（字由卡片疊上：原來如此事務所／各語系名稱） | `push-in` | 敲門兩聲 |
| 1.0–2.0 秒 | 門打開，空的木桌上一封寫著問號的信（問號由合成疊上） | `drift` | 開門聲 |
| 2.0–3.0 秒 | 紅色印章從畫面上方落下，在信上蓋出「受理」（字由卡片疊上）；畫面裡沒有人 | `push-in` | 蓋章「咚」 |

## 結尾蓋章（每集最後 3 秒）

答案卡（`big` 或 `quote` 卡片，墨藍底）被同一個紅色印章蓋上「原來如此」（該語系的口號，見 [README](README.md)），配同一個「咚」。這一格也是 Shorts 最後導回長片的畫面。

## 章節卡

每章一張：奶油色檔案夾，頁籤是芥末黃、印著章節序號，檔案夾封面是章節標題（`chapter` 卡片疊字）。全系列同一個構圖，只換字。

## 選定紀錄

| 項目 | 值 |
| --- | --- |
| 片頭關鍵影格 1（門） | （檔名與 SHA-256，圖檔留在 repo 外的 `VIDEO_WORKDIR`） |
| 片頭關鍵影格 2（桌上的信） | |
| 片頭關鍵影格 3（蓋章） | |
| 站主確認日期 | |
