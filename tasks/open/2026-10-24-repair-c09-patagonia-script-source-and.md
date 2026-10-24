---
id: 2026-10-24-repair-c09-patagonia-script-source-and
title: Repair C09 Patagonia script source and duration
status: in-progress
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T01:25:27Z
created_at: 2026-10-24T01:25:23Z
completed_at:
branch: codex/c09-patagonia-script-repair-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09/script.md
  - docs/videos/story-everyday-patagonia-c09/visual-plan.md
  - docs/videos/story-everyday-patagonia-c09/script-evidence.md
  - docs/videos/story-everyday-patagonia-c09/reviews
---

# Repair C09 Patagonia script source and duration

## Why

C09's owner-approved treatment has a script draft, but the independent 83-line
source/visual review held `c090304`: it made durable pitons cause more people
to return to the same route, which the 1972 preface does not support. That
draft also had only 2,111 spoken Han characters, below 480 seconds at a paper
rate of 270–300 characters/minute. Repair the unsupported claim and add only
new, directly sourced narrative steps. Keep the owner script and paid gates
separate.

## Definition of done

- [ ] Every revised/new sentence and matching shot passes another agent's
      final-hash source and visual-delta review, with no unsupported causal
      claim or unstated historical reconstruction.
- [ ] Two independent readers, seeing only the Traditional Chinese narration,
      give final-hash story verdicts against all 12 listener criteria; record
      any shared HOLD and repair before requesting owner script approval.
- [ ] All narration IDs have exactly one shot/card, the visual precheck and
      name/pronunciation risk are recorded, and paper duration remains clearly
      distinguished from actual voice duration.
- [ ] Submit the reviewable final script/visual direction to the owner; no paid
      voice, image, music, upload or publication occurs under this task.

## Steps

- [x] Read the approved treatment, previous independent HOLD and S1–S4
      primary/contemporary sources. Confirm no active C09 task or open PR owns
      these paths; claim this exact scope in the shared checkout.
- [x] Revise `c090304` to the 1972 preface's actual Yosemite piton-hole claim;
      add source-backed 1960s production, chock-history, 1970 letter,
      site-damage recognition, British-route contrast and 1977 shop details.
- [ ] Lock author bytes, run independent source/visual review and two fresh
      narrator-only blind reads. Resolve any HOLD and redo affected reviews.
- [ ] Run mechanical ID, card streak, source-hash and docs/task hygiene checks;
      prepare a PR with final review receipts and request owner approval.

## How to verify

Compare `Get-FileHash -Algorithm SHA256` of the three author files with the
review receipts; independently inspect every changed ID against S1–S4; extract
only the `旁白` cells for each fresh blind reader; run `npm run check:tasks` and
the scoped video-doc lint if available. Actual body narration must later be
measured from voice WAVs and reach 480 seconds before buying any images.

## Notes

2026-10-24 first author revision: 86 narration rows and paired visual rows,
73 illustrations and 13 cards. Locked author commit `8221e4bc024f2602de927ef881f99876d202e822`;
script SHA-256 `8A35934A9747211EE05115350E3DF65235FEACB3586B49CC11084936DA84F9AE`,
visual SHA-256 `CBA55E719D41C3E7A301CB0B1508E18ED6F5380D58F299F7B04F82EF3885159E`.
Independent source/visual review found 80 PASS and six HOLD: five two-year
cards plus the c090604 rope-loop detail. Two independent narration-only
readers both held chronology, fact detours, hook pace and closing repetition.
All three locked reviews and the old projection are preserved under `reviews/`.

