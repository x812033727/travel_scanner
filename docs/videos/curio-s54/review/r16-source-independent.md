# S54 R16｜獨立史料與書面畫面覆核

2026-10-20 UTC。**兩句 R16 口播的史料 PASS；受影響書面畫面 PASS。** 我未參與 R16 修稿，沒有改五份凍結檔或製作付費媒體。本判定只對下列精確位元組版本、`s54002` 和 `s54013` 及相鄰敘事有效；不是整集重新逐句考證、R16 盲讀／政策、實際生成插圖或新語音音檢的通過證明。

| 凍結檔 | 獨立重算 SHA-256 |
| --- | --- |
| `brief.md` | `e45d0256fba6f068d0bbfc7614edf0444ed88156d850b64aa59f03644f680a0f` |
| `research.md` | `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae` |
| `claims.md` | `0477d725ca08d22589a7287b521d3738db75f2aa5033a5c9e414de8634a4ff1f` |
| `video.json` | `1f030f6c5f58a9d09919f9fb0b6f716e64f14b468c8735ce29987ece2ad6dc02` |
| `script.md` | `538c59b6e861b789a1bbd6ddd4609ee1a47edaac5ea6e98d41bee9ae677e162d` |

五值與 [R16 作者交接](r16-author-oral-repair.md)逐字相同。獨立從固定 Git 提交重新取得 [1839 年法案 A](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt)、[希爾回憶錄 H](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt)和 [Leavitt 1848 年著作 L](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt)。原文 SHA-256 依序為 `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`、`3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`、`cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`，均吻合 `research.md` 固定原文值；以下判讀直接取自原文，不以作者研究表充當第二來源。

| ID／R16 口播 | 原文、上下文和畫面判讀 | 判定 |
| --- | --- | --- |
| `s54002`「寄信的新費率今天正式開始，眼前的櫃台卻連一張郵票都還沒有。」 | 前句 `s54001` 明定想像的日期為 1840-01-10。[H 13061–13083](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13083)說希爾提議先以現金預付，郵票待備妥，並定 1 月 10 日為全國一便士費率日；[H 13139–13147](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13139-L13147)把先行費率與待製郵票分開，[H 13205–13211](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13205-L13211)的 1 月 10 日日記確認已開始。[L 4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144)另分列 1 月 10 日費率與 5 月 6 日郵票。句子沒有把郵票說成 1 月付款方式；[A 9194–9196](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9194-L9196)的 1839 年授權也未被誤當費率生效。畫面提示詞是 January 1840 寄信人在郵局看一個空郵票盤，作沒有郵票的概念插圖；無可讀公文、郵票圖樣或聲稱保存的當日影像。 | **PASS** |
| `s54013`「希爾家也要寄信給外地親戚；他們後來怎麼寄？」 | [H 8761–8773](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L8761-L8773)先舉伯明罕收到倫敦九便士信，再另舉什魯斯伯里親戚；後者的信由伯明罕商人每週包裹代夾，回信由商人在伯明罕投寄。改成「外地」仍是來源許可的較寬地名表達，沒有改成倫敦來信的寄法；`s54014–s54018` 接著講每週包裹，且明說「另一組通信」。`s54013` 畫面只見 1830 年代伯明罕家中一人摺一封**新信**，無地名、可讀文字或錯置倫敦來信的物件。 | **PASS** |

R16 兩句在 `claims.md` 與 `video.json` 各出現一次；逐字反代 R15 舊句後，兩檔各重得 [R15 凍結](r15-author-oral-repair.md) SHA `734af0adfaedcc25ff052c76a3fc1b18e8ad4e7e79f747facfc9df2f9ede46e9`、`37192bb794f6641cc8d181ef92fa7ed9e6ac57e9deba95ddbec696a07128d5f2`。`brief.md` 反代正文 `2,686` 字、`8.26` 分鐘也重得 R15 SHA `c581e4776448e0945906cf215bf605a3711b126759d8ba419352ba1c59bf3102`；`research.md` 與 R15 相同。因此未見超出交接描述的主張或分鏡漂移。其餘未改句承接 [R15 獨立覆核](r15-source-independent.md)，不聲稱本輪重查所有 145 個史實句。

跨檔核對：`video.json` 有 146 景、148 個唯一旁白 ID；145 個歷史正文句與 `claims.md` **145／145** 同 ID 同文，148 個旁白句與 `script.md` **148／148** 同文。`node tools/video/cli.mjs lint --slug curio-s54 --json` 回傳 **0 errors、0 warnings**、7 章、書面估長 **14.115 分鐘**；`npm run test:docs-videos` **236／236 通過**。這些是文字和工具檢查，不是 R16 實際語音長度或品質。R15 音檔及其兩個音檢旗標綁定舊雜湊，不能替代新版完整音檢；後續仍須 R16 盲讀、政策和新語音關卡。
