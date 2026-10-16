# Mods 教學改版

這是 2026-10-09 依站主「開始改善」完成的本機改寫包。沿用同一個工具呼叫計數器，從效果、原理、載入前檢查，到操作與結果核對。原本各章不同的生活比喻已移除。

## 閱讀順序

1. [企劃與證據界線](brief.md)
2. [逐句稿與畫面安排](script.md)
3. [機器可讀影片來源](video.json)
4. [事實查核表](claims.md)
5. [範例程式與尚未執行的測試](demo/README.md)

`assets/` 的五張 SVG 為本次原創機制圖，不是產品截圖；同一版面逐步亮起模型、工具事件、Mod 與介面。畫面中的計數明確標示為示意。公開官方文件擷取由 `video.json` 的 screencast 步驟定義。

## 製作狀態

- 完整改寫、官方來源核對、獨立稿件閱讀審查已完成。
- 保留原有 Sulafat 與 `voice.style`。可關閉 CC，沒有燒錄旁白字幕。
- 新版旁白、實際時長、ASR／音訊審查、成片視覺 QA、字幕包與後台匯入尚未完成。
- 沒有重用原片的 script/audio/final 核准，沒有更動原片的上架狀態。
- 沒有完成本機 Mod 執行驗證。自動核准審查拒絕隔離 CLI 的組合執行指令，唯一原因為 `blocked by policy`；沒有換途徑重試。

同 slug 的正式來源另有英文配音 producer lease，程序是否仍在執行尚未確認。此處的來源不應直接覆蓋正式來源：先確認原工作交接，再以獨立改版工作區和新的來源雜湊進入製作流程。

## 重現檢查

```powershell
node docs/videos/claude-code-mods-no-sandbox-before-install/assets/build-diagrams.mjs
node tools/video/cli.mjs lint --slug claude-code-mods-no-sandbox-before-install
node tools/video/cli.mjs render --slug claude-code-mods-no-sandbox-before-install --workdir <repository 外的新工作目錄> --channel msedge
```

完整動畫渲染可分段續跑；STOP 只代表停在畫面邊界，不是製作成功。靜態畫面預覽不能替代旁白實測、轉場檢查或成片驗收。下一階段必須對照更新後來源重新建立時間軸與審查證據。

本次檔案、預覽、雜湊與檢查結果見 [製作紀錄](revision-review.md)。
