---
id: 2026-09-06-trend-merchant-english-names-backlog
title: 商圈名單還有 95 家沒有英文店名，發布前要逐家查
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T23:38:06Z
created_at: 2026-09-06T21:10:00Z
completed_at: 2026-09-07T07:02:21Z
branch: claude/trend-merchant-names
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
---

# 商圈名單還有 95 家沒有英文店名，發布前要逐家查

## Why

`apps/api/app/foods/data/trend_merchants.json` 有 146 列，其中 **123 列**的 `name_zh`
是中文（那個欄位設計上就是中文）。`FoodMerchant.name` 是英文標籤：en 讀它，ja／ko 缺譯名
時退回它。所以一列沒有 `name_en`，發布之後英日韓讀者看到的就是中文店名。

[[2026-09-06-merchant-names-chinese-in-other-locales]] 已經把**已經發布的 28 家**補完，
匯入器也改成讀 `name_en`。剩下的 **95 列還沒發布**，所以現在沒有人看得到——但它們一上線
就會複製同一個問題。

各城市的分布（`name_zh` 含漢字的列）：`osaka-kyoto` 15、`daegu` 14、`seoul` 13、
`tokyo` 10、`bangkok` 10、`sapporo` 8、`jeonju` 8、`fukuoka` 6，其餘分散。

## Definition of done

- [x] 每一家**有出處印出英文名**的店都有 `name_en`；沒有的留空，讓讀者拿招牌原文去貼地圖。
- [x] 每個 `name_en` 要嘛就在該列的 `name_zh`／`local_name` 裡，要嘛列在測試的
      `SOURCED_ENGLISH_NAMES` 並附出處（既有的守門測試會擋）。
- [x] 正式機跑過 `backfill-merchant-english-names --apply`，已匯入的列跟著更新。

### 訂正（2026-09-07）：原本的 DoD 寫「每一列都要有 name_en」，那是錯的目標

另一個 session 在 #298／#300 定下並用測試釘住的規則是：**英文名必須是某個來源真的印出來的，
不接受我們自己音譯**。理由站得住——讀者拿 `Dongqu Fenyuan` 貼進地圖多半找不到那家店，拿
`東區粉圓` 找得到。台灣的官方觀光頁一個拉丁字都沒有，日本店家的自家網站幾乎都在頁尾或網域
寫了羅馬字，分界線很乾淨。所以這張票的目標不是「全部填滿」，是「有出處的全部填、沒出處的一個
都不填」。

## Steps

- [x] 先撈 `local_name` 裡已經帶拉丁招牌的那些（在 28 家裡佔 16 家），那是最快的一批。
- [x] 其餘逐家查：店家官網／官方 Instagram／當地觀光局頁面／英文媒體上印出來的寫法。
      **查不到就留空**，不要自己羅馬化——見上面的訂正。
- [x] **不要用音譯批次生成**。`川本屋茶舖` 的 slug 就是這樣變成 `chuan-ben-wu-cha-pu`
      ——拿普通話去讀一個日文店名——正確答案是 Kawamotoya。

## How to verify

```bash
cd apps/api && uv run python -c "
import json, re
rows = json.load(open('app/foods/data/trend_merchants.json', encoding='utf-8'))
han = re.compile('[一-鿿ぁ-ヿ]')
print(sum(1 for r in rows if han.search(r['name_zh']) and not r.get('name_en')), 'still need one')
"
```

## Notes

- 匯入器已經接受 `name_en`（`is_latin_script` 驗、`display_name` 用、泰越把中文名存進
  `names_json.zh-TW`），所以這張票純粹是補資料，不必動程式。
- 這 95 家還沒匯入正式機，所以做完之後不需要遷移，直接
  `python -m app.cli import-trend-merchants --apply` 就會帶著英文名建立。

## Result（2026-09-07）

146 列裡 **111 列有 `name_en`**（原本 21），**15 列刻意留白**，全部都是「沒有任何頁面印過拉丁字」：

