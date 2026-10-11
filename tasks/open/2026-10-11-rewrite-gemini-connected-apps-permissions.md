---
id: 2026-10-11-rewrite-gemini-connected-apps-permissions
title: Rewrite the tutorial gemini-connected-apps-permissions from real runs
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:49:18Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/gemini-connected-apps-permissions
---

# Rewrite the tutorial gemini-connected-apps-permissions from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `gemini-connected-apps-permissions`, 「Gemini 能直接叫出 Adobe、Airtable？Connected Apps 怎麼連、連了等於給它什麼」.
- On the site: on YouTube, YouTube id `U4ToEihqiJA` (already uploaded).
- Read as a tutorial. Verdict: rework. Failed 12 of the 16 questions asked.
- The reader's reason: 片名答應讓觀眾看懂「給了它什麼權限」，但全片沒有任何一個真實的授權畫面、權限範圍或設定名稱，示範對話是示意，台灣能不能用也只回「以官網為準」，剩下的大多是任何 App 都適用的一般提醒。
- What it needs, in the reader's words: 需要新的實測：用真實帳號連一到兩個應用程式，把實際授權畫面列出的讀取與寫入範圍、台灣介面的設定名稱與路徑、斷開後的結果，以及台灣帳號到底看不看得到，放上卡片。有了這些再刪掉約三十句通用提醒與「以官網為準」的句子，只改寫不夠。
- Kind of work: new runs, then a rewrite.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); the title's question answered with a specific answer (T1); more than ten narration sentences that hold without the subject (D2); the main result can be had the simple way with nothing lost (W2); the content of the thing taught is on screen (W3); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/gemini-connected-apps-permissions/video.json` in the video-worker container. Copy it into `docs/videos/gemini-connected-apps-permissions/` to rewrite it here.

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
- [ ] The owner decides what happens to the cut that is already on YouTube: a video's file
      cannot be replaced there, so a rewrite is a new upload.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Make the missing runs on the owner's machine (the host worker runs nothing) and record them.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug gemini-connected-apps-permissions
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
