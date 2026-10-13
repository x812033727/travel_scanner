---
id: 2026-10-13-resolve-46-review-and-24-redraft
title: Resolve 46 review and 24 redraft hourly news backlog
status: in-progress
priority: P1
area: ops
owner: codex-news-hourly-backlog
claimed_at: 2026-10-13T05:49:41Z
created_at: 2026-10-13T05:49:35Z
completed_at:
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - docs/news-hourly-backlog-2026-10-13.md
---

# Resolve 46 review and 24 redraft hourly news backlog

## Why

正式站 AI 每小時新聞在 2026-10-13 13:46（Asia/Taipei）有 46 筆待審查、24 筆需重寫／失敗；來源漂移、查證與翻譯錯誤、舊稿重複及 provider 故障混在同一佇列。站主明確授權處理這 70 筆，也要求沿用既有 draft PR #1480。逐篇判斷及稽核證據記在 [`docs/news-hourly-backlog-2026-10-13.md`](../../docs/news-hourly-backlog-2026-10-13.md)。

## Definition of done

- [ ] 70 個基線候選各有可核實的終態（發布／退件）或明確的原因、持有人與可執行的後續票；沒有把新候選、未完成 judge、待查來源或舊 worktree 狀態混算。
- [ ] 發布的每篇經候選／run／稽核及公開語系讀回；保留審查與 redraft 不靠整批 retry 或無旗標 backfill 跳過關卡。
- [ ] 本名冊與既有 draft PR #1480 同步，票在 PR 內完成；未經站主同意不把 draft PR 合併／部署當作任務完成。

## Steps

