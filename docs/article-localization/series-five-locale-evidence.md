# Gemini and Claude Code five-locale series catalogue

## Baseline and scope

- Implementation base: `origin/main` at `50b3cb554713fce8bb979daec1d6db4f4da648bb` (2026-09-28).
- The existing Claude Code source catalogue has 96 lessons (`claude-code.json` SHA-256 `e69f08626ef68b666b63d4b04305566cf3e65b8f4ad582ba155189cd49885e25`). Its original locale overlay covered only the first 60 lessons. The completed overlay covers all 16 groups, 12 paths and the non-ASCII search aliases across zh-CN, en, ja and ko (SHA-256 `998a49b83c4773e3a783e4b1ecb18b1a72ba4c8e35fdfb251cf272d1b83f52f0`).
- The new Gemini API catalogue has 50 lessons and matches every stable slug, number, group and learning-path member of the current web source (SHA-256 `c74dbf8463a74c76fb1ac7a3d2df9844b354bb47f8fdc9e0b9cdadabf8bddb15`). Its overlay translates 8 groups, 5 paths and search aliases into the other four locales (SHA-256 `f014bb397226343e164cce31cd7d869f5bcf52f4151d8b62bcb4d530e2c19c28`).
- The production web source currently has only 50 lessons. Advanced lessons 51–86 exist in planning/test fixtures, not in the production catalogue. A test compares the *enabled* web projection against the API catalogue, so a future advanced rollout cannot silently outrun the API's publication allowlist.

## Publication boundary

The catalogue holds order, paths and search vocabulary, not public article bodies or titles. The API joins it to each locale's *published* hub and lesson revisions before returning a directory or previous/next links. If the hub is absent, the directory and navigation are absent. Withdrawing a lesson removes it from the directory, learning paths and navigation. The existing zh-TW Gemini web projection remains its sole renderer; it now intersects the API's published lesson set before drawing paths, commands or navigation, and uses live published titles and descriptions. An API miss fails closed. The other locales use the API catalogue as their lessons are published. The generic Gemini directory names its actual published hub, uses locale-specific Gemini search copy and renders the `all` platform value as a translated label.

No article JSON, publication state, database schema, image or production service is changed by this PR. It does not assert that the missing article translations have been published.

## Checks

- API: `uv run pytest tests/test_guide_series.py -q` yielded 31 passed, 19 skipped. The skipped integration tests need the CI database service. `uv run ruff check app/guides/series.py tests/test_guide_series.py` and `uv run mypy app/guides/series.py` passed.
- Data: the loader validated five editions each for Claude Code and Gemini, matching stable slugs, group and path IDs, and alias coverage. The new test checks localization and live publication gating.
- Web: focused tests cover zh-TW Gemini/API navigation exclusivity, locale-specific Gemini directory copy, a translated all-platform label and the withdrawal of a lesson from every zh-TW static link surface. A new test checks enabled web/API catalogue identity parity. `npx vitest run --pool=forks --maxWorkers=1` passed all 72 tests across the three affected files. The default Windows thread pool intermittently failed to start a worker under concurrent load; the final single-fork run passed. `npm run typecheck:web`, `npm run lint:web`, a scoped lint after the last edits and `npm run check:i18n` passed (5 locales, 25 namespaces). Full CI remains pending.
- The first PR Web CI run exposed an outdated integration fixture: it returned no Gemini API series while asserting that the directory was visible. The fixture now supplies published entries; all 79 tests across the four relevant Web files pass with a single-fork runner, including the seven Gemini page integration cases. Typecheck, i18n and task checks also pass; CI will rerun at the updated head.

Production import, deployment, browser QA and same-image Docker rehearsal are separate gates. No nonproduction Docker environment is currently available.
