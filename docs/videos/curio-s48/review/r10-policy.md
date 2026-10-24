# S48 R10 — full script policy and site script card

2026-10-20 UTC. The [independent source and written visual review](r10-source-independent.md) and [two fresh narrative readers](r10-official-panel.md) passed the exact R10 script. `review-push --report-only` reported the project without submitting a card; a site readback confirmed `category=explainer`, `format=drama` before Jev was called.

The complete 3,145-character narration was sent once through `policyRequest({ doc, brief })`, request SHA-256 `532a059c1160fbf07c802ecd1c3c8c33d31e4063fde21a93d2f5e13b5e8ee784`. The private pre-dispatch journal and raw answer are in `/workspace/.video-work/curio-s48/review/policy-pre-tts-r10.attempt.json` and `policy-pre-tts-r10.json`; the [public receipt](r10-policy.json) contains only hashes, lengths, scores and the verdict.

Jev returned `questions=explainer`, **PASS**: stance 0.73, demo not applicable, advice 0.01, sponsored 0.08. The public receipt SHA-256 is `fc6864b9416e42f87d5b3e2a8668ecd92c7f0df6d5cda9f25acc53af113e14e1`.

`review-push --gate script` submitted the exact `script.md` SHA-256 `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd`. The site readback shows the R10 card `hand_pushed=true`, `status=pending`; `review-pull --gate script` reports “waiting for the owner”. Separately, the local `approvals.json` records a **delegated editorial choice** under the owner's standing recommended preference for this same SHA. That local choice permits the next production check and does not represent a website decision.
