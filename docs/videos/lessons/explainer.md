# 解說系列共用（奇聞檔案局＋原來如此事務所）：教訓

兩個旁白解說系列都會遇到的教訓。共同規則見 `docs/videos/explainer-series/README.md`；只跟其中一個系列有關的，寫在 `curio.md` 或 `sothatswhy.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟兩個系列的 `_規則與教訓/教訓/解說系列共用教訓.md`（docs/videos/rules-sync）。

## 2026-11-14 · sothatswhy-p12-qr-code · 成片獨立觀眾視角評分關卡（修完才推後台與備份）與八語 MiniMax 配音防呆
站主定案「把觀眾評分加入流程，修完後才推後台跟備份」，將獨立觀眾體驗審查與 P12 八語逐句驗音抓出的跨系列規則收進兩個解說系列共用流程：
- **成片獨立觀眾評分關卡（先修完再備份與 `review-push`）**：兩個解說系列在 `assemble` 與 `qa`（11/11）通過後，禁止直接備份或送審，必須先派**未參與撰稿與生圖的獨立子代理**扮演一般 YouTube 觀眾，同時檢視縮圖（含變體與八語縮圖）、標題說明欄、前 30 秒留存、無字插圖理解度、色溫節奏與收尾互動，寫出 `review/audience-review.md`（六項各 ≥ 7.5／10、總均 ≥ 8.0／10）；凡抓到縮圖裁切、圖解難懂、畫面疲勞或角色瑕疵，**一律先重繪／重組並重過 `qa` 11/11，確認零待修問題後才執行 Google Drive 完整備份與 `review-push --gate final`**。
- **厚塗水粉畫風的色溫呼吸與淺冷底示意圖**：採用暖金窗光＋厚塗水粉後，避免連續十幾鏡維持同一種暖棕木桌色調；每 6–8 鏡應安排明亮冷調藍天窗景、戶外日光或深藍夜空／太空冷色場景換氣，且純機制／數量對比鏡優先用淺米白或冷灰桌面襯托高對比色道具，確保手機小螢幕一目了然。
- **八語 MiniMax 配音（`dub --provider minimax`）跨語系發音防呆**：P12 八語共 1,272 句全數跑過 `check-audio --second-opinion` 抓出四類必防陷阱：(1) **印尼文（`id`）禁寫 `&`**：MiniMax 會把 `&` 唸成英文字母 `"FT"`，一律寫成 `dan`，並避開 `-k k-` 跨詞連音（如 `kotak kecil` 連音吞成 `kota kecil`）；(2) **越南文（`vi`）禁寫千分位句點 `.` 與全大寫詞**：`7.089`、`4.296` 會被當成小數點唸錯，四位數以上改寫成無分隔符 `7089` 或文字；全大寫強調詞（如 `CÙNG LÚC`）易被拼讀或糊音，一律用正常大小寫；單字母等級加分類詞（`mức H`），並避開聲調近音歧義（`hộp sửa`「修正盒」易聽成 `hộp sữa`「牛奶盒」，改用 `hộp cứu hộ`）；(3) **西／葡文（`es`／`pt`）單字母防連讀**：`Si H`／`Se H`／`Nível Q` 易與前後母音連讀成 `CH` 或 `nível que`，改寫為 `En nivel H`／`No nível Q`；(4) **泰文（`th`）緊窗口少塞英文縮寫**：泰語短句夾英文 `QR` 會觸發語種切換停頓而衝破 `fit.json` 時間窗，緊湊句優先用自然泰語指代（如 `ป้ายร้าน`）；若伺服器 Gemini ASR 偶發在轉寫開頭漏出 `"thought"` 觸發 `leaked word`，微調該句 1–2 字重錄即可刷新轉寫。
- 已升為規則：`AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`docs/videos/explainer-series/README.md`、`docs/videos/so-thats-why/dialogue-pilot-20261103/README.md` §9／§10.4／§10.8。

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

