---
id: 2026-09-30-zh-cn-uses-the-taiwan-word
title: zh-CN uses the Taiwan word 备援 in nine published articles; replace it by context
status: done
priority: P3
area: docs
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T13:00:15Z
created_at: 2026-09-30T12:23:51Z
completed_at: 2026-09-30T13:04:56Z
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/web/public/guides/tech-news-taiwan-matsu-cable-20260623
  - apps/web/public/guides/tech-news-taiwan-matsu-cable-tm4-20260918
  - docs/tech-news-2026/research/tech-news-taiwan-matsu-cable-20260623.json
  - docs/tech-news-2026/research/tech-news-taiwan-matsu-cable-tm4-20260918.json
  - docs/news-2026-batch-4/translation-corrections.json
  - apps/api/app/guides/content/ai-news-claude-fable-5-access-20260609.json
  - apps/api/app/guides/content/ai-news-claude-opus-55-20260922.json
  - apps/api/app/guides/content/ai-news-gpt-6-sol-luna-20260923.json
  - apps/api/app/guides/content/ai-news-nvidia-rubin-20260105.json
  - apps/api/app/guides/content/codex-agents-md-scopes.json
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/api/app/guides/content/tech-news-taiwan-6g-spectrum-20260910.json
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-20260623.json
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-tm4-20260918.json
---

# zh-CN uses the Taiwan word 备援 in nine published articles; replace it by context

## Why

The zh-CN reviewer of batch 4.10 (2026-09-30) flagged 「备援」 as Taiwan usage; mainland readers
write 回退／回退机制 (a model or system falling back), 冗余 or 备份 (redundant cables and links)
depending on the sense. It appears 44 times in the zh-CN locale of nine published packs.

## Definition of done

- [x] Each occurrence replaced by the word its context needs (fallback → 回退机制; redundancy →
      冗余; backup → 备份), zh-CN only, zh-TW untouched.
- [ ] `pack_cli lint` clean and the changed packs re-imported with `guides-import --slug`.

## Notes

- Not a find-and-replace: the Matsu cable articles mean redundancy, the model articles mean
  fallback.
- Done 2026-09-30. 44 occurrences (not 43): 36 replaced by context, 8 kept.
  - Rules: model or automatic model switch → 回退机制; architecture node → 冗余节点; degradation
    plan → 后备方案; Codex fallback filenames → 备用文件名／备用清单; cables and microwave →
    备用线路, 微波备用通信, 冗余 (three routes, the whole network), 备份 (the extra layers).
  - Kept: direct quotes of the publishers' own words in quotation marks (“备援再备援” twice,
    “三路由互为备援” twice, “互为备援”) and the official press-release titles in `sources[]` (3).
  - New zh-CN titles: 「…马祖通信备用线路现况」 and 「…三路由冗余与 1.9 Tbps」; the four
    links to them realigned with `align_links.py --apply --only=…`.
  - zh-TW untouched in every pack (compared after parsing). The two cable articles' zh-CN
    hero and diagram re-rendered; the other locales' hero JPGs, which this container
    re-renders with different bytes, were restored to what was published.
- Seen, not done: `align_links.py` also reports 5 stale ja/ko link texts in the AI index
  (targets retitled earlier); and `codex-agents-md-scopes` zh-CN still has other Taiwan words
  (档名, 专案, 资料夹). Both belong to separate tasks.
- Publish: `guides-import --slug` for the nine packs, dry run first.
