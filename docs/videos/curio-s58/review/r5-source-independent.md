# S58 R5｜獨立史料與書面畫面覆核

2026-10-21 UTC。**HOLD：R4 的三組來源／書面畫面退件已窄修；R5 新改寫的 `s58108` 把原文中的郵務機關動作歸到 Dagron 本人。** 本頁僅查下列五檔凍結 R5。未改創作檔、未購買或產生媒體，也未代替雙盲敘事、原生圖片或網站核准。

| 凍結檔 | 本次 SHA-256 |
| --- | --- |
| `research.md` | `1f6adc58345a10655a0bfdf66c87d5337cbd87c8271f41cb4878204bf4e5d5d0` |
| `brief.md` | `fbffce22c2eff5052a4050b06b121e3fc8a62b7ab350ecfd6a150f5788214362` |
| `claims.md` | `67ed990038429d6186487e1f16504ebf3e982d2b8d7c591c75b7c58faf8cceef` |
| `video.json` | `1be17b85b1b41cb1f5e0f9fe21d18c758ef096447cb4c776c5dcba1ba79dda22` |
| `script.md` | `ce03aeae00241c3e178897ea35a4469c697abaddbb268061fd0574eed0dc35e0` |

## 固定原文和整稿對齊

重新從三個固定 Git 提交的 raw URL 取得原始位元組，皆 HTTP 200，與 `research.md` 指定 SHA 相符：

| 原文 | 原始 SHA-256 | 本集用途 |
| --- | --- | --- |
| [D：Dagron](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt) | `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea` | 11 月球、器材、薄膜與自報容量；原始 Latin-1 位元組計 SHA。 |
| [R：Reitlinger](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt) | `ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7` | 10 月另一球；一張手寫紙繫鴿腿，不能與 D 的羽管綁尾混用。 |
| [C：Coxwell](https://github.com/GITenberg/My-life-and-balloon-experiences-b-With-a-supplementary-chapter-on-military-ballooning_75423/blob/b3fb84abae06b6f01e345f1205ab70dac041c9f0/75423-0.txt) | `2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b` | 後寫背景；不當成 D 容量的獨立行政記錄。 |

`video.json` 有 **147 景、142 個 `shot`、5 個 `big`**；`claims.md`、`video.json` 與 `script.md` 的 **147／147 ID 連號且口播逐字相同**。149 個逐句來源 URL 涵蓋 21 種直接行號範圍，提交 SHA、檔名和行號都對應這三份固定原文。`lint --slug curio-s58 --json` 為 0 error、0 warning；工具估全片 14.015 分鐘，真正時長仍需 TTS timeline。142／147 插圖景為 96.6%，`look` 是 `cute-mystery`，20 組 `loops`。縮圖「**五萬則？**」的副標仍明寫 `Dagron 自報的容量`，說明欄連 D／R／C 固定全文與頻道，不宣稱五萬封已送達。

## R4 退件和 R5 改寫段落

| 檢查處 | R5 結果 |
| --- | --- |
| `s58071` 酒桶位置 | 口播改為「酒桶不能拿到阿爾西城的稅卡前，他們只好先留在附近小村」；提示詞只畫一位車夫在小村留下酒桶。符合[D246–249](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L246-L249)的「無法向稅卡出示，先留在小村，再進 Arcis」時序。 |
| `s58089` 單人單動作 | 只畫一位工人把透明薄膜放在攝影桌上，舊紙靜置背景；符合 Curio `image-01` 一人一動作，與[D362–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L362-L370)停用紙製電文、改採透明薄膜一致。 |
| `s58140–s58142` 一月材料 | 現說 Dagron 以鴿郵求助、**請**巴黎兩位聯絡人搭首個離城氣球寄材料；`s58142` 明確提醒這不是實際載運紀錄。`s58141` 不再畫氣球載運，而畫一位攝影師在波爾多桌前封無字請求。符合[D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)的請求、24 日到貨及另外一段十二小時鳥程；沒有冒稱實際出城載具。 |
| `s58055–s58056`、`s58079–s58080` 章節銜接 | 倖存器材如何避搜查由村民借衣物回答；抵 Tours 日期只說一次，再接既有薄膜樣本及當地紙張工作。分別符合[D166–177](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L166-L177)、[D344–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L344-L370)。 |
| `s58107–s58114` 容量新序列 | 每片十二或十六頁、平均約三千則、單鳥至多十八片／逾五萬則／不到一克，分段保留 Dagron 自報與「容量非送達量」的限制；來源為[D420–424](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L420-L424)。但新寫的 `s58108` 主語有下述阻擋。 |

其餘 R3 已修界線持續保留：村長閣樓無虛構夜晚、器材散裝入桶且進城後夜裡重箱、抵 Tours 已有薄膜樣本、R 腿綁紙與 D 尾綁羽管雙錨、沒有虛構全城逐封收件清單、`s58097`／`s58101` 無雙人互動。`s58136–s58137` 的郵政匯票收款只按[D416–418](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L416-L418)標為 Dagron 自報。書面圖維持無可讀法文、無精確假地圖，兩趟球和兩種綁法沒有混畫；原生圖片尚未生成，不能在此判 KEEP。

## 唯一阻擋：`s58108` 的操作者歸屬

R5 口播與主張表同寫：「**達格隆說，他曾讓同一隻鴿子一次帶走十八片；每片又有多少內容？**」第二個「他」把實際放片、派鳥的動作歸到 Dagron。固定原文[D420–424](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L420-L424)的主語卻是「*La légèreté de ces pellicules a permis à l'administration d'en mettre sur un seul pigeon jusqu'à dix-huit exemplaires*」：薄膜的輕度讓**郵務機關**在一隻鴿子身上放**最多**十八片。原段不能證 Dagron 本人裝片或派鳥；也要保持這是他報告的上限，而非固定每次十八片。

窄修建議：`s58108` 改為「**達格隆說，薄膜夠輕，郵務機關一隻鴿子最多能帶十八片；每片又有多少內容？**」或其他保留「Dagron 回報／郵務機關／最多」的自然句；同步改 `claims.md` 與衍生 `script.md`，如需也使 `research.md` 的 P09 主語更清楚。`s58108` 的提示詞是單一郵務員擺放多片無字薄膜，沒有把 Dagron 畫成實際操作者，可保留。修後重新凍結五檔 SHA、核對 147 句對齊，交給未改稿的人覆核。**R5 不能因 lint 0/0 視為來源／書面畫面 PASS，亦不可越過後續雙盲與媒體審核。**
