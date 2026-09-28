---
id: 2026-09-28-produce-video-06-why-openai-killed
title: Produce video 06: why OpenAI killed Sora, and what AI video costs per second now
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-28T10:08:50Z
created_at: 2026-09-28T10:08:25Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/why-openai-killed-sora
---

# Produce video 06: why OpenAI killed Sora, and what AI video costs per second now

## Why

Season video 6 (`docs/ai-video-en-season-01/README.md`, brief `briefs/06-why-openai-killed-sora.md`): OpenAI closed the Sora app on 4/26 and the API on 9/24. The worked example is a cost-per-second-of-video table from each video model's official price page today. zh-TW master with five-language CC and en/ja/ko dubs, like videos 1–4.

## Definition of done

- [ ] `brief.md` in zh-TW with the eight sections and 2–3 outline options; the owner picked one on the outline gate.
- [ ] Script written, verified twice, listener-reviewed; zh-TW narration recorded and checked (Whisper for any flag); no slide state over 15 s.
- [ ] CC in zh-TW, zh-CN, ja, ko, en (each reviewed by a second model); dubs en, ja, ko recorded `--line-by-line` and fitted.
- [ ] Final, publish and dubs gates approved; the owner uploads private; `scoreboard.csv` rows filled.

## Steps

- [x] Planner writes `docs/videos/why-openai-killed-sora/brief.md` from the season brief, re-reading every changeable fact on its official page.
- [x] `review-push --gate outline`; then writer, two verifiers, listener review.
- [ ] Narration and dubs. They were to wait for the Gemini month to reset on 2026-10-01 (8,106 characters left on
      2026-09-28), but the site's Gemini limit went from 300,000 to 2,000,000 and then 5,000,000 characters a month
      around 15:00 UTC on 2026-09-28, so narration started the same day.

## How to verify

```bash
node tools/video/cli.mjs lint --slug why-openai-killed-sora
node tools/video/cli.mjs status --slug why-openai-killed-sora --workdir <VIDEO_WORKDIR>
```

## Notes

- The owner asked on 2026-09-28 to keep planning after the first three were packaged (「繼續計畫別的」).
- Schedule slot: 2026-11-10 15:00 UTC in `schedule.csv`.
- 2026-09-28: brief written (three outlines, A recommended) and sent for the owner's pick as outline review `a8064605-7786-4917-8ed5-ac099e02174a`. `review-push` needs a video.json, so the outline went up through the automation client's calls instead (report, judge — the stance is blank, so it waits for the owner — then submit), the same steps `flow.mjs` `submitOutline` takes.
- 2026-09-28 10:57 UTC: the owner picked outline A (recorded by `review-pull`; bound to brief.md's hash, so the brief is frozen). Writer dispatched with the season's lessons (pace, `say` for versions/years/percents, date-proof wording, dictionary additions through a locked append script).
- 2026-09-28 evening: script done and final before narration. Writer (outline A, ~8.6 min, 30 scenes, 7 chapters); fact-check round 1 (83 claims, 5 fact changes: the title says 官方公告 gave one reason because OpenAI told CBS more the same day, Sora 2's $0.10 is the Standard tier, the "no other explanation" line dropped, the 8x gap is between models) and round 2 (65 claims, 2 changes: the $0.05–$0.40 range is 720p only, the final export is conditional); listener pass (reveals, the owner's 並不貴 marked, voice-safe `say`); translations en, ja, ko, zh-CN, each reviewed by a second model and fixed (ja fitted with a duration model from the season's real Japanese clips). After the reviews ux5y also states Seedance 2.0's 4–15 s. Next, after the Gemini month resets on 2026-10-01: `tts` → `check-audio` (Whisper for flags) → audio gate → render → assemble → dubs `--line-by-line` → captions → qa → final.
- 2026-09-28 15:00–15:30 UTC: narration recorded early after the Gemini limit was raised (see Steps). A site outage (「API 服務目前無法回應」) stopped the first `tts` run after 17 of 30 requests; the re-run reused them and synthesized the other 13 (1,680 characters; narration 08:22). `check-audio`: 101 lines, 71 word for word, 20 same-sound, 1 judged fine by Jev, 9 flagged. Local Whisper (large-v3) heard 46dv, uxum, ux5y and 7pcx as written, so Gemini misheard them (Veo 三點一 as 算便宜, 自家 as 這家). r7yj only gained a spoken 啊, so it stays. Both transcribers agreed that four clips were off: wcet said 這八秒 for 一支八秒, iysq sounded like 一至八秒, nfcf like 契約頁, and hc3t like 描述 for 秒數. The same words pass in itjj and iayh, so these four were retaken as written first (`review/retake-1.json`), with `say` held back in case a retake fails.
- 2026-09-28 15:30–17:10 UTC: narration re-checked after the retakes. Local Whisper agreed with Gemini that four clips were off (一支八秒 → 一至八秒, 秒數 → 描述, 棄用頁 → 契約頁). A retake as written fixed nfcf. wcet, iysq and hc3t now say 一段八秒 and 長度 through `say`, with the captions unchanged. The owner approved the audio at 15:48. Dubs `--line-by-line`: en, ja and ko each needed a few lines trimmed to fit (en 32i6; ja ufsf, 5n89, pnnk, m6en, ctak; ko pnnk). `check-audio --locale` flagged en 8, ja 20 and ko 14 lines, and Whisper large-v3 decided each. Real misreads were fixed and retaken: en na3m (Kling 3.0); ja ctak (0.14秒 → ドル written back), whhz (停止 → 打ち切り), abiv (多社 → 複数社) and 2bmt/xvcc/7crj retaken; ko u9xn (포함끼리 → 포함 기준) and r26r (대체를 정하지). ja qm8a's 廃止ページ was heard as 配置 twice. The same term reads fine in iayh and gxbt, so it stays. QA 9 of 11: links fails because web.archive.org is blocked by this environment's egress proxy and The Verge and Business Insider refuse the checker (both return 200 to curl with our UA); policy fails because the channel stance is blank. Final submitted for the owner's review at about 17:05.
