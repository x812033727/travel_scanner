# seoul-samgyetang-food-guide — Codex 獨立事實查核（2026-09-20）

查核者：Codex／GPT-6；未參與 Claude 原稿撰寫。此檔替換原先「進行中」佔位，原稿與前輪結論均作待查資料。

## 範圍與方法

重新請求 17 個 sources 官方網址，全部 HTTP 200；原始HTML、剔除隱藏區塊的正文、URL與回應摘要在 `codex-evidence/`。這是官方網頁資料查核，不是實地餐飲體驗。HTML可見正文判定剔除head、script、style、noscript、隱藏屬性與Visit Jeju SEO payload；不把評論、周邊推薦或輪播當成主文。沒有繞過任何來源驗證牆。

逐字引文先對原文，用標點／空白正規化輔助找出候選，再人工看句子起訖；長段截斷加刪節號。官方內容可能過時，文章保留查證月份与出發前確認提醒。

## 主張群核對與處理

以下按來源與功能分組，非虛構逐條計數。

| 主張群 | 證據編號 | 判斷及修正 |
| --- | --- | --- |
| 料理材料、鹽的使用順序、夏季習慣 | 01、02 | 繁中與英文正文一致；鹽在桌上的位置未寫，改為按口味用鹽。刪固定一人份推論。 |
| 上桌已熟、三伏、鮑魚加料、白煮雞比較 | 03 | 可見專題正文支持；並非所有菜名都代表加料，標題、summary、正文、FAQ、圖解同步改。 |
| 산삼與토종 | 07、14 | 只列菜名；산삼中文欄改保留韓文，與正文及圖解一致。 |
| 토속촌地址、出口、203m、10–22、語言菜單、1983 | 04、05、17 | 韓英繁中頁一致，1983只歸屬Visit Seoul。 |
| 토속촌韓屋、營業補充 | 06 | KTO確有菜單、21點最後點餐、全年無休；原稿的無欄位／只有백제全年無休不成立，已改。 |
| 토속촌自家官網 | 協調者限制 | 沒有重試驗證牆；沒有價格或從受阻官網補菜單。 |
| 고려地址、七週小公雞、食感、菜單 | 07、10 | 來源相符，感受歸屬官方介紹。 |
| 고려時刻、公休 | 07、10 | Visit Seoul區分平假日，KTO統列10:30–21:00；兩種均列並提醒確認。 |
| 고려出口 | 03、07 | 舊KTO專題7號、Visit Seoul10號，總表只留站名，正文交代差異。 |
| 고려官方中文、歷史 | 08、09 | 中文前後不一致，正文不採；開業年份跨來源不同，不寫。依協調者裁決刪兩代。 |
| 백제地址、雞種、食材、配菜、菜單 | 11、12、13 | 主介紹及菜單相符；刪唯一列食材的誇大比較，고려也有材料。 |
| 백제出口與營業 | 11、12、13 | 出口韓文5／外文6不一致，總表僅站名；9–22、21最後點餐、全年無休相符。 |
| 백년토종地址、菜單、時間、調味 | 14 | 明確是마포 양화로118；不採종로同名店。09–22與無公休欄分清。 |
| 3대地址、交通、蒸籠／sous-vide、菜單、假日 | 15、16 | 相符；刪唯一介紹作法，其他頁同樣有作法。全年依據限定到該頁사시사철。 |
| FAQ／summary／圖解 | 上述 | 同步撤掉全店全年與同鍋加料、一人份等推論；圖解描述與SVG desc同步。 |
| 精確地圖編號 | coordinator-notes | 35597924、11657952沿用協調者的地址比對；本輪未再開Naver，不宣稱已重驗。 |

## 修正記錄

精確替換記錄見 `codex-evidence/changes.json`（25 種主要替換，另有來源標題、句末標點與圖解同步修改）。來源標題移除自加事實摘要，使用真實頁名。圖解PNG會重新渲染並逐張檢視。既有Commons圖片由ingest重新取得授權與作者資料，圖片alt另對輸出畫面檢查。

## 可重現來源索引

