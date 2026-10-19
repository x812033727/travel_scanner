---
id: 2026-10-18-dubs-and-cc-in-es-id
title: 種田娶妻 dubs and CC in es, id, pt, vi, th for episodes 1–5 and the 1–5 compilation
status: done
priority: P2
area: docs
owner: claude-opus-5.5-zt-five-dubs
claimed_at: 2026-10-18T14:49:14Z
created_at: 2026-10-18T14:48:24Z
completed_at: 2026-10-18T16:51:04Z
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.es.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.id.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.pt.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.vi.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.th.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub.sh
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub-lines.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/compile-dh.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-track.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-force.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/README.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/youtube-locales
  - docs/videos/zhong-tian-qu-qi-e001
  - docs/videos/zhong-tian-qu-qi-e002
  - docs/videos/zhong-tian-qu-qi-e003
  - docs/videos/zhong-tian-qu-qi-e004
  - docs/videos/zhong-tian-qu-qi-e005
---

# 種田娶妻 dubs and CC in es, id, pt, vi, th for episodes 1–5 and the 1–5 compilation

## Why

Owner 2026-10-18: to reach viewers outside the zh/en/ja/ko audiences, add Spanish (Latin
America), Indonesian, Brazilian Portuguese, Vietnamese and Thai to 種田娶妻打天下 — dubs, CC
and translated YouTube titles and descriptions. Start with episodes 1–5 and the 第1–5集
compilation (the first YouTube upload), measure, then decide on the rest.

## Definition of done

- [x] Episodes 1–5 have `dub.<locale>.json` for es, id, pt, vi, th, recorded and fitted.
- [x] Each episode's import folder has `dub.<locale>.m4a` and `<locale>.srt` for the five.
- [x] The 第1–5集 compilation has one dub track and one CC file per locale (all eight
      foreign locales), as long as the compilation.
- [x] Translated title and description per locale for the compilation and the five episodes.

## Steps

- [x] dub-lines.mjs and dub.sh accept the five locales (script check, speaking rate, ISO tags).
- [x] dub-glossary.json gets lead, direction and names for the five.
- [x] Translate, record and fit e001–e005.
- [x] compile-dh.mjs builds per-locale dub tracks and CC for a compilation.
- [x] Titles and descriptions.

## How to verify

`CHECK=1 local/dub.sh 001 es` passes; `local/dub.sh 00N <locale>` writes the m4a with the
zh cut's length and about the same loudness; the compilation's tracks match its length.

## Notes

Only episodes the owner has checked get dubbed (e1–24 were checked 10-18).

2026-10-18 (claude-opus-5.5-zt-five-dubs): one agent per locale translated, recorded and fitted
e001–e005; every track equals the zh audio length, loudness within 1 LU of zh.
- Names: Mandarin pinyin for es/pt/id; vi uses Hán-Việt (Hứa Nghiên, Tần Sương, A Lệnh, Đường
  Tiểu Đường), th uses Thai transliteration of Mandarin (สวี่เยี่ยน, ฉินซวง, อาลิ่ง). All merged into
  dub-glossary.json; extra terms per locale in dub-glossary-additions.<locale>.json.
- Series titles: es «Siembra, cásate y conquista», pt «Plantar, Casar e Conquistar», id «Bertani,
  Beristri, Berkuasa», vi «Làm Ruộng Cưới Vợ Đoạt Thiên Hạ», th «ทะลุมิติไปทำนา ได้เมีย ครองแผ่นดิน».
  The CC word in titles is the local search term (Sub Indo, Vietsub, ซับไทย, Legendado).
- The Gemini voices act these lines slower than the narration rates in plan.mjs: measured medians
  es 10.7, pt 9.5, id 10.9, vi 13.2, th 11.9 characters/s (en measured 11.6 against its 15). The
  new locales' RATE in dub-lines.mjs now uses them, so `long?` warns about real misfits.
- Directions with acted sounds (笑, 陪笑, 憨笑, 嗆咳, 打呵欠, 哀號) add 0.5–1 s to a take. Two es
  lines lose only a trailing laugh when cut: listed in dub-force.json with the three ko lines
  the 10-18 ko pass forced, so a rebuild or compilation needs no FORCE=1.
- About 20–30 lines per locale use `{text, say}`: the voice says a short version, the CC keeps
  the full meaning.
- Nobody has listened to the new takes. Worth a listen: lines that ran 2–3× their estimate (the
  System's word-by-word lines, Squire Qian's drawl, Erniu's laughing lines).
- dub.sh now takes a per-episode lock directory (<workdir>/.dub-lock) before assembling, and
  compile-dh.mjs takes the same lock per part: assemble-v4 rewrites segments-v4/lines each run.
- The compilation (e001-005) has en/ja/ko/es/pt/id/vi/th tracks, 438.064 s decoded like the
  picture (each part padded to its picture length, as the zh concat places parts), 198 cues each,
  −14.0 to −14.5 LUFS; copied with descriptions into the import folder `zhong-tian-qu-qi-e001-005`.
