export default {
 id:'B14',
 manual_shot_overrides:[{first_shot:5,last_shot:7,paragraph_ids:['H04','H05','H06'],mode:'one-paragraph-per-shot',reason:'Keep each opening preview and the main question visually intact; no narration edits.'}],
 hook_visual_reuse:[{setup:4,recovery:22,setup_paragraph:'H03',recovery_paragraphs:['I01'],reason:'同一研究資料與素面調味罐圖回收安全疑問，不畫疾病或下毒暗示'},{setup:5,recovery:60,setup_paragraph:'H04',recovery_paragraphs:['T01'],reason:'同一薄膜與封裝基板示意圖回收1999上市，不把膜當晶片本體'},{setup:6,recovery:73,setup_paragraph:'H05',recovery_paragraphs:['T07'],reason:'同一訪談資料與材料模型圖回收2026市場預告，95%留到S075'}],
 source_aliases:['S1','S2','S3','S4','S5','S6','S7'],
 claims:{C01:[0],C02:[2],C03:[4,5],C04:[4],C05:[0],C06:[0],C07:[1],C08:[1],C09:[1],C10:[2],C11:[3],C12:[3],C13:[4],C14:[4],C15:[4,5],C16:[4],C17:[4],C18:[5],C19:[5],C20:[5],C21:[4],C22:[4],C23:[5],C24:[4],C25:[3,4],C26:[4],C27:[4,5],C28:[6],C29:[6],C30:[6],C31:[6],C32:[6],C33:[4],C34:[5]},
 claim_section_end:'## 四、Loops／編排檢查',
 boundaries:['食品安全線與材料研究線分開；1969爭議不是ABF研發已證起因。','1980認可是公司社史說法；FDA問答的GRAS與1990年代受委託審查、少數敏感者未伴食物一次≥3g短暫輕微不適，分開呈現。','舊製程氯化石蠟副產物只是歷史研究起點；不是現今MSG或ABF配方，不畫食品倒進晶片。','晶片、封裝基板、絕緣層、線路分清。圖用大型教學模型／工序示意，不讓AI生成精確工程剖面或可讀線路標籤。','1996客戶需求、深冷樹脂、週末測試與1999引介來自公司2020回顧，不猜客戶品牌、化學原因或四個月完成量產。','約95%只限2026公司主管所述高效能電腦／資料中心伺服器FC-BGA類封裝的絕緣材料市場，不是所有晶片／封裝市占。','T03a/T04受審原文保留，以同一測試流程視覺段落銜接；active row提出的正式章稿合併要求仍待後續編輯與審查，不補字。'],
 loops:[{setup:['H01','H02'],payoff:['O01','O04','O06'],purpose:'成分到專利、再到商品化，順序推進'},{setup:['H03'],payoff:['I01','I02','I03','I04'],purpose:'安全疑問回收，分清公司史與FDA不同範圍'},{setup:['H04'],payoff:['E01','E03','E04','T01'],purpose:'工序困難後，口頭回收開場薄膜與1999上市'},{setup:['H05'],payoff:['T07'],purpose:'首次95%，同時口頭保留公司歸屬及FC-BGA絕緣材料範圍'},{setup:['I08'],payoff:['E01','E02'],purpose:'電流不該相連處需絕緣'},{setup:['E05'],payoff:['E05a','E05b','E06','E09','T02'],purpose:'需求、配方、加工形成薄膜方案'},{setup:['E06a'],payoff:['E07a','T00'],purpose:'材料之外，機器測試與客戶採用'},{setup:['T03'],payoff:['T03a','T04','T05','T06'],purpose:'多樣需求延伸到測試及早期客戶合作'},{setup:['H06'],payoff:['N05'],purpose:'最後才完整連起材料技術與封裝需求'}],
 look_plans:[{id:'generic_researcher',purpose:'一般化研究員從試材、選樹脂到試機；不冒充池田、Nakamura或真實主管肖像，跨時期不暗示同一人。'},{id:'generic_technician',purpose:'當代材料技術員用素面外套與大型模型，維持晶片／基板／膜的物件辨識，不做精確工程重建。'}],
 adaptation:[]
};
