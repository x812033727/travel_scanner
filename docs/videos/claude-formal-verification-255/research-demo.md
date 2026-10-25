# 第三片推薦研究：把測試變成明確規格，再用反例修到可檢查

研究日：2026-10-25。此輪從16:51 UTC開始，限時完成官方重核與新增實跑；只寫scratch，未建立episode/task、未動ForTy、未呼叫付費模型或登入YouTube。本報告不是已完成文稿、成片或敘事關卡收據。

**建議採用。** 新聞有可直接讀取的官方證據，本地已有兩個完整可重跑例子，可支撐約8–12分鐘的單一主線。資訊增益是讓觀眾跟著「寫範圍→找反例→修正→核對保證」完成一份紀錄；直接同題YT流量證據較弱，採用理由以時效和實證完整性為主。

推薦主問題：**要讓程式在明確範圍內做對事、也會結束，我們要把哪些要求寫進規格，再交給什麼工具檢查？**

暫定包裝：「Claude把測試變證明：用255找反例，再檢查256種輸入」。這是編輯提案，未註冊新片、未送標題評分；不可寫成我們重現了Claude／Theorem的239個入口。

## 本週新聞究竟是什麼

下列六個官方頁本輪正常編輯UA重取均HTTP200；原文、雜湊與狀態保存在third-topic-source-*及third-topic-source-http.json。同站請求至少間隔1秒，沒有關閉TLS或改代理。

