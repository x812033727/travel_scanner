# B18 說書節奏完整稿：隔離第三候選

**離線全文文字審查 PASS；正式工人與影片製作仍 HOLD。** [`B18.md`](B18.md) 的 SHA-256 是 `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1`。[後續獨立全文審稿](review-candidate.md)對這份精確稿件判定 P1 0／P2 0，只涵蓋文字的來源、事實與敘事。它修的是[第二版完整稿](../B18-listener-flow-fullscript-candidate-20261017/B18.md)在[獨立讀稿 HOLD](../B18-listener-flow-fullscript-candidate-20261017/INDEPENDENT-READING-HOLD.md)中留下的四項 P2。第二版 `B18.md` SHA `1b7891f00fecbbf09fb1ff9dc131cde291188158acfca616098d93afed83bcdb`、審稿 SHA `98b6609c2d762bffa3844990e4134dad9109ff732de59043da67ecba5b647181` 保持原樣，審查結果不能延伸到本版。更早第一版完整稿與獨立 HOLD 亦原樣保留。

父版是[逐景歸屬 flow 候選](../B18-attribution-flow-candidate-20261017/README.md)，canonical story SHA-256 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`、manifest SHA-256 `8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754`。本稿沿用它的事實、來源和六章因果線，**不是逐景章稿的逐字 patch**；row 與 65 筆場景 claim 的 fact/source 路由沒有由本包修改，65 筆仍是 `UNCHECKED`。

| 第二版 HOLD | 第三版改法 | 採用界線 |
| --- | --- | --- |
| I03 把原文 `ウロコ` 說成 J-Net21 的中文原稱 | I03 先讓扇形板過彎，再說報導的日文名 `ウロコ`、中文可說魚鱗板 | `ウロコ` 必須試聽台灣口音 TTS；字卡保留原文。 |
| N02「那片片」重字 | 改「早期那些扇形板」 | 須通讀全稿聽感。 |
| I01–I04 連續約 93 秒逐段以來源開場 | I01 從盤子掉落進場；I02 撲克牌／名片雙來源在句中點名；I03 過彎後才講 J-Net21 原詞；I04 在試作過程中承接「前面那篇報導」及家屬回想。明講 J-Net21 的段落由 6 降為 5，帶來源家族語由 10 降為 9。 | H02 已把轉角掉盤歸屬 J-Net21，I01 是回到同一問題；I02/I03/I04 可聽見地區分兩種靈感與約十年試作。本版與逐景 flow 的 i1/i5/i6/i7 **句序不同**，若採用必須同步正式章稿和逐景來源審查，不能只移走歸屬。 |
| E05 同義反覆、把備料影響推得過遠 | 保留萬博西口站前、長隊、300 日圓桶裝套組、員工長工時與博志剝蝦剪海苔的回想；只用一句話限縮說明送盤機器不會自動備料。 | 不宣稱減員、實際工時差額或人手重新配置；價格與 1958 首店 50 日圓分開。 |

H02 把第三問改成「盤子怎麼從後場送到客席」，不再推斷相對距離；三個 setup 分別對應轉角、萬博西口站前的送餐量、後場到客席的路線，正文 I、E05、T04 回收。T04 客席布局只作店型比較，不得畫成某間實際店的平面圖。歷史 20／50／300 日圓分時代、撲克牌／名片分來源、道頓堀展店年份不口播、[法院官方判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)只限定第 579776 號 1972 年期滿，以及[日本機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)的 1985 堺東店機器與另外保存的早期板片分開呈現，均延續前兩版邊界。其餘逐段來源列在稿件製作註和來源索引；主要來源為 [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)和[石野官方年表](https://www.ishino-group.com/history/)。

[`check.mjs`](check.mjs)只在本候選目錄寫[`verification.json`](verification.json)，pin flow manifest 與逐檔內容、兩版已審稿及其 HOLD 報告、[採用前 row 快照](../B18-active-before-attribution-flow-20261017/episodes-B18.json)，並釘住本版的[獨立離線讀稿](INDEPENDENT-OFFLINE-READING.md) SHA `b2945b745be24c5429365ccd7a519fecf58bf6d58cd71f1c63cdb3fb0d6eb99e`。它不讀可變的正式 active row；機械檢查六章／25 段／25 來源註、三個 setup 與回收、口頭來源邊界、禁用爭議年份、來源密度及片頭片尾 cue。執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-spoken-source-cadence-candidate-20261017/check.mjs --check
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-spoken-source-cadence-candidate-20261017/check.mjs
```

量字為 2,667 漢字／數字；以歷史試作 300 字／分鐘**估**正文 8 分 53 秒、開場 26 秒，連 5 秒片頭與 21 秒片尾約 9 分 19 秒。這不是 TTS、Jev 或成片實測；正文若較快，可能跌破八分鐘下限，不能靠慢播、空白或重複補時。`J-Net21`、`ウロコ` 和實用新案號碼仍待台灣口音試聽。`OFFLINE_SCRIPT_STRUCTURE_ONLY_HOLD` 是候選機械狀態，**不是獨立全文或正式工人審稿 PASS**。

本版 SHA 已有獨立離線讀稿及後續**獨立全文審稿**，皆未見 P1／P2；這不是正式 worker 或站主的驗收，也沒有 TTS 聽感證據。製稿時產生的 `verification.json` 將 `formal_new_fullscript_review_complete` 記為 `false`，是審稿前的歷史機械收據；後來的審稿結果只記在獨立的 [`review-candidate.md`](review-candidate.md)，不能藉修改舊收據宣稱工人關卡通過。正式製作仍要同步逐景章稿的 i1／i5／i6／i7／n7 句序與來源歸屬，重做 65 筆 worker verifier、listener／narrative、TTS 時長與發音、插圖、繁中 CC、聲畫 QA、成片審核和站主上傳決定；任何改字都需新 SHA 與重新審查。本候選製作當時沒有改正式主機、active、歷史稿與任務票，也沒有模型或媒體付費、匯入、合併、部署、上傳或發布。
