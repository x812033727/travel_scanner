# 規則命中的 117 筆逐筆判讀（2026-09-19）

票：`tasks/open/2026-09-19-review-117-flagged-foreign-guides.md`。這是 2026-09-19 `guides-foreign-place-scan` 命中 165 筆、
站主只退了核對過的 52 筆之後，**還公開著的 117 筆**逐筆看過的結果。背景與 52 筆的處理在
[`2026-09-13-misplaced-guides.md`](2026-09-13-misplaced-guides.md)。

檔案：

- [`2026-09-19-foreign-guides-unreviewed.json`](2026-09-19-foreign-guides-unreviewed.json)：原始清單，每列**多了**
  `verdict`（`reject`｜`keep`）與 `verdict_reason`（一行判讀理由，117 列都有）。規則自己寫的 `reason` 原封不動，
  所以退件時寫進 `review_reason` 的字句還是規則的。
- [`2026-09-19-foreign-guides-keep-ids.txt`](2026-09-19-foreign-guides-keep-ids.txt)：`--skip-ids-file` 用的保留清單：
  2 筆 `keep` 加上 2026-09-13 起就要帶著的 `eff4dc8f-6ea0-4392-abed-f7bf7d6e0e72`。`#` 之後是註解（CLI 會剝掉）。

## 怎麼判

- 對照的是**景點本身**，不是城市：內容明明是另一個國家、或另一個城市的同名景點就 `reject`；內容真的在講這個景點、
  只是文中提到別的國家（NAVITIME 的店頁、含這個景點的清單文）就 `keep`。
- 標題與網址能定的就定；定不了的開頁。共送出 **8 次**請求（6 個原網址 + hoiana 的部落格索引 + 搬家後的同一篇文章），
  UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，每次間隔 1.5 秒，只送網址不送任何個資，
  頁面文字只當資料看。3 支影片不開 YouTube，依標題判（匯出裡沒有頻道欄位）。
- 開頁結果：NAVITIME（`6da32c2d`）被 CloudFront 擋，403；hoiana 原網址（`c4706b00`）404，同文搬到新網址後 200；
  `taiwan.net.tw` 兩頁、韓國觀光數據實驗室、JETRO 都 200。

## 結果

| verdict | 筆數 |
| --- | ---: |
| reject | 115 |
| keep | 2 |

依景點所在國：

| 景點所在國 | reject | keep | 合計 |
| --- | ---: | ---: | ---: |
| 韓國 | 50 | 0 | 50 |
| 越南 | 40 | 1 | 41 |
| 台灣 | 15 | 0 | 15 |
| 日本 | 10 | 1 | 11 |

依語系：zh-TW 50、ja 31、en 23、ko 8、zh-CN 5；依型態：文章 114、影片 3（影片全退）。

## 保留的兩筆

| 介紹 id | 景點 | 為什麼保留 |
| --- | --- | --- |
| `6da32c2d-96a5-48ac-bde3-edee52eb28d6` | MEGA 唐吉訶德澀谷本店（東京） | NAVITIME 的 MEGAドン・キホーテ渋谷本店 POI 頁，就是這個景點本身。標題把店名寫成「MEGA(メガ)ドン・キホーテ 渋谷本店」，對不上 ja 名稱「MEGAドン・キホーテ渋谷本店」，又只寫「渋谷区」沒寫東京／日本；摘要裡有「タイ」，規則就判成泰國。開頁 403，依標題與網址判定。 |
| `c4706b00-7c1d-4eac-9d5e-96229a20f0be` | 會安古城（峴港） | Hoiana 的「會安古鎮：你應該在會安停留多少天？」內容就是會安古城；被判成日本是因為文中列了「日本橋（來遠橋）」，而標題寫「古鎮」對不上景點名「古城」、峴港的目的地別名裡也沒有「會安」。**原網址現在回 404**，同一篇已搬到 `https://www.hoiana.com/zh-hant/blog/how-many-days-should-you-spend-hoi-an`（開頁確認，目前只剩英文版）。死連結不是這條規則的事，另行處理（見文末）。 |

## 規則誤判的形狀（給調 `foreign_place` 的人）

