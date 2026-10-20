# Target X08 v12｜獨立來源差異審查

**來源 PASS。** 2026-10-20，只核對 v11→v12 新問句、對應數字、畫面提示與 Short 1 收束；v11 全片逐數審查見 [原收據](source-audit-v11-independent.md)。此收據不替代 v12 兩位敘事盲讀、實際配音片長或成片 QA。

主片 `video.json` SHA-256 `b0b91c300c35e64bf0345dc3c9a91b027937f36068b75ec2ed32ff7ae914bdbc`；兩支 `shorts.json` SHA-256 `060ddf682a17307c0747aa560916a2a0b8bcb151ffca60cccdc695fc231b862c`。

| 判定 | v12 差異 | SEC 原件核對與界線 |
| --- | --- | --- |
| PASS | `x080208` 仍把 Zellers 回租終期說為最晚 2013-03-31，但改問開店前配送中心數；`x080212` 明答三座。 | [Target FY2012 10-K](https://www.sec.gov/Archives/edgar/data/27419/000104746913003100/a2213506z10-k.htm) Item 2 寫 `all end no later than March 31, 2013` 與 `We also own 3 distribution centers in Canada`。下載 HTML SHA-256 `84d254f13c1aa646c7e3675081cb98eb5ed79dda5f265ab5606fa628dd33072d`。沒有推定每一租回店址按時開門。 |
| PASS | `x080210` 改問加拿大首批 Target 門市何時迎客；`x080225` 答 FY2013 第一季開首批 24 間。 | [Target FY2014 Q1 原始業績公告](https://www.sec.gov/Archives/edgar/data/27419/000002741914000018/a2014q1ex-99.htm) 說 `first quarter 2013 when Target opened its first 24 Canadian stores`。下載 HTML SHA-256 `cda825d969174a631e9eb9f66585574ff711989d20ddf68b0ab73de5817b5568`。主片不把這 24 店逐一認作上述 Zellers 租回店址。 |
| PASS | `x080421` 問樣本擴大後的同店結果；`x080422`–`x080425` 答 82 間、其中 34 間新達資格、這季 +1.6%，並明示不能說同一批老店翻正。 | [Target FY2014 Q3 原始業績公告](https://www.sec.gov/Archives/edgar/data/27419/000002741914000033/a2014q3ex-99.htm) 說 `1.6 percent`、`82 Canadian stores ... including 34 that became mature during the third quarter`。下載 HTML SHA-256 `045ad1e81177229c378790af8ec5240a2776277c987caf0f8062d911214dca77`。Q2/Q3 eligible 店群不同；v12 沒把群體變動誤說成相同老店反彈。 |
| PASS | Short 1 最後一拍 `x080511` 說原件沒有列每店同一天關門，和先前 `x080510` 的截至 2015-05-02 全關並列。 | [Target FY2015 Q1 10-Q](https://www.sec.gov/Archives/edgar/data/27419/000002741915000018/tgt-20150502x10xq.htm) 寫 `As of May 2, 2015, all stores have been closed`；下載 HTML SHA-256 `5916ab69c69940ee20cddd0fc43e7cf2aac187d80294242c0dce038299610a85`。原件只給截至日，沒有最後一家店的確切日；Short 不自行補日。 |
| PASS | 提問鏡頭把配送中心個數與 Q3 結果藏到後續來源句。 | 畫面提示不增加商業事實，亦沒有預先透露要在後面才回答的 3 或 +1.6%。此項仍需生成後逐圖 QA。 |

來源無新待修錯誤；v12 的問答是否自然、兩支 Shorts 是否獨立成立，交兩位未看舊稿的讀者判定。
