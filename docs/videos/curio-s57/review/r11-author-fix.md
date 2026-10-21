# S57 R11｜作者只修八景書面提示詞

2026-10-21 UTC。**R11 是作者候選，未自判書面畫面 PASS。**先完成 [R10 兩位合格讀者固定 OR 正式合併](r10-merge/summary.md)：敘事 13／13 PASS；另有 [R10 非作者獨立史料與書面畫面覆核](r10-source-independent.md)：史料／逐句主張 PASS、書面畫面 HOLD。該獨立覆核由同一工作者先前以**R10 審查者**身份撰寫；本次依新任務改以**R11 作者**身份實作明列的八個 prompt，不把自己的作者收據當作 R11 獨立覆核。未改該 R10 審查紀錄或兩位讀者原票。

| 創作檔 | R10 前版 SHA-256 | R11 候選 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd` | `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd` |
| `claims.md` | `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` | `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` |
| `video.json` | `0275fe764a2a79ee0d122780853bb3bfa21922c86a4f650475c7dc6c1fb39d2f` | `6c18cfe0ae62d80bbb066ec17a397d364b2bb3b47fd2afeaf05fb62ebb66b2be` |
| `script.md` | `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` | `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` |

[R10→R11 精確差分](r11-author-diff.patch) SHA-256 `4f7f138b823ff803040d56d22d19afb32e8a88f39a48e230d0d52270cfb1ec68`。將它在 `/tmp` 的 R11 `video.json` 副本反向套用，恢復 R10 `video.json` SHA `0275fe764a2a79ee0d122780853bb3bfa21922c86a4f650475c7dc6c1fb39d2f`。解析前後 JSON，**只改以下八個 scene 的 `data.prompt`**：`s57114,s57117,s57118,s57120,s57122,s57133,s57135,s57139`。159 個 scene ID、次序、旁白、其他 scene 欄位、所有頂層欄位都相同。`research.md`、`brief.md`、`claims.md`、`script.md` 未改；後三檔中原有的「R10」版本字樣因此只是上一輪內容凍結的標記，不代表它們另獲 R11 審查。

| ID | R10 HOLD → R11 作者窄修 |
| --- | --- |
| `s57114` | 多名搬運者同時帶驢、山羊渡河 → 一名搬運者牽一頭驢過河；只示意 [L5458–5459](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5458-L5459) 的其中一部分，不否認旁白提及的其他同行者。 |
| `s57117` | 水陸兩隊同框 → 一名船上嚮導望向無人的陸路方向，以單人畫面留住尚未會合的問題。 |
| `s57118` | 多人立多面旗且同伴找路 → 一名嚮導在湖岸營地立一面素旗，對應 [L5482–5488](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5482-L5488) 記立旗引導陸隊。 |
| `s57120` | 人、山羊到營與史丹利臥病同時同框 → 只示一位年輕記者在營地歇息；旁白仍按 [L5498–5499](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5498-L5499) 交代到齊與發燒。 |
| `s57122` | 多人等候與病人休息並排 → 一名搬運者在已打包行李旁等待，留出前路。 |
| `s57133` | 記者開門時老人站在舊箱旁 → 一名記者開儲物間門，新貨與舊箱以分開擺放的素面道具示意兩批貨。 |
| **`s57135`** | 兩人共同開李文斯頓舊箱 → **一名年輕記者用槌、鑿開舊箱**；[S13795–13797](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L13795-L13797) 是史丹利第一人稱「I broke open」，本版不再畫成未有記載的共同動作。 |
| `s57139` | 老人與記者雙人交貨 → 一位老人拆開新給的布包；[L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804) 仍支持旁白的援助，畫面不要求模型演雙人接觸。 |

## 作者檢查與交審界線

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，159 句，估時 **13.797 分鐘**、開場 **00:45**。初稿 prompt 多用「lakeside」使畫面地點重複觸發警告；同一輪內換成具體湖岸措辭後重跑為零警告，最終 SHA 以表中版本為準。
- `npm run test:docs-videos`：**236 pass／0 fail**；`npm run check:tasks`：**exit 0，Validated 2384 task files**（僅列其他既有過期持有／範圍重疊警告）。
- R10 與 R11 的 `narrativeHash` 均為 `dcadd0471c15f9a2`；對 R11 prompt-only JSON 執行 `narrativeReviewMatches`，R10 [官方敘事紀錄](r10-merge/official-narrative-record.json)回 `true`。這只證明規則與逐字旁白的工具綁定未改，不是假裝 R11 有新的隔離盲讀。
- 八景的 **prompt 文字**尚待另一位未參與 R11 作者窄修的人獨立核對；R11 史料敘事是否可沿用前版，及書面畫面是否解除 HOLD，均由該非作者判定。原生 MiniMax 圖、語音、配樂、政策、組片及站主審核本輪未做，付費媒體仍停在畫面審查之前。
