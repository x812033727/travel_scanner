# S53 R15｜第一章六景提示詞作者修訂

2026-10-22 UTC。**這是待獨立覆核的紙面修稿，沒有新付費生成，也沒有核收任何圖。** R14 首章批次的 `s53002–s53007` 六張 1280×720 原圖均人工 REJECT，前五張有 judge、`s53007` 當時因 STOP 尚未送 judge。R14 [原生圖回條](r14-first-chapter-six-native-stop.md)保存各原圖 SHA 及具體錯誤。我逐張打開原圖：廣角「public square」常變成現代住宅街或東亞式街道；無年齡線索的人被畫成孩童；1913 室內畫面又補出現代檯燈、字與照片式樓房草圖。

這次只改六個 `data.prompt`，避免延用那些失敗的取景觸發詞；`s53001` 的來源日期卡、`s53008–09` 與其餘 116 景、126 句口播、章界、運鏡、伏筆、音樂、`look` 均未改。`claims.md` 的六列是旁白來源及歸屬界線，沒有舊 prompt 的逐字畫面欄，所以不改主張與劇本。

| 景 | R14 原圖的主要誤導 | R15 提示詞的局部修法 |
| --- | --- | --- |
| `s53002` | 童貌職員、大房屋草圖、黑邊 | 鏡頭靠近 1907 辦公室木板；年長職員的手把**空白**月曆頁固定在板上。日期由旁白說，不把此頁說成存世通知。 |
| `s53003` | 童貌住戶、鋪設人行道的住宅街 | 以單棟低矮木造救災屋的木牆與屋頂佔滿後景；留灰髮、鬢角、成年身形的住戶和泥地。畫的是可帶走的小屋概念，不補造搬法。 |
| `s53004` | 孩童拿紙站在現代感街屋前 | 改在木屋室內，以成年人的舊袖口與手，把**收起的**布錢袋放在無字紙旁；不宣稱留有實際月付收據。 |
| `s53005` | 現代檯燈、有字頁、照片式大樓草圖、黑邊 | 1913 年素牆辦公室內，年長研究者打開無字裝訂書，桌上只留書、窗光；不仿造存世調查封面或頁面。 |
| `s53006` | 童貌人物與東亞式簷口 | 室內桌面中近景，成年職員的手分開兩張空白紙片，錢袋置中；不讓兩片成為可辨的原始租購文件。 |
| `s53007` | 孩童、東亞街景、可讀文字與大量金幣 | 局部木屋門口、泥地和一只**收起的**布錢袋；不指明由住戶、親友、房東或慈善機構哪一方付款。 |

1913 年固定 *San Francisco Relief Survey* [L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994)記 1907 年六月廣場清場要求及小屋搬離；[L10482–10500](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10482-L10500)載名義月租轉成分期購屋；[L10932–10944](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10932-L10944)列搬遷費可能由住戶及多種援助支付。新圖皆為原創概念插畫；沒有捏造某張通知、租約、搬運帳單、住戶個案或搬屋機械。

[結構化差分](r15-six-prompt-structured-diff.json)逐一列出六景舊／新字串及路徑。R15 全檔 SHA-256 **`1617d0290291258231b1f6908f26c4dde988e0f4e77b4e0b63c0e4c9ae7cd349`**；按六項倒序替換可逐位元恢復 R14 **`0cbe40d9189710525bf82627bf21e411c2ea600870ceabc1975873e7b0fe1c19`**。`brief.md`、`research.md`、`claims.md`、`script.md` 的凍結 SHA 不變。CLI lint 0 errors／0 warnings，MiniMax `image-01` 六景非付費 dry-run ready、六張一輪約 US$0.08。私有 `STOP` 在位；帳本仍 **US$0.1115／9 images／8 judges／0 reservations**，低於整集圖、judge、音樂停線 **US$4.78**。

下一位非作者先獨立核這六景的逐字差分、史料歸屬、來源示意與畫面構圖，再決定有 STOP 邊界的一次首章重畫。直接檢查每張原生圖的人物年齡、屋型、年代器物、城市風格、黑邊及可讀字；機器 PASS 不代表可用。`s53007` 的 R14 圖已付費但尚未評審，R15 提示詞不同，不能偷沿用該圖或視為 R15 KEEP。`s53008–09` 沒有生成；更後面的整片插圖、網站卡、人耳、配樂、長片與連結仍待辦。
