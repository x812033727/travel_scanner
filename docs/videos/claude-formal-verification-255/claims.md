# Claude形式驗證255：逐句主張與實作證據

確認日期：2026-10-25 UTC。本文對應目前正式video.json，不是獨立facts／盲讀／音訊或成片通過收據。採A的原生選擇與後續精確修法採用由root保存在production-decision.md；brief不由本代理修改。

## 證據與歸屬

- RUN-A：data/guard.c、compiled-c-results.csv、all-256-cases.json、results.json。原創有限域n=0..255、capacity8byte與額外1byte結尾；guard只判接受，不執行buffer寫入。
- RUN-SAT：data/run_demo.py、sat-output.json、symbolic-vs-c.json。SymPy1.14.0命題SAT，8個輸入布林位元，模型對實際C逐例256/256相符；求解器可有輔助變數。沒有SMT、通用已驗證C翻譯或獨立kernel證書。一律拒絕僅為符號臂，沒有另一份deny-all C執行。
- RUN-B：data/loop.c、loop-all-256.json、loop-results.json。另一個獨立程式；固定n及本地volatile計數器，無外部寫入者。0.25秒只是一筆被runner中止的逾時觀察；完整有限控制圖另確立256步循環。修正版全256個C呼叫返回n+1。
- 本地環境：GCC14.2.0、Python3.12.14、C11；兩份編譯結果皆零錯誤／警告。原始14個manifest檔由news_verify重核一致；本稿沒有重跑會覆寫收據的runner。
- CITED：Anthropic公告、Theorem公開README／origin／checking／statements、C11委員會草案。原始來源與逐句技術邊界見fact-boundaries.md及scratch third-topic-facts-final.md；checking後續原文修正已納入本稿。
- ED：觀眾提問、條件推演、選擇及完成紀錄。不是捏造使用者事故、Claude受測碼或親測供應商pipeline。旁白的「我」只指本次原創程式與保存的執行工作。
- 官方研究239入口／123庫、公開release60入口／25庫與本地各256個輸入分開；不計百分比或相減作研究涵蓋率。
- 原始C與結果的公開資料包已由root正常GET確認：https://github.com/x812033727/travel_scanner/tree/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data 。此網址是GitHub資料，不是模型API／產品App成功操作。

## 逐句對照

