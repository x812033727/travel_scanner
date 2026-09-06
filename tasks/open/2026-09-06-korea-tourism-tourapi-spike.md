---
id: 2026-09-06-korea-tourism-tourapi-spike
title: TourAPI（韓國觀光公社）可行性驗證：先確認拿得到金鑰、連得上、資料量夠不夠
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-09-06T13:17:39Z
completed_at:
branch:
depends_on: []
scope:
  - docs/korea-tourism-tourapi.md
  - docs/hotspot-intelligence.md
  - tools/probe_tourapi.py
---

# TourAPI（韓國觀光公社）可行性驗證：先確認拿得到金鑰、連得上、資料量夠不夠

## Why

**先講結論：這張任務刻意不寫程式。** 三份獨立的對抗式查證都得到同一個結論——TourAPI 的技術面站得住腳，但有三個「不是工程問題」的關卡還沒過，其中任何一個沒過，實作就白做。所以這是一張 spike：把三個關卡問出答案、寫進 `docs/korea-tourism-tourapi.md`，然後才決定要不要開實作任務。也因為使用者現在看不到任何差別，優先度是 P3。

### 這件事到底能不能讓韓國「解鎖」——不能，這點要先講清楚

產品對韓國的發布守門和其他國家不同。`has_exact_map_identity()`（`apps/api/app/hotspots/maps.py:17-24`）在 `country_code == 'KR'` 時只認 NAVER 精準地點頁，Google Place ID 不算：

```python
EXACT_NAVER_PLACE_PREFIXES: tuple[str, ...] = (
    "https://map.naver.com/p/entry/place/",
    "https://map.naver.com/v5/entry/place/",
)
```
（`apps/api/app/hotspots/maps.py:7-10`）

`build_map_links()`（`maps.py:27`）在 `map_match_status != "verified"` 時回 `[]`（`maps.py:42`），KR 分支再要求精準 NAVER 網址（`maps.py:44`）。`_planner_eligible()`（`apps/api/app/hotspots/service.py:1085-1097`）同時要 `map_match_status == 'verified'` 和非空的 `map_links`；美食目錄的 SQL 過濾器 `publishable_merchant_filters()`（`apps/api/app/foods/publication.py:22-52`）也把同一條規則寫進 `exact_identity`。

**TourAPI 給的是座標（`mapx`/`mapy`）和文案，不是 `map.naver.com/p/entry/place/…` 識別碼。** 所以純粹「接一個內容來源」的版本，使用者端零可見變化，只會把審核佇列塞得更滿。真正能讓首爾 AI 行程草稿不再空白的，是「KTO 的 contentid 算不算韓國的精準地圖識別」這個產品決策，那是擁有者要拍板的事，而且和 `tasks/open/2026-09-06-naver-maps-key.md`（`blocked`，owner `claude-fable-5-1`）是同一個決策的兩面。那張任務的 Notes 寫著「不要試圖繞過這條規則」，理由是 Google 的韓國地圖覆蓋不完整——KTO 自己的座標不是 Google 的座標，論證不同，但仍需擁有者明確同意。

**如果使用者拿到 NAVER 金鑰，這張任務的價值大幅縮水**：現有管線就能發布 88 筆 KR 種子、65 筆 pending 景點、67 家 KR 店家，不需要新供應商。**開工前先問使用者 NAVER 金鑰申請到哪了。**

### 已查證的 API 事實（不要再查一次）

**端點與版本。** 現行路徑一律以 `2` 結尾，任何引用 `KorService1` / `areaBasedList1` / `detailCommon1` 的教學都是已退役的世代。

