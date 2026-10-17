---
id: 2026-10-10-whisper-pyav19-second-opinion
title: Fix Whisper second opinion compatibility with PyAV 19
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-10T13:02:23Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/whisper_second_opinion.py
---

# Fix Whisper second opinion compatibility with PyAV 19

## Why

The production second transcriber loads its cached Whisper medium model but
fails before decoding every WAV: `faster_whisper.audio.decode_audio` calls
`av.open(..., metadata_errors="ignore")`, while installed PyAV rejects that
keyword. An actual offline four-clip probe on 2026-10-10 returned
`TypeError: open() got an unexpected keyword argument 'metadata_errors'`.
Native audio checking catches this exception and retains the first transcriber's
flags, causing otherwise avoidable paid retakes/rewording and terminal dub skips.

## Definition of done

- [ ] The installed second transcriber decodes real native WAVs with the supported dependency versions.
- [ ] A regression exercises audio decoding, rather than proving only that faster-whisper imports.
- [ ] Normal check-audio records an actual second transcript without changing QA thresholds, paid counters or owner approvals.

## Steps

- [ ] Reproduce the actual dependency mismatch and choose a compatible decode path or pinned dependency combination.
- [ ] Verify the native locale/clip/hints interface, offline cached model and unchanged transcription settings.
- [ ] Run relevant checks and record guarded post-deploy native readback through the owning release workflow.

## How to verify

Use the actual worker Python `/opt/whisper/bin/python` and stock
`tools/video/tts/whisper_second_opinion.py` with a cached medium model and existing
flagged WAVs. Verify exit 0, one real transcript per requested clip, and no model
download. Then run native check-audio and inspect its second-transcriber entries.

## Notes

- Evidence: `C:/Users/x8120/mokaair-work/stalled-video-resume-20261010-3603/whisper-en-offline-pilot-readonly-v1.jsonl` contains full child stderr and unchanged source/clip/state/STOP pins; probe exit 1, no OOM, no paid calls or downloads.
- The active `2026-10-09-dub-skipped-because-jev-still-hears` task enabled the second transcriber, but its import smoke check did not exercise this decode API.
- A private, per-process compatibility shim is being tested only for the seven-video recovery cohort. It does not repair the installed worker image or the other chat's campaign.
- Claim was refused because `2026-10-09-video-languages-are-four-drop-zh` (`claude-fable-5.1`) currently owns an overlapping scope. This task remains open and unclaimed; do not force the claim or modify the shared source while that ownership is active.

## Recovery provenance (2026-10-11)

- 原文與原 front matter 完整保留；本次僅追加此復原出處。created_at、claimed_at、owner、status、branch、scope 及原 checklist 均未改動；沒有重新認領、釋放或結案。
- 原檔：`<home>/.codex/worktrees/3603/travel_scanㄐ/tasks/open/2026-10-10-whisper-pyav19-second-opinion.md`；分支 `codex/stalled-production-resume-20261010`；HEAD `1bd1d47ceab109b1425af01f1571173e95004c8e`。此檔在該 checkout 是未追蹤原稿。
- 原檔 SHA-256：`cc24ac21cdf03b54e43d4a2aaf8ce89089f2e4a5b086d6bef9d4c21e220eb53f`；原始大小 2768 bytes；原文字節副本保存在清理備份及 scratch `prepared-tasks/originals/2026-10-10-whisper-pyav19-second-opinion.md`。
- 比對基準：main `9c46c14ed5c22388be68dec8301695667a226bee`；此 ID 未見於 main、清理工作區的既有任務及 PR #1450 的 `8a8b64782c5ef9e5ab5a3bc17fd1c3e28ffaae69` 快照。整合前再核對最新 main / PR，若已有同 ID 只合併本段出處，不另開票。
- 完整 operational receipt 原始 archive：`tasks/evidence/worktree-cleanup/2026-10-10-production-resume.original.md`；SHA-256 `f1f278888a2a763a3fc5d4455c721baaa533b1ba41896616a1cf776e6edd8a8a`（14616 bytes）。本輪只保全原始收據，不寫入原 owner scope `docs/videos/recovery/2026-10-10-production-resume.md`。原收據的最後更新記錄至 2026-10-10 21:14 Taipei，不代表此刻程序或製作仍在執行。
- 原票中的「目前」、PR 狀態、claim 衝突及主機狀態都是當時快照。續作前應唯讀核對現有 owner、相同 scope、已知 job / source / review hashes、STOP 與 lease，沿用收據而非重買或重跑未知請求。恢復票不構成 provider / 正式站 / 發布的新授權。
- 21:05 的私人 PyAV 19 四段相容性 pilot 為 exit 0，SHA-256 `ae10fbf530d91f0e0059feb318f2ca4a7b2c23f032ddbb43e7047b38c95637b3`；此證據僅適用原輸入與私有 per-process shim，沒有證明 installed worker 或其他 campaign 已完成修補。21:14 的 V5 JA/EN 啟動記錄尚不等於正常音訊 QA、owner playback、上傳或公開。
