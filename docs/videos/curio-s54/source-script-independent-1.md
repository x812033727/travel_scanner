# S54｜第一版逐句史料與書面畫面獨立覆核

2026-10-20 UTC。**結論：HOLD；此精確凍結版尚不能取得逐句史料及書面分鏡 PASS。** 核心「一月費率先行、五月郵票後到」成立，112,000 的歸屬也守住界線；以下少數句子與提示詞仍須修訂，再以新雜湊覆核。本覆核沒有進行媒體、政策、TTS 或盲讀審核。

## 精確輸入與獨立重開的原文

我直接從三個固定 Git 提交的 `raw.githubusercontent.com` 全文 URL 重新下載 A／H／L 並計算原始位元組 SHA-256，不把 [先前題材可行性 PASS](source-feasibility-2.md) 或作者研究表當作原始證據。

| 輸入 | 本次 SHA-256 | 結果 |
| --- | --- | --- |
| `research.md` | `fbdcdd8b091fcbd1b5d8c8cf885debf6da830f04f613973210fe90b05de5dc30` | 符合 [作者凍結](author-freeze-1.md) |
| `brief.md` | `a991fe01f3567d00b65844fc886212d9e7ccea354109516fb8038319c369b132` | 符合 |
| `claims.md` | `eb08f002ca62d9505dcfc0a7911ce31a4a715902e15ee84d0c9748ac137dd095` | 符合 |
| `video.json` | `6158de12b76eee022effd5e44905a416756a280e2b4a8ac8e37d07095521dab3` | 符合 |
| `script.md` | `a899e942f3e231ff9f5e42dc01eb379149dbaadae289ed7415329d107603797e` | 符合 |
| [A：1839 法案](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) | `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254` | 符合研究表；當時法條，OCR 有破字 |
| [H：希爾回憶錄第一卷](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt) | `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939` | 符合；1880 年姪子編刊的回憶，包含日記轉錄 |
| [L：Leavitt，1848](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt) | `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e` | 符合；倡議者的近時說明，非英國郵局帳本 |

逐句核對 `video.json` 的 **153 句**與 `script.md`：文字順序完全相同。前 150 句各有一列 `claims.md`，文字完全相同；片尾三句中首句重述已查過的時間線，其餘兩句是互動與訂閱。150 個正文場景是 **144 `shot`＋6 數字／日期卡**，另有一個片尾場景；18 組 `loops`。144 條 `shot` 提示詞均逐條閱讀。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json` 本次回傳 **0 errors、0 warnings**，估計旁白 13.8978 分鐘。排除開場八句及片尾後，正文有 2,626 個漢字；每分鐘 325 個漢字估算約 8.08 分鐘。這仍是書面估算，實際正文八分鐘須待 TTS 驗證。

## 通過的主要史料界線

- [A L9188–9240](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) 是 1839-08-17 的授權與可用形式，不是當日一便士費率或郵票開售。全稿主線和企劃沒有把它們壓成同一天。
- [H L13061–13169](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13061-L13169) 記現金先預付、郵票待備妥、1840-01-10 全國一便士費率；[H L13328–13353](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13353) 記 05-01 開售、05-06 准用。[L L4144](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L4144) 只交叉支持 01-10 與 05-06，沒有 05-01。旁白 `s54115–s54116` 已說清這層差別。
- [H L8761–8773](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L8761-L8773) 的伯明罕／倫敦九、十八便士例子與什魯斯伯里商人包裹是兩組通信；稿中分開。[H L9288–9319、17773–17784](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9288-L9319) 支持 Robert Wallace 及較早的改革工作，沒有把希爾寫成唯一改革者。
- `s54095–s54103` 把 112,000、未預付約 13,000–14,000、近 80,000 入信明確歸屬 [H L13213–13250](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13213-L13250) 的日記，沒有稱全國總量、倫敦確址或已貼票。`s54105` 的一月十四日人潮也在該日記段落。希爾的漏 `not`、印量和紅墨銷票均保留當事人回顧的歸屬；1848 年 Leavitt 的家用、店家、回信郵票沒有在旁白倒推為 1840 年首日逐站庫存。

## 須修訂才可 PASS

| 位置 | 具體差距 | 最小修法 |
| --- | --- | --- |
| `s54026` | 旁白說委員會「交出十份報告」；[H L9288–9294](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9288-L9294) 原文是 *no less than ten reports*，只保證至少十份。 | 改「至少十份報告」。 |
| `s54093` | 旁白把「大量通知信」與「預付的人潮」合成「通知信送來預付」。[H L13213–13226](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13213-L13226) 分別記聽說大量 circulars 寄出，以及《Globe》報郵局擠滿預付者；沒有說那些 circulars 均預付。 | 分成「他聽說當晚寄出大量通知信；報紙另說預付的人擠到郵局」等窄句。 |
| `s54117` | 「三個大辦公處，起初反對直接賣郵票」把反對者寫成三處本身。[H L13334–13345](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13334-L13345) 說的是**部門內有人反對在**倫敦、都柏林、愛丁堡三個總局售票。 | 明說「希爾記部門起初反對在三個總局賣郵票」。 |
| `s54113` 卡片出處、`s54150` 主張列 | `s54113` 的「5 月 1 日開售／6 日准用」卡片把 H 與 L 並列，容易使 L 被讀作兩個日期的共同見證；L 只記 6 日。`s54150` 的三日期總結只標 P12／L 的 1848 使用方式，沒有標支持日期的 P07／P09。 | 卡片分注 H 支持兩日、L 只支持 6 日；末句補 P07／P09。 |
| `s54056` 插圖 | 「免郵資寄信特權」配 `foreign-bound blank envelope`，把國際信帶進國內免資問題，對位錯。 | 換成沒有目的地字樣的免資文件或封套概念。 |
| `s54107`、`s54109` 插圖 | January 1840 的寄件人已拿起 `premarked cover`，而預印封套尚在籌備；同章 January 1840 的人看 `May calendar`，但五月准用日到 4 月 22 日才定。[H L13138–13169、13328–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13138-L13169) | 107 畫一人思考空白封套方案；109 畫未標月份的候選日曆，或移到四月決定後。 |
| `s54092`、`s54083` 插圖 | 92 要人在 `blank diary` 寫一個 number，會造出看似可讀的當日日記數字；83 只寫 `a gazette`，未限制虛構可讀版面。兩者均不是取得的實物影像。 | 92 改翻無字頁；83 明寫無字／不可讀的概念報紙。數字與日期交給工具字卡。 |
| `s54115–s54116`、`s54132–s54141` 插圖 | 多條 prompt 把 1848 年 Leavitt 小冊、1880 年希爾回憶錄或 Leavitt 的後來家用／店家／回信方式，置於 `stamp supply workshop in spring 1840`。尤其 115 的「1848 booklet」在 1840 房間、132 的回憶錄在 1840 房間，形成不可能的時間及地點；133–141 的回顧畫面也會抹掉旁白強調的八年差。[L L2372–2422](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2372-L2422) 是 1848 年說明。 | 把後世讀來源的鏡頭移至不標 1840 的研究桌；Leavitt 生活例子改成 1848 年家庭、店鋪、信箱的無字概念插畫。 |

修訂後應重產 `script.md`、`claims.md`、`video.json`、必要的研究／企劃文字，重新凍結雜湊，再就新輸入做獨立覆核；原版 lint 通過不會替新版本背書。
