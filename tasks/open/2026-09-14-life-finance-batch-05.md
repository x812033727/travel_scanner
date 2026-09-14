---
id: 2026-09-14-life-finance-batch-05
title: 生活分享財經系列批次 05：投資入門：觀念與台股（20 篇）
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
  - 2026-09-14-life-finance-lint-rules
  - 2026-09-14-life-finance-batch-01
scope:
  - apps/api/app/guides/content/before-you-invest-checklist.json
  - apps/api/app/guides/content/compound-interest-explained.json
  - apps/api/app/guides/content/risk-and-return-basics.json
  - apps/api/app/guides/content/asset-allocation-basics.json
  - apps/api/app/guides/content/what-is-a-stock.json
  - apps/api/app/guides/content/what-is-an-etf.json
  - apps/api/app/guides/content/index-investing-explained.json
  - apps/api/app/guides/content/taiwan-brokerage-account-opening.json
  - apps/api/app/guides/content/taiwan-stock-order-types.json
  - apps/api/app/guides/content/odd-lot-trading-taiwan.json
  - apps/api/app/guides/content/taiwan-trading-costs.json
  - apps/api/app/guides/content/ex-dividend-taiwan.json
  - apps/api/app/guides/content/dollar-cost-averaging.json
  - apps/api/app/guides/content/portfolio-rebalancing.json
  - apps/api/app/guides/content/market-cap-vs-dividend-etf.json
  - apps/api/app/guides/content/etf-expense-ratio-tracking-error.json
  - apps/api/app/guides/content/mutual-fund-vs-etf.json
  - apps/api/app/guides/content/investment-scam-red-flags.json
  - apps/api/app/guides/content/financial-statement-basics.json
  - apps/api/app/guides/content/investment-information-sources.json
  - apps/web/public/guides/before-you-invest-checklist
  - apps/web/public/guides/compound-interest-explained
  - apps/web/public/guides/risk-and-return-basics
  - apps/web/public/guides/asset-allocation-basics
  - apps/web/public/guides/what-is-a-stock
  - apps/web/public/guides/what-is-an-etf
  - apps/web/public/guides/index-investing-explained
  - apps/web/public/guides/taiwan-brokerage-account-opening
  - apps/web/public/guides/taiwan-stock-order-types
  - apps/web/public/guides/odd-lot-trading-taiwan
  - apps/web/public/guides/taiwan-trading-costs
  - apps/web/public/guides/ex-dividend-taiwan
  - apps/web/public/guides/dollar-cost-averaging
  - apps/web/public/guides/portfolio-rebalancing
  - apps/web/public/guides/market-cap-vs-dividend-etf
  - apps/web/public/guides/etf-expense-ratio-tracking-error
  - apps/web/public/guides/mutual-fund-vs-etf
  - apps/web/public/guides/investment-scam-red-flags
  - apps/web/public/guides/financial-statement-basics
  - apps/web/public/guides/investment-information-sources
---

# 生活分享財經系列批次 05：投資入門：觀念與台股（20 篇）

## Why

[`docs/life-finance-series.md`](../../docs/life-finance-series.md) 的批次 05。站主要在生活分享專區
做第二個垂直領域（第一個是 AI 工具系列），分六批產出約 120 篇財經文章與教學；這張票是其中一批，
scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

**開工前先讀**總表的「不能寫的東西」與「經驗記錄」，以及批次 01 票的 Outcome。
財經是 Google 的 YMYL 類別，這個系列又包含投資題材，措辭規則和 AI 系列不一樣，不要套用舊經驗。

**整批是投資題材，法遵風險最高。** 第 15 篇只比較制度差異（選股邏輯、配息來源），不比績效、不點名商品。
第 18 篇 `investment-scam-red-flags` 會引用「保證獲利」這類詐騙話術當反例，`finance_claim_language`
的 lint warning 在這篇是預期的——審稿時確認它是在指認話術，不是在使用話術。

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

1. `before-you-invest-checklist` · 投資前先做完的四件事：緊急金、負債、保險與目標 · finance, tutorial · 圖：插
2. `compound-interest-explained` · 複利到底怎麼運作：用實際數字看時間的作用 · finance, tutorial · 圖：插
3. `risk-and-return-basics` · 風險與報酬：為什麼高報酬一定伴隨高風險 · finance, tutorial · 圖：插
4. `asset-allocation-basics` · 資產配置入門：股債現金的比例怎麼決定 · finance, tutorial · 圖：插
5. `what-is-a-stock` · 股票是什麼：股東權益、股價與公司價值的關係 · finance, tutorial · 圖：插
6. `what-is-an-etf` · ETF 是什麼：追蹤指數、內扣費用與折溢價 · finance, tutorial · 圖：插
7. `index-investing-explained` · 指數化投資是什麼：為什麼「不選股」也是一種策略 · finance, tutorial · 圖：插
8. `taiwan-brokerage-account-opening` · 台股開戶教學：證券戶、交割戶與電子下單 · finance, tutorial · 圖：插　· 易變
9. `taiwan-stock-order-types` · 台股下單方式：限價市價、ROD／IOC／FOK 與各盤別 · finance, tutorial · 圖：插
10. `odd-lot-trading-taiwan` · 零股怎麼買：盤中零股與定期定額的差別 · finance, tutorial · 圖：插　· 易變
11. `taiwan-trading-costs` · 台股交易成本：手續費、證交稅與折讓怎麼算 · finance · 圖：插　· 易變
12. `ex-dividend-taiwan` · 除權息是什麼：填權息、扣抵與要不要參與 · finance, tutorial · 圖：插
13. `dollar-cost-averaging` · 定期定額：適合什麼情況、什麼時候該檢討 · finance, tutorial · 圖：插
14. `portfolio-rebalancing` · 再平衡怎麼做：頻率、門檻與需要付出的成本 · finance, tutorial · 圖：插
15. `market-cap-vs-dividend-etf` · 市值型與高股息 ETF 的制度差異：選股邏輯與配息來源 · finance · 圖：插
16. `etf-expense-ratio-tracking-error` · 看 ETF 的內扣費用與追蹤誤差：公開說明書怎麼讀 · finance, tutorial · 圖：插
17. `mutual-fund-vs-etf` · 基金與 ETF 差在哪：申購方式、費用與交易時點 · finance · 圖：插
18. `investment-scam-red-flags` · 投資詐騙辨識：代操、假平台與「保證獲利」的共同特徵 · finance · 圖：插　· 易變
19. `financial-statement-basics` · 看懂財報三表：資產負債表、損益表與現金流量表 · finance, tutorial · 圖：插
20. `investment-information-sources` · 投資資訊怎麼查證：公開資訊觀測站與官方揭露管道 · finance, tutorial · 圖：插　· 易變

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
