# A21 品客洋芋片｜完整分鏡準備

狀態：ADAPTED_CANDIDATE_AWAITING_INDEPENDENT_TEXT_AND_STORYBOARD_REVIEW。原全文 SHA：`c250fb1f03f1b4868519a7d902af08247a214b2a228dc372efde8474b94cdc82`；active 旁白 SHA：`80ace226e644630b604c40902f648ff32153fb24fe80e2dbe86e160fafc48193`（段與段以 LF 串接）。這兩者不是同一資料物件，不互相冒用審核。

47 段、2283 字；89 鏡＝78 插畫＋11 數字／來源卡，插畫 87.64%，最多 2 連卡。六章旁白正文 body 估 547.92–595.57 秒；開場後五章另估 508.56–552.78 秒（僅分析分段，不是正式 body 門檻）。片頭 5 秒＋片尾 21 秒另計，總估 573.92–621.57 秒。尚未實錄，不補停頓充長。

六章完整旁白正文 body 字數估算在八分鐘以上，但仍未有配音實測，不能視為長度關卡通過。

## 固定規格與來源範圍

- MiniMax image-01；`look: {"preset":"cute-mystery"}`，不覆寫 style／negative／motion。
- 插畫每張一位一般化人物、一個主要動作、焦點物件、中性光。圖片不生文字、品牌或真人肖像；人物與文件都是相關說明，非史實現場重建。
- 數字卡含必要口徑、名稱及來源。繁中用可關閉 CC；英日韓只在站主選取後製作。
- 切鏡不等於 TTS 句界；跨段鏡保留原段 ID 及字串偏移，不額外添停頓。
- 本集只說 2004 年秋改配方之後、案件內的 Regular Pringles；更早配方、Dippers 與其他系列不在範圍。
- 1966-07-29 為專利申請日，1970-03-03 為核准日；核准文本中的生切片／馬鈴薯麵團是製法選項，不是早期商業配方證據。
- 2007 稅務法庭、2008 高等法院、2009 上訴法院為三個不同裁判層級；示意人物與空白文件不冒充真人或庭審原件。
- 42% 只指案件中的配方近似比例，沒有 50% 的法定門檻；不推廣為當今產品配方或一般稅務建議。
- 2009 過往最多約一億英鎊、其後每年約兩千萬英鎊，均為判決記載的 HMRC 律師估額；沒有欠稅則是美聯社報導中的公司說法。兩者不互代。
- 2025 Sensations Poppadoms 案只是後續引用此案方法，不是品客再審。
- 內部來源取得狀態只留 source-map／審查證據，不能出現在觀眾卡片；旁白原文不因分鏡改寫。

## 原文與 active 稿差異

- **T06**：T05 ends with P&G defending its High Court win; name the tax authority explicitly in T06 so the following appeal argument cannot be misread as P&G seeking to reverse that win. Original v3 fullscript and first storyboard remain preserved.
  - 原文：這回他們要說服上訴法院，高等法院把這句話讀得太窄，而最初稅務法庭的判斷應該恢復。
  - 候選：這回，稅務機關要說服上訴法院，高等法院把這句話讀得太窄，而最初稅務法庭的判斷應該恢復。

## 片頭片尾

- A21-S007 後放既有 **5 秒**片頭。
- A21-S089 後接既有 **21 秒**片尾；最後 **16 秒**保留實際影片／訂閱連結區（片尾第 5–21 秒）。連結目標與資產 hash 留到正式上架包，這裡未設定可點連結。

## 5–8 秒目標以外的估時

22 鏡在估速區間至少一端略短或略長；這是如實估值。短鏡接續說話，長鏡待實錄後調整畫面剪點，不能用假停頓補長。

| 鏡 | 字數 | 秒數 |
|---|---:|---|
| A21-S005 | 10 | 2.40–2.61 秒 |
| A21-S008 | 12 | 2.88–3.13 秒 |
| A21-S010 | 33 | 7.92–8.61 秒 |
| A21-S014 | 20 | 4.80–5.22 秒 |
| A21-S018 | 19 | 4.56–4.96 秒 |
| A21-S020 | 18 | 4.32–4.70 秒 |
| A21-S022 | 15 | 3.60–3.91 秒 |
| A21-S023 | 32 | 7.68–8.35 秒 |
| A21-S025 | 31 | 7.44–8.09 秒 |
| A21-S035 | 19 | 4.56–4.96 秒 |
| A21-S037 | 32 | 7.68–8.35 秒 |
| A21-S041 | 20 | 4.80–5.22 秒 |
| A21-S045 | 19 | 4.56–4.96 秒 |
| A21-S057 | 31 | 7.44–8.09 秒 |
| A21-S058 | 33 | 7.92–8.61 秒 |
| A21-S060 | 19 | 4.56–4.96 秒 |
| A21-S066 | 32 | 7.68–8.35 秒 |
| A21-S067 | 18 | 4.32–4.70 秒 |
| A21-S071 | 20 | 4.80–5.22 秒 |
| A21-S083 | 32 | 7.68–8.35 秒 |
| A21-S087 | 32 | 7.68–8.35 秒 |
| A21-S089 | 31 | 7.44–8.09 秒 |

## hook

原段：H01、H02、H03、H04、H05；164 字。

Active worker 主線：1966年七月寶僑申請包裝專利，讓易碎薄片整齊疊進硬圓筒。罐子處理運送，不能替產品決定稅務分類。預告2007稅務法庭、2008高院換讀法、2009三位上訴法院法官再看前兩回合，三個時刻均不揭勝負。問為什麼爭不是洋芋片、最後誰贏，接五秒片頭。

### A21-S001｜插畫｜估 5.28–5.74 秒

**旁白**：[H01] 一九六六年七月，寶僑在美國申請一項零食包裝專利：

**CID／來源**：C01 → S1

**畫面功能**：包裝專利從辦公桌的送件動作起步，不偽造專利原件

**鏡頭**：Medium shot, push in

**Prompt**：Medium shot in a 1960s packaging office, one generic designer slides a blank application folder into a plain document tray, focused face visible above the tray, soft window light

### A21-S002｜插畫｜估 6.48–7.04 秒

**旁白**：[H01] 讓容易碎的薄片整齊疊起來，裝進硬的圓筒。 [H02] 罐子要解決運送問題。

**CID／來源**：C01 → S1

**畫面功能**：整齊薄片與圓筒先呈現運送解法

**鏡頭**：Close-up, pan right

**Prompt**：Close-up at a packing bench, one generic packer lowers a neat stack of curved snack slices into a plain rigid cylinder, attentive face above the cylinder, mild overhead light

### A21-S003｜插畫｜估 6.00–6.52 秒

**旁白**：[H02] 但罐裡那片零食，幾十年後，會遇上一個包裝解決不了的問題。

**CID／來源**：C01 → S1

**畫面功能**：同一類罐裝零食帶出包裝之外的疑問，不揭勝負

