# 第三片：近期海外 YouTube／AI formal verification 參考

查詢日期：2026-10-25 UTC。研究窗口以最近30天（2026-09-25–10-25）為主，另標出本週影片、舊講座近期上架、相鄰題與未核完的排程候選。先搜尋了本目錄既有檔案：`verify-research.md`及formal／Theorem來源資料已涵蓋10/22官方研究，但未找到專門的YouTube競品報告，因此本輪只補影片研究。

使用工具：由`ALL_TOOLS`發現`search_service_web_run`，實際搜尋、開啟來源頁及點擊YouTube連結。YouTube多次回覆抓取節流或只返回登入殼；普通未登入HTTP請求也被環境代理403拒絕，未改代理或繞過。沒有登入、付費、下載或觀看影片鏡頭。以下「已觀察」只指實際讀到的標題、metadata、說明欄轉載、官方節目逐字稿或連結；第三方AI摘要不當成我們自己的觀看紀錄，也不用其技術結論替代一手研究。

## 先給選題判斷

最貼本週Claude＋Theorem消息的是 **Hyperautomation Labs** 的第1筆：它也以一個小型demo區分測試與證明，競品重合度高。標題中的「10 Million／36 Seconds」僅記錄對方標題及對方自述，**不是我們重跑的benchmark**。我們應保留自己有限域、SAT、gcc的真實範圍，不能換稱CBMC或Anthropic原研究pipeline。

最有助於把「證明的是規格」講清楚的研究者材料是 **ML Street Talk／Lean創作者** 的第2筆，但日期與標題版本有衝突；若需要有清楚官方日期和可讀官方逐字稿的第二參考，選 **DaaX／Christian Szegedy** 的第4筆。兩者都是背景訪談，不能包裝成10/22新研究發布。

## 六支可定位的近期影片與一支官方排程候選

