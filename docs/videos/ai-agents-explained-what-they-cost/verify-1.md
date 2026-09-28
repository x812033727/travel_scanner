# verify-1 — ai-agents-explained-what-they-cost

事實查核（2026-09-28）。撰稿者自查；產線的獨立查核關卡在發布前仍應照 AUTOMATION.md 跑一次。

| # | 說法 | 出處 | 判定 | before → after |
| --- | --- | --- | --- | --- |
| c1 | 一個任務呼叫模型多次、重複處理長歷史 | Agents API：Observability and usage | CHANGED | 投影片引文原為改寫句 → 改成官方原句「An agent may make several model calls while completing a task.」 |
| c2 | 子代理、重試、工具、沙箱都要算 | 同上 | CONFIRMED | — |
| c3 | 五輪示意帳單 | GPT-6 Sol 牌價 2／10 實算 | CHANGED | 補上「假設沒有快取命中」兩句；逐輪重算 0.06、0.115、0.18、0.25、0.34，合計 0.945 |
| c4 | workflow 與 agent 的區分 | Anthropic：Building effective agents | CONFIRMED | — |
| c5 | 工作階段紀錄可查回合、工具呼叫、子代理 | Observability | CONFIRMED | — |
| c6 | 每月支出上限、硬上限擋請求 | OpenAI 說明中心（專案限額） | CONFIRMED（經站內文章） | — |
| c7 | 資料落地只支援美國、不支援 ZDR、自架沙箱也不符 | Agents API 概覽 | CONFIRMED | — |
| c8 | 用量為 best-effort、非最終帳單 | Observability | CONFIRMED | — |

changed_facts：2（都已改正）。

## 會很快過期

- Agents API 仍是公開 beta，文件與計費說明可能調整；GPT-6 Sol 牌價是示意的單價基準。

## 意見與立場

- 站主觀點「套用立場：1、5、6」：先試跑一週記費用、先從唯讀工作開始、設預算上限，都標為建議。表格明說是示意，不是產品實測。
