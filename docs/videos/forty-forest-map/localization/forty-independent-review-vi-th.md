# ForTy VI／TH 獨立字幕與metadata審稿

我是這兩語的獨立審稿者，未撰寫VI／TH翻譯。依 `caption-review.md` 逐句對照當前繁中source、slides與claims，讀取lexicon相關條目、worksheet的glossary／boundaries及目前repo版兩語metadata。沒有讀取作者的自評或44句泰文縮短提案，也沒有改repo、todo、音訊或執行merge／TTS。

## 實讀版本與覆蓋

| 檔案 | SHA-256 | 實際覆蓋 |
| --- | --- | --- |
| video.json | `a62a48382272fb4b9171f2c261b8f736c7516afca35417ccaa842757b04f8a6f` | 92句source、相關slides及全部metadata |
| i18n/vi.json | `cb79f57695b8d9c51635c77eb8e5334453862db4f0196f0b4c2447edcc683abd` | 92／92句＋全部metadata |
| i18n/th.json | `62f64525c12b1222e6e30635d453c48f1f707e28002b8162ecd8d49b13b6560e` | 92／92句＋全部metadata；先讀91句，後補讀新增afyy |

泰文初次快照SHA為 `1db72e232211850e5f504ab3fb81920ae955c36d8b4f2409f12b9c269fa985fb`，當時只有91句，確實缺afyy。root正常native merge後，我補讀目前 `[afyy]`：ก่อนบันทึกช่องที่ 2 ทั้ง 6 คะแนนนี้จะบวกกลับเป็น 1 ไหม?。比對確認舊91句及metadata沒有其他改動，才將本報告覆蓋更新為92／92；沒有把先前缺句當作已審。最後本地核對時三份SHA仍與上表相同。

目前 `[afyy]` 保留記錄第二格前、這6分數、加回1及疑問語氣；與其後0.688→0.996→1的三步直接回收一致，沒有遺漏算步。VI同句也已是對應的新問句。

## 修正清單

語義修正列在前；其餘為具體的自然用語／metadata精確化建議，不是新增事實。下表不含只有總字數較長、尚無實測cue或硬budget依據的句子。建議文字保留原數字、類名、條件與否定。

### VI

| ID／欄位 | 類型與問題 | current | suggested |
| --- | --- | --- | --- |
| erqz | meaning：原文限定為沒有「可見」人為干擾；現文không có dấu hiệu未把可見性明說。用không thấy保留觀察範圍，避免讀成完全沒有任何人為影響證據。 | Rừng nguyên sinh cần cây bản địa và không có dấu hiệu con người tác động. | Rừng nguyên sinh cần cây bản địa và không thấy dấu hiệu con người tác động. |
| rrgq | meaning：cây gỗ通常指喬木／木材樹；原文稀疏木本也涵蓋其他木本植被。應保留較廣的woody vegetation範圍。 | Đất khác còn lại có thể gồm cây đô thị hoặc cây gỗ thưa. | Đất khác còn lại có thể gồm cây đô thị hoặc thảm thực vật thân gỗ thưa. |
| w86h | readability：vẽ loại是「畫類別」的直譯，地圖語境宜說按最高值的類別著色。 | Chọn giá trị lớn nhất để vẽ loại, ô khung đỏ sẽ mang màu xanh của loại đó. | Tô màu theo loại có giá trị lớn nhất; ô khung đỏ sẽ có màu xanh của loại đó. |
| 6ybg | readability：cao nhất duy nhất語序生硬；改用chỉ明說只有這一類最高，保留完整6分數。 | Vì thế ghi rừng tái sinh tự nhiên cao nhất duy nhất, kèm đủ 6 điểm. | Vì thế, ghi: chỉ rừng tái sinh tự nhiên đạt điểm cao nhất; kèm đủ 6 điểm. |
| upmh | readability：tách A với B不適合這裡的概念辨別，宜用phân biệt；不能把分數與正確率當可直接互換的兩種表示。 | Muốn dùng điểm, trước hết phải tách điểm mô hình với tỷ lệ đúng thực tế. | Trước khi dùng điểm, cần phân biệt điểm mô hình với tỷ lệ đúng thực tế. |
| title | metadata：tính 6 loại像在計算類別本身；加入điểm，具體表達本片計算六類分數，也更自然。 | Bản đồ rừng Google ForTy: tính 6 loại từ 2 điểm ảnh Đài Loan | Bản đồ rừng Google ForTy: tính điểm 6 loại từ 2 điểm ảnh Đài Loan |
| description（B選樣子句） | metadata：ví dụ đọc điểm thấp搭配生硬；要清楚是刻意選低分案例來練習閱讀，而不是低準確率或精度抽樣。只替換這個子句，保留其餘正文與credits。 | B là ví dụ đọc điểm thấp được cố ý chọn, không phải mẫu đánh giá độ chính xác. | B là ví dụ có điểm thấp được cố ý chọn để tập đọc, không phải mẫu đánh giá độ chính xác. |

