# A01 輪子行李箱：離線敘事續稿 — HOLD

本資料夾是 `story-rolling-suitcase-v2` 的新隔離候選，基於正式機**唯讀** `snapshot-104` 與前一版已凍結的 manifest `806FB892C40FDCEC61280CBF6FB66BC8DD8B19BA208006FB0E2BB094D6EEB8D0`。前版候選與更早的 `A391F721…85F42` 均保持原狀；兩份對 806 精確 bytes 的獨立 **HOLD** 理由分別保存於 [`review-baseline-806/retention-HOLD.md`](review-baseline-806/retention-HOLD.md) 和 [`review-baseline-806/source-HOLD.md`](review-baseline-806/source-HOLD.md)。新版沒有繼承任何 PASS。

## 聽眾會跟著哪件事

- 開場先聽到 Sadow 提著兩只沉箱，旁邊重機器卻滑過；輪板到第三句才露出。另以 Anita 被丈夫取笑後是否續用、百貨是否真的進貨、機師車庫會做出什麼箱型作三個**不同後段事件**的預告。人物、樣品及決定未在畫面 prompt 裡提早揭示。
- Anita 的 1921 年首次窮遊：每到新地方，丈夫找廉價住處，她與四個孩子在車站守著行李。**另起 1928 年第二趟旅程**，兒子先改好輪子箱才出發；丈夫取笑後，她仍在旅後巡講帶著箱子。沒有她影響 Sadow 的證據。
- Sadow 因自己的重箱與機場輪板而試作，帶樣品赴紐約卻被拒。耶魯教授轉述學生助理電話問得的「已有搬運工」反對理由；Macy 副總裁親手拉過才叫回採購。教授本人用過一只四輪拖帶箱，趕路時會左右擺；另一堂課則談到這類舊式設計轉彎可能翻倒。前者是**個人使用經驗**，後者是**課堂概述**；不說 Plath 曾用那只箱，也不推論所有箱都如此。
- 同機師 Emmer 未標年份的舊機組袋／草圖被婉拒，只留四鏡並放在另一份 Plath 安檢回憶之前，明示無法確定兩件事先後。Plath 對安檢員的「好」是他自己受訪回憶；Travelpro 的 1987 車庫 Rollaboard 則是公司敘述。後續讓同機師請他製作、機組採用、旅客看見、需求迫使搬倉與 1991 年轉全職接續人物線。
- 前版後半六鏡 Samsonite Piggyback 1986–1990 倒帶移出**口播**，只留來源註；1997 四輪及「好推但仍有重量」作短尾聲。Samsonite、Sadow、Plath 之間不主張技術傳承。

`candidate/video.json` 的 **9 組待審回路**皆跨鏡，三個開場 setup/payoff 是 `r17h01→r12o03`、`b6mn→76ur`、`jtmg→3zwf`。其餘見 `source-map.json` 的逐組來源與動作結果；最短估計 payoff 間隔為 10.6 秒，三個開場後段間隔分別 64.7、174.8、294.1 秒（300 CPM）。這只表示稿面沒有九組「下一句答」的假懸念；**畫面與盲聽尚未驗**，不可當留存率 PASS。事件代理在 300 CPM 還有最長 123.4 秒的空檔，未靠加問號填補。

## 來源與邊界

- [Winnetka 歷史學會的 1921 首旅記錄](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)與[1928 輪子箱記錄](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)分開使用；畫素描換餐宿的細節另見[館方家族簡史](https://www.winnetkahistory.org/who-were-the-burnhams/)。1933 遊記原頁尚未直接核閱，館方敘述在口播就地歸屬。
- [ABC 2010 Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)支撐機場、樣品與 Macy 行動；[RNPA《Contrails》印刷第 48 頁](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)重印的 Joe Sharkey 訪談支撐其當時任麻州行李／外套公司副總裁，取代前版 `i37` 錯配的維基來源。[耶魯 2008](https://oyc.yale.edu/economics/econ-252-08/lecture-3)記錄 Shiller 的轉述與個人箱子經驗；[2011 課堂](https://oyc.yale.edu/economics/econ-252-11/lecture-3)是舊式設計轉彎可能翻倒的概述，並非第二次個人實測。講課中不準確的「首創／年份」不引用。Sadow 的[專利](https://patents.google.com/patent/US3653474A/en)只支撐提案，不能當市售實測。
- [ABC／USA TODAY 2012 Plath 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)、[Plath 專利](https://patents.google.com/patent/US4995487A/en)、[Travelpro 沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)是不同證據類型；1989 專利不能倒推 1987 車庫原型逐件規格。[Emmer 第一人稱回憶印刷頁 46–47](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)未標年份，舊機組輪子袋不等於安檢用的獨立金屬推車。
- 候選視覺移除 Sadow 裝輪子的「螺絲」動作、館員觸碰 Anita 館藏、車庫箱子堆到天花板與未記錄的旅客表情；仍須真正圖片審查。全部播出主張在 `candidate/claims.md` 是 **PENDING**。

## 機械檢查與片長

在儲存庫根目錄執行 `node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-story-depth-candidate-20261018/build.mjs --check`。建置核對唯讀 base 檔 SHA、逐句來源前文、分鏡文字、場景／主張／回路 ID，並將輸出和本 README 綁到 `manifest.json`。新候選有 **63 鏡、73 句、1,732 口語單位**；`lintVideo` 0 error，cute 視覺 lint 0 error。所有時間都是文字估算，**沒有實際 TTS、圖片、動態、剪輯或播放器驗證**。

| 估計語速 | 六章旁白 | 距 540 秒下限 |
| --- | ---: | ---: |
| 250 單位／分鐘 | 483.4 秒 | 差 56.6 秒 |
| 275 單位／分鐘 | 445.9 秒 | 差 94.1 秒 |
| 300 單位／分鐘 | 413.2 秒 | 差 126.8 秒 |

正式 `story.mjs checkLength()` 的 cute 10 分鐘帶是**六章 timeline 540–660 秒**（含 hook/outro 旁白；不含外加片頭／片尾動畫）。原試音曾接近 300 CPM；即使按 250 CPM，新版也低於正式下限。刪除拖慢主線的平行商品史後，目前一手人物事件不足以自然補滿十分鐘。**不以慢播、重複專利機構、空鏡或捏造交易補時。** 下一個內容抉擇應是再找到與三位主角直接相關、可核驗且有因果的新事件，或重新評估本題的片長規格；兩者都要經獨立事實與盲聽審核。

正式機的來源是六個 `story/chapters/*.json`，不是本候選的合併 `video.json`。跨章 ID、claim、thumbnail、loop 與 `candidate/series.json` 的大綱仍是 `source-map.json` 所列 **SPEC_ONLY** 遷移，不能直接匯入。未寫正式審稿收據、未更動正式章稿／主機／媒體／付費工作；**狀態維持 HOLD**。
