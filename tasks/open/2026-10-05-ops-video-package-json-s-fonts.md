---
id: 2026-10-05-ops-video-package-json-s-fonts
title: ops/video/package.json's fonts and pinyin-pro can drift from package-lock.json
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T07:36:47Z
completed_at:
branch:
depends_on: []
scope:
  - tools/supply-chain.test.mjs
  - ops/video/package.json
---

# ops/video/package.json's fonts and pinyin-pro can drift from package-lock.json

## Why

The video worker's image installs its packages from `ops/video/package.json` alone (`npm install`
in `ops/video/Dockerfile`, no lock file). That file says it pins "the packages tools/video loads,
at the versions the repository's package-lock.json pins": `@fontsource-variable/jetbrains-mono`
5.3.0, `@fontsource-variable/noto-sans-tc` 5.3.0, `pinyin-pro` 3.29.4 and `@playwright/test`
1.63.0. Only `@playwright/test` is checked (`tools/supply-chain.test.mjs`, task
`2026-10-05-the-video-worker-s-playwright-image`). The root npm Dependabot group bumps the
others in `package-lock.json` (root devDependencies `^5.3.0` and `^3.29.4`) and never touches
`ops/video/package.json`, which is not a workspace. After such a bump, `tools/video` tests in CI
run one pinyin-pro or font release and the worker on the host another: a pinyin change shows up
first in a published video's subtitles, a font change in its frames.

On 2026-10-05 all four match the lock file.

## Definition of done

- [ ] A test fails when a dependency in `ops/video/package.json` is not an exact version or is
      not the version `package-lock.json` resolves for that name, and passes on main.
- [ ] Someone decided, and wrote down in the test's comment or `.github/dependabot.yml`, how a
      weekly npm group that bumps one of these gets past that test (edit `ops/video/package.json`
      in the Dependabot pull request, or keep these packages out of the group the way
      `@playwright/test` is).

## Steps

- [ ] Generalize or add next to the Playwright check in `tools/supply-chain.test.mjs` (the
      Playwright one compares the image tag too; this one only package.json against the lock).
- [ ] Choose how Dependabot bumps reach `ops/video/package.json`; `.github/dependabot.yml` is
      not in this scope yet, add it if the choice changes the groups.

## How to verify

```bash
node --test tools/supply-chain.test.mjs
# Change "pinyin-pro": "3.29.4" to "3.29.5" in ops/video/package.json: the new test fails.
```

## Notes

- Found while doing `2026-10-05-the-video-worker-s-playwright-image`, which left these out on
  purpose: checking them turns every weekly group that bumps them red until someone edits
  `ops/video/package.json`, and that cost deserves its own decision.
