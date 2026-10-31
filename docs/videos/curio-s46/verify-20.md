# S46 R11｜片尾口播政策窄修：作者凍結

2026-10-20 UTC。**這是作者改稿及自查，尚非 R11 獨立史料／書面畫面覆核、兩名新讀者盲讀或 Jev 政策 PASS。**R10 的[獨立來源與畫面](review/r10-source-independent.md)及[雙盲敘事](review/r10-official-panel.md)均只綁 R10 精確檔案。R10 的[完整 `explainer` 政策檢查](review/r10-policy.md)判 **FAIL**：業配 0.34 高於 0.30；Jev 沒指出是哪一句，不能據分數斷言片尾是原因，也不重送同一請求。

R11 只將口播片尾 `bkw999c` 的「想沿原文看更多歷史故事，訂閱奇聞檔案局。」改為「**原著固定版連結放在說明欄，方便核對她的記述。**」消除可疑的口頭訂閱推銷，同時把已存在的固定來源 URL 交代清楚。`video.json.youtube.description` 已列 1895 年自傳的 GITenberg 固定 commit 全文連結；同欄的頻道 URL 也保留。這句是上架內容承諾，沒有新的歷史事實。片尾 `data.cta`「訂閱奇聞檔案局」、共用 21 秒 `v4-endscreen` 與最後 16 秒兩個推薦框和訂閱圈的計畫保持不變；實際可點元素仍須私人上傳後在 Studio 設置、測試。

與 R10 Git 基線相比，`video.json`、`claims.md` 各只改 `bkw999c`，`script.md` 由 `script --slug curio-s46` 重生，除該句及末尾版本標記外未變。`brief.md`、`research.md`、其他 119 句、所有提示詞、卡片、章節、來源與標題未動。

| R11 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| `research.md` | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| `video.json` | `f59ec9508ce6f5d61f867e2d2a74c74166a3bde4282b4153c9b71f07469f752b` |
| `script.md` | `3cc22cc5b69a782a420a78396f715bc22670dddfda3cf3c7ddacaa352df7194a` |
| `claims.md` | `947e5afe656da6df441a4d053e895944342584d3c43c23caa729cbb0aba4d609` |

`video.json`、重生 `script.md` 與 `claims.md` 的 **120/120** ID、旁白與次序相合且無重複；固定自傳 URL 已在說明欄，畫面 CTA 在 `outro.data.cta`。`lint --slug curio-s46 --json`：**0 errors、1 warning**，只警告片尾沒有口播訂閱；畫面訂閱 CTA 仍在，沒有為消警告再加入可疑口播。工具估開場約 0:49、全段 11:42，正文文字未改，先前按每秒 4.5 漢字的保守估計仍約 **8:06**；沒有 TTS 實測。

下一位工作者須對 R11 精確版本重審史料與書面畫面、讓兩名此前未讀 R11 的讀者做同稿盲讀；通過後才對**完整 R11** 做一次新政策判讀，並處理網站審核卡。R10 的政策 FAIL 不會因改字自動解除。至此沒有 TTS、付費插圖、配樂、成片、上傳或可點 Studio 元素。