**鏡頭**：Medium close-up, pull out

**Prompt**：Medium close-up at a kitchen table, one generic shopper studies a curved snack slice beside an unmarked cylinder, puzzled expression, overcast window light

### A21-S004｜插畫｜估 6.48–7.04 秒

**旁白**：[H03] 二〇〇七年，英國稅務法庭要判它算不算應課稅的洋芋片類零食。

**CID／來源**：C02 → S2

**畫面功能**：第一回合法庭預告，與 S035 共用同一圖

**鏡頭**：Wide shot, pan left

**Prompt**：Wide shot in a simple British tribunal room, one generic clerk places a closed case folder on a plain hearing table, attentive face, diffuse window light

### A21-S005｜插畫｜估 2.40–2.61 秒

**旁白**：[H04] 隔年，高等法院換了讀法；

**CID／來源**：C03、C04 → S3、S4

**畫面功能**：高等法院讀法預告，與 S055 共用同一圖

**鏡頭**：Medium shot, tilt down

**Prompt**：Medium shot at a high-ceiling legal reading room, one generic legal reader holds an open blank case folder, thoughtful face turned toward the pages, soft side-window light

### A21-S006｜插畫｜估 6.48–7.04 秒

**旁白**：[H04] 到了二〇〇九年，三名上訴法院法官，又得把前兩回合放在一起看。

**CID／來源**：C03、C04 → S3、S4

**畫面功能**：第三回合三份文件預告，與 S067 共用同一圖

**鏡頭**：Close-up, pan right

**Prompt**：Close-up at an appellate court document counter, one generic clerk arranges three closed plain case folders in one row, serious face above the folders, mild ceiling light

### A21-S007｜插畫｜估 6.24–6.78 秒

**旁白**：[H05] 品客為什麼要爭自己不是洋芋片？打完這三回合，最後是誰贏了？

**CID／來源**：敘事／一般解說 → 沒有新增歷史主張

**畫面功能**：圓筒與案卷並排，開場問題停在結果之前

**鏡頭**：Medium close-up, push in

**Prompt**：Medium close-up at a simple study desk, one generic reader holds a plain snack cylinder beside a closed case folder, curious expression, soft table-lamp light

## origin

原段：O01、O02、O03、O04、O05、O06、O07；303 字。

Active worker 主線：1970核准的包裝專利列Fredric Baur與Harold Hawley；從袋裝易碎、空隙及氧氣／水氣問題，走到規則薄片疊列、圓筒支撐和密封。核准文本有生馬鈴薯切片與馬鈴薯基底麵團兩種可用做法，認為可彎麵團片較適合所需形狀；不推定早期上市配方。由麵團中的馬鈴薯設問，接幾十年後法律怎樣讀「用馬鈴薯做的」。

### A21-S008｜數字／來源卡｜估 2.88–3.13 秒

**旁白**：[O01] 這項專利在一九七〇年核准，

**CID／來源**：C05 → S1

**畫面功能**：專利核准日期與申請分清

**卡**：1970 年核准

**口徑**：US3498798A・3 月 3 日

**來源**：美國專利 US3498798A（S1）

### A21-S009｜數字／來源卡｜估 6.72–7.30 秒

**旁白**：[O01] 發明人是Fredric Baur和Harold Hawley。

**CID／來源**：C05 → S1

**畫面功能**：發明人用文字呈現，不生成真人肖像

**卡**：Fredric Baur
Harold Hawley

**口徑**：US3498798A 列名發明人

**來源**：美國專利 US3498798A（S1）

### A21-S010｜插畫｜估 7.92–8.61 秒

**旁白**：[O02] 文件描述的舊問題很具體：薄片隨意裝進袋子，搬運一碰，容易碎；空隙多，也占地方。

**CID／來源**：C06 → S1

**畫面功能**：鬆散包裝的碎片與空間問題，同一人檢視一袋

**鏡頭**：Wide shot, pull out

**Prompt**：Wide shot in a small loading area, one generic warehouse worker opens a plain snack bag above a shallow tray of broken slices, concerned face, grey doorway light

### A21-S011｜插畫｜估 5.76–6.26 秒

**旁白**：[O03] 他們提出的做法，是先讓每片的大小、形狀一致，再疊成一列，

**CID／來源**：C07 → S1

**畫面功能**：規則形狀讓薄片疊合，以一個動作示範

**鏡頭**：Close-up, tilt down

**Prompt**：Close-up at a packaging workbench, one generic designer aligns one curved snack slice with a neat stack of matching slices, concentrated face partly visible, soft overhead light

### A21-S012｜插畫｜估 6.96–7.57 秒

**旁白**：[O03] 放進有支撐力的圓筒。薄片之間互相靠住，運送時就比較不容易亂移動。

**CID／來源**：C07 → S1

**畫面功能**：圓筒提供支撐，畫出堆疊而非真實實驗證明

**鏡頭**：Medium shot, pan left

**Prompt**：Medium shot at a packing station, one generic worker fits a plain rigid cylinder around a snug stack of curved snack slices, attentive face, diffuse window light

### A21-S013｜插畫｜估 6.48–7.04 秒

**旁白**：[O04] 密封也有任務。文件說，氧氣會讓油脂變質，水氣會讓薄片失去酥脆；

**CID／來源**：C08 → S1

**畫面功能**：保存狀態以開口薄片的檢視表達，不畫氧氣微觀假實驗

**鏡頭**：Medium close-up, push in

**Prompt**：Medium close-up at a storage shelf, one generic food technician examines a snack slice from an open plain container, concerned face, mild ceiling light

### A21-S014｜插畫｜估 4.80–5.22 秒

**旁白**：[O04] 縮小空隙、阻擋外面的空氣，能幫忙維持保存狀態。

**CID／來源**：C08 → S1

**畫面功能**：封口動作接空氣與保存的機制

**鏡頭**：Close-up, pan right

**Prompt**：Close-up at a clean packing table, one generic worker presses a plain lid onto a filled cylinder, focused face above the lid, soft window light

### A21-S015｜插畫｜估 6.48–7.04 秒

**旁白**：[O05] 不過，要疊得整齊，薄片得先做得夠一致。這份核准文本列出兩條路：

**CID／來源**：C09 → S1

**畫面功能**：製法選項置於同一工作檯，不當早期量產配方

**鏡頭**：Wide shot, pull out

**Prompt**：Wide shot in a simple preparation room, one generic designer studies two separate trays containing raw potato slices and a flattened potato dough sheet, thoughtful face, overcast window light

### A21-S016｜插畫｜估 6.96–7.57 秒

**旁白**：[O05] 可以用生馬鈴薯切片，也可以把馬鈴薯基底的麵團壓成片，再切形、油炸。

**CID／來源**：C09 → S1

**畫面功能**：以馬鈴薯麵團壓片，生切片作旁置選項，不畫成純麵粉

**鏡頭**：Medium shot, tilt down

