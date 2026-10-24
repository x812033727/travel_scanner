# S54 R7｜固定來源、逐句主張與書面畫面獨立覆核

2026-10-20 UTC。**史料／逐句主張 PASS；書面畫面 PASS**，只適用於下列精確五檔。這是另一位工作者對 R7 的獨立覆核；R6 [來源覆核](r6-source-independent.md)是前版證據，不能直接作 R7 簽核。敘事盲讀、實際生成圖、TTS、政策和網站關卡另驗。我沒有修改作者五檔，也沒有購買媒體。

| R7 輸入 | 獨立重算 SHA-256 |
| --- | --- |
| `research.md` | `47642150198fa8dcc9a9991a5be9497dfd1f0db4a3085ff3f7d74f7f53126336` |
| `brief.md` | `21f69885d15e85cb2e30a8e7a6407fde7d9e9ead5b6097250a61e8e2f1b8eba6` |
| `claims.md` | `d721b5117622d10d1ce046936d8cd96effe96c94bdbc39b694f4c026aef5b0a8` |
| `video.json` | `049ad513e7e5600a331e71ccdc2bda308a244a971074caffb8df16cbb9b3f87d` |
| `script.md` | `3c8f44af5d1af7a8f5c65e71e8866faa12d32ff0ff09e89f408291b132791684` |

三份固定來源全文亦逐位重算並直接讀取相關行：[A，1839 年法案印本 OCR](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) SHA-256 `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`；[H，希爾回憶錄第一卷](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt) SHA-256 `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`；[L，Leavitt 1848 年倡議書](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt) SHA-256 `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`。H、L 本地 Git HEAD 分別是研究表固定提交 `b508867…`、`df94d1d…`。H 含希爾回顧與日記摘錄，L 是 1848 年近時說明，均未冒稱郵局逐站原帳。

## R7 差分與原文對讀

