---
id: 2026-09-07-admin-controls-under-44px
title: The admin console's own tabs and pills are smaller than every control it publishes
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T09:25:06Z
created_at: 2026-09-07T09:25:06Z
completed_at: 2026-09-07T10:00:37Z
branch:
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/components/admin-analytics-panel.tsx
  - apps/web/e2e/readability.spec.ts
---

# The admin console's own tabs and pills are smaller than every control it publishes

## Why

Measured on production, signed in as an administrator:

| page | control | height |
|---|---|---|
| `/admin/analytics` | 重試 | 24px |
| `/admin/ui-text` | 全部 / 已覆寫 / 未儲存 / 有參數 / 孤兒覆寫 | 33px |
| `/admin/users` | 上一頁 / 下一頁 | 34px |
| `/admin/users` | 管理 | 37px |
| `/admin/hotspots` | six section tabs | 37px |
| `/admin/foods` | four section tabs | 37px |
| `/admin/analytics` | five range buttons | 36px |
| `/admin/settings` | six category tabs | 39px |

The public site holds 44px everywhere. The console did not, and the gap was invisible
because each panel wrote its own `py-2` rather than sharing anything.

The dashboard also showed `814 待審` at **2.34:1** in dark mode: a literal `#a84334` on
`--coral-soft`, which flips from a pale pink to a dark brown between themes. The
review-queue count is the number the console exists to show.

## Definition of done

- [x] Every control in the admin console is at least 44px tall.
- [x] The review badge passes 4.5:1 in both themes.
- [x] A panel added later inherits the floor instead of repeating the mistake.

## How to verify

`npx playwright test e2e/readability.spec.ts -g "admin console holds"`. Both halves were
checked in the failing direction: without the CSS floor it reports the five 36px range
buttons and the 40px refresh icon; without the token it reports 2.34, the same number
production gave.

## Notes

One rule under `.admin-page` rather than a dozen edits, with an `admin-inline-control`
opt-out for anything that genuinely has to be shorter. `min-height` on a `<button>` works
because buttons are inline-block.

The analytics 重試 was underlined text inside a sentence, not a button; the floor alone
would have made it a tall underline, so it became a bordered button.

`contrastOf()` in the spec is now shared by the sidebar case and this one.
