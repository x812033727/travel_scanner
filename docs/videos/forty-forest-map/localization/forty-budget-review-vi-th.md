# ForTy：VI／TH縮句候選獨立語義與預算複核

2026-10-25。僅寫此scratch報告，沒有修改repo、todo、source hash、音訊、速度、門檻或時槽。未建立新代理、未呼叫TTS。

**結論：不能假稱全過。** 最終合併候選50項已逐一對繁中／圖卡讀完：**45項語義可採（VI5、TH40）、TH3項需修、VI／TH各1項4w7g保留完整概念且單句指引未解。** 「語義可採」不等於配音已實際fit；新native預算另外標出超者。

## 實際凍結輸入

| 輸入 | SHA256／版本 |
| --- | --- |
| 最終合併候選forty-budget-proposals-vi-th.json | `c76dc9955e44ee98fe19a3a9fba39b4c1f5bbfc73bef6942d93eaa2a1d1d3d9f`；status=proposal_only_not_applied，VI6／TH44 |
| 最新forty-current-budget-audit.json | `c734477992e99ce18192142a8c1031298668128dd96f4c79e377c29fafde36e9`；current_native_sheet_budgets_after_actual_retake1，speech_hash=`7d55bafd91bc907f` |
| 繁中video.json | `a62a48382272fb4b9171f2c261b8f736c7516afca35417ccaa842757b04f8a6f`；92句，新afyy為問句，不在這50候選內 |
| VI原譯i18n/vi.json | `cb79f57695b8d9c51635c77eb8e5334453862db4f0196f0b4c2447edcc683abd` |
| TH原譯i18n/th.json | `62f64525c12b1222e6e30635d453c48f1f707e28002b8162ecd8d49b13b6560e` |
| 最新VI worksheet | `104f2e345acfed1c103be70a34da4943060c28b5b5678ed33b90706138e25b2f` |
| 最新TH worksheet | `bfc9eed3415b2fcbb7baa4e901e93752dd638b166dde9d64ae065b5f2ecc3ebf` |

先讀舊TH44作背景，之後確實讀到上述最終VI／TH合併檔才作本結論；沒有在檔案未落地時提前宣布完成。候選自己的meaning_check／needs_native_review欄位不是獨立通過證據。

## TH三項需修：都有保義替代，未硬刪核心概念

| ID | 候選問題 | 保義建議 | 字元／最新native指引 |
| --- | --- | --- | --- |
| 7732 | 原文「紅框**只**標出要算的一格」；候選กรอบแดงคือช่อง…僅說是該格，丟掉只標該格／不是整窗口的限定。可用แค่明說。 | **เลือก 10 คูณ 10 ช่องรอบช่องกำหนด กรอบแดงชี้แค่ช่องที่เราคำนวณ** | 61／63；保留10×10、指定格周圍、紅框只標本次算格。 |
| t4w3 | เน้นงอกเอง是「著重自己長」，不如原文的「以自然再生為主／主要」精確，改ส่วนใหญ่。 | **ป่าฟื้นตัวตามธรรมชาติส่วนใหญ่งอกเอง รวมป่าทุติยภูมิที่ฟื้นตัว** | 61／63；保留完整第2類名、主要自然長回及恢復中的次生林。 |
| e826 | จึงเติมพื้นที่อื่น把「補其他土地的**值**」縮成「填其他土地」，數值動作容易變成地面土地。補回ค่า即可。 | **5 ค่านี้ใช้ได้ จึงเติมค่าพื้นที่อื่น แล้วเทียบ 6 ประเภท** | 55／61；保留5值有效、Other的值、接著比較6類。 |

以上字元數只是native單句指引對照，不是已生成音訊或實際整窗fit保證。

## 4w7g：完整意思優先，維持未解狀態

繁中：「你常用地圖看哪種環境？」必須保留觀眾常看、使用地圖、**哪種環境**，不能改成哪個地區／棲地／哪張地圖。

