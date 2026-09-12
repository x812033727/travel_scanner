---
id: 2026-09-11-guides-sitemap-and-entry-points
title: Wire /guides into the sitemap, footer and destination pages
status: done
priority: P2
area: web
owner: claude-opus-5-guides
claimed_at: 2026-09-11T17:07:17Z
created_at: 2026-09-11T15:47:19Z
completed_at: 2026-09-11T23:31:27Z
branch: claude/travel-info-guide-section-4ulqsj
depends_on: []
scope:
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
  - apps/web/components/destination-guide.tsx
  - apps/web/components/destination-guide.test.tsx
  - apps/web/lib/discovery-copy.ts
  - apps/web/lib/destinations-copy.ts
  - apps/web/e2e/seo.spec.ts
  - docs/seo.md
---

# Wire /guides into the sitemap, footer and destination pages

## Why

`/guides` shipped in PR #398, but four pieces were left out because their files were held by
`review` tasks whose pull requests had already merged. Without the sitemap the article pages
are not discoverable at all; the API has served `GET /guides/sitemap`, the publication-aware
list, since #398 for exactly this.

## Definition of done

- [x] The sitemap lists the guide hubs and every published article, each only in the locales
      where it is published, and an expired notice drops out of it.
- [x] The footer and each destination page link to the guides.
- [x] Discovery's label for external articles no longer shares the new section's name.

## Steps

- [x] `guideSitemapEntries()` in `lib/guides.server.ts`, plus three static routes and the
      article entries in `app/sitemap.ts`.
- [x] Cases in `app/sitemap.test.ts` and `lib/guides.server.test.ts`.
- [x] Footer link and destination-page cross-link.
- [x] Relabelled `kinds.article` and `collectionGuide` in every locale of `lib/discovery-copy.ts`.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run build:web
```

End to end against a real stack (no docker daemon in the web container; `/usr/lib/postgresql/16/bin`
and `redis-server` are installed):

```bash
su postgres -c "initdb -D /tmp/pgdata -U travel --auth=trust && pg_ctl -D /tmp/pgdata -o '-k /tmp' start"
redis-server --daemonize yes --save ''
cd apps/api && uv run alembic upgrade head && uv run uvicorn app.main:app --port 8000 &
cd apps/web && API_INTERNAL_URL=http://127.0.0.1:8000 npx next start -p 3000 &
curl -s http://localhost:3000/sitemap.xml
```

## Notes

**Two safety assertions were narrowed, not deleted.** Both are in `app/sitemap.test.ts` and
both break on article entries for the same underlying reason — the section publishes one
locale at a time:

- *"publishes no lastmod at all"* → *"…for the routes whose update date it cannot know"*. The
  original comment is true of a city guide (its content lives behind an API the route
  deliberately does not call) and false of an article, where the API returns the real
  publication date. For a dated notice that signal is the point of the section.
- *"gives every entry all five locales plus x-default"* → *"every **static** entry…"*.
  Requiring five of an article would force the sitemap to advertise translations nobody wrote,
  which is the one thing per-locale publication exists to prevent.

Each carries a comment saying why the rule holds for static routes and not for articles.
Mocking `guideSitemapEntries` to `[]` by default is what keeps every other assertion in the
file — including the whole-array comparison — passing unchanged.

**Malformed-row filtering is tested in `lib/guides.server.test.ts`, not the sitemap test.**
It happens inside the loader, and the sitemap test mocks that loader, so a case there would
have asserted nothing about the code that does the work.

**`destination-guide.tsx` must stay synchronous.** Its copy comes from `destinations-copy.ts`,
so the three new keys went there. Making it `async` to reach `getTranslations` would break
`app/[locale]/destinations/[destinationId]/page.test.tsx`, which renders it through
`render(await Page(...))` and is not in this scope.

**Scope additions:** `lib/destinations-copy.ts` (above) and `lib/guides.server.ts` plus its
test (the loader lives there). The board was at 0 in review, so both were free — no `--force`.

**Verified against a real stack, not only mocks:** an article published in zh-TW and ja with a
Korean draft left unpublished produced exactly three sitemap entries, each with the real
`lastmod` and alternates matching only its own published locales; the Korean draft never
appeared. Setting `valid_until` to yesterday removed the notice from the sitemap while its URL
kept answering 200 and rendered the dated expiry banner.

**收尾（#404 已合併，commit d14a989）。** 開票時 `e2e/seo.spec.ts` 與 `docs/seo.md` 不在
scope 裡，結果 CI 上 `web` 紅了：`seo.spec.ts:64` 寫死 `toHaveLength(365)`，而三個新的
`/guides` 樞紐 × 五語系多出 15 個 URL。兩個檔案都補進 scope 後才改：數字改寫成
`5 * (10 + 33 + 33)` 並註明來源，`docs/seo.md` 一併更正三處不再成立的敘述——其中
「Managed document URLs remain outside the sitemap until publication-aware enumeration is
implemented」與「No artificial `lastmod` is emitted」都已被這次改動推翻，還把舊稱呼
「33 guides」改成「33 destination guides」以免與新專區混淆。

**教訓：改動 `SITEMAP_ROUTES` 會牽動兩個寫死的數字**，一個在 e2e、一個在文件裡。
下次動那張路由表的人，把這兩處一起看。

**中途撞到一個與本任務無關的 CI 中斷**：MinIO 在 Docker Hub 上的公開映像不再開放匿名
拉取，`api` 與 `full-stack-smoke` 因此全紅。那是另開 #407／#409 處理的，不屬於這張票；
記在這裡只是說明為什麼這張票的 CI 中間紅過而與 diff 無關。
