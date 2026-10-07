# Selected language production, 2026-10-07

This record extends the completed Traditional Chinese cut and its basic upload
package. Earlier receipts remain historical snapshots. The owner's saved
language choice at `2026-10-07T13:30:52.197866Z` requests metadata, captions and
dubs for en/ja/ko, and metadata/captions for zh-CN. A fresh authenticated GET at
`2026-10-07T14:50:01.562Z` returned the same choice and response SHA
`845998287d6c4c9a7b1726cff93aa24f9a8261ae05198d5d8376bee760dce32d`.
The YouTube video ID remains null.

The source JSON remains
`6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235`,
and the Chinese cut remains
`6e07ad6f915e35b49df565fceabe42ebee3f78821668f698b6bfc74cbeb7b9d9`.
These dubs use the existing picture and each locale's own measured speech
timeline. This record does not attest to owner listening or Studio upload.

## Source and translation review

All 142 ordered source/target pairs per language were independently reviewed.
The glossary, full station/museum names, specific historical query and travel
dates, holiday exception, distinction between found facts and draft inference,
unmeasured walking/weather, account permissions and payment/dispatch stops
were checked. Worksheets were merged with the normal native `i18n-merge`;
source hashes were written by that tool. Only target line text changed;
metadata, source fields, IDs, order and other worksheet fields have full-object
inverse proofs. No provider request was made for translation or preflight.

The independent Japanese review required six semantic/wording repairs, and the
Korean review required ten. These were incorporated and independently checked
before buying their speech. Korean V4 additionally shortens only three lines
in the remaining estimated over-length windows; complete museum names and both
unmeasured/unverified qualifications were retained. Single-line character
guides are estimates: adjacent lines in one reveal window can share time.

| Locale | Frozen reviewed worksheet | Independent final text review | Native merged translation |
| --- | --- | --- | --- |
| en, before actual fit shortening | `e4396005b3508c8796a4191a977c519edf1c6c8924c6a09225255afc88e1d2fc` | `d3d3bef234e90f3f54cd0f44477022ec0ce6c4ded7cc9d0effe84049ec5168d3` | `b476e7313e83dfa9229f3d92cc8ce4cd8d8362e23d93893db05ae611138e5fad` |
| ja V3 | `ee2a0e26cd7b36fb398ae18434dd06bcf7c862836d64c8d7186ec3a996142e82` | `07cce06399356f72ff51abd032bd62a3269dc2632947f7805fd3a84704fbc2af` | `d16b2df44b30df4a352ae8be86b1dbda60691902f67f6fc00ea0b44369cdf05e` |
| ko V4 | `2624fae6e489302a67d5873ddd1a98fa5dab6f01bb4cdc3812313de932495984` | `770682ab4f4cc9b46f4648fd8cbc5a489487db3f8a13ea4559110f0dae3a9644` | `aa63f2f14a50f95459a42d5ad750d7e2170234c6b0a5975b693cc2595fa7454b` |

Native pure window estimates fell from 31 to zero for the initial reviewed
English worksheet, four to zero for Japanese, and 57 to zero for Korean.
Fresh native dry runs confirmed zero estimated unfit windows and an available
Gemini quota. These estimates were not audio-fit approval. Frozen worksheets,
full pair-by-pair reviews, inverse proofs and actual native merge receipts are
under `<operation>/dub-preflight/` outside Git.

## Actual English fit and first QA

The first full English dub closed at `2026-10-07T14:05:41.348402Z`, exit 1:
142 raw clips existed, but two measured reveal windows did not fit at 1.15x.
The immutable first-fit receipt SHA is
`a5cb976da84a754d705259fade05a2654d91f51d0672eaeee577f8297fb30864`.
Actual reported billable characters were 8,948, including normal failed-split
fallbacks. No unfinished or shared clip was deleted.

Actual shortening round one changed only ag111/ag112/ag020/ag021. The four
source/old/new pairs were separately read and preserve new museum notices,
lack of a web tool, separately checking opening dates, defining completion
first, and places/order/official opening proof. Candidate SHA
`4d16c0d8de89225cd2a31d78c381e63ed13b19b630b08f950caa6a0d8e6994c8`;
author meaning review SHA
`f84a82334e181f083a84492a70da5160153f821bac7b1b9d78562317cdd01d86`.
The actual normal native merge produced English file SHA
`82a0b0bdfe00b0e23a19cc5a8bb1b5d2538b972da5bb6746bb6a30a1e60a7323`.

