# seoul-kalguksu-food-guide — Codex 獨立事實查核（2026-09-20）

查核者：Codex／GPT-6；未參與 Claude 原稿撰寫。此檔替換原先「進行中」佔位，原稿與前輪結論均作待查資料。

## 範圍與方法

重新請求 19 個 sources 官方網址，全部 HTTP 200；原始HTML、剔除隱藏區塊的正文、URL與回應摘要在 `codex-evidence/`。這是官方網頁資料查核，不是實地餐飲體驗。HTML可見正文判定剔除head、script、style、noscript、隱藏屬性與Visit Jeju SEO payload；不把評論、周邊推薦或輪播當成主文。沒有繞過任何來源驗證牆。

逐字引文先對原文，用標點／空白正規化輔助找出候選，再人工看句子起訖；長段截斷加刪節號。官方內容可能過時，文章保留查證月份与出發前確認提醒。

## 主張群核對與處理

以下按來源與功能分組，非虛構逐條計數。

| 主張群 | 證據編號 | 判斷及修正 |
| --- | --- | --- |
| 刀切麵定義／雞、蛤蜊、辣醬／季節豆汁麵 | 01–05 | 可見料理辭典逐字比對相符；辣醬引文保留截斷刪節號。刪無來源刀削比較。 |
| 紅豆刀切麵參考 | 06 | 官方頁可讀；目前正文未使用，保留研究參考。 |
| 명동교자本店地址、登錄與菜單 | 07、09、10 | 명동10길29，2022-003／2022及2023菜單相符；未借目錄不同地址。 |
| 未來遺產定義、主管機關 | 07、08 | 機關全名只在頁尾，改只稱首爾市政府，依協調者裁決。 |
| 명동營業與出口、雞骨 | 09、10 | 10:30–21:00、中秋當日休、4號線8出口、雞骨湯相符。 |
| 황생가湯底、餃子、交通、營業 | 11、12 | 韓文평양식 사골 칼국수相符，繁中正文是刀削麵；未改引文用字。刪未列來源的KTO附近景福宮句。 |
| 하니菜單、吧檯、候位 | 13 | 可見正文支持알곤이／재첩、수육、單人座與候位；未把等待人數寫成固定容量。 |
| 하니位置、名稱與營業 | 14、15 | 주소퇴계로411-15，2/6號線12出口，10:30–22、平日14:30–17、21最後點餐；韓文頁的確沒有대표메뉴欄。 |
| 안동집食材、佐料與白菜包飯 | 16 | 四成豆粉、鯷魚、可搭佐料、附白菜／大醬與小米饭皆有明文；沒有把可搭配改成必附。 |
| 안동집地址、時刻、公休 | 16 | 新館B1／고산자로36길3，平日10–18、六10–17、第二第四日休相符；其餘週日時間沒有擅自補。 |
| 안동집方言詞義 | 16 | 可見正文沒寫慶尚道，刪。 |
| 진성食材、夏季、時間與地址 | 17 | 八小時、香菇紅椒、每天製餃、國產黃豆、B1與兩套時刻相符；刪未列來源中文店名。 |
| 南大門巷新增段 | 18 | 地址、4號線회현5出口、油豆腐／海苔／芝麻／各家醬相符；통깨改整粒芝麻，不擅加白色。 |
| 百年店定義 | 19 | 定義存在正文，不只metadata；未把年限當成該店固定年齡。 |
| 菜單表第6列與FAQ3 | 11、15、05、17 | 韓文引文與牛骨湯標籤存在；콩국수是一般夏季习惯，沒有寫僅夏天販售。 |
| 地圖 | coordinator-notes | 하니1964656612照協調者地址裁決；명동維持본점搜尋，未假稱Naver重新驗證。 |

## 修正記錄

精確替換記錄見 `codex-evidence/changes.json`（9 種主要替換，另有來源標題、句末標點與圖解同步修改）。來源標題移除自加事實摘要，使用真實頁名。圖解PNG會重新渲染並逐張檢視。既有Commons圖片由ingest重新取得授權與作者資料，圖片alt另對輸出畫面檢查。

## 可重現來源索引