c1｜二〇二六年十月二十五日，我的程式容量八位元組，卻接受長度二百五十五？｜RUN-A＋ED提問｜原創guard的255誤接受，非供應商漏洞或Claude實驗結果｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜capacity-accepts-255／zfgp（草稿L001）
c2｜紀錄上只寫不收錯的，全部拒絕能算完成嗎？｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜deny-all-preview／z9dp（草稿L002）
c3｜紀錄還要填返回，另一個計數程式真的會離開嗎？｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-preview／bpnn（草稿L003）
c4｜同一個要求，AI寫出證明後，又交給誰驗收？｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md｜2026-10-25｜proof-preview／c8r2（草稿L004）
c5｜這份紀錄，要回答十月二十二日Claude研究帶來的驗收問題。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://www.anthropic.com/research/formal-verification｜2026-10-25｜research-published／qwaw（草稿L005）
c6｜研究把測試要求，寫成可檢查的命題。｜CITED｜官方研究公告；日期／測試要求到命題／239入口與123庫皆屬官方報告｜https://www.anthropic.com/research/formal-verification｜2026-10-25｜tests-to-fixed-statement／4rff（草稿L115）
c7｜這裡用我自己寫的C程式，先填接受判斷這一列。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜start-contract／5i5d（草稿L006）
c8｜輸入是資料長度，限定零到二百五十五。｜RUN-A＋契約實算｜n=0..255；capacity8byte＋terminator1byte；n+1≤8⇔n∈0..7｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜length-domain／jeaj（草稿L007）
c9｜容量只有八個位元組，還得替結尾留一個位元組。｜RUN-A＋契約實算｜n=0..255；capacity8byte＋terminator1byte；n+1≤8⇔n∈0..7｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜capacity-and-terminator／fzz5（草稿L008）
c10｜所以輸入長度加一，不超過八，才應該接受。｜RUN-A＋契約實算｜n=0..255；capacity8byte＋terminator1byte；n+1≤8⇔n∈0..7｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜mathematical-contract／kkef（草稿L009）
c11｜長度七加一等於八，剛好能收；長度八加一等於九，就該拒絕。｜RUN-A＋契約實算｜n=0..255；capacity8byte＋terminator1byte；n+1≤8⇔n∈0..7｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜seven-versus-eight／m7xu（草稿L010）
c12｜零也合法，因為加上結尾，只占一個位元組。｜RUN-A＋契約實算｜n=0..255；capacity8byte＋terminator1byte；n+1≤8⇔n∈0..7｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜valid-interval／axkg（草稿L011）
c13｜所以紀錄上的接受區間，是零到七。｜RUN-A＋契約實算｜n=0..255；capacity8byte＋terminator1byte；n+1≤8⇔n∈0..7｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜valid-interval／r79s（草稿L012）
c14｜那為什麼開頭的二百五十五，竟然進來了？｜RUN-A＋ED提問｜原創guard的255誤接受，非供應商漏洞或Claude實驗結果｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜why-255-accepted／p2uy（草稿L013）
c15｜沿著總長的計算看：二百五十五加一，先得到二百五十六。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜promoted-addition／vwiq（草稿L014）
c16｜加法先提升成一般整數計算，並沒有直接變成零。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf｜2026-10-25｜integer-promotion／5iky（草稿L015）
c17｜錯版卻把總長，轉回八位元無號整數。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜narrowing-assignment／zfmi（草稿L016）
c18｜這個型別能保存的數字，只有零到二百五十五。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf｜2026-10-25｜eight-bit-range／3mpx（草稿L017）
c19｜二百五十六轉回去，儲存值就成了零。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜narrow-256-to-zero／tew5（草稿L018）
c20｜拿零和容量八比較，程式就回傳通過。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜zero-passes-capacity／femu（草稿L019）
c21｜八位元是型別，八位元組是容量。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf｜2026-10-25｜bits-versus-bytes／64pm（草稿L020）
c22｜這次的錯在轉型儲存，不能把兩種八當成同一件事。｜RUN-A＋C11§6.3.1.1／6.3.1.3｜先int256，再無號窄化為0；非加法UB｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜conversion-location／2yfh（草稿L021）
c23｜紀錄已找到反例，哪一行能把完整總長留下？｜RUN-A｜guard_widened完整運算式；計算與儲存均保留完整值，非僅改左側宣告｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜which-line-to-fix／mvnc（草稿L022）
c24｜讓計算保留完整值，再用十六位元無號整數儲存總長。｜RUN-A｜guard_widened完整運算式；計算與儲存均保留完整值，非僅改左側宣告｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜wide-total／936d（草稿L023）
c25｜如果先把結果縮回八位元，再存進加寬的變數，零仍然是零。｜ED算式推演｜若保留(uint8_t)窄化，256先成0再存uint16仍是0；未另編譯此變體｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜lhs-only-cannot-recover／s57e（草稿L024）
c26｜修正版這一整行，計算和存放總長的轉型都要一起改。｜RUN-A｜guard_widened完整運算式；計算與儲存均保留完整值，非僅改左側宣告｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜complete-wide-expression／yavq（草稿L025）
c27｜輸入二百五十五，加一後仍保存二百五十六。｜RUN-A｜guard_widened完整運算式；計算與儲存均保留完整值，非僅改左側宣告｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜fixed-255-total／ij57（草稿L026）
c28｜它大於容量八，這次正確回傳拒絕。｜RUN-A｜guard_widened完整運算式；計算與儲存均保留完整值，非僅改左側宣告｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜fixed-255-rejects／mfag（草稿L027）
c29｜原本合法的長度七呢？加一得到八，仍然接受。｜RUN-A｜guard_widened完整運算式；計算與儲存均保留完整值，非僅改左側宣告｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜wide-fix-and-valid-seven／vkym（草稿L028）
c30｜但只看這兩筆，怎麼確認中間沒有別的錯？｜RUN-A｜五個小值0..4；完整256列；錯版唯一誤接受255；加寬版兩方向零錯誤｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜how-check-the-middle／84hx（草稿L030）
c31｜我原先選零、一、二、三、四，五個小值都符合預期。｜RUN-A｜五個小值0..4；完整256列；錯版唯一誤接受255；加寬版兩方向零錯誤｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜five-small-examples／wunt（草稿L031）
c32｜把零到二百五十五全部列出來，才能對回完整範圍。｜RUN-A｜五個小值0..4；完整256列；錯版唯一誤接受255；加寬版兩方向零錯誤｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜enumerate-entire-domain／a7te（草稿L032）
c33｜錯版額外放行的只有二百五十五；加寬版只放行零到七。｜RUN-A｜五個小值0..4；完整256列；錯版唯一誤接受255；加寬版兩方向零錯誤｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜only-extra-accepted-value／dfhy（草稿L033）
c34｜這份紀錄另加一個求解模型，把同一輸入寫成八個真假位元。｜RUN-SAT＋C逐值對照｜8個輸入布林位元；誤接受／誤拒絕查詢；非SMT／Rocq證書｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜boolean-input-model／zgkb（草稿L035）
c35｜讓命題求解器找：有沒有不合格的長度，卻得到接受？｜RUN-SAT＋C逐值對照｜8個輸入布林位元；誤接受／誤拒絕查詢；非SMT／Rocq證書｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜false-accept-query／5waf（草稿L036）
c36｜這種尋找真假條件能否同時成立的方法，叫命題SAT。｜RUN-SAT＋C逐值對照｜8個輸入布林位元；誤接受／誤拒絕查詢；非SMT／Rocq證書｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜sat-meaning／unr8（草稿L037）
c37｜錯版找到二百五十五；加寬版找不到這種反例。｜RUN-SAT＋C逐值對照｜8個輸入布林位元；誤接受／誤拒絕查詢；非SMT／Rocq證書｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜sat-bad-versus-fixed／gtuj（草稿L038）
c38｜再問合法長度會不會遭拒絕，修正版也找不到。｜RUN-SAT＋C逐值對照｜8個輸入布林位元；誤接受／誤拒絕查詢；非SMT／Rocq證書｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜sat-false-reject／56e4（草稿L039）
c39｜模型結果逐筆對照C語言程式的實際執行結果，二百五十六筆全相符。｜RUN-SAT＋C逐值對照｜8個輸入布林位元；誤接受／誤拒絕查詢；非SMT／Rocq證書｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜symbolic-versus-compiled／tksv（草稿L040）
c40｜這個範圍很小，逐個測也做得到，求解器沒有多變出一個答案。｜RUN-SAT＋C逐值對照｜8個輸入布林位元；誤接受／誤拒絕查詢；非SMT／Rocq證書｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜small-domain-enumeration／2zma（草稿L041）
c41｜但如果紀錄上只留不准收錯的，全部拒絕能不能交付？｜符號對照＋ED｜同域接受契約；deny-all零誤接受／8誤拒絕，不是另一支已編譯C｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜deny-all-question／4bqi（草稿L042）
c42｜照這個單向條件，永遠拒絕確實沒讓不合格輸入通過。｜RUN-SAT｜實際常數false符號臂；0..7共8個合法值遭拒，無deny-all C執行臂｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜deny-all-two-directions／xfvp（草稿L043）
c43｜可是長度零到七，也一個都進不來。｜RUN-SAT｜實際常數false符號臂；0..7共8個合法值遭拒，無deny-all C執行臂｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜deny-all-two-directions／cabc（草稿L044）
c44｜這個對照是在符號模型裡計算，不是另跑一支C程式。｜RUN-SAT｜實際常數false符號臂；0..7共8個合法值遭拒，無deny-all C執行臂｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜symbolic-contrast-only／jhkm（草稿L045）
c45｜結果是零誤接受，卻有八個誤拒絕。｜RUN-SAT｜實際常數false符號臂；0..7共8個合法值遭拒，無deny-all C執行臂｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜deny-all-error-counts／e6wk（草稿L046）
c46｜只寫不准收錯的，程式就能用拒絕所有人來交差。｜符號對照＋ED｜同域接受契約；deny-all零誤接受／8誤拒絕，不是另一支已編譯C｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜rejection-as-delivery／7d4v（草稿L047）
c47｜請把合法輸入必須接受，也寫成另一個要檢查的條件。｜符號對照＋ED｜同域接受契約；deny-all零誤接受／8誤拒絕，不是另一支已編譯C｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜complete-acceptance-contract／6a2b（草稿L048）
c48｜兩個方向合起來，零到七都要放行，其他長度一律拒絕。｜符號對照＋ED｜同域接受契約；deny-all零誤接受／8誤拒絕，不是另一支已編譯C｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜complete-acceptance-contract／4akm（草稿L049）
c49｜開頭那份單向紀錄，現在補上合法輸入必須接受。｜符號對照＋ED｜同域接受契約；deny-all零誤接受／8誤拒絕，不是另一支已編譯C｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜full-domain-and-functional-result／w9b4（草稿L050）
c50｜這一列可以交付的是接受判斷，程式裡沒有寫入資料緩衝區。｜RUN-A｜僅bool接受判斷，沒有buffer寫入；無真實越界寫入事故｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜guard-object／dkjy（草稿L054）
c51｜我把加寬版的兩項結果填成零：沒有誤接受，也沒有誤拒絕。｜RUN-A｜加寬版完整256列：誤接受0、誤拒絕0；分開填紀錄｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/results.json｜2026-10-25｜save-two-error-columns／8ywa（草稿L051）
c52｜接受判斷這一列完成了；紀錄還有另一列，等著驗收返回。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/sat-output.json｜2026-10-25｜return-row-unfilled／xh98（草稿L052）
c53｜這張紀錄的返回欄，要怎麼填成可核對的要求？｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜return-contract-question／idga（草稿L055）
c54｜我用另一支獨立計數程式填返回欄；輸入是計數上限。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜independent-counter／u2xw（草稿L056）
c55｜上限仍是零到二百五十五，計數器從零開始。｜RUN-B｜獨立loop；n=0..255、i=0、i≤n則加1；n255本次0.25秒逾時被中止｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-start-and-rule／p4u6（草稿L057）
c56｜只要計數器小於等於上限，就加一，否則離開。｜RUN-B｜獨立loop；n=0..255、i=0、i≤n則加1；n255本次0.25秒逾時被中止｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-start-and-rule／v9sd（草稿L058）
c57｜把所需次數寫成上限加一，返回值也要等於這個數。｜RUN-B｜獨立loop；n=0..255、i=0、i≤n則加1；n255本次0.25秒逾時被中止｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-expectation／riuf（草稿L059）
c58｜輸入零，預期做一次加一，返回一。｜RUN-B｜獨立loop；n=0..255、i=0、i≤n則加1；n255本次0.25秒逾時被中止｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-zero／cgit（草稿L060）
c59｜輸入七，預期做八次加一，返回八。｜RUN-B｜獨立loop；n=0..255、i=0、i≤n則加1；n255本次0.25秒逾時被中止｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-seven／y326（草稿L061）
c60｜錯版用八位元計數器；上限二百五十四時，到二百五十五能離開。｜RUN-B｜獨立loop；n=0..255、i=0、i≤n則加1；n255本次0.25秒逾時被中止｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-254-exits／qmcd（草稿L062）
c61｜但上限改成二百五十五，執行在零點二五秒後被工具中止。｜RUN-B｜獨立loop；n=0..255、i=0、i≤n則加1；n255本次0.25秒逾時被中止｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜counter-255-timeout／b3r9（草稿L063）
c62｜它真的不會結束，還是我們等得不夠久？｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜timeout-not-enough／ijcq（草稿L064）
c63｜這次超過等待上限，光憑這點還不能斷定程式永遠不會結束。｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜timeout-not-enough／ihny（草稿L065）
c64｜要看每一步狀態，還得知道下一步會怎麼走。｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜inspect-transitions／4jzv（草稿L066）
c65｜這裡上限固定，沒有其他執行者改計數器。｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜fixed-counter-model／kfft（草稿L067）
c66｜八位元計數器從零加到二百五十五，下一次卻轉回零。｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜cycle-turns-to-zero／58rm（草稿L068）
c67｜條件仍然成立，上限也沒變，後面就會重走同一圈。｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜same-state-same-next-step／mjsr（草稿L069）
c68｜完整控制圖有二百五十六步的環，這個模型因此不能離開。｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜full-control-cycle／kq36（草稿L070）
c69｜逾時是這次執行的觀察；循環，才是控制圖給的理由。｜RUN-B控制圖＋ED｜固定n、無外部寫入者；n255的0..255→0、256步環；timeout非單獨證明｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜timeout-versus-cycle／qjaw（草稿L071）
c70｜那要讓它數完離開，哪裡得多留一個位置？｜RUN-B｜volatile uint16_t宣告與uint16_t更新轉型一起改；255→256後離開｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-needs-room／h6n5（草稿L072）
c71｜把計數器和對應轉型，改成十六位元無號整數。｜RUN-B｜volatile uint16_t宣告與uint16_t更新轉型一起改；255→256後離開｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-complete-repair／p8te（草稿L073）
c72｜到二百五十五再加一，這次能保存二百五十六。｜RUN-B｜volatile uint16_t宣告與uint16_t更新轉型一起改；255→256後離開｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-preserves-256／ghs2（草稿L074）
c73｜二百五十六大於上限，條件不成立，程式離開並返回它。｜RUN-B｜volatile uint16_t宣告與uint16_t更新轉型一起改；255→256後離開｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop.c｜2026-10-25｜counter-condition-fails／9mxr（草稿L075）
c74｜紀錄的返回欄有結果了：每個輸入都離開，並返回上限加一。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜counter-full-domain-exit／ey22（草稿L077）
c75｜返回值和離開條件，在同一列紀錄分欄填寫。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜counter-record-fields／5feu（草稿L079）
c76｜紀錄已分出接受與返回；Claude研究的證明，也驗同一種要求嗎？｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/origin.md｜2026-10-25｜formal-proof-question／rsx8（草稿L083）
c77｜把紀錄對回正式證明時，程式版本、命題和運作模型都要固定。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/origin.md｜2026-10-25｜fix-proof-object／zg4q（草稿L084）
c78｜公開版本的對象，是編譯好的RISC-V二進位程式。｜CITED｜本次公開release60入口／25庫；固定靜態riscv64 Linux binary；非研究覆蓋率｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜binary-object／wzn2（草稿L088）
c79｜Rocq核心在編譯時，檢查AI寫出的證明。｜CITED｜kernel在rocq compile時檢查term；wrapper固定statement型別並Print Assumptions；最後allowlist稽核｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md｜2026-10-25｜actual-proof-checking／cawx（草稿L089）
c80｜工具再把結果對到固定命題，列出它使用的假設。｜CITED｜kernel在rocq compile時檢查term；wrapper固定statement型別並Print Assumptions；最後allowlist稽核｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md｜2026-10-25｜actual-proof-checking／uqde（草稿L090）
c81｜使用的假設，也必須通過允許清單的稽核。｜CITED｜kernel在rocq compile時檢查term；wrapper固定statement型別並Print Assumptions；最後allowlist稽核｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md｜2026-10-25｜actual-proof-checking／5fga（草稿L091）
c82｜開頭的驗收問題，落在Rocq核心與工具對命題、假設的檢查。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md｜2026-10-25｜proof-preview-payoff／wi26（草稿L092）
c83｜檔案能編譯，還不等於目標完成；究竟要證明什麼？｜CITED＋ED提問｜編譯成功不足以替代固定statement與允許假設的檢查｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md｜2026-10-25｜what-is-proved／nzaz（草稿L093）
c84｜公開版比較同一程式的一般版與錯誤檢查版，並非剛才的修正前後。｜CITED｜agreement前提：一般版不超指定記憶體預算的輸入，於模型內兩版皆無指定錯誤｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜agreement-builds／7ip9（草稿L094）
c85｜在系統模型內，輸入須讓一般版不超過指定記憶體預算。｜CITED｜agreement前提：一般版不超指定記憶體預算的輸入，於模型內兩版皆無指定錯誤｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜agreement-premise-and-errors／6x7t（草稿L095）
c86｜符合這個前提，兩版都不會出現指定錯誤。｜CITED｜agreement前提：一般版不超指定記憶體預算的輸入，於模型內兩版皆無指定錯誤｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜agreement-premise-and-errors／5u3j（草稿L114）
c87｜有限的行為紀錄，可以包含程式已經輸出的文字。｜CITED＋原創白話例｜兩版可觀察的有限trace集合相同；輸出文字只是可觀察紀錄的例子，非新增vendor執行｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/statements.md｜2026-10-25｜finite-observable-traces／cnnu（草稿L096）
c88｜兩版可觀察的這些紀錄，允許的集合要相同。｜CITED＋原創白話例｜兩版可觀察的有限trace集合相同；輸出文字只是可觀察紀錄的例子，非新增vendor執行｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/statements.md｜2026-10-25｜same-observable-records／fwc2（草稿L113）
c89｜可是，行為相符會不會順便保證一定結束？｜CITED｜agreement不排除無限執行；只有此release沒有已證halts；不外推整個239案例研究｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/statements.md｜2026-10-25｜agreement-versus-halting-question／e7pc（草稿L097）
c90｜不會。這份公開版本沒有提供終止命題的證明。｜CITED｜agreement不排除無限執行；只有此release沒有已證halts；不外推整個239案例研究｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜this-release-no-halts／3jaw（草稿L098）
c91｜要保證執行會結束，得另外證明終止命題。｜CITED｜agreement不排除無限執行；只有此release沒有已證halts；不外推整個239案例研究｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/statements.md｜2026-10-25｜separate-halting-statement／e2mj（草稿L099）
c92｜這說的是這份公開版本，不代表整個研究都沒處理終止。｜CITED｜agreement不排除無限執行；只有此release沒有已證halts；不外推整個239案例研究｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜separate-halting-statement／4nfp（草稿L100）
c93｜官方研究報告涵蓋一百二十三個函式庫、二百三十九個入口。｜CITED｜官方研究公告；日期／測試要求到命題／239入口與123庫皆屬官方報告｜https://www.anthropic.com/research/formal-verification｜2026-10-25｜research-versus-public-release／cr5k（草稿L085）
c94｜目前公開版本則列六十個入口，來自二十五個函式庫。｜CITED｜本次公開release60入口／25庫；固定靜態riscv64 Linux binary；非研究覆蓋率｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜research-versus-public-release／b7jg（草稿L086）
c95｜這份紀錄還得標版本；研究總量和手上公開版本，要分開填。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md｜2026-10-25｜separate-release-column／i2pt（草稿L087）
c96｜把我們那份紀錄的檢查方法也補上，就能看清交付的差別。｜RUN-A/B＋CITED對照｜guard列舉／命題SAT，loop有限控制圖，兩者均有實際C；未執行官方Rocq｜https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md｜2026-10-25｜official-and-local-methods／te3s（草稿L101）
c97｜接受判斷用完整列舉與命題求解，返回條件用有限控制圖。｜RUN-A/B＋CITED對照｜guard列舉／命題SAT，loop有限控制圖，兩者均有實際C；未執行官方Rocq｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜local-methods／iest（草稿L102）
c98｜兩者都有實際C執行對照，沒有跑過新聞中的Rocq檢查器。｜RUN-A/B＋CITED對照｜guard列舉／命題SAT，loop有限控制圖，兩者均有實際C；未執行官方Rocq｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜actual-c-and-no-rocq-reproduction／3u2q（草稿L103）
c99｜我做的結果只涵蓋這兩個本地範例，不是整個應用程式的認證。｜RUN-A/B＋CITED對照｜guard列舉／命題SAT，loop有限控制圖，兩者均有實際C；未執行官方Rocq｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜local-scope／ucn4（草稿L104）
c100｜紀錄裡分開標出總長的修正，和計數器宣告、更新式的修正。｜ED完成紀錄＋RUN版本綁定｜兩份原始C與結果各自保存；非新實驗／未宣稱媒體通過｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜complete-modification-record／bt2j（草稿L105）
c101｜重跑時先對版本，再把預期和實際結果放在同一列。｜ED完成紀錄＋RUN版本綁定｜兩份原始C與結果各自保存；非新實驗／未宣稱媒體通過｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜expected-versus-observed-delivery／mj65（草稿L106）
c102｜這樣才不會拿改好的程式，去對另一份舊程式的答案。｜ED完成紀錄＋RUN版本綁定｜兩份原始C與結果各自保存；非新實驗／未宣稱媒體通過｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/guard.c｜2026-10-25｜version-bindings／edry（草稿L107）
c103｜把驗收條件寫成明確要求。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://github.com/x812033727/travel_scanner/blob/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data/loop-results.json｜2026-10-25｜completed-repair-record／mhjn（草稿L108）
c104｜留言分享你用AI寫程式的情境。｜原來源RUN／CITED＋ED紀錄操作；同一紀錄連結，兩支C獨立，非新增實驗｜https://www.anthropic.com/research/formal-verification｜2026-10-25｜completed-repair-record／87s6（草稿L109）
c105｜訂閱，一起用真實結果讀懂AI研究。｜ED互動／訂閱邀請｜符合既有頻道立場；不新增事件或製作承諾｜https://www.anthropic.com/research/formal-verification｜2026-10-25｜completed-repair-record／22tu（草稿L110）

