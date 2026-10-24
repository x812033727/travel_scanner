# S54｜一便士郵資題材獨立史料覆核 1

2026-10-20 UTC。**結論：HOLD，限四處文字修正。**三份固定來源可重開，版本與 SHA-256 全部相符；「先有一便士費率，後有郵票可用」的七章、約十分鐘 A 案有足夠史料與可畫場景。下列 P01、P02、P08、P09 的現稿表述須修正後才可當逐句劇本的來源表。本報告沒有改動作者的 [research.md](research.md)、[brief.md](brief.md) 或任務票，也不核准劇本與媒體製作。

## 獨立重開與固定版本

覆核者另建 `/tmp/s54-review-*` 快照，法案從 GitHub Git blob `433e7fa217b90a06f21b491788fb4b08b0ecd487` 取原始位元組，兩本書重新下載固定 Git 提交。以原始全文 `sha256sum` 重算，未正規化換行；以下行號皆為固定純文字的實際行號。

| 來源 | 固定提交或 blob | 本次原始全文 SHA-256 | 結果 |
| --- | --- | --- | --- |
| A：[1839 年 *2 & 3 Vict. c. 52* OCR](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) | Git blob `433e7fa217b90a06f21b491788fb4b08b0ecd487`，表列提交 `eb9f01613383da6020f6a10b8c600dc92bcb5361` | `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254` | 符合 |
| H：[希爾／George Birkbeck Hill，1880 年第一卷](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt) | `b508867f1e1390093789dd72b1d84bcd6bbdaa58` | `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939` | 符合 |
| L：[Joshua Leavitt，1848 年 *Cheap Postage*](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt) | `df94d1d290d2b99b1af422c3595438dea38fbdd8` | `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e` | 符合 |

## 主張逐項覆核

| ID | 判定與原文錨點 |
| --- | --- |
| P01 | **修正措辭。**[H L8761–8773](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L8761-L8773) 支持伯明罕收到倫敦信最低九便士，*slightest enclosure* 使費率升至十八便士；未指明夾的是「一頁」。商人代寄是下一個、與**什魯斯伯里親戚**往來的例子，不能接寫成那封倫敦信的送法。 |
| P02 | **更正人名。**[H L9288–9302](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9288-L9302) 的 Wallace 較早推動改革；同書轉錄的 [1850 年活動標題 H L17773–17784](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L17773-L17784) 明寫 **Robert Wallace**，現稿的 `Walter Wallace` 錯誤。希爾不是唯一改革者的界線正確。 |
| P03 | **通過。**[H L9619–9643](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9619-L9643)、[L13392–13400](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13392-L13400) 支持希爾原預期附膠郵票只作特例、後來需求較高；限於他方案與回憶，不推唯一發明權。 |
| P04–P05 | **通過。**[A L9188–9222](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9222) 是 1839-08-17 授權財政部以命令改費率、按重量計費，命令預先刊登；[A L9226–9240](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9226-L9240) 涉免資權、預印紙／封套／貼附郵票。立法當天不是實際一便士費率或郵票開賣日。 |
| P06 | **通過。**[H L12939–12950](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L12939-L12950)、[L12990–13006](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L12990-L13006) 支持 1839-12-05 過渡：倫敦部分預付信一便士、其他一般單張內陸信四便士**上限**，不是全國每封都四便士。 |
| P07 | **通過。**[H L13061–13083](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13083)、[L13138–13169](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13138-L13169)、[L13205–13209](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13205-L13209) 支持先用現金預付、1839-12-28 命令與 1840-01-10 費率生效；[Leavitt L4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144) 另列 1 月 10 日費率和 5 月 6 日郵票。 |
| P08 | **修正地點與證據性質。**[H L13213–13232](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13213-L13232) 是 1 月 10 日日記先猜當夜不少於十萬封；1 月 11 日日記記前夜寄出 112,000 封，其中 13,000–14,000 未預付，郵局大廳擁擠。原文未在此數字旁明寫「倫敦」，雖由郵局與「從外地收到」的脈絡可推測。不得把 `倫敦一夜` 當作原文直述，更不能擴為全國量或獨立業務報表。 |
| P09 | **修正日期語法。**[H L13328–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13347) 記 4 月 22 日決定 5 月 6 日開始可用郵票預付，郵票於**5 月 1 日**開售；`先於 5 月 1 日開售` 易讀作「5 月 1 日以前開售」，應改成 `5 月 1 日先開售` 或 `較早的 5 月 1 日開售`。[Leavitt L4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144) 只交叉支持 5 月 6 日郵票日期，沒有 5 月 1 日開售細節。 |
| P10–P11 | **通過，保留歸屬。**[H L13353–13384](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13353-L13384) 是希爾對漏字、配發、裁切的事後說法，並非已找到指示信原件；[H L13392–13431](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13392-L13431) 支持他所記每日逾五十萬枚仍不足及紅墨銷票問題。 |
| P12 | **通過，限 1848 年場景。**[Leavitt L2372–2422](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2372-L2422) 說明可預先購買附膠郵票、在家貼好投寄，也記預印封套／紙張；不能倒推 1840 年 5 月首日各地庫存。 |

## HOLD 的精確修正

1. `research.md` P01 的「夾一頁」改為「稍有夾帶物」；P01 及 `brief.md` 第 2 章若提商人，明說這是希爾家與**什魯斯伯里親戚**通信的另一例，不是前述倫敦來信。依據 H L8761–8773。
2. `research.md` P02 把 `Walter Wallace` 改成 **Robert Wallace**，並加入 H L17773–17784 的人名錨點。原 P02 行號只稱 Mr. Wallace，不能支持 Walter 這個名字。
3. `research.md` P08、`brief.md` 第 5 章與任務票 Notes 把 `倫敦一夜` 及 `倫敦該夜` 改成「希爾 1 月 11 日日記記前夜其所述郵局寄出 112,000 封」等不指定地點的措辭；保留「單夜、日記記載、非全國量」的限制。若確需明稱倫敦，另加可重開且明寫地點與這筆數字對應的固定史料。
4. `research.md` P09 的 `郵票先於 5 月 1 日開售` 改成「郵票 5 月 1 日先開售，5 月 6 日才可用於預付」。`brief.md` 已正確分開兩日，毋須修改其日期。

## 題材與畫面可行性

[A 案](brief.md) 的七段依序有九便士舊制、1839 年法律授權、12 月四便士過渡、1 月現金窗口、5 月開售與准用、之後的郵票便利性；每段都能用固定來源解開上一段疑問。預估 8–15 分鐘可信，但尚無逐句劇本及真實語速，不能宣稱時長已驗收。`30–60` 秒濃縮開場、既定 5 秒片頭、21 秒片尾與最後 16 秒連結框位已在企劃；可點連結仍待實際私人上傳後驗收。

匿名寄件人、櫃台、硬幣、稱重、空白公文、印刷機、信封及工具排字日期卡都有可製作場景；現稿禁止仿造可讀法案、真實 Penny Black 版面及遺失的指示信。旁白須保留「希爾記載」的歸屬，不能稱他是唯一改革者或郵票唯一發明人。**上述四處修正後可做窄範圍重查，再判題材 PASS。**
