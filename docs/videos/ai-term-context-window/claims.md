# claims：上下文視窗（Context Window）是什麼

2026-09-30 撰稿者初查（Claude，撰稿封包 2026-09-30）。一行一個可查主張：`id｜主張（照旁白或字卡的寫法）｜來源｜查核日｜用到的場景`。這不是獨立查核；查核代理要拿 `video.json` 的旁白、字卡、標題、縮圖、說明欄逐一對照。官方頁的純文字副本在撰稿封包的 `sources/`，示範資料在 `demo-log.md`。站內文章的網址：https://mokaair.com/zh-TW/life/ai-context-window-explained（2026-09-14 查核發布）。

c1｜上下文視窗是模型單次能處理的容量，用 token 算；「桌面多大，就是上下文視窗」；table 卡「上下文視窗＝容器，這一輪的桌面能放多少」；「算 token 是在量長度；看視窗是在問這一輪放不放得下」｜https://ai.google.dev/gemini-api/docs/tokens（原句「Each Gemini model has a maximum number of tokens it can handle. The context window defines the combined limit of input and output tokens.」）｜2026-09-30｜desk-is-window、desk-table、measure-then-fit
c2｜這一輪的輸入和輸出都佔位子：桌上有本輪問題、應用程式先放好的規則、一部分歷史訊息、你貼的附件、它查到的資料，還要留一塊空位給回答｜https://platform.claude.com/docs/en/build-with-claude/context-windows（原句「Everything in the request counts toward the context window: the system prompt, every message in messages (including tool results, images, and documents), and your tool definitions. The output Claude generates for the turn, including its extended thinking, counts too.」「The context window (up to 1M tokens, depending on the model) holds the conversation history plus the new output Claude generates.」）｜2026-09-30｜question-and-rules、history-stack、clipped-attachments、reserved-corner、desk-is-window
c3｜放什麼上桌是應用程式準備的，不一定是你貼過的全部；有的放全文、有的先搜尋相關段落、有的把舊對話換成一段摘要；歷史訊息可能是全部也可能只是最近幾段；開新對話桌面重來，決議會不會跟過來看應用程式怎麼做；紀錄要先被選進工作集模型才看得到｜站內文章 §視窗裡放的是當次可用的資料（「桌上的東西由應用程式準備，不一定等於你所有上傳檔案或全部聊天紀錄。有些工具把文件全文放入，有些先搜尋相關段落，也有些在對話變長時保留摘要。具體行為由產品實作決定」）；佐證 https://ai.google.dev/gemini-api/docs/long-context（「strategies like arbitrarily dropping old messages, summarizing content, using RAG with vector databases」）與 https://platform.claude.com/docs/en/build-with-claude/context-windows 頁註 1（「Chat interfaces such as claude.ai can also manage the context window on a rolling "first in, first out" basis.」）｜2026-09-30｜hook、desk-few-sheets、hand-places-sheet、three-ways、summary-note、history-stack、flow-diagram、fresh-empty-desk、contracts-to-sort
c4｜三份社區管委會會議紀錄合計 604 字元、535 token（第 41 次 198 字元／180 token、第 42 次 217／188、第 43 次 189／167），同一種編碼 o200k_base；旁白「六百零四個字元」「五百三十五個 token」｜demo-log.md（tiktoken 0.14.0，2026-09-30 自行執行；工具頁 https://pypi.org/project/tiktoken/，curl 只拿得到機器人驗證頁，版本 0.14.0 與 MIT 授權改由 https://pypi.org/pypi/tiktoken/json 確認，2026-09-30）｜2026-09-30｜ruler-by-desk、three-records-desk、longest-record-lifted、document-on-scale、desk-stats
c5｜平均一份約 178 token（535 ÷ 3 ＝ 178.3）；二十萬 token 的桌面放得下 1,121 份，每月開一次會約 93 年；一百萬 token 放得下 5,607 份，約 467 年；算式：視窗 ÷ 平均每份 token（取整數）｜demo-log.md 的 `fits` 欄位｜2026-09-30｜desk-stats、your-own-stack-ruler
c6｜「二十萬」與「一百萬」是官方文件列出的兩個視窗級距；字卡標「以官網為準」，旁白不唸模型名稱、不講價格｜https://platform.claude.com/docs/en/build-with-claude/context-windows（「The context window (up to 1M tokens, depending on the model)」「Other Claude models, including Claude Sonnet 4.5, have a 200k-token context window.」）；https://ai.google.dev/gemini-api/docs/long-context（「Many Gemini models come with large context windows of 1 million or more tokens.」）｜2026-09-30｜desk-stats
c7｜二零二三年一篇研究（Lost in the Middle，Liu 等）：quote 卡原句「performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts」，翻譯「相關資訊出現在輸入的開頭或結尾時，表現通常最高；模型必須從長上下文的中間取用相關資訊時，表現明顯下降」；旁白「答案放在開頭或結尾，表現最好；放在中間，明顯變差」「就算是專門做長上下文的模型，也一樣會在中間迷路」（原句接著寫「even for explicitly long-context models」）｜https://arxiv.org/abs/2307.03172（v3，2023-11-20；摘要）｜2026-09-30｜research-book、lost-middle-quote、dark-corridor、withdrawal-at-end、withdrawal-in-middle
c8｜研究的做法是改變相關資訊在輸入裡的位置（從開頭移到中間、再到結尾），看模型找不找得到；任務是多文件問答與鍵值檢索｜https://arxiv.org/abs/2307.03172（摘要「We find that performance can degrade significantly when changing the position of relevant information」「multi-document question answering and key-value retrieval」）｜2026-09-30｜research-book、many-folders-one-marked、bookmark-in-stack、moving-answer
c9｜第一種忘記，沒送進去：輸入超過視窗時服務會直接告訴你輸入太長｜https://platform.claude.com/docs/en/build-with-claude/context-windows（「If the input alone already exceeds the model's context window, the API returns a 400 invalid_request_error ("prompt is too long") on every model.」）；站內文章 §超限、摘要漏失與理解錯誤有不同處理法（「若服務明確回報輸入過長」）｜2026-09-30｜stack-at-door、cabinet-into-bundles
c10｜壞的摘要 62 字元、55 token，「尚未核准」不見了；好的交接 62 字元、60 token，留住了；「字元數一模一樣，token 數只差五個」；「只帶這句摘要開新對話，桌上就沒有一個字說這個案子不能發包」（壞摘要全文沒有「尚未核准」「未核准」「不得發包」）｜demo-log.md（`summary.keeps_not_approved: false`、`good_handoff.keeps_not_approved: true`；兩段文字都是撰稿自己寫、自己算的，code 卡的 caption 有寫）｜2026-09-30｜one-line-summary、two-texts、sticky-note-falls、summary-three-icons、unused-stamp、handoff-status-strip、new-desk-only-summary
c11｜三份虛構紀錄裡維修案三次都尚未核准：第 41 次「決議『同意研究』…本案尚未核准，不得視為已通過」、第 42 次「列入 5 月區分所有權人會議討論，目前仍未核准，不得先行發包」、第 43 次「區分所有權人會議因人數不足流會，本案延至下次會議，仍未核准」；旁白「第一次同意研究，第二次列入區權會，第三次區權會流會，延期」｜demo-log.md 的三份紀錄全文（虛構的示範資料，不是真實社區）｜2026-09-30｜three-stamped、calendar-three-meetings
c12｜沒有超限、全部放上桌，模型還是可能搞混哪一版有效（前面舊方案、後面才撤回、中間插報價草稿）；把桌子換大沒有修正版本關係；有幫助的做法是明確標出提案、決議、撤回、待查證｜站內文章 §容量上限與有效使用能力分開看（「例如會議紀錄前面有舊方案、後面才正式撤回，中間又插入報價草稿。即使整份資料沒有超限，模型仍可能混淆哪一版有效。這時只把容量加大，沒有修正版本關係。更有幫助的是明確標出提案、決議、撤回與待查證項目」）｜2026-09-30｜reader-two-questions、bigger-table、colour-labels、labelled-row、tabs-few-minutes、movers-with-giant-desk、mixed-versions
c13｜三種處理法：沒送進去→縮小這一輪的工作集、只留相關章節、記下原文在哪、分批後還要合併檢查（某一次的決議可能改了另一份紀錄）；摘要漏掉→摘要留得住主題留不住狀態尤其是否定條件、用已核對的原文補回去、重開對話不能只帶結論還要帶未解問題、取消的方向、驗收要求；原文在卻答錯→把相關段落拉到一起、直接問哪一版有效並要求指出依據、重問答對只是改善訊號不是永久證明、留幾個容易混淆的例子確認方法對別的文件也管用；compare 卡三列｜站內文章 §超限、摘要漏失與理解錯誤有不同處理法 與文末比較表（現象／先查什麼／處理方向）｜2026-09-30｜batches-linked、decision-changes-record、shrink-workset、title-kept-status-erased、originals-back、more-than-conclusions、original-present-wrong、side-by-side-magnifier、ask-for-evidence、signal-lamp、box-of-examples、three-fixes、cabinet-into-bundles；查核第一輪（2026-09-30）：copier-thin-sheet 的「第二種最常見」在文章、brief、outline 都沒有出處，已改成「第二種」；「最難察覺」（original-present-wrong）視為描述、未動
c14｜交接單五格：目標、已確認的事實、原文位置、不能違反的限制、下一步；先由人核對，尤其是數字、日期、決議狀態；「正在討論」不能變成「已經決定」；「同意研究」與「正式通過」不能合併成同一種狀態；長資料待在有整理的地方、按問題取用、留查回原文的路；要比對全文就逐段處理再總體校對；真正要看的是這一輪收到什麼、限制留住了沒、結果追不追得到證據；加長輪（2026-09-30）新增：把紀錄整理成可查核的工作集三步（先列欄位提案、狀態、負責人、缺什麼、原文在哪再按日期建索引；請它把每份紀錄抽成工作表、找不到就留空、位置要查得回去；只帶核對過的工作表和必要原文請它草擬議程）、「要的是一張工作表，不是一篇看起來很完整的摘要」、「寫錯了，回頭查三件事：表對不對、原文在不在、有沒有要它分狀態」｜站內文章 §一般使用者如何保留工作連續性、§把會議紀錄整理成可查核的工作集（「留意『建議』『同意研究』與『正式通過』是否被合併成相同狀態」）、文末提示框（「『正在討論』不能在摘要裡變成『已決定』」）｜2026-09-30｜five-box-form、passing-the-form、handoff-items、checking-by-hand、two-stamps-merged、discussing-vs-decided、organised-cabinet、path-back-to-source、segments-and-final-check、three-checkpoints、workset-steps、worksheet-vs-summary、pen-paused-looking-back、three-things-to-recheck
c15｜記憶功能是倉庫不是桌面：在視窗之外保存，取回來放上桌才佔這一輪的空間；別假設倉庫會逐字留下你給過的每一份文件；很多人把專案、附件、記憶功能當成無限大的空間｜站內文章 §視窗裡放的是當次可用的資料 第三段（「應用程式可以在視窗之外保存偏好或工作紀錄…只要取回的內容被交給模型，它仍然要佔用當次處理空間…也不能假設記憶功能會逐字保留你給過的所有文件」）與 §一般使用者如何保留工作連續性（「不要把專案、附件或記憶功能當成無限空間」）；文章的一手來源是 LangChain Memory overview（2026-09-14）；查核第一輪 2026-09-30 重開 https://docs.langchain.com/oss/python/concepts/memory（200）：「Long-term memory stores user-specific or application-level data across sessions and is shared across conversational threads. It can be recalled at any time and in any thread.」「A full history may not fit inside an LLM's context window」｜2026-09-30｜three-drawers-infinite、warehouse-and-desk、cart-from-warehouse、shrunken-cards、desk-table
c16｜訓練得到的知識在參數裡，是它的本事，不在桌上；今天貼進去的決議它可以照著答，但不會因此變成它的知識｜站內文章 §視窗裡放的是當次可用的資料 第二段（「你今天貼入會議決議，模型可以依它作答，但不代表這些內容立刻成為模型權重的一部分」）；https://platform.claude.com/docs/en/build-with-claude/context-windows（「This is different from the large corpus of data the language model was trained on, and instead represents a "working memory" for the model.」）｜2026-09-30｜desk-table、sheet-not-into-brain、brain-closed-door
c17｜站主觀點（提案，待站主確認）：「我的看法是，先看這一輪桌上有什麼，再決定要補什麼」「忘記的問題，我不靠換更大的視窗解決；摘要一定拿去對原文」「換更大的桌子之前，先問少的那一段是沒放上去還是放了沒讀到」；outro「留在畫面裡的訊息，模型不一定讀到；先看桌上有什麼」；加長輪（2026-09-30）新增「以我的用法，上下文視窗這個名詞，改變我兩個決定」「第一，換不換更大的視窗，先分清是哪一種忘記」「第二，信不信一句看起來很完整的摘要：先對原文，再信」「帶走三件事。先看桌上有什麼；摘要對原文；分清是哪一種，再動手」，以及 cw9er 標成意見的「我的看法是，它要是寫成即將施工，錯的不是模型，是交接」｜brief.md §站主觀點（這個名詞改變的決定有兩個：要不要為更大的視窗付錢或換工具、信不信一句看起來很完整的摘要；失敗的樣子是這集的示範）與 §不做的事（寫錯了錯的是交接）｜2026-09-30｜taking-stock、big-desk-pushed-aside、three-question-cards、closing、crane-question、two-decisions-fork、bigger-desk-or-not、trust-after-checking、three-takeaways
c18｜有官方文件把上下文視窗比作短期記憶：一個人一次記得住的有限，模型也是（旁白不唸公司名）｜https://ai.google.dev/gemini-api/docs/long-context（「An analogy for the context window is short term memory. There is a limited amount of information that can be stored in someone's short term memory, and the same is true for generative models.」）｜2026-09-30｜short-term-memory

