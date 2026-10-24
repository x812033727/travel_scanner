# S50 R7｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS：R6 唯一來源／書面畫面 HOLD (`fire019` 窗邊站位) 已在精確 R7 內容版解除。**本覆核只簽核凍結稿的來源與待畫提示詞差分；不代替同版兩位新讀者盲評、政策、網站劇本卡、實際插圖或 119 句真實音檢。沒有改作者五檔，也沒有生成或購買媒體。

| R7 內容檔 | 重算 SHA-256 |
| --- | --- |
| `brief.md` | `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b` |
| `research.md` | `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95` |
| `claims.md` | `4e07795ddf55b4b686431851664cb1c686333233417e378b87b9e96c1180bedc` |
| `video.json` | `e2c2537dc0fe97807e1f686a7d511b5f64d03680f89c1c0461cec3bbe8ad0234` |
| `script.md` | `5f9ae7f8b89b5f898c982dd51215c5d148901820bf715e10e6d43f8872ef782b` |

三份固定原文亦重算：Pepys `/tmp/new-pepys/4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`；1667 證詞刊本 A `/tmp/curio-s50-A63385/A63385.xml` 為 `0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e`；Vincent `/tmp/curio-s50-A64990/A64990.xml` 為 `36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29`。R7 五檔與三份原文均符合 [R7 作者凍結](r7-author-freeze.md)；`brief.md`、`research.md` 仍是 [R6 獨立覆核](r6-source-independent.md)所見位元。

## `fire019`：PASS

Pepys 1666 年 9 月 2 日 [D L65793–65802](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65793-L65802)先寫 `Jane called us up about three in the morning, to tell us of a great fire they saw in the City`，隨後才寫 `So I rose ... and went to her window`。這只支持珍妮叫醒並報火、佩皮斯後來到她的窗邊；沒有說她叫人時站在窗邊。[Vincent V L2188–2206](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml#L2188-L2206)的橋邊受阻與泰晤士街路線是事後敘述，不是佩皮斯在床上看到的景象。

R7 `fire019` 口播是「有人叫了起來；床上的佩皮斯還不知道橋頭燒成什麼樣。」；待畫提示詞是 `Medium shot in a plain bedroom before dawn, one diarist stirs in bed as an unseen person calls to him, pale light`。兩者都沒有再指定呼叫者從窗邊出聲，且佩皮斯在床、呼叫者未入鏡；「還不知道」也沒有把前一段橋頭火線說成他的當下目擊。`claims.md` 明記日記的先後與 Vincent 敘述的層級；`fire019→fire020` 的 `what` 改為「誰在凌晨叫醒佩皮斯」。緊接的 `fire020` 明說珍妮叫醒並報火，既有提示詞只畫女僕朝窗外火光指去，沒有指定她叫醒人時的站位；`fire021` 才畫佩皮斯到窗前。R6 [窄 HOLD](r6-source-independent.md#fire019窄-hold)所指的口播與提示詞越界已移除。

## R6 基線與機械核對

把 R7 `video.json` 的 `fire019` 口播、提示詞與 `fire019→fire020` 伏筆文字三處還原成 R6，位元 SHA 立即重現 R6 `f231e8bd4118adb40d5c49974dd24747b8bb0cfb1de8528d4735127ca291e892`；把 `claims.md` 的 `fire019` 一列還原，重現 R6 `1006cfea670965d23618cd5de939f7ce70ad3d9731289ea72102916faaa3fc7a`；用還原的 JSON 直接呼叫儲存庫 `screenplay(doc)`，重現 R6 `script.md` SHA `a988c497ac8cc46cc4a80a7e3f268aff62c4ad9dfcd89f5bc8b87c505f1989b7`。因此 R6→R7 的 JSON 僅上述三欄、主張表僅一列，腳本只是同版 JSON 的重生。R6 七句 `fire015/020/032/039/062/078/099` 均逐字仍是 [R6 作者表](r6-author-freeze.md)與 [R6 獨立 PASS](r6-source-independent.md#七句新口播pass)所核版本；其餘 118 句、112 個提示詞和 28 條伏筆均未改。

獨立解析得到 **117 景、119 個唯一口播 ID**；`claims.md` **119/119** 同 ID／文字／順序，`script.md` **119/119** 同文字／順序且與 `screenplay(doc)` 逐位元相同；**113/113** 個 `shot` 提示詞非空，**29/29** 條伏筆 setup 先於 payoff，**9** 章。`node tools/video/cli.mjs lint --slug curio-s50 --json` 為 **0 errors／1 warning／119 lines**；唯一 warning 仍是片尾沒有口頭訂閱提醒，畫面 CTA 不在本次修改範圍。這些是文字與書面畫面核對，並非實際配音時長或圖片驗收。

Gazette `fire037` 的木屋／易燃材料與 London Museum `fire108` 的「火星可能」仍只承接倉庫 [P17 第 5、3 列](../../history-curiosity/topic-checks/P17.md)的先前原站查核。本次用編輯用 User-Agent 對兩個原站 URL 作只讀 GET，兩者皆 `curl` 403、`http_code=000`，沒有收到原站內容；因此**不聲稱本輪直接重驗 Gazette 或 Museum**。這是繼承的來源可達性界線，不影響這次只改 `fire019` 的差分 PASS；正式原站重開仍是票上的待辦。

**下一關：**同一 `script.md` SHA 的兩名新讀者腳本盲評；其後重綁完整政策、網站劇本卡、改句配音與全片 119 句零旗標音檢。來源／書面畫面 PASS 本身不放行插圖、配樂或成片。
