# 第一輪獨立查核：AI 代理跟聊天機器人差在哪

查核日：2026-09-27。查核者未撰寫本片。已讀完整 `video.json` 的 142 句旁白、全部字卡、標題、縮圖及說明欄，並重新開啟下列官方頁（HTTP 200）。同一事實在多句重複時合併一列；純建議、問題句和自製示意列為編輯內容。

| # | 可查主張與位置 | 官方來源／狀態 | 判定與修正 |
| --- | --- | --- | --- |
| 1 | `three-modes`、`ag008`–`ag010`、`ag048`–`ag050`、`ag103`–`ag106`：預設流程與模型依工具回饋選下一步的架構差異 | [Anthropic Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，200，〈What are agents?〉 | CONFIRMED。這是 Anthropic 的工程分類，片中也說聊天介面本身無法分類。無改動。 |
| 2 | `fixed-example`、`ag079`–`ag082`、`ag049`：固定流程適合已知規則的重複任務 | 同上，200，〈When (and when not) to use agents〉 | CONFIRMED 作為工程建議。無改動。 |
| 3 | `no-tool-case`、`tool-boundary`、`ag052`–`ag055`、`ag111`–`ag114`：能否讀即時公告取決於工具；一句文字不等於預約或付款 | 同上，200，〈The augmented LLM〉；實際工具權限屬示範設定 | CONFIRMED 為明確標出的能力邊界，未聲稱任何特定產品能力。無改動。 |
| 4 | `first-rule`、`next-check`、`ag024`–`ag030`、`ag091`–`ag094`：臺博館本館平常週一休館，假日可能例外 | [臺博館開放時間](https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444)，200，〈開放時間〉 | CONFIRMED。字卡的「每週一、除夕及春節初一休館」與原文相同。無改動。 |
| 5 | `task-spec`、`exception`、`exception-context`、`specific-date`、`ag018`、`ag032`–`ag039`、`ag123`–`ag126`：2026-09-28（週一）教師節開館，僅此指定日的例外 | [臺博館 2026 節日公告](https://www.ntm.gov.tw/en/News_Content.aspx?n=5713&s=251424)，200，表格 September 28 行 | CONFIRMED。英文短摘錄和中文翻譯一致；片中沒有推廣成所有週一。無改動。 |
| 6 | `route`、`source-trace`、`ag040`–`ag043`、`ag096`：本館位於二二八和平公園內，能作相鄰散步草案 | [本館交通資訊](https://www.ntm.gov.tw/cp.aspx?n=5445)，200，地址及頁尾；[本館開放時間](https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444)，200，頁尾地址 | CHANGED 來源連結：原 `n=5459` 指向**南門館**交通頁，已將 `video.json.sources` 和 `claims.md` 改為本館 `n=5445`。畫面及旁白未聲稱步行分鐘數。撰稿者仍須同步改 `brief.md`、`demo-log.md`。 |
| 7 | `tool-trace`、`ag119`–`ag122`：製作時先看一般開放時間，再看節日公告 | `demo-log.md` 的製作紀錄及上述兩個官方頁，均 200 | CONFIRMED 頁面內容與可重做的查詢順序；**無產品螢幕錄影或不可改寫的工具日誌**，畫面以自行排版的查詢表重建。字幕與口播不可稱為商用 AI 的錄影。 |
| 8 | `change-decision`、`ag036`–`ag039`、`three-evidence-levels`：指定日的資訊把草案從排除改成保留博物館 | 上述一般頁、節日公告，均 200 | CONFIRMED 為依兩個頁面做出的示範推論，字卡有「草案」界線。無改動。 |
| 9 | `not-done`、`ag044`–`ag047`、`ag095`–`ag102`：沒有實測步行、查天氣、訂票或付款 | 影片的任務範圍和 `demo-log.md`，非第三方可證的外部事件 | OUT OF SCOPE；屬製作流程聲明。現有字卡清楚列為待查，沒有杜撰分鐘數或訂單。 |
| 10 | `pretty-answer`、`example-prompt`、`chat-can-use-tools` 的對話泡泡 | 自製教學示意 | OUT OF SCOPE；`ag006` 說明不是任何產品錄影。無改動。 |
| 11 | `privacy-boundary`、`ag087`–`ag090`：示範輸入沒有姓名、電話、訂單或登入 | `video.json` 和 `demo-log.md` | CONFIRMED 對交付檔案的檢查；僅公開日期、地點。 |
| 12 | `failure-state`、`outside-text`、`approval-point`、`ag060`–`ag063`、`ag107`–`ag110`、`ag135`–`ag142`：失敗時標缺口、外部文字不擴權、付款前人工核准 | [Anthropic Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，200；`brief.md` | OUT OF SCOPE 為編輯建議，沒有表述成所有產品已具備的保證。符合 brief 提案。 |
| 13 | `youtube.title`、`thumbnail`、`youtube.description`：一個行程任務顯示回答與完成之別 | `video.json`、`demo-log.md` 與上列來源 | CONFIRMED 承諾與示範相符；沒有「已訂票」或產品實錄宣稱。 |
| 14 | `article`、`ag072`–`ag074`：說明欄第一行有站內來源文章 | `source_guide=ai-agents-explained` 與上架包產生規則 | NOT YET VERIFIED：須在 `package` 後打開產出的說明欄，檢查實際 URL 與文章內容；目前不阻止文字查核。 |

結果：13 組已確認或判定為編輯內容，1 組來源連結已修，0 組事實被官方來源推翻；1 組上架包連結待產出後驗證。唯一事實依賴特定日期：2026-09-28 開館公告。影片發布後只可稱為當時的示範，不能當成未來出遊建議；出發前須重查。

聽眾檢查：旁白沒有超過 40 字的句子、拉丁字詞、括號或網址；`say` 無需更改。來源引用的中英對照已核。縮圖及 `brief.md` 的站主觀點仍標「提案」，須在送大綱審核前確認。未查證「固定流程一定更穩」的量化比較，因片中只說「可能」。改動的是一個連結，**無需第二輪事實查核**；產線的音訊、成片與上架包檢查尚未完成。
