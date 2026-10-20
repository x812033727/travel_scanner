# B10 獨立事實查核紀錄

日期：2026-10-20（Asia/Taipei）。Reviewer：`/root/facts_b10_a30`。

本輪實際以 curl 經繼承的 HTTPS 代理讀取 6 個列入來源，保持 TLS 驗證，User-Agent 為專案 editorial 值。以下均為本輪讀到的內容，不沿用舊 review 的 sources_opened 或 PASS。原始頁面暫存於 repo 外 `/tmp/brand-facts-b10-a30`；本文件只留必要核對摘要。

## 來源讀取結果

| 索引（JSON零起算） | 來源 | HTTP | HTML字元數 |
| --- | --- | --- | --- |
| 0 | [西友（官方網站，西友的歷史）](https://www.seiyu.co.jp/company/history/) | 200 | 59791 |
| 1 | [公益社団法人日本印刷技術協会 JAGAT（石島暁子，2012年11月15日）](https://www.jagat.or.jp/past_archives/content/view/3934.html) | 200 | 6149 |
| 2 | [文化庁メディア芸術祭（第22回功勞賞，小池一子）](https://www.bunka.go.jp/j-mediaarts-festival/award/single/koike-kazuko/) | 200 | 37214 |
| 3 | [伊丹十三記念館（第14回伊丹十三賞，2022年）](https://itami-kinenkan.jp/award/award14.html) | 200 | 12158 |
| 4 | [ダイヤモンド・チェーンストアオンライン（2018年4月27日）](https://diamond-rm.net/flash_news/24602/) | 200 | 96489 |
| 5 | [Wikipedia日文版](https://ja.wikipedia.org/wiki/良品計画) | 200 | 427926 |

## must_verify 逐項判定

| 零起算主張索引 | 實際核對與必要邊界 |
| --- | --- |
| 0 | 西友官方沿革明載1980年PB無印良品誕生；JAGAT補足創設理念。 |
| 1 | JAGAT原文完整支持過度消費反命題、田中一光與堤清二、材料／工序／包裝三項，以及方針在田中過世後延續。 |
| 2 | 文化廳與伊丹十三記念館皆寫小池一子為creative director、1980參與創設，之後擔任advisory board。 |
| 3 | 維基百科本輪可讀文字中有31食品+9雜貨=40、田中以no brand goods和譯命名、口號由小池考案。保留attributed。 |
| 4 | 維基百科說明段1989六月為西友100%子公司，沿革表另有1990三月營業權受讓及1991七月倫敦。1983青山及杉本內裝亦在內。保留attributed，不稱1989已脫離西友。 |
| 5 | 維基百科明載2000年代折扣店台頭、衣料不振、業績惡化及2001松井就任改革。保留attributed。 |
| 6 | ダイヤモンド2018/04/27報導支持4/25命令、2015/6–2018/1、6現成+2訂製、標撥水實際沒有，以及工廠變更資訊傳遞錯誤；旁白按此報導歸屬，不把維基百科引朝日的布料供應變更說法混成同一官方結論。 |
| 7 | 維基百科仍明確標2025年8月期末，日本717+海外757=1474，含license/Café&Meal/IDÉE。這是帶日期的歷史數字，不是2026目前門市數。 |

## 本輪更正與限制

- 本輪實際重讀全部6個列入來源，更新checked日期；保留只能歸屬維基百科及報導的說法，不冒稱新增公司一手來源。
- 以本輪確認結果重寫caveats，保留兩種資訊傳遞說法、公司成立與營業權日期、2025店數的期間邊界。

- 沒有查詢正式站的既有集數，不能據此宣稱題目未製作；本收據核准企劃事實，不核准未來逐字稿、旁白、圖片或成片。
- 所有列入來源都讀得到HTML。無需新增 reviewer_only。A30的Wikipedia IKEA全文超過40,000字，但日期與one-way位於worker前40,000字內；B10維基百科worker文字31,403字，相關主張未超過上限。

最終企劃故事雜湊：`82031e4f43a4ddd5d3fff9e3a087ff36f891edb4142dd012cb171d843c5608f9`。以 `STORY_KEYS` 投影後執行 `storyProblems`、`reviewProblems`，均無問題。
