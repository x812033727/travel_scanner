---
id: 2026-09-13-password-policy-length-only
title: Password policy is length-only, so 1234567890 is accepted
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-14T00:50:33Z
created_at: 2026-09-13T23:37:54Z
completed_at: 2026-09-14T05:16:09Z
branch: claude/security-check-o5zaj1
depends_on: []
scope:
  - apps/api/app/auth/schemas.py
  - apps/api/tests/test_auth_hardening.py
  - apps/api/app/auth/passwords.py
  - apps/api/app/auth/router.py
  - apps/api/app/community/accounts.py
  - apps/api/app/i18n.py
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

- [x] A password on a common-password list is refused at registration, at change, and at
      reset, with a distinct error code the web app can translate (`password_too_common`).
- [x] The refusal message exists in all five locales.
- [x] Existing accounts are unaffected — this is a policy on new passwords, no forced reset.

## Steps

- [x] Picked a bundled list over a strength estimator: self-contained, no dependency, no
      outbound call. The list is curated rather than a ten-thousand-line blob — see below.
- [x] Enforced in one place. `reject_weak_password` in `app/auth/passwords.py`, called from
      `register`, `change_password` and `reset_password`.
- [x] A specific code, not the generic validation error: `validation_error`'s detail falls
      back to one generic sentence outside zh-TW, so the reader would be told to fix
      something without being told what.
- [x] Message added to `en`, `ja`, `ko`, `zh-CN` in `ERROR_DETAILS`; zh-TW comes from
      `AppError.detail`, which is how `app_error_handler` works and why the zh-TW dict
      deliberately carries only 129 of the 322 codes.
- [x] Rejecting a password built from the account's own email local part.

## What it refuses

A list alone fails the moment someone is told "no" and tries the next obvious thing, so the
structural rules carry most of the weight:

| Rule | Refuses |
| --- | --- |
| the list, case-folded and NFKC-normalised | `password`, `qwerty`, `mokaair`, full-width `１２３４５６` |
| list entry plus decoration | `password!!!`, `password123` — what a composition rule produces |
| fewer than 5 distinct characters | `aaaaaaaaaa` |
| a run along a keyboard row or the alphabet, either direction | `qwertyuiop`, `0987654321` |
| one short unit repeated | `abcabcabcabc`, `12341234` |
| contains the email local part (4+ chars) | `chihiro-market-lemon` for `chihiro@` |

And it has to let ordinary passphrases through, or people go back to `Password1!` and the
policy has made things worse. `correct horse battery staple`, `tuesday-market-lemon-pier`
and `私の犬は毎朝六時に吠える` all pass, and the test pins that.

## Why a curated list and not the top 10,000

The canonical SecLists URL 404s now, and committing a 100 KB word list fetched from a URL
nobody can re-verify is its own small supply-chain problem — in a repository that just spent
a commit pinning every GitHub Action to a SHA, that would be an odd thing to add.

The threat here is online guessing, bounded by `auth_login_account_limit` (10 per account per
15 minutes, ~1,000/day). A blocklist is not what defends against offline cracking — Argon2 is
— nor against credential stuffing, where the attacker already has the exact pair. So the list
is a floor: it refuses the passwords that get guessed first, and the structural rules cover
the shapes people reach for next. That is written at the top of `app/auth/passwords.py` so
the next reader does not mistake it for a strength meter.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_auth_hardening.py -q
npm run check:i18n
```

`test_every_password_entry_point_goes_through_the_same_gate` asserts against the source of
all three handlers rather than exercising them, because what actually goes wrong later is a
fourth entry point added without the call — which no test of the existing three would notice.

## Notes

- No composition rules, deliberately. "One uppercase, one digit, one symbol" produces
  `Password1!`, which is on every leaked list; NIST SP 800-63B advises against them for that
  reason, and this policy refuses that string explicitly.
- `min_length` stays at 10. The blocklist is in addition to the floor, not instead of it.
- **Scope overlap:** `apps/api/app/i18n.py` is also listed by `2026-09-12-food-merchant-enrichment`
  and `2026-09-13-klook-clickout-locale`, which already overlap each other there (`check:tasks`
  warns about it). This change adds four one-line entries next to `password_not_set` in four
  separate locale dicts, far from the `provider_locale` region those tasks work in, so a
  conflict is unlikely — but it is an overlap and it is recorded here rather than left to be
  discovered in a merge.
- The registration form's `passwordHint` in `apps/web/messages` still says only the length
  rule. It is not wrong, and the refusal itself is specific and localised, so this was left
  alone rather than widening the change into the web message catalogue.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