## 畫面上的補充主張

- A原式完整節錄為`uint8_t total = (uint8_t)(n + 1);`；修正式完整節錄為`uint16_t total = (uint16_t)((uint16_t)n + 1u);`。不能只改左側宣告；保留右側uint8_t時，256已先窄化為0。L024是依原式推演，不冒充額外編譯實驗。
- B修正必須同時使用`volatile uint16_t i = 0;`及`i = (uint16_t)(i + 1u);`。不能只換i宣告卻保留8bit更新轉型。
- 原生表顯示錯版接受0..7與255共9個，加寬版8個；一律拒絕符號對照0個。資料包另存直接上界版的完整C結果，但本版不再口述其別解，也沒有另做其SAT查詢。數量是本例行為，不是模型準確率。
- D1完整SVG在修法與拒絕255已講出後才呈現；D2+D3合圖在deny-all誤拒8已講出後才呈現；D4分cycle及exit，第二例不畫成guard下游。
- D5已按公開checking原文更正：Rocq核心在proof與wrapper編譯時都檢查term，wrapper對指定statement型別並列出假設，最後allowlist audit。本片沒有執行該checker。
- agreement前提特指一般版的指定記憶體預算，並在相應系統模型內。兩版可觀察的有限行為軌跡集合相同；不是兩次執行逐步鎖定同步，亦不自動證明終止。公開版本沒有halts證明的結論只留在此版本。
- version-bindings的guard.c SHA前8碼4bfc837e與loop.c前8碼b1d18170，均直接對應本輪保存原始檔；完整雜湊在資料包manifest。不是另一份新程式的結果。
- 正式6張SVG及專用thumbnail-guard.svg／PNG為Mokaair原創，assets已登記source／license／author；C兩檔也登記原創來源。原創圖沒有真實事故、產品UI、IDE操作或供應商checker成功截圖。素材代理已渲染實看；本片原生樣卡與成片仍由root另檢。
- 本片唯一英文逐字短引為README的“No proof in this release proves a halts statement.”，9詞。其餘官方敘述為短篇原創解釋，每來源約200英文字等量內；不挪用供應商proof程式碼。

