# 事實與示範查核表

2026-09-27 撰稿者初查。這是交給**另一位**查核者的索引，不能當成獨立審核已通過。請逐句檢查 `video.json` 及所有字卡，尤其是示範日期、館方原文和資料權限的邊界。

| 編號 | 影片中的主張與位置 | 原始來源 | 初查結果／限制 |
| --- | --- | --- | --- |
| A1 | `ag008`–`ag011`, `ag050`, `ag103`–`ag106`：聊天、固定流程與代理的工程區分；聊天介面也可能含工具 | [Anthropic Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)；站內 `ai-agents-explained` | 官方把預設程式路徑的 workflows 與模型動態決定流程及工具的 agents 區分。片中是教學簡化，不能當所有產品的正式分類。 |
| A2 | `ag052`–`ag055`, `ag111`–`ag114`：模型是否能查資料取決於工具與授權，文字聲稱完成不等於外部動作 | 同上；站內 `ai-agents-explained` | 屬系統設計概念，個別產品能力不可由本片推定。 |
| A3 | `ag024`–`ag027`, `ag091`–`ag094`：臺博館平常週一休館，國定假日可能例外 | [臺博館開放時間與票價](https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444) | 官網明列週二至週日 9:30–17:00、每週一休館，也列假日照常開館。錄製及公開前重查。 |
| A4 | `ag032`–`ag039`, `ag091`–`ag094`, `ag123`–`ag126`：2026-09-28 教師節週一特別開館 | [臺博館 2026 年開閉館公告](https://www.ntm.gov.tw/en/News_Content.aspx?n=5713&s=251424) | 官方表格列 `September 28 (Mon) | Teacher's Day | Open`。這是指定日期的例外，不是每個週一開館。錄製及公開前重查。 |
| A5 | `ag040`–`ag043`, `ag096`：臺博館位於二二八和平公園內，可作散步草案 | [臺博館本館交通資訊](https://www.ntm.gov.tw/cp.aspx?Create=1&n=5459) | 館方地址明列「二二八和平公園內」。沒有查台北車站接駁時間、雨天備案、無障礙動線，也沒有到現場。臺北市觀光局相關頁回傳 403，不作已讀來源。 |
| A6 | `ag119`–`ag122`：製作時先查一般頁、後查年度公告，決策據此改變 | 本目錄 `demo-log.md`，對應上述官方頁 | 真實製作紀錄；不可呈現為特定商用 AI 產品的介面或單獨模型對話。 |
| A7 | `ag060`–`ag063`, `ag107`–`ag110`：工具失敗應說明未完成，外部內容不應擴張權限 | 站內 `ai-agents-explained`；[Anthropic Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 編輯性安全建議；旁白沒有承諾任何代理系統必定做到。 |

## 示意與意見

- `pretty-answer`、`example-prompt`、`chat-can-use-tools` 是自製示意卡；未宣稱為真實產品回覆。
- `ag048`–`ag051` 的「固定流程可能更穩」和 `ag135`–`ag142` 的授權策略屬一般設計建議。核對是否符合 `brief.md` 的待確認站主觀點。
- `ag044`–`ag047`、`ag095`–`ag102` 清楚區分已查資料、推論與未查項目。不要把「草案」改寫為已預訂或已現場走過。

## 覆核前待辦

1. 由非撰稿者於查核當日重新開 A1–A5，逐項檢查所有 `lines`、字卡、標題、縮圖及說明欄；寫 `verify-1.md`。
2. 把所有原文摘錄與畫面中的中文翻譯逐字比對，確認只取必要短句。
3. 站主確認 `brief.md` 提出的頻道立場，然後才送大綱關卡；改稿後重新跑 `lint`。