- 國文：`https://apis.data.go.kr/B551011/KorService2`（data.go.kr 資料集 `15101578`，`한국관광공사_국문 관광정보 서비스_GW`，登錄 2022-06-24、修改 2026-02-26，日更一次）
- 中文繁體：`https://apis.data.go.kr/B551011/ChtService2`（資料集 `15101769`，`한국관광공사_중문 번체 관광정보서비스_GW`，登錄 2022-06-29、修改 2026-02-26）
- 主要 operation：`areaBasedList2`（依地區列出）、`locationBasedList2`（依座標半徑）、`searchKeyword2`（關鍵字）、`searchFestival2`（節慶，帶日期）、`detailCommon2`（含 `overview` 長文）、`detailIntro2`（營業時間／菜單，schema 依 type 而異）、`detailImage2`（圖片清單）、`areaBasedSyncList2`（增量同步，帶 `showflag` 墓碑欄位與 `oldContentid`）
- 官方多語規格書自己寫錯：它叫你代入 `https://apis.data.go.kr/B551011/JpnService/~~`（沒有 `2`）。照抄會得到死路徑。

**認證。** `serviceKey` 走 query parameter（URL-encoded），不是 header、不是 OAuth。`MobileOS` 與 `MobileApp` 兩個參數是**必填**，少給會回錯誤碼 `11 NO_MANDATORY_REQUEST_PARAMETERS_ERROR`。`MobileOS` 的合法值是 `IOS` / `AND` / `WIN` / `ETC`（是 `WIN`，不是 `WEB`）。預設回 XML，`_type=json` 才給 JSON。

**繁體中文是第一方服務，但語言之間各自獨立。** 九個語系（KOR/ENG/JPN/CHS/CHT/GER/FRE/SPN/RUS）各是一個 data.go.kr 資料集、各需一次 활용신청、各有自己的配額桶。**一把金鑰不會同時開兩個語系。**

**`contentTypeId` 國文與多語不同**，這是最常見的整合錯誤，而且錯了不會報錯、只會靜靜回空：

| 類型 | 國文 | 多語（含 CHT） |
| --- | --- | --- |
| 관광지 | 12 | 76 |
| 문화시설 | 14 | 78 |
| 축제·공연·행사 | 15 | 85 |
| 레포츠 | 28 | 75 |
| 숙박 | 32 | 80 |
| 쇼핑 | 38 | 79 |
| 음식점 | 39 | 82 |

**`areaCode` / `sigunguCode` / `cat1..cat3` 已死。** data.go.kr 的參數表把它們標為「미사용항목(삭제예정)」。它們是 Optional，所以送進去不會報錯，只會被忽略而回傳**全國**的 `totalCount`——看起來完全正常，但數字是錯的。現行過濾參數是 `lDongRegnCd`（首爾 `11`、釜山 `26`）與 `lDongSignguCd`，分類用 `lclsSystm1/2/3`。

**座標直接給。** 清單與明細都帶 `mapx`（WGS84 經度）/ `mapy`（WGS84 緯度）。實測覆蓋率：KOR 49,720/49,772（99.90%）、CHT 14,472/14,472（100%）。`coordinate_source_type='official_tourism'` 已經在 `DURABLE_COORDINATE_SOURCES`（`apps/api/app/locations/coordinates.py:6-8`），所以 TourAPI 座標可以合法地耐久寫入——這是整件事技術上最強的論點。`apps/api/app/places/naver.py:29` 的 `_coordinate()` 與 `:41` 的 `_in_korea()` 可直接沿用。

**繁中語料的真實樣貌（三份查證獨立重跑後一致）。** CHT 全庫 14,472 筆，其中 10,797 筆（74.6%）是 `[事後免稅店]` 退稅商店；扣掉購物後，**首爾約 500 筆、釜山約 167 筆**可用（景點+文化：首爾 355、釜山 121）。餐廳：**CHT 首爾 70 家、釜山 13 家**，對比國文的 1,604 與 520。所以「有繁中就不用翻譯」是錯的——餐飲一定要走機器翻譯。CHT 的 `overview` 品質好（99.56% 有值，首爾景點中位數約 213 字）但量少。

**contentid 跨語系不互通。** 14,472 筆 CHT id 沒有任何一筆出現在 49,772 筆 KOR id 中。景福宮在國文是 `contentid=126508`/`contenttypeid=12`，在繁中是 `332517`/`76`，座標卻位元級相同。要對接只能靠 CHT 標題的韓文括號（`景福宮(경복궁)`）；全庫命中率約 91%，但**限縮到真正想要的景點+文化類別後只剩首爾 68.5%、釜山 74.4%**。

