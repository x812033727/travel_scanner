# X03 Netflix｜本機概念試片

本包已交付**未核准的本機概念試片**，用來審看故事、音畫與編排。正式頻道片頭／片尾、逐鏡人工核准、人工聽審、整集供應商費用與 YouTube Studio 可點片尾元素仍須另外完成；本機畫面中的影片框線不能點擊，也不能把參考頻道當成上架目的地。

## 實測結構

| 區段 | 實測長度 | 說明 |
| --- | --- | --- |
| 濃縮開場 | 1,501 影格／50.03 秒 | 第一章，直接進入信箱、DVD 與電腦的問題。 |
| 概念片頭 | 150 影格／5 秒 | 放在開場之後，畫面明標「本機概念試看片」。 |
| 其餘口播正文 | 501.33 秒 | 六章主線與結語，超過八分鐘。 |
| 概念片尾 | 630 影格／21 秒 | 預留兩個影片元素與一個訂閱元素的位置；正式連結須在 Studio 設定。 |
| 全片 | 17,321 影格／577.367 秒（9:37.37） | 1920×1080、30 fps；全檔解碼及連續影格時間戳檢查通過。 |

現行逐句稿 [video.json](video.json) SHA-256 為 `08c931bb000f373fbf5778d02b0703ef1a8b5144c665bfa30afda7c44ed3e5ac`，時間軸 SHA-256 為 `e69b87e5e617e51025a26652d47c4412b324dba754f1dfb7a5cd7b39951e1ef8`。80 句旁白有逐句機械音訊證據，必要的人耳驗聽尚待完成。65 鏡插畫原始候選圖與模型評審保留；[人工選圖收據](reviews/manual-keyframe-selections-a0cbc1ff06c9.json)記錄 49 鏡概念圖替換，均仍標 `needs_review`，並由[視覺檢查](reviews/visual-qc.md)與[史實畫面檢查](reviews/factual-visual-qc.md)交叉審看。12 張原生數字卡和一張口播結語卡已繪製，配樂為 557 秒單曲。

## 目前進度與交付檔

65/65 鏡素材、配樂、概念安全換圖與本機試片均已完成；[整檔技術 QA](reviews/local-preview-qa.md)為 **PASS**。可播放交付檔在 `/workspace/brand-story-preview/netflix-x03/`，原始媒體工作區在 `/workspace/.brand-video-workdir/story-everyday-netflix-x03`。大體積 MP4 不提交到 Git；技術 PASS 仍非正式影片核准。

| 檔案 | 狀態 | SHA-256 |
| --- | --- | --- |
| `preview-review-needed.mp4` | 129 MiB；整檔 QA PASS，49 鏡待審 | `28237f52f5deacd7bbe1ea2c90cf2616cc48d1e57cb296c65c407e587b8cd728` |
| `preview-review-needed.zh-TW.srt` | 92 句可關閉的繁中 CC；逐字 QA PASS | `75ab71893bed30c64cd6dfcdcde07f51db149adaea531d9da6a0e0973aeb4ebc` |
| `preview-review-needed.zh-TW.vtt` | 92 句可關閉的繁中 CC；逐字 QA PASS | `64a74a66524516cbee7ea77508b74001c2ff2a818057c2a2558b100ec871cf49` |
| `preview-review-needed.json` | `approved:false`、`official_branding:false`；輸出與來源 SHA 驗證通過 | `fa4acf0d5e1b5c4a94759eb22c4c91cde35dc1104ae4280fb2fae8f863eac7d4` |
| `thumbnail.jpg` | 最終換圖後重繪，雜湊驗證通過 | `11d30e06d16e6d02766295677e31c07b6be72dd583085f99f836c875b4eb9455` |

已用[本機 QA 檢查器](reviews/local-preview-qa-check.mjs)產生逐項[機器可讀結果](reviews/local-preview-qa-result.json)與[QA 紀錄](reviews/local-preview-qa.md)。驗證範圍包括目前劇本與歷次審查收據鏈、原始生成圖與手選圖雜湊、字卡、配樂、媒體台帳、MP4 完整解碼及連續影格時間戳、解析度、影格率、響度／真峰值、SRT/VTT 字幕逐句對應、片頭片尾時長與旁檔狀態。技術檢查通過只代表檔案符合這些條件，不能取代人耳、人眼或站主對正式版的核准。

## 上架銜接

正式版以站主選定的 5 秒品牌片頭與 21 秒品牌片尾取代概念動畫，再重跑字幕、章節與全檔 QA。若新素材長度不同，必須重新計算所有時間碼。私人上傳後，在 YouTube Studio 最後 17 秒設定兩個影片元素（「最符合觀眾喜好」、「最新上傳」）與訂閱元素，逐一實際點擊測試，才填入真實影片 ID 和公開連結。[上架交接](publishing-handoff.md)保留四份 SEC 原件、標題、說明與史實口徑。

截至素材合併的媒體台帳可見 US$1.7135；這只含可見圖片、評審與配樂工單。語音、轉錄、其他複查、稅費等沒有完整報價，**尚不能確認整集 US$25 硬上限的實際總額**。詳見[製作估算與成本控制](production-quote.md)。
