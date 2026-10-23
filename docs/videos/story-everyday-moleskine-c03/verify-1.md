# C03 Moleskine｜獨立來源審查，第 1 輪

審查日：2026-10-21。**判定：須修稿後重審；不得把本檔當成最終查核通過或付費生成核准。** 本輪逐項讀取交易所保存的義大利招股書、品牌官方歷史與倫理文件、交易所上市公告、D’Ieteren 交易公告／投資簡報／2017 活動報告及 2025 全年、2026 上半年財報。財報與交易原件的 PDF 仍應在正式故事企劃內標成 `reviewer_only`，不能聲稱主機工人能自動擷取。

本判定只綁定下列原始位元組（SHA-256）；任何一檔改動，修稿版需另做雜湊綁定審查：

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `6761a3bc8b256271595fcec778dbbbfdf24137311df22556c0ac0e8c54fc86f3` |
| `source-matrix.md` | `850530fd939e14b263161092cc72806026d197594fe53e2d8c2758c372cae928` |
| `narration-draft.md` | `2c75bb7bb98e4f2681aacb1e940d62ff7c425f9facb3b4859859acf87faca5d9` |
| `shot-plan.md` | `c4c8e78f7fe1132a04a0db8011c4ca59322e423c02d4c98f4228f564e162a3da` |

## 必修項

