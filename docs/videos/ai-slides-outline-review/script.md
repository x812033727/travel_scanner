# AI簡報先審大綱：公開PDF變成4頁有來源的成品

## 場景

### 我從公開報告寫下簡報需求

#### 1. four-page-local-output（big）

旁白（數字與名稱清楚，句尾自然收住）：二〇二六年十月二十五日，我打開報告，寫下簡報需求。

#### 2. sum-question（big）

旁白（問句微揚，像在等對方一起判斷）：兩筆投資放在一起，能直接相加嗎？

#### 3. two-to-four-question（big）

旁白（問句微揚，像在等對方一起判斷）：這份大綱裡的材料，要怎麼分頁才各有任務？

#### 4. handoff-question（big）

旁白（問句微揚，像在等對方一起判斷）：交出去以後，能改字、也能追來源嗎？

#### 5. dated-news-hook（big）

旁白（數字與名稱清楚，句尾自然收住）：十月十九日，Gemini Notebook介紹生成前先審大綱。

### 來源紀錄把金額與使用比例分開

#### 6. local-authored-scope（big）

旁白（承接前句，輕輕帶出新的進度）：要決定兩筆能不能相加，我先填來源紀錄裡的投資範圍。

#### 7. source-record-start（big）

旁白：這份本地原創範例受Google公告啟發，沒有試用Notebook。

#### 8. source-report（table）

旁白（數字與名稱清楚，句尾自然收住）：輸入是Stanford AI指數報告的經濟章。

#### 9. sixty-source-pages（stats）

旁白（數字與名稱清楚，句尾自然收住）：這份公開PDF有六十頁，簡報只需要其中的相關資料。

#### 10. briefing-audience-and-target（steps）

旁白：我給它的任務，是讓一般同事讀懂AI投資和組織使用。
旁白（承接前句，輕輕帶出新的進度）：先填聽眾和用途，才知道哪些內容該留下。

#### 11. report-and-data-year（compare）

旁白：來源紀錄裡，報告年份和資料年份分成兩欄。
旁白（數字與名稱清楚，句尾自然收住）：報告是二〇二六年，這次採用的資料則是二〇二五年。

#### 12. year-label-consequence（big）

旁白（承接前句，輕輕帶出新的進度）：否則一個新報告標題，就可能讓讀者把舊資料讀成新調查。

#### 13. two-metric-question（big）

旁白（問句微揚，像在等對方一起判斷）：同樣寫AI，投資金額和使用比例能共用一張圖嗎？

#### 14. money-versus-respondents（compare）

旁白：金額這邊要記地區、投資類型，還有美元單位。
旁白（承接前句，輕輕帶出新的進度）：比例這邊要記誰受訪，以及他回報的是什麼使用情況。

#### 15. split-metric-record（big）

旁白：它們回答不同問題，我把兩種指標拆開記。

#### 16. two-page-number-introduction（big）

旁白（承接前句，輕輕帶出新的進度）：來源紀錄還留了兩種頁碼，它們負責不同的定位。

#### 17. two-page-number-fields（table）

旁白：印刷頁碼，是報告紙面上標的號碼。
旁白：PDF頁序，則是這個檔案從第一頁開始數的位置。

#### 18. locate-and-identify-figure（steps）

旁白（承接前句，輕輕帶出新的進度）：同事拿到同一份檔案，就能用頁序跳回原頁。
旁白：原頁上還有圖號，能繼續對到同頁的那張圖。

#### 19. prompt-field-question（big）

旁白（問句微揚，像在等對方一起判斷）：把這些條件放進需求，怎樣避免只收到一段摘要？

### 完整需求交出後，作者初稿仍擠在兩頁

#### 20. reusable-full-prompt（big）

旁白（承接前句，輕輕帶出新的進度）：我把這次需求整理成完整提示，你可以照這個格式改。

#### 21. prompt-card-one（steps）

旁白（像示範一句可以直接說的要求，清楚而自然）：請只用我提供的這份公開PDF，替一般同事做四頁簡報。
旁白（像示範一句可以直接說的要求，清楚而自然）：簡報目標約三分鐘。
旁白（像示範一句可以直接說的要求，清楚而自然）：先給大綱，先不要生成投影片。

