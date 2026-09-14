---
id: 2026-09-14-life-finance-batch-06
title: 生活分享財經系列批次 06：海外投資、數位資產與退休（20 篇）
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
  - 2026-09-14-life-finance-batch-05
scope:
  - apps/api/app/guides/content/sub-brokerage-vs-foreign-broker.json
  - apps/api/app/guides/content/w8ben-dividend-withholding.json
  - apps/api/app/guides/content/international-wire-transfer-cost.json
  - apps/api/app/guides/content/us-stock-market-basics.json
  - apps/api/app/guides/content/bond-basics.json
  - apps/api/app/guides/content/money-market-and-time-deposit.json
  - apps/api/app/guides/content/reits-basics.json
  - apps/api/app/guides/content/gold-investment-channels.json
  - apps/api/app/guides/content/forex-basics-for-individuals.json
  - apps/api/app/guides/content/margin-and-leverage-risk.json
  - apps/api/app/guides/content/futures-options-risk-overview.json
  - apps/api/app/guides/content/what-is-cryptocurrency.json
  - apps/api/app/guides/content/bitcoin-basics.json
  - apps/api/app/guides/content/stablecoin-explained.json
  - apps/api/app/guides/content/crypto-exchange-vs-wallet.json
  - apps/api/app/guides/content/taiwan-vasp-regulation.json
  - apps/api/app/guides/content/crypto-tax-taiwan.json
  - apps/api/app/guides/content/behavioral-biases-investing.json
  - apps/api/app/guides/content/retirement-planning-calculation.json
  - apps/api/app/guides/content/fire-movement-realistic.json
  - apps/web/public/guides/sub-brokerage-vs-foreign-broker
  - apps/web/public/guides/w8ben-dividend-withholding
  - apps/web/public/guides/international-wire-transfer-cost
  - apps/web/public/guides/us-stock-market-basics
  - apps/web/public/guides/bond-basics
  - apps/web/public/guides/money-market-and-time-deposit
  - apps/web/public/guides/reits-basics
  - apps/web/public/guides/gold-investment-channels
  - apps/web/public/guides/forex-basics-for-individuals
  - apps/web/public/guides/margin-and-leverage-risk
  - apps/web/public/guides/futures-options-risk-overview
  - apps/web/public/guides/what-is-cryptocurrency
  - apps/web/public/guides/bitcoin-basics
  - apps/web/public/guides/stablecoin-explained
  - apps/web/public/guides/crypto-exchange-vs-wallet
  - apps/web/public/guides/taiwan-vasp-regulation
  - apps/web/public/guides/crypto-tax-taiwan
  - apps/web/public/guides/behavioral-biases-investing
  - apps/web/public/guides/retirement-planning-calculation
  - apps/web/public/guides/fire-movement-realistic
---

# 生活分享財經系列批次 06：海外投資、數位資產與退休（20 篇）

## Why

[`docs/life-finance-series.md`](../../docs/life-finance-series.md) 的批次 06。站主要在生活分享專區
做第二個垂直領域（第一個是 AI 工具系列），分六批產出約 120 篇財經文章與教學；這張票是其中一批，
scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

**開工前先讀**總表的「不能寫的東西」與「經驗記錄」，以及批次 01 票的 Outcome。
財經是 Google 的 YMYL 類別，這個系列又包含投資題材，措辭規則和 AI 系列不一樣，不要套用舊經驗。

**加密貨幣那六篇（12–17）風險最高**，寫的是運作機制與法遵現況，不是參與建議。
第 16、17 篇的法規狀態變動快，每次回查都要重讀金管會與國稅局的公告。

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

1. `sub-brokerage-vs-foreign-broker` · 複委託與海外券商：成本結構與遺產處理的差別 · finance · 圖：插　· 易變
2. `w8ben-dividend-withholding` · W-8BEN 與股息扣繳：30% 是怎麼來的、怎麼填 · finance, tutorial · 圖：插　· 易變
3. `international-wire-transfer-cost` · 國際匯款成本：電匯費、中轉行與匯率價差 · finance, tutorial · 圖：插　· 易變
4. `us-stock-market-basics` · 美股市場基礎：交易時段、漲跌幅機制與報價單位 · finance, tutorial · 圖：插
5. `bond-basics` · 債券入門：票面利率、殖利率與價格為何反向 · finance, tutorial · 圖：插
6. `money-market-and-time-deposit` · 貨幣市場工具與定存：短期資金可以放哪裡 · finance · 圖：插　· 易變
7. `reits-basics` · REITs 是什麼：參與不動產的方式與風險 · finance · 圖：插
8. `gold-investment-channels` · 黃金的參與方式：實體、存摺與基金的差別 · finance · 圖：插
9. `forex-basics-for-individuals` · 外匯基礎：匯率怎麼看、個人換匯與投機的差別 · finance · 圖：插
10. `margin-and-leverage-risk` · 融資與槓桿的風險：維持率、追繳與強制平倉 · finance · 圖：插
11. `futures-options-risk-overview` · 期貨與選擇權：先理解風險再談工具 · finance · 圖：插
12. `what-is-cryptocurrency` · 加密貨幣是什麼：區塊鏈、代幣與價格從哪裡來 · finance, tutorial · 圖：插
13. `bitcoin-basics` · 比特幣入門：供給上限、挖礦與常見誤解 · finance, tutorial · 圖：插
14. `stablecoin-explained` · 穩定幣是什麼：錨定機制與脫鉤風險 · finance · 圖：插
15. `crypto-exchange-vs-wallet` · 交易所與自管錢包：私鑰、助記詞與保管責任 · finance, tutorial · 圖：插
16. `taiwan-vasp-regulation` · 台灣虛擬資產業者法遵現況：洗錢防制登記與投資人保護 · finance · 圖：插　· 易變
17. `crypto-tax-taiwan` · 加密貨幣的稅：交易所得、境內外與申報實務 · finance · 圖：插　· 易變
18. `behavioral-biases-investing` · 投資裡的行為偏誤：損失趨避、定錨與從眾 · finance, tutorial · 圖：插
19. `retirement-planning-calculation` · 退休金試算：勞保、勞退與自己要補的缺口 · finance, tutorial · 圖：插　· 易變
20. `fire-movement-realistic` · FIRE 提早退休：4% 法則的前提與台灣的差異 · finance · 圖：插

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
