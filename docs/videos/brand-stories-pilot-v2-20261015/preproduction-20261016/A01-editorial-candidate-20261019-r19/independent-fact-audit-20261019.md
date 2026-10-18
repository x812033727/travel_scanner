# A01 r19 獨立史料與主張稽核 — HOLD

- 日期：2026-10-19；審查範圍：r18 的 73 筆主張及 r19 新增的 `t46`，共 74 筆；只讀審查，未改候選、來源、任務票、PR 或正式機。
- 綁定 `manifest.json` SHA-256：`9E2EBDD0C82F61BAA8CF50041B13E47E1070BD0C7950D2E577890313D6DB1F6E`。
- 綁定 `candidate/script.md` SHA-256：`42088C3BDDFEF3422FC9AA9E49F7FF68EF532693D533C289D685F079B1A2CABF`。
- 綁定 `candidate/video.json` SHA-256：`8726BFE0697088ACBF69803684E3E51BC7B340F5CA89B706EBD3BFE10CFC7F41`；`candidate/claims.md`：`E53196BBB1348930A9B0B9DB107BCBD965D23B426BF1AD5BCC6336167DC7CFBD`；`source-alignment.json`：`013424AC4E63C874C8429683D4B5F53DBD98E51509E525549F9C92B322B0246C`。
- 結論：**P0 0、P1 2（同一史料過度推論：`t5`、`t46`）、P2 3（`h4`、`o1`、`n61`）；HOLD。** 這是離線候選的獨立史料稽核，不是正式機六章 verifier、listener、兩名敘事讀者或 `story/reviews/script-review.json` 的核准。

## P1：安檢旅客是否真的卸下箱子

