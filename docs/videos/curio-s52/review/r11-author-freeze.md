# S52 R11｜作者修稿凍結：1771 年觀測原報與八分鐘正文

2026-10-20 UTC。R10 刪去兩位盲讀共同否決的重述與旁枝後，正文在較快估速不足八分鐘。R11 沒有回填那些段落，而是加入直接記錄觀測鐘、三人讀時與邊緣判讀的 1771 年皇家學會原報轉錄。此為**作者候選**，不可沿用 R9 的獨立來源 PASS 或 R10 的作者檢查放行 R11 媒體。

| R11 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `8b5ece5ba66ecd672f6d8b89dd8191f087734f1d7277abce1fedca32b663f699` |
| `video.json` | `3b4ae5f3dfda56df5b7d5a18fa397e62ced2e0936bec2350bae03cdc613721c9` |
| `script.md` | `b9bae5c830d5e1260c4a034318f8bcede8a9824affa482b24d50a0e4a032be99` |

新增固定來源：Green／Cook 1771 年《Philosophical Transactions》觀測原報的 [Royal Society Corpus 文字轉錄](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt)，commit `2ac861600a431e8cb2e2eae3b1cdcd33b7350207`，本地原始位元組 SHA-256 `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`。它是 OCR，**不是原刊影像的人工逐格校對**。表格數字欄拼接，故劇本只用清楚的文字敘述和三位觀測者的欄位存在性，不推算秒差；原報說明 [L150–160](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L150-L160) 對初見暗影、亮線漸斷、邊緣難辨與數秒不確定有直接記述。較早 Cook 日誌與 Kippis 固定來源 SHA 仍見 `research.md`。

R11 把五月章起點改為五月十日儀器安妥及鐘的校對，接回五月三十日分遣者訓練；把 Kippis 的 Green 單人四格表留作中段有限線索，隨即翻開 1771 年報告，讓觀眾看到 Cook 與 Solander 各自記法和 Cook 自述的判讀難題。結尾的兩隊外派數據問題仍限定於本集三份固定文本，沒有推稱其他所有史料均缺失。

本地機械檢查：**118 景＝115 張插畫／2 張卡／1 片尾，120／120 旁白與主張表按 ID、順序、字面相同且 ID 唯一；21 組伏筆，8 章；`lint --slug curio-s52 --json` 0 errors／0 warnings，`git diff --check` 通過。**同一 `estimateTimeline` 在 250／300／325 CPM 的濃縮開場為 **43.87／37.80／35.63 秒**，正文為 **10:19.70／8:53.40／8:22.63**；這仍是估時，真正八分鐘要在 TTS 後量。`npm run test:docs-videos` **236／236**、`npm run check:tasks` **2125 票**通過。

下一關須另一位工作者按上列精確五檔 hash 重開三份固定來源，逐句與書面畫面覆核；兩位未讀 R11 的讀者分別盲讀十三題，再按系列合併規則作正式判定。其後才可做精確稿政策、站台卡與付費語音／媒體。R11 未合成語音、插圖、配樂、動畫或成片，也未取得站台劇本核准或真實 YouTube 連結。
