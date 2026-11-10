# S58 R3｜獨立史料與書面畫面覆核

2026-10-21 UTC。**HOLD：三份固定原文、版本、逐句對齊和 R2 的主要引文修正通過；R3 仍有時序／現有樣本的說法、跨來源引文及雙人互動畫面阻擋。** 本頁只查固定 R3；我未撰寫 R3、未改五份創作檔、未產生或購買語音／插圖／配樂，也沒有代替網站審核、雙盲敘事或原生圖片驗收。

| 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `27bebfb771aa8a901cf69528fb23401d351dcc35bdf584ab5e70c2163bfa0ea7` |
| `brief.md` | `49a1bd7cf68e2db074cc128bd08f60739da9ce85f63aa1ba4f7abab9f044e0d4` |
| `claims.md` | `73dcedbcbf30d5abd2db92fd34b789718e61938e8b4a86fe528d109851d332ec` |
| `video.json` | `7283ea2a7e444e2e58e83bb52a40da9548a1dddc1c2d74740971100f33936c48` |
| `script.md` | `6fd7c0585ebb1a47f518d70d769a1094deb54dc90404362df0ce0ed821ef1816` |

## 原文與通過項

用有識別字串的 HTTP 請求重新下載固定 Git 提交的**原始位元組**，而非沿用作者轉錄；三份皆 HTTP 200 且 SHA-256 與 `research.md` 一致：

| 原文 | 原始位元組 SHA-256 | 本次重核 |
| --- | --- | --- |
| [D：Dagron 自述](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt) | `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea` | 原始 Latin-1；[D84–107](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L84-L107)是 **11 月 12 日**兩球與任務；[D119–177](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L119-L177)是射擊、沙袋與落地；[D344–436](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L344-L436)是圖爾紙／薄膜、工作與作者自報的容量、羽管綁尾。 |
| [R：Reitlinger 親歷](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt) | `ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7` | [R510–573](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L510-L573)在 L514 明載 **10 月 28 日**；[R759–792](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L759-L792)是一張手寫紙綁**腿**、只看鳥朝巴黎飛。這是與 D 分開的一趟氣球，且為 1915 年後刊英譯。 |
| [C：Coxwell 後寫綜述](https://github.com/GITenberg/My-life-and-balloon-experiences-b-With-a-supplementary-chapter-on-military-ballooning_75423/blob/b3fb84abae06b6f01e345f1205ab70dac041c9f0/75423-0.txt) | `2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b` | 後寫二手背景，沒有拿它當 Dagron 個別容量的獨立行政證據。 |

`video.json` 有 146 句／141 個 `shot`／5 個 `big`；`claims.md`、分鏡與 `script.md` 的 **146／146 ID 和口播文字一致**，每句都有固定原文連結。20 種實際使用的直接行號範圍皆在對應來源檔內。`lint --slug curio-s58 --json` 為 0 error、0 warning。R2 所指出的 s58077–s58078 交叉段落已改指 [D312–330](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L312-L330)；s58074–s58075 箱子敞開已指 [D289–295](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L289-L295)；s58127 已不再虛構逐戶交件。縮圖已改「**五萬則？**」，副標歸於 Dagron 自報；[D420–424](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L420-L424)確實為 *dépêches* 而非「五萬封已送達」。[D406–418](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L406-L418)的中午到傍晚十副本、十三組、重寄六／約二十／三十五至三十八次，以及 [D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)的一月十八日至二十四日六天整段與十二小時單段鳥程，都被稿子分開並標自報。

## 阻擋：來源與時序

| 句 | 目前稿與畫面 | 固定原文界線；窄修方向 |
| --- | --- | --- |
| `s58067` | 「**夜裡**，一位村長把他們藏進閣樓」；prompt 也設 `soft lamp light`。 | [D183–192](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L183-L192)記村長藏匿，未說夜裡；團隊之後才在[另一地於晚十點抵達](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L190-L201)。刪時段詞、把光線改為中性，不把村長閣樓誤標成後一站夜景。 |
| `s58070`、`s58072` | 先說「把**箱子**裝進空酒桶」，再說「**進城前**……又把設備重新裝箱」。 | [D231–249](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L231-L249)只說**倖存器材**放入空桶；空桶因進城稅卡留在村中，團隊進入 Arcis。[D251–260](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L251-L260)才記**進城後的夜裡**重新裝箱。把 `s58070` 的箱子改為器材、`s58072` 的「進城前」改為「進城後的夜裡」；提示詞不得畫已裝箱的整箱進桶。 |
| `s58080` | 「人到了，薄薄一張能裝大量字的東西，**還沒做成**」。 | Dagron 在 Tours 已拿出其**現有薄膜樣本**，當地負責人才採用該工藝，見[D362–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L362-L370)。原句易讓人以為連樣本都沒有；若要說尚未成批供郵務寄送，須明確限於**量產郵件薄膜**。 |
| `s58123` | 句中同時對比十月紙卷**綁腿**與十一月羽管**綁尾**，主張表只連 P02／R759–792。 | R 能證前半句；後半句須加 [P09／D433–436](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L433-L436)。這與 R2 所修的跨段引文屬同一逐句直引標準。 |
| `s58146` | 「他手裡有了藥品，卻**沒有全城每封私信的收件清單**」。 | [P10／D388–418](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L388-L418)沒有提供逐封收件清單，但不能證 Dagron 當時手裡或別處不存在該清單。宜限縮為「**這份回報**沒有逐封列出私信收件紀錄」，並可引 D 對全篇的結尾。 |

`s58124` 的「薄膜從省外飛回巴黎」目前只連 P07／D344–379 的圖爾薄膜與巴黎放大；建議補 P09／D433–436 的羽管載送來完整覆蓋動線。這是同一修訂可補的引用精度問題；本頁不另宣稱已證明每一片實際送達。

## 阻擋：書面畫面

Curio 的 `image-01` 固定做法是**一人一個可辨動作**，只畫概念插圖，不用無出處的可讀文書或雙人互動代替主動作。R3 的 `s58120` 彎薄膜、`s58122` 綁尾、`s58125` 以燈放大已對準各自口播；但兩個仍在同版的 prompt 不符單人規則：

- `s58097`：`one postal inspector watches a photographer work at a bench`，明確要求檢查員與攝影師兩人同框。可改為一位攝影師調整工作桌設備，畫源自 [D372–379](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L372-L379)的省器材流程，不需可讀信。
- `s58101`：`one postal inspector hands a plain bundle to a workshop assistant`，要求兩人交接。可只畫一位檢查員把素面電文束放上桌；[D406–410](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L406-L410)支持中午送來、公務電文當晚十副本，不要求在單張圖顯示交接的兩張臉。

另外，`s58067` 的燈光與 `s58070`「箱中有箱」提示須跟上面史料窄修；`s58077` 雖以道路上的遠車示意抵防線，正式生成仍應檢查是否看得出主動作。兩趟氣球與腿綁紙／尾綁羽管並未在其他提示詞混為一談；目前無原生圖片可判 KEEP。

## 交接

R3 作者宜只修上述句子、逐句連結及對應 prompt，保留十月二十八日 Reitlinger → 十一月十二日 Dagron → 十一月二十一日 Tours → 一月材料往返的骨架；正文目前按最快估速只約 **8.10 分鐘**，刪句需補來源支持的新動作，不能用重述湊時。修後五檔另凍結 SHA，由未撰寫新稿者重新查史料與書面畫面，並讓兩位新的隔離讀者重作敘事盲讀。此版 **不得**憑 lint 0/0 進入政策、語音、插圖或配樂關卡。
