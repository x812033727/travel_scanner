# S54 R5｜獨立逐句史料與書面畫面覆核

2026-10-20 UTC。**結論：HOLD。** 第五版的日期主線、原始來源邊界和絕大多數書面畫面可成立，但一個新增的精確比例把原文的上限改成定值；五月分發過場也失去直接引證，畫面與相鄰問答需要同步修正。本判定只管史料、引證和書面畫面，不是敘事盲讀、實際語音或成片審核。未修改五份作者輸入，也未開始付費媒體。

## 精確凍結與核對

獨立重算五份輸入 SHA-256，均與 [作者第五版凍結](../author-freeze-5.md) 相同；讀取第四版的[獨立史料覆核](../source-script-independent-4.md)，並由固定 Git 提交的 raw 全文重新取得 A、H、L 三份來源、重算來源 SHA-256、直接讀相關原文行。來源 H 是希爾事後回憶及其中的日記轉錄，L 是 1848 年 Leavitt 的說明，沒有把兩者說成官方逐站帳簿。

| 輸入 | SHA-256 |
| --- | --- |
| `research.md` | `57f24b58a1d407825f71fcd389576ae0ae77e6a547d87b5e1ca8be17863557fa` |
| `brief.md` | `3cb12adb860bdd914001eb53ac2417fd512164eb45da47eca8ad76477148c2ba` |
| `claims.md` | `7ff218d43ecc56514dac1339e3813ff1467d5f7a28040660c71ccd7f4e61cd8f` |
| `video.json` | `b0987d49dd7c625d252b3635d28b81a734d3ab8b7040ccbc42b482d02f88f38c` |
| `script.md` | `db4e32986f5e75282988566e25b8ffa0cece5d28cce82c2cb851eacf5c505337` |
| [A：1839 年法案固定 OCR](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) | `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254` |
| [H：希爾回憶錄第一卷固定全文](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt) | `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939` |
| [L：Leavitt 1848 年固定全文](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt) | `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e` |

正文 148 場、141 條插圖提示詞、7 張工具排字卡，另有三句片尾旁白。148 場的 ID、旁白文字、順序與 148 列 `claims.md` 逐項相符；重產的 `script.md` 與現有逐句稿相符。22 組 `loops` 的端點都存在。155 個主張引證連至上述固定提交及明確原文行。再次執行 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json`：**0 errors、0 warnings**，151 句，工具估計 14.0133 分鐘；這仍非 TTS 實測。前八場工具估計約 44 秒；除去開頭和片尾，正文即使按每分鐘 325 字估算亦超過 8 分鐘。

## 第五版改動及相鄰畫面

| 位置 | 獨立原文與書面畫面核對 | 判定 |
| --- | --- | --- |
| `s54006`–`s54008` 開場 | 只預告指示信漏一字，沒有提前講倫敦收件所缺票。1840 年一月的空托盤、普通封信和窗台是概念場景，不假畫可讀指示信；後文 `s54122`–`s54124` 把漏掉的 *not* 歸屬希爾後來的回憶，並說原件未核到。[H L13354–13359](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13354-L13359)。 | PASS |
| `s54023`–`s54025`，`s54068`–`s54069` | Wallace 反對按郵局實走繞路收費，見 [H L9304–9315](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9304-L9315)。四便士過渡是讓職員先練習按重量計費，預期的大量郵件尚未到，見 [H L12990–12993](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L12990-L12993)。畫面只有無字路線板、秤和安靜大廳；沒有把旁枝例子說成普遍費率。 | PASS |
| `s54070`–`s54073` 新增主管回報 | 希爾轉錄的 12 月 13 日日記說 Bokenham「**do not put more than one letter in twenty into the scale**」，不是確定每二十封正好一封。[H L13049–13059](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13049-L13059)。`s54071`「每二十封信，只有一封得上秤」把**最多一封**變成精確定值；`s54072` 的未增員和 `s54073` 的另一主管增兩人則符合原文。秤和無字人員表畫面沒有額外數據。 | **HOLD：把 `s54071` 改為「每二十封信，最多只有一封得上秤」一類的上限語句，並同步三份逐句文字。** |
| `s54076`–`s54086` 現金先行及命令 | [H L13061–13083](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13083) 提先收現金待郵票；[H L13132–13169](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13132-L13169) 記收款提案、財政部預付決定、12 月 28 日《憲報》及倫敦與鄉間的截止時間安排。`s54088` 的 1 月 10 日才是全國一便士生效日，與 [H L13082–13083](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13082-L13083) 和 [L L4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144) 一致。三處日期和硬幣／空郵票托盤的相鄰畫面不混淆付款方式。 | PASS |
| `s54111`–`s54117` 五月售票與反對者 | [H L13328–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13347) 記 4 月 22 日財政部定 5 月 6 日准用、Baring 想只收郵票而希爾主張現金並行、**部門**反對在倫敦／都柏林／愛丁堡三總局出售，以及 5 月 1 日先開售、當天郵票局銷售 £2,500。`s54114` 即答 `s54113`「誰反對」，沒有虛構具名官員。`s54116` 日期卡寫「1840・5・1 開售」，和 `s54119` 的「1840・5・6 准用」分開，普通空白標籤與托盤不冒充 Penny Black 原件。 | PASS |
| `s54118`–`s54124` 分發 | `s54118`「收件所能否拿到票，還得看分發」的主張列只引 [P09／H L13328–13353](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13353)，沒有引到直接交代倫敦收件所未獲配票的 [P10／H L13354–13359](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13354-L13359)；第四版獨立覆核曾在相同過場補過這項直接引證。`s54118` 的「後來檔案裡研究員合上回憶錄」畫面沒有呈現分發。`s54120` 問准用隔天聽到什麼消息，畫面卻先打開**空庫存抽屜**，早於 `s54121` 旁白揭曉。`s54121`–`s54124` 內容本身符合希爾原文，未顯示可讀的真實指示信。 | **HOLD：`s54118` 補 P10 直接引證，改用不預告結果的分發／運送概念畫面；`s54120` 用中性的待查庫存畫面，將空抽屜留待 `s54121`。** |
| `s54125`–`s54148` 後段與 1848 回信票 | `s54125` 的整張未裁封套仍在印製處；`s54132` 明示 **early June 1840** 收件所未獲供應，分別符合 [H L13361–13369](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13361-L13369)、[H L13383–13389](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13383-L13389)。`s54141`–`s54143` 的銷票畫面無可讀真郵票圖樣，收件所蓋銷記的時點有 [L L2433–2435](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2433-L2435) 直接證據。`s54144`–`s54147` 明示八年後／1848 年場景，回信夾票用法見 [L L2424–2425](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2424-L2425)，未倒灌為 1840 年 5 月首日的供貨事實。 | PASS |

修正上述兩處後，應重產逐句稿、重新凍結五份輸入並對新雜湊再做本關覆核。此 HOLD 不代表第五版正式敘事盲讀結果。
