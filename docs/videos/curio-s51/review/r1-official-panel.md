# S51 R1｜隔離旁白雙盲：敘事 FAIL

2026-10-20 UTC。A、B 兩位讀者各只讀相同的繁中旁白與固定 13 題，彼此隔離，未讀企劃、來源、畫面或對方答案。[原始 payload](r1-official-panel-payload.json)、[A 原始回答](r1-official-panel-a.json)、[B 原始回答](r1-official-panel-b.json)均逐位元封存。[完整合併 JSON](r1-official-panel-merged.json)由 `panelVerdict` 分別判讀兩份原答，再由 `mergePanelVerdicts` 合併，保留每題證據及兩人的原判。封存時 payload 與 `node tools/video/cli.mjs narrative --slug curio-s51 --json` 輸出逐位元相同。

| 固定 R1 輸入或產物 | SHA-256 |
| --- | --- |
| `brief.md` | `82a2e4a3d7a240dd0f249eeeec3b3dffdf1446d9eb049432320e72fe6b6a1023` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `21dd50280e0d89ca998a9cf5a0820589b6ae5ffbf233e49ba988aa6dd477dad1` |
| `script.md` | `5b6c6d0924670033b379c40a00f4ae3991d920661a5479631e5ba2e3143de42b` |
| `video.json` | `1639fd758d59f44b7dbae66603f1148c3abf7dd6229f16b32b3c5b34bdcf20df` |
| 盲讀 payload JSON／CLI 輸出 | `ed6b7a83a77dfdfcffc08fbbf4067bb889e0e642855f093dcdf451486c525bd1` |
| 固定題目與判分規則 | `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75` |
| A 原始回答 JSON | `f39322b7b8095908768a574d94bc9ff90e41077f984bbead8c59336d4c633bff` |
| B 原始回答 JSON | `9d19f1ec87499f8eb2b5d279bb9ff5a6a11a8cc170ab4d4ec38aad2df490dd6e` |
| 合併結果 JSON | `cd5b27584a307aaa44004b543cd1c967017fb4425add16867ff340aa76ab80a4` |

A、B **各 10／13 Yes**，13 題判斷完全一致，**0 題分歧**。兩人共同答 No 的三題都屬必答題；依固定合併規則，三題仍為 No，R1 **敘事 FAIL**。

| 共同 No | 兩人原答所指的問題 |
| --- | --- |
| `chapters_link` | A、B 都指出 `[cal092]` 問能否斷言船長當夜明知船名，下一章首句 `[cal093]` 卻直接報鐵達尼號沉沒，未接住船長認知的疑問。 |
| `payoffs` | A 指 `[cal083]` 問船長是否收到新的火箭總數；`[cal088]` 是吉布森稱已轉告，`[cal090]`、`[cal091]` 又載船長無此記憶、證詞互相矛盾，沒有清楚答案。B 指 `[cal075]` 問多枚火箭是否仍能當普通船燈；`[cal076]`、`[cal077]` 轉答首次回報五枚，沒有清楚回收前一問。 |
| `no_recap` | A 指 `[cal033]` 與 `[cal060]` 重述只有一名無線電員，未點名回呼。B 指 `[cal084]`、`[cal088]`、`[cal111]` 多次說八枚火箭，沒有符合題規的明確回呼。 |

[R1 獨立史料與書面畫面覆核](r1-source-independent.md)另判**旁白史料 PASS、書面畫面 HOLD**；書面提示詞的夜景時段與調查場景仍須修正。若 R2 只改提示詞，且 CLI 產生的旁白／13 題 payload 與本次封存逐位元相同，本敘事 FAIL 仍適用於相同口播；提示詞修正本身不會回收上述三題。更動口播後須重新凍結輸入，交兩名新隔離讀者。網站審核、TTS、圖像、配樂及成片不在本次覆核範圍，也未由此判定放行。
