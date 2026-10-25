# 事實、實作與編輯選擇

確認日期：2026-10-25，查核第 1 輪。範例程式與圖解由本次 AI 協作原創，不是外國影片內容的翻譯。沒有在 Claude 實際執行測試，也沒有把自製程式稱作 Claude Motion。

| ID | 主張／適用畫面 | 證據 | 性質與限制 | 查核 2026-10-25 |
| --- | --- | --- | --- | --- |
| c1 | 兩顆獨立公平六面骰有 36 個等機率有序結果；1+6 與 6+1 分開算 | lab/check_lesson.py 兩層枚舉；verification.json；Python itertools.product 官方頁 https://docs.python.org/3/library/itertools.html#itertools.product（今日可讀，3.15.1 文件：「cartesian product, equivalent to a nested for-loop」；範例 product('ABCD', repeat=2) 同時列出 AB 與 BA） | 獨立且公平的模型假設，不是實際投擲樣本 | CONFIRMED（官方頁＋重新枚舉 6×6=36） |
| c2 | 目標 7 符合 6 種，總和 12 符合 1 種 | lab/verification.json math_checks、check_lesson.py self_test；grid-seven.svg、grid-twelve.svg | 程式枚舉與獨立檢查，沒有隨機抽樣推估 | CONFIRMED（重新枚舉：7 有 (1,6)…(6,1) 共 6 種，機率 6/36=1/6；12 只有 (6,6)） |
| c3 | target_sum 改 6，目標亮格有 5 種 | lab/lesson-sum6.json；verification.json math_checks；demo-sum6.mp4 媒體資訊 | 目標場景及比較會更新；最後固定 sum6 是練習，並非所有畫面都由同一參數控制 | CONFIRMED（重新枚舉：(1,5)(2,4)(3,3)(4,2)(5,1)） |
| c4 | 原創範例可輸出 54 秒、1280×720、24fps 的 H264 無聲 MP4 | lab/verification.json ffprobe 資訊與 hash；render_lesson.py；FFmpeg https://www.ffmpeg.org/ffmpeg.html、ffprobe https://www.ffmpeg.org/ffprobe.html | 實際執行；樣片故意沒有音訊，不宣稱其 SRT 已與語音對齊 | 保留，屬執行紀錄。FFmpeg 三個官方頁（含 https://ffmpeg.org/documentation.html）今日都是 HTTP 503，無法用來佐證。verification.json、render.log 不在查核 payload 裡，發佈前要人工逐字核對終端機輸出。 |
| c5 | Pillow 用於圖形與文字繪製，FFmpeg 合成媒體 | render_lesson.py 使用；Pillow https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html（今日可讀：「provides simple 2D graphics」，另有 text()） | 本次環境 Python 3.12.14、Pillow 12.3.0、FFmpeg 7.1.5；不宣稱是最新版本 | Pillow 用途 CONFIRMED。官方 release notes 顯示最新版為 13.0.0（2026-10-16），12.3.0 是 2026-07-01 發布，範例未在 13.0.0 測過。FFmpeg 用途只依執行紀錄，官方頁 503。 |
| c6 | 不合法目標 13 會清楚報錯結束 | lab/verification.json exit1；lesson-invalid.json；check_lesson.py | 本次範例的檢查行為，不是對所有 AI 生成程式的保證 | 數學部分 CONFIRMED（兩顆骰子總和上限是 12）；exit 1 的執行紀錄不在 payload，待人工核對 |
| c7 | 範例 locale 只接受 zh-TW；字幕為設計時間 | lab/check_lesson.py；narration.json；verification.json limits | 不能只改 locale 就當外語完成；主影片八語獨立製作 | CONFIRMED（與 description、旁白一致） |
| c8 | 要求原始檔、集中資料、先預覽、改一個參數驗收 | 隨片 prompts.txt、lesson-brief.json 與實際範例 | 原創編輯建議；不聲稱任何 AI 一次必然成功 | OUT OF SCOPE（編輯建議） |
| c9 | 選程式動畫處理精確格子和數字 | 本集製作選擇與原創結果 | 不延伸成文字轉影片產品的跑分比較；人物表演不在本範例範圍 | 與站主觀點一致 |
| c10 | 渲染程式有「只產生影格」的選項（run-preview-stills 005752） | 沒有找到證據：render 指令、輸出與 claims 都沒有這個選項 | — | NOT FOUND：旁白改為建議「可以請 AI 加一個只輸出影格的選項」，不再宣稱範例已經有這個選項 |

## 命令的來源

run-check 的命令與摘要取自實際的 summary-check.log。run-render 的命令與輸出取自 render.log 或實際的 summary-render 紀錄，欄位只展示本次結果。終端畫面只使用實際可重做的命令，沒有假造 Claude 對話或產品畫面。

查核備註：兩段輸出的內部數字彼此一致（target_sum=7、highlighted_count=6、--expect-count 6、outcomes=36、probability=1/6），也與重新枚舉的結果相符。log 原檔沒有附在查核 payload。

## 旁白與圖形的區分

原創圖形不是產品截圖。timeline.svg、audio-timeline.svg 標為排程示意；grid 與 distribution 按可重做的數學資料繪製。主影片仍須完成實際旁白、音訊檢查、畫面與字幕檢查，腳本長度不是媒體實測時長。

## 研究引用

近期國外影片的研究只用來支持選題與呈現，沒有複製其腳本或素材。參考表在 brief，原始資料在 research/references.json。點閱數多為第三方公開觀測，不是全站排名或作者即時後台數據，片中沒有引用。
