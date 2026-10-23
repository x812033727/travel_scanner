# C20 Zippo｜v4 五處來源與配鏡差異獨立覆核

查核日：2026-10-23。審稿者與作者分開；只審作者草稿 [PR #1728](https://github.com/x812033727/travel_scanner/pull/1728) 的 `3b27a5af392acfe88a168850aa57d2f27cb2f84d`，不修改作者稿。先前完整逐句／配鏡覆核見 [PR #1746](https://github.com/x812033727/travel_scanner/pull/1746)：舊稿 64 ID 為 **59 PASS／5 HOLD**。這份收據重開五個 HOLD 的原件與新版配鏡，也查相鄰回呼和表尾計數；其餘 59 ID 不偽稱本輪重新全文閱讀。

## 鎖定版本

以下是 `git show HEAD:<path>` 位元組的 SHA-256，與作者收據逐一相符，不以 Windows 工作樹 CRLF 代替 Git blob：

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `F954A0AB9893D6C7087F9D71C8337CB2826F72ABA9FEA1A45C638E16EBDA8C2E` |
| `script-source-notes.md` | `810A0A6FF6BCE5AD731F88F2B79EA65BA25524EEE2592F2E2E28C40A39F6DC3E` |
| `visual-plan.md` | `C0F50CF7217FB09ACF526138C9A002263CF14F2D7E1938AA8C0D442CF1FB121D` |
| `visual-plan.json` | `4E05E34EE1C37A7689FED33B2C6EC93F7E5662B2DD0205B00B71DD1FF4A88295` |

機械比對：`script.md`、來源註記、分鏡 MD、JSON 均為 **64 個唯一 ID，同序**；JSON 逐句旁白與來源標籤、逐鏡提示詞與 MD 逐字相同。55 個 `image`、9 個 `card`，分鏡表尾已更正為 64／55／9。

## 逐處判定

| ID | 判定 | 原件與旁白／畫面合看 |
| --- | --- | --- |
| `c200502` | **PASS** | [Zippo 英國送修頁](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter)「Prepare Zippo Lighter To Ship」明說內膽通常換新，想取回原內膽須在表單註明；[官方 2026 版送修表 PDF](https://cdn.shopify.com/s/files/1/0471/9532/4576/files/UK-Zippo_Repair_Form_V20082026.pdf?v=1787235480) 的「Comments/Special Instruction」及內膽說明沒有「退回原內膽」勾選格。新版畫面是無字備註空間、分開的泛用零件，明示不畫勾選格；與旁白相容，也未把英國作法說成各地通則。 |
| `c200512` | **PASS** | 英國頁「Sending Zippo Lighter / Customers living in the UK」要求寄件保價且可追蹤，地址是 `Yusen Logistics SDC c/o Zippo Repair Clinic`，接著說 Yusen 收到後轉送 Zippo European Repair Clinic；官方表單首頁也寫轉往 Zippo GmbH（Emmerich, Germany）。新版旁白明說先寄當地收件點、再轉維修中心，正確保留兩段路線和英國範圍；配鏡只畫寄件者與空白追蹤標籤，沒有地址或郵資。 |
| `c200513` | **PASS** | 此句拒絕由英國條款推論其他地區寄法與花費。新版無字概念流程圖有英國收件點及後續維修點，旁邊另一地區圖完全留白；不再將 Yusen 收件站誤畫為最終維修點，亦無跨區價格暗示。 |
| `c200514` | **PASS** | [Zippo 美國保固總頁](https://kb.zippo.com/warranty-repair)限定防風口袋打火機的終身承諾；英國頁提供可能換內膽的現行流程，[美國外觀頁](https://kb.zippo.com/zippo-lighter/worn-deco)把裝飾排除於終身保證之外。旁白只對比功能與回到出廠原貌。新版畫面把磨舊外殼、**未安裝**的泛用內套件及空白保證卡並排，沒有成功維修或完整復原的個案結果。 |
| `c200608` | **PASS** | [公司歷史回顧](https://kb.zippo.com/the-history-of-zippo)將首款與終身承諾連在一起；今日美國[功能保固](https://kb.zippo.com/warranty-repair)、[鉸鏈說明](https://kb.zippo.com/zippo-lighter/hinge-broke)、[外觀排除](https://kb.zippo.com/zippo-lighter/worn-deco)及英國內膽流程各有時地邊界。新版畫面只有磨舊的概念小盒、分離的抽象零件與空白卡，沒有釋然人物、完修對比或能關合的修後成品。此句作為歸納不宣稱某位顧客已完成維修；前文已分開英／美條款。 |

相鄰畫面 `c200501–503` 持續把英國內膽替換說成條件流程，`c200508–511` 保留美國鉸鏈與外觀之別，`c200607` 是假設性的同物件對照，未因上述窄修生出新個案。五處差異 **5 PASS／0 HOLD**；與舊版 59 PASS 合看，這四份精確作者檔案的來源／配鏡關卡可判 **64／64 PASS**。這是文字與原件的覆核，不是圖像生成或成片驗收。

## 待下游留意

- `source-matrix.md` 的 M11 舊摘要仍寫「寄往維修中心」。官方地址雖印 `c/o Zippo Repair Clinic`，實際先由 Yusen 收件再轉送；本版**旁白與來源註記已明確更正**。日後若由來源矩陣自動重寫稿件，宜同步把該摘要改窄；此項未使現版五句 HOLD。
- 英國網頁與表單對預計維修週數的文字不同，本稿未報週數；本次不以任一估期作主張。
- 兩位讀者仍須只看新版 64 句旁白，各自重新做敘事盲讀。劇本及逐鏡需站主另核准；實際 TTS ≥480 秒、整片費用與單集預算路由、付費生成、匯入、上傳和發布都未由這份收據通過。
