# 2026-09-29 三支實測 Shorts 修訂

這三份腳本修正已送到後台的實測 Shorts。原始 `pilots/`、`experiments/`、實驗回答與 protocol 保持原樣，避免改寫實測紀錄。

| 腳本 | 修正 |
| --- | --- |
| `shorts-receipt-total.json` | 明確說 A 已要求核對總額，B 再增加算式、限制及格式要求；改寫被旁白檢查標示的句子；補充與其他任務打包、每組一次的限制。275 元及差額 25 元不變。 |
| `shorts-poster-blind.json` | 備案標題由「多寫三句」改成「多加三項設計要求」；說明補齊共用任務及附加要求。將連續辨識失敗的「手機可讀」一句改為自然口語。畫面設計、原始兩張 HTML/CSS 海報及主觀盲選定位不變。 |
| `shorts-prompt-check.json` | 將「加一句先檢查」改成「多加核對要求」，呈現算式、輸出格式及海報要求一起變動；揭露全部任務打包、每組一次，不能分離個別要求效果；改寫被標示的旁白。三題及 3 比 3 結果不變。 |

三份腳本共用 2026-09-28 的兩次打包輸出，並非三場獨立實驗。精確後端模型 ID 沒有回傳，不能據此標稱某品牌版本或作模型排名。原始證據由每份腳本的 SHA-256 固定，新增查核收據必須由獨立審核者閱讀當前腳本後產生。

媒體輸出放在 repo 外。聲音使用正式設定的 Gemini Sulafat，依 voice、style、文字與發音字典計算快取鍵，只有變動或被重錄的句子重新合成。修訂旁白後由同一次 build 重建時間軸、燒錄字幕、SRT 與成片。

重建方式（在 repo 根目錄）：

```powershell
node tools/video/shorts/cli.mjs validate --file docs/videos/ai-shorts/corrections-20260929/labs/shorts-receipt-total.json --source-base docs/videos/ai-shorts
node tools/video/shorts/cli.mjs build --file docs/videos/ai-shorts/corrections-20260929/labs/shorts-receipt-total.json --source-base docs/videos/ai-shorts --workdir <repo外工作目錄> --speech server
node tools/video/shorts/cli.mjs check-audio --dir <BUILD_DIR>
node tools/video/shorts/cli.mjs qa --dir <BUILD_DIR> --verify <獨立查核者產出的verify.json>
node tools/video/shorts/cli.mjs package --dir <BUILD_DIR>
```

另外兩支使用同目錄對應 JSON。套件檢查通過、轉寫檢查通過、人工聽審、後台核准及 YouTube 發布是不同階段；不得改寫失敗的 QA 欄位使其通過。沒有頻道立場時，policy 必須保留失敗。本次修訂不改頻道設定、不設定上架授權、不上傳或發布 YouTube。
