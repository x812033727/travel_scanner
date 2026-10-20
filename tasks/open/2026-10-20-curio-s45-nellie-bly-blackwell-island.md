---
id: 2026-10-20-curio-s45-nellie-bly-blackwell-island
title: Curio S45 Nellie Bly Blackwell Island source-audited episode
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T12:11:49Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s45
---

# Curio S45 Nellie Bly Blackwell Island source-audited episode

## Why

The next Curio history episode needs an original, source-audited topic with the requested condensed opening, series intro and 21-second outro. Nellie Bly's 1887 book offers a bounded first-person account, but the attractive shorthand about no examination, medically proven diagnoses, jury findings and a $1 million budget rise would overstate this one source.

## Definition of done

- [x] Fixed-version source and line-linked research document the correct Sept. 26 island transfer and allegation limits.
- [x] Brief offers two distinct chronological outlines and recommends the assignment-to-grand-jury arc, with site A/B approval honestly pending.
- [x] R8 candidate script, `video.json`, 99 scene-level claims, 18 resolved loops and 0 lint errors / 1 disclosed outro warning. At 300 spoken units/minute the opening is 40.40 seconds and the body is 8:19; actual TTS length is pending.
- [x] An independent R6 scene/source reviewer and two **new R6** narrative readers reviewed the exact frozen candidate. R6 source/written visuals PASS, R6 readers 12/13 and 13/13 without a shared required No. B's incidental description exposure and A's `no_recap` dissent are disclosed in `verify-10.md`. R5's independent source and written-visual review had held that earlier revision for lodging chronology, outdoor-walk prompt and visitor wording; R6 repaired these and explicitly pays off the Bellevue act question.
- [ ] R8 independent source/written-visual delta, two new narrative readers and one new categorized Jev policy verdict on R8 exact words; then local delegated outline/script gates, speech and picture approval, media, render, final QA and PR. R7 narrative failed; see `verify-13.md`.

## Steps

- [x] Read Curio and YouTube skills, series look, task rules and the fixed 1887 text.
- [x] Write `research.md` and `brief.md` in `docs/videos/curio-s45/`.
- [x] Draft and locally lint candidate episode files; truthfully push R6 outline/script cards to site, while preserving their pending status and doing no paid media.
- [ ] After R8 independent source/narrative and policy pass, resubmit changed outline and R8 script cards, record exact local delegated choices and start TTS.

## How to verify

`sha256sum /tmp/s45-bly-59899.txt` → `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`; source commit `c3904b5064d2bafb7e13486489dfe98b560611b5`. `node tools/video/cli.mjs lint --slug curio-s45` → 0 errors, 1 warning (R8 spoken outro omits subscribe request; visual CTA stays). `node tools/video/cli.mjs script --slug curio-s45` wrote the canonical script. Local consistency: 99/99 正文 scene lines match script and scene claims, with pinned line links; 96 shots + 3 cards; 18 valid loop pairs. Estimated body 9:42 at 250 spoken units/minute and 8:19 at 300; speech-only totals 10:29 and 8:59. Actual TTS remains unmeasured. The R8 delta and exact hashes are in `docs/videos/curio-s45/verify-14.md`. No paid media calls in this task stage.

## Notes

Site A/B and script approval are pending; the standing owner preference to adopt recommendations allowed a **local delegated A choice** for an earlier `brief.md` hash, not a fabricated site gate or an R8 hash approval. The source has the Sunday Sept. 25 Bellevue exam and Monday Sept. 26 island journey (chapter VII, lines 1365–1552). Chapter V explicitly describes physical examination. Chapter XVII is Bly's own account of the grand jury visit and result; no independent jury report was consulted. Do not assert her $1 million appropriation figure. No real TTS, image, music, Git staging, commit or push performed by this worker.

R1–R3 frozen file hashes and self-checks remain in `docs/videos/curio-s45/verify-1.md` through `verify-3.md`, R4's independent source PASS in `verify-5.md`, R5's source HOLD in `verify-7.md`, R6 repairs in `verify-8.md`, R6 independent source PASS in `verify-9.md`, R6 narrative PASS in `verify-10.md`, and R7 policy/site/author receipt in `verify-11.md`. Any script edit invalidates its narrative verdict and script gate hash.

