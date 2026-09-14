---
id: 2026-09-14-life-finance-batch-03
title: 生活分享財經系列批次 03：保險與風險（20 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:45:48Z
completed_at:
branch:
depends_on:
  - 2026-09-14-life-finance-series-catalogue
  - 2026-09-14-life-finance-topic
  - 2026-09-14-life-finance-lint-rules
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

- [ ] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg`
      或 Commons 照片）、至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、**兩個 callout（含最後的免責）**、
      sources 每筆有 `checked_on`、至少一個站內 `link`。
- [ ] **每篇最後一個區塊是免責 callout**，用 `docs/life-finance-series-brief.md` 第 5 節的模板，查證日是實際日期。
- [ ] **人工逐篇確認：沒有推薦任何個股／個別基金／個別 ETF／個別保單／個別銀行方案，
      沒有買賣建議、目標價或報酬預測，沒有把行情數字寫進正文。** 這一項機器檢查不到。
- [ ] 合作連結零個——站上沒有金融類內容夥伴，任何帶追蹤參數的網址都會讓整篇被拒。
- [ ] 沒有任何金融機構的 logo、字標、圖示或介面截圖；hero 沒有股價曲線或金幣堆；
      照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA。
- [ ] 級距、費率、額度、申報時程都在撰稿當天查主管機關或業者官網；查不到的寫「以主管機關公告為準」。
- [ ] 站內連結只用指派給的完整網址；旅遊攻略只連總表「可連的旅遊攻略」那張表
      （`taiwan-*` 那幾篇沒有 zh-TW，連過去是壞連結）。
- [ ] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；
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
20. `insurance-sales-questions` · 聽業務員說明時該問的問題：把話術換回條款 · finance · 圖：照

- [ ] 認領後從總表抄出指派（含可連的完整網址），一篇一個撰稿代理、每波最多七個，
      代理照 `docs/life-finance-series-brief.md` 產出工作區。
- [ ] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [ ] `guides-pack lint --render-dir` 逐張看圖；**逐篇讀過確認法遵**；跑測試；更新這張票；commit。

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

（完成後填：踩到什麼、brief 改了哪裡）
