# S58 R4｜獨立史料與書面畫面覆核

2026-10-21 UTC。**HOLD：R3 指定的史實／引文修正、逐句對齊與絕大部分書面畫面已通過；三個小範圍仍須修正，再凍結新雜湊覆核。** 本頁只查下面的 R4 作者候選版。我沒有撰寫或改動五份創作檔，沒有生成或購買媒體，也沒有代替網站核准、敘事盲讀或原生圖片驗收。

| 凍結檔 | SHA-256（本次重算） |
| --- | --- |
| `research.md` | `0adab42902bd00393a4b7c945a4b37a9eae4f61e79cbbd2710085713f8643132` |
| `brief.md` | `8d0d42c6c5cf1de97ee8b497db3d298540b9fc21e1fe3bcee024b749c8960e08` |
| `claims.md` | `f0e340870fa7389224932ca732950fb990b4bdebcf4baaabf2d93fa3d994edc1` |
| `video.json` | `78960f72a00a5fcc245896d680bc18f9481cef6c472dd9fc94d82ad80ae7e547` |
| `script.md` | `b9451d33643dccd8ffc84f4a6f93074f4500adb50855f7a5529d9620eeaa8d0c` |

## 原文與逐句核對

我重新以有識別字串的 HTTP 請求讀取固定 Git 提交的**原始位元組**，三份均 HTTP 200，原始 SHA-256 與研究檔所載一致。D 是 Latin-1；讀取時才解碼，不拿轉碼後文字計算原始 SHA。