The subsequent dub exited zero, buying only those four changed lines: 167
reported billable characters, with 34 request groups reused. Independent actual
media audit SHA
`80ba0a59b86c20c7c9e6b25658b3ed9c25039955c7458d739bd86cc35789123f`
verified exactly four changed raw WAVs and 138 byte-identical originals, all
142 current cache keys/source hashes and speech fingerprint, 84 measured
windows fitting, maximum tempo 1.09x, and sample-exact reconstruction of the
assembled PCM. Logical duration is 629.833333 seconds; encoded AAC duration is
629.900000 seconds. AAC LC is 48 kHz stereo; 384k is the encoder target and
266,692 bps the measured stream rate. Encoded padding was measured separately.

English native QA completed 142/142 at `2026-10-07T14:47:56.042761Z`, exit 1:
129 exact, three judged acceptable, ten requiring further verification.
The resumed run transcribed 95 new clips and reused one previously paid answer
from the speech journal; the earlier 46 cached transcripts were also reused.
This first completed QA does not approve the English dub. A local independent
transcriber is checking those ten raw clips without the script or hints.

## Confirmed-answer recovery

English ag027 ASR received actual HTTP 200, then Windows failed replacing the
native sent journal with its intact confirmed temporary record. The producer
had closed before recovery. The current raw clip, native 16 kHz request,
unique captured response, native answer hash and original sent/temporary bytes
were independently bound and preserved before restoring the exact confirmed
record at `2026-10-07T14:38:21Z`, with zero network calls.
Request SHA
`0a725f16e704643b4d7cf535e0e549bd0c2872d7b1a66810049b97e9940c3d98`;
response/answer SHA
`a564266e8785d5aec293d109f997b953533d21394c293c95f247e8dc45255117`.

The first Japanese synthesis similarly closed at
`2026-10-07T14:53:07.590760Z`, exit 1, after receiving task-spec's four-line
answer. That exact confirmed 48 kHz WAV, its current native Japanese request,
captured HTTP 200 and closed producer were bound before local promotion at
`2026-10-07T14:58:30Z`, with zero network calls. Request SHA
`1b2cc8136b746d1f3387515e8e3a7095ab060f45de3f42127fb1b7c0db2ee262`;
confirmed WAV SHA
`95ca824c53539d694d5c195bc10469bbee0c47a36b2f38c6837fabeffe91033c`.
Its already-paid 143 characters are not charged again by journal reuse.
The resumed synthesis is still in progress at this checkpoint.

These are guarded operator recoveries, not a native tool repair. Originals and
receipts remain under `<operation>/recovery/`; the implementation gap is tracked
by task `2026-10-07-recover-confirmed-speech-answers-when-windows`. Uncertain
requests, unrelated STOP markers and held videos were not cleared or retried.

## Checkpoint, not language delivery

At this checkpoint English has a fitted track but pending audio QA; Japanese
is being synthesized; Korean has reviewed/current native text and no bought
audio yet. The approved basic package and its 718 caption cues remain an earlier
snapshot. Current selected-language captions must be rebuilt from each actual
dub timeline and packaged before the language batch is delivered. A language
card with dubs still requires the owner's real Studio-upload acknowledgement;
no such acknowledgement or YouTube publication is claimed here.

## Measured repairs and independent speech, 15:46 UTC checkpoint

The independent English second transcript actually ran the already cached
`faster-whisper-small` model on the ten frozen current raw WAVs, with CPU int8,
two threads, English language, beam five, no initial prompt, no script/terms
or native hints, and local files only. The model binary is 483,546,902 bytes,
SHA `3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671`.
The actual worker self-completion and retained OS launcher handle both report
exit zero; their distinct PIDs are recorded separately, without inventing a
parent chain. The immutable actual-transcript receipt SHA is
`4552b8eeb80dd8d3b315de671aa4db2386f0ecd125aaa4d7acfb2c2115c263ea`.

A guarded callback returned only those real frozen transcripts after checking
current WAV/source/target/QA/model pins. Normal native `check-audio` closed at
`2026-10-07T15:24:23.435835Z`, exit 1, with 142 checked, five flags genuinely
cleared by the second transcript and five remaining flags. Zero primary ASR
clips were bought again; one normal Jev call checked the differing independent
transcript. No expected words, scores or manual acceptance were substituted.

