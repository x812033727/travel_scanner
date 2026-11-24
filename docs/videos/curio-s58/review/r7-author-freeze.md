# S58 R7｜共同重述阻擋的窄修作者凍結

2026-10-21 UTC。**R7 作者候選，待非作者來源／書面畫面覆核及兩位新盲讀；不是媒體製作或網站核准。** [R6 正式合併](r6-merge/summary.md)封存兩位讀者共同否定 `no_recap` 的 12／13 HOLD；[R6 獨立來源覆核](r6-source-independent.md)只對舊版五檔有效。

| R7 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `fbb902e05bede6a4a88b108aae725667b41058c979ff7a69dea339a188c19e87` |
| `video.json` | `ad330abbe8f0919987c01de2c3227e025af8d1d93cc7f2e3557875d5d7b629ec` |
| `script.md` | `d32bea9d5cc33125cf9b41f1288a8faf78765d96dcd3ed2002abe4ad97f20957` |

## R6 → R7 的三句修改

- `s58068` 去掉前一句 `s58067` 已說的「車夫持葡萄酒通行證」，只問剩下器材先藏進什麼運離村子；`s58069` 仍立即回答空酒桶，`s58071` 仍在 Arcis 稅卡前留桶。
- `s58124` 不再重述 `s58087` 的裸眼難讀，改說歸巢鳥從省外飛回被圍巴黎；畫面仍為巴黎窗邊的一隻帶羽管鳥，沒有聲稱某封私信已送達。
- `s58125` 把問題說成「城裡要怎樣讀出這卷薄膜上的訊息」，接 `s58126` 的電燈光放大；不再重問字有多小。

三句在 `video.json`、`claims.md` 和衍生 `script.md` 同步。其餘三份作者內容及書面畫面提示詞未改。146 景、141 `shot`、5 `big`；濃縮開場 183 漢字，六章正文 2673 漢字，按每分鐘 325 漢字為 **8.22 分鐘**（最終時長仍須 TTS timeline 驗證）。`lint --slug curio-s58 --json` 為 0 error／0 warning；`npm run test:docs-videos` **236／236**，`npm run check:tasks` exit 0。R7 未使用語音、插圖、配樂、合成或上架；網站仍只有先前 report-only 項目，未提交核准卡。

下一步：非作者重核 R7 固定來源、三句與整份書面提示詞；兩位未看前稿的新讀者僅讀 R7 劇本與固定敘事 13 題，各自留原票，最後正式固定 OR 合併。任何改稿都須重凍結，不能沿用 R6 或 R7 的舊票。
