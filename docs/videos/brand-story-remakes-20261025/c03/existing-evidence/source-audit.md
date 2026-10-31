# C03 Moleskine：來源與新規則稽核

稽核日：2026-10-25。稽核者：`/root/find_rules`；來源協查：`/root/find_rules/c09_delta`。範圍限唯讀既有資料與原件，唯一新增筆記為本檔。未讀盲讀報告、未編修作者稿、未操作後台、未呼叫產線的付費或模型API。本檔是新稿的來源指引與風險清單，**不是新 C03 劇本的來源 PASS**；新稿須凍結後逐句獨立查核。

## 結論

既有 C03 已做到舊規格上架包，並沒有完成 10/25 新規則重製。現有一手資料足以支持約 3,500 spokenUnits 的有效重寫：沿同一本黑色空白本，從文化定位、書店與批發的選擇，走到直營營運成本、資本市場估值，再讓 2025/2026 的通路與財務結果檢驗最初承諾。應補來源裡的具體機制與選擇，不靠名人軼事、股權日期清單、會計定義或章首重述湊時長。

本輪直接重開招股書找到一項應比舊稿更精確的用詞：**1997-11-26 是專門商標章節明載的首次申請日，不宜寫成當日完成註冊**。如精確到日，說「首次申請 Moleskine 商標」；若日子不推進故事，可只說現代品牌於 1997 年成形。舊資料與舊簽收不回改，這項精確性留在新稿。

## 版本與既有成果

檢查的主 checkout 為 `/workspace/work/brand-remakes-source`，對照 `/workspace/travel_scanner_ai_news`。以下五檔在兩份 checkout **逐 bytes 相同**；`/workspace/travel_scanner` 沒有這個 C03 目錄。在已存在 Git refs 中，C03 最近改動是 `16b0a27dd`（10/25 上架包收據）、`11e23a876`（上架就緒與解除舊片保留）、`6f9aec8d1`（C01–C20 企劃整併），沒有另一份 10/25 C03 新規則旁白。

| 舊片檔案（`docs/videos/story-everyday-moleskine-c03/`） | SHA-256 |
| --- | --- |
| video.json | `3b12bff0ab09a5827330c25121048912fefee014ec9134df582cff511a755109` |
| script.md | `5f148061a2fa4bb89a42b1d91adfa67a6bad4796ee5a44b82f1eea473722cb46` |
| source-matrix.md | `7d6f3147f73f861e80eb3b56a6d09999866c9067d1e6839e0ef3cc80f140eabb` |
| series.json | `208e2d9761b0159eed174b210dd0e867329b9f8193d6244deb9ffdac22617f0e` |
| reviews/upload-package-20261025.md | `041f3606192796823877a78105da904e6b9c0aa0fd2503e41a6b416d83a368a5` |

上架包收據記錄：94 句、73 張插畫／21 張字卡；純語音開場 31.74 秒、正文 481.02 秒；成片 19,006 格／30 fps = **633.53 秒（10:33.5）**，5 秒 bumper 在開場後 37.87 秒，21 秒 v4 片尾。`upload/final.mp4` 舊收據 SHA 為 `915830a0969b480225c5e4d655794489de29bcfd02cc15ad61a8de24187dc75b`。這些是既有製作收據，**本次沒有取得或重看實際媒體**。

舊票 `tasks/open/2026-10-24-c03-moleskine-finish-to-upload-package.md` 是 `review`，負責人/範圍屬既有上架包工作；本次不動它。舊收據仍列站主看片／上傳／Studio 結束畫面待完成，另有 ASR 近音及 policy 0.59/0.6 註記；不把這些轉寫成新版通過或新版失敗。舊正式後台快照只記 `outline approved`，與本機曾完成 package 是兩個狀態；即時後台由 root 另查。

共享系列 `docs/videos/brand-stories-everyday-reversals-20261020/series.json` 的 `target_minutes` **已是 13**，但 C03 個片 `video.json` 仍是 `[9,11]`；系列設定變更沒有把既有稿自動變成 13 分鐘。`episodes/C03.json` 仍保留舊三預告與舊精確註冊說法，不能當作新稿模板。另有百集題庫的 C03 是開源維護者；只用完整 Moleskine slug 辨識。

## 新規則差距

