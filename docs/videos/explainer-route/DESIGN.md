# Explainer route takes a series' look: design for three pull requests

Ticket: `tasks/open/2026-10-10-explainer-route-takes-a-series-look.md`. Decisions:
[`DECISIONS.md`](DECISIONS.md). Synthesized 2026-10-11 from three work orders and their
critiques; the orders ([`orders/order-pr1.json`](orders/order-pr1.json),
[`order-pr2.json`](orders/order-pr2.json), [`order-pr3.json`](orders/order-pr3.json)) keep the
full reasoning and the measured digests, and this document overrides them wherever the two
differ. The critiques (`critique-pr{1,2,3}.json`) and the prototypes were scratch files of the
design session and are not in the repository: section 8 lists what each critique changed. In
the copied orders `<scratch>` stands for that session's scratch folder and `<repo>` for the
checkout; a path under `<scratch>` that is not named below was not kept.

**Baseline.** Every site below was re-read at `88d7177af` (origin/main, 2026-10-11). Orders 1
and 2 were written at `599835f49`, order 3 and the critiques at `6a26eff42`; between `6a26eff42`
and `88d7177af` only `docs/videos/sothatswhy-b26/**` and `tasks/**` changed, so every code line
number here is valid at both. Line numbers are a convenience: **find each site by its quoted
statement**, and re-check after every rebase.

## 1. Overview