- 01: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=181&vcontsId=178875 — HTTP 200; 可見文字 2408 字；`codex-evidence/01.txt`。
- 02: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=181&vcontsId=178835 — HTTP 200; 可見文字 2380 字；`codex-evidence/02.txt`。
- 03: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=181&vcontsId=178820 — HTTP 200; 可見文字 2376 字；`codex-evidence/03.txt`。
- 04: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=181&vcontsId=178860 — HTTP 200; 可見文字 2387 字；`codex-evidence/04.txt`。
- 05: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=181&vcontsId=178880 — HTTP 200; 可見文字 2383 字；`codex-evidence/05.txt`。
- 06: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=181&vcontsId=178885 — HTTP 200; 可見文字 2375 字；`codex-evidence/06.txt`。
- 07: https://futureheritage.seoul.go.kr/futureHeritageMeet/futureHeritage/view.do?htNo=3605 — HTTP 200; 可見文字 2472 字；`codex-evidence/07.txt`。
- 08: https://futureheritage.seoul.go.kr/definition/heritageOutLine.do — HTTP 200; 可見文字 2400 字；`codex-evidence/08.txt`。
- 09: https://korean.visitseoul.net/restaurants/%EB%AA%85%EB%8F%99%EA%B5%90%EC%9E%90/KOP008570 — HTTP 200; 可見文字 12150 字；`codex-evidence/09.txt`。
- 10: https://tchinese.visitseoul.net/restaurants/%EB%AA%85%EB%8F%99%EA%B5%90%EC%9E%90/TCP008570 — HTTP 200; 可見文字 11568 字；`codex-evidence/10.txt`。
- 11: https://korean.visitseoul.net/restaurants/%ED%99%A9%EC%83%9D%EA%B0%80%EC%B9%BC%EA%B5%AD%EC%88%98/KOP003496 — HTTP 200; 可見文字 12298 字；`codex-evidence/11.txt`。
- 12: https://tchinese.visitseoul.net/restaurants/%ED%99%A9%EC%83%9D%EA%B0%80%EC%B9%BC%EA%B5%AD%EC%88%98/TCP003496 — HTTP 200; 可見文字 11609 字；`codex-evidence/12.txt`。
- 13: https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=7a72f185-a5b8-469d-98b4-67075f5b7147 — HTTP 200; 可見文字 5965 字；`codex-evidence/13.txt`。
- 14: https://korean.visitseoul.net/restaurants/HaniKalguksu/KOPl2poyj — HTTP 200; 可見文字 11262 字；`codex-evidence/14.txt`。
- 15: https://tchinese.visitseoul.net/restaurants/HaniKalguksu/TCPl2poyj — HTTP 200; 可見文字 10746 字；`codex-evidence/15.txt`。
- 16: https://korean.visitseoul.net/restaurants/andongjip-sonkalguksi/KOP32dncy — HTTP 200; 可見文字 11481 字；`codex-evidence/16.txt`。
- 17: https://korean.visitseoul.net/restaurants/%EB%B0%B1%EB%85%84%EA%B0%80%EA%B2%8C-%EC%A7%84%EC%84%B1%EC%8B%9D%EB%8B%B9/KOP042262 — HTTP 200; 可見文字 12013 字；`codex-evidence/17.txt`。
- 18: https://korean.visitseoul.net/shopping/%EB%82%A8%EB%8C%80%EB%AC%B8%EC%8B%9C%EC%9E%A5%EC%B9%BC%EA%B5%AD%EC%88%98%EA%B3%A8%EB%AA%A9/KOP041950 — HTTP 200; 可見文字 11148 字；`codex-evidence/18.txt`。
- 19: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=&vcontsId=214503 — HTTP 200; 可見文字 5038 字；`codex-evidence/19.txt`。

## 工具與圖片驗證

- `intake_check.py`: PASS；正文 4786 字，沒有超過5000硬牆。超過目標4600，保留內容並如實記warning。
- `pack_cli ingest --dry-run`: PASS，無error或warning；然後實際ingest已寫入隔離repo。
- `pack_cli lint --slug seoul-samgyetang-food-guide --slug seoul-kalguksu-food-guide --slug jeju-heukdwaeji-food-guide`: exit 0，`3 entries checked`。
- 修改後圖解用Chrome重新渲染PNG並實際打開檢視；中文字與韓文沒有遮擋／超框。初次因CHROMIUM_BIN未設定失敗，設定已安装Chrome路徑後成功。
- 三篇所有七張輸出照片已逐張打開檢查。蔘雞湯photo-2沒有獨立飯碗或酒杯，alt已修；刀切麵photo-2保留蟹螯／蟹腳／淡菜／瓜片，沒有寫萊姆或憑照片認定湯底；濟州照片是木板切肉，沒有用照片判斷豬品種。
- stdin方式執行intake第一次找不到app.guides時採fallback計數造成誤報，設PYTHONPATH為隔離repo的apps/api後，以上為真正_body_length結果。
- 僅完成內容包收件；未commit、push、PR、部署或發佈。
