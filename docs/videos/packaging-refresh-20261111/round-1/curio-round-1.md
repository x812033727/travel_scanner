# 奇聞檔案局：重新包裝第一輪（10 支，2026-11-18）

看板票 `2026-11-17-curio-repackaging-round-1-top-10`。規則照 [`../README.md`](../README.md) 第二到五節，以及 `curio-episode` skill 的〈標題與縮圖〉。
上一輪（看板票 `2026-11-11-redo-thumbnails-and-titles-for-curio`）已經做了 s01〈赤壁〉和 s11〈長篠〉，這一輪不重做，因為 14 天內同一支影片不改第二次。

## 為什麼是這 10 支、順序怎麼排

- 範圍：已上架的奇聞歷史迷思（S 軸），扣掉 s01、s11，剩下剛好 10 支。
- 第 1 名是 s04〈周瑜〉，因為它的自然曝光和點閱率是已知的：4,530 次、0.55%（`channel-review-20261111-promotion` §4）。
- 其餘 9 支沒有自然數字：這個 session 沒有站台權杖，讀不到原始報表。只好用 2026-11-17 的公開觀看數排序，**公開觀看大多是付費宣傳買的**，只能當成「YouTube 推過多少」的粗略參考。
- 換上去之前，站主在 Studio 每支影片的「觸及」分頁抄下近 28 天的自然曝光和點閱率，填進表格的「換前」欄。

## 現行包裝的共同問題

1. **現行英文標題把答案講掉了**，看了就不必點：
   - s18〈Autopsy Says 168 cm〉
   - s03〈the One Fooled Was Zhang He〉
   - s06〈The Novel Is Off by at Least 11 Years〉
   - s29〈Sun Quan Had None Till 210〉
2. **縮圖大字的第一行沒有大家認得的名字**：「借箭的／不是他？」「那天他／不在？」「沒有／繞路」「被畫／小了」。
3. 縮圖副標寫「二二八年的檔案」「永祿三年的檔案」這種年份標籤，不是一個讓人想點的事實。

## 新標題與縮圖

每支兩個標題（A 是推薦）、兩組縮圖（layout e：左邊深藍字區、右邊放圖，字不壓圖）。
`headline` 第一行放大家認得的名字，第二行用 `**…？**` 寫反轉，每行最多 6 字；`sub` 補一個硬事實，**不寫答案**。
事實欄是每個用到的事實的出處：題庫是 `docs/videos/history-curiosity/topics.json` 的 finding，有 `claims.md` 的集數另外標上。

