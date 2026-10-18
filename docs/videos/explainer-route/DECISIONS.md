# Explainer route takes a series look: decisions that are fixed

Ticket: tasks/open/2026-10-10-explainer-route-takes-a-series-look.md.
On 2026-10-10 (about 14:50Z) the owner was shown four open questions and answered 「用你建議的」
(use what you recommend). The recommendations below are therefore the owner's decisions; the
rest are engineering defaults chosen by the coordinating session and may be argued with in a
design, but only with a concrete reason.

## The owner's four decisions

1. **奇聞檔案局's identity on the host: the channel's, for now.** A `cute-mystery` video gets
   the channel-default bookends and the channel `thumb` thumbnail (tag = the pillar's name,
   headline of at most 6 characters), exactly what the three approved local pilots used
   (curio-h01, curio-u02, curio-l08). No new THUMB_SERIES entry, no new branding registry, no
   new Shorts theme in this ticket. A series-own intro or thumbnail is a follow-up ticket.
   `cute-cartoon` IS 原來如此事務所 and keeps the `sothatswhy` identity everywhere
   `flat-explainer` has it today (series bookends, series thumbnail and its pillar ids, the
   Shorts series). So "is an explainer" (the family: narrator only, stills, no cast, the
   8-minute floor) must be separated from "which series' identity" in code.
2. **The planning document keeps its shape.** Both new presets keep the question-shaped bible
   and brief (question, one-sentence answer, hook, at least two reasons, https sources). For
   奇聞檔案局 the prompt tells the planner to use the reasons as the evidence chapters in the
   order 流傳的版本 → 紀錄裡有什麼 → 目前最站得住的解釋. No change to the brief sections in
   lint, to `_explainer_bible_problem` on the API or to `documentProblem` in the tools.
3. **MiniMax by default for the cute looks.** A request with `cute-cartoon` or `cute-mystery`
   that names no image model is stored with `image-01` by the server, and the request form
   preselects it. Filing a request whose image model's vendor has no key on the site is refused
   at filing, before any paid planning. `image_model` on a one-off request is accepted for the
   explainer family only (a cast drama needs reference sheets that image-01 cannot hold).
4. **Nothing that exists moves.** `flat-explainer` stays byte for byte what it is today:
   preset text, prompt text, payload, Gemini default. Existing rows, look hashes, image cache
   keys, request hashes and unfinished journals must not change. So That's Why's 192 planned
   episodes (docs/videos/long-form/plans.json) stay on `flat-explainer` in this ticket; moving
   them to `cute-cartoon` with `image-01` is a separate ticket, after the owner has approved
   the first MiniMax episode (sothatswhy-b26).

## Engineering defaults (argue only with a reason)

- Names are final: `cute-cartoon` (原來如此事務所) and `cute-mystery` (奇聞檔案局). They go
  into CHECK constraints; both fit String(16).
- Look texts (positive only, `negative: ""`, `motion: "slow push in or gentle drift, no morphing, no cuts"`):
  - cute-cartoon: "cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, bright flat colours with soft cel shading on a warm cream paper ground, ink navy, mustard yellow, stamp red only on the answer, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9"
  - cute-mystery: "cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, flat colours with soft cel shading, a limited palette of deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9"
- Both presets inherit every duration rule of `flat-explainer` (8 to 20 minutes, default 10,
  the 480-second measured floor).
- The series' brief reaches the prompts from a registry in the tools keyed by preset (series
  name, pillars, episode shape, content rules, look allowances). No new columns for it.
- New prompt variants per new preset rather than rewriting the `explainer` variant, so the
  `flat-explainer` prompt bytes are untouched by construction and the stored "prompt sent" row
  does not flip between series.
- The cute looks contradict two sentences of today's explainer prompt ("No mascot or recurring
  character", "anonymous figures … no real faces"): the new variants allow simple chibi
  figures; 奇聞檔案局 may draw a person dead for more than 70 years as a cartoon
  (docs/videos/history-curiosity/README.md §內容守則) and never a living person's likeness.
- The host's writer is NOT offered `screenshot` or `photo` cards in this ticket: the automated
  route has no way to supply and credit an image file (`settle()` empties `assets[]`). That
  part of the ticket's definition of done moves to a follow-up ticket.
- Web, API and tools that know the new preset names ship in one deploy.
- Landing order: (1) presets, migration and family recognition on all three sides; (2)
  `image_model` on the request with the default and the key check, and the form field;
  (3) the prompts. Each pull request needs the duration receipt re-issued by an agent that did
  not write the change.

## Accepted afterwards

- 2026-10-10: the owner also accepted the designer's five choices listed in section 1 of
  [`DESIGN.md`](DESIGN.md) ("Recorded as decided"), after an independent critique had kept all
  five: `steps` and `table` cards for the two cute presets only; the nine yes/no picture checks
  and the picture-variety lint for the cute presets; `settle()` keeps only `{ preset }` of a cute
  look; `genre_spec: null` in a cute bible's planner payload; one discussion variant per series.