| Locale | 本次最終候選 | 本輪判斷 |
| --- | --- | --- |
| VI | Hay xem môi trường gì qua bản đồ? | 語義仍有hay／môi trường／bản đồ；33字超最新28字指引。可保留候選或原全文，待outro整窗真fit，沒有為縮字刪掉環境。 |
| TH | คุณใช้แผนที่ดูสภาพแวดล้อมแบบไหนบ่อย? | 最終合併檔確實已撤短句、保留36字全文；超最新20字指引。全文問環境類型，語義正確。保留unresolved，不縮成問哪張地圖。 |

舊TH19字`ดูถิ่นไหนบนแมปบ่อย?`**不採**：ถิ่นไหน偏向哪個地方／棲地，沒有完整保留環境類型；แมป也換成較隨便的借詞。不能因它剛好19字就當完整等義。此處只拒絕這個已撤候選，不宣稱世界上不存在其他短譯法。

hr4b／4w7g／39nc共用outro視窗，單句max_chars只是精簡指引。是否可用相鄰句的自然停頓與整段讀法容納，必須由原生整窗fit實測；我沒有自行借秒、重配時槽或改語速。

## 新native預算：只標變化後仍超者／新增者

最新audit的VI仍6項、TH變43項；原TH m2p6已不超（最新worksheet max73，原譯可留），不必為舊44清單強制縮它。新audit沒有增加本候選清單以外的VI／TH over ID。

| Locale／ID | 合併候選字元 | 新max_chars | 狀態／可選處理 |
| --- | ---: | ---: | --- |
| VI 4w7g | 33 | 28 | 保留環境問句，單句未解，等outro整窗fit。 |
| TH dkq3 | 44 | 43 | 語義可採，僅多1字；不要刪「只有」或縮掉完整自然更新林類名。若要同義排版，可用`เทียบ6ค่า มีแค่ป่าฟื้นตัวตามธรรมชาติสูงสุด`（42），仍需真fit；刪空格不等於實際聲音變短。 |
| TH mx7g | 51 | 49 | 語義可採，多2字；可用`วาง2ช่องคู่กัน สีเดียวกันแต่ข้อมูลต่างกัน`（41），保留把兩格並排、同色但資訊不同；不是說兩地理像素相鄰。或保留原句交真fit，不硬刪義。 |
| TH 4w7g | 36 | 20 | 最終全文保留，單句未解，等outro整窗fit。 |

原候選其他項未新增超限；本表不把「字元指引內」改記為「已配音fit」。修正三項及下列原譯修正仍需作者正常merge與原生fit。

## 不在50縮句候選內的VI原譯問題，仍須一併處理

這兩句現在雖不在超限六句內，候選通過不能把其語義問題蓋掉。已實讀目前原譯，與root提示的問題一致：

| ID | 現譯問題 | 可用修法／字元 | 最新max |
| --- | --- | --- | ---: |
| erqz | `không có dấu hiệu con người tác động`沒有明白保留「可見」的人為干擾；不能把操作定義讀成絕無歷史干擾。 | **Rừng nguyên sinh cần cây bản địa, không thấy dấu hiệu tác động của con người.**（77）；không thấy明確保留無可見跡象。 | 82 |
| rrgq | `cây gỗ thưa`只指稀疏木本樹木，窄於木本植被，會漏灌木等範圍。 | **Đất khác có thể gồm cây đô thị hay thực vật thân gỗ thưa.**（57）；thực vật thân gỗ保留木本植被。 | 83 |

本輪沒有替另一位原譯審查者寫其結論，也沒有修改這兩句；此處只是為了避免縮句review被誤當整份VI已ready。

## 其餘語義核對與術語

