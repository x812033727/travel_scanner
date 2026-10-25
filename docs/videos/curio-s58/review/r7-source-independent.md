# S58 R7｜獨立史料與書面畫面覆核

2026-10-21 UTC。**PASS：R7 五份凍結檔的固定來源、逐句主張和書面插圖提示詞通過本輪非作者覆核。**這是書面預製作結論；不代替兩位 R7 新讀者的敘事原票及正式合併，也不代表原生圖片、旁白、配樂、成片或網站核准通過。我未修改五份創作檔，未生成或購買媒體。

| R7 凍結檔 | 本次 SHA-256（與 [作者凍結](r7-author-freeze.md) 相同） |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `fbb902e05bede6a4a88b108aae725667b41058c979ff7a69dea339a188c19e87` |
| `video.json` | `ad330abbe8f0919987c01de2c3227e025af8d1d93cc7f2e3557875d5d7b629ec` |
| `script.md` | `d32bea9d5cc33125cf9b41f1288a8faf78765d96dcd3ed2002abe4ad97f20957` |

## 原文和全稿對照

以三個固定 Git 提交的 raw URL 重取原始位元組；D、R、C 都是 HTTP 200，SHA-256 分別與 `research.md` 的 `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea`、`ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7`、`2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b` 一致。D 只為閱讀解成 Latin-1；雜湊針對原始位元組。D 是 Dagron 當事人自述，R 是 Reitlinger **十月另一球**的乘客回憶，C 是 Coxwell 後寫的二手背景；C 不替 D 的容量、成功率或速度作獨立證明。來源提交、檔名和限定用法仍見 [`research.md`](../research.md)。

`video.json` 有 **146 景、141 個 `shot`、5 個 `big`**，141 個書面 shot 提示詞齊全；`claims.md`、`video.json` 和衍生 `script.md` 的 **146／146 ID 從 `s58001` 至 `s58146` 連號、口播逐字一致**。逐句表有 **148 個固定原文連結、21 個不同直接行號範圍**；所有提交、檔名、行號語法和原文檔案長度對上。R6 已覆核的其他主張界線在 R7 仍保持：十月腿綁手寫紙與十一月尾綁羽管分開、Tours 已有薄膜樣本、十八片是 Dagron 所說郵務機關可放的上限、一月球運只是一項請求、十二小時只是一段鳥程。

## R6 → R7 三句及其畫面

| 位置 | 獨立核對 |
| --- | --- |
| `s58068` | 問「剩下的器材能先藏進什麼東西運離村子？」；`s58067` 已交代葡萄酒通行證，`s58069` 立刻答空酒桶。提示詞是車夫看桶與箱，下一張畫散裝器材放入桶；`s58070–s58072` 才按先折返、稅卡前留桶、進城後夜裡重裝箱的順序走。[D231–249](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L231-L249)、[D258–260](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L258-L260) 支持這個次序；沒有把整箱塞入桶或讓桶過 Arcis 稅卡。 |
| `s58124` | 「這隻鳥從省外飛回被圍的巴黎」須按本章的**代表性返城鳥**理解：前景的尾綁羽管據 [D433–436](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L433-L436)，巴黎放大所收薄膜據 [D363–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L363-L370)；Dagron 還自報有薄膜很快抵達、一次鳥從普瓦捷飛返巴黎 [D398–417](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L417)。這幾段**沒有**識別窗邊這隻鳥，也沒有說普瓦捷那鳥必帶羽管或任一私信已交到收件人；巴黎窗台提示詞只是概念插圖，沒有畫拆信或簽收。不能以 R 十月腿綁紙那隻鳥補這項證據。 |
| `s58125` | 問「城裡要怎樣讀出這卷薄膜上的訊息？」接 `s58126` 的電燈光放大，與 [D363–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L363-L370) 對上；提示詞是單人將無字小片舉到放大燈下。此處問讀取方法，沒有再把 `s58087` 的裸眼難讀當作新答案，也沒有要求生成可讀原件。 |

整份書面畫面仍依 `cute-mystery`，**141／146（96.6%）** 為原創概念插圖，卡片僅 5 張；未在提示詞要求可讀法文、假官方文件或把兩趟氣球畫成同一趟。這只審核提示詞和旁白是否矛盾，生成後的圖仍須按系列規則驗收。`node tools/video/cli.mjs lint --slug curio-s58 --json` 實跑為 **0 error／0 warning**，工具估時 **13.90 分鐘**；實際正文與成片時長仍待 TTS timeline。

**交接：**本收據可作 R7 固定來源和書面畫面的 PASS。兩位只讀 R7 劇本的新盲讀者須各留原票，然後正式合併敘事 13 題；五份創作檔任何一字改動都使上述 SHA 範圍失效。此收據不啟動付費媒體或站主核准。
