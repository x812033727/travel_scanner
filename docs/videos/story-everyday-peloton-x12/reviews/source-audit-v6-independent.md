# X12 Peloton｜v6 獨立來源增量查核

**判定：HOLD（v6 凍結稿不可取得整體來源 PASS）。** Commit `7545fae2d5b05f66082d2cb41425714c845fb56c` 新／改的事實、因果、章名及 Short 2 數字卡本身皆有一手依據，但逐來源核對這條故事的時間線時，發現一項足以誤導觀眾的既存時序錯誤。核對日為 2026-10-20。主片 `video.json` SHA-256 為 `e007d6a17a9874f6c6536f56e2390e8e6124c1e8dc6e8987cc26ecb6e5a7b85e`，兩支短片 `shorts.json` SHA-256 為 `93def60bfdb43185b3f97dcb07e2798d608421b932ea19cd1c7b0655a6335ae8`。兩個檔案均與交審雜湊逐位相符。判定前沒有閱讀 Peloton 歷次來源審查或修訂收據。

## 一手原件

直接下載下列 SEC 歸檔 HTML 並計算原件位元組 SHA-256；五份皆與 `source-matrix.md` 所列雜湊相符。以下代碼沿用本集來源矩陣。

| 代碼 | SEC 原件 | 實測 SHA-256 |
| --- | --- | --- |
| A21 | [2021-05-24 公告／8-K Exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1639825/000163982521000174/pton-may24announcement.htm) | `a30d4ed3e6f2340eee67f803c5c510ef42f1c2d61caddcc9966aeee13a742611` |
| K21 | [FY2021 Form 10-K](https://www.sec.gov/Archives/edgar/data/1639825/000163982521000256/pton-20210630.htm) | `a35cb0228c6543b872e4fa27142930105e2373c24fa64d07583449f92860159b` |
| A22 | [2022-07-12 公告／8-K Exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1639825/000163982522000091/ex991pressrelease.htm) | `c3d056d47fb6ffb7124bd36133f7acda5e1c3bb7d1d33e8a5c88f2a5bea54397` |
| K22 | [FY2022 Form 10-K](https://www.sec.gov/Archives/edgar/data/1639825/000163982522000117/pton-20220630.htm) | `b89cb601cadb82c6e2fe193eab3fce0420458a9ffc5758c15d1e368ad8c643b8` |
| K23 | [FY2023 Form 10-K](https://www.sec.gov/Archives/edgar/data/1639825/000163982523000132/pton-20230630.htm) | `1ad92380cc6b6e32ca32161d9105f6704e6d336938f73708d278acf9e81575a1` |

## HOLD：Ohio 的製造任務已於二月轉向

K22 第 44 頁「Properties」明寫：**“In February 2022, as part of the Restructuring Plan, we announced the closing of several assembly and manufacturing plants, including the completion and subsequent sale of the shell facility of Peloton Output Park.”** K22 的「Restructuring Plan」亦重述二月公布的計畫包含完成並隨後出售 Ohio 廠殼。這證明 **Ohio 原定製造用途在二月的公開計畫中已被撤回**；但不證明殼體當時已完成或已出售。A22 的 **2022-07-12** 公告是更廣的退出全部自有製造、擴大 Rexon 合作。K22 九月年報的 `currently are marketing and intend to sell` 是其時出售意向與進度，並非首次宣布 Ohio 的去向。

凍結主片的 `x120422–x120423` 只把二月重整表述為降低固定成本；`x120501` 說七月公司「改口」，`x120509` 接著說 Ohio 原計畫「已不再是製造答案」，`x120513` 更明說「九月提交的年報，**才說出**這座俄亥俄廠接下來的去向」。最後一句的首次揭露含義與 K22 的二月記載直接衝突，前幾句的排列使七月看似 Ohio 首次失去製造任務的原因。Short 2 第七鏡（引用主片 `x12-b05-s02`）「七月公司宣布退出自有製造；**新廠失去原定任務**」也把這兩步緊接為單一轉折。即使這些字句在本次 commit 前已有，這份凍結稿仍不能取得來源 PASS。

**修復邊界：** 主片須在二月段落明確交代「宣布完成 Ohio 廠殼並隨後出售」是**計畫**，再把七月寫成全面退出自有製造與 Rexon **將**主造的後續公告；九月只說年報當時仍在尋買家、意圖出售，不能用「才說出」暗示首次揭露。Short 2 要避免把 Ohio 首次失去原任務歸給七月；可在有限鏡數內先點出二月 Ohio 計畫轉向，再接七月全面自製退出，或移除錯誤的因果暗示。同步核對 `brief.md`、`treatment.md`、`source-matrix.md`、逐句矩陣與生成稿，重編兩個 JSON、計算新 SHA 並獨立重查改句。**不需把二月的出售計畫寫成當時已成交。**

## 增量逐項判定

| 改動 | 原件對照與邊界 | 判定 |
| --- | --- | --- |
| `x120204`：FY2020→FY2021 設備類收入「翻了一倍多」 | K22 同一張三年收入表列 Connected Fitness Products `US$1,462.2m → US$3,149.6m`，約 2.15 倍；K21 的業務敘述也記錄交付增長。採 K22 同表口徑，避開 K21 對 FY2021 印作 `US$3,149.7m` 的 0.1m 差異。後半句是問句，沒有聲稱供應網完全接不住。 | PASS |
| `x120205–x120208`：紙箱／零件／裝配／運輸／長交期／積單 | K21「Manufacturing and Logistics」載有亞洲多家代工、零件由公司或代工廠採購、供應鏈協調；風險段落載有零件短缺、長交期及貨運限制；FY2021 結果段落明寫加急運輸是為緩解 `backlog of demand`，並列運輸與零件成本增加。紙箱移動是概念化的流程畫面，沒有新增訂單或缺料數量，也沒有斷言 Ohio 能解除零件瓶頸。 | PASS |
| `x120416–x120417`：已記毛損與未投產 Ohio 的先後 | K22 的 FY2022 Connected Fitness Products `Gross Profit` 為 **`$(246.3)m`**；A21 只計畫 Ohio 自 **2023** 開始製造 Bike／Bike+／Tread，K22 則說原先打算用該廠製造、其時正對外尋買家。尚未按原計畫投產的未來產能不能倒轉 FY2022 已記錄成本，是時間與會計邊界；文案沒有說新廠永遠不可能改善未來成本。 | PASS |
| `x120605`：在已用連網設備及數位服務上看課程 | K21「Subscriptions／Connected Fitness Subscriptions／Peloton Digital」說連網設備訂閱可透過設備使用課程，Digital 讓會員在自己裝置存取課程；訂閱按月收費。此句沒有把數位訂閱算作硬體銷量。 | PASS |
| `x120607`：月費增加不能當新機訂單；Ohio 原要增加器材產能 | K21 的訂閱服務可在連網設備或 Digital 使用，A21 把 Ohio 目標寫為 Bike／Bike+／Tread 製造，K23 的 FY2023 表則確有訂閱收入增加。月費與新機訂單不能一對一推論，是這些類別的審慎區分，不是 SEC 自述的訂單因果。 | PASS |
| 第六章標題「隔年訂閱收入超過設備收入」 | K23 FY2023 同表列 Subscription `US$1,670.1m`、Connected Fitness Products `US$1,130.2m`。標題限定「收入」，沒有把訂閱毛利或公司獲利帶入。 | PASS |
| Short 2 第二、三鏡：設備／訂閱類收入卡 | K22 FY2021→FY2022 同表分別為設備類 `US$3,149.6m → 2,187.5m`、訂閱類 `US$872.2m → 1,394.7m`；四個新卡面值 `31.5／21.9／8.7／13.9 億美元` 均為正確約數。每行直接標 FY 年度、美元及分類。 | PASS |
| Short 2 第五鏡：毛損卡及旁白 | K22 FY2022 分類表列 Connected Fitness Products 收入 `US$2,187.5m`、收入成本 `US$2,433.8m`、分類毛利 **`$(246.3)m`**。`FY2022 設備類毛損`、`約 2.46 億美元`、`分類毛損 ≠ 公司淨損` 共同保留年度、負值語義與財報分類；改成「扣掉設備類收入成本」符合該表的算法。K22 另列公司的淨損 `US$2,827.7m`，並非這筆分類毛損。 | PASS |

Short 2 的卡面沒有把設備收入跌幅宣稱為七月決策的單一已證實原因；其**收束時序**仍受上方 HOLD 限制。K22 財年於 2022-06-30 結束、A22 於 2022-07-12 宣布退出自有製造及 Rexon **將**主造 Bike／Tread 的日期次序本身正確。

## 對版與範圍

逐一比對 `video.json`、`drafts/narration.md` 和 `line-source-matrix.md`：112 個場景、112 個唯一句 ID、112 列完全一致的旁白及來源代碼；上述改句分別落在 `x12-b02-s04–s08`、`x12-b04-s16–s17`、`x12-b06-s05／s07`。兩支短片各七鏡，引用的主片 scene ID 均存在。主片有 101 景插畫、11 張原生統計卡、15 個 `loops`；與本版 brief、visual plan、quote 所列數量一致。`shorts-script.md` 的改句和 `shorts.json` 一致。這些對版結果與新改句的局部 PASS 不解除上方時間線 HOLD；本次也不是配音、畫面或兩位全新盲讀的驗收。
