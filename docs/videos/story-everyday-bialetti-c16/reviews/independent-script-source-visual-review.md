# C16 Bialetti｜獨立逐句來源與配鏡覆核

審查者：`codex-c16-independent-script-review`（非逐字稿作者）

審查日期：2026-10-23

對象：草稿 PR [#1704](https://github.com/x812033727/travel_scanner/pull/1704)，審查前精確 head `883359dbaaf8e76ed84dcb63521b048e760d616e`。本收據本身後續若推入同一 PR，PR head 會改變；下列判定只繫於表中四份輸入的 Git blob bytes。

## 裁決

**HOLD：85/85 句旁白的來源與 Treatment 邊界通過；85/85 配鏡已逐鏡讀過，其中 78 鏡通過、7 鏡需修正。** 目前不可把整套劇本及逐鏡方向報成獨立審查 PASS，亦不是站主核准或付費製作授權。七鏡的問題集中在把 **1957 年雜誌印刷廣告**畫成展場直立海報，以及把**不同博物館的館藏紀錄**畫成當前／同場展櫃；語音文字不必因本次發現重寫。

| 凍結輸入（`git show HEAD:<path>` 原始 blob bytes） | bytes | SHA-256 |
| --- | ---: | --- |
| `script.md` | 12941 | `1F92C7016D71488D4553E9D3AF246A41B2CC8435CC1A19468BED0106212CE22F` |
| `script-source-notes.md` | 8339 | `A650E4B7A4A7BA0FBCE2C279242C7B447DC5ED6C656168C98045EE96E7978C0A` |
| `visual-plan.json` | 20489 | `1238039373D123C1461BFE3AE4E9020C1F7BB3B7D0BC8B1217DEBBAC2D9BA364` |
| `visual-plan.md` | 13943 | `748B551F18E1FA93184B643D14734BD83F17E34EC7DD943D38D77E16C7E1E548` |

依據已採用的六章 [Treatment](../treatment.md)（Git blob `1B82057CE1CA064C84829F64F2D5B4679CC2E9CCA74F14F24964650636282EEE`）及 [來源矩陣](../source-matrix.md)（`3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713`）審查。逐字稿共 85 個不同 ID，JSON 亦有 85 個不同 ID，順序一一相同；`visual-plan.md` 的 85 列與 JSON 各自的 `kind`、景別／文案及備註完全相同。規劃為 74 鏡原創插圖、11 張後製字卡，字卡最長連續 1 張。這是文字與規劃查核，尚無生成插圖、配音時長或 70% 畫面時間實測。

## 直接核讀的一手來源與邊界

| 主題 | 來源與本輪讀到的定位 | 本稿判斷 |
| --- | --- | --- |
| 1919 工坊及戰後宣傳 | [Bialetti 2007 上市公開說明書](https://www.borsaitaliana.it/prospetti-informativi/926pros_1_it.pdf)，印刷頁 68 §5.1.6；[Museo Omero 人物頁](https://museoomero.it/opere/autori/alfonso-bialetti/)的工坊、早期小量和 Renato 段；[義大利文化部檔案局回顧](https://archivi.cultura.gov.it/archivio-notizie/notizia?cHash=b4df0ebe9d75773a99c305c144cf217c&tx_news_pi1%5Baction%5D=detail&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Bnews%5D=2168)。 | c160202、c160501–504、512、515、608 把公司／館方質性沿革和可證事實分開；無產量或廣告轉銷量數字。 |
| 舊家用器具、結構與館藏實物 | [Museo Omero〈Moka〉](https://museoomero.it/en/opere/moka/) Description、Original Date 1956。 | c160205–210、401–407 只講已有翻轉／過濾器具及摩卡三層水路；c160603 把 1956 當該館實物年代。 |
| 1933 設計回顧、後期登記、洗衣傳說及廣告說法 | [MoMA 藏品 431.2008](https://www.moma.org/collection/works/118645)標 `Designed 1933 (this example 2008)`；[義大利政府《Italia Geniale》產品頁 PDF](https://www.mimit.gov.it/images/stories/download/Catalogo_Italia_Geniale_Schede_prodotti_esposti.pdf)，印刷頁 152–153 列 `Utility models` #34833／1950-07-05、#37736／1951-05-05，且洗衣鍋段以 `Legend has it` 起句；[ADI 完整圖錄](https://www.adi-design.org/upl/ADI%20MOSTRE%20CATALOGHI/Italia_Geniale_CATALOGO-CATALOGUE.pdf)，印刷頁 154–157。 | c160104、301–312、505–507 把後來設計標示與兩項較晚登記分開；c160303–305 明示傳說；c160412–415 把「像咖啡館」限為回顧性行銷願望。字卡兩登記號與日期相符。 |
| 沖煮與義式濃縮差異 | [Navarini 等原始熱工論文全文](https://prokofe.ru/files/public/1545073690_16273_FT107421_experimental_investigation_of_steam_pressure_coffee_extraction_in_a_stove-top_coffee_maker_l.navarini_navarini2009.pdf)，摘要、§1、§3.1；DOI `10.1016/j.applthermaleng.2008.05.014`。 | c160404–410 符合壓力驅動與未達常壓沸點即可開始萃取；c160413–415、609 沒把摩卡飲品說成機器義式濃縮或填一個固定壓力值。 |
| 1957 印刷廣告 | [Fondazione Fiera Milano 透過 Google Arts & Culture 發布的館藏說明](https://artsandculture.google.com/asset/pubblicit%C3%A0-moka-express-bialetti/MgG9-eGz81X0-Q?hl=en)：`aprile 1957`，明列《Fiera di Milano》雜誌第 16 頁的廣告插頁，內容為米蘭展場花壇陳列照片。 | c160509–511 旁白只證當時的展場／印刷宣傳，不推銷量；部分配鏡把來源載體換成直立海報，見下方 HOLD。 |
| 1958、角色、後續產品 | [Bialetti 官方歷史年表](https://bialettiafrica.com/pages/our-history) 1958 和 2010 條；[公司上市公開說明書](https://www.borsaitaliana.it/prospetti-informativi/926pros_1_it.pdf)印刷頁 68。 | c160513 說 Paul Campani 繪角色但不指像父或子；c160516 明說是公司年表的 1958 電視節點；c160610–611 的 Espresso System 是另列產品線。 |
| M16 與 M17 未決 | [MoMA 館簽](https://www.moma.org/collection/works/118645)把小鬍子說成 Bialetti 本人；[Museo Omero 人物頁](https://museoomero.it/opere/autori/alfonso-bialetti/)說成 Renato；[1937 年義大利《Gazzetta Ufficiale》原刊](https://www.gazzettaufficiale.it/eli/gu/1937/11/24/272/sg/pdf)印刷頁 4219 列 Spadini 的 #14691 模型但未附足以裁定合作／權屬／訴訟的原件。 | 85 句沒有指定鬍子角色身份，也沒有說 Alfonso 唯一發明整套原理、1933 專利、Spadini 合作或訴訟勝負。c160107／612 是審慎的編輯總結，未把 HOLD 改為肯定句。 |

## 需修的七個配鏡

| ID | 現稿風險 | 精確修法 |
| --- | --- | --- |
| `c160106` | 在預告 1957 年米蘭廣告時畫概念展場直立空白海報，容易先讓觀眾把後來要揭示的「一張紙」理解成現場海報。 | 改為兩層概念畫面：展覽場地輪廓和一頁素面雜誌／檔案紙，明確不描摹歷史廣告。 |
| `c160508` | 從登記本走向概念展場入口的空白海報，把下一份館藏資料預設為場內張貼物。 | 鏡頭轉向檔案桌上的素面雜誌頁；場地只作該頁所記錄的背景。 |
| `c160510`、`c160511` | 配「這張紙」與其證據能力時畫參觀者看直立印刷海報；[館藏說明](https://artsandculture.google.com/asset/pubblicit%C3%A0-moka-express-bialetti/MgG9-eGz81X0-Q?hl=en)明列的是雜誌第 16 頁印刷廣告，照片記錄米蘭展場花壇陳列。 | 用原創、無字的雜誌頁／檔案夾呈現「印刷物存在」，另用抽象場地線條表達畫中展場；不要重畫原廣告。 |
| `c160602` | 配 MoMA「同一張館藏記錄」時畫館員指向展櫃物件；[MoMA 當前館藏頁](https://www.moma.org/collection/works/118645)標 `Not on view`。館藏與公開展出不是同一事。 | 改畫館藏目錄卡／螢幕與一只**概念**素面壺分置檔案桌，不聲稱它在現場展櫃。 |
| `c160604`、`c160605` | 連續以兩個展示台、同一展廳表現 MoMA 2008 與 Omero 1956，視覺上把兩家不同機構的兩只實物安排成同場展出，來源僅能證各自館藏紀錄。 | 用兩個分隔的館藏資料畫格／檔案夾，各自後製年份；不能畫同一展廳的雙展台或真實藏品重建。 |

`c160519` 是章末泛指未來查閱館藏的概念場景，沒有說具體館館名，未列為停線；修訂時可一併改為檔案桌，讓跨章視覺語法一致。所有七鏡均只需修 `visual-plan.json` 與 `visual-plan.md` 的成對文案，無需購買圖片或改動已通過的 85 句旁白。修訂後重新計算兩份視覺檔的 blob SHA-256，請另一名審查者覆核更動鏡與前後配對；本收據不得被當作修訂版的 PASS。

## 逐句／逐鏡覆蓋

下表每個 ID 都已對照該句旁白、作者逐句來源註記、相同 ID 的 JSON 與 Markdown 鏡頭及上述一手來源。`聲` 是本輪旁白來源判定；`畫` 是配鏡判定。`P`＝PASS，`H`＝上述可定位 HOLD。來源代號沿用 `source-matrix.md`；純過橋／邀請句仍核過與上下句連續性，標為「敘事」。

| ID | 來源／作用 | 聲 | 畫 |
| --- | --- | :---: | :---: |
| c160101 | M06 | P | P |
| c160102 | M02、M08 | P | P |
| c160103 | M01、M03 | P | P |
| c160104 | M03–M04 | P | P |
| c160105 | M03、M09 | P | P |
| c160106 | M11 | P | H |
| c160107 | M03–M05、M17 | P | P |
| c160108 | M01–M12 | P | P |
| c160201 | M01 | P | P |
| c160202 | M01 | P | P |
| c160203 | M01 | P | P |
| c160204 | M01、M06 | P | P |
| c160205 | M02 | P | P |
| c160206 | M02 | P | P |
| c160207 | M02 | P | P |
| c160208 | M06 | P | P |
| c160209 | M06 | P | P |
| c160210 | M06–M07 | P | P |
| c160211 | M03–M04 | P | P |
| c160212 | M03–M04 | P | P |
| c160301 | M03 | P | P |
| c160302 | M03–M04 | P | P |
| c160303 | M05 | P | P |
| c160304 | M05 | P | P |
| c160305 | M05 | P | P |
| c160306 | M03、M13–M14 | P | P |
| c160307 | M03–M04、M13–M14 | P | P |
| c160308 | M03–M04 | P | P |
| c160309 | M03–M04 | P | P |
| c160310 | M03–M04 | P | P |
| c160311 | M03–M04 | P | P |
| c160312 | M03–M04 | P | P |
| c160313 | M03–M06 | P | P |
| c160314 | M06–M07 | P | P |
| c160401 | M06 | P | P |
| c160402 | M06 | P | P |
| c160403 | M06 | P | P |
| c160404 | M06–M07 | P | P |
| c160405 | M06 | P | P |
| c160406 | M06 | P | P |
| c160407 | M06–M07 | P | P |
| c160408 | M07 | P | P |
| c160409 | M07 | P | P |
| c160410 | M06–M07 | P | P |
| c160411 | M07–M08 | P | P |
| c160412 | M08 | P | P |
| c160413 | M07–M08 | P | P |
| c160414 | M07 | P | P |
| c160415 | M07–M08 | P | P |
| c160416 | M09 | P | P |
| c160417 | M09–M11 | P | P |
| c160418 | M09 | P | P |
| c160501 | M09 | P | P |
| c160502 | M09 | P | P |
| c160503 | M01、M09 | P | P |
| c160504 | M09–M10 | P | P |
| c160505 | M04 | P | P |
| c160506 | M04 | P | P |
| c160507 | M03–M04 | P | P |
| c160508 | M04、M11 | P | H |
| c160509 | M11 | P | P |
| c160510 | M11 | P | H |
| c160511 | M11 | P | H |
| c160512 | M10 | P | P |
| c160513 | M10、M16 | P | P |
| c160514 | M09–M11、M16 | P | P |
| c160515 | M01、M09–M11 | P | P |
| c160516 | M12 | P | P |
| c160517 | M01、M11–M12 | P | P |
| c160518 | M03–M05、M11–M12 | P | P |
| c160519 | M13–M14 | P | P |
| c160601 | M13 | P | P |
| c160602 | M13 | P | H |
| c160603 | M14 | P | P |
| c160604 | M13–M14 | P | H |
| c160605 | M03、M13–M14 | P | H |
| c160606 | M01、M06–M07 | P | P |
| c160607 | M03–M04、M11 | P | P |
| c160608 | M09–M12 | P | P |
| c160609 | M07–M08 | P | P |
| c160610 | M15 | P | P |
| c160611 | M07、M15 | P | P |
| c160612 | M01–M12 | P | P |
| c160613 | 觀眾留言題 | P | P |
| c160614 | 本系列訂閱邀請 | P | P |

## 2026-10-23 作者七鏡修訂之獨立差異覆核

作者修訂後、寫入本段之前的草稿 PR #1704 精確 head：`4501a630481d7399c598103c5310f14451f41b84`。從該 head 的 **Git blob bytes** 重算：

| 文件 | bytes | SHA-256 | 相對本收據首輪 |
| --- | ---: | --- | --- |
| `script.md` | 12941 | `1F92C7016D71488D4553E9D3AF246A41B2CC8435CC1A19468BED0106212CE22F` | 未變 |
| `script-source-notes.md` | 8339 | `A650E4B7A4A7BA0FBCE2C279242C7B447DC5ED6C656168C98045EE96E7978C0A` | 未變 |
| `visual-plan.md` | 14126 | `8BFECB74AA53597E9ABF099B497E3F124C056F3AA617BD356DE149005A9B935A` | 改七鏡 |
| `visual-plan.json` | 20672 | `573D4A485E4611B475558C83D0A3CC0BE5A20D672E37F700919BCEFD128DE91B` | 改七鏡 |

Diff 顯示兩份視覺檔只改原 HOLD 的七個 ID。逐項回核同 ID 旁白、前後鏡與[1957 年館藏印刷廣告](https://artsandculture.google.com/asset/pubblicit%C3%A0-moka-express-bialetti/MgG9-eGz81X0-Q?hl=en)、[MoMA 藏品頁](https://www.moma.org/collection/works/118645)、[Museo Omero 藏品頁](https://museoomero.it/en/opere/moka/)後：

| 改動 ID | 差異裁決 |
| --- | --- |
| `c160106` | PASS。預告鏡變成素面雜誌頁與抽象展場花壇，不再把館藏紙件畫成直立海報，也未複製歷史廣告。與 `c160105` 工坊／廚房、`c160107` 年份卡的轉場可接。 |
| `c160508` | PASS。登記本轉到無字雜誌，展場只作遠景輪廓；連接 `c160507` 登記和 `c160509` 印刷廣告字卡。 |
| `c160510`、`c160511` | PASS。以開啟的素面雜誌頁和另置的空白銷售紙，分別對應「印刷宣傳存在」及「無法從單頁推出購買人數」。未把原件重畫成海報。 |
| `c160602` | PASS。館藏目錄卡和獨立概念壺示意圖對應「同一張館藏記錄」，不再聲稱 MoMA 實物此刻陳列。 |
| `c160604`、`c160605` | PASS。兩份各自分隔的館藏檔案及不同資料盒對應兩館、兩個實物年代，不再同場展示兩件藏品。`c160603` 的後製年份卡仍清楚分別歸屬。 |

**新 head 的整套配鏡仍 HOLD，餘一鏡 `c160607`。** 這是本輪順看 `c160606–609` 才發現的首輪漏項，覆寫上方首輪表格對 `c160607` 的 `畫=P`。`c160607` 旁白回收「五〇年代的登記、展場廣告」，配鏡仍把第三份時間線物件畫成`空白海報`；與唯一已定位的 1957 年《Fiera di Milano》雜誌第 16 頁廣告載體不符，也與剛修好的 `c160510–511` 視覺語法衝突。請作者只把此鏡第三份物件改成素面／無字的**雜誌頁或檔案頁**，同步 `visual-plan.md` 與 JSON；不要重畫真實廣告。`c160606` 的工坊／機制、`c160608` 的家庭擴散、`c160609` 的沖煮差異皆可留。

因此此 head 為 **85/85 句來源 PASS、84/85 鏡 PASS、1/85 鏡 HOLD**。85 個旁白 ID、85 個 JSON 鏡頭與 85 個 Markdown 鏡頭仍同序一一配對，Markdown／JSON 各列內容相符。若作者再改 `c160607`，此段視覺雜湊即失效，需以新 head 和新 blob SHA-256 作最終 delta 覆核；本段仍不是站主核准或製作授權。