- VI p2ry／3gwz保留先確認年／位置與缺的第6類補表問句；beg8保留閱讀練習、非隨機精度抽樣及整張圖範圍；ywz8保留所以／也／完整類名；vb62保留模型分數與尚未事後機率校準，沒有換成hậu nghiệm或已校準正確率。
- TH erqz的ที่เห็นได้仍明說可見，沒有刪；2vcb保留40年或以下；vk36仍區分250總量與255nodata；gfes仍先排除、不是分數。所有數字未變。
- TH既有band／補數／0到1／4類零／合1／6次獨立打分否定、A唯一最高、B刻意min(max)選樣／兩個86並列、我圖取首及不是所有分數都留下，均保留；並列未被改成唯一最高。
- TH vb62保留ภายหลัง與尚未校準否定；年份2020、五月、10/21、2017–2025早期序列及每年六分數保留。ci5j仍要求歷史／用途另對參考資料，未變成AI直接知道經營史。
- 3gwz／7iv8的หมวด與其他句的ประเภท意思均是類別，未造成ID／類名錯誤；若要統一，可分別採`ประเภท6 ที่ขาดตอนต้น เติมตารางอย่างไร?`（38／38）及`ประเภท6 อยู่ในยอดรวม ใช้ 250 ลบกลับมา`（37／40）。這是可選一致性改善，不計入三項語義需修。
- vk36若想明說「六類的值」，可用`ค่า6 ประเภทรวม 250 ส่วน 255 แยกใช้เป็นเครื่องหมายไม่มีข้อมูล`（60／64），候選原句在語境中仍可理解，未硬判事實錯誤。

## 完成與未完成

已完成：最終50候選逐項語義核對、三項需修的保義替代、新native預算delta、兩個4w7g未解狀態、VI原譯可見條件／木本範圍追蹤。下表保留全部候選對照，不只列挑出的錯誤。

未執行：套用譯文、改todo、生成或替換音訊、清flags、調整門檻、原生整窗fit。沒有把這些未做的事稱通過。

## 全部50候選逐項表