已讀本地 `AGENTS.md`、`.agents/skills/brand-story/SKILL.md`、`youtube-video/references/story.md` 與 `script-writing.md` 相關段落。以 `docs/videos/channel-review-20261025-story-series/README.md`「站主 2026-10-25 的決定」及 skill 的 10/25 專節為現行決策；同份文件內較早的約 10 分鐘／不燒字幕／三四個預告／舊縮圖說明是歷史。

| 項目 | 舊 C03 實檔 | 新稿所需 |
| --- | --- | --- |
| 時長 | target `[9,11]`；實片 10:33.5 | 目標 13，按本次要求實測 12–14；不能以舊片音檔達標代替 |
| 有效內容 | repo `spokenUnits()` 實算全稿 **2,160**、開場 135、正文 **2,025** | 約 3,500；現有稿差約 1,340 units，須補有來源的新推進 |
| 開場 | 空白本／掛牌場景；三個預告是作家、收購、品牌價值重算 | 觀眾利害＋相關最大數字→具體場景→最多兩預告→題目/規模承諾→中心問句；數字不能錯當現金或銷售 |
| 說給一人聽 | 六章全片只有 **1 個「你」與 0 個「我」**；前五章兩者皆零 | 每章觀眾對話與明示旁白反應；不可編親身經驗 |
| 文字重述 | 舊稿有批發機制、命名與下一本等重提 | 與原來源相符的真回呼／新選擇；刪換字重述與旁支，勿只增加問句 |
| 圖像 | exact cute-mystery；73/94 插畫，約 77.7%；最長連卡 2（舊收據） | 可沿用概念規則與經驗；新逐景配鏡須重新核旁白對應。約 105 張是規劃量，不是硬湊張數 |
| 旁白聲音 | 舊 voice.style 無一秒四到五字；實際音檔未重聽 | 新說書語速 4–5 字/秒、不拖句；實際 TTS 決定時長 |
| 字幕 | `burn_in:false` | 繁中燒錄；其他語言 CC |
| 縮圖 | 舊 headline「新品牌／老故事？」、無 sub，shot 為離店背影 | bold d、黃字黑邊大標、白字副標≤12字，選有表情或物件本身；不得假稱舊縮圖已按新規則重製 |
| 片頭片尾/結尾 | 舊收據有開場後 5 秒＋21 秒 v4；末段答案、留言、訂閱 | 版式可續用；新時間軸/成片再驗，旁白不講下一支 |

程式另有值得 root 在實長驗收時留意的落差：當前 `story.mjs` `composeStory` 對 cute/13 寫 `[12,14]`，但 `lengthBand(13,cute)` 仍落一般 −90/+150 秒，即 **11:30–15:30**。文件說 12–14，不代表舊 worker 的 TTS 門檻已同樣收緊。本次應自行按實測 12–14 收，不單憑 worker 放行。`STORY_CPM` 的舊估算 250/min 與新說書 4.5/s 也不是同一量測；不得用 estimates 冒作實際時長。

## 精確已知來源與可說範圍

原作者來源矩陣的 S1–S13 是最完整索引；其中大部分是 PDF、超過工人可靠擷取範圍，保持 `reviewer_only`，並為新稿逐行附具體頁段。下表是可核的主張範圍，沒有把公司自述升成獨立歷史判定。

