# S61 isolated blind narrative ballot A, round 2

First-time viewer judgment. Source material: `brief.md`, `script.md`, `video.json`, and the official `narrative --slug curio-s61 --json` narration and questions only. Yes: **6/13**; no: **7/13**. The official `narrative --answers` check exited **1** (`passed: false`): six required no answers and one advisory no answer. The exact CLI input is `r2-isolated-blind-a.answers.json`. The stdout verdict is `r2-isolated-blind-a.receipt.json`; the official workdir record with creative binding is `r2-isolated-blind-a.official-narrative.json`. The check used private workdir `/tmp/s61-r2-blind-a`.

Script SHA-256: `1f55c9182b1aac974cecea31d7755b1c310da29db651a6993aa310da9bb63fc9`
Video SHA-256: `800a8c7476bee77fad9b97e8a23e5b7e26007cfcf32e5ee471db371257fec134`

| Official question | Answer | Evidence and reason |
| --- | --- | --- |
| `scene_first` | Yes | [s61001]「一九一七年十二月六日，哈利法克斯的街上，剛經歷一場巨響。」[s61002]「可不到一小時，又有人喊：還有第二次爆炸。」The first four lines put a warning by people on a dated street. |
| `no_spoiler` | Yes | [s61007]「火勢真的朝火藥庫去，還是街上的人只聽見傳言？」[s61010]「第二次巨響最後有沒有來？先回到港口那一撞。」The opener leaves both the threat and the outcome unresolved. |
| `one_line` | Yes | [s61010]「第二次巨響最後有沒有來？先回到港口那一撞。」[s61025]「蒙布朗號起火約二十分鐘後，港口突然傳來巨響。」[s61040]「普林斯說，爆炸還不到一小時，火藥庫的消息已傳開。」After its declared opening flashback, the events move from collision and first blast to warning, response, and aftermath. |
| `no_toc` | **No** | [s61056]「要看清楚，得把警報、行動和結果拆成三張紙。」[s61057]「第一張是警報：普林斯說，當時有人擔心火燒近火藥庫。」[s61058]「第二張是行動：他寫，一整支砲兵隊自願去灌水。」[s61059]「第三張是結果：第二次爆炸沒有發生。」This explicitly announces and numbers the coming explanation. |
| `chapters_link` | **No** | [s61024]「如果第一次危險沒說清，第二次傳來時誰敢不跑？」is followed by [s61025]「蒙布朗號起火約二十分鐘後，港口突然傳來巨響。」The new chapter goes back to the first blast instead of answering the previous chapter's question about reaction to the second warning. Also [s61056]「要看清楚，得把警報、行動和結果拆成三張紙。」to [s61057]「第一張是警報…」is a structural label, not an event consequence. |
| `open_loops` | Yes | [s61016]「兩艘船必須在同一處狹口會過；哪一個動作出錯了？」[s61039]「被警告的是什麼，離火究竟有多近？」[s61053]「更要緊的是，第二次究竟沒發生，還是我們漏看了？」[s61084]「可是空地上的人，今夜能住哪裡？」Unanswered questions recur well within 90 seconds across the body. |
| `payoffs` | **No** | [s61007]「火勢真的朝火藥庫去，還是街上的人只聽見傳言？」receives [s61057]「普林斯說，當時有人擔心火燒近火藥庫。」and [s61062]「所以不能補出誰下令、哪個閥門開了、火離庫有幾步。」The script never resolves whether fire actually reached or approached the magazine; it only confirms reported concern and an unknown distance. [s61030]「少了領隊，誰來分工？」also gets only [s61067]「現場指揮卻重新接起來」without identifying who took over. |
| `no_recap` | **No** | [s61059]「第三張是結果：第二次爆炸沒有發生。」repeats later as [s61097]「最後，第二次爆炸沒有在哈利法克斯發生。」The water explanation also repeats from [s61060]「普林斯把這個結果，歸給砲兵隊的處置。」to [s61098]「普林斯把這點歸於砲兵隊灌水，而不是命運忽然放過。」Neither is an explicit callback. |
| `chapters_are_events` | **No** | The chapter titled 「戰時港口的兩艘船」 names a setting and subjects, while [s61011]「這座港口在戰時忙著運補，軍需船和民用船交錯進出。」opens with background. It does not name an occurrence or reveal. |
| `outro_no_next` | Yes | [s61997]「第二次爆炸是零次；普林斯把結果歸給火藥庫灌水。」[s61998]「如果你當時在街上，會先往空地走，還是留下幫忙？」[s61999]「想聽有出處、不把警報說成結果的歷史故事，訂閱奇聞檔案局。」The complete spoken outro has no next-video promise. |
| `opening_hooks` | Yes | After the street moment, [s61006]「第一次到底怎麼炸的，才讓第二個警報聽來可信？」[s61007]「火勢真的朝火藥庫去，還是街上的人只聽見傳言？」[s61009]「一條是人群如何逃，另一條是有人怎麼處理火藥庫。」[s61010]「第二次巨響最後有沒有來？先回到港口那一撞。」These set at least three distinct later reveals without their outcomes. |
| `one_thread` | **No** | The opening problem is [s61010]「第二次巨響最後有沒有來？」; it is answered at [s61059]「第二次爆炸沒有發生。」The subsequent chapters switch to new problems: [s61074]「消息卻仍需要一條能出城的線。」and [s61084]「可是空地上的人，今夜能住哪裡？」Those logistics do not advance the answered explosion question. |
| `no_detour` | **No** | The principal answer arrives at [s61059]「第三張是結果：第二次爆炸沒有發生。」The extended later section moves through [s61075]「電報公司恢復一條外線。」[s61080]「四小時內，一列醫療列車載著傷者往特魯羅去。」and [s61085]「軍方開始在公地搭起白色帳棚，先給人遮蔽。」These are worthwhile aftermath, but as whole passages they do not resolve why the second warning arose or whether the magazine exploded. |

The main narrative failures are the numbered three-card explanation, two chapter transitions that do not advance the preceding question, unresolved questions about actual fire proximity and replacement command, repeated outcome and water attribution, a setting chapter title, and the sustained relief-logistics turn after the main answer.
