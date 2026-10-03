---
id: 2026-09-29-manual-upload-browser-spec-accepts-windows
title: Manual upload browser spec accepts Windows clipboard line endings
status: done
priority: P3
area: web
owner: codex-clipboard-e2e
claimed_at: 2026-09-29T11:06:01Z
created_at: 2026-09-29T10:58:34Z
completed_at: 2026-09-29T11:13:20Z
branch: codex/shorts-browser-coverage
depends_on: []
scope:
  - apps/web/e2e/admin-video-manual-upload.spec.ts
---

# Manual upload browser spec accepts Windows clipboard line endings

## Why

On Windows Chromium, the operating-system clipboard returns CRLF after the manual-upload panel copies an LF-separated description. `admin-video-manual-upload.spec.ts:125` compares the raw clipboard string with the LF fixture. All four zh-TW new/existing-video cases fail at this assertion even though every character other than line terminators is correct; later caption/thumbnail assertions are never reached.

Discovered during Shorts shared-fixture regression. The unchanged main spec/component and original main runtime fixture reproduce it, so this is independent of the Shorts runtime addition.

## Definition of done

- [x] Copied descriptions compare exactly after normalizing only platform CRLF line endings; preserve all other characters, spaces, paragraph breaks and trailing content.
- [x] The zh-TW new/existing cases pass on desktop and mobile Chromium on Windows and still exercise captions, thumbnail downloads and unchanged form values.
- [x] A real missing/changed description character still fails; do not trim strings, mock clipboard reads, add retries or raise timeouts.

## Steps

- [x] Read `web-i18n-e2e` and inspect the clipboard comparison and current branch/PR ownership before claiming.
- [x] Apply a narrowly scoped newline normalization to the clipboard comparison and run its browser cases.

## How to verify

```bash
cd apps/web
npx playwright test e2e/admin-video-manual-upload.spec.ts -g 'zh-TW manual upload' --repeat-each=3 --workers=1
```

Use the local runtime API with synthetic credentials only. The grep is intentionally not start-anchored because Playwright includes project/file names when matching the full test title. Verify both browser projects and a negative text-mutation check.

## Notes

- 2026-09-29 Windows / Chromium 153.0.8010.12: four traces / 28 clipboard reads show only LF-to-CRLF conversion. Synthetic unsent description grows 48→49 characters; original approved description grows 97→100. Blank-page probes reproduce both strings on desktop/mobile without loading product code or an API.
- Baseline at `452cdd05` / `8e6026d9`: spec and component Git bytes are unchanged. Original runtime fixture SHA256 `98521df362cad2b21819838d0021d763f303856f30ebca9b27cbdbb3eb8063e0` reproduces the desktop new-video failure at the same line. This is not a green manual-upload regression result.
- Private evidence: `<home>/.codex/tmp/video-shorts-browser-20260929/manual-upload-smoke.log`, `manual-baseline.log`, `manual-upload-clipboard-diagnosis.json`, `clipboard-platform-probe.mjs` and `clipboard-platform-probe.json`.
- Prior precedent: `tasks/done/2026-09-14-gemini-advanced-visible-ui.md` records Windows clipboard CRLF normalization, but no existing open ticket tracked this manual-upload spec.

### 2026-09-29 completion

- Changed only the real clipboard read's CRLF-to-LF normalization; exact `toBe(description)` remains. Independent diff review confirms spaces, paragraph counts, other characters and lone CR remain significant. No production component, clipboard mock, timeout or retry changes.
- Local Windows Chromium: zh-TW new/existing cases on desktop and Pixel 7, `--repeat-each=3 --workers=1`: **12/12 passed**, 2.8 minutes, exit 0. Each case exercises all five language descriptions and caption downloads, thumbnail bytes, and new-video form preservation.
- Negative check: temporarily expected `description.slice(1)` while reading the unchanged real clipboard. The assertion failed at line 127 (`ynthetic` versus `Synthetic`), exit 1. Restored exact fixed-file SHA256 `4cfeac0f232a440fef753641ae382f3349d001bcdb9c642e9a854b37efc464e5`; the desktop new-video case then passed again (12.3 seconds, exit 0).
- Scoped ESLint and full web typecheck passed, including a final typecheck after generated-file restoration. Rebased onto upstream `1ce1a337`; full tools passed **732 with 2 existing platform skips, 0 failed** (734 tests, 151.7 seconds), task validation passed for 1154 files, and i18n passed for five locales / 25 namespaces. Before claim and push, inspected active task scopes (including ancestors), available worktrees, remote heads and fully paginated PR files; no outside competing change.
- Evidence: `<home>/.codex/tmp/manual-upload-clipboard-20260929/README.md`, with original/fixed file backups, repeated browser log, negative receipt and restored-case log. Owned loopback servers stopped; generated next-env restored byte-for-byte. Included as a follow-up in draft PR #982 with the Shorts runtime coverage that exposed the issue.