- [x] 固定 2026-10-13 13:46 的 46／24 基線及 70 個候選 ID，區分 `manual_review`／`shadow_review`、`needs_redraft`／`failed` 與來源障礙。
- [x] 人工退件十個有明確重複／過時／證據不足原因的候選：Sonnet 5.5、Morning Minute／Drake、XRP Ledger 延期、Ledger／CryptoBilis、Google Vids、Gemini coworker agent、OpenAI／澳洲舊稿，以及 Evernorth、Pleterski、澳洲聽證三筆舊預告；逐筆讀回候選及稽核。
- [x] 修 Drake `b0825fb1…` 與 XRP Ledger `5186a9c9…` 的指定三語錯句／表格；各送一次重新查核，後台已發布清單讀回，公開頁讀回範圍見名冊。
- [x] Falcon ASR `6384736e…` 五語各補官方來源表格並送一次重新查核；後台已發布，四語公開表格讀回，ja 429 待補驗。
- [x] Kalshi `cf07bd04…` 五語修正過度陳述並重查；目前回到待審，卡 CoinDesk 正文／作者頁差異及不可讀的 `/markets` 導覽頁。
- [x] Flock `7bea807c…` 五語補當事公司回應並重新查核；候選已發布，五語公開 H1／公司回應讀回。
- [x] NVIDIA Astra `e69d8fbc…` 唯一官方來源刷新、繁中標點修正，候選已發布，五語公開 H1／8 倍主張讀回。
- [x] Citrix `dcc3116c…` 日文指定錯句已修、單篇重查並刷新唯一 Google Cloud 正文；新事實、五語及 Jev 審查通過，候選已發布，五語 H1／規則包名／DTLS／UDP 443 讀回。EvoLib `c5912455…` 同一 Microsoft 正文刷新後仍反覆顯示來源變更，不盲目重送。
- [x] AEMA `e0e959d9…` 核唯一 NVIDIA 官方正文與既刊 DSX 不重複，留稽核原因後單次刷新來源；候選已發布，四語公開 H1 讀回、ko 429 待補驗。
- [x] Google Genesis `6cbc274d…` 的 7 月舊公告與 Project Suncatcher `f8830a55…` 的同日已刊發射／來源數字更正，逐筆以具體理由退件並在「已退件」清單讀回；固定基線此時 7 發布、12 退件、51 尚待終態。
- [x] EvoLib `c5912455…` 本地用原生解析器重現 `msr-promo` 推廣卡輪替造成假正文漂移，精確排除後兩次 body hash 穩定；交既有動態 widget 修復票，不再盲刷來源。
- [x] Meta Connect 直播稿 `89156804…` 與同批固定總覽高度重複，且混入導覽／作者頁及未通過事實查核；填具體稽核原因退件、讀回「已退件」。固定總覽候選仍須補官方一手證據及修五語。
- [x] Anthropic ART `2cb24617…` 五語 FAQ／提示框去除超出 9/23 一手來源的現在式斷言，各存草稿並單篇重新查核；後台讀回 AI 代審「發布」與候選已發布，Guide 韓文已發版本 6、五語公開 H1／開頭／重點摘要讀回。
- [x] Apollo 存款推論 `d266ad56…` 查出 1 萬美元按 3.3%–5% 年息應是 330–500 美元，唯一來源及五語稿卻都寫 100 美元；Orchard `77a835d1…` 為 8/03 舊公告、Decrypt 監管回顧 `2c3e35f7…` 為 9/26 舊分析且後有 10/05 CFTC ANPRM。三筆各留稽核理由退件並讀回。
- [x] CLARITY／SEC 豁免 `7fa0b6b6…`、Google Playground `a5ad16d0…`、Manus 融資 `0f23dbf9…`、MetaMask／Lido `1f2dd889…` 各核本站既刊同事件稿後退件；SEC 回購 FAQ `511b2671…` 另因 9/28 官方加入「沒有中心方」條件、原稿漏寫而退件。五筆各讀回候選終態，不使用付費 retry。
- [x] Falcon ja、AEMA ko 公開頁初次 429 後重試成功，H1、關鍵數據／摘要讀回；Anthropic ART 後台「執行紀錄」末段可見驗證、四語審查及 judge-final 的成功階段，但 UI 未提供 run ID。
- [x] CoinDesk／CFTC `e25bc5a4…` 與保留的 10/05 第一方 ANPRM 候選重複；RockawayX `e16c3ba7…` 五語把既有 1.5 億美元以上資金載具與 2030 年預測寫錯。兩筆分別填稽核原因退件，讀回候選及全站 961／962 計數。
- [x] RedotPay `dbda9f17…` 五語說法對照 CoinDesk 與公司一手公告，留稽核原因後單篇刷新來源；新一輪驗證、四語審查及 Jev 通過，候選已發布、五語 Guide 均為已發第 3 版，五語公開 H1／審計與上市時態重點讀回。英文／日文初次 429 後限速重試成功。
- [x] Haiku 5.5 `92c7561b…` 與 Solana Alpenglow `b9c07491…` 查明各只有兩語草稿、其餘三語缺件，前者錯歸 CRYPTO 且免責段重插、後者舊 9/28 時程與 150ms 指標錯；兩篇都非既刊同題重複，保留待分類／來源／內容修復，不付費盲重跑。
- [x] CoinDesk 10/01 資安統計 `ab3d418f…` 以舊 Q3／9 月數字作五語主軸，對照 CertiK 10/13 官方看板已修訂；填來源／數值／時效原因退件，候選及 963 退件計數讀回。
- [x] Deus X Capital `063d6bdb…` 對照公司首頁 CEO 第一方聲明，五語舊稿混用關閉時態、四語把 `formally unwind` 強化為「清算」；留具體稽核理由退件，後台成功提示及 964 退件計數讀回。
- [x] OpenAI 數學 `62a29197…` 同 10/06 既刊手稿事件，五語稿把官方 42% 已形式化顛倒且誤寫 10 份推理摘要；留具體原因退件，後台成功提示及 965 退件計數讀回。10/06 既刊五語已在獨立任務更正並發布，後台版本、五筆稽核與公開頁讀回；10/07 另篇同題既刊稿亦在獨立任務完成五語更正、發布及公開讀回。
- [x] GitHub 開發者政策 `a540117f…` 的五語舊稿仍說 SB 1000 等待 9/30 簽署，州長官網已證實簽署；以日期錯誤及未過獨立查核填原因退件，稽核與 966 退件計數讀回。
- [x] CoinDesk／OpenAI／Google 安全協議 `d3c18ec1…` 與本站已刊五語同事件稿重複；公開繁中全文及唯讀資料庫版本核對後，以具體原因退件，稽核與 967 退件計數讀回，未再次付費重寫。Ethereum 2030 五語檢查過，但需加 Vitalik 一手來源後重審。
- [x] NEAR Intents `4410c38a…` 的 CoinDesk 原文 10/02 補上營運方所稱全部資產返還，五語舊稿仍停在約 380 萬美元遭竊／待補償；以時序錯誤退件，稽核與 968 退件計數讀回。
- [x] CoinDesk 量子安全 Bitcoin 成本 `e4e8e98a…` 與本站 Decrypt 已刊 StarkWare 競賽專文同事件，舊稿 $66 非獨立新發展；人工以已刊重複退件，成功提示、最新稽核與全站 969 計數讀回。
- [x] MoonPay／North Capital `5fcf6a8f…` 的第一方公告僅說簽約且待核准，CoinDesk 匿名消息是「超過」6,000 萬美元；繁中舊稿寫成確定 6,000 萬並漏第一手聲明，證據另混入導覽／作者頁。填明確原因退件，成功提示、稽核與全站 970 計數讀回。
- [x] Samsung Wallet／USDC `9c44b4b5…` 與 10/08 既刊五語稿同事件；一手公告的銀行費用與託管細節未正確寫入候選或既刊。重複候選以具體原因退件、最新稽核與全站 971 計數讀回；既刊五語已在獨立任務發布 v6，已發版本、稽核及公開頁讀回；見 `tasks/done/2026-10-13-correct-published-samsung-wallet-usdc-guide.md`。
- [x] 白宮顧問／CLARITY Act `9ffcd1c1…` 舊稿將參院 9/15 程序表決誤寫成法案最終遭否決，且歷史人工曾記錄站主要求來源不足稿退件；以參院紀錄、單一實質來源及五語錯誤為由退件，成功提示及全站 972 計數讀回。
- [x] Meta Muse Charm `2cba0531…` 與本站 9/24 既刊稿為同場同事件，Jolly 形象非獨立公告；填既刊 URL 與差異退件，成功提示及全站 973 計數讀回。Visa 調查候選另完成一手來源比對，保留待人口外推與修稿鏈修復。
- [x] 海外美元穩定幣 `c8248683…` 9/23 匿名構想無本次新進度，舊數值缺時點，人工以失時效退件並讀回 974；OpenAI 辦公套件 `7027afef…` 與本站已刊 DevDay Space／Pages 專文重疊，五語把尚未上線的 Slides 寫成可用，人工退件並讀回 975。Visa 調查稿仍保留待修。
- [x] Meta Audio `ddf85a1f…` 與本站 9/23 已刊眼鏡陣容稿同事件，候選仍卡事實查核及舊單一來源退件紀錄；人工填既刊 URL 與差異退件，成功提示／稽核／976 計數讀回。EvoLib `c5912455…` 唯一來源 7/30，五語無十月新事件；人工以 75 天失時效退件，成功提示／稽核／977 計數讀回，動態 widget 修復票仍有效。
- [x] Bernie／超級智慧 `0c72c4f4…` 9/23 舊提案稿含無據「20 國」與導覽頁證據；代幣化股票聯盟 `d9deb48d…` 9/24 非約束性工作組稿把參與效益寫得過確定並有日／韓誤譯。各填具體時效／事實原因退件，成功提示、最新稽核及全站 978／979 計數讀回。舊兩篇 Verge 票須按 Bernie 終態更新，不能再重開原稿。
- [x] Franklin Templeton／Bybit `842bf9c7…` 9/28 舊稿把機構限定、FOBXX 總資產及託管性質寫錯；CFTC 9/24 FAQ `4e323ee2…` 舊稿省略非拘束力及 Q12–15 條件，原生來源仍抓取失敗。各填具體原因退件，成功提示、最新稽核及全站 980／981 計數讀回；10/05 ANPRM 另有 10/13 正式刊載，保留修稿。
- [x] THORChain／Bitget `f4602147…` 9/28 五語即時稿仍稱資金持續兌換、入侵細節未公開；Bitget 9/30 調查公告／10/02 服務恢復與 THORChain 10/06 月報均屬後續實質資訊。人工以時序與錯句退件，成功提示、最新稽核及全站 982 計數讀回；不刷舊稿另發。
- [x] Meta Connect 固定總覽 `2ba410eb…` 仍是 9/23 發表會舊稿；候選證據混入動態 `/tech`、作者頁與無關舊文，同場 Muse Charm 已刊、直播候選已退。對照 Meta 官方 9/24 整理後以具體時效與證據原因退件，後台成功提示、重載候選終態與 983 退件計數讀回。固定名冊目前 9 發布、44 退件、17 未有終態；全站第十筆 redraft 是新進 Manus／OPPO，不在固定名冊。
- [ ] 補已發稿的終態 run、稽核、已發版本及尚缺的公開全文證據；釐清 Kalshi 導覽頁障礙。EvoLib 動態元件修復票對其他候選仍有效，本候選因失時效已退件。
- [ ] 分批處理剩餘的明確翻譯／事實問題、來源變更與固定基線尚存 9 筆 redraft／failed，將每次人工決定及其讀回更新名冊。
- [ ] 對無法安全完成的來源抓取、provider 未知結果或程式障礙建立精確後續票並標出持有人，再核對最新佇列與基線 70 筆逐一結案。