| # | 影片 | 新標題（後綴「｜奇聞檔案局」） | 縮圖 A | 縮圖 B | 事實出處 |
| ---: | --- | --- | --- | --- | --- |
| 1 | s04 周瑜 `mYry4W8dqWc` | **A** 周瑜真的被諸葛亮氣死？36 歲那年史書只寫了一句<br>B「既生瑜，何生亮」是周瑜說的？老將程普說的完全不同 | `周瑜\n**氣死的？**`／sub「死時才 36 歲」／底圖：周瑜吐血或怒目的特寫 | `三氣周瑜\n**真的嗎？**`／sub「老將說：像喝醇酒」／底圖：周瑜與諸葛亮對峙 | topics S04：病逝年三十六；程普「若飲醇醪」；「三氣」「既生瑜」是演義 |
| 2 | s18 拿破崙 `rbA2JR7bIrc` | **A** 拿破崙只有 157 公分？一個換錯的單位騙了兩百年<br>B 拿破崙真的很矮？英國漫畫家畫了他兩百年 | `拿破崙\n**很矮？**`／sub「5 呎 2 吋，哪國的吋？」／底圖：拿破崙站在高個子近衛軍中間 | `矮子皇帝\n**誰畫的？**`／sub「一位英國漫畫家」／底圖：諷刺畫風的小拿破崙 | claims np204–np208（168–169 公分；誤當英制讀成 157 公分，「157 是假設的讀法」）；topics S18：吉爾雷 |
| 3 | s08 木牛流馬 `IvogKaRemk8` | **A** 諸葛亮的木牛流馬會自己走？1800 年沒人造得出來<br>B 木牛流馬長什麼樣？史書寫了尺寸卻沒有圖 | `木牛流馬\n**會走？**`／sub「史書只留下尺寸」／底圖：木造機械牛特寫 | `諸葛亮\n**造了什麼？**`／sub「1800 年沒有定論」／底圖：諸葛亮看著設計圖 | topics S08：裴注留尺寸但難解；多種復原，沒有定論 |
| 4 | s09 桶狹間 `S-HraLI6z2g` | **A** 織田信長 2000 打 25000，真的是繞到背後偷襲？<br>B 桶狹間的大雨那天，信長走的是哪一條路？ | `織田信長\n**繞路了？**`／sub「1560 年，一場大雨」／底圖：雨中衝鋒的信長特寫 | `桶狹間\n**怎麼贏的？**`／sub「2000 對 25000」／底圖：今川本陣與雨幕 | topics S09：1560 年；繞路說出自《信長記》，《信長公記》寫冒雨直衝；兵力各書不同 |
| 5 | s06 刮骨療毒 `685u6uO2uZ8` | **A** 關羽刮骨療毒是真的，那醫生是華佗嗎？<br>B 關羽一邊刮骨一邊喝酒，正史裡的醫生叫什麼？ | `關羽\n**刮骨是真的？**`／sub「邊刮邊喝酒吃肉」／底圖：關羽伸臂、面不改色 | `那個醫生\n**是誰？**`／sub「正史只寫兩個字」／底圖：醫生拿刀的手與關羽的臂 | topics S06：正史記刮骨、飲食言笑自若；正史沒寫醫生名字；s06 舊縮圖副標「正史只寫了兩個字：醫曰」 |
| 6 | s03 空城計 `cVGdU7yabfc` | **A** 諸葛亮唱空城計，司馬懿那天真的在城下？<br>B 空城計是真的嗎？西元 228 年城門外站的是誰 | `空城計\n**真的嗎？**`／sub「城門大開，一人彈琴」／底圖：城樓彈琴的諸葛亮 | `司馬懿\n**在哪裡？**`／sub「西元 228 年」／底圖：城下勒馬遲疑的大軍 | topics S03：裴松之駁斥；司馬懿駐宛城；s03 舊副標「二二八年」 |
| 7 | s29 曹沖稱象 `R44IsmWR3V0` | **A** 曹沖稱象是真的嗎？一部北魏佛經裡有幾乎一樣的故事<br>B 曹沖怎麼秤大象？當時的北方有大象嗎 | `曹沖稱象\n**抄來的？**`／sub「佛經裡也有這個故事」／底圖：船身刻線與大象 | `那頭大象\n**哪來的？**`／sub「北方有象嗎？」／底圖：大象站在船上 | topics S29：陳寅恪指出《雜寶藏經》有類似故事，並質疑北方是否有象；是否借用仍有討論 |
| 8 | s05 三顧茅廬 `MVpNgwdSZMY` | **A** 劉備三顧茅廬，還是諸葛亮自己上門？兩本書寫反了<br>B 三顧茅廬是誰找誰？諸葛亮自己的文章這樣寫 | `三顧茅廬\n**誰找誰？**`／sub「兩本史書寫反了」／底圖：茅廬門口劉備與諸葛亮對看 | `諸葛亮\n**自己上門？**`／sub「出師表：三顧臣於草廬」／底圖：諸葛亮走在去見劉備的路上 | topics S05：〈出師表〉寫三顧；《魏略》《九州春秋》說諸葛亮北行求見 |
| 9 | s02 草船借箭 `WOYPoicmnJU` | **A** 草船借箭的不是諸葛亮？那艘差點被射翻的船上是誰<br>B 草船借箭真的發生過？主角換人了 | `草船借箭\n**另有其人？**`／sub「一艘被射到快翻的船」／底圖：插滿箭、傾斜的大船 | `諸葛亮\n**沒借箭？**`／sub「建安十八年，濡須口」／底圖：船上看不清臉的主帥背影 | topics S02：《魏略》建安十八年濡須之戰，船一側中箭快翻覆；演義移到赤壁、換成諸葛亮 |
| 10 | s17 杜鵑俳句 `9PFjkI2Zib4` | **A**「杜鵑不啼就殺了它」是織田信長說的？<br>B 信長、秀吉、家康的杜鵑俳句，是誰寫的？ | `織田信長\n**說過嗎？**`／sub「不啼的杜鵑就殺了」／底圖：信長冷眼看著籠中杜鵑 | `三首俳句\n**誰寫的？**`／sub「信長、秀吉、家康」／底圖：三英傑並排，杜鵑在中間 | topics S17：三首見於江戶後期《甲子夜話》，是後人的評語 |

- 所有中文標題在後綴前都不超過 30 字。
- 縮圖 A、B 的 `sub` 都不講答案：例如 s18 只問「哪國的吋？」，不寫 168 公分。
- s06 縮圖 A 的第二行「刮骨是真的？」6 個字，到上限了，畫的時候注意 `fitText` 縮字後要看得清楚。

## 八語標題（標題 A）

