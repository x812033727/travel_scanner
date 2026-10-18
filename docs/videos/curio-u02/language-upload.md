# U02 英、日、韓語上傳交付紀錄

既有 [U02「51 區」影片](https://youtu.be/uZ9TlblvrCw) 的英文、日文、韓文音軌已補齊；重新載入 Studio 確認三語音訊、CC、標題說明共九個項目皆已發布。395 個字幕 cue 與六個 metadata 欄位逐字讀回通過，現行檔案、後台實體附件及已核准語言包 consumer 的獨立核對也通過。原 M4A、字幕、原片及後台來源保持不變，影片維持私人。

本次只處理既有影片的語言上傳及交付驗證，不重新合成、不產生付費請求、不修改原片、原始稿、譯稿或共用素材狀態。H01、H02、L08 不在此票範圍。

## 目前狀態

| 項目 | 英文 | 日文 | 韓文 |
| --- | --- | --- | --- |
| 既有正式音訊檢查 | 126/126，0 flags，0 unchecked | 126/126，0 flags，0 unchecked | 126/126，0 flags，0 unchecked |
| 本機上傳音軌 | M4A，704.5 秒 | M4A，704.5 秒 | M4A，704.5 秒 |
| 本機 CC | 126 cues | 135 cues | 134 cues，現行空白修正版 |
| Studio 音軌 | 已發布，原 M4A | 已發布，原 M4A | 已發布，原 M4A |
| Studio CC | 已發布；126/126 原文字串相符 | 已發布；135/135 原文字串相符 | 已發布；134/134 現行修正版相符 |
| Studio 標題說明 | 已發布；兩欄逐字相符 | 已發布；兩欄逐字相符 | 已發布；兩欄逐字相符 |

[最終 Studio 讀回][studio-published] 於 `2026-10-12T05:07:59.305Z` 保存重新載入後的三列九項已發布狀態。截圖 `studio-three-languages-published-names.jpg` 記錄語言順序，`studio-three-audio-published.jpg` 記錄同順序音訊／CC 已發布，`studio-en-published-detail.jpg` 補英文詳細資料；窄視窗分圖保存，沒有調整 viewport。JSON SHA：`c50d07b26cdc21ec4b596a4b1950f881228fcf080fd0b63c70b57e89904a8af2`。接手時三個音訊欄為空，後台卻已有「你說已上傳」文字；這次使用原核准 M4A 完成補上傳，未轉檔、替換素材或重新合成。

音訊的既有 native `check-audio` 最新成功狀態分別為 EN `2026-10-11T18:36:09.963Z`、JA `20:41:44.285Z`、KO `20:34:45.743Z`；三語各有 126 個現行 cache line，旗標檔為空。這些是先前製作的本機檢查，本輪沒有重跑付費音訊檢查。

## 固定交付檔案

下表來自本輪直接讀取 `<home>/mokaair-work/videos/curio-u02/upload` 的實際位元組與 SHA-256。

| 檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `dubs/en.m4a` | 26,314,380 | `04b907ac5932be7c5d34a608fa9ae66beda43e51b0cc1ea524e8fa322d25f885` |
| `dubs/ja.m4a` | 29,379,160 | `0c1a2f362d8d0094fb3eec5a321cc82c9d049ef8d6c1f578cc9a21ac8dfeb395` |
| `dubs/ko.m4a` | 26,601,155 | `5e3cfcd32adc4ca962911eef1e5e4b21bc245408b89ee10c728de9c84aa22c17` |
| `captions/en.srt` | 11,605 | `60be005b1eb48aebdf63715efb6b4d1f2e7954c39e66363f88fa867fbd1c0cf5` |
| `captions/ja.srt` | 13,751 | `e388e02c30332a2635c9aca5610a97794e36050d52bdf717c5ee52d26308a3cc` |
| `captions/ko.srt` | 12,685 | `cf9b525f3e349fed2c1f8dbd056d4e4832974a996a0a96a1d544f0af1235e87f` |
| `captions/zh-TW.srt` | 12,005 | `5bc2d8402229c03ade1173b3fc4554ac247b9260157a80d3dc78feaa1b71d54b` |
| `final.mp4` | 186,609,008 | `d0956ff8dd824375957091f593984914d99d60ccb7ed4e6c03c8fe4937eb79b8` |

韓文使用表中的 `cf9b525f…`。該版僅調整 cue 13／122 的空白／換行，保留 134 cue 時間、126 個來源 ID 及全部非空白文字；本輪逐字讀回確認 Studio 使用精確修正後文字。原 publish 附件 `68da424d…` 為歷史版本，不可誤作本次交付檔案。

## Studio 字幕與標題說明讀回

[逐字驗證收據][studio-text] 在 `2026-10-12T04:59:22.564Z` 通過 69 項檢查，16 個輸入雜湊前後一致。EN 126／JA 135／KO 134，共 395 個擷取的原始字幕字串連同 LF 換行、空格逐字相等，沒有 trim、折疊空白或 Unicode 正規化。另以明確的 LF 轉單一空格規則核對 395 個 DOM 標籤，也全數相符；三語共六個標題／說明欄位逐字相符。JSON SHA：`c74dc57b99832c3e4bb3d4a5a52831b8c30f21baf18c0f2268ce9c9dac82a10f`。

這是全 cue 文字讀回。可見 textarea 僅有 EN 4／JA 5／KO 5 個，未宣稱全片 Studio 時碼核對；唯一一次字幕下載嘗試逾時，沒有取得可核對的下載檔。因此下載位元組相同、完整時間同步及播放器試聽仍未驗證。

## 後台與來源綁定

原核准 final review 為 `2cdf2a9d-789a-4a63-8078-c88d2049536d`，原核准 publish review 為 `f05f540f-98ef-4a85-87ad-a1ae5a2fc6fb`，publish metadata SHA 為 `2f71d8cf2883f53a30e7288cd69ec5af50b7fab7679419fb66de82e5f78fd3d1`。本機現行 `review/languages.json` SHA 為 `b1de6a4d43fcf4f777ad67298bd62b0728a6072be30980f1979b3c7e278cdd52`。

本輪 [獨立後台與本機讀回][approved-readback] 於 `2026-10-12T04:55:10.409Z` 至 `04:55:42.469Z` 通過：實際 SSH exit 0，PostgreSQL `REPEATABLE READ, READ ONLY` 後 rollback；14 個原 publish 附件與 11 個語言附件，共 19 個不同實體 SHA，大小與串流雜湊全部相符。11 個現行語言附件與本機檔案一致。native `read_approved_package(verify_files=True)` 回傳 `APPROVED_CONSUMER_PASS`，接受三語音軌及含繁中的四語 CC，韓文選用現行 `cf9b525f…`，原 publish 的 `68da424d…` 保留為歷史版本。

語言 review `a0c010cf-0e38-40ed-bd8b-bec37be99cab` 現為 approved；其既有決策時間是 `2026-10-11T23:07:10.131196Z`，不是本輪的新核准。本輪沒有點擊核准或改動後台。bb7a 舊 pending／consumer 409／YouTube ID 空白快照已由這次實際讀回更新，不能當作現況。

同一次稽核重新核對全部 513 個既有 QA 輸入雜湊，前後完全一致；三份原 M4A 與 upload 副本相同，皆為 704.5 秒、AAC／48 kHz／雙聲道，嚴格完整解碼到 null 無錯誤。原成片和繁中字幕綁定保持不變。這些核對不代表 Studio 播放或人工試聽。

## 完成交付與驗證界線

三語音軌補上傳及發布、CC／metadata 完整文字讀回、後台實體附件和 consumer 核對均已完成。上傳與處理中收據保留為歷史，以最終重新載入的 Studio 發布收據判定本次交付。

本輪內容測試 `docs-video-tests.log` 為 199/199 通過、0 failed／skipped，耗時約 32 秒；`task-check.log` 驗證 1,850 個任務檔，僅既有無關 stale-claim 警告。兩項實際 exit 0，root 的 diff check 亦通過；文件子任務沒有重跑測試。

本輪私人 audit：`<home>/mokaair-work/video-language-uZ9TlblvrCw`。既有媒體：`<home>/mokaair-work/videos/curio-u02`。先前製作交接：`<home>/.codex/worktrees/bb7a/travel_scanㄐ/docs/videos/curio-language-delivery/README.md`；先前完整收據位於 `<home>/mokaair-work/videos/_audit/curio-backend-completion-20261012-bb7a`。不修改 bb7a 的稿件、狀態或任務。

原影片維持私人；本輪尚未建立完整播放器試聽、公開發布或站主播放驗收證據。三張外語縮圖不是本次要求的 CC／音軌補件範圍。

[approved-readback]: <home>/mokaair-work/video-language-uZ9TlblvrCw/u02-approved-readback-2026-10-12T04-55-10-408Z.json
[studio-text]: <home>/mokaair-work/video-language-uZ9TlblvrCw/studio-text-and-metadata-readback.json
[studio-published]: <home>/mokaair-work/video-language-uZ9TlblvrCw/studio-three-languages-published.json