#### 22. prompt-card-two（steps）

旁白（像示範一句可以直接說的要求，清楚而自然）：每頁只回答一個問題，列出要用的數字、資料年、單位。
旁白（像示範一句可以直接說的要求，清楚而自然）：列出受訪母體或統計範圍、報告印刷頁碼和PDF頁序。
旁白（像示範一句可以直接說的要求，清楚而自然）：把投資金額和使用比例分開。
旁白（像示範一句可以直接說的要求，清楚而自然）：總額與其中一部分，不要相加。

#### 23. prompt-card-three（steps）

旁白（像示範一句可以直接說的要求，清楚而自然）：來源若有未對齊處，列成待確認，不要替我挑一個數字。
旁白（像示範一句可以直接說的要求，清楚而自然）：等我一次回覆全部修改後，再產出四頁簡報。
旁白（像示範一句可以直接說的要求，清楚而自然）：同時交可編輯檔、PDF和逐頁引用清單。
旁白（像示範一句可以直接說的要求，清楚而自然）：未確認的數字只作註記，不畫成確定結論。

#### 24. missing-year-question（big）

旁白（問句微揚，像在等對方一起判斷）：大綱如果漏了資料年份，要在哪裡補上？

#### 25. specific-field-feedback（table）

旁白：就在該頁的資料年欄，直接要求補上年份。

#### 26. outline-usability-question（big）

旁白（問句微揚，像在等對方一起判斷）：有了完整需求，第一份大綱就一定合用嗎？

#### 27. author-initial-outline（table）

旁白：我設計的初稿範例，只有兩頁，還沒有排成投影片。
旁白（承接前句，輕輕帶出新的進度）：一頁叫AI投資和採用概況，另一頁叫整理成一張總覽圖。

#### 28. same-material-both-pages（table）

旁白：兩頁都塞了同一組金額、地區、使用比例和待確認數字。

#### 29. material-list-not-page-question（big）

旁白：它列出了材料，卻沒有替每頁分配一個讀者問題。

#### 30. author-written-stages（big）

旁白（承接前句，輕輕帶出新的進度）：我自己寫的初稿和整批修改要求，都留在範例紀錄裡。

#### 31. no-product-conversation（big）

旁白：這些階段是一次產出時保存的，並沒有真的停下來等我回覆。

#### 32. what-decision-to-change（big）

旁白（問句微揚，像在等對方一起判斷）：既然每頁沒有分工，要修改的到底是哪個決定？

### 集中修改讓四頁各自有了任務

#### 33. change-page-question（big）

旁白（承接前句，輕輕帶出新的進度）：開頭問材料怎麼分頁，我把每頁要回答的問題寫進修改。

#### 34. concentrated-feedback-a（steps）

旁白：照需求分頁，把投資金額和使用比例分成不同的問題。
旁白：全球企業投資及其中私人投資不可相加。
旁白（承接前句，輕輕帶出新的進度）：國別頁只比較私人融資，別叫全國AI總支出。

#### 35. concentrated-feedback-b（steps）

旁白：資料頁保留先前的資料年、單位、母體或範圍，以及兩種頁碼。
旁白：未對齊的生成式AI比例，保留為兩處來源註記。
旁白（承接前句，輕輕帶出新的進度）：最後按剛才的交付清單，把成品和引用紀錄一起交齊。

#### 36. visible-change-question（big）

旁白（問句微揚，像在等對方一起判斷）：集中修改要落到哪裡，才算真的改好了？

#### 37. page-one-metric-separation（diagram）

旁白：第一頁把讀者的問題分成投入多少錢、多少人回報使用。
旁白（承接前句，輕輕帶出新的進度）：金額對應投資範圍，比例對應受訪者和組織。

#### 38. global-page-relationship（big）

旁白：第二頁把全球金額，做成能看出包含關係的圖。

#### 39. global-corporate-value（stats）

旁白（數字與名稱清楚，句尾自然收住）：全球企業AI投資是五百八十一點六九，以十億美元計。

#### 40. global-private-subset-value（stats）

旁白（數字與名稱清楚，句尾自然收住）：其中私人AI投資，按相同單位是三百四十四點六六。

#### 41. sum-question-payoff（big）