照 [`../README.md`](../README.md) 第四節：同一套公式翻，不逐字翻。保留系列後綴，字幕標記由工具加在最後。

| # | en | ja | ko |
| ---: | --- | --- | --- |
| 1 | Did Zhuge Liang Really Anger Zhou Yu to Death at 36?｜Curio Archive | 周瑜は本当に諸葛亮に憤死させられた？36歳の記録｜奇聞ファイル局 | 주유는 정말 제갈량 때문에 화병으로 죽었나? 36세의 기록｜기문파일국 |
| 2 | Was Napoleon Only 157 cm? One Mixed-Up Unit, 200 Years｜Curio Archive | ナポレオンは157cmだった？200年続いた単位の取り違え｜奇聞ファイル局 | 나폴레옹은 157cm였나? 200년을 속인 단위 하나｜기문파일국 |
| 3 | Did Zhuge Liang's Wooden Ox Walk by Itself? 1,800 Years, No Rebuild｜Curio Archive | 諸葛亮の木牛流馬はひとりで歩いた？1800年誰も再現できず｜奇聞ファイル局 | 제갈량의 목우유마는 혼자 걸었나? 1800년 동안 아무도 못 만들었다｜기문파일국 |
| 4 | Oda Nobunaga, 2,000 vs 25,000: Did He Really Take the Back Route?｜Curio Archive | 織田信長2000対25000、本当に迂回奇襲だった？｜奇聞ファイル局 | 오다 노부나가 2,000 대 25,000, 정말 우회 기습이었나?｜기문파일국 |
| 5 | Guan Yu's Bone Scraping Was Real. Was the Doctor Hua Tuo?｜Curio Archive | 関羽の骨削りは史実、では医者は華佗？｜奇聞ファイル局 | 관우의 뼈 긁기는 사실, 그럼 의사는 화타였나?｜기문파일국 |
| 6 | Zhuge Liang's Empty Fort: Was Sima Yi Even Outside the Gate?｜Curio Archive | 諸葛亮の空城計、司馬懿は本当に城の前にいた？｜奇聞ファイル局 | 제갈량의 공성계, 사마의는 정말 성문 앞에 있었나?｜기문파일국 |
| 7 | Cao Chong Weighing the Elephant: Is It Real? A Buddhist Sutra Tells It Too｜Curio Archive | 曹沖が象を量った話は本当？仏典にもほぼ同じ物語が｜奇聞ファイル局 | 조충의 코끼리 무게 재기는 사실? 불경에도 거의 같은 이야기가｜기문파일국 |
| 8 | Liu Bei's Three Visits, or Did Zhuge Liang Come to Him? Two Books Disagree｜Curio Archive | 三顧の礼か、諸葛亮が自ら訪ねたのか？二つの書が逆を記す｜奇聞ファイル局 | 삼고초려인가, 제갈량이 직접 찾아갔나? 두 책이 반대로 썼다｜기문파일국 |
| 9 | Straw Boats Borrowing Arrows: Not Zhuge Liang? Who Was on That Ship?｜Curio Archive | 草船借箭は諸葛亮じゃない？転覆しかけた船に乗っていたのは｜奇聞ファイル局 | 초선차전은 제갈량이 아니었다? 뒤집힐 뻔한 배에 탄 사람은｜기문파일국 |
| 10 | "If the Cuckoo Won't Sing, Kill It": Did Oda Nobunaga Say That?｜Curio Archive | 「鳴かぬなら殺してしまえ」は織田信長の言葉？｜奇聞ファイル局 | "울지 않는 두견새는 죽여라"는 오다 노부나가가 한 말일까?｜기문파일국 |

