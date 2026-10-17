# verify-2: ai-agent-vs-chatbot — 第二輪逐句獨立來源複核

查核日：2026-10-07；收據寫入UTC：2026-10-07T11:19:25.424Z。查核者未撰寫此片；本輪讀142句、36場景全部data、sources、YouTube title/description/tags與thumbnail，並核對claims、demo-log、brief及verify-1。編輯者root已套用兩句與一個歷史字卡標題的修正；本查核者只寫本檔，沒有修改brief、video或i18n，沒有付費、核准或執行製作。

## 方法與判定界線

官方外部事實以今天實際GET成功的原頁為準；本輪四個指定primary URL全部HTTP200，沒有以搜尋摘要替代。HTML保存與可重算文字擷取都有SHA。工作方式的定義沿用Anthropic工程分類，不能變成對全部商用產品的正式分類或性能保證。建議、提問、自製示意與製作聲明標OUT OF SCOPE，並逐句說清邊界；這個標記不代表它们已取得外部事件確證。CHANGED表示本輪要求的修正已套用並逐字核對，並非待改。

2026-09-27查詢與2026-09-28行程是L1的既有repo歷史紀錄。本輪2026-10-07依次讀一般時間、地址與年度公告，可重現一般週一規則與指定日期例外的比較；不能將新GET冒充9/27原request的確證。沒有原9/27不可改寫HTTP、模型工具呼叫或產品錄影，也沒有證明旅客實際到訪／入館／付款。公告的Open是安排，與實際營運、完成預約及owner接受不同。

## 來源及metadata

私有保存path以下一律以`<home>`表示使用者家目錄，沒有憑證或私人識別紀錄。所有頁面的requested/retrieved UTC、response body bytes/hash及提取方式完整保留於`<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/collection.json`。text擷取演算法：HTMLParser排除comment/script/style/noscript，解碼字元、逐文字節點壓縮空白，以UTF-8/LF保存。全頁擷取hash包括導覽／頁尾；不是宣稱動態頁HTML永久不變。

