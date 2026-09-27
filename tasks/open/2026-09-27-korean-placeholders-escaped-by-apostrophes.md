---
id: 2026-09-27-korean-placeholders-escaped-by-apostrophes
title: Korean copy prints three placeholders literally, and check:i18n cannot see an apostrophe-escaped placeholder
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-27T05:59:56Z
completed_at:
branch:
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

- [ ] The three Korean strings print their values. Quote them with U+2018/U+2019, as
      `usage.packages.archiveConfirm` already does (`‘{name}’`).
- [ ] `check:i18n` fails on a placeholder that `en` substitutes and a locale prints
      literally, and the travelpayouts help (literal in `en` too) still passes.

## Steps

- [ ] Fix the three strings.
- [ ] In `tools/check-i18n.mjs`, compare parameters by what the message parser sees: format
      each message with `intl-messageformat` and a marker value per parameter, and flag a
      parameter whose marker does not appear. A literal in `en` stays allowed.
- [ ] Add `tools/check-i18n.test.mjs` (it has no test yet) with one escaped case, one
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

- Found on 2026-09-27 while adding Korean copy for the drama settings
  (`2026-09-27-video-drama-settings-ux`): the new Korean strings use `‘…’` for that reason.
- The scan that found them formats every message in every locale with a marker per
  parameter and reports the ones whose marker is missing from the output.
