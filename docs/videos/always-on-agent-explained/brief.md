# Chatbots Are Over. Here's How an AI Agent Actually Works (and Fails).

slug：`always-on-agent-explained`｜narration_locale：en｜企劃日 2026-09-28｜季企劃與包裝：`docs/ai-video-en-season-01/briefs/02-always-on-agent-explained.md`

## 觀眾

People who use ChatGPT or Claude every week and keep hearing "agent" without a picture of what changes. Hook audience: anyone who watched OpenAI's DevDay (2026-09-29) or read about an always-on assistant that keeps working after the chat closes. Searches: "what is an AI agent", "AI agent vs chatbot", "openai always on agent", "computer use AI explained".

## 觀眾看完能做到的事

- Trace what an agent does between "just handle it" and the result: goal, tool call, observation, next step, stop condition; and spot when a demo is really just a chatbot with nice formatting.
- Ask three questions before handing an agent a task: what evidence will I get that it finished, what can it touch while I am not watching, and what does a wrong answer cost me.

## 站主觀點

套用立場：3、4、5

An agent's output is a claim until I have opened its evidence: the file, the diff, the booking reference. I treat "always-on" as a reason to draw boundaries first, not as magic; an agent that acts while I sleep needs walls more than one I watch. The benchmark numbers (OSWorld 72.6% for GPT-6 Astra, 81.8% partial for Claude Opus 5.5, as their makers report them) mean one task in four or five still goes wrong, so the question is never "is it smart enough" but "what happens to the wrong ones". This is my reading; the numbers are the companies' own.

## 示範或實算

A real agent run on a harmless, checkable task, recorded on writing day and shown step by step on `steps` and `chat` slides (chapter 2): "Find the official API prices of three models, write a comparison table to a file, and tell me which page each number came from." The slides show the actual sequence: the goal, each tool call (fetch page → read → write file), the observation the agent acted on, and the stop. Then the calculation in chapter 3 on a `stats` slide: at the reported success rates, out of 100 computer-use tasks about 27 fail with Astra's number and about 18 with Opus 5.5's partial score; what that means when the task is booking, paying or deleting.

## 大綱

### 選項 A：一次真實執行，拆成五拍（建議）

Angle: one real run carries the whole explanation; the DevDay news frames why it matters now. Differs from B, which starts from the news and explains later.

Hook: "This week OpenAI showed an assistant that keeps working after you close the window, and every lab is building the same thing. Most explanations stop at 'it can use tools'. So I gave one agent a boring task, recorded every step it took, and I'm going to show you the five moves that turn a chatbot into an agent, plus the one in four tasks where, by the makers' own numbers, it still gets it wrong."

| # | Chapter | s | Scenes |
| --- | --- | --- | --- |
| 1 | The one-sentence difference | 70 | `title`; `compare`: chatbot (text in, text out) vs agent (goal, tools, loop, stop); `big`: "goal + tools + loop" |
| 2 | A real run, step by step | 160 | `steps`: goal → tool call → observation → next step → stop; `chat`: the actual messages and tool results; `code`: the file it wrote; `table`: the prices it found with their pages |
| 3 | Where it fails: the numbers the makers publish | 90 | `stats`: OSWorld 2.0 scores as reported (Astra 72.6%, Opus 5.5 81.8% partial), Astra's ~40 minutes per task; `bullets`: the four common failure shapes (wrong page, stale data, half-finished, confidently wrong) |
| 4 | What "always-on" changes | 80 | `bullets`: acts while you are away, keeps state across chats, may hold its own identity (per what DevDay actually announced); `quote`: the official wording; `cta`: link to video 1 for the walls |
| 5 | Three questions before you hand it a task | 100 | `steps`: evidence / reach / cost of a wrong answer; `chat`: a bad delegation vs a good one for the same errand |
| 6 | Do this before your first agent task | 60 | `table`: the evidence checklist; `big`: "read the file, not the summary" |
| 7 | So is the chatbot over? | 40 | `outro`: "the chat is now the receipt, the work happens behind it; your job is to open the receipt"; next step: the Mokaair article on agent delegation, or the next video |

Total ≈ 600 s. Worked example: chapters 2–3.

### 選項 B：從 DevDay 開始講

Angle: news first (what was announced, what it costs, who gets it), then the explanation. Better if DevDay lands something big; risk of aging faster.

Hook: "OpenAI just announced an assistant that never logs off. Here's what it can do while you sleep, what it can't, and how to know the difference."

Chapters: What DevDay actually announced (90 s: `quote`, `table`) → How an agent works in five moves (120 s: `steps`, `chat`) → The failure rate nobody puts on the poster (90 s: `stats`) → A real run (120 s) → Three questions (90 s) → `outro` (40 s).

If DevDay announces nothing of the kind: the hook uses the September computer-use numbers instead, and chapter 4 becomes "what agents shipping this fall have in common".

## 會過期的事實

| Fact | Re-check at |
| --- | --- |
| What OpenAI announced on 2026-09-29, product name, pricing, availability | openai.com/index/devday-2026/ and the launch post; the "o" always-on agent was a leak until DevDay, never state it as fact from leaks |
| OSWorld 2.0 and time-per-task figures | openai.com/index/gpt-6-astra/ (403 to our fetcher on 2026-09-28; DataCamp's 2026-09-03 write-up carried 72.6% and ~40 minutes) and anthropic.com/news/claude-opus-5-5 (81.8% partial, 2026-09-22) |
| The prices the demo agent finds | each vendor's pricing page on writing day |
| Whether the CLI used in the demo still supports the same flags | its docs on writing day |

## 素材

- The agent transcript is the channel's own recording; nothing is invented and nothing is cut to make it look better.
- `quote` slides only for official wording; no product screenshots (interfaces change and are copyrighted).
- Mokaair article on delegating to agents if one exists on writing day; otherwise the closing points to video 1.

## 不做的事

- No claim that any agent "understands" or "wants"; no anthropomorphic language beyond quoting marketing and labelling it.
- No ranking of agent products; no purchase advice beyond the three questions.
- No reproduction of the OpenAI incidents in detail (video 1 has them).

