# S54 R10｜獨立史料與書面畫面覆核

2026-10-20 UTC。**旁白史料 PASS、逐句主張對齊 PASS；書面畫面 HOLD 一景。**本結果僅綁定下列五檔；盲讀、政策、語音、實際生成圖與站台審核各有獨立關卡。

| 凍結檔 | 獨立重算 SHA-256 |
| --- | --- |
| `research.md` | `412eef60918feb5c989d0e1675e8a6f7373ba9f720428cb9221d797d1975b60f` |
| `brief.md` | `5e234769e00988f427151afc953407ff52711df6c12c74043e64b67567509942` |
| `claims.md` | `6c1848776533319a8c2119c98d5c3320ca3574fb787ae220da4a6ad8ffb9d151` |
| `video.json` | `67aec9cf177fe7a0639573dcf59249893f641cf51f70da152cd3ba0207fa59d6` |
| `script.md` | `d48b818f3eefecf633f75f9a206bb10d22a212831b7855e902739da2e3b30938` |

## 固定原文與新段落

我重新由三個固定 Git 提交下載原始文字，再各自計算全文 SHA-256：1839 年 [法案](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`；希爾與其姪子 1880 年編刊的 [第一卷](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13208-L13250) `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`；Leavitt 1848 年 [《Cheap Postage》](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2372-L2435) `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`。這與研究表固定版本相同。希爾日記是事後著作的轉錄，並非獨立的郵局業務總表。

| R10 位置 | 原文對讀與判定 |
| --- | --- |
| `s54082–89` | [希爾一月十日日記 H 13208–13219](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13208-L13219)先記全國一便士費率、引 *Globe* 報紙稱預付寄信者擠滿郵局，再寫自己猜當晚不少於 100,000 封、超過一年前同日三倍；他聽說通函寄出，為免干擾未到場。[H 13245–13248](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13245-L13248)是他後來記述大廳為本人和職員各歡呼三聲。R10 用「引報紙／猜／估／聽說／回憶」歸屬，沒有說他人在現場。**PASS**。 |
| `s54090–94` | [一月十一日日記 H 13221–13227](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13221-L13227)才寫前一夜 112,000 封，其中約 13,000–14,000 未預付，以及大廳收費辦法不足的混亂。R10 把這些句子放在一月十日的猜測與歡呼之後，並說明數字非全國逐站合計，沒有誤稱貼票。**PASS**。 |
| `s54144–47` | [Leavitt L 2395–2403、2413–2425](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2395-L2425)記可先買附膠票，在家貼信後投信箱；英國仍有預付封套；替對方回信預付時可以夾入一枚郵票。稿子明說是八年後對既行制度的說明，沒有倒畫成 1840 年首日。**PASS**。 |
| 全段日期邊界 | [1839 法案 A 9194–9222、9230–9240](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9194-L9240)只是授權；[H 13328–13345](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13345)分開 5 月 1 日售票與 5 月 6 日准用；[Leavitt 註 10 L 4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144)也分列 1 月 10 日費率、5 月 6 日郵票。正文維持三個不同時點。**PASS**。 |

## 畫面待修

`s54109` 旁白說「四月二十二日財政部定下新時點」，但提示詞把畫面設在 **May 1840 的 London receiving house**，並令職員翻開四月日曆。這可能使四月的決定被畫成五月收件所內發生；[希爾 H 13328–13329](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13329)說的是 4 月 22 日財政部議決。請作者將此**單一場景提示詞**改成四月的決策或單純後來讀檔的示意，再重產 `script.md`（若生成器要求）與凍結雜湊。其餘 139 個插圖提示詞及 7 張工具字卡作為**書面**示意，未見具體與旁白相反的日期、人物、數字或已貼票的 1 月畫面；此報告不替實際生成圖背書。

## 對齊與檢查

`video.json` 共 147 個編號敘事場（140 插圖、7 字卡），另有 3 句片尾旁白與 23 組 loop。`claims.md`、`script.md` 和場景 ID、順序、旁白 **147/147 逐列同文**；140 個插圖提示詞皆非空。濃縮開場 151 個漢字，正文 2,631 個漢字，在 325 字／分鐘的最快估算法下為 **8.10 分鐘**，仍須 TTS 實測。`VIDEO_WORKDIR=/workspace/.video-work NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s54 --json` 回傳 **0 errors、0 warnings**。

此書面畫面 HOLD 僅針對 `s54109`，不否定上列史料或既有盲讀；修正後必須以新雜湊重查此處和各後續關卡。