| # | es | pt | id | vi | th |
| ---: | --- | --- | --- | --- | --- |
| 1 | ¿Zhuge Liang mató de rabia a Zhou Yu a los 36?｜Archivo Curioso | Zhuge Liang matou Zhou Yu de raiva aos 36?｜Arquivo Curioso | Benarkah Zhou Yu Mati karena Dibuat Marah Zhuge Liang di Usia 36?｜Arsip Kisah Unik | Chu Du thật sự bị Gia Cát Lượng chọc tức đến chết năm 36 tuổi?｜Hồ Sơ Kỳ Bí | โจวอวี๋ถูกขงเบ้งยั่วจนตายจริงหรือ? บันทึกตอนอายุ 36｜แฟ้มลับเรื่องแปลก |
| 2 | ¿Napoleón medía solo 157 cm? Una unidad confundida durante 200 años｜Archivo Curioso | Napoleão tinha só 157 cm? Uma unidade trocada por 200 anos｜Arquivo Curioso | Napoleon Cuma 157 cm? Satu Satuan Keliru Selama 200 Tahun｜Arsip Kisah Unik | Napoléon chỉ cao 157 cm? Một đơn vị đổi nhầm suốt 200 năm｜Hồ Sơ Kỳ Bí | นโปเลียนสูงแค่ 157 ซม.? หน่วยวัดที่สับสนมา 200 ปี｜แฟ้มลับเรื่องแปลก |
| 3 | ¿El buey de madera de Zhuge Liang caminaba solo? 1800 años sin réplica｜Archivo Curioso | O boi de madeira de Zhuge Liang andava sozinho? 1800 anos sem réplica｜Arquivo Curioso | Lembu Kayu Zhuge Liang Bisa Jalan Sendiri? 1.800 Tahun Tak Ada yang Bisa Membuat｜Arsip Kisah Unik | Trâu gỗ ngựa máy của Gia Cát Lượng tự đi được? 1800 năm chưa ai làm lại｜Hồ Sơ Kỳ Bí | วัวไม้ม้าเลื่อนของขงเบ้งเดินเองได้? 1800 ปีไม่มีใครสร้างได้｜แฟ้มลับเรื่องแปลก |
| 4 | Oda Nobunaga, 2000 contra 25 000: ¿de verdad atacó por la retaguardia?｜Archivo Curioso | Oda Nobunaga, 2 mil contra 25 mil: atacou mesmo pela retaguarda?｜Arquivo Curioso | Oda Nobunaga, 2.000 Lawan 25.000: Benarkah Menyerang dari Belakang?｜Arsip Kisah Unik | Oda Nobunaga 2.000 đánh 25.000: thật sự đi vòng đánh úp?｜Hồ Sơ Kỳ Bí | โอดะ โนบุนากะ 2,000 ต่อ 25,000 อ้อมไปตีด้านหลังจริงหรือ?｜แฟ้มลับเรื่องแปลก |
| 5 | El raspado de hueso de Guan Yu fue real. ¿El médico era Hua Tuo?｜Archivo Curioso | A raspagem do osso de Guan Yu foi real. O médico era Hua Tuo?｜Arquivo Curioso | Kisah Guan Yu Dikerik Tulangnya Itu Nyata, Tapi Apakah Dokternya Hua Tuo?｜Arsip Kisah Unik | Quan Vũ cạo xương chữa độc là thật, nhưng thầy thuốc có phải Hoa Đà?｜Hồ Sơ Kỳ Bí | กวนอูขูดกระดูกรักษาพิษเป็นเรื่องจริง แต่หมอคือฮัวโต๋หรือ?｜แฟ้มลับเรื่องแปลก |
| 6 | La ciudad vacía de Zhuge Liang: ¿estaba Sima Yi ante la puerta?｜Archivo Curioso | A cidade vazia de Zhuge Liang: Sima Yi estava mesmo diante do portão?｜Arquivo Curioso | Siasat Kota Kosong Zhuge Liang: Benarkah Sima Yi Ada di Depan Gerbang?｜Arsip Kisah Unik | Không thành kế của Gia Cát Lượng: Tư Mã Ý có thật ở dưới thành?｜Hồ Sơ Kỳ Bí | กลเมืองว่างของขงเบ้ง สุมาอี้อยู่หน้าประตูเมืองจริงหรือ?｜แฟ้มลับเรื่องแปลก |
| 7 | ¿Cao Chong pesó un elefante? Un sutra budista cuenta casi lo mismo｜Archivo Curioso | Cao Chong pesou um elefante? Um sutra budista conta quase o mesmo｜Arquivo Curioso | Benarkah Cao Chong Menimbang Gajah? Sutra Buddha Punya Kisah yang Mirip｜Arsip Kisah Unik | Tào Xung cân voi là thật? Một bộ kinh Phật có câu chuyện gần như y hệt｜Hồ Sơ Kỳ Bí | โจชงชั่งช้างจริงหรือ? คัมภีร์พุทธก็มีเรื่องแทบเหมือนกัน｜แฟ้มลับเรื่องแปลก |
| 8 | ¿Las tres visitas de Liu Bei o Zhuge Liang fue a buscarlo? Dos libros se contradicen｜Archivo Curioso | As três visitas de Liu Bei ou Zhuge Liang foi até ele? Dois livros discordam｜Arquivo Curioso | Liu Bei Datang Tiga Kali, atau Zhuge Liang yang Datang Sendiri? Dua Kitab Bertolak Belakang｜Arsip Kisah Unik | Lưu Bị ba lần đến lều cỏ, hay Gia Cát Lượng tự tìm đến? Hai cuốn sách viết ngược nhau｜Hồ Sơ Kỳ Bí | เล่าปี่ไปเยือนสามครั้ง หรือขงเบ้งไปหาเอง? หนังสือสองเล่มเขียนกลับกัน｜แฟ้มลับเรื่องแปลก |
| 9 | ¿Las flechas con barcos de paja no fueron de Zhuge Liang? ¿Quién iba en ese barco?｜Archivo Curioso | As flechas dos barcos de palha não foram de Zhuge Liang? Quem estava no barco?｜Arquivo Curioso | Pinjam Panah dengan Perahu Jerami Bukan Zhuge Liang? Siapa di Kapal yang Hampir Terbalik Itu?｜Arsip Kisah Unik | Thuyền cỏ mượn tên không phải Gia Cát Lượng? Ai đứng trên con thuyền suýt lật?｜Hồ Sơ Kỳ Bí | ยืมเกาทัณฑ์ด้วยเรือฟางไม่ใช่ขงเบ้ง? ใครอยู่บนเรือที่เกือบล่ม｜แฟ้มลับเรื่องแปลก |
| 10 | «Si el cuco no canta, mátalo»: ¿lo dijo Oda Nobunaga?｜Archivo Curioso | "Se o cuco não canta, mate-o": Oda Nobunaga disse isso?｜Arquivo Curioso | "Kalau Burung Kukuk Tak Berkicau, Bunuh Saja": Benarkah Oda Nobunaga yang Bilang?｜Arsip Kisah Unik | "Chim cu không hót thì giết": Oda Nobunaga có từng nói vậy?｜Hồ Sơ Kỳ Bí | "นกคุกคูไม่ร้องก็ฆ่าเสีย" โอดะ โนบุนากะพูดจริงหรือ?｜แฟ้มลับเรื่องแปลก |

