# S49 R14 isolated official narrative merge

Script SHA-256: `0903ccc03e433c44d7f41f9ebf2325a6c051d7be50622bba5209a87d1802d2e1`.
Sources: `r14-isolated-blind-a.json` and `r14-isolated-blind-b.json`; their file hashes are recorded in `r14-isolated-official-merge.json`.
Rule: a question passes when **either** frozen reader answers yes. Reader B’s citations were reformatted as bracketed narration IDs for the CLI parser; its original review was not changed.

| Question | Reader A | Reader B | Merged |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | Yes | Yes | Yes |
| `one_line` | Yes | Yes | Yes |
| `no_toc` | Yes | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | Yes | Yes | Yes |
| `no_recap` | No | No | **No** |
| `chapters_are_events` | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | No | Yes | Yes |

**Official result: HOLD on `no_recap` only.** Both readers marked it no. Reader A cited `moon064`「畫面越來越像地球；但所有景色只在文章的文字裡。」 and `moon070`「每多一個局部特徵，讀者離真正的觀測證據卻沒有更近。」 Reader B cited `moon082`「牠們收起翅膀、直立走路，文中的觀測者才說像人。」 and `moon083`「先說遠處不像鳥，拉近才像人；它還能看得多清楚？」

The readers differed on `no_detour`. Reader A saw the press responses as a list, including `moon112`「不是。先前那本重印書收的《費城詢問報》摘錄說，是真是假，讓讀者自己判斷。」 Reader B marked yes because `moon108`「它先轉去土星」 leads to `moon109`「它不只一次把未知變成肯定句，還讓肯定句帶上精確數字。」 and the press section answers the opening editor question. The stated OR rule therefore marks `no_detour` yes.

CLI command and raw output are in `r14-isolated-official-cli.txt`; the exact CLI verdict is in `r14-isolated-official-cli.json`. The CLI exited 1 because its required `no_recap` answer is no. Its archived verdict has 13 answers, `passed: false`, and `failed: ["no_recap"]`.
