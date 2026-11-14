# 主張與來源（sothatswhy-p12-qr-code）

對應 [`brief.md`](brief.md) 的「查核清單與邊界」。每一條列出片中可以怎麼說、可用的數字、來源與注意事項。
撰稿只能使用「可用說法」裡的數字與範圍；寫進 `build_scenes.py`／`video.json` 後，再交由獨立代理逐句對照查核（`verify-1.md`）。
以下來源均於 **2026-11-14** 直接讀取英文原文核對。

## 來源清單（對應 `video.json` 的 `sources`）

1. **[1] DENSO WAVE, "What is a QR Code?" (`qrcode.com`)** — `https://www.qrcode.com/en/about/`（2026-11-14 讀取全文）
2. **[2] DENSO WAVE, "Readable from any direction in 360°" (`qrcode.com`)** — `https://www.qrcode.com/en/about/featurePage/featurePage5.html`（2026-11-14 讀取全文）
3. **[3] DENSO WAVE, "History of QR Code" (`qrcode.com`)** — `https://www.qrcode.com/en/history/`（2026-11-14 讀取 Section 1–4 全文）
4. **[4] DENSO WAVE, "QR Code Model 1 and Model 2" (`qrcode.com`)** — `https://www.qrcode.com/en/codes/model12.html`（2026-11-14 讀取全文）
5. **[5] DENSO WAVE, "Point for determining the code area" (`qrcode.com`)** — `https://www.qrcode.com/en/howto/code.html`（2026-11-14 讀取全文）
6. **[6] DENSO WAVE, "Information capacity and versions of QR Code" (`qrcode.com`)** — `https://www.qrcode.com/en/about/version.html`（2026-11-14 讀取全文與版本 1–40 容量表）
7. **[7] DENSO WAVE, "Error correction feature" (`qrcode.com`)** — `https://www.qrcode.com/en/about/error_correction.html`（2026-11-14 讀取全文）
8. **[8] DENSO WAVE, "QR Code Standardization" (`qrcode.com`)** — `https://www.qrcode.com/en/about/standards.html`（2026-11-14 讀取全文與 Outline Specification 表）
9. **[9] Martyn Riley & Iain Richardson, "An introduction to Reed-Solomon codes: principles, architecture and implementation" (hosted on Carnegie Mellon University CS)** — `https://www.cs.cmu.edu/~guyb/realworld/reedsolomon/reed_solomon_codes.html`（2026-11-14 讀取全文）

---

## C01 一般方形 QR Code 部分污損時有機會恢復資料，但不保證每次都能完全恢復

- **主張**：QR Code 具備錯誤修正能力，即使圖案部分弄髒或破損，仍有機會還原資料；但視污損程度與情況，資料不一定能完全恢復。
- **可用說法**：「QR Code 有錯誤修正的能力，就算弄髒一小塊或破了一點，有時候還是能把資料救回來。」「不過開發它的官方也寫得很明白：要看弄髒或破損的情況，不代表怎麼傷都一定救得回來。」
- **數字**：最高約可還原 30% 的碼字（詳見 C09）。
- **來源**：[1]、[7]
- **可信度／注意**：高。[1] 原文：「QR Code has error correction capability. Data can be restored even if the symbol is partially dirty or damaged. A maximum 30% of codewords*1 can be restored*2. … *2: Data restoration may not be fully performed depending on the amount of dirt or damage.」片中務必保留「有時候／看情況」，絕不保證任意破損必能掃描成功。

## C02 一般方形 QR Code 靠三個角落的位置偵測圖形，從 360 度任何角度辨認方向

