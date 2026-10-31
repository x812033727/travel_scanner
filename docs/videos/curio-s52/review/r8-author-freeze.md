# S52 R8｜R7 公開資料 HOLD 與雙人敘事 FAIL 的作者修稿

2026-10-20 UTC。[R7 獨立來源／書面畫面](r7-source-independent.md)對其逐句旁白及書面畫面 PASS，卻因三處公開資料問題判整關 HOLD；[兩名新讀者正式合併](r7-merged-narrative.md)的 `no_spoiler`、`chapters_link`、`no_recap`、`no_detour` 四題 FAIL。以下是作者修稿及本地機械驗證，**不是** R8 獨立來源、畫面或敘事通過。

| R8 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `f37cf719962ee51c0f1d85bb68fa682b34cca341a91795487fb04c0940f50a6d` |
| `research.md` | `0754754d882e465db696227137fc96b16428a3ec6a05f8a1bac67b9708594091` |
| `claims.md` | `7ae40a021a894fcce9d8d1c79363027a6dfbdf2c4059008e40655d7875483c12` |
| `video.json` | `e9955702d9236c8dda062f2321fabf7db0dec93fa3e3d81b2120f51a3cbf373c` |
| `script.md`（CLI 重生） | `69998ebb3a7e29f61d7b0ed78649235afd9dbe48a3c424b3e90749111593d612` |

定點修補：

- 開場 `s52001`–`s52004` 改為三人在 6 月 3 日觀測處**等待接觸並準備各自記時**，不先說整天無雲或看完整段凌日；`s52008` 改為「**就算**天空如願放晴」的條件問句。首章章名同步改為「六月三日，觀測處等待接觸」。晴天與完整觀測留給 `s52082`–`s52084` 首次揭示。開場的觀測場景、五個待答問題與 30–60 秒時長保留。
- `s52102` 作為接觸分歧章第一句，直接回答上一章 `s52101`：Cook 說暗影**干擾接觸時刻判定**。`s52103` 接著說三人各自記時，`s52105→s52106` 再揭示是否一致；不在章首重講圓邊模糊。對應概念畫面轉為記時紙條，不畫具體未核秒數。
- 四月岸上段刪 `s52030` 船炮射程、`s52038` 溝通不確定口播及 `s52049` 隔日移船；仍留 `s52035` 帳篷及佔地、`s52036` 當地人圍觀且無武器。新 `s52307→s52308` 緊接同處 5 月 17 日 Cook／Green 在岸上準備觀測**木星衛星食卻被雲擋住**，使觀測處真實受天氣影響；`s52053→s52054/s52058` 回到 6 月金星的儀器準備與分遣備援。這是另一次觀測，**不推斷 6 月 3 日曾有雲**，也不稱測試、演習或同一頂帳篷。4 月 15 日英國守衛隊開槍打死一名大溪地人、Cook 非現場目擊的史料仍在 `brief.md`、`research.md`、YouTube 說明欄，來源視角界線保留。
- 新 `s52309` 據 Cook 5 月 31 日條加入長艇傍晚完工，銜接 Gore 6 月 1 日乘長艇出發；不說長艇原先損壞。`s52069` 公開章名修為「**六月一至二日，兩隊出發**」，分別對齊 Gore 1 日與 Hicks 2 日清早。YouTube 說明改成「**本集核對**的格林四個時刻取自 Kippis 後出轉錄，尚未核格林原刊」，不冒稱別處沒有原刊。`claims.md` `s52127` 移除重複裸網址，保留 Cook 6 月 4 日與 Kippis 格林表的兩個有效固定錨點。

固定 Cook／Kippis 全文 SHA 未變：`c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`、`c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`。新增事實直接據 Cook [5 月 17 日 L5439–5457](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5439-L5457)與 [5 月 31 日 L5941–5950](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5941-L5950)。Cook 的「大氣或暗影」仍只作當事人詞語；Kippis 表仍只作 Green 一組四格，表內兩段差 20 秒仍不當三人秒差，亦不推定未核原刊不存在。編者前言誤寫的 `June 1st` 不替代 Cook 當日 `June 3rd`。

作者本地機械檢查：**117 景**（113 插畫、3 卡、1 片尾），**119/119** 句 ID 唯一且與 `claims.md` 同序同字，`screenplay(doc)` 與重生 `script.md` 逐位元相同，**18 組** setup/payoff 均在正確順序。`lint --slug curio-s52 --json` **0 errors／0 warnings**；250／300／325 CPM 的濃縮開場 **44.33／38.20／35.97 秒**、正文 **567.83／490.00／462.53 秒**。325 CPM 估值仍未達八分鐘，必須以真實 TTS 及音檢判定硬關。`npm run test:docs-videos` **236/236**、`npm run check:tasks` **2,124 票**、`git diff --check` 通過。沒有呼叫 S52 付費語音、插圖或配樂。

下一手應按上列**精確五檔 SHA**由另一位工作者重核逐句來源、書面畫面、章名和 YouTube 說明，再由兩位此前未讀 R8 企劃、史料或評語的新讀者各只讀 R8 純旁白，按固定 13 題盲評並正式合併。兩關通過後才考慮政策、站台劇本卡、真實 TTS／音檢與媒體。
