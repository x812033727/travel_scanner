# Verifier prompts: an EPISODE's tension and continuity check, and the RECAP

## `verifier:episode` (on top of `verifier-drama.md`)

The bible is `setting_md` plus `characters` (which must equal `cast` word for word); the history is `recaps`; the contract is `beats`. Two checks on top of the drama checker's continuity pass:

1. Tension: `coverage` scores `hook`, `conflict`, `turn` and `cliffhanger` as `有` (delivered), `弱` (present but flat, late, or told rather than shown) or `無` (missing); a cliffhanger followed by a summary or a moral is `弱`.
2. Series continuity: names, ranks, wounds, objects and places against `setting_md` and `recaps`; a mystery resolved that `mysteries` marks reserved; a payoff without its setup; a character speaking against their `speech` habit.

Also name any resemblance to a well-known existing work in `similar_works`. Fix ids, spellings, `characters` lists and prompt contradictions as before; do not restructure.

Answer: `{"report", "video"|null, "claims", "changed_facts", "coverage": {"hook", "conflict", "turn", "cliffhanger"}, "problems": [zh-TW sentences the owner reads on the script's review card], "similar_works": [...]}`. The worker writes `coverage`, `problems` and `similar_works` to `<workdir>/review/script-check.json`, which `review-push --gate script` shows at the top of the owner's card.

## `verifier:recap`

After the episode is assembled: `video` (the final script), `beats`, `previous_recaps`, `episode`. Answer `{"recap": zh-TW ≤ 150 characters, what happened and what it changed, no adjectives, "state": {"characters": {id: one line}, "mysteries": {id: "planted"|"advanced"|"revealed"}, "open_threads": [...]}}`. The worker sends it to `POST /video/automation/series/<slug>/episodes/<n>/recap`; the next episode's writer and checker read it.

## `verifier:episode` with the retention rules (docs/videos/BINGE.md)

When the genre section at the end of the prompt carries `RETENTION_RULES`, add a third check and report it:

3. Retention: `coverage.satisfaction` says whether the `beats.satisfaction` moments are played (有), only mentioned (弱) or missing (無); `retention` names the lines: `hook_line` (the line id that is the hook), `satisfaction_lines` (one line id per satisfaction beat, in order), `cliffhanger_line` (the line id of the cliffhanger; it must be the last line of the script). Name ids only: the tool measures the seconds on the estimated timeline (`retentionNumbers`) and ignores any number you write.

Answer then: `{"report", "video"|null, "claims", "changed_facts", "coverage": {"hook", "conflict", "turn", "cliffhanger", "satisfaction"}, "problems": [...], "similar_works": [...], "retention": {"hook_line", "satisfaction_lines", "cliffhanger_line"}}`. On a hands-off series the worker judges the script from this before sending it (`scriptVerdict`: no 無, at most one 弱, no problems, no similar works, hook inside 8 s, first satisfaction inside 30 s, at least 2, cliffhanger last) and the site approves it on arrival by the same rule (`script_check_passed`), so every problem you list sends the script back to the writer.
