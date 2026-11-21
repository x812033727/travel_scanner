# curio-w08-claw-machine 查核第二輪（獨立唯讀覆核）

- 查核日期：2026-11-21
- 查核角色：獨立唯讀 Fact-Check Auditor（`verify-2` Round 3），未參與本集撰稿、亦未執行第一輪查核。
- 查核對象：
  - `docs/videos/curio-w08-claw-machine/video.json`
  - `docs/videos/curio-w08-claw-machine/brief.md`
  - `docs/videos/curio-w08-claw-machine/claims.md`
  - `docs/videos/curio-w08-claw-machine/verify-1.md`
  - `docs/videos/history-curiosity/pool/batches/w-heimao-02-20261119.json`（候選題 `N9075` 與來源紀錄 `WH12-S016`–`WH12-S020`、`WH12-S023`–`WH12-S025`）
- 來源實測：全數 8 筆一手／機構網址皆於 2026-11-21 獨立實抓 HTTP 200，並直接檢索原始 HTML／PDF／數位化專書原文核對每一筆日期、法條、金額、比例、機台數與專名。

## 總判定（Overall Verdict）

**`PASS`**

- 統計：`CONFIRMED`: **24** ｜ `NEEDS_TIGHTENING`: **0** ｜ `NOT FOUND`: **0**
- 所有年份、日期、幣別／金額（美元／美分／日圓／新台幣）、聯邦與台日法條條號、營收占比與機台數量皆與 8 筆一手／機構來源原文吻合。

## 五大合規領域總結

| # | 合規項目 | 判定 | 獨立覆核摘要 |
|---|---|---|---|
| 1 | **1956 人物紅線** | **PASS** | 全片旁白與全部提示詞皆未點名、未描繪任何在世或 1956 年後過世之真人。唯一於輔助檔案／專利出處引用之真人為美國專利 `US1882563A` 發明人 William D. Bartlett（逝於 1948 年，早於 1956 年紅線），正片僅以「有人拿到專利」帶過、畫面提示詞寫匿名 `a 1930s American mechanical inventor`。Mental Floss 受訪修復師、Sega 開發人員與台日官員均不點名、不入畫。 |
| 2 | **1962 成文法 vs. 嘉年華口述史分界** | **PASS** | 成文法（Pub. L. 87-840 司法部年度登記／永久烙印序號、`15 U.S.C. § 1178(3)` 法定三要件：非投幣、手搖曲柄、嘉年華／州郡博覽會專用）與嘉年華口述實務（自壓獎品 1 美元內、店員收 10 美分拉細繩解鎖手搖桿）及 FBI 砸機口述史完全分界，絕無混寫。 |
| 3 | **排除「1890 年代巴拿馬運河模型」誤傳** | **PASS** | 全文嚴格排除未經證實之 1890 年代傳聞，依 Bueschel (1993) *Arcade 1*（`WH12-S023`）準確定位於 1914 年巴拿馬運河通航完工後、約 1918 年紐約布魯克林誕生挖斗雛形。 |
| 4 | **台灣場主／台主分租商業中立性** | **PASS** | 客觀依經濟部規範（`WH12-S020` 第二點、第十點）介紹場主與台主雙層分租與資訊揭露規定，明確警示絕非躺賺，如實揭露飽和亂象、違規改裝、禁放現金／福袋／戳戳樂、禁止金錢買回、任意歸零視同非法電玩開罰與泡沫退潮；說明欄附無合作贊助聲明。 |
| 5 | **提示詞零版權 IP 角色／零商標／零數字** | **PASS** | 全部提示詞零版權 IP 角色（僅素色無版權幾何布偶與無字素色方盒）、零商標與品牌字樣、零畫面價格與招牌數字；生圖展開階段對告示牌與年代詞彙加註 `zero text, zero letters, zero numbers` 防護。 |

## 逐項主張查核表（24/24 CONFIRMED）