- **主張**：傳統一維條碼只在單一方向編碼，容量約 20 個英數字元；一般方形 QR Code 在縱橫兩個方向編碼，並在三個角落配置方形的位置偵測圖形（position detection patterns），讓讀取器不論從 360 度哪個方向掃描，都能避開背景干擾、穩定辨認出碼的位置與方向。第四個角沒有同樣的大方框，旋轉時才分得出哪一邊朝哪裡。
- **可用說法**：「以前的傳統條碼，只在橫的這一個方向排線條，大約只能裝二十個字元。」「一般方形的 QR Code 改成橫的、直的兩個方向都裝資訊，還在三個角落放了大大的方形定位圖案。」「不管你把手機正著拿、歪著拿、甚至倒過來，三百六十度任何角度，讀取器一抓到這三個角，馬上就知道碼在哪裡、轉了幾度。」「正因為第四個角長得不一樣，轉過頭才不會分不清上下左右。」
- **數字**：傳統條碼約 20 個字元；360 度全方向讀取；3 個角落。
- **來源**：[1]、[2]、[3]
- **可信度／注意**：高。[1]：「While conventional bar codes are capable of storing a maximum of approximately 20 digits… Since QR Code carries information both horizontally and vertically…」[2]：「QR Code is capable of 360 degree (omni-directional), high speed reading. QR Code accomplishes this task through position detection patterns located at the three corners of the symbol. These position detection patterns guarantee stable high-speed reading, circumventing the negative effects of background interference.」限定為「一般方形 QR Code」（不推到只有一個角的 Micro QR 或長方形 rMQR）。「第四個角長得不一樣才分得出轉向」是由「三個角落辨認 360° 方向」直接推得的幾何事實，不額外宣稱讀過 ISO 座標公式。

## C03 定位圖形的方形與 1:1:3:1:1 黑白比例，是開發團隊統計大量印刷品挑出最少見的比例

- **主張**：1994 年發表 QR Code 的日本公司 DENSO WAVE（當時為 DENSO 旗下部門），由原昌宏（Masahiro Hara）帶領兩人開發團隊研發；「QR」代表 Quick Response（快速反應）。為了不讓讀取器把旁邊的文字或圖案誤認成定位圖形，他們先選了商務表單上最不常出現的「方形」，接著把傳單、雜誌、紙箱上的圖畫與符號轉成黑白圖樣，日復一日統計黑白寬度比例，找出印刷品上最少出現的比例 `1:1:3:1:1`，作為定位圖形的黑白寬度比。
- **可用說法**：「QR 是英文 Quick Response 的縮寫，意思就是快速反應，是一九九四年日本的 DENSO WAVE 團隊發表的。」「當年帶頭開發的工程師原昌宏，團隊只有兩個人。為了不讓機器把海報或紙箱上的字看錯成定位框，他們先挑了表單上最少見的正方形。」「接著他們抱來一大堆傳單、雜誌和紙箱，全部轉成黑白，連續好幾天統計黑白寬度的比例，最後找出印刷品上最罕見的一組節奏：一比一比三比一比一。」「切過角落這個回字框的中心，黑、白、黑、白、黑的寬度剛好就是一、一、三、一、一。讀取器只要一抓到這個罕見比例，就知道『找到碼了』！」
- **數字**：1994 年發表；2 人開發團隊；黑白寬度比 `1:1:3:1:1`。
- **來源**：[3]
- **可信度／注意**：高（屬開發公司官方自述史）。[3] Section 1 & 2 原文：「He dared to try this with only one other person as his team member. … According to Hara this was because “it was the pattern least likely to appear on various business forms and the like.” … they decided to do an exhaustive survey of the ratio of white to black areas in pictures and symbols printed on fliers, magazines, cardboard boxes and so on after reducing them to patterns with black and white areas. They continued the task of surveying innumerable examples of printed matter all day long for days on end. Eventually, they came up with the least used ratio of black and white areas on printed matter. This ratio was 1:1:3:1:1. … In 1994, DENSO WAVE (then a division of DENSO CORPORATION) announced the release of its QR Code. The QR in the name stands for quick response…」注意：[3] 提到的「比其他碼快 10 倍以上」沒有測試條件，依素材池覆核規則**不引用**；也不談圍棋故事（官方歷史頁未寫）。

## C04 Model 2 嵌入校正圖形（alignment pattern），幫助曲面印刷或斜拍變形時順利讀取