沒有主張、只有比喻或提問的場景：scroll-tiny-desk、archive-one-sheet、brain-cloud、endless-table、figure-mid-table、ch3、long-table-months、pages-turn-themselves、old-plan-withdrawal、quote-in-middle、warning-sign、two-checks、passed-check-failed-exam、forgot-which-kind、agenda-blank-status、copier-thin-sheet、crane-question（條件句，不是實測結果；加長輪 2026-09-30 已標成站主意見「我的看法是」，列入 c17）、article-cta、empty-handoff-sheet、ch5、ruler-desk-warehouse、desk-ruler-warehouse-brain、article-on-desk。

## 與企劃不同的地方

1. **shot 數 76、場景 89**，高於 OUTLINE 的「38 到 45 個 shot」。原因：每個畫面狀態 ≤ 8 秒、影片要 ≥ 9.5 分鐘，而配方 B 的 13 張卡片裡有 7 張是單狀態卡，卡片只撐得起約 130 秒；剩下的 470 秒只能靠插圖，每張最多 7.7 秒就是 60 張以上。`docs/videos/ILLUSTRATED.md` 的成本估算本來就是每支 55 到 75 張，這集落在裡面。
2. 配方 B 的卡片之外多加兩張：第二章「一句話定義」用 `big`（桌面多大，就是上下文視窗），第六章「跟誰容易搞混」用 `table`（token／上下文視窗／記憶／模型參數，README 的段落表建議 compare 或 table）。配方 B 原有卡片的相對順序沒動：title → stats → chapter → diagram → quote → code → compare → cta → chapter → bullets → outro。
3. `cta` 放在第四章結尾、compare 之後、第五章章節卡之前（OUTLINE 的章節節拍把 cta 寫在第四章；配方那一行寫在 bullets 之後，兩處不一致，取節拍）。
4. 第一章是 title 卡加兩個 shot（OUTLINE 寫一個）：第二個 shot 只有一句章末問題「那它這一次，到底拿到了什麼？」加 1200 停頓，讓第一章也照說書式規則以問題收尾；全長 19 秒。
5. 開場的兩句合成一句「上個月的對話還在畫面裡，模型這一次卻可能一個字都沒看到。」放 title 卡（兩句分開會讓 title 卡超過 8 秒）；「往上滑」的畫面交給第一張插圖。
6. `stats` 卡四格（OUTLINE 三格）：多放「178｜平均每份 token」，是示範 JSON 裡本來就有的中間數。
7. 「換新對話只帶這句摘要，模型會把維修案寫成即將施工」改成條件句：旁白說「桌上就沒有一個字說這個案子不能發包」（摘要內容的事實）與「它要是寫成即將施工，錯的不是模型，是交接」；沒有跑過模型，不說成實測。
8. 第六章的站主觀點用了兩句加一個提問（都出自 brief 的同一段），不只一句。
9. 片尾只指說明欄第一行的文章：token 那一集狀態還是 planned，沒上架。
10. 多用了 OUTLINE 來源 1 的一句「context window is short term memory」（c18，第二章一個 shot），節拍裡沒有。
11. 章節長度：第二章 113 秒（節拍約 100）、第三章 117、第四章 165（約 150）、第五章 103、第六章 87。