| 固定原文 | 原始位元組 SHA-256 | 這次核對的邊界 |
| --- | --- | --- |
| [D：Dagron 自述](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt) | `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea` | 11 月球、器材與旅程；圖爾既有薄膜樣本；郵務量、匯票與一月化學材料事件均是 Dagron 自報。 |
| [R：Reitlinger 乘球親歷](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt) | `ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7` | [R514](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L514-L514)為 10 月 28 日另一球；[R759–792](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L759-L792)是一張手寫紙綁腿，作者只看見鳥朝巴黎飛。 |
| [C：Coxwell 後寫綜述](https://github.com/GITenberg/My-life-and-balloon-experiences-b-With-a-supplementary-chapter-on-military-ballooning_75423/blob/b3fb84abae06b6f01e345f1205ab70dac041c9f0/75423-0.txt) | `2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b` | 僅為氣球向外、鴿子返城的背景；稿中沒有拿它核實 D 的容量或送達量。 |

`video.json` 有 **147 景、142 張 `shot`、5 張 `big`**；`claims.md`、`video.json`、`script.md` 的 **147／147 ID 與口播逐字相同**。逐句主張表的 149 個固定原文 URL，落在 21 種不同的直接行號範圍；每個提交、檔名和行號均在對應的三份固定檔內，沒有漂移連結。`node tools/video/cli.mjs lint --slug curio-s58 --json` 回 0 error、0 warning；其 13.93 分鐘是工具預估，仍須日後以實際音檔核時。142／147 插圖景超過系列七成下限，`look` 是 `cute-mystery`，20 組 `loops` 已配置。縮圖以「**五萬則？**」並寫 `Dagron 自報的容量`，沒有把 *dépêches* 當五萬封已送達。說明欄列 D／R／C 固定全文與頻道連結，十月和十一月兩球分述。

## R3 退件修正與新增因果節拍

| R3 指定處 | 本版結果與原文 |
| --- | --- |
| 原 `s58067` 村長閣樓的「夜裡」 | 現為 `s58063`「一位村長同意把他們藏進閣樓」，中性日光；[D183–192](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L183-L192)未給藏匿時段，已不外加夜景。 |
| 原 `s58070`／`s58072` 箱入桶、進城前重裝 | 現 `s58069` 明說**倖存器材**入空酒桶且提示詞畫散裝機件；`s58072` 明說**進城後夜裡**重裝箱。對得上[D231–260](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L231-L260)。中間新增持葡萄酒通行證的車夫、徵車折返，交代為何換路。`s58071` 畫面另有下述阻擋。 |
| 原 `s58080` 抵圖爾時樣本仍未做成 | 現 `s58080`／`s58086` 明確拿出**既有薄膜樣本**，其後才採用薄膜製作郵務電文；符合[D355–379](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L355-L379)。 |
| `s58123`／`s58124` 腿與尾、製作與載送混合主張 | 兩句都補足雙錨：`s58123` 指[R759–792](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L759-L792)和[D433–436](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L433-L436)；`s58124` 指[D344–379](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L344-L379)和[D433–436](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L433-L436)。提示詞只畫本段尾部羽管。 |
| 原 `s58146` 無全城逐封收件清單 | 現 `s58146`／`s58147` 只說 Dagron 的一月例子沒有量出或逐封證明**私信**何時送到；[D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)足以支持這個證據限制。 |
| 原 `s58097`／`s58101` 雙人互動畫面 | 現兩個提示詞分別是一位檢查員看片盤、一位檢查員放無字電文束；沒有雙人交接。 |

新增的 `s58136`／`s58137` 分開交代縮拍郵政匯票、巴黎收款人拿到錢，且兩句都明示 Dagron 自報；[D416–418](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L416-L418)確有這項聲稱。這不是獨立的收款紀錄。數字段也把十八片／逾五萬則／不到一克稱為他的最高容量報告，沒有轉寫成所有私信的送達量；重寄六、平均二十、少數三十五至三十八次均維持他的自報而未倒算成功率。

## 阻擋：兩個來源畫面界線、一個插圖動作

| 位置 | R4 內容 | 固定原文界線與窄修方向 |
| --- | --- | --- |
| `s58071` 的提示詞，連同口播「酒桶過不了檢查」 | `one cart driver stops closed wine barrels before a city tax barrier` 會畫成酒桶已推到城市稅卡前接受檢查。 | [D246–249](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L246-L249)說**無法把桶拿去稅卡**，便先留在一個小村，然後進 Arcis。口播可限為「因不能帶酒桶過稅卡，先留在村裡」，提示詞畫在小村留下桶，不把桶擺在關卡。 |
| `s58141` 提示詞及 `s58142` 口播 | 前者畫 `one balloon pilot loads a plain wrapped chemical parcel into a wicker basket`；後者斷言「材料再由氣球向外」。 | [D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)明說一月十八日**請**巴黎聯絡人搭第一個出城球寄材料、二十四日材料已到波爾多；沒有在這段確認實際出城載具。`s58141` 的口播用「請」已準確；畫面宜改為一人準備無字請求或從請求的角度示意。`s58142` 應寫成「他請對方由氣球向外寄材料」等歸屬明確的表述，保留已證實的六天到貨和十二小時鳥程。 |
| `s58089` 提示詞 | `one workshop assistant removes fibrous paper sheets from a camera table and sets down clear film` 要求一張定格圖同時表達取走紙、放下薄膜兩個動作。 | Curio `image-01` 書面規則是一人一個可辨動作。可只畫一人把透明薄膜放在攝影桌上，舊紙作靜態背景。此處是可愛概念插圖，原文[D362–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L362-L370)支持紙製電文停用、改採薄膜。 |

其餘書面提示詞保持兩趟球、手寫紙綁腿與縮微羽管綁尾的區別；用無字紙張、無字通行證與概念器材，未要求可讀法文或自造官方原件。必要的鳥／球空景有明確敘事用途。原生圖片仍須按系列九題品質評審及和旁白是否矛盾驗收，這份收據沒有替圖片判 KEEP。

## 交接

作者只需窄修 `s58071`、`s58089`、`s58141`／`s58142` 的口播或提示詞與相應主張列，再凍結五檔新 SHA，由未撰寫該版的人重核這些變動和 147 句對齊。**這版尚不能作史料／書面畫面 PASS，也不應憑 lint 0/0 進入語音、插圖、配樂或網站審核關卡。**