**Prompt**：Medium shot at a preparation bench, one generic cook presses a potato-based dough sheet with a plain roller, a separate tray of raw potato slices nearby, focused face, mild overhead light

### A21-S017｜插畫｜估 6.96–7.57 秒

**旁白**：[O06] 文中認為，可以彎折的馬鈴薯麵團片，更適合做出這種包裝需要的形狀。

**CID／來源**：C09 → S1

**畫面功能**：可彎折的麵團片貼合曲面，對應專利偏好

**鏡頭**：Close-up, pan left

**Prompt**：Close-up at a forming bench, one generic cook bends a thin dough piece over a simple curved mould, attentive face above the mould, soft side light

### A21-S018｜插畫｜估 4.56–4.96 秒

**旁白**：[O07] 但當馬鈴薯成了麵團的一部分，做出來的零食，

**CID／來源**：C09 → S1

**畫面功能**：成品與原料的關係形成下一段問題

**鏡頭**：Medium close-up, push in

**Prompt**：Medium close-up at a kitchen worktop, one generic cook holds a formed curved slice above a bowl of potato dough, curious face, grey window light

### A21-S019｜插畫｜估 6.24–6.78 秒

**旁白**：[O07] 還算「用馬鈴薯做的」嗎？幾十年後，英國法庭得為這幾個字作決定。

**CID／來源**：C09 → S1

**畫面功能**：零食物件從廚房接往法律文件，沒有暗示專利引發官司

**鏡頭**：Wide shot, pan right

**Prompt**：Wide shot in a legal consultation room, one generic assistant sets a plain snack cylinder beside a closed law book, questioning expression, soft daylight

## idea

原段：I01、I02、I03、I04、I05、I06、I07、I08；380 字。

Active worker 主線：2006年一月HMRC發函判Regular Pringles用標準稅率，寶僑上訴。先限定只審2004秋改配方後版本，排除早期、Dippers等；只在此介紹各粉類混麵團再切形油炸。當時裁判引用VAT Act1994：一般食品零稅率、即食洋芋片及馬鈴薯材料製成的類似產品是例外。兩條件都要成立，只排除這項例外不等於排除所有稅法。留下稅額及輸了是否補欠稅兩問題。

### A21-S020｜插畫｜估 4.32–4.70 秒

**旁白**：[I01] 二〇〇六年一月，英國稅務機關發函給寶僑，

**CID／來源**：C30 → S2

**畫面功能**：稅務機關發函只用匿名收信動作

**鏡頭**：Medium shot, pull out

**Prompt**：Medium shot at an office mail desk, one generic employee opens a plain envelope beside a closed product file, attentive face, diffuse morning light

### A21-S021｜插畫｜估 5.76–6.26 秒

**旁白**：[I01] 認定Regular Pringles應適用標準稅率。

**CID／來源**：C30 → S2

**畫面功能**：標準稅率認定留在旁白，空白文件不是判決原件

**鏡頭**：Close-up, tilt down

**Prompt**：Close-up at an administrative desk, one generic reader studies a blank letter beside an unmarked snack cylinder, worried expression, mild desk-lamp light

### A21-S022｜插畫｜估 3.60–3.91 秒

**旁白**：[I01] 公司提出上訴，把產品帶進稅務法庭。

**CID／來源**：C30 → S2

**畫面功能**：公司上訴用遞交案卷示意，不模擬真人證詞

**鏡頭**：Wide shot, pan left

**Prompt**：Wide shot at a courthouse filing counter, one generic legal assistant places a thick plain folder in an intake tray, purposeful face, overcast window light

### A21-S023｜數字／來源卡｜估 7.68–8.35 秒

**旁白**：[I02] 受審的是二〇〇四年秋天改配方之後的Regular Pringles。

**CID／來源**：C10 → S2、S3

**畫面功能**：先限清本案產品與配方年代

**卡**：本案 Regular Pringles

**口徑**：2004 年秋改配方之後

**來源**：2007 判決 §2／2008 判決 §1–4（S2、S3）

### A21-S024｜插畫｜估 6.96–7.57 秒

**旁白**：[I02] 更早的版本、沾醬用的Dippers和其他特殊系列，都不包括在內。

**CID／來源**：C10 → S2、S3

**畫面功能**：把受審物件獨立放在托盤，其他款式不冒充本案

**鏡頭**：Medium shot, push in

**Prompt**：Medium shot at a product archive shelf, one generic archivist selects a single plain cylindrical package for a separate tray, other differently shaped unmarked containers remain on the shelf, focused face, soft ceiling light

### A21-S025｜插畫｜估 7.44–8.09 秒

**旁白**：[I03] 這款零食把馬鈴薯粉、玉米粉、小麥澱粉和米粉等材料混成麵團，再切形、油炸。

**CID／來源**：C11 → S2、S4

**畫面功能**：混合材料是麵團，不用原料名假標籤或錯誤比例圖

**鏡頭**：Close-up, pan right

**Prompt**：Close-up in a preparation kitchen, one generic cook folds a dough ball in a bowl with four small plain ingredient bowls nearby, attentive face, mild window light

### A21-S026｜插畫｜估 6.96–7.57 秒

**旁白**：[I04] 如果只是選零食，這可能只是口感差異；放進當時英國的增值稅規則裡，

**CID／來源**：C12 → S2、S3、S4

**畫面功能**：選購口感與法律分類接在同一物件上

**鏡頭**：Medium close-up, pull out

**Prompt**：Medium close-up beside a snack shelf, one generic shopper examines a single curved slice over an open plain cylinder, thoughtful expression, diffuse daylight

### A21-S027｜插畫｜估 5.76–6.26 秒

**旁白**：[I04] 分類卻會改變稅務待遇。 [I05] 判決引用的一九九四年增值稅法，

**CID／來源**：C12 → S2、S3、S4

**畫面功能**：翻到法律文件，從購物轉入課稅問題

**鏡頭**：Wide shot, tilt down

**Prompt**：Wide shot in a law library alcove, one generic researcher opens a thick blank-paged law book at a reading stand, focused face, soft high-window light

### A21-S028｜數字／來源卡｜估 6.72–7.30 秒

**旁白**：[I05] 讓一般食物原則上適用零稅率，但列了一些例外。即開即食的洋芋片，

**CID／來源**：C12 → S2、S3、S4

**畫面功能**：零稅率與例外只能放在本案引用法律範圍

**卡**：一般食物：原則零稅率

**口徑**：英國《1994 年增值稅法》・另有例外

**來源**：本案 2007／2008／2009 判決法條段（S2–S4）

### A21-S029｜插畫｜估 5.52–6.00 秒

**旁白**：[I05] 以及用馬鈴薯、馬鈴薯粉或澱粉做的類似產品，就在其中。

**CID／來源**：C12 → S2、S3、S4

**畫面功能**：例外涵蓋原料粉與澱粉，畫面不另設比例線

