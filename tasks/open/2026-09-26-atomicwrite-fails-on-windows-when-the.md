---
id: 2026-09-26-atomicwrite-fails-on-windows-when-the
title: atomicWrite fails on Windows when the target is briefly locked (EPERM on rename)
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-26T02:29:02Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/paths.mjs
---

# atomicWrite fails on Windows when the target is briefly locked (EPERM on rename)

## Why

On 2026-09-26, one full `npm run test:tools` run on Windows failed
`check-audio flags only the line Jev doubts, writes a redo file, and reuses its work`
(`tools/video/tts/check.test.mjs:132`) with:

```
Error: EPERM: operation not permitted, rename '...\review\check.json.27168.tmp' -> '...\review\check.json'
    at atomicWrite (tools/video/core/paths.mjs:52)
    at checkAudio (tools/video/tts/check.mjs:172)
```

The same file passed four times in a row on its own. Windows refuses to rename over a file that
another process holds open for a moment, for example Defender or the indexer scanning a file
that was just written. The rename fails at once, although waiting a few milliseconds would let
it through. Linux CI never sees this. The owner's machine does, and `check-audio`, `tts`,
`approve` and `auto` all save state through `atomicWrite`: one unlucky rename ends the command.

## Definition of done

- [ ] On Windows, `atomicWrite` retries a rename that fails with `EPERM`, `EACCES` or `EBUSY` for a
      short, bounded time before giving up, the way graceful-fs does. Other platforms and other
      errors behave as before.

## Steps

- [ ] Add the retry in `tools/video/core/paths.mjs`, with a test that fakes a rename failing twice.

## How to verify

`node --test tools/video/core/*.test.mjs`. On Windows, `npm run test:tools` run a few times in a row.

## Notes

Seen while working on `2026-09-26-the-render-font-check-fails-slides`, which does not touch
`paths.mjs`.