## 我懷疑但沒動的事

1. lint 的估計是每分鐘 250 單位；`automated.md` 說 Gemini 實唸比估計短約兩成，所以成片可能只有 8 到 8.5 分鐘、低於 9 分鐘的目標。這裡的驗收是 lint 的 Estimate（10.1 分），沒有為此加長；如果 `tts --dry-run` 證實偏短，該加的是內容不是句長。
2. PACKET 的「38 到 45 個 shot」和「每個狀態 ≤ 8 秒」「9.5 分鐘以上」三條在配方 B 下不能同時成立，我取後兩條（見上面第 1 點）。
3. 章名「上下文視窗跟 token、記憶差在哪」有拉丁字母詞；lint 不檢查章名，章名不唸，照 OUTLINE 原樣。
4. 第 4 章開頭那句「三次都尚未核准」和第 41 次紀錄的「同意研究」並存：紀錄原文是「決議『同意研究』…本案尚未核准，不得視為已通過」，兩者不衝突，但查核者可以確認觀眾不會把「同意研究」聽成核准。
5. c15 的一手來源（LangChain Memory overview）今天沒有重開，只用站內文章（2026-09-14 查核）；旁白裡這段是文章的說法，沒有引用任何產品的記憶功能細節。
6. `quote` 卡的英文原句很長（約 210 字元），版型能不能一行行排好要看 render；縮短就不是原句，所以沒動。
7. 第一章 19.2 秒，離 20 秒的上限只有 0.8 秒；實唸會更短，所以沒再砍。
8. 平均換畫面 5.99 秒（門檻 6.0）是估計值，實唸較快會更低；沒有再拆 shot。