| Locale / ID | Actual zh-TW source | Frozen proposal | Meaning verdict | Candidate chars / old max / current max | Current budget note |
| --- | --- | --- | --- | --- | --- |
| vi/p2ry | 要找對這五個值，得先確認資料年份和位置。 | Để tìm đúng 5 giá trị, cần xác định năm dữ liệu và vị trí trước. | ACCEPT meaning only; not an audio-fit approval | 64 / 69 / 69 | Within current character guideline; actual native fit still needed |
| vi/3gwz | 開頭少掉的第六類，要怎麼補回這張表？ | Bổ sung loại thứ 6 thiếu ban đầu vào bảng thế nào? | ACCEPT meaning only; not an audio-fit approval | 50 / 54 / 54 | Within current character guideline; actual native fit still needed |
| vi/beg8 | 這是閱讀練習，不是拿隨機樣本估整張圖的精度。 | Bài tập đọc, không dùng mẫu ngẫu nhiên ước tính độ chính xác cả bản đồ. | ACCEPT meaning only; not an audio-fit approval | 71 / 73 / 73 | Within current character guideline; actual native fit still needed |
| vi/ywz8 | 所以它也塗成自然更新林的顏色。 | Vậy nó cũng mang màu rừng tái sinh tự nhiên. | ACCEPT meaning only; not an audio-fit approval | 44 / 50 / 52 | Within current character guideline; actual native fit still needed |
| vi/vb62 | 它是模型分數，還沒有做事後的機率校準。 | Đây là điểm mô hình, chưa hiệu chuẩn xác suất sau khi tạo điểm. | ACCEPT meaning only; not an audio-fit approval | 63 / 63 / 63 | Within current character guideline; actual native fit still needed |
| vi/4w7g | 你常用地圖看哪種環境？ | Hay xem môi trường gì qua bản đồ? | KEEP_FULL_UNRESOLVED; environment question retained; shared outro fit pending | 33 / 27 / 28 | Over single-line guideline; do not drop environment / usual maps meaning |
| th/7732 | 指定格周圍取十乘十格，紅框只標出我們要算的那一格。 | เลือก 10 คูณ 10 ช่องรอบช่องกำหนด กรอบแดงคือช่องที่เราจะคำนวณ | REVISE; see exact semantic repair above | 60 / 63 / 63 | Within current character guideline; actual native fit still needed |
| th/jw6i | 另一格同樣綠，讀出的結果也會一樣嗎？ | อีกช่องก็เขียว ผลที่อ่านได้เหมือนกันไหม? | ACCEPT meaning only; not an audio-fit approval | 40 / 43 / 47 | Within current character guideline; actual native fit still needed |
| th/5ur9 | 本週DeepMind介紹ForTy，就從這兩格讀起。 | DeepMind แนะนำ ForTy สัปดาห์นี้ อ่าน 2 ช่อง | ACCEPT meaning only; not an audio-fit approval | 43 / 45 / 43 | Within current character guideline; actual native fit still needed |
| th/m2p6 | 這個綠格要讀的不只有樹，還有它們如何長成、用來做什麼。 | ช่องเขียวไม่ได้บอกแค่ต้นไม้ แต่บอกว่าเกิดอย่างไร ใช้ทำอะไร | ACCEPT meaning only; not an audio-fit approval | 58 / 62 / 73 | Original text is already within current budget; shortening optional |
| th/erqz | 先看原始林，它要求原生樹種，沒有可見人為干擾。 | ป่าปฐมภูมิต้องมีไม้พื้นถิ่น ไม่มีรอยมนุษย์รบกวนที่เห็นได้ | ACCEPT meaning only; not an audio-fit approval | 57 / 59 / 58 | Within current character guideline; actual native fit still needed |
| th/t4w3 | 自然更新林則以自然長回來為主，也含恢復中的次生林。 | ป่าฟื้นตัวตามธรรมชาติเน้นงอกเอง รวมป่าทุติยภูมิที่ฟื้นตัว | REVISE; see exact semantic repair above | 57 / 63 / 63 | Within current character guideline; actual native fit still needed |
| th/66nz | 如果森林是人種的，又要怎麼放進這張表？ | ถ้ามนุษย์ปลูกป่า จะใส่ในตารางนี้อย่างไร? | ACCEPT meaning only; not an audio-fit approval | 40 / 45 / 44 | Within current character guideline; actual native fit still needed |
| th/2vcb | 它採用的輪伐期條件，是四十年或以下。 | เงื่อนไขรอบตัดฟันประเภทนี้คือ 40 ปีหรือต่ำกว่า | ACCEPT meaning only; not an audio-fit approval | 46 / 48 / 47 | Within current character guideline; actual native fit still needed |
| th/9wmz | AlphaEarth先把多年衛星觀測整理成一組數字。 | AlphaEarth รวมข้อมูลดาวเทียมหลายปีเป็นชุดตัวเลขก่อน | ACCEPT meaning only; not an audio-fit approval | 51 / 53 / 53 | Within current character guideline; actual native fit still needed |
| th/5nt9 | 訓練還要搭配專家與區域資料標記的地點，讓觀測線索對回土地類型。 | ฝึกด้วยจุดติดป้ายจากผู้เชี่ยวชาญและข้อมูลภูมิภาค เพื่อจับคู่เบาะแสกับประเภทที่ดิน | ACCEPT meaning only; not an audio-fit approval | 81 / 82 / 81 | Within current character guideline; actual native fit still needed |
| th/m8cb | 這個綠格的五個整數，就裝著這些類別的模型分數。 | จำนวนเต็ม 5 ค่าในช่องเขียว เก็บคะแนนโมเดลของแต่ละประเภท | ACCEPT meaning only; not an audio-fit approval | 55 / 55 / 55 | Within current character guideline; actual native fit still needed |
| th/yi97 | 十公尺網格是輸出尺度，不是每棵樹的定位清單。 | กริด 10 เมตรเป็นสเกลผลลัพธ์ ไม่ใช่พิกัดต้นไม้ทุกต้น | ACCEPT meaning only; not an audio-fit approval | 51 / 55 / 55 | Within current character guideline; actual native fit still needed |
| th/2k27 | 讀值時把固定類別名放在旁邊，數字就不會換到其他類。 | วางชื่อประเภทตามลำดับไว้ข้างค่า ตัวเลขจะได้ไม่สลับประเภท | ACCEPT meaning only; not an audio-fit approval | 56 / 59 / 59 | Within current character guideline; actual native fit still needed |
| th/vk36 | 六類的值合計兩百五十，兩百五十五另作無資料記號。 | 6 ประเภทรวม 250 ส่วน 255 แยกใช้เป็นเครื่องหมายไม่มีข้อมูล | ACCEPT meaning only; not an audio-fit approval | 57 / 64 / 64 | Within current character guideline; actual native fit still needed |
| th/gfes | 遇到無資料記號就先排除那一格，不把它當成分數。 | เจอเครื่องหมายไม่มีข้อมูล ตัดช่องออกก่อน ไม่ใช่คะแนน | ACCEPT meaning only; not an audio-fit approval | 52 / 52 / 52 | Within current character guideline; actual native fit still needed |
| th/e826 | 這一格的五個值都有效，可以補出其他土地，然後比較六類。 | 5 ค่านี้ใช้ได้ จึงเติมพื้นที่อื่น แล้วเทียบ 6 ประเภท | REVISE; see exact semantic repair above | 52 / 55 / 61 | Within current character guideline; actual native fit still needed |
| th/svhy | 欄位名稱要跟著值走，單看一串數字分不出是哪一類。 | ชื่อช่องต้องคู่ค่า ดูแค่ตัวเลขจะแยกประเภทไม่ออก | ACCEPT meaning only; not an audio-fit approval | 47 / 55 / 55 | Within current character guideline; actual native fit still needed |
| th/3gwz | 開頭少掉的第六類，要怎麼補回這張表？ | หมวด 6 ที่ขาดตอนต้น เติมตารางอย่างไร? | ACCEPT meaning only; not an audio-fit approval | 37 / 38 / 38 | Within current character guideline; actual native fit still needed |
| th/7iv8 | 第六類留在總量裡，用兩百五十扣回來。 | หมวด 6 อยู่ในยอดรวม ใช้ 250 ลบกลับมา | ACCEPT meaning only; not an audio-fit approval | 36 / 40 / 40 | Within current character guideline; actual native fit still needed |
| th/8hpb | 這些儲存值，要怎麼換成零到一的模型分數？ | เปลี่ยนค่าที่เก็บเป็นคะแนนโมเดลช่วง 0 ถึง 1 อย่างไร? | ACCEPT meaning only; not an audio-fit approval | 52 / 56 / 56 | Within current character guideline; actual native fit still needed |
| th/eym7 | 其餘四類的儲存值是零，換成分數也都是零。 | อีก 4 ประเภทเก็บ 0 แปลงเป็นคะแนนก็ยังเป็น 0 ทั้งหมด | ACCEPT meaning only; not an audio-fit approval | 51 / 52 / 52 | Within current character guideline; actual native fit still needed |
| th/k3i2 | 把六項分數加起來，剛好是一。 | รวมทั้ง 6 คะแนน ได้ 1 พอดี | ACCEPT meaning only; not an audio-fit approval | 26 / 35 / 35 | Within current character guideline; actual native fit still needed |
| th/p9sg | 這是同一個總量的拆分，不是六次互不相關的打分。 | แบ่งจากยอดรวมเดียว ไม่ใช่ให้คะแนน 6 ครั้งแบบไม่เกี่ยวกัน | ACCEPT meaning only; not an audio-fit approval | 56 / 58 / 58 | Within current character guideline; actual native fit still needed |
| th/dkq3 | 比較這六項，只有自然更新林最高。 | เทียบ 6 ค่า มีแค่ป่าฟื้นตัวตามธรรมชาติสูงสุด | ACCEPT meaning only; not an audio-fit approval | 44 / 44 / 43 | Still over by 1; see no-meaning-loss alternatives above |
| th/w86h | 選最大值來畫分類，紅框格就呈現它的綠色。 | เลือกค่าสูงสุดวาดประเภท ช่องกรอบแดงจึงเป็นสีเขียว | ACCEPT meaning only; not an audio-fit approval | 49 / 53 / 53 | Within current character guideline; actual native fit still needed |
| th/wh49 | 這個動作叫取最大值，選的是類別，不會留下所有分數。 | นี่เรียกว่าเลือกค่าสูงสุด เลือกประเภท ไม่เก็บคะแนนทั้งหมดไว้ | ACCEPT meaning only; not an audio-fit approval | 60 / 62 / 62 | Within current character guideline; actual native fit still needed |
| th/xxju | 只看綠格能讀類名，展開數值才知道這格的分布。 | ช่องเขียวบอกแค่ชื่อประเภท เปิดค่าจึงเห็นการกระจายของช่องนี้ | ACCEPT meaning only; not an audio-fit approval | 59 / 61 / 61 | Within current character guideline; actual native fit still needed |
| th/appe | 換到同一區塊的另一格，這次刻意挑最高分最低的位置。 | อีกช่องในบล็อกเดิม จงใจเลือกจุดที่คะแนนสูงสุดต่ำสุด | ACCEPT meaning only; not an audio-fit approval | 51 / 62 / 65 | Within current character guideline; actual native fit still needed |
| th/beg8 | 這是閱讀練習，不是拿隨機樣本估整張圖的精度。 | ฝึกอ่าน ไม่ใช่สุ่มตัวอย่างวัดความแม่นยำทั้งแผนที่ | ACCEPT meaning only; not an audio-fit approval | 49 / 52 / 52 | Within current character guideline; actual native fit still needed |
| th/97h6 | 自然更新林和其他土地同為八十六，這次有兩項並列最高。 | ป่าฟื้นตัวตามธรรมชาติกับพื้นที่อื่นได้ 86 เท่ากัน มี 2 ประเภทสูงสุดร่วม | ACCEPT meaning only; not an audio-fit approval | 71 / 71 / 72 | Within current character guideline; actual native fit still needed |
| th/wnrz | 我們這張衍生圖，用類別順序取第一個最高者。 | ภาพดัดแปลงของเรา เลือกตัวแรกที่สูงสุดตามลำดับประเภท | ACCEPT meaning only; not an audio-fit approval | 51 / 52 / 52 | Within current character guideline; actual native fit still needed |
| th/ywz8 | 所以它也塗成自然更新林的顏色。 | จึงใช้สีป่าฟื้นตัวตามธรรมชาติเช่นกัน | ACCEPT meaning only; not an audio-fit approval | 36 / 36 / 37 | Within current character guideline; actual native fit still needed |
| th/ww8v | 還記得開頭那個綠格嗎，它的最高者只有一個。 | จำช่องเขียวแรกได้ไหม? สูงสุดมี 1 ประเภท | ACCEPT meaning only; not an audio-fit approval | 39 / 41 / 40 | Within current character guideline; actual native fit still needed |
| th/mx7g | 把兩格擺在一起，同樣的顏色就不再是同樣的資訊。 | วาง 2 ช่องคู่กัน สีเดียวกันไม่ได้ให้ข้อมูลเหมือนกัน | ACCEPT meaning only; not an audio-fit approval | 51 / 53 / 49 | Still over by 2; see no-meaning-loss alternatives above |
| th/vb62 | 它是模型分數，還沒有做事後的機率校準。 | คะแนนโมเดลยังไม่ปรับเทียบความน่าจะเป็นภายหลัง | ACCEPT meaning only; not an audio-fit approval | 45 / 45 / 45 | Within current character guideline; actual native fit still needed |
| th/ci5j | 模型看見的是觀測線索，土地歷史和經營用途還要對照參考資料。 | โมเดลเห็นเบาะแส ประวัติที่ดินกับการใช้ประโยชน์ยังต้องเทียบข้อมูลอ้างอิง | ACCEPT meaning only; not an audio-fit approval | 71 / 71 / 71 | Within current character guideline; actual native fit still needed |
| th/6ss6 | 分數讀清楚後，再替同一列紀錄保留位置和資料年。 | อ่านคะแนนแล้ว เก็บตำแหน่งและปีข้อมูลในบันทึกแถวเดียวกัน | ACCEPT meaning only; not an audio-fit approval | 55 / 60 / 60 | Within current character guideline; actual native fit still needed |
| th/rume | 二〇二〇基準資料在五月公開，描述的是那一年的土地狀態。 | ข้อมูลฐานปี 2020 เผยแพร่เดือนพฤษภาคม บอกสภาพที่ดินปีนั้น | ACCEPT meaning only; not an audio-fit approval | 56 / 62 / 62 | Within current character guideline; actual native fit still needed |
| th/pvkj | 正式資料論文在十月二十一日出版。 | บทความข้อมูลทางการตีพิมพ์วันที่ 21 ตุลาคม | ACCEPT meaning only; not an audio-fit approval | 41 / 43 / 43 | Within current character guideline; actual native fit still needed |
| th/ncx4 | 那次介紹也分享二〇一七到二〇二五年的早期年度序列。 | ครั้งนั้นยังแชร์ชุดรายปีเบื้องต้น ตั้งแต่ 2017 ถึง 2025 | ACCEPT meaning only; not an audio-fit approval | 55 / 63 / 63 | Within current character guideline; actual native fit still needed |
| th/nqyj | 要比較同一處，先固定位置，再保留每年的類別順序和六分數。 | เทียบที่เดิม ตรึงตำแหน่ง เก็บลำดับประเภทกับทั้ง 6 คะแนนของทุกปี | ACCEPT meaning only; not an audio-fit approval | 63 / 72 / 72 | Within current character guideline; actual native fit still needed |
| th/wfb2 | 只換顏色，會把剛才看到的並列和分數差距藏起來。 | เปลี่ยนแค่สีจะซ่อนผลเสมอและส่วนต่างคะแนนที่เพิ่งเห็น | ACCEPT meaning only; not an audio-fit approval | 52 / 59 / 58 | Within current character guideline; actual native fit still needed |
| th/hr4b | 這一列紀錄，就保住了單一綠色省略的資訊。 | บันทึกแถวนี้เก็บข้อมูลที่สีเขียวสีเดียวละไว้ | ACCEPT meaning only; not an audio-fit approval | 44 / 46 / 46 | Within current character guideline; actual native fit still needed |
| th/4w7g | 你常用地圖看哪種環境？ | คุณใช้แผนที่ดูสภาพแวดล้อมแบบไหนบ่อย? | KEEP_FULL_UNRESOLVED; environment question retained; shared outro fit pending | 36 / 19 / 20 | Over single-line guideline; do not drop environment / usual maps meaning |