旁白：開頭問能不能相加，這裡的關係是總額包含其中一部分。

#### 42. double-count-reason（big）

旁白（承接前句，輕輕帶出新的進度）：再加一次私人投資，就把已包含的部分重複算了。

#### 43. page-two-subset-output（diagram）

旁白：所以我在短的那條旁邊加上其中，頁面留下包含關係。

#### 44. national-total-question（big）

旁白（問句微揚，像在等對方一起判斷）：那地區比較，能直接改叫各國AI總支出嗎？

#### 45. regional-private-scope（table）

旁白：第三頁沿用報告整理的Quid私人AI投資口徑。

#### 46. us-private-value（stats）

旁白（數字與名稱清楚，句尾自然收住）：同為二〇二五年，以十億美元計，美國是二百八十五點八八。

#### 47. china-private-value（stats）

旁白（數字與名稱清楚，句尾自然收住）：中國是十二點四一，統計範圍和單位相同。

#### 48. private-not-national-spend（big）

旁白：這裡比較同一套私人融資統計，不是兩國全部公私支出。

#### 49. page-three-same-scope-output（diagram）

旁白：圖上兩條長度，對應的是同一年、同單位、同類投資。

#### 50. usage-page-new-unit（big）

旁白（承接前句，輕輕帶出新的進度）：第四頁換成使用情況，金額的美元單位就不能帶過來。

#### 51. survey-reported-ai-use（stats）

旁白（數字與名稱清楚，句尾自然收住）：這份調查中，百分之八十八的受訪者回報，
旁白：自己的組織至少有一項業務使用AI。

#### 52. survey-not-census（big）

旁白（承接前句，輕輕帶出新的進度）：這是受訪者自述，不能寫成全球所有公司的普查結果。

#### 53. unresolved-block-delivery-question（big）

旁白（問句微揚，像在等對方一起判斷）：生成式AI有一格未解，簡報要因此卡住嗎？

#### 54. two-source-observations（stats）

旁白（數字與名稱清楚，句尾自然收住）：摘要列百分之七十，描述組織在至少一項業務使用。

#### 55. wording-needs-alignment（compare）

旁白（數字與名稱清楚，句尾自然收住）：詳文列百分之七十九，描述受訪者回報組織經常使用。

#### 56. both-2025-unresolved（big）

旁白：都指二〇二五年，問法和分母是否一致仍待確認。

#### 57. do-not-adopt-either-rate（big）

旁白：不把這兩個值當成已確認的採用率，也不因此判定報告寫錯。

#### 58. page-four-annotation-output（diagram）

旁白（承接前句，輕輕帶出新的進度）：兩處留註記，其餘確認內容繼續交付。

### 第二到第四頁接回原報告

#### 59. citation-record-connects-pages（big）

旁白：引用紀錄把第二到第四頁接回原報告，第一頁則是作者問題總覽。

#### 60. find-original-figure-question（big）

旁白（問句微揚，像在等對方一起判斷）：開頭問怎麼追來源，拿到這份簡報後，要怎樣找回原圖？

#### 61. page-two-citation-filled（table）

旁白（數字與名稱清楚，句尾自然收住）：簡報第二頁對應印刷第一百七十八頁，PDF第八頁。
旁白（數字與名稱清楚，句尾自然收住）：圖號是四點二點一，兩個金額都出自這張圖。

#### 62. follow-the-citation（steps）

旁白：核對時先用PDF頁序到原頁，再看圖號、數值和單位。
旁白（承接前句，輕輕帶出新的進度）：你要引述給同事，也能把報告印刷頁碼一起留下。

#### 63. page-three-citation-filled（table）

旁白（數字與名稱清楚，句尾自然收住）：簡報第三頁對應印刷第一百八十二頁，PDF第十二頁。
旁白：這頁的來源標記，把同一張私人投資圖和兩個地區連在一起。

#### 64. page-four-citation-filled（table）

旁白（數字與名稱清楚，句尾自然收住）：簡報第四頁對應印刷第一百九十三頁，PDF第二十三頁。

#### 65. annotation-source-position（table）

旁白（數字與名稱清楚，句尾自然收住）：待確認註記另連到摘要的印刷第一百七十三頁，PDF第三頁。