### 授權：可商用，但有一條會咬人的紅線

`cpyrhtDivCd` 逐筆、逐圖標示。KOGL（공공누리）定義：

- **Type1**：出處標示 ／ 可商用 ／ **可改作**
- **Type3**：出處標示 ／ 可商用 ／ **禁止變更與二次著作**

兩個資料集頁面都明寫「공공누리 1유형, 3유형 이미지 제공됨」——Type3 確實在資料流裡。而且 Type3 的「변경금지」在文體部與韓國著作權委員會的定義裡逐字包含「**형식의 변경**」（格式變更）。**這代表 `next/image` 最佳化、CDN transform、自己產縮圖、裁切成卡片比例，對 Type3 圖片都是違約**，而 TourAPI 이용약관 제11조允許 KNTO 因此中止供應。

**出處標示對所有類型都是強制的**（`knto.or.kr/helpdeskCopyrightguide` 逐字："제 1유형을 포함하여 어느 유형이든 출처…는 반드시 표시하여야"），內容須含發行年、機關名、機關首頁 URL、以及有署名時的作者名，線上使用還須提供連結。機關 URL 用 `kto.visitkorea.or.kr`。另有兩條禁令：不得用於損害被攝者名譽／人格權，不得作為企業 CI/BI；KOGL Type1 條款也禁止讓第三方誤以為公家機關與使用者有特殊關係或背書。

### 配額：把「1,000」當成永久天花板來設計

兩個資料集都寫：심의유형「개발단계 : 자동승인 / 운영단계 : 심의승인」、신청 가능 트래픽「개발계정 : 1,000 / 운영계정 : 활용사례 등록시 신청하면 트래픽 증가 가능」。

**但同一頁的英文版「Application for Use」寫的是「Development level : allowed / Operation level : Not allowed」，而且兩個資料集都一樣。** 有人跑了對照組：KMA 短期預報資料集（15084084）同一欄位寫的是「Operation level : allowed / Development account: 10,000」——所以這是逐資料集的設定，TourAPI 的正式階段申請確實被關著，不是入口網站的預設值。任何需要正式流量的計畫都建立在一個沒解決的矛盾上。

## Definition of done

- [ ] docs/korea-tourism-tourapi.md 存在，且對下列三個關卡各寫下一個帶日期與出處的明確答案（「問了但沒回」也算答案，要寫是誰在哪天問的）
- [ ] 關卡 A（帳號）：非韓籍申請者能否取得 data.go.kr 金鑰，有書面答覆或明確的替代路徑（韓國在地協作者／韓國法人／KNTO 回信）
- [ ] 關卡 B（連通性）：從正式機 VPS egress 對 apis.data.go.kr 的實測數字——嘗試次數、成功次數、延遲分佈；失敗時記錄是否已向 data.go.kr 註冊 VPS IP 並重測
- [ ] 關卡 C（資料量）：以 lDongRegnCd=11 與 lDongRegnCd=26 取得 KorService2 與 ChtService2 的首爾／釜山 totalCount，並與同一次未加地區參數的全國 totalCount 對照，證明過濾確實生效
- [ ] docs/hotspot-intelligence.md 的來源政策表多一列 TourAPI，Status 反映關卡結果（Evaluating／Enabled／Rejected），並寫明可耐久保存的欄位與圖片的 KOGL 限制
- [ ] tools/probe_tourapi.py 可重跑，任何人不必重讀本任務就能重現關卡 B 與 C 的數字
- [ ] 三個關卡全過時，開一張實作任務（scope 見 Notes）；任一關卡沒過時，本任務以「不可行／暫緩」結案，理由寫在 docs/korea-tourism-tourapi.md 裡

## Steps