Ordinary English retake one changed only ag016/ag020/ag038/ag080/ag120;
137 raw WAVs remained byte-identical. Its actual 251 billable characters are
added to the prior 9,115, rather than treating its invocation as the whole cost.
Retake two changed only ag038/ag120, with 140 WAVs byte-identical and 99 actual
additional billable characters. Both tracks fit all 84 measured windows,
maximum 1.09x. Free independent audits verified native keys, each full raw WAV,
every sample of reconstructed PCM, actual AAC and actual caption candidates.

| Frozen private audit | Full audit SHA | Actual owned synthesis responses | Verified billable characters | Native QA at that snapshot |
| --- | --- | --- | --- | --- |
| `en-retake-r1-media` | `390008daf7c3eb62ab76ad3b1be467de46aca259c186f8bfdca82bb952865013` | 65 | 9,366 | 142 checked, ag120/ag038 flagged |
| `en-retake-r2-media` | `6896cae0f2bce0e8e83a1b6a4343a1a6c56798298908619f7245dc51b6b6e5d2` | 67 | 9,465 | 142 checked, ag038 flagged |

The actual second-retake audio QA at `15:37:55Z` still hears `We drop it` for
`We'd drop it`. After the two ordinary retakes, listener reword round one changes
only ag038 to `We planned to drop the museum. It can stay.` (43/43 worksheet
characters). The prior planned removal and present permission to retain the
museum remain explicit. Its independently reviewed candidate SHA is
`22f1bbde6530df15ec106c1fb3d325ee0a3fac2202fbb4ada689e2d52a86cca0`,
peer receipt SHA
`52987d1e56f2884668a196986e27b171a4212699995cb1bf20d0eb41d591d31c`.
Normal native merge at `15:45:58Z` produces translation SHA
`1a7990dadd21eb12a349a3963bbf5782882f3b000380ad99ffdfd844418e1f28`;
the other 141 entire entries, metadata and source hashes are preserved by
whole-object inverse proofs. At this checkpoint its new audio is pending;
the old raw WAV and original flag remain preserved and are not passed as QA.

Japanese's first complete synthesis had seven actual over-length windows /
13 affected lines. The first-fit receipt SHA is
`d8e3f6c347ba20022bdf8c32bfb0f1c3f1db21d0b95c16e75b5217c16b9f32b7`.
Actual shortening round one changes exactly those 13, retaining the complete
station/museum name, near/first route relation, opening evidence, address page,
institutional walking guidance and our unmeasured/unverified qualifications.
The independent peer corrected ag097's unnatural collocation before adoption;
candidate V2 SHA
`82ee3fda3e156b713141c298bb15db9d527cc187250423413b38fe76d4c65180`,
peer SHA `a4c06d2c14064b7b90f87dfc167fbc88ed604415b9a4de3b97ec0b2ea2efd117`.
This is one actual shortening round; the free text-only candidate revision is
not a second paid audio attempt. Normal merge at `15:31:39Z` writes Japanese
translation SHA
`63857b37de609fe1e39d54ed1c5ea18a34e20e0f8ab87b21a9769e029f57a1e5`.

The Japanese producer actually closed at `2026-10-07T15:35:14.070Z`, exit zero:
six native groups / 13 changed lines, 30 groups reused, 274 reported billable
characters. All 84 measured windows fit, nine sped up, maximum 1.12x. Its free
independent audit verified the 13 changed / 129 identical raw WAV cohort and
complete PCM/AAC/caption binding. Audit SHA
`48413e0a36301cc15fff3de28eddf9ee6442dbc2397ccb7e737f0b939aa400f6`,
receipt SHA
`d4837c9c4d452b425fe829f982b58f8d5c579f7ac6b2b0995005d5cc9d4e46fa`.
Its 62 actual owned HTTP 200 captures total 5,360 billable characters:
1,156 before the confirmed-answer replacement failure, 3,930 after recovery,
and 274 for shortening. The already-paid 143-character recovered answer is
counted once. Every request body, response header, PID and producer interval
is bound; no unknown response or missing header is counted as zero.

Japanese's full native audio QA is running at this checkpoint; media-fit
integrity is separate from pronunciation QA. Korean still has reviewed native
text but no bought speech. The original base package was copied before any
selected-caption/package rebuild; immutable preservation receipt SHA
`b65a928da1a6b241447ad338290f2bb00850f623c3ed384b688096ed2b502773`.
No Studio upload, owner listening acceptance, language approval or publication
is inferred from these production receipts.

## Updated dub checkpoint, 2026-10-07 16:31 UTC