| # | 真YouTube URL／實際可見標題 | 頻道／關係 | 日期證據 | 片長證據 | 可驗views快照；查詢日均2026-10-25 |
|---|---|---|---|---|---|
| 1 | [Claude Found the Bug 10 Million Tests Missed (in 36 Seconds)](https://www.youtube.com/watch?v=RxGLRbkCjeU) | Hyperautomation Labs；獨立解說，本週直接相關 | [Zolotube轉載頁](https://zolotube.com/watch?v=RxGLRbkCjeU)明列2026-10-23；未讀得YT原頁日期 | **未取得精確片長**；說明欄末章到6:19，不能把章節起點當總片長 | 同一轉載頁本次可見 **4,638**；頁面未另標觀看數快照時間，僅能稱2026-10-25讀頁值，不能稱YT即時值 |
| 2 | [AI Can Write the Proof. Who Checks It? — Leonardo de Moura](https://www.youtube.com/watch?v=ZpQFebTK75A)；另一索引保留舊題名 *The Programming Language That Referees Mathematics — Leo de Moura* | Machine Learning Street Talk；Lean創作者受訪，研究者背景片 | [DS TV](https://www.dutchstartup.ai/en/tv/ai-can-write-the-proof-who-checks-it-leonardo-de-moura)列2026-10-03；[PSI](https://postsingularityinstitute.com/en/syntheses/UCMLtBahI5DMrt0NPvDSoIRQ_ZpQFebTK75A/)列2026-09-29。**日期與題名版本衝突，未由YT原頁裁定** | PSI列 **74 min**，只作分鐘級資料；不是已核實74:00 | PSI列 **18K**，該頁標記2026-10-06；是第三方約數歷史快照，不是本次YT即時數 |
| 3 | [AI Seminar: Learning Programming Abstractions for Automating Formal Verification](https://www.youtube.com/watch?v=aqkcvzdoGuo) | Amii；研究機構官方講座／Jocelyn Qiaochu Chen | [DS TV](https://www.dutchstartup.ai/en/tv/learning-programming-abstractions-for-automating-formal-verification)列影片2026-10-09；[官方研討會紀錄](https://sites.google.com/ualberta.ca/ai-seminar/past-seminars/2026)把原講座列於 **2026-09-11** 並直接連到同YT ID。**舊講座近期上架候選，非10/09新研究** | **未取得** | **未取得**，沒有補造 |
| 4 | [Episode 27 — Verify the Output, Not the Model: Formal Methods and the Future of AI Safety](https://www.youtube.com/watch?v=dii8jSgMr50) | DaaX／Token Drop；Christian Szegedy訪談，官方節目頁及逐字稿 | [DaaX官方頁](https://daax.ai/podcast/episode-27-formal-verification)列 **2026-10-03**；YouTube發布欄本輪未讀得 | 官方列 **約31分鐘**，章節到30:50；不寫成精確31:00 | **未取得** |
| 5 | [Building verification loops in Claude Code](https://www.youtube.com/watch?v=mQZB0l-rhxE) | Claude／Anthropic官方；**相鄰AI coding教學**，不是形式證明發布 | [Post-Cutoff](https://postcutoff.com/v/claude-building-verification-loops/)列 **2026-09-25**，並自述9/29核過YT日期；在30天窗口邊界。[Claude官方影片目錄](https://claude.com/resources/videos)亦有同題名及YT連結 | 第三方列 **3:08**；官方目錄列 **3 min**，分鐘級吻合 | Post-Cutoff列 **349,031，截至2026-10-16**；第三方歷史快照 |
| 6 | [No More Heroes - Terence Tao Talks to Numberphile About AI](https://www.youtube.com/watch?v=bAnwMdfcMVw) | Numberphile；Terence Tao訪談，**相鄰AI數學／證明評論**，不是軟體驗證實作 | [ChronoTube](https://www.chronotube.com/channels/UCoxcjq-8xIDTYp3uz647V5A)列 **2026-10-15 13:58:59 GMT**；[Post-Cutoff](https://postcutoff.com/v/numberphile-terence-tao-no-more-heroes-ai/)同列10/15；實際YT連結返回同標題 | ChronoTube列 **19:45** | 本輪最後開啟Post-Cutoff頁可見 **995,768，截至2026-10-24**。更早快照有929,611（10/21）、956,249（10/22）；不混成同一時點數值 |
| 7 | [Beyond Vibe Coding: Formal Verification for AI-Generated Software](https://www.youtube.com/watch?v=P9xCUmjkPUM) | Microsoft Reactor官方；Carl Kadie／Rust＋Lean，直接相關的**排程／錄影候選** | [Microsoft官方活動頁](https://developer.microsoft.com/en-us/reactor/events/27635/)明列 **2026-10-22 00:30–01:30 UTC**，iframe直接指向該YT ID；**本輪未核實YT發布欄或錄影可播放性** | **未取得實際片長**；活動排程一小時不能當60:00影片 | **未取得** |

## 已讀文字與可採用的編輯推論分開

1. **Hyperautomation Labs：已觀察**轉載的頻道說明欄談10/22研究，並明白揭露自己的例子是刻意放入bug、用CBMC檢查的小demo，和原研究pipeline不同。**編輯推論**：觀眾入口與我們的測試／證明小demo很近，可作競品比較；其測試次數、耗時、checker通過數等只屬對方自述，本輪未重現。題名不證明整支片的技術主張都正確。

2. **ML Street Talk：已觀察**DS TV明確標為「頻道description」的文字及章節，涉及Lean的小kernel、獨立checker、Claude／zlib和人類選擇規格；PSI保留另一題名、日期及約數流量。**編輯推論**：適合解釋trusted checker和spec gap。沒有親自觀看或獨立重現訪談中的zlib、kernel事件；不能直接把該訪談的軟體案例和Anthropic／Theorem的Rocq／RISC-V研究合併。

3. **Amii：已觀察**官方研討會頁摘要談TacMiner與VeriSoftBench，重點是從已有proof重用抽象及衡量模型在真實Lean專案中的表現；直接點官方連結取得帶「AI Seminar」前綴的YT頁標題。**編輯推論**：這是專業背景與模型限制素材，受眾比一般新聞片窄。講座日期與影片索引日期必須分列。

4. **DaaX：已觀察**官方節目頁的日期、約長、同ID嵌入及完整逐字稿。受訪者把輸出驗證、規格撰寫成本和模型整體驗證分開，也承認形式方法仍有規格限制。**編輯推論**：是本輪最清楚可讀的一手訪談文字來源；這些是受訪者的判斷，不是新的實驗benchmark，也不代表xAI或其他任職組織的官方立場。

5. **Claude：已觀察**官方目錄的標題、3分鐘標記，以及關於tests／type checks／linters的簡短介紹。細部內容目前主要由第三方AI摘要轉述，沒有拿其畫面段落當自己的觀看片筆記。**編輯推論**：只能作「日常驗證迴圈」的相鄰教學對照，不應把browser checks、測試或lint直接叫形式證明，更不能說這支9/25教學是10/22新研究消息。

6. **Numberphile：已觀察**YT頁標題、ChronoTube日期／片長，以及第三方頁的歷史view快照。細部影片摘要屬Post-Cutoff的AI整理。**編輯推論**：可看AI數學議題的受眾興趣，不能用它的流量推定軟體形式驗證也會有同樣流量；不採用摘要中的數學突破、論文數等作本片技術事實。

7. **Microsoft Reactor：已觀察**官方活動文案與YT embed：Carl Kadie以RangeSetBlaze為例，介紹AI寫程式、規格及可機器檢查proof的流程。**編輯推論**：官方且高度切題，但本輪只核到活動排程／embed，不能把「將示範」改寫為已觀看完成的成功展示。

## 可直接交給撰稿／選題者的界線

- 已找到六支有真YT URL及可讀題名／描述證據的影片，另有一支官方活動embed候選；沒有宣稱七支皆已完整播放或皆有完整一手metadata。
- 搜尋並未找到可直接核讀的Anthropic／Theorem本週官方研究發布影片。10/22新聞事實仍應回到既有`verify-research.md`中的官方研究與附錄，不從評論影片倒推。
- 流量只記來源頁可見快照；views未取得的條目不補數。不能把第三方轉載讀頁時間冒稱YT統計更新時間。
- 規格、證明、SAT、SMT、Rocq、Lean、CBMC與測試各自保留名稱；我們自己的有限域demo不是任何競品或廠商研究的重現。

本輪只建立本檔，未修改影片、repo、聲音或其他研究檔。