**鏡頭**：Medium shot, pan left

**Prompt**：Medium shot at a food study table, one generic researcher places a small bowl of potato powder beside a tray of snack slices, attentive face, mild overhead light

### A21-S030｜插畫｜估 6.72–7.30 秒

**旁白**：[I06] 所以，寶僑爭的並非「這東西能不能吃」。法庭得回答：它夠不夠像洋芋片？

**CID／來源**：C13 → S2、S4

**畫面功能**：相似性用並排觀察表達，不直接畫成完全相同

**鏡頭**：Close-up, push in

**Prompt**：Close-up at a product comparison desk, one generic examiner studies a smooth curved slice beside an irregular crisp, curious face above the tray, soft window light

### A21-S031｜插畫｜估 6.00–6.52 秒

**旁白**：[I06] 而且，能不能說它是用馬鈴薯材料做的？ [I07] 哪怕原料裡有馬鈴薯，

**CID／來源**：C13 → S2、S4

**畫面功能**：另一條件是材料關係，畫面焦點移到原料碗

**鏡頭**：Medium shot, pan right

**Prompt**：Medium shot at a sample bench, one generic examiner points to a plain bowl of potato powder next to a formed slice, thoughtful face, diffuse side light

### A21-S032｜插畫｜估 6.72–7.30 秒

**旁白**：[I07] 只要產品不夠像洋芋片，就不會因這一項例外而被課稅。寶僑要爭的，

**CID／來源**：C13 → S2、S4

**畫面功能**：分類工作示意，不將任一條件畫為唯一裁決

**鏡頭**：Wide shot, pull out

**Prompt**：Wide shot in an evidence sorting room, one generic legal assistant compares two open plain folders beside a sample tray, careful expression, mild ceiling light

### A21-S033｜插畫｜估 5.76–6.26 秒

**旁白**：[I07] 正是這兩道條件。 [I08] 從標準稅率改成零稅率，究竟牽涉多少錢？

**CID／來源**：C13 → S2、S4

**畫面功能**：兩個條件接往稅款問題，不提前給估額

**鏡頭**：Medium close-up, tilt down

**Prompt**：Medium close-up at an accounts desk, one generic bookkeeper opens a blank ledger beside two closed case folders, puzzled expression, soft table-lamp light

### A21-S034｜插畫｜估 5.28–5.74 秒

**旁白**：[I08] 如果公司最後輸了，又是不是得一次補繳一大筆欠稅？

**CID／來源**：敘事／一般解說 → 沒有新增歷史主張

**畫面功能**：是否欠繳先保留問題，不畫拖欠帳單或追債

**鏡頭**：Close-up, pan left

**Prompt**：Close-up at a records desk, one generic clerk studies an unmarked payment envelope beside a closed ledger, uncertain expression, overcast window light

## engine

原段：E01、E02、E02a、E03、E04、E05、E06、E07、E08；519 字。

Active worker 主線：回收2007第一審：倫敦法庭聽公司西歐零食主管證詞、收多冊文件。寶僑以規則外形、口感、麵團及分享罐再封蓋主張差異；消費者先分另類，必須合併時又歸洋芋片。HMRC說市面也有罐裝；法庭認為粉／澱粉本可成麵團，合看各因素而非機械計分，雖近邊界仍相似。此處首次說約42%且最大單一原料，判寶僑敗、標準稅率。接「made from」究竟要什麼角色的爭點。

### A21-S035｜插畫｜估 4.56–4.96 秒

**旁白**：[E01] 二〇〇七年，第一回合在倫敦的稅務法庭展開。

**CID／來源**：C02、C31 → S2

**畫面功能**：2007 第一回合場景回收 H03，尚未揭結果

**鏡頭**：Wide shot, pan left

**Prompt**：Wide shot in a simple British tribunal room, one generic clerk places a closed case folder on a plain hearing table, attentive face, diffuse window light

### A21-S036｜插畫｜估 5.76–6.26 秒

**旁白**：[E01] 法庭聽取寶僑西歐零食部門主管的證詞，還收到多冊文件，

**CID／來源**：C02、C31 → S2

**畫面功能**：證詞及多冊資料用一位證人與案卷示意

**鏡頭**：Medium shot, push in

**Prompt**：Medium shot at a hearing table, one generic business witness opens a thick plain binder beside several closed binders, earnest expression, soft side-window light

### A21-S037｜插畫｜估 7.68–8.35 秒

**旁白**：[E01] 包括公司回答稅務機關追問的資料。 [E02] 寶僑的律師強調，品客形狀規則、顏色均勻，

**CID／來源**：C02、C31、C14 → S2

**畫面功能**：形狀規則是當事人論點，樣品近看

**鏡頭**：Close-up, pan right

**Prompt**：Close-up at a sample review table, one generic legal representative lifts one uniformly curved slice from an orderly row, focused face above the samples, mild overhead light

### A21-S038｜插畫｜估 6.00–6.52 秒

**旁白**：[E02] 入口還有化開的口感。用麵團製作，在他看來更像蛋糕或餅乾。

**CID／來源**：C14 → S2

**畫面功能**：蛋糕餅乾是律師類比，不畫成法庭已採納分類

**鏡頭**：Medium close-up, pull out

**Prompt**：Medium close-up at a legal preparation desk, one generic advocate points to a plain biscuit beside a dough sample, thoughtful face, soft desk-lamp light

### A21-S039｜插畫｜估 7.20–7.83 秒

**旁白**：[E02a] 消費者調查也沒有只給一種答案。參與分組的消費者會把品客另列一類；

**CID／來源**：C32 → S2

**畫面功能**：消費者分組是調查示意，不畫調查原件或真受試者

**鏡頭**：Wide shot, tilt down

**Prompt**：Wide shot in a simple survey room, one generic participant places a plain cylinder in its own sorting tray, attentive face, diffuse window light

### A21-S040｜插畫｜估 5.28–5.74 秒

**旁白**：[E02a] 但若必須併入另一類，他們又會把它放到洋芋片那邊。

**CID／來源**：C32 → S2

**畫面功能**：被要求合併時把同一物件移到洋芋片一組

**鏡頭**：Close-up, pan left

**Prompt**：Close-up at a sorting table, one generic participant moves a plain cylinder into a tray holding unmarked crisp bags, thoughtful face above the tray, mild ceiling light

### A21-S041｜插畫｜估 4.80–5.22 秒

**旁白**：[E02a] 能認出它不同，和它夠不夠相似，並不是同一件事。

**CID／來源**：C32 → S2

**畫面功能**：不同與相似可同時存在，用單人比較動作銜接

**鏡頭**：Medium shot, push in

**Prompt**：Medium shot at a sample display, one generic researcher studies a curved slice and an irregular crisp on one plate, puzzled expression, soft window light

### A21-S042｜插畫｜估 6.48–7.04 秒

