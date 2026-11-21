---
id: 2026-11-20-localize-busan-3-day-itinerary-into
title: Localize busan-3-day-itinerary into en, ja, ko, zh-CN (Route B)
status: done
priority: P1
area: api
owner: antigravity
claimed_at: 2026-11-20T16:59:46Z
created_at: 2026-11-20T16:57:45Z
completed_at: 2026-11-20T18:02:56Z
branch: agy/localize-wave3c-busan-batch2
depends_on: []
scope:
  - apps/api/app/guides/content/busan-3-day-itinerary.json
  - apps/web/public/guides/busan-3-day-itinerary
---

# Localize busan-3-day-itinerary into en, ja, ko, zh-CN (Route B)

## Why

`busan-3-day-itinerary` (`kind: howto`) is a flagship high-intent South Korea itinerary guide that was previously published only in `zh-TW` (live v8, normalized `source_sha256: afde92628b0224e33c9b7a5a2b319b504b5cfdae17d23a9bf91c3a3d9123c21f`, matching repo bytes). Adding `en`, `ja`, `ko`, and `zh-CN` expands organic search and AI-answer visibility across four international locales as Wave 3C Batch 2 of the frontend exposure rescue program.

## Definition of done

- [x] All five locales (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) validate cleanly against `GuideDocument` with matching block structure (31 blocks, 13 sources) and localized 1600×900 SVG schematic area maps (`diagram-1-{en,ja,ko,zh-cn}.svg`).
- [x] `zh-TW` document and original assets (`hero.jpg`, `photo-1.webp`, `photo-2.webp`, `diagram-1.svg`) are byte-identical to baseline (`afde92628b0224e33c9b7a5a2b319b504b5cfdae17d23a9bf91c3a3d9123c21f`, zero deleted lines in `busan-3-day-itinerary.json`).
- [x] Every target locale underwent independent translation (`antigravity-translator-<loc>`) and separate independent text + rendered-SVG review (`antigravity-reviewer-<loc>`), with all findings fixed (`open_findings: 0`) and hash-bound in a validated `route-b-review-v1` receipt (`sha256: 8b2f250be512b5c097b6024963edc92f9e90024c1072771c46adb619b4df36fe`).
- [x] `zh-TW`-only cross-article references (`busan-dwaeji-gukbap-food-guide`, `busan-milmyeon-food-guide`, `busan-jeonpo-yeongdo-cafe-guide`, `daegu-2-day-itinerary`) are converted to plain prose or omitted per Route B policy, while destination and food-list links resolve to `/<locale>/destinations/busan` and `/<locale>/foods?city=busan`.
- [x] `pack_cli lint --slug busan-3-day-itinerary` exits 0 with zero errors; `pytest tests/test_guides_content_pack.py` and `translation_checks.py` pass cleanly.
- [x] Follow-up unclaimed release ticket filed with `depends_on` pointing to this task.

## Steps

