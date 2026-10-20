# FedEx X11 v5｜獨立來源差異審查

**判定：HOLD，一處地理口徑須明說後重綁雜湊。** v5 新增的 F32–F34 與其他改寫的日期、設施數、計畫／成果界線，均能在 SEC 原件找到依據；但 `x110612`–`x110613` 在加拿大與美國進度並列之後，沒有說清 FY2026「雇員與服務商按市場並用」所指的是**美國地面業務**。請把「美國地面業務」放進 `x110612`（連同 `say` 與衍生稿重編），使 `x110613` 的「全國」明確指美國。改稿會產生新 SHA-256，這份收據不能沿用為新版 PASS。另請在 `x11-b06-s12` 的圖像審查時，避免同框的兩種司機被看成同一市場的實際配置；原件只說按市場安排。

- 本次鎖定主片 `video.json` SHA-256：`3d2a7d1d422105802fd1d755fa8f90f1ca5667057f76aa133d90db0f5efba0d8`。
- 本次鎖定兩支 `shorts.json` SHA-256：`7d352677b785667866b6ef09e7c4f4934d6659fb966f334c8d98c4ac063dcaa6`。
- 差異基線是 [v4 獨立來源收據](source-audit-v4-independent.md)所綁的主片 `b2226de5962c60ffa90ee177011a9203deb340d3ebbe2355d9be8c79d512d5b0` 與 Shorts `7413df056023ae9dfc38f57fa34526c26b0e4d3e4206d911c92a7120db99ba45`。本次逐一比對 v4→v5 的旁白、畫面提示、資料卡、說明欄與兩支 Shorts，並直接檢索下列五份原始申報 HTML；作者的 [F 矩陣](../source-matrix.md)與 [修訂說明](../revision-v5.md)只用來定位待查句子，不作獨立證據。

| 原件 | 本地 HTML SHA-256 | 已核主張 |
| --- | --- | --- |
| [FY2022 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017022012762/fdx-20220531.htm) | `27ea3122e13dc3adb37c379f8b055ba850125ed636d1063c5b83a45d8314cfcc` | Express／Ground／Services 的舊分工與服務承諾。 |
| [FY2023 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017023033201/fdx-20230531.htm) | `630ceceb23295ffae3ba52509394758a378d8f8f934899111ae66244c6286eed` | one FedEx 宣布、組織改造預期、Network 2.0 多年期及三段工程。 |
| [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017024083577/fdx-20240531.htm) | `8f21468ed36509a9ba715479ee766fbf0b98615dd0cd436be1eab4309a9e1141` | 2024-04 加拿大分階段開始、2024-06-01 法律合併、美國超過 50 處、空運／國際與地面安排的未來方向。 |
| [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000104891125000011/fdx-20250531.htm) | `f65d13a0b23d5687a5fcd7681eae63f60f538ef0bc254c654c63365a1958cb35` | 美加約 290 實施地點、美國約 130 地點、加拿大完成、兩組舊網設施存量及整合風險。 |
| [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000104891126000105/fdx-20260531.htm) | `b24489462a93674730fd19432953fba9c9bc544a1bbc2b7e50a45fb1f360fff2` | 持續進行的三段網路工程、美國約 360 地點、美國 2027 曆年底預期及美國地面業務的用工措辭。 |

五份檔案的內嵌 XBRL 均標為 FedEx Corporation／CIK `0001048911`、`10-K`、對應 FY 與 5 月 31 日期末；片中、Shorts 和修訂說明的 SEC 連結均是同一 CIK、對應檔名與原件的 Archives 路徑。現行雲端代理的允許網域沒有 `www.sec.gov`，所以本次未重做即時 HTTP GET 或聲稱驗證了此刻的網站狀態；本地原件的雜湊與此前下載紀錄相同。

