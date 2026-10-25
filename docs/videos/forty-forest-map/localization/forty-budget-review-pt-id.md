# ForTy PT／ID 縮句提案獨立覆核

狀態：**ID／PT均已完成獨立逐句覆核**。直接比較目前繁中、現行兩語譯文及候選縮句，沒有沿用作者三遍自評作為判定。ID建議6處精確化，PT建議8處修正／精確化；原有7項保全文unresolved維持。沒有改repo／todo／音訊，沒有spawn或執行TTS。這是文字審查，不是實際配音fit收據。

## 綁定資料

- 當前video SHA-256：`2b689e3f9e2f38d8da58b5fd1d5d999a2ef5d8e917102680a8c6de06cd859ca6`，92句。
- ID i18n SHA-256：`c20f51a2665d8123af6afac19a334a0459f6ea550cc599eac284597cd840eb31`，92句。
- PT i18n SHA-256：`93ab5f101ea15769fc1e6d08fe9305c0320d61e65b1f83779ded445fc0d0e13d`，92句。
- PT／ID提案檔SHA-256：`87d001853222dc1ef589ca9035ac331a37b5ce9f5171dc44714be6911a5ac1b8`。
- 提案內宣告source仍是`a62a48382272fb4b9171f2c261b8f736c7516afca35417ccaa842757b04f8a6f`；本次依2b689實際來源審，不沿用舊hash作為語義證據。7句中文ASR同義改寫的像素／森林稱呼不改數字或關係，ID現譯文也未因本次縮句先改動。採納時仍由root走正常current source resync／merge，不手改hash。
- 字數上限以本次讀取的原生ID todo為準，不盲用提案較舊max_chars；例如jw6i現62、dkq3現57、y64h現54、ywz8現62、mx7g現61。
- 原生todo SHA-256：ID `5c005bf537e935585e0c6aba9a7baf7a6816f63e6e472e97aa174edbe8b190f4`；PT `8d64f076940f45303c7fdd8e65702ee901d21def82c3485b92aeca04f5fdf1a3`。
- 範圍：71項ID與79項PT候選全部逐句讀完；另讀ID其餘21句、PT其餘13句作上下文與數值核對，兩語均覆蓋92句。所有候選old_text均與本次現行i18n相同。提案內characters逐項重算無誤；是否在時窗內仍須正常原生fit。

## ID建議修正

以下都是可保義的具體修法；不是說每個當前候選都已經反義。數字沒有發現翻錯，重點是讓運算對象、像素與註記動作不靠猜。

| ID | 問題 | 現候選 | 自然且保義的建議 | 字元／當前max |
| --- | --- | --- | --- | --- |
| 7iv8 | `250 kurang jumlah`未指明扣哪個總和，可能讀成250扣「總量本身」；此處要扣已介紹的前五值之和。 | Kelas ke-6 sisa total: 250 kurang jumlah. | Kelas 6: 250 dikurangi jumlah 5 nilai lain. | 43／43 |
| u362 | 句首`2 lahan lain`可能聽成兩塊其他土地，缺少「儲存值2」標記；要明確對到第6類。 | 2 lahan lain dibagi, menjadi 0,008. | Nilai 2 untuk lahan lain dibagi, menjadi 0,008. | 47／49 |
| w86h | 自然度／指涉精確化：`isi bingkai merah`容易像把框本身填色；源文是紅框內的像素呈分類綠。 | Pilih maksimum; isi bingkai merah pakai hijau kelas itu. | Pilih skor tertinggi; piksel berbingkai merah jadi hijau. | 57／57 |
| 8m2e | `cocokkan dengan hasil nyata`省略操作對象，緊接acuan independen可能讓人以為對照參考資料而非模型分數；明說skor。 | Untuk membaca skor sebagai peluang benar, pakai acuan independen; cocokkan dengan hasil nyata. | Untuk baca skor sebagai peluang benar, pakai acuan independen; cocokkan skor dengan hasil nyata. | 96／98 |
| ncx4 | `seri tahunan awal`沒有清楚保留early-release版本狀態，與較早年代序列可能混淆。 | Pengenalan itu juga berbagi seri tahunan awal 2017–2025. | Pengenalan itu juga berbagi seri tahunan rilis awal 2017–2025. | 62／68 |
| bu6j | 候選只剩欄位清單，源文「寫進紀錄」的可完成動作不明；有足夠空間保留記錄動詞。 | Dalam satu baris piksel: tahun, lokasi, 6 skor, dan semua kelas tertinggi. | Tulis dalam satu baris piksel: tahun, lokasi, 6 skor, dan semua kelas tertinggi. | 80／82 |

