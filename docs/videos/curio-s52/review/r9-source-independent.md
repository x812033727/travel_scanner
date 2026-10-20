# S52 R9｜獨立史料與書面畫面覆核：PASS／PASS

2026-10-20 UTC。此判定**只綁定** [R9 作者凍結](r9-author-freeze.md)的下列五檔，不沿用 R8 的 HOLD，也不替代兩位新讀者盲評、政策、站台、真實語音或生成圖驗收。重新讀兩份固定全文的相關原文、117 句口播及主張對照、111 張插畫提示詞、3 張卡、8 個公開章名與說明欄。**史料 PASS；書面畫面 PASS。**

| R9 精確內容檔 | 重算 SHA-256 |
| --- | --- |
| `brief.md` | `111be5ff148cc4eac2f03f47170c733d1dd7ea0c5cb83cf6dd366cd4e388f551` |
| `research.md` | `2c250ef9cbab57599978db34567e7737680b264442bfbd9d3f89d31a61633a1e` |
| `claims.md` | `0d7bb27e448f983e0f09ff4b124ccd4495454000b0f692356d8894c9f4cad7ea` |
| `video.json` | `f4c4276a83adf04719782887fd7b88e01960ebedf316404e93b8a1a2672fd03e` |
| `script.md` | `927e1cd8f4e787afb8ae998c49985e61b7612400e375e3c4dadcb4995b108f16` |

本地固定 Cook 全文 `/tmp/curio-s52-sources/cook-8106.txt` 重算 SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`；Kippis 全文 `/tmp/curio-s52-sources/kippis-7777.txt` 重算 SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`。固定 commit URL 見 [research.md](../research.md)。Cook 是經 Wharton 1893 編輯轉錄的船長日誌；Kippis 是後出敘述，不能算另一組獨立觀測。Cook 編者前言誤寫 `June 1st`，本稿以 6 月 3 日當日日誌為準。

## R8 HOLD 修正及 R9 定點改句

- Cook 的 [`[April 1769.]` L5049](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5049)先於 [L5439–5457 的星期一 17 日與受雲遮蔽的木星第一顆衛星食](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5439-L5457)，[`[May 1769.]` 到 L5592](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5592)才開始。`s52307` 旁白、`claims.md` 與 `script.md` 均為「四月十七日」；`s52307/08` 提示詞均為 `17 April 1769 night`；企劃 A 節拍、研究 R02A 與 `s52053` 解釋亦為四月。未把 4 月受雲阻礙說成 6 月 3 日凌日失敗，沒有暗示與 4 月 15 日同一頂帳篷。
- [Cook L5950–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5950-L5982)記 6 月 1、2 日兩隊出發、3 日晴空與三人接觸讀時分歧、4 日兩隊「成功」返回；它沒有給外派兩隊逐人的四格秒數。[Kippis L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)的 `According to Mr. Green` 在表前散文，只給格林一組四格。`s52078/79` 現在問「只看這幾天的庫克日誌」可否對上三處逐人讀時；`s52127/28` 回答這份日誌與 Kippis 格林表不能逐項比對，沒有宣稱別處不存在外派觀測資料。四格 09:25:42／09:44:04／15:14:08／15:32:10 及表內 18:22、18:02、20 秒的兩段差與原文、算術吻合；沒有拿這 20 秒冒充三人差值。
- `s52206` 現接在晴空、空氣清澈之後，以圓盤邊緣判讀導入接觸問題，與 [Cook L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)的記述相符；提示詞是紙上圓邊及空白時刻單。`s52036` 無武器旁枝、`s52132` 重述及曝曬溫度計口播均已刪去。接觸時刻的「大氣或暗影」仍歸於 Cook 的用詞，沒有當作已核定的現代單一成因。

其餘主張的主要錨點仍符合 [R8 逐句查核](r8-source-independent.md)：[Kippis L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)的皇家學會請求、[Cook 1893 編者前言 L790–803](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L790-L803)的日地距離目的、[Cook L5371–5425](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5371-L5425)的設站與英國守衛隊開槍死亡、[Cook L5941–5962](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5941-L5962)的準備及分遣、[Kippis L1133–1154](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1133-L1154)的後出補述，均依敘述者標示。企劃、研究及 YouTube 說明保留 4 月 15 日死亡、Cook 非現場目擊與無大溪地人獨立證詞的界線；劇本未虛構同意、目擊或動機。

## 書面畫面、形式及未過關項

115 景＝111 張插畫、3 張資料卡、1 個片尾；117/117 句 ID 唯一，`video.json`、`script.md`、`claims.md` 同序同字；111/111 插畫提示詞非空且逐景與旁白、日期及來源層級相符。3 張卡分別標 Kippis 的大溪地人姓名轉寫、Cook 的「大氣或暗影」、Kippis 的格林一組四格，未造假三人或三處精確讀秒。提示詞用匿名人物、紙上示意與遮蓋的泛稱儀器；沒有畫裸眼直視太陽、未核精密器材或開槍死亡過程。`s52014` 船邊複合場景等仍須在實際生成圖時看是否憑空畫出確定船型／史料，但書面提示詞本身不構成衝突。

146 個 `claims.md` 來源連結全部指向這兩份固定 commit 並帶行錨；114 條史實／設問句均有來源，另 3 條片尾互動句不新增史實。`screenplay(doc)` 與 `script.md` 逐位元相同；18 組 setup/payoff 均存在且順序正確，公開 8 個章名與 6 月 1–2 日的先後相符。`node tools/video/cli.mjs lint --slug curio-s52 --json` 為 **0 errors／0 warnings**、117 lines。`look` 為 `cute-mystery`、有配樂設定；YouTube 說明含兩份固定來源、來源限制、4 月 15 日事件與頻道連結。

企劃保留 **30–60 秒濃縮開場後 5 秒原版動畫片頭**、**21 秒片尾與末 16 秒兩推薦框／訂閱圈**，片尾有三句旁白。作者按 250／300／325 CPM 估開場 44.33／38.20／35.97 秒、正文 562.93／485.60／458.27 秒；最快估值低於八分鐘，須以真實 TTS 測量。動畫、成片與 Studio 可點連結尚未實作或驗收；這份 PASS 僅放行 R9 的史料與**書面**畫面給下一關，不代表媒體已完成。
