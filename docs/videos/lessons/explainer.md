# 解說系列共用（奇聞檔案局＋原來如此事務所）：教訓

兩個旁白解說系列都會遇到的教訓。共同規則見 `docs/videos/explainer-series/README.md`；只跟其中一個系列有關的，寫在 `curio.md` 或 `sothatswhy.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟兩個系列的 `_規則與教訓/教訓/解說系列共用教訓.md`（docs/videos/rules-sync）。

## 2026-11-13 · curio-s42／curio-w02／story-b01／sothatswhy-p18／sothatswhy-p23 · 一般觀眾視角六支連看檢討
站主請 AI 以一般觀眾視角連看頻道最新六支影片，抓出五個跨集重複出現的結構問題：
- **對話做片漏寫 `pauses`／`still_motion` 與「一句一景」抵銷緊湊停頓**：用 Claude 對話配對影音權杖做片走本機 `cli.mjs`，不跑主機 `settle()`，S42 與 B01 漏寫就退回 300／700 毫秒舊停頓；而寫了 `line_ms: 0` 的集數若把稿子切成一句一景（S42 92 句／73 景、B01 137 句／137 景、P23 71 景裡 50 景單句），每句結尾都變成 `scene_ms` 換景停頓，`line_ms: 0` 形同虛設。同角色同節拍連續 2–3 句要併進同一個 `scene.lines[]`。
- **Gemini 把 `voice.style` 語速打折**：寫「一秒四到五個字」甚至「一秒五個字以上」時，`Sulafat`／`Leda` 實測常落在 3.6–4.3 字／秒，不到站主定的 4.4 字／秒下限；可在 `voice` 加 `"tempo": 1.08`–`1.15` 用 `ffmpeg atempo` 不變調微加速達標。
- **縮圖破梗或選空白靜物**：P23 縮圖直接寫「鏡子沒翻左右／翻的是前後」把全片答案講完；W02 縮圖右框放一本闔上的無字紅皮書，手機列表毫無吸睛度。縮圖只寫反常識衝突或硬數字、嚴禁破梗答案，右圖必選誇張表情或強烈反差。
- **內部查核與作畫備註寫進公開說明欄**：S42、W02、B01 在 `youtube.description` 寫史料算式與「誰過世超過四百年、誰不畫臉」，像內部工程紀錄；一律留在 `claims.md`，說明欄只留給觀眾看的鉤子、受眾、章節、乾淨來源與系列 hashtag（`#奇聞檔案局`、`#原來如此事務所`、`#品牌故事`）。
- **外語標題漏系列名、留言區零置頂引導**：外語 `i18n/<locale>.json` 統一帶八語定版系列後綴；每支上架包交付一則低門檻二選一置頂留言草稿並勾選系列播放清單。
- 已升為規則：`.agents/skills/curio-episode/SKILL.md`、`docs/videos/explainer-series/README.md`、`docs/videos/packaging-refresh-20261111/README.md`、`.agents/skills/youtube-video/references/publish.md`。