| 留白 | 為什麼 |
| --- | --- |
| 大邱 8 家（笑瞇瞇燉排骨、眞城粉食、松林食堂、馬堂燒肉、燕巖茶園、流浪酒吧、貓頭鷹、阿嬤家食堂） | 大邱市美食入口網只登記韓文，沒有官網，英文媒體沒寫過 |
| 釜山 2 家（緣之洋菓子、四・留白・茶盞） | Instagram／Threads 顯示名只有韓文 |
| 全州 真談洞蕎麥麵、濟州 再演食堂 | 同上；「Jaeyeon」只出現在我們自己的 name_zh 括號裡，沒有頁面印它 |
| 台南 金得春捲、阿松割包 | 唯一印出拉丁字的是一個 WordPress 鏡像站，而且把金得讀成日文 Kintoku——總評列為致命錯誤 |
| 高雄 蠔爽 | 眷村官方頁只有中文（另一個 session 上一輪就是這樣判的） |

### 怎麼做的

1. 研究工作流：20 個城市各兩個獨立視角（店家自己的網站／IG；觀光局與英文媒體）→ 仲裁 →
   唱反調的驗證者。第一輪跑到驗證階段撞到帳戶額度，續跑又把研究重跑一遍再撞一次；
   最後改成只跑驗證的精簡工作流（12 個城市，吃已整理好的提案）才跑完。
2. 我自己用 curl 把每一個引用頁面開一次找那個字串：86 筆提案 58 筆直接命中；驗證者修過名字或
   換了出處的 38 筆再開一次（含 r.jina.ai 代理），又找回 24 筆；剩下 14 筆是 Instagram／Facebook
   登入牆，驗證者是從搜尋引擎索引的 og:title 讀到顯示名——跟上一輪 faidama 的先例同一種證據。
   Tripadvisor 擋腳本的兩筆（泰成水果店、東區粉圓）我親自用瀏覽器開過 h1。
3. 總評抓到的：金得→Kintoku（剔除）、兩個大邱名字不是文觀部式（Nakyoung／Nokyang——但那是
   Creatrip 與 edaily **印出來的**寫法，依「有出處」規則保留，沒有改成沒人印過的 Nagyeong／Nogyang）、
   效뜨改用店家自己的 Hiếu Tử（本來就在 name_zh 裡）。

### 上一輪撤掉的七個，這次有五個找到印出來的出處

另一個 session 撤掉它們的理由是「該列引用的官方頁沒有拉丁字」——對。但規則本身寫的是
「不在該列裡的英文名要列在清單並附出處」，所以有別的頁面印出來就合格：
Harajuku Gyozaro（Truly Tokyo）、Ganso Curry Tantanmen Masatora Souhonten（Tabelog 英文站；
征虎的讀音 まさとら 正是官網振假名）、Dongqu Fenyuan Bingdian（Tripadvisor h1）、
Tai Cheng Fruit Shop（Tripadvisor h1，店家 FB 帳號也是 Tai.cheng.fruit.shop）、Xiu'an Douhua（OpenRice 英文站）。
金得春捲與蠔爽維持留白。要是擁有者覺得 Tripadvisor 這種第三方列表不算數，把那五筆從
`SOURCED_ENGLISH_NAMES` 拿掉、資料檔裡的 `name_en` 刪掉即可，測試會一起擋住。

### 沒改的

- 大邱兩家的 Nakyoung／Nokyang 拼法（見上）。
- `busan-momos` 用 Visit Busan 印的「Momos Roastery & Coffee Bar」，不用店家網站拼出來的長名。
- 這 111 家裡已經匯入正式機的列要靠 `python -m app.cli backfill-english-names --apply` 更新，
  匯入器不會回頭改既有的列。

## 正式站（2026-09-07，部署 0b314ac 之後）

`backfill-merchant-english-names --apply`：資料庫裡找到 145 列，**改了 90 列**，55 列本來就一致，
沒有任何一列被判成「後台改過」而略過。

接著把 33 個城市的已發布店家（112 家）在四個語系各掃一遍：

| 語系 | `name` 仍含漢字 |
| --- | --- |
| en | **2**——金得春捲、蠔爽，正是刻意留白的那兩家（沒有頁面印過拉丁字） |
| ko | 2（同上） |
| ja | 37——日文店名本來就是漢字（白金茶房、渋谷…），不是沒翻 |
| zh-TW | 70，與套用前逐字相同（泰成水果冰店仍是泰成水果冰店，FUGLEN TOKYO 仍是 FUGLEN TOKYO） |

指令名是 `backfill-merchant-english-names`，不是任務檔先前寫的 `backfill-english-names`。
