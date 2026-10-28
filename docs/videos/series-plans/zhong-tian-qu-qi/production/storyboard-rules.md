# 種田娶妻 分鏡規則（第 6 集起必守）

站主 2026-10-16 看完第 1–2 集：「貼圖感太重」「語音跟影片好像有些脫鉤」。量到的原因與之後的寫法：

## 說話的鏡頭一定會動嘴（站主：「之後的分鏡說話鏡頭都照這個寫」）

- 只要台詞的 `speaker` 在這一鏡的 `characters` 裡（人在畫面上說話），`data.motion` 第一句就寫他在說這句話：`Xu Yan speaks a short Mandarin line, 「…」, his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes`，動作接在後面。兩句以上寫 `speaks 2 short Mandarin lines, 「…」 then 「…」`。
- 說話鏡頭不能是 `visual: "still"`，也不要用 `data.source` 切別鏡的素材（切來的嘴型對不上這句台詞）。
- 畫外說話（`X speaks off screen`）時，畫面上的人要有反應動作（轉頭、皺眉、握拳），不是站著。
- 第 1–2 集照這個重拍了 34 鏡（`hailuo/gen-speak.mjs` 產生提示詞），試拍 e1-s23 嘴型明顯會動。

## 少用靜圖，台詞不要長過片段

- 第 1 集靜圖緩推占 19%、第 2 集 27%，加上台詞比 4 秒片段長時停在最後一格（7–8%），整集就像貼圖。
- 靜圖只用在沒人說話、本來就該停住的畫面（插入鏡頭、系統面板的主觀鏡頭），一集不超過 10% 的時間。
- 一個鏡頭的台詞（含前後空白）控制在 4 秒內；長的台詞拆成兩鏡（說話人正面、聽的人反應）。剪接遇到超長時會先把片段放慢最多 1.6 倍，還不夠才停格。

## 收工前要用聲音看一遍

- 只看聯絡表與第 0 格 PSNR 抓不到對嘴問題；每集交出去前要開聲音看完整一遍，特別注意畫面上的人說話時嘴有沒有動。

## 剪接（v4 起）

2026-10-16 和熱門 AI 真人劇比過（《冷宮醫后》前 120 秒：鏡頭中位數 1.25 秒、大量特寫與局部、依場景冷暖、配樂與音效滿版），第 1 集 v3 的中位數是 2.75 秒、沒有配樂音效、整集同一種金色光。之後每集用 `hailuo/assemble-v4.mjs` 加一份 `edit-e00N.json` 剪：

- 台詞 1.07 倍速，前後空白縮短；超過 3 秒的鏡頭切成原景＋1.3 倍推近（`punch` 可改推近位置）。
- 分場調色（`grades`：office／night／river／indoor／day）＋暗角＋顆粒，壓掉 AI 的均勻亮光。
- 片名卡、角色第一次出場的名牌（`names`）。**字幕用 CC 軟字幕，不燒進畫面（站主 10-16）。**
- 配樂用 Lyria 依情緒生成幾段 cue（`music-zt.mjs`，每首約 US$0.08），用 sidechain 壓在台詞下；音效用 CC0 音效庫，系統台詞前自動「叮」。

## H3 正文與秒數（2026-10-28 起；站主再看仍有貼圖感後量到的三個原因）

原因與來源寫在 `.agents/skills/minimax-h3-colab/references/motion-quality.md`：每支只買 4 秒（107 幀，低於 H3 訓練範圍 124–362 幀）、剪接用複製幀慢放再停格、正文沒有風格詞與首格錨句而且固定尾句跟運鏡打架。`hailuo/gen-dh.mjs` 與 `hailuo/assemble-v4.mjs` 已照下面改，分鏡要配合：

- **秒數**：`gen-dh.mjs` 預設買 5 秒；畫面上有人說話約 3 秒以上、或 motion 有兩拍（`then`、`;`）買 6 秒；`data.buy_seconds` 可指定。多的在剪接切，比停格便宜（5 秒 60 點、6 秒 72 點；以前 4 秒 48 點）。
- **motion 寫軌跡，不寫狀態**：起點 → 預備動作（移重心、吸一口氣、先看一眼）→ 主動作加重量與物理的字（weighted step、the sleeve catches the air、momentum carries the arm through、settles）→ 收勢。一鏡一事；兩個動作就拆鏡或買 6 秒。
- **運鏡只寫在 `camera`**，motion 裡不要再寫 the camera…（`gen-dh.mjs` 會把尾巴的 camera 子句丟掉並列出鏡號）。`locked` 就是 locked：正文寫 `The camera holds a static shot`，不再改成慢推；要推就寫 `slow push in`，整集不要都是同一種推。
- **說話句照舊放在動作前**；嘴要閉的鏡頭寫 `lips remain closed`。
- **剪接**：台詞比片段長時 `assemble-v4.mjs` 慢放上限從 1.35 降到 1.25，而且用光流補幀（`minterpolate`）不再複製幀；還不夠的鏡頭 note 會印 `held`，下一集那種鏡頭買 6 秒。補幀慢（1080p 一支慢放鏡約 1–2 分鐘 CPU），所以秒數買夠、少讓它慢放才是正解。`edit-e0NN.json` 可用 `"interpolate": false` 退回舊行為、`"slow_max"` 調上限。
- 新寫法的效果沒有實拍對照（站主 10-28 定不排小樣）：第 31 集起用新寫法，看成片時特別看說話鏡有沒有在 6 秒內做完動作、locked 鏡有沒有漂。
