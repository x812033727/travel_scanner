---
id: 2026-09-06-broken-merchant-citations
title: Nine merchant citations are dead, unreachable or not HTML
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:33:38Z
created_at: 2026-09-06T00:52:12Z
completed_at: 2026-09-06T07:53:23Z
branch: claude/merchant-sources
depends_on: []
scope:
  - apps/api/app/foods/merchant_catalog.py
---

# Nine merchant citations are dead, unreachable or not HTML

## Why

A merchant's cited page is its evidence: it is what an administrator opens to confirm the
place is real and where it is, and it is what `fill-food-merchant-coordinates` reads. Nine of
the 63 first-party citations in `MERCHANT_DIRECT_SOURCE_SEEDS` cannot be opened at all, so
those merchants carry evidence that proves nothing.

Found by running the coordinate fill over every merchant on 2026-09-05:

```
fetch_failed: 6    http_500: 1    not_html: 2
```

Two are identified: `www.taicheongbakery.com.hk` serves a certificate that does not cover its
own hostname, and `https://www.krua-apsorn.com/` answers 500. The other seven are in the run
report and need naming before they can be fixed.

This is the same class of rot as the two country-level sources repaired in #165, where the JP
food page had been a hard 404 for every one of the ten Japanese dishes and the TW one had
silently become a New Taipei City page. Nobody notices a citation going bad, because nothing
reads it until someone does.

## Definition of done

- [x] Every URL in `MERCHANT_DIRECT_SOURCE_SEEDS` returns a real page about that merchant.
- [x] Any that cannot be repaired are removed rather than left broken — a merchant with no
      first-party source is honest, one with a dead link is not.
- [x] Existing rows are repaired too, not only the seed constants: `FoodMerchantSource.source_url`
      is written at creation, so changing the constant alone leaves production untouched.

## Steps

- [x] Get the nine slugs: `/root/coordfill_all.json` on the `hostinger2` VPS holds the full
      run, one row per merchant with its outcome.
- [x] Re-check each by hand. A 403 is not proof of rot — tourismthailand.org and
      discoverhongkong.com both answer 403 to a bot and are fine in a browser; that was
      checked in #165 and they were deliberately left alone.
- [x] Replace or remove. If replacing, fetch and read the new page first; #165 has the
      pattern, including a `_official_listing` vs `_merchant_website` choice that must match
      what the page actually is.
- [x] Add a migration rewriting the old strings in `food_merchant_sources.source_url`, in the
      style of `0039_repair_dead_food_sources`.
- [x] Update the count assertions in `tests/test_food_catalog.py` if the seed count changes.

## How to verify

Re-run the coordinate fill and confirm the unreadable outcomes are gone:

```bash
docker compose -f docker-compose.prod.yml exec -T api \
  python -m app.cli fill-food-merchant-coordinates | head -c 400
```

`fetch_failed`, `http_500` and `not_html` should all be absent from `outcomes`.

## Notes

The failure reasons are individually named because of #162 — before that every unreadable
page collapsed into one `fetch_failed`, which said only that something went wrong somewhere.
That change is what makes this task actionable.

Scope overlaps `2026-09-06-missing-merchant-sources`: both edit
`apps/api/app/foods/merchant_catalog.py`. They are separate problems (repair the broken
versus supply the absent) but cannot be worked in parallel. Whoever claims one should look at
the other first — doing both in one branch is reasonable.

2026-09-06 claude-fable-5-1：9 條逐條重查。4 條台灣（沁園春、福生小食店、石精臼、阿松割包）本機
開得了，是 VPS 當時抓不到，不動。5 條真壞，處理如下：

| slug | 原本 | 現在 |
| --- | --- | --- |
| tainan-hanlin | hanlin-tea.com.tw 每次連線被 reset | 臺南旅遊網 2236（赤崁店地址） |
| hong-kong-tai-cheong | 官網憑證不含自己的網域 | HKTB 泰昌餅家頁 |
| bangkok-krua-apsorn | 官網全站 500 | TAT 頁 |
| krabi-ruen-mai | 2019 年的 PDF | TAT 頁 |
| singapore-hill-street-kway-teow | STB 的 PDF，且沒提到這攤 | 移除 |

遷移 `0048_repair_merchant_citations` 把既有列的 `source_url`／type／scope／title／claims 一起改寫
（seeder 是用 URL 找既有列，只改常數會多出一列）；三家原本從 seed 複製來的
`official_website_url` 清掉，因為新來源都不是店家自己的站。`test_migration_dead_branches.py`
種一家店三條來源驗證改寫、刪除與不相干列不動。正式機 `fill-food-merchant-coordinates` 的
`fetch_failed／http_500／not_html` 在部署後看，補在下方。

2026-09-06 部署後：alembic head `0048_repair_merchant_citations`；`food_merchant_sources` 仍引用四條舊網址的列 0、
新加坡 PDF 那列已刪；`fill-food-merchant-coordinates` dry-run 的 outcomes 只剩 `no_source` 31、`http_403` 6、
`no_coordinates` 144、`would_fill` 1（→ `--apply` 填入），`fetch_failed`／`http_500`／`not_html` 都是 0。
