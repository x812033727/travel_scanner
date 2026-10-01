# Editing the site's copy from the admin panel

The frontend copy lives in `apps/web/messages/<locale>/<namespace>.json` — 22
namespaces, five locales, about 3,250 keys — and is bundled into the web image, so
changing a sentence used to mean a rebuild and a deploy. `ui_text_overrides` lets an
administrator replace individual sentences from the admin panel instead.

## How the two layers fit together

The JSON catalogs stay the versioned **defaults**. The database holds only
**overrides**: one row per namespace, key and locale, and nothing else. A missing row
means "show the catalog text", so an override written for zh-TW never leaks into en,
and dropping the row restores the default without a restart.

```text
admin  ── PUT / DELETE / batch ──▶  /api/v1/admin/ui-text  ──▶  ui_text_overrides
                                          │                          │
                                          └── after commit: delete ──┘  Redis ui-text:overrides:<locale>
                                                                            ▲
every page render: apps/web/i18n/request.ts ── GET /api/v1/runtime/ui-text?locale ──┘
       │
       └── JSON defaults + overrides ── copy-on-write merge ──▶ getTranslations / NextIntlClientProvider
```

The catalogs are kept on purpose. They are what `tools/check-i18n.mjs` checks in CI,
what the web server shows when the API is unavailable, what a pull request can review,
and the baseline every override is validated against. The database is a layer over
them, not a replacement.

## What can be edited

Every namespace of `apps/web/i18n/request.ts` except `legacy`. That namespace drives
`apps/web/components/legacy-ui-localizer.tsx`, which rewrites DOM text by literal zh-TW
string; an override there would change city names and trip titles coming back from the
API. It is refused in four places: the API allowlist (`UI_TEXT_NAMESPACES` in
`apps/api/app/ui_text/schemas.py`), a database `CHECK`, the web loader, and the editor.

Text that is not in a catalog cannot be edited here: the hardcoded Chinese still left
in a few dozen components, the dictionaries in `apps/web/lib/api.ts`, the problem
strings the BFF writes itself, and the API's own `ERROR_DETAILS`. Moving a string into
`messages/*` is what makes it editable.

## Validation on save

The API has no copy of the catalogs, so the editor sends the default text it is
overriding (`default_value`) with every write. The API keeps it as `default_snapshot`
and enforces, in this order:

- the value is not blank (`ui_text_value_empty`) — but it is **never trimmed**: dozens
  of defaults are separators such as `", "` whose surrounding space is the point;
- CRLF becomes LF and no other control character is allowed
  (`ui_text_value_control_chars`);
- both the override and its default parse as valid ICU messages
  (`ui_text_braces_unbalanced`), including nested plural/select branches. A missing
  `other` branch, duplicate selector or unknown argument format is a syntax error;
- runtime arguments retain their names and types in each branch, including plural
  offsets and `#` references (`ui_text_parameters_mismatch`). Reordering prose or
  repeating an argument in the same branch is allowed; moving it to another branch,
  changing a number to a date or dropping a selector is not;
- literal `{token}` URL-template names remain the same. These are extracted from
  parsed literal text separately from runtime arguments, so compact plural prose
  such as `one{hello}` is not mistaken for a parameter named `hello`.

ASCII apostrophes have ICU escaping semantics: `Hello '{name}'` prints the literal
`Hello {name}`, so it cannot override `Hello {name}`. Use curly quotation marks
(`Hello ‘{name}’`) or doubled ASCII apostrophes (`Hello ''{name}''`) to keep the
argument active. Ordinary contractions such as `You're {name}` remain valid.
Intentionally quoted URL tokens stay literal: Travelpayouts help can keep
`'{destination}'`, `'{departure_date}'`, `'{return_date}'` and `'{sub_id}'`.
Quoted standalone brace symbols such as `'{'` are also valid; raw brace counting
does not decide whether a message parses.

HTML-like help paths such as `<slug>` remain literal (`ignoreTag: true`); validation
does not add rich-text callbacks. Number/date/time presentation styles can change
while their argument types stay the same. The web uses the installed FormatJS
parser, and the API uses a pure Python syntax validator with the same contract.
`docs/ui-text-icu-cases.json` supplies shared acceptance and rejection cases to both
test suites; web tests also check the actual formatted text.