### TH

| ID／欄位 | 類型與問題 | current | suggested |
| --- | --- | --- | --- |
| w86h | readability：วาดประเภท是「畫類別」的直譯；改為依最高值所屬類別著色，仍保留紅框格顯示綠色的結果。 | เลือกค่าสูงสุดมาวาดประเภท ช่องในกรอบแดงจึงแสดงสีเขียวของประเภทนั้น | ลงสีตามประเภทที่ได้ค่าสูงสุด ช่องในกรอบแดงจึงเป็นสีเขียวของประเภทนั้น |
| title | metadata：คำนวณผล 6 ประเภท把結果直接接「6種類」較生硬；具體說計算六類คะแนน，保留2像素與台灣。 | แผนที่ป่า Google ForTy: 2 พิกเซลไต้หวัน คำนวณผล 6 ประเภท | แผนที่ป่า Google ForTy: 2 พิกเซลไต้หวัน คำนวณคะแนน 6 ประเภท |
| description（首句） | metadata：ผลที่ดิน是生硬直譯，容易不清楚結果指什麼；說明是土地分類分數。只替換首句，保留其餘完整credits與URL。 | คำนวณผลที่ดิน 6 ประเภทของ ForTy จาก 2 พิกเซลจริงในไต้หวัน รวม OtherLand (พื้นที่อื่น) | คำนวณคะแนนการจำแนกที่ดิน 6 ประเภทของ ForTy จาก 2 พิกเซลจริงในไต้หวัน รวม OtherLand (พื้นที่อื่น) |

以上metadata建議只改title、指定首句或B子句；不重寫／截短資料署名、CC BY或資料包段落。兩語現在的來源／授權內容本身沒有缺失。

## 逐句檢查中保留的正確內容

- 六類均能辨認且前後一致：VI為rừng nguyên sinh／rừng tái sinh tự nhiên／rừng trồng／rừng trồng thâm canh／cây trồng thân gỗ và nông lâm kết hợp／đất khác；TH為ป่าปฐมภูมิ／ป่าฟื้นตัวตามธรรมชาติ／ป่าปลูก／สวนป่า／พืชไม้ยืนต้นและวนเกษตร／พื้นที่อื่น。`mfsh`的樹作簡稱與source同樣縮寫，不算另造類別。rrgq的木本範圍縮窄另列語義修正。
- A輸入0、248、0、0、0及B輸入0、86、0、1、77完整，零沒有漏；248／164加總、250−248=2、250−164=86、逐項除250及0.992／0.008／0.344／0.004／0.308都正確。新增0.344＋0.344=0.688，＋0.308=0.996，＋0.004=1，以及另外兩類0不改總和，也逐句保留。
- `[u5js]` 的121.4東經／24.7北緯與 `[fe8z]`、`[ymf8]` 的121.42234東經／24.69528北緯均正確；兩個像素中心座標的小數5位沒有被縮寫。10×10、10公尺亦保留，沒有變成逐樹定位。250總量與255無資料標記沒有交換；排除無資料、不當分數的否定完整。248不是樹木棵數、不是平方公尺的兩項否定完整。
- `[3pse]` 的嚴格超過40年與 `[2vcb]` 的40年或以下對應正確；輪伐期不等於現齡的限定保留。其他土地仍可能有城市樹木或稀疏木本，兩語沒有翻成裸地。
- `[dkq3]`／`[6ybg]` 的A唯一最高，與 `[97h6]` 的B兩類同86並列最高，有保留下來；並列除250得到同0.344。`[wnrz]` 仍限定「我們這張衍生圖」按類別順序取第一個最高者，沒有擴張為官方所有地圖的規則。`[7qfx]` 也保留並列紀錄與取首顯示。
- `[sbkg]` 至 `[bs4s]` 仍把模型分數與實際正確率分開，保留未做事後機率校準、需獨立參考檢查，以及不能直接稱99.2%判對機率；沒有反轉否定。`[beg8]` 與說明欄也保留B刻意低分取樣、非隨機估全圖精度的範圍。
- 2020資料年、5月公開、10月21日論文出版，以及另行分享的2017–2025早期年度序列均保留。`[88pk]` 明說這兩個2020格只能回答這個版本輸出；沒有把年度序列說成本片親自逐年實測。這是翻譯與來源敘述一致性核對，沒有重新取數或測試年度輸出。
- 我逐句讀完兩語全部92句，另對35個含重要數字的ID做數字／重複0檢查。第一人稱VI Tôi、TH ฉัน保留；VI對觀眾用bạn，TH沒有ครับ且片尾有ค่ะ。AI、ForTy、DeepMind、AlphaEarth、Google、CC BY皆使用正確Latin／縮寫，沒有轉寫產品名。

