---
id: 2026-10-27-repair-kimi-foreign-reference-caption-pacing
title: Repair Kimi foreign reference caption pacing
status: done
priority: P2
area: tools
owner: codex-ai-tech-news
claimed_at: 2026-10-27T02:24:02Z
created_at: 2026-10-27T02:23:37Z
completed_at: 2026-10-27T03:10:17Z
branch: codex/ai-tech-kimi-20261026
depends_on: []
scope:
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
  - docs/videos/kimi-k31-3d-delivery/captions/reading-balanced
  - docs/videos/kimi-k31-3d-delivery/receipts/production/caption-pacing
  - docs/videos/kimi-k31-3d-delivery/production-progress.json
  - docs/videos/kimi-k31-3d-delivery/README.md
  - tasks/open/2026-10-26-ai-tech-kimi-k31-3d-delivery.md
---

# Repair Kimi foreign reference caption pacing

## Why

Some foreign narration-reference caption cues exceed their unchanged reading-speed limits although the complete original sentence window has sufficient time. Spoken-weight allocation differs from the actual display-width metric. Improve feasible internal timing without shortening a translation, changing sentence windows or touching any audio. Original overfull windows remain reported.

## Definition of done

- [x] Native caption logic makes only feasible foreign narration-reference cue timing more readable; exact text/cuts/count/order and first/last endpoints remain, all locale/min-duration limits unchanged, measured/source and actual dub timing preserved.
- [x] Meaningful regression checks cover feasible actual skew, infeasible unchanged findings and measured/source/dub preservation.
- [x] One normal Kimi captions stage runs under the unique native producer lease after full before archives; actual nine-locale output/intended/frame windows/source/audio/global holds are independently verified.
- [x] Current changed SRTs and honest component results are delivered to the same pending review with old versions retained, then normal full binary downloads verified. Keep old whole-QA false, source approvals/listening pending and foreign checked M4A0/8.
- [x] Scoped public receipts/progress/task/Git/PR are saved without auto-merge, deployment or YouTube.

## Steps

- [x] Read latestcheckpoint/AGENTS/skills/task/progress; inspect actual processes/LEASE/state/mtimes/globalholds and collisions for the exact caption code and episode.
- [x] Claim this narrow task on the existing sole Kimi branch/PR; parent remains blocked/unclaimed.
- [x] Review native fix and independent regression evidence; preserve all original code/media/CC bytes before the one native captions run.
- [x] Root runs normal stage once, verifies current nine-locale outputs and all protected original source/audio/QA/journals/holds.
- [x] Separately review/release current-only backend delivery; verify complete actual readback before updating public docs and completing this task.

## How to verify

Use the unchanged LOCALE_RULES (zh9/ja8/ko12/en20/esptidvi17/th15), MIN_CUE_MS900 and LINGER_MS400. Never extend a sentence window, omit text, resynthesize or transcribe. Only foreign reference allocation with no matched own measured timing may change; source and actual dubbed paths stay exact. Rebuild native captions, check all full intended literal text and monotonic same source-line endpoints, genuine v4 intro5/outro21 boundaries, actual component before/after findings, and retain irreducible overfull lines. Exact unchanged main3cbd/body3784/sourcea8/114WAV/8i18n/QAfalse/R4false/DFA sent/global342d+ad19. Normal final/audio review cannot attach any unverified dub. New backend phase preserves the old whole falseQA and existing choices/history, archives old changed subtitle FileRefs, and has no paid/approval/projectPUT routes. No other project/page/schedule/global pipeline setting changes.

## Notes

- Baseline HEAD3e3155271b1addf845cdc9e3ee403272d02e1466/PR1873 OPEN DRAFT no-auto-merge; currentpendingb189 has28 verified refs, sourceunlistenedM4A1/foreignchecked0/8. Previous media/backend helpers are obsolete and must not replay.
- Exact sharedcode collision and episode collision return no active tasks/sole ownPR1873. Current KimiLEASE absent, state last2026-10-26T23:29:57, no actualWhisper/check-audio producers; heldASRPID304867 dead but reservation unchanged. New providerAPI delta audit found no new legitimate lookup, so all unknowns and paid holds remain.
- Root will retain the original47 subtitle speed findings as a dated historicalQA/component record, not clear flags or claim wholeQA passes. This is still narration-reference CC, not future foreigndub timing.
- New scratch: /workspace/work/ai-tech-next/new-popular-topic-20261026/caption-pacing-20261027. No new topic/DNSwatch/ForTy retry/otherchat/merge/deploy/YouTube.

- Actual completed delivery: final code df93ab9f/a514fe10 independently reviewed; final unit session12993 exit0/55PASS, targeted caption/stages/dub-package/renewal session15105 exit0/167PASS. Original second fixture failure and all interim code/test review histories remain; final correction preserves original inheritance and applies only after it. First Root pure-profile builder17004 failed before imports/writes on unused font/render pin scope; original preserved, V2 native-only111pins builder68442 exit0. Ordinary+ownednativepreflight30077 exit0. One native captions session65174/PID360369 exit0,20 original byte-copy archives/19 actual outputs plus one real state event,1583 protected inputs unchanged. Independent Rootpost40518 exit0/proof99145dfbd1a0efde7ce799f6b49207ee004213eaac887c0caac71276eefbc2f2; original/passing/residual group times and full literal text verified, current47→23 findings.
- One backend helper91802/PID361034 exit0/auth1GET4PUT7POST1fileGET7/denied0/paid0. Six en/es/pt/id/vi/th current SRTs replaced at original indices; six old versions retained plus component report; samepending now35refs, all28 old binary contents remain live. Normal all35 session40763 exit0 and independent GET29313 exit0/HTTP200/full45281B839c814e283cb8cc136917e1eb9cedf99afc19def65699977e9f5f490816e0d5. Rootall35 verifier16159 exit0/proofe0a57ef46646e224f79875ce63ea822dd9f2c22609e2e2f1024d3baff34c069d. Publicdocs writer72852 exit0/35newtextfiles+3existingdocs. Old wholeQAfalse47+3/R4/sourceaudio/globalholds/114listeningpending/foreigncheckedM4A0/8 preserved; parent remainsblocked/unclaimed, no approval/merge/deploy/YouTube.
