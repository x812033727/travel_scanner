# Site experience and managed information pages

## Delivery boundaries

This release adds three palette families (mocha, lagoon and forest), each in light and dark mode, moves language controls to top headers, expands all reviewed card topics and separates reading sources into articles and videos. Empty introductions and coordinate-only fact sections render nothing. Data, moderation gates, provider costs and API identifiers are unchanged.

The original dirty checkout remains untouched. The feature branch starts at main `95122362` and incorporates main `d9ef8fcd`, preserving the intervening Stay22 integration and first-click/retry fixes. This change does not merge this PR, deploy, publish a policy, collect personal data or submit a paid provider request as part of verification.

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

Dirty editors use a shared navigation guard before link navigation, language preference writes and browser Back. This also covers the stored language preference arriving asynchronously from the shared login-state request; cancelling it preserves both the draft and the authenticated session without changing the locale cookie. Planner confirmation keeps its existing draft flow; closing or navigating must not silently discard edits. Account action menus close on Escape/outside click and after selection.

The native-history dispatcher belongs in the root parser-blocking nonce script, before Next initializes its own history listener. It contains no user data and delegates only to currently active draft guards. Do not replace that ordering with a late capture-only effect: the isolated Chromium timeline reproduced a native traversal that reached the router without invoking that capture listener, even though a jsdom-dispatched event passed. A compatibility bootstrap in isolated component tests is not proof of the production ordering; keep the same-document browser regression cases.

## Verification record

Automated UI cases use explicitly synthetic localhost fixtures, not production users, venues, publication evidence or provider licensing proof. `site-experience.spec.ts` exercises all six palettes through actual controls and records desktop/Pixel 7 screenshots. `site-pages.spec.ts` verifies SSR publication states and isolated admin save/preview/publish/restore/dirty-return behavior. `discovery-card-details.spec.ts` keeps five-language source, image and full-topic coverage; the planner suite covers draft Browser Back.

Local checks and built-in browser observations are recorded in the task/PR when complete. PostgreSQL migration and full-stack jobs must be green in CI before this PR is considered ready; local SQLite tests alone are not production migration evidence.

### Current verification and remaining acceptance

