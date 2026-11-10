# S57 R2｜獨立史料與書面畫面差分覆核

2026-10-20 UTC。**史料與書面畫面 PASS，限下列精確 R2 五檔。** 我未參與 R2 作者修稿，也沒有改創作檔、呼叫付費語音、產圖或判定實際插圖。R1 的[全 189 句來源／畫面審查](r1-source-independent.md)是 HOLD；本次將 R2 與該凍結版逐欄比對，重新開啟兩份固定全文，獨立核對所有變更及原先阻擋點。敘事盲讀、政策、音訊與成片另有關卡。

| 凍結檔 | 本次重算 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `911eb30d15273aa3ab5a57795e28e5a9c3fb4a8fa60059f3f152dc3eb578765a` |
| `claims.md` | `5f03685898d9b256e9d3eaf0d7534efe3eaf4b9393f3ad86e418787ad1bb27f9` |
| `video.json` | `53ee5cd8a93ff5474ffbccbde47379c9872303a4d09442a1f1d699fb8d25b4ff` |
| `script.md` | `604a4f10dbd6ac5b8c7602939a40f58252307a82810bd70d6c2d8b2a63fd29da` |

## 固定史料與版本層級

我重新下載 [S：史丹利的節錄出版敘述](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt) 與 [L：Waller 身後編刊《最後日記》第二卷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt)。兩個固定 GitHub 引用頁均回 HTTP 200；raw 全文 SHA-256 分別為 S `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`、L `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`，與 R1 相同。`claims.md` 的 **218 次、43 個不同固定行號引用**均仍落在對應來源的全文行數內，所有來源連結與 R1 逐列相同。S 書名頁註明 *Abridged*；L 是身後編刊本，不等於已校驗的親筆日記全本。

## 三句口播阻擋點已解除

| ID | R2 獨立判讀 | 結論 |
| --- | --- | --- |
| `s57050` | 現句「身後編刊日記寫到相遇，這段卻沒那句原話」只說**出版段落**未載名句；[L5252–77](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5277) 寫到相遇而未刊那句，[S9530–45](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9530-L9545) 印出史丹利一方的問候。排版卡也改成「身後編刊日記／相遇段未載名句」，沒有反推親筆手稿內容。 | PASS |
| `s57077` | 現句說日記記下女兒艾格妮絲的**話**，與 [L5741–51](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5751) 的 `My daughter Agnes says` 相符；不再指稱特定來信。`s57077–s57079` 三景移除信封／家書道具，只用人物與空白工作筆記示意。 | PASS |
| `s57116` | [L5474–76](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5474-L5476) 記元旦 `storm-stayed`；現句只說「風暴」。最終 prompt 為湖畔營地、深色陰天和人固定貨包，**已移除 `heavy rain` 及 `rainy inland route`**，未把風暴種類定成暴雨。 | PASS |

## 鏡頭位置與片尾時序

- `s57028`、`s57030–s57032` 四景從湖邊改到 **Paris Grand Hotel assignment room**。史丹利出版敘述 [S62–94](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L62-L94) 明寫在巴黎 Grand Hotel 見 Bennett；空白筆記與不可讀地圖只是卡通示意，沒有定出當時未知的李文斯頓位置。`s57029` 的人名卡未改。**PASS。**
- `s57100–s57102` 的港口明寫烏吉吉／湖東岸，`s57104–s57110` 是烏吉吉湖畔村落，`s57111–s57112` 是離村東行路。這符合 [L5414–28](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5414-L5428) 的 12 月 13 日回村、15 日備往東走；[L478–80](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L478-L480) 的「東岸」是編者地理說明。北岸探察景止於 `s57099`，`s57103` 卡片不需改。**PASS。**
- `s57188–s57189` 從死亡卡後的活人道路鏡頭改成兩張回顧排版卡，分別寫「1874 年編刊／蘇西與楚馬追述」及「日記帶走了／他選擇留下」。[L9976–85](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L9976-L9985) 分開本人日記末頁與兩人追述；後一張明示本集對 1872 年選擇的回顧，沒有在 1873 年去世後仍畫他行動。**PASS。**

## 版本差分與下一關

R1→R2 只有 **23 個場景 ID** 改動：`s57028`、`s57030–s57032`、`s57050`、`s57077–s57079`、`s57100–s57102`、`s57104–s57112`、`s57116`、`s57188–s57189`。只有上述 **3 句**改口播；`claims.md` 只改相同 23 列的口播或畫面界線，**來源連結零改動**；其餘 166 景與 `video.json` 非場景欄位逐值相同。R2 有 189 個唯一 ID，`claims.md` **189／189** 與 JSON 逐字相同，`script.md` **189／189** 與 JSON 逐字相同。`lint --slug curio-s57 --json` 為 **0 errors、0 warnings**；168／189 景仍為系列 `shot` 插圖（88.9%），21 張 `big` 卡承擔日期、來源或片尾回顧。

R1 審查提到 `s57005`、`s57073`、`s57083` 可能混景，三者原文未改，仍是**非阻擋的生成前提示詞清晰度建議**；生成圖片須另看原圖。`claims.md` 導言仍沿用「R1 作者候選稿」字樣，是非阻擋的版本標籤精度問題；若更改，須重綁本報的 claims SHA。兩份來源對**相遇精確日期**仍不一致，本片沒有說出任一精確日，本 PASS 不解決日期校勘。請依本五檔新版另交兩位無前情讀者盲讀與正式合併，再做政策關卡；在那以前不進付費語音、插圖或配樂。