| ID | URL／title／publisher | HTTP | access UTC | text extraction SHA-256 |
| --- | --- | ---: | --- | --- |
| S1 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)；Anthropic | 200 | 2026-10-07T10:50:35.553Z | `900c44e2f04d8d0a17ce0138c6e5ba704b4e7040820c38646ea0d1ca7aedc0f4` |
| S2 | [國立臺灣博物館-開放時間與票價](https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444)；國立臺灣博物館 | 200 | 2026-10-07T10:50:36.146Z | `9047834e8bce08b42157c3ae6e38163552c4ae7fb93771189fec37901fd56956` |
| S3 | [NTM Opening and Closing Dates for Holidays and Commemorative Days in Year 2026](https://www.ntm.gov.tw/en/News_Content.aspx?n=5713&s=251424)；National Taiwan Museum | 200 | 2026-10-07T10:50:41.115Z | `21488406f032aa436a3114d254c4f4c792cc4b09362083bbe7d557c544afc93a` |
| S4 | [國立臺灣博物館-交通資訊](https://www.ntm.gov.tw/cp.aspx?n=5445)；國立臺灣博物館 | 200 | 2026-10-07T10:50:38.710Z | `b26081992739a21927887c61a4d445391cb5ffd8008bceec32cd3d86a9403796` |
| S5 | [AI 代理（AI Agent）是什麼：從回答問題到完成任務](https://mokaair.com/zh-TW/life/ai-agents-explained)；Mokaair | 200 | 2026-10-07T10:50:36.409Z | `0db0a796d4c7e9d404a1d4aa87001cfb06eba679b6be2d0e7b8b82a0fa75e9b7` |

| ID | 原HTML保存path | bytes | 原HTML SHA-256 |
| --- | --- | ---: | --- |
| S1 | `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/sources/anthropic-effective-agents.html` | 174660 | `dd21017fd0dd6b72f020bbeaf69a3faf2ba7246c447144f452a34200e51ec3fe` |
| S2 | `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/sources/ntm-hours.html` | 143207 | `b3477bef03781b7147b1f8a5ed25ded0cb1545e393a67f2cb23c5b592ee21653` |
| S3 | `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/sources/ntm-2026-holidays.html` | 97852 | `02c414a7607f8af3f3f498b13d2b93fa89c71196e364fa334dcb174d64d888a9` |
| S4 | `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/sources/ntm-main-address.html` | 142729 | `2d615b7e8b789f1e42e0cdfac64b16ad62177eedd287c978c97e543b4b7563f3` |
| S5 | `<home>/mokaair-work/ai-teaching-continuation-20261007/next-agent-source-audit/sources/mokaair-source-article.html` | 476866 | `ef71a6edbf5bd485652538bfa0cff398537e9852c61c74a6e52260d83057916c` |

S1顯示發布日2024-12-19，並有工具環境已改變的更新提醒；目前核心workflow／agent定義仍支持本片，片中沒有宣稱當前SDK或模型版本。S3顯示日期2026-03-03，不等於access UTC；其9/28列為Monday／Teacher’sDay／Open。S2一般時段09:30–17:00與週一休館、假日例外並存。S4本館地址為襄陽路2號、二二八和平公園內，目前另有M5約10分鐘的館方交通建議；這不是本次實測。沒有9/27頁面hash，因此不宣稱這些文字是在9/27後新增。S3另有未被本片引用的9/25星期疑點，不用它外推本片9/28結論。

S5是另外實读HTTP200的站內自有文章，可驗ag073及延伸閱讀本文存在，不能替代S1–S4官方外部事實。本輪web工具第一次讀本站報Internal Error，之後本地公開GET200且保存全文；不隱去這個讀取差異。实际上架包第一行還需package後核對，不能把source_guide等同已完成上架包。

L1：本目錄demo-log.md；L2：claims.md；L3：brief.md；L4：verify-1.md。它們是repo文稿紀錄，非第三方頁面，也非不可改寫runtime證據。L1所載臺北市觀光局403只作當時製作聲明，本輪沒有新讀該頁，沒有將其當作今日HTTP證據。

## 142句逐句核對

| # | 句ID／scene | 目前text（say） | 判定 | source | 具體核對與限制 |
| ---: | --- | --- | --- | --- | --- |
| 1 | ag001 / hook | 它說幫你排行程，到底查過資料了嗎？；無say | OUT OF SCOPE | — | 開場問題，不是已執行工具或產品能力的聲明。 |
| 2 | ag002 / hook | 拿一個週一去博物館的任務，就能看出差別。；無say | OUT OF SCOPE | S2/S3 | 導入有週一例外的歷史示範；不是今天的出遊建議。 |
| 3 | ag003 / hook | 看到最後，你會有一張能自己使用的交辦清單。；無say | OUT OF SCOPE | 本稿 task-recipe | 教學交付承諾；同稿四欄交辦式可供使用，不是外部事實。 |
| 4 | ag004 / pretty-answer | 先看最常見的一種：你打一行問題，它回一份清單。；無say | OUT OF SCOPE | 本稿 pretty-answer | 自製常見情境描述；「常見」未當成市場佔比或特定產品測量。 |
| 5 | ag005 / pretty-answer | 清單可能很順，也可能完全沒有查開館日。；無say | OUT OF SCOPE | 本稿 pretty-answer | 可能漏查的假設例，不是實測模型輸出。 |
| 6 | ag006 / pretty-answer | 這段回答是我們做的教學範例，沒有錄製任何產品畫面。；無say | OUT OF SCOPE | L1/本稿 | 製作紀錄與稿件的示意聲明一致；不能據此獨立證明所有歷史製作動作。 |
| 7 | ag007 / pretty-answer | 它提供想法，但目前還沒有可驗收的行程。；無say | OUT OF SCOPE | 本稿 pretty-answer | 按片中自訂驗收標準評價這份示意清單，沒有宣稱真實訂單。 |
| 8 | ag008 / three-modes | 聊天回答，下一步還是由你自己去做。；無say | OUT OF SCOPE | S1 | 僅此處「只回答」的教學模式；後文ag103–106保留聊天介面可用工具，不外推所有聊天產品。 |
| 9 | ag009 / three-modes | 固定流程則照預先寫好的路徑，逐項處理。；無say | CONFIRMED | S1 | 與官方的預先寫好程式路徑workflow定義相符。 |
| 10 | ag010 / three-modes | 代理會看工具回來的資訊，再決定下一步。；無say | CONFIRMED | S1 | 與官方模型依環境／工具回饋選擇流程的agent定義相符。 |
| 11 | ag011 / three-modes | 三者沒有誰一定比較高級，關鍵是工作需求。；無say | OUT OF SCOPE | S1 | 按需求選架構的工程建議；没有絕對高低或量化性能保證。 |
| 12 | ag079 / fixed-example | 例如每個月整理同一張表，欄位都相同。；無say | OUT OF SCOPE | 本稿 fixed-example | 每月同欄位報表是自製假設任務，沒有實測模型。 |
| 13 | ag080 / fixed-example | 程式照預設條件輸出報表，可能比代理更穩。；無say | OUT OF SCOPE | S1 | S1建議已知任務用workflow；「可能」是工程建議，不是已測性能比較。 |
| 14 | ag081 / fixed-example | 別因為現在流行代理，就把每件小事都交給它猜。；無say | OUT OF SCOPE | S1 | 按需求避免不必要複雜度的編輯建議，「流行」未當數量或時事主張。 |
| 15 | ag082 / fixed-example | 先看路徑會不會變，再決定需不需要彈性。；無say | OUT OF SCOPE | S1 | 按固定路徑或彈性需求選架構的建議。 |
| 16 | ag111 / no-tool-case | 沒有查網頁工具的助理，看不到博物館的新公告。；無say | CONFIRMED | S1/L1 | 限於本示範沒有其他公告輸入的助理；若使用者提供新公告，不能泛稱仍無法取得內容。 |
| 17 | ag112 / no-tool-case | 它可以幫你想路線，開放日期仍要另外查證。；無say | OUT OF SCOPE | S2/S3 | 開放日期需要来源的建議，路線仍为草案。 |
| 18 | ag113 / no-tool-case | 這不是它說話不夠聰明，而是工具範圍不同。；無say | OUT OF SCOPE | S1 | 工具範圍與口語流暢度分開的解說，不是智力測試。 |
| 19 | ag114 / no-tool-case | 選工具前，先弄清楚它能讀什麼、能做什麼。；無say | OUT OF SCOPE | S1/S5 | 先確認讀取及動作範圍的建議。 |
| 20 | ag012 / interface-trap | 有聊天框，不代表背後只會聊天。；無say | CONFIRMED | S1 | 官方客服案例可同時有聊天介面、工具與對外動作；介面本身不足以分类架構。 |
| 21 | ag013 / interface-trap | 同樣地，畫面寫著代理，也不保證它真的做完。；無say | OUT OF SCOPE | S1 | 提醒看執行結果；沒有宣稱某產品已失敗或必然成功。 |
| 22 | ag014 / interface-trap | 你要看的是：它用了什麼工具，拿到了什麼結果。；無say | OUT OF SCOPE | S1 | 驗收提問，對照實際工具結果的建議。 |
| 23 | ag015 / interface-trap | 然後問，結果有沒有改變它後面的做法。；無say | OUT OF SCOPE | S1 | 依回饋檢查後續決策的驗收建議。 |
| 24 | ag083 / tool-result | 光是回答說我查過，還不足以當證據。；無say | OUT OF SCOPE | S1/本稿 tool-result | 文字不等於執行證據的驗收立場。 |
| 25 | ag084 / tool-result | 最好能看到讀了哪一頁，得到哪一項結果。；無say | OUT OF SCOPE | S1/本稿 tool-result | 提供來源與結果的建議。 |
| 26 | ag085 / tool-result | 接著看它有沒有因為結果修正草案。；無say | OUT OF SCOPE | S1/本稿 tool-result | 依結果修正草案的驗收建議。 |
| 27 | ag086 / tool-result | 如果沒有，使用者還是得自己補完查核。；無say | OUT OF SCOPE | 本稿 tool-result | 缺少證據時使用者需補驗的建議，不是測得必然負擔。 |
| 28 | ag016 / task-spec | 這次我給一個不含個資的公開資料任務。；無say | OUT OF SCOPE | L1/本稿 | 歷史任務範圍声明；交付稿件不含旅客識別資料，不證明未記錄的外部行為。 |
| 29 | ag017 / task-spec | 替旅客排台北車站附近的半日博物館散步。；無say | OUT OF SCOPE | L1/S4 | 歷史示範的任務目標；不是已走過的實際路線。 |
| 30 | ag018 / task-spec | 這是歷史示範：二〇二六年九月二十七日查詢，規劃九月二十八日。；無say | CHANGED | L1/S3 | 已套用歷史標示：9/27查詢日來自既有紀錄，9/28為規劃日期；目前讀頁不能確證原9/27請求。 |
| 31 | ag019 / task-spec | 只查官方公開頁，不預約，也不付款。；無say | OUT OF SCOPE | L1 | 沿用紀錄的只讀、無預約付款邊界，非第三方可證的執行事件。 |
| 32 | ag115 / task-not-question | 一句台北有什麼好玩，適合找靈感。；無say | OUT OF SCOPE | 本稿 task-not-question | 問題提示的假設示例，不是產品錄影。 |
| 33 | ag116 / task-not-question | 但要交付可用行程，就得補上日期和範圍。；無say | OUT OF SCOPE | L1/本稿 task-not-question | 任務規格要有日期範圍的建議。 |
| 34 | ag117 / task-not-question | 還要講清楚，哪些事需要證據。；無say | OUT OF SCOPE | 本稿 task-not-question | 指定證據需求的建議。 |
| 35 | ag118 / task-not-question | 交辦越明確，最後越容易判定有沒有完成。；無say | OUT OF SCOPE | 本稿 task-not-question | 交辦明確有助驗收的編輯判斷，沒有量化研究結論。 |
| 36 | ag020 / success-rule | 完成標準也要先講，不然一句排好了很難檢查。；無say | OUT OF SCOPE | 本稿 success-rule | 先定完成標準的編輯建議。 |
| 37 | ag021 / success-rule | 我要它列出地點、順序和館方的開館證據。；無say | OUT OF SCOPE | L1/S2/S3 | 自訂交付欄位，來源可核對，但不表示实际已入館。 |
| 38 | ag022 / success-rule | 交通與天氣沒有確認，就直接標出待查。；無say | OUT OF SCOPE | L1 | 交通與天氣待查的處理規則；未捏造分鐘或預報。 |
| 39 | ag023 / success-rule | 這些欄位，比看它的語氣有多自信更有用。；無say | OUT OF SCOPE | 本稿 success-rule | 驗收偏好，不是有量化證據的品質比較。 |
| 40 | ag087 / privacy-boundary | 我們不需要真實姓名、電話或住宿訂單。；無say | OUT OF SCOPE | L1/本稿 privacy-boundary | 本示範不需要旅客識別資料，稿件輸入欄位符合。 |
| 41 | ag088 / privacy-boundary | 只用公開的日期、地點和目標，就能示範完整流程。；無say | OUT OF SCOPE | L1 | 公開日期地點足以示範這份教學任務，不泛稱全部旅行工作。 |
| 42 | ag089 / privacy-boundary | 也沒有讓代理登入旅客帳號。；無say | OUT OF SCOPE | L1 | 無登入的歷史紀錄聲明，未独立查帳戶存取。 |
| 43 | ag090 / privacy-boundary | 先用低風險任務練習，更容易看清它的能力。；無say | OUT OF SCOPE | S1/S5 | 低風險起步的編輯建議，沒有量化安全保證。 |
| 44 | ag024 / first-rule | 我先打開博物館的開放時間頁。；無say | OUT OF SCOPE | L1/S2 | 只按既有製作紀錄核對查詢敘事；不是9/27原始HTTP證據。 |
| 45 | ag025 / first-rule | 一般規則很清楚：每週一休館。；無say | CONFIRMED | S2 | 本館一般週一休館，與官方目前規則一致。 |
| 46 | ag026 / first-rule | 如果查到這裡就停，這天的行程會被排除。；無say | OUT OF SCOPE | S2/S3 | 只讀一般規則會排除博物館的示範推論，不宣稱模型真的如此決策。 |
| 47 | ag027 / first-rule | 這份官方頁面也提醒，國定假日可能正常開放。；無say | CONFIRMED | S2 | 官方明列國定假日及連續假期照常開館；片中「可能」沒有保證任一指定日。 |
| 48 | ag028 / next-check | 這就是需要回饋的轉折。；無say | OUT OF SCOPE | S2/S3 | 示範轉折的編輯解說。 |
| 49 | ag029 / next-check | 我沒有直接把週一休館貼進答案。；無say | OUT OF SCOPE | L1 | 沿用紀錄的研究敘事；没有不可改寫原始請求證明當年動作。 |
| 50 | ag030 / next-check | 看到例外規則，下一步改成查當年的開閉館公告。；無say | OUT OF SCOPE | L1/S2/S3 | 紀錄所述補查方法可在今天比較重現；不驗證原模型的內部選路。 |
| 51 | ag031 / next-check | 這一步是實際查詢，不是模型憑印象補一句。；無say | OUT OF SCOPE | L1/S2/S3 | 「實際查詢」只屬repo歷史紀錄的聲明；今日確實讀到兩頁，不將兩者混成同一執行。 |
| 52 | ag119 / tool-trace | 這不是畫一條想像中的代理流程。；無say | OUT OF SCOPE | L1/S2/S3 | 實際查詢的來源是既有repo紀錄；目前頁面支持其內容，未確證舊模型工作流程。 |
| 53 | ag120 / tool-trace | 製作時真的先開一般時間頁，再開年度公告。；無say | OUT OF SCOPE | L1/S2/S3 | 先一般頁、後年度公告是既有紀錄的順序；今天依序讀取重現比較，不能當9/27原請求確證。 |
| 54 | ag121 / tool-trace | 每一步拿到的結果，放在同一張表讓你核對。；無say | OUT OF SCOPE | 本稿 tool-trace/S2/S3 | 重建查詢表可核對資料內容，不把字卡當原生工具trace或產品錄影。 |
| 55 | ag122 / tool-trace | 它沒有替任何旅客按鈕，也沒有登入個人帳號。；無say | OUT OF SCOPE | L1 | 無按旅客按鈕或登入的紀錄声明，不以公開頁證明帳戶行為。 |
| 56 | ag032 / exception | 當年公告真的列出了這個日期。；無say | CONFIRMED | S3 | 2026年度公告仍明列September28的日期。 |
| 57 | ag033 / exception | 九月二十八日雖然是週一，教師節照常開館。；無say | CONFIRMED | S3 | 2026-09-28(Mon)/Teacher’sDay/Open為館方公告安排；不是觀測當天營運。 |
| 58 | ag034 / exception | 所以原本的週一休館判斷，對這一天不成立。；無say | CONFIRMED | S2/S3 | 按公告比較，一般週一休館不適用此指定日；只驗公告推論。 |
| 59 | ag035 / exception | 畫面上的英文只節錄必要的一行，來源放說明欄。；無say | OUT OF SCOPE | S3/本稿 sources | quote字卡英文與公告一列一致；来源已列稿件，实际產出說明欄仍待package檢查。 |
| 60 | ag091 / exception-context | 一般規則和節日公告，不是互相矛盾。；無say | CONFIRMED | S2/S3 | 一般週一規則與指定節日例外可同時成立。 |
| 61 | ag092 / exception-context | 前者講平常的週一，後者講指定日期。；無say | CONFIRMED | S2/S3 | 兩頁資訊適用範圍不同，符合目前原文。 |
| 62 | ag093 / exception-context | 如果只摘一句週一休館，就會漏掉例外。；無say | CONFIRMED | S2/S3 | 單摘週一規則確會漏掉S3列出的指定日Open。 |
| 63 | ag094 / exception-context | 這也是為什麼來源要對到你問的那一天。；無say | OUT OF SCOPE | S2/S3 | 來源對日期的驗收建議。 |
| 64 | ag036 / change-decision | 你看到的不是多放一個連結而已。；無say | OUT OF SCOPE | 本稿 change-decision | 解說證據應影響決策的教學立場。 |
| 65 | ag037 / change-decision | 新資料讓行程草案做了實質修改。；無say | OUT OF SCOPE | L1/S2/S3 | 草案修改來自歷史紀錄與目前可重現的推論，不確證原9/27代理動作。 |
| 66 | ag038 / change-decision | 原本要刪掉博物館，現在可以保留。；無say | CONFIRMED | S2/S3 | 在該歷史日期的草案中可保留博物館，並未將今日日期當成9/28。 |
| 67 | ag039 / change-decision | 這才是依工具回饋調整下一步的意思。；無say | CONFIRMED | S1/S2/S3 | 作為回饋選下一步的教學解釋，與S1工程模式相符；未證明特定產品實作。 |
| 68 | ag123 / specific-date | 這裡還有一個容易犯的錯。；無say | OUT OF SCOPE | 本稿 specific-date | 轉場提醒，不是外部事實。 |
| 69 | ag124 / specific-date | 九月二十八日開館，不代表所有週一都開。；無say | CONFIRMED | S2/S3 | 9/28的Open只适用该日期，不能推出全部週一開館。 |
| 70 | ag125 / specific-date | 交付物要保留日期和館名，不能只寫週一可去。；無say | OUT OF SCOPE | S2/S3 | 保留日期館名的編輯建議。 |
| 71 | ag126 / specific-date | 旅行資訊常有這種例外，出發前要再核一次。；無say | OUT OF SCOPE | S2/S3 | 旅行例外与出發前核對的建議，未主張例外的統計頻率。 |
| 72 | ag040 / route | 交付物是一份可以回頭檢查的草案。；無say | OUT OF SCOPE | L1 | 明稱交付物為草案，沒有冒充已完成預訂。 |
| 73 | ag041 / route | 從台北車站附近出發，先到臺博館本館。；無say | CONFIRMED | S4/L1 | 台北車站至本館是館方交通頁提及的出發範圍；本片不承諾接駁分鐘或实測。 |
| 74 | ag042 / route | 接著是二二八和平公園，作為附近的戶外停留點。；無say | CONFIRMED | S4/S2 | 本館地址頁尾位於二二八和平公園內，草案安排附近戶外停留有位置依據。 |
| 75 | ag043 / route | 這個順序是草案，不冒充現場導航結果。；無say | OUT OF SCOPE | L1 | 明確限定草案與未實測導航，保留。 |
| 76 | ag095 / source-trace | 你也能逐格拆開這份行程。；無say | OUT OF SCOPE | 本稿 source-trace | 將草案按欄位核對的教學方法。 |
| 77 | ag096 / source-trace | 能否入館看節日公告，地點則看博物館的地址頁。；無say | CONFIRMED | S3/S4 | 公告核對日期、地址頁核對地點的方法有明確對應。 |
| 78 | ag097 / source-trace | 館方有步行建議，但我們未實測，也沒查天氣。；無say | CHANGED | S4/L1 | 已承認館方步行建議；未實測與未查天氣仍僅按歷史紀錄核對，沒有實測時長。 |
| 79 | ag098 / source-trace | 所以它們應該留白，不該變成漂亮的假數字。；無say | OUT OF SCOPE | S4/L1 | 「留白」针对未實測实际分钟與未知天氣，不否認可引用且應標來源的館方約10分鐘建議。 |
| 80 | ag127 / three-evidence-levels | 你可以把代理交付的資訊分三層。；無say | OUT OF SCOPE | 本稿 three-evidence-levels | 三層是此片自訂資訊整理法。 |
| 81 | ag128 / three-evidence-levels | 已查到的，附上原始來源。；無say | OUT OF SCOPE | 本稿 three-evidence-levels | 已查項附原始來源的建議。 |
| 82 | ag129 / three-evidence-levels | 依來源推論的，明講這是一份草案。；無say | OUT OF SCOPE | 本稿 three-evidence-levels | 推論標草案，保留非實測界線。 |
| 83 | ag130 / three-evidence-levels | 沒有查到的，就列待查，別擠進已確認欄。；無say | OUT OF SCOPE | 本稿 three-evidence-levels | 未知不擠入已確認的編輯要求。 |
| 84 | ag044 / not-done | 真正能用的交付物，還要寫明沒有做什麼。；無say | OUT OF SCOPE | 本稿 not-done | 交付應寫出未完成項目的建議。 |
| 85 | ag045 / not-done | 這次沒有實測步行時間，也沒有查天氣。；無say | OUT OF SCOPE | L1 | 未實測步行與未查天氣的製作聲明；目前館方估計並不改變此未實測範圍。 |
| 86 | ag046 / not-done | 沒有訂票，當然也沒有付款。；無say | OUT OF SCOPE | L1 | 無訂票付款為既有紀錄聲明，不藉來源頁證實外部帳戶事件。 |
| 87 | ag047 / not-done | 把待查寫出來，是完成品質的一部分。；無say | OUT OF SCOPE | 本稿 not-done | 品質立場，不是量化研究結論。 |
| 88 | ag099 / hand-check | 驗收不用把它做過的事全部重做一遍。；無say | OUT OF SCOPE | 本稿 hand-check | 抽查策略的建議，未聲稱可以省略高風險查驗。 |
| 89 | ag100 / hand-check | 先抽查最影響行程的資訊，像是開館日。；無say | OUT OF SCOPE | S2/S3 | 將開館日列為優先核對項的建議。 |
| 90 | ag101 / hand-check | 確認館名、日期和來源頁真的對得起來。；無say | OUT OF SCOPE | S2/S3/S4 | 館名日期來源逐項核對的建議；不是本人已入館的聲明。 |
| 91 | ag102 / hand-check | 出發前再查當日公告，避免資訊過期。；無say | OUT OF SCOPE | S2/S3 | 未來實際出發前重查的通用建議，不把歷史9/28當成未來。 |
| 92 | ag131 / deliverable-shape | 結果最好讓下一個人接得下去。；無say | OUT OF SCOPE | 本稿 deliverable-shape | 可接手交付的編輯標準。 |
| 93 | ag132 / deliverable-shape | 先看順序，再看每一站的來源。；無say | OUT OF SCOPE | S2/S3/S4 | 逐站核對來源的方法建議。 |
| 94 | ag133 / deliverable-shape | 狀態要分清已確認和待確認。；無say | OUT OF SCOPE | 本稿 deliverable-shape | 狀態分類的建議，非實際工作全部完成的聲明。 |
| 95 | ag134 / deliverable-shape | 最後列出人要做的下一步，而不是只說完成。；無say | OUT OF SCOPE | 本稿 deliverable-shape | 人員下一步清單的建議。 |
| 96 | ag048 / fixed-flow | 等等，固定流程也能查兩個頁面啊。；無say | CONFIRMED | S1 | 預設workflow也可包含多工具查詢，並非只有agent可讀兩頁。 |
| 97 | ag049 / fixed-flow | 沒錯。若例外規則都寫好，固定流程也能可靠完成。；無say | OUT OF SCOPE | S1 | 已知規則適合workflow的工程建議；可靠不是實測成功率或零錯誤保證。 |
| 98 | ag050 / fixed-flow | 代理的差別，是模型可依回饋選下一步。；無say | CONFIRMED | S1 | 模型动态决定流程及工具，與官方定義相符。 |
| 99 | ag051 / fixed-flow | 這不是一場工具高低排名。；無say | OUT OF SCOPE | S1 | 表明非優劣排名，保留。 |
| 100 | ag103 / chat-can-use-tools | 有人會問，我平常的聊天工具也能打開網頁啊。；無say | OUT OF SCOPE | S1 | 觀眾假設問題，沒有點名或測試當前商用產品。 |
| 101 | ag104 / chat-can-use-tools | 對，所以不能用有沒有聊天框來分類。；無say | CONFIRMED | S1 | 官方客服agent案例含聊天介面與工具，支持介面不是分類依據。 |
| 102 | ag105 / chat-can-use-tools | 一次工具查詢，也不等於整個任務都自動完成。；無say | OUT OF SCOPE | 本稿 chat-can-use-tools | 工具查詢與整份交付不同的驗收建議。 |
| 103 | ag106 / chat-can-use-tools | 看它能否持續推進、修正，並交出可查結果。；無say | OUT OF SCOPE | S1 | 持續推進與交付的自訂驗收規格，不保證所有代理都做到。 |
| 104 | ag135 / autonomy-spectrum | 不是一開代理，就要它從頭到尾自己做主。；無say | OUT OF SCOPE | S1/S5 | 自主度可分階段的設計建議，不宣稱所有產品都能如此設定。 |
| 105 | ag136 / autonomy-spectrum | 你可以先只給讀資料和做草稿的能力。；無say | OUT OF SCOPE | S5 | 先讀資料與草擬的授權建議。 |
| 106 | ag137 / autonomy-spectrum | 等你看過成果，再決定要不要開更多動作。；無say | OUT OF SCOPE | S5 | 增加動作前由人決定的建議。 |
| 107 | ag138 / autonomy-spectrum | 對外送出或付費的步驟，先讓它停下來問。；無say | OUT OF SCOPE | S1/S5 | 對外／付費前停下的編輯要求，不是本審查給予此授權。 |
| 108 | ag052 / tool-boundary | 模型可以要求查資料，但不會憑一句話創造權限。；無say | OUT OF SCOPE | S1/S5 | 工具與授權需由系統提供的建議，沒有聲稱模型能自行增加帳戶權限。 |
| 109 | ag053 / tool-boundary | 這次它能讀公開頁，不代表能進你的帳號。；無say | OUT OF SCOPE | L1/S5 | 示範只讀範圍不等於帳戶能力；不是對所有助理設定的獨立審核。 |
| 110 | ag054 / tool-boundary | 如果它說已經訂好，卻沒有訂單，請視為未完成。；無say | OUT OF SCOPE | S5 | 要求訂單證據的驗收規則，非存在某訂單的事實。 |
| 111 | ag055 / tool-boundary | 文字敘述和外部世界的狀態，要分開核對。；無say | OUT OF SCOPE | S5 | 敘述與外部狀態分開驗證的編輯建議。 |
| 112 | ag056 / handoff-check | 驗收時，我會問三個問題。；無say | OUT OF SCOPE | 本稿 handoff-check | 三個問題為片中明示的自訂清單。 |
| 113 | ag057 / handoff-check | 第一，工具有沒有真的取得資料。；無say | OUT OF SCOPE | S1/本稿 | 驗收提問，不表示工具已完成。 |
| 114 | ag058 / handoff-check | 第二，新資訊有沒有改變下一步。；無say | OUT OF SCOPE | S1/本稿 | 回饋是否影響決策的驗收提問。 |
| 115 | ag059 / handoff-check | 第三，最後那份東西能不能逐項核對。；無say | OUT OF SCOPE | 本稿 handoff-check | 交付是否可核對的提問。 |
| 116 | ag060 / failure-state | 如果官方頁打不開，代理不該自己猜一個時間。；無say | OUT OF SCOPE | S5 | 官方頁不可讀時不猜時間的建議；此次四頁均可讀，非報告已發生故障。 |
| 117 | ag061 / failure-state | 它應該說，哪些查到了，哪些頁面沒讀到。；無say | OUT OF SCOPE | S5 | 披露已讀／未讀的建議，不是所有產品都做到的保證。 |
| 118 | ag062 / failure-state | 再把無法確認的部分交回人處理。；無say | OUT OF SCOPE | S5 | 缺口交還人的編輯流程。 |
| 119 | ag063 / failure-state | 這樣的部分完成，比漂亮的錯答案有價值。；無say | OUT OF SCOPE | 本稿 failure-state | 對部分完成的價值判斷，沒有量化比較。 |
| 120 | ag107 / outside-text | 代理打開的網頁，可能有與任務無關的指令。；無say | OUT OF SCOPE | S5 | 外部資料可能含无關指令的情境提醒，不是本次已發現攻擊。 |
| 121 | ag108 / outside-text | 那是外部資料，不應因此擴大你交辦的權限。；無say | OUT OF SCOPE | S5 | 外部內容不擴權的編輯安全要求，不是已驗證的防護能力。 |
| 122 | ag109 / outside-text | 你原本只准查資料，它就不該自行付款。；無say | OUT OF SCOPE | L1/S5 | 只查資料任務不付款的規則，沒有新付款授權。 |
| 123 | ag110 / outside-text | 設定停止線，是為了讓結果仍由你掌握。；無say | OUT OF SCOPE | S1/S5 | 停止條件的工程建議，不保證所有架構自動遵守。 |
| 124 | ag064 / task-recipe | 你可以從一個小而能回查的任務開始。；無say | OUT OF SCOPE | S1/S5 | 从可回查小任務開始的建議。 |
| 125 | ag065 / task-recipe | 先寫目標與准用的資料，再寫不能跨過的邊界。；無say | OUT OF SCOPE | S5 | 交辦目標、資料與邊界的建議。 |
| 126 | ag066 / task-recipe | 最後指定驗收方式，像是附來源的待辦清單。；無say | OUT OF SCOPE | S5/本稿 task-recipe | 驗收規格的示例，不是第三方測試結果。 |
| 127 | ag067 / task-recipe | 有缺口就標待確認，不必硬湊完整答案。；無say | OUT OF SCOPE | S5 | 不捏造未知答案的建議。 |
| 128 | ag139 / approval-point | 如果任務後半段會碰到預約，先寫好核准點。；無say | OUT OF SCOPE | S1/S5 | 預約前核准點的建議。 |
| 129 | ag140 / approval-point | 查資料和產草案可以直接做。；無say | OUT OF SCOPE | L1/本稿 approval-point | 限于交辦允許的公開讀取與草案，不是所有資料無條件可讀。 |
| 130 | ag141 / approval-point | 使用帳號、下單或付款，要先等人決定。；無say | OUT OF SCOPE | S5 | 帳戶、下單與付款等人決定的規則，不代表已操作。 |
| 131 | ag142 / approval-point | 這能讓代理知道，哪裡應該交接，而不是硬闖。；無say | OUT OF SCOPE | 本稿 approval-point | 交接停止線的設計意圖，不保證模型必然遵守。 |
| 132 | ag068 / example-prompt | 比起一句幫我排行程，這樣交辦更容易驗收。；無say | OUT OF SCOPE | 本稿 example-prompt | 自製提示範例的教學比較，沒有A/B測試宣稱。 |
| 133 | ag069 / example-prompt | 請它只查官方公開頁，交出草案和來源。；無say | OUT OF SCOPE | L1/本稿 example-prompt | 只讀官方頁的交辦規格，不是新授權。 |
| 134 | ag070 / example-prompt | 沒查到的列出來，不准預約或付款。；無say | OUT OF SCOPE | L1/本稿 example-prompt | 待查、無預約付款停止線，保留。 |
| 135 | ag071 / example-prompt | 你保留最後決定權，也知道哪裡要自己再看。；無say | OUT OF SCOPE | 本稿 example-prompt | 人保留決定權的建議，不保證所有系统會遵守。 |
| 136 | ag072 / article | 完整的代理概念和交辦方法，在說明欄第一行。；無say | OUT OF SCOPE | S5/本稿 source_guide | 文章存在，但实际上架包第一行尚未產出；這是後續package验收依賴。 |
| 137 | ag073 / article | 文章也拆開聊天回答、固定流程與代理。；無say | CONFIRMED | S5 | 今天實讀的文章包含三種工作方式的區分。 |
| 138 | ag074 / article | 你可以對照自己正在用的工具，看看它真的做到哪裡。；無say | OUT OF SCOPE | S5 | 請觀眾自行對照工具的下一步，沒有特定產品測試結論。 |
| 139 | ag075 / answer | 回到開場：會回答，不等於完成任務。；無say | OUT OF SCOPE | 本稿 answer | 總結可驗收任務的編輯立場。 |
| 140 | ag076 / answer | 代理的價值，是依真實回饋選下一步。；無say | CONFIRMED | S1 | 依環境回饋使用工具與選下一步符合官方agent模式。 |
| 141 | ag077 / answer | 最後還得交出能檢查的結果。；無say | OUT OF SCOPE | 本稿 answer | 本片的交付標準，非所有產品必然具備。 |
| 142 | ag078 / answer | 拿四欄交辦式，挑一件小任務試試看。；無say | OUT OF SCOPE | 本稿 task-recipe | 四欄小任務CTA與片中可用範例一致。 |

## 36場景data／字卡核對

| # | scene / template | 全部data核對 | 判定 |
| ---: | --- | --- | --- |
| 1 | hook / title | 問題與交辦清單承諾，屬教學；沒有商用模型實測。 | CONFIRMED（內容與範圍） |
| 2 | pretty-answer / chat | 自製示意對話；ag006明示未錄製產品畫面，沒有產品名稱或真實訂單。 | CONFIRMED（內容與範圍） |
| 3 | three-modes / table | S1工程分類的簡化；「可查交付物」是期望，不是所有代理保證。聊天框可含工具的界線在後文保留。 | CONFIRMED（內容與範圍） |
| 4 | fixed-example / steps | 報表為自製假設；S1支持已知規則用workflow，未做性能測量。 | CONFIRMED（內容與範圍） |
| 5 | no-tool-case / big | 本次沒有其他公告輸入且缺查詢工具的情境；不可外推所有工具／資料渠道。 | CONFIRMED（內容與範圍） |
| 6 | interface-trap / big | 聊天介面與名稱不證明執行能力；無特定產品比較。 | CONFIRMED（內容與範圍） |
| 7 | tool-result / compare | 查來源／結果／決策的編輯驗收清單，不是實際工具trace。 | CONFIRMED（內容與範圍） |
| 8 | task-spec / steps | 已改title為歷史示範；日期欄仍2026年9月28日；4欄目標來源停止線保留。9/27執行日只按L1記錄。 | CONFIRMED（內容與範圍） |
| 9 | task-not-question / compare | 兩種自製提示示例，没有實驗或產品回覆。 | CONFIRMED（內容與範圍） |
| 10 | success-rule / bullets | 自訂完成規格，開館來源S2/S3可核；交通與天氣待查。 | CONFIRMED（內容與範圍） |
| 11 | privacy-boundary / big | 公開日期地點的稿件輸入；無旅客識別資料，無外部帳戶事件確證。 | CONFIRMED（內容與範圍） |
| 12 | first-rule / quote | quote的休館短句與S2原文相符；旁白ag027同步保留假日例外。 | CONFIRMED（內容與範圍） |
| 13 | next-check / steps | 一般→例外→公告為歷史紀錄重建及當前可重現的比較，不證明當年模型選路。 | CONFIRMED（內容與範圍） |
| 14 | tool-trace / table | 表格按L1重建；S2/S3支持結果內容，不是原始產品畫面或不可改寫執行trace。 | CONFIRMED（內容與範圍） |
| 15 | exception / quote | S3列9/28(Mon)/Teacher’sDay/Open，短摘錄與翻譯匹配；確認的是公告安排。 | CONFIRMED（內容與範圍） |
| 16 | exception-context / table | S2一般規則、S3指定例外適用范围不同，表格比較正確。 | CONFIRMED（內容與範圍） |
| 17 | change-decision / compare | 日期例外可改歷史草案的推論，未確證9/27特定代理的實際決策。 | CONFIRMED（內容與範圍） |
| 18 | specific-date / big | 指定日不得外推每週一，与S2/S3相符。 | CONFIRMED（內容與範圍） |
| 19 | route / steps | S4與S2地址頁尾支持公園內本館，歷史草案順序非現場導航／可達性證明。 | CONFIRMED（內容與範圍） |
| 20 | source-trace / bullets | S3對入館安排，S4對地址；ag097承认館方交通建議，實測與天氣仍未知。 | CONFIRMED（內容與範圍） |
| 21 | three-evidence-levels / table | 已查／推論／未知為編輯分類；表中實际天氣與步行仍未測，不否認S4有估計。 | CONFIRMED（內容與範圍） |
| 22 | not-done / table | 表內開館指2026/9/28公告安排，不是當前營運保證；實測／天氣／訂票付款只按L1聲明。 | CONFIRMED（內容與範圍） |
| 23 | hand-check / steps | 原頁、狀態、出發前重查為編輯清單，不是新增核准。 | CONFIRMED（內容與範圍） |
| 24 | deliverable-shape / bullets | 4個交付欄位為自訂教學規格。 | CONFIRMED（內容與範圍） |
| 25 | fixed-flow / compare | S1支持按已知路徑或模型彈性選架構；未有量化可靠性比較。 | CONFIRMED（內容與範圍） |
| 26 | chat-can-use-tools / chat | 自製對話「有工具的助理」是情境；S1客服例支持聊天與工具可同存。 | CONFIRMED（內容與範圍） |
| 27 | autonomy-spectrum / steps | 讀取→草擬→人核准為編輯建議，不保證產品都具備相同权限控制。 | CONFIRMED（內容與範圍） |
| 28 | tool-boundary / big | 公开讀取與帳戶／支付分開，文字不是訂單；建議而非工具能力審核。 | CONFIRMED（內容與範圍） |
| 29 | handoff-check / bullets | 3問題為自訂驗收標準，不是已測產品得分。 | CONFIRMED（內容與範圍） |
| 30 | failure-state / steps | 條件式故障處理建議；本次4個primary頁面都200，不說它們目前不可讀。 | CONFIRMED（內容與範圍） |
| 31 | outside-text / big | 外部資料不擴權的建議；沒有宣稱本次遭攻擊或防護必然有效。 | CONFIRMED（內容與範圍） |
| 32 | task-recipe / steps | 4欄交辦式存在於本稿，可作CTA交付，不是科學分類。 | CONFIRMED（內容與範圍） |
| 33 | approval-point / compare | 可做／先問人屬任務規格，未下單付款或提供操作授權。 | CONFIRMED（內容與範圍） |
| 34 | example-prompt / chat | 自製提示、規格化交付示例；無登入個資與產品實錄宣稱。 | CONFIRMED（內容與範圍） |
| 35 | article / cta | S5本文存在且含本片相關概念；实际package首行仍待物化驗收。 | CONFIRMED（內容與範圍） |
| 36 | answer / outro | 回饋選路符合S1；可查結果與4欄CTA是編輯收束。 | CONFIRMED（內容與範圍） |

## 標題、metadata與縮圖

- YouTube title：AI 代理跟聊天機器人差在哪？一個行程任務看懂。只承諾一個行程任務的教學，沒有特定產品實測、已訂票或現場走過承諾。
- Thumbnail：AI 代理入門／會回答 ≠ 有完成／同一個行程任務，差在哪？。自製文字，與未完成≠已回答的編輯立場一致，沒有外部品牌／產品錄影。
- Description明列2026年9月27日示範查詢與出發前重查；新增正文及字卡歷史標示已讓聽眾不用依賴描述才能知道日期已過。tags為主題分類，非外部數據主張。
- source_guide=ai-agents-explained：S5文章可讀；ag072、article.data.sub與quote資料來源進說明欄，是之後actual package驗收依賴。此處沒有產出或核准upload metadata。
- brief的編輯立場未被本輪改寫或重新授權；outline gate不等於音訊、final、language choice或YouTube approval。

## 本輪修正readback與語音綁定

| 位置 | 前 | 目前已套用 |
| --- | --- | --- |
| ag018 / task-spec | 日期是二〇二六年九月二十八日。 | 這是歷史示範：二〇二六年九月二十七日查詢，規劃九月二十八日。 |
| task-spec.data.title | 這次交辦的四個欄位 | 歷史示範：2026/9/27 查詢 |
| ag097 / source-trace | 步行分鐘與天氣，我手上的來源沒有證明。 | 館方有步行建議，但我們未實測，也沒查天氣。 |

- native speech hash：`80b70c13bcc03e34`。由本worktree的`loadProject`／`speechHash`純函式讀當前doc及native pronunciation lexicon計算，沒有TTS或網路調用。原稿同一lexicon的speech hash為`a0b7b73157946605`，本次兩句改稿確實改變speech hash；不是visual-only修改。
- 當前native visual hash：`96d0eb2df7f98207`。字卡標題與四個sources.checked_on=2026-10-07分別readback；voice、142句ID與未受影響的140句完整欄位不變。
- ag018當前text固定為「這是歷史示範：二〇二六年九月二十七日查詢，規劃九月二十八日。」；30個Unicode字元。
- ag097當前text固定為「館方有步行建議，但我們未實測，也沒查天氣。」；21個Unicode字元。
- 日期欄的2026年9月28日、影片title、章節及brief保留；沒有新增句、scene或補時。

## 聽眾、字幕與本收據的實際限制

142句沒有大於40個Unicode字元的句子；未發現旁白Latin詞、括號或URL，沒有say替換。日期數字與兩筆未知邊界仍清楚。這是文字檢查，沒有音訊timeline／SRT的實際CPS、TTS fit、Jev或owner聽音結論；四語需正常merge更新受影響的ag018/ag097 source_hash，再按實測timeline跑caption檢查。本輪沒有完整四語翻譯核准。

沒有執行native lint、facts CLI、QA、provider请求或任何approval mutation。nativefacts只會選最新verify-N.md並檢查仍引用的未找到claim，不能把它的ok當成來源、音訊、成片或owner接受的全套驗收。当前官方來源未推翻本片被引用的日期／館名／時段或工程區分；歷史執行聲明按L1存檔內容处理，沒有升格为外部事實確認。

本輪逐句計數：CONFIRMED 23；CHANGED且已readback 2；OUT OF SCOPE 117；未找到需删除的外部事實0；合計142。36場景全部data已核對，方法性與編輯性內容的CONFIRMED僅指與稿件所述範圍相符。沒有超過3個外部事實變更，沒有以該門檻要求新增第三輪；后續原稿事实或speech字段變動仍須再查受影響範圍。

## 當前source與後續visual-only rebind

當前`video.json`完整SHA-256：`96b1e5fc9c31c9be0f87fefa214cedd54cab00233140d7d6a5498ae1725a3b48`。本收據釘住此source以及speech hash `80b70c13bcc03e34`、ag018／ag097上述完整text和所有142句欄位。brief SHA-256：`9093fcc62ad70a60bfcd8680389c833d85de87aba090a8028f0302a11976ba23`，與原始複核完全相同。

若後續只為排版／safe area修scene.data且完整語音欄位不變，可以記錄新source完整SHA與native visual hash，並明確標visual-only rebind。必須重新計算speech hash仍等於`80b70c13bcc03e34`、逐句比對voice／id／text／say／pause／emotion／cue／pronunciation_hints／audio_ref等原生語音影響欄位、確認ag018與ag097完全相同，再核對改動畫面沒有改日期／館名／公告引文／來源含義。新SHA本身不能證明沒有語音變動，也不能讓舊查核自动覆蓋新增事實。原收據source SHA作为歷史綁定保留，不倒填或稱舊檔為当前檔。


## Visual-only source rebind (2026-10-07)

Independent append reviewed at UTC 2026-10-07T11:37:13.093Z. The original142-line fact review above remains bound to source SHA-256 `96b1e5fc9c31c9be0f87fefa214cedd54cab00233140d7d6a5498ae1725a3b48`; its original text and source-access receipts were preserved byte for byte. The baseline verify-2.md SHA-256 is `80eec9b495d73ca9b53a32e8481534b01dcdf77f16af6d39c8954c2a3d768f5e`, with a same-byte private copy at `<home>/mokaair-work/ai-agent-continuation-20261007/visual-candidate/verify-2.baseline.md`. This append does not rewrite the original source pin or present the old scene-template names as the current layout.

The applied visual candidate's full source SHA-256 is `905ac35021688b7ca80264f12afd6f8973b959317438538e2199bdb4536a058c`; its native visual hash is `b9ae256bfd4c2369` (previous `96d0eb2df7f98207`). Direct readback of the applied repository source and the retained pre-visual snapshot verifies:

- The same36scenes and142line IDs/order remain. Every spoken field, voice/style, pause/hint/emotion/audio-reference field, chapter, YouTube metadata and nonvisual source field is identical after removing only optional line reveal values and scene template/data.
- Native speech hash is `80b70c13bcc03e34` for both source versions. All36complete native request plans are identical under the current native lexicon; complete plan JSON SHA-256 `15a108e0e405795dfa11f8f91ee1328609fc90e545c436051e07e82cbc22da57`. This is an offline pure-function comparison, with no provider request.
- The official source titles/URLs and allfour checked_on dates remain exactly as already reviewed (2026-10-07). This visual revision did not perform a new source lookup or change those access records.
- ag018 retains the exact historical September27query/September28plan sentence quoted above; ag097 retains the exact official walking-suggestion versus no empirical measurement/no weather-check qualification quoted above. Neither sentence changed in this visual revision.
- Twelve scene-template conversions, two verbatim compare-verdict moves, and48reveal-bearing lines (51elements) change presentation only. Original closure quote, annual holiday table row/translation, publisher labels, date-only exception and no-login/no-booking/no-payment limits remain. The added fourth three-modes row, hook checklist, flexibility bullet and date-only holiday qualification paraphrase unchanged narration.

The independent candidate semantic receipt at `<home>/mokaair-work/ai-agent-continuation-20261007/visual-candidate/independent-semantic-review.json` SHA-256 `002789035cf59b3c7132ccce5c69b70f20c7c65a0493122306a6d1fb651d96dc` records all48reveal targets and resolves the eight prior cue findings. Its offline reconstruction from142existing WAVs matches84measured states,19182frames at30fps (639.4seconds), maximum14.133333seconds and zero states longer than15seconds. These are PCM/frame-timing checks, not listening or native audio-quality approval.

Facts above therefore remain applicable to the identical speech and preserved source content of this applied visual version. Font-ready render geometry and image inspection remain a separate required review: lower15%means important text bottom y<=918 in a1920x1080frame. No rendered-image PASS, ASR/Jev/audio approval, owner listening/player acceptance, language-choice approval, final approval, upload package or YouTube action is asserted by this rebind. Historical demo-log execution remains a committed record, not newly established raw September27request evidence.
