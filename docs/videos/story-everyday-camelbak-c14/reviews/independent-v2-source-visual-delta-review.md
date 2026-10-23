# C14 CamelBak v2｜獨立逐句來源與逐鏡文字覆核

- 審查者：`codex-c14-v2-independent-review`，未撰寫 C14 作者稿，也未讀或簽署任何純旁白盲評。
- 日期：2026-10-23（Asia/Taipei）；受審 draft PR [#1695](https://github.com/x812033727/travel_scanner/pull/1695) 作者 HEAD `580192b776c058d0261d787606ad5eec2191e833`。本收據審的是該 HEAD 的內容，不預先替後續修訂背書。
- 結論：**逐句來源 PASS；逐鏡文字 HOLD（I01 一張字卡）**。整體劇本／分鏡尚不可採用；修正 I01 後須以新 JSON／MD SHA 複核，不可把本輪來源 PASS 當成雙盲、音長、圖片或站主核准。

## 固定版本與審查範圍

| 檔案 | 本輪直接計算的 SHA-256 |
| --- | --- |
| `treatment.md` | `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E` |
| `source-matrix.md` | `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E` |
| `script.md` | `6F52F13283B8B14941D40A0DBE19D299B8266824A33E22201EEB99C700B25119` |
| `script-source-notes.md` | `6627DC1CDAA301B80B30C087BF3DC746DA1F60032BB29C05EA2047C95F0C9EBD` |
| `visual-plan.md` | `003F2377E74DE402C8F2FCE477A03EBCD4206E6B890585CDC2A230DF1325DC31` |
| `visual-plan.json` | `23E7B36BC84C2A8214CE928F72EC4C12CCCAA6F21D9ED7FF85A0236896AD0DE0` |

舊 [v1 來源／畫面 PASS](independent-script-visual-review.md) 綁舊 SHA；v1 雙盲 HOLD 只由作者收據及 PR 狀態得知，本輪未讀盲評內容。逐行重讀 v2 61 句、來源筆記、61 個 JSON 鏡頭與視覺總綱；另與 `07cd2d43e` 的 v1 作者檔作 diff。既定 [Treatment 採用](owner-treatment-adoption.md)及其獨立差異審查只界定企劃，不替 v2 口播或畫面作證。

## 本輪獨立重開的原件

| 原件 | 讀回結果與證據界線 |
| --- | --- |
| S1 [CamelBak 公司歷史](https://www.camelbak.com/company-history.html) | 頁面明列 `Founded in 1989`；沒有首售日、比賽月日或首款零件。 |
| S2 [CamelBak NZ 地區品牌回顧](https://camelbak.co.nz/pages/about-us) | `From IV to Oh Yeah` 明寫品牌回憶的 **1989 Hotter’N Hell**、Michael Eidson、點滴袋、襪子、車衣背後、管與衣夾；`Drop Everything` 明寫 Jeff Wemmer 帶商品到賽事販售、**1993** 騎機車從佛羅里達到加州拜訪單車店。是事後品牌敘事，非當年賽事或成交紀錄。 |
| S3 [Compass Diversified 2014 Form 10-K](https://www.sec.gov/Archives/edgar/data/1345122/000134512615000005/codi-12312014x10k.htm) | CamelBak 節第 525–535 行有 1989 創立、首款 ThermoBak、九〇年代初山地車追隨者；第 569–593 行描述**當時**的水袋背包、活動別設計、跑步腰包、2006 年進瓶類與 Better Bottle、後續瓶款，以及 **2014 CamelBak 毛銷售額**中水袋背包 37%、瓶類約 50%；第 630、655–657 行談瓶類拓寬整體客群／通路與 2014 通路類別。第 531 行的 148.7m 是**淨銷售額**，不作百分比分母。歷史仍是母公司回顧。 |
| S4 [Fawcett US5085349A](https://patents.google.com/patent/US5085349A/en) | 具名發明人 Roger R. Fawcett；1990-02-08 申請、1992-02-04 授權／公開。說明書第 150、156–158、212 行支持騎車取瓶難題與常閉、受壓打開的管端軟閥；不證 Eidson 原型、首款 ThermoBak 採用日期或零件。 |
| S5 [Fawcett US5803333A](https://patents.google.com/patent/US5803333A)；S7 [US5060833A](https://patents.google.com/patent/US5060833A/en) | S5 第 137–140 行的 **1988** 是較晚專利背景對背包與水容器組合的回顧，非 S2 比賽原件；S7 具名 James M. Edison、Arthur D. Henderson，不能與 Michael Eidson 混同。兩者均未被 v2 口播拿來改定比賽年。 |
| S6 [USPTO 2017 異議檔](https://ttabvue.uspto.gov/ttabvue/ttabvue-91234513-OPP-1.pdf) | 直接開 PDF 本輪逾時；從 **USPTO 同一原件的搜尋索引節錄**核到 CAMELBAK `1988/12/16` 與 THERMOBAK `1989/03/24` 的 first-use 聲稱。這是登記聲稱，非比賽日或訂單證明。v2 只在研究筆記保留，沒有口播或卡片以 S6 定年；此讀取限制不支撐任何額外口播判定。 |

## 61 句來源判定（每個 ID 已讀）

| 口播 ID | 判定及依據 |
| --- | --- |
| H01、H02、H03、H04、H05 | PASS。H01 是 S4 的一般騎車取瓶問題；H02–H03 明歸屬 S2；H04 把原型與 S3 首款商品分開且承認缺商品化步驟；H05 的後期水瓶問題由 S3 的 2006 產品線兌現。 |
| O01、O02、O03、O04、O05、O06、O07、O09、O10、O11 | PASS。S2 的職業／騎乘／襪袋／管／衣夾逐件對上，O03、O05、O09 的物件功能是可讀出的窄推論。O10 **只說品牌事後把該場騎乘記為 1989**，沒有將 S5 的 1988 組合或 S6 的首用聲稱混作同一場；O11 問商品化，未編首售日。 |
| I01、I03、I05、I06、I07、I08、I09、I10 | PASS。I01 只述品牌／母公司 1989 創立說法；I03 是 S3「首款 ThermoBak」；I05–I06 不倒貼 2014 零件；I07–I08 限九〇年代初山地車追隨者。I09 提出管口問題後，I10 **先**聲明 Fawcett 專利是另一人的平行解法。 |
| E01、E02、E03、E04、E05、E06 | PASS。S4 支持 Fawcett 的申請年及常閉／咬合開／鬆開關；E04–E05 明答專利**不能證明**首款採用。E06 轉到 S2 的 Wemmer，未聲稱閥造成販賣或將 1990 申請排成上市後改版。 |
| T01、T02、T03、T04、T05、T06、T07、T08、T09 | PASS。S2 支持賽事販售、1993 機車巡店與佛州至加州範圍；T02、T05 的「其他騎士可遇見商品」為機會層級推論，不是成交紀錄；T06 僅把 S2 與 S3 的早期騎車對象並看，T07 否認單人旅程造成後來成績；T08–T09 將 2006 當下一個**資料有明記**的產品轉彎，沒有把 2014 店種帶回 1993。 |
| N01、N02、N03、N04、N05、N06、N07、N08 | PASS。S3 支持 2006 進入瓶類及 Better Bottle 後的兒童／騎車與日常客群；N04–N06 把騎乘出口近嘴邊與日常瓶可手拿作明示情境推論，沒有聲稱現行商品規格或醫療效益。 |
| N09、N10、N11、N12、N13、N14、N15、N16 | PASS。N09–N11 把 2014 店種及整體通路擴展分開，否認逐店「首次因瓶進貨」因果；N12–N16 的山地車、越野騎車、步行／登山、雪地及跑步腰包形態逐項對 S3 的 2014 商品段，不倒填首款商品。 |
| N17、N18、N19、N20、N21、N22、N23 | PASS。N18–N19 明說 **CamelBak、2014 年、毛銷售額、瓶類約 50%／水袋背包約 37%**，N20 排除現況市占與 Wemmer 單因果；N21 回答騎乘／日常兩種拿水位置，N22–N23 是留言與訂閱邀請，未另立史實。 |

## 逐鏡文字判定

**HOLD：I01 後製卡的日期否定語。** `visual-plan.json` 的 I01 `post_text` 是「**公司回顧：成立於 1989 年｜不是原型比賽日期**」。O10 前一張卡卻寫「品牌多年後回顧：騎乘 1989」；S1／S3 的 1989 成立年份**不能替比賽定年**，但 S2 確實也把那場騎乘記在 1989。I01 目前的「不是原型比賽日期」容易被讀成「1989 不是原型比賽年份」，與 O10 及口播 O10 衝突。請只修 I01 卡，例如「**公司回顧：1989 年成立｜成立年份不證比賽日期**」，或只留「**公司回顧：1989 年成立**」。修後另出新版 SHA 再覆核 I01／O10，並同步改任何重複的視覺總綱文字；本審查者不改作者檔。

其餘逐鏡文字 **PASS（限紙上文字）**：H01–H05、O01–O11、I03–I10、E01–E06、T01–T09、N01–N23 的鏡頭逐一對口播，49 個插圖 prompt 都是泛用物件／無名人物，不要求商標、可讀字、真人長相、真實賽場／店面、專利附圖或未證銷售場景；12 張後製卡除 I01 外只把姓名、年份、產品名、2014 比例置於 `post_text`。尤其 E01 卡先標「另一人」，E02–E05 不畫專利圖或產品譜系箭頭；T03／T04 才標 1993 與走訪範圍；N18／N19 的卡片保留同年同分母。圖像是否真的合規仍須生成後逐張驗收。

獨立 JSON 檢查：61 個唯一行 ID 與 61 句同序；`look` **恰為** `{"preset":"cute-mystery"}`，預定模型 MiniMax `image-01`；49 插圖／12 卡，最長連卡 2，卡片沒有 prompt 或 motion。插圖 prompt 未見品牌／產品／真人姓名、logo、畫風 token（含 `cute`、`mystery`、`cartoon`、`chibi`、`style`）；符合 [brand-story skill](../../../../.agents/skills/brand-story/SKILL.md) 的精確 look／禁名規則與 [curio-episode skill](../../../../.agents/skills/curio-episode/SKILL.md) §插圖提示詞「畫風只在 look 裡」的規則。正文紙上 505.4 秒、插圖 397.5 秒（78.7%）、片頭 H05 後 5 秒、片尾 21 秒，**全是字元估計與排版**。未 TTS，不能判正文實際 ≥480 秒、實際插圖 ≥70%、鉤子實際間隔、任何圖片品質或成片 PASS。

本輪沒有讀盲評內容、生成圖片／聲音、付費、匯入、上傳、發布、合併或部署。
