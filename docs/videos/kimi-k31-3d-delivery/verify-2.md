# 全文事實查核2：PASS（限目前文字與證據版本）

查核日：2026-10-26 UTC。已逐讀目前42景、114句的 `text`、全部12筆 `say`、畫面 `data`、縮圖、標題說明與標籤，以及完整 script、claims、brief、R1修訂及verify-1。這不是盲評、旁白聽校、模型測試、製造認證、影片QA、核准或全部製作規則完成。

**獨立性**：查核人 `/root/dns_watch_readonly` 不同於R1查核人及source作者，沒有撰寫本片稿件或原始教具／有限檢查器。先前曾只看實際STL與規格，實作本題的獨立拓撲／五平面剖切證明；因此並非第一次接觸幾何證據。那次是原創教具的幾何驗證，從來不是Kimi模型測試。本輪未重跑幾何命令、未讀R2盲評答案，也未改source或任何審核答案。

## 精確版本

| 文件 | SHA-256 |
| --- | --- |
| video.json | `c06830338a9b1b00267a854b29a61d721c89328b912af217b28b17fe74bcc066` |
| script.md | `7de52a40bfb3df6742219f162e5b659fabb39031280d94a025f9616e1e5c7aad` |
| claims.md | `dddc9642d3b8f1bfe57ec2b8d6f6749efe0116ebade8aeac8b50f0820e528df5` |
| revision-R1.md | `2b2acff632edf1e8505afc913fce33358c603ccf63ad764703023043558d33ea` |
| verify-1.md（原REVISE保留） | `4998ebc664498e2e667d18ddb668a815387d5f8b78cc64ce41c795ed3bd4dcbf` |

114個唯一ID與script的句子、順序完全相同；12個say_for均對上目前text的NFC SHA-256前12碼，逐筆say亦保留對應日期、數字、否定與範圍。R1修訂文件保留較早的4efd…中間版本，末段最終交接及實際檔案則同為目前c068…；本PASS只綁上表版本，不替中間稿或後續改稿背書。

## 三項R1必修：全部解決

| R1項目 | 目前實際文字／位置 | 判斷 |
| --- | --- | --- |
| 開場教具身分 | 第一個口播 `2g58` 即說「二零二六年十月二十六日，我在這台電腦打開兩份自製墊圈教具」；`dag4`另明說不是Kimi生成失誤。 | CONFIRMED。純音也能知道是編輯自製，沒有靠PNG字卡才揭露。 |
| 台北發布日期 | 新聞移到 `lqfp`，text與say均明說「台北時間十月二十四日」；本機示範日期10/26另列。 | CONFIRMED。當日本輪新GET的官方首帖仍為 `2026-10-23T20:12:59.921Z`，台北為10/24 04:12:59.921；未拿blog修改日當首發。 |
| 判斷來源 | `a2bm` 改成「檢查器把檔案的座標與三角形，對照同一份外部規格」。 | CONFIRMED。`check.py`實際讀外部mm、尺寸及體積條件；不再說每個判斷只從STL取得。 |

開場實際引用中性圖00，SHA `569b6bd06455d340de64ad07c7bcea90a94ce5b51494f9ac2f63d90f6e5162ff`；原四張結果圖仍在後段，所有五張SHA對上source assets。這裡是引用與位元組核對，沒有冒稱本輪另做瀏覽器實跑或視覺審片。

## 完整主張表

逐句及159個查核表面（114句、42個scene.data、YouTube／縮圖／assets）另存本輪scratch的 `full-source-claims.json`。下表按證據群合併，未把問句或編輯建議誤算成供應商事實。

