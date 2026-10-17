# B18 聽眾流暢版完整逐字稿：隔離第二候選

**HOLD；尚未正式審稿、採用或製作。** [`B18.md`](B18.md) 是在[第一版完整稿](../B18-fullscript-candidate-20261017/B18.md)與其[獨立全文審稿 HOLD](../B18-fullscript-candidate-20261017/INDEPENDENT-FULLSCRIPT-REVIEW.md)之後，專修兩項 P2 的新版。第一版與審稿原樣保留，審查只綁第一版 SHA-256 `41d3e8d321bdfbb94fefb8039df3713303e5380779ede982165d1d0f1596dfa6`，**不延伸到本版**。本版 SHA-256 `1b7891f00fecbbf09fb1ff9dc131cde291188158acfca616098d93afed83bcdb`。

本版以[逐景來源承接 flow 候選](../B18-attribution-flow-candidate-20261017/README.md)為父版，manifest SHA-256 `8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754`，canonical story SHA-256 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`。row 與 65 筆逐景 claim 的來源／fact 路由未變，**65 筆仍為 `UNCHECKED`**。本稿重新寫成六章口播，不是可直接覆蓋工程 `story/chapters/` 的逐字 patch。逐景版 i5 明講 J-Net21、i6／i7 用「同一篇報導／報導還記載」承接；本稿 I03／I04 同樣保持可聽見的連續先行詞。N02 的回顧則減少重唸來源名，與逐景 n7 的表面句子不同，正式採用須同步對齊並重審。

| 第一版 P2 | 本版修正 | 保留的界線 |
| --- | --- | --- |
| 25 段中 10 段唸 J-Net21，約 15 段帶來源家族語 | 依同一離線計數規則降為 6 段、10 段；非 `attributed` 事實的完整來源留在逐段製作註／字卡 | 轉角堵帶與扇形解法、撲克牌／名片兩說、警告與加盟店獨立、萬博表彰與約 240 店、後場直線、家屬推測及法院第 579776 號窄認定仍可聽見地歸屬。不能為節奏把有爭議說法改成無來源定論。 |
| H02 萬博與日後店型像章節目錄 | 三個 setup 現落在轉角掉盤、萬博西口站前店面的人潮、後場師傅如何把盤子送到客席；正文 I、E05、T04 回收 | 沒寫可考證資料以外的特定開門或排隊動作，也不在開場揭露魚鱗板、桶裝套組或直線帶答案。 |

口播與畫面的史實界線沿用第一版：早期立食店 20 日圓、1958 首店 50 日圓、萬博桶裝套組 300 日圓分清；1960／1962 道頓堀資料歧異不口播展店年份；[法院官方判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)只支持第 579776 號這一項實用新案 1972 年期滿，未把其他權利或競爭者的進場原因一併歸因；[日本機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)列出的 1985 堺東店機器與另外保存的早期板片分開畫。源流還依 [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)及[石野官方年表](https://www.ishino-group.com/history/)逐段標註。具體採用範圍見稿末來源索引與每段製作註。

[`check.mjs`](check.mjs)只在本候選資料夾寫[`verification.json`](verification.json)。它 pin 住 flow parent 的 manifest **及其逐檔內容**、第一版與其 HOLD 審查，以及[採用前 row 唯讀快照](../B18-active-before-attribution-flow-20261017/episodes-B18.json)；不依賴會變動的正式 `episodes/B18.json`。機械檢查六章、25 段及 25 個來源註、三個懸念回收、必須口播的來源歸屬、避開有爭議口播日期、來源名密度和片頭片尾 cue。執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-listener-flow-fullscript-candidate-20261017/check.mjs --check
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-listener-flow-fullscript-candidate-20261017/check.mjs
```

Flow parent 的 `build.mjs --check` 曾在正式 row 尚未變更時通過；現在同一 checkout 有並行的 row／review 採用工作，它的「舊 active review 必須失效」現場斷言會因採用時序而失敗。本候選的 checker 改核對 flow manifest 的固定檔案，沒有把現場可變的 active row 當作測試依據，也沒有修改那些採用檔案。

量字為 2,759 漢字／數字，以歷史 300 字／分鐘**估**正文 9 分 12 秒、三段開場 26 秒，連 5 秒片頭與 21 秒片尾約 9 分 38 秒。這不是實際 TTS／Jev 或成片時長；不能以慢播、靜音或重複補時。`J-Net21`、`ウロコ` 與實用新案號碼的台灣口音念法、相鄰來源承接的聽感，均待實際試聽。`verification.json` 的 `OFFLINE_SCRIPT_STRUCTURE_ONLY_HOLD` 絕非正式全文審稿 PASS。

下一關是以**本版 SHA** 做獨立逐段史實與聽眾審稿，特別核對 E05 備料推論、T04 客席布局推論和 H02 三個 setup；修正後須再產生新雜湊。然後才可談與正式章稿對齊、65 筆 worker verifier、listener／narrative、TTS 實測、插圖、繁中 CC、聲畫 QA、成片審核與站主上傳決定。本包沒有改正式主機、原稿、歷史審稿或 task；沒有模型／媒體付費、匯入、PR、合併、部署、上傳或發布。