2026-10-24 second author revision: 76 narration rows and 76 paired visual
rows, 64 illustrations and 12 cards, longest card streak 2. Script SHA-256
`D187ED3C48FF6C28D5080F35CA9F7C4566108322BABA68B755F2CF90D2F9C5B7`,
visual SHA-256 `394B9968AC3E55DC33A67C524E04E0604FBD07F473E8A442D740532BE6B13960`,
evidence SHA-256 `734F4DE54A23D64888E986EA2C0DF23618FC80E42CA1BD830806D34FB7D99B0C`.
Fresh narration-only projection `reviews/narrator-only-d187ed3c4.txt` SHA-256
`893A76C399F156D32514E7D7A5A4899979372E9539186A4FB9C19EC7653A29C9`
received two independent blind reads without shared hard HOLD; both gave a
soft request to reconnect Patagonia's clothing label before the ending.
Independent source/visual review found 67 PASS and nine HOLD: five instances
that treated the report's 1977 publication date as a visit date, two cards
that treated it as recollection date, one coastal/climbing-area conflation,
and one company/personal forging ambiguity. Locked receipts are in `reviews/`.
About 2,053 spoken Han yielded paper estimates
6:51–7:36 at 300–270 Han/min, so actual 8:00 body duration is a clear risk.
Do not pad with repeated facts; measure voice only after owner script and
cost gates. These are not voice evidence. No paid calls. The approved
treatment and source matrix are unchanged; S4's 1977 business profit quote
was deliberately excluded because it would expand this story's approved
factual scope and confuse the 1972 motive.

2026-10-24 third author revision: narrow corrections to all nine HOLD IDs;
1977 now labels only the report publication, coastal travel and climbing-area
sales remain distinct, and continued piton manufacture belongs to the
company. One S4/S7-supported c090609 line reconnects Patagonia's later
clothing label with the reported shop without claiming the seen jackets had
that label. Current 77 narration rows and 77 paired visual rows; 65
illustrations, 12 cards, longest card streak 2. Script SHA-256
`F55BFB219F3EDE82EB8F6281DD7719B1FB1B178EE1F2CB036C6277D15F27EC64`,
visual SHA-256 `0F0F4835003ED1EAFE2A9780200FEDC4EEA4FB6CA40697D5FB03F4254AE4108D`,
evidence SHA-256 `D18F9E8EE78906F5D875E7B2BA9776E4849804D06FCBDB78AB2B7FB503BD5A86`.
New LF narrator-only projection `reviews/narrator-only-2d8bcb231.txt` SHA-256
`2D8BCB231475BC94AC1FEB3D873E91E309FDCA3BDE79DC440608E2E9D3D82E4A`
needs two new blind reads and a new independent final-hash source/visual
review. About 2,109 spoken Han yields 7:02–7:49 at 300–270 Han/min:
actual body duration ≥480 seconds remains HOLD. No paid calls.

2026-10-24 fourth author revision: the independent review of locked commit
`7386e78f927a1ad4343ace66eadde6f625ee6fcb` found 76 PASS and one HOLD
at `c090302`: S1 gives 100 pitons/day, while narration said "over 100".
Its earlier nine HOLDs were resolved. Exact projection SHA-256
`2D8BCB231475BC94AC1FEB3D873E91E309FDCA3BDE79DC440608E2E9D3D82E4A`
was read by blind reader B, whose 12-question story verdict had no hard HOLD;
blind reader A's exact `git show` read was rejected by automatic approval
review as `blocked by policy`, so A produced no verdict. Locked receipts are
under `reviews/`; neither result transfers to this new version. The author
narrowed `c090302` to "about 100" and paired its visual note. Current script
SHA-256 `C4FBE7CF1118B93F9D1A1398CF6E4C75EB3077699EECCFBA152BB357DBF145C1`,
visual SHA-256 `6E724C5CEC19182F80553486225F417780E51342D98B6DCC18F4892DF614659F`,
evidence SHA-256 `15B39299520FC153A1A84ADFC4B0011D454F626AF35B014F3DB493198D611B62`.
New LF narrator-only projection `reviews/narrator-only-c4fbe7cf1.txt` SHA-256
`09A689C4274657898AE542F16EB3A783CB2EAB282BF5C73A936A69B533E4C531`
is a new review input, not a PASS. It has 77 rows and about 2,110 spoken Han;
paper duration is 7:02–7:49 at 300–270 Han/min, below the real 480-second
body gate. The approved treatment/source matrix still use shorthand "1977
still sold"; the script confines 1977 to the report publication year, and
this task does not silently change approved treatment bytes. No paid calls.