## 示範輸入、操作、預期、觀察與核對

### A：接受判斷

輸入：n為0..255的整數資料長度，容量8byte，另需1byte結尾。預期：應且只應接受n+1≤8，也就是0..7。

操作：先讀錯版n+1的int完整值與uint8_t窄化值，對照255→256→0的比較；把計算、轉型與總長儲存完整改成guard_widened的16bit運算式。直接n<8版是同契約別解，不算新案例。

觀察：錯版只多接受255；修正版接受0..7，誤接受／誤拒絕各0。獨立命題位元模型逐值對C256/256相符，加寬版的誤接受與誤拒絕查詢皆UNSAT；直接上界版只有完整C結果及逐值對照，沒有另做其SAT查詢。符號deny-all雖零誤接受，但0..7共8個全誤拒；這一臂沒有已編譯C。

核對：比對data/all-256-cases.json與compiled-c-results.csv，原始C hash在data/manifest.json；SAT公式／回傳在sat-output.json。本地結果支持這份契約，不含真實buffer寫入或整個應用認證。

### B：獨立計數器

輸入：另一份程式，n作計數上限，仍為0..255，i=0。規則：i≤n則加1。預期：n+1次增量後離開，返回n+1。

操作：對照錯版8bit宣告及更新轉型，完整走固定n255的狀態轉移；再把i宣告及更新轉型都改為uint16_t。

