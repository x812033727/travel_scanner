# jeju-heukdwaeji-food-guide — Codex 獨立事實查核（2026-09-20）

查核者：Codex／GPT-6；未參與 Claude 原稿撰寫。此檔替換原先「進行中」佔位，原稿與前輪結論均作待查資料。

## 範圍與方法

重新請求 12 個 sources 官方網址，全部 HTTP 200；原始HTML、剔除隱藏區塊的正文、URL與回應摘要在 `codex-evidence/`。這是官方網頁資料查核，不是實地餐飲體驗。HTML可見正文判定剔除head、script、style、noscript、隱藏屬性與Visit Jeju SEO payload；不把評論、周邊推薦或輪播當成主文。沒有繞過任何來源驗證牆。

逐字引文先對原文，用標點／空白正規化輔助找出候選，再人工看句子起訖；長段截斷加刪節號。官方內容可能過時，文章保留查證月份与出發前確認提醒。

## 主張群核對與處理

以下按來源與功能分組，非虛構逐條計數。

| 主張群 | 證據編號 | 判斷及修正 |
| --- | --- | --- |
| 品種與價位、meljeot | 03、04 | 黑豬本地品種、毛色體型、較高價位與蘸醬有正文；沒有醫療營養承諾。 |
| 部位／斤肉／一般豬混售／共烤海鮮 | 01、02 | 英繁中主題頁可見正文與部位卡支持；목살中文採協調者台灣用語，항정살未冒充官方中文譯名。 |
| 돔베고기照片說明 | 03、04 | boiled pork／木板／名字相符；繁中把pork belly誤作豬肚，移除該不可靠引文片段。照片不能證明黑豬品種。 |
| 黑豬肉街 | 05 | 건입동、機場車程20分左右、칠성로／탑동相符；不稱政府指定街，不搬主題頁門牌來替換街區頁。 |
| 아랑조을거리 | 06 | 천지로2、알아서 좋은 거리、對街市場相符；不採隱藏舊文字店數。 |
| 돈사돈 | 07 | 可見新正文有2006、연탄、목살／오겹살、店員烤、煮멜젓與김치찌개收尾；地址우평로19。 |
| 흑돈가 | 08、09 | 可見正文炭火／厚切／멜젓，KTO支持較厚切、煮滾及hangjeongsal／黑豬泡菜鍋；道路地址用KTO原韓文。 |
| 곱들락 | 10 | 함덕18길19、곱다詞義、熟成、목살／오겹살、代烤、鹽／佐料、其他肉、東岸行程皆有可見正文；不恢復套餐及秤重。 |
| 뚱딴지 | 11 | 第二代、原肉熟成、專人烤和說明吃法、韓牛海鮮菇蔬菜有可見正文；刪沒明文支持的菊芋詞義。 |
| 삼합 | 12 | 태평로482번길50、서귀동、黑豬＋章魚鮑魚貝蝦、靠市場支持；刪未證實不在아랑조을거리的否定。 |
| 營業時間 | 07–12 | Visit Jeju可見이용안내為空，延續裁決全篇不列時間；沒有拿隱藏SEO時刻使用。 |
| 隱藏資料 | HTML現況 | 本輪HTMLParser移除#__SEARCH_DATA__、display:none、hidden／aria-hidden、head／script／style；沒有採評論、tag當店家配方或菜單。 |
| 圖解、summary、FAQ | 01–12 | 去除油脂香氣最明顯的無依據比較；正文與SVG desc同步。 |
| 地圖 | coordinator-notes | 돈사돈11840561依協調者交代沿用；本輪未宣稱Naver重驗。 |

## 修正記錄

精確替換記錄見 `codex-evidence/changes.json`（6 種主要替換，另有來源標題、句末標點與圖解同步修改）。來源標題移除自加事實摘要，使用真實頁名。圖解PNG會重新渲染並逐張檢視。既有Commons圖片由ingest重新取得授權與作者資料，圖片alt另對輸出畫面檢查。

## 可重現來源索引

- 01: https://www.visitjeju.net/en/detail/view?contentsid=CNTS_300000000012875 — HTTP 200; 可見文字 4482 字；`codex-evidence/01.txt`。
- 02: https://www.visitjeju.net/zh/detail/view?contentsid=CNTS_300000000012875 — HTTP 200; 可見文字 1734 字；`codex-evidence/02.txt`。
- 03: https://www.visitjeju.net/en/themtour/view?contentsid=CNTS_200000000012741&menuId=DOM_700000000010782 — HTTP 200; 可見文字 11654 字；`codex-evidence/03.txt`。
- 04: https://www.visitjeju.net/zh/themtour/view?contentsid=CNTS_200000000012741&menuId=DOM_700000000010782 — HTTP 200; 可見文字 4041 字；`codex-evidence/04.txt`。
- 05: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_200000000007287 — HTTP 200; 可見文字 1615 字；`codex-evidence/05.txt`。
- 06: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_300000000012852 — HTTP 200; 可見文字 1594 字；`codex-evidence/06.txt`。
- 07: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000020104 — HTTP 200; 可見文字 2564 字；`codex-evidence/07.txt`。
- 08: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000001043&menuId=DOM_200000000011265 — HTTP 200; 可見文字 2529 字；`codex-evidence/08.txt`。
- 09: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=45468 — HTTP 200; 可見文字 6877 字；`codex-evidence/09.txt`。
- 10: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000020562 — HTTP 200; 可見文字 2499 字；`codex-evidence/10.txt`。
- 11: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_300000000012846 — HTTP 200; 可見文字 1650 字；`codex-evidence/11.txt`。
- 12: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_300000000012845 — HTTP 200; 可見文字 1735 字；`codex-evidence/12.txt`。

## 工具與圖片驗證

- `intake_check.py`: PASS；正文 4556 字，沒有超過5000硬牆。落在目標區間。
- `pack_cli ingest --dry-run`: PASS，無error或warning；然後實際ingest已寫入隔離repo。
- `pack_cli lint --slug seoul-samgyetang-food-guide --slug seoul-kalguksu-food-guide --slug jeju-heukdwaeji-food-guide`: exit 0，`3 entries checked`。
- 修改後圖解用Chrome重新渲染PNG並實際打開檢視；中文字與韓文沒有遮擋／超框。初次因CHROMIUM_BIN未設定失敗，設定已安装Chrome路徑後成功。
- 三篇所有七張輸出照片已逐張打開檢查。蔘雞湯photo-2沒有獨立飯碗或酒杯，alt已修；刀切麵photo-2保留蟹螯／蟹腳／淡菜／瓜片，沒有寫萊姆或憑照片認定湯底；濟州照片是木板切肉，沒有用照片判斷豬品種。
- stdin方式執行intake第一次找不到app.guides時採fallback計數造成誤報，設PYTHONPATH為隔離repo的apps/api後，以上為真正_body_length結果。
- 僅完成內容包收件；未commit、push、PR、部署或發佈。

## 收件後補圖（Codex，2026-09-20）

批次資產清單發現此篇只有封面和圖解，補入 Commons `File:Samgyeopsal-gui.jpg`（CC0）的內文照片；再次 `pack_cli ingest --dry-run` 與 ingest 都成功，產物 `photo-1.webp` 已實際開圖。圖中為金屬盤裡的熟五花肉，不是烤盤上的現烤畫面；alt 依實際畫面修正。這是一般五花肉示意，原圖 metadata 不能證明豬種或濟州地點，caption 明說不能拿照片判斷是否黑豬肉。此補圖不改逐店或料理主張；需在最後全批 lint 再確認。
