# C03｜獨立來源與書面配鏡差分查核

查核日：2026-10-26。查核者：`/root/approved_visual_source_delta`，未參與作者稿。

**SOURCE PASS／WRITTEN VISUAL PASS。** 143句、110景。只核准來源與書面共圖計畫；`actualasset_verified=false`，未實測TTS及12–14分鐘。

## 本次四輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `9639d356ca5bdcb18e85c3631ea754a0f69888949358111f452541654ac7fdd9` |
| script.md | `1698aa0a955713ae5f0eaf9234ad307e32332aa7a02aaa966b8e34bd01736709` |
| narration-only.json | `3d5461032a626e9c3246b5b2214af504e3fffee81c1a83cdda38dc2ba532c235` |
| claims.json | `c8eaf8b7d01704417b147ff7af3080e5a6041d964b9cc6830d5b0153f6eb4328` |

image-reuse-plan.json：`ff55c22c39680a0eb46505e56cd2aea7102ed811cddc591bad3d27ef7683fed3`。完整獨立逐句收據：[reviews/source-teaser-visual-independent.json](reviews/source-teaser-visual-independent.json)。

## 不可變來源基線與差分

來源已核基線video SHA：`65ca1b602a5048e4f6af7c721bf1bd15abf152616c07d179f6ff5b6350c02005`；原獨立收據 `history/before-teaser-image-plan/reviews/source-r3-delta.json` SHA `b4b15def639f0addb280c3cd238de2fdd51d005697fe16a96e22d7ca7725f390`；原verify SHA `1dc587379c910d1a02fb3c35f8206eaca49b01a32c4fcee76e291d84857e74da`。143句的ID、scene及文字SHA逐句實比全同，script/narration/claims JSON、brief、series逐bytes未變。全110景只有h04/h05兩個prompt/camera共4leaf變化，108景完整物件未變，所有9數字卡完整未變。claims.md只加書面計畫附錄。全部64個archive與55個auxiliary及原批53個檔案SHA實核全同，歷史HOLD保留。

本輪親讀招股書原PDF139–140（SHA `bf33730ab8fae0290e95c65ac1e70e734fdeb5061f99e96154f8071772e774fe`）、FY2025原PDF42（SHA `52fdbd6260f2093d264d51ba9e15fe6621e65639b04e64c4d1096a35844827a9`），及官方Code of Ethics §1 HTTP200（SHA `cea751b2482c7e28fd2ac351986c8175534fa5097aae54ab4b6186de4ae4a385`）。匿名圖書館閱讀畫面未冒認史料或歷史作家使用現代商品；空白預測文件與帳本相容五年估算，未提前畫出€107.4m減損。原數字卡保留。

## 原生實算與共圖停止條件

官方screenplay新舊及已批runtime逐bytes相同，SHA `4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`。以現有runtime唯讀字典 `30b814bbdb103aa143cac8b9cfd483f0e379100dcaf3638d18b8866f7fb636fe` 原生計算narrative/speech/look/mix全同，pictures由 `5905cc7dcd62b707` 變為 `057e50e3a5d588d4`；既存native record的narrativeReviewMatches新舊均true，不據此重判敘事。獨立lint新舊均0 errors、31 soft warnings。producer僅memory replay，四輸入及claims.md逐bytes重現；build聲音常值與既有source同值，沒有實際voice變動。

| 共圖pair | 完整composed prompt SHA | seed1 1K key | seed1 2K key |
| --- | --- | --- | --- |
| authors-old-notebook-context | `294fd034c8940154fa4e85f9da4d91673048b486a0bc3bb79f9eba256fd150a0` | `d412156e47533c92` | `ec476f9db34ff556` |
| financial-remeasurement-context | `d780f4974c16a74fe8eab85dd18c6ea166d3fdca2571941c77259584e499d2e1` | `be22fa92ca5132e1` | `d66150a0b42363b4` |

兩端resolveLook、完整composeShotPrompt、camera/cast/references/size/seed及Stage.imageKey等值。這些key的live cache目前全missing，尚無實圖：**第二條teaser命令現在必須停，不得派送新圖或另購相似圖。** 正式生成須先正常驗收payoff，第二命令前重查live cache與accepted實檔SHA。兩端judge/retake任何差異停pair；最終官方manifest、trim衍生selected檔、render/assembly引用與實檔SHA全同才可聲稱實際共圖。

## 既有原件來源表

未變事實依上述精確來源基線接鏈；本輪沒有冒稱重開全部原件。

