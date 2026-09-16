---
id: 2026-09-14-life-finance-lint-rules
title: 財經文章的免責與措辭 lint 規則
status: review
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-16T11:16:56Z
created_at: 2026-09-14T11:45:30Z
completed_at:
branch: claude/brave-hopper-8ezxba
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_pack_ingest.py
  - docs/travel-guides.md
---

# 財經文章的免責與措辭 lint 規則

## Why

財經系列（[`docs/life-finance-series.md`](../../docs/life-finance-series.md)）有 120 篇，會由六個批次、
六個以上的 session、數量不明的撰稿代理寫出來。撰稿指令一篇只被讀一次，
而 AI 系列的經驗記錄已經證明規則會漂移（批次 03 送出 13 個連到不存在文章的連結）。

財經是 Google 的 YMYL 類別，而且這個系列包含投資題材：台灣《證券投資信託及顧問法》限制
未取得許可者為報酬提供證券投資分析與建議。**「每篇都要有免責聲明」這種樣板要求，
靠人盯 120 篇會漏；`lint_document` 是站上既有的「審稿標準裡機器讀得懂的部分」，
而 `test_the_packaged_life_content_passes_lint` 每次 CI 都會把全部 life 內容包跑一遍。**
把樣板檢查放進去，等於每次 CI 重驗這 120 篇。

## Definition of done

- [x] `lint_document` 認得文章的 topics，並對帶 `finance` 的文章多跑兩條規則。
- [x] `finance_no_disclaimer`（**error**）：帶 `finance` 的文章若沒有一個 `callout` 的
      `text` 含免責標記字串，就是 error。
- [x] `finance_claim_language`（**warning**）：帶 `finance` 的文章正文出現絕對化措辭
      （保證獲利／穩賺／包賺／必漲／必跌／無風險／報明牌／飆股／老師帶單…）時提醒審稿者。
- [x] `docs/travel-guides.md` 的 `### Editorial rules (the review standard for a pack)` 底下
      新增一小節記這兩條規則——`lint_document` 的 docstring 說那一節**就是**它編碼的規則集，
      規則沒有寫在那裡，下一個維護者會把它刪掉。
- [x] 既有的 273 篇 life 內容包仍然全綠（它們都沒有 `finance`，規則不會觸發）。

## Steps

### 1. 簽名

`lint_document` 目前是 `(document: GuideDocument, kind: Kind)`，拿不到 topics。

- [x] 改成 `lint_document(document, kind, *, topics: Sequence[str] = ())`。
      **關鍵字參數加預設值**，這樣 `tests/test_guides_pack_ingest.py` 既有的呼叫不用改就仍然編得過。
- [x] 正式呼叫點只有兩處，兩處都已經有 `pack` 在手：`pack_ingest.py:808` 與 `:902`，
      各加 `topics=pack.topics`。

### 2. 規則

```python
#: 一句話、一個地方。docs/life-finance-series-brief.md 的免責樣板必須逐字含這一句。
FINANCE_DISCLAIMER_MARKER = "不是投資建議"
FINANCE_CLAIM_WORDS = re.compile(
    r"保證(獲利|賺|不賠)|穩賺|包賺|必漲|必跌|無風險|報明牌|飆股|老師帶單|躺著賺"
)
```

- [x] `finance_no_disclaimer` 是 **error**：樣板檢查，零誤判，脆弱正是它的用處。
      今天沒有任何內容包帶 `finance`，所以 CI 現在就是綠的。
- [x] `finance_claim_language` 是 **warning，不是 error**。`investment-scam-red-flags`
      這篇本來就要引用那些詞當詐騙話術的特徵；設成 error 會擋掉一篇正當的文章，
      並且教下一個寫作者去繞過 linter。站上把 `no_diagram`、`no_internal_link`
      也放在 warning，同一個道理。
- [x] 規則只對帶 `finance` 的文章生效，其他 life 文章（AI 系列 273 篇）完全不受影響。

### 3. 測試（`tests/test_guides_pack_ingest.py`）