- Validated code revision: `470d16d6dea750f1643e7745f94652d6c47daa99`. [Full CI](https://github.com/x812033727/travel_scanner/actions/runs/34357389559) and the planner/discovery workflows passed: 2,805 API cases (15 skipped), 1,445 Web unit cases and 376 isolated browser cases (4 skipped), with Ruff, mypy, fresh/upgrade PostgreSQL migrations, TypeScript, lint, i18n, production builds, containers and full-stack workflows. Subsequent documentation-only commits do not change this implementation; current-head checks are linked from the PR.
- The native same-document Back regression is resolved: both accept/cancel cases pass on desktop and Pixel 7, including the chosen destination and retained draft assertions. The eight-width topbar checks also pass. All twelve final palette screenshots were visually inspected. [Final-code automated screenshots](https://github.com/x812033727/travel_scanner/actions/runs/34357389559/artifacts/10106686351) are synthetic CI captures, not built-in-browser manual evidence.
- **Only manual acceptance remains open:** an approved isolated preview is needed for the built-in-browser checks below. Policies remain unpublished, and the PR remains a draft without merge or deployment.

Earlier checkpoints are retained below for traceability; their subsequently fixed failures are not current open regressions:

- PR: https://github.com/x812033727/travel_scanner/pull/380 (draft; no merge or deployment).
- Local production webpack build/TypeScript completed; subsequent fixes are checked against the current head in CI. Latest local full ESLint and five-language checks passed.
- Local focused evidence: initial API 86 passed / 18 skipped; CMS/discovery 50 passed; publication-only rendering/loader 20 passed; shared overlays/navigation/mobile 36 passed; managed metadata 41 passed; root-provider page fixtures 9 passed; palette tokens and fill-gradient checks 24 passed.
- The complete planner unit file passed 62 cases on an independent rerun. An earlier complete run had one non-reproduced busy-close failure; this is not erased from the record. An earlier worker-start timeout occurred under severe local RAM pressure, not as an application assertion.
- CI on `488c49d4` passed the complete API suite, Ruff, mypy, existing-database and new site-page PostgreSQL migration checks, Web unit tests, TypeScript, lint, five-language validation and production build. Planner/discovery browser acceptance, full-stack admin workflows and production container builds also passed. The broader browser suite exposed registry fixture expectations, CSS color parsing, a compact language control's touch area and an asynchronous stored-language navigation bypass; follow-up fixes retain the original assertions. Current-head full CI is still required.
- After synchronizing main, [CI on `b18786fc`](https://github.com/x812033727/travel_scanner/actions/runs/34350586621) passed all jobs: 2,783 API cases (15 skipped), 1,416 Web unit cases and 360 isolated browser cases (4 skipped), alongside fresh/upgrade PostgreSQL migrations, containers and full-stack workflows. Its twelve desktop/mobile palette screenshots were visually inspected; these are automated fixture captures, not built-in-browser manual acceptance.
- Additional same-document, multi-entry browser Back tests on `62def3cd` exposed four failures despite ordinary Back coverage passing. Keep the assertions and use test-only history timelines to diagnose the lifecycle before claiming the draft guard complete. API, containers and full-stack checks on that head passed. The inspected desktop CMS capture also exposed intrinsic-size topbar overlap; a responsive fix now has eight-width geometry coverage awaiting CI.
- [Diagnostics on `c5438391`](https://github.com/x812033727/travel_scanner/actions/runs/34354138812) passed 362 browser cases (4 skipped) including all eight topbar widths, but retained the four same-document Back failures. All four timelines show the enabled capture listener was not invoked for native traversal, while Next's bubble listener navigated first; cleanup happened afterward. This is not evidence of a CMS refetch or a stale auth preference. A parser-blocking, nonce-protected history bridge is being added before router initialization; it forwards only to active guards and leaves unguarded navigation untouched. Current-head native browser proof is required before marking this resolved. [Automated screenshots and diagnostic traces](https://github.com/x812033727/travel_scanner/actions/runs/34354138812/artifacts/10105459199) include synthetic documents only; the four new topbar screenshots were visually checked.
- The local preview server launch was rejected by execution policy. Therefore **no new-palette built-in-browser desktop/Pixel 7 audit is claimed yet**. Automated palette screenshots and composite contrast results are produced by the isolated CI browser suite; they are not production data or manual browser evidence.
- Remaining manual acceptance: six palette views at desktop/Pixel 7 sizes, large text, nested modal/touch close flows and read-only visits across public tools, community, pet-friendly and account pages. Use an approved isolated preview; do not perform production writes or metered actions.

The sampled thresholds follow [WCAG text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). Token calculations alone do not establish whole-site conformance; rendered alpha layers, functional borders and focus states must also be checked.

### Frontend inspection checklist

This is a coverage inventory, not a claim of completed manual acceptance. The new/expanded UI suites are `navigation`, `readability`, `site-experience`, `site-pages`, `discovery-card-details` and `planner-premium`. Separate existing full-stack suites exercise additional community and admin flows; neither set substitutes for the requested built-in-browser inspection.

| Area | Automated coverage in these UI suites | Remaining isolated-preview inspection |
| --- | --- | --- |
| Home | Five locales, top language/query preservation, mobile navigation, one auth request, font size and menu focus | Desktop/phone first paint, long copy, touch and maximum font size |
| Explore | Full topics, image/empty states, five-language details, safe grouped sources, Escape/focus/URL restoration | Real published content lengths, failed images, X/backdrop/Back/reopen sequence |
| Saved | Saved entry and empty-state fixtures; shared child-dialog contract | Full saved-list view and return path; mutations only against test fixtures |
| Trips | Manual create/edit/reorder/undo/reload, AI preview/cancel/explicit apply, nested tools, dirty Back | Soft keyboard, long itinerary, touch drag and nested windows; no production save/AI/route request |
| Travel tools | Preserved queries, sign-in continuation/idempotency, cost gates and synthetic search/comparison results | Read-only disclosure/tab/close behavior, flight-status entry and error states; no paid live query or booking |
| Community | Shared dialog contract, not a community page journey in these six suites | Public feed/post/profile and translation-entry states; posting/messaging only on isolated test services |
| Pet friendly | No direct pet-page journey in these six suites | Visibility gate, filters, unknown conditions, sources and detail close; reports/trip additions only on isolated fixtures |
| Login | Error state, email retained/password cleared, return query and maximum-font layout | Keyboard/password reveal/Back; successful auth, reset and verification mail only with test accounts |
| My/account | All six palettes through actual controls, contrast/focus samples, persisted and system preferences | Account menus, sign-out and setting windows; no changes to real credentials or personal data |
| Information/CMS | Exact-locale metadata, unpublished/unavailable states, read-only permissions, synthetic revision workflow and native multi-entry Back | Long editor/touch controls and human document review; no real publication |

For every manual row, use desktop and Pixel 7 dimensions, keyboard and touch, large text, both brightness modes, nested layers and service-error states. Record the preview URL/commit, observed result and screenshot before checking a row complete. When a module is disabled, inspect its unavailable state without changing production settings. Shared jsdom dialog tests mock native `showModal`; they establish component contracts, not browser top-layer behavior.
