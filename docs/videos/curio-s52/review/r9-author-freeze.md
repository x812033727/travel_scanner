# S52 R9｜4 月 17 日與敘事三項失敗的作者修稿

2026-10-20 UTC。R8 [獨立史料／書面畫面](r8-source-independent.md)因木星衛星食月份錯誤判 HOLD／HOLD；R8 [兩名新讀者正式合併](r8-merged-narrative.md)因 `payoffs`、`no_recap`、`no_detour` 判 FAIL。此處記錄 R9 **作者版**和本地機械檢查，不代替 R9 另一位工作者的史料／畫面覆核或兩位新讀者的盲評。

| R9 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `111be5ff148cc4eac2f03f47170c733d1dd7ea0c5cb83cf6dd366cd4e388f551` |
| `research.md` | `2c250ef9cbab57599978db34567e7737680b264442bfbd9d3f89d31a61633a1e` |
| `claims.md` | `0d7bb27e448f983e0f09ff4b124ccd4495454000b0f692356d8894c9f4cad7ea` |
| `video.json` | `f4c4276a83adf04719782887fd7b88e01960ebedf316404e93b8a1a2672fd03e` |
| `script.md`（CLI 重生） | `927e1cd8f4e787afb8ae998c49985e61b7612400e375e3c4dadcb4995b108f16` |

固定 Cook／Kippis 全文 SHA 仍為 `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`、`c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`。Cook [L5049 的 `[April 1769.]`](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5049)、[L5439–5457 的 17 日星期一及受雲阻的木星衛星食](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5439-L5457)、[L5592 的 `[May 1769.]`](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5592)界定該事件為 **4 月 17 日**。`s52307` 旁白與主張表、`s52307/08` 英文插圖提示詞、企劃 A 節拍與研究 R02A 都已同步；`s52307` 刪「又」以免暗示 4 月 15 日那頂帳篷留宿。舊 R8 快照保持不動，不能把其錯月引用當現稿。

敘事改動限於 R8 正式失敗：

1. `payoffs`：`s52078` 改問「**只看這幾天的庫克日誌**，三處逐人的接觸秒數能互相對上嗎」，避免暗示本集已檢查所有可能的外派原始文件；`s52079` 只核出發段當時未列讀時表，`loops` 的回收改指 `s52128`。`s52127→s52128` 在 6 月 4 日歸來記錄後回答：Cook [L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)沒有兩隊逐人四格時刻，不能與 Kippis 的格林一組 [L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)逐項比對；未宣稱外派人員沒有在別處留存資料。
2. `no_recap`：刪 `s52132`，因 `s52118` 已說明主站三人秒差在這份表中算不出。正文以 `s52128` 的外派隊資料缺口作新結論，然後進既有觀眾互動片尾。
3. `no_detour`：刪 `s52036` 的「沒有武器」旁枝；`s52026` 仍說岸地有人生活，企劃、研究與 YouTube 說明仍明列英國守衛隊 4 月 15 日開槍死亡及 Cook 非現場目擊。`s52206` 由無關的曝曬溫度計高溫改為晴朗天氣到「圓邊那一刻」的讀時轉折，概念插圖同步由溫度計改成圓邊與空白時刻單；不提前判定現代成因。

本地機械結果：**115 景＝111 插畫、3 卡、1 片尾**；**117/117** 句 ID 唯一並與 `claims.md` 同序同字，`screenplay(doc)` 與 CLI 重生 `script.md` 逐位元相同；**18 組** setup/payoff 順序正確。`node tools/video/cli.mjs lint --slug curio-s52 --json` 為 **0 errors／0 warnings**。250／300／325 CPM 估算濃縮開場 **44.33／38.20／35.97 秒**，正文 **562.93／485.60／458.27 秒**；300 CPM 為 **8:05.60**，最快估值 325 CPM 為 **7:38.27**。正文八分鐘硬關仍須真實 TTS 實測。`npm run test:docs-videos` **236/236**、`git diff --check` 通過。`look` 維持原定 `cute-mystery`，保留系列配樂設定、30–60 秒開場後的 5 秒原版動畫片頭、21 秒片尾和最後 16 秒兩推薦框／訂閱圈及來源／頻道連結計畫；動畫與 Studio 可點元素尚未實作。

下一手應按上列**精確五檔 SHA**由另一位工作者重核 Cook 四月／五月月份邊界、R9 改句、書面提示詞、主張與公開說明；由兩位此前未讀 R9 企劃、史料及評語的讀者各只讀 R9 純旁白，按固定 13 題盲評並正式合併。通過後才考慮全稿政策、網站劇本卡、真實 TTS／音檢與 MiniMax 畫面。本輪沒有呼叫 S52 付費語音、插圖或配樂，也沒有成片。