This checkpoint updates the earlier pending snapshots. It records saved
native results and scoped read-only reconciliation. It asserts no final
language package, submitted language card, owner listening/player acceptance,
Studio acknowledgement or publication. The source remains
`6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235`.

### English: final native audio check passed

The second and last listener wording revision changes only ag038 to
`The museum was to be left out. It can stay.` (43 worksheet characters).
It preserves the former plan to remove the museum and the present possibility
of keeping it in the draft, without asserting an actual removal or visit.
Normal native merge produced the current English JSON full SHA
`8e4c9a00e68591b06a8f1edf20d9813ba164e86993786dc1dbd5afba90843a3f`.
Candidate SHA `7b1a51d5f3f3a9fcbce8e16958e01592e3cb2b3d250011dc481001c74a88ec7a`;
independent text-review SHA
`464069fa51525f429ec03ead21a426740f82be539feef0274cb50fb67d75a5c0`;
actual normal-merge proof SHA
`7284b9f25e870a91b2a6b30feb8f973d91a392f6810cac721fd0af3047f6eebd`.

The saved `20261007T162056Z-dub-en` invocation closed at
`2026-10-07T16:22:42.438533Z`, exit 0: one request / one changed line,
43 reported billable characters, 35 reused native groups. Its current fit
report has no over-length windows, all 84 windows represented and maximum
tempo 1.09x. The 43 characters describe this invocation; they are not a
cumulative cost reconciliation or a zero-cost assertion.

The actual `20261007T162256Z-check-audio-en` run closed at
`2026-10-07T16:23:03.814460Z`, exit 0: 142/142 checked, 133 exact,
four accepted by Jev, five cleared by the real independent second transcript,
zero remaining flags. This run transcribed one changed clip and made no new
Jev call. Older primary-heard text and genuine second-transcript records
remain intact; no expected transcript, score or manual flag clearance was
substituted. Native QA pass is separate from owner listening acceptance.

| Current English artifact / saved receipt | Full SHA-256 |
| --- | --- |
| `dubs/en.m4a` | `377ef358cadb178f9fa548a291da8015f0bc99c6966cfb2ae4cca544bc04ecdf` |
| `dubs/en/timeline.json` | `84863f76c16f11b1aeceaa6b32545e592b7b3708ab849e5bdaf1e9ca29fd627e` |
| `dubs/en/fit.json` | `759dc0b386dbc8694c22a1c2481c2a7538ab076c2432221cfff051ecee0aaf90` |
| `review/check.en.json` | `99b152839e2e097c4eb1e7b9a262973167f80e2163481382d61a17cc1136925e` |
| `review/check-flags.en.json` | `1e455a2753ce09b512c14a206ac4bb4e8bcdc0675c0f3e37d2a076fa237364b3` |
| `logs/20261007T162056Z-dub-en.exit.json` | `63b0ac165b6814de166e333b8bce4bb3fddc01063193e91d5587260ea8640252` |
| `logs/20261007T162256Z-check-audio-en.exit.json` | `d5145eb0b5d9a28af2a60b50f07c01736cab80ad93ea0e6909ed3a0fe6cf49e6` |

Artifact paths above are relative to the episode work directory; logs/private
receipts are relative to `<operation>`. This excerpt records native
fit/check results and hashes. The later full media audit must separately bind
the final raw cohort, reconstructed PCM, encoded track and selected captions.

### Japanese: real second transcripts, first retake dispatched

The cached local model actually produced 34 blind Japanese transcripts; no
source, terms or native hints were passed to the model. The frozen receipt at
`<operation>/offline-audio-evidence/ja-priority34-v2/receipt.json` has SHA
`015f411b4268c077a14b0abdd5f3aaa1195615cb24b2323875d55add03d5feb2`.
Normal native `20261007T160650Z-check-audio-ja` closed at
`2026-10-07T16:06:57.175256Z`, exit 1: 142 checked, 97 exact,
11 accepted by Jev, 11 cleared by the independent second transcript and
23 still flagged. It transcribed no primary clips and made one normal Jev
call. Exit receipt SHA:
`16bcb0cf79c954b51305fa25c55642576e0dc01a8efc007b5d83b51f0686d0c6`;
saved stdout SHA:
`1370748a598aed5d6298d5fcce9c84e05324efaa0c34d2b697053002ea4e29ad`.

