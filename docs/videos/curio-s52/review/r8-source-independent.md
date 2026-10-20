# S52 R8｜獨立史料與書面畫面覆核：HOLD

2026-10-20 UTC。只覆核下列 R8 精確五檔；R7 的結論不沿用。重新讀固定 Cook／Kippis 全文、逐句主張、劇本、分鏡提示詞、企劃及公開資料。**來源 HOLD，書面畫面 HOLD**：新增木星衛星食段把 1769 年 **4 月 17 日**誤寫為 **5 月 17 日**，且兩個相連插圖提示詞也寫錯月份。其餘 118 句口播的史實未見新的衝突；除兩個錯月提示詞外，其他書面畫面未見新的衝突；這不放行全稿政策、網站卡、語音、原生插圖或成片。

| R8 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `f37cf719962ee51c0f1d85bb68fa682b34cca341a91795487fb04c0940f50a6d` |
| `research.md` | `0754754d882e465db696227137fc96b16428a3ec6a05f8a1bac67b9708594091` |
| `claims.md` | `7ae40a021a894fcce9d8d1c79363027a6dfbdf2c4059008e40655d7875483c12` |
| `video.json` | `e9955702d9236c8dda062f2321fabf7db0dec93fa3e3d81b2120f51a3cbf373c` |
| `script.md` | `69998ebb3a7e29f61d7b0ed78649235afd9dbe48a3c424b3e90749111593d612` |

固定原文仍是 `/tmp/curio-s52-sources/cook-8106.txt` SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`、`kippis-7777.txt` SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`；固定 commit URL 見 [research.md](../research.md)。Cook 是 Wharton 1893 編輯轉錄的船長日誌；Kippis 是後出的近時代敘述，不能當第二組獨立讀秒。兩份原文完整本地 hash 均重核相同。

## 必修：4 月 17 日寫成 5 月 17 日

Cook 本文先標 [**`[April 1769.]` L5049**](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5049)，在 [L5370 的 15 日星期六、L5429 的 16 日星期日、**L5439 的 17 日星期一**及 L5455–5457](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5370-L5457)記庫克與格林在岸上船用帳篷過夜，準備觀測木星第一顆衛星的食，受雲妨礙。直到 [L5592 才出現 **`[May 1769.]`**](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5592)。因此該 17 日絕非五月；錯誤不是資料來源有歧義。

受影響位置：

1. `video.json` `s52307` 旁白和由它產生的 `script.md` 說「五月十七日」；`claims.md` `s52307` 的句子與解釋也寫「5 月 17 日」。`s52053` 的解釋把雲阻也誤註「5 月 17 日」。`s52308` 旁白的雲阻本身有據，無需改事實。
2. `video.json` `s52307`、`s52308` 提示詞都指定 `May 17 night`，必須改為四月日期；否則圖文仍會給出錯誤時間。第 4 月 15 日岸上段之後接 4 月 17 日，在敘事順序上自然成立。
3. `brief.md` 的本版描述及 A 節拍、`research.md` 的 R02A 行與下一步描述均把此事定作五月。舊版 `review/r8-author-freeze.md` 是當時作者快照，應保留並由下一版凍結紀錄指出已被此審核推翻。

R9 最小修法：將上述口播、主張、企劃及研究統一為「**四月十七日**」；`s52307` 可順手刪「又」，避免暗示四月十五日曾在同頂帳篷過夜，因 Cook [L5425–5427](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5425-L5427)說當晚拆帳篷回船；`s52307/08` 英文畫面月份同步改為 April。重生 `script.md`、重新凍結五檔 SHA，再由不同人重核精確修訂。不要把 4 月 17 日雲阻說成 6 月 3 日金星凌日失敗。

## 其餘核對結果

- [K L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)支持 1768 年 2 月 15 日皇家學會請求派船、4 月 3 日已覓船及候選島。日地距離目的明確歸 [C 的 1893 編者前言 L793–803](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L793-L803)，沒有當成庫克當日口述。
- [C L5375–5425](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5375-L5425)支持 4 月 15 日設站及當地人圍觀；同段確記英國守衛隊開槍打死一名大溪地人，庫克與 Banks 在半英里外、聽槍才返回。R8 旁白聚焦觀測；`brief.md`、`research.md` 和 YouTube 說明仍明列死亡及庫克非現場目擊，未聲稱大溪地人已同意、未畫傷害場景。這只是本版清楚標示的編輯邊界，沒有替居民提供獨立證詞。
- [C L5941–5961](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5941-L5961)支持 5 月 30 日準備並教人使用儀器、5 月 31 日傍晚長艇完工、Gore 6 月 1 日往 Eimeo 和 Hicks 6 月 2 日清早往大溪地東方。R7 的 `s52069` 章名錯誤已改成「六月一至二日，兩隊出發」；長艇未被說成曾損壞。[K L1133–1154](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1133-L1154)的 Morton 建議與觀測前夜不安均標作 Kippis 後出記述。
- [C L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)是 **6 月 3 日當日日誌**：無雲、完整觀測、幾乎無風、曝曬溫度計較熱、接觸時刻受「大氣或暗影」干擾、三人有超預期讀時差。沒有把這句判成已證實的現代單一光學成因；1893 編者前言 [L1069–1073](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L1069-L1073)的 `June 1st` 誤寫未進旁白。
- [K L1165–1185](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1185)在表前散文歸給 Green，一組四格為 09:25:42、09:44:04、15:14:08、15:32:10。前兩格差 18:22，後兩格差 18:02，兩段差 20 秒；R8 清楚說這不是三人讀時差。YouTube 說明已限定「本集核對的……取自 Kippis，尚未核格林原刊」，沒有暗示原刊不存在。[C L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)的 6 月 4 日分遣隊返回和庫克稱「成功」有據，不推出逐人秒數。`claims.md` `s52127` 重複裸網址已去掉，仍留兩個有效固定行錨。
- 除日期錯誤的 `s52307/08`，其餘 111 張插畫提示詞與 3 張卡無明顯旁白／來源衝突。提示詞中的天象是概念紙圖，無裸眼直視太陽、未核器械零件、特定肖像或三人精確差值。書面提示詞的結論不能代替 MiniMax 原圖驗收。

## 機械、形式與未過關項

117 景＝113 插畫、3 卡、1 片尾；119/119 旁白句 ID 與 `claims.md` 同序同字、句 ID 唯一；113/113 插畫提示詞非空；18 組 setup/payoff 存在且順序正確；`screenplay(doc)` 與 `script.md` 逐位元相同。`node tools/video/cli.mjs lint --slug curio-s52 --json` 回報 **0 errors／0 warnings**、8 個章節。`look` 為原定 `cute-mystery`，有系列配樂設定，公開說明含兩份固定來源及頻道連結。企劃與分鏡保留 30–60 秒濃縮開場後 5 秒原版動畫片頭、21 秒片尾及最後 16 秒兩推薦框／訂閱圈的規格；R8 尚未實際渲染它們或設 YouTube Studio 可點元素。

以 250／300／325 字每分鐘估算，開場為 44.33／38.20／35.97 秒，旁白正文為 567.83／490.00／462.53 秒。最快估值 **7:42.53**，仍須以真實 TTS 判定八分鐘硬關。本輪沒有 S52 付費語音、插圖、配樂、網站卡或成片；兩位 R8 新讀者的敘事盲評是另一個關卡，不能用此史料報告替代。
