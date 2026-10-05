---
id: 2026-09-20-visitjeju-hidden-payload-recheck
title: Recheck live articles quoting Visit Jeju after its site redesign
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-visitjeju-recheck
claimed_at: 2026-10-05T07:01:51Z
created_at: 2026-09-20T13:05:00Z
completed_at:
branch: claude/visitjeju-recheck
depends_on: []
scope:
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/api/app/guides/content/korea-food-guide-must-eat.json
---

# Recheck live articles quoting Visit Jeju after its site redesign

## Why

`visitjeju.net` 改版了。每一頁現在都有一個隱藏區塊：

```html
<div style="display:none" id="__SEARCH_DATA__"> … </div>
```

裡面是**舊版的長介紹**（`sbstseo` 欄位）、兩種地址與營業時間。畫面上的 `상세정보` 已經換成比較短的新摘要。

2026-09-20 寫韓國美食特輯時發現：濟州黑豬肉篇的規格與撰稿筆記逐字抄下來的「官方原文」**有一半在那個隱藏區塊裡**，草稿有 **12 項事實只有隱藏區塊撐得住**，全部刪掉或改寫。

**這兩篇已經在正式站上的文章也引用 Visit Jeju**，寫作時間比改版早，所以很可能有同樣的問題：

| 文章 | 引用的 Visit Jeju 頁 |
| --- | --- |
| `jeju-3-day-itinerary` | 성산일출봉的開放時間、休息日、登頂時間（韓文頁＋英文頁） |
| `korea-food-guide-must-eat` | Traditional Jeju Island Foods、Jeju's Signature Heukdwaeji、Great Dine-alone Spots on Jeju |

`korea-food-guide-must-eat` 的風險比較高：它引的正是特輯這次撞到的那幾個主題頁（黑豬肉、돔베고기、고기국수）。

**這不是「引文位置」的問題。** 那個 div 就在 `<body>` 裡，位置對，但畫面上看不到。真正的標準一直都是**讀者打開那一頁看得到的字**。

## Definition of done

- [x] 兩篇文章裡每一條出自 Visit Jeju 的主張，都確認在**可見**文字裡站得住
- [x] 只有隱藏區塊撐得住的主張已刪除或改寫（結果：沒有一條只靠隱藏區塊；改了一條說過頭的，見 Notes）
- [x] 營業時間類的資訊（성산일출봉）與官方可見頁一致

## Steps

- [x] 用 `C:\Users\x8120\mokaair-work\korea-food-specials\tools\split_visible.py` 把每一頁切成「可見」與「隱藏」兩份（那個工作區已經不在了，在 session scratchpad 用 stdlib `html.parser` 重寫一支：`head`、`script`、`style`、`noscript`、`template`、HTML 註解、`hidden`、`aria-hidden="true"`、行內 `display:none`／`visibility:hidden` 與 `#__SEARCH_DATA__` 都算隱藏）
- [x] 逐條比對兩篇文章的主張
- [x] 只有隱藏那份撐得住的，當作沒有來源處理
- [x] 更新 `sources` 的 `checked_on`
- [ ] 正式站：`guides-import --slug jeju-3-day-itinerary --slug korea-food-guide-must-eat --locale zh-TW --publish`。publish after merge (coordinator, owner consent)

## How to verify

```bash
cd apps/api && python -m app.guides.pack_cli lint --kind howto
```

零錯誤，且兩篇的每一條 Visit Jeju 主張都能在可見文字裡找到對應。

## Notes

- 外部請求的 User-Agent 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放任何個人資料；同網域間隔至少 1 秒。
- 這個陷阱也寫在韓國特輯的 `prompts/SOURCE-TIPS.md`（「visitjeju.net 把舊版內容藏在 `display:none` 的區塊裡」一節）。
- 同批還沒寫的濟州文章（涯月咖啡、舊左・細花咖啡、濟州豬肉湯麵）已經在各自的撰稿指令裡帶上這條，不需要這張票處理。
- 值得順手想一下：**別的官方站有沒有同樣的做法**。這類 SEO 隱藏區塊不是 Visit Jeju 獨有的手法。

