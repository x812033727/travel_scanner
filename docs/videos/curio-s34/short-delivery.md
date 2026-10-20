# S34 直式短片交接（2026-10-20）

本片 `curio-s34-short-1` 取自已核准的 S34 長片分鏡，六拍講述薛克頓選擇較遠南喬治亞島求援的風向理由。口播與畫面所述依《South!》第九章；來源覆核及 9:16 中央裁切另經獨立覆看。

## 檔案與收據

本機製作目錄：`/workspace/.video-work/shorts/curio-s34-short-1/3a4b53bf4bf00d50-1792475082476/`。

| 項目 | 結果 |
| --- | --- |
| 集數短片稿 `shorts.json` | SHA-256 `13b59fdca9d3bfa1955af354d8c77ef78f4bc761c9219b75c91ee76fae67e954`；`from-episode --check` 通過，六張影格與來源雜湊相符。 |
| 製作稿 `script.json` | SHA-256 `04d7b16631ad880c0907341d85fd07d8f7dd09481ba90e295c7fd438c305fd5c`。 |
| 成片 `upload/final.mp4` | SHA-256 `4b512a95c81efe8e3e554de5b9a4853d0f9fe733da3fa8fdb6680aec57019034`；1080 × 1920、30 fps、31.83 秒。 |
| 畫面覆看 | `midpoint-review-grid.png`；六幕中央裁切均保留主要人物、船與海岸，第 4 幕改用 `covered-boat`，第 6 幕改用 `land-sighted`。 |
| 語音 | `check.json`：8 句核聽，0 句標記；響度 −14.03 LUFS，真峰值 −2.11 dBTP。 |
| 字幕 | `caption-validation.json`：繁中、英文、日文、韓文各 8 段，逐段與 `timeline.json` 時碼相符，零錯誤；四語內容亦經獨立語義覆看。 |
| 後台草稿 | `draft-report-receipt.json`：後台鍵值 `curio-s34-short-1`，`format=shorts`、`shorts_line=cut`、`source_slug=curio-s34`；讀回時 `reviews=[]`、`youtube_video_id=null`。只呼叫可逆的 `client.report`，未送審或發布。API 回覆不提供另個 UUID。 |
| 品管 | `qa.json`：11/13 通過，SHA-256 `4cdb463167717d00cd8cf3db067325b32a3da7bd0f3ec1794750d3a88d3024a2`。精華短片政策、字幕、聲音、版位、史實、畫面首尾等均通過；僅 `metadata`、`links` 因長片尚無真實 YouTube 網址而未過。 |
| 上傳包 | `package.json`：3/4 通過；影片、四語字幕、封面及揭露資訊齊全，僅說明欄缺長片真實網址。這是未完成的檢查結果，不是可發布的包。 |

## 解鎖後續流程

長片 `curio-s34` 取得真實 YouTube 影片 ID 後，在站台記錄該 ID，讓短片工具從來源影片記錄生成真實連結。接著於本製作目錄重跑 `qa` 和 `package`，確認兩者全通過並核對成片雜湊仍為上表值，再依 Shorts 流程送交正式成片與發布審核。不可先填假 ID 或假網址，也不可把本次後台草稿當成已核准發布。
