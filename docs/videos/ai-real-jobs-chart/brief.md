# AI Can Now Do 21% of Real Freelance Jobs. Last October It Was 2.5%.

slug：`ai-real-jobs-chart`｜旁白繁體中文（台灣）；英文以 CC 字幕與英文配音音軌提供｜企劃日 2026-09-28｜季企劃第 2 支（原 `ai-fails-96-percent-jobs`，前提已過期，見 claims.md 的「與季企劃不同的地方」）

## 觀眾

台灣與其他華語觀眾優先：在辦公室、代理商上班或自由接案的工作者，2026 年兩種標題都看過，一種是 2 月「AI 在 96% 的真實工作上失敗」（ColdFusion 的影片，2026-09-28 時觀看次數約 97 萬），另一種是一整年把 AI 當成裁員理由的公告。他們想用白話弄懂哪一邊才是真的，以及這對自己的工作代表什麼。英語觀眾透過英文 CC 字幕與英文配音音軌收看。中文搜尋：「AI 會取代我的工作嗎」、「哪些工作會被 AI 取代」、「AI 取代工作 2026」、「AI 裁員」、「AI 96% 工作做不到」、「Remote Labor Index」；英文搜尋：「will ai take my job 2026」、「ai fails 96% of jobs」、「remote labor index」、「ai layoffs 2026」、「which jobs will ai replace」。

## 觀眾看完能做到的事

- 正確解讀 Remote Labor Index 的數字：在真實的付費專案（多數是自由接案工作）中，AI 交出的成果被評為和專業人士一樣好的比例。這個比例從 2.5%（2025 年 10 月）升到 20.83%（排行榜上的 GPT-6 Astra，2026-09-28），但也代表大約每五個真實專案仍有四個失敗。
- 這週就拿自己的任務清單做三個問題的測試（AI 能不能把這件事起草成我打得開、檢查得了的東西？誰來檢查？做錯一次的代價多大？），把每項任務標成「AI 起草」、「頂多初稿」或「人的工作」；六個月後再做一次。

## 站主觀點

套用立場：3、5

我先讀研究，再看標題，也會交代數字從哪裡來、沒涵蓋什麼。2 月那則標題在當時是對的，現在已經不對了：同一個測驗在十一個月內進步了八倍多，但它也仍然顯示，最強的 AI 在大約五分之四的真實專案上會失敗。這兩件事同時成立；而且裁員公告和基準測試回答的是不同的問題，所以不論是「AI 做不了真正的工作」，還是「AI 正在搶走所有工作」，在數據面前都站不住腳。要採取的行動是一份任務清單，而不是對未來的某種感覺。我對一份真實職務說明的逐項判讀是個人意見，會標明是我的看法；這裡沒有任何內容是職涯或財務建議。

## 示範或實算

1. 用 `table` 投影片畫出曲線，數字都來自官方來源：Remote Labor Index 於 2025-10-29 推出，當時最好的 AI 代理 Manus 是 2.5%（scale.com）；2 月「96% 失敗」標題背後的最佳成績是 3.75%（排行榜上的 Claude Opus 4.5 thinking；ColdFusion 2026-02-13 的影片說 96.25%，這個數字見於第三方對該影片的摘要）；Claude Fable 5 在 2026-07-01 達到 15.8%（safe.ai）；GPT-6 Astra 20.83%、Claude Fable 5.1 17.92%，是 2026-09-28 從排行榜讀到的（labs.scale.com）。在 `big` 投影片上實算：20.83 ÷ 2.5 = 8.3，「十一個月成長八倍多」；100 − 20.83 = 79.17，「仍有大約五分之四失敗」。
2. 在 `table` 投影片上把一份真實的職務說明逐項拆開：美國勞動部 O*NET 的 Market Research Analysts and Marketing Specialists（市場研究分析師與行銷專員）任務清單（13-1161.00，共 13 項任務；職業頁標示「Updated 2026」，網站更新日 2026-08-25），列出其中 8 項，每項標上站主的判讀；再用 `stats` 投影片呈現計數（4 項「AI 起草、你檢查」；2 項「頂多初稿」；2 項「人的工作」）。

## 大綱

### 選項 A：從過期的標題開始，畫出曲線，再回到你的工作（推薦）

一行說明：以 2 月那則已經過期的標題當鉤子、成長曲線當收穫、裁員當張力、任務清單當行動，和從裁員切入的選項 B 不同。

開場鉤子（口播）：「今年二月，有一支廣為流傳的影片說，AI 在 96% 的真實工作上都會失敗。在當時，這句話沒有錯。同一個測驗現在顯示，最強的 AI 可以完成大約 21% 的真實付費專案。去年十月，這個數字還只有 2.5%。接下來我會告訴你，這個測驗在量什麼、為什麼公司還是照樣裁員，還有三個問題，讓你知道這對你的工作代表什麼。」

