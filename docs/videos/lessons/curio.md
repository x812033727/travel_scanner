# 奇聞檔案局：教訓

只跟奇聞檔案局有關的教訓。所有 AI 劇都會遇到的寫在 `shared.md`，奇聞和原來如此都會遇到的寫在 `explainer.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟 `AI劇/奇聞檔案局/_規則與教訓/教訓/教訓.md`（docs/videos/rules-sync）。
之前的教訓：`.agents/skills/curio-episode/references/w03-lessons.md`。

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
