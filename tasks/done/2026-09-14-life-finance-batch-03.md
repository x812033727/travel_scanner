---
id: 2026-09-14-life-finance-batch-03
title: 生活分享財經系列批次 03：保險與風險（20 篇）
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-15T01:02:14Z
created_at: 2026-09-14T11:45:48Z
completed_at: 2026-09-15T15:10:24Z
branch:
depends_on:
  - 2026-09-14-life-finance-series-catalogue
  - 2026-09-14-life-finance-topic
  - 2026-09-14-life-finance-batch-01
scope:
  - apps/api/app/guides/content/insurance-basics-taiwan.json
  - apps/api/app/guides/content/insurance-policy-checkup.json
  - apps/api/app/guides/content/term-vs-whole-life-insurance.json
  - apps/api/app/guides/content/medical-insurance-reimbursement.json
  - apps/api/app/guides/content/hospital-daily-benefit.json
  - apps/api/app/guides/content/accident-insurance-basics.json
  - apps/api/app/guides/content/cancer-insurance-basics.json
  - apps/api/app/guides/content/disability-income-insurance.json
  - apps/api/app/guides/content/long-term-care-insurance.json
  - apps/api/app/guides/content/travel-insurance-basics.json
  - apps/api/app/guides/content/flight-delay-baggage-insurance.json
  - apps/api/app/guides/content/credit-card-travel-insurance.json
  - apps/api/app/guides/content/overseas-medical-claim.json
  - apps/api/app/guides/content/compulsory-auto-insurance.json
  - apps/api/app/guides/content/home-fire-insurance.json
  - apps/api/app/guides/content/insurance-policyholder-beneficiary.json
  - apps/api/app/guides/content/insurance-claim-process.json
  - apps/api/app/guides/content/insurance-surrender-lapse.json
  - apps/api/app/guides/content/online-insurance-purchase.json
  - apps/api/app/guides/content/insurance-sales-questions.json
  - apps/web/public/guides/insurance-basics-taiwan
  - apps/web/public/guides/insurance-policy-checkup
  - apps/web/public/guides/term-vs-whole-life-insurance
  - apps/web/public/guides/medical-insurance-reimbursement
  - apps/web/public/guides/hospital-daily-benefit
  - apps/web/public/guides/accident-insurance-basics
  - apps/web/public/guides/cancer-insurance-basics
  - apps/web/public/guides/disability-income-insurance
  - apps/web/public/guides/long-term-care-insurance
  - apps/web/public/guides/travel-insurance-basics
  - apps/web/public/guides/flight-delay-baggage-insurance
  - apps/web/public/guides/credit-card-travel-insurance
  - apps/web/public/guides/overseas-medical-claim
  - apps/web/public/guides/compulsory-auto-insurance
  - apps/web/public/guides/home-fire-insurance
  - apps/web/public/guides/insurance-policyholder-beneficiary
  - apps/web/public/guides/insurance-claim-process
  - apps/web/public/guides/insurance-surrender-lapse
  - apps/web/public/guides/online-insurance-purchase
  - apps/web/public/guides/insurance-sales-questions
---

# 生活分享財經系列批次 03：保險與風險（20 篇）

## Why

[`docs/life-finance-series.md`](../../docs/life-finance-series.md) 的批次 03。站主要在生活分享專區
做第二個垂直領域（第一個是 AI 工具系列），分六批產出約 120 篇財經文章與教學；這張票是其中一批，
scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

**開工前先讀**總表的「不能寫的東西」與「經驗記錄」，以及批次 01 票的 Outcome。
財經是 Google 的 YMYL 類別，這個系列又包含投資題材，措辭規則和 AI 系列不一樣，不要套用舊經驗。

第 10–13 篇（旅平險、不便險、刷卡附贈旅遊險、海外就醫核退）是旅遊銜接篇。
**保險文最容易踩到「推薦個別保單」**：寫的是險種與條款結構，不是哪張保單好。

## Definition of done

