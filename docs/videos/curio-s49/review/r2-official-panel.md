# S49 R2 隔離旁白雙盲：正式敘事 FAIL

2026-10-20。A、B 兩位讀者各只讀相同的繁中旁白及固定 13 題，彼此隔離；[原始題目與旁白](r2-official-panel-payload.json)、[A 原始回答](r2-official-panel-a.json)、[B 原始回答](r2-official-panel-b.json)均逐位元封存。[完整合併 JSON](r2-official-panel-merged.json)由 `tools/video/core/narrative.mjs` 的 `panelVerdict` 及 `mergePanelVerdicts` 產生，保留每題、兩人證據和分歧；未改寫任一人的答案。封存 payload 與當前 `video.json` 的 CLI 輸出逐位元相同。

| 精確輸入或產物 | SHA-256 |
| --- | --- |
| 盲讀 payload JSON | `c8498a352e93dee56842093c941bd3fba35e0000a0bf3ea96fd11ae059cc9eb9` |
| payload 中的旁白文字 | `589e4da13324fafd11c44421c0d5d519570bbc59e76c23a8470c3d864afa900e` |
| 固定 13 題與判分規則 `PANEL_RULES_SHA256` | `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75` |
| A 原始回答 JSON | `900a3e89e7339a13b704456aa73d1a789720a8ef11831a2529c0642b00e9e7d7` |
| B 原始回答 JSON | `c5fb11d8b0ad65b351a4a491f67a4519bfd50b1cb7d720de8af39aafd06cbab1` |
| 合併結果 JSON | `a5a3bab1b729ce023e6c0e6bb172d3e654746c63846ae1d3b0ab45411ccc69f3` |
| `brief.md` | `48c3dc196b668c3ce3d58b4b3ffc26973262eb450587abfcc39d10d421057568` |
| `research.md` | `9476f53555e51da2471a72f75249e7e5fc8ed4ce3e30627578ce86cf4198c327` |
| `claims.md` | `2fcbd24ed8bbd6c6bb77d62194e81c4bc2ff4611e6aa0f8269f8a7c090e42a2d` |
| `script.md` | `ee25ba5be03898a2bfa5a6523e7fbb5bdc6000088aa91fd1eab0615a2ca84624` |
| `video.json` | `c1a298292932ba96d4b9def21a4e421426397166ea27d4597727b7cab48ee543` |
| Locke 1859 固定全文 `/tmp/s49-moon-hoax-62779.txt` | `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` |
| Jacoby 1902 固定全文 `/tmp/s49-jacoby-53396.txt` | `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` |

`narrative_hash` 為 `a17306f19b1e97df`，`script_hash` 為 `b498418230250f1484494c6a8a3129e94fefd87add259c116cd08f40c1e0fa5e`。A 判 **9／13 Yes**，B 判 **11／13 Yes**；依固定合併規則，同題兩人都答 No 才失敗，合併 **11／13 Yes、FAIL**。共同失敗均為必答題：

| 共同 No | 兩人的具體依據與下一輪修稿方向 |
| --- | --- |
| `payoffs` | A、B 都指出 `[moon098]` 問「讀者會不會要求真正的驗證？」，`[moon099]` 卻轉成報導安排觀測意外；後面的報紙反應也沒有明說讀者是否要求驗證。把問句收窄到後文能回答的報導動作，或補上有來源的讀者行為與明確回收。 |
| `no_recap` | A 指出 `[moon009]` 的赫歇爾真旅程在 `[moon129]` 再講一次；B 同時點出 `[moon010]`、`[moon052]`、`[moon129]` 反覆交代真實南天研究，沒有點名回呼。壓縮重述，讓收尾只給新的結論。 |

兩處**分歧**亦原樣保留：`one_line` 為 A No、B Yes；A 指 `[moon027]` 提到 1859 重印本後 `[moon031]` 回到報導敘事，B 認為全文沿同一篇報導的觀察順序推進。`no_toc` 為 A No、B Yes；A 把 `[moon055]`「它先讓讀者看地形」讀作講法預告，B 認為這是在描述報導內的事件順序。兩題依規則合併 Yes，不能把分歧寫成兩人一致。

[R2 獨立來源與書面畫面覆核](r2-source-independent.md)對上列五個交付檔的結論仍是固定來源事實 PASS、書面畫面 PASS；**敘事關卡 FAIL，現稿不放行 TTS、插圖、配樂或成片**。R3 若改動旁白，須重生 `script.md`、重核受影響的來源與書面畫面，然後以新精確 payload 請兩位全新隔離讀者重評；本站大綱／劇本與媒體關卡仍各自待處理。