## 進度

- 2026-09-30：brief.md、spec.json → video.json（89 景、76 shot、101 句、2,099 單位、估 10.1 分）、claims.md、demo-log.md、shorts.json 都寫完；`lint --slug ai-term-context-window` 0 錯誤 0 警告。
- 2026-09-30 查核第一輪（獨立查核者，Claude）：94 條主張全部重開來源與重跑 demo_context.py（輸出逐位元相同），1 條 NOT FOUND（cwdgg「最常見」，已刪），其餘確認；詳見 verify-1.md。
- 待辦（不在撰稿範圍）：站主確認 brief 的站主觀點提案；`tts --dry-run` 看實際長度；`keyframes` 生圖後看 76 張插圖的 judge 分數；lexicon.json 不用新增（旁白只用 token 與 AI，兩個都已在字典）。
- 2026-09-30 加長＋聽眾審稿（Claude，LENGTHEN 封包）：直接改 video.json（沒有再用 spec.json）。111 景（97 shot、14 卡）、127 句、2,570 單位，`lint --slug ai-term-context-window` 0 錯誤 1 警告（估 12.3 分，超過 target_minutes 的估計值警告，照封包留著）；估計的畫面狀態最長 7.9 秒（開場 title 卡，原本就有）、平均 5.9 秒換一張、插圖佔 79%、第一章 19 秒。單位數沒到封包的 2,650：這集起跳就是 89 景，每加一個 shot 除了旁白本身還多 1 秒停頓（0.3 句尾加 0.7 換景），2,650 單位會把 Estimate 推到約 12.6 分，兩個範圍在這集的結構下不能同時成立，取 Estimate 範圍的上緣。新句子與改動列在下面兩節。

