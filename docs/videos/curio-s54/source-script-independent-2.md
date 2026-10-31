# S54｜第二版逐句史料與書面分鏡獨立覆核

2026-10-20 UTC。**結論：HOLD。** 第二版已修正第一版主要的日期、歸屬與畫面問題，但這組精確雜湊仍有一處一月郵票畫面倒置，以及三處逐句敘述／引證差距。這是 146 句正文、146 列主張及 140 條插圖提示詞的書面覆核；不是作者自評、盲讀、TTS、付費插圖或成片審核。

## 凍結輸入與重新取得的原文

我由 `research.md` 所列三個固定 Git 提交的 `raw.githubusercontent.com` 全文 URL 重新取得原始位元組，逐項重算 SHA-256；沒有把研究表或前版覆核當作第二來源。

| 輸入 | 本次 SHA-256 | 核對 |
| --- | --- | --- |
| `research.md` | `fbdcdd8b091fcbd1b5d8c8cf885debf6da830f04f613973210fe90b05de5dc30` | 符合 `author-freeze-2.md` |
| `brief.md` | `a991fe01f3567d00b65844fc886212d9e7ccea354109516fb8038319c369b132` | 符合 |
| `claims.md` | `f64cc147bf64a07a1acade4ec0f15b58a6f11d4c3c9956a74bd83a67f0e40625` | 符合 |
| `video.json` | `3cfc7a138dd42501b1c506062f705006f8ea0f04a300be8dae696cc8b5ec0745` | 符合 |
| `script.md` | `dd43df11a9436d94f0e6da52ccc243a39dc8c49cc19079bb09d07e57c5684fc3` | 符合 |
| [A：1839 年郵資法案](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) | `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254` | 固定版印本 OCR，有破字 |
| [H：希爾回憶錄第一卷](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt) | `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939` | 1880 年姪子編刊，包含希爾日記轉錄 |
| [L：Leavitt，1848](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt) | `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e` | 近時倡議說明，不是英國郵局原始帳本 |

## 逐句和畫面檢查

`video.json` 有 146 個正文場景（140 `shot`、6 張工具排字卡）、19 組由先到後的 `loops`，另有三句片尾旁白。`script.md` 的 146 句正文與影片 ID、文字、順序完全相符；`claims.md` 的 146 列亦逐列相符；片尾三句與 `script.md` 相符。六張卡的數字、日期及出處逐張核對。所有 140 條插圖提示詞均讀過，並與相鄰旁白及來源時間線對照。

本次執行 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json`：**0 errors、0 warnings**，書面旁白估計 13.9206 分鐘、149 句。排除開場八景與片尾後，正文 2,637 個漢字，以每分鐘 325 字估算 8.11 分鐘。這不是實際 TTS 時長。

第一版列出的主要差距已修好：`s54026` 明說「至少十份」；`s54091` 只說希爾聽到通知信，沒有把通知信寫成預付人潮；`s54114–s54115` 明說部門反對在倫敦、都柏林、愛丁堡三處總局賣票；`s54111` 卡片明說 H 記兩個五月日期，L 只交叉支持 5 月 6 日；`s54145–s54146` 補齊一月與五月的 P07／P09 引證。原 `s54056` 國際信、原一月預印封套／五月日曆、可讀日記數字／公報，以及把 1848 小冊或 1880 回憶錄放在 1840 工作室的畫面均已移除。現在的 `s54142–s54144` 將 1848 年實用情景放在晚期閱讀／1848 年場景。

四個關鍵時點也沒有混寫：[A L9192–9222](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9192-L9222) 是 1839-08-17 授權，不是當日費率；[H L13061–13083](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13083) 與 [H L13139–13169](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13139-L13169) 支持 1840-01-10 先用現金預付的一便士費率；[H L13328–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13347) 區分 5 月 1 日開售與 5 月 6 日准用；[L L4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144) 只交叉支持 1 月 10 日與 5 月 6 日。`s54090–s54103` 的 112,000、未預付約 13,000–14,000、早上入信近 80,000 均歸屬 [H L13213–13243](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13213-L13243) 的日記，沒有變成全國合計或貼票信數。

## 須修訂才可 PASS

| 位置 | 原文對照與差距 | 最小修法 |
| --- | --- | --- |
| `s54014–s54015` 敘述銜接 | [H L8761–8767](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L8761-L8767) 的「不到四分之一盎司」只修飾前面的**倫敦來信及其夾帶物**；H 緊接才另提哈丁頓，再於 [H L8767–8773](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L8767-L8773) 提什魯斯伯里包裹。R2 的 `s54013` 先插入哈丁頓信，`s54014` 隨即說「整封信」不到四分之一盎司，`s54015` 再以這封輕信引向繞路；當下容易把重量誤配到哈丁頓或什魯斯伯里那組。`s54022` 後來區分倫敦與什魯斯伯里，仍未釐清前面重量的指涉。 | 將重量句緊接倫敦兩次夾帶物價格，明說「那封倫敦來信」；轉什魯斯伯里時另起一組，不以重量作其繞路前提。同步改主張表與生成劇本。 |
| `s54042`、`s54141` 主張表引證 | `s54042` 的「能不能使用卻要靠命令」是 [A 第五條 L9230–9240](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9230-L9240) 的法定授權；現列只標 P03／H L9619–9643，該段是希爾的構想。`s54141` 的「法案的不得重用」同樣須標 A／P05；現列只標 P11／H，H 支持銷票困難，但不是法條本身。 | 兩列補 P05／A L9230–9240；保留 H 作希爾方案及銷票問題的證據。 |
| `s54131–s54132` 與 P10 引證範圍 | 現列與 `research.md` P10 均止於 H L13384。`s54131` 後半句「郵票局說已照需求供應」在 [H L13385–13386](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13383-L13389)；`s54132`「難以判斷責任」在 L13386–13389，超出標示範圍。 | 把 P10 與兩列的 H 範圍延至 L13389；維持「希爾說」的歸屬。 |
| `s54109` 插圖 | 提示詞指定 `at a crowded January 1840 letter hall, a sender holds a loose label away from a letter`。一月公眾持有鬆散郵票／標籤的畫面，與 [H L13061–13064](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13064)、[H L13139–13146](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13139-L13146) 的「先現金、票待備妥」及 [H L13328–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13347) 的五月開售／准用次序牴觸。這是前版一月畫面錯置的殘留。 | 把鬆散無字標籤留在早期印製／規劃桌，或改到五月場景；一月窗口只畫現金、素信及空供應格。 |

另有一處非獨立阻斷的畫面提醒：`s54094` 的晚期研究者 `marks a single unlabelled ledger`，而 112,000 的可核來源是希爾日記，不是另一份業務帳本。若要讓插圖的證據層級更清楚，可換成無字日記或普通研究筆記；不要畫可讀數字或看似官方原簿。

修好上述位置後，更新受影響的 `video.json`、`claims.md`、`script.md`（及 P10 的 `research.md`），重新凍結雜湊並覆核。現版 lint 通過不能替修改後的位元組背書。
