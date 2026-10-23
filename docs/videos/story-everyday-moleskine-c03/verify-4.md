# C03 Moleskine｜本機逐鏡稿第四輪獨立查核

查核日：2026-10-21。**結論：EDITORIAL_VIDEO_VERIFIED_LOCAL；可進唯讀乾跑與實際配音前檢。**本輪在[第三輪編輯稿查核](verify-3.md)後，對最終 `video.json`、20 段旁白、數字卡、來源矩陣及場景界線再做獨立覆核，並核算製作前報價。下列 SHA-256 是本結論的適用範圍；改動口播、卡片或畫面語意後須重新查改動處。這是**本機編輯與來源查核**，不是主機故事企劃匯入收據、TTS 實測、圖像驗收、付費許可、站主看片核准或上架證明。

## 綁定版本

| 文件 | SHA-256 |
| --- | --- |
| `video.json` | `C39B3667A6CC3C5C9F0673DB3C075B1870EFB3D35D60ECF70739F689F10A0A8E` |
| `brief.md` | `452843FFA08CAB1DB5E877B717BE0E84B3AAEB09B8CDEC4D7CD1B3DADE9BF58E` |
| `source-matrix.md` | `A64E3FDA9F2C6D267C2244594527AC892D0E81F833E41E9DA49A863AFBCFC780` |
| `narration-draft.md` | `78955FEEBFAA88CC677688843AE9D181C3F4714401820566406A5BC99ECF9348` |
| `shot-plan.md` | `2CE42B53C5151799EE2CE20C37864ACF159C6C1254CB08188F357E85653EE763` |
| `scene-map.md` | `10D6AC2DEB3CDD59A6B829BEE0BC5930F022C2879250BFD2A14BE447957B558C` |
| `production-quote.md` | `193BE7B4742ADEE64F69BDBE74BEF2E437E4EAEC3619AB4CC96C8253A834B62C` |

## 逐句與來源結果

