# 事實、實作與編輯選擇

本表更新日期：2026-10-26（Asia/Taipei）。這是依目前教材原始檔與實際執行證據更新的主張台帳；第 1 輪的歷史查核保留在 `verify-1.md`，第 2 輪獨立查核保留在 `verify-2.md`，不以本次更新改寫過去的查核或核准紀錄。範例程式與圖解由本次 AI 協作原創，不是外國影片內容的翻譯。沒有在 Claude 實際執行測試，也沒有把自製程式稱作 Claude Motion。

| ID | 主張／適用畫面 | 證據 | 性質與限制 | 目前查核結果 |
| --- | --- | --- | --- | --- |
| c1 | 兩顆獨立公平六面骰有 36 個等機率有序結果；1+6 與 6+1 分開算 | `materials/lab/check_lesson.py` 兩層枚舉；`materials/lab/verification.json`；`verify-2.md`；Python itertools.product 官方頁 https://docs.python.org/3/library/itertools.html#itertools.product（笛卡兒積，等同巢狀迴圈；官方頁的歷史讀取紀錄見 `verify-1.md`） | 獨立且公平的模型假設，不是實際投擲樣本 | CONFIRMED（獨立枚舉 6×6=36；有序結果分開計數） |
| c2 | 目標 7 符合 6 種，總和 12 符合 1 種 | `materials/lab/verification.json` math_checks；`materials/lab/check_lesson.py` self_test；`materials/lab/grid-seven.svg`、`materials/lab/grid-twelve.svg`；`verify-2.md` | 程式枚舉與獨立檢查，沒有隨機抽樣推估 | CONFIRMED（7 有 (1,6)…(6,1) 共 6 種，機率 6/36=1/6；12 只有 (6,6)） |
| c3 | target_sum 改 6，目標亮格有 5 種 | `materials/lab/lesson-sum6.json`；`materials/lab/verification.json` math_checks 與 demo-sum6.mp4 媒體資訊；`materials/lab/frames-only-verification.json`；`verify-2.md` | 目標場景及比較會更新；最後固定 sum6 是練習，並非所有畫面都由同一參數控制 | CONFIRMED（(1,5)(2,4)(3,3)(4,2)(5,1)；本輪使用現有教材原始檔執行預覽，摘要回傳 target_sum=6 highlighted_count=5） |
| c4 | 原創範例可輸出 54 秒、1280×720、24fps 的 H.264 無聲 MP4 | `materials/lab/verification.json` 兩支 MP4 的 ffprobe 資訊、大小與 SHA-256；`materials/lab/render_lesson.py`；`verify-2.md` 的完整獨立轉檔；FFmpeg 官方原始文件 https://github.com/FFmpeg/FFmpeg/blob/master/doc/ffmpeg.texi（本輪讀取 HTTP 200） | 規格來自實際完整轉檔與 ffprobe，不是文件推算；樣片故意沒有音訊，不宣稱其 SRT 已與語音對齊 | CONFIRMED（已保存的完整轉檔及獨立查核均為 1,296 影格、54 秒、1280×720、24fps、無音軌；本輪影格預覽不重算為 MP4 實測） |
| c5 | Pillow 用於圖形與文字繪製，FFmpeg 合成媒體 | `materials/lab/render_lesson.py` 的 ImageDraw 與 ffmpeg 子程序；`materials/lab/verification.json` runtime；`materials/lab/requirements.txt`；`verify-2.md`；Pillow https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html；FFmpeg 官方原始文件同 c4 | 完整範例實測環境為 Linux、Python 3.12.14、Pillow 12.3.0、FFmpeg 7.1.5；跨平台安裝說明不代表各系統都已實機驗證 | CONFIRMED（Pillow 鎖定 `Pillow==12.3.0`，本輪預覽亦實際使用 12.3.0；不主張它或其他工具是最新版本） |
| c6 | 不合法目標 13 會清楚報錯結束 | `materials/lab/verification.json` 負面案例；`materials/lab/lesson-invalid.json`；`materials/lab/check_lesson.py`；`verify-2.md` 另從當前教材實際重跑的紀錄 | 本次範例的檢查行為，不是對所有 AI 生成程式的保證 | CONFIRMED（exit 1，`target_sum must be an integer from 2 to 12`；兩顆骰子總和上限為 12） |
| c7 | 範例 locale 只接受 zh-TW；字幕為設計時間 | `materials/lab/check_lesson.py`；`materials/lab/narration.json`；`materials/lab/verification.json` limits；輸出 timeline 的 timing 欄位 | 不能只改 locale 就當外語完成；主影片八語獨立製作 | CONFIRMED（與 description、旁白一致；本輪輸出的字幕與旁白仍為未對音訊的草稿） |
| c8 | 要求原始檔、集中資料、先預覽、改一個參數驗收 | 隨片 `materials/prompts.txt`、`materials/lesson-brief.json` 與實際範例；`verify-2.md` 的獨立重做 | 原創編輯建議；不聲稱任何 AI 一次必然成功 | 編輯建議；本範例的核心操作另有執行證據 |
| c9 | 選程式動畫處理精確格子和數字 | 本集製作選擇與原創結果 | 不延伸成文字轉影片產品的跑分比較；人物表演不在本範例範圍 | 與站主觀點一致 |
| c10 | 渲染程式有「只產生影格」的選項（run-preview-stills 005752） | `materials/lab/render_lesson.py` 的 `--frames-only` 引數與略過 render 的條件；`materials/lab/install.txt` 現有操作說明；`materials/lab/frames-only-verification.json` 的完整命令、stdout、exit code、時間與來源／輸出雜湊 | 選項略過 MP4 編碼；仍輸出六張 PNG、聯絡表及旁白／SRT／timeline 草稿。摘要中的 54 秒是設計場景時間，沒有產生可量測時長的影片 | CONFIRMED（本輪對 lesson-sum6.json 實際執行 exit 0，六張 1280×720 PNG、零支 MP4；現有旁白使用既有選項，無需改寫） |

