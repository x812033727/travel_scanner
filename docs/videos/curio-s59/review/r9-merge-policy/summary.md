# S59 R9｜雙盲敘事正式合票與來源關卡

2026-10-21 UTC。**敘事固定 OR 13／13 PASS；事實、逐句引註及書面畫面 PASS；口播來源層級 s59059 窄幅 HOLD，因此付費媒體仍暫停。**本結論只適用於 R9 凍結的五檔，不沿用其他版本的票。

| R9 凍結檔 | SHA-256 |
| --- | --- |
| research.md | 39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d |
| brief.md | 9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3 |
| claims.md | 54e6c2f1d8fb533161ed48980ef1043faf6716c70999576507de9d6a735da747 |
| video.json | a0f986b5f1f578f6170b62ad24e17775b87ef4d3eb463104de9975a84928e4e6 |
| script.md | 6c28555d04104c676f76414479f038f426893f940a183e2518e3e9abac22cc09 |

兩位全新隔離讀者只看劇本與固定十三題，分別封存 [A 原票](raw-ballot-a.json)、[B 原票](raw-ballot-b.json)、[A 評語](raw-review-a.md)、[B 評語](raw-review-b.md)及各自的官方 CLI 收據和原始輸出。A 為 12 YES，唯一 NO 是 no_detour，指 s59062–64 的鐘錶二重唱比較；B 為 13 YES。固定 OR 使十三題全部通過，包含 R8 共同失敗的 payoffs。見 [合票稽核](merge-audit.json)。

[正式合票程式](formal-merge.mjs)在合票前後核五檔 SHA，核兩張原票、評語及個別官方 CLI 輸出的 SHA、十三題順序、每則引句與口播逐字相符，以及相同的 panel 規則與劇本綁定。它用 [合併答票](merged-answers.json)獨立執行官方 narrative CLI；結束碼 0、passed:true、failed:[]、13 題與 13 YES 一致。[原始 stdout](cli-stdout.json)、[stderr](cli-stderr.txt)、[退出碼](cli-exit-code.txt)、[正式紀錄](official-narrative-record.json)和[執行狀態](cli-status.json)均已封存。

[R9 獨立史料與書面畫面覆核](../r9-source-independent.md) SHA-256 為 20a0f368a288743f82d49ac6ade58771dd44e2d34207e591ab417e86b5a0ffee。110 句的史實與 124 個引註實例、100 張書面分鏡及 10 張卡片均 PASS，但 s59058 明說是愛迪生晚年回憶，下一句 s59059 換講杜蒙塞爾的 1878 年箔磨損與手搖觀察，沒有在口播重新點名來源。聽者可能把這段同代觀察誤歸愛迪生，因此**來源層級 HOLD**；逐句表引註正確不能替代觀眾聽到的歸屬。R10 只需在 s59059 補上短的杜蒙塞爾歸屬，重凍結並由獨立工作者核差分與故事；R9 敘事 PASS 不能移作改稿後核准。

[政策關卡](policy-gate.json)因口播來源未過仍為 HOLD。沒有站主畫面卡審核或付費媒體呼叫。