### 2026-10-05 重驗（claude-opus-5-5-visitjeju-recheck）

抓了五個 Visit Jeju 網址（全部 HTTP 200，沒有轉址），外加世界遺產本部兩頁；每頁切成可見與隱藏兩份比對。景點頁另外用內建瀏覽器打開，點過「더보기 +」與「펼치기 +」看讀者實際看到什麼。

**一個要記住的反例**：景點頁的 `이용안내`（英文版 `Tip`）在 curl 抓到的 HTML 裡是空的 `<ul>`，按下「더보기 +」才由前端畫出 `이용 시간`、`상세 정보`、`요금 정보`。分季時間、休息日、禁帶食物、票價就在這裡，而且跟 `#__SEARCH_DATA__` 裡的 `usedescinfo` 一字不差。讀者按一下就看得到，所以算可見；只用 HTMLParser 判斷會把它誤判成「只在隱藏區塊」。正文的「펼치기 +」只是解除高度裁切，點開前後字數一樣，不會顯示隱藏區塊。這條另開票寫進 skill：`2026-10-05-write-the-visit-jeju-hidden-payload`。

| # | 主張（節錄） | 頁面 | 可見文字 | 結果 |
| --- | --- | --- | --- | --- |
| J1 | 城山日出峰是世界自然遺產的凝灰岩火山口 | 성산 kr／en | 상세정보：응회구、유네스코 세계자연유산 | 相符 |
| J2 | 3、4 月與 9、10 月 05:00 到 19:00、18:00 停止售票 | 성산 kr／en；世界遺產本部 | 이용안내「더보기」：(춘·추절기) 05:00~19:00 (매표 05:00~18:00)；本部頁同 | 相符（正文、表格、圖解 desc、行前檢查都不用動） |
| J3 | 5 到 8 月 04:30 到 20:00、19:00 停止售票 | 同上 | (하절기) 04:30~20:00 (매표 04:30~19:00)；本部頁同 | 相符 |
| J4 | 11 月到 2 月「Visit Jeju 與世界自然遺產本部的公告不一致」 | 同上 | 兩邊今天都是 06:00~18:00（매표 06:00~17:00）；本部頁另寫「필요시에는 관람시간을 따로 정할 수 있음」 | **已改**：寫出 06:00 到 18:00、17:00 停止售票，保留「必要時另訂時間，出發前看當期公告」 |
| J5 | 每月第一個週一休，遇假日改隔天（正文、callout、description） | 성산 kr／en；本部頁 | 매달 첫 번째 월요일 정기 휴무(공휴일인 경우 다음 날 휴무)；本部頁只寫第一個週一 | 相符 |
| J6 | 步道分收費的登頂段與免費的周邊段，登頂約 30 到 40 分鐘 | 성산 kr／en | 상세정보：유료 탐방구간／무료 탐방구간、약 30~40분 | 相符 |
| J7 | 山頂步道禁止帶食物 | 성산 kr／en | 이용안내：음식물 반입 금지／No outside food allowed | 相符 |
| J8 | 門票以官網為準 | — | 兩頁今天都是成人 5,000 韓元 | 沒動（原文本來就不寫數字；要補數字是另一個編輯決定） |
| M1 | 濟州的招牌是黑豬肉 | 黑豬肉頁 en | one of Jeju's representative foods | 相符 |
| M2 | 本地人烤黑豬肉會蘸멜젓 | 黑豬肉頁 en；傳統美食頁 en | people dip their Heukdwaeji into … mel-jeot；locals like to dip the meat in … meljeot | 相符 |
| M3 | 有的店把鮑魚、蝦子與蕨菜放同一個烤盤 | 黑豬肉頁 en | grilled together with Gosari (Ferns), seafood like Abalone, Shrimps | 相符 |
| M4 | 濟州市舊城區的黑豬肉街「整條都是專門店」 | 傳統美食頁 en；黑豬肉頁 en | Black Pork Street on Chilseong Road in old Jeju City … find some famous black pork restaurants；a lot of restaurants specializing in heukdwaeji | **已改**：「整條都是專門店」說過頭，改成「聚集了許多黑豬肉專門店」；舊城區有可見文字撐 |
| M5 | 官方頁提醒點餐時確認是不是黑豬肉 | 黑豬肉頁 en | Helpful Travel Tips 2 | 相符 |
| M6 | 鮑魚粥 | 傳統美食頁 en | One of the most popular dishes is abalone porridge | 相符 |
| M7 | 고기국수，豬骨白湯配黃麵 | 傳統美食頁 en | broth made from slow-boiled pork … Yellow noodles … milky white soup | 相符（頁面寫豬肉熬湯，沒寫「骨」；兄弟篇 `jeju-gogi-guksu-food-guide` 依店家頁寫豬骨，維持） |
| M8 | 夏天的水拌生魚片（물회） | 傳統美食頁 en | typically enjoyed during the hot summer days | 相符 |
| M9 | 白帶魚（갈치）「清湯或鹽烤」 | 傳統美食頁 en／zh | 只有烤魚段的 galchi；兩個語系都沒有白帶魚湯（kr 版網址只有頁框，沒有這篇的內文） | **查不到，照協調者指示保留原文**：這句不是掛 Visit Jeju 的引文，갈치국是濟州常見菜，但今天沒有官方頁能撐「清湯」；下一次改這篇時找一個來源或刪掉「清湯」 |
| M10 | Visit Jeju 一人食專題介紹的店多半設靠窗吧檯 | 一人食頁 en | 四家裡 Hamoribap 吧檯看村景、Sunitable 與 Aewol Donkatsu 靠窗 counter seat；Danso 是圓矮桌 | 相符（頁面寫於 2020-12-30） |

