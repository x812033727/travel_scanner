# S54｜第三版逐句史料與書面畫面獨立覆核

2026-10-20 UTC。**結論：HOLD。** 第三版修好了第二版的四項主要差距，但這組精確雜湊仍有三處會使五月配發畫面與希爾原文牴觸，以及兩列逐句引證不足。這是書面史料與分鏡審核；不是作者自評、盲讀、TTS、已生成插圖或成片審核。

## 凍結輸入與獨立重開原文

我直接從下列固定 Git 提交的 `raw.githubusercontent.com` URL 重新取得三份原始全文，重算其原始位元組 SHA-256；沒有把作者研究表或前版覆核當成第二來源。工作區五份輸入也與 `author-freeze-3.md` 逐一相符。

| 輸入 | 本次 SHA-256 |
| --- | --- |
| `research.md` | `fa0af44ff0c35ab422f89150813d2201514eede3a6df56ed5f96df671d3e03f4` |
| `brief.md` | `a991fe01f3567d00b65844fc886212d9e7ccea354109516fb8038319c369b132` |
| `claims.md` | `2cb1cc200b911054cd11d7ab20b68899fc88a8c57fe3dab32c603706170789a7` |
| `video.json` | `4fe7c0bd30a8347dddc6d28e06370e969e2d5049529470d83bb496cd41a488a5` |
| `script.md` | `cef9c47c8a7bc980b327e4753041821a7e35ac2b9fe1ec17581f70441ea40b2d` |
| [A：1839 年法案固定印本 OCR](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) | `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254` |
| [H：希爾回憶錄第一卷固定全文](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt) | `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939` |
| [L：Leavitt 1848 年固定全文](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt) | `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e` |

逐一讀過 `video.json` 的 146 個正文場景，其中 140 條 `shot` 插圖提示詞、6 張工具排字卡；`claims.md` 的 146 列 ID、旁白文字和順序均與 `video.json`、`script.md` 逐列相符，另有三句一致的片尾旁白。19 組 `loops` 均存在。六張卡的日期、價格、數字和出處也核對了原文。重新執行 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json` 得 **0 errors、0 warnings**，工具估計 149 句、13.9128 分鐘；這不是 TTS 實測。

## 史料與已修好的第二版問題

- [A L9192–9222](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9192-L9222) 的 1839-08-17 是授權財政部日後以命令調整費率，並非該日一便士費率或郵票生效；[A 第五條 L9230–9240](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9230-L9240) 容許命令採用預印紙、封套、貼附郵票，且規定郵票不得曾用過。第三版 `s54042`、`s54141` 已補 A／P05；沒有把法案說成即時發售通知。
- [H L13061–13083](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13083)、[H L13139–13169](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13139-L13169) 把 1840-01-10 費率與先用現金預付、郵票待備妥分開；[L L4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144) 交叉記 1 月 10 日費率和 5 月 6 日郵票。`s54109` 的一月提示詞現只畫素信與空供應格，沒有前版誤置的一月鬆散郵票。
- [H L8761–8773](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L8761-L8773) 的不到四分之一盎司只屬倫敦來信及夾帶物；第三版 `s54013–s54017` 已把倫敦、哈丁頓、什魯斯伯里分開。[H L13383–13389](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13383-L13389) 的兩部門說法與希爾無法判責也已納入 P10 和相應主張列。`s54094` 改成無字日記與空白地圖，沒有再暗示另一份官方帳本。
- [H L13213–13243](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13213-L13243) 的 112,000 封、未預付約 13,000–14,000 封、早上從鄉間收到近 80,000 封均被歸屬希爾日記，沒有說成全國合計、倫敦已確定的地點或貼票信件。[H L13328–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13347) 分清 5 月 1 日開售和 5 月 6 日准用；`s54111` 卡片特別註明 L 只交叉支持 5 月 6 日。

## 需修才可 PASS

| 位置 | 原文對照與差距 | 最小修法 |
| --- | --- | --- |
| `s54118` 插圖與主張列 | 提示詞把 5 月 7 日倫敦收件所的存貨抽屜寫成 `half-empty stock drawer`，容易畫出已有部分郵票；[H L13354–13359](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13354-L13359) 卻說**沒有任何倫敦收件所領到郵票**。本列旁白的「希爾隔天聽見配發消息」也只引 P09／H 13328–13353，恰好停在消息前一行。 | 畫空存貨抽屜／空架；主張列補 P10／H 13354–13359。 |
| `s54125` 插圖 | 提示詞寫 `inside a London receiving house ... a postal worker holds an uncut sheet at a counter`。[H L13361–13369](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13361-L13369) 說郵票局想交整張，**郵局拒絕把未裁封套發給收件所**。畫面卻把未裁整張放進收件所。 | 把整張紙留在印製／部門交接處；收件所只畫等待供應的職員或空格。 |
| `s54130` 插圖 | 提示詞把「首次發售一個月後」的倫敦收件所固定在 `May 1840`，還寫 `sparse supply shelf`。[H L13345–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13345-L13347) 首次發售是 5 月 1 日；[H L13383–13389](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13383-L13389) 說一個月後倫敦收件所仍 `unsupplied`。五月定位和有少量存貨的架子都可能倒置這段話。 | 改為「首次發售約一個月後」或六月初，不指定五月；畫空供應架。 |
| `s54141` 主張列 | 「收信時蓋清楚銷記」的**時點**可由 [L L2433–2435](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2433-L2435) 的 `office where they are received` 直接支持；目前只列 H／P11 的銷票困難與 A／P05 的不得重用條件，兩段都沒有明寫「收信時」。 | 給本列補 L 2433–2435，並將研究表 P12 範圍延至該處；或拿掉特定時點，只說郵局蓋銷記。 |

這些是書面提示詞與逐句引證問題，不能靠生成後的可愛畫風判定消除。其餘提示詞為示意性匿名寄件人、職員與無字物件，未見要求模型重建可讀法案、希爾日記、真實 Penny Black 肖像或 1840 年已出版的 1848 小冊子。修訂後應更新受影響的 `video.json`、`claims.md`、`script.md`／`research.md`（依所選修法），重新凍結五份雜湊，再做另一次獨立覆核；本次 HOLD 只對上表第三版位元組成立。
