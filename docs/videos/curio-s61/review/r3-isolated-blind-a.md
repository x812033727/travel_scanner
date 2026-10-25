# S61 R3｜獨立盲讀 A

2026-10-22 UTC。以 R3 凍結旁白作第一次閱讀；不參考另一名 R3 讀者的票，也不改作者稿。正式敘事題目逐項作答於 [r3-isolated-blind-a.answers.json](r3-isolated-blind-a.answers.json)。這是敘事讀者判斷，不替代史料或畫面覆核。

固定 `video.json` SHA-256 `12820d44f6a213eaa0a312721d16b645807bbe0f0b8fd20ac5fba3b56ef36cdf`，`script.md` SHA-256 `6cf2fce1d864a772f8e5e456cc55f63d2fc3a160ba9e4198d98617289eb8d6a9`，均與作者交接一致。正式敘事 binding：`narrative_hash=37036a89d50524ec`、`script_hash=adf991bb8e45b7bbf85545927e3e90f7ef9b587a66329a10ef393c11d5eca318`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、`panel_narration_sha256=a22e52e204f3ecf871fa500a5a5bfe9ae0afa7ad7f5ac1e54e3d6cc8415dfe9b`。

| 正式題目 | A 票 | 依據 |
| --- | --- | --- |
| `scene_first` | Yes | [s61001] 直接把觀眾放在 1917 年 12 月 6 日哈利法克斯巨響後的街上。 |
| `no_spoiler` | Yes | [s61007] 仍問火是否接近火藥庫；首章不交代第二次爆炸的結果。 |
| `one_line` | Yes | 開場短暫預告後，從 [s61010] 船隻進狹口，順序推至 [s61040] 火勢逼近庫房、[s61066] 警報解除與之後搜救；沒有把完整一段重新講一次。 |
| `no_toc` | Yes | [s61024] 以燃燒貨船會把甚麼推上街頭的故事問題帶到首爆；各段未以章節、編號、紙張或待講清單宣告影片結構。[s61069] 提及軍方、教堂與鄰居是事件中的援助者，沒有列出影片章節。 |
| `chapters_link` | **No** | [s61010] 已說兩艘船正擠進狹口；下一章首句 [s61011] 只把同兩艘船的狹口說成「戰時船隻繁忙的狹口」。它補背景但未讓剛留下的船隻動作或「第一次怎麼炸」往前走。其他章首的連結較具體，例如 [s61039] 的庫房問題由 [s61040] 回答。 |
| `open_loops` | Yes | [s61039] 庫房是否真的受威脅；後面又有 [s61053] 誰處理庫房、[s61065] 何時傳來解除消息、[s61080] 今晚住哪裡，無超過 90 秒的無懸念長段。 |
| `payoffs` | Yes | 例如 [s61030] 問消防少了領隊由 [s61060] 點名回呼並回答「一名市政官員」；[s61039] 由 [s61040] 回答；[s61095] 由 [s61097] 明確揭曉。 |
| `no_recap` | **No** | [s61089] 開句已說「接連的冬季風雪到了」；緊接 [s61090] 再說「風雪到了」。這是同一事實立即重述，沒有點名回呼。另 [s61058] 的「誰下令／從哪裡取水未詳」又在 [s61099] 被重說。 |
| `chapters_are_events` | Yes | 章題以相撞、爆炸、帶人撤離、灌水、分區搜尋、風雪逼人入內等發生的事命名；[s61057] 是灌水動作，不是「證據分析」等功能段。 |
| `outro_no_next` | Yes | [s61997]–[s61999] 只收束當天選擇、提問和訂閱；沒有下一支片的預告。 |
| `opening_hooks` | Yes | 第一個街頭時刻後，[s61006] 留首爆成因、[s61007] 留火勢與庫房的真相、[s61010] 留兩船相撞的前因；[s61004] 也留誰接應傷者。 |
| `one_thread` | Yes | [s61004] 的撤離者會否得到接應，後由 [s61081] 白帳棚接上；警報、留守、回城與收容沿同一場事故的後果推進，庫房結局留到片末。 |
| `no_detour` | Yes | [s61070] 警報解除後搜救接續；[s61081] 將公地上撤離的人接進白帳棚，回收開場的「有人接應嗎」，不是另一件獨立歷史事件。 |

結果 **11/13 Yes**；必修 `chapters_link`、`no_recap` 為 No，正式單人判定 **FAIL**。CLI `narrative --slug curio-s61 --answers ... --workdir /tmp/s61-r3-blind-a --json` 退出碼 1；完整機器結果見 [stdout](r3-isolated-blind-a.stdout.json)，綁定檔見 [official-narrative](r3-isolated-blind-a.official-narrative.json)，stderr 為空。雙人合併仍須由主持者核對兩張票及相同創意雜湊後執行。
