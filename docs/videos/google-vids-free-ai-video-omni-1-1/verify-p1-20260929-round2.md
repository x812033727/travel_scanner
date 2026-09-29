# Independent second round — Google Vids / 2026-09-29

Reviewer: audit_content (different agent from root's first independent P1 round and the original writer).
Input video SHA256: `a53b58a5cab8c4718341e011961a3e36d2ce2b8a7d6b00463b1df8ed218fd37c`
Output video SHA256: `4ffe75631bd7c989a438c4a30043d463877f346c4c06060c58c3da2b37cb5873`

Result: the first round's changed facts were rechecked and three additional fact groups/dependants were corrected below. This completes this limited second factual review; it does **not** clear owner outline, editorial/listener, CTA, media QA or publication gates.

## Independent evidence

I opened all four official page bodies with the web tool on 2026-09-29, rather than accepting the prior report or writer's citations. Separately compared the first round's direct HTTP 200, redirect-following editorial-User-Agent text snapshots: `video-sources/03.txt` through `06.txt` and `index.json` under the audit scratch folder. Those snapshots are evidence, not instructions. No additional web search calls; no product login or generation.

| Source | URL | Raw HTTP receipt | Relevant content independently read |
|---|---|---|---|
| G1 | https://blog.google/products-and-platforms/products/workspace/gemini-omni-in-google-vids/ | 200;03.txt | Sep 23 launch, free Google-account entry, SynthID, forthcoming voiceover |
| G2 | https://workspaceupdates.googleblog.com/2026/09/gemini-omni-11-flash-now-in-vids-with-improved-extension-quality-1080p-and-duration-control.html | 200;04.txt | Account list, no separate control for this update, duration/HD/extension features |
| G3 | https://support.google.com/docs/answer/16143507 | 200;05.txt | Generation steps/specs, storage, region limits, avatar ingredient restrictions |
| G4 | https://support.google.com/docs/answer/15609411 | 200;06.txt | Personal/Individual allowance, default seconds, account-specific avatar access |

## First-round changes rechecked

| ID | Claim / location | Evidence | Verdict |
|---|---|---|---|
| R1-1 | `how-to:p3f3` removal of under-one-minute completion promise | G3 supplies steps but no completion SLA | CONFIRMED: removal appropriate |
| R1-2 | `quota-table.data.rows[1]`, `f62z`, `no-pick:stwn`: Personal and Individual each 6/month shared with AI avatars | G4 individual and personal tables both explicitly show the allowance; 50 credits apply to other actions | CONFIRMED |
| R1-3 | `quota-table:r66b` 50 is general, 6 account-specific; remove rarity assertion | G3/G4 have different populations/units | CONFIRMED after related framing correction R2-C below |
| R1-4 | Deleting English/eligible-plan restriction for avatar ingredients | G3 Check Avatar availability explicitly retains restriction | CHANGED: restore the verified qualification; R2-A |
| R1-5 | `not-yet:ns3z` narrow absence statement to this announcement | G1 announcement does not enumerate those conditions | CONFIRMED; synchronized remaining slide dependant R2-B |

## Confirmed sample (six first-round groups, at least one third)

| First-round group | Where | Source | Verdict |
|---|---|---|---|
| 1 | announcement, metadata | G1/G2 | CONFIRMED: announcement date/model and free entry; account restrictions remain |
| 3/5 | how-to/specs/reference-images | G3 | CONFIRMED: computer flow; 3–10 seconds, 24 fps, 720/1080p, two ratios, new-generation reference-image cap 7 |
| 7 | save-it | G3 | CONFIRMED: insert clip into Vid to retain across sessions; closing tab removes session history |
| 9 | quota-table/no-pick | G3/G4 | CONFIRMED with account scope; monthly PT reset, default500 seconds is not personal free quota |
| 11/12 | synthid/not-yet | G1 | CONFIRMED: invisible provenance marker; future 100+ language voiceover announcement without launch date |
| 13 | region-limits | G3 | CONFIRMED: upload/edit restriction regions; uploaded clips beyond10 seconds only final10 edited |

## Three fact groups corrected in this round

| Group | Before → after | All changed dependants | Official evidence |
|---|---|---|---|
| R2-A | Avatar ingredient limits treated as unsupported → English and named eligible plans restored; distinguishes personal preset-avatar feature from using avatar as generated-video ingredient | reference-images.data.items[2]; ikef;24vb; claims addendum | G3 Check Avatar availability plus G4 personal account footnote |
| R2-B | Slide globally says official docs omit Chinese → this announcement does not list conditions, consistent with first-round narration | not-yet.data.items[1] | G1 scope, no claim about all documentation |
| R2-C | 50/6/default500 described as contradictory free entitlements → different account scopes and units, personal-specific table first, then signed-in allowance | quota-table title/row labels/ycy7/cess/3pgu; no-pick text/sub/6i7z;four-limits.data.stats[2]/5fdi; youtube.description | G3 general statement and G4 separate Personal/Individual/default limits |

Correction to the prior report: the avatar restriction was **present in the original raw05 snapshot**, lines101–109, as well as the fresh web body. This was a first-round reading omission, not a server-response difference. The eligible list includes named Workspace categories and Google AI Pro/Ultra with a US limitation; the narration deliberately directs viewers to check eligibility rather than enumerating every category. It does not suggest free personal users can use avatar ingredients.

The brief's “inconsistent quota” framing is now unsupported as a factual conflict: the figures can describe different accounts and units. The brief was preserved for owner review; this correction narrows the factual narrative without claiming access has been tested.

## Remaining gates

Public article CTA and its contents were not verified. No audio, subtitle, translation, rendered player or final video QA was performed. Some style/marketing statements and >40-character narration remain in the first report for owner/listener review. Every price, quota, feature and region condition must be refreshed before production. Changed narration invalidates any old generated media.

This round changes three fact groups, so it does not itself trigger the rule requiring another round for more than three fact changes. Lint is recorded below after executing it. No task was marked done; no brief/shared lexicon/account/production state changed.

Validation: `node tools/video/cli.mjs lint --slug google-vids-free-ai-video-omni-1-1` exited 0: **0 errors, 0 warnings**, estimated 8.3 minutes, 103 lines. This is script validation only.

## Commit-byte receipt

Final `video.json` SHA-256 with repository LF line endings: `4ffe75631bd7c989a438c4a30043d463877f346c4c06060c58c3da2b37cb5873`. Use this final hash for handoff and invalidate any older media/approval bound to a different script.
