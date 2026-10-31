# C09 EN / JA 翻譯作者報告

完成 draft → critique → final 三步。EN、JA 各填 95 句、6 章，以及完整 title、description、tags 與 thumbnail 三欄；工作表僅保留 final，初稿未另存。

讀取完整 canonical video.json（含全部場景、來源）、兩語 worksheet 的 source/glossary/boundaries，以及已讀過的 caption-translate.md 規則。只改 text，所有 source/id/todo/glossary/boundaries/parts 等保護欄位維持不變。未執行 merge、git、provider、backend 或 source_hash 寫入。

EN title: Why Did Patagonia's Future Founder Urge Fewer Pitons in 1972?
JA title: 後のPatagonia創業者は、なぜ1972年にハーケンを控えるよう勧めた？

## 術語表

| 原詞 | EN | JA |
| --- | --- | --- |
| Patagonia / 巴塔哥尼亞標籤 | Patagonia / Patagonia label | Patagonia / Patagoniaのラベル |
| Chouinard-Equipment（原URL） | URL 原樣保留；公司名如需敘述用 Chouinard Equipment | 同左，不以片假名改寫品牌 |
| AI | AI | AI |
| 修納德 | Chouinard | Chouinard |
| Frost / Rowell / Bernstein（來源作者） | Frost / Rowell / Bernstein | 原 Latin 姓名保留 |
| 岩釘 | piton | ハーケン |
| 軟鐵岩釘 / 硬鋼釘 | soft-iron piton / hard-steel piton | 軟鉄製ハーケン / 硬い鋼製ハーケン |
| 金屬楔塊 / 可拆楔塊（岩塞） | metal chock / removable chock | 金属製チョック / 回収できるチョック |
| 固定岩釘 | fixed piton | 固定ハーケン |
| 岩縫 / 保護用裂縫 | crack / protection crack | 亀裂 / 安全確保に使う亀裂 |
| 敲入、拔出 | hammer in, pull out / remove | 打ち込む、引き抜く / 回収する |
| 鐵砧 / 煤爐 | anvil / coal forge | 金床 / 石炭炉 |
| 模具 / 壓床 | die / press | 金型 / プレス機 |
| 型錄前言 / 型錄書評 | catalog preface / catalog review | カタログの前書き / カタログ書評 |
| 攀岩者 / 大岩壁 | climber / big wall | クライマー / 大岩壁 |
| 優勝美地 / 酋長岩 / 文圖拉 / 加州 | Yosemite / El Capitan / Ventura / California | ヨセミテ / エル・キャピタン / ベンチュラ / カリフォルニア |

Chocks 使用較廣的被動楔塊器材名稱，不擅縮成某一款 nuts，不加入 cams；ハーケン與チョック全篇分開，也不改為膨脹螺栓。日本語地名使用慣用地名，品牌與上述作者 Latin 姓名保持原拼法。

## 來源名稱與時層

| 原件順序 | EN | JA |
| --- | --- | --- |
| 1 | Chouinard / Frost, 1967 equipment article | Chouinard／Frost、1967年の器材記事 |
| 2 | Chouinard / Frost, full reprint of the 1972 catalog preface | Chouinard／Frost、1972年カタログ前書きの全文再掲 |
| 3 | Rowell, 1973 catalog review | Rowell、1973年のカタログ書評 |
| 4 | Bernstein, interview report published in 1977 | Bernstein、1977年発表の取材記事 |
| 5 | Patagonia, 2012 company-history retrospective | Patagonia、2012年の社史回顧 |

說明欄原本只有參考 URL，兩語保留相同結構與全部五個 URL，未自行加入不同來源或來源日期。1967 當事人器材文、1972 前言全文重刊、1973 書評、1977 刊出採訪與2012品牌回顧維持分開；來源作者姓名沒有增添進未說出姓名的旁白。

## Critique 與已套用修正

