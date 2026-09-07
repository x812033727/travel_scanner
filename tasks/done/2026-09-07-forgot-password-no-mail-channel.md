---
id: 2026-09-07-forgot-password-no-mail-channel
title: 登入頁沒有忘記密碼，後端也沒有任何寄信管道
status: done
priority: P1
area: web
owner: codex-community
claimed_at: 2026-09-07T10:14:20Z
created_at: 2026-09-07T01:46:13Z
completed_at: 2026-09-07T15:32:49Z
branch: codex/mokaair-community
depends_on: []
scope:
  - apps/web/app/[locale]/login
  - apps/web/components/auth-form.tsx
  - apps/web/components/auth-form.test.tsx
---

# 登入頁沒有忘記密碼，後端也沒有任何寄信管道

## Why

Members who forget their password need a safe recovery entry. The community
foundation now provides durable SMTP, hashed single-use reset tokens and revocation.

## Definition of done

- [x] The login page links to the localized recovery flow without revealing account existence.

## Steps

- [x] Connect the login entry and verify it with the community account-safety flow.
- [x] Validate real SMTP delivery and single-use reset in the full-stack acceptance environment.

## How to verify

Run the auth-form and community component tests, then request a reset through
the localized login entry with Mailpit/SMTP enabled. Follow the received link,
change the password once, and verify old sessions and replayed links are rejected.

## Notes

The localized entry, generic reset response, encrypted durable mail job and
fragment-based confirmation route are implemented in the community worktree.
Component tests and the real Mailpit/SMTP desktop and Pixel 7 reset/deletion
journeys passed in CI 34137517824 at 43d0481. This covers token replay rejection,
old-session revocation and immediate profile hiding. Production SMTP delivery
remains an operator launch gate in docs/community.md; no production service is enabled.
