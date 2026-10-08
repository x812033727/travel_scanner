---
id: 2026-10-07-admin-deployment-panel-labels-the-release
title: Admin deployment panel labels the release_guard preflight check
status: done
priority: P3
area: web
owner: claude-deploy-copy
claimed_at: 2026-10-07T04:01:09Z
created_at: 2026-10-07T03:57:40Z
completed_at: 2026-10-07T04:01:10Z
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - apps/web/components/admin-deployments-panel.tsx
  - apps/web/components/admin-deployments-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Admin deployment panel labels the release_guard preflight check

## Why

#1360 gave the deployment agent's preflight a `release_guard` check (the deploy hold and a staged
release not yet activated). The admin deployment panel shows a check's name through its label
table (`labelKeys` in `admin-deployments-panel.tsx`), and a name missing from it is shown raw, so
the admin read `release_guard` as the heading of that card.

## Definition of done

- [x] The `release_guard` check has a label in all five locales and the panel shows it with the
      check's detail; the raw name is not shown.

## Steps

- [x] Add `release_guard` to `labelKeys` and `deploymentsPanel.labels.release_guard` to the five
      `admin.json` files; a panel test for a failed `release_guard` check.

## How to verify

`npm run check:i18n && npm run lint:web && npm run typecheck:web`, and
`cd apps/web && npx vitest run components/admin-deployments-panel.test.tsx`.

## Notes

- 2026-10-07, claude-deploy-copy: this replaces my own earlier version, which labelled a
  `release_hold` check from a parallel implementation of the deploy hold
  (2026-10-07-deployer-agent-honors-deploy-hold). #1360 landed that ticket first with
  `release_guard`, so the parallel implementation was dropped from #1361 and the label follows
  main's name. The five `admin.json` files are bound by the duration receipt, rebound by an
  independent reviewer in the next commit.