These are saved pre-retake results. The first ordinary Japanese retake was dispatched at 16:30:31 UTC under
immutable authority SHA
`73a18d92545b24abbf7842dc18b31ed72f51de9dd46edf6eede757353b483c34`.
The 23 old flagged clips and all 142 full raw hashes were saved beforehand.
This checkpoint does not infer
that changed Japanese WAVs, new fit or final QA have passed. Japanese text
at this checkpoint remains
`63857b37de609fe1e39d54ed1c5ea18a34e20e0f8ab87b21a9769e029f57a1e5`.
New audio requires its own actual evidence and final binding.

### Korean: 51 retained clips, one held attempt unresolved

Native `20261007T155622Z-dub-ko` closed at
`2026-10-07T15:58:40.629591Z`, exit 3. Fifty-one current raw clips are
preserved. The unresolved 352-byte request uniquely matches the current
single-line native body `tool-trace#0 / ag121`:
`단계별 결과는 한 표에서 확인합니다.`.
Full request SHA:
`d6c8b6b435708c7e72b6abe9d7a07ddb3825a33428033c4ed54efe24f636781b`;
current Korean translation SHA:
`aa63f2f14a50f95459a42d5ad750d7e2170234c6b0a5975b693cc2595fa7454b`.

The actual saved response was HTTP 502, 110 bytes, code
`upstream_unavailable`, detail `API 服務目前無法回應`.
Full response SHA:
`cf504ec26cddb7bd293c51de483a95fe7163c5ce853d7700505be3ccca30376b`.
The schema-1 `speech` journal remains `held`, full SHA
`6e85882c2aaa20b00d5617c04514a8d7e66161c5c87e4f65b9e7a755ca159693`.
No usable answer/WAV or confirmed temporary record exists for this key;
ag121 raw is absent. A complete Korean track is not claimed.

Fresh read-only inspection verifies the present compiled paid speech route's
distinction between 502 for failure to connect and 504 for a lost response and exact response
body. A bounded historical search found the previous successful 7524
build and activation, route inventory and source/build continuity. However,
current API/web containers were created after this attempt; the old compiled
`speech` POST import/call and this attempt's internal connect-error code
were not recovered. The earlier compiled graph was for
`speech/transcribe`. The evidence supports the never-connected
interpretation but does not conclusively clear historical execution or charge.
The attempt remains unknown; no zero-cost, forget or retry clearance follows.

| Read-only receipt under `<operation>/recovery/d6c8b6b435708c7e72b6abe9d7a07ddb3825a33428033c4ed54efe24f636781b/` | Full SHA-256 |
| --- | --- |
| `host-contract-independent-audit.json` | `d732ebdb50b0062692cedb51edc1100bb835d162055e6e5b00b8ca3397755ae1` |
| `historical-continuity-supplement.json` | `824df297396e84b4751a4fbcf4da7ffb3c576d222e794854e97fd57c8402f6e6` |

The coordinator reports one explicit async owner request about possible
duplicate charge, with no reply at delegation. No owner approval is asserted;
Korean-dependent work remains gated and elapsed time is not consent. The new
private continuation entry beside those immutable receipts is
`ko-held-status-20261007T163154409043Z.json`, SHA `5173fce04dcc72b6f91a04c7757a4ccbb904e8c6714a552293d3837476093107`.
It preserves the hold and 51 preserved clips and requires fresh trusted owner
authority/native guards before the coordinator decides further action. It is
not permission to retry. Citation STOP and unrelated unknown requests remain
outside scope.

This checkpoint grants no language-card approval, owner listening/player
acceptance, complete selected-language package, Studio acknowledgement or
YouTube publication. Add Japanese actual final evidence and the full
selected-dub media/caption audit only after they finish.

### Independent final English media and cost binding

The free auditor actually closed at 16:28:18 UTC, exit zero. Its audit SHA is
`3c6b48bcb76da136961c20ddb8017936073db93af8d533980bb5f32d77b427b0`,
completion receipt SHA
`9b5075bb638867260abc9168fd506719b406071c22960cbabe4fa010c7b279bf`.
All 142 native keys/raw clips and every sample of reconstructed PCM match;
only ag038 differs from the immutable second ordinary retake, and the other
141 raw files are byte-identical. The AAC is measured as 629.9 seconds,
48 kHz / two channels, 266,102 bps actual, with encoder target 384k kept
separate. Logical timing is 629.833333 seconds. All 84 windows fit at maximum
1.09x; 142 fresh caption candidates have no cue issues. Native final QA is
bound to the actual closed 16:22:56 invocation and the current full inputs.