## 命令的來源

run-check 與 run-render 的命令及短摘要保存於 `materials/lab/verification.json` 的 `summary_commands`。`verify-2.md` 記錄已逐字對照工作區的原始 summary-check.log、summary-render.log；這些原始 log 並未作為目前 `materials/lab/` 的檔案交付，不把它們列為隨片現有檔案。終端畫面只使用實際可重做的命令，沒有假造 Claude 對話或產品畫面。

兩段輸出的內部數字彼此一致（target_sum=7、highlighted_count=6、--expect-count 6、outcomes=36、probability=1/6），也與獨立枚舉相符。影格預覽的本輪驗收直接執行目前 `materials/lab/` 原始檔；完整命令與逐字 stdout 在 `materials/lab/frames-only-verification.json`，生成檔留在 `/workspace/work/ai-animation-01/ledger-frames-only/`，不將生成媒體加入原始碼。

## 歷史查核的適用範圍

`verify-1.md` 記錄當時原生查核 payload 沒有附入程式與原始執行檔，因此將 c10 判為 NOT FOUND，並要求人工核對 c4、c6。這反映當時收到的證據不完整，不能據此推論教材沒有該選項。`verify-2.md` 已讀取並重做教材，確認現有影格選項與原旁白一致；本輪又從實際教材路徑完成影格預覽驗收，現行 c10 依此確認。歷史文件及其當時統計均保留，不追溯代填通過。

第 1 輪記錄的 ffmpeg.org 三頁 HTTP 503，以及第 2 輪記錄的官方網頁逾時，仍是各輪當時的觀測。本輪已成功讀取 FFmpeg 官方 GitHub 的 `doc/ffmpeg.texi`（HTTP 200），不把舊的連線失敗寫成目前沒有可用官方文件。工具版本只記錄實測與鎖定值，不沿用歷史報告中未由本輪證據支持的「最新版」或發布日期判斷。

## 旁白與圖形的區分

原創圖形不是產品截圖。timeline.svg、audio-timeline.svg 標為排程示意；grid 與 distribution 按可重做的數學資料繪製。主影片的旁白、音訊、畫面與字幕驗收須以各自的實際媒體紀錄判定；本表的 54 秒僅指獨立無聲範例，腳本長度或預覽的設計時間都不是主影片實測時長。

## 研究引用

近期國外影片的研究只用來支持選題與呈現，沒有複製其腳本或素材。參考表在 brief，原始資料在 `research/youtube-20261025.json`。點閱數多為第三方公開觀測，不是全站排名或作者即時後台數據，片中沒有引用。
