# S54 R13｜獨立史料與書面畫面覆核

2026-10-20 UTC。**史料 HOLD（僅 `s54135` 的備貨者主語）；書面畫面 PASS。** 本輪在作者 R13 凍結後，重新下載固定版本的一手法案與希爾回憶錄、Leavitt 近時記述，核對 R12 指出的錯誤、R13 五月供應結尾、145 句逐字對齊及書面畫面。未改企劃、主張、口播、提示詞或媒體；不代表盲讀、實際出圖或 TTS 放行。

| R13 凍結檔 | 獨立計算 SHA-256 |
| --- | --- |
| `brief.md` | `5024ad2639127676c4f0a04a0b57e22bdfafae85023badfbd56d927e3c48e9af` |
| `research.md` | `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae` |
| `claims.md` | `0addcc9b709e39665ef90cd875b2db6b870ec8ac04168614a54a5acf8acb076a` |
| `video.json` | `6c1e8d68127dbdda74c1ea58a3b38fbe20251e64c1bad11e5a61608e31b3f71d` |
| `script.md` | `446cbbe27fcc8560b325fd77a0487fc4b5ab68ceae7bd185734796e4b3fd13c2` |

## 唯一 HOLD：`s54135` 多了一位備貨者

口播、主張表及 `video.json` 同寫：「希爾先前備下的大批封套」。[固定 Hill H 13390–13399](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13390-L13399) 只說 *the great stock of covers which had been prepared*，沒有指明是希爾備貨。較早的 [H 13270–13290](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13270-L13290) 說他督促整體執行，也未將這批庫存歸於他本人。建議三處同步改為「另一頭的印刷廠也被需求逼緊：先前備下的大批封套，居然派不上多少用場。」保留印量與需求的對比即可。這是新增的主語歸屬，不應由作者凍結紀錄自行宣告史料通過。修稿須重新凍結五檔並做定點獨立覆核。

## R12 問題與 R13 五月段落

- `s54031` 現寫希爾希望郵局免去**收郵資及相關帳目**；[H 9612–9614、9638–9642](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9612-L9642) 正是「collection of the revenue」及「all accounts relating to that collection」，已無 R12 無據的「逐封」。`s54094` 現僅說希爾隔天記收款辦法不足、現場混亂；[H 13221–13225](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13221-L13225) 直接支持，沒有再替兩個記載補一條因果。
- 對照 [R12 來源 HOLD](r12-source-independent.md) 與 [R13 作者差分](r13-author-fix.md)：R12 `s54141–46` 的 5 月 21／29 日銷記與防重用支線已撤出；因此原 `s54143` 把希爾「得知」說成「親眼見到」的錯誤不在現稿。R13 `s54130–34` 接封套裁切與分發，`s54135–39` 接附膠郵票偏好與每日逾五十萬枚仍不足，`s54140–46` 最後才問發售約一個月後的倫敦收件所供應和兩部門爭執。這與 [H 13353–13400](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13353-L13400) 相容；「Meanwhile」的產量記述可放在約一個月後的結局之前，但沒有拿印量推各站到貨數。`s54141–42` 的「約一個月」自 5 月 1 日首次發售起算；書面畫面用 1840 年六月初，沒有把費率日、售票日與准用日混為一天。
- `s54143–46` 分別歸屬郵局的「取不到」、郵票局的「已應付甚至超過要求」、兩邊不易問話、希爾難以判責；[H 13383–13389](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13383-L13389) 支持，沒有創造當場目擊或確定是哪一部門失責。`s54133–34` 問與答也符合希爾說不願找忙碌的財政大臣出面。
- 重新取得 [1839 年法案固定版](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240)；序言與第一、五條分別寫一便士改革方向、財政部後續命令權及三種可授權的預付形式。法案沒有說 1839-08-17 就全國收一便士或開賣郵票。Hill 的 1 月 10 日費率與 5 月 1 日發售、5 月 6 日准用，及 [Leavitt 1848 的日期交叉記述](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4136-L4146)，仍與稿子主線相符。

三份固定全文重新下載的 SHA-256：Hill `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`、法案 `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`、Leavitt `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`；皆與 `research.md` 相同。R12 完整檔案未保留成可做逐位元組差分的快照，以上「差分」只限 R12 審核紀錄與 R13 作者凍結紀錄可逐項比對的敘事主張。

## 對齊、開場、時長與畫面

- `video.json` 有 145 個唯一敘事 ID；`claims.md` 145 列與 `script.md` 145 句各與場景口播 **145／145 逐字一致**，缺列、重複及不一致均為零。這是逐字對齊；本輪逐條重讀的是 R13 受影響的主張，並不把 145 列對齊冒稱 145 個歷史斷言全數重新查證。138 個插圖景、7 個工具字卡、24 組 loop；`cute-mystery` 及配樂設定均保留。
- 第一章 `s54001–08` 濃縮開場 153 個漢字；排除這八句和片尾的正文 2,645 漢字，按最快每分鐘 325 字為 **8 分 08.31 秒**。這是書面保守估計，實際片長待 TTS。重跑 `node tools/video/cli.mjs lint --slug curio-s54 --json`：**0 errors／0 warnings**、7 章、148 句、工具估 13.927 分鐘。
- 逐讀 `s54031`、`s54094`、`s54109` 與 `s54120–46` 的書面 `data.prompt`：一人一動作的年代概念插圖、空架和無字資料夾；沒有可讀的原指示信、法案、真 Penny Black 版面或把希爾畫成 1 月 10 日大廳目擊者。`s54109` 仍在四月規劃室；結尾畫面從五月印刷／分配到六月初空收件所，與旁白順序相符。**書面畫面 PASS；實際生成圖須另審。**

解除本次來源 HOLD 的定點條件：改 `s54135` 的三處文字、重算五檔 SHA，另一位工作者核新句及書面畫面。R13 尚須兩位乾淨盲讀者重新判 13 題；在新凍結與關卡通過前，不得把舊六句 TTS 快取當成此版旁白。