- [ ] 先問使用者兩個問題並把答覆記進 docs/korea-tourism-tourapi.md：(1) NAVER 金鑰申請進度如何——若即將到手，本任務應直接降級或關閉；(2) 是否願意讓 KTO 的 contentid 充當韓國的精準地圖識別，或明確拒絕。第二題若是「否」，本任務只剩座標與繁中文案的價值，請照實記錄。
- [ ] 建立 docs/korea-tourism-tourapi.md，先把本任務 Why 段的已查證事實搬進去成為基準文件（端點、認證、contentTypeId 對照表、lDongRegnCd、KOGL Type1/Type3、配額矛盾），之後每過一個關卡就補一節。
- [ ] 關卡 A：到 https://auth.data.go.kr/sso/common-signup 實際嘗試註冊，把看到的會員類型與步驟原樣記下。同時寄信給 tourapi@knto.or.kr（電話 070-4287-3219）問兩件事：非韓國居民可否取得 TourAPI 金鑰；15101578 與 15101769 的 운영단계 활용신청 是否開放、1,000 的配額是每個 API 還是每個帳號。副本可寄 opendata_help@nia.or.kr。
- [ ] 關卡 A 備援：同步申請 Visit Seoul API 金鑰（https://api.visitseoul.net/apiinfo/apiovr/view/3?lang=en），其金鑰頁未載明國籍或韓國法人要求。申請時要注意它要求登記「呼叫端 URL」且只允許該 URL 呼叫，機制未明，BFF 從伺服器端呼叫是否適用要問清楚。
- [ ] 撰寫 tools/probe_tourapi.py：只依賴 httpx（apps/api 已有此相依），參數為 service key、service 名稱（KorService2/ChtService2）、lDongRegnCd 與重複次數；帶桌面瀏覽器 User-Agent；同時解析 JSON 與 XML 兩種錯誤格式，且不可以 HTTP 200 當成功判準（實測錯誤是 HTTP 403 帶 JSON body）；輸出每次嘗試的延遲與結果碼，最後印出成功率。
- [ ] 關卡 B：把 tools/probe_tourapi.py 拿到正式機 VPS 上，用 api 容器的 python 執行（見 How to verify），連續打至少 20 次，記錄成功率與延遲。三份獨立查證在本地分別得到 1/15、0/17、0/3 的成功率，而同一時間 www.data.go.kr 與 api.visitkorea.or.kr 都秒回——所以「打得通」目前是未證實的。失敗就用錯誤碼 32 UNREGISTERED_IP_ERROR 的線索去 data.go.kr 登記 VPS 固定 IP，再測一次。
- [ ] 關卡 C：用 dev key 各打兩次，KorService2 與 ChtService2 各一組：areaBasedList2?lDongRegnCd=11&numOfRows=1 與 lDongRegnCd=26&numOfRows=1，再打一次完全不帶地區參數的當對照。三個數字都記進文件；若加了 lDongRegnCd 之後 totalCount 沒變小，代表參數沒生效，數字不可信。
- [ ] 更新 docs/hotspot-intelligence.md 的來源政策表：新增 TourAPI 一列。保留欄位要寫清楚——contentid、mapx/mapy、來源網址、名稱、overview 可耐久保存（這點與 Google Places 那一列相反，別照抄），圖片只能依 cpyrhtDivCd 原樣顯示且 Type3 禁止任何格式變更。
- [ ] 依三個關卡的結果收尾：全過就用 npm run tasks -- new 開實作任務（scope 見 Notes），把本文件連結寫進去；任一沒過就在 docs/korea-tourism-tourapi.md 寫下結論並把本任務 done 掉，讓下一個人不必重來。

## How to verify

```bash
# 關卡 B —— 從正式機的實際 egress 測，不要在本機測
scp tools/probe_tourapi.py <vps>:/tmp/probe_tourapi.py
ssh <vps> 'docker compose -f docker-compose.prod.yml exec -T api python - < /tmp/probe_tourapi.py \
  --service KorService2 --ldong 11 --repeat 20'
```

預期輸出是「成功 N/20、延遲中位數 X 秒」。目前尚無任何一次從正式機成功的紀錄；本機的三次獨立實測分別是 1/15、0/17、0/3。