#### 66. adopted-versus-annotation（table）

旁白（承接前句，輕輕帶出新的進度）：這個差異只放在註記欄，不列入已採用的五項數值主張。

#### 67. editable-handoff-question（big）

旁白（問句微揚，像在等對方一起判斷）：但同事要改字時，交一張排好的圖片就夠嗎？

#### 68. handoff-two-uses（big）

旁白（承接前句，輕輕帶出新的進度）：我把同一份內容，分成觀看用和修改用兩種交付。

#### 69. pdf-and-pptx-handoff（compare）

旁白：PDF是四張頁面圖片，能打開看版面，沒有可抽取的文字。
旁白：開頭問能不能改字，這次也交付了PPTX可編輯檔。

#### 70. pptx-native-object-evidence（table）

旁白（承接前句，輕輕帶出新的進度）：其中的文字和形狀分開保存，沒有嵌入頁面圖片。

#### 71. editable-unit-text（table）

旁白：像投資頁的單位，也留在原生文字方塊裡。

#### 72. powerpoint-test-boundary（big）

旁白（承接前句，輕輕帶出新的進度）：檔案已重新開啟檢查結構，尚未在PowerPoint裡原生渲染。

#### 73. before-presenting-in-your-app（steps）

旁白：如果你要在那裡正式播放，先打開確認字型和換行。

#### 74. completed-delivery-package（diagram）

旁白：簡報、可編輯檔與逐頁來源，現在是一份能核對的交付包。

#### 75. news-workflow-connection-question（big）

旁白（問句微揚，像在等對方一起判斷）：那這份本地流程，和Google的新功能到底接在哪裡？

### Google公告新增生成前的大綱審查

#### 76. review-position-connection（big）

旁白：新聞裡的審稿位置，正是這份簡報決定每頁內容的地方。

#### 77. official-format-and-review（table）

旁白：Gemini Notebook可以先選形式和風格，再開啟Review。

#### 78. official-review-objects（compare）

旁白（承接前句，輕輕帶出新的進度）：做簡報時審的是大綱，做影片時則是製作筆記。

#### 79. official-feedback-then-proceed（steps）

旁白：把修改集中一次寫完，再按Proceed進入生成。

#### 80. review-is-optional（big）

旁白（承接前句，輕輕帶出新的進度）：產品也保留直接生成的選擇，審查步驟不是強制。

#### 81. outline-lock-after-proceed（big）

旁白：按Proceed後，就不能繼續改這份大綱。

#### 82. review-this-deck-content（table）

旁白：因此像其中一部分、私人投資這些內容，值得在這時確認。

#### 83. account-availability-question（big）

旁白（問句微揚，像在等對方一起判斷）：這個選項，現在每個帳號都看得到嗎？

#### 84. announced-gradual-rollout（stats）

旁白（數字與名稱清楚，句尾自然收住）：Workspace公告列十月十六日起分批推出，最長十五天。

#### 85. announcement-versus-help（compare）

旁白：公告列多類帳號，說明頁卻把共同製作列為Ultra功能。

#### 86. no-account-result-to-resolve（big）

旁白（承接前句，輕輕帶出新的進度）：我沒有帳號操作結果能對齊這個差異，不能保證免費可用。

#### 87. check-your-option（steps）

旁白：你要用產品時，先確認自己的方案和審大綱選項。

#### 88. goal-not-tied-to-menu（big）

旁白（承接前句，輕輕帶出新的進度）：確認自己帳號的審大綱選項後，用同一份需求改寫聽眾和篇幅。

#### 89. adapt-the-same-brief（table）

旁白：把其中的一般同事，改成你的實際聽眾。
旁白：再把頁數和講述時間，改成你要交付的範圍。
旁白（承接前句，輕輕帶出新的進度）：讓大綱帶著問題與來源交回來，你就有具體內容可以修改。

#### 90. write-your-first-page（outro）

旁白：沿用這份需求，寫下你第一頁要回答的問題。
旁白：留言分享，你要把什麼做成簡報。
旁白（承接前句，輕輕帶出新的進度）：訂閱，用真實成品讀懂AI工具。

narrative adf143177bedb0ad
speech 05e0b1bf9dc3cdb4
