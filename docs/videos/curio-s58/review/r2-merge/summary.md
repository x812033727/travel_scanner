# S58 R2｜正式雙盲敘事 OR 合併診斷

2026-10-20 UTC。**敘事 HOLD：固定 OR 合併 8／13 YES，五個必答題未過。**這是兩位無前情讀者對下表精確 R2 劇本的正式敘事票合併；[同版獨立史料與書面畫面覆核](../r2-source-independent.md)也為 HOLD，兩關各有獨立理由。沒有改動 R2 五份創作檔或執行政策、語音、插圖、配樂、合成與其他付費媒體。

| R2 凍結創作檔 | SHA-256 |
| --- | --- |
| `research.md` | `8a1db1dc2a9441a7b16683c70067203ddc7be6c0070560f32c02d91b5e32de34` |
| `brief.md` | `7b44818f6b681a4ee786c00a32359b4181772aeaa1b5cd897bcd13871b1ad016` |
| `claims.md` | `73f9ea7122ec728357b7eb3c8487b9657b4bbe0e6d140c4b0514a7deddc2d471` |
| `video.json` | `d69ce07f441aeabddc231d4d98fe4437ffea4e7c763198d2a61be1161bebe0cb` |
| `script.md` | `9d590c8c3e6f93628d87d4618276ee967364aa36e0b54c7008c9266b6daae0ac` |

## 原票、OR 規則與官方回條

原始 [A 票](raw-ballot-a.md)與 [B 票](raw-ballot-b.md)逐字複製封存，SHA-256 分別為 `9ad26823d4360c49212f14d5b2f05c7ba7783269dd03ab6f893e43a209d29bc9`、`9ed2f8a7d5d2f35def56aedf04da388c9fdf1c02f4555c59d7c710e541ab18a4`，與原路徑 `../r2-blind-a.md`、`../r2-blind-b.md` 相同。A 是 **6 YES／7 NO**，B 是 **7 YES／6 NO**；兩票都明載只讀 R2 `script.md` 與官方 13 題。

[轉錄程式](build-merge.mjs)按原票順序和布林票轉為[官方形狀 A 答案](ballot-a.json)、[B 答案](ballot-b.json)，從固定 `video.json` 選取各原票理由所指的場景 ID 與逐字句作帶括號引用；對章名等非單句理由，引用相鄰代表句，保留原票理由全文於[稽核](merge-audit.json)。逐項以正式 `panelVerdict` 驗算，沒有改動任何一票的 YES／NO。[稽核](merge-audit.json) SHA-256 `8533b88c5738aa1318f9d628a412c25f43e27679d689980b4252047da99612a5`，保留原票雜湊、每題理由、引用、個別與合併結果。官方規則 `PANEL_RULES_SHA256` 是 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

以 `mergePanelVerdicts` 的固定 **OR** 規則合併：任一讀者有帶場景 ID 的 YES，該題為 YES；只有兩票都 NO 才未過。[合併答案](merged-answers.json) SHA-256 `a71a7c9fc5ef3a4091749bea1902a125c58588703f9b9726d4abb8074a080d67`。`no_toc` 是 A NO、B YES；`chapters_are_events` 是 A NO、B YES；`opening_hooks` 是 A YES、B NO。三項按 OR 均通過，單票異議完整留在原票與稽核，沒有寫成雙票一致。

五檔 SHA 在 CLI **之前及之後**都與上表一致。[CLI 執行回條](cli-status.json)記錄完整命令、隔離工作目錄、前後 SHA、原票與輸出雜湊。以 `node tools/video/cli.mjs narrative --slug curio-s58 --answers docs/videos/curio-s58/review/r2-merge/merged-answers.json --workdir /tmp/curio-s58-r2-merge-formal-XeYP5W --json` 執行正式關卡，**CLI exit 1、`passed:false`、五個 required fail、零 advisory fail**。保留[原樣 stdout](cli.stdout.json)（SHA-256 `827c1946c0d83f74115d529e3992c06ea0b2e85ebc760e9e67de7535d56908e2`）、[空 stderr](cli.stderr.txt)、[退出碼](cli.exit-code.txt)及[官方敘事紀錄](official-narrative-record.json)（SHA-256 `f471cfb7ef98fbd8b9731b7799fe6d28eefbba1f78afba18380fd41e53ee0fd4`）。官方紀錄 `round=1`、`narrative_hash=e41d386112b07a74`、`panel_narration_sha256=8b4882b3b38424be4992e08405f9e1ef9b40b6425221dbb9ecb466566a1a4289`。

## 五項雙票共同 NO

| 必答題 | 精確斷點與下一版修稿方向 |
| --- | --- |
| `no_spoiler` | 兩票均指開場 `s58005–s58007` 已交代另一球墜落、沙袋裂開與**用盤子倒沙的辦法**，後面 `s58041`、`s58047–s58048` 又才演一遍。開場若保留氣球場景，應停在這些結果之前。 |
| `one_line` | 兩票均指先講 11 月 12 日，同片正文再倒回 10 月 28 日，繼而重講 11 月的槍聲、墜球、沙袋與盤子。回到更早起點本身可行，問題是同一段 11 月事件在開場和正文各說了結果。 |
| `payoffs` | 兩票均指 `s58049` 問下面有沒有敵兵，`s58050` 只是再說團隊不知道，後文也沒正面回答；`s58139` 問嚴寒妨礙鳥飛怎麼辦，`s58140–s58141` 又重述限制。B 另指 `s58020` 問十月鳥能否送達，`s58027` 只承認沒看見收件人。下版應把無可查證答案的問句改為來源能回答的問題，或用有新資訊的答案回收。 |
| `no_recap` | 兩票均指 `s58005–s58007` 與 `s58041`、`s58047–s58048` 重報同一組墜球／沙袋／盤子事實；A 另指 `s58140–s58141` 與 `s58155` 的重述，B 另指 `s58147–s58148` 的材料到達及 `s58150–s58151` 的十二小時。下版不能只刪第一組而忽略其他單票指出的重複。 |
| `no_detour` | 兩票均指 `s58069–s58075` 的教士、留衣、郵務員與司機接力過長，減緩器材能否留下的主問題；B 另指 `s58105–s58108` 在已問如何送回巴黎後，又回到排頁、電文分類和匯票。須讓必要史實直接推進器材→薄膜→返城信息的因果鏈。 |

**執行註記：**正式 CLI 已完整執行並封存以上原樣檔案；外層歸檔程式的第一次結尾驗證把 `stdout.failed` 誤當字串陣列，因此封存後報錯。CLI 實際回傳的是含 `id` 的物件陣列。已修正[歸檔程式](run-cli.mjs)該驗證式，沒有重跑或覆蓋官方 CLI 紀錄；隨後對已封存檔獨立核對原票、合併答案、stdout、record 的 SHA 與五項失敗、空 advisory，全部一致。

**交接：**R2 的來源／書面畫面及正式敘事均 HOLD。CLI、雙票與前後 freeze 封存完成後，R3 作者才可修改創作檔。R3 須重新凍結五檔、重交非作者史料／書面畫面覆核及兩位新盲讀與正式合併；R2 不進政策或付費媒體關卡。
