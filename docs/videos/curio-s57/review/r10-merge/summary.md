# S57 R10｜兩份合格隔離原票的固定 OR 正式合併

2026-10-21 UTC。**正式敘事 PASS：13／13 YES；書面畫面仍 HOLD，不放行付費插圖。**本紀錄只合併在相同 R10 `script.md` SHA 上凍結的兩份全新盲讀原票，不改票、不改五份創作檔，也不採用已披露前輪資訊的補充閱讀。[獨立史料與書面畫面覆核](../r10-source-independent.md)的分項結論是**史料／逐句主張 PASS、書面畫面 HOLD**。敘事 PASS 不會覆蓋後者。

| 凍結創作檔 | R10 SHA-256（CLI 前後均相同） |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd` |
| `claims.md` | `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` |
| `video.json` | `0275fe764a2a79ee0d122780853bb3bfa21922c86a4f650475c7dc6c1fb39d2f` |
| `script.md` | `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` |

## 原票資格及轉錄

[A 原票](raw-ballot-a.md)從 `../r10-blind-a.md` 逐位元組複製，SHA-256 `363b3bd2668b6a91ce1642fafde6bf384aefb6f9d75a9744eb36d3b195b20822`；原票披露只讀本版 `script.md` 與固定 13 題，**12 YES／1 NO**，唯一 NO 為 `one_line`。 [B 原票](raw-ballot-b.md)從 `../r10-clean-blind-b.md` 逐位元組複製，SHA-256 `8a4f6a302b8fc0464eb0c38ba7aa2f13aa10f961f211ce11e262d518c557c7b1`；同樣披露只讀本版稿與 13 題，**12 YES／1 NO**，唯一 NO 為 `no_recap`。兩份 [A](ballot-a.json)／[B](ballot-b.json) 工具答案依各自表列票轉錄，每題的工具證據由原票理由點名的現版場景 ID 搭配 `video.json` **逐字旁白**；原理由、引用 ID、選取的有效 ID、原票 SHA 和轉錄規則均保留在[稽核檔](merge-audit.json)。

兩份原票的可修異議原樣保留：A 指 `s57063–s57068` 的勸歸在 `s57069,s57072–s57079` 又從日記說了一次，兼指出 Bennett 委派向前回跳，因此 `one_line` NO；B 指開場 `s57006/s57007` 的病痛／備貨在 `s57014/s57011` 重說但沒有點名回扣，因此 `no_recap` NO。這是**兩項不同的單票異議**，不能稱為兩位都認同沒有問題。B 原票另外把已不存在的 `s57082`（數處）與 `s57049`（一處）列在長串說明中；相關 YES 列均另有有效場景 ID，轉錄採原票中第一個有效 ID 並在稽核列出無效 ID，未新增理由或改票。兩份原票的選填 `chapters_are_events` 理由沒有逐字 ID；轉錄以其點名的〈蘇西跑來報信〉事件配 `s57036`，於稽核明列。選填列不影響必答閘門。

`../r10-supplemental-a.md` 與 `../r10-supplemental-b.md` 均自述曾讀到作者收據中的 R9 結果，**未納入**兩份合格隔離原票的固定 OR；它們的 NO 不得偷換成正式第三票。

## 固定 OR 與官方工具

在 panel 規則 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75` 下，依序以 `panelVerdict(A)`、`panelVerdict(B)` 和 `mergePanelVerdicts([A,B])` 執行固定 OR：同題任一讀者的帶 ID YES 即通過；全體 NO 才失敗。[完整合併 verdict](merged-verdict.json)保留兩名讀者逐題答案；[官方工具答案](merged-answers.json) SHA-256 `729dceae630ee9473b800c3a2b2cbf5a4db038fab7fb83fab268f313ed738544`。

| 13 題結果 | A | B | 固定 OR |
| --- | --- | --- | --- |
| `one_line` | NO | YES | YES，保留 A 異議 |
| `no_recap` | YES | NO | YES，保留 B 異議 |
| 其餘 11 題（含選填 `chapters_are_events`） | YES | YES | YES |

執行 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r10-merge/merged-answers.json --workdir /tmp/curio-s57-r10-formal-merge-20261021 --json`。官方 CLI **exit 0、`passed:true`、`failed:[]`、`advisory:[]`**；[原樣 stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[exit code](cli-exit-code.txt)、[前後 SHA、命令及工作目錄](cli-status.json)、[官方 narrative record](official-narrative-record.json)都已封存。官方 record SHA-256 `46ae72cfb6e0843567cf9e0c4b53b4aef5788fd8afc0371c72c1c030597e3754`。

**政策與媒體停點：**此處只判敘事；獨立 R10 書面畫面 HOLD 的八景 `s57114,s57117,s57118,s57120,s57122,s57133,s57135,s57139` 須另交作者窄修並對新 SHA 獨立複核。此正式合併沒有核准政策、站主審片、付費旁白、插圖、配樂、組片、上傳或發布。若 R11 只改這八景的 `data.prompt`、保持 R10 旁白與 script／panel 規則不變，敘事內容未被重寫；是否沿用本 R10 敘事票仍由後續版本閘門按其 hash binding 判斷，不能把本紀錄偽稱為 R11 新盲讀。