規則讀的是 `title + summary`，非拉丁字的國名／城市名用**純子字串**比對，命中另一國、又找不到本國提示、
本景點名、城市名或別名時就是 finding。這批裡真正判錯的只有 2 筆，但它們各自是一種會重複的形狀：

1. **標題改寫店名 + 摘要裡的兩假名國名。** NAVITIME 一類的 POI 站會把店名寫成「MEGA(メガ)ドン・キホーテ 渋谷本店」
   （加讀音、加空白），景點的 ja 名稱就不再是它的子字串；地址寫區（渋谷区）不寫都，目錄裡的東京別名也沒有渋谷／澀谷。
   剩下的就是摘要裡任何一個「タイ」——它是 Thailand 的日文，也是「タイム」「スタイル」「タイプ」的一部分（摘要不在匯出裡、
   頁又被擋，這筆到底是哪一個沒法確認；Don Quijote 在泰國也有分店）。例：`6da32c2d`（keep）；`94f810a9`（JETRO，verdict 沒錯，
   但 elsewhere 寫「タイ」是因為摘要提到泰國企業，標題寫「対日」而不是「日本」，本國提示一樣沒中）。
   可以做的：比對本景點名前先把標題的全形／半形括號內容與空白剝掉；把目的地的住宿區名（澀谷、原宿……）也算成本國提示；
   兩個假名長的國名只在標題裡算數，或要求前後不是片假名。
2. **地標名裡含另一國國名。** 會安的「日本橋」（來遠橋）、河內玉山祠對台灣「玉山」、各地的「中國城」都會讓 `country_mentions`
   撿到別國；配上景點名寫法不同（會安古**城**／會安古**鎮**）與峴港別名沒有會安／Hội An／Hoi An／ホイアン，就沒有任何東西
   指回越南。例：`c4706b00`（keep；2026-09-13 那次也是同一篇被命中）。可以做的：`會安古城` 的別名加上會安、會安古鎮、Hội An、
   Hoi An、ホイアン，search terms 加日本橋、來遠橋；更一般地，在 `country_mentions` 之前先把已知含國名的地標名（日本橋、玉山）
   從文字裡拿掉。
3. **理由字眼只反映這一次的摘要（verdict 對、理由錯）。** 同一個部落格首頁 `yoke918.tw` 在不同景點下被報成台灣、台南、沖繩
   （`57823a26`、`14b90974` 是沖繩；`25a519a0` 是台南），因為每次探索的摘要不一樣；交通部觀光署的同一頁「指南宮」在 `d469749d`
   下被報成泰國（摘要剛好是「泰國巴博元帥致贈的金佛」那句），在 `c7aac200` 下被報成台灣。退件時 `review_reason` 會照寫，
   所以會出現「內容講的是沖繩」的台灣部落格。可以做的：標題優先，或回報命中最多次的國家，而不是第一個命中的。

## 不是規則誤判、但搜尋端該知道的形狀

這 115 筆規則都判對了；它們會進來，是 2026-09-16 之前搜尋只丟景點名造成的。重複最多的：

- **「市場」的雙義。** 釜山國際市場的 ja 搜尋收到訪日「市場」分析（`1c2ffc5b`、`3467abb4`、`3c6eab28`、`94f810a9`、`a716dd4a`，
  加上 Yahoo!トラベル的日本市集分類頁 `c7b531b1`）；台中第二市場的 ko 搜尋收到韓國觀光數據實驗室的泰國市場動向報告 `e588910e`。
- **名字的一部分撞名。** 第二市場→札幌二条市場（7 筆）；豐南門→台南（12 筆台南清單）；豐沛之館→札幌豐平館、東京豐洲、江蘇沛縣、
  花蓮豐之谷；白馬國家公園→長野白馬村（7 筆）；金山寺→京都金閣寺；黃金山→新北金山／萬里；圓山公園→台北圓山；
  同春市場→「春の絶景」、大邱西門市場；Royal Portrait Museum→倫敦 National Portrait Gallery；應陵→韓國江陵。
