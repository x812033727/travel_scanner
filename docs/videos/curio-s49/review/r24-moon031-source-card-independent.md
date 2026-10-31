# S49 R24｜`moon031` 來源字卡獨立紙審

2026-10-22 UTC。**R24 創作差分 PASS；完整分鏡仍 HOLD。**本回只審 `moon031` 改字卡的來源、相鄰分鏡、差分及既有圖片綁定，沒有新增或核准影像、語音或成片。

## 原文與畫面

固定的 Locke 名下 1859 年重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[L398–413](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L398-L413) 確有虛構 Herschel／Brewster 對話：其中稱 Herschel **父親望遠鏡的鏡筒**重 `3,000 lbs.`。這不是可核實的器材重量，也不是 1835 年原報掃描。現行旁白以「文章說」限定，字卡上標 `1835 年虛構報導`、主文 `鏡筒重三千磅`、下標 `1859 重印本所載，非器材紀錄`，三者合讀沒有把報導數字當史實。`claims.md` 的 P05 錨點涵蓋該原文；字卡亦未假造實物、設計圖或原報影像。相鄰 `moon030` 是已收的省去鏡筒想像插畫，`moon032` 接續報導內的暗室構想；新卡位於兩張 `shot` 之間，不打斷這個因果接點。

## 差分與系列規則

我以 [R24 結構差分](r24-moon031-source-card-structured-diff.json) 的 `after` 各替回 `before`，親自重新雜湊：`video.json` 精確還原 R23 `fb144f9e2af0b6c59b08c477a149b21af6291af8b0b328934d96d87e1c3fe0b8`，`claims.md` 精確還原 R23 `0071e502905c7669a6bfb70c406921d52e82d5fa54a3e4c8ffd75240eb157809`。目前 R24 雜湊分別是 `98e00e94079f0725068ecdc44be124934fc69540c0d9be62a0c8340d2222d13c`、`e6a8115bc1b9c14078e99059b836cb6d15027f67fe073671de1daa45d9d54190`；劇本仍是 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。故可見的內容差異僅是 `moon031` 的 `shot → big` 和 claims 同列的視覺註解；台詞、來源鏈及其他場景未改。

正文共 128 景：120 `shot`、8 `big`，插圖占 **93.75%**，卡片最多連續 **2** 景，符合系列至少 70% 插圖、最多 3 張連續卡片的界線。這張卡只承載一個數字與來源，不是以卡片取代尚可修補的整集畫面：R21／R22／R23 的三張實際 `moon031` 原圖均已退件，兩輪提示修補已用盡；R23 逾時 job 是同一請求鍵回收，非第四張。[R23 原圖停線](r23-moon031-terminal-retry-stop.md)記錄了最後一張的似字形問題。獨立重跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` 得 **exit 0，0 errors／0 warnings，131 lines**。

## 既有圖片與下一關

私人 manifest SHA-256 `0407c0e6ac63aa6e5d394aecbd2ed9963ccf01a33babd1da015f764105e65b48`，與 R23 終態快照逐位元相同；除 `moon031` 外的 **26** 個已收選圖檔案均存在且各自雜湊符合 manifest。帳本 SHA-256 `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`，仍為 **US$0.9990／74 image／74 judge／0 reservations**，小於 US$5.30 整集上限；`STOP` 在位、沒有待續 job。R24 沒有新增付費呼叫。

manifest 尚含 R23 被人工退件的 `moon031-1-trim.jpg`，且仍綁 R23 的 shot 清單；**不能把這份舊 manifest 當成 R24 已可輸出的完整 storyboard**。工具的 `shotScenes` 只取 `template: "shot"`，`assemble` 另要求 manifest 的 `pictures_hash` 對齊當前 `video.json`，所以在正式分鏡審核前須重新建立 R24 清單並檢查 `moon031` 實際呈現的是字卡、舊退件圖未被引用。保留其餘 26 張的選圖與雜湊，不再對 `moon031` 付費重畫。全片其餘場景、站台卡、人耳旁白與成片關卡仍待完成。