## 聽眾審稿改動（2026-09-30）

- cwr09: token 是模型自己的單位，不是字數；我拿三份會議紀錄算過一次。 → token 是模型自己的單位，不是字數；拿三份會議紀錄實際算一次。（示範是製作時工具跑的計算，不替站主編經驗）
- cwpzq: 我把三次會議壓成一句話，六十二個字元，看起來很完整。 → 把三次會議壓成一句話試試看：六十二個字元，看起來很完整。（同上）
- cw9er: 它要是把維修案寫成即將施工，錯的不是模型，是交接。 → 我的看法是，它要是寫成即將施工，錯的不是模型，是交接。（標成意見；看法出自 brief §站主觀點與 §不做的事；「維修案」由前一句 cwio4 的「這個案子」承接，拿掉是為了不讓 27 單位的長句連續四句）
- cwb3u: 你貼的附件、它查到的資料，也都攤在這張桌上。 → 你貼的附件，還有它查到的資料，也都攤在這張桌上。（cwb3u、cw2m7、cwos5 連續三句都 19 單位，換節奏）
- cwftv: 你可能覺得，反正全都在桌上，它自己會翻。 → 你可能覺得，反正都在桌上，它自己會翻、會找。（cwz0e、cwmrv、cwftv 連續 15、16、17 單位，換節奏）
- cw5l9: 沒有超限，全部都放上桌了，模型還是可能搞混哪一版才有效。 → 沒有超限，全都上桌了，它還是可能搞混哪一版才有效。（cwad3、cw5l9 都 25 單位再接 28，換節奏）
- 檢查過沒動的：第一人稱只剩 cw4rn、cw0y7（已標「我的看法是」、逐句出自 brief §站主觀點）和新加的 cwk4g（「以我的用法」）；沒有英文介面名、書面語、打招呼、括號、阿拉伯數字；最長句 31 單位（cwicb）；停頓只在開場 900、「你以為」600、五個章末問題 1200；token 第一次出現在 cwos5「單位是 token」，下一景 cwr09 就說它是模型自己的單位；沒有純重複的句子可刪。