7iv8建議中的5是已知五個儲存值的明示，不是新增測量。w86h的highest-score→色彩關係由前句已確立的最高類承接，沒有把類別ID大小當成分數。4w7g維持原全文「Lingkungan apa yang biasanya kamu lihat lewat peta?」51字元／max22的unresolved；不能縮成問用哪張地圖、製圖或漏掉環境種類／習慣。

## ID逐子句核對結果

除上表的指涉／操作／版本精確化外，未發現其餘候選把原意反轉、丟失必要數值或合併類別。特別確認：

- 第3類`hutan tanaman`與第4類`hutan perkebunan`分開；3pse保留栽植或播種、主要形成方式、這份資料及>40年，未提案的2vcb保留≤40年。輪伐安排與當前樹齡否定保留。
- 250為六類總量、255另作無資料的vk36原文保留；5個儲存整數、補第6類、排除無資料而非當分數均未變成六個已存band。
- A五值[0,248,0,0,0]、其餘4類0、248總和、250−248=2、÷250=.992／.008、6分數和1及唯一最高均未改。
- B原始[0,86,0,1,77]、86+1+77=164、Other86、自然更新與其他土地2類並列、共同.344、種植園.004、樹作.308、其餘兩類0均保留。0,344／0,004／0,308是ID小數逗號，不是數值變動。
- A121.4°E／24.7°N與B指定像素中心121.42234°E／24.69528°N均保留，bujur timur與lintang utara方向正確；ymf8縮句仍是24,69528°北緯，沒有換成窗口幾何中心。
- 新驗算.344+.344=.688，+.308=.996，+.004=1，另2類0不改總和保留。ecb8的逐值對回類別與小數／漏項檢查仍能對回固定類名，沒有以加總1宣稱分類正確。
- `regenerasi alami／regenerasi`依已介紹的full類名只指第2類；`hutan tanaman`沒有與`hutan perkebunan`合併。樹作短稱仍指既定第5類。這些縮句不增加新類。
- `Peta kami`清楚限定本片衍生圖；`maksimum pertama dalam urutan kelas`保留按類序取第一個最大者，沒有宣稱官方硬分類層的tie規則已驗證。7qfx保留兩類同為最高與取首顯示註記。
- `skor model`和`ketepatan sebenarnya／peluang benar`分開，未校準、99.2%不能直接當正確機率的否定均保留。
- B刻意選最低最大值與非隨機精度樣本保留；2020兩像素僅說明本版本輸出，不冒充2017–2025本次實測。年度版狀態只需按ncx4精確化。
- 記錄年、位置、全部6分數與所有最高者未丟；bu6j宜按上表恢復寫入動作。
- DeepMind、ForTy、AlphaEarth官方拼字沒有被改成中文讀音或其他型號。

## ID預算與狀態說明

70項候選在目前原生max_chars內，4w7g明確保全文未解。部分新時窗已能放原譯，例如jw6i、y64h、ywz8；若root選擇保留較完整原文，不必為縮而縮。上述新修法已按Unicode字元逐字計數，不改時窗、速度或門檻。

**ID文字判定：建議採上表6處精確化後，按原生整窗／實際付費配音再檢查；不是fit通過。** 其他原句和數字沒有額外問題。

## PT建議修正