| 索引 | 原件／定位 | 可用與必守界線 |
| --- | --- | --- |
| S1、S4、S5 | [2013 上市招股書](https://www.borsaitaliana.it/prospetti-informativi/1513pros_1_it.pdf)：印刷121–122／138–139歷史；印刷137–138定位/書店；印刷163–165通路；印刷258商標 | 1995 重啟舊型制產品、品牌/法人時間分開；「待寫的書」、優先書店、直/間接通路與當時契約風險。發行人自述；不證每個顧客因故事購買，不證直接造成全部成長。精確申請日見下節。 |
| S2 | [Our Heritage](https://www.moleskine.com/en-hk/the-world-of-moleskine/our-heritage/)，A Creative History；已整併企劃另用[官方法文頁](https://www.moleskine.com/fr-ch/le-monde-de-moleskine/notre-histoire/) | 官網轉述 Chatwin／《歌之版圖》與圖爾1986停業；未取得同期工廠/店鋪檔案。不能具體重建店主對話或保證那就是現代品牌供應鏈。 |
| S3 | [Code of Ethics](https://www.moleskine.com/en-no/code-of-ethics.html)，§1 Purpose and Scope | 1997品牌與2007-01-01公司名稱分開；歷史藝術家與舊類型是品牌回顧，非使用過現代商標商品、非真人背書。 |
| S6 | [2017-12-13 投資人日簡報](https://dieterengroup.imgix.net/documents/presentations/moleskine_lorenzo_viglione.pdf)，投影片11、15–16；[2016活動報告](https://dieterengroup.imgix.net/annual-reports/3_moleskine.pdf)，印刷35、37；[2017年報](https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf)，印刷7 | 約1.2萬/2萬/2.9萬是批發 doors，不是自營店或全書店。**2016年底直營採年報79家**；簡報78的衝突保留，不刪歷史紀錄。 |
| S7 | [交易所2013-04-03上市新聞稿](https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2013/moleskine.en.htm) | STAR掛牌與上市時市值約€487.6m（口播約4.88億）；不是公司收入、募入現金或淨利。 |
| S8 | [D’Ieteren 2016-09-22收購公告](https://dieterengroup.imgix.net/press-releases/DIeteren-Moleskine_-ENG_FINAL.pdf)，頁1–2 | 簽約41%、每股€2.40、整體**股權**估值約€506m及擬收餘股。不是當日已100%，不是企業價值EV或公司進帳。高端定位/委外生產/成本管理是買方給的獲利解釋。 |
| S9 | [2017-01-24收購完成公告](https://dieterengroup.imgix.net/press-releases/2017_01_24_Moleskine_squeeze_out_EN.pdf) | 完成餘股強制收購，連庫藏股達全部股份，同日撤牌；不可挪到2016/9。 |
| S10 | [2017 Activity Report — Moleskine](https://dieterengroup.imgix.net/annual-reports/3_moleskine_en.pdf)，印刷42–45、50–51；[2017年報](https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf) | 2017紙本81%/非紙本19%是**當年銷售額比重**；零售營運壓力/虧損、電商遷移影響都限當年。推出智慧筆不等於數位轉型成功。 |
| S11、S12 | [2025全年業績（2026-03-10發布）](https://dieterengroup.imgix.net/press-releases/20260310_FY-2025-Results_EN_FV.pdf)，頁9–10、23–25；減損另見2、39、41–42、55–56 | 2025銷售€117.8m、同比−3.7%；公司指批發、尤其美國大客戶謹慎控庫存，其餘通路有機成長。品牌無形資產減損約€107.4m不是同額現金流出/本子退貨；稅後影響€77.4m不可混。不是上市後連年衰退的證明。 |
| S13 | [2026-09-09半年業績PDF](https://dieterengroup.imgix.net/press-releases/20260909_Press-release_H1-2026-results_EN_FV-with-appendix.pdf)，頁1–2、9、11、16；[發布頁](https://www.dieterengroup.com/press-releases/dieteren-group-half-year-2026-results) | H1銷售€52.2m、同比+2.2%；有機+6.2%與匯率−4.0%分開，口徑排除匯率及合併範圍變動。營業結果微降，稅前虧損縮小與財務費用/部分股東貸款減免有關；不能說全面復甦、整筆債務免除或營業利潤回升。半年只比同半年。 |

### 本輪直接核到的招股書用詞與可擴寫段落

協查以原 PDF bytes 核：4,571,857 bytes、773頁，SHA-256 `bf33730ab8fae0290e95c65ac1e70e734fdeb5061f99e96154f8071772e774fe`。頁碼下列以 PDF 實體頁（1-based）／印刷頁並列。

- **PDF260／印刷258，§11.2**：`Il primo deposito del marchio “Moleskine” è stato effettuato in Italia il 26 novembre 1997`。`deposito` 是首次申請/送件；後文還區分核准與 pending。歷史段 `registrando` 不足以把精確日升格為完成註冊。品牌名/用詞也非1997才被首次發明。
- **PDF139／印刷137**：「待寫的書」定位，可講物件沒內容但顧客可能成為作者；必標這是發行人的策略，不能拿來替買家動機下定論。
- **PDF140／印刷138**：書店優先通路，足以把「為何不是只放文具架」變成主角的一次選擇；不能把這個選擇寫成已證明的唯一成功原因。
- **PDF165–167／印刷163–165**：直/間接通路互補、寄售/非寄售安排與風險移轉。能用一箱貨到誰手裡、誰負責存貨/補貨的具體動作講機制；須保留原契約/期間，不能套到2025某美國客戶或杜撰退貨事故。

## 對 13 分鐘有效內容的建議

可用一條「這本空白本如何讓下一個人願意買」主線，不必把全部13個來源都念成一排。

1. 舊型制被出版社接住：文化故事如何提供辨識，1995產品／1997現代品牌與歷史人物分開。補的是決定與限制，不新增名人現場。
2. 走進書店：用招股書的「待寫的書」與書店選擇，具體說明公司怎樣安排商品被看見。旁白反應可連到觀眾買筆記本的經驗，但不是偽造顧客訪談。
3. 換成更多貨架：批發能觸及別人的店、直營可控制展示卻需自己營運；用招股書/2017原件補有意義的機制，而非重念「通路很重要」。
4. 公司被標價：市值、股份交易與品牌資產是不同觀察；只在這本本子的旅程需要時解釋，不連開三段會計課。
5. 2025與2026檢驗：美國批發客戶少補貨影響公司sell-in，不能單憑此判消費者sell-through；新半年銷售回升但營業結果未升，少付融資費用能縮虧卻不是經營毛利自動變好。這是新的矛盾與選擇，不是「有故事卻騙人」的指控。

約3,500 units只是起稿預算。可先把增量分到書店定位、批發/直營具體安排、資本/存貨風險三處；新稿實際逐句來源不足就刪，不拿泛論或同一句反覆說填額。13分鐘要靠新TTS與成片實測12–14，所有新句/新配鏡另綁SHA重審；舊圖評、舊盲讀和舊站主核准只保留歷史用途。

## 本輪財務原件覆讀補充

協查本輪重新開啟上述核心原件均 HTTP 200；H1 2026 PDF 為 5,511,707 bytes，和招股書一樣仍須 `reviewer_only`。下列是可供作者直接追原件的有效擴寫定位，不代替新稿句級簽收：

- **2017投資人日簡報PDF11**：`Priority to covering the territory through wholesale distribution`。PDF22–25談接近顧客、改善據點生產力、建立零售網；2016分銷改善被零售低於預期和品類組合部分抵銷。PDF27另有整合一次性成本、美國零售環境及管理變動；PDF28的目標與29的前瞻聲明不可寫成已完成。
- **2017活動分冊印刷44–45／PDF5–6**：門市網絡、營運/體驗優化、平台移轉伴隨電商下降、紙本占銷售81%。**2017全報財務印刷7／PDF65**：`higher weight of the loss-making Retail channel`，同頁有人員、IT/SAP與策略成本；不可推每一家店皆虧，亦不可直接歸因2025減損。
- **FY2025 PDF10、42**：美國部分大客戶控庫存與當年銷售；品牌無形資產減損€107.4m，稅後€77.4m。不同會計欄位分開，不把這些當作退款、產品退貨或現金流出。
- **H1 2026 PDF9、11、21**：減免€76.4m股東貸款後，仍有€186.8m集團內融資。財務費用減少與調整後稅前虧損縮小可相連；不可說整筆債清償、營業利潤回升或全年已復甦。

已有舊輪糾正另包括：有機成長口徑、1995「尚無品牌」的過度推論、缺乏綁定而刪去的2010/2013收入與2016年底95.5%持股、股東貸款僅減免部分本金、78→79家。新作者若翻用舊稿片段，不能把已刪或舊版PASS的數字無條件加回。

已將來源頁碼/原句傳給新作者 `/root/remake_c03`（此前作者服務失敗而未寫C03）；傳遞來源指引不構成作者自核。後續新稿由本來源審查者在凍結SHA後獨立查核。

### S1 產品型制與委外原件追加定位

- **PDF123／印刷121**，亦見PDF139／印刷137：黑硬封面、圓角、鬆緊帶、內袋。這是舊型制/現代產品辨識，不構成法國工坊傳承證據。
- **PDF159／印刷157**：`L’attività di produzione in senso stretto è affidata ad una rete di fornitori esterni`（實際生產交給外部供應商網）。同頁Operations掌握流程、品質、供應商控制，並按月作滾動12月需求計畫；**PDF160／印刷158**接歷史銷售、庫存及交期。製造地與比例數字限原件2011期間，不可推為2025或今日現況。
- 同一委外句也見 **PDF543／印刷541，§22.3.1**。委外模式已有S1直接證據，不必只靠S8買方解釋；仍不得推出每本手工、義大利自有本廠或法國工坊延續。概念插圖若展示供貨/品管，要避免畫成發行人親自操作其自有工廠。

上述原件追加定位已直接傳 `/root/remake_c03`；獨立來源審查者未讀作者新稿。
