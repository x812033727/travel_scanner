# S52 R3｜獨立逐句史料與書面畫面覆核：限縮 HOLD

2026-10-20 UTC。另一位工作者不以 [R3 作者凍結](r3-author-freeze.md)當史料證據，重新打開兩份固定原文，對 139 句旁白、主張列及 136 個正文畫面逐一核對。本裁決只涵蓋**文字史料與書面提示詞**；不替代兩位盲讀者、政策、站台、語音、生成圖片或成片驗收。

| 精確 R3 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `8b6165127e6a6d5727d93eae233d135f358e991fbd26227bb82d462df588ab5d` |
| `research.md` | `37f3c0286f214a2848db85674c29b40c09f7b230baf7ce5b5e2442a1ff683edd` |
| `claims.md` | `e8d152f807b62882188fe2c762dc2f3209c3e775b80c1a4e45c4b859157fe37e` |
| `video.json` | `12c77037e76ab6f33674ae873f214330e4adb1b0b80aaf619144574fe3e7aa29` |
| `script.md` | `9253bd1be13e175d7e08ef01f4dc98e023a9210541831e01c6414adaee96a146` |

固定原文在 `/tmp/curio-s52-sources/` 重算 SHA：Cook `cook-8106.txt` 為 `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`；Kippis `kippis-7777.txt` 為 `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`。固定 Git commit URL 見 [research.md](../research.md)。Cook 本是 1893 年 Wharton 編輯轉錄，Kippis 是後出的英國敘述；二者不構成兩次獨立凌日觀測。

## 需要作者修改的三處

| ID | 獨立發現與可行改法 |
| --- | --- |
| `s52019` | 「對派船的人來說，重點是留下**能互相比較**的觀測。」所列 K [L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)說請派船觀測；Wharton 前言 [C L793–803](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L793-L803)說當時欲估日地距離；K [L1133–1149](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1133-L1149)說庫克分兩隊是防大溪地主站失手。這幾段沒有直接把「互相比較」寫成派船者的**重點**。可把旁白收成「對派船的人來說，重點是把金星凌日記錄帶回去」，或另補直接說明方法的固定來源；主張列同步。 |
| `s52028` 畫面 | 提示詞把庫克選的 4 月 15 日海灣東北角沙岸畫成有「**nearby dwellings in the distance**」。Cook 當日 [C L5378–5396](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5378-L5396)一面記居民和首領在場，一面明稱所選沙岸 **not near to any of their Habitations**。K [L1026–1030](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1026-L1030)後稱漁民住在海角，未給出 15 日所選沙岸旁的屋舍位置。保留有人生活的海灣與在場居民，**刪掉「nearby dwellings」**即可，不要改成無人島。 |
| `s52117` 及 `s52116/17` 畫面 | 旁白稱「**表頭只寫格林**」；K [L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)實際在表格**之前**用散文 `According to Mr. Green,` 引出四個時刻，表內是接觸名稱及 h/min/sec，並無格林姓名欄／表頭。可說「基皮斯後來印出四個時刻，表前只註明依格林記錄」，並把「one named column／single observer heading」兩景改為書本旁註或無字單人資料卡，保留它**只有格林一組**的關鍵結論。 |

這些是可定點修的文字／畫面問題；本版因此**旁白史料 HOLD、書面畫面 HOLD**，不能把其餘通過項寫成整集 PASS。`s52135`「島上的人沒有在這兩本書裡自己說話」意在說沒有大溪地人的獨立第一手文本；Kippis [L1026–1030](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1026-L1030)仍轉述歐瓦以手勢傳話。建議作者收成「這兩本英國文本沒有死者或同行大溪地人的獨立證詞」，避免讓觀眾以為完全沒有當地人的言行記錄。`s52076` 的六月二日主觀測處提示詞寫 `April 1769`，若不是明確倒回 15 日的畫面，宜改 `early June 1769` 以免時序混淆；這兩項建議不另作獨立 HOLD。

## 已核過的來源邊界與一致性

- K [L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)支持 1768-02-15 請求與派船；日地距離的說明明歸 Wharton 1893 前言 C L793–803，沒有冒稱庫克當日原話。C 前言 L1069–1073 誤寫 `June 1st`，R3 正文依 Cook [C L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)當日日誌及 K L1151–1165 正確說 **6 月 3 日**。
- C [L5375–5425](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5375-L5425)支持 4 月 15 日首領交換食物、沙岸標界、留守隊帶隊者下令開槍、一名大溪地人死亡，以及庫克和 Banks 不在現場、聽槍後返回；`s52033–48` 沒補死者動機或把庫克畫成現場目擊。`s52046` 用非暴力文字卡，沒有傷害過程。C [L5429–5437](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5429-L5437)支持次日船移近岸與居民帶椰子來。
- C [L5941–5961](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5941-L5961)支持 5 月 30 日教儀器、6 月 1 日 Gore 往 Eimeo、Banks 與部分當地人同行，以及 6 月 2 日 Hicks 往大溪地東面；K L1133–1149 的同行姓名是後出轉錄，`s52073` 卡片已有此標示。沒有把 Eimeo 當今名 Moorea 的未核等值。
- C [L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)同時支持無雲、全程可見、「Atmosphere or Dusky shade」、兩次內接觸最受干擾、三人記時差距超出預期，以及 Solander 倍率較大。`s52099` 卡片用原文，不冒稱已證實金星大氣或單一現代光學成因。K [L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)只列 Green 一人的四時刻，上午 **09:25:42**／**09:44:04** 兩個已念數字正確，未從此算三人秒差。
- C [L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)支持 6 月 4 日傍晚分遣者 `return'd with success`；R3 明說這只是庫克的評語，不能代替各隊精確表，也不斷言全程失敗。金星圖是紙面概念示意，提示詞未叫人裸眼看太陽或發明望遠鏡濾光結構。

`video.json` 共 **137 景**：132 `shot`、4 `big`、1 `outro`；正文插圖占 **132/136 = 97.1%**。139 句 ID 唯一、`claims.md` **139/139** 按 ID／字面／順序相同，`screenplay(doc)` 與 `script.md` 逐位元相同；17 組伏筆 ID 有效。CLI `lint --slug curio-s52 --json` 為 **0 errors、0 warnings**；`git diff --check` 通過。`estimateTimeline` 在 250／300／325 CPM 的濃縮開場為 **42.43／36.60／34.53 秒**，其後至片尾前正文 **627.70／543.00／513.37 秒**（最快 8:33.37）；這些是文字估值，仍需真實 TTS 測長。5 秒品牌片頭、21 秒片尾與可點的 Studio 結束畫面尚未製作／核驗。

**下一關：**作者只改上表必要句、主張及對應提示詞，凍結 R4 五檔 hash；另一人按 R4 精確差分重查來源及書面畫面，兩位新讀者隔離評完整劇本。R3 HOLD 不被作者本地 lint 或別版的題材可行性 PASS 抵消；未放行政策、TTS、插圖或其他付費媒體。
