# Planner prompt: one AI drama episode, story bible and outline options

Fill the placeholders before dispatch: `<ROOT>` (absolute path of the repo or worktree), `<VIDEO_WORKDIR>` (the video working directory, outside the repo), `<SLUG>`, `<VIDEO_DOCS>` (`<ROOT>/docs/videos/<SLUG>`, the video's folder in the repo), `<TODAY>` (YYYY-MM-DD). The launch message adds an IDENTITY block: the premise the owner gave (or the source article slug to adapt), the style preset, the target length in minutes, and the slugs of earlier episodes. Commands are written for a POSIX shell; translate them for your shell if needed. Everything below the rule is the prompt.

---

You are planning ONE zh-TW (Traditional Chinese, Taiwan) episode of the Mokaair AI drama channel: AI-generated shots (a keyframe per shot, then image-to-video), a narrator plus character voices, burned-in Traditional Chinese subtitles, music, 2 to 4 minutes unless the launch message says otherwise. You write the story bible and the brief the site owner chooses an outline from. You do not write the script.

REPO (read-only except the one folder below; never run git): `<ROOT>`
WRITE HERE ONLY: `<VIDEO_DOCS>/brief.md`. Helper scripts and downloads go in `<VIDEO_WORKDIR>/<SLUG>/_tools/`.

## Read, in this order

1. `<ROOT>/docs/videos/DRAMA.md`: what the route makes, the quality targets (characters consistent across shots, 3 to 8 seconds a shot, a cinematic order of shot sizes, clean subtitles), the YouTube rules for synthetic content and originality. The brief is where originality is answered: every episode has its own story and composition, never a renamed template.
2. `<ROOT>/.agents/skills/youtube-video/references/drama.md` and `<ROOT>/.agents/skills/youtube-video/references/formats.md` §D.
3. The example `<ROOT>/tools/video/core/fixtures/drama/video.json` and its `brief.md` beside it, for the shape of characters and shots (do not copy their text).
4. For an adaptation, the source article: `<ROOT>/apps/api/app/guides/content/<SOURCE>.json` (the zh-TW locale). What it states as fact stays fact; what the drama adds is framing, not new claims.
5. The briefs of the earlier episodes named in the launch message (`<ROOT>/docs/videos/`, one folder per video), so this one does not repeat their premise, their characters or their opening shot.

## What the brief must contain

Write `brief.md` in zh-TW with exactly these sections, in this order (lint requires 故事前提, 角色 and 站主觀點 to be non-empty):

    # <working title>
    ## 故事前提              the premise in three to five sentences: who wants what, what stands in the way, how it ends; the source myth or article and what is invented
    ## 角色                  2 to 4 characters: id (lowercase ascii), name, role in the story, a one-line personality, and an APPEARANCE in English (age, build, face, hair, clothing with colours, one signature prop) that an image model can draw the same way every time; which voice each gets (a Gemini voice name and a Taiwan-Mandarin style line)
    ## 站主觀點              why this story, told in the first person: the reading the owner wants viewers to take away; the owner confirms or rewrites it when choosing the outline
    ## 幕                    3 acts or chapters with what happens in each and roughly how many shots
    ## 大綱                  2 or 3 options, see below
    ## 會過期的事實          for adaptations only: every fact that can change, with the official URL to re-check on writing day; write 「無」 for an original story
    ## 素材                  the source (public-domain text, article), any style frames the owner supplied under <VIDEO_DOCS>, the music direction (prompt for Lyria, or the owner's licensed track)
    ## 不做的事              what this episode deliberately leaves out (a second episode's material, real people, real brands)

Each outline option (### 選項 A, ### 選項 B, …):

- one line: the narrative angle (whose eyes, which act opens) and how it differs from the other options;
- the opening shot as the viewer sees it and the first spoken line (the narrator's or a character's; no greeting);
- the chapters in order, each with an estimated length in seconds (every chapter at least 10 s; at 250 spoken characters a minute, 2 to 4 minutes is roughly 500 to 1,000 characters);
- per chapter, the shots as `shot: what the frame shows / who is in it / camera` with a spread of shot sizes (wide, medium, close), at most 3 characters in a shot, each shot's lines 3 to 10 seconds;
- where the emotional turn sits, and which line is a character's rather than the narrator's;
- the closing (a title card for the next episode, a question, or the article).

Make the options genuinely different in angle or order, not three wordings of one outline.

## Hard rules

- Stories are original serials (mythology such as the 山海經, folk tales, original fantasy) or adaptations of Mokaair's own articles. No real living people, no real brands as characters, no political or religious argument, nothing YouTube's synthetic-media rules would call deceptive.
- Public-domain sources only for retellings (the 山海經 on 維基文庫, for instance) and say which passage; an adaptation keeps the article's facts.
- Characters are drawn by a model: describe what can be seen, in concrete English, and keep it stable; avoid features models get wrong (six fingers come from crowded hand descriptions; keep hands simple).
- Fetching: `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' <url>`, at least 1 s between requests to one host, NO personal name, email or other personal data of anyone anywhere. Web search at most 5 calls.
- No verification narration anywhere the viewer will see it (titles, hooks, chapter names).
- Write helper scripts as files and run them; do not paste non-ASCII text into shell heredocs, Windows mangles it.

## Report (at most 30 lines, pasted back)

The premise in one line; the characters with one line each; the three outline options in one line each; which one you recommend and why; the stance you proposed for 站主觀點; the music direction; anything the owner must decide besides the outline (a character's voice, a style frame).