## How to verify

在正式站 `/zh-TW/admin/news` 依名冊候選 ID 開詳情，核候選狀態、原因、人工決定及 run 結果；對發布候選從詳情逐一開五語前台連結，核 H1、修正句與 Guide 版本。用當次查到的正式站數字和固定 70 ID 名冊比較，不從計數差推導逐筆成果。本地 `npm run check:tasks` 驗票格式；PR #1480 的 CI／merge／deploy 狀態需另外讀回。

## Notes

此票僅 claim `docs/news-hourly-backlog-2026-10-13.md` 的 repo 內容範圍；舊 worktree／舊票仍由他人持有，不動它們。此工作會話較早的正式站 SSH `plink` 呼叫被自動審核阻擋，未改用其他通道重送；後續協作審查者以獲允許的單次唯讀 SQL 核對安全協議既刊稿，另以後台 UI 讀回退件。「重新查核」是非終態，Anthropic 已另作終態讀回。`retry` 可能重起付費撰稿並清掉人工決定；French OAuth 失敗的實際付費結果未明，先核 run／RQ／供應商收據。2026-10-13 17:50 的全站 UI 為待審 8、需重寫 10、已發布 605、已退件 983；佇列流動，且多出 10/13 Manus／OPPO 新候選，不能直接用差額結案。固定 70 ID 名冊是 9 發布、44 退件、17 未有終態。名冊逐項寫了來源 URL 導覽頁、CFTC 官方 HTTP、翻譯失敗、重複及 AI judge handback 的不同處理方案。
