---
id: 2026-09-10-account-mail-reply-to
title: Automated account mail has no Reply-To, so user replies reach nobody
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-10T17:06:12Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/config.py
  - apps/api/app/community/jobs.py
  - apps/api/tests/test_community_foundation.py
  - docs/contact-channels.md
---

# Automated account mail has no Reply-To, so user replies reach nobody

## Why

`send_mail` in `apps/api/app/community/jobs.py` sets `Subject`, `From` and `To` and
nothing else. `From` is `COMMUNITY_MAIL_FROM`, which the owner has confirmed as
`support-noreply@mokaair.com` — a send-only mailbox (see
[`docs/contact-channels.md`](../../docs/contact-channels.md)).

So every email verification, password reset and account-deletion confirmation invites
a reply that nobody will ever read. The people most likely to reply are exactly the
ones already in trouble: the link expired (30 minutes, single use), or they did not
request the mail at all and want to report it.

The published documents tell readers to write to `support@mokaair.com`, but a reply in
a mail client goes wherever the headers point, not where a policy page says.

## Definition of done

- [ ] Replying to any automated account mail reaches `support@mokaair.com`.
- [ ] The reply address is configuration, not a literal in the code, and an unset
      value sends mail with no `Reply-To` rather than a broken one.
- [ ] A test asserts the header on a built message, so the next sender change cannot
      silently drop it.

## Steps

- [ ] Add a `community_mail_reply_to: str = ""` setting next to `community_mail_from`
      in `apps/api/app/config.py`.
- [ ] Set `email["Reply-To"]` in `send_mail` when the setting is non-empty.
- [ ] Cover it in `apps/api/tests/test_community_foundation.py` alongside the existing
      mail-configuration cases: set, unset, and the header's exact value.
- [ ] Drop the "reply gap, still open" workaround paragraph from
      `docs/contact-channels.md` and document the new variable instead.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_community_foundation.py -q && uv run ruff check . && uv run mypy app
```

## Notes

Filed while publishing the owner's two confirmed mailboxes into the information-page
drafts (`2026-09-06-legal-content-from-owner`). The fix was not done there because
`apps/api/app/config.py` was held at the time by
`2026-09-09-configurable-catalog-review-run-call-limit`; nothing else blocks it.

Do not "fix" this by making `COMMUNITY_MAIL_FROM` the public `support@` mailbox. The
sender and the reply address are deliberately different: automated mail must be
identifiable as automated, and the public mailbox should not be the envelope sender
for bounce traffic.
