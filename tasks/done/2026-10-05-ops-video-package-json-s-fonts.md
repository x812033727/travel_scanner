---
id: 2026-10-05-ops-video-package-json-s-fonts
title: ops/video/package.json's fonts and pinyin-pro can drift from package-lock.json
status: done
priority: P3
area: tools
owner: claude-opus-5-5-video-fonts-pinyin-sync
claimed_at: 2026-10-05T13:17:08Z
created_at: 2026-10-05T07:36:47Z
completed_at: 2026-10-05T13:28:08Z
branch: claude/video-fonts-pinyin-sync
depends_on: []
scope:
  - tools/supply-chain.test.mjs
  - ops/video/package.json
  - .github/dependabot.yml
  - .agents/skills/dev-and-ci/references/dependabot.md
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

- [x] A test fails when a dependency in `ops/video/package.json` is not an exact version or is
      not the version `package-lock.json` resolves for that name, and passes on main.
- [x] Someone decided, and wrote down in the test's comment or `.github/dependabot.yml`, how a
      weekly npm group that bumps one of these gets past that test (edit `ops/video/package.json`
      in the Dependabot pull request, or keep these packages out of the group the way
      `@playwright/test` is).

## Steps

- [x] Generalize or add next to the Playwright check in `tools/supply-chain.test.mjs` (the
      Playwright one compares the image tag too; this one only package.json against the lock).
- [x] Choose how Dependabot bumps reach `ops/video/package.json`; `.github/dependabot.yml` is
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
- 2026-10-05 claude-opus-5-5-video-fonts-pinyin-sync: added `.github/dependabot.yml` and
  `.agents/skills/dev-and-ci/references/dependabot.md` to the scope (the decision changes the npm
  groups, and the reference tells whoever reviews the weekly PRs what to add). No overlap: no
  active task or open PR touched any of the four paths.
- Test: `the video worker installs exactly the versions package-lock.json resolves` compares every
  dependency in `ops/video/package.json` with `package-lock.json`'s `node_modules/<name>` version.
  The lock always holds one exact version, so equality also rules out ranges; `@playwright/test`
  is covered again (harmless, its own test also compares the image).
- Decision: edit `ops/video/package.json` on the Dependabot pull request, and keep these packages
  out of `minor-and-patch` so that red does not hold back the week's other bumps, the way
  `@playwright/test` is. Unlike Playwright they come together in a `video-worker` group
  (`patterns: ["@fontsource-variable/*", "pinyin-pro"]`, minor and patch): fontsource releases
  its fonts together, so one red pull request needs one edit instead of several that conflict in
  the lock. The wildcard also takes noto-sans-jp/kr/sc, which the worker does not install; a
  pull request that moves only those stays green. Read in dependabot-core (main, 2026-10-05):
  `DependencyGroup#contains?` rejects an `exclude-patterns` match first and a group without
  `patterns` matches every other name; `WildcardMatcher` turns `*` into `.*`, so it crosses the
  `/` of a scope. Majors of these packages still arrive one per package, as before.
- Found a second gap and filed it: `tools/video/render/fonts.mjs` draws ko, zh-CN and ja
  thumbnails with noto-sans-kr/sc/jp (#1109, #1111), which `ops/video/package.json` never got, so
  in the worker `render --thumbnails-only` throws "not installed" and every language batch keeps
  the video's own thumbnail. A second test now requires every `FONT_PACKAGES` font in
  `ops/video/package.json` or in `WORKER_FONTS_NOT_INSTALLED_YET` with an open task;
  `2026-10-05-video-worker-image-lacks-locale-thumbnail` (P2) installs them. Left out here because
  it changes the worker image and turns on a path that has not run on the host.
