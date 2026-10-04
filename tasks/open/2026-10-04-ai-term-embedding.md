---
id: 2026-10-04-ai-term-embedding
title: AI term embedding video
status: in-progress
priority: P2
area: docs
owner: codex-ai-series-continuation-embedding
claimed_at: 2026-10-04T12:42:32Z
created_at: 2026-10-04T12:42:30Z
completed_at:
branch: codex/ai-term-embedding-20261004
depends_on: []
scope:
  - docs/videos/ai-term-embedding
---

# AI term embedding video

## Why

Continue the owner's existing AI video series with the tier-1 Embedding topic already listed in `docs/videos/ai-terms/terms.json` and `docs/videos/long-form/plans.json`. The article/video slug is `ai-term-embedding`; this is backlog production, not a new topic or a competing LLM/RAG episode.

The episode should let a viewer distinguish a related search result from one that satisfies the actual conditions. A reproducible offline example can calculate cosine similarity for explicitly hand-assigned vectors, then check rainy-day activity conditions. Label those coordinates as a numerical illustration, not measured model embeddings, a fixed meaning for each dimension, or proof of factual truth. Any genuine model demonstration instead needs its actual model/version, inputs, outputs and execution evidence.

The owner's continuation request includes completed-media backup to G followed by eligible local cleanup. This task therefore remains unfinished until the current film, selected languages and exact backend delivery are verified, followed by the existing archive safeguards. Source preparation alone, a successful generation, or an old approval is not completion.

## Definition of done

- [x] A source-bound brief offers distinct outlines, states the viewer's practical outcome and uses the real channel stance; the normal outline review is approved and its exact hash is pulled before dependent production.
- [x] `video.json`, claims, source records and independent fact/listener reviews explain Embedding accurately, distinguish it from LLM generation and the wider RAG workflow, and contain no unresolved factual or demonstration claim.
- [x] The offline demonstration is independently recomputed from preserved inputs and actual outputs, with an explicit hand-assigned-vector boundary or genuine model provenance. Sources and dated product/version claims are checked against primary material when the script is written.
- [ ] Actual substantive spoken PCM and actual body/final duration each meet the effective long-form minimum of eight minutes. Current clip, narration and timeline SHA bindings, pronunciation checks, chapters and cadence pass; silence, repetition or slower playback do not fill the minimum.
- [ ] Current illustrations and rendered frames are independently inspected against their prompts and framing; real failures remain recorded. The current storyboard gate, final QA and exact final review pass without editing verdicts, lowering thresholds or buying duplicate unknown requests.
- [ ] The current upload package, branding, captions, metadata and disclosures pass the normal publish checks and exact-hash approval. Only the owner's current selected language parts are produced/reviewed, with explicit selection and current language gate evidence; undecided/unfinished parts preserve their sources.
- [ ] Fresh sanitized backend GET readback proves the current final/publish/languages statuses and matching delivered final/package/language hashes. Backend approval, automatic policy approval, owner listening/playback and YouTube publication remain distinct states.
- [ ] An explicitly completed candidate is archived under the new G batch with per-file source SHA-256, complete ZIP integrity/safe restore verification and fresh DriveFS cloud ID/MD5/size/zero-pending-operation proof. Unavailable/insufficient G or incomplete cloud proof preserves all originals.
- [ ] Eligible local media is removed only from the reviewed exact per-file plan after fresh backend, source, active-process, reparse and retention/shared-dependency checks, using native PowerShell and a verified journal. Text, JSON, approvals, source code, receipts, unfinished media and retained/shared sources remain available.

## Steps

