# Formal255 rich-stage auditor revision

PREPARATION ONLY. No actual audit was run and no audioPASSproof issued.

New module SHA: ae768b1535a16206e9a65af5e3c243753eb92615b1a7700dd4aef2ea9fc10b82

Original723 module SHA: 723ab3b85f8059ff8d84e407e3a53b5615594374eccf086fd369e9fbd85b0a9b

First actualREVISE SHA: 7446e1deaf793acc3f750057506ff67551d85b4a86f76e8ea2aad6b39d7301fe

## Actual contract and correction

Producer history completion uses event native_step_finished / phasecheck and a full nested native stage object. Capture.stage and actual state latestENcheck run are deeply equal objects, not string labels. Immutablecapture520d2260...0fef demonstrates stagecheck-audio at2026-10-26T00:27:20.722Z and wrapper completion at00:27:20.776Z. The original723 module incorrectly required a string. Its actualREVISE is preserved with105acceptedclips and that single stageproblem.

captureMetadata now requires all three full objects to agree, explicit nativecompletion/check labels, valid exact native timestamp, matching locale, exactly expected105rows/count,0flags/unchecked. Missing/string/mismatched stage/run objects are rejected. nativeReceipt supplies its existing latest actual native run. Existing full raw/capture/log/artifact hashes, completed-process checks, matching thresholds, native WAV/currenttarget/cache, native PCM reconstruction, framebounds, native AAC rule and all8/readyscope remain unchanged.

Only the capture function/call, corresponding schema fixtures/newtests, header and distinct default safe output name differ. Reversing exactly these disclosed changes reproduces original723 bytes. Diff file: formal-language-auditor-rich-stage.diff.

## Pure verification

Syntax check passed.63puretests pass: all original38case names/order retained plus25observed-schema positive and perturbation negatives. Cases reject wrongphase/event/nestedlabel, missing/string objects, alteredat/count/flag/unchecked/locale/counters, rawIDs/fullSHA and logSHA. Stage objects in positive fixture are separate deep clones, proving value equality rather than reference identity. Full output saved in formal-language-auditor-rich-stage-selftest.json.

No actualaudit, ASR, TTS, ffprobe, credentials, network or paidcall. Originalmodule/selftests/firstfailedproof+log/capture remain exactSHA. Producer/event/state/cache/media were read only. Root must inspect then run the requestedactualaudit independently; concurrent sharedproducer changes remain legitimate rejections.

Future root-dispatched example, NOTexecuted:

node /workspace/work/ai-tech-next/verify-formal-language-delivery.rich-stage.mjs --profile formal255 --locale en --audit --out formal-language-audio-audit.en-rich-stage.NEW.json
