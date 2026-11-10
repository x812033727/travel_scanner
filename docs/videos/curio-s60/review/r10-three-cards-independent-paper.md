# S60 R10｜三張來源卡獨立紙審

2026-10-22 UTC。**PASS：僅限 s60003、s60007、s60008 的 template/data 卡片替換與來源界線。** 我不是此次來源卡作者；先前曾撰寫這三景被替換的插圖提示詞，本次獨立核對 root 新寫的卡面文字，不宣稱整集原創或原圖獨立覆核。

## 差異與旁白

將作者 JSON 的三項 old template/data 反套現稿，重建 video SHA-256 恰為 `67c40dcdc56373a9aff78f21743f67f41bae7aba296f8afd3681b7cf79061a7e`（R9 凍結版）。因此本輪只有三景 template/data 變更，全部 109 個 spoken lines、ID、情緒、其他場景及頂層設定逐欄不變。script.md 的重新產生不代表新語音內容核准；本紙審沒有聆聽或重新辨識。

| 景 | 卡面核對 | 結論 |
| --- | --- | --- |
| s60003 | 「帳門牢牢繫合」及「阿蒙森《南極》・離開小帳時」直接對應固定文本 L13081–13083 的 securely laced together；中文為短譯，來源與離開時間有明示，不混作 Scott 當晚逐字發言。 | PASS |
| s60007 | 90°S 配「位置如何確認？」是南極緯度目標／待確認問題。前一句 s60006 仍問升旗腳下是否精確，後續仍解釋觀測；Amundsen L12789–12796 明說初估且非精確點，卡面未斷言升旗時已測定精確點。 | PASS |
| s60008 | 「帳內的小袋／給挪威國王的信」對應 L13064–13068 的小袋、寫給國王的信及另給 Scott 的短信；是收件對象，不表示國王已收到原件。原旁白仍問最後可證明送達誰，懸念不提前回答。 | PASS |

來源：固定 `/tmp/s60-verify-amundsen-4229.txt` SHA-256 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`，已重新讀 L12789–12814、L13060–13083。沒有添加未載的送達結論、精確定位或人物引言。

## 卡片比例與製作狀態

現稿 109 景：100 shot、9 big，按景數插圖 **91.74%**；最大連卡 **3**（s60007–009），s60002–003 為2張。以既存 17952 幀語音時間軸的逐景長度配對**現稿 template**計算，shot 為 16429 幀／17952 幀（**91.52%**），亦超過70%。既有 timeline 的三景 template 尚寫舊 shot，這是唯讀交叉計算，後續組片需由製作流程更新；本次不改 timeline 或 manifest。現稿其餘未製作插圖仍須後續原圖審核，比例不是素材完成率。

來源卡確實由 root 作者紀錄列出的三次用盡才改，沒有第4張圖。本覆核沒有生成媒體、付費、改 manifest、修改 production 檔或操作 Git。

## 凍結雜湊

- `video.json`：`b1e634627ab1d64a256e938543dcf330ac6c770f8e11747bb85c58649334ca11`
- `script.md`：`f973e8c0210be9c5657fe12b574af2d79e3cb24aa3a75a59bcf380957381d99a`
- `claims.md`：`21eab7637a46aebc28b7638d4bd720d08c7614d0aa78589d82a6d15034550edb`
- `review/r10-exhausted-three-source-cards-author.md`：`d1aaf01c16e15603919a05f57ccaf973cd67c6037653c05031983304b49ccc0d`
- `review/r10-exhausted-three-source-cards-author.json`：`54a16c4c89750ed6d08613e38b4dd0fc87702762a515c67c22c903d024b7277e`