| PR | What lands | A user can afterwards | Cannot yet |
| --- | --- | --- | --- |
| 1 | `cute-cartoon` and `cute-mystery` exist in tools, API (CHECK constraints) and web labels; "is an explainer" (family) is split from "whose identity" | see the two names in the settings tab's default-style list; nothing else | file a cute request from the site (the request form still offers five presets) |
| 2 | a one-off explainer request may name its image model; cute presets are stored with `image-01`; a model whose vendor has no key is refused at filing | pick an image model for a `flat-explainer` request | pick a cute preset in the form (the field's cute behaviour is built and unit-tested, shown from PR 3) |
| 3 | each cute preset is planned, written, checked and discussed from its own series' prompts; the form offers both | file a 原來如此事務所 (`cute-cartoon`) or 奇聞檔案局 (`cute-mystery`) explainer on the host | get `screenshot`/`photo` cards, a series-own intro/thumbnail for 奇聞檔案局, or accept-best pictures (follow-ups) |

Rules that hold for all three:

- **`flat-explainer` does not move by one byte** (owner's decision 4): preset text, prompt text,
  payloads, look hash, image keys, durable stage keys, unfinished journals.
- **No pull request edits a file that `prompts.mjs references()` reads into a payload**:
  `.agents/skills/youtube-video/references/{drama.md,series.md,script-writing.md,formats.md}`,
  `docs/videos/README.md`, `tools/video/core/fixtures/{drama,minimal}/*`,
  `tools/video/templates/fixtures/showcase/video.json` (`prompts.mjs` 16, 34-44:
  `drama: read(SKILL, "drama.md")`). One changed byte there moves the durable key of every
  unfinished drama-format stage (`video_ai_receipt_input_changed`). Documentation goes to
  `docs/videos/DRAMA.md` and `docs/videos/DRAMA-FLOW.md`, which no payload reads and the receipt
  does not bind. Also untouched: `tools/video/long-form/{plans.mjs,admin-catalog.mjs}`,
  `docs/videos/long-form/plans.json` (the 192 planned episodes stay on `flat-explainer`).
- **The request form holds the cute presets back until PR 3.** PR 1 and PR 2 leave
  `REQUEST_PRESETS` at five values; PR 3 adds the two. Between PR 1 and PR 3 a cute request can
  only come from a direct API call (do not make one: it would be written from So That's Why's
  prompts, and before PR 2 drawn by Gemini at 2K).
- Web, API and tools of one pull request ship in one deploy; landing order 1, 2, 3.
- **Duration receipt**: the implementer never edits `docs/videos/long-form/review.json` or
  `review.md`. After each pull request is pushed, an agent that did not write it adds a
  `DURATION_ONLY` increment for that pull request's bound files on top of the receipt as it then
  stands on main, and runs `node tools/video/long-form/cli.mjs check`. `review.test.mjs` is red
  until then. One increment per pull request.
- Do not pipe a check through `tail`. Run `npm run test:tools` whole at least once per pull
  request (the designers' scratch runs of `automation.test.mjs` timed out without a failure).

### Recorded as decided (owner accepted, critique kept all five)

1. `steps` and `table` cards for the two cute presets only (`flat-explainer` keeps its six).
2. The nine yes/no picture checks and the picture-variety lint for the cute presets.
3. `settle()` keeps only `{ preset }` of a cute look (a writer's style/negative is dropped).
4. `genre_spec: null` in a cute bible's planner payload.
5. One discussion variant per series (`discuss-cartoon`, `discuss-mystery`).

## 2. Names (one name per thing, across the three pull requests)

| Thing | Name | Lives in | PR |
| --- | --- | --- | --- |
| family list, tools | `EXPLAINER_PRESETS` (frozen array of three) | `tools/video/core/drama.mjs` | 1 |
| family test by preset name | `isExplainerPreset(preset)` | same | 1 |
| family test on a document | `isExplainer(doc)` (existing, rebuilt on the above) | same | 1 |
| identity on a document | `explainerSeries(doc)` -> `"sothatswhy"` or `null` | same | 1 |
| identity table (private) | `EXPLAINER_IDENTITY` (order 1 called it `EXPLAINER_SERIES`; renamed so it cannot be confused with PR 3's registry) | same | 1 |
| legacy constant | `EXPLAINER_PRESET` stays exported, compared nowhere | same | 1 |
| family, API | `EXPLAINER_PRESETS: tuple[StylePreset, ...]`, `is_explainer_preset(preset)`; `EXPLAINER_PRESET` removed | `apps/api/app/video_automation/schemas.py` | 1 |
| family, web | `EXPLAINER_PRESETS`, `isExplainerPreset(preset: string)` | new `apps/web/lib/video-presets.ts` | 1 |
| form bounds | `requestMinutes(preset)` | `apps/web/components/admin-video-series.tsx` | 1 |
| cute default model, API | `PRESET_IMAGE_MODELS` | `schemas.py` | 2 |
| cute default model, web | `PRESET_IMAGE_MODEL` | `apps/web/lib/video-presets.ts` | 2 |
| vendor a named model is asked of | `series_image_vendor(row, model_id)` | `apps/api/app/video_media/jobs.py` | 2 |
| catalogue list for a picker | `imageModelOptions(options)` | `apps/web/components/admin-video-settings.tsx` | 2 |
| form's image-model state | `requestImageModel(preset, choice, models)` | `admin-video-series.tsx` | 2 |
| cute subset | `CUTE_EXPLAINER_PRESETS`, `isCuteExplainer(doc)` | `tools/video/core/drama.mjs` | 3 |
| cards per preset | `explainerCardTemplates(preset)`, `CUTE_EXPLAINER_CARD_TEMPLATES` | same | 3 |
| preset -> variants (the one table) | `EXPLAINER_VARIANTS`, `explainerVariants(preset)`, `isExplainerStageVariant(variant)`, `EXPLAINER_DISCUSS_VARIANTS` | new `tools/video/automation/explainer-series.mjs` | 3 |
| series profile registry | `EXPLAINER_SERIES_PROFILES`, `explainerProfile(preset)`, `EXPLAINER_SERIES_INSTRUCTIONS` | same | 3 |
| discussion variant pickers | `documentDiscussVariant(series)`, `scriptDiscussVariant(state)` | `tools/video/automation/discuss.mjs` | 3 |

Variant names: `flat-explainer` -> `bible-explainer` / `explainer` / `discuss` (as today);
`cute-cartoon` -> `bible-explainer-cartoon` / `explainer-cartoon` / `discuss-cartoon`;
`cute-mystery` -> `bible-explainer-mystery` / `explainer-mystery` / `discuss-mystery`.

Site dispositions (every comparison found by `git grep` for
`flat-explainer|EXPLAINER_PRESET|isExplainer|is_explainer` at `88d7177af`):

- FAMILY (`isExplainerPreset` / `is_explainer_preset`): `drama.mjs` 195, 212, 557;
  `duration.mjs` 20; `lint.mjs` 135; `automation/series.mjs` 58; `flow.mjs` 349, 475-478, 504,
  931; `schemas.py` 427, 790, 795, 820, 828; `series.py` 219, 1430, 1475, 1497;
  `admin-video-series.tsx` 373, 375, 376, 411.
- IDENTITY (`explainerSeries`): `branding.mjs` 62; `render/plan.mjs` 16; `shorts/episode.mjs` 19.
- Data only, untouched: `long-form/plans.mjs`, `long-form/admin-catalog.mjs`. `judge.py`'s
  `"explainer"` is a video category, not the preset.

---

## 3. Pull request 1

**Title:** `feat(video): cute-cartoon and cute-mystery join the explainer family on tools, API and web; flat-explainer does not move`

No prompt, payload, image-model or request-form change.

### 3.1 Changes

Tools:

1. `tools/video/core/drama.mjs` `PRESETS` (91; `"flat-explainer"` entry at 109 untouched): add
   two entries directly after it, each with exactly `style`, `negative: ""`,
   `motion: "slow push in or gentle drift, no morphing, no cuts"`. The two `style` strings are
   the look texts of [`DECISIONS.md`](DECISIONS.md) character for character (378 and 401 characters;
   SHA-256 `55521d0368ebd90abc139968e0c0d60c64f5c74f1da9e482f3e145eb96dc9422` and
   `357820a7ce41cfb5fc5c3175db292bf0132ee83d84674618abccf9d4f2585900`). Comment: positive text
   only because MiniMax image-01 has no negative prompt; which series each belongs to.
2. Same file, at `EXPLAINER_PRESET` (143): keep the constant (tests import it; comment that
   nothing compares with it). Add
   `export const EXPLAINER_PRESETS = Object.freeze(["flat-explainer", "cute-cartoon", "cute-mystery"]);`
   `export const isExplainerPreset = (preset) => EXPLAINER_PRESETS.includes(preset);`
   `const EXPLAINER_IDENTITY = Object.freeze({ "flat-explainer": "sothatswhy", "cute-cartoon": "sothatswhy", "cute-mystery": null });`
3. Same file, `isExplainer` (195):
   `export const isExplainer = (doc) => isDrama(doc) && isExplainerPreset(doc.look?.preset);`
   and below it
   `export const explainerSeries = (doc) => (isExplainer(doc) ? EXPLAINER_IDENTITY[doc.look.preset] : null);`
4. Same file, `isKnowledgeLongform` (212): `|| doc.look?.preset === "flat-explainer"` becomes
   `|| isExplainerPreset(doc.look?.preset)`.
5. Same file, `validateDrama` message (557):
   `` `an explainer (look preset "${doc.look.preset}") has no characters: the narrator tells it` ``
   (identical text for `flat-explainer`). `EXPLAINER_CARD_TEMPLATES` is not changed here.
6. `tools/video/core/duration.mjs` (5, 20): import `isExplainerPreset`;
   `if (!isExplainerPreset(preset)) return minutes;`.
7. `tools/video/core/lint.mjs` (8, 135): import `isExplainerPreset`;
   `return isExplainerPreset(preset) ? BRIEF_SECTIONS_EXPLAINER : BRIEF_SECTIONS_DRAMA;`.
8. `tools/video/core/branding.mjs` (62): `const series = explainerSeries(doc);`.
9. `tools/video/render/plan.mjs` (16):
   `export const thumbnailSeries = (doc) => explainerSeries(doc);`.
10. `tools/video/shorts/episode.mjs` (8, 19):
    `export const episodeSeries = (video) => (explainerSeries(video) === EPISODE_SERIES ? EPISODE_SERIES : ILLUSTRATED_SERIES);`.
11. `tools/video/automation/series.mjs` (17, 58):
    `export const isExplainerOneOff = (series) => isOneOff(series) && isExplainerPreset(series?.style_preset);`.
    `seriesFacts`, `documentPayload`, `documentInputs`, `documentProblem`, `explainerBrief` are
    not edited.
12. `tools/video/automation/flow.mjs`: import (23) `isExplainerPreset` instead of
    `EXPLAINER_PRESET`; `planProblem` (349) `isExplainerPreset(preset) ? EXPLAINER_SECTIONS : DRAMA_SECTIONS`;
    `settle` (475-478) `if (isExplainerPreset(preset)) { settled.look.preset = preset; settled.characters = []; }`
    (the request's own preset, not the constant); (504)
    `settled.characters = isExplainerPreset(settled.look?.preset) ? [] : ...`; `variantOf` (931)
    `return state.format === "drama" && isExplainerPreset(state.style_preset) ? "explainer" : null;`.
    No payload builder is touched. Note for the implementer: line 504 reads the *settled* look,
    which for a non-explainer request is the writer's own; a story writer that answers
    `look.preset: "cute-cartoon"` has its cast emptied exactly as `"flat-explainer"` does today.
    That is existing behaviour, wider; do not "fix" it.
13. `tools/video/templates/templates.mjs`: **not edited** (order 1's comment-only edit is dropped;
    the file is held by an open ticket and nothing needs it).

API:

14. `apps/api/app/video_automation/models.py` `STYLE_PRESETS` (71):
    `("cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "cute-cartoon", "cute-mystery", "custom")`.
    The three CheckConstraints (207, 498, 666) follow.
15. `apps/api/app/video_automation/schemas.py` (49-52): `StylePreset` Literal in the same order;
    remove `EXPLAINER_PRESET`; add
    `EXPLAINER_PRESETS: tuple[StylePreset, ...] = ("flat-explainer", "cute-cartoon", "cute-mystery")`
    and `def is_explainer_preset(preset: str | None) -> bool: return preset in EXPLAINER_PRESETS`.
    A tuple, not a frozenset (order 2 assumed a frozenset; the tuple is the decided form).
16. Same file: `DramaRequestIn._episode_length` (427) `if is_explainer_preset(self.style_preset):`;
    `SeriesIn._enough_to_plan_from` (790)
    `if is_explainer_preset(self.style_preset) and self.kind != "one-off":` with message
    `f'style_preset "{self.style_preset}" is for a one-off explainer only: '` + the unchanged
    second half; (795), (820), (828) the same substitution.
17. `apps/api/app/video_automation/series.py`: import (66); `is_explainer` (219)
    `return is_one_off(series) and is_explainer_preset(series.style_preset)`;
    `patch_target_minutes` (1430) and `patch_problem` (1475)
    `explainer = is_explainer_preset(changes["style_preset"])`; (1497)
    `and is_explainer_preset(changes.get("style_preset", series.style_preset))`; the 422 text
    drops 扁平 (`插畫解說只給單集作品用：長篇與品牌故事都有角色，解說沒有`).
    **Added by the synthesis (critique 1 should-fix 5, closes order 3's risk 6):** in
    `patch_problem`, once a bible doc exists a one-off may not move between two *different*
    explainer presets either. The second condition becomes
    `written = any(doc.kind == "bible" for doc in docs)` and
    `if written and (explainer != is_explainer(series) or (explainer and changes["style_preset"] != series.style_preset)):`
    -> `SeriesRefused(409, "video_series_explainer_fixed", ...)`; for the explainer-to-explainer
    case use the text `故事聖經已經寫了，不能換成另一個解說系列的風格；要換請撤回這部再重新發起`.
    Nothing existing changes (one explainer preset exists today, and the same-preset PATCH stays
    allowed). `doc_problem` and `_explainer_bible_problem` (222) are not edited (decision 2).
18. New migration `apps/api/migrations/versions/NNNN_video_cute_presets.py`: see 3.4.
19. No edit: `create_one_off`, `settings.py` (231 follows the tuple), `admin_api.py`,
    `requests.py`, `video_media/*`.

Web:

20. New `apps/web/lib/video-presets.ts`:
    `export const EXPLAINER_PRESETS = ["flat-explainer", "cute-cartoon", "cute-mystery"] as const;`
    `export const isExplainerPreset = (preset: string): boolean => (EXPLAINER_PRESETS as readonly string[]).includes(preset);`
    with a comment naming the API and tools mirrors. (Order 1 put these in
    `admin-video-settings.tsx`; a plain module avoids a value import of that client component.)
21. `apps/web/components/admin-video-settings.tsx` `STYLE_PRESETS` (39): add the two names in
    the API's order. `admin-video-settings-drama.tsx` is not edited (its select is server-driven).
22. `apps/web/components/admin-video-series.tsx`: import `isExplainerPreset` from
    `@/lib/video-presets`; `PRESETS` (81) and `REQUEST_PRESETS` (84) **unchanged**, with a comment
    that the two cute presets join `REQUEST_PRESETS` in the pull request that gives them their
    prompts; add
    `export const requestMinutes = (preset: string) => (isExplainerPreset(preset) ? EXPLAINER_MINUTES : DRAMA_MINUTES);`;
    (373) `const duration = requestMinutes(preset);`; (375-376)
    `if (isExplainerPreset(next) !== isExplainerPreset(preset)) setMinutes(requestMinutes(next).default);`;
    (411) `isExplainerPreset(preset) ? ... : ...`. No Han characters typed into the component.
23. `apps/web/messages/{zh-TW,zh-CN,en,ja,ko}/admin.json`: in each of the three blocks
    `videoReviews.presets`, `videoSettings.stylePresets`, `videoSeries.presets`, two keys between
    `flat-explainer` and `custom` (30 strings). Wording (default; the owner may change it later):
    zh-TW `可愛卡通解說（原來如此）` / `可愛卡通解說（奇聞檔案局）`; zh-CN `可爱卡通解说（原来如此）` /
    `可爱卡通解说（奇闻档案局）`; en `Cute cartoon explainer (So That's Why)` /
    `Cute cartoon explainer (history and curiosity)`; ja `かわいいカートゥーン解説（原來如此事務所）` /
    `かわいいカートゥーン解説（奇聞檔案局）`; ko `귀여운 카툰 해설(原來如此事務所)` / `귀여운 카툰 해설(奇聞檔案局)`.

Docs: 24. `docs/videos/DRAMA.md` `look` row (line 64): add the two names to the preset list.

### 3.2 Tests

Commit the pin-only assertions first on current main and see them green, then make the change
(the digests below were measured at `599835f49` on a prototype; the builders are unchanged since).

- New `tools/video/core/explainer-family.test.mjs`: (1) the family list and
  `isExplainerPreset` false for `ink-wash`, `custom`, `undefined`, `null`, `"constructor"`;
  (2) the two looks: the two SHA-256 above, lengths 378/401, `negative === ""`, keys
  `[style, negative, motion]`, cast-less `lookHash` `b2c37ca2bc627cd1` / `98a370ae40badbaf`,
  `shotPromptBudget` at limit 1500 with camera `"tilt down"` 1093 / 1070; (3) `flat-explainer`
  is what it was: `sha256(JSON.stringify(PRESETS["flat-explainer"]))`
  `0646ae3434271709496daa3d9e83f1d5c19bfe0e6760c1d6c2860e6a3afb6881`, `lookHash`
  `bd2b3b49af8e9623`, `visualHash(explainerFixture())` `1ee426698cc02ed3`, shot `flash` composed
  prompt `ea312665764d5a793065d1fd6ef3a76cc70c31be1232315c03896c59d11147e3`, `keyframeKey`
  `5169040efab27447` (2K) and `7c56c03a202a1cc8` (1K); (4) family rules for each of the three
  presets on a copy of `explainerFixture()` (valid, no cast, `needsMinimumLength`,
  `isKnowledgeLongform`, clip refused, `briefSectionsFor` explainer); (5) identity:
  `explainerSeries`/`thumbnailSeries` `sothatswhy`, `sothatswhy`, `null`; `episodeSeries`
  accordingly; (6) no bare comparison: no non-test `.mjs` under `tools/video` matches `===`/`!==`
  beside `EXPLAINER_PRESET` or `"flat-explainer"`, and the identifier appears only in
  `core/drama.mjs` (comment in the test: this does not see `.includes()`, `switch` or a `Set`);
  (7) **the three sides agree**: read `apps/api/app/video_automation/schemas.py` and
  `apps/web/lib/video-presets.ts` as text (as `tools/video/production/design.test.mjs` reads API
  source) and compare their `EXPLAINER_PRESETS` with the tools' list.
- `tools/video/core/duration.test.mjs` (bound): the two `effectiveEpisodeMinutes` tests over all
  three presets; `isKnowledgeLongform` true for each; a `cute-mystery` drama of 14,399 body
  frames has a `knowledgeDurationProblems` entry and 14,400 has none.
- `tools/video/core/branding.test.mjs` (bound): `cute-cartoon` takes the series intro,
  `cute-mystery` the channel's.
- New `tools/video/automation/explainer-family.test.mjs`: `settle()` keeps a cute request's
  preset although the writer answered `flat-explainer`; with `flat-explainer` the settled look,
  `lookHash` and `visualHash` are unchanged; `planProblem` and `variantOf` for the three and for
  `ink-wash`; `documentInputs` of the literal job in order 1 is
  `66a99ecc45f9cf42fab4fbfca083f99fca9821095ac70b77f918aaa7eb3157e9`.
- `tools/video/automation/series.test.mjs` (bound): `isExplainerOneOff`/`documentVariant` for the
  three; in the existing one-off end-to-end test pin `sha256(instructions)` and
  `sha256(canonicalJson(payload less today and lexicon))` of the three stage calls (values in
  order 1, test 5; if Linux CI disagrees on a payload digest, pin sorted payload keys and
  `drama_settings` instead); a second run for each cute preset (variants `bible-explainer` then
  `explainer`; Shorts series `sothatswhy` / `illustrated`).
- `tools/video/automation/prompts.test.mjs`: the four explainer instruction digests
  (`planner:bible-explainer` `55ffd024da8e9da7443dca79f973424efcdf277de3a9fa1ec3415af764391a90`,
  `planner:explainer` `32b471d9fcf00ac4540446ba89cbf335f4c4180241b5246301ad3662009451ed`,
  `writer:explainer` `185af9a701ecbb1317f00dd130cbf260e8e664a7275a423bad66c415cb703e72`,
  `verifier:explainer` `c1619a921db55d8a0e92c4f28282dc4d4568e589012d6c07e27917bb3a352842`), with a
  comment: a change here moves the durable key of every unfinished explainer journal; deploy with
  none unfinished, then update the digest.
- New `apps/api/tests/test_migration_NNNN_video_cute_presets.py` (integration): a copy of
  `test_migration_0113_video_flat_explainer.py` for the new revision (old five-preset check
  restored, both inserts fail before and pass after, idempotent upgrade, downgrade refuses while a
  cute row exists).
- New `apps/api/tests/test_video_explainer_family.py`: Literal == tuple == migration
  `NEW_PRESETS`; names at most 16 characters; `SeriesIn` on `series`/`story` refuses each cute
  preset; `is_explainer`, `doc_problem`; `patch_problem`: 422 on a long/story series, 409 when
  crossing the explainer line with a bible, **409 for `flat-explainer` -> `cute-cartoon` and
  `cute-cartoon` -> `cute-mystery` once a bible exists, allowed before one exists**. This file
  posts no cute preset over HTTP (PR 2 would otherwise need it to patch
  `admin_api.load_runtime_settings`); keep it so.
- `apps/api/tests/test_video_explainer_duration.py` (bound): parametrise over the three presets;
  the style-only table of `patch_target_minutes` gains the four rows of order 1.
- New `apps/web/components/admin-video-explainer-family.test.tsx`: `isExplainerPreset`; every
  `STYLE_PRESETS` name has a non-empty label in the three blocks of the five locales; **the
  hold**: the request form's style select has exactly the five option values; the series and
  binge forms offer the four story presets; a queued `cute-mystery` request shows its label.
- `apps/web/components/admin-video-explainer-duration.test.tsx` (bound): `requestMinutes`.
- Run also `admin-video-series.test.tsx` and `admin-video-reviews.test.tsx` (the web part of
  order 1 was designed by reading, never executed).

### 3.3 Receipt-bound files (20)

`tools/video/core/{drama,duration,lint,branding}.mjs`, `tools/video/core/{duration,branding}.test.mjs`,
`tools/video/automation/{flow,series}.mjs`, `tools/video/automation/series.test.mjs`,
`apps/api/app/video_automation/{models,schemas,series}.py`,
`apps/api/tests/test_video_explainer_duration.py`, `apps/web/components/admin-video-series.tsx`,
`apps/web/components/admin-video-explainer-duration.test.tsx`, the five `admin.json`.

### 3.4 Migration

**Number: the next free number on main at implementation time.** At `88d7177af` the head is
`0128_video_languages_four`, but `0129` is already used by an unmerged branch
(`claude/dub-retry-request`, local and on origin: `0129_video_dub_retries`, also revising 0128).
Before writing the file: fetch, `uv run alembic heads`, and look at that branch's pull request;
if it merged or will merge first this is `0130_video_cute_presets` revising
`0129_video_dub_retries`. Re-run `alembic heads` after every rebase until merge. The number
appears in: file name, docstring `Revision ID`/`Revises`, `revision`, `down_revision`, the
integration test's file name and `MIGRATION` constant, the loader path in
`test_video_explainer_family.py`, the comment in `models.py`.

Shape: a copy of `0113_video_flat_explainer.py`. `OLD_PRESETS` the five names, `NEW_PRESETS` the
seven in `models.STYLE_PRESETS` order. The three (table, check) pairs of 0113:
`video_automation_settings`/`ck_video_drama_preset`, `video_drama_requests`/`ck_video_drama_request_style`,
`video_drama_series`/`ck_video_drama_series_style`. `upgrade()` recreates the three under the
same names (idempotent, no data change). `downgrade()` counts rows using either new name in each
table and raises `RuntimeError(f"{used} rows of {table} use the cute-cartoon or cute-mystery preset; change them to another preset first")`,
then restores the old checks. No jsonb operator.

### 3.5 Deploy notes

- One deploy for web, API and tools. The migration rewrites three CHECK constraints on small
  tables; no backfill, no CLI.
- Safe with a `flat-explainer` or story run unfinished (instructions and payloads byte-identical).
- **Every machine that runs the worker pulls the tools before any cute row exists.** An old
  worker would take a cute one-off as a story, pay for a bible with a cast and be refused each
  round.
- **Do not pick a cute preset as the drama default in the settings tab before PR 3** (that
  select is server-driven and lists the two as soon as the API does; `settle()` falls back to
  the settings' preset).
- Note the per-preset row counts of `video_drama_requests`, `video_drama_series` and the settings
  row before the deploy.
- Rollback: the previous release reads the upgraded database while no row uses a cute name; if
  one does, its list endpoints answer 500 until that row is changed.

### 3.6 Host checks (read-only)

1. `alembic current` prints the new revision (head); `/ready` 200.
2. `SELECT conrelid::regclass, conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conname IN ('ck_video_drama_preset','ck_video_drama_request_style','ck_video_drama_series_style');` lists seven presets each.
3. Per-preset counts equal the numbers noted before; no cute row.
4. `/admin/videos`: the settings' default-style select shows the two labels, no raw key; the
   request form has five style options; the series and binge forms four.
5. Worker checkout: `node -e "import('./tools/video/core/drama.mjs').then((m) => console.log(m.EXPLAINER_PRESETS.join(','), m.lookHash({ format: 'drama', look: { preset: 'flat-explainer' }, characters: [] }), m.resolveLook({ preset: 'cute-mystery' }).negative === ''))"` prints `flat-explainer,cute-cartoon,cute-mystery bd2b3b49af8e9623 true`.
6. The worker's log has no `video_ai_receipt_input_changed` and no `must be one of` look error;
   `GET .../drama-requests` and `/series` answer 200.

### 3.7 Risks

- Three hand-kept preset lists on the server (tuple, Literal, migration) plus tools and web; the
  new tests compare all of them.
- The payload digests were measured on Windows; fallback given in 3.2.
- Receipt churn: 20 bound files, and other open pull requests rewrite the receipt too.
- Board: see section 6.

---

## 4. Pull request 2

**Title:** `feat(video): a one-off explainer request names its image model; the cute presets default to MiniMax image-01 and a request the site cannot draw is refused at filing`

Line numbers below are order 2's shifted to `88d7177af` (`flow.mjs` +5 below line 380;
`schemas.py` +1 below line 608).

### 4.1 Changes

API:

1. `schemas.py`, beside the explainer constants (52-57):
   `PRESET_IMAGE_MODELS: dict[str, str] = {"cute-cartoon": "image-01", "cute-mystery": "image-01"}`
   (`flat-explainer` deliberately absent).
2. `schemas.py` `DramaRequestIn` (411): field
   `image_model: str | None = Field(default=None, min_length=1, max_length=128)`;
   `@field_validator("image_model")` returning `_known_image_model(value)` (697); a second
   `@model_validator(mode="after")` `_image_model_for_preset` after `_episode_length`: a model on
   a non-explainer preset raises
   `ValueError("image_model is for an explainer preset only: a cast drama is drawn with the settings' image model, whose reference sheets hold a face across shots")`;
   none named and `PRESET_IMAGE_MODELS.get(self.style_preset)` set -> stored as
   `_known_image_model(default)`. `flat-explainer` with none stays `None`.
3. `series.py` `create_one_off` (1279): `image_model=payload.image_model` on the
   `VideoDramaSeries(...)` row and `"image_model": payload.image_model` in the audit metadata.
4. `apps/api/app/video_media/jobs.py`, after `_series_image_model` (186):
   `def series_image_vendor(row: VideoAutomationSettings, model_id: str) -> str: return _series_image_model(row, model_id)[0]`;
   extend the module docstring's exception sentence. Nothing else in the file.
5. `apps/api/app/video_automation/admin_api.py` `create_drama_request` (381): after the
   `drama_enabled` refusal and before `create_one_off`, only when `payload.image_model is not None`:
   resolve `vendor = series_image_vendor(row, payload.image_model)` (a `MediaJobFailed` re-raised
   as `AppError`), then if `not key_for(await load_runtime_settings(session), vendor)` raise
   `AppError(409, "video_drama_image_model_not_configured", f"網站還沒有 {vendor} 的金鑰，圖片模型 {payload.image_model} 畫不了這支解說；先到 AI 設定填 {vendor} 的金鑰，或改選別的圖片模型")`.
   When no model is named nothing is looked up. The refusal therefore covers **named and
   defaulted models only**; a request that follows the settings is not re-checked at filing (as
   today). Say so in the pull request text.
6. No change: `requests.py`, `DramaRequestOut` (no echo: every new request is shown as its
   one-off series card, and `SeriesSummary` already returns `image_model`, 1000), `settings.py`,
   `models.py`. No migration.

Tools:

7. `flow.mjs` `draftEpisode` (2116), in the `series.json` object right after
   `chapter: episode.chapter_number,` (2179):
   `...(oneOff && typeof series.image_model === "string" && series.image_model ? { image_model: series.image_model } : {}),`
   with the comment of order 2. Not added to `state`, `seriesPayload` or `seriesFacts`. A long
   series still writes no key.
8. `flow.mjs` `draftBudget` (3060): body order `if (state.story) return {};` then for
   `state.format === "drama"`: `{}` unless `state.series` and
   `isExplainerPreset(state.style_preset)`; read `series.json`'s `image_model`; none -> `{}`;
   otherwise `limit = imagePromptLimit({ provider: imageModelVendor(model, null) }, null)`,
   `budget = shotPromptBudget({ look: resolveLook({ preset: state.style_preset }), camera: LONGEST_CAMERA_WORD, cast: null, limit })`,
   return `{ prompt_budget_chars: Math.min(budget, WRITER_PROMPT_MAX) }` (inside `try`, `{}` on
   error); then the slides branch unchanged. Comment must say the figure assumes the seven camera
   words (lint allows a camera of up to 120 characters). Callers (2269, 2795, 2913, 3037)
   untouched. With today's looks the value is 1000 (uncapped 1,093 / 1,070 / 1,056).
9. No change: `media/stages.mjs`, `media/keyframes.mjs`, `media/prompt-budget.mjs`, `story.mjs`,
   `automation/series.mjs`.

Web:

10. `apps/web/lib/video-presets.ts`:
    `export const PRESET_IMAGE_MODEL: Readonly<Record<string, string>> = { "cute-cartoon": "image-01", "cute-mystery": "image-01" };`
    (typed by `string`, **not** by `REQUEST_PRESETS`, which does not hold the cute names until PR 3).
11. `admin-video-settings.tsx`, beside `mediaChoice` (269):
    `export function imageModelOptions(options: MediaOptions | undefined): Array<MediaOption & { provider: MediaProvider }> { return MEDIA_PROVIDERS.flatMap((provider) => (options?.images?.[provider] ?? []).map((option) => ({ ...option, provider }))); }`.
12. `admin-video-series.tsx`: value import of `imageModelOptions`, `mediaProviderLabels`,
    `type MediaOptions` from `@/components/admin-video-settings` (line 10). Export
    `requestImageModel(preset: string, choice: string | null, models: readonly { value: string }[])`
    returning `{ offered: isExplainerPreset(preset) && models.length > 0, presetDefault, value: choice ?? presetDefault }`
    where `presetDefault` is `PRESET_IMAGE_MODEL[preset]` when the catalogue offers it, else `""`.
    `NewDramaForm` gains props `media?: MediaOptions; configured?: readonly string[]; noKey?: string`
    (mount passes `settings?.media_options`, `settings?.configured_providers`, `ts("noKey")`);
    state `imageChoice: string | null`; `changePreset` also resets it when
    `!isExplainerPreset(next) || PRESET_IMAGE_MODEL[next] !== PRESET_IMAGE_MODEL[preset]`; the
    select (label `t("imageModel")`, options as in order 2 change 11: label, vendor, no-key mark,
    price; the `t("imageModelFollows")` empty option only when `presetDefault` is `""`; retired
    models filtered out) renders after the minutes label only when `offered`; body adds
    `image_model: offered && value ? value : undefined`.
13. Same file: `SeriesSummary` gains `image_model?: string | null`; the one-off card's facts line
    and the series page header append `t("imageModel", { model })` when set.
14. Five `admin.json`: `videoReviews.imageModel`, `videoReviews.imageModelFollows`,
    `videoSeries.imageModel` (`{model}`), wording as order 2 change 13.

Docs: 15. `docs/videos/DRAMA-FLOW.md` section 二: the sentences order 2 wanted in
`references/drama.md` (the form's image-model field, image-01 by default for the cute presets,
409 `video_drama_image_model_not_configured`, `series.json` `image_model`). **`references/drama.md`
is not edited** (it is payload).

### 4.2 Tests

- New `apps/api/tests/test_video_drama_request_image_model.py`: schema cases, `create_one_off`
  storage and audit, HTTP cases (409 without a MiniMax key and `create_one_off` not awaited; 201
  with one; `flat-explainer` naming none reads no runtime settings; 422 on a cast preset) and the
  integration case, all as order 2 test 1.
- `apps/api/tests/test_video_drama_requests.py` (bound): the exact audit dict gains
  `"image_model": None`. Nothing else.
- `apps/api/tests/test_video_media_jobs.py`: the `image-01` one-off override case; the no-key
  case builds the context first and then assigns
  `ctx.runtime = Settings(hotspot_guide_gemini_api_key="g", minimax_api_key="")` (passing
  `runtime=` through `_context(...)` is a duplicate keyword); `series_image_vendor` cases.
- `tools/video/automation/series.test.mjs` (bound): a `flat-explainer` + `image-01` one-off
  writes `image_model` into `series.json` and its writer payload has `prompt_budget_chars === 1000`;
  the existing end-to-end test gains "no own `image_model` key" and "no `prompt_budget_chars`";
  a long series whose context names a model writes no key.
- `tools/video/automation/automation.test.mjs` (bound): the `draftBudget` cases of order 2 test 6.
- `tools/video/media/look-keyframes.test.mjs` (bound), **as corrected by critique 2**: one new
  test on the explainer fixture rewritten to `look: { preset: "cute-mystery" }` with a
  `series.json` naming `image-01` and a status carrying `image.usd_per_image_2k: 0.134`, the
  MiniMax catalogue row and `limits.image_prompt_chars_minimax: 1500`. Dry run prints
  `server: minimax image-01 (provider key checked on submit); pictures at 1K`; every expected
  budget is computed with `shotPromptBudget({ look, camera: scene.data.camera, cast: "", limit: 1500 })`
  (the fixture's cameras give 1067, 1074, 1070, 1071: no `107x` pattern). Paid path for one
  shot: no `size`, no `negative_prompt`, `manifest.image` minimax/image-01,
  `image_selection_version === 1`. Counter-case **inside the new test** on a fresh sandbox with
  the same 2K-priced status and no `series.json`: the request asks `size: "2K"`. The fake site
  changes in two places only: the 2K price lookup becomes
  `(status.slides_image ?? status.image).usd_per_image_2k`, and the 1K lookup searches
  `Object.values(status.models.images).flat()`. The existing explainer test (around 625) is left
  as it is (it draws with no `size`: `STATUS.image` has no 2K price).
- `tools/video/media/stages.test.mjs`: the `imageStatus` unit case of order 2 test 8.
- `tools/video/core/explainer-family.test.mjs` (PR 1's): extend the "three sides agree" case to
  compare `PRESET_IMAGE_MODELS` in `schemas.py` with `PRESET_IMAGE_MODEL` in `video-presets.ts`.
- New `apps/web/components/admin-video-request-image-model.test.tsx`: rendered cases for a cast
  preset (no field, no key in the body), `flat-explainer` (field with the "same as the drama
  settings" entry; choosing `image-01` sends it), no-key marking and the 409 alert, `/settings`
  503 and `images: {}` (no field), one spinbutton and the style select's exact name, the one-off
  card and header line. **The cute presets are not in the form yet**, so their behaviour is
  tested on `requestImageModel` directly: value `image-01` at once, no "follows" entry,
  `cute-cartoon` -> `cute-mystery` keeps a pick, `presetDefault` `""` when the catalogue lacks
  `image-01`. PR 3 adds the rendered cute cases.
- Must pass unedited: `test_video_series.py`, `test_video_explainer_duration.py`,
  `test_video_automation_settings.py`, `admin-video-explainer-duration.test.tsx`,
  `admin-video-reviews.test.tsx` (exact body at 317), `admin-video-series.test.tsx`. Before
  pushing, grep PR 1's merged tests for an HTTP post of a cute preset; any such test must patch
  `admin_api.load_runtime_settings`.

### 4.3 Receipt-bound files (13)

`apps/api/app/video_automation/{schemas,series}.py`, `apps/api/tests/test_video_drama_requests.py`,
`apps/web/components/admin-video-series.tsx`, the five `admin.json`,
`tools/video/automation/flow.mjs`, `tools/video/automation/{automation,series}.test.mjs`,
`tools/video/media/look-keyframes.test.mjs`.

### 4.4 Migration

None. `video_drama_series.image_model` exists (String(128), nullable, migration 0111).

### 4.5 Deploy notes

- One deploy; `DramaRequestIn` forbids unknown keys, so a new web against an old API gets 422 on
  every explainer request that sends `image_model`.
- Version-sensitive side: **the worker's `draftEpisode`** (the writer of `series.json`). The
  media stages that read the key already exist on main, so an older checkout that only draws
  works; an older `draftEpisode` on a row naming `image-01` asks for 2K pictures and every shot
  is refused 422 `video_media_model_not_allowed` after the bible and script were paid for.
  Confirm the worker's checkout before the first request that names a model.
- Safe with explainer work in flight (true only because `references/drama.md` is not edited): a
  `flat-explainer` request naming no model gives the same row, `series.json`, writer payload and
  cache keys. Never backfill the key into an existing video (it re-keys every picture).
- Needs PR 1 deployed first. MiniMax must have a key on the site before the first cute request
  (it has: the slides draw with `image-01`).
- Budget: nothing changes. A 130-picture episode at up to three takes is at most 390 pictures
  and 390 judge calls (about US$5.27; one take US$1.76); the monthly judge-call count is the
  tighter limit and is not checked at filing (429 at draw time, as today).

### 4.6 Host checks (read-only)

1. `GET /api/v1/admin/video-automation/settings`: `media_options.images.minimax` has `image-01`;
   `configured_providers` contains `minimax`.
2. `/admin/videos?tab=drama`, form opened, nothing submitted: a cast preset shows no image-model
   field; `flat-explainer` shows it with "same as the drama settings" selected; no option carries
   the no-key mark. (The cute presets are checked after PR 3.)
3. `SELECT slug, style_preset, image_model, created_at FROM video_drama_series WHERE kind = 'one-off' ORDER BY created_at DESC LIMIT 10;` every earlier row has `image_model` NULL.
4. A `flat-explainer` episode started after the deploy with no model: no `image_model` key in
   its `series.json`, first job at the settings' model and 2K price.
5. `node tools/video/cli.mjs media-status`: `budget images` and `budget judge_calls` each have
   at least 390 left before a 130-picture episode.
6. After PR 3, on the first cute request (the owner's action): the row and the audit entry carry
   `image-01`; `series.json` has the key; `keyframes --dry-run` prints `minimax image-01`,
   `pictures at 1K` and no shot OVER BUDGET (budgets near 1,07x for `cute-mystery`, 1,09x for
   `cute-cartoon` when the camera is one of the seven words); the first job row is
   minimax / image-01 / 0.0035.

### 4.7 Risks

- Naming a Gemini model on an explainer draws at 1K (softer under a camera move than "same as
  the settings" at the same price); follow-up.
- `flat-explainer` + `image-01` is allowed but its 204-character negative reaches MiniMax as
  `. Avoid: ...` text; the form does not stop it.
- A cute one-off PATCHed to a cast preset before its bible exists keeps `image-01` (API only);
  follow-up with `POST /series`.
- The filing check is a point in time; the dry run says `(provider key checked on submit)`
  rather than `ready` unless a settings choice is on MiniMax (cosmetic).

---

## 5. Pull request 3

**Title:** `feat(video): cute-cartoon and cute-mystery explainers are written from their own series' prompts; flat-explainer's prompts do not move`

### 5.1 Prompt texts

All new prompt text is one new file, `tools/video/automation/explainer-series.mjs`. Its full
source is **section 3 of [`prompt-texts.md`](prompt-texts.md)** (write it LF, UTF-8, no BOM; the
scratch copy of the file itself was not kept, section 3 is the source). Section 1 there says
which block goes into which text, section 4 has the ten composed texts with length and SHA-256,
section 5 the nine digests of existing texts that must not move. Exact code hunks for the other
files: [`orders/pr3-on-6a26eff.diff`](orders/pr3-on-6a26eff.diff) (a `diff -ru` of the tools
with PR 1's prototype, `n-pr1/`, against the same with PR 3, `n-pr3/`; it applies at `88d7177af`
on top of PR 1 and holds no hunk for `explainer-series.mjs`, which comes from section 3 above).
The checks the prototype was verified with: [`orders/verify-pr3.mjs.txt`](orders/verify-pr3.mjs.txt)
(kept as text so no tool runs it; it expects the scratch tree and is a model for the tests of 5.3).

**The synthesis edited the texts** (critique 3 must-fix 2 to 4 and the cheap should-fixes; patch
script and the originals were scratch files and are not kept), then regenerated
[`prompt-texts.md`](prompt-texts.md) with its generator and re-ran `verify-pr3.mjs` on the
scratch tree (all seven groups pass):

- Part lengths are given for the 10-minute target and scale with `target_minutes` (cartoon:
  hook 20 s, background about 2 min, chapters 6 to 7 min, answer about 1 min, close 20 s;
  mystery: hook 20 s, 流傳的版本 about 1.5 min, 紀錄 6 to 7 min, 解釋 about 1.5 min, close 20 s);
  "the parts together reach the target and never fall under 8 minutes".
- 奇聞檔案局: a person living or dead for under 70 years is never drawn as that person: an
  invented generic figure from behind or small in the distance, by common role and plain
  clothing only, never by name or any identifying feature, or left out. The checker's flag and
  the discussion refusal say the same.
- Both checkers check `youtube.title`, `youtube.description` and the thumbnail (headline, sub,
  each variant's) as well as narration and cards.
- Also: gore/corpses/violence never drawn, a death told plainly once in words; the bible planner
  re-plans a premise the series never tells; `NO_PAGES` added to both discussion planners and a
  待查核 rule to the writers; one voice for opinions; line-length target vs limit; "the intro and
  outro clips are the tool's, the outro card is yours"; three or four 紀錄 lines preferred, two
  allowed. The dead 「示意」 sentence is dropped (nothing told the planner to ask for it; the
  description's AI-illustration line stays).

**Digests must be re-pinned by the implementer.** The ten digests now in `prompt-texts.md`
section 4 were recomputed by the generator from the edited source and differ from every digest
quoted in order 3 (for example `writer:explainer-mystery` is now 16,053 characters,
`5f8b7e3c…2fa562`). Compute them again from the committed file before pinning anything, and do
not copy a digest from `orders/order-pr3.json`. `prompt-texts.md` section 6 (rule sources) is the
generator's static text and may describe a rule in its earlier wording. The nine digests of
*existing* texts (section 5) are unchanged and are pinned as they stand.

### 5.2 Changes

1. New `tools/video/automation/explainer-series.mjs` (5.1). Imports only
   `explainerCardTemplates` from `../core/drama.mjs`; nothing from `prompts.mjs`.
2. `tools/video/automation/prompts.mjs` (bound): import `EXPLAINER_SERIES_INSTRUCTIONS` above the
   story-prompts import (14). In `instructionsFor` (772): above `const base` (776) add
   `` const seriesOwn = variant && Object.hasOwn(EXPLAINER_SERIES_INSTRUCTIONS, `${stage}:${variant}`) ? EXPLAINER_SERIES_INSTRUCTIONS[`${stage}:${variant}`] : null; ``;
   in `base` the variant group gets `|| seriesOwn` as its **last** operand; the genre line (780)
   becomes `const genre = !anime && base !== seriesOwn && GENRE_STAGES.has(stage) ? genreBlock(series) : "";`.
   Nothing else in the file. For every existing call `seriesOwn` is null and the composed text is
   identical.
3. `tools/video/automation/flow.mjs` (bound): import
   `{ explainerProfile, explainerVariants, isExplainerStageVariant }`. `settle`: first statement
   inside PR 1's `if (isExplainerPreset(preset)) {`:
   `if (explainerProfile(preset)) settled.look = { preset };`. `variantOf` (931):
   `return state.format === "drama" ? explainerVariants(state.style_preset)?.stage ?? null : null;`.
   Line 3044: `this.variantOf(state) === "explainer"` becomes
   `isExplainerStageVariant(this.variantOf(state))`. No payload builder, not `draftBudget`,
   **not `acceptBestPictures`**.
4. `tools/video/automation/series.mjs` (bound): import `{ explainerProfile, explainerVariants }`;
   (60)
   `export const documentVariant = (kind, series) => (kind === "bible" && isExplainerOneOff(series) ? explainerVariants(series.style_preset)?.bible ?? "bible-explainer" : kind);`;
   private `const isProfiledExplainer = (series) => isExplainerOneOff(series) && explainerProfile(series.style_preset) !== null;`;
   in `documentPayload`'s base only (521)
   `genre_spec: isLongAnime(series) || isProfiledExplainer(series) ? null : GENRE_SPECS[series.genre] ?? null,`.
   Line 571 (`judgeDocument`), `seriesFacts`, `documentInputs`, `documentProblem` untouched.
5. `tools/video/automation/discuss.mjs` (bound): imports; (23)
   `Object.freeze(["discuss", "anime-discuss-plan", ...EXPLAINER_DISCUSS_VARIANTS])`;
   `export const documentDiscussVariant = (series) => (isExplainerOneOff(series) ? explainerVariants(series.style_preset)?.discuss ?? "discuss" : "discuss");`
   `export const scriptDiscussVariant = (state) => (state?.format === "drama" ? explainerVariants(state.style_preset)?.discuss ?? "discuss" : "discuss");`;
   the literal `"discuss"` in the stage calls at 187 and 387 becomes the two helpers. The
   `keepAnswer(..., "discuss")` labels (191, 213, 391, 402) are file names: leave them.
6. `tools/video/core/drama.mjs` (bound): after line 21 `CUTE_EXPLAINER_PRESETS`,
   `CUTE_EXPLAINER_CARD_TEMPLATES = [...EXPLAINER_CARD_TEMPLATES, "steps", "table"]`,
   `explainerCardTemplates(preset)`; `isCuteExplainer(doc)`; `validateDrama` (556)
   `const cards = explainer ? explainerCardTemplates(doc.look?.preset) : CARD_TEMPLATES;`;
   `CUTE_LOOK_WORDS` above `DARK_LIGHT` (784); `pictureVarietyProblems` (813) covers
   `isCuteExplainer(doc)` and matches the cute words for it. Hunks in the diff.
7. `tools/video/media/keyframes.mjs` (not bound): import `isCuteExplainer`; (519)
   `const checks = (slides || isCuteExplainer(doc)) && Boolean(status.limits?.judge_checks);`.
8. `apps/web/components/admin-video-series.tsx` (bound): `REQUEST_PRESETS` (84) becomes
   `["cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "cute-cartoon", "cute-mystery", "custom"]`;
   comment reworded. `PRESETS` (81) stays. No new string.
9. `docs/videos/DRAMA-FLOW.md` section 二: about ten lines (zh-TW) on `EXPLAINER_VARIANTS`, the
   two profiles, their discussion variants, the nine checks and the variety lint, **and that a
   cute explainer's failing picture blocks the video after two prompt-fix rounds** (below).
10. Byte-identical in this pull request: every payload-read file of section 1,
    `templates.mjs`, `lint.mjs`, `render/plan.mjs`, `run-receipts.mjs`, `apps/api/**`,
    `apps/web/messages/**`, `docs/videos/so-thats-why/README.md`, `plans.json`.

**Pictures that keep failing (critique 3 must-fix 1): option (b), the code is left alone.**
On the drama route there is no accept-best: `flow.mjs` 2899-2902 calls `acceptBestPictures`,
which returns null unless `illustrated(video)` (2934); `media/keyframes.mjs` 277 refuses
`--accept-best` for a non-illustrated video; `review/sync.mjs` 1133 lists kept pictures for
illustrated videos only. So a cute explainer whose shot still fails after 3 takes x (1 + 2
prompt fixes) **blocks with `prompt_fixes:keyframes` and waits for the owner's retry**; it does
not go on to the owner's keyframe gate. Order 3's "not a hard block" is wrong and is withdrawn.
Why (b) and not (a): extending the three predicates also changes which cuts are sent for manual
review (`keyframes.mjs` 274-276 warns that a drama's kept shot could have its storyboard and cut
approved on arrival with nobody asked to look), `sync.mjs` is receipt-bound, and none of it was
prototyped. (b) fails closed: nothing is published and no paid work is lost. A follow-up ticket
makes the host route match the conditions the pilots were measured under.

Other corrections to order 3 carried here: the pilots used more than the eight cards (also
`bullets`, `quote`, `screenshot`; `curio-l08` has no `table`), the choice of eight stands;
`variantOf` returns names for which no `planner:explainer-<x>` text exists, on purpose (a cute
request is always a series row), and a test pins what `instructionsFor("planner", "drama", "", "explainer-mystery")`
falls back to.

### 5.3 Tests

- New `tools/video/automation/explainer-series.test.mjs`: `verify-pr3.mjs` turned into
  `node:test` cases, group by group (order 3 test 1), with these changes: the ten new digests are
  recomputed (5.1); the nine existing digests keep PR 1's pins in `prompts.test.mjs` and add the
  other five here; both verifier texts contain `youtube.title` and `thumbnail`; both writer
  texts contain `never fall under 8 minutes`; the mystery texts contain `never drawn as that person`;
  the planner fallback assertion above.
- New `tools/video/core/explainer-cute.test.mjs`: cards per preset, the channel thumbnail under
  `cute-mystery` (valid with `{headline, tag, sub, shot}`; `pillar` and `layout: "right"`
  refused), `checkBrief` with the labelled 原因 lines, variety lint for cute only (order 3 test 2).
- `tools/video/automation/series.test.mjs` (bound): the cute-mystery end-to-end test of the diff
  (bible under `bible-explainer-mystery`, `genre_spec` null, labelled 原因 in `brief.md`, look
  `{ preset: "cute-mystery" }`, channel thumbnail untouched, Shorts series `illustrated`). The
  existing `flat-explainer` test is not edited.
- `tools/video/media/look-keyframes.test.mjs` (bound): the judge test of the diff, added after
  PR 2's change to the fake site, which it does not touch. For `flat-explainer` assert "the
  scored rubric, not the checks" (no item carries a check cost) rather than five key names: a
  real run has four keys because `settle` forces `burn_in` false.
- `tools/video/automation/discuss.test.mjs`: `discuss-mystery` for a cute-mystery bible and
  script; `discuss` with today's digest for `flat-explainer`.
- `apps/web/components/admin-video-explainer-family.test.tsx`: re-pin on purpose to the seven
  option values; `cute-mystery` switches minutes to 8-20/10 and files `style_preset`
  `"cute-mystery"` with `image_model` `"image-01"` when the harness's settings offer it.
- `apps/web/components/admin-video-request-image-model.test.tsx`: add the rendered cute cases
  PR 2 could not reach (preselected `image-01`, no "follows" entry, pick kept between the two
  cute presets, reset on leaving them).

### 5.4 Receipt-bound files (8)

`tools/video/automation/{prompts,flow,series,discuss}.mjs`, `tools/video/automation/series.test.mjs`,
`tools/video/core/drama.mjs`, `tools/video/media/look-keyframes.test.mjs`,
`apps/web/components/admin-video-series.tsx`.

### 5.5 Migration

None. No API change, no new i18n key.

### 5.6 Deploy notes

- Web and worker tools in one deploy; the API is not touched.
- No existing run needs draining (nine instruction digests and the payload digests identical).
  The one run that would stop is a cute video filed by direct API call between PR 1 and now;
  check there is none (host check 1).
- **Expect the first host episodes of each series to block at keyframes** if any picture of 100
  to 140 still fails after two prompt-fix rounds (the pilots passed about 80% on the first
  take). The owner retries from the block; nothing is lost. This is the known cost of option (b).
- No host model has read the new texts: the first episode of each series is a pilot the owner
  reads at the bible and script gates. Every later wording change is a new prompt and stops an
  unfinished **cute** run with `video_ai_receipt_input_changed` (never a `flat-explainer` one).
- The settings page's "prompt sent" list gains rows such as `planner · bible-explainer-mystery`.

### 5.7 Host checks

1. Before the deploy: no one-off row in `cute-cartoon`/`cute-mystery` with an episode not yet at
   the script gate.
2. Worker: SHA-256 of `instructionsFor("writer", "drama", "", "explainer")` is `185af9a7…03e72`
   and of `("planner", "drama", "", "bible-explainer")` `55ffd024…91a90`; of
   `("writer", "drama", "", "explainer-mystery")` the digest the implementer pinned.
3. `/admin/videos`: the request form lists the two cute presets with labels, minutes 8 to 20,
   image model `MiniMax image-01` preselected with no "same as the drama settings" entry.
4. After the owner files the first `cute-mystery` request: run `planner/bible-explainer-mystery`;
   the bible's 原因 has 流傳的版本, two to four 紀錄, 目前最站得住的解釋 in that order and a closing
   starting 存檔 or 未結; then `writer/explainer-mystery` and `verifier/explainer-mystery`.
5. That video's `video.json`: `look` exactly `{"preset": "cute-mystery"}`, `characters` `[]`,
   thumbnail with `headline` (at most 6 counted characters), `tag` (one of 歷史懸案, 奇異現象, 預言,
   外星與太空, 都市傳說), `sub`, `shot` and no `pillar`/`layout`/`variants`; plus PR 2's check 6.
6. The first judged pictures' job rows carry the nine check keys (text, anatomy, detached,
   subject, frame, style, details, awkward, generated); a `flat-explainer` video drawn the same
   day is scored on the rubric. A block of kind `prompt_fixes:keyframes` on a cute video is
   expected behaviour, to be retried, not a regression.
7. An owner's line on that bible is recorded as `planner/discuss-mystery`.

### 5.8 Risks

- The nine checks were measured on slides pictures of these looks; the "generated" question
  names an even outline, which the look asks for. A misfire costs redraws and, per the above, a
  block. Fallback: one line in `keyframes.mjs`.
- The variety lint's same-move rule is an error and spends free repair rounds.
- A cute writer still receives `references/drama.md` and the drama example (written for other
  routes); the prompt says it wins; `settle` forces `burn_in` false and drops a writer's style
  and negative.
- An owner cannot tune a cute look per video through the script (decided choice 3).
- A hands-off one-off's bible is still judged with the story genre spec (API only); follow-up.
- `cute-mystery` Shorts are saved as series `illustrated` (theme 你以為 · 其實) until the
  series has its own.

---

## 6. Ticket scope to widen (before anyone claims)

The ticket's scope lacks most paths; `tools/video/automation/flow.test.mjs` in it does not
exist. Either widen it or file one child ticket per pull request (preferred, so the parent does
not hold `flow.mjs` and `prompts.mjs` across three pull requests). Paths to add:

- PR 1: `apps/api/app/video_automation/{models,series}.py`,
  `apps/api/tests/{test_migration_NNNN_video_cute_presets,test_video_explainer_family,test_video_explainer_duration}.py`,
  `apps/web/lib/video-presets.ts`,
  `apps/web/components/{admin-video-explainer-family,admin-video-explainer-duration}.test.tsx`,
  `tools/video/core/{duration,lint,branding}.mjs`,
  `tools/video/core/{duration,branding,explainer-family}.test.mjs`, `tools/video/render/plan.mjs`,
  `tools/video/shorts/episode.mjs`, `tools/video/automation/series.mjs`,
  `tools/video/automation/{series,prompts,explainer-family}.test.mjs`, `docs/videos/DRAMA.md`.
- PR 2: `apps/api/app/video_automation/series.py`,
  `apps/api/tests/{test_video_drama_requests,test_video_drama_request_image_model}.py`,
  `apps/web/lib/video-presets.ts`, `apps/web/components/admin-video-request-image-model.test.tsx`,
  `tools/video/automation/{automation,series}.test.mjs`,
  `tools/video/media/{look-keyframes,stages}.test.mjs`,
  `tools/video/core/explainer-family.test.mjs`, `docs/videos/DRAMA-FLOW.md`.
- PR 3: `tools/video/automation/{explainer-series,series,discuss}.mjs`,
  `tools/video/automation/{explainer-series,series,discuss}.test.mjs`,
  `tools/video/core/explainer-cute.test.mjs`, `tools/video/media/keyframes.mjs`,
  `tools/video/media/look-keyframes.test.mjs`, `docs/videos/DRAMA-FLOW.md`,
  `apps/web/components/{admin-video-explainer-family,admin-video-request-image-model}.test.tsx`.
- Each reviewer's ticket: `docs/videos/long-form/review.json`, `docs/videos/long-form/review.md`.
- Drop from the scope: `apps/api/app/video_automation/settings.py`,
  `apps/api/tests/test_video_automation_settings.py`, `tools/video/core/drama.test.mjs`,
  `tools/video/automation/flow.test.mjs` (none is edited).

Board at `88d7177af`: `2026-10-10-photo-paste-card` (status review, merged as #1425) still holds
`tools/video/core/lint.mjs`, `tools/video/render/plan.mjs`, `tools/video/automation/prompts.mjs`
and `automation.test.mjs`; close it first or `claim` is refused. (`policy-demo-exempts-explainer-slides`
is already in `tasks/done`.) Open and unclaimed with overlapping scope:
`2026-10-10-photo-card-edge-cases` (`lint.mjs`, `plan.mjs`), `2026-10-10-host-writer-prompt-forbids-photo`
(`prompts.mjs`; a different paragraph, not folded in).

## 7. Follow-up tickets to file

1. A cute explainer keeps the judge's best take like illustrated slides (`flow.mjs`
   `acceptBestPictures`, `media/keyframes.mjs` `acceptBest`, `review/sync.mjs`
   `acceptedPicturesOf`, with the manual-review routing and a test).
2. `screenshot` and `photo` cards for the host's explainer writer (needs a way to supply and
   credit an image file); whether `quote` is offered to the 奇聞檔案局 writer.
3. 奇聞檔案局's own intro, thumbnail series and Shorts theme.
4. Move So That's Why's 192 planned episodes to `cute-cartoon` with `image-01`, after the owner
   approves `sothatswhy-b26` (decision 4).
5. `POST /series` (kind one-off) and `PATCH /series/{slug}`: the cute default and the key check;
   clear `image_model` when a one-off leaves the explainer family.
6. An explainer that names a Gemini model is drawn at 1K (`usd_per_image_2k` on
   `MediaOptionView`; `imageStatus` keeping the named model's 2K price).
7. A long series whose row names its own image model: the same worker/server disagreement
   (needs a decision on character-sheet reuse).
8. `imageStatus` reads the key state from `status.slides_image` too (dry run says `ready`).
9. A hands-off explainer bible is judged with the story genre spec (`series.mjs` 571).
10. Documentation that is payload or bound, in one deploy with no drama journal unfinished: the
    explainer paragraph and preset list of `.agents/skills/youtube-video/references/drama.md`,
    `docs/videos/so-thats-why/README.md`'s "use preset custom" sentence,
    `.agents/skills/animation-camera/references/model-misreads.md` line 35, and
    `docs/videos/history-curiosity/look.md` §縮圖 (`外星` against the prompt's `外星與太空`).
11. The writer's two Shorts are saved before the checker runs; a number the checker corrects in
    the long video stays as written in `shorts.json` (same for `flat-explainer` today).
12. Whether the settings tab's default-style select should stop offering explainer presets.

## 8. Must-fix items: applied and rejected

Applied (8 of 8): critique 1: (1) migration number left open, (2) sites re-based; critique 2:
(1) `references/drama.md` not edited, (2) the look-keyframes test rewritten; critique 3: (1)
option (b) with the claim corrected, (2) to (4) prompt texts edited. **Rejected: none.**

Should-fix items not taken as written: critique 3 (9) keeps the words "two to four times"
(a planned assertion matches them) and adds the preference in brackets; critique 3 (3) is
resolved by dropping the 「示意」 sentence rather than wiring it; critique 2 (1) and (6) are
follow-ups 5 and 6; critique 1 (8) is taken (no `templates.mjs` edit).

## 9. Still needs the owner

Nothing blocks implementation. Defaults taken that the owner may want to overrule later:

- The preset labels' wording in five locales (3.1 item 23).
- 奇聞檔案局's likeness rule as now worded, the dropped 「示意」 label, and the two shortened
  thumbnail tags `奇異現象` and `預言` (the other three are the pilots'): best read at the first
  host episode's script gate.
- The first cute episodes on the host may block at keyframes and need the owner's retry;
  follow-up 1 removes that if the owner wants the slides route's behaviour.
- Operational, for the coordinator rather than the owner: who re-issues each receipt (not the
  author), and closing the `photo-paste-card` ticket.

Not verified by anyone: the API and web parts were designed by reading and never executed; the
whole of `automation.test.mjs`; anything on the host; the remote state of open pull requests.
