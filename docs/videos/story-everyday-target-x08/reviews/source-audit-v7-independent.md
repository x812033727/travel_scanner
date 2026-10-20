# X08 Target Canada v7｜五句獨立來源查核

結論：**PASS**。本次只查 `video.json` 的五句修訂及其前後語境，未讀其他 reviews，未改稿。五句的事實、歸因及敘事暗示均未超出可查原件；下表的界線須隨文理解。

## 版本與原件

| 檔案 | 重新計算的完整 SHA-256 |
| --- | --- |
| `video.json`（v7） | `ab4d99818ee51bfe9e81893c813caac56f33af68be5de5002844506a97bd7764` |
| `shorts.json`（未變） | `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543` |

以 `git HEAD` 的 v6 對照，旁白文字只改動 `x080206`、`x080216`、`x080306`、`x0803a08`、`x0803a09` 這五句。直接重新讀取 [Target FY2012 Form 10-K（T12）](https://www.sec.gov/Archives/edgar/data/27419/000104746913003100/a2213506z10-k.htm) 與 [Target FY2013 Form 10-K（T13）](https://www.sec.gov/Archives/edgar/data/27419/000002741914000014/tgt-20140201x10k.htm) 原始 HTML；SHA-256 分別為 `84d254f13c1aa646c7e3675081cb98eb5ed79dda5f265ab5606fa628dd33072d` 與 `dbbdbee947bf108d0b4026a0ca4923a0df7a655cfbb27ee57b074e84f6b36225`，均與 `source-notes.md` 定錨值相同。另對照 `source-matrix.md` 的 TC05、TC06、TC23、TC27、TC10、TC11、TC29；矩陣只作索引，以下判斷以 SEC 原文為準。

## 逐句判定

| 句 ID／v7 原句 | Yes/No | 原文證據及說法邊界 |
| --- | --- | --- |
| `x080206`「買到的是開店權利，並非已開門的 Target。」 | **Yes** | T13 Note 7 寫 `purchased the leasehold interests in 189 sites operated by Zellers`，又寫將其中 54 個據點的 `right to acquire the leasehold interests` 售予第三方。T12 Note 8 說取得店址隨後回租予 Zellers，租期最晚至 2013-03-31。故「開店權利」在前句已明言「租約權利」的語境中，是租賃據點權益的口語簡稱；不可解讀為取得全部房地產所有權、189 家 Target 已營業，或每個據點均保證開店。 |
| `x080216`「這批新店的商品，開張後能順利賣完嗎？」 | **Yes** | T12 Item 2 只說 `plans to open 124 stores in Canada in 2013`，並列已有 3 座加拿大配送中心；Item 1 / Distribution 描述一般商品及部分食品的配送途徑。這句是指向開業後銷售結果的問句，未把計畫當成已開店，也沒有宣稱所有商品實際賣完或任何具體配送故障。後文才以 T13 的低於預期銷售與 `excess inventory` 回答。`賣完`不能拿來推定零售業原本應把每件商品售罄。 |
| `x080306`「答案在庫存：公司說銷售低於預期，過多的商品得清貨。」 | **Yes** | T13 MD&A / Canadian Segment / Gross Margin Rate 原文：`The gross margin rate of 14.9 percent reflects efforts to clear excess inventory following lower than anticipated sales and supply chain start-up challenges.` 「公司說」保留公司自述的歸因；「過多的商品得清貨」準確轉述 `clear excess inventory`。`答案在庫存`須連同緊接的 `x080307`「供應鏈剛起步，也增加了壓力」理解，不能說庫存是年報唯一原因、所有店都空架，或此句解釋全部營運虧損。 |
| `x0803a08`「優惠卡之外，這張新店網還有大片賣場要經營。」 | **Yes** | T13 MD&A 說 FY2013 分批開了 124 家店、合計 `14.2 million total retail square feet`；同段描述加拿大 REDcard。T13 風險章稱改善銷售取決於行銷、市場接受、商品組合及避免庫存過多。「大片賣場要經營」是有面積與營運風險作底的敘事轉場，未宣稱面積本身造成虧損。逐句矩陣此行只列 TC11；若維護引文索引，應同列支持面積的 **TC29**。 |
| `x0803a09`「這批店的賣場，合計一千四百二十萬平方英呎。」 | **Yes** | T13 MD&A / Canadian Segment / Sales 原文：`We opened 124 Canadian Target general merchandise stores during 2013 with 14.2 million total retail square feet.` 14.2 million 正是一千四百二十萬，口徑是 FY2013 **已開 124 家店的零售面積總和**；前一句「新店網」使「這批店」的指涉成立。不可把面積套到 189 個租賃權據點或退出公告時的 133 家店，也不可推出單店客流。 |

三處修訂鏡頭亦未引入相反事實：`x080206` 改為規劃台、`x080216` 為新店入口、`x0803a08` 為預期與實際銷售文件；`x080306` 仍為過剩紙箱，`x0803a09` 為正常營業賣場。這些畫面沒有暗示 189 家已開、全部空架，或由面積單獨造成失敗。
