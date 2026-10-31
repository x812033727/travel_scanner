# S49 R26｜第二章提示詞的私人圖單離線重綁

2026-10-22 UTC。**26 張既收圖綁定 PASS；第二章八景僅書面 PASS，原生圖及全片 storyboard 仍待。**[R26 八景非作者紙審](r26-next-chapter-eight-prompt-independent-pass.md)已按精確稿通過；本回只更新私人 keyframes manifest 的視覺雜湊，沒有影像、judge、音樂或其他付費呼叫。

## 精確差分與圖單

現行 R26 `video.json` SHA-256 `57027ce7870f736e8662b6774ed4f6e85922d153e6ac864fb8a9ca1cf389ca22`。以[六提示詞可逆差分](r26-next-chapter-six-prompt-structured-diff.json)逐一將 `after→before`，可逐位元還原 R24 `video.json` SHA `98e00e94079f0725068ecdc44be124934fc69540c0d9be62a0c8340d2222d13c`。六個變動僅為 `moon032/034/035/036/037/038` 的 `data.prompt`，都尚未畫；其餘場景、台詞、運鏡、首章與 `moon031` 字卡未變。R24 `visual_hash=30ca7d69acc3fc9a` 恰等於舊 manifest；R26 工具計算值為 `5781d6810538eb41`，`look_hash=98a370ae40badbaf` 不變。

`STOP` 在位、jobs 空且 ledger 未變時，先備份 R24 私人 manifest 至 `/workspace/.video-work/curio-s49/rebind-backups/r24-manifest-before-r26-prompts.json`（SHA-256 `4f40a7ad117ed6393b4fea39e4cfbd206ee0312b1c6c9b25ba8e3bc48e72c611`），再離線、原子地**只改 `visual_hash`**，新 manifest SHA-256 `d6089aa83b3de5ee2e3e32bfeddd55b0ed3adcc2f19d7892a805bec060a31bcb`。將新 manifest 的 `visual_hash` 換回 R24 值後，整個 JSON 與備份逐項相等；其中 26 張先前 KEEP 的完整條目、選圖、judge、縮圖來源及空的 contact sheet 清單均未動。`moon031` 退圖仍不在 manifest；只讀 `renderPlan` 確認該景仍輸出帶「鏡筒重三千磅」的 `big` 字卡。

對這 26 張執行工具 `keyframeProblems` 得 **0 問題**，包含實際選圖檔案 SHA 核對。完整 R26 分鏡有 120 個 `shot`，目前仍有 **94 張未畫**；其中第二章 `moon032–039` 八景書面放行、原生圖未驗。私人 ledger SHA-256 維持 `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`，即 **US$0.9990／74 image／74 judge／0 reservations**，低於整集 US$5.30 上限；jobs 空、`STOP` 保持。下次付費試畫仍須逐景限額、看原圖並依故障停批，不能由本次重綁宣稱全片已完成。