| # | 主張／位置 | 來源與本輪狀態 | 判斷；before → after |
| --- | --- | --- | --- |
| c01 | 本機示範10/26；`lqfp`台北發布10/24 | [官方首帖JSON](https://forum.moonshot.ai/t/kimi-k3-1-pro-has-launched-start-exploring-now/629.json)，本輪HTTP200、11:49:51Z | CONFIRMED；R1未標時區 → 目前text/say均標台北，兩個日期用途分明。 |
| c02 | 3D Make線上預覽、編輯、下載列印資產；`2sc4/h9gn/zwa9` | [官方blog](https://www.kimi.com/en/blog/kimi-k3-1-pro)，本輪HTTP200、11:49:50Z | CONFIRMED為官方功能宣告；未升格成我們已登入、生成、匯出或驗列印。 |
| c03 | `ekg8`與說明欄：完整權重11/4前釋出的承諾 | 同一官方blog，HTTP200，仍用未來時態，明列2026 | CONFIRMED；保留「承諾」，沒有寫成權重、授權或自架已驗證。 |
| c04 | `0glu/y868/0m8z`與字卡：92.7、with-tools、Voxel IoU、1000／17900、max effort、Claude Code harness | 同一官方blog的3D段、圖alt與BenchCAD註腳，HTTP200 | CONFIRMED，限定供應商自報的open-model子集；`dzyw`否定列印成功率，未宣稱本片重跑或所有用途排名。 |
| c05 | `hrlr/vum2/cen6`：本次已讀說明未指定STL、未親測匯出／權限 | 本輪官方blog實際文字；完整raw全詞STL命中0。八來源舊快照清單亦已讀 | CONFIRMED為有界的「已讀頁未寫／未親測」；不推論服務不存在STL支援。Quickstart佔位沒有被當數字來源。 |
| d01 | 兩份自製教具；名義外徑40、孔16、厚5、外部宣告mm | 實際STL、spec、provenance及短alias，N/A本機；四組逐bytes核對 | CONFIRMED；全非Kimi產物，填孔是刻意反例。 |
| d02 | `ox5o`及字卡：兩者三軸外框40×40×5 | 同SHA實檔＋原獨立proof，N/A | CONFIRMED；限定X/Y/Z bounding box，不稱任意方向直徑精準40。 |
| d03 | `njr0/q8wd/ip0k/pqc3`：兩者封閉，封閉表面仍可包住通孔 | 同SHA實檔與獨立拓撲：每邊2面、方向／vertex-link、連通性；ring genus1、filled genus0 | CONFIRMED；沒有把單一edge測試或封閉性當成製造認證。 |
| d04 | `o3u0/fu17/ul11`：三角形STL、單位由外部指定、沒有自動保留建模歷史 | [Autodesk](https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/SLD-3D-PRINT.htm)、[LOC ASCII](https://www.loc.gov/preservation/digital/formats/fdd/fdd000506.shtml)、[LOC家族](https://www.loc.gov/preservation/digital/formats/fdd/fdd000504.shtml)，本輪均HTTP200；實際ASCII結構 | CONFIRMED。只說STL與本檢查器範圍，不說所有3D格式無單位；來源檔建議是編輯判斷。 |
| d05 | `h0ab`／體積字卡：512與256面；5269.401與6273.097 mm³ | 原有限結果＋相同SHA獨立proof，N/A | CONFIRMED；三位小數與原值正確。mm³依外部mm假設，不由STL自帶。面數未當品質分數。 |
| d06 | 完整兩條check.py命令；33條射線：ring0、filled33受阻 | check.py原碼、兩個保存結果、已完成短命令收據及R1實跑收據，N/A；本輪不另執行 | CONFIRMED。filled `accepted_for_this_limited_spec=false`，孔與1%體積條件仍為false；exit0僅完成計算。原checker沒有最小淨空欄位。 |
| d07 | `5fad/x4k6/1cox/6rli/su1a`：有限取樣／指定軸向，未驗任意孔、自交、壁厚、切片、材料、強度／列印 | 實際原碼與原獨立proof limitations，N/A | CONFIRMED；所有否定及製造界線仍在，未把PASS外推成安全／承重保證。 |
| d08 | `v4r0/8q11/qlqs`：中高剖面兩圈對一圈，不同高度仍區分中心材料 | 先前獨立proof於Z0.5、1.25、2.5、3.75、4.5，另不同射線spotpeer；同實檔SHA | CONFIRMED為這兩個fixture在五個高度的證據，不是本輪新模型實驗或任意幾何全域定理。 |
| d09 | `i9h8/pypq/c8u0`：64段近似、最小淨空15.980727…／約15.98，差不到0.02 | 實際剖面邊距原獨立proof，N/A；16−15.98072729845233＝0.01927270154767 | CONFIRMED；名義16與最窄值分清。「棒子」是用途情境，沒有實際棒材、列印件或試配記錄。 |
| d10 | `c8hn/33ye/edz9/f106/vw33`：新增最小淨空至少16，這份教具不合；未實作新gate | d09量值與數值比較；實際spec沒有minimum-clearance欄位，check.py沒有該條件 | CONFIRMED為有條件推論。新條件只寫在人可讀交付要求；沒有假稱改spec後重跑、原checker已驗或制定製程公差。 |
| d11 | `3w3j/cezr/rwiy/oe9l/fxx4/45nk`：本checker只讀ASCII；交付原檔＋同版規格＋結果；改名非轉格式 | 實際read_ascii、實際檔案與LOC格式資料；brief站主觀點 | CONFIRMED／編輯建議。沒有承諾Kimi特定匯出或完整CAD可編輯來源。 |

本輪五個新的公開GET使用正常TLS、代理及 `Mokaair-editorial/1.0`，同host間隔至少一秒，沒有認證、帳號或付費請求。blog與forum raw SHA不同於較早快照；本輪重讀的相關實際段落及首帖時間仍支持上述主張，未把不同raw說成byte-exact。Autodesk／LOC兩頁SHA則與R1相同。完整HTTP狀態、日期與body hash在scratch `public-primary-reads.json`；論壇只保留必要首帖時間，未存使用者資料。

## 實檔、未完成項目與結果

- 原創demo凍結清單 `df702ae6a482f3aa344cc238971178e3ca9ae4e0f3cde88e2485a4c4d80a2323` 的30檔，本輪逐檔SHA與bytes全部相符；兩STL、spec、checker及四個短alias仍與原始來源相同。先前獨立proof `3faf79ed…`、freeze `7d53e4fc…` 的身分與限制未變，沒有重新命名成Kimi測試。
- R1的verify-1仍為原REVISE，正式敘事false不由本查核覆蓋。R2敘事由其他讀者負責，本輪不讀其答案、不代填PASS。
- 三頻道各20萬／七日的新聞群門檻仍未證明，brief與reference-study明示未PASS；採題是站主委派下的編輯推薦，不是門檻通過。
- 全文114句沒有超過40字的text；12筆say的事實限定均一致。這是文字檢查，不代表任何讀音或目前音檔已聽校。
- 本輪沒有改事實或source，沒有重跑原生lint。已讀R1修訂末段綁c068…的正常離線lint真exit0、0errors／0warnings、估12.065556分鐘；估值不當成實際旁白或成片長度。
- 原source八個已綁文件結束前再次核對未漂移。production-progress仍有R1階段的舊source欄位，屬ROOT後續進度更新，不拿它代替此報告的目前版本綁定。

**結論：16個證據群的現有主張與限定均有支持；本輪事實修改0、NOT FOUND 0、未解事實項0。R1三項已解決，可就目前文字事實交回下一正常關卡；不因此宣稱整片、八語、音檢、QA、流量門檻、製造或上架包完成。** 本輪不因事實改動要求再一輪（修改0）；往後source或素材換版仍需重新綁定。