- **主張**：日常廣泛使用的改良版 QR Code Model 2 在碼內嵌入校正圖形（alignment pattern），即使印在彎曲表面上，或因為拍攝角度傾斜導致畫面變形，讀取器也能參照校正圖形有效對齊讀取。
- **可用說法**：「現在大家日常掃的改良版（Model 2），裡面還藏了小小的『校正圖形』。就算印在彎彎的飲料罐上，或者你拿手機斜斜地拍、畫面有點變形，讀取器也能靠它把格子對齊。」
- **數字**：Model 1 最大版本 14（73×73）；Model 2 最大版本 40（177×177，最多 7,089 個數字）。片中不必背 Model 1 數字，只需交代改良版加了校正圖形抗曲面與斜拍變形。
- **來源**：[4]
- **可信度／注意**：高。[4] 原文：「QR Code created by improving Model 1 so that this code can be read smoothly even if it is distorted in some way. QR Codes that are printed on a curved surface or whose reading images are distorted due to the reading angle can be read efficiently by referring to an alignment pattern embedded in them.」注意：官方頁未寫校正圖形的精確座標與隨版本增加的數量表，片中只說「藏在裡面的小校正框」（常見在右下角附近，不背座標公式）。

## C05 四周必須留出 4 個模組寬的空白「靜區」（quiet zone）

- **主張**：QR Code 圖案四周都必須保留一圈完全不印任何東西的空白邊界，稱為 margin 或 quiet zone（留白／靜區），寬度需要至少 4 個模組（4 個小方格寬）。
- **可用說法**：「QR Code 四周那一圈白邊可不是多餘的裝飾，它叫做留白區，也叫靜區。官方規定四個邊都要留出四個小方格寬、什麼都不能印的乾淨空白，機器才分得出哪裡是碼的邊界、哪裡是外面的花紋。」
- **數字**：四周各 4 個模組寬（four-module wide margin at all sides）。
- **來源**：[5]
- **可信度／注意**：高。[5] 原文：「The QR Code symbol area requires a margin or "quiet zone" around it to be used. The margin is a clear area around a symbol where nothing is printed. QR Code requires a four-module wide margin at all sides of a symbol.」注意：官方頁只規定需要 4 格留白，未給出留白剩幾格會失敗的百分比，片中只說「如果花邊貼太近、吃掉這圈留白，就算裡面的黑格一塵不染，機器也可能認不出邊界」。

## C06 黑白小格稱為「模組」（module），版本 1 到 40 從 21×21 長大到 177×177

- **主張**：組成 QR Code 的黑白小方點稱為模組（module）。規格從版本 1（21×21 個模組）到版本 40（177×177 個模組），每升一版，每邊增加 4 個模組。最多可容納 7,089 個純數字，或 4,296 個英數字元，或 2,953 個位元組。
- **可用說法**：「QR Code 裡面這一顆一顆黑白小方格，正式名字叫『模組』。最小的版本一，每邊是二十一格乘二十一格；每升一版，每邊就多長出四格，一路到最大的版本四十，每邊有一百七十七格，最多可以塞進七千零八十九個數字！」
- **數字**：Version 1 = `21×21` modules；每版每邊 `+4` modules（例如 Version 2 = `25×25`、Version 3 = `29×29`）；Version 40 = `177×177` modules；最大容量純數字 `7,089`、英數 `4,296`、8 位元位元組 `2,953`。
- **來源**：[6]、[8]
- **可信度／注意**：高。[6] 原文：「The symbol versions of QR Code range from Version 1 to Version 40. … (The module refers to the black and white dots that make up QR Code.) … commencing with Version 1 (21 × 21 modules) up to Version 40 (177 × 177 modules). Each higher version number comprises 4 additional modules per side.」[8] Outline Specification 表同列相同數字。注意：**不講**時序圖形（timing pattern）、格式資訊（format info）與遮罩（masking），因公開頁無細節。

## C07 資料區以 8 位元組成一個「碼字」（codeword），並加上 Reed-Solomon 錯誤修正碼

