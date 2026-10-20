# S47｜R4 敘事退稿與 R5 作者修訂

日期：2026-10-20。[R4 固定版來源與書面畫面獨立差分](review/r4-source-independent.md)判 **PASS**，但同版兩位真正全新的盲讀者分別答 [A 12/13](review/r4-blind-a.md)、[B 11/13](review/r4-blind-b.md)。兩人共同把必答 `no_recap` 判 **No**：`wr084/094` 重念 59 秒，`wr092/095` 重念 57 秒，而沒有明確回看之前的資料。B 另把 `payoffs` 判 No，因 `wr064` 的「奧維爾壓得住嗎」未得到直接回答。依雙讀者正式規則 **R4 敘事 FAIL**；原版凍結 SHA 和裁決見 [verify-6.md](verify-6.md)。R4 的來源 PASS 不能移用給 R5。

R5 保留一條從動力機到當日四趟及晚間電報的時序、固定 W/N 來源、開場四個未解時刻與事件章名，只作兩處窄修：

| R5 改動 | 作者自查的來源、敘事與畫面界線 |
| --- | --- |
| `wr064→wr065` | 問「奧維爾的控制難在哪裡」，下一句直接答他後來記述的**前舵太近平衡中心，易轉過頭**；新增明確 `loop`。原文也提氣流不規則及駕駛經驗不足，前舵是具體一項難處，不說成唯一原因。[W800–813](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L800-L813)。`wr064` 畫俯臥駕駛、前舵框架、簡化雙層翼／後槳／滑橇，不能畫現代座艙、輪子或虛構故障。 |
| `wr093→wr094` | `wr093` 明說「回看剛才」的 **852 英尺、59 秒**，是回呼 `wr084`，問轉錄電報是否說全；`wr094` 新增**小冊轉錄電報未報地面英尺數**的文本比較，並回答最長時間較奧維爾後述少兩秒，回呼 `wr092` 的 57 秒，避免把兩數再講成新發現。W 記實測地面距離與時間；N 轉錄電報報最長時間、風與空速等，**沒有報地面距離**，不能概括為「電報只報時間」。[W846–855](https://github.com/GITenberg/The-Early-History-of-the-Airplane_25420/blob/85d336f5a53986caf06e063025ca8189980962f3/25420.txt#L846-L855)、[N1619–1631](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1619-L1631)。書面畫面是成年讀者把兩張**無字**紙並排的示意，不冒充歷史原件，也不說奧維爾曾做這個比較。 |
| `wr095`、企劃 A | 只說小冊**作者認為**傳送時弄錯，並明說本集未核對電報原紙；不再緊接著重念 57。企劃 A 的觀眾判斷及電報章同步標出「未報地面距離」這個新比較。N 的原文是作者對 57/59 差異的判斷，不升格為已查過原紙的結論。[N1619–1626](https://github.com/GITenberg/Wright-Brothers-National-Memorial-North-Carolina_57725/blob/063e08af43aae0605c0ad9f32f5ed08fa771fc29/57725-0.txt#L1619-L1626)。 |

## R5 凍結候選

| 檔案 | SHA-256 |
| --- | --- |
| [brief.md](brief.md) | `9ddc5d8f1eafe282df7edb7fd827cc20ef88098e22cf161577dcb72a38901107` |
| [research.md](research.md) | `493d6bf8e73d9832c05300b2c9643e7e53c1448ac2215c54e2f32f9ad10fa357` |
| [script.md](script.md) | `e3d615643941c04d2c17f6fa39d185306ff9c3993eebb62ed1947d87bc92b392` |
| [video.json](video.json) | `a421a3b05102fecb533ef09120a4e992897c284f9a2924421b5d27f04fcffbae` |
| [claims.md](claims.md) | `831a556638d57de46b282af0d4eab7fd9c3ae037c421b7cf2747d273543c19bd` |

固定 W `/tmp/s47-wright-25420.txt` SHA `1cbdc94a6e6851df735fb7171e7ed8d08608c44964237266fac93c2f71e2308c`、N `/tmp/s47-wright-nps57725.txt` SHA `546d76a2ea15dfa0317427b56e0b31e42d3f867f7ef465c82e70e3971e7d1d5f` 未變；可重取連結在 [research.md](research.md)。

作者機械自查：已由上表 `video.json` 重生 `script.md`；97/97 正文景為 `shot`，100/100 句含三句片尾與 `claims.md` 的 ID、順序、口播逐字一致；114 個 W/N 固定行段連結皆在文本範圍內；15 組伏筆的設置和回收 ID 都存在且先後有效。`lint --slug curio-s47 --json` 為 **0 errors／0 warnings**；任務檔 `git diff --check` 與 R5 文件逐行尾端空白檢查均無格式錯誤。`npm run check:tasks` 驗證 2117 份任務檔，原有持有時間／範圍警告未指向 S47。開場按 250 口播單位／分鐘含停頓估 **57.33 秒**、按 325 估 **45.97 秒**；後者正文 `wr009` 至片尾前約 **493.4 秒（8:13.4）**，純正文口播 2183 單位按 250 估 **523.92 秒（8:43.92）**。以上只是靜態估算，**不是 TTS 或成片實測**；原創 5 秒片頭、21 秒片尾及最後約 16 秒推薦／訂閱框仍為製作規格，尚未組片或啟用可點連結。

R5 **僅為作者自查候選**。仍須另一人按上表**精確 R5 SHA** 重做來源及書面畫面差分，再由兩位真正全新、互不相見的讀者各按官方 13 題盲讀；不得沿用 R4 評語或 PASS。推薦 A 只在本機企劃；S47 尚無網站大綱／劇本核准，未買語音、原生插圖或配樂，亦無成片、上傳或短片。
