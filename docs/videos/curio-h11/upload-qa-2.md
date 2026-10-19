# H11「四葉」版四語上傳包本機驗收

日期：2026-10-16（Asia/Taipei）。繁中成片已由站主在後台核准，SHA-256 `54EFA17859D4359B84A9266799108B3C0DE0597DDFAAA2F1B4B3F556801FF1BC`；站主在影片語言面板選定 en／ja／ko 的標題說明、字幕與配音。英、韓音軌已經站主試聽接受，日語仍等聽感結果。本收據記錄目前可重建的**本機包**；未送新版 `publish`／`languages` 審核，也未上傳 YouTube。

`captions --slug curio-h11` 已按三語配音時間軸重切：zh-TW 104、en 84、ja 121、ko 121 cues。`package --slug curio-h11` exit 0，四項檢查 4／4：核准成片與基礎檔、四語說明、四語字幕、合成媒體揭露。`upload/` 有 `final.mp4`、`thumbnail.jpg`、`metadata.json`、四份 `description.<locale>.txt`、四份 `captions/<locale>.srt`、三份 `dubs/<locale>.m4a` 和 `UPLOAD.md`。英、日、韓無語系專用縮圖，沿用 `thumbnail.jpg`；縮圖非站主所選三部件之一。

| 檔案 | SHA-256 |
| --- | --- |
| `upload/final.mp4` | `54EFA17859D4359B84A9266799108B3C0DE0597DDFAAA2F1B4B3F556801FF1BC` |
| `upload/metadata.json` | `E89C18865BDDA4D49E031455FF46CF39B67B7B212D3CB84F7CF59CD88D50BF34` |
| `upload/captions/zh-TW.srt` | `7DC5C8561372CEF38B1B50BE5CD7CD3719CD8ED0D79CD497BBD3FA3ED93F8D10` |
| `upload/captions/en.srt` | `27AD785C12FC58BDB99D77FB3757F8E342B26808AA022B8DEBDC1BA09B3F08A9` |
| `upload/captions/ja.srt` | `3F57BA5A0ACE21406FFD529A6374E11C6EFD86693D7A182C4A683E8BC036B2AD` |
| `upload/captions/ko.srt` | `6E84A9AD2BECB5744FA68019A0C26A8BF91AC33CDD034AA2007775EDFA791ECB` |
| `upload/dubs/en.m4a` | `1F99A4E972FF550487ABF83DFB04F16F7283B3B84B9169E5C3A8A9CB0E7475F9` |
| `upload/dubs/ja.m4a` | `52048F3AC27C411DC05A7666514A0B710D01D49E46E2B747783A53409FFD2CEE` |
| `upload/dubs/ko.m4a` | `BE09949E8773DF5686C4D9F94EF8C3E1B26D4257C3291CF3B460BCE1D46D1A3A` |

接下來先讀回日語人耳結果。有任何日語重錄或改稿，本收據、字幕、上傳包與後台審核必須按新版重建；若站主接受這條音軌，核對上述 SHA 後送新上傳包與語言審核卡供站主審閱。上傳及排程由站主在 Studio 操作。

## 2026-10-16 日語試聽與後台送審

站主已聽完日語逐句頁並回覆「日語旁白可以」；英、韓亦已分別由站主試聽接受。這是三語音軌的聽感確認，不是後台語言卡核准或 Studio 上傳確認。本次未改動劇本、配音、字幕或成片，也沒有新增付費呼叫。

重新核對本表所列的成片、四語字幕、三語音軌與 `metadata.json` 的 SHA-256，九項全部吻合。重新執行 `package --slug curio-h11`，退出碼 0，上傳包檢查 4／4，成片仍為已核准的 `54EFA178…801FF1BC`，`metadata.json` 仍為 `E89C1886…D88D50BF34`。本機 `languages.json` 的 en／ja／ko 均勾選標題說明、字幕、配音。

已依序執行 `review-push --gate publish`、`review-push --gate languages`，兩次均成功送出。其後各自以 `review-pull` 讀回，**publish 與 languages 均為 `waiting for the owner`**。請以目前這份四語上傳包在 `/admin/videos` 審閱；未宣稱任何一張卡已獲核准。YouTube Studio 尚未上傳，未排程或發布；站主先前選擇親自操作 Studio。

再以影片工具同一唯讀 GET 端點讀回最新卡片：`publish` review ID `78c54776-53db-4f4c-b902-536f871f30dd`、`content_sha256` `E89C18865BDDA4D49E031455FF46CF39B67B7B212D3CB84F7CF59CD88D50BF34`、`pending`；`languages` review ID `fef69bcd-548f-4837-af28-5d8108d287ac`、`content_sha256` `8B35A601DE8F5A705E44AD5DF2946A09404C43CF36BB9F51923902216E4521AB`、`pending`。先前繁中基礎包的 `publish` 卡 `52c30ba2-0309-4879-bf36-331366d74e8a` 已標 `superseded`，不得用它代替最新審核。
