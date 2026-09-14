---
id: 2026-09-14-life-finance-batch-02
title: 生活分享財經系列批次 02：銀行、支付與信用（20 篇）
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
  - apps/api/app/guides/content/digital-bank-account-taiwan.json
  - apps/api/app/guides/content/high-interest-savings-taiwan.json
  - apps/api/app/guides/content/mobile-payment-taiwan-guide.json
  - apps/api/app/guides/content/credit-card-cashback-basics.json
  - apps/api/app/guides/content/credit-card-choose-by-spending.json
  - apps/api/app/guides/content/credit-card-revolving-interest.json
  - apps/api/app/guides/content/installment-zero-interest-cost.json
  - apps/api/app/guides/content/credit-score-jcic-taiwan.json
  - apps/api/app/guides/content/build-credit-from-zero.json
  - apps/api/app/guides/content/bank-transfer-fees-taiwan.json
  - apps/api/app/guides/content/foreign-currency-account-taiwan.json
  - apps/api/app/guides/content/online-forex-exchange-taiwan.json
  - apps/api/app/guides/content/overseas-card-fees-dcc.json
  - apps/api/app/guides/content/overseas-atm-withdrawal.json
  - apps/api/app/guides/content/online-banking-security.json
  - apps/api/app/guides/content/warning-account-prevention.json
  - apps/api/app/guides/content/debit-vs-credit-card.json
  - apps/api/app/guides/content/credit-card-dispute-chargeback.json
  - apps/api/app/guides/content/epayment-vs-ewallet-taiwan.json
  - apps/api/app/guides/content/bank-account-opening-guide.json
  - apps/web/public/guides/digital-bank-account-taiwan
  - apps/web/public/guides/high-interest-savings-taiwan
  - apps/web/public/guides/mobile-payment-taiwan-guide
  - apps/web/public/guides/credit-card-cashback-basics
  - apps/web/public/guides/credit-card-choose-by-spending
  - apps/web/public/guides/credit-card-revolving-interest
  - apps/web/public/guides/installment-zero-interest-cost
  - apps/web/public/guides/credit-score-jcic-taiwan
  - apps/web/public/guides/build-credit-from-zero
  - apps/web/public/guides/bank-transfer-fees-taiwan
  - apps/web/public/guides/foreign-currency-account-taiwan
  - apps/web/public/guides/online-forex-exchange-taiwan
  - apps/web/public/guides/overseas-card-fees-dcc
  - apps/web/public/guides/overseas-atm-withdrawal
  - apps/web/public/guides/online-banking-security
  - apps/web/public/guides/warning-account-prevention
  - apps/web/public/guides/debit-vs-credit-card
  - apps/web/public/guides/credit-card-dispute-chargeback
  - apps/web/public/guides/epayment-vs-ewallet-taiwan
  - apps/web/public/guides/bank-account-opening-guide
---

# 生活分享財經系列批次 02：銀行、支付與信用（20 篇）

## Why

[`docs/life-finance-series.md`](../../docs/life-finance-series.md) 的批次 02。站主要在生活分享專區
做第二個垂直領域（第一個是 AI 工具系列），分六批產出約 120 篇財經文章與教學；這張票是其中一批，
scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

**開工前先讀**總表的「不能寫的東西」與「經驗記錄」，以及批次 01 票的 Outcome。
財經是 Google 的 YMYL 類別，這個系列又包含投資題材，措辭規則和 AI 系列不一樣，不要套用舊經驗。

第 11–14 篇（外幣帳戶、線上結匯、海外刷卡 DCC、海外 ATM）是旅遊銜接篇，
指派要從總表「可連的旅遊攻略」表挑完整網址給代理。

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

1. `digital-bank-account-taiwan` · 數位帳戶是什麼：開戶流程、優利活存與使用限制 · finance, software · 圖：插　· 易變
2. `high-interest-savings-taiwan` · 高利活存怎麼看：利率級距、額度上限與實際拿到的利息 · finance · 圖：插　· 易變
3. `mobile-payment-taiwan-guide` · 台灣行動支付總整理：綁定方式、回饋與適用場景 · finance, software · 圖：插　· 易變
4. `credit-card-cashback-basics` · 信用卡回饋入門：現金回饋、紅利與哩程的差別 · finance, tutorial · 圖：插　· 易變
5. `credit-card-choose-by-spending` · 依消費習慣選信用卡：先算出自己的支出結構 · finance, tutorial · 圖：插
6. `credit-card-revolving-interest` · 循環利息與最低應繳：只繳最低到底會付多少 · finance · 圖：插　· 易變
7. `installment-zero-interest-cost` · 分期零利率的真實成本：手續費、定價與現金折扣 · finance · 圖：插
8. `credit-score-jcic-taiwan` · 聯徵信用報告怎麼查：信用評分是怎麼算出來的 · finance, tutorial · 圖：插　· 易變
9. `build-credit-from-zero` · 信用小白怎麼建立信用：第一張卡與往來紀錄 · finance, tutorial · 圖：插
10. `bank-transfer-fees-taiwan` · 轉帳與跨行手續費：什麼情況免費、什麼情況要錢 · finance · 圖：插　· 易變
11. `foreign-currency-account-taiwan` · 外幣帳戶開戶與用途：換匯、存款與領現金 · finance, tutorial · 圖：插　· 易變
12. `online-forex-exchange-taiwan` · 線上結匯教學：銀行 App 換匯、匯率價差與機場提領 · finance, tutorial · 圖：插　· 易變
13. `overseas-card-fees-dcc` · 海外刷卡手續費與 DCC：選當地幣別還是台幣 · finance, tutorial · 圖：插　· 易變
14. `overseas-atm-withdrawal` · 海外 ATM 提款：跨國提款卡、手續費與安全 · finance, tutorial · 圖：插　· 易變
15. `online-banking-security` · 網銀與帳戶安全：裝置綁定、OTP 與常見詐騙手法 · finance, tutorial · 圖：插
16. `warning-account-prevention` · 警示帳戶是怎麼來的：避免帳戶被凍結的實際做法 · finance · 圖：插
17. `debit-vs-credit-card` · 金融卡與信用卡差在哪：扣款時點、爭議款與額度 · finance, tutorial · 圖：插
18. `credit-card-dispute-chargeback` · 刷卡爭議款怎麼申請：時限、證明文件與流程 · finance, tutorial · 圖：插
19. `epayment-vs-ewallet-taiwan` · 電子支付與電子票證：法規分類與實際差別 · finance · 圖：插　· 易變
20. `bank-account-opening-guide` · 第一次開戶要帶什麼：臨櫃、線上與未成年開戶 · finance, tutorial · 圖：插　· 易變

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
