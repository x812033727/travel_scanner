# U09 四語上傳包本機驗收

日期：2026-10-17（Asia/Taipei）。站主已試聽並接受 U09 現行英／日／韓三語旁白；機械音訊 QA 的 EN 10、JA 20、KO 24 個旗標仍保留，不記成零旗標。本收據只證明本機包及送審版本；後台核准、Studio 音軌上傳、排程和公開要各自讀回。

獨立稽核發現首次 `package` 沿用舊 `frames/manifest.json` 的三語縮圖缺漏紀錄，雖然現行三語譯稿已有來源雜湊相符的縮圖字。這份舊包的 metadata SHA `94740E9C5EB17868DFFD9251E936BC93A0484256E09A177830439CFE193F7CB6` 曾送 publish／languages 兩張卡，**後台已把兩張舊卡標為 `superseded`**。只用 `render --slug curio-u09 --thumbnails-only` 補三語縮圖，沒有重畫任何成片鏡頭；原 `thumbnail.jpg` SHA `E7265CE4…5AA2DE`、聯絡表 SHA `AA6F9C30…DCF3` 前後相同。更新的 `frames/manifest.json` SHA `083DC6BC64BE3C6783692624587718095A85A3D78CE698443FBB0F7C07534939`，只增加現行三語縮圖紀錄。三張 1280×720 圖已目視，無裁字或缺字。

**現行新版** `node tools/video/cli.mjs package --slug curio-u09` 成功，內建上傳包檢查 **4／4 通過**：核准的成片、四語說明、四語字幕、合成內容揭露。包內 `final.mp4` 為已核准 SHA-256 `78FAAD29FB5B6556CAF18ACD21063250797F55DA4029638A6EA20349D6156C18`，大小 168.48 MiB；`upload/metadata.json` SHA-256 `4CEACE32B226D9B42783CC456B6C6CD7C7CEB30B20A163A9F7D7B351053E14D7`，列 en／ja／ko 三語皆勾 metadata、captions、dub，且 `thumbnails` 包含三語、`skipped_thumbnail_locales` 為空。現行包包含原 `thumbnail.jpg`、三張分語縮圖、四語 `description.*.txt`、四語 `.srt` 和三條 `.m4a`。

逐檔比對包內副本與現行產物，下列十個 SHA-256 全部一致：

| 檔案類別 | 語言 | SHA-256 |
| --- | --- | --- |
| 配音 `.m4a` | en | `A63300723641258A64A279EDDB74BF8E022BF1CD15AA90888ED00BA1B10D47B7` |
| 配音 `.m4a` | ja | `066EA9CBA36180058710C8369045F2D55A3C98DC1D65623E82963718E23784D9` |
| 配音 `.m4a` | ko | `9239141A03EF1F23D3D6CAB51623BA052ADF1E15E66A4B1CEFB64D008BB73B44` |
| 字幕 `.srt` | zh-TW | `C9B98CC58C20C56B18438AAD03BA2E7F89B9CFF4119316857AD0139CC8B75831` |
| 字幕 `.srt` | en | `EC348773D0C455C959472D242793C20FB1765AE9ADDDE7B2109061E68A7417F3` |
| 字幕 `.srt` | ja | `D8C021D532DE995697FFEEA0C4A1E2FCD930003B64D5952B52CB237C44CD75CB` |
| 字幕 `.srt` | ko | `CEA99282DFCF7C4E1BA103D2F332CE39592F6EBFFD62D57B60A9571D7F5B92EC` |
| 分語縮圖 `.jpg` | en | `FF286313D8FFD17352D04FCC55A858988DCAFF3F3CFFCAF1EF23C7DC50227AB0` |
| 分語縮圖 `.jpg` | ja | `560EC3C8D3EC5EB93CA0E9ED9AB99449E5D2C71886BA93965EA578E8F866DE51` |
| 分語縮圖 `.jpg` | ko | `5D8CB256FA352F6C2ADEF35B3A9CA7CCDD6B04E99F854E738475AA500A371AE0` |

`captions/manifest.json` 記 zh-TW 105、en 104、ja 109、ko 109 cue，四語 `problems: []`，外語時間軸皆為 `dub`。英文第 91 cue 本機獨立 `checkCues` 複核為 18.6 CPS、0 問題；SRT／VTT 全 104 cue 同文同時；包內英語 SRT 的 `08:32.133–08:34.500` 與修正版來源 SHA 相同。其他核對：U09 `lint` 0 錯誤、1 項既有 `later-support` 約 10.1 秒鏡頭時長警告；`git diff --check` 通過；`npm run check:tasks` exit 0，所列警告涉及其他已久認領和既有重疊任務。

後台**最新** publish 卡 ID `febf304b-511e-4a06-ac47-9d84eb439b7b`，content SHA 為現行 metadata 的 `4CEACE32…14D7`，唯讀 GET 與 `review-pull` 均確認 `pending`，等待站主核准。最新 languages 卡 ID `4b526710-8719-43a4-a433-c9d5ded8d310`、`review/languages.json` SHA-256 `E170FA4BB6194114D0294377B28FD1E77B6E7D9733101C5D826DC78432F6C1B5`，讀回也為 `pending`。先前無分語縮圖的 publish 卡 `e0f65d56…` 與 languages 卡 `00a9ab6e…` 已讀回 `superseded`，不可再拿其待審狀態代表現行版本。

本機包路徑：`<VIDEO_WORKDIR>/curio-u09/upload/`；操作說明在 `upload/UPLOAD.md`。本收據不宣稱站主已核准上傳包、已在 Studio 上傳音軌、排程或公開。
