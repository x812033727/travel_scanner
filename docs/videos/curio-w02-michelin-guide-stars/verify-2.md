# curio-w02-michelin-guide-stars 查核第二輪（R2 重製版）

- 查核日期：2026-11-21
- 查核者：獨立查核代理（Independent Fact Auditor，未參與 `curio-w02-michelin-guide-stars` R1／R2 稿件撰寫與第一輪查核）
- 查核對象：
  1. `docs/videos/history-curiosity/topic-checks/W02.md`（71 列查核基準與查核限制）
  2. `docs/videos/curio-w02-michelin-guide-stars/verify-1.md`（第一輪查核判定與修正要求）
  3. `docs/videos/curio-w02-michelin-guide-stars/video.json`（R2 定稿：`youtube.title`、`youtube.description`、`thumbnail`、28 筆 `sources`、81 景 `scenes[].data.prompt` 與 `t001`–`t091` 共 91 句旁白）
  4. `docs/videos/curio-w02-michelin-guide-stars/claims.md`（R2 逐句出處對照表，共 91 列）
- 工具檢查：`node tools/video/cli.mjs lint --slug curio-w02-michelin-guide-stars` → `zh-TW` 本體 **0 errors、0 warnings**（僅外語舊版 `i18n/*.json` 待 R2 定稿後重翻之例行提示），預估片長 10.1 分鐘、91 句、2,472 spoken units、10 個章節。

## 結論

**通過（PASS）。** 事實錯誤 **0**、超譯／過強表述 **0**、來源限制違反 **0**、畫面人物／商標違規 **0**、NOT FOUND 引用 **0**。

---

