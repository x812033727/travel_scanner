# 第四支VI／TH獨立文字交叉審查

結論：需窄幅文字修正。兩語各118句、6章、title／description／tags、完整三段prompt與縮圖三欄均逐一對照。審查者未撰寫VI／TH；VI另由未寫過這兩語的子讀稿獨立核讀，再由本審查者完整閱讀並整合。未讀VI／TH作者自審報告。

不等同actual fit、音訊、ASR或媒體PASS；未merge，未改原final／todo／source／正式i18n，沒有服務／付費／backend。

核心五值與單位、2025資料／2026報告、企業含私人子集不可加、國別只比私人融資、88%受訪自述組織至少一業務、70／79未解不判錯、作者同次build非產品互動、S1總覽／S2–4定位、圖片PDF／原生可編輯PPTX與未PowerPoint原生驗證，以及Ultra／rollout無免費保證均保留。

## Metadata完整compose字節

| 語言／方案 | UTF-8 bytes | 距5000B |
|---|---:|---:|
| VI原稿 | 3976 | 1024 |
| VI必修description＋章名 | 3979 | 1021 |
| TH原稿 | 4975 | 25 |
| TH只改母體＋分母 | 4993 | 7 |
| TH整合建議＋footer等義縮字 | 4984 | 16 |

以上透過原生composeDescription純函式、當前timeline、全部6章、sources、assets credits、hashtags與原pinned URL實際計算，article=null，精確重現原TH4975B；沒有寫正式翻譯或merge。TH整合方案把「ชุดข้อมูล:」縮成「ชุด:」，只縮套件標籤，所有檔名種類、完整prompt與URL均留下。

## 必修與exact候選

### vi description.text

理由：「88% là người trả lời…」的自然越語讀法可能成為「88%是受訪者」，未明確表達比例的分母。刪除 là 並補 rằng，明確保留「88%受訪者自述其組織…」；其餘說明、三段完整提示與pinned URL全部保持。

修改片段：
- old：88% là người trả lời tự báo cáo tổ chức mình dùng AI trong ít nhất một nghiệp vụ
- candidate：88% người trả lời tự báo cáo rằng tổ chức mình dùng AI trong ít nhất một nghiệp vụ

完整old／candidate及TH最小必修版本均在JSON；未覆寫原稿。

### vi lines[id=nx2z].text

理由：來源明寫資料年；目前只剩 năm，未保留本片特別區分的資料年／報告年。預算足夠，應明寫 năm dữ liệu，並保留單位、母體或範圍及雙頁碼。 整合覆核亦補được，明確是受調查群體，避免nhóm khảo sát被讀成調查組；與uqnr術語一致。

old：Trang dữ liệu giữ năm, đơn vị, nhóm khảo sát hoặc phạm vi, cùng hai kiểu số trang.
candidate：Trang dữ liệu giữ năm dữ liệu, đơn vị, nhóm được khảo sát hoặc phạm vi và hai kiểu số trang.
字元：82 → 92／max 103；remaining 11

### vi chapters[scene=review-position-connection].text

理由：「Google thêm duyệt trước tạo」是不自然的越語動詞串，也省掉章節主題大綱。候選用自然章名表達Google的「先審大綱、再生成」位置，保留Google與先後關係；章名按原生規則可重寫為可搜尋的自然標籤。

old：Google thêm duyệt trước tạo
candidate：Google: duyệt dàn ý rồi tạo
字元：27 → 27／max 30；remaining 3

### th lines[id=cwpj].text

理由：術語更正：分母是ตัวส่วน；ตัวหาร是除數。年份、問法與分母一致性仍待確認都不變。

old：ทั้งคู่เป็นปี 2025 ยังต้องตรวจว่าคำถามกับตัวหารตรงกันไหม
candidate：ทั้งคู่เป็นปี 2025 ยังต้องตรวจว่าคำถามกับตัวส่วนตรงกันไหม
字元：56 → 57／max 58；remaining 1

### th lines[id=uqnr].text

理由：受訪母體應明示被調查的population；กลุ่มสำรวจ可被讀成調查組／調查人員。保留或統計範圍及兩種頁碼；若字數仍超限不刪母體。

old：ระบุกลุ่มสำรวจหรือขอบเขตสถิติ เลขหน้าพิมพ์และลำดับหน้า PDF
candidate：ระบุประชากรที่สำรวจหรือขอบเขตสถิติ เลขหน้าพิมพ์และลำดับหน้า PDF
字元：58 → 63／max 60；remaining -3

### th lines[id=nx2z].text

理由：同上，資料頁的母體要指被調查人口，非調查組。คง等義保留資料年、單位、母體或範圍與雙頁碼，刪重複末尾ไว้。

old：หน้าข้อมูลเก็บปีข้อมูล หน่วย กลุ่มสำรวจหรือขอบเขต และเลขหน้าทั้งสองแบบไว้
candidate：หน้าข้อมูลคงปีข้อมูล หน่วย ประชากรที่สำรวจหรือขอบเขต และเลขหน้าทั้งสองแบบ
字元：73 → 73／max 74；remaining 1