| Anchor | 原件 | 定位與範圍 |
| --- | --- | --- |
| S1a | Moleskine 2013 年義大利上市招股書 | PDF 123／印刷121；PDF139／印刷137，舊式型制、1995重新生產；發行人回顧，不證法國原工坊直接傳承 |
| S1b | Moleskine 2013 年義大利上市招股書 | §11.2，PDF260／印刷258，Il primo deposito…26 novembre 1997；首次商標申請，不能寫當日完成核准 |
| S1c | Moleskine 2013 年義大利上市招股書 | PDF139–140／印刷137–138，libro ancora da scrivere；prioritariamente…librerie；公司定位、目標客群與書店策略，非全體買家動機 |
| S1d | Moleskine 2013 年義大利上市招股書 | PDF140／印刷138，新管理層投入communication/brand management/merchandising；2006收購後策略，非獨立效果測試 |
| S1e | Moleskine 2013 年義大利上市招股書 | PDF159–160／印刷157–158，Sviluppo e controllo dei fornitori；2013招股書所述委外、流程品質與滾動12月需求規劃，不推現在製造地 |
| S1i | Moleskine 2013 年義大利上市招股書 | PDF160／印刷158，Pianificazione fabbisogni：新產品銷售預測；tra la produzione ed il lancio…3 e i 6 mesi；2013招股書當時安排；生產與上市之間平均間隔，不是純製造工期、下單至出貨或今日固定交期 |
| S1f | Moleskine 2013 年義大利上市招股書 | §6.1.3.5，PDF165／印刷163，直間接通路synergy；發行人策略與自述效益，非已證唯一成長原因 |
| S1g | Moleskine 2013 年義大利上市招股書 | PDF166／印刷164，consignment/non-consignment貨權與風險；向零售商售出後提貨；2013招股書當時一般契約，非消費者結帳，非2025特定客戶合約 |
| S1h | Moleskine 2013 年義大利上市招股書 | PDF167／印刷165，non-consignment出貨或交付；月度向零售商銷售資料與庫存；2013當時契約，配送商到零售商的Sell-In，非終端消費者Sell-Out |
| S2 | Moleskine, Our Heritage | Our Heritage，A Creative History；品牌轉述查特文及1986停產故事；非同期工廠檔案 |
| S3 | Moleskine, Code of Ethics | Code of Ethics §1 Purpose and Scope；歷史人物使用舊類型；2007-01-01公司名稱，不能說使用現代品牌 |
| S5 | Moleskine 2013 年義大利上市招股書 | PDF123–124／印刷121–122，2006收購及法人重整；非1997品牌初創，非2016交易 |
| S6a | D’Ieteren 2017 年投資人簡報 | 2017投資人日投影片11、15–16，批發doors；約1.2萬/2萬是批發據點，非自營店、非全書店 |
| S6b | D’Ieteren2016 ActivityReport及2017年報 | 2016 Activity Report印刷35、37；2017 Annual Report財務印刷7／PDF65；2016年底79直營店；保留投資簡報78衝突 |
| S7 | 義大利交易所 2013 年上市公告 | 2013-04-03上市新聞稿，STAR；market capitalisation €487.6m；上市時整家公司市值，不是銷售收入或募入現金 |
| S8a | D’Ieteren 2016 年收購公告 | 2016-09-22公告PDF1，41%/€2.40/€506m equity value；簽約及計畫，不是已全數收購；估值不是公司現金收入 |
| S8b | D’Ieteren 2016 年收購公告 | 2016-09-22公告PDF1–2，2015營收€128m及premium/outsourcing/cost management；買方當時獲利解釋，未來目標不能當已完成 |
| S9 | D’Ieteren 2017 年完成收購公告 | 2017-01-24 Holds 100% of the Shares公告；完成餘股強制收購、連庫藏股達全部、同日撤牌 |
| S10a | D’Ieteren 2017 Activity Report — Moleskine | 2017 Activity Report分冊PDF6／印刷44–45，81%/19%及Smart Writing；2017銷售比重與當年產品，非現在產品組合或數位轉型成功 |
| S10b | D’Ieteren 2017 Activity Report — Moleskine | 2017 Activity Report分冊PDF5–6／印刷44–45，直營+16.6%、網店-3.7%、平台遷移及人員/IT；當年銷售、營運及投資，不等於利潤 |
| S10c | D’Ieteren 2017 Annual Report | 2017 Annual Report財務印刷7／PDF65，loss-making Retail channel；當年零售通路虧損，不可說每一家店虧損或造成2025減損 |
| S11 | D’Ieteren 2025 Full-Year Results | 2025 Full-Year Results PDF10，Moleskine Results；數表PDF23–25；2025同比、部分美國大客戶控庫存，不是全體消費者拒買 |
| S12 | D’Ieteren 2025 Full-Year Results | 2025 Full-Year Results PDF10、42，品牌無形資產減損與2026–2030現金流；€107.4m稅前品牌減損，非現金支出、退貨或稅後€77.4m |
| S13a | D’Ieteren 2026 Half-Year Results | 2026 Half-Year Results PDF9、11，銷售52.2m/2.2%、有機定義；PDF16營業比較；只比同半年；有機排除匯率及合併範圍變動；非全年 |
| S13b | D’Ieteren 2026 Half-Year Results | 2026 Half-Year Results PDF9、21，€76.4m waiver、186.8m intersegment financing；減免部分本金降低財務費用，非全數免債或營業利潤回升 |

本查核沒有付費、後台呼叫或runtime/approval/media寫入，也不授權發布。生成後圖片QA、實際共圖、媒體實長與成片驗收仍未完成。
