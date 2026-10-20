# X11 FedEx｜v4 作者修訂與來源差異

**作者交審紀錄，不是來源或盲讀 PASS。** v4 鎖定主片 `b2226de5962c60ffa90ee177011a9203deb340d3ebbe2355d9be8c79d512d5b0`、兩支 Shorts `7413df056023ae9dfc38f57fa34526c26b0e4d3e4206d911c92a7120db99ba45`（SHA-256）。舊版 [來源審查](reviews/source-audit-v3-independent.md)、[盲讀 A](reviews/blind-a-v3-independent.md)、[盲讀 B](reviews/blind-b-v3-independent.md) 只適用 v3；兩位盲讀都判 FAIL，不能當 v4 結果。

## 針對兩份盲讀的修訂

| 範圍 | v4 改法 | 待新讀者確認 |
| --- | --- | --- |
| `x110212`、`x110308`–`x110317` | 去掉「先看／再來／最後」的目錄語氣；同一件概念包裹從站內出口牽到取配車，再牽到城際幹線。原 `x110311` 無法證實的「哪一道分流」及 `x110317` 無答案的三段先後問題改為來源可答的設備、路線、幹線連鎖。 | 問題與 payoff 是否真的相扣，沒有改成另一份三項清單。 |
| `x110320`–`x110326`、`x110501`、`x110601` | 加拿大轉換與用工身分問題各在相鄰句回收；第 5 章第一句直接給美加地點範圍，第 6 章第一句直接答加拿大完成。 | 章首是否接住上一章的疑問，沒有先念標籤。 |
| `x110502`–`x110507`、`x110607` | 290 地點只口播一次；其後只解釋統計地域與單位。第 6 章移除對成本／時程風險的再口播。 | 是否通過 no_recap，同時仍讓觀眾分清美國與美加口徑。 |
| `x110609`–`x110619` | 原七句 Freight 股權支線移到影片說明欄；改由 2026 年報記載的現有地面設施流程、導入中的分揀變動及服務商路線資料，接續同一件概念包裹到收件門口。 | 這段是否推進「公司合了但實體網仍需逐地做」的主問題，沒有成為場站科技清單。 |
| 章名、`x11-b02-s15`、兩支 Shorts | 第 4／5／6 章名不再先寫結論；十萬輛車的鏡頭換成車模型；Short 1 以美國 50 多處與未完成收束，Short 2 給 FY2025 加拿大／美國和 FY2026 美國的獨立時間線。 | 畫面不先爆雷，鏡頭語義和口播一致；Shorts 實測時長仍待 TTS。 |

## 新增／改時點的一手來源覆核入口

- [FedEx FY2025 10-K，2025-07-21 申報](https://www.sec.gov/Archives/edgar/data/1048911/000104891125000011/fdx-20250531.htm)，`Item 1 > Federal Express Segment > Operations`：`We have completed implementation of Network 2.0 in Canada and implemented Network 2.0 at approximately 130 locations in the U.S.`；同文件 `Item 7` 把加拿大完成點寫為 FY2025 第四季。請核對 `x110601`–`x110602`、F22／F24，並把美國約 130 與同份文件美加約 290 的不同地域口徑分開。
- [FedEx FY2026 10-K，2026-07-20 申報](https://www.sec.gov/Archives/edgar/data/1048911/000104891126000105/fdx-20260531.htm)，`Item 1 > Express U.S. Domestic > Operations`：`As of May 31, 2026, we have implemented Network 2.0 at approximately 360 locations in the U.S.`；同文件公司**預期**美國於 2027 **曆年底**完成。請核對 `x110603`–`x110604`、F18／F27 與 `x11-b06-s04` 卡片，不能把 360 換算成完成率。
- 同一 [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000104891126000105/fdx-20260531.htm) 的 `Item 1 > Express U.S. Domestic > Operations` 寫 `we utilize both employee couriers and service providers ... using a market-by-market approach`、拖車 GPS 標籤通知控制中心、六面條碼相機與輸送帶、`implementing dynamic scheduling tools`、`introducing capabilities to allow certain packages to bypass station sortation`、以及提供服務商含 `near real-time data` 的路線最佳化工具。請核對 `x110606`–`x110617`、F28／F30／F31 的**現在運作**和**導入中**措辭；不可說所有設施相同，或說這些設備全由 Network 2.0 新裝。
- FY2025 `Item 1A` 已有 `historically operated separately and independently` 及 `There can be no assurance` 的整合風險段落；`x110516`–`x110521` 現在明確放在 FY2025。FY2026 同樣重述此風險，見 F19。風險可能發生，不能寫成已發生的節省或損失。

**規格初查：**六章、127 句，實質正文 2511 個稿面字元（按每分鐘 300 字約 8.37 分鐘；正式 Sulafat 音訊仍須實測），17 組逐句 loop，108 景中的 101 插畫鏡頭／6 原生資料卡／1 片尾卡。Short 1 稿面 214 字，約 42.8–51.4 秒；Short 2 為 188 字，約 37.6–45.1 秒（皆按每分鐘 300–250 字）。US$25 是整片硬上限，尚未乾跑核價或付費製作。
