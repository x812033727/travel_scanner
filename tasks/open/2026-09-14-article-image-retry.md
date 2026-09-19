---
id: 2026-09-14-article-image-retry
title: Article images recover from rate limits
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-14T00:37:36Z
completed_at:
branch: codex/article-image-retry
depends_on: []
scope:
  - apps/web/components/guides
  - apps/web/components/content-blocks.tsx
  - ops/nginx/10-rate-limit.conf
  - ops/nginx/mokaair.conf.example
  - ops/nginx/ci-validate.conf
  - ops/nginx/article-images.md
  - tools/test-guide-image-rate-limit.py
---

# Article images recover from rate limits

## Why

The user's existing Chrome page recorded HTTP 429 for all six intelligence covers on
2026-09-14. Failed images remain broken until reload. Both cards and article body images
share the page request bucket and lack transient-failure recovery.

## Definition of done

- [x] Local article images do not consume the SSR request budget; HTML remains limited.
- [x] Cards, hero and body images retry at most twice, including failures before hydration.
- [x] Regression checks pass and host activation steps are documented.
- [ ] Merge and separately activate the web release and enabled host nginx configuration.

## Steps

- [x] Implement scoped nginx exemption and bounded image retries.
- [x] Validate and record deployment boundary.

## How to verify

- From apps/web: `npx vitest run components/guides/guide-image.test.tsx components/guides/article.test.tsx components/content-blocks.test.tsx` — 91 passed.
- `npm run lint:web`, `npm run typecheck:web`, `npm run check:i18n` — passed.
- `npm run build:web` — passed, all 293 static pages generated.
- `python3 tools/test-guide-image-rate-limit.py /path/to/nginx` — passed using nginx 1.28.3 in WSL: config syntax, 120 images, preserved page budget and 7 non-image routes.
- `node tools/tasks.mjs check` — passed (existing stale/overlap warnings).
- Host rollout and rollback: `ops/nginx/article-images.md`. Neither host nor web production has been changed.

## Notes

The keepalive task is already present in origin/main but its deployment ticket still holds
the site template and CI harness in review. This user-authorized image fix only changes
the page limit zone references in those two files; its keepalive directives remain intact.
No production activation is included in this task's current authorization.

### 2026-09-19 補註

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

程式已隨 PR #470（2026-09-14 合併）和之後的部署上線。剩下的只有主機 nginx 設定的啟用；主機上是否已套用這次的 limit zone 引用沒有紀錄，接手時先比對 `/etc/nginx` 與 `ops/nginx`，改正式主機設定要站主同意。
