---
id: 2026-10-23-c20-zippo-source-bound-six-chapter
title: C20 Zippo: source-bound six-chapter Treatment
status: review
priority: P1
area: docs
owner: codex-root-c20
claimed_at: 2026-10-23T03:47:26Z
created_at: 2026-10-23T03:47:16Z
completed_at:
branch: codex/brand-story-zippo-c20
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/treatment.md
  - docs/videos/story-everyday-zippo-c20/source-matrix.md
---

# C20 Zippo: source-bound six-chapter Treatment

## Why

The approved twenty-episode plan names C20 as the Zippo repair-promise story. The series plan's official links are discovery leads, not verified claims. Establish what the original product and guarantee were, what today's repair actually covers, and where later company recollections are the only history source before writing a script.

## Definition of done

- [x] Six-chapter Treatment tells a chronological, hook-led story with the owner-fixed Curio look and an eight-minute body target.
- [x] Claim matrix binds every date, mechanism, scope, and exception to directly readable primary sources, marking company recollections.
- [ ] A different agent audits the exact Treatment and matrix hashes; any HOLD is repaired and rechecked.
- [ ] Draft PR and owner Treatment gate remain separate from script approval, paid media, upload, and publication.

## Steps

- [x] Read the series plan and brand-story / Curio / YouTube story rules.
- [x] Open Zippo's history, repair, guarantee, current-product and original US patent records.
- [x] Write Treatment and source matrix.
- [ ] Push draft PR, obtain independent claim review, and read back state.

## How to verify

Read each source at its cited page or section. Compare the claim matrix to Treatment line by line; compute Git blob SHA-256 for both author files. Run `npm run check:tasks` and `git diff --check`; inspect PR head, draft status, and auto-merge state.

## Notes

2026-10-23: Official Zippo history says the first pocket lighter was made in 1933 and offered the repair promise at $1.95; these details are later company recollection. US 2,032,695 is the original 1934-filed/1936-granted patent, with multiple listed inventors. Today's windproof lighter repair page says inserts normally are **replaced**, not repaired, and the finish is excluded; the separate arc insert has a two-year warranty. Do not claim every Zippo product has lifetime coverage or that shipping, fuel, flints, or a pristine exterior are free. The causal economics of the guarantee are not established by these sources.

2026-10-23: Reopened the current service pages: the old US `/pages/repairs-windproof-lighter` URL redirects to a general knowledge page. The still-readable **UK official repair page** directly supports its normal replacement-of-insert procedure, while the current US knowledge base independently states the windproof-product scope and finish exclusion. Treatment and matrix now name these as distinct regional sources, not one universal policy. The original US patent scan confirms *two* named inventors (Gimera and Blaisdell), whereas the assignee partnership lists five people; the script must not conflate them. Current draft has 13 matrix items and remains subject to independent audit and owner Treatment adoption.

2026-10-23: Author Treatment and matrix staged as exact Git blobs. SHA-256 Treatment `DDB768024F4560C00CEEF298C1D2EE48145683544DF0BECE4E88331885D2A2B6`; matrix `741689FC4BF7D2705546567DEE067AAA884C58CFF61E1ABC9D13C1BC8B3A78CB`. `npm run check:tasks` and `git diff --check` pass, with unrelated pre-existing queue warnings. Independent review has not yet run; these hashes are author evidence only. Owner has not adopted C20 Treatment.