**旁白**：[E03] 那只圓筒也成了辯論的一部分。案中品客多數裝在分享用的大罐，

**CID／來源**：C15 → S2

**畫面功能**：圓筒回到爭點，分享規格用大罐示意

**鏡頭**：Wide shot, pan right

**Prompt**：Wide shot at a domestic dining table, one generic host places a large plain snack cylinder in the centre of the table, welcoming expression, overcast daylight

### A21-S043｜插畫｜估 5.52–6.00 秒

**旁白**：[E03] 配上可以重新封口的塑膠蓋，和平常的小袋洋芋片不同。

**CID／來源**：C15 → S2

**畫面功能**：重新封口的塑膠蓋作為可見差異

**鏡頭**：Close-up, pull out

**Prompt**：Close-up at a kitchen counter, one generic user presses a plain plastic lid back onto a snack cylinder, relaxed face above the lid, mild overhead light

### A21-S044｜插畫｜估 6.96–7.57 秒

**旁白**：[E03] 寶僑把包裝當成差異，但稅務機關指出，市面上也有洋芋片裝在罐子裡。

**CID／來源**：C15 → S2

**畫面功能**：罐裝不是單一品牌獨占特徵，保留匿名包裝

**鏡頭**：Medium shot, tilt down

**Prompt**：Medium shot beside a shop shelf, one generic stock clerk holds an open plain can containing irregular crisps, focused face, diffuse ceiling light

### A21-S045｜插畫｜估 4.56–4.96 秒

**旁白**：[E04] 對法庭來說，不能看到麵團，就立刻把產品排除。

**CID／來源**：C16 → S2

**畫面功能**：麵團不自動排除的法律考量回到樣品

**鏡頭**：Medium close-up, pan left

**Prompt**：Medium close-up at an evidence table, one generic legal reader studies a dough sample beside an open blank case folder, thoughtful face, soft side light

### A21-S046｜插畫｜估 5.76–6.26 秒

**旁白**：[E04] 因為法條自己寫了馬鈴薯粉和澱粉，用這些材料製造薄片，

**CID／來源**：C16 → S2

**畫面功能**：法條提到粉與澱粉，圖只示原料材料

**鏡頭**：Close-up, push in

**Prompt**：Close-up at a materials bench, one generic technician lifts a plain scoop of potato powder over a bowl, attentive face above the bowl, mild window light

### A21-S047｜插畫｜估 6.00–6.52 秒

**旁白**：[E04] 本來就可能需要先做成麵團。 [E05] 它也沒有把每個差異分別打分，

**CID／來源**：C16、C17 → S2

**畫面功能**：從材料到整體評估，不畫假打分表

**鏡頭**：Wide shot, pan right

**Prompt**：Wide shot in a product review room, one generic examiner lays a blank observation sheet beside a tray of sample slices, concentrated face, soft overhead light

### A21-S048｜插畫｜估 6.72–7.30 秒

**旁白**：[E05] 再加總出一個分數。法庭把外觀、味道、原料和銷售等因素合在一起看，

**CID／來源**：C17 → S2

**畫面功能**：整體考量外觀、材料與販售包裝，同鏡單一觀察動作

**鏡頭**：Medium shot, pull out

**Prompt**：Medium shot at a broad exhibit bench, one generic examiner studies snack slices, an ingredient bowl and plain packages arranged together, thoughtful face, diffuse window light

### A21-S049｜插畫｜估 7.20–7.83 秒

**旁白**：[E05] 認為品客雖然接近分類邊界，仍然足夠相似。 [E06] 另一道條件，輪到馬鈴薯含量。

**CID／來源**：C17、C18 → S2

**畫面功能**：由相似性轉到原料問題，不用比例秤誤造法定門檻

**鏡頭**：Close-up, tilt down

**Prompt**：Close-up at a case preparation table, one generic reader turns a blank page beside a potato powder bowl, serious face, mild desk-lamp light

### A21-S050｜數字／來源卡｜估 6.72–7.30 秒

**旁白**：[E06] 法庭採用的案中比例約為百分之四十二，是最大的單一原料；它認為，

**CID／來源**：C18 → S2

**畫面功能**：42% 只屬本案配方，沒有最低門檻含義

**卡**：約 42%

**口徑**：案中馬鈴薯原料比例・最大單一原料

**來源**：2007 稅務法庭判決 §5(2)、§17（S2）

### A21-S051｜插畫｜估 6.48–7.04 秒

**旁白**：[E06] 其他材料的存在，不妨礙產品由馬鈴薯粉做成。 [E07] 第一個答案出來了：

**CID／來源**：C18、C02 → S2

**畫面功能**：多種原料與馬鈴薯粉同在，先呈理由再到裁決

**鏡頭**：Medium shot, pan left

**Prompt**：Medium shot at a food analysis bench, one generic technician examines a formed slice beside several plain ingredient bowls, attentive face, soft window light

### A21-S052｜數字／來源卡｜估 6.72–7.30 秒

**旁白**：[E07] 寶僑的上訴被駁回，這個版本的Regular Pringles，

**CID／來源**：C02 → S2

**畫面功能**：第一回合結果只對案中版本

**卡**：2007：寶僑上訴駁回

**口徑**：本案 Regular Pringles・標準稅率

**來源**：2007 稅務法庭判決 §19（S2）

### A21-S053｜插畫｜估 6.96–7.57 秒

**旁白**：[E07] 要適用標準稅率。 [E08] 但寶僑還有一個可以爭的地方。法條寫「用馬鈴薯做的」，

**CID／來源**：C02、C19 → S2、S3

**畫面功能**：敗訴後再讀關鍵詞，畫面不偽造引文

**鏡頭**：Medium close-up, push in

**Prompt**：Medium close-up at a legal research desk, one generic advocate places a plain bookmark in an open law book, intent expression, mild table-lamp light

### A21-S054｜插畫｜估 7.20–7.83 秒

**旁白**：[E08] 到底只要含有馬鈴薯就夠，還是馬鈴薯必須在產品裡扮演更主要的角色？

**CID／來源**：C19 → S2、S3

**畫面功能**：原料角色留成疑問，供下一章接續

**鏡頭**：Wide shot, pan right

**Prompt**：Wide shot in a quiet study room, one generic legal researcher studies a potato beside a bowl of dough and a finished slice, questioning face, diffuse window light

## turn

原段：T01、T02、T03、T04、T05、T06、T07；317 字。

Active worker 主線：2008七月Warren法官另讀條文：將油視為烹調媒介，追問普通洋芋片與馬鈴薯的對應關係，要求類似產品也符合。案中品客未過此條件，寶僑暫勝、零稅率。法官有討論相似性，但未另判不相似；若made-from讀法錯誤，相似性可能發回。接著上訴的是HMRC，寶僑轉為守住勝訴的一方。以三名法官應看高院新解釋還是原課稅決定設問，未先揭標準。

### A21-S055｜插畫｜估 6.72–7.30 秒

