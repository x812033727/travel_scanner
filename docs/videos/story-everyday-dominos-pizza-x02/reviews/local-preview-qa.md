# X02 達美樂｜本機概念試片影音 QA

2026-10-20。檢查對象是 `review/local-preview/preview-review-needed.mp4`、同名繁中 SRT／VTT 與 JSON 側錄，位於 `/workspace/.brand-video-workdir/story-everyday-dominos-pizza-x02/`。本次對修正版 `--allow-review-needed --force` 原子發布後的檔案執行獨立、唯讀檢查；詳細機器結果見 [QA 結果 JSON](local-preview-qa-result.json)，可重跑程式見 [QA checker](local-preview-qa-check.mjs)。

**技術 QA：PASS。編輯、品牌與上架：HOLD。** 這是明標「未核准」的本機概念試片，並非正式可上架成片。

| 檢查 | 結果與證據 |
| --- | --- |
| 全檔完整性 | MP4 **141,736,428 bytes**，SHA-256 `ba430870cad347ccdc6275d21dc6a9cf2c52c8ae433f81b4ffd5a3eec1f4452d`；FFmpeg 全檔影音解碼沒有錯誤。獨立 ffprobe 數出 **16,363 個封包／16,363 個解碼影格**，首格 PTS 為 0，相鄰 PTS 均差 512（30 fps），無跳格或重複時間戳。 |
| 規格與長度 | H.264 High、1920×1080、30 fps、yuv420p limited-range BT.709；AAC 48 kHz 雙聲道。正文 15,583 格，加片頭 150 格、片尾 630 格，總長 **545.433 秒（9:05.43）**。AAC 軌長 545.500 秒，比影像長 0.067 秒，在檢查所設 0.11 秒容差內。 |
| 音量 | 全片 EBU R128 整合音量 **−14.0 LUFS**，真峰值 **−1.0 dBTP**；符合 −14±1 LUFS、≤−0.5 dBTP 的技術門檻。此量測不能替代三句待確認旁白的人耳檢查。 |
| 字幕 | 繁中 **95 cues**；SRT `a954357982666723ea005866071cc264ccbb2816d6fc20e80e8b084060816b00`、VTT `35a65128bea1ee757958894dba19e706417c1a6e5baa3f8c09932b92b3b0a012`。兩檔與現行劇本及實測時間軸重新產生的內容**逐位元組一致**，0 項時間／閱讀速率警告。首章末句 45.267–49.907 秒；第二章首句 55.533–61.923 秒；片頭 50.533–55.533 秒內沒有字幕，片尾 524.433 秒起也沒有字幕。 |
| 側錄與來源 | 側錄 SHA-256 `8c054bf599a8aefecdbd05e574d4a6d27c740d36fa50b98065c9d5c756162567`，明載 `approved: false`。劇本、時間軸、選圖 manifest、字卡 manifest、配樂 manifest、**120 個字卡檔**及三個輸出檔的雜湊均與實物相符；63 張選圖檔也逐一核對 SHA。14 個 `needs_review` 鏡頭的 ID、選圖檔、雜湊及問題紀錄保留且一致。 |
| 可見媒體費用 | 台帳 245 筆，重算與儲存總額一致，無未結預留或重複 job ID：**US$1.7135**（123 張圖、121 次評審、1 首配樂）。這只涵蓋台帳內媒體工作；未列出的 TTS、轉錄、稅費或供應商費用不在此結論內，不能由此宣稱全片 US$25 上限已完整審計。 |

抽查實際 MP4 的 0、1515、1516、1591、1665、1666、6561、10116、11694、15732、15733、15883、16362 格。第 1516 格開始 5 秒概念片頭，第 1666 格回到第二章正文；第 15733 格開始 21 秒概念片尾，片尾中段有兩個影片框和訂閱位，但它們只是畫面版位。抽格可見 `x02-b04-s02` 腳邊紙盒有假字、`x02-b05-s04` 日曆有假標頭；`x02-b05-s12` 已是空白圖板，未見先前候選圖的虛構急跌曲線。這些抽查與 [63 鏡逐張視覺 QA](visual-qc.md)一致，不能消除 14 個鏡頭的待審旗標。

正式成片仍須處理 14 張 `needs_review` 插圖，並在人耳確認 `x020103`（00:17.17）、`x020406`（04:02.80）、`x020504`（05:37.20）三句旁白，見[音訊紀錄](audio-revision.md)。還須替換站主選定的正式片頭／片尾品牌素材、重驗最終檔，私人上傳後在 YouTube Studio 實際配置並點測兩個影片連結與訂閱元素；MP4 內的框線本身不可點。這些是編輯與發布條件，不是本次技術 QA 的通過項。

從 repo 根目錄重跑（唯讀；路徑依執行環境調整）：

```sh
node docs/videos/story-everyday-dominos-pizza-x02/reviews/local-preview-qa-check.mjs --workdir /workspace/.brand-video-workdir > /tmp/dominos-x02-local-preview-qa-result.json
```

checker 會重新計算來源與輸出 SHA、字幕預期位元組、側錄綁定、全片解碼與逐格 PTS、完整音量。重跑產物應與本頁的雜湊及 [已封存結果](local-preview-qa-result.json) 相符；一旦劇本或媒體改動，須重新產出概念片並再次檢查。
