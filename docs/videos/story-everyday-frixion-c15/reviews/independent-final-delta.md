# C15 FriXion｜最終修稿來源與配鏡差異獨立覆核

**判定：PASS（只限本次 H07、H08、N05 差異及機械配對）。** 2026-10-23 由非作者代理直接讀 PILOT 原件，再對照作者草稿 PR #1701 的 `be7bad23848f925dda3495701802bafa0f8f43c4`。這份收據不代替兩位新讀者對整篇純旁白的盲讀，也不代表站主核准或實測配音／圖片完成。

## 精確輸入

下列為該提交的 **Git blob bytes** SHA-256；Windows checkout 可能對 JSON 做換行轉換，因此不以工作目錄的 JSON 檔案雜湊替代 Git blob 雜湊。

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `C75E85C881F51942C8CAD0BDD0185615F2CBDB6A2CCF2F6EED846724A6ECEBD4` |
| `script-source-notes.md` | `5429A1B0B04C412A0A50E8F47A4B39123CAE06D9E79771FCBEE9F26F23F2C121` |
| `visual-plan.md` | `60CD58C0F2BA2874550B34714132CDA8B56712DB81C43C1103F0644B2BB35A45` |
| `visual-plan.json` | `B9E67726FDB99B71B3D6086AC38765EE513171F57E2261213FC843B66BC992A5` |

比對前版 `31e43913902cc397a4bd3e6924a01b692f63f83f`：實質改動只有 H07、H08、N05 的旁白，N05 的插圖提示詞與護欄，H07／N05 的紙上秒數；其餘為狀態與來源備註。沒有把 PR #1715 的舊位元組 PASS 直接移植到新稿。

## 直接來源與逐項判定

| ID | 原件核對 | 配鏡核對 | 結論 |
| --- | --- | --- | --- |
| H07 | [PILOT 開發故事 Part 2](https://www.pilot.co.jp/media_english/006/index.html)「2002–2006」明說實驗室小燒杯可達成的墨水性能，轉成產線大量且同品質很難；研發人員往返實驗室與工廠。新句以「小量墨水進入工廠考驗」概述量產難題，沒有再提前說 2004 年決定或虛構失敗批數。 | 未變動的畫面是匿名工作者、無字筆和小混合器皿；護欄寫明「量產難題概念，不是工廠影像」。不作歷史現場或具體工法證據。 | PASS |
| H08 | [PILOT 開發故事 Part 1](https://www.pilot.co.jp/media_english/005/)記載 1976 年 Magic Cup 使用 Metamo Color、其後改良與縮小微膠囊；[Part 2](https://www.pilot.co.jp/media_english/006/index.html)接續可擦筆的透明化及工業化。句子是待答問題，問同一技術路線如何走向筆，沒有斷言 1976 杯子與市售筆採相同配方。來源備註也明定不得如此推論。 | 未變動的杯子與無商標筆並置，只表現待答關係，沒有畫成一杯墨水直接灌進筆。 | PASS |
| N05 | [PILOT 現行 FriXion FAQ](https://www.pilot.co.jp/support/frixion/frixion_1.html)明說三成分在微膠囊中受摩擦熱改變，墨色轉為無色；新句只講摩擦熱使墨色變無色，消除與 I07 的微膠囊重複。 | 新提示詞只畫抽象深色筆劃在筆尾摩擦下變淡；不再重畫微膠囊，也不表示墨水被物理刮除。實際生成仍須檢查畫面是否把筆尾錯畫成硬筆尖或顯示墨屑。 | PASS |

機械檢查：`script.md`、`visual-plan.md` 與 `visual-plan.json` 都是 87 個相同順序且唯一的 ID；JSON 的 87 個 `narration` 全與劇本逐字相同。72 張候選插圖、15 張後製字卡；每張插圖均標 `MiniMax image-01` 與精確 `cute-mystery` preset。這些只是文字方案和紙上時間，未生成圖片、未測得正文 480 秒或插圖時間占比。

**下個關卡：**兩位全新且彼此隔離的讀者只看這版 ID／旁白，重判開場、重複、時間目錄與單線故事；任何再改稿須重算四檔雜湊並按差異覆核。此收據沒有付費、匯入、上傳或發布權限。
