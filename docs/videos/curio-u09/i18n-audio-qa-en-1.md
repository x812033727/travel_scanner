# U09 英語配音與音訊差異 QA

日期：2026-10-16（Asia/Taipei）。U09 繁中成片及英／日／韓三語選擇已由後台讀回；英語文稿在獨立審稿後通過。本收據記錄英語配音和差異分流，不代替站主試聽或語言上傳包審核。

## 綁定檔案

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `719CFEA737CFCF0C21D704CB91B3085F28F83B46DCD10682A704A62996617E17` |
| `i18n/en.json` | `2F5A696FE49EB73237076F238B26A537C0BA3351FA9D94B22A1CB278238CFBEA` |
| 本機 `dubs/en.m4a` | `A63300723641258A64A279EDDB74BF8E022BF1CD15AA90888ED00BA1B10D47B7` |
| 本機 `dubs/en/narration.wav` | `2ACEFCA62E0409816F23E1245ADF53F840CD584842BF05A1253C0E54C6AC783B` |
| 本機 `dubs/en/timeline.json` | `E58F21C0DC5E5B34806D941DDE0FFC9F3A4D9CB67B53FF2B0DF6553AB2D5348C` |
| 本機 `review/check.en.json` | `21E69659C59590BAEF2E64D48238F40C094E51887A05CCD3418CEA331826F57A` |
| 本機 `review/check-flags.en.json` | `DFEAA9FD8810ABEB20F1A2239624239306246680BBD65F8DB3D9A49C5488126B` |
| 本機 `review/whisper-small-en-flags-20261016.txt` | `3554FCCF45C215A6DC483611D73E3510BB81C6FCEEFB2BAF96B80D697A6AD94B` |
| 本機 `review/whisper-medium-en-focus-20261016.txt` | `E79E26A847A4C98C777BE07C0BB4FC4A46BB74C9EA96625591968AD7693B2D3F` |
| 本機 `review/dub-en.html` | `8F22F6149CEFBEFEAD40D9D9E79B3522438CDAC92A242BE4B6A24795ADC8A899` |

`dub --locale en --dry-run` 原估 101 次合成、6,310 計費字元、0 個無法容納時槽。實跑 101／101 請求、0 快取沿用，102 句音訊全部落入時槽、0 句需加速。`ffprobe` 量得成品 620.5 秒。先在五集共享帳本預留英語 TTS US$0.15，後以 101 次／6,310 字元核銷 US$0.15；這是保守停手估算，沒有供應商最終美元發票。

`check-audio --locale en` 完成 102／102 句 Gemini 轉寫、1 次 TypeSafe Jev 判讀：88 句逐字一致、4 句 Jev 接受、10 句自動旗標。QA 預留並核銷 US$0.50，英語新增合計 US$0.65／站主核准的 U09 多語增額 US$2.50。接上 main 的英語漏字規則後，先本機檢查 102 句快取的 WAV 雜湊與提示詞均命中，再重跑 `check-audio`，新增轉寫 **0**、Jev **0**；10 句旗標不變，其中 `3d181765` 改明列 `thought` 漏字疑點。共用帳本仍保留初次付費時的舊旗標雜湊，這份收據記錄現行重跑雜湊。

離線複核使用本機 faster-whisper small、CPU int8、英文、beam 5、無 VAD／前文提示；另用 medium 同設定只核對兩個關鍵句。兩者都是辨識模型，不等於真人聽辨。

| 句 ID | Gemini 主要差異 | 離線結果與分流 |
| --- | --- | --- |
| `8748fb3d` | Bell→Belle | small 為 Bell；同音拼寫，無重錄依據。 |
| `e3e46d77` | Hewish→Huish | small 為 Hewish；陌生人名拼寫差異，請站主留意發音。 |
| `3d181765` | 句首 `thoughtMoving` | small、medium 都沒有 `thought`，但新版規則仍標漏字；請站主聽開頭後決定，暫不重錄。 |
| `544d8e26` | Bell→Belle | small 為 Bell，但把 rolls 寫成同音的 roles；無明確發音錯誤。 |
| `5d94082f` | Bell→Belle | small 為 Bell；同音拼寫，無重錄依據。 |
| `336cd716` | Bell→Belle | small 為 Bell；標點差異，無重錄依據。 |
| `22561e92` | Hewish→Huish，recorder's→recorders | small 與核准稿相同；所有格同音，請站主留意人名。 |
| `9bc5a454` | roll→role | small 為 roll；同音拼寫，無重錄依據。 |
| `049813c5` | publish→published，日期序數化 | small、medium 都聽成 published；中文原句的刊出事實未變，但與英文核准稿時態不同，請站主定向試聽決定是否重錄。 |
| `3ecdf437` | turn→turned | small 為 turn；無重錄依據。 |

逐句試聽頁在 `<home>/mokaair-work/videos/curio-u09/review/dub-en.html`，先顯示這 10 句，能切換全部 102 句；102 個音檔連結已核對，沒有缺檔。優先聽 `3d181765` 句首與 `049813c5` 的 publish／published，其餘請順聽人名。英語目前等待站主聽感判定；沒有將旗標直接當作錯字重錄。日、韓配音與 QA、四語上傳包及 Studio 上傳均不在本收據完成範圍。

## 站主後續試聽決定（2026-10-17）

站主已試聽現行英／日／韓三語逐句頁，明確回覆三語旁白都可以，包含英語 `3d181765`、`049813c5` 與人名疑點。英語保留現行音軌，不定向重錄；`check-audio` 的 **10 個自動旗標仍如實保留**，人工接受不改寫轉寫資料。此決定只解決聽感關卡；上傳包、後台語言卡與 Studio 上傳另行處理。
