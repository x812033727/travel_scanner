# 嵌入向量：A 案來源包

目前完成來源撰稿、離線重算及獨立事實／聽眾審稿；尚未合成旁白、產圖、渲染、上傳或發布。獨立查核記在 verify-1.md，綁定目前 video.json 的 SHA-256，不能代替影音驗收。

## 核准大綱與內容

採核准 A 案「第一名，門卻關著」六章順序。正常 outline gate 已由協調者提交並從伺服器取回：approved_at 2026-10-04T12:51:37.582098Z；review-pull 2026-10-04T12:51:55.742Z。核准 brief SHA-256 是 `c7509f90e80de9fc4acc4c409ee6f46a564a25dfad9adbb1360622289cfdcdbb`。本包沒有改核准 brief.md 或 claims-source-notes.md。

以原創社區活動的「搜尋第一名但門關著」開場，先說明手填向量，再分開內容表示、分數、原文條件。最後回應關門原因，留一個觀眾動作：回讀原文，圈必要條件，沒寫的保留未知。全文採繁中旁白；聲音維持 Gemini Sulafat，使用既有 STORY_VOICE_STYLE 的標準國語、台北語調。沒有新增 model 欄位、改付費設定或修改共用發音字典。

## 檔案與重建

- video.json：六章完整長片，156 個穩定 line IDs、121 個 scene、80 個 shot。
- build.mjs：重建 video.json、shorts.json、draft-metrics.json；只處理本集來源。
- line-ids.txt：保留六個起始 ID，另外由正常 CLI 產生 220 個保留 ID；本稿使用其中 150 個。
- demo.py、demo-log.md：原創標準函式庫程式與兩次實跑紀錄。
- claims.md：22 個主張及全部 scene 的證據對照。
- shorts.json：兩支從本片抽出的精華，各沿用五個 shot；沒有新增待購圖片。
- draft-metrics.json：估算時長、口播量、節奏、插圖占比與完整合併 prompt 長度。

從 repo root 執行：

```text
node docs/videos/ai-term-embedding/build.mjs
node tools/video/cli.mjs lint --slug ai-term-embedding
```

離線示例從本集資料夾執行：

```text
python -X utf8 demo.py
python demo.py rank-first
python demo.py rank-last
python demo.py top
python demo.py all
python demo.py control
```

重建不會呼叫模型、合成音訊、買圖或寫伺服器。程式需要既有 repo Node 工具；示例只需 Python 標準函式庫。private 收據應放在 `<home>/mokaair-work/ai-series-continuation-20261004/`，不寫入來源包。

## 原創示意與可重跑邊界

六筆活動、人物、查詢向量及資料向量全部由作者手填。兩個數值維度沒有自行命名，不是任何模型 embedding、tokenizer、訓練結果、否定句能力測試、ANN、資料庫效能或真實營業資訊。第一個數值畫面之前，toy-disclosure 已用旁白與正式字卡明示這個範圍；兩支短片也各自先聲明。

餘弦完整排序為 N001、N002、N004、N003、N005、N006；作者指定只查前兩筆得到空符合清單，查全六筆才得到 N003。N004、N006 仍為 UNKNOWN。另一個控制只改相同人工向量的 open_today 欄位，分數不變，條件從 MATCH 改為 REJECT；沒有把改過的文字送去編碼。MATCH 僅符合虛構欄位，不是真實活動保證。所有正文數值與終端摘錄均可在 demo-log.md 重現。

官方機制資料與原創實算分開引用。Google 與 Sentence Transformers 的當日官方文件、代表性 SBERT 論文，以及已發布 [Mokaair 嵌入文章](https://mokaair.com/zh-TW/life/ai-term-embedding)，均列在 claims-source-notes.md、claims.md 與 video.json。既有自有 SVG 用於正式圖解，精確向量、公式與六筆清單放字卡，生成插圖只承擔故事動作。

## 目前估算與待實測

口播共 3,109 單位，估算 body 為 885.47 秒，約 14.76 分鐘。target_minutes 的 8–12 是原先規劃區間；為把六筆資料、機制邊界與控制講清楚，本稿超過原估。較短句補了必要條件與計算範圍，估state都在5–7秒，沒有用空白或停頓湊時長。尚未合成旁白，以上不是成片時長。

| 章 | 估算起點 |
| --- | --- |
| 第一名，門卻關著 | 00:00 |
| 內容怎麼變成表示 | 02:11 |
| 分數比的是什麼 | 05:06 |
| 重跑排序，回讀原文 | 07:24 |
| 同維度還要相容 | 11:23 |
| 條件圈出來，未知留下來 | 13:37 |

估算state最短5秒、最長7秒、平均5.7秒，cadence hard problems為空；插圖占約50.75%。六章各有獨立場所、當地光源、人物互動及手部特寫；每個shot一句旁白，精確條件留在字卡。80個raw prompts都是ASCII，最長309字元；實際scene＋style＋camera＋avoid合併最長1,288字元，build在超過450／達到1,500時拒絕重建，沒有暗中截斷。這只證明來源要求與長度，未證明模型實圖會符合動作、裁切或無字要求。

CLI lint目前0 errors、1 warning：開場章約131秒，啟發式把整章當hook。真正hook是第一句，估在4.97秒內；第二景承諾估在11.03秒內。保留核准的六章，不為消除警告增設短章或加靜音。後續以實際TTS timeline重驗章節、state、插圖占比與開場時間。

兩支 Shorts 的口播量為 120／138 單位，使用長片既有 shot。短片目前亦只有已獨立審查的來源，沒有實際時長或播放驗收。全部音訊聽辨、實圖審查、長片與短片渲染／播放、正式上傳，以及完成後的 G 槽備份雜湊與清理，仍屬後續製作關卡。
