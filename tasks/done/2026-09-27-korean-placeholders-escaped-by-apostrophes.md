---
id: 2026-09-27-korean-placeholders-escaped-by-apostrophes
title: Korean copy prints three placeholders literally, and check:i18n cannot see an apostrophe-escaped placeholder
status: done
priority: P2
area: web
owner: codex-gpt6-i18n
claimed_at: 2026-09-30T01:54:23Z
created_at: 2026-09-27T05:59:56Z
completed_at: 2026-09-30T01:59:44Z
branch: codex/korean-icu-placeholders
depends_on: []
scope:
  - apps/web/messages/ko/admin.json
  - apps/web/messages/ko/catalogReview.json
  - apps/web/messages/ko/hotspotThemes.json
  - tools/check-i18n.mjs
  - tools/check-i18n.test.mjs
---

# Korean copy prints three placeholders literally, and check:i18n cannot see an apostrophe-escaped placeholder

## Why

The web copy is ICU MessageFormat. An ASCII apostrophe right before `{` starts a quoted
literal, so `'{source}'` prints the text `{source}` instead of the value. Korean quotes a
word with `'...'`, and three Korean strings put that quote around a placeholder, so Korean
visitors and admins read a raw placeholder:

| File | Key | Renders |
| --- | --- | --- |
| `apps/web/messages/ko/admin.json` | `aiSettings.overview.inherits` | `{source}의 모델을 이어받음` |
| `apps/web/messages/ko/catalogReview.json` | `actionUnavailable` | `현재 {action} 작업을 할 수 없습니다` |
| `apps/web/messages/ko/hotspotThemes.json` | `intros.generateTitle` | `{name} 소개문 생성` |

`npm run check:i18n` passes all three: `tools/check-i18n.mjs` reads parameters with the
regex `/\{([A-Za-z_][\w]*)/g`, which does not know ICU quoting, so the parameter looks
present and the locale matches `en`. Nothing in CI can see this class of bug.

Not a bug: `providerFields.travelpayouts_static_url_template.help` escapes
`{destination}`, `{departure_date}`, `{return_date}` and `{sub_id}` in all five locales on
purpose. It documents the tokens of a URL template, so they must print literally.

## Definition of done

- [x] The three Korean strings print their values. Quote them with U+2018/U+2019, as
      `usage.packages.archiveConfirm` already does (`‘{name}’`).
- [x] `check:i18n` fails on a placeholder that `en` substitutes and a locale prints
      literally, and the travelpayouts help (literal in `en` too) still passes.

## Steps

- [x] Fix the three strings.
- [x] In `tools/check-i18n.mjs`, compare actual argument sets from the
      `intl-messageformat` AST, including every plural/select branch. A literal
      in `en` stays allowed. The AST approach replaces marker rendering; see Notes.
- [x] Add `tools/check-i18n.test.mjs` (it has no test yet) with one escaped case, one
      curly-quoted case and the travelpayouts case.

## How to verify

```bash
npm run check:i18n
node --test tools/check-i18n.test.mjs
```

Before the fix, this lists the three Korean strings (run from the repository root):

```bash
node -e 'const F=require("intl-messageformat").IntlMessageFormat;console.log(new F("\x27{source}\x27", "ko").format({source:"X"}))'
```

It prints `{source}`; with `‘{source}’` it prints `‘X’`.

## Notes

- 2026-09-30 collision audit: the claim tool reported two old review scopes.
  Withdrawal work landed in PR #870 (79e26fcd) and preloaded approval work in
  PR #978 (9656d0d9), both ancestors of origin/main. The latter's 31ce checkout
  has no tracked changes; the former branch no longer exists. No open PR changes
  any of this ticket's five paths. Used claim --force for these stale overlaps
  without changing either owner's task or branch.
- Use the IntlMessageFormat AST with ignoreTag: true to compare all actual
  argument names. This replaces the proposed marker rendering, which only
  visits one plural/select branch and cannot safely format numeric/date markers.
- Regression coverage: 19 tests, including all three actual Korean renders,
  reversal to the three original strings (exactly three failures), intentional
  URL-template literals in all five locales, nested plural/select/ordinal
  branches, number/date/time arguments, malformed ICU attribution, duplicate
  keys, namespace/allowlist/key validation and the real catalog CLI.
- No message keys or argument names change; admin text override keys remain valid.

- Found on 2026-09-27 while adding Korean copy for the drama settings
  (`2026-09-27-video-drama-settings-ux`): the new Korean strings use `‘…’` for that reason.
- The scan that found them formats every message in every locale with a marker per
  parameter and reports the ones whose marker is missing from the output.
