# S58 R6｜獨立史料與書面畫面覆核

2026-10-21 UTC。**PASS：以下五檔 R6 的固定來源、口播主張與書面插圖提示詞通過獨立覆核。** 此結論只涵蓋來源和**尚未生成的畫面文字**；不代替 R6 的新雙盲敘事、原生圖片驗收、網站核准、語音／配樂或成片 QA。我沒有撰寫或修改五份創作檔，也沒有購買或生成媒體。

| R6 凍結檔 | 本次 SHA-256 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `f69dace9c1bc7434564da46fbcd74146a453a3bf253781dacfd86bec254f3ccd` |
| `video.json` | `0ece21cb763b15b9ce2d2cc96d363c789c5f1021bd9a52856d17c0119b51b37b` |
| `script.md` | `c1e6e201108663a6c3af9c7c96e56ad07e3fe73b60e4f13f017c8d044aeaec10` |

## 原文與整稿檢查

我再次以具識別字串的 HTTP 請求重取三個固定 Git 提交的**原始位元組**，皆 HTTP 200、SHA-256 與研究檔一致。D 的 SHA 指 Latin-1 原始檔，閱讀時才解碼。

| 固定原文 | 原始位元組 SHA-256 | 使用邊界 |
| --- | --- | --- |
| [D：Dagron 自述](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt) | `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea` | 十一月旅程、薄膜和一月請求；容量、速度與收款為當事人回報。 |
| [R：Reitlinger 乘球親歷](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt) | `ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7` | 十月**另一趟**氣球；手寫紙繫鴿腿，只看見鳥朝巴黎飛。 |
| [C：Coxwell 後寫綜述](https://github.com/GITenberg/My-life-and-balloon-experiences-b-With-a-supplementary-chapter-on-military-ballooning_75423/blob/b3fb84abae06b6f01e345f1205ab70dac041c9f0/75423-0.txt) | `2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b` | 氣球向外、鴿子返城的二手背景；未拿來證 D 的個別數字。 |

`video.json` 現有 **146 景、141 個 `shot`、5 個 `big`**；`claims.md`、`video.json`、衍生 `script.md` **146／146 ID 連號且口播逐字一致**。逐句主張表的 **148 個固定原文連結、21 種不同的直接行號範圍**，其提交、檔名與行號都落在對應原文內。`node tools/video/cli.mjs lint --slug curio-s58 --json` 為 0 error／0 warning。141／146 書面插圖景占 96.6%，`look` 是 `cute-mystery`，20 組 `loops`；縮圖「**五萬則？**」副標明示 `Dagron 自報的容量`，說明欄連三份固定原文。工具估全片約 13.97 分鐘，實際時長要以將來 TTS timeline 驗證。

## R6 改動與證據界線

| 位置 | 獨立核對 |
| --- | --- |
| `s58068–s58071` 酒桶問答與關卡 | 問題是倖存**器材**先藏進什麼載具，`s58069` 立即回答空酒桶；`s58070` 交代前方徵車、折返；`s58071` 說不能把酒桶拿到 Arcis 稅卡，故先留在小村。畫面是單人看桶與器材、散裝器材入空桶、車夫掉頭與在小村留桶，沒有箱中再套箱或桶到稅卡接受檢查。[D231–249](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L231-L249)依次記葡萄酒通行證、器材入空桶、徵車與村中留桶；[D258–260](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L258-L260)才是進城後夜裡重新裝箱。 |
| `s58108` 十八片歸屬 | 現為「達格隆說，薄膜夠輕，**郵務機關最多能**讓一隻鴿子帶十八片」。[D420–424](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L420-L424)的主語是 *l'administration*、上限是 *jusqu'à dix-huit*；R5 誤寫 Dagron 親自操作的阻擋已消失。`research.md` P09 也明列是他自報的最高容量，非每鳥送達量；提示詞是一位郵務員與幾片無字薄膜，未要求生成圖數出十八片。 |
| `s58140–s58143` 一月請求 | `s58140` 只問 Dagron 向巴黎聯絡人**請求**何種寄回方式；`s58141` 回答請搭第一個離城氣球；`s58142` 明說這不是實際載運紀錄；`s58143` 才說 24 日材料抵波爾多。畫面不呈現已實行的氣球回運。[D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)只證一月十八日以鴿郵求助、**請**對方用首個出城球寄送、六天後到貨，沒有指定實際回運載具。 |
| `s58144–s58146` 結尾 | 十二小時明確限於 Dagron 自報的**普瓦捷到巴黎**一段鳥程；`s58146` 只說這沒有量出每封私信何時抵達。R5 原最後一景 `s58147` 已從場景、主張表、劇本全部移除，無孤立 ID 或殘存逐封送達聲稱。[D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)支持此窄界線；六天往返不能改稱十二小時整段行程。 |

先前已修的村長閣樓時段、Tours 現有薄膜樣本、R 腿綁紙與 D 尾綁羽管雙錨、Dagron 自報的郵政匯票收款，以及 `s58097`／`s58101` 單人提示詞仍在本版。其餘提示詞維持無可讀法文／虛構官方原件、兩趟氣球不混畫的 Curio 概念插圖做法；書面 PASS 不預判生成後圖片是否須重畫。

**交接：**R6 可把這份固定史料／書面畫面 PASS 作為下一關的證據；仍需兩位未接觸前稿的讀者只讀 R6 劇本，保留各自原票並正式合併敘事結果。任何修改五份創作檔都會改變本收據的精確 SHA，屆時須重核改動後版本。此收據本身不是語音、插圖、配樂或網站核准。
