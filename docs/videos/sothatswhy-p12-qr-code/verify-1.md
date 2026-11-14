# 查核報告 1（sothatswhy-p12-qr-code）

- 查核者：獨立查核與評分代理（未參與撰稿）
- 日期：2026-11-14
- 方法：逐句讀 `video.json` 的 159 句台詞（`p001`–`p159`，與 `script.md` 的 80 個場景一一對應）、`youtube.title`、`youtube.description`、`thumbnail.data`（`headline`、`sub`），以及全部 80 個場景的 `data.prompt` 畫面提示詞。本集沒有卡片（全部是 `shot`）。對照 `brief.md` 的邊界禁區與 `claims.md` 的 C01–C11，並另外獨立查核 `claims.md` 之外或跨段銜接的句子（超商結帳紅光刷碼、同心回字框斜切比例幾何、1994 年發表與一年半研發時序、Reed-Solomon 1960 年發明背景、正中央貼小圖案與容錯額度、Alphanumeric 英數模式字元集限制、Model 2 各版本校正圖形有無與術語一致性、轉寫稿單讀是否有未交代道具詞）。每一條都重新抓取來源讀英文原文核對（含 `qrcode.com/en/about/` 與 `version.html` 透過 jQuery `.load()` 載入的 `featurePage1–6.html`、`versionPage1_10.html`、`versionPage31_40.html`、`versionPageMixed.html` 子頁），不只沿用 `claims.md` 的引文。
- 打不開的來源：無。`video.json` 列出的 9 筆來源與其動態載入子表全部成功抓回原文；另補查 Wikipedia「QR code」與「Reed–Solomon error correction」核對技術史與模式字元集。
- 字數：19 句替換台詞均已用程式逐句驗算，不論含標點總字數、去標點實字數或 `build_scenes.py` 的 `spoken_units` 均**等長或更短**，且全片「你」字次數不減、最長句壓回 25 實字以內。
- 結論統計（台詞 159 句）：OK 140、FIX 19（歸納為 F01–F10 共 10 組問題）、NOT FOUND 0。另外標題、說明、縮圖共 3 項：OK 2、FIX 1（`youtube.description` 見 F11）。80 景畫面提示詞沒有事實錯誤（附 2 則生圖防呆建議）。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F01 | p005、p027–p028、p085（所長） | 一九九四年兩位工程師天天量傳單線條在找什麼？／還記得開頭提到的一九九四年嗎？／日本 DENSO WAVE 的工程師原昌宏，當時團隊只有兩個人！／DENSO WAVE 官方舉了一個很清楚的算例： | FIX（年份歸屬與 1994 年組織名稱） | ① DENSO WAVE 官方歷史頁（`qrcode.com/en/history/` Section 1–2）：原昌宏與另一名成員在專案初期統計傳單、雜誌、紙箱找出 `1:1:3:1:1` 比例後，歷經**一年半**反覆試誤才完成開發（"A year and a half after the development project was initiated and after innumerable and repeated trial and error, a QR Code … was finally created"），並於 **1994 年發表**（"In 1994, DENSO WAVE (then a division of DENSO CORPORATION) announced the release of its QR Code"）。1994 是發表年，不是初期天天量傳單的年份（推算約 1992–1993）。② 1994 年尚無獨立的 DENSO WAVE 公司，當時是 DENSO 旗下部門（官方歷史頁特別括號註明 `then a division of DENSO CORPORATION`；本庫 `s2-A26-A38.md` A36 亦明列勿把 DENSO WAVE 說成 1994 年即為獨立公司）。把 `p005` 改「當年」、`p028` 改「一九九四年發表時，DENSO 的原昌宏團隊只有兩個人」，並在 `p085` 補「開發方 DENSO WAVE」銜接，時序與組織名稱皆精確且不產生轉寫孤兒詞 |
| F02 | p014（所長） | 你在超商結帳應該看過，沒對準紅光方向就刷不過。 | FIX（生活例子過度概化） | 9 筆來源均未提超商結帳。台灣現行超商（7-Eleven、全家等）為刷手機載具與電子發票 QR Code，櫃檯多已改用二維影像式掃描器（2D imager），超市檯面亦多為多向雷射窗，斜拿一維條碼照樣能嗶過，小朋友去超商實測容易發現與台詞相反。真正「沒橫切過整排線條就讀不到」的是**傳統單線紅光刷條碼**，限定清楚即完全成立 |
| F03 | p034（所長） | 猜猜看，所有印刷品裡最罕見的比例是幾比幾？ | FIX（過度肯定） | `qrcode.com/en/history/` 原文："surveying innumerable examples of printed matter … Eventually, they came up with the least used ratio of black and white areas on printed matter"。兩人統計的是抱來的大量傳單、雜誌與紙箱樣本，並非普查世上「所有印刷品」。改「這些印刷品裡」精確扣回前句 `p032` |
| F04 | p055（所長） | 最小的版本一，每邊是二十一乘二十一顆模組； | FIX（幾何語病，易算錯） | `qrcode.com/en/about/version.html`："Version 1 (21 × 21 modules) up to Version 40 (177 × 177 modules). Each higher version number comprises 4 additional modules per side." 版本一**每邊**是 21 顆模組，**整張正方形**才是 21×21（441 顆）模組。原句說「每邊是二十一乘二十一顆」，緊接 `p057` 又說「最大版本四十，每邊有一百七十七顆」，小朋友按字面算會以為版本一每邊 441 顆比版本四十還大。改「整張是二十一乘二十一顆模組」即消歧義 |
| F05 | p068、p079–p080（所長） | 原資料裝成一排木盒後，後面會再加上一排數學算出來的修正碼字。／就算中間那碗被蓋住了，你拿十減掉三和二，／馬上就算出裡面一定是五！ | FIX（未交代的插圖道具詞闖入台詞） | 單讀轉寫稿會出現兩處沒頭沒尾（`no_orphans`）：① `p064` 只說「打包成一小盒」，`p068` 卻突然冒出插圖材質「木盒」；② `p077`–`p078` 只說「三個數字，三、五、二」，完全沒提碗，`p079` 卻突然說「中間那碗」。分別改成「小盒」與「中間那個數／中間」，轉寫稿獨立可讀，且與畫面木盒、三碗彈珠依然完全契合 |
| F06 | p070（所長） | 就是開頭提到，為了保護遙遠太空通訊而開發的！ | FIX（技術史初衷過度簡化） | DENSO WAVE `error_correction.html` 頁尾註解雖簡寫 "originally developed as a measure against communication noise for artificial satellites and planetary probes"，但核對 CMU 教材（Riley & Richardson [9]）與技術史（Reed & Solomon, *J. SIAM* 8(2), 1960；Wikipedia「Reed–Solomon error correction」）：1960 年 Reed 與 Solomon 在 MIT 林肯實驗室提出此碼時是一般抗雜訊通道的多項式理論碼，至 1969 年 Berlekamp–Massey 解碼法與 1977 年航海家號（Voyager）採用後才成為深空探測經典防護。改成「連遙遠太空通訊都靠它保護訊號」，同時相容官方頁、CMU 教材與嚴格數學史，且不必動 `p006` 與 `p071`–`p074` |
| F07 | p087–p088（所長） | 那就必須加上兩倍、也就是一百盒修正碼字，／兩邊合起來，總共變成兩百盒碼字！ | FIX（漏講關鍵數字導致下句未卜先知） | 全片從 `p001` 到 `p088` 從未出現「百分之二十五」，所長在 `p088` 只講到「總共變成兩百盒碼字」，小問卻在 `p090` 突然抗議「不是一半嗎？怎麼只算百分之二十五？」，變成小問自己背出還沒講的官方規格。在 `p087`–`p088` 先由所長點出「官方把修正率算成百分之二十五」，`p089`–`p090` 的反問才合乎對話邏輯 |
| F08 | p127（所長） | 帳本卻一口氣壞了八盒，額度瞬間爆表！ | FIX（過度肯定且與前章算例表面衝突） | 前章 `p093` 才剛講過「兩百盒裡壞五十盒都能修好」；此處八盒雖在版本一 M 級（最多修 4 盒）確實爆表，但若直接斷言「壞了八盒，額度瞬間爆表」，在大容量碼未必超限，且容易讓記得「能修五十盒」的小朋友困惑。改為「額度就很容易爆表」，精確傳達分散損傷四倍消耗額度的風險而不作絕對保證 |
| F09 | p136–p139（所長） | 反過來，要是網址長達五十個英數字元，／M 級的版本二最多只裝三十八個，那怎麼辦？／想把剛剛那五十個字元全塞進去，整張碼就得升級到版本三，／每邊長大成二十九乘二十九顆模組才裝得下！ | FIX（編碼模式錯誤＋未調高容錯＋每邊語病） | 三個問題疊在一起：① QR Code 的「英數字元（Alphanumeric）」模式僅支援大寫 `A–Z`、`0–9` 與 9 個符號（` $%*+-./:`），**不支援小寫 `a–z`**（Wikipedia「QR code」§Encoding）；一般含小寫的 `https://` 網址須走 8 位元 Binary 模式，而 `versionPage1_10.html` 載明版本三 M 級 Binary 上限僅 **42** 字元，根本裝不下 50 字元網址！② 小問在 `p131` 問的是「為什麼不全開 H 級」，`p142` 總結「本來想讓它更耐髒，結果格子太擠」，但原句全程固定在 M 級（50 個英數字元連版本二 L 級上限 47 都裝不下），沒有示範「調高容錯導致升版」。查同一張官方表 `versionPage1_10.html` **純數字（Numeric）**欄：**50 個純數字在版本二（25×25）M 級裝得下（上限 63），一旦改開 H 級只裝 34 個，必須升到版本三（29×29，H 級上限 58）**——既沿用 `p134` 的純數字、完全符合第 69 鏡 `version-upgrade-grid`（25×25 滿出來 vs 29×29 裝得下），又讓因果徹底咬合！③ `p139` 刪去誤植的「每邊」。`claims.md` C11 的括號算例同步更新 |
| F10 | p155（所長） | 不妨看看它的乾淨白邊，還有右下附近那顆小對齊框！ | FIX（版本一無此框＋術語前後不一） | ① 前文 `p041`、`p045`、`p152` 皆稱「小校正圖形／小校正框／校正框」，未曾出現「對齊框」。② Model 2 的版本一（21×21）**沒有**校正圖形（0 顆），版本二至六有 1 顆在右下附近，版本七以上有多顆；且 `qrcode.com` 公開頁 [4] 未保證每張碼右下必有唯一一顆。改為「找找右下附近有沒有小校正框」，任何版本的實物觀察都成立 |
| F11 | `youtube.description` | …一九九四年開發團隊怎麼從成堆印刷品裡找出最罕見的黑白比例…為什麼一整滴咖啡跟散開的小墨點命運完全相反。 | FIX（與 F01、F08 同步收緊） | 同 F01、F08：把「一九九四年開發團隊」改為「一九九四年問世前，兩人團隊」，避免誤讀為 1994 年當下才量傳單；把「命運完全相反」改為「為什麼遮住一樣大，一整滴咖啡跟散開的小墨點結果可能完全相反」，補上保留語 |