| 項目 | 結果 | 核對依據與邊界 |
| --- | --- | --- |
| 20 段口播與 94 場台詞 | **PASS** | 去掉段末方括號製作註記後，逐段串接 `video.json` 的 `lines[].text`，**20／20 完全逐字相等**；場景沒有添加未審過的口播事實。§11 改用「就在開場那天」，回指 §01 及卡片的 2013-04-03；§18「但這還不是全部」是轉場，不新增事實。 |
| 歷史起源與產品定位 | **PASS** | [2013 年招股書印刷頁 121–122、138–139](https://www.borsaitaliana.it/prospetti-informativi/1513pros_1_it.pdf)、[品牌 heritage](https://www.moleskine.com/en-hk/the-world-of-moleskine/our-heritage/)與[倫理文件](https://www.moleskine.com/en-no/code-of-ethics.html)支持 1995 重啟、1997 註冊、2007 公司名及「待寫的書」的發行人定位。1986 圖爾只以品牌轉述說；不把歷史作家畫成使用現代商標商品。 |
| 股權、通路與營運時間線 | **PASS** | [2013 交易所公告](https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2013/moleskine.en.htm)、[2017 投資人簡報](https://dieterengroup.imgix.net/documents/presentations/moleskine_lorenzo_viglione.pdf)、[2016 簽約公告](https://dieterengroup.imgix.net/press-releases/DIeteren-Moleskine_-ENG_FINAL.pdf)、[2017 完成收購公告](https://dieterengroup.imgix.net/press-releases/2017_01_24_Moleskine_squeeze_out_EN.pdf)、[2017 活動報告](https://dieterengroup.imgix.net/annual-reports/3_moleskine_en.pdf)及[年報](https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf)分別支持上市市值、批發據點／直營、41% 簽約、100% 完成／下市、紙本 81% 及當年零售虧損。卡片與口播未混同批發據點和自營門市，也未把 2016 簽約說成當日完成。 |
| 2025 與 2026 H1 財務 | **PASS** | [2025 全年業績](https://dieterengroup.imgix.net/press-releases/20260310_FY-2025-Results_EN_FV.pdf)支持 €117.8m、−3.7%、美國大客戶控庫存與 €107.4m 品牌無形資產減損；減損是帳面評價，不作同額現金支出或消費者離棄。[2026 半年業績頁 2、9](https://dieterengroup.imgix.net/press-releases/20260909_Press-release_H1-2026-results_EN_FV-with-appendix.pdf)支持 €52.2m、+2.2%、零售與美國批發回升、營業結果微降、財務費用下降。§19 已改成「減免那筆集團內股東貸款的**部分本金**」；原件仍列未償本金，不再暗示整筆免除或營業利潤轉強。 |

## 11 張後製卡逐項覆核

| 段落卡 | 所述數字／標籤 | 對應來源表 | 結果 |
| --- | --- | --- | --- |
| 01 | 2013-04-03 掛牌 | S7 | PASS |
| 02 | 1986 圖爾停業，明標「品牌轉述／非獨立工廠檔案」 | S2 | PASS |
| 04 | 1995 重啟生產、1997 商標 | S1 | PASS |
| 05 | 「待寫的書」為發行人定位 | S4 | PASS |
| 07 | 2005 約 1.2 萬、2010 約 2 萬**批發據點** | S6 | PASS |
| 11 | 上市市值約 4.88 億歐元，明標非營收 | S7 | PASS |
| 12 | 2016 年底 78 家**直營店** | S6 | PASS |
| 13 | 2016 年 9 月簽約收購 41% | S8 | PASS |
| 15 | 2017 紙本產品占**銷售** 81% | S10 | PASS |
| 18 | 2025 品牌無形資產減損約 1.074 億歐元，標非現金流出 | S12 | PASS |
| 19 | 2026 上半年銷售約 5,220 萬歐元、同比 +2.2% | S13 | PASS |

所有卡片的 `data.source` 均給出發行方及原件；`video.json` 的全片 `sources` 保留這些一手原件連結。PDF 的 `reviewer_only` 限制仍在 `source-matrix.md`，不能因 JSON 列出 PDF URL 就聲稱主機工人已讀全文。若後續改走主機故事企劃／匯入流程，`must_verify`、`reviewer_only` 與獨立 review JSON 應依該流程的 **story plan schema** 建立；它們不是 `video.json.sources` 的欄位，本收據也不代替主機企劃查核。

## 敘事與畫面核對

- `video.json` 有 **94 場：83 張 still、11 張 stats 卡**，插畫占 **88.3%**；最多連續一張卡。21 條 `loops` 的 setup／payoff 台詞 ID 均存在。六章段號與 `brief.md`、`scene-map.md` 相同。圖像 prompt 未放品牌、人名、年份或真實文件，`shot.data` 也沒有 `style`、`negative`；品牌名只留在旁白與後製字卡／縮圖文字。
- 已收斂三處畫面因果：§03 只看現成圓角樣本，不暗示手工製程；§17 的普通貨架及少量封箱訂單不畫成零售全面萎縮、缺貨或倒閉；§19 只更新無字貸款帳卡，不把部分本金減免畫成整筆貸款結清。其餘交易、工廠、書店與人物均為匿名示意；生成後仍須檢查假字、商標、真人近似與實際畫面是否誤導。
- repo `spokenUnits` 重算為**全稿 2,160，02–20 共 2,025**；以 250 units／分鐘推算，後者純語音約 **8:06**，最長 §18 約 **0:40**。本機 `lint --json` 回傳 **0 errors、0 warnings**、94 lines、預估 **10.24 分鐘**；`brief.md`／`scene-map.md` 的約 10:12 也是事前估算，兩者都不能代替 TTS 量長或句級 30–45 秒鉤子實測。

## 製作前報價算式與停線

[製作前報價](production-quote.md)的純算式通過：83 圖 × 3 次 = **249** 次；249 × US$0.0035 = **US$0.8715**（向上預留 0.88），249 × US$0.01 = **US$2.49**，三次圖片與評審上界 **US$3.3615**；另加一首配樂 US$0.08，約 **US$3.44**。預留欄 0.88 + 2.49 + 0.08 + 2.50 + 9.00 + 10.05 = **US$25.00**。這是上界及餘額分配，不是已核銷的全成本。

報價明列服務端 `max_usd_per_video` 為 US$200、未設本片 US$25 pilot budget，故**服務端上限不能執行站主的 US$25 停線**；每次付費前仍須人工核對本片已花、未結算、預估下一次最壞費用。TTS 可用、圖片／評審／配樂餘額和媒體帳本 US$0 是報價文件記錄的瞬時 `--dry-run`／`media-status` 讀值；本輪只核算其邏輯及算式，**沒有重新查供應商餘額、語音計價或實際帳單**。報價所列 Gemini TTS 約 2,582 可計費字元，和 lint 的 7,473 不同，因 `tools/video/core/lint.mjs` 的算法是 Azure 用的漢字雙計加每行標記估數，不能拿來替代 Gemini 乾跑報價。配樂乾跑仍缺 TTS 的 `timeline.json`，待時間軸後再驗。口播 02–20 的預估 8:06 只有六秒餘裕，若實際純語音不足八分鐘，應停在插畫前修稿、重查及重報價。

## 下一關

本次服務快照及圖片／TTS 的部分唯讀乾跑已列於[製作前報價](production-quote.md)；生成前仍須重讀最新單價與本片已花／待結算帳本，並測台灣口音 TTS 的 **02–20 實際時長至少八分鐘**及音訊品質。US$25 表含已查到的圖片與配樂單價，但語音、文字及其他預留額尚非可核銷全成本；付費許可仍待站主決定。其後按實際畫面逐張驗收，看片接受、上傳與 Studio 結束畫面驗證各有獨立收據。
