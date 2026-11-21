---
id: 2026-11-20-localize-japan-shinkansen-ticket-guide-into
title: Localize japan-shinkansen-ticket-guide into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-20T16:09:41Z
created_at: 2026-11-20T16:09:17Z
completed_at: 2026-11-20T16:51:15Z
branch: agy/localize-wave3c-airports-batch1
depends_on: []
scope:
  - apps/api/app/guides/content/japan-shinkansen-ticket-guide.json
  - apps/web/public/guides/japan-shinkansen-ticket-guide
---

# Localize japan-shinkansen-ticket-guide into en, ja, ko, zh-CN (Route B)

## Why

`japan-shinkansen-ticket-guide` (`kind: howto`) is a flagship high-intent Japan transit guide that was previously published only in `zh-TW` (live v10, normalized `source_sha256: e785b0d683a434305a1c3cdf7d040bd4edaecae9ab4a1cebfddc6bea5a1d0814`, matching repo bytes). Adding `en`, `ja`, `ko`, and `zh-CN` expands organic search and AI-answer visibility across four international locales as Wave 3C Batch 1 of the frontend exposure rescue program.

## Definition of done

- [x] All five locales (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) validate cleanly against `GuideDocument` with matching block structure (31 blocks, 19 sources) and localized SVG decision tree (`diagram-1-{en,ja,ko,zh-cn}.svg`).
- [x] `zh-TW` document and original assets (`hero.jpg`, `photo-1.webp`, `photo-2.webp`, `diagram-1.svg`) are byte-identical to baseline (`e785b0d683a434305a1c3cdf7d040bd4edaecae9ab4a1cebfddc6bea5a1d0814`, zero deleted lines in `zh-TW`).
- [x] Every target locale underwent independent translation (`antigravity-translator-<loc>`) and separate independent text + rendered-SVG review (`antigravity-reviewer-<loc>`), with all findings fixed (`open_findings: 0`) and hash-bound in a validated `route-b-review-v1` receipt (`sha256: 86d575a74047e620c007f65ab3213c2db1bb0cea6ae3aa1e7629b20479901272`).
- [x] Internal article links use exact verbatim published titles for target locales (`tokyo-transit-passes`, `kansai-airport-to-osaka-kyoto`), and `zh-TW`-only articles (`kanazawa-2-day-itinerary`, `sendai-airport-access-loople-bus-guide`) are omitted per Route B policy.
- [x] `pack_cli lint --slug japan-shinkansen-ticket-guide` exits 0 with zero errors; `pytest tests/test_guides_content_pack.py` and `translation_checks.py` pass cleanly.
- [x] Follow-up unclaimed release ticket filed with `depends_on` pointing to this task.

## Steps

- [x] Pin live `zh-TW` v10 document from `mokaair.com` and confirm `repo_hash == live_hash` (`e785b0d6…`).
- [x] Produce `en`, `ja`, `ko`, and `zh-CN` documents and localized 1600×900 SVGs via four separate translator subagents.
- [x] Render all four SVGs via headless Chromium and run four independent reviewer subagents.
- [x] Apply all reviewer fixes (terminology, Taiwan-only phrasing removal in `ko`, arrowhead/border clearance, `>= 15px` SVG font sizes, and cutoff-time parity with body prose), re-render, and visually inspect all four PNGs.
- [x] Validate `route-b-review-v1` receipt via `prepare_route_b_bundle.load_review`, merge into content pack, copy SVGs, and pass lint/tests/translation checks.
- [x] File unclaimed follow-up release task for host publication.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug japan-shinkansen-ticket-guide
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content japan-shinkansen-ticket-guide
npm run check:tasks
```

## Notes

- **Pinned `zh-TW` source**: live version `10`, normalized `source_sha256`: `e785b0d683a434305a1c3cdf7d040bd4edaecae9ab4a1cebfddc6bea5a1d0814`.
- **Localized documents & SVG assets**:
  - `en`: `How to Buy Shinkansen Tickets: smartEX, EX Hayatoku 21, Station Ticket Machines, and When the JR Pass Pays Off (2026)` — `document_sha256`: `21a6b40604c1017b5eaa417d9f52a86a01001eab1a8408f68e617795f9d1d305`; `diagram-1-en.svg`: `b3a051fc3e4dd906af1ad1734cf943e872f59ed4f97b77ad1d5c92e3bde81440`
  - `ja`: `新幹線のきっぷ購入ガイド：スマートEX、EX早特21、駅の券売機、JR Passがお得になる条件（2026年版）` — `document_sha256`: `64ad592439186a861af742c576ff52c9a73bae51d753d9d54695f8feb53effed`; `diagram-1-ja.svg`: `f94f88c6e3ea18dc62d61c4090085ab3a59f0c2373760423b0825a6a58969f4e`
  - `ko`: `신칸센 티켓 구매법: smartEX, EX 하야토쿠 21, 역 발매기, JR Pass는 언제 이득일까?(2026년판)` — `document_sha256`: `b3a7004f27d95444630c44e3adb8f37c63dbadbd396661e8e333538548c2e210`; `diagram-1-ko.svg`: `c3730545209349ef112b70738563f5dd5251ba8f75fc0a365a1494feed72baf3`
  - `zh-CN`: `新干线车票怎么买：smartEX、EX早特21、车站售票机，JR Pass 什么时候才划算（2026 年版）` — `document_sha256`: `d1fd644bd5d034a9c125bdc84b8a2e2f47d30baf47bbbe1c7cd821bf1a476738`; `diagram-1-zh-cn.svg`: `04126b255d0f7db3b926b34ae68a589b4331e847ac9501851fb1ccc4b97e9567`
- **Independent review highlights**:
  - `en`: clarified `¥320 refund fee`, idiomatic prose polish, aligned cutoff time (`11:30 PM`) between SVG and prose, widened side cards for `>= 15px` labels.
  - `ja`: resolved arrowhead label collisions on `はい`/`いいえ`, tightened cross-line seasonal doubling wording (`3路線`), unified footer reference.
  - `ko`: removed Taiwan-only reader framing (`대만에서` → `출발 전에` / `사용 중인 국가·지역에서`), fixed `아니요` border clipping, aligned `23시 30분` across SVG/description/prose, disambiguated `승차권` vs `추가권`.
  - `zh-CN`: unified diamond/arrow/card geometry so all three right-side cards align cleanly with zero border contact, fixed Taiwanisms (`机台` → `售票机`), aligned `指定席选座免费`.
- **Work artifacts**: kept outside the repository in the session's persistent scratch directory (`route-b-review-v1` receipt `sha256: 86d575a74047e620c007f65ab3213c2db1bb0cea6ae3aa1e7629b20479901272`).
- **Lint warnings retained intentionally**: `no_summary` across all 5 locales and `text_length` on `en` (9,790 chars); per `article-localization` rules, source structure is preserved and translated prose is not trimmed to silence `text_length`.
