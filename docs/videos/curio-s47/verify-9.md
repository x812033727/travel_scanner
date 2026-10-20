# S47｜R5 敘事退稿與 R6 作者修訂

日期：2026-10-20。[R5 來源／書面畫面獨立差分](review/r5-source-independent.md)對原版判 **PASS**，但兩位真正隔離的新讀者各答 [A 12/13](review/r5-blind-a.md)、[B 12/13](review/r5-blind-b.md)，共同把必答 `no_recap` 判 **No**，所以 [R5 正式敘事 FAIL](verify-8.md)。兩人同指出 `wr097` 在 `wr091` 電報後又念四趟；A 指 `wr010–011` 重覆重量／馬力門檻，B 指 `wr078–079` 及 `wr085` 相近操控／路線回述。兩人都認可 `wr093` 的「回看剛才」及 `wr094` 的電報未報地面距離是有新資訊的回呼；R6 留著這段。R5 的來源 PASS 只屬原版，不移用給 R6。

R6 繼續一條從兄弟造動力機到十二月十七日四次試飛及電報的時序，固定 W/N 來源、開場四個未解時刻、八個事件章名與卡通示意畫面規則不變。

| R6 改動 | 作者自查的來源、敘事與書面畫面界線 |
| --- | --- |
| `wr011→wr020` | `wr010` 仍只說**引擎本身**至少八匹煞車馬力／不超過兩百磅；`wr011` 換成**整機連駕駛**初估五百五十磅及「多出力能否放寬總重」的新問題，於 `wr020` 回答七百五十或八百磅，新增 `loop`。這些是奧維爾的**後述設計估算**，不是當場秤重。[W506–526](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L506-L526)、[W580–587](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L580-L587)。整機無字草圖不冒充原圖紙。 |
| `wr076–079` | `wr076` 只說第三趟先拉平、原本較高一側降過頭、右翼先觸地的**可見結果**；`wr078` 才給奧維爾後述「側向控制比預想更有力」的**判斷**，不再重講「只要扭更大」。`wr079` 改給小冊的**11:40 第三趟起飛**時間，問威爾伯會否接手，下一章 `wr080` 用正午第四趟回答；刪掉「兩次落地都帶來操控經驗」的泛泛回述。[W834–856](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L834-L856)、[N1555–1564](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1555-L1564)。懷錶是無字時間示意，不當作當日測量物證。 |
| `wr085` | 先前已在 `wr081–084` 說第四趟較平的路段、最後再俯仰及地面距離，故本句改給**小冊作者的因果解釋**：兄弟不願在強風中讓陌生新機飛高，部分俯仰還未改正便觸地。這是小冊歸納，不說成原始高度紀錄或逐秒實測。畫停妥的簡化雙層翼機與風中人物，無現代座艙／輪子。[N1582–1585](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1582-L1585)。 |
| `wr097`、企劃 A | 最後一句不再說 `wr091` 已報的四趟，改引小冊所載**威爾伯的說法**：陌生新機練習不到一分鐘，懂當時條件的人反而驚訝它能飛得長。這給片名「只有十二秒」一個新參與者角度；不說是威爾伯在電報當晚當場說，也不裁定航空史優先權。畫機旁回望的卡通意象，不加對話框或可讀假引文。[N1582–1591](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1582-L1591)。 |

## R6 凍結候選

| 檔案 | SHA-256 |
| --- | --- |
| [brief.md](brief.md) | `d4eefcb524fc68217f5b9a122039e07537bb92ec34226f447c85bec2d1295f06` |
| [research.md](research.md) | `493d6bf8e73d9832c05300b2c9643e7e53c1448ac2215c54e2f32f9ad10fa357` |
| [script.md](script.md) | `0dd8a74680d53b3133401b03495454df79564c23a0335dace21c8f13e38d3603` |
| [video.json](video.json) | `3d8e87514a92de3ac42a2c3fadb23d5e1e0a54033be36daf27a9265506e15d45` |
| [claims.md](claims.md) | `9675fb565211d4d2cc80a038aa18ea29db62a396bcf8cb0a7d6d214b77a090ae` |

固定 W `/tmp/s47-wright-25420.txt` SHA `1cbdc94a6e6851df735fb7171e7ed8d08608c44964237266fac93c2f71e2308c`，N `/tmp/s47-wright-nps57725.txt` SHA `546d76a2ea15dfa0317427b56e0b31e42d3f867f7ef465c82e70e3971e7d1d5f` 未變，重取連結在 [research.md](research.md)。

作者機械自查：已由上表 `video.json` 重生 `script.md`；97/97 正文景為 `shot`，100/100 句含三句片尾與 `claims.md` 的 ID、順序、口播逐字一致；113 個 W/N 固定行段連結皆在文本範圍內；16 組伏筆的設置和回收 ID 都存在且先後有效。`lint --slug curio-s47 --json` 為 **0 errors／0 warnings**。開場按 250 口播單位／分鐘含停頓估 **57.33 秒**、按 325 估 **45.97 秒**；後者正文 `wr009` 至片尾前約 **495.8 秒（8:15.8）**，純正文口播 2196 單位按 250 估 **527.04 秒（8:47.04）**。這些只是靜態估算，**不是 TTS 或成片實測**；原創 5 秒片頭要在濃縮開場之後，21 秒 `v4-endscreen` 片尾最後約 16 秒留推薦／訂閱框，實際可點連結仍待私人上傳後由 Studio 設定與測試。

R6 **僅為作者自查候選**。仍須另一人按上表**精確 R6 SHA** 重做來源及書面畫面差分，再由兩位真正全新、互不相見的讀者各按官方 13 題盲讀；不可沿用 R5 評語或 PASS。推薦 A 只是本機企劃；S47 尚無網站大綱／劇本核准，未買語音、原生插圖或配樂，亦無成片、上傳或短片。