| ID | 問題 | 現候選 | 自然且保義的建議 | 字元／當前max |
| --- | --- | --- | --- | --- |
| e826 | 新current時窗max為56，候選仍58；這是新增的預算差異。保留五個有效值、補OtherLand及比較六類，不能靠刪數字解決。 | 5 valores válidos: calcule outras terras; compare 6 tipos. | 5 valores válidos: calcule outras terras; compare as 6. | 55／56 |
| erqz | `ação humana visível`較像看見人的行動，應精確保留森林可見人為干擾的判準。 | Floresta primária: nativas, sem ação humana visível. | Floresta primária: nativas, sem distúrbio humano visível | 56／56 |
| 7iv8 | `a soma`可再明示為已介紹的五個儲存值之和，讓聽眾可直接跟算；不把250誤當要扣掉的總和本身。 | A 6ª é o resto: 250 menos a soma. | A 6ª: 250 menos a soma dos 5 valores. | 37／38 |
| w86h | `verde do máximo`容易把綠色當成最大數值的色階；源文是先取最高分的類，再用該類的綠色畫指定像素。 | No quadro vermelho, pinta-se o verde do máximo. | O máximo dá ao pixel marcado o verde da classe. | 47／50 |
| 7qfx | 候選保留並列與取首顯示的事實，但`exibe-se`獨立敘述不夠明確要求把顯示規則也寫進紀錄；可讓Anote統攝兩項。 | Registre regeneração e outras terras empatadas; exibe-se a primeira. | Anote regeneração e outras terras empatadas, com a primeira exibida. | 68／73 |
| vb62 | `sem calibrar chance depois`的語序不自然，也可能聽成之後不進行校準的安排。用a posteriori明確指事後校準，而非未來禁令。 | Nota do modelo sem calibrar chance depois. | Nota sem calibrar chances a posteriori. | 39／43 |
| 8m2e | `compare com resultados reais`省略所比對的分數，緊接參考資料可能讓操作對象混淆；要明說compare a nota。 | Nota como chance de acerto pede referência independente; compare com resultados reais. | Nota como chance pede referência independente: compare a nota com resultados reais. | 83／87 |
| bu6j | 候選只剩同列欄位清單，沒有保留「寫進」的可完成動作。 | Na mesma linha do pixel, ano, posição, 6 notas e todos os máximos. | Na mesma linha do pixel, anote ano, posição, 6 notas e todos os máximos. | 72／73 |

e826的`as 6`以陰性冠詞承接前文已明定的classes，與陽性的valores區分，沒有把六類改成六個已存值。7iv8明示的5也是已介紹的五個儲存值，沒有新增輸入。vb62的Nota沿用既定glossary＝模型分數，chances承接前後文的正確機率，a posteriori保留事後限定；沒有把分數說成已校準機率。8m2e的chance同樣承接前句chance de acerto。erqz未加句點是為保留完整判準且在現行56字元內，不刪任何語義。

## PT逐子句核對結果

除上表8處外，未發現其餘PT候選的數值錯誤、否定反轉或類別合併。具體確認：

