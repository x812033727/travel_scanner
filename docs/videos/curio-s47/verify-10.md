# S47｜R6 獨立覆核、雙盲與政策關卡

日期：2026-10-20 UTC。這份紀錄只適用下列五檔的精確 SHA-256。改動企劃、資料、口播或畫面提示詞後，相關關卡須重審。

| 檔案 | SHA-256 |
| --- | --- |
| [brief.md](brief.md) | `d4eefcb524fc68217f5b9a122039e07537bb92ec34226f447c85bec2d1295f06` |
| [research.md](research.md) | `493d6bf8e73d9832c05300b2c9643e7e53c1448ac2215c54e2f32f9ad10fa357` |
| [script.md](script.md) | `0dd8a74680d53b3133401b03495454df79564c23a0335dace21c8f13e38d3603` |
| [video.json](video.json) | `3d8e87514a92de3ac42a2c3fadb23d5e1e0a54033be36daf27a9265506e15d45` |
| [claims.md](claims.md) | `9675fb565211d4d2cc80a038aa18ea29db62a396bcf8cb0a7d6d214b77a090ae` |

[另一人的 R6 來源及書面畫面差分](review/r6-source-independent.md)為 **PASS**。兩位此前未看過 S47 R6 的獨立讀者讀同一 `script.md` 和 `video.json`；協調者轉交的完整十三題判斷分別保存為 [A](review/r6-blind-a.md) 和 [B](review/r6-blind-b.md)。A **12/13**，B **13/13**。

| 官方敘事題 | A | B | 合併 |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | Yes | Yes | Yes |
| `one_line` | Yes | Yes | Yes |
| `no_toc` | Yes | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | Yes | Yes | Yes |
| `no_recap` | **No** | Yes | **Yes，分歧** |
| `chapters_are_events` | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | Yes | Yes | Yes |

正式規則 [`mergePanelVerdicts`](../../../tools/video/core/narrative.mjs) 是某題至少一位讀者有引文答 Yes 則合併 Yes；必答題只有全員 No 才 FAIL。B 以 `wr050/067/093–094` 的新比較和明確回呼支持 `no_recap` Yes。因此 **R6 合併敘事 PASS**，不是全員一致。A 在 `wr027→028` 看見相鄰「兩成」重述，並提醒 `wr999a` 片尾觀眾問句略突兀；保留這兩則工藝備註，不改寫 A 的判斷，也不為此改動已過關版本。

## Jev 政策

在五檔仍為上列 SHA 時，以 `policyRequest({ doc, brief })` 生成**完整當版口播**與 `brief.md` 的站主觀點，向站台 `/api/video/automation/judge/policy` 送出**一次**請求；沒有裁短劇本另送或重試。請求 SHA-256 為 `a5894a31a3b9f2bc6617cb8fd60db97de81567559db1fd0f1f2ca7d38364a65b`，口播 2936 字元、觀點 103 字元。2026-10-20 15:01:18 UTC 開始，HTTP 200，回覆 `passed: true`。原站台判語：**「Jev：符合立場 0.77、有示範 0.63、建議 0.01、業配 0.15，通過」**。此為政策 PASS；它不等於來源審查、網站劇本批准或聲畫成片批准。請求與回覆留於私有工作檔 `/tmp/s47-r6-policy-request.json`、`/tmp/s47-r6-policy-answer.json`，公開紀錄不含權杖。

## 本地建議與待辦

在來源、書面畫面、合併敘事及 Jev 皆 PASS 後，本地推薦**採企劃 A**，並以本頁精確 `script.md` SHA 申請站台劇本核准。這是可供站主委派核准的具體版本，**尚非網站 `hand_pushed` 的大綱或劇本核准**。站台兩關仍待提交與確認；TTS、原生圖、配樂、成片、Short、私人上傳與可點的片尾推薦／訂閱連結均未做。估時只是 [R6 靜態計算](verify-9.md)，不是聲音或影片實測。
