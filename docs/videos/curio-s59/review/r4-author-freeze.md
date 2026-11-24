# S59 R4｜作者窄修與五檔凍結收據

2026-10-21 UTC。A 案〈1878 年科學院聽見留聲機說話，為何有人懷疑腹語？〉之 **R4 作者候選**。R3 [正式敘事](r3-merge/summary.md)因兩位盲讀者共同的 `no_recap` 未過而 HOLD；R3 [史料與書面畫面](r3-source-independent.md)為 PASS／PASS，但舊版結論不能放行 R4。R4 未執行 TTS、付費圖片、政策評審、站主審批或發布。

| 凍結檔 | R4 SHA-256 |
| --- | --- |
| `research.md` | `d0077504f3dbe828363158a25c7e7dade955089f49dbb03a734893739e12467e` |
| `brief.md` | `9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3` |
| `claims.md` | `e19a8aa75c7d61bbba54b4d747db3b7025ac34599964ac0c4c115fbacd8d8c0b` |
| `video.json` | `108db5d8ae5b540e396b1e9add3490c7ac8761e1aaa7dfd76b172edbadaba226` |
| `script.md` | `5b18eb40b5c3434599abbd939d3231fc30837e360bfaff0ea00d23cdca89cf48` |

具體 R3→R4 差分、行號與畫面界線見[逐景稽核](r4-author-delta-audit.md)；[全句來源行號預檢](r4-source-citation-audit.md)核 110／110 ID／文字與 D／E 固定原檔 SHA。D 為 1878 同代記載，E 為愛迪生 1910 年晚年自述，譯本 T 只輔助閱讀，不增加獨立證人。機械唱歌／鐘錶驅動是 D 的前文例子，未當作 3 月 11 日秘書室程序。

六章、110 句、12 組 `loops`、100 張插圖景與 10 張工具排版卡。濃縮開場 9 句、196 漢字，工具估約 56 秒；正文 2,610 漢字，按最快每分鐘 325 漢字約 **8.03 分鐘**。全片工具估 13.31 分鐘，實長待語音；固定 5 秒頻道片頭與 21 秒 `v4-endscreen`、說明欄兩份來源及頻道連結、長片核准後擷取 Short 的安排仍在。`script` CLI 生成 narrative hash `6c63c018a205170c`；`visualHash(video.json)` 為 `6c891383737963b9`。

驗證：`node tools/video/cli.mjs lint --slug curio-s59 --json` **0 errors／0 warnings**；`npm run test:docs-videos` **236／236 PASS**；`node tools/tasks.mjs check` 退出 0（其他舊任務有警告）；凍結後再次重算五檔 SHA 與本表相同。作者僅逐項自查固定 13 題的結構，不對自己的版本寫敘事 PASS。接下來需**全新獨立史料／書面畫面覆核和兩位無前情敘事讀者**，固定 OR 後才可判政策門檻；任何五檔改動皆使這版審稿過期。