`t5`（`turn-05`，沿用 r18）說 Plath 看見前方旅客「解彈力繩、將箱子從外置金屬推車卸下」；r19 新增的 `t46`（`turn-06`）說旅客「費力解開……彈力繩，將箱子從推車取下」。[2012 年 USA TODAY／ABC 刊載的報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)只說安檢隊伍前方旅客正費力**試圖**把以彈力繩綁住的行李從笨重金屬推車解開，沒有交代是否成功卸下。這段是記者敘述，不是 Plath 逐字直接引言；他的直接引言是後段與安檢員的對話。[Plath 的專利](https://patents.google.com/patent/US4995487A/en)描述外置推車在安檢與登機反覆拆裝的通則，也不能獨立證實那名旅客完成卸箱。

兩筆主張都應改為「正費力想解開／取下」，不說已完成；`t5` 的「Plath 受訪回憶」宜改成「2012 年受訪報導記述」。目前口播 `turn-05` 的「正費力處理」及 `turn-06` 的「得解開繩子，再把箱子卸下來」是困境與所需步驟，沒有斷言已成功；`turn-06` 圖像提示詞 `strains to free` 也停在嘗試階段。可保留口播與畫面，只窄修兩筆主張並重算候選與收據。r19 不能沿用 r18 的限縮審查作正式通過。

## P2：歸屬與措辭精度

1. **`h4`／`hook-04`：**口播與主張說「1970 年，Sadow 帶著樣品走進百貨公司」。所引 [ABC 2010 年 Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)只直接給出調整樣品、拜訪與被拒、Macy's 於 1970 年 10 月展示人偶的順序；沒有明記各次拜訪日期。[Sadow 2010 年《紐約時報》受訪，RNPA 2016 年重印第 48 頁](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)稱機場啟發在 1970 年、其後用數月推銷，可補此來源支持年份脈絡；或者口播拿掉精確年份。此處未判為年份已錯。
2. **`o1`／`origin-01b`：**「第二次環遊世界」可能讓觀眾以為 1921 年第一次已環繞全球。[Winnetka 歷史學會輪箱文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)概稱兩次 world tours，但其[家族史頁](https://www.winnetkahistory.org/who-were-the-burnhams/)具體寫 1921 年旅行以歐洲與非洲為主，1928 年才是第二趟較廣的旅程。為免造成兩次環球之印象，可寫「第二趟長途旅行」；`origin-r12-01` 的「第二次環遊」也應一起檢查。
3. **`n61`／`now-outro`：**「沒有史料把三人的故事直接接成發明傳承」是對不存在證據的廣泛斷言；Winnetka、Sadow 和 Plath 的各篇來源只足以說本集審閱的史料**未證實**三人間的直接傳承。片尾「這三人的故事沒有可證實的直接傳承」已較保守，但主張表和口播仍可限縮為「本集查到的資料，沒有證實三人直接傳承」，避免暗示已搜盡全部史料。`n16`、`n63` 的相同界線應連帶保持一致。

## 74 筆的核對方法與界線

逐筆對照 `candidate/claims.md`、`candidate/script.md`、65 鏡的 `candidate/video.json` 與 `source-alignment.json`。74 個主張 ID 各唯一，74 個場景主張引用各唯一；r19 的 `turn-06` 已綁 `t46`。只有 `turn-security-question`、`now-consumer-question` 兩個純提問鏡頭沒有主張。這些結構檢查只證綁定存在，不證每句史實成立。以下列出每個被查 ID 所依的來源與讀取方式；「直接」表示開啟原頁全文或 PDF 原頁，「索引」表示官方／原始來源的搜尋擷取文字，並非直接讀完整原頁。

| 來源、核對 ID | 讀取 | 本輪結果 |
| --- | --- | --- |
| [ABC 2010 Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)：`h1 h3 h4 i35 i36 i21 i22 i34 i23 i25 e26 e27 e28 e29 e30 e31 e32 e33 e35 n17 n16` | 直接全文 | 除 `h4` 日期歸屬外，所述細節與當事人回憶／報導相合。 |
| [Winnetka 輪箱收藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)：`h10 h9 o25 o2 o1 o29 o26 n61` | 官方索引全文擷取；原頁逾時 | `o1` 第二次環球措辭、`n61` 無直接傳承的界線如上。 |
| [USA TODAY／ABC 2012 Plath 報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)：`h6 t5 t46 t6 t17 t29` | 直接全文 | `t5`、`t46` 把嘗試卸箱寫成完成；其餘事件有歸屬。 |
| [Winnetka 1921 旅行文章](https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/)：`o30`；[Winnetka 家族史](https://www.winnetkahistory.org/who-were-the-burnhams/)：`o32` | 官方索引全文擷取；原頁逾時 | 家人守著行李與母女以畫換餐宿的主張有文獻；不將場景固定成某一站。 |
| [1939 年 2 月 9 日 Midland 原報紙掃描](https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download)：`o27 o34` | 原始館藏的搜尋 OCR；完整 48 MB PDF 因 TLS 逾時未逐頁視讀 | OCR 支持前日茶會、黑斗篷、實用帽、輪箱與另一袋；具體版面及辨字仍需正式複核。 |
| [Sadow 1970 年申請的專利](https://patents.google.com/patent/US3653474A/en)：`i26 i24 i32 i33` | 直接全文 | 航站搬運背景、申請日期、可拆拖帶、原提把相合。 |
| [Yale 2008 Shiller 講課逐字稿](https://oyc.yale.edu/economics/econ-252-08/lecture-3)：`e37 e38`；[Yale 2011 講課逐字稿](https://oyc.yale.edu/economics/econ-252-11/lecture-3)：`e39` | 直接全文 | 轉述搬運工異議、2008 個人晃擺經驗與 2011 翻倒概述皆有分開歸屬；不採納講課裡「第一只」或專利年份等不準確概括。 |
| [Travelpro 公司沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)：`e34 t4 t7 t31 n40 n42 n43 n63`；[Travelpro 公司故事](https://travelpro.com/pages/our-history)：`n41` | 直接全文 | 廣告語、747 機師、公司所稱 1987 設計、機組採用、1989 倉庫、1991 離職均有歸屬。 |
| [RNPA Contrails 2016 年 PDF](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)：`t39 t40 t41 t42 t43 t44 t45 n44` | 直接讀原 PDF 第 46–48 頁 | 第 46–47 頁為 Bill Emmer 第一人稱記憶，未標那段故事年份；第 48 頁是 Joe Sharkey 2010 年《紐約時報》文章重印，作者沒有混作 Emmer。 |
| [Plath 1989 年申請的專利](https://patents.google.com/patent/US4995487A/en)：`t21 n62` | 直接全文 | 只支持外置推車的通則限制，不證實那位特定安檢旅客的動作。 |
| [West Seattle High School Alumni Association《Chinook》2024 年 PDF](https://wshsalumniassociation.org/wp-content/uploads/2024/05/Chinook-May-2024.pdf)：`t7b` | 直接讀官方 PDF 第 17 頁 | Plath 自填簡歷寫 1988；與 Travelpro 公司 1987 的分歧應保留歸屬。候選引用的 `sl8.com` 鏡像未另比對逐位元組。 |
| [Global Traveler 2007 年 Kim Ballis 訪談](https://www.globaltravelerusa.com/reinventing-the-wheel/)：`n45` | 原刊索引全文擷取；原頁逾時 | 當時執行長說其他機師請 Plath 製作；不據其回溯年份定年。 |
| [Judi Dash 1993 年《洛杉磯時報》實測](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)：`n55 n56 n57 n58 n59` | 直接全文 | 四家受測、主要百貨**或**專賣店、機艙收納與外袋實測均限於原文。 |
| [Samsonite 2011 年招股書第 80 頁](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf)：`n1`；[Travelpro 樓梯比較](https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases)：`n14` | 直接全文 | 1997 平衡四輪直立箱及「部分旅客」走樓梯困難的範圍相合。 |

61 筆可由直接開啟的原頁／PDF 全文對讀，13 筆僅以原刊或館藏的索引文字抽核，特別是 `o27/o34` 仍需直接檢視 1939 年掃描版面。此輪沒有做圖像、實際 TTS、媒體長度、正式機 104→新版接續或每章模型審稿。所有 74 筆仍為 `PENDING`；尚未發正式主機可採納的驗收收據。`candidate/series.json` 只有 23 個編輯來源，企劃索引 23／24 另在 25 個來源的擬採用提案中，不能拿這份離線稿直接替代正式機來源企劃。
