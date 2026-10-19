# U09 韓語配音與定向音訊 QA

日期：2026-10-17（Asia/Taipei）。U09 繁中成片已核准；後台選定 en／ja／ko 的標題說明、字幕與配音。此收據只記韓語譯稿、配音、音訊差異及站主試聽；不代表已在 Studio 上傳或發布。

## 定向譯文修正

獨立審稿通過的韓語初稿 `i18n/ko.json` SHA-256 為 `3BFEFC995B7DD9480D0FDA52CFD76BCC836349C4F1FB1754BCACF641792313FB`。後續逐句核對發現 `b6d2d02b` 的初稿將中文「不靠振盪，還可以靠旋轉」說成「不是振盪，而是旋轉」，把尚在比較的解釋寫成確定結論。只將該句改為 `진동 말고 자전도 가능합니다. 서두의 5월 두 쪽 논문은 물리학자 토머스 골드가 썼습니다.`；50 個 Unicode 字元，未超過該句 `max_chars` 52。其他 101 句、句 ID、來源雜湊及 metadata 未改；反向替換該句可重現初稿雜湊。獨立再審確認新句與繁中原意相符。現行 `i18n/ko.json` SHA-256 為 `E8AEAF6DABD8CC1AE550775B5A235BAF2896C9ED17DEA956F23C44C1CF63BBB3`。

## 媒體與機械 QA

首輪 Gemini 韓語配音共 101 次 grouped 請求、2,863 計費字元，產出 102 句 WAV、620.5 秒音軌，0 個超時槽；首輪 `check-audio` 完成 102／102 句 Gemini 轉寫及 1 次 TypeSafe Jev 判讀，73 句逐字一致、5 句 Jev 接受、24 句自動旗標。首輪 TTS US$0.15、QA US$0.50 已依共享停手帳本保守核銷。

`dub --dry-run` 對定向修訂只列 **1 個新 grouped 請求／50 字**，其餘 100 個請求命中快取；實跑也恰好只新增該請求。再跑 `check-audio --locale ko` 只新增 **1 句轉寫與 1 次 Jev**，沿用其他 101 句快取；現行音訊仍為 102／102 句已轉寫、73 句逐字一致、5 句 Jev 接受、24 句旗標。新句 Gemini 轉寫把 `서두의` 聽成 `그 뒤에`，但句首修正的 `진동 말고 자전도 가능합니다` 轉寫吻合；辨識差異不能單憑機械結果判定需要重錄。站主其後試聽現行三語逐句頁，明確回覆「三語旁白都可以」，包含這句新錄韓語；因此不再重錄。**24 個機械旗標保留原值**，不宣稱 ASR 零旗標。

本機 faster-whisper small 對同一新 WAV 另聽為 `진동 말고 자전도 가능합니다. 서두에 5월 2쪽 논문은 물리학자 토 머스 골드가 졌습니다.`，支持句首關鍵修正，也顯示後半仍有模型辨識差異。離線文字檔 `review/whisper-ko-b6-20261017.txt` SHA-256 `D1E8ED537377161B6AEDC7C7DDFDF4D80ADFA14CAC09E01FE222FBEE0D71B73D`；試聽者對現行音檔的接受是最終聽感判定。腳本在寫出 UTF-8 文字檔後，向 cp1252 主控台印韓文時回 `UnicodeEncodeError`，因此程序 exit 1；錄音與文字檔已落地，沒有重跑模型或付費呼叫。

| 現行產物 | SHA-256 |
| --- | --- |
| `video.json` | `719CFEA737CFCF0C21D704CB91B3085F28F83B46DCD10682A704A62996617E17` |
| `dubs/ko.m4a` | `9239141A03EF1F23D3D6CAB51623BA052ADF1E15E66A4B1CEFB64D008BB73B44` |
| `dubs/ko/timeline.json` | `15E00CC4F55B05406F98E0D8D6E745B6ABDA1210CEC19F5FC20B4C6CDA49E1DD` |
| `dubs/ko/fit.json` | `C7D86590FB911EE6BF46DF44BFB79E7B913D9AF5570F3594015A63F16C4464A2` |
| `dubs/ko/audio/b6d2d02b.wav` | `338D65C8FCAA82AC82B4FBA1A7F9C5ADC67787E869B4B522A16AF876FEBE9132` |
| `review/check.ko.json` | `35B9857BAC75A7B44EF2985ED649EC5599FFECB0DE21499FB2929699FA7F2FE5` |
| `review/check-flags.ko.json` | `FB8A34321B2A1CBEA66A96014A1CB13CEDD44680F2BEF99F12BC76863F099DF5` |
| `review/dub-ko.html` | `45793E84C20F7FEBED8C815375DD2C6F9502BCEC6D1986CD43A918A7D2B3E481` |

定向 TTS US$0.02 與 QA US$0.15 亦已按預留全額保守核銷。這些是供應商無單次美元硬上限時的停手估算，並非最終發票；兩次均有明確成功請求／快取數，沒有新 hold。核銷後共享帳本 U09 估算累計 US$7.3535／8.50，五集含當時 H12 final QA 預留為 US$26.2295／39.00；其他任務其後可能更新帳本，後續付費須重新讀回。

韓語逐句試聽頁：`<VIDEO_WORKDIR>/curio-u09/review/dub-ko.html`，包含 102 個現行 WAV 連結、24 旗標、0 未驗句。機械旗標優先分流的句 ID 為 `acc6618c`、`e3e46d77`、`54c3000a`、`718638d1`、`0e6c77f2`、`f76bb3e1`、`b6d2d02b`、`f28a86d7`；它們已由站主在三語試聽頁一起接受。韓語字幕依現行韓語音軌切成 109 cue，manifest 為 0 問題。上傳包與後台語言審核是後續關卡。
