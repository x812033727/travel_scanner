# S63 R4｜作者窄幅修稿紀錄

2026-10-22 UTC。此稿從[正式 R3 雙人盲讀 HOLD](r3-formal-merge-audit.md)出發；只改七個場景 ID 的旁白及其必要插圖／錨點，再更新來源與製作界線文件。R3 原票與 R3 PASS 史料回條保留於原雜湊，不移作 R4 的核准。

## 回應與史料界線

| ID | R3 問題與 R4 改法 | R4 固定依據／畫面 |
| --- | --- | --- |
| `s63008`–`s63009` | 兩位讀者共同指出開場 `s63009` 已揭曉他爬出箱；改為「木箱真能把他送到安全地方嗎？」。`s63008` 也改成假設性的北方法律問題，避免另一句預先說他已在北方演說。 | Brown／Stearns [L1564–1649](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1564-L1649)；`s63008` 畫空講台，沒有提前畫出成功抵達的布朗。 |
| `s63015` | A 指出再說一次十三歲入廠；改成成年後仍在廠與菸葉捲束、壓塊這個新動作。 | 工序 [L1039–1047](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1039-L1047)，後期工作／須請假 [L1454–1456](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1454-L1456)；畫一位成年布朗捲菸葉，不畫少年。 |
| `s63016` | B 單人 No `no_detour`：刪去容量／實際人數／受奴役人數的三連數字，換成自由黑人與受奴役者同廠、布朗無法自行離廠的行動限制。 | 同廠身分 [L1032–1038](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1032-L1038)，請假須求准 [L1454–1456](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1454-L1456)；畫單人望向工廠門。工時仍只在 `s63018` 述一次。 |
| `s63028`–`s63030` | B 指出 `s63029` 重複前句的洗衣收入與養家；改成 `s63028` 只述南希洗衣、布朗剩餘工錢養家，`s63029` 只述另付 72 美元租屋與實際同住，`s63030` 承接原書說的短暫安穩，向一個晴朗早晨提問，不暗示租屋翌日即出事。 | Brown／Stearns [L1245–1262](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1245-L1262)；72 美元不標年租。`s63029` 改畫布朗在租屋門口；`s63030` 不再重畫數錢。 |

## R4 候選與下一關

R4 作者凍結：`video.json` SHA-256 `0f4cb372e473ed68c54de32fffa9449b98e372a920e7e01700927321eba31364`；`script.md` `85af6713b18b42ad1177063cc3dfc5b5665810d70334678114693460dd3161d7`；`claims.md` `5cbcca08555bf337269a4a9b572bb0c3bd5bd28d19662715f93d9ac151861617`。只變更 `s63008`、`s63009`、`s63015`、`s63016`、`s63028`、`s63029`、`s63030` 這七個 ID；仍是 127 句、121 shot、6 卡。開場 167 漢字，按 325 字／分鐘約 31 秒；正文排除訂閱句有 **2,690 漢字，8.28 分鐘**。Episode lint 0 錯誤／0 警告，`git diff --check` 通過。

**R4 尚未通過獨立史料／書面畫面覆核或兩位全新的正式盲讀。**R3 的兩位讀者已看過舊稿，不能用來批 R4。沒有呼叫付費語音、圖片、音樂或影片服務，亦未產生可上架長片、Short 或真實互連 watch URL。
