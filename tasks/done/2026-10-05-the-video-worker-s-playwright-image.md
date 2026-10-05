---
id: 2026-10-05-the-video-worker-s-playwright-image
title: The video worker's Playwright image tag and @playwright/test version can drift apart
status: done
priority: P3
area: tools
owner: claude-opus-5-5-playwright-tag-sync
claimed_at: 2026-10-05T07:27:14Z
created_at: 2026-10-05T07:26:52Z
completed_at: 2026-10-05T07:38:29Z
branch: claude/playwright-tag-sync
depends_on: []
scope:
  - tools/supply-chain.test.mjs
  - .github/dependabot.yml
  - .agents/skills/dev-and-ci/references/dependabot.md
---

# The video worker's Playwright image tag and @playwright/test version can drift apart

## Why

The video worker's image starts `FROM mcr.microsoft.com/playwright:v1.63.0-noble@sha256:…`
(`ops/video/Dockerfile`, pinned by PR #1239). That image carries the browser builds of one
Playwright release, and the worker drives them through the `@playwright/test` that
`ops/video/package.json` installs (`npm install` in the image, without a lock file). A client
from another release looks for browser builds the image does not have and fails at launch, on
the host, in the middle of a video job. `tools/video` in CI and on a laptop runs with the
version in the root `package-lock.json`, so that is the third place the version lives.

Nothing kept the three together:

- PR #1239's Dependabot docker entry for `/ops/video` ignored only semver-major and -minor, so a
  patch tag (`v1.63.1-noble`) could arrive alone while `ops/video/package.json` and the lock file
  stayed at 1.63.0.
- The root npm entry's `minor-and-patch` group bumps `@playwright/test` in `package-lock.json`
  (it is `apps/web`'s devDependency, `^1.63.0`) without touching the image or
  `ops/video/package.json`, which is not a workspace and has no Dependabot entry.
- `tools/supply-chain.test.mjs` checked that the image is pinned by digest, not which release it is.

## Definition of done

- [x] `node --test tools/supply-chain.test.mjs` fails when the Playwright version in the
      `ops/video/Dockerfile` image tag differs from `@playwright/test` in `ops/video/package.json`
      (including a range there) or from `@playwright/test`, `playwright` or `playwright-core` in
      `package-lock.json`, and passes on main as it is (all 1.63.0).
- [x] Dependabot no longer proposes a Playwright image tag on its own: the `/ops/video` docker
      entry ignores patch tags too and keeps refreshing the digest of the tag in use, and the
      `@playwright/test` npm bump arrives as a pull request of its own instead of inside the
      weekly `minor-and-patch` group, where its expected red would hold back the other bumps.
- [x] The comments in `.github/dependabot.yml` and the Dependabot procedure in the `dev-and-ci`
      skill say why, and what a person adds to the red `@playwright/test` pull request.

## Steps

- [x] Add the test to `tools/supply-chain.test.mjs` and prove it red for each drift (patch tag
      alone, a range in `ops/video/package.json`, a missing lock entry, no Playwright `FROM`).
- [x] `.github/dependabot.yml`: `exclude-patterns: ["@playwright/test"]` on the npm group; add
      `version-update:semver-patch` to the `/ops/video` docker ignore; rewrite both comments.
- [x] Validate `.github/dependabot.yml` against the SchemaStore Dependabot schema.
- [x] `.agents/skills/dev-and-ci/references/dependabot.md`: the ecosystem list and a section on
      the `@playwright/test` pull request.

## How to verify

```bash
node --test tools/supply-chain.test.mjs        # 9 pass
npm run check:tasks
# Drift: change `v1.63.0-noble` to `v1.63.1-noble` in ops/video/Dockerfile and run the test
# again; "the video worker's Playwright image is the release of the @playwright/test it
# installs" fails and lists the four 1.63.0 entries. Restore the file.
```

What only GitHub proves: after merge, Insights > Dependency graph > Dependabot shows the
configuration parsed, and the next `@playwright/test` release opens its own npm pull request
(red until the image and `ops/video/package.json` are added to it) while the `/ops/video`
docker entry opens nothing but digest refreshes.

## Notes

- Choice. The npm side leads and the docker side only refreshes digests. The other way round
  cannot work: the docker entry ignores minor tags (a Playwright minor is a migration like any
  other base image's), so it would never propose 1.64, and the npm group would still bump the
  lock file alone. With npm leading, every release (patch, minor or major) arrives as one
  `@playwright/test` pull request that the new test turns red until a person adds the image tag
  and digest and `ops/video/package.json` to it; touching `ops/video/` then runs the
  `Video worker image` workflow, which builds the image and renders the example in it.
- Rejected: Dependabot's multi-ecosystem groups (`multi-ecosystem-groups` /
  `multi-ecosystem-group`). They put whatever each ecosystem found that week into one pull
  request; they do not make the versions match (npm can see 1.63.1 a day before Microsoft
  pushes the image), they need `patterns` on every member entry, which changes how the root npm
  entry groups everything else, and still nothing would update `ops/video/package.json`. An npm
  entry for `/ops/video` was not added either: it has no lock file, and it would bump the fonts
  and pinyin-pro there on their own schedule, a new way for that file to drift from the lock.
- Checked in dependabot-core (main, 2026-10-05): an `update-types` ignore of
  `version-update:semver-patch` is the range `> current, < next minor`
  (`common/lib/dependabot/version.rb`, `ignored_patch_versions`), so the current tag stays a
  candidate, and `docker/.../update_checker.rb` `digest_requirement_up_to_date?` still compares
  that tag's digest, which is how a same-tag rebuild arrives. `v1.63.0-noble` parses as version
  1.63.0 with suffix `-noble` (`docker/.../tag.rb`, `VERSION_WITH_SFX`). Group exclusion:
  `common/lib/dependabot/dependency_group.rb` `contains?` rejects an `exclude-patterns` match
  before anything else, and a group without `patterns` matches every other name, so
  `minor-and-patch` keeps everything but `@playwright/test`.
- The docker ignore uses `dependency-name: "*"` rather than the image's name: Dependabot names
  the dependency `playwright` (the image path without the registry, `shared_file_parser.rb`
  `build_dependency`), which is easy to get wrong, and Playwright is the only image in
  `ops/video/Dockerfile`; the comment says so.
- `ops/video/package.json` also pins `@fontsource-variable/*` and `pinyin-pro` "at the versions
  the repository's package-lock.json pins", and nothing checks those either; they match today.
  Left alone here because checking them would turn every weekly group that bumps them red until
  someone edits that file, which is a decision of its own: filed as
  `2026-10-05-ops-video-package-json-s-fonts`.
- `.agents/skills/dev-and-ci/references/dependabot.md` was added to the scope: it is the
  procedure an agent follows for weekly Dependabot pull requests, and the `@playwright/test` one
  is now expected red until someone adds two files. References are not mirrored under
  `.claude/skills/` (#1222), so there is no second copy.