### th lines[id=yw8i].text

理由：หลายบัญชี是多個帳號，來源是多類帳號。補ประเภท保留account types，คู่มือ在此指help文件，未改變Ultra差異或保證免費。

old：ประกาศระบุหลายบัญชี แต่หน้าช่วยเหลือระบุร่วมสร้างเป็นฟีเจอร์ Ultra
candidate：ประกาศระบุหลายประเภทบัญชี แต่คู่มือระบุร่วมสร้างเป็นฟีเจอร์ Ultra
字元：66 → 65／max 68；remaining 3

### th description.text

理由：必修：人口母體改ประชากรที่สำรวจ、分母改ตัวส่วน。整合候選另把原來的文字／形狀精確成可編輯文字／形狀，並將footerชุดข้อมูล:等義縮為ชุด:以保留全長預算。所有三段完整prompt、日期、數字、範圍、否定及固定c830 URL均保留。

精確替換片段：
- กลุ่มสำรวจ/ขอบเขตสถิติ → ประชากรที่สำรวจ/ขอบเขตสถิติ（+15B）
- ตัวหาร → ตัวส่วน（+3B）
- PPTX คงข้อความ/รูปร่างดั้งเดิม → PPTX คงข้อความ/รูปร่างที่แก้ไขได้（+9B）
- ชุดข้อมูล: PDF 4 หน้า → ชุด: PDF 4 หน้า（-18B）

完整old／candidate及TH最小必修版本均在JSON；未覆寫原稿。

## 可選精確化／自然化

- vi lines[id=b7sd].text ｜ 目前的「hai chỗ ở nguồn」可以理解，但也可能像是把註記寫在原報告兩處；用 về hai đoạn nguồn 更清楚指向保留兩處來源觀察，不要求修改原來源。
  - old：Tỷ lệ AI tạo sinh chưa khớp: giữ chú thích hai chỗ ở nguồn.
  - candidate：Tỷ lệ AI tạo sinh chưa khớp: giữ chú thích về hai đoạn nguồn.
  - chars 59 → 61／max 64
- vi lines[id=yf5s].text ｜ 全片語境已讓 bài 可被理解為簡報，因此非必修；改為 slide 可避免單句聽成一般作業或文章，且仍保留留言、你想做什麼與簡報。
  - old：Bình luận: bạn muốn làm bài về gì?
  - candidate：Bình luận: bạn muốn làm slide gì?
  - chars 34 → 33／max 34
- th lines[id=xxcb].text ｜ ดั้งเดิม偏原來的／原始的；可改為可編輯文字方塊，明確傳達此例原生文字物件而非頁面圖片。前後文已說PPTX可編輯／物件分開，故列精確化建議，不冒列新事實錯誤。
  - old：เช่นหน่วยหน้าลงทุน ยังอยู่ในกล่องข้อความดั้งเดิม
  - candidate：เช่น หน่วยหน้าลงทุนอยู่ในกล่องข้อความที่แก้ได้
  - chars 48 → 46／max 49
- th lines[id=3vx9].text ｜ แนะนำให้常讀成建議去做；แนะนำการ更直接表達官方介紹生成前審大綱機制。日期與產品名不變。
  - old：19 ตุลาคม Gemini Notebook แนะนำให้ตรวจโครงร่างก่อนสร้าง
  - candidate：19 ตุลาคม Gemini Notebook แนะนำการตรวจโครงร่างก่อนสร้าง
  - chars 55 → 55／max 65
- th lines[id=kh9k].text ｜ อย่าเพิ่ง較明確表達先不要生成；目前ยังไม่ต้อง在口語中也可理解為還不用／暫不生成，故非事實必修。
  - old：เสนอโครงร่างก่อน ยังไม่ต้องสร้างสไลด์
  - candidate：เสนอโครงร่างก่อน อย่าเพิ่งสร้างสไลด์
  - chars 37 → 36／max 44

## TH原12條超限的保義處理

