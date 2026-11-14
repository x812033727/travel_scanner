# 解說系列共用（奇聞檔案局＋原來如此事務所）：教訓

兩個旁白解說系列都會遇到的教訓。共同規則見 `docs/videos/explainer-series/README.md`；只跟其中一個系列有關的，寫在 `curio.md` 或 `sothatswhy.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟兩個系列的 `_規則與教訓/教訓/解說系列共用教訓.md`（docs/videos/rules-sync）。

## 2026-11-14 · curio-m17／curio-p17／sothatswhy-p12 · 兩個解說系列全面改採「劇場級動畫光影×厚塗水粉質感」內建生圖與泰語 Hashtag 修正
站主確認升級樣張後指定兩個旁白解說系列（奇聞檔案局、原來如此事務所）「以後用這樣的風格」，並同步收攏 `curio-m17` 抽檢與 `curio-p17` 實作抓到的跨系列規則：
- **生圖路線（兩個系列全面停用 MiniMax 生圖）**：所有關鍵影格一律改由代理內建 `generate_image`（`AspectRatio: "16:9"`）生成，再以 `keyframes import --provider external --usd 0` 匯入，**嚴禁退回 MiniMax `image-01`**；遇到 `gemini-3.1-flash-image` 配額冷卻時，先完成八語翻譯、配音與 `check-audio`，分批等待配額恢復。`video.json` 仍保留 `"look": { "preset": "cute-mystery" }`（奇聞）或 `"cute-cartoon"`（原來如此）以通過系列身分與版型檢查。
- **角色設定卡鎖定（含跨鏡歷史人物）**：除了原來如此的 `chief`／`kid` 與奇聞的串場研究員外，奇聞單集內只要同一位可入畫歷史人物（過世滿 70 年）跨超過 3–4 鏡出場，就必須先用 `generate_image` 產出該人物的固定設定圖（鎖死髮色、髮型與主色年代服裝），之後每鏡出場都在 `ImagePaths` 傳入設定圖（重繪既有鏡頭時一併傳入前一版構圖圖檔），避免像 `curio-m17` 瑪麗・雪萊六鏡換六套穿搭與髮色。
- **五大畫面質感配方與防留白／防招牌字實戰句**：每鏡英文 Prompt 必帶 `High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background.`；桌面物件近景必須明確補上背景顏料塗滿四邊最外層像素（避免厚塗水粉自動留出畫紙白邊），街道外景必須寫 `plain unadorned walls with zero hanging shop signs`（避免木招與布招冒出亂碼字母）；匯入前必切四格 2 倍放大圖由獨立子代理逐張審過（含地圖／地球儀方位與時代道具考證，避免 1816 年出現插電檯燈或地球儀插錯國家）。
- **泰語系 Hashtag 組合母音與 5,000 bytes 說明欄上限**：`tools/video/core/metadata.mjs` 的 `hashtagsFrom` 原本用 `/[^\p{L}\p{N}_]/gu`，把泰文上下母音與聲調（Unicode `\p{M}` Combining Mark）全部削光，導致 `#ปีที่ไร้ฤดูร้อน` 變成亂碼子音串 `#ปทไรฤดรอน`；已修正為 `/[^\p{L}\p{M}\p{N}_]/gu`。同時外語（尤其泰文，每字 3 UTF-8 bytes）說明欄組完後務必壓在 `< 4,500` bytes 安全區間，避免貼上完整來源清單與補回母音後衝破 YouTube 5,000 bytes 硬上限。
- **首尾呼應提示詞節制與收尾章名份量**：十步架構全片「如開頭說的／還記得開頭…嗎？」顯性提示詞留頭尾最多 2 次即可，中段直接講事實，避免 11 分鐘出現 8 次像照大綱打勾；最後一章 `chapter` 標題要寫收束全片因果的總結句，不要拿單一花絮烏龍當最後一格章名。
- 已升為規則：`AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`docs/videos/history-curiosity/look.md`、`docs/videos/explainer-series/README.md`、`tools/video/core/metadata.mjs`。

## 2026-11-13 · curio-s42／curio-w02／story-b01／sothatswhy-p18／sothatswhy-p23 · 一般觀眾視角六支連看檢討
站主請 AI 以一般觀眾視角連看頻道最新六支影片，抓出五個跨集重複出現的結構問題：
- **對話做片漏寫 `pauses`／`still_motion` 與「一句一景」抵銷緊湊停頓**：用 Claude 對話配對影音權杖做片走本機 `cli.mjs`，不跑主機 `settle()`，S42 與 B01 漏寫就退回 300／700 毫秒舊停頓；而寫了 `line_ms: 0` 的集數若把稿子切成一句一景（S42 92 句／73 景、B01 137 句／137 景、P23 71 景裡 50 景單句），每句結尾都變成 `scene_ms` 換景停頓，`line_ms: 0` 形同虛設。同角色同節拍連續 2–3 句要併進同一個 `scene.lines[]`。
- **Gemini 把 `voice.style` 語速打折**：寫「一秒四到五個字」甚至「一秒五個字以上」時，`Sulafat`／`Leda` 實測常落在 3.6–4.3 字／秒，不到站主定的 4.4 字／秒下限；可在 `voice` 加 `"tempo": 1.08`–`1.15` 用 `ffmpeg atempo` 不變調微加速達標。
- **縮圖破梗或選空白靜物**：P23 縮圖直接寫「鏡子沒翻左右／翻的是前後」把全片答案講完；W02 縮圖右框放一本闔上的無字紅皮書，手機列表毫無吸睛度。縮圖只寫反常識衝突或硬數字、嚴禁破梗答案，右圖必選誇張表情或強烈反差。
- **內部查核與作畫備註寫進公開說明欄**：S42、W02、B01 在 `youtube.description` 寫史料算式與「誰過世超過四百年、誰不畫臉」，像內部工程紀錄；一律留在 `claims.md`，說明欄只留給觀眾看的鉤子、受眾、章節、乾淨來源與系列 hashtag（`#奇聞檔案局`、`#原來如此事務所`、`#品牌故事`）。
- **外語標題漏系列名、留言區零置頂引導**：外語 `i18n/<locale>.json` 統一帶八語定版系列後綴；每支上架包交付一則低門檻二選一置頂留言草稿並勾選系列播放清單。
- 已升為規則：`.agents/skills/curio-episode/SKILL.md`、`docs/videos/explainer-series/README.md`、`docs/videos/packaging-refresh-20261111/README.md`、`.agents/skills/youtube-video/references/publish.md`。