Table totals: 45 meaning-acceptable, 3 requiring semantic repair, 2 environment questions retained with unresolved single-line guideline. This is not a claim that all50 native dubs fit.

## 追加：root套用後兩句w86h小差異，未重審50項

本追加保留原報告與原輸入結論；追加前本報告SHA256為`de7c4d1ed33b1692c6908f03d16413aa41fb05ff6059fd23bc937bc13bac6e81`。新套用收據forty-vi-th-budget-application.json SHA為`5089e7bde7e9df0678dabb31801c2847a94c0c633f8c49fe5c37dc855bded658`。

實際新VI i18n SHA：`75b086679c0d2d7af263f6653fba1a27707b6a497b59d20fe9dcd636b1f5603d`；新TH i18n SHA：`8ab3f177fa284f1ad73a03fc0ff915742d83cde27dc0777c8391d0bf94c65ced`。沒有拿原檔SHA綁新譯文。

| Locale／ID | 實際新句 | 小差異判讀與建議 |
| --- | --- | --- |
| VI w86h | Tô màu theo loại điểm cao nhất; ô khung đỏ mang màu xanh của loại đó.（實數69／74） | 最高類別著色、紅框格綠色及該類歸屬都保留；但loại điểm高分種類的黏接不自然，宜補có，明確是「具有最高分的類別」。建議**Tô màu theo loại có điểm cao nhất; ô khung đỏ mang màu xanh của loại đó.**（72／74）。 |
| TH w86h | ลงสีตามประเภทค่าสูงสุด ช่องกรอบแดงจึงเป็นสีเขียว（實數48／53） | 核心可理解且數學不變；更自然明確可說**ลงสีตามประเภทที่มีค่าสูงสุด ช่องกรอบแดงจึงเขียว**（47／53），用ที่มี表達類別具有最高值。ช่อง仍指紅框內格，沒有把紅框線本身變綠。 |

兩候選保持最高值的類別、著色與紅框格轉綠。VI補có是建議修法；TH為自然度改善。沒有稱以上字符數即證明native fit。root另外採用的erqz／rrgq及先前三Thai修正仍依其原收據，本追加不重審50項，也不替新合併後整份VI／TH或音訊判全過。