```bash
# 關卡 C —— 兩個服務各三個數字，過濾有沒有生效看得出來
python tools/probe_tourapi.py --service KorService2 --ldong 11 --count-only   # 首爾
python tools/probe_tourapi.py --service KorService2 --ldong 26 --count-only   # 釜山
python tools/probe_tourapi.py --service KorService2 --count-only              # 全國，對照組
python tools/probe_tourapi.py --service ChtService2 --ldong 11 --count-only
python tools/probe_tourapi.py --service ChtService2 --ldong 26 --count-only
python tools/probe_tourapi.py --service ChtService2 --count-only
```

判準：前兩個數字必須明顯小於對照組。若三個一樣大，就是 `lDongRegnCd` 沒生效（極可能是誤用了已廢止的 `areaCode`），數字作廢。作為對照，這次查證從 KNTO 自家的入口索引量到的參考值是 KOR 首爾 8,011、KOR 釜山 2,227、CHT 首爾約 4,600、CHT 釜山 1,074——但那是無契約的內部端點，只能當量級參考，不可寫成 API 的保證值。

```bash
# 文件與看板檢查
npm run check:tasks
```

本任務不動 `apps/api` 與 `apps/web` 任何檔案，所以 lint／typecheck／pytest 不會因它而變動；`tools/probe_tourapi.py` 是獨立腳本，不進 `npm run test:tools`（該指令只掃 `tools/*.test.mjs`）。

## Notes

### 授權立場（決定了就不要再吵）

- 兩個資料集皆為**免費**、`이용허락범위 제한 없음`，但描述另外把圖片切出來走 KOGL：「공공누리 1유형, 3유형 이미지 제공됨」。引用「無限制」時必須把圖片的但書放在旁邊。
- **Type1 可改作，Type3 不可。** 且 Type3 的「변경금지」在政府定義中逐字含「형식의 변경」。所以 `next/image` 最佳化、CDN transform、自產縮圖、裁切比例，對 Type3 圖片一律違約。要用就用 KNTO 自己給的 `firstimage2` / `smallimageurl`，並對該路徑關掉最佳化。
- `cpyrhtDivCd` 必須**逐筆且逐圖**保存，遇到不認識的值要**拒絕**而不是預設顯示。KNTO 自己的代碼表另有 Type2、Type4（禁商用）與 Type5（공사만사용）。
- 出處標示對所有類型強制，內容含發行年、機關名、`kto.visitkorea.or.kr`、有署名時的作者名，線上須附連結。文案不得暗示 KTO 背書（例如把韓國內容標成「官方」而與 KTO 署名並列）。禁止用於損害被攝者名譽／人格權，禁止作為企業 CI/BI。
- **本任務的建議是：圖片直接排除在第一版之外。** 資料庫裡目前沒有任何景點或店家的圖片欄位（`grep` 全 schema 只有 `trip_plans.cover_image_url`），沒有卡片會渲染照片。要做圖片就是 migration + 五語系卡片改版 + Type3 審查。Goal 那句話裡的「photos」不要當成範圍。

### 配額

- 開發帳號 **1,000**（入口網站慣例是每日，但資料集頁面沒有蓋上「일일」字樣，寫的時候要照實註明）。自動核准、即時發放。
- 正式階段的申請在這兩個資料集上被標為 **Not allowed**（見 Why）。**所有設計都必須在 1,000 的天花板下成立**：全量回填不可行（首爾+釜山國文清單約 10,238 筆，再加三個 detail 呼叫約 30,700 次，等於一個月冷啟動），只有小量（數百筆）匯入加上每晚 `areaBasedSyncList2` 差異同步塞得進去。
- 每秒上限存在但這兩個資料集沒公布數值（data.go.kr 問答板有「초당 서비스 요청제한 횟수 초과」的討論串）。客戶端一律要自己節流。
- 錯誤碼：`22` 配額用盡、`30` 金鑰未註冊、`31` 期限過期、`32` IP 未註冊、`11` 缺必填參數、`03` 無資料。`32` 的存在代表可以做 IP 白名單，這對固定 IP 的 VPS 有用。

### 仍未證實（UNVERIFIED），以及該讀哪一頁

