# C07 Dr. Martens｜裁短褲腳更正來源差異覆核 v9

審查日：2026-10-22。審查者：`codex-c07-v9-source-review`。**結論：PASS（僅限本次更正後三檔的來源及逐鏡文字差異）**。v8 的「反摺」歸因 HOLD 已在旁白、逐鏡及來源說明中一併修正；v8 已 PASS 的其他句鏡在本次差異中未改。這不是站主劇本核准、實圖驗收、旁白時長、付費或發布許可。

## 精確版本與差異

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `F13F4327C2A26C08EB64DF89C416A9AB628ACDCC98A17592D0B946C0F2BE07C2` |
| `visual-plan.md` | `6C20B067444DCEF920570771D56F0EB8F0AB763E974D86816D4136BB2AB46DD3` |
| `script-source-notes.md` | `E9DDAD4A6E8BCE656622083A4D91E9E405A90EAED9C8FF279A0E98A8381681C7` |

比較 v8 HOLD 所審稿件 commit `0dd54af9c9`（三檔 SHA 分別 `44C2EB2F…C9B8B3`、`7EDFD94E…7FFCF`、`FDD04EB7…05F484A`）及本次作者更正 commit `44d0b9715de70882b3cb02ae1ac8937389b7f5d2`。更正 commit 對三個待審檔案的內容差異只有 **3 句旁白、4 鏡畫面及一段來源說明**。作者另更新 `script-review-summary.md` 的狀態及哈希；它不新增史實主張。

兩張表各 **77 個唯一 ID，集合與順序一對一**；逐鏡為 **64 `shot`、13 `stats`**，最多連續兩張卡。三個待審檔案搜尋「反摺」均無命中。64/77 是鏡數而非插圖時間占比；正文是否達 480 秒仍待真實 TTS。

## 直接來源及逐列判斷

[A1｜Arthur Crucq，〈Double “Class”. On the Popularization of Dr. Martens〉，《Widok》31（2021）](https://www.pismowidok.org/en/archive/2021/31-visuality-of-social-classes/double-class-on-the-popularization-of-dr.-martens) 本輪 HTML 直接可讀。其第 46–47 行把**六〇年代末**早期 skinhead 的衣著寫為短髮、`jeans with cut-off legs or starched trousers held up by braces`，並說他們腳上穿擦亮的 Dr. Martens；原文沒有 rolled-up／turned-up 褲腳，也沒把每雙靴指定為 1460。[M1｜London Museum 1995 館藏物件及歷史說明](https://www.londonmuseum.org.uk/collections/v/object-91428/boot-ankle-boot/) 將品牌靴被 skinhead 青年採用放在六〇年代末。A1 是研究者的歷史分析，M1 是館方後來的概述；兩者都不是某位青年或一雙特定靴的同期追蹤紀錄。

| 更正位置 | 結果與歸因界線 |
| --- | --- |
| 旁白 `c070102`；逐鏡 `c070102–103` | **PASS**。從 1960 年產品檔案到六〇年代末青年採用的「不到十年」仍是概括時間線；「裁短褲腳」對應 A1 的 cut-off legs。逐鏡只畫匿名青年和不指定型號的無標誌靴，且明說不是工廠下線的同一件實物。相鄰問句 `c070103` 沒把整個群體指認為特定真人。 |
| 旁白及逐鏡 `c070404` | **PASS**。旁白的「把牛仔褲腳裁短」是對 A1 已記載的穿著樣式作日常語氣表述；畫面改成匿名青年**穿著裁短的牛仔褲**，不演出可考人物當場裁褲腳，也不指定靴款。相鄰 `c070409` 仍分別寫裁短和熨挺兩種褲裝，未把兩者拼成同一人的衣著。 |
| 旁白及逐鏡 `c070612` | **PASS**。結尾用郵路、裁短褲腳、格紋時尚款串接已講過的工作／青年／1995 物件節點，是編輯性收束，沒指定單一轉型日或同一雙靴。畫面用郵包、褲腳、格紋的抽象影子，未冒充 1995 館藏原物。 |
| `script-source-notes.md` 的 `c070401–414` 段 | **PASS**。「裁短牛仔褲腳的穿法」與 A1 原文一致；該段仍限定階級符號為研究者分析，沒有推論每位穿靴者的音樂或政治立場。 |

前一版 [v8 收據](script-source-review-v8.md) 對其他改動的逐 ID PASS 及來源限制仍適用，因為本次作者對這些列沒有字面更動；v8 的 HOLD 項由上表覆核閉合。本收據只在上述三個**完整 SHA-256** 均相符時成立。沒有審查實際生成圖、配音、盲讀或站主核准。