- **主張**：構成資料區的單位稱為「碼字」（codeword），在 QR Code 裡 1 個碼字等於 8 個位元（1 byte），不等於畫面上單獨 1 格模組。QR Code 的錯誤修正並不是把同一份原資料原封不動抄好幾遍，而是在原資料後面加上數學計算出來的「Reed-Solomon 碼」；這套數學方法最初是為了對抗人造衛星與行星探測器的通訊雜訊而開發，也用在音樂 CD 等儲存媒體上。
- **可用說法**：「讀取器不是一格一格分開救，而是把八個位元打包成一小盒，叫做一個『碼字』——所以一個碼字不是你眼睛看到的單獨一小格喔！」「那缺了一盒怎麼救？它不是把網址傻傻抄三遍，而是在原本的資料後面，加上一組用數學算出來的『修正碼字』，叫做 Reed-Solomon 碼。」「這套數學原本是為了讓人造衛星和行星探測器從遙遠太空傳訊號回地球時，就算遇到雜訊也不怕漏字而發展出來的；連家裡的音樂 CD 刮到一點點還能播，靠的也是它！」
- **數字**：`1 codeword = 8 bits`（1 byte）。
- **來源**：[1]、[7]、[9]
- **可信度／注意**：高。[7] 原文：「codeword is a unit that constructs the data area. One codeword of QR Code is equal to 8 bits. … The QR Code error correction feature is implemented by adding a Reed-Solomon Code* to the original data. … *Reed-Solomon Code is a mathematical error correction method used for music CDs etc. The technology was originally developed as a measure against communication noise for artificial satellites and planetary probes. It is capable of making a correction at the byte level, and is suitable for concentrated burst errors.」[9] 亦載明 Reed-Solomon 用於 Compact Disk、barcodes、satellite communications 等，且為附加 parity symbols 的系統碼（systematic code），不是把原資料複製多份。

## C08 未知錯誤位置時，修 1 個受損碼字需要 2 個 Reed-Solomon 修正碼字（官方 100＋100＝200 算例）

- **主張**：在不知道哪個碼字出錯的情況下，Reed-Solomon 碼要修正 `t` 個碼字的錯誤，需要準備兩倍數量（`2t` 個）的 Reed-Solomon 修正碼字。DENSO WAVE 官方舉例：如果有 100 個原本的資料碼字，希望其中壞掉 50 個時還能救回來，就必須加上兩倍、也就是 100 個 Reed-Solomon 碼字，總共變成 200 個碼字。片中可用「三個數字加總和線索」做白話入門比喻（明說「打個比方」），幫觀眾直覺理解「靠數學關係反推缺漏，而不是抄備份」，再接回官方「修 1 個未知位置的壞碼字要花 2 個修正碼字」的真實規則。
- **可用說法**：「打個最簡單的比方：假設你有三個數字三、五、二，你不抄備份，而是在旁邊多記一條線索『三個加起來等於十』。就算中間那個五被咖啡蓋住了，看前後的三和二，再看總和十，馬上就算得出中間一定是五！」「當然真正的 Reed-Solomon 數學比加法厲害得多，因為手機事先根本不知道『哪一盒』被弄髒了，它得同時找出『哪一盒壞掉』跟『原本裝什麼』。所以每想救回一個壞掉的碼字，就得先準備兩個修正碼字！」「官方舉過一個很清楚的例子：假設原本有一百個資料碼字，你想讓它就算壞掉五十個也能救回來，那就得加上兩倍——也就是一百個修正碼字，合起來總共兩百個碼字。」
- **數字**：修 1 個未知位置碼字需 2 個修正碼字（`2t = n - k`）；官方算例：100 個原資料碼字 + 100 個 Reed-Solomon 碼字 = 總共 200 個碼字，可修正其中 50 個碼字。
- **來源**：[7]、[9]
- **可信度／注意**：高。[7] 原文：「For example, if there are 100 codewords of QR Code to be encoded, 50 of which need to be corrected, 100 codewords of Reed-Solomon Code are required, as Reed-Solomon Code requires twice the amount of codewords to be corrected. In this case, the total codewords are 200, 50 of which can be corrected.」[9] Section 2：「A Reed-Solomon decoder can correct up to t symbols that contain errors in a codeword, where 2t = n-k.」「三個數字加總等於十」必須在台詞裡明確說「打個最簡單的比方」，不冒充實際的多項式／有限體演算法，也不講伽羅瓦體（Galois field）等艱深名詞。

