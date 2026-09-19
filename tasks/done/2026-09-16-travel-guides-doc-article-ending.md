---
id: 2026-09-16-travel-guides-doc-article-ending
title: Article anatomy in docs/travel-guides.md still ends with the other-language list
status: done
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:10:05Z
created_at: 2026-09-16T14:08:04Z
completed_at: 2026-09-19T11:16:56Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on:
  - 2026-09-16-news-date-field-and-news-list
scope:
  - docs/travel-guides.md
---

# Article anatomy in docs/travel-guides.md still ends with the other-language list

## Why

`2026-09-16-article-pages-stop-showing-the-other` removed the other-language section from the
bottom of every article, but "What a travel article looks like" in `docs/travel-guides.md`
still ends its anatomy line with "→ sources → other languages". The file was held by another
active task at the time, so the correction could not ride along with the code change.

## Definition of done

- [x] The anatomy line ends at the sources, and says where a translation is offered instead:
      `alternates.languages` in the head for crawlers, the header's language switcher for the
      reader, and the "not translated yet" screen for an article missing in this language.

## Steps

- [x] Edit the one line (`docs/travel-guides.md`, "What a travel article looks like").
- [x] Check no other paragraph in the file promises a language list under an article.

## How to verify

`grep -n "other languages" docs/travel-guides.md` finds nothing that describes the end of an
article.

## Notes

Waiting only on `docs/travel-guides.md` becoming free; there is no code to change.

### 2026-09-19 done in repo (claude-fable-5-1)

- The claim needed `--force`: `docs/travel-guides.md` is still held by
  `2026-09-13-adsense-ads-txt-drift`, which sits in `review` under the same owner although its
  pull request has merged and deployed.
- "What a travel article looks like" now ends its anatomy at the sources and says where a
  translation is offered instead: `alternates.languages` in the head for crawlers, the header's
  language switcher for the reader, and the "not translated yet" screen (`guides.notTranslated`
  in `article-page.tsx`) for an article missing in this language, which lists the languages that
  do have it; the sentence points at the Per-locale hreflang section below it.
- `grep -n "other languages" docs/travel-guides.md` finds nothing. The only other mentions of the
  language set (Per-locale hreflang) describe the head and the not-translated page, not a list
  under the article.
- Documentation only; nothing to import or deploy.
