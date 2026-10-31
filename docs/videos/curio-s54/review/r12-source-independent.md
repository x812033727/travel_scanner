# S54 R12｜獨立史料與畫面覆核

2026-10-20 UTC。**史料 HOLD；書面畫面 PASS。** 本輪只核作者凍結稿及其固定史料，未改劇本、主張表、畫面或媒體。兩處口播把史料說得比原文更確定；修正並重新凍結後，須重核受影響句及雜湊。本紀錄不代表敘事盲讀、TTS 或成片放行。

| 凍結檔 | 獨立計算 SHA-256 |
| --- | --- |
| `brief.md` | `0eabd20a735ba729c9b22f4a2c035a29230d07d0a95f134ffdf8050d46dd0f11` |
| `research.md` | `a0456817c7d5a2bf19f5dc940d0dadca456bcbffea908328e90ef16f301cad34` |
| `claims.md` | `f517635d938fe01c161b3bc76cc5b8766a91df9936dba656f734ffb49f7cefc5` |
| `video.json` | `a18316bc5ec45f1512b3268b2c5f95be3771ec4ffffeab77a4927a47dd36a9b2` |
| `script.md` | `b0583005ab8442335e1874c2881a5fc47d8e8d67f1f8db4cbb61bc7531003d3d` |

## HOLD：兩處須收緊口播

1. **`s54031`**：「希爾希望郵局不必再**逐封記下**收款帳目。」希爾的方案寫的是郵局可免收郵資及免做與收款相關的**所有帳目**；回憶亦說希望免除記帳。[H 9612–9614、9638–9642](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9612-L9642)沒有逐封記帳這一具體作業。建議「希爾希望郵局不必再收郵資，也不必再做相關帳目。」並把主張表同步；若保留一句原意，刪去「逐封」即可。
2. **`s54143`**：「五月二十一日日記裡，他仍**見到**完全沒蓋銷的票……」原文說這些案例 *have come within my knowledge*，即希爾**得知**案例，不表示他親眼見票。[H 13425–13435](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13425-L13435) 建議「五月二十一日日記裡，他仍得知有些票完全沒蓋銷，或只留下幾乎看不見的痕跡。」並同步主張表。

`s54094` 把預付人潮和大廳混亂連在一起：1 月 10 日日記引述《環球報》稱預付人群湧入，1 月 11 日日記將混亂明確歸於收款辦法不足；[H 13208–13225](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13208-L13225)足以支持這段概括，但更貼近原文可寫成「希爾隔天記：大廳收郵資的辦法不夠，現場一片混亂。」這是精度建議，非另立 HOLD。

## 已核對的史料與差分

- 從固定 GitHub commit 重新取得希爾、1839 年法案及 Leavitt 原文；本地原文 SHA-256 分別為 `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`、`f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`、`cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`，均與 `research.md` 記錄相同。
- 以 R11 政策覆核請求保存的舊稿逐字比較：R12 收窄 `s54005` 的提問；`s54031` 改寫並刪除重複的 `s54032`；`s54094` 回收開場；片尾刪除 1848 年 Leavitt 支線，以 1840 年 5 月的 `s54142–46` 接續。Leavitt 仍只交叉證實 1 月 10 日及 5 月 6 日日期。[L 4136–4146](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4136-L4146)
- `s54005` 的擁擠提問及 `s54094` 的收款能力不足，有希爾 1 月 10、11 日日記支持。[H 13208–13225](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13208-L13225)
- 片尾黑票、紅色銷記，5 月 21 日的漏銷、魚膠等薄層、向化學師求助及 5 月 29 日 Bokenham 對總局供墨後情況的**暫時判斷**，均可在希爾原文逐項定位。[H 13410–13417](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13410-L13417)、[H 13425–13463](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13425-L13463)。`s54146` 使用「似乎減少」且歸於主管的說法，沒有宣稱問題已消失。Bokenham 的主管身分見 [H 13050](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13050)。

## 對齊、時長與書面畫面

- `video.json` 有 145 個敘事場（138 插圖、7 工具字卡）及一個含 3 句的片尾；`claims.md` 145 個唯一敘事 ID 與場景口播 **145／145 逐字相同**，`script.md` 同樣 **145／145 逐字相同**。主張列有 151 個固定原文連結；上述變動句均指向相應固定來源。這是對齊和定點史料核查，不冒稱逐一重新證實全部 145 句歷史敘述。
- 開場 153 漢字、正文 2,630 漢字；按 325 字／分鐘為 8.09 分鐘。`node tools/video/cli.mjs lint --slug curio-s54 --json` 回報 0 errors／0 warnings、7 章、148 句、工具估長 13.87 分鐘；實際長度仍待 TTS。
- 已審 R12 改動場的書面 `imagePrompt`：`s54005`、`s54031`、`s54094`、`s54142–46` 使用無可讀原件的概念插圖，未指定真郵票肖像或虛構文書；`s54109` 仍呈四月政府規劃場景。`s54144` 的畫面在郵局房內示意塗層，原文未指定地點；出圖時避免讓場景被理解為經證實的犯案地點。**書面畫面 PASS**，實際圖片需另審。

解除本次來源 HOLD 的條件：作者定點修正兩句，重算五檔 SHA-256，另一位工作者核新句與主張表對齊；敘事盲讀與後續媒體關卡仍須按新雜湊進行。