The capture reconciliation binds 69 actual HTTP 200 synthesis responses to
current and separately pinned historical native request plans, full body
hashes, producer PIDs/times and billable headers. Total verified synthesis
characters are 9,551 = 8,948 + 167 + 251 + 99 + 43 + 43; each listener round's
43-character response is counted once. Unbound bodies, uncertain responses
and missing headers are zero for this English cohort. This is a character
receipt, not an invoice or a provider currency estimate.

The five reused independent transcripts were separately traced back to real
completed blind model segments. Each current complete WAV and target/source
entry equals its frozen earlier input. The lineage supplement SHA is
`1599f416a78360605d3df1a4ee4982eb3c1180c9abb5a7a1bb29b41d878f1711`.
It buys no new transcription and changes no native scores. The native caption
and upload package rebuild remains a later step; candidates do not constitute
published captions, subjective listening or owner approval.

### Japanese second ordinary retake: closed media checkpoint, nine QA flags

This is the actual 2026-10-07 17:15 UTC checkpoint. It supplements the earlier
English and Korean records; it does not replace their history or declare the
selected-language package complete. Source remains
`6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235`;
the current Japanese translation remains
`63857b37de609fe1e39d54ed1c5ea18a34e20e0f8ab87b21a9769e029f57a1e5`.

The first ordinary Japanese retake produced 23 actual HTTP 200 synthesis
responses and 523 verified billable characters. Its media audit is
`<operation>/dub-media-audits/ja-retake-r1-media/audit.json`, SHA
`04143d2d500682029b90190aad6b4ec909e21a629f77655d5546f9cf75eac476`.
The separate actual-blind transcript lineage receipt is
`<operation>/review-receipts/ja13-blind-lineage-independent-20261007T170031006143Z.json`,
SHA `83904a576c47b5444577f5634e5866cd35166bd27f1fe08018369f8b8be59e78`.
It binds 13 real completed independent model segments to their frozen input
WAVs and native adoption, including eleven earlier segments and two newly
cleared first-retake segments. It is not human listening or blanket approval
of the second-retake audio.

The original second ordinary retake, native prefix
`20261007T164749Z-dub-ja`, actually closed exit 1 when Windows refused the
confirmed-answer journal rename. Ten requested raw clips had completed; the
ag131 answer and its complete WAV already existed. The guarded local restore
preserved the original sent record, confirmed temporary record and WAV, and
promoted that same answer with zero network requests. The separate authority
SHA `80fb7e3890d0081863c3b756a6b040acb09ede83515a549170b50b34ff94fcbc`
then dispatched only the five unfinished targets. Native continuation
`20261007T170835Z-dub-ja` closed at `2026-10-07T17:10:53.659387Z`, exit 0:
four new synthesized requests, 95 billable characters and one prior journal
answer reused. This completes the same second ordinary round; no third
ordinary retake was dispatched.

The free V2 media auditor actually closed at `2026-10-07T17:15:17.973Z`,
exit 0. All 142 current native request/cache/raw/source bindings and the full
reconstructed PCM match. The original second-round targets
`ag001/ag006/ag111/ag026/ag033/ag094/ag125/ag042/ag097/ag101/ag131/ag132/ag063/ag065/ag068`
all have changed complete WAV SHA values relative to the immutable first-round
audit; the other 127 complete WAVs are byte-identical. All 84 windows fit,
with maximum tempo 1.08x. The current AAC is measured as 629.9 seconds,
48 kHz / two channels, 310,738 bps actual; the encoder target 384k and logical
629.833333-second PCM grid remain separate. Its full SHA is
`ba7af4ddf52e33619acbf926c26ad11ec8bb0a70eaf8e73e12c05bdf45964cd6`.
There are 142 fresh cue candidates and zero cue issues; these candidates do
not establish that the selected native captions or upload package have been
rebuilt.

| Immutable private evidence | Full SHA-256 |
| --- | --- |
| `<operation>/dub-media-audits/ja-retake-r2-media/audit.json` | `ae41af42f990bc80799697a7ea647ca5d35808ec1c0ac203b27ae431081794c6` |
| `<operation>/dub-media-audits/ja-retake-r2-media/receipt.json` | `f5130111a8a1a669ca11e97380d9cd224b7a795233702a3b8e7aecc1408e27de` |

