# S50 R2 隔離旁白雙盲：正式敘事 FAIL

2026-10-20 UTC。兩位不同讀者各只收到相同的繁中旁白和固定 13 題，未讀企劃、來源、主張、畫面、舊評或彼此答案。輸入由 `node tools/video/cli.mjs narrative --slug curio-s50 --json` 產生；保存的 payload 與目前 CLI 輸出**逐位元組相同**，SHA-256 為 `5fabb78e84a137064916b175771586145ea08b51bed5e8200fe20de51a64688a`。題規 SHA-256 為 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

| 固定 R2 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `99840a8e85b464e695fce17e57ac8a109f8aec793c803ea7ae59dc46b0f309e6` |
| `research.md` | `109557d74963733a6b8b3715739d49ec1d68648f5f34a7c9e10d52a9f940e6c7` |
| `claims.md` | `bb93edb6455fc520291dc12fca380afcfdd2cf96a0b721eead8f9966868311bf` |
| `video.json` | `e6a88bad3361fbac91f715eb2d1ac9d580c9920a8ebd82840b6429124ed4b69a` |
| `script.md` | `4844bc20450470bd32e3bb7027c6105f16058e36bb7757b39030ebeb50edab9e` |

原始答案保留為 [A JSON](r2-official-panel-a.json)（SHA-256 `c6a862e50b624602768613441ae29e85856fb9224270b18cd1ec31fa5d650728`）和 [B JSON](r2-official-panel-b.json)（`3b8afe78348f5c5c3ce5f25625c0ebf28fdb35b05e33dc4311d62eeb67edc4e7`）。兩份分別經 `panelVerdict`，再經 `mergePanelVerdicts`；[完整合併 JSON](r2-official-panel-merged.json) SHA-256 為 `17a58d0cc57dc3fcede0486713c027127b3b8ae181e5cad095ed2802456437b4`。

兩位各答 **8／13 Yes**，**13 題完全一致，0 題分歧**。共同 No 是五道必答題：`no_spoiler`、`one_line`、`chapters_link`、`payoffs`、`no_recap`。依固定合併規則，必答題兩人都答 No 即失敗；本輪**合併 FAIL**，不是進入網站劇本關卡的版本。

| 共同失敗題 | 讀者指出的原句與修稿方向 |
| --- | --- |
| `no_spoiler` | `[fire008]` 在開場先給出後章 `[fire079]` 的 13,200 棟統計；`[fire003–004]` 也提前交代屋主後來的證詞。開場應停在結果之前。 |
| `one_line` | `[fire003]` 先跳到數月後的證詞，再由 `[fire009]` 返回大火初期；B 另指出 `[fire009]` 的 1667 年刊本與 `[fire020]` 的 1666 年九月二日經歷倒序。需維持一條依發生或查出順序推進的線。 |
| `chapters_link` | `[fire104]` 已說議會未作判斷，下一章首句 `[fire105]` 只重述同一結論。讓新章首句帶來前章疑問的下一個動作或新答案。 |
| `payoffs` | A 指出 `[fire014]` 問聖馬格努斯教堂能否擋火，後文未明說它的結果；B 指出 `[fire002]` 問第一團火碰到什麼，而 `[fire114]` 只說烤爐是否點火無定論。掛出的問題須有文本能交付的清楚新答案，或把問法收窄到證據能回答的事。 |
| `no_recap` | A 指出 `[fire008]` 與 `[fire079]` 重複 13,200 棟，沒有明確回呼；B 指出 `[fire018]`、`[fire101]`、`[fire114]`、`[fire999a]` 多次重述點火目擊／火星未證實。刪重述或改為明確回呼並補新事實。 |

本判定只涵蓋上述精確 R2 旁白的故事結構。[獨立原文與書面畫面覆核](r2-source-independent.md)另有其限定的 PASS，Gazette 與 London Museum 的官網直接核驗仍待完成。R3 應修稿、重新凍結雜湊，再交兩位新隔離讀者；網站核准、TTS、圖像、配樂、成片及 Studio 關卡均未在本輪執行。
