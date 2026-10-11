---
id: 2026-10-11-rewrite-meta-anti-scam-2fa-passkey
title: Rewrite the tutorial meta-anti-scam-2fa-passkey from real runs
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
  - docs/videos/meta-anti-scam-2fa-passkey
---

# Rewrite the tutorial meta-anti-scam-2fa-passkey from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `meta-anti-scam-2fa-passkey`, 「臉書、IG 帳號被盜之前：Meta 防詐騙活動要你開的兩個設定，雙重驗證和通行金鑰」.
- On the site: on YouTube, YouTube id `_v1vc2s3_MU` (already uploaded).
- Read as a tutorial. Verdict: rework. Failed 10 of the 16 questions asked. A second reader: rework, 8 failed.
- The reader's reason: 影片說要一步步帶人開兩個設定，卻沒有任何一張真實畫面，步驟寫到「照畫面指示完成」「同一區裡找找看」就停，觀眾自己打開設定搜尋「雙重驗證」就能得到一樣的結果。
- What it needs, in the reader's words: 要在真實帳號上把雙重驗證和通行金鑰各走一遍，放上帶日期與 App 版本的畫面、每個選項的實際名稱、驗證 App 和簡訊該怎麼選、備用碼與登入裝置在哪裡，並把活動的市場數與觸及人數連同出處放上卡片。這需要新的實測和新的事實，不是只改稿；同時刪掉重複的「碼不給人」和「以官網為準」。
- Kind of work: new runs, then a rewrite.

What it failed: an observed result or sourced fact the viewer would not have predicted (W5); the main result can be had the simple way with nothing lost (W2); the content of the thing taught is on screen (W3); the viewer could make or change one from what is shown (W4); a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2). Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/meta-anti-scam-2fa-passkey/video.json` in the video-worker container. Copy it into `docs/videos/meta-anti-scam-2fa-passkey/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug meta-anti-scam-2fa-passkey
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