## 加長新增的句子（2026-09-30）

每句一個新 shot，除非註明是既有場景的第二句或卡片。依據只用 claims 已有的 c 編號、demo-context.json 的欄位、文章段落、brief §站主觀點。

第二章
- cw0fm｜如果你把一批合約丟給它整理，先問一句：它這一次拿到了哪幾份？｜c3（桌上的東西由應用程式準備，不一定是你貼過的全部）；場景取自 brief §觀眾（把一批合約丟給 AI 整理的專案助理）
- cw0gl（summary-note 第二句）｜哪一種，看你用的工具怎麼做。｜c3（文章：具體行為由產品實作決定）
- cw3si｜最長的一份，兩百一十七個字元。｜c4；demo `records[1].chars` = 217
- cwof9｜算出來一百八十八個 token。｜c4；demo `records[1].tokens` = 188
- cw4k9｜你自己的文件也能算：視窗大小除以每份的 token 數，就是放得下幾份。｜c5（算式：視窗 ÷ 平均每份 token）；brief §觀眾看完能做到的事 3

第三章
- cw5mv｜他們測的是多份文件一起放進去的問答。｜c8（multi-document question answering）
- cwotj｜看相關的那一份放在哪裡。｜c8（changing the position of relevant information）
- cw6fn｜換成你的長桌，撤回單在最後面還好。｜c7（開頭或結尾表現最好）；「撤回單在最後面」是 c12 文章例子的位置（後面才正式撤回）
- cwprg｜要是被夾在中間，它就容易漏看。｜c7（放在中間，明顯變差）
- cw8rl｜如果你是管委會的幹部，先把每份紀錄貼上標籤。｜c12（明確標出提案、決議、撤回與待查證項目）
- cwptq｜比換一個更大的視窗有用。｜c12（只把容量加大，沒有修正版本關係；更有幫助的是明確標出…）