| # | 章節 | 秒 | 場景 |
| --- | --- | --- | --- |
| 1 | 2 月以來變了的那個數字（The number that changed since February） | 25 | `title` |
| 2 | Remote Labor Index 在量什麼（What the Remote Labor Index measures） | 75 | `steps`：真實專案（多數是付費的自由接案工作）、23 類工作、同一份需求說明、人工評審；`stats`：240、11.5 小時、$200、$143,991（專案合計價值） |
| 3 | 曲線：十一個月從 2.5% 到 21%（The curve: 2.5% to 21% in eleven months） | 60 | `table`：2025 年 10 月 → 2026 年 2 月 → 2026 年 7 月 → 2026 年 9 月 28 日；`big`：11 個月成長超過 8 倍，仍有大約五分之四失敗 |
| 4 | AI 還會做錯什麼（What AI still gets wrong） | 95 | `bullets`：推出時 AI 交付成果被退件的原因；`compare`：有進步但還不能交件 vs 仍然做不到；`stats`：讓 AI 評 AI，成果被高估約 3 倍和 2.5 倍 |
| 5 | 那公司為什麼還在裁員？（So why are companies cutting people?） | 80 | `stats`：2026 年 1–8 月以 AI 為由的裁員 116,175 人、約占 22%、3–7 月的頭號原因；`compare`：裁員公告說的 vs 測驗量的 |
| 6 | 用三個問題檢查你自己的工作（Test your own job in three questions） | 150 | `steps`：三個問題；`table`：O*NET 任務清單加上我的判讀；`stats`：我的計數；`bullets`：這週就做 |
| 7 | 所以 AI 會搶走你的工作嗎？（So will AI take your job?） | 35 | `outro` |

實算範例在第 3 章和第 6 章。結尾的下一步：留言提問「你清單上的哪一項任務最先有變化？」依估算工具，英文稿全長約 520 秒；改成中文旁白約 2,170 字（以每分鐘 250 字計）。

### 選項 B：從裁員開始

一行說明：先講今年美國以 AI 為由的 116,175 人裁員，再講顯示五個真實專案仍有四個失敗的測驗，最後才是任務清單；和從過期標題切入的選項 A 相比，情緒張力更強，但也更容易聽起來像在給建議。

開場鉤子（口播）：「今年，美國雇主已經把超過十萬人的裁員，算在 AI 頭上。可是最強的 AI，在真實的付費專案裡，還是五個有四個會失敗。不是有人錯了，就是兩邊回答的根本是不同的問題。」

章節：裁員（The layoffs，80 秒）→ 測驗（The test，75 秒）→ 曲線（The curve，60 秒）→ AI 還會做錯什麼（What AI still gets wrong，95 秒）→ 你的任務清單（Your task list，150 秒）→ `outro`（35 秒）。

## 會過期的事實

| 事實 | 撰稿當天重新確認的來源 |
| --- | --- |
| 排行榜數字（GPT-6 Astra 20.83%、Claude Fable 5.1 17.92%、Claude Fable 5 15.80%、Claude Opus 4.5 thinking 3.75%、Manus 2.5%） | https://labs.scale.com/leaderboard/rli 是即時更新的排行榜；榜首分數一變，標題的數字就要跟著改 |
| 推出時的數字（240 個專案，多數是付費的自由接案工作；23 類工作；中位數 11.5 小時與 $200；合計價值 $143,991，部分專案金額是接案者自己估的；各種失敗類型的比例，分母是被退件的 AI 交付成果） | https://scale.com/blog/rli （2025-10-29）、https://arxiv.org/abs/2510.26787 |
| 7 月的結果、範例、自動評分的高估幅度 | https://safe.ai/blog/significant-increase-in-digital-labor-automation （2026-07-01） |
| 以 AI 為由的裁員（1–8 月 116,175 人、約 22%、3–7 月的頭號原因、8 月退居第 4） | https://www.challengergray.com/blog/challenger-report-august-job-cuts-up-58-consumer-products-food-lead/ 與報告 PDF https://www.challengergray.com/wp-content/uploads/2026/09/Challenger-Report-August-2026.pdf （報告註明 2026-09-03 發布，網頁顯示的日期是 Sep 02）；9 月的報告在 10 月初發布 |
| O*NET 13-1161.00 的任務清單 | https://www.onetonline.org/link/summary/13-1161.00 （職業頁標示「Updated 2026」，網站更新日 2026-08-25） |
| 2 月那則標題 | https://www.youtube.com/watch?v=z3kaLM8Oj4o （2026-02-13） |

## 素材

- 只用原創投影片：表格、數據卡、對照卡。不放排行榜、ColdFusion 影片或任何公司的截圖。
- 職務任務的文字取自 O*NET OnLine（U.S. Department of Labor, Employment and Training Administration），依 CC BY 4.0 授權使用，並在影片說明欄註明出處；畫面上用的是縮短並譯成中文的版本，附上職業代碼，出處也要註明內容經過修改（CC BY 4.0 的要求）。

## 不做的事

- 不給職涯、財務或法律建議；不預測失業率；不說「學 AI，不然就會被取代」。
- 不點名任何公司用 AI 取代了人；裁員原因採用 Challenger 對雇主說法的統計。
- 不批評 ColdFusion：它的數字在 2 月是對的，影片也會這樣說。
- 不宣稱 Remote Labor Index 量的是整份工作；它量的是一個個專案（多數是自由接案工作），影片會講清楚。