- 01: https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=181&vcontsId=178340 — HTTP 200; 可見文字 2392 字；`codex-evidence/01.txt`。
- 02: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=178344 — HTTP 200; 可見文字 6225 字；`codex-evidence/02.txt`。
- 03: https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid=47e4dd8d-3daf-4552-abac-e43a17fc90ea — HTTP 200; 可見文字 5676 字；`codex-evidence/03.txt`。
- 04: https://korean.visitseoul.net/restaurants/TosokchonSamgyetang/KOPywjsmm — HTTP 200; 可見文字 11299 字；`codex-evidence/04.txt`。
- 05: https://tchinese.visitseoul.net/restaurants/x/TCPywjsmm — HTTP 200; 可見文字 10852 字；`codex-evidence/05.txt`。
- 06: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=97919 — HTTP 200; 可見文字 6718 字；`codex-evidence/06.txt`。
- 07: https://korean.visitseoul.net/restaurants/%EA%B3%A0%EB%A0%A4%EC%82%BC%EA%B3%84%ED%83%95/KOP008646 — HTTP 200; 可見文字 11468 字；`codex-evidence/07.txt`。
- 08: https://tchinese.visitseoul.net/restaurants/x/TCP008646 — HTTP 200; 可見文字 11004 字；`codex-evidence/08.txt`。
- 09: https://futureheritage.seoul.go.kr/futureHeritageMeet/futureHeritage/view.do?htNo=154 — HTTP 200; 可見文字 2130 字；`codex-evidence/09.txt`。
- 10: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=99774 — HTTP 200; 可見文字 6842 字；`codex-evidence/10.txt`。
- 11: https://korean.visitseoul.net/restaurants/%EB%B0%B1%EC%A0%9C%EC%82%BC%EA%B3%84%ED%83%95/KOP006151 — HTTP 200; 可見文字 12034 字；`codex-evidence/11.txt`。
- 12: https://tchinese.visitseoul.net/restaurants/x/TCP006151 — HTTP 200; 可見文字 11679 字；`codex-evidence/12.txt`。
- 13: https://english.visitseoul.net/area/Baekje-Samgyetang1/ENP006151 — HTTP 200; 可見文字 15314 字；`codex-evidence/13.txt`。
- 14: https://korean.visitseoul.net/restaurants/BaengnyeonTojong/KOPo3ewu8 — HTTP 200; 可見文字 11240 字；`codex-evidence/14.txt`。
- 15: https://korean.visitseoul.net/restaurants/%EB%B0%B1%EB%85%84%EA%B0%80%EA%B2%8C-3%EB%8C%80-%EC%82%BC%EA%B3%84%EC%9E%A5%EC%9D%B8/KOP042260 — HTTP 200; 可見文字 11644 字；`codex-evidence/15.txt`。
- 16: https://tchinese.visitseoul.net/restaurants/x/TCP042260 — HTTP 200; 可見文字 11108 字；`codex-evidence/16.txt`。
- 17: https://english.visitseoul.net/PalaceArea/TosokchonSamgyetang/ENPywjsmm — HTTP 200; 可見文字 14218 字；`codex-evidence/17.txt`。

## 工具與圖片驗證

- `intake_check.py`: PASS；正文 4854 字，沒有超過5000硬牆。超過目標4600，保留內容並如實記warning。
- `pack_cli ingest --dry-run`: PASS，無error或warning；然後實際ingest已寫入隔離repo。
- `pack_cli lint --slug seoul-samgyetang-food-guide --slug seoul-kalguksu-food-guide --slug jeju-heukdwaeji-food-guide`: exit 0，`3 entries checked`。
- 修改後圖解用Chrome重新渲染PNG並實際打開檢視；中文字與韓文沒有遮擋／超框。初次因CHROMIUM_BIN未設定失敗，設定已安装Chrome路徑後成功。
- 三篇所有七張輸出照片已逐張打開檢查。蔘雞湯photo-2沒有獨立飯碗或酒杯，alt已修；刀切麵photo-2保留蟹螯／蟹腳／淡菜／瓜片，沒有寫萊姆或憑照片認定湯底；濟州照片是木板切肉，沒有用照片判斷豬品種。
- stdin方式執行intake第一次找不到app.guides時採fallback計數造成誤報，設PYTHONPATH為隔離repo的apps/api後，以上為真正_body_length結果。
- 僅完成內容包收件；未commit、push、PR、部署或發佈。
