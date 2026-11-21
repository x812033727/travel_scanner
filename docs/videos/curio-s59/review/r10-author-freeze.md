# S59 R10｜杜蒙塞爾來源歸屬窄修，作者凍結

2026-10-21 UTC。**作者預檢完成，待全新獨立來源差分覆核及兩位隔離敘事盲讀；付費媒體 HOLD。** [R9 正式合票](r9-merge-policy/summary.md)敘事固定 OR 已 13／13 PASS，但獨立史料覆核認為 s59058 明說愛迪生晚年回憶，緊接著 s59059 改述杜蒙塞爾同代觀察而沒在口播轉換來源，觀眾可能誤歸愛迪生。R10 只改這一句。

| 凍結創作檔 | R10 SHA-256 |
| --- | --- |
| research.md | 39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d |
| brief.md | 9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3 |
| claims.md | 5f3066ba0baaaf78404600f38e5e9eda4a93c2eece14bbc296eff274dc618cb7 |
| video.json | 70487214ddbb2cc45f4af58d28ab894de9235ab811c4250b5bf16dbd638f5ffa |
| script.md | 94acc30b9822e77e26dae56625b179ec17e8af8ce3879d8b35289a3c60824b42 |

[結構化差分](r10-author-structured-diff.json) SHA-256 1ee06f645f8a6939e7b8f9e9bacde3dba1fffe9cf9b366ee63515bfbd5e8b247。只改 video.json 的 s59059 台詞葉節點與 claims.md 同行台詞；逆換後 R9 的 video、claims 和工具生成 script 原始 SHA 全部精確復原。research、brief、所有提示詞、卡片及其他 JSON 欄位不變。visualHash 仍是 3e39a4b9868072e1；narrativeHash 從 2b1c46b809933014 改為 2dcbf2d4ae93d84b。

s59059 現以「杜蒙塞爾說」明白換回 1878 年來源，再說錫箔痕多播變淺、可重聽但漸糊，並把手搖難題接到下一句；來源是 [D6955–6976](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6955-L6976)。它沒有宣稱巴黎初試因箔磨損或手搖速度而失敗。短寫「箔痕」只是為了在同一句容納歸屬與直接回收；所有圖畫提示詞未變，仍須獨立畫面覆核。

script CLI 重生 script.md，110 句、100 張 shot、10 張 big、12 組伏筆；正文扣除開場九句與末兩句為 2,627 漢字，按每分鐘 325 漢字最快估算 8.08 分鐘，全片工具估 13.37 分鐘。lint 0 error／0 warning，docs-video tests 236／236，check:tasks exit 0（既存長期認領警告）。這些是作者與形式檢查；R9 敘事及史料收據對 R10 失效，必須有新版本綁定票。沒有付費呼叫。
