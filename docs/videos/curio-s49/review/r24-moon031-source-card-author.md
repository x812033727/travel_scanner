# S49 R24｜`moon031` 來源卡退路

2026-10-22 UTC。**作者候選，待另一位獨立紙審；沒有重畫。**`moon031` 已有三張實際原生圖：R21 童貌與現代大海報、R22 擬報紙字列及放在紙上的立體圓筒、R23 [最後一次原圖](r23-moon031-terminal-retry-stop.md)則是成年舊式讀者旁邊的似字母曲線與底線，並非鏡筒線條。三圖均人工退件；機器 R22/R23 PASS 不改變原圖判斷。R23 的服務逾時先以 **US$0** 記失敗，隨後同一 job ID／請求鍵回收為一張成功圖，**不是第四張**。依三次出圖、兩輪提示修補的上限，此景不再付費重試提示詞。

R24 只把 `moon031` 從 `shot` 改成 `big` 來源卡：

| 位置 | 字樣 |
| --- | --- |
| 上標 | **1835 年虛構報導** |
| 主文 | **鏡筒重三千磅** |
| 下標 | **1859 重印本所載，非器材紀錄** |

固定 1859 年 Locke 名下重印本原文 SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[P05 L398–413](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L398-L413)是在虛構的 Herschel／Brewster 對話內，讓 Herschel 說**父親望遠鏡的鏡筒**重 `3,000 lbs.`。保留原旁白「文章說，赫歇爾父親那架大望遠鏡，光鏡筒就重三千磅。」；卡片只標報導內的數字及重印來源，沒有畫出可被誤認為真的望遠鏡、原報影像或設計原件。`moon030` 前景仍是已人工 KEEP 的 1830 年代成年學者想像示意，`moon032` 後景是下一段虛構光學方案；此單格來源卡沒有新增年齡或年代錯置的人物。

[逐字可逆結構差分](r24-moon031-source-card-structured-diff.json)保存 `moon031` scene 區塊及 [claims](../claims.md) **同列畫面欄**的 R23／R24 全文；`new→old` 位元組回填可還原 R23。`video.json` SHA-256 `fb144f9e2af0b6c59b08c477a149b21af6291af8b0b328934d96d87e1c3fe0b8` → **`98e00e94079f0725068ecdc44be124934fc69540c0d9be62a0c8340d2222d13c`**；`claims.md` `0071e502905c7669a6bfb70c406921d52e82d5fa54a3e4c8ffd75240eb157809` → **`e6a8115bc1b9c14078e99059b836cb6d15027f67fe073671de1daa45d9d54190`**。史實主張、其他場景及全部台詞未改；只有本格改卡片而不再有運鏡。`script.md` 仍為 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`，語音文字綁定不變。

正文現在 **120 shot／8 big＝120／128＝93.75% 插圖**，高於 70%；最多連續 **2** 張資訊卡（`moon047–048`），本卡夾在 `moon030` 與 `moon032` 兩個 shot 之間。CLI `lint --slug curio-s49 --json` exit **0**、**0 errors／0 warnings**、131 句，stdout／stderr／exit 同目錄保存。私有 manifest SHA-256 `0407c0e6ac63aa6e5d394aecbd2ed9963ccf01a33babd1da015f764105e65b48`、ledger SHA-256 `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893` 均未動；26 張已人工 KEEP 的選圖保持原樣。manifest 裡雖仍留有被退件的 R23 `moon031` 圖，`big` 場景不應使用它，分鏡覆核須確認實際輸出採卡片。帳本仍 **US$0.9990／74 image entries／74 judge／0 reservations**，低於 **US$5.30** 上限；`STOP` 在位。本輪沒有付費、commit 或 push，完整 storyboard、網站卡與人耳審查仍待後續關卡。
