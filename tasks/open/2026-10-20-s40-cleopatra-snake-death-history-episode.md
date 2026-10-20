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

2026-10-20 04:04 UTC：另一輪獨立全尺寸審視 verify-8 暫留的 24 景，又確認其中 12 景有誤導性的年代、人物年齡、道具或虛構證據圖，故暫留實為 12 景。只補改 `cl001,cl020,cl022,cl026,cl037,cl049,cl055,cl061,cl064,cl068,cl069,cl071` 的正面提示詞；連前輪共 71／83 景待重畫，旁白及史料不動。最新 `video.json` SHA `5f0897aeb2a6ff7d9b36e79cf9387bfb5084563c70ba625b5329a7fd94030c27`；獨立 exact-hash prompt/source/period/diff 覆核 PASS，lint 0 錯誤／3 年代錨點警告。帳本仍 US$1.6595／3.44、無未結預留。先用 `keyframes --takes 1`，其後按全尺寸結果與帳本在上限內定點補畫；S05 未釋出圖片時窗前 **不送出付費圖**。詳 [verify-9.md](../../docs/videos/curio-s40/verify-9.md)。

2026-10-20 04:46 UTC：共享窗口釋出後 S40 `keyframes --takes 1` 先畫 20 景，到 `cl026` 用專案 STOP 正常暫停，manifest 32 景、帳本 US$1.9295／3.44、預留 0。逐鏡盤點查出 31 景把歷史真名送到 MiniMax，依系列 skill 改為身份、服飾、年代與動作描述；另修有明確事實錯置或評審未過的無花果、密封信、陵門、兩人抬安東尼、凱旋示意像等。初步把 12 張保留圖全判重畫的尺度過嚴；依系列可愛插畫規則獨立重判為只退 `cl006` 的嬰兒比例安東尼，其他 11 張留。最終 **36／83 處 prompt-only**、`video.json` SHA `223bfdc30b72b3929a97a4e1a574bb0788c3c1bb666c7ada28d43b8aefd0984e`，獨立來源／年代／人名／diff 全 83 景 **PASS**；劇本／claims／音訊不變，lint 0 錯誤／3 重複身份錨點警告。續畫 67 對圖片與評審最壞累計 US$2.834，S40 STOP 仍在，待 S05 定點補圖結束並重算供應商近 60 分鐘請求後接續。詳 [verify-10.md](../../docs/videos/curio-s40/verify-10.md)。

2026-10-20 05:18 UTC：S40 在共享 MiniMax rolling60 約 112 次時有限接續 `keyframes --takes 1`；新增 22 張成功圖與 `cl001/038` 兩次跨景 ReadTimeout（失敗各 US$0），依 root 指示以 STOP 正常停於 `cl040`，manifest SHA `b0f869124f1d8f931c650a55b27af4f8209b1a98175feedca9457542a5096530`，US$2.2265／3.44、預留 0。前40景原尺寸重判 27 KEEP、11 史實/身份/動作 HARD、2 timeout MISSING；不因 chibi 比例重買。HARD 11 景只改 prompt，特別 cl022 改受威脅後恢復進食、cl028 禮盒仍留女王身旁；最終 `video.json` SHA `2523d67d174b416a89eb9831c207ff76199e92c85fb4529bf9e91928101d18a8`，獨立全83 exact-hash source/period/diff **PASS**，lint 0 error/3 錨點警告。S40 STOP 持續等 S05 尾輪完畢並重算共享 rate/budget 後才續首輪；圖像全景、分鏡、成片與上架包尚待完成。詳 [verify-11.md](../../docs/videos/curio-s40/verify-11.md)。

2026-10-20 約 07:00 UTC：後續正規補圖與來源卡後，現行 `video.json` SHA `6621acfa126abd87f4b303e59d2e2a0b83736b3d1379d9965e3bece583d4c359`、入選 manifest `531295a9c1d20f7b5c8d54103fa59bb9c408bfc41ea0ce66f6714f2d631d32a2`；84 句旁白未變，script-only 獨立盲讀 13/13，lint 0 error／3 重複身份錨警告。**60/83 插圖、最長三連卡**；五景機評未過 `cl005,017,027,051,070`，另 `cl050,062` 機評雖過但原尺寸與死亡狀態／年代服飾矛盾。帳本 **US$3.3875／US$3.44**、無預留；只容再一張卡，而六次最便宜的快取評審也要 US$0.06，超過 US$0.0525 餘額。已停止 S40 付費、釋出圖片窗口給 S26；不推 storyboard、不宣稱成片。七景逐項、被排除 donor、精確來源與恢復條件見 [verify-12.md](../../docs/videos/curio-s40/verify-12.md)。

2026-10-20 約 07:55 UTC：找到不用增加卡片比例或提高預算的**條件式**修法：把五組相鄰史料卡各合併成一景，保留 84 句核准旁白的 ID／順序／WAV，再把五個不合格插圖景改成有精確來源的卡片；僅 `cl062,070` 待重畫。獨立來源與卡片節奏覆核 PASS、官方 lint 0 errors／3 舊警告；現行 `video.json` SHA `4dc025b856c1124c6e5972d7d18c183b7e5bd9b08b944733208b3105eb813f8c`，正文 **55/78 插圖＝70.51%**、最多三連卡，最長卡片狀態 14.3 秒。帳簿仍 US$3.3875／3.44、無預留；先跑 exact cache-aware dry-run，確認只需兩次標準圖加評審，兩次約 US$0.027。新版三連卡死亡揭曉須再經獨立敘事盲讀；未過不得付費或推 storyboard。詳 [verify-13.md](../../docs/videos/curio-s40/verify-13.md)。
