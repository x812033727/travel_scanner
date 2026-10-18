---
id: 2026-10-11-rewrite-google-vids-free-ai-video-omni-1-1
title: Rewrite the tutorial google-vids-free-ai-video-omni-1-1 from real runs
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/google-vids-free-ai-video-omni-1-1
---

# Rewrite the tutorial google-vids-free-ai-video-omni-1-1 from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `google-vids-free-ai-video-omni-1-1`, 「用 Google 帳號免費做 AI 影片：Google Vids 的 Gemini Omni 1.1 能做什麼、額度到底多少」.
- On the site: final video approved, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 8 of the 16 questions asked.
- The reader's reason: 整支只是把官方說明頁轉述一遍、沒有任何一次實際生成的結果，標題問的中文提示能不能用與額度到底多少，最後都叫觀眾自己登入看。
- What it needs, in the reader's words: 要用個人 Google 帳號實際跑一次，把中文提示能不能生成、登入後畫面顯示的額度是 6 還是 50、插進 Vid 與匯出的實際畫面和成品放上卡片，並把旁白裡四十多句「某頁寫」的出處句刪到只留卡片上的來源標示。這需要新的實測，不是只改寫就能補上。
- Kind of work: new runs, then a rewrite.

What it failed: more than ten narration sentences that hold without the subject (D2); the main result can be had the simple way with nothing lost (W2); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2). Also D3, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/google-vids-free-ai-video-omni-1-1/` on main.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
      For a tutorial that means real runs in the run log, the simple way run beside the
      subject on the same input, and no narration about the making.
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Make the missing runs on the owner's machine (the host worker runs nothing) and record them.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug google-vids-free-ai-video-omni-1-1
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
