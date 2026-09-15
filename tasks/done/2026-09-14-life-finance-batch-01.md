---
id: 2026-09-14-life-finance-batch-01
title: 生活分享財經系列批次 01：理財基礎與記帳（20 篇）
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-14T12:32:52Z
created_at: 2026-09-14T11:45:48Z
completed_at: 2026-09-14T13:30:03Z
branch: claude/beautiful-fermat-0klj9k
depends_on:
  - 2026-09-14-life-finance-series-catalogue
  - 2026-09-14-life-finance-topic
scope:
  - docs/life-finance-series-brief.md
  - docs/life-finance-series.md
  - apps/api/app/guides/content/personal-finance-first-steps.json
  - apps/api/app/guides/content/finance-glossary-50-terms.json
  - apps/api/app/guides/content/expense-tracking-getting-started.json
  - apps/api/app/guides/content/expense-tracking-app-choose.json
  - apps/api/app/guides/content/household-budget-methods.json
  - apps/api/app/guides/content/bank-account-separation-system.json
  - apps/api/app/guides/content/emergency-fund-how-much.json
  - apps/api/app/guides/content/fixed-cost-subscription-audit.json
  - apps/api/app/guides/content/payslip-explained-taiwan.json
  - apps/api/app/guides/content/labor-pension-self-contribution.json
  - apps/api/app/guides/content/labor-insurance-vs-pension.json
  - apps/api/app/guides/content/einvoice-carrier-taiwan.json
  - apps/api/app/guides/content/personal-balance-sheet.json
  - apps/api/app/guides/content/monthly-money-review.json
  - apps/api/app/guides/content/savings-goal-planning.json
  - apps/api/app/guides/content/spending-triggers-and-habits.json
  - apps/api/app/guides/content/couple-money-management.json
  - apps/api/app/guides/content/kids-allowance-money-education.json
  - apps/api/app/guides/content/bank-fee-audit.json
  - apps/api/app/guides/content/financial-document-organization.json
  - apps/web/public/guides/personal-finance-first-steps
  - apps/web/public/guides/finance-glossary-50-terms
  - apps/web/public/guides/expense-tracking-getting-started
  - apps/web/public/guides/expense-tracking-app-choose
  - apps/web/public/guides/household-budget-methods
  - apps/web/public/guides/bank-account-separation-system
  - apps/web/public/guides/emergency-fund-how-much
  - apps/web/public/guides/fixed-cost-subscription-audit
  - apps/web/public/guides/payslip-explained-taiwan
  - apps/web/public/guides/labor-pension-self-contribution
  - apps/web/public/guides/labor-insurance-vs-pension
  - apps/web/public/guides/einvoice-carrier-taiwan
  - apps/web/public/guides/personal-balance-sheet
  - apps/web/public/guides/monthly-money-review
  - apps/web/public/guides/savings-goal-planning
  - apps/web/public/guides/spending-triggers-and-habits
  - apps/web/public/guides/couple-money-management
  - apps/web/public/guides/kids-allowance-money-education
  - apps/web/public/guides/bank-fee-audit
  - apps/web/public/guides/financial-document-organization
---

# 生活分享財經系列批次 01：理財基礎與記帳（20 篇）

## Why

[`docs/life-finance-series.md`](../../docs/life-finance-series.md) 的批次 01。站主要在生活分享專區
做第二個垂直領域（第一個是 AI 工具系列），分六批產出約 120 篇財經文章與教學；這張票是其中一批，
scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

**開工前先讀**總表的「不能寫的東西」與「經驗記錄」，以及批次 01 票的 Outcome。
財經是 Google 的 YMYL 類別，這個系列又包含投資題材，措辭規則和 AI 系列不一樣，不要套用舊經驗。

這是**試點批次**。學到的東西寫回 `docs/life-finance-series-brief.md`，並在總表的「經驗記錄」留一段，
02–06 開工前會先讀。第 2 篇 `finance-glossary-50-terms` 是總索引，`display_order` 填 10。

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