## 逐句查核對照表（`t001`–`t091`）

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| t001 | 1900 年創刊時法國輪胎公司免費送的小冊子；一到三星 | CONFIRMED | 1889 法國輪胎公司（#1）、1900 首版 35,000 本免費（#3）、一至三星制度（#14） | MICHELIN Guide About Us / History 存檔 | https://web.archive.org/web/20241227184206/https://guide.michelin.com/en/about-us | ✅ |
| t002 | 坊間總傳餐廳能買星；各地觀光單位公開掏錢把指南請進城市 | CONFIRMED | 「坊間總傳」標示流傳說法（#45）；各地觀光單位公開出資引進（#24 #34 #38 #41 #42） | Asia Business Daily；CapRadio 存檔；Colorado Sun | https://coloradosun.com/2025/09/19/do-colorado-cities-pay-to-have-restaurants-reviewed-for-the-michelin-guide/ | ✅ |
| t003–t004 | 2026-07 台北發布會頒 61 家星級餐廳，交通部長致詞；照觀光署提供的資料由其管轄單位合作引進 | CONFIRMED | 2026-07-21 台北典禮（#55）、61 家星級（#57）、部長致詞標明「照觀光署提供的資料」（#56 #63） | 產經新聞網 2026；聯合新聞網 2026 | https://www.1111.com.tw/news/jobns/166823 | ✅／△ |
| t005–t006 | 2017 年韓國國會追問首爾版合約金額；同年外媒對比提到「美國城市從沒付過錢」，幾年後美國破功 | CONFIRMED | 2017-10 國會監查（#25 #28）；WaPo 2017 經 Eater 轉述（#37）與 2019 加州付費（#38） | The Korea Times 2017；Eater 2018 | https://www.eater.com/2018/7/18/17540672/michelin-guides-restaurants-tourism-bangkok-thailand-south-korea-singapore-funding | ✅／△ |
| t008–t014 | 1889 克萊蒙費朗創立輪胎公司、車少；1900 首版 35,000 本免費送，含地圖、換胎、加油、食宿 | CONFIRMED | 「in Clermont-Ferrand in central France in 1889 … 35,000 copies were given out for free」（#1 #2 #3） | About Us、History 存檔 | https://web.archive.org/web/20250115052246/https://guide.michelin.com/kr/en/article/features/history-michelin-guide | ✅ |
| t015–t016 | 法國汽車媒體與《遠見》引述統計全法登記 2,897 輛；如果這數字沒錯平均一車 12 本 | CONFIRMED | L'argus「2 897 voitures」與遠見「僅2897輛」；35,000÷2,897≈12.1，保留「如果這數字沒錯」（#4） | L'argus；遠見 2010 | https://www.largus.fr/actualite-automobile/la-saga-du-guide-michelin-3690383.html | △ |
| t018–t019 | 百年史傳記作者指無證據顯示送書讓輪胎賣更好；126 年共有三種買單的人，第一種為米其林本業 | CONFIRMED | 達蒙「沒有證據顯示指南增加輪胎銷量」（#5）；1900–2026 共 126 年、三種買單人（#3） | 關鍵評論網 2024 | https://www.thenewslens.com/article/198852 | △ |
| t021–t027 | 官網記載 1920 安德烈・米其林見指南墊在輪胎行工作台下及付費名言；1920 改賣七法郎並撤除付費廣告 | CONFIRMED | 標明官網軼事（#8）、名言（#10）、1920 定價 7 法郎（#11）與同步撤除付費廣告（#12） | About Us、台灣官網存檔 | https://web.archive.org/web/20260722031649/https://guide.michelin.com/tw/zh_TW/about-the-michelin-guide-taipei | ✅／△ |
| t028–t032 | 1926 首標單顆星滿百年；五年後擴成一到三星（其餘不標星），1936 公開標準；二星繞道、三星專程，「我覺得」量開車距離 | CONFIRMED | 「In 1926 … single star. Five years later … in 1936」（#14 #15 #16）；開車距離標明「我覺得」 | About Us、台灣官網存檔；食尚玩家 2026 | https://supertaste.tvbs.com.tw/esg/360622 | ✅ |
| t034–t036 | 照米其林官方說法神祕客全職、不掛鉤外部、匿名多次、餐費自付；《天下雜誌》寫年均吃 250 家 | CONFIRMED | 標明「照米其林官方的說法」（#13 #17）與單一二手來源「《天下雜誌》寫過」（#19） | 台灣官網存檔；天下雜誌 2017 | https://www.cw.com.tw/article/5086023 | △ |
| t038–t042 | 美國餐飲媒體 Eater 引述《金融時報》2011 年虧逾 2,400 萬美元；財報同年母集團營收逾 200 億歐元；第三種買單人觀光單位；2016 起五亞城登場；2017 經 Eater 轉述前高層對《華郵》談贊助 | CONFIRMED | 標明 Eater 引述 FT（#20）、財報 207.19 億歐元（#21 #71）、五城（#23）、經 Eater 轉述 WaPo（#24） | Eater 2018；Tyrepress 2012 | https://tyrepress.com/2012/02/michelin_claims_strategic_validation_in_2011_financial_report | ✅／△ |
| t044–t048 | 2017-10《韓國時報》報議員宋基錫稱公社至 2020 付約 20 億韓元（折合 180 萬美元）、官員拒談；被指控收錢換出書非買星；出版前三個月關門義式餐廳上榜與米其林回應 | CONFIRMED | 標明議員說法 `2 billion won ($1.8 million)` 與官員拒談（#22 #28）；切清指控範圍（#31）；出版前三個月關門與回應精準（#25 #26） | The Korea Times 2017 | https://www.koreatimes.co.kr/amp/lifestyle/travel-food/20171024/credibility-of-michelin-guide-seoul-questioned | ✅／△ |
| t049–t053 | 同篇店主稱有人推銷摘星顧問、米其林否認；兩年後韓媒轉述 KBS 報付顧問費得星、另有店主提告稱被討年付 5,000 萬韓元；米其林否認稱內部查無證據，提告查無公開處分報導 | CONFIRMED | 標明轉述與「她說」、不念店名與姓名，如實呈現否認與查無公開處分報導（#27 #66 #67 #68 #69） | Korea Times 2019；Wikitree 2019；에너지경제 2019 | https://www.koreatimes.co.kr/lifestyle/travel-food/20191203/s-korean-chef-takes-legal-action-against-michelin-over-pay-for-star-collusion | △／⚠ |
| t054–t056 | 經 Eater 轉述美國城市從沒付錢只撐兩年；2019 加州觀光局證實付 60 萬美元擴出舊金山灣區 | CONFIRMED | 標明經 Eater 轉述（#37）；Visit California 2019 付 $600,000 擴出灣區（#38 #39） | CapRadio 存檔 | https://web.archive.org/web/20201029163331/https://www.capradio.org/articles/2019/05/29/michelin-dining-guide-honors-three-sacramento-restaurants/ | ✅ |
| t057–t060 | 早兩年的一七年二月泰國內閣推五年相關觀光計畫核准 1.435 億泰銖（不等於全給米其林）；2021 年底續約五年，新聞稿稱 2019 外國客餐飲花費翻倍（出錢方成績單） | CONFIRMED | 2017-02 核准 143.5M 泰銖且明言不等於全給米其林（#33）；2021-12 續約五年與出資方自述翻倍（#34 #35） | Khaosod 存檔；泰國觀光局 2021 | https://www.tatnews.org/2021/12/acclaimed-michelin-guide-thailand-gets-5-year-extension-from-2022-2026 | ✅／△ |
| t061–t066 | 2023 亞特蘭大三年 100 萬美元；科羅拉多報紙查核 2023 起各出 7–10 萬美元、錢不保證拿星只確保評審來；《波士頓環球報》評論酸小鎮被關門外；2025-10 米其林坦言需觀光夥伴分攤差旅 | CONFIRMED | 逐項對齊 #41 #42 #43 #44（標明評論）與 #70（米其林 2025-10 自述） | Colorado Sun 2025；Boston Globe 2025；The Star 2025 | https://www.thestar.com.my/lifestyle/travel/2025/10/23/michelin-wants-us-to-trust-its-hotel-ratings-but-should-we | ✅／△ |
| t068–t071 | 《遠見》寫爭取八年、2018-03 首版；公視報首發上千萬元付秘密客來台評選等費用 vs 前一年《天下》寫米其林支付；當年官方未說明外傳預算，台灣這筆誰準、總額多少公開報導都查不到 | CONFIRMED | 完整落實 #46 #48 #49 #50 #62 之「台灣這筆」「當年」「公開報導查不到」且不念外傳金額 | 遠見 2017；公視 2019；天下 2017 | https://news.pts.org.tw/article/454636 | △／⚠ |
| t072–t075 | 2024-08 美食展交通部長稱米其林已「同意」再增兩縣市；2025 實增新北、竹縣、竹市三個，觀光署自稱十年計畫成果；回收部長致詞鉤子 | CONFIRMED | 逐項對齊 #52 #53 #54 #56 #63 | 中央社 2024；台灣官網 2025 存檔；產經新聞網 2025 | https://www.cna.com.tw/news/aopl/202408020072.aspx | ✅／△ |
| t077–t082 | 七月典禮評選七地、61 家落五地、前一年納入的新北與竹市掛零；台南 2022 納入等四年到 2026 首星且開業不到一年；「我認為」當成買星紀錄撐不住 | CONFIRMED | 逐項對齊 #32 #53 #57 #58 #59 #60 #61，個人推論標明「我認為」 | 聯合新聞網 2026；產經新聞網 2026 | https://udn.com/news/story/7270/9641657 | ✅ |
| t083–t091 | 主打撤廣告自費試吃建立信任；拆清「請指南進城的差旅推廣費」與「餐廳摘星（米其林強調不影響、查不到官方或法院認定買星）」兩筆帳；官方故事工作台與 126 年三種買單人；互動結尾不提下一支 | CONFIRMED | 逐項對齊 #3 #8 #11 #12 #17 #32 #38 #42 #45 #49 #56 #69 #70 | 同上各列 | — | ✅ |

---

## 標題、說明欄、縮圖、`sources` 與 81 景 `prompt` 總檢

- **標題、說明欄、縮圖**：`heimao-left` 版型，`headline`（`"米其林**憑什麼收錢？**"`）與 `sub`（`"1900 年免費送，如今城市掏錢請"`）不破梗、未聲稱買星，且已修正舊版副標問題；說明欄移除內部備忘雜訊並保留無合作與 AI 生成揭露。**PASS**。
- **`sources`（28 筆）與 `claims.md`（91 列）**：`claims.md` 與 `video.json` 逐字同步，所有查核列來源 100% 收錄且零孤兒連結。**PASS**。
- **81 景 `scenes[].data.prompt`**：零品牌名、零公司名、零真名、零禁用負面詞或畫風字；在世與 1956 年後人物零入畫亦無路人替身；年代、地點與數量（12 本、7 銀幣、5 釘、6 城鎮牌、7 釘、7 盤 5 花 2 空）全數吻合。**PASS**。

VERDICT: PASS