第四章
- cw9ec｜像是一口氣把一整櫃的報告全丟進去，門太小；最直接的做法，是分批。｜c9（輸入超過視窗，服務回報過長）；c13／文章 §超限、摘要漏失與理解錯誤（縮小本輪工作集…必要時分批抽取）
- cwaua｜壞的那句什麼都記得：報價、燈具、旅遊。｜c10；demo `summary.text`（三家廠商報價 18 至 22 萬元；中庭燈具已更換完成；年度旅遊 6 月 14 日去宜蘭）
- cwsjq｜就是沒說維修案還沒核准。｜c10；demo `summary.keeps_not_approved` = false
- cwchh｜好的那句留的是狀態：尚未核准、流會延期、不得發包，還有待辦。｜c10；demo `good_handoff.text`（維修案狀態：尚未核准，區權會流會延期，不得發包；待辦是臨時防水方案報價）

第五章
- workset-steps（新 steps 卡，三個 reveal）｜把紀錄整理成可查核的工作集：列欄位，建索引／抽成工作表／只帶核對過的表｜c14；文章 §把會議紀錄整理成可查核的工作集 三段
- cwcp2｜第一步，先列欄位：提案、狀態、負責人、缺什麼、原文在哪；再按日期建索引。｜同節第一段（先列出任務需要的欄位：提案名稱、目前狀態、負責人、尚缺資料與原始段落。再依日期建立索引）
- cwcxa｜第二步，請它把每份紀錄抽成工作表；找不到就留空，位置要查得回去。｜同節第二段（請模型針對相關紀錄抽取欄位，要求找不到就留空，並保留可回查的位置）
- cwdzl｜第三步，只帶核對過的工作表和必要原文，請它草擬議程。｜同節第三段（只帶入已核對的工作表與必要原文，請模型草擬議程）
- cwex2｜要的是一張工作表，不是一篇看起來很完整的摘要。｜同節第二段（預期產物是工作表，而不是先寫一篇看似完整的摘要）
- cwflo｜寫錯了，回頭查三件事。｜同節第三段（如果它把未核准維修寫成即將施工，就回頭檢查…）
- cwslc｜表對不對、原文在不在、有沒有要它分狀態。｜同節第三段（工作表是否有錯、原文是否真的在本輪上下文，以及指示是否要求區分狀態）

第六章
- cwk4g｜以我的用法，上下文視窗這個名詞，改變我兩個決定。｜c17；brief §站主觀點（這個名詞改變的決定有兩個）
- cwka0｜第一，換不換更大的視窗，先分清是哪一種忘記。｜c17；brief §站主觀點（要不要為更大的視窗付錢或換工具：先分清楚是沒送進去、摘要漏掉還是看了卻答錯，再說）；旁白不提付錢
- cwkop｜第二，信不信一句看起來很完整的摘要：先對原文，再信。｜c17；brief §站主觀點（信不信一句看起來很完整的摘要：先對原文再信）
- cwmw3（three-takeaways 第一句）｜帶走三件事。｜引導句，沒有主張
- cwnro（three-takeaways 第二句）｜先看桌上有什麼；摘要對原文；分清是哪一種，再動手。｜c17；outro 卡的三行（brief §站主觀點、§大綱最後一句）

寫了又拿掉的（時間放不下）：「視窗給的是容量；資料整理好、核對過，容量才派得上用場」（文章 §一般使用者 末段）、「存著，不等於這一輪在用」（c15）、「只看局部摘要，跨文件的關係會漏掉」（c13）；要補到 2,650 單位時可以先加這三句。