- **非韓籍能否註冊 data.go.kr。** 三份查證中兩份實際打開 `https://auth.data.go.kr/sso/common-signup`，只看到 일반회원（만 14세 이상 **내국인**）、어린이 회원（**내국인**）、기업회원（**국세청에 등록된 사업자**）三種，第 4 步是 본인인증，`?lang=en` 無效；英文入口 `https://www.data.go.kr/en/index.do` 根本沒有註冊入口。反向證據是 gov.kr 的 TourAPI 服務頁（B55101100003）把 신청자격 寫成「개인 및 민간, 공공 등」且無需文件——但那描述的是服務，不是發金鑰的入口網站帳號。**這是第一號阻塞項，性質等同 `tasks/open/2026-09-06-naver-maps-key.md`。**
- **正式流量到底開不開放。** 讀 `https://www.data.go.kr/en/data/15101578/openapi.do` 與 `https://www.data.go.kr/en/data/15101769/openapi.do` 的「Application for Use」欄，並與韓文頁的 심의유형 對照；答案要由 tourapi@knto.or.kr 書面確認。
- **1,000 是每個 API 還是每個帳號。** 若是每帳號，KorService2 與 ChtService2 共用一桶。
- **apis.data.go.kr 從正式機打不打得通。** 本機三次實測都幾乎全滅，且是這個 gateway 專屬（同時間 www.data.go.kr、auth.data.go.kr、api.visitkorea.or.kr、knto.or.kr 都正常）。因為 v1 與 v2 路徑一起失敗，所以「KorService1 已於 2025-08-10 停用」這件事也只是旁證（data.go.kr 只列出 `*Service2`、Swagger 只有 `*2` operation），沒有讀到公告原文。
- **TourAPI 이용약관 제11／12／13조的原文**沒讀到——`api.visitkorea.or.kr` 是前端渲染的 SPA，`#/agrAgreement` 抓不到文字。內容（強制標示來源、違反可中止供應、資料不保證持續提供、韓國法院管轄）很可能正確，但不要當成已讀過的原文引用。
- **Visit Seoul API 是否已正式開放。** 其首頁仍掛著「Expected opening: End of October 2025」的公告，金鑰頁卻讀起來像已上線。它的配額完全未公布（條款只說會在網站公告），這比 TourAPI 明確的 1,000 更弱而不是更強。其分類數（Food 6,568 等）是七個語系的合計，zh-TW 的分拆未知，**不可拿來和 TourAPI 的「繁中首爾 70 家餐廳」做同基準比較**。
- **Type1/Type3 的實際比例**無法從入口索引量測（`cpyrhtDivCd` 不在索引 schema 裡），只有拿到金鑰打 `detailImage2` 才知道。

### 不要再重新論證的決定

- **不要在任務文案裡把「약 26만 건」（國文）或「약 8만 건」（繁中）當成 POI 數。** 兩者都是資料集頁的行銷數字，計的是所有 operation 的列數；「8만」更是逐字重複出現在英、日、繁中三個資料集頁上的樣板文字。實測的相異 POI 數是 KOR 49,772、CHT 14,472。
- **不要用 `areaCode=1` / `areaCode=6` 當首爾／釜山。** 那是已廢止參數，送進去不報錯只被忽略，會回全國數字。用 `lDongRegnCd=11` / `26`。另外 2026-07-01 起法定洞代碼大改（仁川新增區、광주+전라남도 併為 전남광주통합특별시 代碼 12），整個語料在那天被批次改寫且 `modifiedtime` 被集體推進到 26-06-30——任何靠 `modifiedtime` 的增量鏡像都要能承受「全庫一夜變髒」。
- **不要拿 `api.visitkorea.or.kr/hub/*.do`（`getTourDbInfo.do`、`getNuri.do`、`getArea.do`）當契約。** 本任務 Why 段裡所有覆蓋率數字都出自那個未公開的入口索引端點（KOR 回應 80.9 MB、CHT 18.2 MB，且 `areaCd` 欄在 58%／81% 的列上是空的，城市分佈是用 `addr1` 前綴推的）。只能當量級參考。
- **不要用 CHT `contentid` 當任何東西的鍵**（跨語系命名空間完全不相交），也不要只靠座標比對（KOR 自己就有 7,474 組完全重複的座標）。要對接就靠 CHT 標題的韓文括號，座標當 tie-breaker。
- **不要宣稱 TourAPI 解決營業時間排程。** `tasks/open/2026-09-06-opening-hours-aware-scheduling.md` 建立在 Google 的結構化 periods 上，而 `detailIntro2` 的 `usetime` / `restdate` 是自由文字散文，餵不進 `_safe_slots`，那張任務的 DoD 也明文禁止用散文猜營業時間。
- **不要碰 ranking 公式**（45% Wikimedia 瀏覽量／25% 成長／20% 編輯相關性／10% 信心度）。TourAPI 在這輪不得成為第五個計分項。
- **不要碰 `apps/api/app/hotspots/discovery.py`**（`ALLOWED_TYPES` 正在 `2026-09-06-measure-the-flood-before-widening-allowed` 底下被量測中）。

