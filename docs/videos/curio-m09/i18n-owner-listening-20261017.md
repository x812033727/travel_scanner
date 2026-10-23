# M09 多語旁白站主試聽與上傳包

日期：2026-10-17（Asia/Taipei）。站主已試聽並接受 M09 日語、韓語旁白；先前英語旁白也已獲站主試聽接受。這是人耳判定，不把自動轉寫的旗標改寫成零，也沒有重錄或新增付費 QA。

- 日語：95／95 句完成機械 QA，24 句旗標保留在 `i18n-audio-qa-ja-1.md`；音軌 SHA-256 `7D02E468699D2CFB71910D7C3ABCD41EAC92E1E9D1CBB9DF938739A40FA2A145`。
- 韓語：95／95 句完成機械 QA，19 句旗標保留在 `i18n-audio-qa-ko-1.md`；音軌 SHA-256 `7A264D836D28247CB63F5C0E44AD9C5C59899D92334F4189870EC94B9C155336`。
- `captions` 重建後，繁中、英、日、韓各 95 cues，manifest 四語均無問題。
- `package` 已組成獲核准的成片 SHA-256 `9D9799CDF2E1B9165BD3F7817860107B085518AD47C18E03CC7C97BE4D6BF2F7`、四語標題說明與字幕、三語配音及三語縮圖；上傳包 4／4 項檢查通過。`upload/metadata.json` SHA-256 `14939DCCAC842FF400C493301BBEF04039CEA00B6473C0B2E25F483A9FE94802`。

上傳包位於 `<home>/mokaair-work/videos/curio-m09/upload/`。後台唯讀讀回最新 `publish` 卡 `3fa63c7c-4b46-4289-bd68-7c629758b90b`，內容 SHA-256 `14939DCCAC842FF400C493301BBEF04039CEA00B6473C0B2E25F483A9FE94802`；最新 `languages` 卡 `cc8e7ea3-3164-466c-8ee1-473850532ecd`，內容 SHA-256 `DB2141C20319DDE0DDE300E3C38300A3A53C6B63D0AA02691B6849CA6945749F`。兩卡於 2026-10-17 送達，讀回均為 `pending`。卡片核准、Studio 私人上傳、四語播放及公開排程仍各需獨立驗證。

後續於 2026-10-17 01:58 UTC 再讀回時，同一 `publish` 與 `languages` 卡片 ID、SHA 均為 `approved`；兩份核准已用 `review-pull` 寫入本機 `approvals.json`。上段 `pending` 是首次送審時的歷史狀態。Studio 私人上傳、網址回填及四語播放仍待站主完成與確認；沒有把後台核准當成 YouTube 上傳。
