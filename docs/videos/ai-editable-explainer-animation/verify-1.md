# verify-1.md：ai-editable-explainer-animation 事實查核（第 1 輪，2026-10-25）

## 結論

只改了一句旁白（005752），其餘事實都保留。

- **數學主張**：重新枚舉兩顆六面骰後全部成立。
- **Python itertools.product**：官方頁今日可讀，確認是笛卡兒積，等同巢狀迴圈。
- **Pillow ImageDraw**：官方頁今日可讀，確認可畫圖形與文字。
- **FFmpeg**：三個官方頁（documentation、ffmpeg、ffprobe）今日都回 HTTP 503。payload 裡也沒有 mokaair.com 的查證文章。所以片中與 FFmpeg 有關的內容只能保留不含數字的用途說明，目前就是這樣寫的。
- **終端機輸出**：解析度、幀率、秒數只出現在 run-render 的終端機輸出，屬於本次執行紀錄。claims.md 指向 lab/verification.json、render.log，但這兩個檔案不在 payload 裡，我無法逐字對照。這幾項保留，並列在最後一節，發佈前要人工核對。

## 逐條查核

| # | 主張 | 位置 | URL／證據 | 判定 | 修改前 → 修改後 |
|---|---|---|---|---|---|
| 1 | 兩顆公平骰子共有 36 種有序結果，分別放在橫軸與直軸 | brief-all 21c1bc；run-check 輸出 outcomes=36 | https://docs.python.org/3/library/itertools.html#itertools.product（product 是笛卡兒積）＋重新枚舉 6×6 | CONFIRMED | — |
| 2 | 1+6 與 6+1 分開算（有序） | brief-ordered 8f5f2e；brief-prompt-one 719e7c | 同上，product('ABCD', repeat=2) 的範例同時列出 AB 與 BA | CONFIRMED | — |
| 3 | 總和 7 有 6 格，機率 1/6 | hook-grid、build-seven；run-check 輸出 highlighted_count=6 probability=1/6；指令 --expect-count 6 | 枚舉：(1,6)(2,5)(3,4)(4,3)(5,2)(6,1)，6/36=1/6 | CONFIRMED | — |
| 4 | 總和 12 有 1 格 | build-twelve（grid-twelve.svg），c2 | 枚舉：只有 (6,6) | CONFIRMED | — |
| 5 | target_sum 改成 6 後有 5 格 | revise-config a1f88a；revise-six 05bc8a；revise-five f6f6be 與 numeral 5 | 枚舉：(1,5)(2,4)(3,3)(4,2)(5,1) | CONFIRMED | — |
| 6 | 不合法的目標（13）會說明原因並停止 | check-boundary 75368c，c6 | 兩顆骰子的總和最大是 12，所以 13 確實不可能。程式以 exit 1 結束的行為依 claims.md 所記 verification.json，原檔不在 payload | CONFIRMED（數學部分）；執行紀錄見最後一節 | — |
| 7 | 範例的 locale 只接受 zh-TW；樣片字幕是設計時間，未與旁白對齊 | build-local-language b13c3e、audio-sample ba0179、run-render 52cf29、description | claims.md c7（check_lesson.py、narration.json） | CONFIRMED（自家範例的限制，與 claims 一致） | — |
| 8 | 用繪圖套件（Pillow）畫圖與文字 | build-dependencies b22122、description | https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html：「provides simple 2D graphics」，另有 text() | CONFIRMED | — |
| 9 | 用影片工具（FFmpeg）把影格接成影片 | b22122、a2d3d8、description | https://ffmpeg.org/documentation.html、https://www.ffmpeg.org/ffmpeg.html、https://www.ffmpeg.org/ffprobe.html 皆 HTTP 503；沒有 Mokaair 文章 | CONFIRMED（只是描述用途，沒有數字；說法依本次執行紀錄） | — |
| 10 | 樣片 1280x720、24fps、54 秒、無音訊 | run-render 終端機輸出；description 寫「範例 MP4 刻意無聲」 | 執行紀錄 render.log／verification.json（claims c4），ffprobe 官方頁 503 | CONFIRMED（終端機逐字執行紀錄，ran_on 2026-10-25）；原檔未附，見最後一節 | — |
| 11 | Python 3.12.14 | run-check、run-render 的 tool_version | claims c5 記錄的本次環境；官方 itertools 頁是 3.15.1 文件，不涉及執行版本 | CONFIRMED（本次環境紀錄，不宣稱最新） | — |
| 12 | 渲染程式有「只產生影格」的選項 | run-preview-stills 005752 | claims.md、brief、run-render 指令與輸出都沒有這個選項的定義或執行紀錄 | NOT FOUND | 「如果只是想檢查圖形，使用只產生影格的選項，先看圖再做完整影片。」→「如果只是想檢查圖形，可以請 AI 加一個只輸出影格的選項，先看圖再做完整影片。」 |
| 13 | 範例不是 Claude Motion 實錄，也不宣稱任何單一產品能一次完成 | description、check-scope 84576e | brief 的站主觀點、claims.md 開頭 | CONFIRMED | — |
| 14 | 主片另有八語的配音與 CC | description | brief 列英、日、韓、西、葡、印尼、越、泰，共 8 種 | CONFIRMED | — |
| 15 | 資料與製作確認日 2026-10-25 | description | today、brief | CONFIRMED | — |
| 16 | 標題、縮圖、標籤 | youtube.title、thumbnail、tags | 不含數字或產品宣稱 | OUT OF SCOPE | — |
| 17 | 其餘操作建議（先預覽、留版本、靜音檢查等） | 多處 | 編輯建議，claims c8 | OUT OF SCOPE | — |

