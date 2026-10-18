# 頻道浮水印

站主 2026-10-11 要求在影片上加 logo 或浮水印，擔心影片被原檔搬到其他平台。
決定是右上角一個小台標：`Mokaair`，下面一行小字 `YouTube @Mokaair`，米白字、深色描邊。
只有之後新做的片才有；已成片、已核准、已上傳的片一律不動。

它擋得住原檔照搬，擋不住刻意裁切或貼圖遮蓋。要真的去不掉，就得放進畫面中央，
每位正常觀眾都會一直看到，站主沒有選那個做法。

## 哪些畫面有、怎麼放上去

成片是逐場景編碼、最後 `-c copy` 接起來的，沒有整支重編的那一步，
所以標記在每個場景畫出來或編碼的時候就放進去：

| 畫面 | 怎麼放 |
| --- | --- |
| 投影片、卡片、螢幕錄影（HTML 畫的） | `chrome()` 把圖畫在右上角，取代原本的 `MOKAAIR` 小字 |
| 片段、靜態圖運鏡、會漂移的卡片 | `assemble` 編該場景時用 ffmpeg 疊一層 |
| 卡片式 Shorts、漫劇裁切的 Shorts | 編碼時疊在標題列右端（安全區 x 78–902 之內） |

兩種放法用的是同一張圖、同一個位置，換場景時標記不會跳。實測投影片畫的與 ffmpeg 疊的
在同一批像素上（互比 39.6 dB，錯開一個像素剩 15.9 dB）。

插圖投影片裡只有一個狀態的卡片會被 `assemble` 當成運鏡畫面慢慢漂移。標記畫進卡片的話會
跟著漂，切到下一張圖又跳回來，所以這種卡片的右上角留空，由 `assemble` 疊上不動的標記。
`frames/manifest.json` 的每個卡片場景用 `marked` 記錄它自己的畫面有沒有標記。

## 誰決定一支片有沒有標記

只有 `render` 決定，而且只決定一次：

- 這支片有釘選檔 `watermark.json` → 用釘選的版本。
- 沒有釘選，但已成片、已核准、已有上架包或已上傳 → 不加。重畫出來的畫面跟以前逐位元組相同。
- 其餘（第一次畫）→ 用目前的版本，寫進 `frames/manifest.json` 的 `watermark`，
  manifest 寫完後才寫 `watermark.json`。

`assemble` 不自己判斷，只照 manifest 做，並把 `watermark`（版本、雜湊、位置）記進
`checks.json`。兩個階段各判斷一次會出錯：第一次 `assemble` 沒過檢查時仍會留下 `final.mp4`，
下一次就會把它當成「標記出現之前就做好的片」，結果投影片有標記、滿版畫面沒有。

`core/state.mjs` 不比對浮水印，所以換了預設版本不會讓任何舊片重新排隊。

已成片但還沒核准的片要補標記，明確指定：

```bash
node tools/video/cli.mjs render --slug VIDEO --workdir /video-work --adopt-watermark
node tools/video/cli.mjs assemble --slug VIDEO --workdir /video-work
```

之後照一般流程重新送成片關卡；新的 MP4 是另一組 bytes，原本的核准不算數。
已核准、已有上架包、已上傳的片會被 `--adopt-watermark` 拒絕。

Shorts 沒有釘選：每次建置都是新的目錄，新建置一律帶目前的版本，`checks.json` 記下是哪一版。

## 版本只增不改

圖在 `tools/video/watermark/<版本>/`，`long.png` 給 1920×1080、`shorts.png` 給 1080×1920，
各自的 SHA-256 與位置登記在 `tools/video/core/watermark.mjs`。這是 `tools/video` 底下唯一進 git
的媒體檔（片頭片尾留在 repository 外，見 [BRANDING.md](BRANDING.md)）：它只有幾十 KB、
不含授權素材，而且每支釘選的片都靠版本號找回同一組 bytes，所以必須跟著程式碼走。

換外觀就加新版本，不要改舊檔：

```bash
node tools/video/watermark/generate.mjs --out /outside/repo/mark-v2 --channel msedge
```

看過圖之後複製到新的版本目錄，把指令印出的尺寸與 SHA-256 登記進去，再改 `CURRENT_WATERMARK`。
不同機器的瀏覽器畫出來的反鋸齒略有差異，所以同一個版本絕不重畫；測試會擋下被改過的檔。

標記是不透明的。溶接與 Shorts 的循環尾都會把一格已經帶標記的畫面疊到另一格上，
半透明的標記在重疊處會變亮。長片的標記疊在溶接之前，兩張各帶一次標記的畫面互溶，
結果仍是一次；Shorts 的標記疊在卡片與字幕之上、循環尾之下，最後一格才會精確回到第一格。

## 從有標記的集數裁 Shorts

`shorts from-drama` 從 16:9 成片裁出 608 px 寬的視窗。集數右上角有標記時，視窗掃過去會露出
半個放大的標記，所以工具讀集數 `checks.json` 的 `watermark.box`，把每個視窗限制在標記左邊；
被推回來多少記在 `checks.reframe.shots[].mark_shift`。主體本身就在標記那一側、視窗已經框不到
它時，建置會停下來並指出是哪個鏡頭，請改 `--from`／`--to` 避開。

## 不會有標記的東西

- 片頭片尾：本來就是頻道動畫。
- 縮圖：有自己的品牌字。
- 匯入的成片（`import`、`shorts import`）：只複製位元組，不重編。
- 合集裡的舊集：合集直接接各集已核准的正文。
- 這個功能上線前已經 render 的片，以及已經在 YouTube 上的片（YouTube 不能換檔）。

## 檢查

- 會問「畫面有沒有文字、logo、浮水印」的模型只看關鍵圖與原始片段，從不看成片，
  所以標記絕不能畫進關鍵圖或片段，只能在 `render`／`assemble` 放。
- 投影片場景的 PSNR 比的是含標記的來源圖，照常通過。
- 「從別的片段切出來的鏡頭」那個檢查拿編好的第 0 格比乾淨片段，比之前先把標記的方框
  在兩邊都塗黑（`psnrArgs` 的 `mask`）。
- Shorts 的封面仍是第一段的第 0 格，循環檢查照舊。
