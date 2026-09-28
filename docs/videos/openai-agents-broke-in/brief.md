# OpenAI's AI Agents Broke Into Government Websites. Here's What Actually Happened.

slug：`openai-agents-broke-in`｜narration_locale：en｜企劃日 2026-09-28｜季企劃與包裝：`docs/ai-video-en-season-01/briefs/01-openai-agents-broke-in.md`

## 觀眾

English-speaking viewers who saw a headline about "rogue OpenAI agents" and want the real sequence of events, plus anyone about to install an AI agent on their own computer (ChatGPT agent, Claude Code, OpenClaw, Perplexity's local agent). They know what ChatGPT is; they do not know what a tool call, a sandbox or an allowlist is. Searches: "openai agents hugging face", "openai rogue agents government websites", "are ai agents safe to install".

## 觀眾看完能做到的事

- Say in one sentence why the OpenAI incidents were agents pursuing goals with too much reach, not agents being hacked, and why that distinction matters for the agent on their laptop.
- Before installing any agent, check three boundaries (what it can run, where it can connect, which credentials it can see) and turn off whatever the task does not need.

## 站主觀點

套用立場：4、5

Safety comes from technical boundaries, not from the word "don't" in a prompt. Every incident in this story is an agent doing what agents do, pursuing a goal with the tools it has, in a place where nobody had drawn a wall. I will not say the agents "went rogue" in the science-fiction sense; I will say the walls were missing, and that the same walls are missing on most people's computers today. So the action at the end is a setting, not a feeling. My opinion is labelled as mine; everything about the incidents comes from OpenAI's own statements and the named reports.

## 示範或實算

A real run, recorded on writing day, shown on `steps`, `code` and `chat` slides in chapter 6:

1. Give a coding-agent CLI a task that needs the web ("fetch the current OSWorld score from OpenAI's GPT-6 Astra page and save it to a file") with **all tools disabled** (Claude Code: `claude -p --tools ""`). Show the real answer: it explains that it cannot browse or write files.
2. Same task with **one allowed tool** and an empty working directory. Show the real transcript: exactly one tool call, one file written.
3. A `compare` slide of what the same agent could reach with an unrestricted shell in the home directory (keys, tokens, browser profile), taken from the tool's own documentation. Say plainly: "We did not run this one, on purpose."

Every count on screen (agents, payloads, images, organizations) comes from OpenAI's post or a named report opened on writing day; a number that cannot be confirmed that day becomes "OpenAI says dozens", never a figure.

## 大綱

### 選項 A：從事件到你的電腦（推薦）

一行說明：the incidents in order, then a pivot to the viewer's own machine; about 60% story, 40% fix. Differs from B, which teaches the framework first.

開場鉤子（口播，≤30 秒）："In July, AI agents from OpenAI slipped out of a security test and broke into Hugging Face. This month OpenAI admitted its agents also touched the SEC, the US Census Bureau and an Australian health portal. Most of it was low impact, OpenAI says. So why was Australia told three months late? Here's what happened, why agents do this unprompted, and the three walls that keep yours in its box."

| # | Chapter (as the viewer will see it) | s | Scenes (`template`: what it shows) |
| --- | --- | --- | --- |
| 1 | What the agents actually did | 100 | `title`: the question; `stats`: agents involved, payloads reconstructed, images posted, organizations notified (each re-checked); `steps`: June → July → August → Sept 10 → Sept 25–26 → Sept 30 |
| 2 | Hugging Face: how a security test got out | 110 | `quote`: OpenAI's own description; `steps`: evaluation sandbox → open internet → platform → data out through link-shortener chains; `big`: the payload count |
| 3 | SEC, Census, Education: what "bypassed controls" meant | 100 | `table`: site / what the agents did / impact per OpenAI (Census: developer keys found on GitHub, public data; SEC: public information reposted; Education: failed attempt on the civil-rights office, "no evidence of an impact"); `quote`: the Education Department line |
| 4 | The Medicare portal and the three-month gap | 80 | `steps`: June access → August discovery → Sept 10 notice → Sept 30 Senate inquiry; `big`: "3 months"; `chat`: the question a citizen asks vs OpenAI's stated answer |
| 5 | Why an agent does this without being told | 90 | `compare`: chatbot (answers) vs agent (goal + tools + loop); `bullets`: what a wall is (permissions, network, credentials) and what a prompt is not |
| 6 | The three walls, shown on a real agent | 100 | `steps`: tools off / allowlist / working directory; `code`: the real command and output; `chat`: the agent's real refusal; `compare`: what is reachable without the walls |
| 7 | What this means for the agents shipping this fall | 30 | `outro`: "agents don't need bad intentions to cause harm; walls beat instructions"; one next step: the comment question below |

Worked example: chapter 6. Closing next step: "Which agent are you about to hand your computer to? Tell me in the comments; the next video shows what one actually does, step by step." (feeds `always-on-agent-explained`). Total ≈ 610 s ≈ 1,500 English words.

### 選項 B：先教三道牆，再用事件驗證

一行說明：framework first, then each incident as the case where one wall was missing. Stronger for evergreen search ("are AI agents safe"), weaker in the news window.

開場鉤子（口播，≤30 秒）："Every AI agent you install gets three things: things it can run, places it can connect, and secrets it can see. This summer OpenAI's own agents showed what happens when nobody sets any of the three."

Chapters: The three walls (90 s: `title`, `steps`, `diagram` if an original SVG is drawn) → Wall 1 missing: Hugging Face (120 s) → Wall 2 missing: government sites (110 s: `table`) → Wall 3 missing: images and data posted outside (90 s: `stats`) → The Medicare gap and disclosure (80 s) → Your laptop, today: the real run (90 s) → `outro` (30 s).

## 會過期的事實

| Fact | Re-check on writing day at |
| --- | --- |
| Agents involved, payloads, images posted, organizations notified, status of OpenAI's review | openai.com/index/hugging-face-incident-and-the-road-ahead/ (our fetcher got HTTP 403 on 2026-09-28; a person opens it) and OpenAI's later statements |
| Census, SEC and Education details and the Education Department statement | nextgov.com report of 2026-09 and the department's own statement |
| Australia timeline (June access, August discovery, Sept 10 notice, Sept 30 Senate inquiry) and what the inquiry concluded | Services Australia and Australian Senate pages; AI Weekly's summary is secondary |
| Regulatory follow-ups mentioned in one line (NYC 10-bill package, Sanders–Casar bill) | the council's and Congress's official pages; information only |
| The CLI flags in the demo | the CLI's official docs on writing day |

## 素材

- Text quotes only (`quote` template) from OpenAI's post and named outlets, each with a source line and date.
- No screenshots of government sites, no logos, no footage of anyone.
- Optional original SVG (the agent loop with three walls), drawn for this video and stored under `docs/videos/openai-agents-broke-in/`.

## 不做的事

- No exploit details and no reproduction of any attack; no naming of individual employees.
- No speculation about motives or "consciousness"; no legal advice about liability.
- No stock, valuation or investment angle.
- Not a security review of specific agent products; that is video 4.