## C09 L／M／Q／H 四級約 7%／15%／25%／30% 的分母是「總碼字」，不是原資料、更不是畫面面積

- **主張**：為什麼官方算例裡「100 個原資料碼字、可修 50 個」不叫 50%，而叫 25%（對應 Q 級）？因為污漬與破損不會只挑原本的資料碼字下手，Reed-Solomon 修正碼字自己也會被弄髒！所以官方一律用「總碼字」（原資料＋修正碼字，例中為 200）當分母：50 ÷ 200 ＝ 25%。官方四個錯誤修正等級分別為 L（約 7%）、M（約 15%）、Q（約 25%）、H（約 30%）的總碼字恢復率。這既不是原資料比例，更不是整張圖隨便剪掉 30% 面積都能讀的保證；若傷到定位圖形或留白導致找不到碼，修正碼字再多也派不上用場。
- **可用說法**：「為什麼一百個資料能救五十個，官方卻只寫百分之二十五？因為咖啡滴下來的時候，才不會乖乖閃開修正碼字！」「不管是原本的資料盒，還是後來加進去的修正盒，統統都可能被弄髒。兩百個總碼字裡面，不管是哪五十個壞掉都能修好，五十除以兩百，就是百分之二十五，對應官方的 Q 級！」「QR Code 一共分成 L、M、Q、H 四個等級，大約能救回總碼字的百分之七、百分之十五、百分之二十五，到最高的百分之三十。」「注意喔，這裡算的是『總碼字』，不是整張圖的面積！要是那一滴墨水剛好毀掉角落的定位框，手機連這裡有個碼都認不出來，後面再強的數學修正也根本輪不到上場。」
- **數字**：L 約 `7%`、M 約 `15%`、Q 約 `25%`、H 約 `30%`（皆保留「約／大約」，分母皆為 total codewords）。
- **來源**：[1]、[2]、[7]、[8]
- **可信度／注意**：高。[7] 原文：「Thus, the error correction rate for the total codewords is 25%. This corresponds to QR Code error correction Level Q. In the example above, the error correction rate for QR Code codewords can be considered as 50%. However, it is not always the case that codewords of not Reed-Solomon Code but only QR Code are susceptible to dirt and damage. QR Code therefore represents its error correction rate as a ratio of the total codewords.」[8] Outline 表：「Level L: Approx. 7% of codewords can be restored. Level M: Approx. 15%… Level Q: Approx. 25%… Level H: Approx. 30%…」注意：不給出「中間貼商標最多能貼幾 %」的保證數字，只解釋「中間能放小圖，是因為避開了角落定位框，而且把容錯等級調高，把被蓋住的那幾盒當成受損碼字修回來」。

## C10 同樣大小的污損，「集中成一塊」往往比「零散小點」更好修

- **主張**：Reed-Solomon 以整個 8 位元碼字（symbol／byte）為單位修正：同一個碼字裡面，不論只錯 1 個位元還是 8 個位元全錯，對解碼器來說都只算「1 個碼字錯誤」。因此 DENSO WAVE 與通訊教材都指出，Reed-Solomon 特別適合修正「集中的突發錯誤」（concentrated burst errors）：一整塊集中的污漬如果剛好落在少數幾個碼字裡，只消耗少數幾個碼字的修正額度；反過來，同樣面積如果散成許多小污點、分別打中很多不同的碼字，每碰一個碼字就壞一包，修正額度很快就會用光。
- **可用說法**：「因為它是以『八個位元一整盒』為單位在修的！同一盒裡面，不管你只弄髒一格，還是八格全毀，在帳本上都只算『壞掉一盒』。」「所以官方特別點出，這套數學最擅長對付『集中在一起的突發損傷』！想像八滴小墨水集中成一整坨，剛好全蓋在同一盒或兩盒上面，那才壞掉兩盒，輕輕鬆鬆就能修好；」「可是如果這八滴小墨水像撒胡椒一樣散開，剛好分別滴進八個不同的盒子裡，就算每一盒只髒了一小點，帳本上卻一口氣壞了八盒，額度一下就被吃光了！」
- **數字**：1 個碼字 ＝ 8 位元；錯 1 位元與錯 8 位元同計為 1 個碼字錯誤（symbol error）。
- **來源**：[7]、[9]
- **可信度／注意**：高。[7] 原文：「It is capable of making a correction at the byte level, and is suitable for concentrated burst errors.」[9] Section 2〈Symbol Errors〉原文：「One symbol error occurs when 1 bit in a symbol is wrong or when all the bits in a symbol are wrong. … Reed-Solomon codes are particularly well suited to correcting burst errors (where a series of bits in the codeword are received in error).」注意：片中的「八滴墨水蓋兩盒 vs 分散滴八盒」是直接根據此位元組錯誤規則設計的概念圖解說（不宣稱某支手機掃描實驗數據，也不講未讀 ISO 的碼字在矩陣裡實際怎麼折線排列）。