**旁白**：[T01] 二〇〇八年七月，高等法院的Warren法官採取了另一種讀法。

**CID／來源**：C03、C20 → S3、S4

**畫面功能**：2008 高院讀法回收 H04 的第二預告

**鏡頭**：Medium shot, tilt down

**Prompt**：Medium shot at a high-ceiling legal reading room, one generic legal reader holds an open blank case folder, thoughtful face turned toward the pages, soft side-window light

### A21-S056｜插畫｜估 5.04–5.48 秒

**旁白**：[T01] 普通洋芋片炸過、含有油，為什麼仍算用馬鈴薯做的？

**CID／來源**：C03、C20 → S3、S4

**畫面功能**：油炸含油的洋芋片讓讀法有可見問題

**鏡頭**：Close-up, pull out

**Prompt**：Close-up beside a simple fryer, one generic cook lifts a basket of potato slices above the oil, focused face, mild overhead light

### A21-S057｜插畫｜估 7.44–8.09 秒

**旁白**：[T02] 他的讀法，是把烹調用的油看成加工媒介，追問馬鈴薯在產品裡扮演的角色。

**CID／來源**：C20 → S3、S4

**畫面功能**：烹調媒介只以烹調動作示意，不當新化學證據

**鏡頭**：Medium shot, pan left

**Prompt**：Medium shot in a demonstration kitchen, one generic cook lowers a tray of raw potato slices toward a frying basket, attentive face, diffuse window light

### A21-S058｜插畫｜估 7.92–8.61 秒

**旁白**：[T02] 即使成品含油，洋芋片仍是把馬鈴薯加工而來；其他類似產品，也得有相應的關係。

**CID／來源**：C20 → S3、S4

**畫面功能**：加工前後並列，不把類似產品等同純馬鈴薯

**鏡頭**：Wide shot, push in

**Prompt**：Wide shot at a food preparation bench, one generic cook compares a raw potato slice with a fried crisp on separate small plates, thoughtful face, soft ceiling light

### A21-S059｜插畫｜估 5.28–5.74 秒

**旁白**：[T03] 依這種解釋，案中品客沒有通過「用馬鈴薯做的」這一關。

**CID／來源**：C03、C20 → S3、S4

**畫面功能**：依高院解釋檢視案中成品，結果保持當時範圍

**鏡頭**：Medium close-up, pan right

**Prompt**：Medium close-up at a legal exhibit table, one generic reader examines a curved snack slice beside an open blank folder, serious expression, grey window light

### A21-S060｜數字／來源卡｜估 4.56–4.96 秒

**旁白**：[T03] 寶僑這次贏了，上訴獲准，產品可以適用零稅率。

**CID／來源**：C03、C20 → S3、S4

**畫面功能**：第二回合勝訴不要冒充最終結局

**卡**：2008：寶僑勝訴

**口徑**：高等法院・本案產品零稅率

**來源**：2008 高院判決 §79–86（S3）

### A21-S061｜插畫｜估 6.72–7.30 秒

**旁白**：[T04] 法官也討論了相似性。不過，這次勝訴靠的是「用馬鈴薯做的」這項條件；

**CID／來源**：C21 → S3

**畫面功能**：兩條件中勝訴依據不同，文件比較留在匿名讀者

**鏡頭**：Close-up, pull out

**Prompt**：Close-up at a law library desk, one generic researcher touches one of two blank document tabs in an open binder, focused face, mild desk-lamp light

### A21-S062｜插畫｜估 5.52–6.00 秒

**旁白**：[T04] 若這個讀法有誤，他認為，相似性的判斷可能得發回重審。

**CID／來源**：C21 → S3

**畫面功能**：條件式發回保留可能性，不畫成已重審

**鏡頭**：Wide shot, tilt down

**Prompt**：Wide shot in a court records room, one generic clerk holds a closed plain case folder above an empty return tray, cautious expression, soft window light

### A21-S063｜插畫｜估 6.96–7.57 秒

**旁白**：[T05] 英國稅務機關HMRC接著提出上訴。這一次，寶僑從提出上訴的一方，

**CID／來源**：C22 → S4

**畫面功能**：稅務機關提出上訴，動作與原公司上訴方向有別

**鏡頭**：Medium shot, pan left

**Prompt**：Medium shot at an administrative filing desk, one generic tax official places a fresh plain appeal folder into an outgoing tray, determined expression, diffuse overhead light

### A21-S064｜插畫｜估 6.00–6.52 秒

**旁白**：[T05] 變成要守住高院勝訴的一方。 [T06] 這回，稅務機關要說服上訴法院，

**CID／來源**：C22 → S4

**畫面功能**：銜接寶僑守住勝訴與稅務機關上訴；匿名讀者比較卷宗，不把同鏡兩方論點歸給一位律師

**鏡頭**：Close-up, push in

**Prompt**：Close-up at a legal preparation table, one generic legal reader compares two open blank case folders, concentrated face, soft table-lamp light

### A21-S065｜插畫｜估 6.24–6.78 秒

**旁白**：[T06] 高等法院把這句話讀得太窄，而最初稅務法庭的判斷應該恢復。

**CID／來源**：C22 → S4

**畫面功能**：兩份裁判放在同一閱讀桌供比較，沒有畫成相傳技術

**鏡頭**：Medium shot, pan right

**Prompt**：Medium shot in a courthouse study alcove, one generic legal reader compares two open blank case folders, thoughtful face, overcast window light

### A21-S066｜插畫｜估 7.68–8.35 秒

**旁白**：[T07] 三名上訴法院法官，該從高院的新解釋下手，還是回頭檢查最初那份課稅決定？

**CID／來源**：C23 → S4

**畫面功能**：應檢查哪份判斷先留問句，不出裁判結果

**鏡頭**：Wide shot, pull out

**Prompt**：Wide shot in a court document archive, one generic clerk lifts the lowest of three plain case folders from a shelf, attentive face, mild ceiling light

## now

原段：N01、N02、N03、N03a、N04、N05、N06、N07、N08、N09、N10；600 字。

Active worker 主線：2009-05-20第三回合開頭直接揭三位法官一致准HMRC上訴、恢復原課稅決定，再答需檢查原法庭法律錯誤而非只重秤因素。接P&G全部／幾乎全部主張、法官果醬反例、替代馬鈴薯本質未具體說明、普通洋芋片含量變動與法條未定最低百分比，不加50%門檻。回收錢：律師估過去最多1億英鎊／往後每年2千萬；AP報公司稱一直保護性繳稅，非欠稅確數。最後三句首次給2025後案仍引用、問觀眾漏後續的品牌故事、訂閱；接21秒片尾。

### A21-S067｜插畫｜估 4.32–4.70 秒

**旁白**：[N01] 二〇〇九年五月二十日，第三回合有了答案：

**CID／來源**：C04 → S4

**畫面功能**：第三回合回收 H04 的三份文件預告