| 來源 | 本輪確認／可用敘述 | 容易誤報之處 |
| --- | --- | --- |
| [Anthropic研究公告](https://www.anthropic.com/research/formal-verification) | 頁面明列Published Oct22,2026。官方報告與Theorem合作，讓Claude為123個OSS-Fuzz函式庫的239個入口產生特定RISC-V二進位安全性證明。方法把既有測試所要求的條件變成形式規格，再由Rocq檢查證明；原文有輸入／記憶體／單執行緒／系統模型限制。 | 這是研究公開，未確認是ClaudeApp新按鈕或新模型發布；官方實驗總量不是本片親測或全部已公開下載。正文若要用64MB數字需保留原文界線，不把MB與MiB、自動補上的≤／<混用。 |
| [Theorem官方blog](https://theorem.dev/blog/) | 同一合作研究列October22,2026，交叉確認消息日期。 | 不把blog索引日期推成OSSVerify產品首次推出日；本輪未找到可證明其首次推出日的欄位。 |
| [OSS Verify官方方案](https://theorem.dev/oss-verify/) | 現行方案向符合資格的開源專案提供免費驗證；核心維護者申請，交付對編譯後fuzz target的Rocq證明，錯誤／修補另提供維護者。 | 不能叫任何人貼程式就免費即時驗整個產品。沒有申請、送PR、建Docker或測服務；它是可用官方方案資訊，不是本輪服務實測。 |
| [公開proof README](https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md) | 本輪表格實數60個入口、25個函式庫，與頁面總數相符。證明針對該release的靜態riscv64二進位與LPS模型；該release的agreement證明**沒有證明halts**。 | 不將239/123與公開60/25混成同一數；不把「不出現指定錯誤」自動說成「每次一定結束」。不用龐大statement清單的數量當已證明數。 |
| [proof來源與checker規則](https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/origin.md) | 語言模型寫proof；checker要求固定statement的type，稽核允許的assumptions，Rocq kernel決定接受。 | 一份檔案能compile不等於目標命題已被無額外假設證明；不能把未完成skeleton的Admitted當成果。本輪沒有執行該checker。 |
| [statement種類](https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/statements.md) | 官方把行為agreement與halts等命題分開，適合對應本片不同規格的正向成果表。 | 本片自己的模型不是這些statement的Rocq證明，不可稱SAT／SMT／Rocq同一種工具。 |

原文定位短引只需：公告「Published Oct 22, 2026」；公開README「No proof in this release proves a halts statement」。不複製官方長段落。正式稿每頁衍生摘要控制200英文詞等量內、逐字引用各頁≤25詞；本片主要篇幅應是下面的原創實算，而非把公告逐段翻譯。官方概述中的「正常退出」與公開release具體statement的保證應分層歸屬，不借此宣稱我們找到供應商錯誤。

本輪沒讀或執行全部180M行proof，沒跑64MB輸入的vendor pipeline；未驗證全部239入口。環境無Rocq/coqc、Lean/lake、Z3、cvc5、Boolector；有GCC14.2.0、Python3.12.14、SymPy1.14.0。沒有安裝全域套件或下載checker容器。

## 已經實跑的主幹一：8byte容量，卻放行255

證據根目錄：formal-demo。既有guard.c、run_demo.py及完整輸出本輪重新核對manifest，九檔SHA全部一致。

規格先說清：payload長度n∈0..255，另需1byte結尾，容量8byte；應且只應接受n+1≤8，也就是0..7。這些是本片自己設計的教學碼，不是聲稱找到真實軟體漏洞或量測Claude修bug能力。

錯版把總長存回uint8_t再比較。刻意挑的正常小值0、1、2、3、4，五例都符合預期；不能稱隨機測試統計或真的跑了千萬次。完整域的真實編譯C執行結果只有n=255誤接受：C先提升為int算出256，再窄化成uint8_t的0。說「窄化儲存繞回」，不要說加法本身發生未定義有號溢位。

修法一用uint16_t保存總長，修法二用n<8直接判斷。兩修法全部256例都符合規格。另以獨立布林位元模型和SymPy的dpll2命題SAT查詢；模型與編譯C逐例256/256相符，找到反例255，排除255後無第二個反例，修正後誤接受／誤拒絕兩種查詢均UNSAT。這是**有限域枚舉＋命題SAT**；沒有SMT、Rocq或獨立kernel proof certificate。

| 實作／模型 | 接受數 | 誤接受 | 誤拒絕 | 可帶走的結果 |
| --- | ---: | --- | --- | --- |
| 錯版GCC guard | 9 | [255] | [] | 五個小例子不足以發現邊界錯誤。 |
| 加寬總長GCC guard | 8 | [] | [] | 同一明確輸入域的功能與拒絕條件都對上。 |
| 直接上界GCC guard | 8 | [] | [] | 相同規格可有不同正確寫法。 |
| 一律拒絕（符號對照） | 0 | [] | [0..7] | 只問「沒有誤放行」會接受沒功能的答案；必須加應接受條件。 |

不執行buffer寫入，所以成果是guard行為符合規格，不是完整應用的記憶體安全認證。

可重跑：`python /workspace/work/ai-tech-next/formal-demo/run_demo.py`。輸出包括all-256-cases.json、compiled-c-results.csv、symbolic-vs-c.json、sat-output.json、results.json及manifest.json。執行會更新求解時間等產物，現有收據的來源hash已保存，不能把新run時間混成舊測量。

## 已經實跑的主幹二：沒有陣列存取，也要知道會不會返回

本輪新增並RUN：loop.c、run_loop_demo.py、loop-all-256.json、loop-results.json、loop-manifest.json。只用現成GCC，編譯零警告／錯誤；五檔manifest全吻合。完整方法另見formal-demo/loop-README.md。

這是**第二個獨立小程式**，同樣令n∈0..255。規格要求i從0加到n後離開，返回n+1。錯版i是uint8_t：n≤254全部實際返回，n=255實際C子程序在0.25秒限額被終止。**逾時只是一筆觀察，不能單靠它證明永不結束。** 另完整探索有限控制狀態，255時依序走0..255再回0，條件持續成立，因此該確定控制模型有256步循環。

修正版i改uint16_t。全部256個真實編譯C呼叫均返回預期n+1，並逐例對上模型；255時i到256可離開。本地計數器設volatile，使其讀寫對C編譯器可觀測；沒有外部寫入者或指標逸出。此模型只檢查上述固定n／本地i控制狀態，不涵蓋OS中斷、並行或任意程式。

| 迴圈版本 | 編譯C觀察 | 有窮控制模型結果 |
| --- | --- | --- |
| uint8_t錯版 | 255個輸入正常返回；255這個輸入timeout | 唯一不結束輸入為255，cycle長256。 |
| uint16_t修正版 | 全256個輸入正常返回，值皆n+1 | 全256個輸入皆在n+1次增量後離開。 |

這段是**有限控制圖完整探索＋實際C執行**，沒有叫SAT、SMT或Rocq。正確guard會先拒絕255，所以不能演成「修正guard放行255後仍卡住」；兩個獨立例子只是用同一邊界值，讓不同規格的成果看得見。

可重跑：`python /workspace/work/ai-tech-next/formal-demo/run_loop_demo.py`。錯版255子程序有0.25秒timeout，會被runner終止，不讓無限迴圈佔住工作環境。timeout不是效能benchmark，不能說修正版快了多少倍。

兩例的數據合表在third-topic-demo-summary.json。新增實測在本輪幾分鐘內完成，沒有用時長或輸入數冒充vendor研究。

## 8–12分鐘如何有持續資訊增益

以下只是編輯計畫約9分30秒，不是音訊實測。前兩例都已有真輸入、動作、結果與修正，無需另塞泛泛警告。

| 估時 | 同一主問題的進度 | 可見實證／觀眾能跟算的動作 |
| --- | --- | --- |
| 0:00–0:25 | 為什麼長度255被8byte的guard放行？ | 先呈實際錯版輸入／返回值，再帶出問題，不先講長定義。 |
| 0:25–1:10 | 本週Claude＋Theorem把測試變成什麼？ | 官方10/22日期、研究與public subset分層；用原創流程圖標本地例子的位置。 |
| 1:10–3:10 | 寫出範圍、五樣例、完整域、反例與修正 | n+1≤8；255+1先得256、窄化成0；加寬後完整256例對規格。 |
| 3:10–4:20 | 為什麼一律拒絕也能通過某條要求？ | 用誤接受／誤拒絕兩欄表，把缺少的功能條件補完整；不要演成我們發現vendor reward hacking。 |
| 4:20–6:35 | 要求會返回，再做一次反例→修正 | 第二個真C程式、timeout觀察、256狀態cycle、加寬後全256返回；不用timeout冒充證明。 |
| 6:35–8:15 | 新聞中的正式checker實際多做哪些事？ | 原創圖：固定binary與statement→AI寫proof→type／assumptions audit→kernel；對照本地的GCC／SAT／狀態圖，清楚標各自範圍。 |
| 8:15–9:30 | 完成一份可用的交付紀錄 | 兩列填入輸入域、應接受／拒絕／返回條件、反例、修法、檢查方法及未涵蓋範圍；帶走下一次可重跑命令。 |

若正式朗讀不足8分鐘，優先把兩個實際修正和規格對照講明白；不重述239／proof行數或以空白拉長。若盲讀仍像課程，可把新聞範圍壓縮、更多時間留給真實反例與修正，但不能省掉local方法歸屬。

站主觀點候選：有一個可重跑、範圍明確且保留功能的修正，比一句「AI已證明沒問題」更能讓人使用。這是編輯判斷，須在正式brief確認，沒有捏造站主私人經驗。

## 海外YouTube參考與可採製作映射

完整七筆與來源／日期衝突／缺值在third-topic-yt-research.md；六支可定位影片，加一支官方活動embed候選。未登入或觀看鏡頭，故沒有剪點／音效／留存測量。以下只摘要可採用範圍，不拿第三方評論驗證技術事實。

| 參考 | 已觀察資料 | 本片原創設定與驗收 |
| --- | --- | --- |
| [Hyperautomation Labs本週直接相關](https://www.youtube.com/watch?v=RxGLRbkCjeU) | 10/23第三方頁有標題／description，明說自己的planted-bug＋CBMC小demo；讀頁值4638，未標統計時刻。 | 用我們自己的255、GCC、SAT及狀態圖；標明不同工具／不同原始碼。對方「10million／36秒」只屬其標題，不採為本片benchmark。 |
| [MLST／Leonardo de Moura](https://www.youtube.com/watch?v=ZpQFebTK75A) | 研究者訪談description涉及kernel與spec；第三方日期9/29及10/3、題名版本不同；74min與18K均第三方分鐘級／歷史快照。 | 以本地一律拒絕的8個誤拒絕，讓spec gap有真正可算的結果；不把Lean訪談混成Rocq研究。 |
| [DaaX／Christian Szegedy](https://www.youtube.com/watch?v=dii8jSgMr50) | 官方10/3節目頁有約31分鐘與完整逐字稿，views未取得。 | 把「驗輸出」落到本地完整表，保留checker與模型範圍；不假稱已看其鏡位。 |
| [Amii正式方法講座](https://www.youtube.com/watch?v=aqkcvzdoGuo) | 原講座官方9/11，第三方上架索引10/9；片長與views未取得。 | 只作專業背景資料，不包成10/9新研究，不挪用其未讀benchmark。 |
| [Claude驗證迴圈教學](https://www.youtube.com/watch?v=mQZB0l-rhxE) | 官方目錄約3分鐘；第三方列9/25、3:08，349031截至10/16。是tests／typechecks／lint相鄰教學。 | 與形式證明分層；可讓日常工具使用者理解位置，不稱lint等於proof。 |
| [Numberphile／Terence Tao談AI](https://www.youtube.com/watch?v=bAnwMdfcMVw) | 10/15，第三方19:45；最後讀頁快照995768截至10/24。是AI數學相鄰題。 | 只作受眾興趣線索，不推定軟體形式驗證同樣熱或某手法造成高點閱。 |
| [Microsoft Reactor活動候選](https://www.youtube.com/watch?v=P9xCUmjkPUM) | 官方活動排10/22UTC，直接embed同YTID，談Rust／Lean／RangeSetBlaze；未核影片發布日、可播性或實際片長。 | 可列官方延伸資源；不能說已看完或已重現Rust／Lean。 |

直接同題僅一筆可見約4.6K第三方讀頁值，沒有足夠頻道同類基準／訂閱規模／多時點數據可以計算觀看速度、CTR或因果。Numberphile的高views是相鄰題，不能拿來代替本題熱度證據。

## 下一步可做、但此輪尚未做

1. root若採用，再依既有流程查重／登記episode與正式brief，沿用8–12分鐘和八語交付；本報告沒有直接建立它們。
2. 保留兩份C、runner、完整256例、SAT原始結果、cycle與hash；正式畫面採原創算式、真實stdout摘要及不混用方法名稱的流程圖。
3. 正式稿應給至少兩個可跟算的反例／修正，把最後的成果表填完整。所有數值繫結本地JSON，官方總量始終標「官方報告」。
4. 若要真正跑Rocq／Lean／SMT或官方checker，需另規劃可用環境與時間；本輪沒有這些執行證據，不能在旁白裡補稱已驗過。

此輪完成研究與兩個可重跑實證即停，不啟動新付費階段、服務申請或持續背景工人。