觀察：錯版n0..254返回，n255於本次0.25秒逾時中止。控制圖0..255→0建立256步環；不能只用timeout說無限。修正版全256個C呼叫及控制圖均返回預期n+1，n255時返回256。

核對：loop-all-256.json逐例包含模型與實際C；loop-results.json保存逾時命令與預期／實際。只分析固定n、無外部寫入者的本地volatile計數器，不泛化OS排程／並行／通用停機問題。

## 與企劃不同的地方

- 保留選A的一條主線、七章與三個冷開預告。首章加入2026-10-25本次執行日期的真實誤接受場景，沒有目錄、機制劇透或假人物。
- 同一份紀錄連結兩個獨立程式；正文刪除n<8別解支線；資料包保留該版完整C結果，但未稱另做SAT查詢。
- 依來源核對完整展示左右運算式與loop兩處修正。官方檢查順序按新checking原文更正；一般版預算前提及有限trace都保留。
- 將有限軌跡用已輸出的文字作原創白話說明，仍保留可觀察、有限與集合相同；未新增未執行的vendor範例。
- 刪除重複的單例返回結算、兩列重述及計數完成總結，直接用開場回呼的全域實際返回結果收束。
- 不製作Shorts；教學卡片無shot。八外語仍走各自翻譯、獨審、實際配音與fit，不能以本稿宣稱語言交付完成。