## 二、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p004 | 飲料店一張沾冰咖啡的 QR Code 掃得過，旁邊花邊貼很近的新碼卻掃不過 | OK | DENSO WAVE [1]、[5] | 開場具體情境設定，對應部分污損有機會還原（[1] `featurePage4`）與四周須留 4 格靜區（[5]），未宣稱任意污損必過 |
| p006–p008 | 保護太空探測器的數學藏在方塊裡；遮一樣大整滴咖啡與小墨點命運相反；核心提問（p005 見 F01） | OK | DENSO WAVE [7]；CMU [9] | 開場懸念與核心提問；航海家號等深空探測器確實使用 Reed-Solomon 碼保護訊號，集中 vs 分散在 p116–p129 完整展開 |
| p009–p013 | 小問猜從左上角讀；傳統一維條碼往單一方向排線條，最多大約裝 20 個英數字元（p014 見 F02） | OK | DENSO WAVE [1]、[3] | [3]："With barcodes, information is coded in one direction (one dimension) only"、"a barcode can only hold 20 alphanumeric characters or so"；[1] `featurePage1`："approximately 20 digits"。「大約」保留語正確 |
| p015–p026 | 一般方形 QR Code 橫直雙向裝資訊、三個角落放回字形定位框、360 度皆可抓位置；第四角不畫大框才分得出上下左右；小問問桌上黑線干擾 | OK | DENSO WAVE [1]、[2]、[3] | 限定「一般方形的 QR Code」（排除單角 Micro QR 與長方形 rMQR）；[2]："360 degree (omni-directional), high speed reading … through position detection patterns located at the three corners"。四角全同旋轉 180° 對稱不可分屬直接幾何事實，未引未購 ISO 座標公式 |
| p029–p033 | QR＝Quick Response（快速反應）；先挑商務表單最少見的正方形，再抱傳單、雜誌、紙箱轉成黑白連日統計寬度（p027–p028 見 F01、p034 見 F03） | OK | DENSO WAVE [3] | [3]："The QR in the name stands for quick response"、"it was the pattern least likely to appear on various business forms"、"fliers, magazines, cardboard boxes … all day long for days on end"。遵守 `brief.md` 未引無測試條件的「快 10 倍以上」，也未講圍棋傳聞 |
| p035–p038 | 罕見比例為 `1:1:3:1:1`；橫、直、斜切過回字框正中心皆為此黑白寬度比 | OK | DENSO WAVE [3]；幾何驗算 | [3]："This ratio was 1:1:3:1:1 … regardless of the angle of scanning, which could be any angle out of 360°"。以同心正方形半寬 1.5、2.5、3.5 驗算，過中心任意角度之截線段皆乘上同一比例因子，黑白寬度比恆為 `1:1:3:1:1` |
| p039–p044 | 日常改良版 Model 2 內藏小校正圖形；印在彎曲飲料罐或斜拍變形時可參照對齊 | OK | DENSO WAVE [4] | [4]："QR Codes that are printed on a curved surface or whose reading images are distorted due to the reading angle can be read efficiently by referring to an alignment pattern embedded in them" |
| p045–p052 | 四周須留四格寬乾淨空白「留白區／靜區」；第二張花邊吃掉四格白邊導致卡在找邊界；小問追問被蓋住的黑格怎麼救 | OK | DENSO WAVE [5] | [5]："requires a margin or 'quiet zone' around it … a clear area around a symbol where nothing is printed. QR Code requires a four-module wide margin at all sides of a symbol" |
| p053–p054、p056–p058 | 黑白小方點稱「模組」；每升一版每邊 +4 顆，最大版本四十每邊 177 顆，最多裝 7,089 個純數字或 4,296 個英數字（p055 見 F04） | OK | DENSO WAVE [6]、[8] | [6]："The module refers to the black and white dots"、"Each higher version number comprises 4 additional modules per side"；`versionPage31_40` 與 [8] Outline 表：Version 40（177×177）上限 Numeric `7,089`、Alphanumeric `4,296`。未跨界講時序圖形、格式資訊或遮罩 |
| p059–p067 | 推翻「同網址抄三遍」；以 8 個位元打包成一個「碼字」，不是單獨一小格（p068 見 F05） | OK | DENSO WAVE [1]、[7]；CMU [9] | [7]："One codeword of QR Code is equal to 8 bits"；[9] 說明 Reed-Solomon 為附加 parity symbols 的系統碼，並非把原資料重複抄三份 |
| p069、p071–p074 | Reed-Solomon 碼名稱；人造衛星與行星探測器傳資料抗雜訊、音樂 CD 輕微刮傷照常播放皆用同一套數學（p070 見 F06） | OK | DENSO WAVE [7]；CMU [9] | [7]："used for music CDs etc. … artificial satellites and planetary probes"；[9]："Compact Disk, DVD, barcodes … Satellite communications"。「後來」亦符合時間序（1977 航海家號 → 1982 音樂 CD） |
| p075–p078 | 小問問不抄備份怎麼算；「打個最簡單的比方」三個數字 3、5、2 加總等於 10 線索（p079–p080 見 F05） | OK | `claims.md` C08 | `p077` 明確說出「打個最簡單的比方」，沒有把總和校驗冒充真實有限體多項式演算法，亦遵守禁區不談伽羅瓦體 |
| p081–p084、p086、p089–p090 | 真正演算法比加法厲害；未知哪盒髒掉時須同時找位置與數值，每救 1 個壞碼字需準備 2 個修正碼字；100 盒原資料救 50 盒與小問質疑為何只算 25%（p085 見 F01、p087–p088 見 F07） | OK | DENSO WAVE [7]；CMU [9] | [9]："correct up to t symbols that contain errors in a codeword, where 2t = n-k"、"identify the position and magnitude of up to t errors"；[7]："100 codewords of QR Code to be encoded, 50 of which need to be corrected, 100 codewords of Reed-Solomon Code are required … total codewords are 200" |
| p091–p098 | 污漬也會弄髒修正碼字，故以「總碼字」為分母（50÷200＝25% 對應 Q 級）；L／M／Q／H 四級分別約救總碼字的 7%／15%／25%／30% | OK | DENSO WAVE [7]、[8] | [7]："represents its error correction rate as a ratio of the total codewords"；[8] Outline 表：L Approx. 7%、M Approx. 15%、Q Approx. 25%、H Approx. 30% of codewords。四個數字皆帶「大約／約」並明講分母為「總碼字」 |
| p099–p106 | 不能拿剪刀隨便剪三成：官方明寫依污損情況不保證一定救回；百分比算總碼字盒數而非面積；墨水蓋爛角落定位框使手機認不出碼時，修正盒輪不到上場 | OK | DENSO WAVE [1]、[2]、[7] | [1] `featurePage4` 註 2："Data restoration may not be fully performed depending on the amount of dirt or damage"。清楚區分定位與碼字修正兩階段分工 |
| p107–p115 | 一般方形碼正中央貼小圖案仍能掃，是因避開三角與四周白邊並調高容錯，把遮住的幾盒當壞碼字算回，但會先花掉一部分救命額度 | OK | DENSO WAVE [2]、[5]、[7]；Wikipedia QR code | Wikipedia「QR code」§Artistic embellishment 亦印證：中央貼圖利用高容錯把遮蔽區當受損碼字重建，並預先消耗容錯額度、降低後續抗污餘裕；台詞未給出保證百分比 |
| p116–p126、p128–p129 | 以 8 位元整盒碼字為最小修正單位，同盒髒 1 個位元與 8 個位元全毀都算壞 1 盒；擅長對付集中的突發損傷，八滴聚成一坨蓋兩盒只壞兩盒，散進八盒則壞八盒（p127 見 F08） | OK | DENSO WAVE [7]；CMU [9] | [7]："correction at the byte level, and is suitable for concentrated burst errors"；[9]："One symbol error occurs when 1 bit in a symbol is wrong or when all the bits in a symbol are wrong"。遵守禁區未談交錯區塊表或折線排列 |
| p130–p135 | 為什麼不全開 H 級：同一版格子總數固定，修正盒佔空間；版本一開 L 級最多裝 41 個純數字，開 H 級只剩 17 個數字（p136–p139 見 F09） | OK | DENSO WAVE [6]、[7] | `versionPage1_10` 核對：Version 1（21×21）Numeric 欄 L＝`41`、M＝`34`、Q＝`27`、H＝`17`，數字完全一致 |
| p140–p147 | 若杯套或發票貼紙面積一樣小，升版使格子變密、黑點縮太細，暈開或手抖反而更難掃；髒污工廠常選 Q／H、乾淨大量資料選 L、日常最常選折衷的 M 級（約 15%） | OK | DENSO WAVE [5]、[7] | 明確加上前提「如果杯套或發票留給你的貼紙一樣小」，遵守禁區未宣稱調高容錯必定放大外框公分尺寸；[7]："Level Q or H may be selected for factory environment … Level L may be selected for clean environment with the large amount of data. Typically, Level M (15%) is most frequently selected." |
| p148–p154、p156–p159 | 小問自己回收片頭兩張碼的成敗原因；所長總結兩步分工；日常觀察邀請前句；「原來如此！」、留言題與訂閱呼籲（p155 見 F10） | OK | 同上各段 | 完整回收全部伏筆，無新增未查核主張 |
| `youtube.title` | QR Code 沾到咖啡還能嗶，換個地方卻失靈？｜原來如此事務所 | OK | 同上 | 前 7 字即主體，問句呈現真實反差、不破梗，亦未保證缺角必過 |
| `thumbnail.data` | 缺一塊 **還能嗶？**／換個地方乾乾淨淨卻失靈（右圖 `kid-coffee-tile`） | OK | 同上 | 大字 7 字＋問號，只拋反常識衝突、不洩漏因果答案，主體在右側避開文字欄 |

