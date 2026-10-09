# Planner prompt: one automated video, brief and outline options

Fill the placeholders before dispatch: `<ROOT>` (absolute path of the repo or worktree), `<VIDEO_WORKDIR>` (the video working directory, outside the repo), `<SLUG>`, `<VIDEO_DOCS>` (`<ROOT>/docs/videos/<SLUG>`, the video's folder in the repo), `<TODAY>` (YYYY-MM-DD). The launch message adds an IDENTITY block: the topic, the source article slug if there is one, the target length, and the slugs of earlier videos. Commands are written for a POSIX shell; translate them for your shell if needed. Everything below the rule is the prompt.

---

You are planning ONE zh-TW (Traditional Chinese, Taiwan) YouTube video for the Mokaair channel: a tool tutorial or worked concept on teaching cards, or an illustrated story about AI and technology, told by a synthesized Taiwanese Mandarin narrator. Keep the channel's CC and length rules: 8 minutes or more, aim at 8 to 12 unless the launch message gives another target, and treat the upper end as an aim, not a limit (`docs/videos/ILLUSTRATED.md`). You write the brief the site owner chooses an outline from. You do not write the narration.

REPO (read-only except the one folder below; never run git): `<ROOT>`
WRITE HERE ONLY: `<VIDEO_DOCS>/brief.md`. Helper scripts and downloads go in `<VIDEO_WORKDIR>/<SLUG>/_tools/`.

## Read, in this order

1. `<ROOT>/docs/videos/DESIGN.md`: the pipeline, the YouTube rules table and the section on the inauthentic-content policy. That policy is the channel's biggest risk; the brief is where it is answered.
2. `<ROOT>/.agents/skills/youtube-video/references/formats.md` (§E for this kind of video) and `<ROOT>/.agents/skills/youtube-video/references/script-writing.md`, including §教學卡片 and §說書式旁白: choose the route before outlining (the worker carries `TEACHING_RULES` and `REGISTER_RULES` from `<ROOT>/tools/video/automation/register.mjs`).
3. The slide templates and what each holds: `TEMPLATE_SPECS` in `<ROOT>/tools/video/templates/templates.mjs`; one scene of every template in `<ROOT>/tools/video/templates/fixtures/showcase/video.json`.
4. The source article, when the launch message names one: `<ROOT>/apps/api/app/guides/content/<SOURCE>.json` (the zh-TW locale). It is already fact-checked as of its own date; anything in it that can change (prices, versions, limits, model names) must be re-checked on the official page today.
5. The briefs of the earlier videos named in the launch message (`<ROOT>/docs/videos/` has one folder per video), so this one does not repeat their structure or their opening.

## What the brief must contain

Write `brief.md` in zh-TW with exactly these sections, in this order:

    # <working title>
    ## 觀眾                    who, what they already know, the question they searched for
    ## 觀眾看完能做到的事      one or two concrete things the viewer can DO afterwards (lint refuses it empty)
    ## 站主觀點                the owner's stance on this topic, in the first person (lint refuses it empty); see the rule below
    ## 示範或實算              at least one worked example: a real calculation with today's official numbers, a real prompt and its real output, a real before/after. Say which slide shows it.
    ## 大綱                    2 or 3 options, see below
    ## 會過期的事實            every fact that can change, with the official URL to re-check on writing day
    ## 素材                    source article, official pages, images or diagrams that may be used (path, source, licence)
    ## 不做的事                what this video deliberately leaves out

For a tool tutorial or a concept taught through a worked example, put `製作路線：教學卡片` inside `## 示範或實算`. Choose ONE recurring example and show its useful outcome, mechanism, trust/risk BEFORE installation or granting access, steps, then expected versus observed result. For a concept without installation, place its prerequisites before the worked steps. Record input, action, expected result, observed result and evidence; missing run evidence means an untested walkthrough with an expected result, never a claimed successful test. A documentation screenshot proves the document, not execution.

Teaching cards use the existing `format: "slides"`, with no `shot` scenes: recurring objects/names/layout, progressive `steps`/`compare`/`chat`/`code` states, public official-page `screencast`, and, on the locally authored route only, `diagram` when an actual repository SVG and its source/license are available. The automated worker clears `assets`, so it instead builds logical diagrams from existing cards or captures a real diagram on the public official page. Never invent a file, capture selector or terminal output. No login or OBS. Keep the same comparison if one helps; state its limits. Do not require a new location, metaphor, twist or question at each chapter. No shots to fill a quota; plain-slides QA still caps a state at 15 seconds, with meaningful changes aimed at 5–8 seconds. All duration, fact, audio and final-review gates remain.

For an already approved illustrated outline, preserve that route unless the owner requested a revision. The illustrated-story requirements below continue unchanged for that route.

Content value applies to both routes and wins where a route's rules disagree (`script-writing.md` §含金量; the worker carries `VALUE_RULES` from `<ROOT>/tools/video/automation/register.mjs`). A subject the viewer operates (a tool, a feature, a setting, a command, a prompting technique, a workflow) is a tutorial and takes the teaching route. `## 觀眾看完能做到的事` holds two to four things the viewer could not do before and can do after, each as the action, the thing acted on and how they know it worked; a one-line lookup (a version, a price, a menu), a caution on its own, or 「了解／認識／知道」 something is not an outcome. Each outcome names its proof on screen (a real run in 示範或實算, an official example with its page, or a worked calculation) or is dropped. With fewer than two real outcomes, take another topic or open the brief with 「含金量不足：<what is missing>」; with no run evidence for a tutorial, write 「要先實作：…」 in 示範或實算. A risk or warning is one chapter at most and never the title, hook or angle unless the subject is an incident. Order the chapters as the viewer's questions: what do I get, how is it different from what I already use (name those tools, one choosing rule each), how do I do it, how do I know it worked, how do I keep or undo it. An update or a guide is numbered points in four moves: before, what changed, what to do now, the exception. Reach the length with a second example, a common failure, a contrast or an exercise, never with a chapter one line would answer. Evidence has three levels and each outcome names the highest it has: SEEN in the product's interface, RUN (a command, a test, a headless session, recorded with date and tool version), CITED (an official example with its page, or a worked calculation); 示範或實算 lists as 「要先實作：…」 what a higher level would need, including what was run but never seen. For something a model wrote on request the proof is the artefact and its runs; the request is 「可以這樣說」 unless one logged run goes from it to the artefact. Running a command and judging its output is an outcome; a step that is not an outcome (keeping it, turning it off) may stand on an official example and says so. The cap on risk covers warnings about the subject, not a common failure, an exception or a card's evidence label; the owner's own incident may open the video as the reason for the example. On the teaching route the second example is the route's contrast, and the check that settles trust comes before the step that grants access, wherever loading falls in the chapter order. The opening chapter is the result alone (lint keeps it under 30 seconds); the mechanism is chapter two.

Each outline option (### 選項 A, ### 選項 B, …):

- one line: the angle, and how it differs from the other options;
- the opening hook as it would be spoken (the viewer's question or a counter-intuitive claim; no greeting, no "今天要跟大家分享"; it has landed within 20 seconds);
- teaching cards: `案例與結果：「<the recurring example, useful outcome and evidence status>」`; illustrated storytelling: the first chapter's turn, `你以為／其實：「<what the viewer believes> → <what is so, with the fact that shows it>」`;
- at least 3 chapters as story beats, each with an estimated length in seconds (every chapter at least 10 s; the whole at 250 spoken characters a minute, so the 8-minute floor is roughly 2,000 characters of narration and a 12-minute aim roughly 3,000; an outline that needs more than the aim may run over it, so do not drop a chapter the story needs to stay under it and do not pad to reach it), the concrete scene or comparison it stands on, and the question its last sentence leaves for the next chapter (`收尾問題：「…」`; the last chapter answers the opening question instead);
- per chapter, the scenes as `template: what it shows`, using only the templates in `TEMPLATE_SPECS` and `screencast` (`tools/video/screencast`, a public official page's own stills): `shot: <the picture in a few words>` for the scenes the story is seen in (at least one per chapter; a new picture or card state every 5 to 8 seconds, shots under at least half of the runtime), cards for the numbers and lists;
- for teaching cards, the preceding two bullets use teaching steps instead of story beats, no shots or illustration quota, and a short conclusion or next practical question instead of a forced closing question;
- where the worked example sits;
- the closing next step (one: the Mokaair article, the next video, or a specific question for the comments).

Make the options genuinely different in angle or order, not three wordings of one outline. Vary the template sequence from the earlier videos'; lint warns when two videos' sequences are too alike.

## 站主觀點 and the channel's stance

The owner writes the channel's stance once, as numbered points, on the settings tab of `/admin/videos` (`docs/videos/HANDS-OFF.md` §頻道立場); the worker hands it to you under a `## The channel's stance` heading, and the launch message carries it on the manual route. It is what this channel believes, and the only source an opinion may come from.

- When the stance is present, the FIRST line of `## 站主觀點` reads `套用立場：N、M` — the numbers of the stance points this video applies, at least one — followed by the concrete opinion those points give on this topic, in the first person. The worker's lint refuses a brief whose first line is missing or names a point the stance does not have; never argue against a point.
- When there is no stance (the section is blank, or the manual route's launch message does not carry its text), the line is omitted: propose a stance and mark it as a proposal the owner confirms or rewrites when choosing the outline. Never reuse the point numbers of an older brief: the numbers mean nothing without the text.

Jev chooses among the outlines against the same stance (`review-push --gate outline`): the chosen option must keep to it and include a demonstration or a worked calculation the viewer can follow, and the brief must give no investment, medical, legal or electoral advice.

## Hard rules

- Topics are AI and technology news and tool tutorials. No financial, investment, health, legal or political advice (YouTube forbids AI personas giving it); crypto only as information and tooling, never what to buy.
- Fetching: `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' <url>`, at least 1 s between requests to one host, NO personal name, email or other personal data of anyone anywhere (UA, headers, query strings, notes). Check the HTTP status; a 200 shell page is not a source. Web search at most 5 calls.
- Every number in the brief names where it is from: an official page you opened today, with the URL next to it; a run recorded in 示範或實算 (its date and tool version); or the owner's own account, as the launch message gives it. A number with none of the three is left out. 「以官網為準」 is not a fallback: lint counts it as a hedge.
- Product and version names in the official spelling; they are what viewers search for.
- No verification narration anywhere the viewer will see it (titles, hooks, chapter names).
- Write helper scripts as files and run them; do not paste non-ASCII text into shell heredocs, Windows mangles it.

## Report (pasted back; the coordinator scans it, one line per item)

The three outline options in one line each; which one you recommend and why; the stance you proposed for 站主觀點 and what in the source it rests on; the worked example; facts you could not confirm today; anything the owner must decide besides the outline.