- 第1類原生樹種保留；第2類自然恢復為主並包含恢復中的次生林，t4w3全文保留未解。第3類`floresta plantada`的栽植／播種、主要形成方式、本資料的>40年保留；第4類`plantação`的經營更密集、常見少樹種／同齡／規則間距及≤40年保留。輪伐期不是當前年齡的否定保留。`plantada`與`plantação`沒有互換或合併。
- 樹木作物與農林複合仍同屬第5類；油棕、橡膠、果園與非木材農產品在yiya全文保留未解。其他土地仍可含城市樹木或稀疏木本，沒有變成全是裸地。
- 多年衛星線索→AlphaEarth數字→ForTy形狀／季節／生長週期線索，以及專家／區域標記對應土地類型的方向未變。jkby全文保留未解，沒有只剩泛稱padrões而漏掉三種線索。
- 六類固定次序、五個儲存整數、250總量、255無資料及先排除nodata都保留；未變成六個已存band，也未拿255當有效分數。
- A依序[0,248,0,0,0]，自然更新248、其餘4類0、總和248、250−248=2OtherLand、各÷250得.992／.008、另4類0、和1、唯一最高全部保留。
- B同一block刻意挑最小最高分，beg8的非隨機估全圖精度界線全文保留未解。原始[0,86,0,1,77]，86+1+77=164，250−164=86，類2／類6同為86、÷250同為.344；類4為1→.004，類5為77→.308，類1／類3為0，數字與類名沒有錯配。
- 新問句afyy、.344+.344=.688、+.308=.996、+.004=1與另兩類0不改總和，均保留。PT小數逗號不是數值變更。ecb8保留漏項／小數及各值所對類別的檢查，不把總和1當成實地分類正確證明。
- A的121.4°E／24.7°N及B指定像素中心121.42234°E／24.69528°N完整保留，east／north方向正確。B的center只指pixel，不是10×10窗口幾何中心；10m輸出並未變成逐樹定位。
- `Nosso mapa`只指本片衍生圖；`1º máximo na ordem das classes`保留按類順序取第一個最高者。兩類並列不因單色顯示而分出勝負；未宣稱已驗證官方hard-class層的tie規則。兩像素同色仍可有不同資訊。
- 既定短稱`regeneração natural／regeneração`只指第2類；`primária`、`plantada`、`plantação`與`cultivos arbóreos`分別對應既有類1／3／4／5。`nota`只指模型score，沒有與`acurácia real`混用，99.2%不能直接當判對機率的否定保留。
- 2020基準五月公開、資料論文10月21、2017–2025年度序列是preliminar均保留。PT的`preliminar`清楚指版本狀態，無需套用ID的awal→rilis awal修法。兩個2020像素只說明此版本輸出，沒有冒充本次實測整個年度序列。
- 保留固定同位置、每年類序與六分數的比較操作，最後一列年／位置／六分數／所有最高者都在；按bu6j修法恢復明確寫入動詞。全程沒有把資料年或座標當作地面真值。
- ForTy、DeepMind、AlphaEarth及AI拼字未改，未另創型號、類名或品牌代音。

## PT預算與未解項目

對current todo逐項重算：**72項在max內；6項作者原有保全文unresolved；另1項e826因current max56而58字元過線**。不是作者宣告73項皆在current max內；採上表e826的55字元修法後，才是73項在current字數上限內。提案每列characters與Unicode字元實算一致；差異出在當前max，不是字數計法。

| PT ID | 原全文字元／current max | 保留的必要內容 |
| --- | --- | --- |
| 5ur9 | 69／41 | 本週、DeepMind介紹ForTy、從兩像素開始讀；不改成2020基準本週首發。 |
| t4w3 | 106／60 | 自然更新林、以自然長回為主、恢復中的次生林。 |
| yiya | 109／85 | 完整第5類、油棕／橡膠／果園、非木材農產品。 |
| jkby | 105／65 | ForTy使用數字、種植形狀、季節、生長週期線索。 |
| beg8 | 93／50 | 閱讀練習、不是隨機樣本估全圖精度。 |
| 4w7g | 48／19 | 詢問你通常用地圖看哪種環境；不改成製圖或刪習慣／環境。 |

這6項和ID 4w7g均正確保全文待原生整窗fit，不要求硬砍。數字／範圍／類別／否定不能為字元過線而刪除。

## 最終文字判定與適用範圍

**建議ID採6處、PT採8處修法後，使用current source／todo正常merge及整窗fit。** 分類計數：ID語義／指涉5、可讀性1；PT語義／指涉6、可讀性1、current預算1；兩語數值事實錯誤0、品牌名錯誤0、另新增字幕順序錯誤0。這些不是14個反義錯誤，多數是讓計算對象與完成動作可直接聽懂的精確化。

當前150候選已逐句覆核，所有建議新文字都實算在本次current max內；原7項unresolved保全文。未改任何譯文、todo、hash、source、音訊或metadata。metadata既有獨審修法已由root另行處理，不在此重提包裝改寫。**字數合格不等於配音fit通過；本報告未執行付費音訊或對音檢狀態作判定。**