Cost evidence retains both real producers: original second-round PID 39000
has eleven captured HTTP 200 responses / 257 characters, including ag131's
already paid answer; continuation PID 3788 has four responses / 95
characters. Reuse adds no new capture. Across the supplied completed Japanese
runs, the collector verifies 100 observed HTTP 200 captures / 6,235
characters, with no unknown billing or unbound request bodies. These are
observed character receipts, not an all-time provider total or invoice.

The actual native `20261007T171101Z-check-audio-ja` closed at
`2026-10-07T17:13:15.175257Z`, exit 1: 142 checked / zero unchecked,
105 exact, 15 accepted primary judgments, 13 native secondary clears and
nine flags. Native state `judged: 37` counts all primary nonmatches and must
not be relabeled as 37 accepted judgments. The current flags are
`ag001/ag006/ag111/ag094/ag125/ag097/ag101/ag132/ag068`; the audit binds
every verdict to the current complete clip, target, spoken form and hints.
It explicitly records `native_qa_pass: false`. Japanese listener wording
review and any bounded listener rounds are still pending. No score,
threshold, flag or source was overridden.

English retains its independently bound native zero-flag result and the
69 actual synthesis captures / 9,551 characters documented above. Korean
retains the exact 51 current partial clips and unresolved ag121 held request;
its selected part is working, not skipped or complete. The free selected
caption/package helper is independently static-reviewed, but its real audit
still requires final Japanese evidence, a fresh owner-selection snapshot and
exact current held Korean identity. No language-card approval, owner
listening/player acceptance, complete selected-language package, YouTube
upload or publication follows from this checkpoint.


## Selected delivery, 2026-10-07 18:36 UTC

This append supersedes the pending selected-language checkpoint above without changing its historical evidence. The Traditional Chinese source, approved 1080p film and 629.833333-second logical timeline remain unchanged. English is current and native QA-zero. Japanese is a documented bounded skip; Korean remains held and working. The selected batch is not complete.

The Japanese second-listener round changed only ag097 to `博物館の歩行案内あり。私たちは測らず、天気も未調査。` (26/26 characters). Independent meaning review SHA `cd4653387027093c9a100127c3185302ae80a98dcb6f9f671051043ec6e0af42` retains museum walking guidance and our separate measurement/weather negatives. Normal native merge produced full JA SHA `b44699979a3aeb27a4eb4336bc89784d6af81c54643f935ce70b0d070cbf68d5`; the other 141 whole entries, metadata and source hashes remain identical. Actual `20261007T180401Z-dub-ja` closed exit 0, one partial request / 26 observed billable characters, 35 groups reused. All 84 windows fit, maximum tempo 1.08x. The independent complete-media audit verifies all 142 current raw/native-key/source bindings, reconstructed PCM identity, only ag097 changed and the other 141 WAVs byte-identical. It binds 109 observed owned HTTP 200 captures / 6,456 synthesis characters across the supplied eight closed Japanese runs; this is not an invoice or all-time total.

Actual new-clip blind transcription used the cached local model once, without source text or hints, and returned `博物館の歩行案内あり、私たちは図らず、天気も未調査`. Normal native adoption `20261007T181024Z-check-audio-ja` closed exit 1: 142 checked, zero unchecked, 111 exact, 15 accepted primary judgments, 15 genuine secondary clears and one remaining flag ag097. Primary/secondary verdicts remain 0.18/0.10. The 15 clear secondary entries have actual model segments, full frozen/current WAV equality and current whole source/target entry lineage. Written 測らず and 図らず have the same reading; the transcript mismatch is not evidence of a proven wrong TTS pronunciation or owner listening acceptance. It remains a native QA failure.

Two ordinary rounds and two independently reviewed listener wording rounds actually completed. The interrupted ordinary round 2 and its same-round continuation remain separate real closures, not a third retake. Following `docs/videos/DUBS.md`, skipping does not invent a QA pass or raise a limit. Final distinct review retains `faithful_change_available: true`: further faithful wording might exist, but both actual listener rounds are spent. Root actually prepared and committed the bounded disposition with exit 0, preserving the entire best track, narration, source, target, QA, raw ledger and paid evidence. Only `dubs/ja/skipped.json` was written in the native workspace; no absent `auto.json` was fabricated, and no score, threshold, owner choice, Korean held request or main film was changed. The private preparation failures and incomplete copies remain preserved; their narrow path/fsync repairs did not buy new audio or fix shared native journal code.