1. `personal-finance-first-steps` · 個人理財第一步：先看懂收支，再談存錢與投資 · finance, tutorial · 圖：插
2. `finance-glossary-50-terms` · 財經名詞速查：50 個理財與投資常見詞彙一次搞懂 · finance, misc · 圖：插
3. `expense-tracking-getting-started` · 記帳新手入門：記什麼、記多久、怎麼不半途而廢 · finance, tutorial · 圖：插
4. `expense-tracking-app-choose` · 記帳 App 怎麼選：自動同步、手動輸入與隱私的取捨 · finance, software · 圖：插　· 易變
5. `household-budget-methods` · 預算怎麼抓：50/30/20、信封法與零基預算的差別 · finance, tutorial · 圖：插
6. `bank-account-separation-system` · 帳戶分離法：用三到四個帳戶把錢分開管 · finance, tutorial · 圖：插
7. `emergency-fund-how-much` · 緊急預備金要存多少：怎麼算、放哪裡、什麼時候可以動 · finance, tutorial · 圖：插
8. `fixed-cost-subscription-audit` · 固定支出健檢：訂閱、電信與保費一年能省下多少 · finance, daily · 圖：插
9. `payslip-explained-taiwan` · 看懂薪資單：勞保、健保、勞退提繳與實領差在哪 · finance, tutorial · 圖：插　· 易變
10. `labor-pension-self-contribution` · 勞退自提 6%：怎麼提、省多少稅、什麼時候不適合 · finance, tutorial · 圖：插　· 易變
11. `labor-insurance-vs-pension` · 勞保與勞退不是同一件事：老年給付各自怎麼領 · finance · 圖：插　· 易變
12. `einvoice-carrier-taiwan` · 電子發票載具設定教學：手機條碼、歸戶與自動對獎 · finance, tutorial · 圖：插　· 易變
13. `personal-balance-sheet` · 寫一張個人資產負債表：把自己的淨值算出來 · finance, tutorial · 圖：插
14. `monthly-money-review` · 每月收支回顧：30 分鐘看完一個月的錢去哪了 · finance, productivity · 圖：插
15. `savings-goal-planning` · 存錢目標怎麼設：把「想買」換算成每月要存的金額 · finance, tutorial · 圖：插
16. `spending-triggers-and-habits` · 錢為什麼會不見：找出自己的消費觸發點 · finance, daily · 圖：照
17. `couple-money-management` · 兩個人的錢怎麼管：共同帳戶、分攤比例與定期對帳 · finance, daily · 圖：照
18. `kids-allowance-money-education` · 零用錢怎麼給：把金錢觀教給孩子的實際做法 · finance, daily · 圖：照
19. `bank-fee-audit` · 銀行手續費健檢：跨行、匯款與帳管費怎麼省 · finance · 圖：插　· 易變
20. `financial-document-organization` · 財務文件整理：保單、對帳單與稅單放哪裡才找得到 · finance, productivity · 圖：插

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

（完成後填：踩到什麼、brief 改了哪裡）

## Outcome

二十篇全部落地，`lint --kind life` 零 error，`catalogue_missing_pack` 從 120 降到 100，
`test_guides_content_pack.py` 等四個測試檔 107 passed，ruff 與 mypy 全綠。

做法：我先親自寫兩篇（`personal-finance-first-steps`、`labor-pension-self-contribution`）
跑完整條產線，把踩到的坑寫進 brief 第 10.5 節，再分三波派 18 個撰稿代理，一篇一個。

### 給批次 02–06 的七件事

1. **hero 不要畫成由低到高的長條。** 我自己第一版把五個步驟畫成遞增柱狀，渲染出來就是
   一張績效成長圖——正是 brief 第 2 節自己禁止的視覺語言。順序題材要用序列（等大的方塊
   排成一列），不要用高度。已寫進 brief 10.5。
2. **`--no-render` 是反向旗標**，有 `hero.svg` 時加了會直接失敗，不是跳過渲染。
3. **圖解頁尾的 `© Mokaair 製圖 2026` 會讓 `2026` 變成「圖上的數字」**，正文必須出現，
   否則 `diagram_number_not_in_text` 擋下整篇。慣例是表格 caption 寫「查證於 2026 年 9 月」。
4. **字數會貼著上限寫。** 收進來的每一篇都落在 2,900–3,031，三篇小幅超出編輯區間
   （超 1、28、31 字）。內容查過都不是湊字，所以照收，但這是「寫到上限」而不是
   「寫完就停」的訊號。brief 新增 10.6 節，批次 02 起瞄準 2,200–2,600 字。
5. **政府網站 403 有兩種合格處理，都要在 `notes.md` 寫明讀取方式：**
   - 限定官方網域的 `WebSearch` 取回該頁原句，逐字比對後採用（`monthly-money-review`
     對電子發票查詢期數就是這樣做的，我事後獨立複查，一致）。
   - 讀不到就**放棄那個來源**，改引其他官方單位（`einvoice-carrier-taiwan` 直接 403、
     Wayback 快照又被截斷且無文字層，最後完全不引電子發票平台，改用高雄國稅局與
     稅務入口網）。兩種都比「引用一個自己沒讀到的網址」誠實。
6. **會過期的數字，用官方表格自己印的金額反推。** `payslip-explained-taiwan` 的健保
   5.17% 出處是民國 110 年的公告，我查不到 115 年度是否仍適用。解法不是再查公告，
   而是拿健保署 115.1.1 生效的負擔金額表，用 `投保金額 × 5.17% × 30%` 重算表上印的
   金額——58 個等級 × 6 欄共 348 筆全部吻合，且 5.00% 與 5.47% 都對不上。
   這比公告更硬。**下次遇到「這個費率還適用嗎」，先找有沒有當期的金額表。**
7. **中途修正比事後退回省一輪。** 第 6 點那件事我是在代理還在跑的時候發現並送回去的，
   而且給的是可執行的判準（去表裡挑一級對算式），不是「再查一次」。

### 額度

一篇一個代理、18 個同時跑，沒有撞到額度，和 AI 系列「每波最多七個」的經驗不同。
每篇約 19–33 分鐘，查證重的（payslip、einvoice）接近上限。