- [x] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg`
      或 Commons 照片）、至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、**兩個 callout（含最後的免責）**、
      sources 每筆有 `checked_on`、至少一個站內 `link`。
- [x] **每篇最後一個區塊是免責 callout**，用 `docs/life-finance-series-brief.md` 第 5 節的模板，查證日是實際日期。
- [x] **人工逐篇確認：沒有推薦任何個股／個別基金／個別 ETF／個別保單／個別銀行方案，
      沒有買賣建議、目標價或報酬預測，沒有把行情數字寫進正文。** 這一項機器檢查不到。
- [x] 合作連結零個——站上沒有金融類內容夥伴，任何帶追蹤參數的網址都會讓整篇被拒。
- [x] 沒有任何金融機構的 logo、字標、圖示或介面截圖；hero 沒有股價曲線或金幣堆；
      照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA。
- [x] 級距、費率、額度、申報時程都在撰稿當天查主管機關或業者官網；查不到的寫「以主管機關公告為準」。
- [x] 站內連結只用指派給的完整網址；旅遊攻略只連總表「可連的旅遊攻略」那張表
      （`taiwan-*` 那幾篇沒有 zh-TW，連過去是壞連結）。
- [x] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；
      `test_guides_content_pack.py` 全綠。

## Steps

這二十篇（slug · 標題 · topics · 圖 · 易變）：

1. `insurance-basics-taiwan` · 保險基本觀念：保險買的是什麼、應該先保什麼 · finance, tutorial · 圖：插
2. `insurance-policy-checkup` · 保單健檢怎麼做：把手上的保單列成一張表 · finance, tutorial · 圖：插
3. `term-vs-whole-life-insurance` · 定期險與終身險：保費結構與各自的適用情境 · finance · 圖：插
4. `medical-insurance-reimbursement` · 實支實付醫療險：收據正副本、限額與常見誤解 · finance, tutorial · 圖：插
5. `hospital-daily-benefit` · 住院日額怎麼看：給付條件與健保病房差額 · finance · 圖：插
6. `accident-insurance-basics` · 意外險：「意外」的定義比你想的窄 · finance · 圖：插
7. `cancer-insurance-basics` · 癌症險與重大傷病：一次金與療程給付的差別 · finance · 圖：插
8. `disability-income-insurance` · 失能扶助險：收入中斷時的保障怎麼看 · finance · 圖：插
9. `long-term-care-insurance` · 長照險怎麼理解：給付門檻與其他替代方案 · finance · 圖：插
10. `travel-insurance-basics` · 旅平險要保什麼：醫療、意外與海外急難救助 · finance, tutorial · 圖：插　· 易變
11. `flight-delay-baggage-insurance` · 不便險：班機延誤與行李延誤怎麼賠、證明怎麼留 · finance, tutorial · 圖：插　· 易變
12. `credit-card-travel-insurance` · 刷卡附贈的旅遊保險：保了什麼、沒保什麼 · finance · 圖：插　· 易變
13. `overseas-medical-claim` · 海外就醫與健保核退：要帶回來的文件與申請時限 · finance, tutorial · 圖：插　· 易變
14. `compulsory-auto-insurance` · 汽機車強制險與任意險：理賠範圍差在哪 · finance · 圖：插　· 易變
15. `home-fire-insurance` · 住宅火險與地震險：房貸綁的那張保單保了什麼 · finance · 圖：插
16. `insurance-policyholder-beneficiary` · 要保人、被保險人、受益人：填錯會怎麼樣 · finance, tutorial · 圖：插
17. `insurance-claim-process` · 理賠申請流程：文件、時限與被拒賠的常見原因 · finance, tutorial · 圖：插
18. `insurance-surrender-lapse` · 解約、停效與復效：繳不出保費時有哪些選項 · finance · 圖：插
19. `online-insurance-purchase` · 網路投保：能買什麼、和臨櫃差在哪 · finance, software · 圖：插　· 易變
20. `insurance-sales-questions` · 聽業務員說明時該問的問題：把口語說法換回條款用語 · finance · 圖：插

- [x] 認領後從總表抄出指派（含可連的完整網址），一篇一個撰稿代理、每波最多七個，
      代理照 `docs/life-finance-series-brief.md` 產出工作區。
- [x] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [x] `guides-pack lint --render-dir` 逐張看圖；**逐篇讀過確認法遵**；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders \
  --catalogue ../../docs/life-finance-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- AI 系列的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。
- AI 系列批次 03 曾經送出 13 個連到不存在文章的連結。指派給完整網址、代理不准自己組，就是為了這個。

## Outcome

二十篇全部落地，`lint --kind life` 零 error，`catalogue_missing_pack` 從 80 降到 60，
55 條站內連結逐條解析全部通過（目標包存在、有 zh-TW、網址區段與包的 kind 相符），
`test_guides_content_pack.py` 與 `test_guides_pack_ingest.py` 35 passed / 5 skipped。

### 這一批最值錢的產出是一個坑，而且它有四種形態

**示範條款在 `law.fsc.gov.tw` 上是舊版，現行版在 `law.lia-roc.org.tw`。** 這件事本身不難記，
難的是它不只一種長相——四種形態是四個代理各自從不同角度踩到的，湊起來才完整：

1. **條次整段位移。** 住院醫療費用（實支實付型）「保險金的申領」舊第 18 條 → 現行第 19 條，
   「除外責任」舊第 11 條 → 現行第 12 條；日額型「保險金的申領」舊第 14 條 → 現行第 15 條。
   現行版修正日期是民國 113-06-28。
   **我第一次修的時候只把數字加一，結果得到一個號碼正確、內容過期的引用，比原本更難發現。**
   現行第 19 條寫的是「醫療費用**收據正本**。但如為電子文件，必要時本公司得要求提供紙本文件。」
   舊版只寫「醫療費用收據」；現行第 11 條也從一句話擴寫成兩款，第二款正是副本理賠的依據。
2. **條次沒動，內容改了。** 長期照顧保險單示範條款（`FL077956`）自民國 104 年起一直是 23 條，
   條號清單完全一致，改的全是內容——第 14 條申領文件的簡易智能測驗（MMSE）現行版已刪。
   第 17 篇的代理把 104 年歷史版整份抓下來逐條比對才看得出來。**只比對條次會完全看不出來。**
3. **條次與文字都對，但引文只抄了前半句。** `accident-insurance-basics` 漏掉
   「但超過一百八十日致成失能者，受益人若能證明……不在此限」，讀者會以為逾期就完全沒機會。
   `home-fire-insurance` 漏掉住宅火險參考條款第 24 條第 7 款的但書
   「但因承保之危險事故發生導致政府命令之焚毀或拆除者，不在此限」——而火災導致政府命令拆除
   正是最可能發生的情況，漏掉會得到相反結論。
4. **同一條並列兩個版本，抄錯半邊。** 示範條款有不少條文寫成
   「（辦理電子商務適用）……（未辦理電子商務適用）……」，條名與條次都只有一個。
   人壽保險單示範條款第 2 條契約撤銷權，電子商務版本是「得以**書面或其他約定方式**」，
   非電子商務版本才是「得以**書面**」。只抓 `第N條` 往下抄一段就會抄到另外半邊。

**唯一可靠的做法是逐條讀現行全文，不是推算條次。** 四種形態與實測對照表已寫進 brief 2.5。

### 第二個發現：不是所有保險條款都在 lia 站

`law.lia-roc.org.tw` 是**人壽**保險公會的系統，示範條款清單三十九筆全是人身保險，
**一筆財產保險都沒有**。住宅火險、地震險這類產險的對應文件不叫「示範條款」叫「**參考條款**」，
由**中華民國產物保險商業同業公會**（`nlia.org.tw`）公告、金管會核定。查不到就是站別選錯了。
參考條款一樣有版本坑，而且正好是上面第 2 型：住宅火災及地震基本保險參考條款的
114-07-15 版與現行 115-01-01 版第 1 至 77 條一條都沒位移，但第 2 條承保範圍類別補上第五款、
第 69 條承保損失定義多排除了「結構補強之費用」。附加條款自己也會過期——擴大地震保險
附加條款的公告文件停在民國九十年代，文內引用主約的條次已經對不上現行主約。

### 額度中斷的兩種復原策略

批次 02 學到「額度是整個 session 累積的，不是看並行數」，這一批照做分三波（7／7／6），
第二波仍在 16:00 UTC 附近被砍掉三個代理。兩種情況要用不同做法：

- **檔案殘缺**（pack 草稿還在壓字數）→ 派新代理接手工作區，並**要求重新查證**而不是沿用草稿。
  批次 02 這樣做抓出五個實質錯誤。
- **檔案齊全只缺 `notes.md`** → 協調者自己用 `curl` 收尾。**週額度擋 API 呼叫（含 WebFetch），
  但不擋網路**，`curl` 那條路一直是通的。
  這種情況下 `notes.md` 開頭要明寫「這份不是原撰稿代理寫的」，並分「協調者重新核對通過的項目」
  與「未由協調者逐條重驗的部分」兩節——不替沒看過的查證背書。

### 代理更正了我指派裡的五處事實錯誤

派工前我自己寫的指派有五處是錯的，代理逐條讀現行全文之後更正，協調者再 `curl` 複驗：

- 「每一項各有限額」→ 審查應注意事項第 53 點：分項限額與總限額**擇一**。
- 「失能程度表是判準」→ 第 87-2 點：失能扶助保險**不得引用**傷害保險那張表。
- 《全民健康保險保險對象在國內外自墊醫療費用核退辦法》**不存在**，正確是
  《全民健康保險自墊醫療費用核退辦法》（`L0060005`）。
- 「保險法第 116 條有六、七項」→ 現行全文**八項**；而且我把第 8 項當成墊繳的授權條文，
  它實際寫的是「已約定墊繳且本息超過保單價值準備金時，停效與復效之申請準用第一項至第六項」，
  墊繳機制本身在示範條款第 6 條。
- 契約撤銷權我給的是「未辦理電子商務適用」那一版（見上面第 4 型）。

**這件事本身就是經驗**：指派寫得越具體越好，但協調者寫的具體內容也會錯，
所以指派要說的是「去讀哪一份的現行全文」，不是「條文內容是什麼」。

代理也自己避開了兩個我沒點名的坑：保險法第 63 條寫的是逾期通知者「對保險人因此所受之損失
負賠償責任」而非請求權當然消滅；兩型住院醫療示範條款根本沒有等待期條文，規則在人身保險
商品審查應注意事項第 67 與 78 點，所以正文明寫「示範條款沒有這一條」。

### brief 改了哪裡

新增 **2.5 保險篇的額外限制**整節（不得出現保險公司或商品名稱、不做費率比較、不給投保金額
建議、不寫「該不該買」、條款用語照抄正式名稱、理賠是個案認定不寫成通則、免責 callout 加句
「理賠與否、給付金額以保單條款與保險公司核定為準。」），以及上面四種版本坑形態、
產險走 `nlia.org.tw` 參考條款、「示範條款沒寫的東西不要說成示範條款寫的」、
失能扶助保險不得引用傷害保險失能程度表。10.5 另補「前後遮蔽」與可直接複製的 `render_svg` 片段。

### 順手改的

總表第 20 篇的「圖」欄從「照」改「插」（批次 01 的經驗記錄：全部自繪是對的決定），
標題的「話術」改成「把口語說法換回條款用語」——「話術」帶貶義，與這篇「不得對業務員這個
職業做任何價值判斷」的紅線直接衝突。

### 留給下一批的

**sitemap 落地後實測 986／1000，只剩 14 列。批次 04 開工前一定要先拆**
（`2026-09-14-sitemap-split-before-1000-rows`，該票的兩個依賴目前都還是 `review`）。