### 三個關卡都過之後，實作任務的建議 scope（本任務已預先確認不與現有任何 open 任務衝突）

```
apps/api/app/korea_tourism/        # 新套件：client.py、import_hotspots.py、cli.py
apps/api/app/config.py
apps/api/app/admin/service.py
apps/api/app/cli.py
apps/api/tests/test_korea_tourism.py
apps/web/components/admin-settings-panel.tsx
```

實作時的落點都已查過：`PROVIDER_DEFINITIONS` 在 `apps/api/app/admin/service.py:102`（`odsay` 那筆在 `:358-366` 可當範本，label/description 用繁中寫在 Python 裡沒問題，`tools/check-i18n.mjs` 只掃 `apps/web/{app,components,lib}/**/*.tsx`）；`_configured` 在 `:560`；`_production_test_required` 在 `:903`；`test_provider_connection` 在 `:1809`。`OFFICIAL_PROVIDER_HOSTS` 在 `apps/api/app/config.py:59-77`（`odsay_api_base_url` 在 `:76`），要加 `apis.data.go.kr`。`providerCategoryOf` 在 `apps/web/components/admin-settings-panel.tsx:89-120`，漏加會靜靜掉進「其他」，類別選 `content`。**在 `fieldMeta`／`secretLabels` 用字面 `label:`（先例：`amadeus_client_id: { label: "Client ID" }` 在 `:275`、`travelpayouts_marker: { label: "Marker" }` 在 `:227`）而不是 `localized: true`**，就不必動 `apps/web/messages/*/admin.json`，也就不會撞到 `2026-09-06-admin-panels-i18n-remaining`。

資料模型第一階段不需要 migration：`TravelHotspot`（`apps/api/app/models.py:396`）已有 `coordinate_source_type`（`:427`）、`coordinate_source_url`（`:428`）、`origin`（`:446`）、`review_status`（`:447`）、`metadata_json`（`:457`，是 `JSON` 不是 `jsonb`，禁用 `?`、`@>`、`<@`、`||`）；`FoodMerchantSource.source_type`（`:765`）的 CHECK 已含 `official_tourism`。`contentid` 先放 `metadata_json`（無唯一鍵，去重在 Python 做），要專屬欄位再開第二階段的 migration（目前 head 是 `apps/api/migrations/versions/0049_trip_place_candidates.py`，平行 session 會搶編號）。可抄的先例是 `apps/api/app/hotspots/candidate_sources.py`（只做取得、不做決定）、`apps/api/app/hotspots/candidate_import.py:40`（`persist_resolutions(..., apply=False)` 預設 dry-run，`CANDIDATE_ORIGIN` 在 `:28`）與 `apps/api/app/foods/trend_import.py`（開頭的 docstring 就是這類匯入的治理範本：一律 `review_status='pending'`、`is_active=False`、`map_match_status='unverified'`）。匯入務必設上限——上一次審核積壓是 482 筆，清掉它花了一整張 P2 任務和一整個 session。