An empty value is not a delete. Restoring the default is an explicit `DELETE`, or
`"value": null` in a batch, so an accidentally cleared field cannot silently remove an
override. The web loader repeats the syntax, runtime and literal-template checks
against the live default when it merges. An invalid row already saved in the database
is skipped and the valid catalog default is displayed, including when the row comes
from an existing API cache. This change does not delete or rewrite saved rows.

## API

Public, anonymous, `Cache-Control: no-store`:

```text
GET /api/v1/runtime/ui-text?locale=<en|ja|ko|zh-TW|zh-CN>
→ { "locale": "en", "version": "<16 hex>", "entries": { "navigation.home": "Start", … } }
```

`version` is a content hash of every override in that locale, so it changes on add,
update and delete. Keys are flat `"<namespace>.<key>"`; namespaces never contain a dot.

Administrator routes (`AdminUser`), each returning the refreshed snapshot for the
locale and namespace it touched:

```text
GET    /api/v1/admin/ui-text?locale=en[&namespace=navigation]
PUT    /api/v1/admin/ui-text/{locale}/{namespace}/{key}   { "value", "default_value" }
DELETE /api/v1/admin/ui-text/{locale}/{namespace}/{key}   → 404 ui_text_override_not_found
POST   /api/v1/admin/ui-text/batch   { "locale", "namespace", "entries": [ { "key", "value"|null, "default_value" } ] }
```

A batch holds at most 100 entries, is validated in full before any row changes, and is
applied in one commit. Values are capped at 2,000 characters, defaults at 4,000, keys at
200 (`^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*$`).

## Cache and invalidation

The public payload is read on every server-side render, so each locale's payload is
cached in Redis under `ui-text:overrides:<locale>` for `UI_TEXT_CACHE_TTL_SECONDS`
(300 by default). **Every write deletes all five keys after its commit** — the first
administrator write in this codebase that invalidates a cache. The TTL is therefore a
safety net for a missed invalidation, not the propagation mechanism: a change is visible
on the next request. A Redis failure on read falls through to the database; a failure on
write or delete is logged and the TTL covers it.

## Audit

`ui_text_updated` (PUT and batch) and `ui_text_reset` (DELETE) are written to
`admin_audit_logs` with `target = ui-text:<locale>:<namespace>`. The metadata carries the
key and the before/after text (truncated to 500 characters); a batch lists every key
whose value actually changed, with `"after": null` for a restore. Both actions appear in
the provider-settings activity list and in the snapshot's own `audit` field.

## The editor

`/{locale}/admin/ui-text`, in the sidebar as 前台文案. Three things are in the query
string — `?ns=`, `?locale=` and `?ref=` — so a particular screen can be linked to and a
reload lands back on it. An unknown value falls back silently rather than redirecting, so
the selects always show what is actually in effect and a stale bookmark cannot bounce
between two URLs.

Defaults come from the page, not the API: it imports the one catalog being edited and
flattens it server-side. All five locales together are 3,418 sentences, and sending them
to the browser to edit twenty would be the wrong trade. The namespace picker also carries
each namespace's key count, which is free — `i18n/request.ts` has already imported every
catalog on the same request.

Each row shows the key, the default, the same sentence in a reference locale, and the
placeholders it has to keep. **An empty box means "use the default"**: a field that
trims to nothing is sent as `value: null`, the same delete the API's `DELETE` performs, so
restoring and editing are one path and the save bar counts them the same way. ICU syntax and
argument compatibility are checked as you type with the same rules the API applies, and the save button
turns into a count of what needs fixing while anything is wrong — next-intl renders the
raw key path when an argument it needs has gone, and that would land on the public page.

Saving goes through `POST /batch`, split into hundreds automatically. A failure re-reads
the snapshot and trims only the drafts that now match the server, so unsaved text stays in
the form and a half-applied save does not leave the screen lying about what is live.

Orphans — overrides whose key has left the catalog — are listed with everything else and
have a filter of their own. The loader skips them on every render, so this screen is the
only place they can be seen or cleared. `admin.json` alone holds 973 sentences, so the
list is searchable and paged fifty at a time.

## Web side

The loader lives in `apps/web/lib/ui-text.server.ts` and the merge in
`apps/web/i18n/request.ts`. The merge is copy-on-write — the imported JSON modules are
shared across requests, so mutating them would make "restore default" wait for a
restart — and it never creates a key: an override whose key left the catalog, or whose
placeholders no longer match the default, is skipped and shown as orphaned in the
editor. `tools/check-i18n.mjs` compares `UI_TEXT_NAMESPACES` with the catalog directory
so a new namespace cannot be added on one side only.