- 隱藏區塊：兩個景點頁的 `sbstseo` 今天跟可見正文相同；三個主題頁（`/themtour/view`）的 `sbstseo` 是空的，隱藏區塊只有標題與 tag。黑豬肉頁的 `sbstseo` 是可見正文的開頭。**兩篇沒有任何一條只靠隱藏區塊撐住**。
- 來源：世界遺產本部那筆原本指 `https://www.jeju.go.kr/wnhcenter/index.htm`（世界自然遺產中心首頁），今天首頁已經沒有城山日出峰的時間公告，換成本部的城山日出峰탐방안내頁 `https://www.jeju.go.kr/jejuwnh/heritage/seongsan/intro.htm`（`seongsan.htm` 會轉到這裡，填最終網址）。五筆 Visit Jeju 來源與這一筆的 `checked_on` 改成 2026-10-05；傳統美食頁的來源標題改成這篇實際用到的內容（原本列的돔베고기文章沒用到）。
- 別的官方站：同一天掃過 VISITKOREA（About Korean Food）、Visit Seoul（廣藏市場）、Visit Busan（札嘎其）與世界遺產本部城山頁，超過 200 字的 `display:none` 只有 cookie 提示，沒有 SEO 隱藏正文。
- 檢查：`pack_cli lint --slug jeju-3-day-itinerary --slug korea-food-guide-must-eat` exit 0（各一個既有的 `no_summary` warning）；`pack_cli lint --kind howto` exit 0、0 error、330 warning、152 entries；`pytest tests/test_guides_content_pack.py` 9 passed、5 skipped。`intake_check.py --from-content` 兩篇都 FAIL，但全部是這次沒碰的既有項目（沒有 summary、五欄表、`foods?city=` 連結、must-eat 的「這篇」出現兩次），圖解數字檢查 ok。
- 圖解 SVG 只寫 9、10 月的時間，今天仍然正確，沒有改 `apps/web/public/guides/jeju-3-day-itinerary/diagram-1.svg`。
- 正式站要等合併後由協調者在站主同意下 `guides-import --slug` 匯入，這張票不碰主機。
