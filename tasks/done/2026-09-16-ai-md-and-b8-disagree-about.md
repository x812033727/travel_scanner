---
id: 2026-09-16-ai-md-and-b8-disagree-about
title: ai.md and the AI ticket's B8 disagree about whether an ai-news article may carry finance
status: done
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-16T22:05:39Z
completed_at: 2026-09-16T23:04:03Z
branch:
depends_on: []
scope:
  - docs/news-2026-batch-4/ai.md
---

# ai.md and the AI ticket's B8 disagree about whether an ai-news article may carry finance

## Why

批次 4 的兩份規格對同一件事給了相反的答案，而 B8 還沒動筆：

- `docs/news-2026-batch-4/ai.md` 第 54–56 行：「沒有免責 callout — AI 篇不帶 `finance`
  主題，不要加投資免責。照 `BRIEF.md` 放一個一般 `callout`」。
- `tasks/open/2026-09-16-news-batch-4-3-ai-news.md` 第 80 行把 B8 排成
  「`ai-news-chatgpt-financial-services-20260910`：ChatGPT for Financial
  Services（帶 finance，必附免責）」。

這是編輯決定，不是程式缺陷。工具在兩種讀法下都是對的：
`docs/news-2026-batch-4/check_article.py` 的 callout 數與免責檢查都看內容包**自己的
topics**，和站上 `pack_ingest._finance_problems` 一樣，所以帶 `finance` 的 AI 文章會被要求
第二個 callout 與該語系的免責標記，不帶的則只要一個 callout。兩邊都測過（見 Notes）。

但寫 B8 的代理會先讀 `ai.md`，照它寫就不會帶 `finance`，於是這篇文章進不了 `finance` hub，
也不會有免責 callout；反過來照票寫就與 `ai.md` 矛盾。誰先讀到哪一份，決定文章的主題，
這是這張票要擋掉的事。

## Definition of done

- [ ] 站主決定 B8 帶不帶 `finance`。
- [ ] `ai.md` 與 AI 票的 B8 那一列講同一件事（改其中一邊，或兩邊都補上「B8 是例外」）。
- [ ] 決定寫進 `ai.md`，寫成規則而不是單篇例外，下一批才不會再碰一次。

## Steps

- [ ] 問站主：`ChatGPT for Financial Services` 這種「AI 公司推出金融產品」的新聞，
      算不算 `crypto.md`／`life-finance-series` 意義下的理財內容。
- [ ] 照裁定改 `ai.md`（若 B8 帶 `finance`，把「AI 篇不帶 finance」改寫成
      「除非文章本身談理財產品，例如 B8」）。
- [ ] 若裁定改的是票，請 AI 票的持有人改 B8 那一列，不要在這張票裡改別人的檔案。

## How to verify

規格本身沒有可執行的測試；可驗的是工具在兩種答案下都正確：

```bash
cd apps/api
uv run python ../../docs/news-2026-batch-4/check_article.py <B8 的 slug> --full
```

帶 `finance` 的內容包必須被要求兩個 callout 與該語系的免責標記
（`zh-TW` 是「不是投資建議」），不帶的只要一個；兩者都不該是 `FAIL` 以外的行為。

## Notes

在移植工具時實測過兩個方向（`MOKAAIR_ROOT` 指向沙箱根目錄，正式內容一個位元組都沒動，
文章用的是批次 3 的 `ai-news-siri-ai-ios-27-20260914` 加上 `summary`／`faq` 後的副本）：

- topics `['ai','gadgets','ai-news']`、一個 callout → `OK ... EXIT=0`。
- topics `['ai','finance','ai-news']`、文章自己的 callout ＋ 帶該語系標記的免責 callout
  → `OK ... EXIT=0`。
- topics `['ai','finance','ai-news']`、只有一個 callout → `EXIT=1`，五語各一行，包括
  `lint zh-TW: error: finance_no_disclaimer: ...`、
  `1 callouts, want 2 (the article's own and the finance disclaimer)`、
  `blocks must end faq, callout, callout, link, link`、
  `zh-TW needs a disclaimer callout containing '不是投資建議'`。

所以工具不需要跟著這個決定改；要改的只有規格。`check_article.py` 裡免責那一段的註解
現在明寫兩份規格互相矛盾、由這張票決定，不再把票的讀法寫成已定案。

## 開票時這件事已經解決了（2026-09-16）

這張票是工具移植的代理開的，但它看到的是舊狀態。同一個矛盾在 commit `856b4501`
就已經解掉，而且解的方向跟這張票的建議一致：

- `docs/news-2026-batch-4/ai.md` 第 54 行的標題已經改成
  「## 沒有免責 callout，B8 也一樣」，底下逐段寫明 B8 為什麼不掛 `finance`
  （主題怎麼掛看的是文章在寫什麼，不是標題裡有沒有 financial；掛上去會讓一篇 AI 新聞
  出現在理財專區，還會觸發 error 級的 `finance_no_disclaimer`），以及那篇的一般 callout
  要明講「本站沒有試用、也不是投資建議」。
- `tasks/open/2026-09-16-news-batch-4-3-ai-news.md` 第 80 行已經改成
  「ChatGPT for Financial Services（**不掛 finance**，理由見 `ai.md`）」。

兩處現在一致，沒有剩餘工作，直接結案。留下這張票是因為它記錄了一個真實的衝突，
以及**規格衝突要開票而不是自行決定**這個正確的反應。
