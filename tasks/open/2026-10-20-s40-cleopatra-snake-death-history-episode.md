---
id: 2026-10-20-s40-cleopatra-snake-death-history-episode
title: S40 Cleopatra snake death history episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-root
claimed_at: 2026-10-20T01:15:05Z
created_at: 2026-10-20T00:14:38Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s40
---

# S40 Cleopatra snake death history episode

## Why

Make a source-bounded Curio S40 about whether Cleopatra VII definitely died by a snake bite. The prior candidate memo had only Plutarch; this preproduction reopens him and adds Suetonius and Cassius Dio without treating any of the later authors as an eyewitness.

## Definition of done

- [x] Reopen fixed Plutarch full text and at least one separate ancient author; record versions and witness limits.
- [x] Draft two historically sound options, a 8+ minute story body, claims, shots and loop map, with lint at 0 errors and warnings.
- [x] Pass new independent script-only 13-question blind read and a separate source/prompt audit of exact script hash.
- [ ] Only after gates and whole-episode budget record, progress paid TTS, stills, music and final package.

## Steps

- [x] Pin full Plutarch, Suetonius and Dio translations with SHA-256 and passage scope in `research.md`.
- [x] Write `brief.md`, `video.json`, generated `script.md`, `claims.md`, and `verify-1.md` under `docs/videos/curio-s40`.
- [x] Resolve R1 blind (8/13) and source/prompt reviewer findings in R2, then regenerate and re-run local gates.
- [x] Receive fresh R2 script-only blind (10/13) and source/prompt audit; preserve reports and resolve cited issues in R3.
- [x] Receive fresh R3 script-only blind (12/13) and source/prompt audit (spoken and prompts 83/83; three claim pointers short); preserve reports and resolve cited issues in R4.
- [x] Fresh R4 blind 13/13 and source 83/83 passed; independent still audit identified five specific prompt blockers, preserved in [verify-r4-blind.md](../../docs/videos/curio-s40/verify-r4-blind.md) and [verify-r4-source-visual.md](../../docs/videos/curio-s40/verify-r4-source-visual.md).
- [x] Obtain independent focused check of the five repaired R4a prompts on exact new JSON hash before media.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s40 --json` reports 0 errors/0 warnings on R4a. The R4 blind/source evidence and R4a five-prompt repair are in `docs/videos/curio-s40/verify-5.md`; compare current exact JSON hash before accepting any focused recheck.

## Notes

R1 independent script-only blind 8/13 and source/prompt audit are preserved as `verify-r1-blind.md` and `verify-r1-source-visual.md`; R2 repair in `verify-2.md`. Fresh R2 blind 10/13 and source/prompt audit are preserved as `verify-r2-blind.md` and `verify-r2-source-visual.md`; R3 repair in `verify-3.md`. Fresh R3 blind 12/13 and source/prompt audit (83/83 narration and still prompts, three narrow citations) are preserved as `verify-r3-blind.md` and `verify-r3-source-visual.md`; R4 repair in `verify-4.md`. R4 `video.json` SHA-256 `6550826de8efd242c65af210ec6b6687f1da329ffe9e28684714394a0baaf6d2`: 84 spoken lines, 83 still shots + outro, estimated story body 8:32 and full length about 9:15, 25 loops, lint 0/0. Exact hash must be refreshed after any later edit. Sources and line-level qualification in `research.md`; do not convert `what really took place is known to no one` to a no-snake claim. No paid media. R4 blind/source results and R4a visual repairs follow below.

2026-10-20 01:19 UTC：獨立 R4 新讀者盲讀 **13/13**，固定全文來源 **83/83 句**通過，唯靜圖 `cl019,cl031,cl032,cl033,cl055` 含陵墓／宮殿混淆、虛構紙條和封口籃等五處不宜開畫。主代理認領後僅改這五個 prompt，解析 JSON diff 無其他變化；R4a video SHA `f4386a4f14882c5e169f7dabd14023c33beff770d3ac15fc46202246db4afec3`，script 與 claims 雜湊不變，lint 0/0。R4a 提示詞尚待獨立定點覆核，無付費媒體；詳 [verify-5.md](../../docs/videos/curio-s40/verify-5.md)。

2026-10-20 01:28 UTC：獨立 R4a 五景定點覆核 **PASS**，另外 78 景與全部旁白未動，lint 0/0；正式 `narrative --answers` 記錄 **13/13 PASS**。依站主持續授權，由主編代理登錄 A 大綱及劇本 exact-hash 本機 gate，並清楚標示非站主親自審閱。84 句 TTS 已啟動，故事正文實測、逐句音檢及圖／樂費用上限仍待完成；尚未開圖、配樂或上傳。見 [verify-6.md](../../docs/videos/curio-s40/verify-6.md)。

2026-10-20 02:04 UTC：R4a 84 句語音正文實測 8:22.77。初檢 22 旗標、兩輪定點重配後仍有 6 句；R4b 僅改 `cl023,cl024,cl045,cl049,cl064,cl075` 的口語與 claims，來源與 83 張提示詞不變。新獨立官方盲讀 **13/13**、六句固定原典定點覆核 **PASS**、lint 0/0；exact hashes、同音問題及下一輪音訊關卡見 [verify-7.md](../../docs/videos/curio-s40/verify-7.md)。未清零前不開圖；初報整集插圖加音樂上限 US$3.44，開畫前核實。

2026-10-20 02:13 UTC：R4b 重配後全片只剩 `cl075`「試救／施救」同音字旗標；再重配一次仍在。R4c 僅將稿、JSON、claims 改為來源同樣支持的「施救」。新獨立官方盲讀 **13/13**、狄奧 LI.14 定點來源覆核 **PASS**，84／84 文字、83 景提示詞不變，lint 0／0。現可本機核准 R4c，再只重配一行及全片音檢；詳 [verify-7.md](../../docs/videos/curio-s40/verify-7.md)。

2026-10-20 02:24 UTC：R4c exact-hash 劇本與旁白已依站主持續委託登錄本機核准（非站主親自試聽）；定點重配後全片 **84/84 句、音檢 0 旗標**。實際故事正文 **8:21.73**。83 張插圖最多三次的報價 **US$3.36**，549 秒配樂 **US$0.08**，整集圖樂上限 **US$3.44**；配樂已產生並實支 US$0.08，插圖尚未開畫。共享供應商時窗先留給 S04 修圖；後續逐張驗收與成片仍待完成。詳 [verify-7.md](../../docs/videos/curio-s40/verify-7.md)。

2026-10-20 02:28 UTC：網站音訊卡已 `review-push --gate audio` 提交、狀態 pending。供應商新時窗重置後開始 83 景 `keyframes --takes 2`，屬已記錄 US$3.44 整集圖樂上限內；尚須等生成完並逐張看圖，不能把請求中當成成片。

2026-10-20 03:40 UTC：首輪 83 張全尺寸審圖完成，機器 69 通過／14 `needs_review`，但另有 45 張機器通過圖帶現代或東亞服飾、燈具、家具等誤導性年代錯置。帳本共 119 次 image、117 次 judge，連配樂 US$1.6595／3.44。兩位審圖者交叉覆核 59 景的正面、來源安全修圖提示；僅改 `video.json` prompt，旁白 84/84、劇本與 claims 不動。新版 SHA `7bf3a70edcb09f8a74192511d1d33274c1a6dc82c2b9d62496921824aadc9b6f`；lint 0 錯誤／3 個為了防年代漂移而保留的重複年代詞警告。最終 JSON 的非 prompt 欄位與來源／年代定點覆核 **PASS**。**尚未重畫或合成**；S05 正用共用時窗，S40 待時窗後再在上限內正常重跑 `keyframes`，逐張驗收。詳 [verify-8.md](../../docs/videos/curio-s40/verify-8.md)。
