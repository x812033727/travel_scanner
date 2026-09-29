---
id: 2026-09-29-manual-upload-browser-spec-accepts-windows
title: Manual upload browser spec accepts Windows clipboard line endings
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-29T10:58:34Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/admin-video-manual-upload.spec.ts
---

# Manual upload browser spec accepts Windows clipboard line endings

## Why

On Windows Chromium, the operating-system clipboard returns CRLF after the manual-upload panel copies an LF-separated description. `admin-video-manual-upload.spec.ts:125` compares the raw clipboard string with the LF fixture. All four zh-TW new/existing-video cases fail at this assertion even though every character other than line terminators is correct; later caption/thumbnail assertions are never reached.

Discovered during Shorts shared-fixture regression. The unchanged main spec/component and original main runtime fixture reproduce it, so this is independent of the Shorts runtime addition.

## Definition of done

- [ ] Copied descriptions compare exactly after normalizing only platform CRLF line endings; preserve all other characters, spaces, paragraph breaks and trailing content.
- [ ] The zh-TW new/existing cases pass on desktop and mobile Chromium on Windows and still exercise captions, thumbnail downloads and unchanged form values.
- [ ] A real missing/changed description character still fails; do not trim strings, mock clipboard reads, add retries or raise timeouts.

## Steps

- [ ] Read `web-i18n-e2e` and inspect the clipboard comparison and current branch/PR ownership before claiming.
- [ ] Apply a narrowly scoped newline normalization to the clipboard comparison and run its browser cases.

## How to verify

```bash
cd apps/web
npx playwright test e2e/admin-video-manual-upload.spec.ts -g 'zh-TW manual upload' --repeat-each=3 --workers=1
```

Use the local runtime API with synthetic credentials only. The grep is intentionally not start-anchored because Playwright includes project/file names when matching the full test title. Verify both browser projects and a negative text-mutation check.

## Notes

- 2026-09-29 Windows / Chromium 153.0.8010.12: four traces / 28 clipboard reads show only LF-to-CRLF conversion. Synthetic unsent description grows 48→49 characters; original approved description grows 97→100. Blank-page probes reproduce both strings on desktop/mobile without loading product code or an API.
- Baseline at `452cdd05` / `8e6026d9`: spec and component Git bytes are unchanged. Original runtime fixture SHA256 `98521df362cad2b21819838d0021d763f303856f30ebca9b27cbdbb3eb8063e0` reproduces the desktop new-video failure at the same line. This is not a green manual-upload regression result.
- Private evidence: `C:/Users/x8120/.codex/tmp/video-shorts-browser-20260929/manual-upload-smoke.log`, `manual-baseline.log`, `manual-upload-clipboard-diagnosis.json`, `clipboard-platform-probe.mjs` and `clipboard-platform-probe.json`.
- Prior precedent: `tasks/done/2026-09-14-gemini-advanced-visible-ui.md` records Windows clipboard CRLF normalization, but no existing open ticket tracked this manual-upload spec.
