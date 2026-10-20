# S40 R4 定點修訂：待全新獨立審核

2026-10-20。這是撰稿者按 **R3 獨立審核**完成的修訂紀錄，並非 R4 的盲讀、來源覆核或站主簽核。[R3 純劇本盲讀](verify-r3-blind.md)鎖定 `script.md` SHA-256 `b01c0ef524555d798efcb09b2503cffe0f10cdaee9a3bb9867b11a1b8540c1e7`，得 **12/13**；封存報告 SHA-256 `9332a96cdbdfd06ea6099ee6db8dccbe6974268b616809b34f2eca228e9fc992`。[R3 來源／畫面覆核](verify-r3-source-visual.md)報告 SHA-256 `1637e1311ff465fc06f6051080459267f719ae1a64c9326d8419f3deca2e33a3`，判旁白 **83/83**、prompt **83/83** 史料相容，窄引用 **80/83**，三筆須修。兩份原報告原樣留存。

## 修訂對照

| R3 審核點 | R4 定點處理 |
| --- | --- |
| `payoffs` 唯一未過：`cl012` 提女王要求王位留給孩子，後文卻無法交代是否准許 | `cl012` 改成她與使者隔門交談，問能否讓她親自開門；`cl013` 立即答「沒有」並轉向高窗。王位要求不是本集死因問題所需，也不能從本輪來源補出孩子最終是否保住王位，因此不再把它設成待回答的故事承諾。畫面仍是隔門談判，符合普魯塔克 L61448–60。 |
| `cl009` 的 `P-0` 起點 L61395 漏掉陵墓內財寶的位置 | [research.md](research.md) 的 `P-0` 及 [video.json](video.json) 的 Plutarch URL 起點延到固定全文 **L61323**；L61323–30 寫財寶移入陵墓，L61444–47 寫屋大維的顧慮。 |
| `cl029`、`cl030` 的 `P-a` 終點 L61575 漏掉准留財物和傳記評論 | `P-a` 終點延到固定全文 **L61580**；L61576–80 分別涵蓋准留財物、待遇承諾與作者所說屋大維受騙。未把作者的內心描寫升格為獨立目擊事實。 |

## R4 精確檔案與自查

| 檔案／輸出 | SHA-256 |
| --- | --- |
| [video.json](video.json) | `6550826de8efd242c65af210ec6b6687f1da329ffe9e28684714394a0baaf6d2` |
| [script.md](script.md) | `b255fb2ae6cefbed88b9913e1be046f5ffc0fd35cf1b94d06347460f96f7e7b3` |
| [claims.md](claims.md) | `ee568874c7b4198186e70eec5683a17a55f969cf657002b01360b8b5c258499c` |
| [research.md](research.md) | `8dc1ff645e20a4af8c75437d72444e4ee7665748e7b996c5dc462b9a8781f425` |
| `node tools/video/cli.mjs narrative --slug curio-s40 --json` 的本地 stdout | `5765e51d08c90d213c76aebc96b2342735ab4d511e8d309a178eb4c8b4afaf7e` |

- `node tools/video/cli.mjs lint --slug curio-s40 --json`：**0 errors、0 warnings**；84 句、83 張 `shot` 與 1 張 outro，估約 **9.26 分鐘**。純旁白時間碼 `cl006` 00:36 至 `cl084` 09:08，正文 **8 分 32 秒**；TTS 實際時長仍待重測。
- 機械核對：83 張 `shot` 各有 prompt，逐一對應 83 行 `claims.md` 的 ID 與完整旁白文字。25 組已宣告懸念的 payoff 都在 setup 後；相鄰新懸念最多相隔 **45 秒**。
- 三份固定古代全文的版本與檔案雜湊仍見 [research.md](research.md)；本輪僅延長已核過的同一 Plutarch 全文引用區間。沒有新的死法斷言，也沒有拍成蛇咬或髮針使用的確定現場。

**下一關**：對以上 R4 精確雜湊重新封存純劇本 13 題獨立盲讀，再獨立核對來源、主張指標與 83 個 still prompt。若改稿，這些雜湊和審核必須再刷新。尚未通過 R4 審核；未執行付費語音、插圖、配樂或上片。