## C11 提高容錯等級會減少同版本容量或讓格子變多變密，日常最常選 M 級（約 15%）

- **主張**：每個版本的模組總數固定，提高錯誤修正等級就必須塞入更多修正碼字，能裝原資料的空間就會變少；例如最小的版本 1（21×21），L 級最多裝 41 個數字（或 25 個英數字），開到 H 級只剩 17 個數字（或 10 個英數字）。反過來，如果要裝同樣多的資料又調高容錯等級，就得升到更高版本、長出更多模組（例如 50 個純數字在版本 2 的 25×25 開 M 級最多可裝 63 個，但改開 H 級上限掉到 34 個，就必須升到版本 3 的 29×29、H 級上限 58 個才裝得下）。若印刷面積固定，格子變多就會讓每一格變小，反而更容易受印刷模糊或手震影響。因此需依環境取捨：容易弄髒的工廠環境常選 Q 或 H 級，乾淨且資料量大的環境可選 L 級，而一般日常最常選的是折衷的 M 級（約 15%）。
- **可用說法**：「既然 H 級這麼能救，為什麼不把世界上所有 QR Code 都開到 H 級？因為修正碼字也要佔位子啊！」「拿最小的版本一、整張二十一乘二十一格來說，開 L 級可以裝四十一個數字；一旦開到最高的 H 級，能裝的數字直接掉到只剩十七個！」「反過來，要是有五十個純數字，版本二開 M 級夠裝，改開 H 級卻只裝三十四個，就得升級到二十九乘二十九格的版本三才塞得下。要是印在杯套或小貼紙上的面積一樣小，格子越多，每一顆黑點就縮得越細，稍微印糊一點或手抖一下反而更難認！」「所以工程師會看場合挑：容易沾油污的工廠選 Q 或 H，乾淨但資料超多的地方選 L，而我們日常最常看到的，其實是剛剛好的 M 級，大約百分之十五。」
- **數字**：
  - 版本 1（`21×21`）：L 級純數字 `41`（英數 `25`），H 級純數字 `17`（英數 `10`）（[6] 版本表）。
  - 50 個純數字由 M 級調高到 H 級：版本 2（`25×25`）M 級純數字上限 `63`、H 級上限 `34`，因此開 H 級需升至版本 3（`29×29` 模組，H 級純數字上限 `58`）（[6] `versionPage1_10.html`）。
  - 日常最常用等級：Level M（`15%`）（[7]）。
- **來源**：[5]、[6]、[7]
- **可信度／注意**：高。[7] 原文：「Raising this level improves error correction capability but also increases the amount of data QR Code size. To select error correction level, various factors such as the operating environment and QR Code size need to be considered. Level Q or H may be selected for factory environment where QR Code get dirty, whereas Level L may be selected for clean environment with the large amount of data. Typically, Level M (15%) is most frequently selected.」[6] `versionPage1_10.html` 表列：Version 1 L = 41 numeric / 25 alphanumeric，H = 17 numeric / 10 alphanumeric；Version 2 Numeric M = 63、H = 34；Version 3 Numeric H = 58。注意：不宣稱「調高等級一定讓印刷出來的公分尺寸變大」（因為若把每格印得更細，外框公分數可以不變，只是每格變小）。
