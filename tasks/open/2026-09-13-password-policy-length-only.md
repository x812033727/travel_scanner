---
id: 2026-09-13-password-policy-length-only
title: Password policy is length-only, so 1234567890 is accepted
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-13T23:37:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/auth/schemas.py
  - apps/api/tests/test_auth_hardening.py
---

# Password policy is length-only, so 1234567890 is accepted

## Why

`apps/api/app/auth/schemas.py` is the whole policy:

```python
password: str = Field(min_length=10, max_length=128)
```

Ten characters and nothing else, so `1234567890`, `password12` and `qwertyuiop` all pass
at registration, at password change, and at reset.

Everything around this is already strong — Argon2 through `pwdlib`, a dummy hash so a
missing account and a wrong password take the same time, per-account and per-IP login
limits, `auth_version` invalidating every existing token when the password changes. Those
defences bound how fast someone can guess online. They do nothing about a password that
appears in the first thousand entries of any leaked list, because that one is guessed on
the first few tries, inside any rate limit.

`docs/security-audit-2026-09.md` filed this as API-12 and recommendation #8.

## Definition of done

- [ ] A password on a common-password list is refused at registration, at change, and at
      reset, with a distinct error code the web app can translate.
- [ ] The refusal message exists in all five locales.
- [ ] Existing accounts are unaffected — this is a policy on new passwords, not a forced
      reset.

## Steps

- [ ] Pick the mechanism. A bundled top-N list (the SecLists / Have I Been Pwned top 10k,
      shipped as a file and checked case-folded) is self-contained and adds no dependency
      and no outbound call. A zxcvbn-style strength estimator catches more but is a new
      dependency. Prefer the list unless there is a reason not to.
- [ ] Enforce it in one place. `RegisterRequest`, `ChangePasswordRequest.new_password` and
      the reset path must all go through it — a policy that holds at registration and not
      at reset is not a policy.
- [ ] Reject with a specific code (`password_too_common`), not the generic validation
      error, so the web app can say what is actually wrong.
- [ ] Add the message to all five locale files and run `npm run check:i18n`.
- [ ] Consider rejecting a password that contains the account's own email local part.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_auth_hardening.py -q
npm run check:i18n
```

Add cases for a common password at each of the three entry points, and one long unique
passphrase that must still be accepted — a policy that rejects good passwords is worse
than the one it replaced.

## Notes

- Do not add composition rules (an uppercase, a digit, a symbol). They push people toward
  `Password1!`, which is on every list, and NIST SP 800-63B advises against them for
  exactly that reason. A blocklist plus a length floor is the current guidance.
- Do not lower `min_length` while adding the list.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
