# S54 R9｜一月日記與銷記段的獨立史料／書面畫面覆核

2026-10-20 UTC。**旁白史料 PASS、主張對齊 PASS、書面畫面 PASS**，僅對下表五檔有效。R9 的敘事雙盲、政策、實際配音、生成插圖與站台關卡仍未由本報告裁決。

| 凍結檔 | 獨立重算 SHA-256 |
| --- | --- |
| `research.md` | `4ef0c1f2f3857940fd9487016dbddd1c96bb834d0dd6f7d73c0efa93f34476e4` |
| `brief.md` | `9ef676cf3ae4223c7a1e537015db8218eae00a675ba52d91de37ee3217c17bb8` |
| `claims.md` | `ff757d5d19c86e22eedeec8d989d34a03880426949c087450a3b1c4ee124f2d7` |
| `video.json` | `38328e853243c2423b94864df8c466da9c20c56801efb28b3749764bad5aa872` |
| `script.md` | `d3d85c6b69290596690a83e28acd8cdf95c07a912f25d98abc718f57406e20db` |

## 固定原文與 R9 改動

獨立讀取完整固定來源文字並重算位元組：1839 年法案 OCR `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`、希爾及姪子 1880 年編刊第一卷 `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`、利維特 1848 年書 `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`。版本與 `research.md` 的固定提交相同。希爾的日記是後來書中轉錄的本人記述，並非另取的 1840 郵局帳簿。

| R9 位置 | 直接對讀與邊界 | 判定 |
| --- | --- | --- |
| `s54072`、`s54083` | [希爾 13061–13169](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13169)將先收現金與郵票待備妥分開；1 月 10 日費率先上路。R9 只在 `s54072` 說一次現金方案，`s54083` 轉問當晚寄件量，未把一月畫成已有郵票。 | PASS |
| `s54084–89` | [希爾書中 1 月 10–11 日日記 13205–13225](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13205-L13225)：他估當晚不少於 100,000 封、超過一年前同日三倍，說聽聞大量通函寄出；為免妨礙郵局作業沒有去現場。翌日日記寫前一晚寄出 112,000 封。R9 明寫「猜／估／聽說／日記」，沒有把估計或 112,000 說成全國總數或官方獨立統計。`s54084–85` 的後來讀檔者及 `s54086–87` 的匿名大廳／書桌是概念插畫，提示詞無可讀日記或正式帳單。 | PASS |
| `s54140–42` | [希爾 13410–13431](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13410-L13431)稱漏蓋或去掉銷記是難題；[1839 法案第五條 9230–9240](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9230-L9240)把未用過列為條件；[利維特 2433–2435](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2433-L2435)解釋收信時蓋銷記防重用。R9 刪去紅墨細節，畫面只用無字紙票示意，未重建真正 Penny Black。 | PASS |

R8 兩位讀者的具體異議保存在 `r8-isolated-merge.md`：舊 `s54084` 重講現金，舊 `s54085` 重講收件人付款，`s54140–43` 偏長。R9 現行句子已改成上表新史料；第九版的敘事效果須由**兩位全新只讀稿讀者**裁決。工作區沒有 R8 五檔的完整位元組快照，故此報告不聲稱重建 R8→R9 全檔雜湊差分；已逐句重核 R9 新事實、主張錨點與相應畫面，並以 R8 的精確獨立報告為既有基線。

## 對齊與靜態檢查

`video.json` 有 146 個編號敘事場：139 個插圖、7 張工具卡，另有 3 句片尾旁白；23 組 loop。`script.md` 與 `claims.md` 的 146 個 ID、順序、旁白**逐列完全同文**，139 個插圖皆有非空提示詞。首章後、片尾前的正文有 2,612 個漢字，以最快 325 CPM 估 **8.04 分鐘**；尚非實際 TTS 時長。`VIDEO_WORKDIR=/workspace/.video-work NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s54 --json` 退出碼 0，**0 errors／0 warnings**。