| v5 句子／畫面 | 原件核對與界線 |
| --- | --- |
| `x110107`、`x110109`、`x110227`、`x110301`，主片標題／說明欄 | FY2023 Item 1 只說當時宣布把 Express、Ground、Services 等帶入 Federal Express；FY2024 Item 1 才報告 2024-06-01 合併，FY2025 Item 1 說舊網地面營運仍在 Network 2.0 下整合。新版問「**合併後**為何仍逐地整合」並由下一章立即答 one FedEx，沒有再假稱這幾份申報能證明歷史上「為何等到 2024 才合併」。**PASS。** |
| `x110318`–`x110325`（舊 `x110326` 刪除）、`x110401`、`x110404` | FY2023 Item 1 原文 `The organizational redesign will be implemented in phases with full implementation expected in June 2024`；接著另稱 Network 2.0 是 `the multi-year effort`。`x110321` 保留「當時預計」，指組織改造而非實體網完成；`x110319` 也拿掉原「下一批」這種來源未給的先後排序。FY2024 Item 1 另證實加拿大於 2024-04 開始分階段轉換、Ground／Services 於 **2024-06-01** 併入。這個六月日期在 FY2024 的 5 月 31 日期末之後，不能混為該財年內完成的路網工程。**PASS。** |
| `x110415`–`x110420` | FY2024 Item 1 用 `will leverage ... enabling a distinct focus on air and international volume while facilitating a more holistic approach to how we move packages on the ground`；新版的「希望／要／想達到」忠於未來營運方向，`x110418` 也排除每條路線已完成驗收的解讀。限時與按日承諾可回溯 FY2022 Item 1；`x110420` 是概念包裹的編輯性轉場，不是實測的調線順序。**PASS。** |
| `x110508`–`x110514` | FY2025 Item 1 原文稱截至 **2025-05-31**，Federal Express 有約 **720 處 legacy Ground** 與 **530 處 legacy Express** 設施支撐美加地面業務，且 `these operations are being consolidated`。同一申報的約 **290** 是美加已實施最佳化的**地點**，不是設施總數或完成分母。新版只說舊網來源的**營運**逐步整合，並禁止把 720／530 和 290 相除；不能由原件推出每處舊設施仍各自獨立。**PASS。** |
| `x110517`–`x110519` | FY2025 Item 1A 說舊兩網 `historically operated separately and independently`，完整整合可能涉及既有流程、IT、人員、服務商與法律合約風險。新版把「可能受影響」留在風險語氣，未說損失已發生。**PASS。** |
| `x110606`–`x110611`、`x110614`–`x110618` | FY2026 Item 1 寫 `In 2026, we continued our network transformation`，並用現在進行的 `modernizing and consolidating ... reducing ... optimizing` 描述分揀、取配、幹線。FY2023 Item 1 的三項是當時計畫；新版說它們至 FY2026 仍在推進，沒有把美國約 360 個實施地點當全美完成率。加拿大已完成 Network 2.0；美國 **2027 曆年底**仍只是公司的預期。`x110616` 是這些日期與進度的有限總結，`x110617`–`x110618` 是提問和訂閱邀請，沒有額外歷史事實。**PASS。** |
| `x110612`–`x110613`、`x11-b06-s12` | FY2026 Item 1 的 `we utilize both employee couriers and service providers ... using a market-by-market approach` 位於 **Express U.S. Domestic** 的地面業務段落；FY2025 Item 1 也明說 `in U.S. surface operations`。新版在加拿大／美國比較後省去美國限定，讓「全國」沒有明確指涉。**HOLD：**在 `x110612` 補「美國地面業務」，並讓同框司機畫面維持跨市場的示意性，不暗示原件證明某一市場兩種司機同站作業。 |

**Short 1：**8 句均逐字重用主片；v5 把加拿大過渡句換成 `x110303` 的 Network 2.0 名稱，畫面標題也寫明該計畫。`x110404` 自帶 **2024 年**，因此單獨觀看不會把六月一日讀成 2023 年。FY2024 申報只稱美國 `more than 50 locations` 已實施，Short 沒換算成完成百分比。來源層面 **PASS**。

**Short 2：**8 句均逐字重用主片；FY2025 約 290 是美加地點、約 130 是美國地點且加拿大已完成；FY2026 約 360 是美國截至 2026-05-31 的地點數，2027 **曆年底**是預期。沒有相除、相加或把預期當完成。來源層面 **PASS**；「為何還沒全改完？」這個標題是否由進度口播充分回答，交由同版敘事盲讀，不以來源收據代判。

六張原生資料卡保留了年別、單位、地理範圍及預期標籤；v5 沒有把刪掉的拖車 GPS、掃碼、排班或路線工具說成 Network 2.0 的已完成成果。這份收據只核來源與口徑，不驗收故事效果、語音時長、插畫成片或上架。
