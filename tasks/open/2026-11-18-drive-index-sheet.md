---
id: 2026-11-18-drive-index-sheet
title: Generate a daily Google Drive index sheet of every show and episode
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-18T02:27:51Z
completed_at:
branch:
depends_on:
  - 2026-11-18-drive-links-in-admin
scope:
  - docs/videos/ai-drama-drive/catalog.py
  - tools/video/automation/drive-index.mjs
---

# Generate a daily Google Drive index sheet of every show and episode

## Why

Nothing lists what is on Drive: the explainer catalog (`docs/videos/ai-drama-drive/catalog.py`) covers only 奇聞檔案局/原來如此事務所 and is uploaded by hand; the dramas, Shorts and other series have none, and 製作檔/ has no manifest, so a session cannot tell whether reference art already exists (2026-11-12-tai-nainai-e009-e060-missing-refs).

## Definition of done

- [ ] A Google Sheet (or CSV) under `AI/備份/_總表`, refreshed daily, one tab a show: code, title, topic, state, YouTube, Drive folder link, backup state, size.
- [ ] Each 製作檔 upload leaves a manifest.json the index reads.

## Steps

- [ ] Generalise catalog.py to every series, reading ids from the site (phase 1).
- [ ] Have todrive.sh write manifest.json + SHA256SUMS.
- [ ] Schedule it on the host beside rules-sync.

## How to verify

See the steps; each lands with tests.

## Notes

Phase 2 of the Drive plan.