> **八語標題是代理翻的，還沒有經過逐語審。** 上架前照 `article-localization` 的逐語審方式，每個語言請另一個代理讀一次，尤其是 es、pt、id、vi、th 裡的三國人名（照各地慣用譯名），以及加上字幕標記後的總長（不超過 100 字元）。

## 縮圖成品：還沒畫

- 各集的成片在雲端硬碟 `curio-rebrand-<slug>/out/final.mp4`，每支約 160 MB。這個雲端 session 沒辦法把影片下載下來截圖，所以**這一輪只交規格**。
- 畫的方法照上一輪 [`../../curio-s01/thumbnail-redo-20261111.md`](../../curio-s01/thumbnail-redo-20261111.md)：
  1. 從成片截出上表寫的底圖畫面，裁掉燒進去的字幕和右上角浮水印。
  2. 用 `tools/video/templates/templates.mjs` 的 `thumbnailHtml`（layout e）加 `tools/video/render/browser.mjs` 的 `openRenderer`，畫出 1280×720 的圖。
  3. 每個語言各一張，放到雲端硬碟該集的 `thumbnails-redo-20261118/`。圖不進 repo。
- 誰來畫：在能讀雲端硬碟成片的環境，例如站主的電腦或掛著 Drive 同步的工作階段，用這份規格畫。

## 量成效（之後回填）

| # | 影片 | 換前 28 天自然曝光／點閱率 | 換上日期 | 換後 14 天自然曝光／點閱率 | Studio 勝出組 |
| ---: | --- | --- | --- | --- | --- |
| 1 | s04 周瑜 | 4,530／0.55%（10/04–11/07） | | | |
| 2 | s18 拿破崙 | | | | |
| 3 | s08 木牛流馬 | | | | |
| 4 | s09 桶狹間 | | | | |
| 5 | s06 刮骨療毒 | | | | |
| 6 | s03 空城計 | | | | |
| 7 | s29 曹沖稱象 | | | | |
| 8 | s05 三顧茅廬 | | | | |
| 9 | s02 草船借箭 | | | | |
| 10 | s17 杜鵑俳句 | | | | |

## 站主要做的

1. 縮圖畫好之後，在桌機版 Studio 每支影片打開「測試與比較」，放現行縮圖加 A、B（最多三組；也可以選標題加縮圖的組合）。
2. 一次最多換 3–4 支，跑 10–14 天，看 YouTube 判定的勝出組（依觀看時間占比，不看點閱率）。這樣如果效果不好，還有其他支當對照。
3. 告訴我換上去的日期，我記進 [`../../channel-changes/README.md`](../../channel-changes/README.md)，第 14 天回來對答案。
4. 換標題只能在 Studio 做，或由站主明確同意後，用主機的 `video-youtube-caption-titles --set-title` 批次改（[`../README.md`](../README.md) 第三節）。
