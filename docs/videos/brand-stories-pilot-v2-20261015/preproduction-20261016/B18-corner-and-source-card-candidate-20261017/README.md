# B18 轉角旁白與首店來源字卡候選

**狀態：隔離離線候選，整片 HOLD。** 父版是[四筆來源指標候選](../B18-scene-source-pointers-candidate-20261017/README.md)，其 manifest SHA-256 為 `88ce01e6108927a6d22a59d14196719139010bd086478dcb2a62d1c27bf5eba1`。該父版指出四筆逐景引用位置，卻保留了與史料不符的「盤子在轉角卡住」及漏列 J-Net21 的首店字卡；它仍是失敗的 HOLD 證據，不在原地覆寫。

[J-Net21 原文](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)在「町工場の経営者が協力」段寫的是轉角處**輸送帶壅塞、盤子掉落**，也明記首店在近鐵布施站附近。[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)記轉角難題、1958 年約 20 坪首店，但未給「盤子卡住」的細節；[日本機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)記 1958 年 4 月布施首店，但未給車站附近的位置。

| 逐景主張 | 原指標 → 候選指標 | 可讀原文的窄範圍 |
| --- | --- | --- |
| `e1` / `engine-s041` | JSME `1` → J-Net21 `0` | J-Net21「店のそばに機械メーカー…」附近記近鐵布施站附近首店；約 20 坪仍由發明協會的字卡來源支持。 |
| `h5` / `hook-s004` | JIII `2` → J-Net21 `0` | J-Net21「町工場の経営者が協力」記輸送帶在轉角壅塞、盤子掉落；本版同步修正旁白與 claim。 |
| `i1` / `idea-s024` | JIII `2` → J-Net21 `0` | 同段直接記轉角輸送帶壅塞與盤子掉落。 |
| `i5` / `idea-s031` | JIII `2` → J-Net21 `0` | 同段記採用組合扇形板片的輸送帶，後稱「ウロコ」。 |

這四筆 source 指標承接父版；JIII 的扇形**靈感**說法仍保留在其可支持的其他位置。法院 PDF 專屬 `h7/t7/t8` 仍是 source `3`／fact `4`；1962 年可讀登記 `e6/e7` 仍是 JIII source `2`、無 row fact 綁定。全部 65 筆逐景判斷仍是 `UNCHECKED`。

本版的建置器只提出以下窄修正：

1. `hook-s004` 的第一句與 `h5.claim` 改說「輸送帶在轉角堵住、盤子掉下來」；hook 的懸念與 idea 的 I01 回扣 `loops.what` 同步。畫面仍是匿名工坊、轉角壅塞、盤子傾斜的事故前一瞬間，沒有冒充史料照片。
2. `engine-s041` 來源字卡由「機械學會／發明協會」改為「J-Net21／發明協會」，讓車站位置與約 20 坪各有可直接讀到的出處；正文、數字、副標不改。
3. **隔離提出** B18 row 的 `chapters.idea.point` 與 `must_verify[3].claim` 同步改正「卡住／卡盤」。這會改 canonical story hash，既有 `episodes/reviews/B18.json` 的 row review 對新版本**失效**，不得複製為新收據。其餘九筆必查事實不變。
4. [`fullscript-impact.json`](fullscript-impact.json)釘住舊凍結全文與審稿雜湊，列明 H02、I01 和 loop 表的必要措辭替換及替換後全文雜湊。舊 `scripts/B18.md` 另有 1978 年權利說法，與現行企劃區分法院 1972 年的做法不一致；這份映射**不是完整新版逐字稿**，舊全文和舊文字審稿不能沿用作新版通過證據。

`build.mjs --write` 只在此目錄產生 row、系列投影、六章、覆蓋表、差異與驗證檔；`--check` 重算並逐位元組核對。建置器核對父版每個雜湊，保證僅上述欄位變化，並確保 85 景、88 句、65 筆 `UNCHECKED`，法院 PDF 專屬 `h7/t7/t8` 與可讀登記 `e6/e7` 的來源指標不變。

[`delta.json`](delta.json) 記所有候選檔的前後完整 SHA-256：row `21122b7d…6043e9d` → `aea048c9…ccec3`，hook 章 `a0105459…699b3` → `cb671336…47d1`，idea 章因 I01 回扣文字同步也有單欄變更，engine 章 `cca8c696…e866f` → `06230be1…bad99`；canonical story `da692f38…4a5e1` → `4585c9e5…80280`。舊 row review SHA-256 `06012b65…94ed` 與舊全文 review SHA-256 `1583b363…9cdb` 皆**不是**新候選的通過收據。

已用正式靜態卡 renderer 輸出 [`engine-s041-320x180.png`](engine-s041-320x180.png) 與 1920×1080 圖，layout 回報零問題；人工在 320×180 檢視時，來源標籤、日期／面積標題和「布施首店」均可辨識。縮圖 SHA-256 `063ed05b…f6a9`，完整值在 [`card-preview.json`](card-preview.json)。這是單張字卡可讀性檢查，不是整片成片或獨立史實審核。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-corner-and-source-card-candidate-20261017/build.mjs --write
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-corner-and-source-card-candidate-20261017/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-corner-and-source-card-candidate-20261017/render-card.mjs --write
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-corner-and-source-card-candidate-20261017/render-card.mjs --check
```

正式採用前，需由獨立審稿者重新查核新 row、四筆逐景來源及 H02 的新旁白；完整新版全文要重建並重審，不能拿歷史逐字稿只改一句當成現行全片。再處理正式工人逐章 verifier／listener／narrative 與 TTS、圖像、CC、成片關卡。本包不修改現用 `episodes/B18.json`、審稿收據、`stories.json`、舊全文或主機；未做付費呼叫、匯入、合併、部署或上傳。

採用時須另行把本候選 row 兩處措辭投影到 active `stories.json`，重做 hash 綁定 row review；以新版 row 與六章重建完整逐字稿並重審，解決舊稿 1978 年口播後，才可談匯入。本候選與父版都保持 HOLD。