## 統計

共 17 條：

- CONFIRMED 13
- CHANGED 0
- NOT FOUND 1（第 12 條，只改寫句子，line id 不變）
- OUT OF SCOPE 2

changed_facts = 1。

## 規則檢查

- **免責語**：「以官網為準」家族用語在旁白中出現 0 次；description 也沒有使用。
- **查證用語**：旁白裡沒有「經查證」「根據官方文件」「截至查證」「本影片」。
- **來源欄位**：沒有使用 stats 或 quote 卡片，所以不需要「官網 YYYY-MM-DD」欄位。終端機卡片都有 ran_on 2026-10-25。
- **個人資料**：腳本中沒有任何人的個人資料。

## 即將過期的事實

- **Pillow 版本**：官方 release notes 列出 13.0.0（2026-10-16）是目前最新版，本次執行用的是 12.3.0（2026-07-01）。觀眾照說明安裝會拿到 13.0.0，而範例沒有在 13.0.0 上跑過。建議在隨片說明鎖定版本，或在 13.0.0 上重跑一次。
- **Python 文件版本**：今天官方文件已是 3.15.1，執行環境是 3.12.14。片中沒有說出版本號，不影響旁白，只影響終端機卡片的 tool_version 欄位。
- **FFmpeg 7.1.5**：只寫在 claims.md，片中沒有出現。官方頁今天無法讀取，無法確認狀態。

## 觀點不一致

沒有發現。

- 旁白沒有出現「我的看法是」這類觀點句。
- route-choice 寫「選程式動畫」，並把理由限定在精確的格子與數字；route-other 說明人物表演不適合；84576e 不延伸成產品保證。這三處都和站主觀點一致。

## 有疑慮但沒有修改

1. **原始執行紀錄不在 payload**：run-check 與 run-render 的輸出（OK、outcomes=36、1280x720 24fps duration=54s audio=none）依 claims.md 指向的 summary-check.log、render.log、verification.json。這些檔案沒有附在 payload，我無法逐字比對。數學部分我已獨立重算確認。發佈前請人工確認終端機文字與 log 逐字一致，影片規格與 ffprobe 結果相同。
2. **錯誤結束的行為**：13 會以錯誤結束、exit 1，這點同樣只有 claims.md 的轉述，lesson-invalid.json 的執行紀錄不在 payload。
3. **FFmpeg 官方頁**：三頁都是 HTTP 503，claims.md 原本把它們列為證據。我已在 claims.md 註明讀取失敗。片中沒有引用 FFmpeg 的任何數字，所以不需要改旁白。
4. **教材包內容**：f064e3 說教材包保留了需求、提示詞和程式，description 列的是資料檔、程式、提示詞與檢查方法。兩者大致相符，但教材包本身不在 payload，無法逐項確認。
5. **縮到手機寬度預覽**：1de727 要觀眾這樣做，屬於操作建議，沒有宣稱已經實測，不更動。