| Immutable private evidence | Full SHA-256 |
| --- | --- |
| `<operation>/dub-media-audits/ja-listener-r2-media/audit.json` | `ca5cd2b35a89fa0fe3727ad6b69277a966cb92bc3efce096f078b1f4ae895e21` |
| `<operation>/dub-media-audits/ja-listener-r2-media/receipt.json` | `9ee2e96ebf80cdc50113f67be16738dd26c0621e2ef29904148821b49ceafc9e` |
| `<operation>/dub-media-audits/ja-listener-r2-media/old-second-lineage-v2-bounded.json` | `8b18212f3c17ad206a4fbd1d711b22df3533ead6a4643a16241084626162f1c6` |
| `<operation>/ja-bounded-disposition/filled-20261007T181502Z-2814f8f0-e0c4-4d6e-955b-75cff2679c10/inputs.ready.json` | `6d1b8396acdbaa4d69ccf8ee38b01dd5bb07cdf9c65b52478496b52ac6f4759f` |
| Same directory `final-disposition.independent-review.json` | `7975a11c673867425142518d01045ddfa45a2f8022648ed79fda9d133b27e7d6` |
| `<operation>/ja-bounded-disposition/prepared-20261007T182848370Z-89f3cc77-9d92-4782-90d9-7a391a42c7dd/bounded-disposition.json` | `5a80142c4a0a32b6a636d9e6d8adc2b66c1bf46385bb454f6c52b605f6dbb996` |
| Retained current `dubs/ja.m4a` | `4ebade3e267d7d97b22c3531e11072c035d0fd13c32473956423c35b1d718d3d` |
| Current `dubs/ja/skipped.json` | `ee45c7e00865263963b9580d350fd9d3d52885d19b848161d2632a3bf2d1c4e8` |

Normal native captions and package actually closed exit 0. Current cues are zh-TW142 / EN142 / JA143 / KO143 / zh-CN142 = **712**, replacing the historical 718-cue base package. English captions follow its current dub timeline; Japanese captions retain the native current-dub timing despite bounded upload exclusion; Korean captions use the main narration windows because its dub is incomplete. These are native proportional caption intervals, not claimed word-level foreign-language measurements. Five metadata/descriptions, six current chapter clocks and four official source URLs are bound to current native reconstruction. There is one upload dub copy (EN), fifteen upload files including UPLOAD.md, and four fallback foreign thumbnails retain the approved Chinese thumbnail. Native package check is 4/4, which permits a missing working Korean dub and does not mean all selected languages completed.

Actual free selected-caption/package auditor `20261007T183156Z-selected-caption-audit-902e3c5f` closed exit 0. Its receipt is `<operation>/caption-review/selected-package-2026-10-07T18-32-08.322Z-dddfcaab-a516-4b5e-a25f-c015a8422774/receipt.json`, full SHA `f74846a9b2fed811cedf2782d464826ce45591568802e97060a4f89a2302024f` (680,593 B), status `partial_ko_held_working`, mechanical checks true / chosen languages complete false. Independent current-file readback SHA `9f974e8b122b208b1a410979a85976a0ef4e987e478b8e2bb02d25f5ae9b0bd7` rechecks 55 current files, eight exact delivery-copy pairs and fifteen-file inventory. Source and media did not change when later review commands appended native state/approvals.

Current upload metadata is `4d1d9f57327aa1205c0abe187297e02d7ce9a1a88e77f383f4835587f74f2ce6` (8,904 B). Normal publish review `285cfe5b-c0ab-4cf9-86ef-db4214b33c35` approved this exact hash at 18:33:58 UTC under the existing automatic setting; normal review-pull recorded it. Language review `2f2d801d-a877-473c-af00-932b8fa9f142`, manifest SHA `c56a1aabbc16d12c6f738d277773085cc1edf303d07224915ea6c87a7fc4429f`, is **pending**, with real files attached. Fresh GET 18:36:54 UTC / HTTP200 / body SHA `ce2bb461ac9b3639c8dabf0232a2df3449fcf28164eb6f004fc0426479f89c1a` reports EN metadata/CC/dub ready, JA metadata/CC ready and dub skipped, KO metadata/CC ready and dub working, zh-CN metadata/CC ready. Original language choices remain unchanged; YouTube ID/sync are null and ready_to_upload is false. Studio upload/acknowledgment, owner full-player/listening acceptance, merge, deployment and publication have not occurred. Korean 51 current clips and its unresolved ag121 held journal remain byte-preserved; no retry authorization or zero-charge claim was invented.