## 我懷疑但沒動的事

- 形式驗證新聞與本地概念實算的教學價值，仍需正式盲讀／聽眾審查；本檔不自行判定敘事全過。
- 實際旁白長度與卡片overflow尚未量測；文字估時不是音長。若音訊不足正文8分鐘，依真實內容再補，不能加空停頓。
- C／SAT／Rocq／RISC-V由root正常共享字典程序新增，尚未試聽，null不當作已聽過的證據。既有Sulafat與style未改。
- 公開checker是CITED，未下載／執行；rocqchk也沒有在本片使用。不借kernel名義抬高本地SAT或圖探索的保證。

## 進度

正式video.json與逐句claims已完成；所有scene均有真實口白，不含佔位文字。此版為一次有界R1，以同一紀錄的完成／空白／填入進度連結兩個獨立程式。初稿未通過的原生敘事及verify-1原封保留；本版待新的facts與fresh原生敘事，未自稱通過。尚未TTS、音檢、正式卡片QA或成片QA；各關卡由真實收據決定。


## R1版本差異與待驗

開場明示2026-10-25本次執行，三個預告停在答案前。同一張紀錄從接受判斷完成、獨立返回欄待填，到填入返回結果，再對回官方固定命題；沒有把guard輸出接成loop輸入。刪除直接上界別解及重複零誤差／返回結算。完整C修法、輸入域、算式、結果、官方數量與保證前提未擴張。縮圖採1440×1360原創專用圖；靜態原生克隆預覽不等於本版成片QA。
