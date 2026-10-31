# S52 R12 雙盲敘事評分合併

稿件：`docs/videos/curio-s52/script.md`。合併前後的 SHA-256 均為 `b9bae5c830d5e1260c4a034318f8bcede8a9824affa482b24d50a0e4a032be99`。B 的 13 題判斷先凍結在 `r12-isolated-blind-b.json`（SHA-256 `dff21e78518da6984a849880971ee331b397ed4eb0da6c514d2001c0e13e8b6c`），之後才讀 A 的獨立結果。合併規則：每題任一讀者答「是」，合併即為「是」。合併答案在 `r12-merged-answers.json`。

| 題目 | A | B | 合併 |
| --- | --- | --- | --- |
| `scene_first` | 是 | 是 | 是 |
| `no_spoiler` | 是 | 是 | 是 |
| `one_line` | 是 | 是 | 是 |
| `no_toc` | 是 | 否 | 是 |
| `chapters_link` | 是 | 是 | 是 |
| `open_loops` | 是 | 是 | 是 |
| `payoffs` | 否 | 是 | 是 |
| `no_recap` | 否 | 否 | **否** |
| `chapters_are_events` | 是 | 是 | 是 |
| `outro_no_next` | 是 | 是 | 是 |
| `opening_hooks` | 是 | 是 | 是 |
| `one_thread` | 是 | 是 | 是 |
| `no_detour` | 是 | 否 | 是 |

用 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s52 --answers docs/videos/curio-s52/review/r12-merged-answers.json` 重跑，CLI 只報 `FAIL no_recap`，退出碼 1。正式判定為 **HOLD**；產生的評分記錄在 `/workspace/.video-work/curio-s52/review/narrative.json`，其中 `failed` 只有 `no_recap`。

## 最小修稿請求

兩位讀者在同一題找到了不同的重複，以下三處都須處理，再用新稿重新盲評：

1. s52308 已說「但雲擋住了；那次天象，他們沒能看見。」s52053 又說「四月的觀測曾被雲擋下；到了五月，儀器何時才安置好？」刪掉 s52053 的前半句，保留「到了五月，儀器何時才安置好？」作為章末問題。
2. s52094 已說「基皮斯把這四個接觸時刻，印成一張表。」s52116 又說「基皮斯只印一張四格表，真能算出三人相差幾秒嗎？」把 s52116 改成明確回呼，例如「還記得基皮斯那張表嗎？只靠它，真能算出三人相差幾秒嗎？」
3. s52316 再說「後出傳記那四格不是三人記錄的全貌」，重講 s52118 的結論；此句可只留下承接原報的新疑問，例如「原報中的『碰到』，究竟指哪一道邊？」這也移除 B 在 `no_toc` 指出的「先看」。

稿件尚未修改；本報告只記錄雙盲合併與修稿位置。