- [x] Read the 20:30 collision refresh and record the already-created isolated worktree, branch and claim; keep this task's changes inside `docs/videos/ai-term-embedding` plus its own task file.
- [x] Recheck candidate worktree/branch/remote/PR/backend collisions before this source PR; repeat before any paid stage. Keep the active LLM production separate; do not duplicate or stop its job.
- [x] Read the current `youtube-video` skill and effective long-form/AI-terms plan; prepare `brief.md` with distinct outline options and a concrete viewer action. Submit/pull through the existing outline gate, preserving automatic versus owner decision evidence.
- [x] Write source, claims and one bounded demonstration; preserve the computation code, inputs, outputs and source hashes under this episode's scope/private evidence. Have an independent reviewer recompute the example and check all claims and the complete spoken script.
- [x] Resolve English pronunciations within the current scope without overwriting the shared lexicon/registry owners. If shared files are necessary, coordinate their actual scope through the task protocol rather than silently expanding this claim.
- [x] Run source lint and TTS/media dry-runs. Inspect current settings, provider combined prompt limits, price/cap and local/remote activity. Current preparation has bought no Embedding TTS/images; do not start dependent paid stages before their normal prerequisites are current.
- [ ] Produce actual narration, measure substantive speech/body time, check current clip hashes and pronunciation, make bounded genuine redo/rewrite only where needed, then submit/pull the exact audio gate. Preserve every uncertain paid request and reconcile its existing receipt before any retry.
- [ ] Generate bounded visual pilots on the existing authorized model/budget, inspect real pixels, then complete illustrations. Reuse unchanged image keys/verdicts and preserve failed originals; only source-bound changed shots are remade. Submit/pull the normal current storyboard gate.
- [ ] Render, assemble with current Mokaair branding, write captions and run final QA. Inspect the actual film and submit/pull the current final gate; a partial STOP exit or high aggregate image score is not a complete film.
- [ ] Build/recheck the upload package and normal publish gate. Read the owner's current language selection from the backend, produce only selected metadata/captions/dubs, verify their source-bound files and submit/pull the language gate. Keep all selected-language sources until current delivery is complete.
- [ ] Save fresh sanitized backend delivery readbacks and matching final/package/language hashes. Declare the completed scope explicitly only when all applicable current delivery conditions pass; do not infer YouTube upload or owner acceptance.
- [ ] Use the private backup runbook/helper for a new explicit candidate inventory, staged ZIPs, new G publish and cloud/restore proof. Audit retention, shared consumers and active use; preserve originals on any failure or uncertainty.
- [ ] Review the exact deletion plan as the executing agent under the owner's existing backup-then-cleanup authorization. If eligible, remove verified media one file at a time with native PowerShell, journal/post-verify, and retain archive/restore pointers before closing this task.

## How to verify

Run from the isolated repository root. These are verification checkpoints for the corresponding completed stage, not instructions to buy media during initial source preparation:

```powershell
npm run check:tasks
node tools/video/cli.mjs lint --slug ai-term-embedding
node tools/video/cli.mjs status --slug ai-term-embedding
node tools/video/cli.mjs tts --slug ai-term-embedding --dry-run
node tools/video/cli.mjs keyframes --slug ai-term-embedding --dry-run
```

Keep media under `<home>/mokaair-work/videos/ai-term-embedding`, outside git. Preserve exact demonstration inputs and output; an independent recomputation must reproduce every displayed cosine score/ranking and separately verify the stated activity conditions. After synthesis, inspect actual PCM samples, current full clip/narration/timeline hashes, current transcript results, chapter/cadence checks and measured speech/body/final durations; planned seconds and word counts do not prove the minimum.

At each existing review gate, use `review-push --slug ai-term-embedding --gate <outline|audio|storyboard|final|publish|languages>` only when that stage is ready, followed by `review-pull --slug ai-term-embedding`; verify the persisted current hash/status through paired backend GET. Run the normal final `qa`, package/file checks and selected-language checks when their inputs exist. Keep no raw credentials in evidence. No gate is bypassed by this task's checklist.

