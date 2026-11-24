# S58 R2｜獨立史料與書面畫面覆核

2026-10-20 UTC。**HOLD：R2 五檔的來源版本與逐字對齊通過，但逐句引文和書面畫面仍有阻擋點。**本覆核只針對下列固定版本；沒有修改創作檔，也沒有產生或購買語音、插圖、配樂、成片。這不是敘事雙盲、實際成圖、站主核准或媒體放行。

| R2 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `8a1db1dc2a9441a7b16683c70067203ddc7be6c0070560f32c02d91b5e32de34` |
| `brief.md` | `7b44818f6b681a4ee786c00a32359b4181772aeaa1b5cd897bcd13871b1ad016` |
| `claims.md` | `73f9ea7122ec728357b7eb3c8487b9657b4bbe0e6d140c4b0514a7deddc2d471` |
| `video.json` | `d69ce07f441aeabddc231d4d98fe4437ffea4e7c763198d2a61be1161bebe0cb` |
| `script.md` | `9d590c8c3e6f93628d87d4618276ee967364aa36e0b54c7008c9266b6daae0ac` |

## 重開來源與通過項

獨立下載三個固定提交的原始文字，均 HTTP 200、原始位元組 SHA-256 與 `research.md` 一致：

| 來源 | 原始 SHA-256 | 本次直接核到的界線 |
| --- | --- | --- |
| [D：Dagron 自述](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt) | `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea` | 原始 Latin-1 位元組；D84–107 是 11 月 12 日 *Niepce*／*Daguerre* 分裝、D119–177 是交火和落地、D344–436 是 Tours、薄膜、羽管及自報容量。 |
| [R：Reitlinger 親歷](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt) | `ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7` | 書名頁為 1915 年姪子英譯；R514 明載 **10 月 28 日**，R535–573 是郵袋、風向及 Cassier，R778–792 是手寫紙卷綁**腿**、看鳥朝巴黎飛，未證實到達。這是另一趟球。 |
| [C：Coxwell 後寫綜述](https://github.com/GITenberg/My-life-and-balloon-experiences-b-With-a-supplementary-chapter-on-military-ballooning_75423/blob/b3fb84abae06b6f01e345f1205ab70dac041c9f0/75423-0.txt) | `2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b` | C5438–5453 輔助外飛氣球／返城鴿子的方向；C5482–5490 的總數轉引他人，不能替 D 的個別容量作獨立證據。 |

R2 的 P01 修補**通過**：`research.md` 和 `claims.md` 的八處 P01 逐句引文全指 [R510–573](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L510-L573)，其中 R514 確實含日期。D420–436 的十二或十六頁、平均約三千則、最多十八片、逾五萬則／不足一克、片卷入羽管並綁**尾**，都在原文；稿子把逾五萬定位為 Dagron **自報的容量**，沒有當成送達統計。D398–404 的 1 月 18 日至 24 日往返與 Poitiers→巴黎十二小時鳥程也沒有混算；D413–418 的重寄次數沒有倒算成功率。

逐一讀五檔、按 ID 比較後，`video.json`、`claims.md`、`script.md` 的 **156／156** 句及 ID 逐字相同且連號；151 個 `shot`、5 個 `big`。R 的十月腿綁紙與 D 的十一月出城／後續尾綁縮微薄膜，在旁白中分成兩段；D 的 *Daguerre* 下落沒有被說成乘客死亡。這些對齊與正確界線不能代替下列單句的引文核對。

## 阻擋點：逐句引文

1. **s58077–s58080 的直接引文錯段。**四句在 `claims.md` 全指 P06／[D183–249](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L183-L249)，但箱子在普軍攔查時被迫敞開、Dagron 歸因於此的設備損失與雨，見 [D278–295](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L278-L295)；抵法軍防線及法方起初不信、拖慢旅程，見 [D312–330](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L312-L330)。D183–249 最後是空酒桶行程，未含這四句事件。研究錨點與四處 claims 引文須補到正確行，不能把原本 P06 當成已證明全段。
2. **其餘直接引文有跨段缺口。**s58029 的「鴿子綁紙卷」只鏈 P01／R510–573，紙卷在 [R778–781](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L778-L781)；s58036 的風向只鏈 P03／D84–107，應核 [D119–126](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L119-L126)；s58051 的剩餘沙袋和降落判斷只鏈 P04／D119–140，應核 [D142–149](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L142-L149)。這些內容可在同份原文找到，但目前逐句表的直接連結沒有指到它。
3. **s58127 的「抄給收件人」超出所引文字。**P07／[D363–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L363-L370) 只明說在巴黎以電光放大透明片，沒有描述接收、抄寫並交到每位收件人手中。若保留後兩個具體工序，須補直接來源；否則把這句限縮為原文明說的放大閱讀。s58013 的「普通對外通訊難以使用」也非 P01／R510–573 的直接敘述，可補 [C5438–5439](https://github.com/GITenberg/My-life-and-balloon-experiences-b-With-a-supplementary-chapter-on-military-ballooning_75423/blob/b3fb84abae06b6f01e345f1205ab70dac041c9f0/75423-0.txt#L5438-L5439) 並維持二手層級。

## 阻擋點：書面畫面

- `video.json` 的縮微機制關鍵三景不貼口播：s58120 說「把底片捲起來」，prompt 卻是畫家排空白數字卡；s58124 說「羽管最後綁在鴿尾」，prompt 又畫放片入羽管；s58125 說與十月**腿綁紙卷**不同，prompt 才畫**尾綁羽管**。需讓關鍵動作與對應口播同景可辨，並繼續避免把兩趟鳥的載物位置混成同一種做法。這是書面提示詞問題，尚無實際圖片可判。
- 縮圖 `thumbnail.data.headline` 用「**五萬封？**」，但 D420–424 原字是 *dépêches*，R2 口播與主張表均用「**逾五萬則**」且標自報容量；`brief.md` 已否決把「五萬封」當主標的 B 案。即使縮圖副標寫「Dagron 自報的容量」，標題單位與被否決的誤讀仍需修正。

## 檢查與交接

`node tools/video/cli.mjs lint --slug curio-s58`：**0 errors、2 warnings**；警告是「十一月」及「十二」不同事實語境的重複詞提示。`npm run test:docs-videos`：**236 pass／0 fail**。`npm run check:tasks`：**exit 0**，有其他任務的既存持有逾時與範圍提醒。工具門檻不會查出上述史料引文／提示詞錯位。

作者修正以上逐句引文、s58127 與書面畫面後，需重新凍結五檔 SHA，再由非作者對新版本覆核；此 R2 HOLD 不給敘事雙盲或付費媒體放行。
