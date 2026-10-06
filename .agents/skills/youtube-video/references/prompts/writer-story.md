# Writer prompt: ONE CHAPTER of a brand story, and the story's picture fix

Writer stage, variant `story` (`STORY_INSTRUCTIONS["writer:story"]` in `tools/video/automation/story-prompts.mjs`, which is what the worker actually sends; this page is the readable copy). The route is `references/story.md`; the design is `docs/videos/STORY.md`. A story is non-fiction told by a narrator alone over still cartoon pictures, so it does not use the drama's common rules (which forbid real brands): it has its own.

## What every call carries

`chapter` (`key` of hook, origin, idea, engine, turn, now; `number`; `point`, what this chapter tells; `budget`: `seconds`, `chars`, `shots`), `plan` (`question`, `takeaway`, all six `chapters` for context, `thumbnail`, `image_notes`, `sensitivity`, title and logline), `facts` (the plan's `must_verify`: `index`, `claim`, `sources`, `core`, `attributed`, `reviewer_only`, and the `chapters` each belongs to), `caveats`, `sources` (each: `index`, `url`, `publisher`, `kind`, `supports`; a readable page as `passages` cut around the chapter's figures, years and names, a page the worker cannot read as `read: "plan"` with only its `supports` line), `previous_lines` (the last sentences of the chapter before), `look`, `cast`, `names`, `story_rules` (lint's story rules), `script_writing`, `lexicon`, `line_ids`.

## Rules (the common part every story stage shares)

- Tell only what `facts` and the passages say. Every figure, year, name, price and quotation comes from one of them; nothing from memory, nothing invented, no filler. A fact of `facts` is told as the plan writes it.
- What is told beyond `facts` rests on an official page, or on two independent reliable sources (major media, an encyclopedia, a museum, a court document; two editions of one site are one source); what a single non-official source alone says is told as that source's account.
- `caveats` are the plan's fact checker's orders: what they say not to mention is not mentioned; a figure they say the sources disagree on is told their way; somebody's account is told as that person's.
- A fact marked `attributed`, and any anecdote on one non-official source, is somebody's account: 「照某某的說法」「據說」, never settled fact. A legend no source confirms is told only as a legend, and only when a passage mentions it.
- Negative events as a ruling or an official document tells them; a negative claim about a living person needs two sources; no guessing at motives, health or private life.
- No investment, medical, legal or political advice, no sponsorship, never tell anyone to buy. No 「經查證」「根據資料」「本影片」 in the narration.
- The narration may name brands, products and people; the pictures may not: no name of `names` in any prompt, camera or appearance, no logo, lettering, written word, trademark, copyrighted character or real person's likeness. A founder is a generic cartoon figure of the right era, dress and trade.

## The chapter

- One chapter per call; the worker merges the six, numbers the claims and lints the whole.
- Length: `budget` is the chapter's share of a 13-minute story (3,250 characters, about 90 shots). The plan's point is shorter on purpose: the rest comes from the passages, which say more than the plan does, and from explaining what the facts mean. Whatever is told beyond the plan is told from a passage, and the checker looks for it there. When the passages hold less, the chapter is shorter: never padded.
- Scenes `<key>-01`, `<key>-02`, …, every one a shot `{id, template: "shot", data: {prompt (English ≤ 1000, one frame, no name, no text), camera (push in, pull out, pan left, pan right, tilt up, tilt down, drift), visual: "still", characters?}, lines}`; 1 to 3 sentences, 25 to 42 characters, 6 to 12 seconds a shot. The last chapter ends with one outro card `now-outro` that answers `plan.question` in a line and gives one next step. The hook's first sentence is the question or a counter-intuitive fact; one of its shots draws `plan.thumbnail.idea` (named in `thumbnail_shot`).
- Lines: one spoken sentence each, about 18 characters, at most 40, narrator only; ids from `line_ids`; figures in Arabic digits as the plan writes them; every Latin word in `lexicon` or `lexicon_additions`. A line takes an `emotion` cue (zh-TW, at most 80 characters) where the delivery turns (slower on a figure or a year, a lift on the chapter's question, a held breath before the turn, warmth on a person's account): at least a third of the lines carry one (lint warns below that); a cue says how the sentence is spoken, never what it means. The narration's performance plan (`voice.performance`, `docs/videos/ILLUSTRATED.md` §聲音表演) is the voice's, set with the voice, not the chapter's to write. (The worker's text, `STORY_INSTRUCTIONS["writer:story"]`, does not carry the cue rule yet: `tools/video/automation/story-prompts.mjs` was outside the scope of `2026-10-05-voice-performance-contract`.)
- Claims: one row per checkable claim: `{claim, scene, source, fact}` (`fact` null when it is the writer's own, from a passage).

Answer: `{"title", "scenes", "claims", "lexicon_additions", "thumbnail_shot"?}`.

**Lint fix** (`lint_errors` and `current` present): change only what the errors name, keep every other line and id, return the whole chapter.

**Length fix** (`resize` and `current` present, after tts measured the narration off its band): `resize.seconds` says about how much to add (> 0) or cut (< 0) in this chapter. Cut what matters least, never a fact or an attribution; add only what the passages hold; keep the id of every line kept. When the passages hold nothing more: `{"no_more": true, "reason": "<zh-TW>"}`, and the video waits for the owner.

## The picture fix: variant `story-fix`

`STORY_INSTRUCTIONS["writer:story-fix"]`. `fix` (`kind`: keyframes, clips or look; `targets` with what the judge or the checks said; `owner_note` when the owner sent the storyboard back), `shots` (the named shots with their lines; every shot when the owner's note names none), `look`, `names`, `cast`, `image_notes`, `sensitivity`, `story_rules`. Rewrite only what draws them (fewer subjects, simpler hands, a plainer camera move, no text or logo, the subject clear of the bottom fifth where the subtitles sit); never a line. Answer `{"shots": [{"id", "prompt", "camera", "characters"?}]}`, or for look `{"characters": [{"id", "appearance"}]}`, holding only what changes. The worker lints the patch before keeping it: a name of the story in a prompt is refused before anything is drawn.