| id / field | 初稿問題或檢查 | final 修正 |
| --- | --- | --- |
| JA c09r034 | Draft used 打ち抜き, which could mean die-cutting, for hammering in and pulling out pitons. | Changed to 打ち込みや引き抜き; kept the possible loosening and flaking of thin rock. |
| JA c09r011 / c09r029 | Draft had unnatural 持ち上がれて wording, and moved discussion of carrying gear after its benefit across the worksheet clause order. | Rewrote the carrying sentence naturally; put size classification and carrying first, then quick access and less fumbling. |
| EN+JA c09r072 | Literal calculation/計算 could obscure that the review recorded an accusation rather than a company admission of motives. | Used an admission of the company's motives / 内部の思惑を認めた記録; did not infer a financial motive. |
| EN c09r073 / c09r074 | Draft converted a rhetorical challenge into a firm no-right conclusion. | Restored Others wondered ... what right did they have? while keeping the view attributed to critics. |
| EN c09r087 / EN+JA c09r092 | Draft weakened the viewer's uncertainty and changed the clothing-factory question into a statement. | Restored you might still wonder, the explicit relationship question and the narrator's first person. |
| EN c09r097 | Draft sometimes it took could imply an observed, completed payback rather than an attributed estimate. | Used estimating that recouping the cost could sometimes take 5 to 10 years; kept the following independent-financial-report limitation. |
| JA c09r008 / c09r021 / c09r027 / c09r040 / c09r044 / c09r046 / c09r057 / c09r060 | Draft used broad mountaineering terms or ambiguous guide wording in a rock-climbing story. | Used クライマー/クライミング and クライミングガイドブック, without turning chocks into pitons or adding a modern technique claim. |
| JA c09r089 / EN+JA c09r065 | Draft pressing wording could lose shaping into new pitons; foothold wording could read as deliberate polishing. | Explicitly said metal was pressed into new pitons; used worn smooth / 磨かれて光って for footholds while retaining the preface's crack comparison. |
| EN+JA title / description / c09r085 / c09r093 | Checked temporal attribution and the risk of naming Patagonia as the 1972 catalog issuer or 1977 as the visit date. | Title frames Chouinard as Patagonia's future founder; description and narration keep 1977 as publication year, while the 1973 clothing label stays attributed to the later brand retrospective. |
| EN+JA all lines and metadata | Checked 95 line IDs, six chapters, every year and amount, 100 pitons/day, 2/hour, US$0.30 versus US$1.50, May–September, 72 pages and 5–10 years. | Kept each source layer, both authors' usage discussion, the review author's observations and judgments, and Chouinard's economic estimates distinct. |
| EN+JA tools / conditions / thumbnail / tags | Checked pitons versus removable chocks versus fixed pitons, suitability conditions, absence of a safety guarantee, and no-piton rather than no-rope climbing. | Kept conditional preference rather than a full sales stop; preserved thumbnail's one newline in both locales; omitted series names from title/tags and kept Patagonia plus piton/climbing search terms. |

## 疑點與保留限定

- 未提供實際 timeline、SRT 或 timed max_chars。長句保留完整數字、條件、否定與歸屬，沒有為軟字數刪去事實；時序、閱讀速度、配音可讀性及媒體品質尚未驗證。
- c09r079 原句只寫「同年」，沒有重說年份。EN 保留 that same year，JA 保留 同じ年，未因前面的1973書評而自行填成1973。若要字幕直接明說年份，需先由協調者依一手來源澄清繁中稿指涉；本次沒有擅改 source 或補年份。
- 1946 可回收硬鋼釘及英國較早使用的楔塊，均未說成 Chouinard 的發明；1957 可得性、沿岸鍛造、每小時2枚及價格比較，保留回憶／受訪歸屬。
- 1972 前言是合適路線優先考慮可拆楔塊，原本不用岩釘者繼續不用；必要時考慮固定岩釘並記入當地指南。沒有改成全面停售、不再製造、每種裂縫都適用或安全保證。
- 不帶的是岩釘，並非沒有繩索或其他裝備；成功僅限該次、該路線，不替每面岩壁作保。沒有把公司或書評作者觀點改成獨立普遍證明。
- 1977 明確只是採訪文章刊出年，沒有寫成已確認的到訪年份。1973 僅就品牌後來回顧的服裝標籤使用說明，不擅加獨立公司成立證明。
- 書評中的「說一套、做一套」指責仍是書評記錄的批評；服裝補貼器材及數千美元／5至10年回本仍為 Chouinard 的說法和估算，不是獨立財報，也未推論後續生產的財務動機。
- 保留第一人稱反應、對你的問句與原子句順序。縮圖 headline 保留原本一次換行、兩行結構；title/tags 省略兩個系列名稱，保留 Patagonia 與產品／攀岩搜尋詞。
- 除 c09r079 的原稿年份指涉與實際時序驗證外，沒有未解決的術語或數字翻譯疑點；仍待未參與翻譯者獨立評閱。

這是文字準備，不代表 SRT、dub、後台語言選擇、實際時序或成片驗收已完成。C03 的製作優先順序未改。