## 三、畫面提示詞

全部 80 個場景的 `data.prompt` 逐一核對過，沒有畫出錯誤事實、沒有違反雙角色不同框規則，也沒有觸犯 `BANNED` 禁字表。重點核對紀錄與兩則生圖防呆調整如下：

- **幾何與數量概念正確的關鍵鏡頭**：
  - `two-stands-open`、`quiet-zone-compare`：左為中間沾冰咖啡但保留三角與四格寬留白邊、右為花邊緊貼外圍黑格吃掉留白邊，與 C01、C05 完全一致。
  - `ratio-blocks`：過回字框中心的發光切線配五塊積木（`thin dark, thin pale, triple-wide dark, thin pale, thin dark`），精準對應黑：白：黑：白：黑 ＝ `1:1:3:1:1`。
  - `alignment-can`：彎曲鋁罐上的方格右下附近有一顆珊瑚色發光小嵌套方框，符合 Model 2（版本二至六）單顆校正圖形位置。
  - `peg-boxes-row`、`one-peg-vs-eight-pegs`、`burst-puddle-two-boxes`、`scatter-drops-eight-boxes`：以「每盒八顆圓木栓」具象化 8-bit 碼字，左盒髒 1 栓與右盒髒 8 栓同掛一枚叉號、濃咖啡蓋兩盒 vs 八滴散落八盒，與 CMU [9] 的 symbol error 定義完全吻合。
  - `v1-capacity-compare`、`version-upgrade-grid`、`dense-sticker-blur`：`21×21` 盤裝彈珠對照、`25×25` 滿出來對照 `29×29` 全裝下（與 F09 修正後的 50 個純數字升 H 級完全對齊）、同寬度小貼紙粗格清晰 vs 細密微糊，因果清楚。
