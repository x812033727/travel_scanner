# H10 多語交付前檢查：英／韓可用材料與日語停點

日期：2026-10-17（Asia/Taipei）。檢查範圍為已選的英、日、韓三語上傳材料；本輪只做本機、無付費的產物準備與核對，沒有上傳、送審、配音、轉寫或修改繁中成片。繁中已核准成片 `final.mp4` SHA-256 仍為 `912F39E5DF15E0FEC7AADE44FE6872B28E8C6E5E9EDA63F60EEECB7E4949017C`。

## 英語與韓語材料

`captions --slug curio-h10` 重建字幕後，`captions/manifest.json` SHA-256 為 `857EAFC477626BF8D600D0AEA175CD324B71F36D561922D6AE5B0B02BDEBB88E`。英語 122 段、韓語 124 段，均使用各自配音時間軸且 `problems: []`；繁中 102 段也沒有問題。英文 SRT SHA-256 `E5421074D6ACB0521EEDBB8E408C8CD883A78C8855954F8721BC229A25CD90A7`，韓文 SRT `BAA644C0DBAF74FDD9DFA2C659B6AC65D42BF79061CA98806ABBE1F2F4979F51`。英／韓配音均為 614.2 秒，最後字幕分別止於約 9:51.86／9:51.19，沒有超出音軌；其 M4A SHA-256 分別是 `6382426E07EB5809F63A08C5CC77583DD25D9B6B18BEE9840BE856F4D8508BAD` 與 `9A1B5262B50B7549B64AFE8772370C9DB8E9CA53CE0125AEF72F8BE398B87C14`。`dubsForUpload` 讀回可用語系僅 `en`、`ko`。站主已分別回覆「英語旁白可以」與「韓語旁白可以」；韓語原有 16 句自動旗標及離線複核證據仍保留於 `i18n-audio-qa-ko-1.md`，這兩次聽感回覆不等於上傳包核准。

用現有 `video.json`、翻譯和已核准成片時間軸唯讀執行 `composeMetadata`：英、韓的標題／說明皆 `problems: []`，英語標題 81 字、說明 1,852 UTF-8 bytes；韓語標題 36 字、說明 2,097 bytes。兩份文案均含 2026 年近況與來源連結。尚未生成正式 `upload/metadata.json` 或 `upload/description.*.txt`，不能視為上傳包檢查完成。

原英文縮圖文案過長會溢出，原韓文文案將一個詞拆行；只改 `i18n/en.json` 的 `thumbnail.headline` 為 `Ships found\n**Crew?**`，以及 `i18n/ko.json` 的同欄為 `배 발견\n**사람은?**`，沒有改任何旁白句。重跑 `render --thumbnails-only` 後生成英／日／韓本機縮圖，影片畫格未重繪。英、韓縮圖經另一位審核員在 1280×720 原尺寸與 320×180 預覽尺寸目視通過，沒有裁切、重疊或改變「船找到，船員呢？」的疑問：

| 語系 | 本機縮圖 | bytes | SHA-256 |
| --- | --- | ---: | --- |
| en | `thumbnails/en.jpg` | 84,200 | `FDBF6390F3A7249735D20AB2D78752FA192A9BC68496BF949648A4067A6934D7` |
| ko | `thumbnails/ko.jpg` | 79,865 | `9EA8D2AFDEE0FC31A7C568A3A83D89934F54AF27DD56E953A0EECE79FA343395` |

本輪修改後 `i18n/en.json` SHA-256 `4F1E314D49A8E8C277AA3117CDF14A817B055E1F2C0C896D7EAC82E77F712DF0`，`i18n/ko.json` SHA-256 `580EA0BAFEC34B1BDEC2543454361331EDC95136E040F04A6B66841DDB505733`。縮圖文字不參與逐句配音翻譯雜湊；重建字幕後英、韓仍讀回 `timing: dub`。

## 日語與交付停點

現行 `i18n/ja.json` 已把 `he2b2172` 的不成句譯文修正，但舊配音仍對舊文稿。字幕 manifest 的日語 123 段顯示 `timing: narration`，並明確回報日語配音比譯稿舊；`dubsForUpload` 沒有可交付的日語音軌。站主已表示日語有錯句、會另給句 ID，目前尚未收到。首輪待聽的高風險句包括 `h93d6e3d`（9 月／10 月 18 日）、`hc9c15f2`、`h3e67f13`、`hbb9c913`；證據見 `i18n-audio-qa-ja-1.md`，自動辨識不能替代站主聽感。

後台勾選了三語的標題說明、字幕和配音，因此現在不可執行會組裝全部選定語系的 `package`，也不可用舊日語音軌送 `review-push --gate languages`／`--gate publish`。目前沒有正式三語上傳包，沒有多語審核或 Studio 上傳。H10 多語保守估算已用 US$1.99／US$2.00，本輪新增 US$0；任何定向重錄與付費 QA 前要先核對新增額度與帳本。

後續依序：取得站主日語錯句 ID；針對日語譯稿及確定錯音做獨立審核；核對追加額度後只重錄必要句並跑定向 QA；站主試聽日語新版；重建日語字幕，確認三語 `timing: dub` 且無字幕問題；再跑完整 `package`、上傳包檢查及相應後台審核。上傳至 Studio 由站主處理。

本機檢查：`lint --slug curio-h10 --json` 為 0 errors、2 個既有畫面提示詞 warnings；`git diff --check` 與 `npm run check:tasks` 通過。本收據只記錄本機可用材料，不標記 H10 完成。