**鏡頭**：Close-up, pan right

**Prompt**：Close-up at an appellate court document counter, one generic clerk arranges three closed plain case folders in one row, serious face above the folders, mild ceiling light

### A21-S068｜數字／來源卡｜估 6.96–7.57 秒

**旁白**：[N01] 三名上訴法院法官一致同意HMRC勝訴，恢復稅務法庭的課稅決定。

**CID／來源**：C04 → S4

**畫面功能**：最終勝負在此首次可見，三名一致以文字表達

**卡**：2009：HMRC 勝訴

**口徑**：5 月 20 日・三名法官一致・恢復原課稅決定

**來源**：上訴法院判決 §44、§67、§68（S4）

### A21-S069｜插畫｜估 5.04–5.48 秒

**旁白**：[N02] 焦點落回最初的稅務法庭。即使寶僑已在高院贏過，

**CID／來源**：C23 → S4

**畫面功能**：焦點回到原法庭案卷，不把上訴當重新投票

**鏡頭**：Medium shot, tilt down

**Prompt**：Medium shot at an appellate reading desk, one generic researcher opens the earliest plain case folder from a stacked set, focused face, diffuse window light

### A21-S070｜插畫｜估 6.48–7.04 秒

**旁白**：[N02] 仍得指出原法庭哪裡犯了法律錯誤。原法庭若用對法律、結論合理，

**CID／來源**：C23 → S4

**畫面功能**：法律錯誤與理由是檢查重點，文件不生假內容

**鏡頭**：Close-up, pan left

**Prompt**：Close-up at a judicial study table, one generic legal reader follows a blank page with a plain ruler, attentive face, soft table-lamp light

### A21-S071｜插畫｜估 4.80–5.22 秒

**旁白**：[N02] 上訴法院不能只因自己看重不同因素，就推翻它。

**CID／來源**：C23 → S4

**畫面功能**：另一種權重不直接推翻原裁判，用保留原卷示意

**鏡頭**：Wide shot, push in

**Prompt**：Wide shot in a case records room, one generic archivist returns an intact closed folder to its shelf, thoughtful expression, grey doorway light

### A21-S072｜插畫｜估 5.52–6.00 秒

**旁白**：[N03] 寶僑主張，法條要求產品全部或幾乎全部由馬鈴薯做成。

**CID／來源**：C24 → S4

**畫面功能**：全或幾乎全是當事人的讀法，不用真理天平

**鏡頭**：Medium close-up, pan right

**Prompt**：Medium close-up at a legal preparation desk, one generic advocate points toward a potato beside a bowl of mixed dough, insistent expression, mild window light

### A21-S073｜插畫｜估 7.20–7.83 秒

**旁白**：[N03] 判決用果醬反問：橘子和葡萄柚一起煮成果醬，難道就既不是用橘子做的，

**CID／來源**：C24 → S4

**畫面功能**：果醬是判決中的比喻；不指真實庭上煮食

**鏡頭**：Close-up, pull out

**Prompt**：Close-up in a domestic kitchen, one generic cook stirs a small pot of marmalade with an orange and a grapefruit beside it, thoughtful face, soft overhead light

### A21-S074｜插畫｜估 6.24–6.78 秒

**旁白**：[N03] 也不是用葡萄柚做的？ [N03a] 律師接著說，至少得有足夠的「馬鈴薯本質」。

**CID／來源**：C24、C33 → S4

**畫面功能**：果醬保留兩種水果來源，再回材料本質問題

**鏡頭**：Wide shot, tilt down

**Prompt**：Wide shot at a kitchen worktop, one generic cook studies a spoonful of marmalade above a plain jar, cut orange and grapefruit nearby, curious face, diffuse window light

### A21-S075｜插畫｜估 6.72–7.30 秒

**旁白**：[N03a] 法官追問這究竟指什麼，卻沒有得到更具體的說明；光靠味道也不行，

**CID／來源**：C33 → S4

**畫面功能**：馬鈴薯本質未說清，以法律讀者疑問表達

**鏡頭**：Medium shot, pan left

**Prompt**：Medium shot in a consultation room, one generic legal reader studies a potato and a seasoned crisp on one sample plate, puzzled expression, soft table-lamp light

### A21-S076｜插畫｜估 5.52–6.00 秒

**旁白**：[N03a] 洋芋片炸過、加了調味後，原本的馬鈴薯味已經大不相同。

**CID／來源**：C33 → S4

**畫面功能**：油炸與調味影響味道，圖只呈調味動作

**鏡頭**：Close-up, push in

**Prompt**：Close-up at a snack preparation bench, one generic cook sprinkles seasoning over fried potato slices, focused face above the tray, mild ceiling light

### A21-S077｜插畫｜估 6.00–6.52 秒

**旁白**：[N04] 高等法院那套對應洋芋片的讀法，也遇到難題。上訴法院指出，

**CID／來源**：C25 → S4

**畫面功能**：比較標準的難題回到文件與樣品，非另開稅務課

**鏡頭**：Wide shot, pan right

**Prompt**：Wide shot in a product reference room, one generic researcher studies several plain crisp packets beside an open blank binder, thoughtful face, grey window light

### A21-S078｜插畫｜估 6.48–7.04 秒

**旁白**：[N04] 普通洋芋片本身的馬鈴薯含量就有變動；拿它來要求相近的含量，

**CID／來源**：C25 → S4

**畫面功能**：普通洋芋片含量可變，不畫不存在的精確百分比

**鏡頭**：Medium close-up, pull out

**Prompt**：Medium close-up at a sample table, one generic examiner compares crisps from two unmarked packets on separate plates, concentrated face, soft side light

### A21-S079｜插畫｜估 6.24–6.78 秒

**旁白**：[N04] 標準本身反而不確定。 [N05] 那要多少才夠？法律沒有指定最低百分比，

**CID／來源**：C25、C26 → S4

**畫面功能**：沒有最低百分比，圖不添加任何數字刻度

**鏡頭**：Close-up, tilt down

**Prompt**：Close-up at a law library desk, one generic reader holds an open blank law book above a sample plate, questioning expression, mild desk-lamp light

### A21-S080｜插畫｜估 6.48–7.04 秒

**旁白**：[N05] 法院也不另畫一條線。法官認為，不必先找出所有產品的精確界線，

**CID／來源**：C26 → S4

**畫面功能**：眼前個案判斷與所有精確界線分開

**鏡頭**：Medium shot, pan left

**Prompt**：Medium shot in a legal study room, one generic examiner points to a single curved snack slice on a small plain plate, focused face, diffuse window light

### A21-S081｜插畫｜估 5.28–5.74 秒

**旁白**：[N05] 才能判斷眼前這款；替條文加門檻，反而是在代替立法。

**CID／來源**：C26 → S4

**畫面功能**：不替條文加門檻，以閱讀既有書本示意

**鏡頭**：Wide shot, push in

