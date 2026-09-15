---
id: 2026-09-14-life-finance-batch-04
title: 生活分享財經系列批次 04：稅務與政府制度（20 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:45:49Z
completed_at:
branch:
depends_on:
  - 2026-09-14-life-finance-series-catalogue
  - 2026-09-14-life-finance-topic
  - 2026-09-14-life-finance-batch-01
scope:
  - apps/api/app/guides/content/income-tax-filing-taiwan.json
  - apps/api/app/guides/content/tax-filing-app-guide.json
  - apps/api/app/guides/content/standard-vs-itemized-deduction.json
  - apps/api/app/guides/content/tax-dependents-taiwan.json
  - apps/api/app/guides/content/medical-expense-deduction.json
  - apps/api/app/guides/content/donation-deduction-taiwan.json
  - apps/api/app/guides/content/mortgage-interest-deduction.json
  - apps/api/app/guides/content/rent-expense-deduction.json
  - apps/api/app/guides/content/dividend-income-tax-options.json
  - apps/api/app/guides/content/overseas-income-minimum-tax.json
  - apps/api/app/guides/content/second-generation-nhi-supplement.json
  - apps/api/app/guides/content/tax-refund-schedule-taiwan.json
  - apps/api/app/guides/content/gift-tax-taiwan.json
  - apps/api/app/guides/content/estate-tax-basics-taiwan.json
  - apps/api/app/guides/content/house-land-transaction-tax.json
  - apps/api/app/guides/content/property-holding-tax.json
  - apps/api/app/guides/content/overseas-shopping-customs-duty.json
  - apps/api/app/guides/content/inbound-duty-free-allowance.json
  - apps/api/app/guides/content/side-income-tax-taiwan.json
  - apps/api/app/guides/content/government-subsidy-lookup.json
  - apps/web/public/guides/income-tax-filing-taiwan
  - apps/web/public/guides/tax-filing-app-guide
  - apps/web/public/guides/standard-vs-itemized-deduction
  - apps/web/public/guides/tax-dependents-taiwan
  - apps/web/public/guides/medical-expense-deduction
  - apps/web/public/guides/donation-deduction-taiwan
  - apps/web/public/guides/mortgage-interest-deduction
  - apps/web/public/guides/rent-expense-deduction
  - apps/web/public/guides/dividend-income-tax-options
  - apps/web/public/guides/overseas-income-minimum-tax
  - apps/web/public/guides/second-generation-nhi-supplement
  - apps/web/public/guides/tax-refund-schedule-taiwan
  - apps/web/public/guides/gift-tax-taiwan
  - apps/web/public/guides/estate-tax-basics-taiwan
  - apps/web/public/guides/house-land-transaction-tax
  - apps/web/public/guides/property-holding-tax
  - apps/web/public/guides/overseas-shopping-customs-duty
  - apps/web/public/guides/inbound-duty-free-allowance
  - apps/web/public/guides/side-income-tax-taiwan
  - apps/web/public/guides/government-subsidy-lookup
---

# 生活分享財經系列批次 04：稅務與政府制度（20 篇）

## Why

[`docs/life-finance-series.md`](../../docs/life-finance-series.md) 的批次 04。站主要在生活分享專區
做第二個垂直領域（第一個是 AI 工具系列），分六批產出約 120 篇財經文章與教學；這張票是其中一批，
scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

**開工前先讀**總表的「不能寫的東西」與「經驗記錄」，以及批次 01 票的 Outcome。
財經是 Google 的 YMYL 類別，這個系列又包含投資題材，措辭規則和 AI 系列不一樣，不要套用舊經驗。

**整批幾乎全是易變。** 級距、扣除額與申報時程每年公告，一律當天查財政部稅務入口網與各地區國稅局，
查不到就寫「以主管機關公告為準」。第 17、18 篇是旅遊銜接篇。

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

1. `income-tax-filing-taiwan` · 綜所稅申報全流程：時程、申報方式與查詢碼 · finance, tutorial · 圖：插　· 易變
2. `tax-filing-app-guide` · 報稅 App 與線上申報教學：認證、下載所得與繳稅 · finance, tutorial · 圖：插　· 易變
3. `standard-vs-itemized-deduction` · 標準扣除額與列舉扣除額：哪一種對自己划算 · finance, tutorial · 圖：插　· 易變
4. `tax-dependents-taiwan` · 扶養親屬怎麼報：資格、文件與常見爭議 · finance · 圖：插　· 易變
5. `medical-expense-deduction` · 醫藥及生育費列舉：哪些收據可以用 · finance · 圖：插　· 易變
6. `donation-deduction-taiwan` · 捐贈列舉扣除：限額與收據要求 · finance · 圖：插　· 易變
7. `mortgage-interest-deduction` · 房貸利息扣除額：條件、上限與自用住宅認定 · finance · 圖：插　· 易變
8. `rent-expense-deduction` · 租金支出扣除：房東不配合時可以怎麼處理 · finance · 圖：插　· 易變
9. `dividend-income-tax-options` · 股利所得二擇一：合併課稅與分開計稅怎麼算 · finance, tutorial · 圖：插　· 易變
10. `overseas-income-minimum-tax` · 海外所得與最低稅負制：什麼時候需要申報 · finance · 圖：插　· 易變
11. `second-generation-nhi-supplement` · 二代健保補充保費：哪些收入會被扣、怎麼算 · finance · 圖：插　· 易變
12. `tax-refund-schedule-taiwan` · 退稅什麼時候入帳：批次時程與退稅方式 · finance · 圖：插　· 易變
13. `gift-tax-taiwan` · 贈與稅：免稅額、婚嫁贈與與父母幫忙買房 · finance · 圖：插　· 易變
14. `estate-tax-basics-taiwan` · 遺產稅入門：課稅範圍、扣除額與申報時限 · finance · 圖：插　· 易變
15. `house-land-transaction-tax` · 房地合一稅：持有期間與稅率級距怎麼對應 · finance · 圖：插　· 易變
16. `property-holding-tax` · 房屋稅與地價稅：自用稅率與繳納時程 · finance · 圖：插　· 易變
17. `overseas-shopping-customs-duty` · 海外購物關稅：郵包、快遞與自用免稅額怎麼算 · finance, tutorial · 圖：插　· 易變
18. `inbound-duty-free-allowance` · 入境台灣免稅額度：菸酒、行李與應申報物品 · finance, tutorial · 圖：插　· 易變
19. `side-income-tax-taiwan` · 兼職與接案的稅：扣繳、執行業務所得與費用率 · finance · 圖：插　· 易變
20. `government-subsidy-lookup` · 政府補助怎麼查：查詢入口、資格與常見申請 · finance, tutorial · 圖：插　· 易變

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