- **生圖防呆調整（已直接修入 `build_scenes.py`）**：
  - `open-teasers`、`survey-brochures` 的傳單／雜誌改為幾何色塊樣張與條紋紙盒，`kid-clutter-q` 的 `menu stands` 改為格紋杯墊，從源頭避免生圖在紙頁上畫出假字。

## 建議修改（已全數套入 `build_scenes.py` 與 `claims.md`）

- `p005`：`一九九四年兩位工程師天天量傳單線條在找什麼？` → `當年兩位日本工程師天天量傳單線條在找什麼？`
- `p014`：`你在超商結帳應該看過，沒對準紅光方向就刷不過。` → `以前單線紅光刷條碼，你沒橫切過線條就讀不到。`
- `p027`：`還記得開頭提到的一九九四年嗎？` → `還記得開頭那兩位日本工程師嗎？`
- `p028`：`日本 DENSO WAVE 的工程師原昌宏，當時團隊只有兩個人！` → `一九九四年發表時，DENSO 的原昌宏團隊只有兩個人！`
- `p034`：`猜猜看，所有印刷品裡最罕見的比例是幾比幾？` → `猜猜看，這些印刷品裡最罕見的比例是幾比幾？`
- `p055`：`最小的版本一，每邊是二十一乘二十一顆模組；` → `最小的版本一，整張是二十一乘二十一顆模組；`
- `p068`：`原資料裝成一排木盒後，後面會再加上一排數學算出來的修正碼字。` → `原資料裝成一排小盒，後面再加上數學算出來的修正碼字。`
- `p070`：`就是開頭提到，為了保護遙遠太空通訊而開發的！` → `就是開頭提到，連遙遠太空通訊都靠它保護訊號！`
- `p079`：`就算中間那碗被蓋住了，你拿十減掉三和二，` → `就算中間那個數被蓋住，你拿十減掉三和二，`
- `p080`：`馬上就算出裡面一定是五！` → `馬上就算出中間一定是五！`
- `p085`：`DENSO WAVE 官方舉了一個很清楚的算例：` → `開發方 DENSO WAVE 舉過一個清楚算例：`
- `p087`：`那就必須加上兩倍、也就是一百盒修正碼字，` → `就得加上兩倍的一百盒修正盒，總共兩百盒，`
- `p088`：`兩邊合起來，總共變成兩百盒碼字！` → `官方把修正率算成百分之二十五！`
- `p127`：`帳本卻一口氣壞了八盒，額度瞬間爆表！` → `帳本一口氣壞八盒，額度就很容易爆表！`
- `p136`：`反過來，要是網址長達五十個英數字元，` → `反過來，要是有五十個純數字想印成碼，`
- `p137`：`M 級的版本二最多只裝三十八個，那怎麼辦？` → `版本二 M 級夠裝，改開 H 級只裝三十四個怎麼辦？`
- `p138`：`想把剛剛那五十個字元全塞進去，整張碼就得升級到版本三，` → `想維持 H 級塞進剛剛那五十個數，就得升級版本三，`
- `p139`：`每邊長大成二十九乘二十九顆模組才裝得下！` → `長大成二十九乘二十九顆模組才裝得下！`
- `p155`：`不妨看看它的乾淨白邊，還有右下附近那顆小對齊框！` → `不妨看看它的白邊，找找右下附近有沒有小校正框！`
- `youtube.description` 第二段同步更新為「一九九四年問世前，兩人團隊」與「結果可能完全相反」；第 2 章標題同步改為「八位元裝成一盒，太空數學補缺口」。