**Prompt**：Wide shot in a quiet library aisle, one generic researcher returns a closed law book to a plain shelf, considered expression, soft overhead light

### A21-S082｜插畫｜估 6.48–7.04 秒

**旁白**：[N06] 至於爭了三回合的稅款，二〇〇九年判決記下，HMRC律師估計，

**CID／來源**：C27 → S4

**畫面功能**：金額先交代為訴訟律師估算，不畫稅務追繳帳單

**鏡頭**：Medium close-up, pan right

**Prompt**：Medium close-up at a legal accounts desk, one generic accountant studies a blank estimate sheet beside an open case folder, careful expression, grey window light

### A21-S083｜數字／來源卡｜估 7.68–8.35 秒

**旁白**：[N06] 過去的稅最多約一億英鎊，之後一年約兩千萬英鎊。這是訴訟牽涉的估計規模。

**CID／來源**：C27 → S4

**畫面功能**：兩個估額的期間、上限與說話者都保留

**卡**：過去最多約 £1 億
之後每年約 £2,000 萬

**口徑**：2009 年 HMRC 律師估計訴訟稅款規模

**來源**：2009 上訴法院判決 §1（S4）

### A21-S084｜插畫｜估 6.00–6.52 秒

**旁白**：[N07] 它並不等於寶僑積欠這麼多。美聯社當年報導，公司發言人說，

**CID／來源**：C28 → S5

**畫面功能**：公司說法的歸屬與估額分開，不把新聞當獨立核帳

**鏡頭**：Medium shot, pull out

**Prompt**：Medium shot at a newsroom reading desk, one generic reporter studies a blank statement sheet beside a closed notebook, attentive face, soft window light

### A21-S085｜數字／來源卡｜估 7.20–7.83 秒

**旁白**：[N07] 一直有先保護性地繳稅，所以沒有欠稅；勝負和實際是否已繳，必須分開看。

**CID／來源**：C28 → S5

**畫面功能**：已繳與欠稅由公司發言人說法限縮；這是摘要而非逐字引文

**卡**：保護性繳稅／沒有欠稅

**口徑**：公司發言人說法・不等同獨立核帳

**來源**：美聯社／NBC，2009-05-20（S5）

### A21-S086｜插畫｜估 5.52–6.00 秒

**旁白**：[N08] 這場官司界定的是英國的課稅範圍；它留下的判斷方法，

**CID／來源**：C29 → S6

**畫面功能**：案卷進入後來判決的參考脈絡，不重播勝負

**鏡頭**：Wide shot, tilt down

**Prompt**：Wide shot in a legal reference archive, one generic researcher takes a plain case volume from a shelf, interested expression, mild ceiling light

### A21-S087｜數字／來源卡｜估 7.68–8.35 秒

**旁白**：[N08] 到二〇二五年另一宗Sensations Poppadoms零食稅案，

**CID／來源**：C29 → S6

**畫面功能**：後續案名年份明確區隔，並非品客再審

**卡**：2025：另一宗零食稅案

**口徑**：Sensations Poppadoms・引用本案方法

**來源**：Walkers 判決 [2025] UKUT 155（S6）

### A21-S088｜插畫｜估 6.72–7.30 秒

**旁白**：[N08] 還被法庭拿來引用。 [N09] 你還聽過哪個品牌故事，只流傳中間贏的那一回，

**CID／來源**：C29 → S6

**畫面功能**：合上後續卷宗接觀眾的未完整故事，不新增品牌例子

**鏡頭**：Medium close-up, pan left

**Prompt**：Medium close-up at a home reading table, one generic viewer closes a plain case book beside an unmarked snack cylinder, curious expression, soft window light

### A21-S089｜插畫｜估 7.44–8.09 秒

**旁白**：[N09] 沒有把後來說完？ [N10] 想把熟悉商品背後的真實轉折聽完整，歡迎訂閱這個系列。

**CID／來源**：敘事／一般解說 → 沒有新增歷史主張

**畫面功能**：留言與訂閱保留旁白，圖不畫假按鈕或下一集

**鏡頭**：Close-up, push in

**Prompt**：Close-up at a home desk, one generic viewer places a blank bookmark into an open notebook, warm attentive face, mild table-lamp light

## 鉤子回收

| setup | payoff | 新資訊 |
|---|---|---|
| H01、H02 | O02、O03、O04、O05、E03 | 圓筒先解運送與保存，再成為相似性論點之一；不說包裝造成訴訟。 |
| H03 | E01、E07 | 2007 法庭預告回收第一回合與稅率結果。 |
| H04 | T01、T02、T03、T04 | 2008 換讀法回收高院解釋與暫時勝訴。 |
| H04、H05 | N01 | 2009 三回合問題在末章第一段回答。 |
| O07 | I03、I06、E06、T02、N03、N03a、N04、N05 | 麵團中的馬鈴薯角色，逐步走到 made from 的法律判斷。 |
| I08 | N06、N07 | 稅款估額與是否欠繳分別作答，不把兩者合成債務。 |
| E08 | T02、T03 | 用馬鈴薯做成的讀法帶來高院轉折。 |
| T05、T06、T07 | N01、N02 | 上訴法院先檢查原法庭有無法律錯誤，再給最終結果。 |

## 可選 look 計畫

- **generic_package_designer**：包裝與製法以匿名設計員示意；不指定發明人肖像。 未產生設定圖、未綁正式角色。
- **generic_legal_reader**：三個法院層級使用不同書桌、文件與鏡位，僅匿名解說，不重建任何特定法官或律師。 未產生設定圖、未綁正式角色。

## 檢查與下一步

官方 shot_reading：78 張插畫、0 traps；原段重建及來源映射通過純結構檢查。此包由編輯製作，沒有獨立審者 PASS。

- Independent review of this editorial storyboard
- Formal chapter JSON and claim/line mapping, real verifier/listener/narrative checks
- Actual TTS duration; body length must be checked without padding or slowing speech
- Concrete full-film quote before paid work; no paid authorization provided by this package
- Image judge, branding asset binding, render, playback and owner review
- Owner-selected languages and separate upload/end-screen targets

## 開場預告同圖回收

- **A21-S004 / H03 → A21-S035 / E01**：同一稅務法庭案卷與匿名書記官圖；首次只預告審理，E01 才展開第一回合。；asset key `a21-hook-reuse-4`。
- **A21-S005 / H04 → A21-S055 / T01**：同一高院讀卷示意圖；H04 不放結果，T01 才接新讀法。；asset key `a21-hook-reuse-5`。
- **A21-S006 / H04 → A21-S067 / N01**：同一上訴法院三份文件圖；不畫三人互動，末章才給勝負。；asset key `a21-hook-reuse-6`。

78 個插畫位置規劃 75 張獨立圖。每組必須綁同一張已收片 file/hash，prompt/camera/preset 逐字相同；model/size/seed/cast/references 也需一致。尚無圖片，不能聲稱已命中快取。