| # | 主張 | 判定 | 原文依據 | 來源 |
|---|---|---|---|---|
| 1 | 1951-01-02 美國《強森法》（15 U.S.C. §§ 1171–1178）將投幣靠運氣換財物機具視同賭博機，嚴禁跨州運送 | CONFIRMED | 15 U.S.C. Ch. 24（`Jan. 2, 1951`）& Mental Floss | `WH12-S017`, `WH12-S016` |
| 2 | 執法最嚴時，據古董機台修復師口述 FBI 曾拿大鐵鎚砸毀焚燒機台 | CONFIRMED | Mental Floss 口述史（`destroyed them with sledgehammers, then burned them`），正片與說明欄均標明口述 | `WH12-S016` |
| 3 | 2024 年度日本街機總營收 6,148 億日圓、景品遊戲 4,177 億日圓（占 68%／近七成） | CONFIRMED | JAIA 官方統計表（`6,148 億円`、`4,177 億円`、`68%`） | `WH12-S019` |
| 4 | 台灣長出 24 小時無人店並演化出經濟部規範正式定義之「場主」「台主」雙層分租 | CONFIRMED | 經濟部規範第二點(二)明定台主與場主定義 | `WH12-S020` |
| 5 | 夾娃娃機最早為迷你挖土機鐵斗；1914 年巴拿馬運河通航完工後蒸汽挖土機紅遍全美，約 1918 年布魯克林誕生雛形 | CONFIRMED | Bueschel (1993) *Arcade 1* p. 244, 257（一次大戰前尚無） | `WH12-S023` |
| 6 | 1926 年芝加哥投幣機展推出 1 美分四面玻璃木框 `Miniature Steam Shovel` 抓糖；同年 `Erie Digger` 問世 | CONFIRMED | *Arcade 1* p. 244 & Mental Floss（引 1935 *Automatic Age*） | `WH12-S023`, `WH12-S016` |
| 7 | 1928 年純機械手搖 `Panama Digger` 推出，挖斗機橫掃 1930 年代美國街頭 | CONFIRMED | *Arcade 1* p. 244, 257 | `WH12-S023` |
| 8 | 1932 年 William D. Bartlett 獲准美國專利 `US1882563A`（電動馬達 5 美分 `Miami Digger`，通電限時對準、雙纜繩自動放斗） | CONFIRMED | US Patent 1,882,563（1932-05-20 申請、1932-10-11 獲准）& Mental Floss | `WH12-S024`, `WH12-S016` |
| 9 | 1932 年電動機台箱底改鋪玉米粒，埋入銀幣與名錶 | CONFIRMED | Mental Floss（`silver dollar`, `kernel corn`, `watches`） | `WH12-S016` |
| 10 | 違反《強森法》最高罰 5,000 美元或判刑 2 年（§ 1176），機台沒收（§ 1177） | CONFIRMED | 15 U.S.C. §§ 1176–1177 | `WH12-S017` |
| 11 | 電動挖斗機從 1932 年至 1951 年風光近二十年（19 年） | CONFIRMED | 1932–1951 年表對照 | `WH12-S024`, `WH12-S017` |
| 12 | 1956 年 Chicago Coin 推出不掉實物獎品、純計分制 `Steam Shovel` | CONFIRMED | *Arcade 1* p. 283（May 1956） | `WH12-S023` |
| 13 | 1962-10-18 修法（Pub. L. 87-840）：跨州廠商須每年向司法部登記並永久烙印序號 | CONFIRMED | 15 U.S.C. §§ 1171, 1173 & DOJ 1962 指南 | `WH12-S017`, `WH12-S025` |
| 14 | 1962 年修法 `15 U.S.C. § 1178(3)` 唯一法定豁免三要件：非投幣、純靠手搖、限嘉年華或州郡博覽會 | CONFIRMED | 15 U.S.C. § 1178(3) & DOJ 1962 指南 | `WH12-S017`, `WH12-S025` |
| 15 | 據老攤商口述實務：獎品自壓 1 美元內避嫌、店員收 10 美分拉細繩解鎖手搖桿 | CONFIRMED | Mental Floss 口述史（與成文法清楚分離） | `WH12-S016` |
| 16 | 1970 年代末歐日跨海改造為上方滑軌吊爪並專夾絨毛玩偶；二十多年後於東亞翻紅 | CONFIRMED | Mental Floss（`trolley-style claw machines`）& Sega 年表 | `WH12-S016`, `WH12-S018` |
| 17 | 1985 年日本 Sega 推出初代 `UFO Catcher`（開發名 `Eagle Catcher`），鎖定女性與孩童、粉紅直立百貨櫥窗擺大門口、兩步驟先橫移再往深處操作 | CONFIRMED | 4Gamer 全文轉載 Sega 2020-06-23 35 週年官方新聞稿 | `WH12-S018` |
| 18 | 1991 年新版 `NEW UFO Catcher` 靠人氣布偶與賽馬玩偶引爆收藏潮（2001 第七代白色機身） | CONFIRMED | Sega 35 週年官方新聞稿（去品牌改稱可愛布偶與賽馬玩偶） | `WH12-S018` |
| 19 | 日本《風営法》第 23 條第 2 項原則禁止送獎與換現金；警察廳准許直接抓取，2001 年明文約 800 日圓以下、2022 年調升為 1,000 日圓以下 | CONFIRMED | JAIA 官方媒體頁（2001-09-20、2022-03-01 生安発第 30 号） | `WH12-S019` |
| 20 | 日廠開發不於一般商店零售的「遊樂設施專用景品」，批發價全數壓在上限之內 | CONFIRMED | JAIA 官方媒體頁原文 | `WH12-S019` |
| 21 | 2024 年度全日本景品遊戲設置台數突破 258,900 台（實為 258,903 台） | CONFIRMED | JAIA 2024 年度官方統計表（`258,903` 台） | `WH12-S019` |
| 22 | 台灣經濟部《自助選物販賣事業管理規範》明定具「保證取物」（現行上限新台幣 990 元、累投不歸零）與「對價原則」經評鑑為非屬電子遊戲機者免電玩牌照 | CONFIRMED | 經濟部規範（113.10.14 附件）第二點、第三點 | `WH12-S020` |
| 23 | 經濟部規範明訂店內須標明場主與台主資訊、聯絡方式及錄影監視告示 | CONFIRMED | 經濟部規範第十點(一)(二)(三) | `WH12-S020` |
| 24 | 台灣規範嚴禁擺放現金、福袋、戳戳樂及金錢買回，違規改裝或任意歸零視同未經評鑑之非法電子遊戲機開罰 | CONFIRMED | 經濟部規範第一點、第三點、第七點、第八點、第九點 | `WH12-S020` |

