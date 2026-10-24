# S52 R7｜獨立史料與書面畫面覆核：HOLD

2026-10-20 UTC。只審下列 R7 精確五檔；R6 的 PASS 不沿用。直接重讀固定 Cook／Kippis 全文，再核 `claims.md`、`video.json`、`script.md`、企劃與研究筆記。**旁白逐句主張 PASS；113 張插畫提示詞與 3 張卡的書面畫面 PASS；公開章節／說明欄的來源措辭 HOLD，因此整個來源與畫面關卡 HOLD。**這不是兩位新讀者的敘事盲評，也不是政策、真實語音、原生生成圖或成片驗收。

| R7 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `f1b99c9bead5a9fb3db48b35fd4e1bab453706ee6c61506300bf189350731ad2` |
| `research.md` | `9801a0276575d6ec7087cff6fda93594eb3b5ecf06ed2bc5e536f718069c83ab` |
| `claims.md` | `a9128c55c5b79caa55c6fc1426751ff682e7bd1a16ad9fa6e73d6c066c9fa65a` |
| `video.json` | `299a4786575de86b35a9b5abcf9cb419177a5d642a2525a17aa1f5032e0a5148` |
| `script.md` | `4baf82930dd2b3c4eb48e91d117400775697da91c001ef6a852779209c2c72b5` |

本地原文 `/tmp/curio-s52-sources/cook-8106.txt` SHA `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`，`kippis-7777.txt` SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`；固定 commit URL 見 [research.md](../research.md)。C 是 Cook 日誌經 Wharton 1893 編輯轉錄；編者前言與夾注另屬後出材料。K 是 Kippis 後出傳記，沿用既有觀測敘述，不是第二次獨立量時。

## 逐句與畫面結論

- [C L5375–5414](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5375-L5414)寫 4 月 15 日選海灣東北岸、設線時大溪地人圍觀、Cook 不確定溝通是否被理解，並記留守帶隊軍官下令開槍、一名大溪地人死亡；Cook 與 Banks 約半英里外聞槍才回。R7 旁白保留當地人在場、設線及理解不確定，刪去死亡事件支線；`brief.md`、`research.md` 與 `video.json` 說明欄仍明列死亡及 Cook 非現場目擊，沒有替死者加動機或畫傷害過程。這符合本版明示的編輯邊界。
- [K L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)支持皇家學會 1768 年 2 月 15 日請求、原列馬克薩斯／友誼群島候選與 4 月 3 日已覓船；日地距離目的正確歸給 [C 編者前言 L793–803](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L793-L803)，非 Cook 當日日誌。新增 `s52301` 的候選島有據，`s52302` 的 Morton 提醒和 `s52303` 的觀測前夜焦慮均明確歸 Kippis [L1133–1154](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1133-L1154)，未扮作 Cook 目擊。
- [C L5941–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5941-L5975)確認 5 月 30 日準備與教導、Gore 6 月 1 日往 Eimeo、Hicks 6 月 2 日**清早**往島東、6 月 3 日無雲且空氣極清、幾乎無風、Cook／Green／Solander 的接觸讀時分歧及內接觸難判。`s52074` 提示詞的清早光線吻合。Cook／Green 望遠鏡同倍率、Solander 較大；新增 `s52305` 只說前兩人仍列於讀時不同者，未推出唯一成因。Cook 的 `Atmosphere or Dusky shade` 保持當事人用語，不宣稱已證實金星大氣或單一現代效應。編者前言的 `June 1st` 誤記沒有進旁白。
- [K L1165–1185](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1185)在表**前散文**寫 `According to Mr. Green`，表內一人四格為 09:25:42、09:44:04、15:14:08、15:32:10。首兩格相隔 18:22、後兩格相隔 18:02，兩段差 20 秒，首尾跨 06:06:28；`s52094/90/91/52201/52203/52204/52207/52208` 均按格林一人與此算術敘述，沒有把 20 秒當三人差。`s52306` 明說本集未核 Green 原刊。新增概念接觸示意 `s52304` 及相關畫面未重建器械或裸眼看太陽。Cook [L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)的 6 月 4 日 `return'd with success` 沒有逐人秒數；`s52127→s52128` 和 `s52132` 正確區分兩隊歸來與主站三人秒差的資料缺口。
- 全部 113 個非空插畫提示詞與 3 張文字卡逐景檢過。岸上有居民，未畫 4 月 15 日開槍、傷口、Cook 在場目擊或已同意築站；圖中的天象圓點和鐘面是示意，未指定未核的光學零件、三人精確差值或未核原刊內容。書面畫面 PASS 只表示提示詞及卡文不與來源和旁白衝突，仍須看原生生成圖。

## 必修項

1. `video.json` 的 `s52069` 章名 **「六月一日，兩隊出發」**把兩隊都放在 6 月 1 日。Cook [L5950–5960](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5950-L5960)明記 Gore 1 日、Hicks 2 日清早。改成「六月一至二日，兩隊出發」等不誤定日的章名，重生 `script.md`，並核章節輸出。
2. `video.json` 的 YouTube 說明句 **「格林的一組四個時刻只見於 Kippis 後出轉錄」**未限定「本集已核的兩份文本」，會被讀成其他史料沒有這四格；Kippis [L1183–1185](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1183-L1185)還指向 *Philosophical Transactions* 卷 61。本集沒有核該原刊。改成「本集核對的格林四個時刻取自 Kippis 後出轉錄；未核格林原刊」等限定來源範圍的句子。
3. `claims.md` 的 `s52127` 在有效的 `[J L5977–5982](…)` 後緊貼第二份裸露的 `(https://…#L5977-L5982)`，造成重複網址殘留。刪掉裸露副本，保留 J 與 I 兩個固定行錨。此處來源本身正確，是主張表呈現修補。

作者修三處後須重新凍結五檔 hash，再由另一位工作者核精確差分；本 HOLD 不能當修後 PASS。

## 機械與時長

117 景＝113 插畫、3 卡、1 片尾；113/113 插畫提示詞非空；119/119 句 ID 唯一、與主張表同序同字，117 景 ID 唯一；`screenplay(doc)` 與 `script.md` 逐位元相同；18 組 setup/payoff 全在稿內且依序有效。`node tools/video/cli.mjs lint --slug curio-s52 --json` 為 **0 errors／0 warnings**；`npm run check:tasks` exit 0，驗證 2,124 票（另有其他票的既有警告）。`estimateTimeline` 在 250／300／325 CPM 的濃縮開場為 **42.90／37.00／34.90 秒**，正文為 **563.30／486.20／458.97 秒**；325 CPM 僅 **7:38.97**，正文八分鐘仍須真實 TTS／音檢。未做 S52 語音、插圖、配樂或網站操作。
