---
id: 2026-10-11-rewrite-supabase-rls-anon-key-check-hands-on
title: Rewrite the tutorial supabase-rls-anon-key-check-hands-on from real runs
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/supabase-rls-anon-key-check-hands-on
---

# Rewrite the tutorial supabase-rls-anon-key-check-hands-on from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `supabase-rls-anon-key-check-hands-on`, 「AI 幫你做的 App，資料庫鎖了嗎？Supabase RLS 實作教學：一行請求查外露，再鎖起來」.
- On the site: retrying, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 6 of the 16 questions asked. A second reader: rework, 6 failed.
- The reader's reason: 標題寫「實作」，但四次請求的回傳全部是「預期・未實測」，觀眾拿到的是整理過的官方文件，而不是跑出來的結果。
- What it needs, in the reader's words: 需要新的執行紀錄，不只是改寫：把四次請求在本機實際跑一遍，換成帶日期與版本的真實回傳並填滿「實際」欄。同時補上啟動本機 Supabase、建立測試使用者、把 user_id 寫進三列、取得 token 的完整指令，並刪掉「沒有跑過」這類交代製作的旁白。
- Kind of work: new runs, then a rewrite.
- Paused on the host: a `STOP` file another session placed on 2026-10-10 is in its work folder, and on 2026-10-11 the owner decided it stays paused, so the worker pays for nothing more. Remove it only when the rewrite is ready to be produced.

What it failed: a choosing rule tied to an observed result (W6); the main result is the output of a real run (E1); every step to repeat is on a card in full (E2); the example can be followed without an unseen download (E3). Also D3, S1, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/supabase-rls-anon-key-check-hands-on/video.json` in the video-worker container. Copy it into `docs/videos/supabase-rls-anon-key-check-hands-on/` to rewrite it here.

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
node tools/video/cli.mjs lint --slug supabase-rls-anon-key-check-hands-on
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
