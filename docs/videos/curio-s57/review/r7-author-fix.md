# S57 R7｜作者窄修與五檔凍結

2026-10-21 UTC。**R7 是作者候選，尚無本版的獨立史料、書面畫面或敘事 PASS。**[R6 來源報告](r6-source-independent.md)對 R6 歷史主張 PASS、書面畫面 `s57150` HOLD；[R6 正式雙盲合併](r6-merge/summary.md)為固定 OR **12／13 HOLD**，兩票共同 NO `no_recap`，A 單票另 NO `no_detour`。R6→R7 的[逐行 patch](r7-author-diff.patch) SHA-256 是 `0ae81484c0eb0a535fc845b3eaca332473b0722ff2135a599337d9f273f2a076`。這份紀錄只交代作者修法，不代替獨立審查。

| 創作檔 | R6 SHA-256 | R7 凍結 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `48f287375b22a77929130046c15c55079c78d9376996a033709dc7a1d625b933` | `0474bc0e793cbda07021da98b3ea972a50b60fe87eacb708baf85457bdf554f6` |
| `claims.md` | `71b0f3405bd254e7be0d464d34d81c98fb78b08951e046b331ec79a34af03919` | `d4b8958f6f9c7b7fd62ec172ae39279d096086f22f4bdcc1fb2c07ef79401d38` |
| `video.json` | `e766dbe4ac40932abfa5bea1a89713604b2fbb64158bf3523376bde0aa0131cc` | `f3befaaeb100cb0d9c275be56851691b174ef423777f1955375e520119bb71e7` |
| `script.md` | `f2d8c42f6b71698121199d7c3c26ddde958eddf1d25be96783356c8ef404ef87` | `185558e4d0e0ca51794126d8289ffb0d54065191d00cc010a2a6b72ff4d0245f` |

## 精確修法與來源界線

- **畫面：**`s57150` 原 `Two shot ... discusses ... with young reporter` 改為只畫**一位年輕記者合上一個素面旅行包**，不畫尚未到場的人手、不演兩人互動，對應[原日記 L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804)的人手請求。`s57110,s57147,s57159,s57168,s57173` 另隨改稿更新成一人一動作提示；`s57189` 收尾卡改「兩份文字／同一場分路」。R7 原生插圖尚未生成或驗收。
- **同章重播：**刪 `s57145,s57146,s57148,s57153` 四景與 claims 列；`s57147` 留一個「還缺哪種援助」問題，`s57149` 只回答**同行人手未齊**，`s57150` 才交代由史丹利從海岸安排，`s57151` 保留日記的非奴隸條件。這讓 2 月補給到手後的敘述不再三次重報「繼續考察／不返家」。開場 `s57010`「兩人為何分路」的 loop payoff 從結句 `s57189` 移到 `s57157`，其前兩句已交代李的預計南／西路線，該句交代史丹利往海岸。
- **第二次勸歸與晚段回看：**`s57110` 改為史丹利出版回憶中的**最好驢代步承諾**，不再重述李的拒絕；見[S12425–12443](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L12425-L12443)，不能當承諾已履行。`s57159–s57160` 明指**先前日記**的友人想法與「不被別人搶先」的本人期望，分別見[L5741–5751](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5751)、[L5769–5778](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5769-L5778)；不冒充 1872 年 2 月新決定、不把地理猜想當定論。
- **封日記與收尾：**`s57168` 用[L5873–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881)補出封印材料與禁開要求，才回收開場五道封印。`s57173` 用[S14360–14394](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L14360-L14394)補史丹利**說會**留下兩位隊員、自己在前站等一天接最後交代，不說已履行。`s57189` 不再重報不返家決定，只回看日記文字後來收錄於 Waller [1874 年編刊本](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L10-L44)，與史丹利出版回憶形成兩個來源層次；不推定原物移交編者的路徑。

**精確集合：**刪四景 `s57145,s57146,s57148,s57153`；改八景口播／claims `s57110,s57147,s57149,s57159,s57160,s57168,s57173,s57189`；改六景 prompt `s57110,s57147,s57150,s57159,s57168,s57173`；改 `s57189` 卡字及 `s57010` loop payoff。`research.md`、相遇精確日 HOLD、S 節錄本與 L 身後編刊本的來源層級、2 月 **18 新援助→19 藥箱→20 藏布**時序均未變。R6 A 單票所指的 12 月信／電報三拍 R7 未刪；其時序承接 R6 獨立 PASS，是否構成岔段留新讀者再判，不能宣稱 A 異議已解。

## 作者檢查與交審

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，163 景，工具估時 **13.80 分鐘**。首章 **00:45**（30–60 秒濃縮開場）；正文 **2,610 漢字**，按每分鐘 325 字約 **8.03 分鐘**。`cute-mystery` 插圖鏡頭 **145／163 = 89.0%**，18 資訊卡，15 條 loops。固定 5 秒片頭及 21 秒片尾／連結槽位規格在企劃，真實可點連結待影片 ID。
- `claims.md` 與 `video.json` **163／163 ID 與台詞逐字對齊**，無重複 ID，script 由 CLI 重生；`npm run test:docs-videos` **236 pass／0 fail**；`npm run check:tasks` exit 0（僅其他既有警示）。
- R7 須由**不同審查者**在本表五檔 SHA 上重核史料／書面畫面，再由兩名全新隔離讀者各自只讀劇本回答 13 題，最後固定 OR 正式 CLI 合併。此作者紀錄沒有給 R7 史料、畫面、敘事或政策自我 PASS。未執行付費語音、插圖、配樂，也未聲稱站主人工核准。
