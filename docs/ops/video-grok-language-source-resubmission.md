# Grok language source resubmission preparation

Project: `grok-4-7-bedrock-output-doubles`.

The owner approved language review `178a957d-19f9-451d-b1cc-fe516f4d2b2e` at
2026-10-04 16:03:04.832208Z. Its legacy manifest SHA-256 is
`6837b14635018e7b9a0a0a3fdd6124ff2648f668b4628f6bb109e53ccfb275f7`.
At 17:01:46Z the actual deployed `read_approved_package(verify_files=True)`
refused this approved batch with `409 video_youtube_languages_invalid` and
"old language review lacks a verifiable source manifest and metadata; resubmit".
This is an attachment/provenance defect, not evidence of an active producer.

All ten existing ReviewStore attachments and their canonical copies have been
read and verified against their approved bytes, sizes and SHA-256: four
descriptions, four captions, English dub and Korean dub. Native branded metadata
was independently recomputed; all ten metadata fields and all four description
and caption copies match. English and Korean each retain 92 current clips with
92 passing technical QA records, exact speech/translation bindings and no flags.
This evidence does not replace owner listening or Studio upload confirmation.

Japanese remains explicitly skipped:
`2 lines (t3ut, uaxy) do not fit even at 1.15x after 2 shortening rounds`.
There is no completed Japanese track or Japanese QA result to attach. Do not
regenerate speech, widen the tempo limit or turn this skip into a ready result.

An operational successor must bind these existing sources:

- Final review `962a3ac8-7f7e-42aa-bb1d-e6f1a63c440f`, SHA-256
  `dcbadae47567967705196df9559eb1b4768a8aff9f48c7a96bc93848686a76e5`.
- Publish review `cbe78b61-2306-4760-8733-b951a54c0d14`, SHA-256
  `4faedfa12559bbf4aa19b1be342d66454eb0570aeba8869c2f797d0cef1ba664`.
- Current multilingual metadata SHA-256
  `e0915b483fa33c90b6e277ff10bd8448ba83e570a2f50365f12c9001e9cced7d`,
  12,178 bytes; the approved publish metadata remains 3,607 bytes.
- Branding `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`
  and speech string `0501230483dd96ae`, including its leading zero.
- Original four-locale choice at 2026-10-04 14:13:45.684867Z. Script and
  compilation identities remain null in the source contract. The actual final
  review payload has no speech or compilation key; fixtures must preserve that
  key absence instead of inventing explicit null values.

Schema 1 `languages_manifest` must include source, original choice, exact
ready/skipped locale states and eleven descriptors (the original ten plus
metadata). The proposed review additionally contains the manifest, for twelve
attachments. The old approval, ten files, canonical legacy manifest and metadata
must remain intact. No project PUT is necessary.

Read-only evidence through 17:05:39Z is frozen locally under `<temp>`:

- `mokaair-grok-language-sourceproof-readonly-20261004-1655-compact-v2.json`,
  SHA-256 `20ffcac3b358e83093f9a8eab9bb25088e4f0940ae5ff1d5a917d824ca744006`.
- Full source evidence SHA-256
  `62561d66fdd684070fe0061ff05cd9188b8b776f688c4b803ac9783c87934f9e`.
- Native metadata and technical QA evidence SHA-256
  `4d738787463d83ed0afe7cb5cc32e3c45ca1e29ad5b4b1d3cc0effc0cc7e8859`.

The current owner is active and has effective owner role. Sources, original
choices, request/ack nonce, protected settings and uploader-disabled setting were
stable. Jobs and locks were empty at the snapshot. This does not establish an
atomic producer lease. The canonical `upload/report.json` is absent; guard its
absence rather than calling it a verified existing file. Any later live action
requires a fresh read-only preflight and a frozen packet/driver.

The complete offline candidate is frozen under
`<temp>/mokaair-grok-resubmit-20261004`. Exact identities:

- `packet/languages-manifest.json`, 3,983 bytes, SHA-256
  `00e8260712b3eac0f7b65f45162665049e5b158373144ea40f93fd6fe2668afb`.
- `packet/review-request.json`, 3,489 bytes, SHA-256
  `db802a72ca8d8ce6c696d26e9e699aaf64a5d4818033d3fa226cf144a9ce35e0`.
- `builder.mjs`, SHA-256
  `84d0bbec46b5b1080803ca37a64264d80e7330ecbbeefb29cb7d24021f309cb1`.
- `submit-once.mjs`, SHA-256
  `b83eb1f0df6c1258552185af97bca9735fc792e1d7f7942b889be9bc4422baaf`.
- `freeze.json`, SHA-256
  `66b2962c44d7fe1a29509d346301ad1beaca3925a672fddb54d81d17517e958c`.
  Root verified all eighteen source/candidate bindings after independent tests.

Thirteen submission/flow and eleven backend cases passed, including independent
root runs. A separate reviewer passed seventeen packet cases and twenty-four
cases using the real request adapter and exact wire shape. The latter includes
normal `Automation.languages` with the complete twelve-file pending row: no
commands, models or network calls, and the old canonical manifest remains exact.
Connection or accepted-response body loss leaves durable intent and prevents
every later POST. Source, choice, retry, decision time, old payload and file drift
all refuse. These tests use counting mocks and no real network or paid calls.

Independent packet evidence SHA-256:
`7ed17cf68210555127b8034a342857eca523d7f9247595605e3360460e1caf30`.
Independent adapter/flow evidence SHA-256:
`09168bc8f29c09741f78f35cd87d8a763cbac08abfc57fcde47a29e695a9d8f9`.

At 17:15:11-17:15:16Z the deployed consumer also passed a read-only,
`verify_files=True` cross-contract check. It read all ten original files from the
real ReviewStore and the two proposed JSON files from memory only. A pending
transient candidate correctly refused approval; a separate hypothetical approved
transient copy composed successfully. No ORM copy belonged to the real session;
dirty/new/deleted counts were zero and the real review stayed approved. Neither
new JSON was stored before or after the check. This proves candidate compatibility,
without creating an actual review, approval or stored replacement.

Cross-contract evidence SHA-256:
`ed7cb5b8291eaf6512485b6c053ce6e5f90b6899f8e1ec064d49f44f22da3447`.
The fixed receipt directory was genuinely absent at both ends of this snapshot:
`/var/lib/mokaair/video-work/grok-4-7-bedrock-output-doubles/review/ops/grok-language-schema1-20261004`.
Any future intent in that namespace permanently prohibits another POST, including
after an unknown response. Do not switch directories to bypass the receipt.

Preparation is complete; a specific owner decision is still required. No Grok
file PUT, review POST, owner approval, paid generation, deployment, worker restart
or YouTube action has occurred. If authorized, use the frozen driver for two small
JSON PUTs and one review POST after fresh owner/source/settings/store checks.
Verify the actual new pending review and all twelve stored files afterwards.

The completed Cloudflare-only resubmission request does not authorize making a
new Grok pending batch the current language version. Obtain a specific owner
decision after the complete packet and transport are independently validated.
The broader normal-producer fix already belongs to
`2026-09-30-youtube-approved-languages-sync`; its overlapping scopes remain held.
This document and preparation do not modify that producer or its task claims.
