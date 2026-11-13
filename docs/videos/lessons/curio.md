# 奇聞檔案局：教訓

只跟奇聞檔案局有關的教訓。所有 AI 劇都會遇到的寫在 `shared.md`，奇聞和原來如此都會遇到的寫在 `explainer.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟 `AI劇/奇聞檔案局/_規則與教訓/教訓/教訓.md`（docs/videos/rules-sync）。
之前的教訓：`.agents/skills/curio-episode/references/w03-lessons.md`。

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
