# S53 R16｜四張退圖的作者定點修訂

2026-10-22 UTC。**這是待非作者覆核的提示詞改稿，沒有新付費媒體或新圖驗收。** 我直接看了 R15 六張原生 JPEG：[驗收回條](r15-six-native-stop.md)的 `s53002`（灰髮年長職員）與 `s53005`（灰髮年長研究者）KEEP，這兩張的提示詞和圖片鍵**逐字保留**。`s53003` 的人物已成年、屋型與泥地也對，但木屋和地面像照片；`s53004/06/07` 明明要求成年手部，MiniMax 仍自動補成童貌全身人物，且帶黑邊、現代扣包、表單橫線／文件櫃或現代背包。

R16 只改被退的四個 `data.prompt`。它沿用這集可用圖的實測線索：讓**可見的灰髮、皺紋與高領衣著**承載年齡，不再只要求畫面外的「成年手部」；收起室內背景與文件道具，將金屬扣包／大背包改為小型繫口布袋。

| 景 | R16 收窄處 | 史料及畫面界線 |
| --- | --- | --- |
| `s53003` | 年長住戶的中近景，手扶低矮木屋的簡單木板門；屋頂邊線與淡天空取代大面積近照片地面。 | 1913 調查記有住戶在符合條件下搬離住屋；這是木屋概念示意，不畫未查到的搬運機械。 |
| `s53004` | 灰髮、皺紋、1907 年高領衣著的年長女性，把小繫口布袋放在**單張全空白**紙旁。 | 月繳款的租購狀態由旁白交代；空白紙不是保存的收據或契約，也不表示所有付款者是年長女性。 |
| `s53006` | 灰髮年長職員只翻**一張全空白折紙**，小布袋放桌側；素牆與窗光取代文件櫃、相框。 | 「租還是買」是旁白問題，圖沒有聲稱取得兩種原始表單或已知道案。 |
| `s53007` | 灰髮年長觀察者望向低矮木屋門口一只小繫口布袋；不用童貌、心形現代衣標或大肩包。 | 旁白問誰負擔搬遷費。圖不把布袋指定給住戶、親友、房東或慈善機構，亦不示意未知搬法。 |

固定 1913 年 *San Francisco Relief Survey* [L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994)記廣場小屋與搬離條件；[L10482–10500](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10482-L10500)記月租改為分期購屋；[L10932–10944](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10932-L10944)記住戶、親友、房東及慈善團體等支付搬遷費。四張人物均是匿名概念角色，非歷史個案或照片重建。

[四項可逆差分](r16-four-prompt-structured-diff.json)列出每景舊／新字串。R16 `video.json` SHA-256 **`817819fb64717fb3dc6e5bd1e1957a5e7d14d9f8fb455001ac0d4a609ee62f12`**；倒序還原四項便逐位元回到 R15 **`1617d0290291258231b1f6908f26c4dde988e0f4e77b4e0b63c0e4c9ae7cd349`**。另外 120 景、126 句口播、`brief.md`、`research.md`、`claims.md`、`script.md`、運鏡、品牌及配樂未動。CLI lint **0 errors／0 warnings**；四景 MiniMax 非付費 dry-run ready、約 US$0.05 一輪。私有 `STOP` 存在，帳本仍 **US$0.1925／15 images／14 judges／0 reservations**，低於整集圖、judge、音樂 **US$4.78** 停線。

請非作者先核四景差分與來源／畫面界線，才考慮各景一次受控原生圖重試。若再次出現童貌、現代器物、照片／3D 背景、黑邊或可讀字，直接退圖；不能因機器 9.29 PASS 放行。屆時這四景已各有第三張生成嘗試，應優先依系列規則評估同章合規已收圖重用或資訊卡，並維持插圖比例與連續卡片上限；不要無限追加付費提示詞輪次。網站、人耳、其餘插圖、配樂與成片仍未通過。