- [x] 帶 `topics=("finance",)`、沒有免責 callout 的文件 → `finance_no_disclaimer`，level 是 `error`。
- [x] 同一份文件加上含 `FINANCE_DISCLAIMER_MARKER` 的 callout → 不再出現這個 code。
- [x] 正文含「穩賺」且帶 `finance` → `finance_claim_language`，level 是 **`warning`**，不是 error。
- [x] 同樣的文字但 topics 是 `("ai",)` → 兩條規則都不觸發。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_pack_ingest.py tests/test_guides_content_pack.py -q
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life   # 273 篇既有內容包仍無 error
cd apps/api && uv run ruff check . && uv run mypy app
```

## Notes

- **這張票現在還不能認領。** `apps/api/app/guides/pack_ingest.py` 在
  `tasks/open/2026-09-14-claude-code-tutorial-center.md` 的 scope 裡，那張票是 `status: review`
  且有 owner，`review` 屬於 `HOLDS_SCOPE`，所以 `claim` 會拒絕。等它合併，
  或等它的認領超過 24 小時變成 stale。
- `tasks/open/2026-09-14-pack-ingest-urlopen-scheme.md`（open）也要改同一個檔案。
  兩張 open 票可以並存，只是不能同時 active；先落地其中一張，或一起做。
- **批次票不再依賴這張票。** 原本六張批次票把它寫進 `depends_on`，但那會死鎖：
  這張票在 `pack_ingest.py` 合併前認領不了，批次票就永遠開不了工。而且 lint 規則本來就不是
  ingest 的前提——`docs/life-finance-series.md` 一直是這樣寫的。
  **規則落地時要回頭把已經寫好的財經內容包重跑一次 `lint --kind life`**：
  照 brief 寫的文章帶著那段免責樣板，應該直接過，但要驗過才算。
- **機器只擋得住樣板。** 「有沒有變相推薦個股」「風險講得夠不夠」是讀不出來的，
  那留在每張批次票的 Definition of done，由人逐篇看。不要試圖用正規表示式做這件事：
  會在這個系列賴以為生的教育性句子上大量誤判，還給人一種已經擋住了的錯覺。
- 不要做成前端統一渲染的免責條。那要動五語系 `messages/`（連帶 `check:i18n`）與文章元件，
  而且會出現在 `expense-tracking-getting-started` 這種不需要投資免責的篇上。
  站上把自動揭露條留給合作連結；逐篇 callout 進到索引得到的正文裡，對 E-E-A-T 也比較好。

## 實作紀錄（claude-opus-5, 2026-09-16）

三處與票上寫的不同，都是實作時查到的事實，不是改範圍：

1. **呼叫點行號漂掉了。** 票上寫 `pack_ingest.py:808` 與 `:902`，實際是 `:876` 與 `:976`
   （`lint_document` 本身在 `:189`）。兩處都已經有 `pack` 在手，照票上的做法補 `topics=pack.topics`。

2. **「今天沒有任何內容包帶 `finance`」已經過期。** 財經批次 01–03 合併後，
   現在有 **60 篇** life 內容包帶 `finance`。實測這 60 篇（全部 zh-TW 單語）
   每一篇都已經有逐字含「不是投資建議」的 callout，所以規則設成 error 仍然全綠——
   結論不變，理由不同：不是「規則不會觸發」，而是「既有內容本來就合規」。
   這反而讓規則更有價值：它現在就在守那 60 篇。

3. **免責標記改成五語，且觸發範圍不是整個 `finance` 家族。** 兩個發現：
   - `lint_all` 是**逐語系**送進 `lint_document` 的（`:990` 附近），而且不會告訴它現在看的是哪個語系。
     單一中文標記會讓任何多語系財經文章的四份譯文全部變成 error。
     所以改成 `FINANCE_DISCLAIMER_MARKERS` 五語元組，casefold 比對，任一命中即可。
     這對接下來的幣圈五語批次是必要條件。
   - 觸發主題定為 `{finance, investing, crypto}`，**不是**整個財經家族。
     `crypto` 要單獨列，因為 `retopic` 只會替 `website`／`marketing` 這兩個新父主題補父層
     （`retopic.py:531` 的 `LIFE_SEED_TOPICS[:8]`），`finance` 屬於原本的八個，
     所以 `crypto-*` 文章永遠不會自動帶到 `finance`，會整個逃過這條規則。
     反過來，`banking`／`credit`／`tax-insurance`／`finance-basics` 刻意排除：
     實測有四篇帶這些子主題、沒有免責且**本來就不該有**——
     `taiwan-company-registration`、`wise-transfer-checklist`、`youtube-payment-tax-info`、
     `household-inventory-spreadsheet`。要求它們掛投資免責，正是票上 Notes 警告的那種誤判，
     而且會教會寫作者「這段是樣板、貼上去就好」，免責條就是這樣失去意義的。

驗證：`pack_cli lint --kind life` 845 篇 0 error（`finance_claim_language` 也 0 筆）；
`test_guides_pack_ingest` 28 passed、`test_guides_content_pack` 與 `test_guides_content_links` 全綠；
`ruff check`、`ruff format`、`mypy app` 全過。
