# S55 R5｜獨立來源與書面畫面覆核

2026-10-20 UTC。**PASS：R5 已修正 R4 的來源歸屬 HOLD，書面分鏡的投料畫面也已標清為機制示意。** 本 PASS 僅涵蓋下列精確版的來源、逐句主張與書面畫面；不代表敘事盲評、站主劇本核准或實際圖片、配音、配樂、影片驗收。我沒有修改作者五檔或生成付費媒體。

## 精確凍結與原文

| 檔案 | 本輪重算 SHA-256 |
| --- | --- |
| `research.md` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` |
| `brief.md` | `e603fdcccf91d884b71cf073005299bcf97dfa8b8cd4a35a44a9b8ea46a28f77` |
| `video.json` | `4964298ad28fd5daeca1b1a71dbdc0a6cccbe4010bfcff053e0b171b1e4270df` |
| `script.md` | `323ed25718b4f20d1fa5dd8fa9311d7afe1810b5418e1615688528510c9fcd21` |
| `claims.md` | `677fa4c37b555c6ea4862678c3ec8296c5e283bcdc626e7a73e91cab86c0af17` |

我再從固定提交的全文網址下載 F／M／E 至 `/tmp/s55-{f,m,e}-independent-r5.txt`。SHA-256 依序為 F `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`、M `2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`、E `5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`，均與固定版相同。F 是 1783 信件的 1907 編刊；M、E 是後出資料，層級仍按 [R4 獨立收據](r4-source-independent.md) 分開。

## R4 阻點逐項重查

1. **`s55032`–`s55033` PASS。** [F 165–173](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L165-L173) 說 Gonesse 落地與破裂消息隔天才傳來，破裂原因是 `It is suppos'd` 的被動推測，未指名猜測者。R5 改成「**信裡記下一種推測**：內部氣體膨脹」及「**這不是已查明的原因**；落地時富蘭克林本人不在那裡」；`claims.md` 同步標未署名。`s55032`–`s55033` 的提示詞把破球放在分隔的回報插圖，富蘭克林只在書房接消息，沒有假裝他在 Gonesse 目擊或親自提出原因。
2. **`s55125`–`s55126` PASS。** [F 334–343](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L334-L343) 說乘員**可以**投稻草續火、再升起並隨風前行，沒有說富蘭克林親見當次自由航程的一次具體投料。R5 把共用提示詞改為 `separate symbolic mechanism illustration`、`generic hot-air balloon rider`、`unmarked landscape`，`claims.md` 也明定這是可行操作的機制示意。它不再把一次具體投料固定到巴黎上空的乘員視角。

為核對修改範圍，我把 R5 的這兩句、`s55125` 提示詞及四列畫面界線暫時反向替換，`video.json` 與 `claims.md` 的 SHA 都回到 R4 凍結值；`script.md` 反向替換兩句與重生的 narrative／speech 尾碼後，也回到 R4 凍結值。`research.md`、`brief.md` 逐位元組維持 R4 SHA。因此 R4 [已通過的其餘來源、日期及畫面界線](r4-source-independent.md#已通過的來源與書面畫面界線)仍適用：十月繫留與十一月 La Muette 試升／自由飛分清，F 編者的 Nov. 22 信／Nov. 21 航行與 E 一致，M 的 Oct. 21 不當另一趟自由飛；`s55144` 的 12 月 Charles／Robert 載人氫氣球只留一句技術對照。

## 對位與工具檢查

`claims.md` **145 列**與 `video.json` 旁白 ID／文字同序同文；ID `s55001`–`s55145` 連續不重複。`script.md` **147 句**（含 2 句片尾）與 JSON 同序同文；**135 個 `shot`**、14 組有序 `loops`、縮圖指定的 `s55002` 均有效。**159 個**逐句連結全部指向固定 F／M／E 提交的現有行，沒有空來源列。`VIDEO_WORKDIR=/tmp/curio-s55-r5-source-independent node tools/video/cli.mjs lint --slug curio-s55 --json` 回 **0 errors、0 warnings**，工具估全稿 **13.888 分鐘**；這不是實際配音時長。`git diff --check`、`npm run check:tasks` 均退出 0；任務檢查仍有其他既存逾期／重疊警告。

本 PASS 解除 R4 的**來源與書面畫面 HOLD**。下一關是讓兩位未看 brief、research、claims 或來源的新讀者，分別對**這份 R5 `script.md` SHA** 盲讀，再按官方 OR 規則合併；實際媒體另待製作後驗收。