Before archive/cleanup, follow `<home>/mokaair-work/ai-series-continuation-20261004/BACKUP-RUNBOOK.md` and `archive_candidates.py`: explicit completed candidate, SHA-bound fresh backend readback, stable per-file source inventory, ZIP integrity/safe restore proof, fresh cloud ID/MD5/size/operations=0, current process/retention/reparse checks and exact per-file PowerShell journal. Mount free space is a cache/capacity preflight, not cloud quota or proof of synchronized backup. A missing final or language part is a hold, not permission to regenerate already archived media.

When preparing a reviewable source PR, rerun the collision check and repository checks applicable to its changes. Do not merge, deploy, publish to YouTube or change cost/uploader settings from this task initialization.

## Notes

- Initial handoff: 2026-10-04. The task was already claimed as `codex-ai-series-continuation-embedding` on `codex/ai-term-embedding-20261004`; worktree `<home>/.codex/worktrees/ai-series-next-20261004/travel_scanㄐ`. Frontmatter/status are preserved. This initialization changes only this task's body and saves a private receipt.
- Collision evidence is the prior 20:33-20:37 snapshot in `<home>/mokaair-work/ai-series-continuation-20261004/NEXT-refresh-2030.md`: all 34 registered worktrees, 441 local branches and 32 exact remote-head trees had no Embedding source/scope; 66 backend rows had no matching slug/topic. Local and then-current remote main agreed on the existing tier-1 backlog. These are pre-claim observations, not a distributed lock or a claim of fresh remote ownership at every later stage.
- At initialization the isolated checkout was on the claimed branch and Embedding was source preparation without a completed source package or outline approval. The later source/outline checkpoints below supersede that initial stage only; audio/storyboard/final/publish/languages, finished film, paid Embedding generation, G backup and local cleanup remain incomplete.
- The LLM episode is still live in the original worktree (PID37152 at the 20:30 preflight, source `ai-term-large-language-model`). Check current full command/log/receipts before any future action; PID alone may be reused. Do not touch its source/media/backend record or start a duplicate stage while preparing Embedding.
- Existing topic references are `docs/videos/ai-terms/README.md` (suggested order 8), `docs/videos/ai-terms/terms.json` and `docs/videos/long-form/plans.json`. The article and self-owned diagram were GET-available in the collision refresh; Sentence-BERT and Sentence Transformers primary sources were reachable then. Recheck source-specific claims when authoring; the refresh is not independent approval of an unwritten script.
- Registry/lexicon paths have active owners in other tasks. This claim covers only the Embedding episode folder; keep shared files read-only until properly coordinated. Other worktrees' unfinished films, selected language work, receipts and existing approvals remain untouched.
- At the 20:30 completion audit, no current AI candidate was eligible for new archive cleanup. Token/engineering lacked current delivery gates; DevDay had a different current backend final, superseded old publish and 11 selected language parts working. Do not recycle their historical receipts for Embedding or treat an empty local language map as a decided zh-TW-only release.
- Private continuation evidence and future audit receipts live under `<home>/mokaair-work/ai-series-continuation-20261004`; the new G archive base is `G:/<My Drive>/Backup/Mokaair/ai-series-continuation-20261004/<timestamp>`. Public repository notes use `<home>`/`<My Drive>` placeholders. Keep machine paths, media, paired credentials and private readbacks outside the public repository.
- Current source checkpoint: video SHA-256 `487f33c8dccd93057470a6b8d2ab3f6eac465a826d9de8e2f2d720d3669efeeb`, approved brief `c7509f90e80de9fc4acc4c409ee6f46a564a25dfad9adbb1360622289cfdcdbb`. The normal outline policy selected A and auto-approved it at `2026-10-04T12:51:37.582098Z`; exact hash/choice pulled at `12:51:55.742Z` and independently read back. This is automatic policy approval, not owner acceptance of film or audio.
- Full source contains 3,109 spoken units, 156 stable line IDs, 121 scenes, 80 illustrations and six chapters. The body estimate is 885.47 seconds (14.76 minutes), above the initial 8–12 planning range but within the effective 8–30 range; planned seconds do not establish measured speech/final duration. Estimated states are 5–7 seconds and illustration share 50.75%. Lint has zero errors and one whole-opening-chapter warning; the actual first hook/promise are estimated at 4.97/11.03 seconds. Verify these on the real timeline after TTS.
- Independent `verify-1.md` SHA-256 `15a6c0ffe9db0bbd4b17f1d71a982f897110845afaf62331858d521847a75adb` covers all 156 narration lines, 177 visible-card strings, metadata/thumbnail, two Shorts and the self-owned SVG. Twenty-two grouped claims have 21 confirmations, one explicit opinion and zero unresolved changes. Seven primary/article sources returned HTTP 200 today. Independent JS arithmetic plus actual Python 3.14.6 execution reproduce the full JSON and five displayed terminal outputs. Hand-filled coordinates are explicitly a toy; no embedding model, tokenization, training, ANN, vector database or reranker was tested.
- Author and reviewer independently checked byte-identical regeneration, preserved IDs and closed claim boundaries. Current narration is Chinese, Gemini Sulafat with the established Taiwan Mandarin story style; no shared lexicon or registry was changed. The existing model and cost limits remain unchanged.
- Actual dry-runs passed: 121 TTS requests, 3,941 billable characters if synthesized; Sulafat ready in the existing monthly budget. The 80-picture dry-run estimates US$1.09 for one take / US$3.28 at three takes under the US$20 episode cap. The actual MiniMax scene+Style+Camera+Avoid audit covers all 80 prompts, maximum 1,288 characters, with no truncation and none reaching 1,500. These are readiness/cost estimates; no Embedding TTS or image request was bought and no finished-media claim is made.
- Source-only PR verification: `npm run test:tools` initially failed under system Node 24.13 with native crash code `3221226505`. The corrective run with bundled Node 24.19 completed 1,548 tests: 1,538 passed, ten skipped, zero failed. Both original and corrective logs are retained privately as `embedding-test-tools-2030.log` and `embedding-test-tools-bundled-2030.log`; the system failure is not reported as a pass.
- Pre-PR lint under bundled Node 24.19 again returned zero errors and the documented whole-opening-chapter warning. README stage wording now reflects the completed independent source/listener review, and `verify-1.md` preserves the original README hash plus the explicit documentation-only update. The frozen video, approved brief and Shorts hashes remain unchanged. Media acceptance is still outstanding.
- Fresh pre-PR collision check at `2026-10-04T13:43:53.745Z` covered 35 registered worktrees, 443 local branch heads, all 32 exact remote heads and the open PR file scopes. Only this worktree has the Embedding source/active claim; no committed competing source, open PR touching this scope or landed main source was found. GET-only backend readback at `13:41:16.297Z` returned 67 rows and this slug's exact approved-A outline, no later gate, no decided language selection and `ready_to_upload=false`. No separate Embedding production process was found; the simultaneous lint process belonged to this verification. Recheck live state before dependent media work.
- The first staged diff check found one new blank line at `demo.py` EOF; the earlier check could not see untracked content. Only that blank line was removed, preserving the original code. New code SHA-256 is `75950a028e51828f1b3338f5074fd29a0af523bd745976c7a005542506263a0c`; Python 3.14.6 reran JSON and five terminal modes twice, all 12 stdout values exactly matching the independent baseline. Current demo-log hash is `5089564cb5bba2c08eb8320e1848706adde137c99e9a449519017415c768f05e`; `verify-1.md` keeps historical reviewed hashes and records the whitespace/documentation rebind, current hash `c013803c3d74245f18228efbd0584c5e6b57c94202cbc1adf9b55481f2f58ccd`. The frozen video remains `487f33c8dccd93057470a6b8d2ab3f6eac465a826d9de8e2f2d720d3669efeeb`.
