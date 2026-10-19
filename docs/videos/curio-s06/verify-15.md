# S06 R11 five-line audio clarity revision — frozen for new review

R10 passed formal independent blind review 13/13 and a separate pinned-source/80-prompt audit, but its measured 81-line narration was not audio-clear. The first `check-audio` found eight flagged lines; an eight-line retake cleared three, leaving `gs020`, `gs022`, `gs116`, `gs119`, and `gs057` flagged. The second raw receipts are [`audio-check-r10b.json`](audio-check-r10b.json) SHA-256 `c07dd806dafebbef6cebba5c215d055a1195683c8a05486e614b3c88b7d0783c` and [`audio-flags-r10b.json`](audio-flags-r10b.json) SHA-256 `4c39a4d1b9352bcb4d1ce9a0795c7e951fe66dac1b3a380163e68031e0b8454a`. The measured R10 story body after retake was 525.33 seconds (8:45.33); it is **not** timing evidence for this revised script.

The R11 script changes only those five sentences, preserving the same claims and scene prompts:

- `gs020` removes a repeated recap of the novel doctor's farewell (already stated at `gs105`) and asks what the historical biography writes first. This also avoids speech recognition confusing 辭行／此行 and 陳壽／陳述.
- `gs022` still attributes the stray arrow and absent tent-entry scene to 〈關羽傳〉, but says 流矢擊中 rather than the ASR-confused 流矢射中. The biography does not depict the physician entering the tent.
- `gs116` says the biography does not name the archer but specifies the wounded arm, avoiding the homophone 陳壽／陳述. It leaves the left/right reveal at `gs024`.
- `gs119` retains the explicit novel-to-history callback and G's blood-filled vessel, saying 盛血的盤器 rather than ASR-confused 血盛於盤器. It does not claim the two vessels have the same shape or depict visible blood.
- `gs057` names 《三國演義》 in full so the listener hears the fictional Fan Castle setup clearly; it still asks the chronology question answered at `gs059`.

Current frozen `script.md` SHA-256 is `0ed28722fed8194562cb45348966e621ef47b4b3427e7f92b0e970129f636fca`, `video.json` SHA-256 is `87e48100cc1ff7f090175cc7f1019009adbfc74eef69d9cb25c308a9fb3734dc`, and the narrative hash is `99f4339b73b5114e`. The 81 claim rows remain 81/81 exact; lint reports zero errors and zero warnings, and the static full-run estimate is 8.9 minutes. **The previous R10 approval and narrative receipt are for another script hash.** Do not resume TTS, audio approval, music or paid images until a fresh context-isolated blind reader clears this exact R11 script and a source-delta review confirms the five lines.
