# Curio S40 blind narrative receipt (r4c)

## Blind inputs and integrity

- Read only `script.md` and the 13 questions returned by `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s40 --json` before sealing this verdict.
- `script.md` SHA-256: `08a7e46a7d1271ca407f7e4e265bd7c0eb57340239411948b28498e09367327f`.
- Exact saved CLI JSON output SHA-256: `e14af57f06e2e03e8edc02367d73c3b06ce9d9e3044fa9828eb39a2fb9b194e3` (`/tmp/curio-s40-official-narrative-r4c.json`).
- The supplied card/layout binding is video.json SHA-256 `c6f3efbbf32ed39dcf74faca717c314e7e90f6e5cb34d3186d12d71aa28b5aba`. It is context, not independently checked in this blind read.
- Verdict: **13 Yes, 0 No**. Script line references below are to the hashed file.

| Official ID | Answer | Script lines and reason |
| --- | --- | --- |
| `scene_first` | Yes | L9–17: the mausoleum in Alexandria, the basket carrier, and the guard inspecting figs put the first four spoken sentences in an action. |
| `no_spoiler` | Yes | L9–25: the snake is introduced as a claim, while the letter, unopened door, and later triumph image stop before the death scene or final answer (L213, L343–347). |
| `one_line` | Yes | L31–347 follows Cleopatra's capture, guarded final days, death, and examination of its cause; the opening basket/door preview (L9–25) rejoins that sequence at L175–213 rather than starting a separate story. |
| `no_toc` | Yes | L31's “先回到那扇門還關著的時候” places the story before the previewed door opening; it does not list the video structure. The other transitions stay with actions or questions (L81–85, L133–139, L233–239, L283–289, L321–327). |
| `chapters_link` | Yes | The seven later chapter starts take up the prior open item: door → earlier closed door (L25→31); knife capture → guarded survival (L79→85); unnamed young man → Dolabella (L133→139); basket in room → sealed letter (L187→193); basket's explanation → snake claim (L233→239); Dio question → Dio's uncertainty (L283→289); another author's wording → “被認為” (L321→327). |
| `open_loops` | Yes | Questions or held outcomes occur throughout: L17–25, L39–79, L89–133, L147–187, L209–233, L263–283, and L301–343. The CLI time marks place no stretch of the body over 90 seconds without one. |
| `payoffs` | Yes | Concrete payoffs include closed-door question → window and ladder (L55–71), fasting → children used to make her eat (L89–97), Octavian's belief → his mistaken confidence (L109–129), Dolabella → removal news (L133–143), basket → reported snake story and its hearsay status (L233–247), Dio's judgment → no firm cause (L283–305), and rescue/eyewitness questions → qualified wording and no proof (L317–347). The broad choice at L39 resolves through the threat of capture and her death (L43–47, L129, L213); the guard question at L17 resolves as unverified rather than a witnessed miss (L247, L267). |
| `no_recap` | Yes | The return to the figs explicitly calls back “開頭那籃” and adds the snake claim (L239–247). The later marks and source versions add different evidence and limits (L267–279, L289–313); the final snake image supplies a public depiction, then separates it from proof (L335–347). |
| `chapters_are_events` | Yes | Each heading names an action or revealed event: guard opens figs (L5), Antony is hauled inside (L27), guards keep the queen alive (L81), Dolabella brings news (L135), the sealed letter leaves (L189), basket is said to hold a snake (L235), Dio places her in the palace (L285), and Octavian orders treatment while a snake image enters the triumph (L323). |
| `outro_no_next` | Yes | L355 asks viewers to subscribe; it does not name a next video, episode, or file. |
| `opening_hooks` | Yes | After the guard's first basket inspection (L9–13), the snake-under-figs claim (L17), sealed letter and dispatch (L21), impending door opening (L25), and later triumph snake image (L25) all hold their outcomes for later. |
| `one_thread` | Yes | Cleopatra's last available choices and the uncertain death method connect the capture (L31–85), guarded deception and removal news (L89–159), death scene (L175–229), and conflicting accounts/evidence (L239–347). |
| `no_detour` | Yes | The attempted fasting, inventory and apparent wish to live explain how Octavian guarded and misread her (L85–129); the visit to Antony's tomb, basket, and letter lead to her death (L139–225); every later source comparison tests the snake-bite claim (L239–347). |

This is a narrative judgment from the script and official question text only; it does not verify historical claims, visuals, or the supplied video.json binding.
