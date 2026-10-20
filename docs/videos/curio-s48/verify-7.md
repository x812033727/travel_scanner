# S48｜R6 配音實測與音訊關卡：HOLD

2026-10-20 UTC。配音前重新核對 [R6 獨立史料／書面畫面 PASS](review/r6-source-independent.md)、[正式雙盲敘事 PASS](review/r6-official-panel.md)及[全稿 Jev 政策 PASS](review/r6-policy.md)，並以 SHA-256 守住五份精確輸入。本站 `curio-s48` 為 `category=explainer`、`format=drama`；配音前讀到唯一的劇本卡 `content_sha256=ddf43a0f76cef45f378d3d34c4a1050d7391eaf11bf2faf8f8f3f3f0833e3c5f`、`hand_pushed=true`、`status=pending`、`decided_at=null`。本機 `approvals.json` 記錄站主常設推薦偏好下的**委派本機編輯選擇**：精確大綱 A 與精確 R6 劇本；SHA 為 `a199332dda8eb6956ca7a35c64404274cc4c03d5b334980867c82f8ec3ca410a`。這兩筆不是網站或站主審核決定；沒有將任何卡標為已核准。

| 精確 R6 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `video.json` | `5d8245536c1271f6cd99b930155beb3c9532e1e0b4e1247690531282ceee9bfe` |
| `script.md` | `ddf43a0f76cef45f378d3d34c4a1050d7391eaf11bf2faf8f8f3f3f0833e3c5f` |
| `claims.md` | `4324f4a9980a2a1aaab7e85c91115c7ad43f3a9c55c79f8ab042129b76e7d3b9` |

## 合成與逐句覆核

先跑 `tts --slug curio-s48 --dry-run`：102 件待合成、預估 2,896 billable characters；`gemini:Sulafat` 顯示 ready、免費額度足夠。首次合成實際 102 件／2,896 字元，首輪完整 `check-audio` 覆核 102/102 句：64 字面吻合、13 同音或語助詞差異、3 句 Jev 判可接受、**22 句 flagged**，結束碼 1。原始完整 `narration.wav`、`timeline.json`、22 份受標 WAV、原樣 `check.json`／`check-flags.json` 均在私有工作目錄封存。

第一輪只對這 22 句執行 `tts --dry-run --redo`（634 字元、Sulafat ready），再實際重唸 22 件／634 字元，其餘 80 件沿用。完整覆核重新轉錄 22 句，結果 72 字面吻合、14 同音／語助詞、3 Jev 可接受、**13 flagged**，結束碼 1。第二輪先封存當時完整 WAV／時間線與 13 份受標 WAV，再確認 `tts --dry-run --redo` 為 13 件／364 字元、Sulafat ready，實際重唸 13 件／364 字元，其餘 89 件沿用。最終完整覆核重新轉錄 13 句，結果 **75 字面吻合、15 同音／語助詞、3 Jev 可接受、9 flagged**，結束碼 1。三次覆核均各檢查 102/102 句且各呼叫 Jev 一次；三輪合成共 **137 件實際請求、3,894 billable characters**。最後一輪後 speech journal 為空，沒有未確定的付費請求。

| 私有收據（基址 `/workspace/.video-work/curio-s48/review/`） | SHA-256／結果 |
| --- | --- |
| `audio-r6-first/manifest.json`；`check-r6-first.json`、`check-flags-r6-first.json`、`tts-r6-first.log`、`check-r6-first.log` | `7caccac47d761a5a7412db98ce9f68f17faf40b5b84030c485b92aa3cc63199d`；22 flags |
| `audio-r6-redo1/manifest.json`；`check-r6-after-redo1.json`、`check-flags-r6-after-redo1.json`、兩份 redo1 log | `26d3d644856c9a785d8ce817ef44841a19aaaed11d5b4e254de8e658334c4d80`；13 flags |
| `audio-r6-redo2/manifest.json`；`check-r6-after-redo2.json`、`check-flags-r6-after-redo2.json`、兩份 redo2 log | `ef5fa15591b2df6b2ae5d972ed04f734e69db53c3b8a4893ccdbd9bb9e9f8526`；9 flags |
| 最終 `narration.wav` | `234d8e6fd730d4cdc871389ae1cab154a3a3350a65646616dd594e90b13b7b82` |
| 最終 `timeline.json` | `7de15356a439cca60f9432243954b4731faea9157dab0c6872767b87ef24c3ea` |
| 最終 `check-r6-after-redo2.json`；`check-flags-r6-after-redo2.json` | `84eaa8729530864a8760021525019158d7738b80097ab10698724f07275eaca3`；`02bc52e873fe2dce19034f79d630ce1a93a08c8e1982d1f372be7b1ab10eaf85` |

## 實測時間與未過項

最終時間線為 30 fps、102 句、21,516 影格，`speech_hash=0018090769148747`。濃縮開場 `atl001` 到正文首句 `atl009` 為 **1,643 格／54.77 秒**，落在 30–60 秒要求內；正文 `atl009` 到片尾首句 `atl999a` 為 **19,449 格／648.30 秒（10:48.30）**，高於 8 分鐘。含三句片尾的完整旁白為 **21,516 格／717.20 秒（11:57.20）**；`ffprobe` 的單聲道、48 kHz、16-bit WAV 時長同為 717.200 秒。這些是成品旁白的實長，仍不是影片配樂、畫面或片頭片尾成片時長。

最終官方 `check-audio` 仍標以下九句，須保留原始腳本／聽取 WAV 後處理，不能把它們報成通過：

| 句子 | Jev 分數 | 最終轉錄中的關鍵落差 |
| --- | ---: | --- |
| `atl029` | .26 | 「測試室」成「測試時」 |
| `atl040` | .13 | 「先在船上」成「現在船上」 |
| `atl049` | .08 | 「翌日清晨」成「一日清晨」 |
| `atl054` | .36 | 「坎寧」成「卡寧」 |
| `atl059` | .05 | 「船上繼續找」成「纏上繼續扯」 |
| `atl066` | .06 | 「搜索」成「收縮」 |
| `atl090` | .13 | 「剩下那頭」成「繩子那頭」 |
| `atl095` | .06 | 「另引《旁觀者》」成「令旁觀者」 |
| `atl099` | .03 | 「引賽勒斯記下」成「硬塞了十幾下」 |

已用完本次允許的兩輪限縮重唸，因此**音訊關卡 HOLD**。未推送音訊審核卡、未宣稱站台核准，未畫插畫、買媒體、配樂、組片或提交版本。後續須針對這九句做聽感及措辭／發音字典覆核，若改動腳本文字或發音規則，應重凍結對應精確輸入與必要關卡，再繼續製作。