| ID | 原chars/max | 候選chars/remaining | 處理 |
|---|---:|---:|---|
| 7ya8 | 65/62 | 59/3 | บันทึกที่มา是同一來源紀錄的短稱，保留是否可相加、作者先填投資範圍。 |
| fskd | 69/54 | 保留原句 | 保留作者任務、同事理解AI投資與組織使用AI；未找到在54字內仍自然且不刪限定的更短句，保持原句待實際fit。 |
| sxfi | 51/49 | 48/1 | 刪列舉中的和，不刪地區／投資類型／美元單位。 |
| 5s9a | 58/38 | 保留原句 | 同事、同一檔、PDF頁序與回到原頁都必須保留；38字初步預算過緊，不以只說回原檔或泛稱頁碼取代。 |
| 2ai4 | 66/57 | 64/-7 | เฉพาะ改แค่，仍是只用作者提供的公開PDF、一般同事、4頁；未承諾能縮入時窗。 |
| 7g33 | 52/38 | 47/-9 | ครบ保留全部，ครั้งเดียว保留一次集中，รอ／จึง保留等我回覆後才生成，4頁與簡報都留。 |
| 2knx | 49/42 | 43/-1 | 每頁引用集合以อ้างอิงรายหน้า表示，保留可編輯檔／PDF／逐頁引用及一併交付，未刪任何交付種類。 |
| cht8 | 55/49 | 保留原句 | 原句已短且有未確認值只註記、不畫成確定結論兩層限制；不為49字預算刪否定或不確定性。 |
| wy6f | 55/38 | 保留原句 | 作者設計的初稿例、僅2頁、尚未排成投影片都需保留；38字內未找到可信自然短譯。 |
| b7sd | 58/46 | 保留原句 | 保留生成式AI比例、未對齊與兩處來源註記；不把兩處同報告觀察改成兩份獨立報告，保持原句待fit。 |
| iswb | 38/37 | 36/1 | 只將หนึ่ง改成數字1；自己組織、AI、至少一項業務／function條件完全保留。 |
| j47b | 75/60 | 59/1 | 刪在欄位等贅詞，保留差異只註記、排除於五項已採用數值主張；若仍超限照實保留。 |

以下可直接核對exact短句；都只是建議，負remaining仍未過初步預算：

- 7ya8 old：จะรู้ว่าสองยอดบวกได้ไหม ฉันกรอกขอบเขตลงทุนในบันทึกแหล่งข้อมูลก่อน
  candidate：จะรู้ว่าสองยอดบวกได้ไหม ฉันกรอกขอบเขตลงทุนในบันทึกที่มาก่อน
- sxfi old：ยอดเงินระบุพื้นที่ ประเภทลงทุน และหน่วยดอลลาร์สหรัฐ
  candidate：ยอดเงินระบุพื้นที่ ประเภทลงทุน หน่วยดอลลาร์สหรัฐ
- 2ai4 old：ใช้เฉพาะ PDF สาธารณะที่ฉันให้ ทำสไลด์ 4 หน้าให้เพื่อนร่วมงานทั่วไป
  candidate：ใช้แค่ PDF สาธารณะที่ฉันให้ ทำสไลด์ 4 หน้าให้เพื่อนร่วมงานทั่วไป
- 7g33 old：รอฉันตอบข้อแก้ไขทั้งหมดครั้งเดียว แล้วทำสไลด์ 4 หน้า
  candidate：รอฉันตอบข้อแก้ไขครบครั้งเดียว จึงทำสไลด์ 4 หน้า
- 2knx old：ส่งไฟล์แก้ได้ PDF กับรายการอ้างอิงรายหน้าพร้อมกัน
  candidate：ส่งไฟล์แก้ได้ PDF และอ้างอิงรายหน้าพร้อมกัน
- iswb old：องค์กรตนใช้ AI ในงานอย่างน้อยหนึ่งด้าน
  candidate：องค์กรตนใช้ AI ในงานอย่างน้อย 1 ด้าน
- j47b old：ความต่างนี้อยู่เฉพาะช่องหมายเหตุ ไม่รวมในข้อกล่าวอ้างตัวเลข 5 ข้อที่นำมาใช้
  candidate：ความต่างนี้แค่หมายเหตุ ไม่รวมข้อกล่าวอ้างตัวเลข 5 ข้อที่ใช้

TH受訪母體必修若仍超初步字數，不得再刪母體來湊fit；詳見JSON逐句字數。VI原稿0條超max，VI兩條caption建議均仍在預算；TH原稿12條超max，不把字元估計當實際音訊時長。

## 輸入凍結SHA256

- /workspace/work/travel-scanner-slides/docs/videos/ai-slides-outline-review/video.json：`296fa0c93be25c7074ec50259db650f5663aca2324a5e0a16da2118406757c2f`
- /workspace/work/travel-scanner-slides/docs/videos/ai-slides-outline-review/claims.md：`2c56550a6ffde77c8ee781f909554a8c94c9f7d787f877fc34b4c385160778f7`
- /workspace/work/travel-scanner-slides/docs/videos/ai-slides-outline-review/verify-5.md：`e812c5e1603b74c2d3dc117889df3802b0320e29e01fdffcd94c95258986cac9`
- /workspace/work/ai-tech-next/fourth-translation-vi.final.json：`e78c1d55042a6605f723c69cddad0b4dec3bc4b4330c9f53b569df0832454f67`
- /workspace/work/ai-tech-next/fourth-translation-th.final.json：`1851a4ab9346f50ca286682714632888935eb757d245a67445df05de4fc60846`
- /workspace/work/travel-scanner-slides/.agents/skills/youtube-video/references/prompts/caption-translate.md：`605e3b06224b25e66252bf5fba68ee1885b9654c762a0dd3606060042303019e`

全部236個逐句source／old／字數／max／remaining與finding對照，以及完整metadata候選、原生compose雜湊，均存JSON。翻譯僅有建議；原始兩語final SHA保持不變。
