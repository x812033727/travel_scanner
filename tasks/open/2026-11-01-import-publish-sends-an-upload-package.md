---
id: 2026-11-01-import-publish-sends-an-upload-package
title: import --publish sends an upload package before the languages batch, which then can never be sent
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-01T06:55:16Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/import
---

# import --publish sends an upload package before the languages batch, which then can never be sent

## Why

2026-11-01: zhong-tian-qu-qi-e032 and e034 got `import --from DIR --publish --clips …` right after their final cut was
approved, before the owner had ticked languages. The package went through (with every language's dub and CC in it) and
the owner approved it. Then the owner ticked the languages, and `import --languages` refuses ("an upload package was
already sent; a languages batch after it would not match it", `tools/video/import/import.mjs` around line 290). The site's
`ready_to_upload` (apps/api/app/video_reviews/admin_service.py) needs `locales_decided_at` and no chosen part "working",
so both videos are neither ready to upload nor eligible for the Drive backup
(`apps/api/app/video_backup/admin_status.py` `_eligible`). docs/videos/COMPILATIONS.md row 6 says "先送語言、再送上傳包",
but nothing enforces it.

## Definition of done

- [ ] `import --publish` refuses when the owner has not decided languages, or when a chosen part has no approved
      languages batch, and says to run `--languages` first (a video with only zh-TW chosen still goes).
- [ ] A test in tools/video/import for both refusals.
- [ ] Write down the recovery for a package already sent in that order (e032, e034), once the owner picks one.

## How to verify

`node --test tools/video/import/*.test.mjs`
