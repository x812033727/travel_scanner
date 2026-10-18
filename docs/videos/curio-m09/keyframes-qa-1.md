# M09 插畫第一輪人工驗收與定向修圖準備

日期：2026-10-16（UTC）。本收據記錄已完成的本機產圖批次與目視檢查，並非分鏡核准。

## 綁定的產圖快照

- 產圖時 `video.json` SHA-256：`6B63F16674C69547ECA872614ADC988582F836024F571498334E4CE46CBAC5EC`。
- 本機 `keyframes/manifest.json` SHA-256：`676551E9D17494F58CD674B53EDD4DD5281258DC87264044BB9CEEEA6B90937E`。
- 87／87 插畫鏡頭已有選圖；86 張通過圖像評審，`month-meaning` 三次仍未通過。四頁聯絡表均已逐格目視。
- 本輪另放大檢查 16 張選圖：`scan-tease`、`not-simple-wheel`、`visible-clues`、`inside-layer`、`hidden-question`、`scan-recalled`、`layers-visible`、`gear-count`、`inscription-question`、`months-upper`、`calendar-use`、`different-dials`、`numbers-read-year`、`saturn-period`、`numbers-purpose`、`epicyclic-idea`。其餘 71 張只完成聯絡表級檢查，後續仍可逐張放大複核。

## 待修鏡頭

| 鏡頭 | 評審 | 人工目視問題 |
| --- | --- | --- |
| `month-meaning` | 未通過 | 三次生成仍有多餘月相、字樣或手部錯誤；未能清楚表達一次新月至下一次新月。 |
| `not-simple-wheel` | 通過 | 選圖看成單一大輪，無法清楚看出兩枚齒輪嚙合；旁白說單一齒輪不能獨自完成工作。 |
| `inscription-question` | 通過 | 螢幕呈木紋狀，沒有青銅內側刻痕；旁白在問內藏的字。 |
| `months-upper` | 通過 | 兩個普通圓盤不見螺旋月分軌道；旁白說上方指針追蹤月份。 |
| `numbers-read-year` | 通過 | 紙上仍有偽漢字樣記號，會把古希臘機械刻字誤畫成其他文字。 |
| `epicyclic-idea` | 通過 | 兩個木圈分開擺放，未呈現兩種圓周運動疊合。 |
| `node-explain` | 通過 | 兩個環分離，未呈現月球軌道與太陽視路徑的交會。 |

`different-dials` 是一般圓盤而非螺旋，但仍顯示兩個不同盤與指針，足以配合該句旁白，暫不列為必修。其餘畫面依系列規則只因可能誤導的內容矛盾退修；可愛卡通化與無關的小物不構成退修理由。

## 費用與下一步

- 這一輪本機媒體帳本由 US$1.9845 增至 US$2.7100：新增 53 次 MiniMax image-01 圖像呼叫（US$0.1855）及 54 次 Gemini 圖像評審（US$0.5400），合計 **US$0.7255**。這是工具估算，並非供應商最終帳單。
- 加上已結算的繁中旁白與音訊 QA US$0.70，M09 目前估算花費 **US$3.4100／6.00**。共用帳本已由協調者結算；本輪不改帳本。
- 上述七鏡已在 `video.json` 各作一處定向提示詞修訂。新 `video.json` SHA-256：`3A121001740A7FFDBD8F87150E36B18A56D68999901DD40E0885F5432EB67520`。原 manifest 仍對應舊提示詞快照，尚未重產，不能用它申請分鏡審核。
- `lint --slug curio-m09` 為 0 error、2 個既有研究角色／室內場景詞頻 warning；七鏡 `keyframes --dry-run --takes 3` 顯示 MiniMax image-01 ready、提示詞皆未超上限，一輪約 US$0.09、三輪工具四捨五入約 US$0.28。按每次 US$0.0135 計，七鏡最多三次的停手估額是 **US$0.2835**。這次只乾跑，**沒有付費重畫**。
- 待協調者在最新 main 上重新確認工具規則和可用預算，再按七鏡定向產圖；需 87／87 通過評審並完成獨立目視驗收，才送分鏡後台。尚未送審、成片或上傳。
