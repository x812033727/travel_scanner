# 奇聞檔案局：教訓

只跟奇聞檔案局有關的教訓。所有 AI 劇都會遇到的寫在 `shared.md`，奇聞和原來如此都會遇到的寫在 `explainer.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟 `AI劇/奇聞檔案局/_規則與教訓/教訓/教訓.md`（docs/videos/rules-sync）。
之前的教訓：`.agents/skills/curio-episode/references/w03-lessons.md`。

## 2026-11-14 · curio-f01 · 獨立觀眾評審（Audience Review）發現

對 F01（1812 格林初版灰姑娘）進行深度觀影體驗評審（評分 93.5/100，Grade A），吸取 H36 經驗並發現三項前置防禦瑕疵：
- **提示詞景別前綴去重（Prompt Prefix Idempotency）**：在將景別（如 `Close-up insert of`）拼接進提示詞時，若原始描述已帶有景別前綴，會疊加出 `Close-up insert of Close-up insert of`，浪費 token 並干擾生圖模型權重。下次怎麼做：提示詞組裝工具必須先做冪等去重，確保景別前綴永遠只出現一次。
- **Speaker 與 Motion 屬性脫鉤（Decouple Speaker from Motion）**：`motion` 欄位不可盲目按說話者套用 `Chief/Kid keeps subtle ambient drift`。純物件鏡頭（`nobody: true`）與 19 世紀歷史重現鏡頭必須填寫鏡頭運鏡（`Subtle cinematic lighting drift and gentle optical drift`），嚴禁讓所長微動套入歷史或無人特寫。
- **古籍與文獻鏡頭嚴禁提示具體文字（No Text in Period Prop Prompts）**：展示古書、封底、標題頁時，嚴禁提示詞要求模型生成特定單詞（如 `Bäumlein` 或 `1812 gothic Fraktur`），模型極易生成怪異亂碼而破壞滿版美感。下次怎麼做：寫為 `aged leather bound folio with clean blank debossed crest, zero text, zero letters`，具體文字留給後製 CC 字幕或字卡。
- **防離場結案章鎖定成功**：將結案章句精確鎖定在倒數第 3 景（Shot 166），其後僅留 6.5 秒（互動提問 1 句 + 訂閱 CTA 1 句），徹底杜絕 H36 完播率斷崖現象。

## 2026-11-14 · curio-h36 · 獨立觀眾評審（Audience Review）發現

對 H36（卡迪夫巨人騙局）進行深度觀影體驗評審（評分 86.0/100，A-），發現四項重大體驗瑕疵與升級經驗：
- **片尾離場標誌（結案章）排他鎖定（防完播率雪崩）**：`奇聞檔案局，第 X 號結案！` 是最強烈的離場信號（Exit Cue）。H36 曾將結案句放在倒數第 15 景，後面還拖帶巡迴與大眾心理學，導致觀眾聽到結案就離開、完播率斷崖。下次怎麼做：結案章必須是敘事與哲理總結的最後一句話，其後僅允許 1–2 句（≤ 8 秒）的提問與訂閱 CTA。
- **`nobody: true` 提示詞無人/人物衝突（Prompt Negation Clash）**：生圖模板強制插入 `completely empty with zero humans, zero bystanders, zero limbs`，若同一景描述又出現「兩名工人靠在鐵鏟旁」或「遊客排隊」，模型會產生幽靈殘肢或畸形假人。下次怎麼做：純無人機制景（工具、岩石、金幣、報紙、門票、印章）才設 `nobody: true`；1869 年歷史人群與工人不設 `nobody`，提示詞寫為 19 世紀復古匿名剪影／群像（`Historical editorial scene featuring anonymous 19th-century period figures`）。
- **縮圖嚴禁指定辦公室/所長 Shot 0（CTR 毒藥），且嚴禁字卡破梗劇透**：H36 原本縮圖指定 `7jnm`（所長在辦公室拿資料夾），在推薦流中點擊率會暴跌；字卡寫 `雙巨人 全是假` 也破壞了懸念。下次怎麼做：縮圖必須綁定全片最具視覺衝擊的核心奇觀（如泥坑巨石腳趾 `xd9z`、石人出土或雙巨人對峙），字卡維持衝突反問（`**假告假**\n誰是真？`），嚴禁直白宣告謎底。
- **喜劇神包袱留白（Comedic Beats）**：荒謬神反轉（如「假貨罵假貨是假貨！」「叫一塊石膏舉手宣誓！」）全片機械式 150ms 換場停頓讓大腦來不及發酵笑點。下次怎麼做：在核心反轉與吐槽句後方注入 350–500ms 停頓留白，讓觀眾會心一笑與沉浸。
- **劇場級動畫光影 × 厚塗水粉質感定案**：16:9 滿版、暖深褐色手繪墨線、窗邊斜射暖金日光、髮絲輪廓光、空氣微細光塵、奶油散景、無文字空白介面。
- 已升為規則：`.agents/skills/curio-episode/SKILL.md` §每一集的順序與檢查、§標題與縮圖、§插圖提示詞怎麼寫。

## 2026-11-13 · curio-s10／s13／s14／s23–s26-v2 · 站主發現、Claude 量
設定都是新版，實測語速卻都不到 4.4：停頓（0／150 毫秒）與 beat 都對，聲音指示也寫了「一秒四到五個字」，七集實測只有 4.08–4.33 字／秒。站主定 4.4 為下限，不符合的全部重做，八語改用 MiniMax 重錄。
- **怎麼量**：timeline.json 每句 `audio_samples` 加總 ÷ 48000 是純講話秒數；字數用稿子去掉空白與標點。全片長度除會把換景停頓算進去，偏低。
- **為什麼慢**：Gemini 會把聲音指示裡的速度打折扣，要寫比目標快的速度（原來如此寫「一秒五個字以上」才念到 4.4）。
- **下次怎麼做**：錄完旁白先量語速，到 4.4 才送審；check-audio 過了不代表語速對。
- **重錄的限制**：同一集正在跑 `keyframes` 時，`tts` 會被鎖（「the project is held by keyframes」）什麼都不送；換聲音指示的重錄排在關鍵影格畫完之後。
- 已升為規則：`.agents/skills/curio-episode/SKILL.md` §系列定案〈語速與停頓〉〈八語〉。

## 2026-11-13 · curio-s23-v2／s24-v2／s25-v2 · Claude（c14 重做）
image-01 插圖過了 judge 還不夠，獨立放大檢查每集都抓出約一半要重畫。三集都反覆出現下面這些問題，都是 judge 放過、放大看才看到的：
- **錶面、刻度、書頁會長出字或數字**：寫「closed」「face down」都沒用。改成闔上的木製錶盒、闔上的書、綁繩的卷軸、捆起來的紙束。錶盒的黃銅扣片會被看成眼睛或字，寫 `a plain wooden box tied with a simple cord`。
- **只寫手的鏡頭會冒出整張臉**：常常就是那位不該入畫的人（例如 1912 年的寫信人）。一律改成只畫物件的靜物，並設 `nobody`。
- **畫風開頭**：`Flat 2D drawing, bold dark outlines, simple shapes.` 有效。換成 `Flat 2D picture, heavy dark linework.`、`Flat 2D image, strong inked contours.` 幾乎都被畫成動畫背景或 3D。lint 會警告這個開頭用太多次，不用理它。
- **戶外場景**（樹、果園、草地）：一直被畫成柔邊的白天風景。改成 `deep navy night sky` 配單一物件的近景才過。
- **三角帽**（牛頓的代表物）：俯視一直畫成軟呢帽、牛仔帽，甚至長角。正面視角（`Front view of a plain matte black three-cornered tricorn hat with its wide brim folded up into three sharp points`）才畫得出來。帽子要全集一致：宣告代表物的那一景，要跟後面每一景同一頂。
- **Ada 走樣**（變小孩、包頭、短髮、短袖、耳環、眼鏡歪）：固定描述要加 `shoulder-length wavy black bob with a side fringe, white collared shirt under a long-sleeved mustard knit cardigan, adult proportions, chest up`。手上不拿東西，只寫一個表情。
- **天平、弩炮、倒插的箭、打開的門**：模型畫不出特定的傾斜或方向。改成不靠那個動作也能對上旁白的畫面，例如用兩樣東西對比、畫結果、換一個物件。
- **judge 只因小地方退件的 take**（瀏海少一撮、多一個髮夾）：放大檢查乾淨的話，可以用 `keyframes import --provider external --usd 0` 直接選用，比一直重畫省錢。