- [x] Pin live `zh-TW` v8 document from `mokaair.com` and confirm `repo_hash == live_hash` (`afde9262…`).
- [x] Produce `en`, `ja`, `ko`, and `zh-CN` documents and localized 1600×900 SVGs via four separate translator subagents.
- [x] Render all four SVGs via headless Chromium and run four independent reviewer subagents.
- [x] Apply all reviewer text and SVG geometry fixes (terminology, stop-count parity between SVG and prose, Nampo↔Gamcheon arrow clearance, Gwangalli border clearance, `>= 15px` SVG typography), re-render, and visually inspect all four PNGs.
- [x] Validate `route-b-review-v1` receipt via `prepare_route_b_bundle.load_review`, merge into content pack, copy SVGs, and pass lint/tests/translation checks.
- [x] File unclaimed follow-up release task for host publication.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug busan-3-day-itinerary
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && PYTHONUTF8=1 uv run python ../../docs/news-2026-batch-4/translation_checks.py app/guides/content busan-3-day-itinerary
npm run check:tasks
```

## Notes

- **Pinned `zh-TW` source**: live version `8`, normalized `source_sha256`: `afde92628b0224e33c9b7a5a2b319b504b5cfdae17d23a9bf91c3a3d9123c21f`.
- **Localized documents & SVG assets**:
  - `en`: `3-Day Busan Itinerary: Haeundae & Gwangalli Night Views, Gamcheon, Nampo, Songdo Cable Car & Blueline Park` — `document_sha256`: `fe730d1622809868d0ef99db8a3604e4dfa6ef2cfb7a00cc9b703b59e9abd9c7`; `diagram-1-en.svg`: `5f094e57bf3bc17cef91559b093560636878aa933b7f7e00a5432ca09dac6785`
  - `ja`: `釜山2泊3日モデルコース：海雲台・広安里の夜景、甘川文化村・南浦洞、松島ケーブルカー＆ブルーラインパーク海岸列車` — `document_sha256`: `749917e4f0f1cff0851fc0276068c9dfdb4731b00ce06c6b3d59f21dcc46112c`; `diagram-1-ja.svg`: `7521bf6a190340716ef4d8204b91b9643d4be0a919fe9bb60fd01babe3496dd2`
  - `ko`: `부산 2박 3일 여행 코스: 해운대·광안리 야경, 감천문화마을·남포동, 송도해상케이블카와 해운대 블루라인파크` — `document_sha256`: `56d00e2185bcab02f8d78ed97ca1d88d6fcc9c7cf8b19d1f687a83dba0be81d7`; `diagram-1-ko.svg`: `e77a4cc17d0e78ddf2389b802a96959a3e30bbae5243c67b52a32c04e05c6a8a`
  - `zh-CN`: `釜山三天两夜行程参考：海云台广安里夜景、甘川洞南浦洞、松岛缆车与 Blueline Park 海岸列车` — `document_sha256`: `57f9d93356e4d59f21c87a38f8aa295565c8de2ea5d3c952cd575d2fdec70189`; `diagram-1-zh-cn.svg`: `f42ed3eb9b5a5cea463fe61a11a8baa563be180421debeeb68b93d81aca2dafc`
- **Independent review highlights**:
  - `en`: corrected `Gwangan Bridge` naming and faithful rendering of keeping luggage stationary across nights, echoed `Line 2, 16 stops` and `Line 1, 8 stops` in prose, widened Nampo↔Gamcheon gap (`60px`), pulled `청사포 Cheongsapo` label cleanly inside the canvas margin, and gave `Bus or Taxi` clear separation.
  - `ja`: echoed `2号線で広安・センタムシティ経由16駅` and `1号線で8駅` in prose and diagram description, fixed `利用状況`/`その後は`/`地下鉄に4回` phrasing, and widened Nampo↔Gamcheon gap (`75px`).
  - `ko`: fixed `요금` and `09:00–17:00예요` grammar, relocated `8정거장` from Toseong to the Nampo→Seomyeon segment for accuracy, and shifted Gwangalli + Haeundae→Gwangalli arrow endpoint cleanly clear of card borders.
  - `zh-CN`: removed unverified parenthetical `（利木津大巴）`, kept Gamcheon transit wording lodging-neutral while aligning `8 站` to Nampo→Seomyeon, changed `交通票券` to `交通通票`, widened Nampo↔Gamcheon gap (`75px`), and enlarged Day badges to `r="28"`.
- **Work artifacts**: kept outside the repository in the session's persistent scratch directory (`route-b-review-v1` receipt `sha256: 8b2f250be512b5c097b6024963edc92f9e90024c1072771c46adb619b4df36fe`, `evidence_sha256: f1c70e94b5f8be70773d5b8ee212584d5526f528ba0f146b3edc95ef38898f63`).
- **Lint warnings retained intentionally**: `no_summary` across all 5 locales and `text_length` on `en` (9,815 chars); per `article-localization` rules, source structure is preserved and translated prose is not trimmed to silence `text_length`.
