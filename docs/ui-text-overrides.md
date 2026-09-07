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
- braces are balanced (`ui_text_braces_unbalanced`) — seven English defaults use ICU
  plural syntax, and a plural missing its closing brace would render as the raw key;
- the set of `{placeholder}` names equals the default's (`ui_text_parameters_mismatch`),
  extracted with the same expression `tools/check-i18n.mjs` uses.

An empty value is not a delete. Restoring the default is an explicit `DELETE`, or
`"value": null` in a batch, so an accidentally cleared field cannot silently remove an
override. The web loader repeats the placeholder check against the live default when it
merges, so this validation protects the person typing; the loader protects the page.

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

## Web side

The loader lives in `apps/web/lib/ui-text.server.ts` and the merge in
`apps/web/i18n/request.ts`. The merge is copy-on-write — the imported JSON modules are
shared across requests, so mutating them would make "restore default" wait for a
restart — and it never creates a key: an override whose key left the catalog, or whose
placeholders no longer match the default, is skipped and shown as orphaned in the
editor. `tools/check-i18n.mjs` compares `UI_TEXT_NAMESPACES` with the catalog directory
so a new namespace cannot be added on one side only.