## Cue順序、字數與未審的縮短提案

worksheet的三組boundaries均逐句對照：4av2先查0–250範圍再查總和250；z33x先講6分數壓成1標籤再否定自動分出高低；8m2e先獨立參考再檢查真實結果。兩語沒有發現跨cue交換數字或論述順序。

指定路徑 `captions/zh-TW.srt` 目前不存在，搜尋此workdir亦沒有srt／vtt；只有timeline.json。因此此處是文字及boundaries的順序審查，未宣稱已完成實際切cue、配音時窗或音訊審查。兩份worksheet均未提供max_chars，不能列成硬budget通過或失敗。

- VI（約80字）軟長提醒：11句，3pse=96、v9fh=90、7id9=93、yiya=90、5nt9=92、beg8=92、mfsh=82、z33x=90、7qfx=90、8m2e=92、ci5j=88。目前內容完整，僅憑整句長度沒有另列必改缺陷；實際工具會分cue，root可依時窗再縮周邊語句，不能刪類名、三例、單位、否定或計算步驟。
- TH（扣除Unicode上下標記後約60字）軟長提醒：7句，yiya=66、5nt9=63、6ybg=62、97h6=66、z33x=67、8m2e=73、ci5j=67。目前內容完整，僅憑整句長度沒有另列必改缺陷；實際工具會分cue，root可依時窗再縮周邊語句，不能刪類名、三例、單位、否定或計算步驟。

泰文44句縮短候選沒有merge，因此不在本次repo版審查結論內，也未被當成已修。`[4w7g]` 現文為「คุณใช้แผนที่ดูสภาพแวดล้อมแบบไหนบ่อย?」，仍完整詢問「你常用地圖看哪種環境」，本句目前沒有語義缺陷。root提醒的19字候選尚未在此接受審稿；後續若縮成只問「在地圖看什麼」，就會丟掉「哪種環境」這個具體對象，不能僅為字數採用。應保留สภาพแวดล้อมแบบไหน／สภาพแวดล้อมใด或同等意思，以及地圖與平常／常用語氣。

## Metadata核對

兩語各7章均齊全；現行title分別60／56字，均≤100，tags未超過500字、沒有新增channel name。三項縮圖文字都有值，headline維持兩行與**重點**，5值／6類數字保留。沒有發現需要刪掉或重造縮圖文案的錯譯；這裡未render，因此不宣稱字體已實測≥24px。

兩語description的三條來源URL均逐字保留：

1. https://doi.org/10.25452/figshare.plus.32288616.v1
2. https://creativecommons.org/licenses/by/4.0/
3. https://github.com/x812033727/travel_scanner/tree/e0c70c899/docs/videos/forty-forest-map/data

Neumann等（2026）、Forest Typology 2020 (v1)、CC BY 4.0、裁切／補數／取首分類／重繪及沒有衛星背景圖的credits全部保留。沒有發現授權、來源連結或版本範圍的metadata事實錯誤；上方metadata建議僅處理自然度及結果究竟指分類分數的清晰度。

## Verdict與計數

| 語言 | verdict | meaning | facts | glossary | cue order | readability | budget | metadata | thumbnail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VI | ready after fixes | 2 | 0 | 0 | 0 | 3 | 0（無max_chars，不代表時窗已通過） | 2 | 0 |
| TH | ready after fixes | 0 | 0 | 0 | 0 | 1 | 0（無max_chars，不代表時窗已通過） | 2 | 0 |

VI共7項（語義2、自然度3、metadata2）；TH共3項（自然度1、metadata2）。兩語均已實讀92／92，TH新版afyy已補審。軟長提醒另列，不混算為hard budget失敗；沒有假稱已審未merge的44句提案或其19字4w7g。修正由root／作者依正常原生流程處理，本審稿只寫本報告。
