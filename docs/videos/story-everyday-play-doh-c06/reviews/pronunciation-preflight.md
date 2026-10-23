# C06 Play-Doh｜獨立配音文字預檢

- 審核：獨立發音預檢代理 `codex-gpt6-c06-pronunciation-audit`，2026-10-22；僅檢查文字與綁定，未呼叫付費 TTS。
- 結論：**PASS（靜態配音文字）**。94 句中有 30 句含拉丁字母；這 30 句都有中文 `say`，且 `say` 不留拉丁字母。每句 `say_for` 都等於該句 `text` 正規化 NFC 後的 SHA256 前 12 碼。其餘 64 句沒有不必要的 `say`／`say_for`。
- `script.md` SHA256：`80671FCE0CC1D03E46B68361173FB547B156C255F1AF10468E3011389E08232F`
- `video.json` SHA256：`666CD45A5E126D7F17DD95CCE1CACE213B07EAA2597340D3661D5CC3C3C4CBFA`

## 名稱與念法

| 文字 | 預定讀法 | 判定 |
| --- | --- | --- |
| Play-Doh（c060410、c060416、c060509、c060613） | 培樂多 | 與[孩之寶繁體中文台灣說明](https://instructions.hasbro.com/zh-hant-tw/instruction/play-doh-kitchen-creations-drizzy-ice-cream-playset-featuring-drizzle-compound-and-6-non-toxic-play-doh-colors)的產品名稱一致。該頁只用於核對當代中文名稱，不替歷史敘述背書。 |
| Kutol、Kroger、The Strong、Rainbow Crafts、Macy's、Marshall Field's、Fun Factory、General Mills、Kenner、Hasbro | 庫托、克羅格、史壯玩具博物館、彩虹工藝公司、梅西百貨、馬歇爾菲爾德百貨、造型工廠、通用磨坊、肯納、孩之寶 | 全集同詞同讀，意思可辨；Kutol 的「庫托」是暫定音譯，沒有取得公司正式念法音檔，不宣稱官方譯名。 |

`say` 中有替換英文名稱後留下的中文字間空格（例如「史壯玩具博物館 的」）。靜態檢查無法判定 Gemini 是否會因此停頓；首輪音檔須逐句聽讀、對照轉錄，對實際誤唸或不自然停頓的句子做有界重唸。此 PASS 不代替站主稿件核准、故事專屬發音字典關卡、實際配音長度或音訊驗收。