R6 repaired `bly011–014` (back-parlor wait before room terms/payment), `bly017–020` (overnight care, morning coffee/bun, then police call), `bly080` outdoor-walk prompt, `bly035` visitor uncertainty and `bly031` direct Bellevue payoff. Keep 30 cents as one night's fee, about 70 cents as the amount carried before payment, and the second clean/new boat only on the grand-jury revisit. R7 changes only the last spoken outro line and the explanatory `claims.md` footer; the body remains R6.

2026-10-20 R6 的[新獨立來源／書面畫面差分](../../docs/videos/curio-s45/verify-9.md)在當時精確雜湊判 **PASS**；當時真正全新的兩名同版敘事讀者尚待審。R5 的讀者及站台狀態不能冒充 R6 結果；沒有付費媒體或完成影片。

2026-10-20 R6 [雙盲](../../docs/videos/curio-s45/verify-10.md) A 12/13、B 13/13，無共同必答 No，正式敘事 **PASS**；A 的 `bly062/064` 輕微重述異議與 B 曾看見影片說明欄的限制均保留。精確 R6 稿的史料／書面畫面也 PASS；政策、站台關卡、TTS 實測、插圖和成片仍未完成。

2026-10-20 R7 只改片尾 `bly999c` 口播以測試 R6 categorized Jev 的業配分數；R6 的 tutorial 與 categorized 兩次政策結果均 **FAIL**，詳[作者收據](../../docs/videos/curio-s45/verify-11.md)。另一位覆核者核對固定原著 URL 已在實際 YouTube 說明欄，判[精確 R7 來源／書面畫面差分 PASS](../../docs/videos/curio-s45/verify-12.md)。當時 R7 的新雙盲與政策結果仍待完成；網站 outline A／舊 R6 script 為 hand_pushed pending，無媒體支出。

2026-10-20 R7 [新雙盲](../../docs/videos/curio-s45/verify-13.md) A 11/13、B 11/13，兩人共同必答 `no_recap` No，正式敘事 **FAIL**；另有一人質疑片尾新問題未回收、另一人質疑 `bly055` 彈琴段。R8 只修這些敘事問題，重凍結後再審來源／畫面和雙盲，政策新呼叫及語音皆未做。

2026-10-20 R7 checkpoint: 初次 R6 政策請求在站台尚無 S45 row 時被誤當 tutorial，Jev 因示範 .12 判 FAIL；站台登記為 `explainer` 後，以同一精確 R6 請求重評，示範不適用，但業配 .35 > .30，仍 FAIL。兩份匿名回條、站台原樣 `hand_pushed pending` 的 A 大綱／舊 R6 劇本卡、R7 單句片尾中性化修訂和精確雜湊均在 [verify-11.md](../../docs/videos/curio-s45/verify-11.md)。R6 `tts --dry-run`：102 句、約 2,515 可計字元、Gemini Sulafat ready；**沒有實際合成**。站台 A 大綱和舊劇本卡均仍 pending，本地授權代理選 A 的 outline 雜湊註記因 R8 `brief.md` 改版而過期，**沒有站主站台核准**。

2026-10-20 R8 [作者來源差分與凍結收據](../../docs/videos/curio-s45/verify-14.md)：`bly055` 鋼琴支線改為飯後列隊等開門；`bly064` 直接說醫師吩咐添衣；`bly097→098` 回答陪審團是否支持她，同時限制為 Bly 的書中記述；片尾改成觀眾可以回答的證詞選擇題。`lint` 0 errors／1 片尾警告，99/99 對應、18 回收，估計主體 8:19。**下一工作者**先對 R8 精確雜湊做獨立來源與書面畫面差分，再請兩位全新隔離讀者評官方十三題；通過後才重送站台卡、記精確本地代理選擇及對 R8 新稿做一次分類正確的政策判讀。政策通過前不做付費語音／圖像；影片、Short、PR 均未完成。

2026-10-20 R8 [獨立來源及書面畫面差分](../../docs/videos/curio-s45/review/r8-source-independent.md) **PASS**：另一人重開 1887 固定版，逐項驗 `bly055/062–064/097–098/999b` 及相應提示詞，陪審團結論只歸 Bly 自述，不假裝已讀原報告。此 PASS 僅適用 R8 `script.md` SHA `6210aa1a85ca1e69ee01a3cfe9ce5a970336b262cdc3beb8cd1e944f1da1603e`／`video.json` `c3fa833ef6f60de7e3ef90e1fc7436d72add3c6a30d3756b6a97bfbaaa28d4ce`，雙盲敘事、政策與站台仍待；沒有付費媒體。
