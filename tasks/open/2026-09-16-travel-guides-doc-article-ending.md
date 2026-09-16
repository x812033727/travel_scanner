---
id: 2026-09-16-travel-guides-doc-article-ending
title: Article anatomy in docs/travel-guides.md still ends with the other-language list
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-16T14:08:04Z
completed_at:
branch:
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

- [ ] The anatomy line ends at the sources, and says where a translation is offered instead:
      `alternates.languages` in the head for crawlers, the header's language switcher for the
      reader, and the "not translated yet" screen for an article missing in this language.

## Steps

- [ ] Edit the one line (`docs/travel-guides.md`, "What a travel article looks like").
- [ ] Check no other paragraph in the file promises a language list under an article.

## How to verify

`grep -n "other languages" docs/travel-guides.md` finds nothing that describes the end of an
article.

## Notes

Waiting only on `docs/travel-guides.md` becoming free; there is no code to change.
