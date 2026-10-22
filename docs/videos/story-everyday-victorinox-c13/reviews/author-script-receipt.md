# C13 Victorinox｜作者逐字稿交接收據

**狀態：作者交稿；沒有授予逐句來源 PASS、盲讀 PASS 或站主逐字稿採用。** 2026-10-23（Asia/Taipei）。範圍只含下列逐字稿、來源筆記與逐鏡規劃；沒有生成、配音、付費、匯入、上傳、合併或發布。

## 輸入綁定

| 已採用輸入 | SHA-256 |
| --- | --- |
| `treatment.md` | `A4A47F06F52490B4044267405445F31AC31EF7FB2C19575D59511D5BE0C57F20` |
| `source-matrix.md` | `295A7793DE618FEF714FA530F78592527EF77E82BAA38EE5594745B8386641D1` |

站主 Treatment 採用憑據為 `reviews/owner-treatment-adoption.md`；本次未改動上述兩檔或憑據。

## 本次交付雜湊

| 作者檔案 | SHA-256 |
| --- | --- |
| `script.md` | `3396B18F8E6C2FE0ED64AB8B25A30E249D025C6BB26A7165259C14AC1BFBD7E3` |
| `script-source-notes.md` | `9AC5E0879AEB153CA2C5102E1791DED69BC532B16A71139605FF9B189F92CC2A` |
| `visual-plan.md` | `E191433B42FE743A938CA4A95AE06CE86CA92C276D4C74EC5301936AE17F054E` |
| `visual-plan.json` | `38F8D379E5DD788D05608310F89F5FB2F9E4CA33EED1871B6C0B7CD88FF9F9B3` |

## 作者自檢與未通過的通用檢查

- 機械核對：六章、75 句、2,718 個口播字元；75 個唯一鏡頭，行 ID 一對一，所有句子均有 S/M 標記。依字數暫排正文 599 秒（未實測）、總長 625 秒；插畫 490／599 秒＝81.8%，最長連續字卡 2，暫排最大具體鉤子間距 43 秒（含 5 秒片頭與末段）。`look.preset` 為 `cute-mystery`，片頭 5 秒、v4 片尾 21 秒另列。
- 歷史邊界：1945 是美軍 Post Exchange，不補造成民航機場；1989 北美手錶及 1999 授權旅行用品先於 2001；7 月 30 日合營宣布與 11 月營運不同；瑞士 AG 不等於美國 SABI；S10 十月約 30% 與 S5 Q4 近三分之一並列未定論；2002 年四項產品／傳單狀態分開；員工借調明說為 CEO 後來回憶；2005／2014／2017 不強接單一因果。
- `npm run check:tasks` **exit 1**：兩個既有未追蹤的 `tasks/open` ghost 檔與已完成任務 ID 重複。本任務未刪改或暫存它們。
- `npm run test:docs-videos` **exit 1**：137 項中 131 pass、6 fail；失敗由本工作樹未安裝 `node_modules`、`tools/video/tts/check.mjs` 找不到 `pinyin-pro` 等現有環境依賴觸發。沒有執行可能長時間卡住的 `npm ci`；本片沒有媒體生成或需新程式行為的改動。

## 待下一關

請另一名代理對以上精確 SHA 逐句重讀一手／當期來源並簽 PASS/HOLD，再做至少兩位盲讀、繁中念法與 TTS 時長核對。若來源改稿，應重新出 SHA 與收據。站主逐字稿採用和單集付費預算核准均須另立；此收據不代替任何後續關卡。
