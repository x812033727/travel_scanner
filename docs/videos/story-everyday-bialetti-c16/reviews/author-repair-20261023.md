# C16 Bialetti｜作者修訂與狀態行同步收據

依[首輪及第二輪獨立稽核](../../brand-story-independent-reviews/C16-bialetti-20261023.md)記錄作者修正；本收據本身**不作獨立裁決**，也不是站主核准、劇本或製作授權。草稿 PR #1698 維持 `no-auto-merge`。

## 凍結範圍

| 文件 | 首輪審核 SHA-256 | 第二輪差異覆核已讀的 SHA-256 |
| --- | --- | --- |
| `treatment.md` | `B0367876AF7F283ABEF9AA1F952918B3CE2653C28B48469375B25F813D1E6487` | `7C4D675CAD01D6A255ADF540B05131A72488E97F51E7238090CA10A8ED52F5A1` |
| `source-matrix.md` | `02E1740E09E64C4BDAD90DFEAB01EBDCBA21DF89757029CEAC71D7E4888C85FF` | `3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713` |

修訂起點為 PR #1698 `7b5e7ada72083b1ee08a80013b3464cda842996e`。若這兩份正文再改字，以上新雜湊失效，須重新產生收據並獨立複核。

## 按稽核項修正

| 項目 | 可直接核的定位 | 作者修正與仍留的界線 |
| --- | --- | --- |
| M04／M05／M08 | [ADI《Italia Geniale》完整圖錄](https://www.adi-design.org/upl/ADI%20MOSTRE%20CATALOGHI/Italia_Geniale_CATALOGO-CATALOGUE.pdf)：印刷 154–155／完整 PDF 第 78 頁有 #34833、#37736 及 `Legend has it`；印刷 156–157／PDF 第 79 頁有圖 5 的 1933 標示與咖啡館廣告語。 | 用已直接開啟的完整圖錄取代原先無法覆核的 MIMIT 節錄定位；兩組跨頁分開。1950／1951 登記不補作 1933 專利；廣告語不證實杯中咖啡相同。 |
| M07 與 Treatment 第 4 章 | [Navarini 等原研究 DOI 10.1016/j.applthermaleng.2008.05.014](https://www.sciencedirect.com/science/article/pii/S1359431108002299)，§1；[全文副本](https://www.prokofe.ru/files/public/1545073690_16273_FT107421_experimental_investigation_of_steam_pressure_coffee_extraction_in_a_stove-top_coffee_maker_l.navarini_navarini2009.pdf)。 | 移除已回 404 的協會 PDF、`9 bar ± 1` 及 Treatment 的「協會定義」；只保留原研究的摩卡與機器義式濃縮在沖煮、感官上的質性差異。不給摩卡壺固定壓力。當時 Treatment 首段仍明示差異覆核 HOLD，後見下方狀態行同步。 |
| M17 | [義大利王國《Gazzetta Ufficiale》1937-11-24 第 272 號](https://www.gazzettaufficiale.it/eli/gu/1937/11/24/272/sg/pdf)，印刷頁 4219／PDF 第 11 頁，表列 Spadini Otello Amleto 的 #14691 多面體咖啡容器模型。 | 把 1937 公告列成**另一件**同期模型線索；公告無完整圖紙，De Ponti、契約及訴訟原件仍未讀到。維持起源／權屬／抄襲判斷 HOLD。 |
| M18 | [ES318772A1 公開書目](https://patents.google.com/patent/ES318772A1/en)，`Priority date`、`Filing date`、`Publication date`、`Original Assignee`。 | 分開 1964-10-15 優先權、1965-10-14 西班牙申請、1966-03-16 公開；原受讓人欄是 `Alfonso Bialetti and Co SpA`，不稱 Alfonso 個人是該件申請人。此件不補作 1933 原始專利。 |

上述 ADI 完整圖錄、1937 原刊與 ES318772A1 網頁由作者另行打開核對；Navarini 全文由首輪獨立審核直接閱讀，未新增數值主張。矩陣變更列保留 `RECHECK` 的作者標記；其[第二輪獨立差異裁決](../../brand-story-independent-reviews/C16-bialetti-20261023.md)已對凍結雜湊判定來源修正 PASS。M16 人物身分及 M17 的起源權屬仍為 HOLD；本輪無逐字稿或付費作業。

## 第二輪 PASS 後的狀態行同步

第二輪審核凍結 PR head `11a59a5e82486590419e947fca57b24fff754626`、Treatment SHA-256 `7C4D675CAD01D6A255ADF540B05131A72488E97F51E7238090CA10A8ED52F5A1` 及矩陣 SHA-256 `3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713`。審核指出 Treatment 首行仍把已通過的來源差異覆核標成 HOLD。本次**只改 Treatment 的狀態行**：企劃來源差異覆核已通過，可交站主審方向；M16 與 M17 的未決事實仍不寫成確定旁白，劇本與付費製作仍未獲核准。六章內容與矩陣位元組不變。

| 狀態行修訂後文件 | SHA-256 | 說明 |
| --- | --- | --- |
| `treatment.md` | `1B82057CE1CA064C84829F64F2D5B4679CC2E9CCA74F14F24964650636282EEE` | 只待獨立做狀態行及雜湊的機械核對，不重判未變的史實。 |
| `source-matrix.md` | `3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713` | 與第二輪 PASS 凍結值相同。 |
