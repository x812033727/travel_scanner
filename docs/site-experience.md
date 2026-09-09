# Site experience and managed information pages

## Delivery boundaries

This release adds three palette families (mocha, lagoon and forest), each in light and dark mode, moves language controls to top headers, expands all reviewed card topics and separates reading sources into articles and videos. Empty introductions and coordinate-only fact sections render nothing. Data, moderation gates, provider costs and API identifiers are unchanged.

The original dirty checkout remains untouched. The feature branch starts at main `95122362`. This change does not merge, deploy, publish a policy, collect personal data or submit a paid provider request as part of verification.

## Information-page workflow

`/admin/site-pages` manages privacy, terms, about and contact in zh-TW, zh-CN, en, ja and ko. Readers need `settings.read`; initialization, editing, restoring and publishing need `settings.manage`. The API remains authoritative. General UI-text overrides cannot modify document bodies or published revisions.

Migration `0069_site_pages` creates page and append-only revision records, with fresh-database guards. It does not seed or publish content. The administrator's explicit **Create missing drafts in five languages** action initializes only missing slug/locale pairs, including full source-controlled drafts. Repeating it never overwrites edited or published content.

Drafts contain headings, paragraphs, lists and HTTP/HTTPS or simple mailto links, not arbitrary HTML or embeds. Each save, publication and restoration checks `expected_version`; a conflicting request preserves the editor's unsaved inputs. Changes and full revisions share a transaction with their audit entry. Restoring creates a new draft and never changes the public pointer.

Before publication, operators must fill the page's pending facts and an effective date that is not in the future, review the text and explicitly confirm publication with a reason. Facts are public document fields, not internal notes. The initial drafts deliberately do not invent an operator, location, public contact, retention schedule or legal arrangements. The software's completion check is not legal verification; the owner must confirm applicable requirements and review all language versions before publishing.

Public `GET /api/v1/site-pages/{slug}?locale=...` returns only the exact locale's published revision and `Cache-Control: no-store`. A missing publication is distinct from a service failure. SSR metadata and body share a request-scoped load, without stale cross-request caching, draft fallback or a different-language fallback.

## Appearance

`mokaair-theme` keeps the existing system/light/dark setting. `mokaair-palette` stores mocha/lagoon/forest independently. One root provider synchronizes all in-page controls and storage events; the nonce-protected prepaint bootstrap applies both before hydration. Invalid or unavailable storage falls back to system mode and mocha. The system preference changes brightness, not the selected color family.

The planner follows the site palette unless an existing valid `travel-planner-theme` selects one of its four custom palettes. The new follow-site choice preserves that opt-out. Brand wordmark colors, photographs and semantic error/success meanings remain distinct from the interactive palette. Functional borders and focus rings use their own opaque tokens; a pale primary in dark mode uses dark foreground text rather than forced white text.

## Interaction acceptance

Read-only dialogs close via X, Escape and backdrop, with only the top layer responding. Focus returns to the opener and body scrolling is restored after the last layer closes. Hidden links inside closed details are excluded from tab trapping; visible summaries remain reachable. Search suggestions close on outside click, focus exit and Escape without swallowing selection.

Dirty editors use a shared navigation guard before link navigation, language preference writes and browser Back. Planner confirmation keeps its existing draft flow; closing or navigating must not silently discard edits. Account action menus close on Escape/outside click and after selection.

## Verification record

Automated UI cases use explicitly synthetic localhost fixtures, not production users, venues, publication evidence or provider licensing proof. `site-experience.spec.ts` exercises all six palettes through actual controls and records desktop/Pixel 7 screenshots. `site-pages.spec.ts` verifies SSR publication states and isolated admin save/preview/publish/restore/dirty-return behavior. `discovery-card-details.spec.ts` keeps five-language source, image and full-topic coverage; the planner suite covers draft Browser Back.

Local checks and built-in browser observations are recorded in the task/PR when complete. PostgreSQL migration and full-stack jobs must be green in CI before this PR is considered ready; local SQLite tests alone are not production migration evidence.