## 獨立開啟實測 HTTP 200 來源清單

| 來源編號 | 標題 | 網址 | 狀態 |
|---|---|---|---|
| `WH12-S023` | Bueschel (1993) *Arcade 1*（Internet Archive） | https://archive.org/details/arcade-1-1993-book-scans | HTTP 200 ✅ |
| `WH12-S024` | US Patent 1,882,563 (William D. Bartlett, 1932) | https://patents.google.com/patent/US1882563A/en | HTTP 200 ✅ |
| `WH12-S016` | Mental Floss〈Dime After Dime〉 | https://www.mentalfloss.com/fun/dime-after-dime-gripping-history-claw-machines | HTTP 200 ✅ |
| `WH12-S017` | 15 U.S.C. Ch. 24 (§§ 1171–1178) | https://www.govinfo.gov/content/pkg/USCODE-2020-title15/pdf/USCODE-2020-title15-chap24.pdf | HTTP 200 ✅ |
| `WH12-S025` | DOJ *Gambling Devices Act of 1962* | https://www.justice.gov/sites/default/files/criminal-oeo/legacy/2014/06/06/gamblingdvc-1962.pdf | HTTP 200 ✅ |
| `WH12-S018` | 4Gamer：Sega「UFO Catcher」35 週年官方發表文 | https://www.4gamer.net/games/999/G999905/20200623101/ | HTTP 200 ✅ |
| `WH12-S019` | JAIA：日本國內景品遊戲法規與 2024 年度統計 | https://jaia.jp/%E3%83%A1%E3%83%87%E3%82%A3%E3%82%A2%E3%81%AE%E3%81%BF%E3%81%AA%E3%81%95%E3%81%BE%E3%81%B8/ | HTTP 200 ✅ |
| `WH12-S020` | 台灣經濟部：《自助選物販賣事業管理規範》 | https://gcis.nat.gov.tw/elawAp/api/lawAttachment/243 | HTTP 200 ✅ |
