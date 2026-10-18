---
id: 2026-10-11-rewrite-meta-muse-marketplace-address-leak-settings
title: Tighten the explainer meta-muse-marketplace-address-leak-settings
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
  - docs/videos/meta-muse-marketplace-address-leak-settings
---

# Tighten the explainer meta-muse-marketplace-address-leak-settings

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `meta-muse-marketplace-address-leak-settings`, 「AI 代理幫你回二手買家，會把住址也講出去嗎？Meta Muse 事件與交出帳號前該拿掉的資料」.
- On the site: on YouTube, YouTube id `cLGsfZHe024` (already uploaded).
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked.
- The reader's reason: 事件經過與「住址是他自己交出去、又按了 Allow Always」這段機制值得看，但片名答應的「兩個設定」沒有任何工具的選項名稱與位置，第四章還岔去講 Muse Charm 等與住址無關的產品消息。
- What it needs, in the reader's words: 把第四章的 Muse Charm、Home Link、開源、零日漏洞刪掉，換成至少一兩個實際工具上「住址存在哪一欄、怎麼刪」與「送出前要我確認」選項的名稱與位置，並補上第三章「叫它不要說也擋不住」的實際例子（片中案例裡 Robb 根本沒禁止過）。這需要補查新的事實（實際設定頁或一次實測），另外刪減約二十句「據報導」與十來句比喻只需改寫。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: one exact thing to do, check or decide, in full on a card (A1). Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

not in the repository: on the host, `/opt/mokaair/docs/videos/meta-muse-marketplace-address-leak-settings/video.json` in the video-worker container. Copy it into `docs/videos/meta-muse-marketplace-address-leak-settings/` to rewrite it here.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.
- [ ] The owner decides what happens to the cut that is already on YouTube: a video's file
      cannot be replaced there, so a rewrite is a new upload.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Cut what repeats and add the one thing the reader says is missing.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug meta-muse-marketplace-address-leak-settings
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