1. **有機成長口徑，§§18–19**：2025 的「其他通路按不計匯率變動的算法」與 2026 的「若排除匯率影響，有機成長是 6.2%」都把 `organic` 縮成只排除匯率。集團 2026 上半年業績的腳註 5 定義為固定匯率並排除合併範圍變動。建議把兩句改成「按公司有機成長口徑」，同時保留 2026 **實際歐元營收年增 2.2%** 與 **有機成長 6.2%** 的區別。[2026 官方半年業績，第 9、11 頁](https://dieterengroup.imgix.net/press-releases/20260909_Press-release_H1-2026-results_EN_FV-with-appendix.pdf)。
2. **來源表漏綁 §10 的銷售數字**：2010 約 €53m、2013 約 €87m 能在[D’Ieteren 2017 投資人簡報第 25 張](https://dieterengroup.imgix.net/documents/presentations/moleskine_lorenzo_viglione.pdf)核對，但 `source-matrix.md` 的 S6 僅定位投影片 10、14–16，沒有列這兩個數字及其頁碼。修稿後若保留這組比較，將它們加入 S6 或新增一列；若時長需刪，這兩個數字可以整組移除。
3. **2016 年底持股來源，§14**：95.5% 可由[集團 2016 年原始年報](https://dieterengroup.imgix.net/annual-reports/rapport_en.pdf)的交易時間線核實，現有 S9 只連 2017-01-24 的 100% 完成公告。將 2016 年原件補進 S9，或為縮時刪去「年底超過九成五」，直接從 2016 簽約過渡到 2017 年 1 月完成。[2017 完成公告](https://dieterengroup.imgix.net/press-releases/2017_01_24_Moleskine_squeeze_out_EN.pdf)明說連同庫藏股持有全部股份並下市。
4. **時長與分鏡重新對帳**：`shot-plan.md` 的 9:15、83 張插畫／11 卡是事前容量，不是 20 段草稿的實測時長。草稿約 2,800 個漢字，含數字展開後很可能超過約十分鐘目標；正式句級切分及 TTS 前須先精簡、再按實際旁白重排鏡頭與 US$25 全片估價。不能把預算表的 83 張或 9:15 當成已驗收結果。

## 逐項來源判定

| 範圍 | 判定 | 原件對照與限制 |
| --- | --- | --- |
| S1–S4；§§02–06 | **通過，有歸屬限制** | [2013 招股書印刷頁 121–122、138–139](https://www.borsaitaliana.it/prospetti-informativi/1513pros_1_it.pdf)記錄 1995 由 Modo&Modo 重啟生產、1997-11-26 首次註冊商標、「尚待寫成的書」定位及優先選書店。這些是發行人描述的起源／策略，沒有證明每位買家的動機。[品牌倫理文件](https://www.moleskine.com/en-no/code-of-ethics.html)明列 1997 年品牌和 2007-01-01 以 Moleskine 為持有商標權公司名；舊式筆記本不等於 1997 年後商品。 |
| S2；§02 | **通過，維持歸屬** | [品牌 Heritage](https://www.moleskine.com/en-hk/the-world-of-moleskine/our-heritage/)以 Chatwin 的《The Songlines》轉述 1986 年圖爾製造者關閉與買剩餘本子的故事。草稿已明說是品牌轉述，並未把工廠身分或店主話語寫成獨立檔案事實。繪圖只可示意讀書／購本，不重建特定實景與真人。 |
| S5；§§08–09 | **通過，法人勿混淆** | [招股書印刷頁 121–122、357–358](https://www.borsaitaliana.it/prospetti-informativi/1513pros_1_it.pdf)記錄 2006 年秋 Modo&Modo 由 Appunti／Syntegra 相關方收購及其後公司重整；[2016 收購公告第 1 頁](https://dieterengroup.imgix.net/press-releases/DIeteren-Moleskine_-ENG_FINAL.pdf)簡述 2007 公司名稱。2013 上市發行人的法人沿革另始於 2010，旁白的「名字」說法尚未誤稱同一法人從 1995 不變。 |
| S6；§§07、10、12 | **部分通過，補頁碼** | [2017 投資人簡報第 15 張](https://dieterengroup.imgix.net/documents/presentations/moleskine_lorenzo_viglione.pdf)支援批發據點約 12k／20k／29k、2016 年 78 間直接營運店及電商 37 國；`doors` 不是 29,000 間自營店。第 25 張支援 §10 的 2010 €53.4m、2013 €87.0m 銷售，但來源表漏列。投資人簡報的前瞻目標不得當已發生業績。 |
| S7；§§01、11 | **通過** | [義大利交易所 2013-04-03 公告](https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2013/moleskine.en.htm)支持 STAR 掛牌和約 €487.6m 市值；旁白正確區分市值與營收／公司收款。 |
| S8–S9；§§13–14 | **通過，但補 95.5% 原件** | [2016-09-22 收購公告](https://dieterengroup.imgix.net/press-releases/DIeteren-Moleskine_-ENG_FINAL.pdf)只寫簽約收購 41%、約 €506m 全公司股權估值和餘股要約計畫；[2017-01-24 完成公告](https://dieterengroup.imgix.net/press-releases/2017_01_24_Moleskine_squeeze_out_EN.pdf)才證實 100%／下市。稿件沒有將簽約錯說成完成；§14 年底 95.5% 需補 2016 年報來源。 |
| S10；§§15–16 | **通過，限定 2017** | [D’Ieteren 2017 活動報告印刷頁 44–45](https://dieterengroup.imgix.net/annual-reports/3_moleskine_en.pdf)確認紙本占當年銷售 81%、非紙本 19%、智慧筆及電商平台遷移；[2017 全報](https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf)明說直營零售當年虧損。不能外推到 2026 每一家店。 |
| S11–S12；§§17–18 | **通過，限定 FY2025** | [2025 全年結果第 10、42 頁](https://dieterengroup.imgix.net/press-releases/20260310_FY-2025-Results_EN_FV.pdf)支持 €117.8m 對 €122.3m、年減 3.7%，批發尤其美國大客戶控庫存，其他通路有機成長，以及品牌無形資產減損 €107.4m／稅後 €77.4m。減損基於未來現金流估算，非同額現金流出或退貨；有機口徑文字仍須修。 |
| S13；§19 | **通過，限定 H1 2026** | [2026 半年結果第 2、9 頁](https://dieterengroup.imgix.net/press-releases/20260909_Press-release_H1-2026-results_EN_FV-with-appendix.pdf)支持半年銷售 €52.2m、實際年增 2.2%、有機 +6.2%、零售表現良好、美國批發回升、營業結果 €0.7m 略降、調整後集團應占稅前虧損 €4.7m。後者改善主要是 €76.4m 集團內股東貸款減免帶來較低財務費用，不能寫成營業利潤回升。草稿保留了這條界線。 |

## 敘事與安全刪減建議

現稿沿同一本空白本，按起源、命名、書店與批發、資本擴張、收購、2025／2026 財報走，開頭三個疑問有後段回收。敘事方向成立，但每段常重述前一段的限制，造成時長超目標，讀者在後半段容易只記得數字。縮稿時先保住 §02 品牌轉述、§03–04 的 1995／1997 分界、§05–07 的「待寫的書→書店→批發」、§13–14 的「簽約→完成」、§17–19 的「2025 減損→2026 局部回升」；刪去重複的反例與第二次定義。

- §§03–04：「舊顧客／舊時代藝術家不能背書」講一次即可；保留 1995、1997 精確先後及章末問題。
- §§05–06：「不是全部買家都因故事而買／沒有買下作家歷史／不是普通辦公紙」可合併一兩句，保留「待寫的書」與書店通路的因果。
- §§08–09：2006 投資方和 2007 公司名保留，刪第二次「不是從梵谷時代一直傳承」說明。
- §§10–12：保留 2013 掛牌市值，2010／2013 銷售比較及通路 78／37／29k 可擇一組做數字卡；必須區分批發與自營。每增加一組數字都要留足讓觀眾消化的時間。
- §§15–16：保留 2017 紙本 81% 和直營當年虧損，其餘產品清單與組織投資可壓縮。
- §§17–19：保留 2025 年減損是帳面評價及 2026 上半年回升、營業利潤未回升；三種財務數字不必全進旁白，可分流字卡和描述欄。

此輪**未**驗算句級 `video.json` 與素材提示詞，未做盲評、配音時長或站主審核。修稿後先重算正文分鐘數、每 30–45 秒鉤子及至少八個真實回收的 `loops`，再重排逐鏡表並進行第二輪獨立審查。
