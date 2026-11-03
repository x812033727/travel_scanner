# S63 R6｜作者窄幅修稿紀錄

2026-10-22 UTC。R5 的[獨立史料／書面畫面 PASS](r5-source-visual-independent.md)只適用 R5 雜湊；[正式雙盲合併](r5-formal-merge-audit.md)是 **12／13 HOLD**。兩位各指出一個 `no_recap` 位置：A 說 `s63052` 再提三個孩子，B 說 `s63106` 又演開場敲箱。B 另指出 `s63126` 片尾新問題沒有回收；其 `payoffs` 單人否決在官方 OR 合併下通過，但作者也處理這個具體問題。

| ID | 窄幅修法 | 固定 Brown／Stearns 原文及畫面界線 |
| --- | --- | --- |
| `s63002`、`s63004`、`s63106` | 開場只停在接收者害怕開箱、箱內是否還能出聲；敲箱與問話首次在正文發生。`s63106` 只說有人終於敲蓋，隨後 `s63107` 問話、`s63108` 布朗應聲。 | [B09 L1564–1572](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1564-L1572)：眾人先怕開箱，稍後有人敲問；示意鏡頭由一人猶豫轉為一人真正敲箱，不要求插圖產生可讀標籤。 |
| `s63052` | 不再重講三個孩子，改為布朗提醒讀者：告別不是虛構，而是南方日常現實。 | [B03 L1388–1394](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1388-L1394)，是布朗陳述經 Stearns 筆寫的出版主張，非獨立社會統計。書面畫面只留一名成年人及遠去後的空路，不畫三個孩子。 |
| `s63126` | 刪去「出箱算結束還是開始？」的新問題，換成來源中的新事實：有人告訴布朗，北方人會為保護他而違法；這種說法未消除他對法律的疑慮。片尾以陳述收束。 | [B10 L1622–1638](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1622-L1638)；明說是布朗「有人告訴他」，不把口頭說法畫成確曾發生的違法營救。單人停在講堂門檻的光影之間，不暗示取得法律自由。 |

對 R5 的可逆 JSON 結構差異只涉及以上 **五個 scene ID**；`video.json` 其他頂層欄位不變。R6 作者凍結：`video.json` SHA-256 `8f8903a7ec270c61636953a7d675840a838604c268132722658c05b26f2dbf68`；`script.md` `dfafdb178646575cc4cefab9c14621284835299caf1c75f3eea86e7835d82bd9`；`claims.md` `10a28deb76976f1b7c32eb4ab0188c6fda33e93d1914d2d1536c1ecd7eb9c18e`。仍是 127 句、121 shot 和 6 張資訊卡。開場 175 漢字，**約 32 秒**；正文排除開場和 CTA 為 **2,682 漢字＝8.25 分鐘**（325 字／分），保持八分鐘以上。Episode lint 0 錯誤／0 警告，`git diff --check` 通過。

**R6 尚待全新獨立史料／書面畫面審核，以及兩位未看過 R5 的正式盲讀者。**舊版 PASS／HOLD 票不能移作 R6 媒體准入。尚未呼叫付費圖像、語音、音樂或影片服務；沒有成片、Short、上架或互連 watch URL。
