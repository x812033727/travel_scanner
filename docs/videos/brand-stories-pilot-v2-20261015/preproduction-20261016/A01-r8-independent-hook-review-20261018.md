# A01 r6→r7→r8 獨立鉤子快審（2026-10-18）

狀態：**r8 增量審查未發現新的 P0／P1／P2；全稿與正式製作仍 HOLD。** 本文件只記錄這三輪離線候選的鉤子、敘事因果與畫面銜接快審，不是獨立事實審稿 PASS，也不是正式機的 `story/reviews/script-review.json` 收據。

## 凍結版本

| 候選 | `manifest.json` SHA-256 | 本次審查關係 |
| --- | --- | --- |
| r6 | `2022C21F9F2EF3E41A674E7E7C81568344427DC5A0AB413C6F97CA82A75FCC76` | 首輪快審，發現下述 P1 |
| r7 | `37B1FD3FB4E7C67A1DDE34D00A854D02A3E09B1DD2995D418B4EBCE1767A2A8B` | r6 P1 已解除；發現下述三項 P2 |
| r8 | `3475E820D22DF7F9D8FD850764D450F17630A2DCDD390949F9147D03062C42B8` | 只審 r7→r8 增量；三項 P2 已解除，增量未見 P0／P1／P2 |

## 問題與回讀

1. **r6 P1：兩份來源被剪出未證實的因果。** `now-packing-question` 在 1993 年《洛杉磯時報》記者把衣物與平裝書放入 Travelpro 外袋的個案前，問「箱子越好推，旅客會不會反而裝得更滿」，再用 2010 年一位空服員的觀察回收。記者只記錄自己那只箱子的機艙收納結果，沒有說她因為輪子好推才多裝。r7 刪除該預埋問句和過場畫面，在記者個案結束後以「多年後，一位受訪空服員觀察」另起來源；r8 保持該改法。來源：[1993 年記者實測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)、[2010 年空服員訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)。
2. **r7 P2：Shiller 與 Plath 的經歷容易被剪成一條傳承。** Shiller 自用四腳輪拖帶箱晃擺後，原稿緊接「另一位決定動手的人，是……Plath」，容易讓觀眾推斷 Plath 在修 Shiller 那只箱子。r8 的 `turn-04` 改成「Shiller 說的是他自己的拖帶箱。接下來……Plath，碰上另一種行李難題」，t4 主張列補上不同實物與影響關係未證的限制。來源：[Shiller 逐字稿](https://oyc.yale.edu/economics/econ-252-08/lecture-3)、[Travelpro 人物資料](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)。Emmer 未標年份的草圖回憶與 Plath 未標年份的安檢經歷仍不可排定先後。
3. **r7 P2：安檢口播與畫面不對位。** `turn-05` 口播說前方旅客的外置推車卡在安檢，原畫面只見 Plath 排隊。r8 畫面改為前方旅客開始解開彈力繩、準備卸下獨立金屬推車上的箱子，並明確禁止畫出後來的螺絲固定方案、安檢員答覆或通關結果。t5 主張列同步限縮至這次回憶。來源：[Plath 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)。
4. **r7 P2：1928→1939 回路說明過期。** `r17h01 → r3o01` 的 `what` 仍寫「父親嘲笑後」，但父親反應已移出開場。r8 改成「旅後是否仍帶輪箱；1939 年一場茶會報導記她身旁有輪箱」。這僅證一場出席，不能識別為 1928 年同一只實物，也不能推論逐年持續使用；1939 年原報的全文與影像未在本次快審重新核對。

## 實際核對範圍

- 以 SHA-256 核對三輪 `manifest.json`；逐一執行 r6、r7、r8 的 `build.mjs --check`，均退出 0。建置檢查是離線機械檢查，不能代替聽眾或主機審查。
- 讀取三輪 `README.md`、`candidate/script.md`、`candidate/video.json`、`candidate/claims.md`、`source-map.json` 與 `validation.json`；比對 r7→r8 的口播、提示詞、主張列及回路說明。
- 對 r7 與 r8 的 `video.json` 逐場、逐回路做 JSON 正規化後 SHA-256 比對：67 場中 65 場相同，僅 `turn-04` 口播與 `turn-05` 畫面不同；10 組回路中 9 組相同，僅首組 `what` 不同；其餘頂層欄位相同。`series.json` 的實檔 SHA-256 均為 `abeb7a283809a696c7ab8734ffa10ec83ec5494b7cf99584497e4e9cb3f2cafc`；`lexicon.json` 均為 `fce7f8651bf3614864999cfa22233376d90bf73d7e4caa37cb57d6345b2e7627`。`script.md` 只有對應口播及衍生末尾雜湊變化；`claims.md` 只有 t4／t5 兩列變化。
- 直接核對上述可開啟的 Sadow、Plath、1993 記者、Shiller、Travelpro 與 Sadow 專利頁面。其他既有主張的所有原始來源未逐一重驗；1939 原報與 Emmer PDF 未在這次快審完成全文獨立重驗。

## r8 仍未通過的關卡

r8 有 67 鏡、78 句、71 個主張、10 組登錄回路、1,860 口語單位。250／275／300 單位每分鐘的**文字估計**分別為 518.5／478.2／443.1 秒；即使按 250 估，仍比正式 540 秒下限少 21.5 秒。`duration_540_gate=HOLD`。300 單位每分鐘估計下，宣告回路問句最長空檔 240.1 秒、全部口播問句最長空檔 131.7 秒；來源事件代理最長 40.4 秒，但它只是選取事件的未審文字代理，`source_event_45_second_gate=UNREVIEWED_PROXY_ONLY`，`strict_45_second_gate=HOLD`。10 組登錄回路含短轉折，不能當作八組有效長鉤或留存效果已通過。

獨立完整事實審查、成片畫面審查、實際 TTS 時長與盲聽都未執行；正式機六章資料銜接與審稿收據未完成。r8 驗證表記錄 `independent_fact_review`／`independent_listener_review`／`independent_visual_review=NOT_RUN`、`script_review_receipt=NOT_ISSUED`、`actual_tts_or_media=NOT_RUN`、`production_or_paid_work=NOT_RUN`。本次沒有正式機寫入、匯入、媒體生成或付費呼叫。