## 來源

```json
[
  {"title": "DENSO WAVE: What is a QR Code?", "url": "https://www.qrcode.com/en/about/", "checked_on": "2026-11-14"},
  {"title": "DENSO WAVE: Readable from any direction in 360°", "url": "https://www.qrcode.com/en/about/featurePage/featurePage5.html", "checked_on": "2026-11-14"},
  {"title": "DENSO WAVE: History of QR Code", "url": "https://www.qrcode.com/en/history/", "checked_on": "2026-11-14"},
  {"title": "DENSO WAVE: QR Code Model 1 and Model 2", "url": "https://www.qrcode.com/en/codes/model12.html", "checked_on": "2026-11-14"},
  {"title": "DENSO WAVE: Point for determining the code area", "url": "https://www.qrcode.com/en/howto/code.html", "checked_on": "2026-11-14"},
  {"title": "DENSO WAVE: Information capacity and versions of QR Code", "url": "https://www.qrcode.com/en/about/version.html", "checked_on": "2026-11-14"},
  {"title": "DENSO WAVE: Error correction feature", "url": "https://www.qrcode.com/en/about/error_correction.html", "checked_on": "2026-11-14"},
  {"title": "DENSO WAVE: QR Code Standardization", "url": "https://www.qrcode.com/en/about/standards.html", "checked_on": "2026-11-14"},
  {"title": "Riley & Richardson: An introduction to Reed-Solomon codes (CMU CS)", "url": "https://www.cs.cmu.edu/~guyb/realworld/reedsolomon/reed_solomon_codes.html", "checked_on": "2026-11-14"},
  {"title": "Wikipedia: QR code", "url": "https://en.wikipedia.org/wiki/QR_code", "checked_on": "2026-11-14"},
  {"title": "Wikipedia: Reed–Solomon error correction", "url": "https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction", "checked_on": "2026-11-14"}
]
```