| R7 位置 | 獨立核對 | 判定 |
| --- | --- | --- |
| `s54009–12` 舊費率收窄 | [H L8761–65](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L8761-L8765) 把伯明罕收到倫敦信的九便士、一件夾帶物升至十八便士、全件可能未滿四分之一盎司放在同一例子。R7 不再口播第二件夾帶物的價格或哈丁頓另例；`s54013–18` 的什魯斯伯里商人代寄仍明示是另一組通信，符合 H L8767–73。 | PASS |
| `s54025–28` 可能不會寫字的寄件人 | [H L9619–32](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9619-L9632) 說帶已寫好的信者有時不能重寫封套地址，於是提議背面帶膠的小紙片；[H L9634–38](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9634-L9638) 將它稱作原本的例外方案。R7 用「可能」並歸於希爾的設想，不把個案當全國統計或唯一發明權。 | PASS |
| `s54042–53` 法案與生效程序 | [A L9192–96、9222、9230–40](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9192-L9240) 是八月十七日法案、財政部按重量定費與日期的權力、提前十日《倫敦憲報》、日後可用預印紙／封套／未用過的貼附郵票。`s54043` 才回收誰決定日期，`s54044` 僅一句公告條件；稿中沒有稱八月當日已按新價收費或郵票已售。 | PASS |
| `s54062→63` 四便士提問／回收 | [H L12990–93](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L12990-L12993) 明言暫行四便士是讓職員先練「按重量」計費，預期郵件增加尚未到來。`s54055–58` 仍把四便士限為其他地區一般單張內陸信**上限**，12 月 5 日實施見 H L12939–50。 | PASS |
| `s54066` 保留 R6 的精確上限 | [H L13049–59](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13049-L13059) 的主管回報是「**not more than one letter in twenty**」上秤。R7 逐句仍說「每二十封信，**最多**只有一封得上秤」，沒有退回確定 1/20 的舊錯誤，並明示這是希爾日記所記主管回報。 | PASS |
| `s54072–84` 12 月至 1 月 | [H L13061–64](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13064) 提郵票待備、先收現金；[H L13132–47、13162–69](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13132-L13169) 記收款提案、預付決定、12 月 28 日命令、窗口時間；[H L13082–83](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13082-L13083) 與 [L L4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144) 分別支持 1 月 10 日一便士費率。R7 沒再重述三種形式；現金預付和貼票准用未混作同日。 | PASS |
| `s54094→95`、`s54098–101` 1 月日記數字與通道 | [H L13213–43](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13213-L13243) 的 1 月 11 日日記先記前晚寄出 112,000、當早鄉間寄入近 80,000；1 月 13 日條目記約 70,000 封寄出，1 月 14 日條目記寄出寄入各約 90,000，並記財政大臣答應請警察主管維持通行。`s54094` 新問寄入數量，沒有重問 `s54082` 已答的收款混亂；所有數量仍歸希爾日記，112,000 沒說成全國逐站總數。`s54101` 的「郵局通道」宜理解為**郵局附近的進出路徑**；原文只寫 *thoroughfares* 暢通，不能推成已知的室內走廊。現有畫面寫郵局外入口附近的無字路線，仍在此界線內。 | PASS，`s54101` 語意留意 |
| `s54103→04`、`s54109` 預付憑證與五月決定 | [H L13139–46](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13139-L13146) 指郵票待印妥；[H L13328–36](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13336) 指 4 月 22 日定 5 月 6 日准用，現金仍可並行。`s54104` 立即回答 `s54103` 的「哪種憑證」；`s54109` 的財政大臣與希爾意見亦有直接出處。 | PASS |
| `s54113–19` 售賣、准用、配發 | [H L13338–59](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13338-L13359) 區分 5 月 1 日先開售、5 月 6 日准用、約 5 月 7 日希爾得知倫敦收件所未配票。`s54115` 的主張列保留 R6 新補的 **P10／H L13354–59** 直接引證；畫面只移動無字封包及無字分發板，沒有預告缺貨。`s54118` 提問時是闔上的無字庫存簿，`s54119` 才畫空架作答案。 | PASS |
| `s54120–34` 漏字、裁切與延誤 | [H L13354–89](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13354-L13389) 支持希爾所說漏掉 *not*、整張封套未裁與缺切紙機器、約一週後郵局說不能分發，以及初發一月後倫敦收件所仍欠供應、兩部門各執一詞。`s54123→24` 的問答立即指出裁單張；`s54130–31` 新句保留希爾未弄清障礙的界線。稿與提示詞均無可讀的原始指示信，也沒有把希爾事後回憶冒充找到原件。 | PASS |
| `s54135–47` 後果與刪除旁枝 | [H L13392–13417](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13392-L13417) 支持附膠郵票較受歡迎、每日逾 50 萬枚仍不足與紅墨銷票疑慮；[L L2395–2415、2433–35](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2395-L2435) 支持**1848 年**在家貼票投寄、封套仍售及收信蓋銷記。R7 不再口播 Leavitt 的回信夾票例；後期用法未倒灌為 1840 年 5 月的首日供應。 | PASS |

## 對齊與畫面關卡

- R7 `video.json` 有七章、147 個正文場景：140 條插圖提示詞、7 張工具排字卡，另有片尾三句，合計 150 句。147 場 ID 不重複，與 `claims.md` 的 147 列 ID／旁白字串**逐列同序同字**；`script.md` 的 148 個場景區塊／150 句亦與 `video.json` 同序同字。23 組 `loops` 的起點與回收 ID 均存在，R7 新問答的相鄰 ID 亦逐一核對。
- 全部 140 條書面插圖提示詞已讀：法案、日記、指示資料及 1848 小冊子只用無字、空白或不可讀道具；票僅是抽象空白標籤，不重建 Penny Black 肖像或可讀真票。`s54115` 分發過場與 `s54118→19` 延後揭示如上表；`s54123→24` 的未裁整張封套和裁切台符合 H L13361–69；後段 1848 畫面明示 1848 年。具體生成圖尚未出現，本 PASS 只管書面提示詞。
- 本次 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json` 退出碼 0，**0 errors／0 warnings**，報 150 句與 13.8806 分鐘書面估計。開頭八場工具估計約 44 秒；排除開頭八場與片尾，139 場正文有 **2,627 漢字**，按 325 字／分為 **8.08 分鐘**。這不是實際語音時長。

**結論：R7 固定來源／逐句主張與書面畫面 PASS。** 若稿、主張、研究、企劃或提示詞再變，須按新 SHA 重核；這份收據不替代敘事雙盲、語音或實際圖像驗收。
