# C05 逐句來源獨立覆核（非付費草稿）

- 日期：2026-10-22
- 查核者：`kincho_source_check`；未參與撰稿，只讀並對一手頁面覆核，不修改檔案。
- 綁定 `script.md` SHA-256：`7D07A7A12478E4956B1DA110819F9C30514BA0C52DA007868F8644A401D78980`
- 同步核對 `visual-plan.md` SHA-256：`7A7068BF5E38E0784EBA4A7DEA93A36FC0A3B988AC64F5B3750EA6FABBD117C3`
- 結論：**六章 88 句逐句來源 PASS；正文長度 HOLD；不等於劇本、逐鏡或付費製作核准。**

查核者對 88 句各自判定，最終均為 PASS：H01–H08、O01–O16、I01–I16、E01–E20、T01–T12、N01–N16。各句使用的來源 ID 與原件對應在 `script.md` 的依據欄；本收據只對上列雜湊有效。首輪 94 句時 O07、E13、E14、E17 需修；第二輪 88 句時 E06、T05、N13 需修。最終稿已逐項更正，並對更新後的完整 88 句重核。

| 來源邊界 | 查核結果 |
| --- | --- |
| 1888 試作 | O07 的「舶來除蚤粉與竹筒」依[金鳥年表](https://www.kincho.co.jp/kaisha/ayumi/index.html)；不把 `のみとり粉` 擅寫成已確認的除蟲菊粉。 |
| 妻子與木模 | I01 把妻子構想歸於金鳥後年記述；I08–I14、E13–E14 按[博物館木模登錄](https://sts.kahaku.go.jp/sts/detail.php?no=910191180001)及[原廠保存物件頁](https://www.kincho.co.jp/new/tech/)區分「原擬填料的試作木模」與約 1910 年後保存的擠出設備。 |
| 申請、上市、製法 | E02 只說[金鳥年表](https://www.kincho.co.jp/kaisha/ayumi/index.html)記載 1900 年專利**申請**；E04 為 1902 年上市。E06 的完整工序缺口只限本次查到的物件資料；[原廠另篇事後回顧](https://www.kincho.co.jp/gaichu/column/100nen.html)稱上市時兩卷手工盤成，不能當同時期製造紀錄，也不能把該頁的 75 公分／七小時倒推成 1902 年規格。 |
| 雙卷與今日用法 | E16–E17 只說擠出的兩根合起來手盤；[技術頁](https://www.kincho.co.jp/new/tech/)未說機器同時擠出。T02–T04 的減少折斷／成本是公司回顧、沒有獨立數字；T05 明言轉到今日，T06–T11 的拆卷／保管按[現行 Q&A](https://www.kincho.co.jp/seihin/qa/qa_uzumaki.html)。 |
| 年代與成分 | E18 的 1940 年自動打型機按[戰前年表](https://www.kincho.co.jp/kaisha/ayumi/ayumi03.html)；E19 的手卷設備使用期按技術頁。N05–N08 的約 75 公分／七小時只屬現行規格；N12–N13 以[工廠說明](https://www.kincho.co.jp/factory/listen/detail.html)和[原廠蚊香解說](https://www.kincho.co.jp/gaichu/taisaku/ka_uzumaki.html)區分現行合成擬除蟲菊酯與早年除蟲菊原料，不比較兩代效力。 |

來源矩陣 F08 仍寫「兩條同時押出」，與技術頁可讀文字不符；這是 **Treatment PR #1672 的矩陣勘誤**，不能讓其已採用雜湊替錯誤背書。本稿和畫面都採原件更窄的說法；矩陣另待受控修訂、重綁雜湊。

長度停線：旁白 1,548 字元，以專案每分鐘約 250 字規劃值約 **6.19 分鐘**，距八分鐘正文約少 452 字元。未產生或計時 TTS；不能宣布八分鐘達標。畫面表 65 狀態、50 shot／15 card 的插圖比率只是狀態數，未測實際畫面時間。

## 79 句修訂版｜獨立來源及逐鏡重核（2026-10-22）

- 查核者：`/root/c08_readonly_scout`，未撰寫本版旁白或畫面計畫。
- 判定：**PASS，限於下列固定雜湊的 79 句旁白事實、來源界線與 79 個逐句畫面意圖**。上方 88 句舊版 PASS 僅為歷史紀錄；其中「F08 仍寫同時押出」及舊長度估算均不適用於本版。

| 固定文件 | SHA-256 |
| --- | --- |
| [script.md](../script.md) | D49FE268109DDCE4BF6E44A3E75831467735DEC23E58D11BCC92065EE533288D |
| [visual-plan.md](../visual-plan.md) | 7908331CE21FE658321D8117D7429ECCA3C1F48C3D558E57B0885E5F26138CAE |
| [treatment.md](../treatment.md) | 4A1C596B9A8A6E9278C99205E9EE381E4FD5AF4EAD5CDC6C448A852D5E7FC8D0 |
| [source-matrix.md](../source-matrix.md) | A7EB8401ABCC5715C46352187C0EFE100FA3AA47E22A020A1FC16FFD55504516 |

逐句覆蓋：**H01–H08、O01–O14、I01–I12、E01–E17、T01–T12、N01–N16，共 79／79 個不同 ID**；V001–V079 各自對應一個旁白 ID，無缺漏、重複或未定義的來源 ID。79 個畫面意圖中 63 個標為 `shot`、16 個標為 `card`，這只是節拍分類，並非畫面時間實測。

| 段落 | 對原件的逐句核對與界線 |
| --- | --- |
| H01–H08 | [金鳥技術遺產頁](https://www.kincho.co.jp/new/tech/)及[資料館](https://www.kincho.co.jp/factory/shiryou/index.html)支持早期直條約 20 公分／40 分鐘；[木模登錄](https://sts.kahaku.go.jp/sts/detail.php?no=910191180001)支持 1895 試作物；手卷擠出機是約 1910 年起的後年設備。現行雙卷拆法見[產品 Q&A](https://www.kincho.co.jp/seihin/qa/qa_uzumaki.html)。H01 的燃燒場景標為情境示意，V001 已改成正在燃燒，與旁白一致。 |
| O01–O14 | [資料館](https://www.kincho.co.jp/factory/shiryou/index.html)支持舊時草木煙與加水增煙；[明治年表](https://www.kincho.co.jp/kaisha/ayumi/index.html)支持 1885–1890 節點，O07 保留原文「舶來除蚤粉」而未擅改成除蟲菊粉。[工廠說明](https://www.kincho.co.jp/factory/listen/detail.html)支持白花與有效成分、細直條易折。其餘桌面長度、單根時間及貨架提問屬明示的幾何或敘事推論，未冒充歷史現場。 |
| I01–I12 | [明治年表](https://www.kincho.co.jp/kaisha/ayumi/index.html)將 1895 構想歸於妻子ゆき；[國立科學博物館登錄](https://sts.kahaku.go.jp/sts/detail.php?no=910191180001)記錄木模為 1895 試作品，原擬填料推出螺旋；[原廠技術頁](https://www.kincho.co.jp/new/tech/)明說木模不適合大量生產。旁白只把較長路徑與較小占地作幾何推論，畫面不臨摹館藏或假造量產現場。 |
| E01–E17 | [明治年表](https://www.kincho.co.jp/kaisha/ayumi/index.html)只證 1900 **申請**、1902 **上市**；未找到原始申請件或上市完整工序。[技術遺產頁](https://www.kincho.co.jp/new/tech/)只證後年設備把已擠出的兩根長條手卷及原廠所述雙卷運損／成本優點，沒有同時擠出、雙卷首用年或獨立成本數字。[資料館](https://www.kincho.co.jp/factory/shiryou/index.html)分列約 1919 年 58 公分／6 小時及約 1922 年另一手卷款／12 小時；E16 已改成**不同年代商品的時數紀錄**，不暗示同時販售或同款升級。海外海報只按[技術頁](https://www.kincho.co.jp/new/tech/)作宣傳存在的證據，未推銷量。 |
| T01–T12 | [戰前年表](https://www.kincho.co.jp/kaisha/ayumi/ayumi03.html)記 1940 自動輪轉打型機**完成**，[技術頁](https://www.kincho.co.jp/new/tech/)的手卷設備使用期約至 1957，[戰後年表](https://www.kincho.co.jp/kaisha/ayumi/ayumi04.html)另記 1957 改良機完成；三者未被說成同廠逐日換線紀錄。[工廠說明](https://www.kincho.co.jp/factory/listen/detail.html)支持約 1955 年 allethrin 實用化、花田縮減與約 1957 年轉左旋的原廠回顧；旁白未將其寫成所有產品同年換配方或性能提升。現行拆卷／保存按[Q&A](https://www.kincho.co.jp/seihin/qa/qa_uzumaki.html)，未倒推早年。 |
| N01–N16 | [工廠說明](https://www.kincho.co.jp/factory/listen/detail.html)把慢燃歸於香條斷面空隙少、氧氣較不易進入；V064 已畫**稀疏氧氣仍有少數進入**，避免暗示完全隔絕。現行約 75 公分／7 小時及另有約 3／12 小時見[Q&A](https://www.kincho.co.jp/seihin/qa/qa_uzumaki.html)。現行有效成分、混料、擠片打型與染綠均限公司所述產品；N10／V073 明指昔日蚊遣**草葉的葉色**意象，不把煙畫成綠色或推回 1895／1902。片末的路徑、密度及雙卷運送是三條分開的機制。 |

此 PASS 不證明旁白已達八分鐘、冷開場／鉤子／插圖畫面時間已達標，也不核准最終 prompt、圖片張數、TTS、配樂、成本、匯入、上傳或發布；這些需各自實測與審核。站主對新版 Treatment／來源矩陣雜湊的窄幅重綁，以及對本版劇本與逐鏡方向的決定，仍是獨立關卡。若上述四份文件有實質改動，須重新核對新雜湊。
