# S54 R13｜史料精度與五月供應主線的作者凍結

2026-10-20 UTC。[R12 獨立史料覆核](r12-source-independent.md)因 `s54031` 的「逐封記帳」與 `s54143` 的「見到」而 **HOLD**；[無背景讀者 A](r12-clean-blind-a.md)因尾端先到發售後一個月、再退回 5 月 21／29 日，且銷記防重用支線離開印製與配發主題，對 `one_line`、`no_detour` 投 **No**。本紀錄只凍結作者 R13 修稿，不冒稱獨立史料、畫面或敘事 PASS。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `5024ad2639127676c4f0a04a0b57e22bdfafae85023badfbd56d927e3c48e9af` |
| `research.md` | `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae` |
| `claims.md` | `0addcc9b709e39665ef90cd875b2db6b870ec8ac04168614a54a5acf8acb076a` |
| `video.json` | `6c1e8d68127dbdda74c1ea58a3b38fbe20251e64c1bad11e5a61608e31b3f71d` |
| `script.md` | `446cbbe27fcc8560b325fd77a0487fc4b5ab68ceae7bd185734796e4b3fd13c2` |

## 差分與史料界線

- `s54031` 改成「希爾希望郵局免去收郵資，以及與收款有關的帳目」，不再聲稱逐封記帳；主張表改指 [希爾方案 H 9612–9643](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9612-L9643)。`s54094` 按覆核精度建議去掉「預付人潮讓」的因果表述，僅說希爾隔天記收款辦法不足、現場混亂；來源是 [H 13221–13225](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13221-L13225)。
- `s54130–46` 重排為同一條供應線：裁封套後仍有分發問題；一週後郵局稱無力分發，希爾追問、未找忙碌的財政大臣出面而繼續催促；公眾更要附膠郵票，日產五十多萬枚仍趕不上；**最後**才到發售約一個月後倫敦收件所仍未獲供應、兩部門各執一詞。此序以 [H 13353–13400](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13353-L13400)為界；「印出」不等於已經配到倫敦收件所，不能由五十萬產量推各站收貨數。
- R12 `s54141–46` 的銷記、防重用口播與其畫面全部撤出，故 `s54143` 的「希爾親眼見到」錯誤主張不再存在。新 `s54141–46` 只處理倫敦供應與當事人無法判責的結尾。`s54133` 新增「是否請財政大臣出面」提問、`s54134` 回答；舊 `s54136` 的提問由 `s54137` 回收，`s54141` 的供貨問題由 `s54142` 回收。相關 loop 和主張表已同步。R11 留下的 `s54109` 四月政府規劃室畫面保持原修正。
- 書面畫面改為收件所空架、印刷廠、希爾的概念研究室等單人動作；印量、部門主張均不畫成可讀官方帳冊、真 Penny Black 肖像或已核原件。這只是作者畫面提示，生成圖仍須獨立檢查。說明欄保留固定的法案、希爾、Leavitt 日期交叉證據與頻道連結；沒有捏造影片 ID 或可點的片尾網址。

`video.json` 有 145 個敘事場（138 插圖、7 工具字卡）及 3 句 outro；`claims.md`、`script.md` 與場景口播各 **145／145 逐字對齊**，24 組 loop。開場 153 漢字，正文 2,645 漢字，以最快每分鐘 325 字計為 **8 分 08.31 秒**；`lint --slug curio-s54 --json` 為 **0 errors／0 warnings**、7 章、148 句，工具總估 **13.93 分鐘**。這不是 TTS 實測；`git diff --check` 通過。

下一關由不同工作者直接重開固定史料並核 R13 受影響口播、主張表和書面畫面；兩位完全無先前對話背景的讀者需重做 13 題敘事。R12 的獨立判定不自動沿用。S54 舊稿 TTS 只留下六句草稿快取；`/workspace/.video-work/curio-s54/STOP` 保留，新稿通過之前不得繼續語音、圖片或成片。