- **部落格首頁。** 23 筆的網址是站台根目錄（`yoke918.tw` 10、`bunnyann.tw` 5、`travelss.net` 5、`fullfen.tw` 2、`fullfenblog.tw` 1），
  同一個首頁掛在五、六個越南／韓國景點下。首頁永遠不是單一景點的介紹，探索時可以直接丟掉 path 是 `/` 的候選。
- **順化的四座陵與安定宮、長前橋** 收到的幾乎全是台灣清單文與部落格首頁（22 筆），全州的豐南門、豐沛之館也是（`taiwan.net.tw`、
  Klook、KKday 的台南頁）。

## 站主在主機上跑的

api 映像檔只有 `apps/api`，看不到 `docs/`，所以先把 skip 清單放進容器（或改用三個 `--skip-id`，見下）。

```bash
cd /root/travel_scanner && git pull     # 要有 docs/catalog-content-reviews/2026-09-19-foreign-guides-keep-ids.txt
docker compose -f docker-compose.prod.yml cp \
  docs/catalog-content-reviews/2026-09-19-foreign-guides-keep-ids.txt api:/tmp/foreign-guides-keep-ids.txt

# 1. 只列不寫：預期 findings 正好 115 筆（就是 JSON 裡 verdict=reject 的那些）、skipped 3
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-foreign-place-scan \
  --skip-ids-file /tmp/foreign-guides-keep-ids.txt --verbose | tee /tmp/foreign-scan-before.txt

# 1b. 核對 id 集合（輸出最後那段 JSON 的 findings 對 JSON 檔的 reject 列）；extra 與 missing 都要是 []
python3 - <<'PY'
import json, re
text = open('/tmp/foreign-scan-before.txt', encoding='utf-8').read()
report = json.loads(text[re.search(r'^\{', text, re.M).start():])
found = {f['guide_id'] for f in report['findings']}
rows = json.load(open('docs/catalog-content-reviews/2026-09-19-foreign-guides-unreviewed.json', encoding='utf-8'))['guides']
expected = {r['guide_id'] for r in rows if r['verdict'] == 'reject'}
print(len(found), 'findings;', len(expected), 'expected; extra:', sorted(found - expected), 'missing:', sorted(expected - found))
PY

# 2. 清單相符後，同樣的參數加 --apply（actor 是站主的管理員 email）；預期 rejected 115、already_rejected 0、missing 0
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-foreign-place-scan \
  --skip-ids-file /tmp/foreign-guides-keep-ids.txt --apply --actor-email <admin>

# 3. 再跑一次第 1 步：預期 findings 0、skipped 3
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-foreign-place-scan \
  --skip-ids-file /tmp/foreign-guides-keep-ids.txt --verbose
```

不放檔案的等價寫法，三個 `--skip-id`：

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-foreign-place-scan \
  --skip-id 6da32c2d-96a5-48ac-bde3-edee52eb28d6 \
  --skip-id c4706b00-7c1d-4eac-9d5e-96229a20f0be \
  --skip-id eff4dc8f-6ea0-4392-abed-f7bf7d6e0e72 --verbose
```

- 第 1 步若多於 115 筆：多出來的是 2026-09-19 07:50 那次掃描之後才核准的列，不在這份判讀裡，退之前逐筆看標題。
- 退件理由是規則自己的「地點不符：內容講的是〈X〉，這個景點在〈城市〉（〈國家〉）」；上面形狀 3 說過 X 偶爾會是摘要撿到的
  字（台灣部落格寫成沖繩），只影響理由字句，不影響該不該退。
- 之後每次重跑掃描都要帶著這份 skip 清單（三個 id）；2026-09-12 那次少了一筆就是因為 skip 清單沒帶。

## 後續（不在本票範圍）

- `c4706b00` 的 `canonical_url` 已經 404，同文搬到英文 slug，而且 zh-hant 路徑下現在是英文內容。保留是就這條規則而言；
  死連結／語言不符要另開票處理（更新網址或重新探索這個景點的 zh-TW 介紹）。
- 2026-09-13 文件「沒退的」一節提到的 hoiana 文章，就是這裡的 `c4706b00`，已在 skip 清單裡。
