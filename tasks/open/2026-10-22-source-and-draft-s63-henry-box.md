---
id: 2026-10-22-source-and-draft-s63-henry-box
title: Source and draft S63 Henry Box Brown escape episode
status: in-progress
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-22T12:49:01Z
created_at: 2026-10-22T02:07:54Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s63
---

# Source and draft S63 Henry Box Brown escape episode

## Why

The owner wants more distinct Curio history films with a complete long and Short package, animated condensed opener/intro/outro, and honest end links. Henry Box Brown's box escape can form a single source-led investigation, but its familiar 27-hour and exact-date claims are frequently told without identifying who said them. This task pins the Brown/Stearns account, whose quoted title page has no printed year, then writes a script that keeps Brown's own decisions and his continued insecurity central.

## Definition of done

- [x] A distinct A/B outline and recommended single story have an independently feasible pinned primary source, explicit 1848 family-separation versus undated-escape boundary, and full media/end-link plan.
- [x] A script/storyboard and one-to-one line/source/visual map carry a 30–60 second condensed opener, at least eight minutes of body even at 325 Chinese units per minute, the fixed 5-second intro/21-second outro, and no fabricated upload or paid-media receipts.
- [x] Frozen author hashes pass the Curio video lint; separate source/visual and fresh official dual-blind narrative audits pass on the same R8 freeze before any paid media.
- [ ] Produce and verify narration, original artwork, music, animated long film, subtitles, Short and actual upload package with honest links; keep owner and media review gates bound to the final files.

## Steps

- [x] Search existing S01–S62 briefs/topic catalog/tasks for Brown overlap and claim a narrow S63 scope.
- [x] Pin the GITenberg Brown/Stearns source by commit and raw SHA; distinguish Brown-mediated narrative from Stearns and Samuel May appended voices.
- [x] Draft source boundaries and A/B outline, including website owner versus local delegated decisions, Shorts and Studio links.
- [x] Independent feasibility receipt, frozen script/storyboard, claims, script export, lint and docs/task check; R3 source/visual audit passed 127/127 lines.
- [x] R8 exact hashes receive an independent source/visual PASS and fresh official dual-blind narrative PASS, with raw ballots and official isolated CLI replay retained.

## How to verify

From this branch worktree:

```bash
sha256sum /tmp/curio-s63-box-brown-1849.txt
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s63 --json
node tools/tasks.mjs check
git diff --check
```

The fixed raw text must hash to `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2`. The `/tmp` file is disposable source cache, not a committed asset.

Frozen preproduction hashes after R3 source/visual PASS: `video.json` `00cb544ad03d325f8eb666c3d037bf8a0aa3df1026c5c528ae54749a7d8e5090`; `script.md` `557427e904b22b40e8f326f9acd7947950c507c089ee6cee5dd4ea5be68dc37d`; `claims.md` `d1548e7232d4660da2518fac718dc1c00d45878a873d1ef90054e41f63769ee7`. The independent [R3 receipt](../../docs/videos/curio-s63/review/r3-source-visual-independent.md) counts 2,686 story-body Han characters excluding the CTA, or 8.26 minutes at 325 CPM, and a 168-character opener, about 31 seconds. `lint` reported 0 errors/0 warnings; docs-video tests passed 236/236. The subsequent formal blind result is recorded below; no paid media has been started.

## R3 official blind HOLD (2026-10-22 UTC)

Two fresh readers each received only the same frozen R3 narration and 13 official questions. Their separate source ballots and CLI receipts are under `docs/videos/curio-s63/review/r3-isolated-blind-{a,b}.*`. The [formal OR merge](../../docs/videos/curio-s63/review/r3-formal-merge-audit.md) is **11/13 HOLD**: both readers answered No on `no_spoiler` (`s63009`) and `no_recap` (different repetitions at `s63015` and `s63029`); B alone marked `no_detour` at `s63016`. The official CLI replay exited 1 with exactly the two shared required failures. R3 script and source/visual PASS remain archived for their frozen hashes, but the episode cannot enter paid media. The author then made the narrow R4 revision recorded below; it needs fresh independent checks.

## R4 author repair and source review (2026-10-22 UTC)

The [R4 author repair](../../docs/videos/curio-s63/review/r4-author-repair.md) changes only seven scene IDs to keep the box exit and Northern speech unresolved in the opener, remove duplicate age and household income facts, and replace the factory number list with Brown's work and ability to leave. Frozen R4 hashes: `video.json` `0f4cb372e473ed68c54de32fffa9449b98e372a920e7e01700927321eba31364`; `script.md` `85af6713b18b42ad1177063cc3dfc5b5665810d70334678114693460dd3161d7`; `claims.md` `5cbcca08555bf337269a4a9b572bb0c3bd5bd28d19662715f93d9ac151861617`. Story body excludes CTA and remains 2,690 Han characters, 8.28 minutes at 325 CPM; opener is 167 Han characters, about 31 seconds. Lint remains 0/0. The [independent R4 source/visual receipt](../../docs/videos/curio-s63/review/r4-source-visual-independent.md) passes 127/127 lines, their anchors and written visuals against these exact hashes. The [formal R4 dual-blind merge](../../docs/videos/curio-s63/review/r4-formal-merge-audit.md) is **12/13 HOLD** on `no_recap`. No paid media may start on this draft.

## R5 author repair (2026-10-22 UTC)

The [R5 repair memo](../../docs/videos/curio-s63/review/r5-author-repair.md) splits one source sentence into two sequential events at `s63103` and `s63104`: six-o'clock wagon arrival, then inquiry for the addressed box and loading. It removes the repeated receiver planning without adding undocumented speech. Frozen R5 hashes: `video.json` `118430ef07ca7ac2e6d7c198088bdd1ef312755e126fef15ea2b310475a39adf`; `script.md` `dee3cb408979b3ca7dff85fb00e63915c2e54e555a0ee22e776e28fc97556c0f`; `claims.md` `5b616ce92afd61feed9264e57da240388619588e636550a91e93a315e2d6a9fc`. Body excluding opener and CTA is 2,673 Han characters, 8.22 minutes at 325 CPM; opener remains 167 Han characters, about 31 seconds. Lint 0/0. The [independent R5 source/visual receipt](../../docs/videos/curio-s63/review/r5-source-visual-independent.md) passes the unchanged 125/127 lines by exact diff and independently checks the two revised lines. The [formal R5 dual-blind merge](../../docs/videos/curio-s63/review/r5-formal-merge-audit.md) is **12/13 HOLD** on `no_recap`: A flags `s63052`, B flags `s63106`. B alone also flags final `s63126` on `payoffs`; OR merge passes that question while preserving the concern. R6 needs fresh source and blind checks.

## R6 author repair (2026-10-22 UTC)

R6 [作者窄幅修稿](../../docs/videos/curio-s63/review/r6-author-repair.md)從 R5 兩個 `no_recap` 位置及 B 單獨的片尾 `payoffs` 顧慮出發，只改 `s63002`、`s63004`、`s63052`、`s63106`、`s63126` 五個場景 ID。凍結雜湊：`video.json` `8f8903a7ec270c61636953a7d675840a838604c268132722658c05b26f2dbf68`；`script.md` `dfafdb178646575cc4cefab9c14621284835299caf1c75f3eea86e7835d82bd9`；`claims.md` `10a28deb76976f1b7c32eb4ab0188c6fda33e93d1914d2d1536c1ecd7eb9c18e`。開場 175 漢字約 32 秒，正文排除開場與 CTA 2,682 漢字約 8.25 分鐘（325 字／分）；lint 0/0。[R6 獨立來源／畫面審核](../../docs/videos/curio-s63/review/r6-source-visual-independent.md)以完全相同的 R6 凍結雜湊 PASS，五個修改 ID 均無阻擋項，另外 122 個場景逐欄未變。[R6 正式雙人盲讀合併](../../docs/videos/curio-s63/review/r6-formal-merge-audit.md)為 **12／13 HOLD**：A 否決 `no_spoiler`（`s63001`）及 `no_recap`（`s63124`），另非必答章名題否；B 否決 `no_recap`（`s63062`）。官方 OR 與 CLI 重播共同只擋 `no_recap`。作者另凍結 R7 才能重新送獨立審核；付費媒體維持封鎖。

## R7 author repair (2026-10-22 UTC)

R7 [作者窄幅修稿](../../docs/videos/curio-s63/review/r7-author-repair.md)以 R6 原票的具體意見為準，把開場 `s63001`–`s63004` 搬到里奇蒙交箱前，`s63009` 畫面不再先抵費城，並把章名改成事件；`s63062` 改為禱告動作，不再重複逃脫方案失敗；`s63067` 改為布朗追求自由的選擇，以免和新開場重述交箱；`s63123`–`s63124` 依 Stearns 腳註分說 1,200 美元索價及仍未知的籌款結果。九個場景 ID 改動、其餘 118 個場景逐欄相同。凍結雜湊：`video.json` `423f78e9ff18b5b77b14a0ad2fbfe71053cf08aba051a640c53038aa012c2263`；`script.md` `0b5f9bad1330cf0ffbb30998a6e3799b3f88386ffda70867fc047b6a8f4ab408`；`claims.md` `ac6a96737c7e84bff49991801874285de2d2a78b637f4e98899e8b16a37942d7`。開場 187 漢字約 34.5 秒，正文排除開場與 CTA 2,685 漢字約 8.26 分鐘（325 字／分）；lint 0／0。R7 只是一份作者候選，仍待新獨立來源／畫面查核，以及兩位未讀 R6 的正式盲讀；**不可沿用 R6 PASS，付費媒體維持封鎖**。

全新審核者已就上述**相同 R7 三檔雜湊**獨立核對九個新場景的逐句來源、資訊卡與書面畫面，並精確比對其餘 118 個場景；[R7 來源／畫面回條](../../docs/videos/curio-s63/review/r7-source-visual-independent.md)為 **PASS，無阻擋 ID**。回條記下 `s63067` 插圖「成箱」出自相鄰 B05 L1494 的非阻擋連結精度註。這只完成來源關，正式雙盲敘事仍未審；未開始付費媒體。

[R7 正式雙人盲讀合併](../../docs/videos/curio-s63/review/r7-formal-merge-audit.md)經全新 A、B 原票、`panelVerdict`／`mergePanelVerdicts` 逐題 OR 與官方 CLI 隔離重播，為 **12／13 HOLD**；兩人都否決 `no_recap`，A 指 `s63125` 重提開箱與法律未解，B 指 `s63053` 重提妻兒已離開。A 另單獨否決 `payoffs`（`s63125` 尚未給安全問題新答案），正式合併此題由 B 的「是」通過但顧慮保留。R7 來源 PASS 不會解除敘事 HOLD；R8 作者須定向修兩處並再次取得獨立來源／畫面及兩位未讀 R7 的新盲讀。付費媒體仍封鎖。

## R8 author repair (2026-10-22 UTC)

R8 [作者窄幅修稿](../../docs/videos/curio-s63/review/r8-author-repair.md)僅改 `s63053`、`s63125`、`s63126` 三個場景及一條 loop 回收 ID；124／127 個場景逐欄相同。告別後的重述改成 Brown 說過去阻止自己逃走的顧慮已消失；片尾不再第二次說開箱與法律未解，新增他**聽說**北方選民數量為南方兩倍及其若能影響北方會主張另立更好法律的主張。開場安全疑問改由 `s63120` 直接回收。凍結 SHA-256：`video.json` `c417bc8c6f0df78e9c4d8e910db038b6f4ea07c760cc7f3c2e69e98224f63f08`；`script.md` `63caedb24623bd8339607dd5b11e249ce1a4e6691779279a6d8c64ef5bbd665e`；`claims.md` `68c4139f38976d09b9b1b21bdb239eaa4ecb0ddd2f053b0ef445b971d636fe5e`。開場 187 漢字約 34.5 秒、正文排除開場和 CTA 2,676 漢字約 8.23 分鐘（325 字／分）；lint 0／0。**R8 尚待新獨立史料／畫面審核與兩位未讀 R7 的正式盲讀，不得啟動付費媒體。**

另一名獨立審核者已就上述**完全相同 R8 三檔雜湊**查核三個新場景與 `s63009→s63120` 回收點，精確確認其餘 124 個場景未動。[R8 史料／畫面回條](../../docs/videos/curio-s63/review/r8-source-visual-independent.md)為 **PASS、無阻擋 ID**；選民比例明示 Brown「聽說」，改革主張明示「若有影響力」。這項來源關本身不判敘事；其後兩位未讀 R7 的新讀者另審相同 R8 凍結封包，結果見下段。

[R8 正式雙人盲讀合併](../../docs/videos/curio-s63/review/r8-formal-merge-audit.md)在完全相同的 R8 凍結稿和官方 13 題上 **PASS 13／13**。全新 A 原票 13／13「是」，全新 B 原票 12／13「是」，B 單獨否決 `no_recap`，因 `s63026` 和 `s63027` 都提「五十美元」；兩句分別是 B02 原文明列的先付及其後每年付款，正式 `mergePanelVerdicts` 逐題 OR 通過。兩張原票、機械合併、三次隔離官方 CLI 輸出及綁定證據全部留存；合併 CLI exit 0，failed／advisory 皆空。史料與敘事稿件關已解鎖；語音、實際插圖、成片、Short、上傳與真實連結仍須逐項製作驗收。

## Production preflight and blocker (2026-10-22 UTC)

站主在本次對話明示「用推薦的決定就好不用問我」；依此**授權代理採推薦選項**，本機 CLI 在 `/workspace/.video-work/curio-s63/approvals.json` 記錄 A 案大綱及完全相同 R8 `script.md` 的核准，note 清楚說明站主未逐頁親審。`brief.md` 為當前狀態而更新後才綁定大綱；`script.md` SHA-256 仍為 `63caedb24623bd8339607dd5b11e249ce1a4e6691779279a6d8c64ef5bbd665e`。

網站配對權杖檔已存在，不記錄或輸出其內容；加 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1` 後，`tts --dry-run` 可查到 Gemini Sulafat：127 請求、3,214 計費字元、約月度免費額度 0.6%。`keyframes --dry-run` 查到 MiniMax image-01：**121 張插圖，單次約 US$1.63、每張最多三次時整集上限約 US$4.90**，截至此時 S63 花費 US$0.00。現有 branding 包的片頭 150 格＝5 秒、片尾 630 格＝21 秒；正式成片須檢查片頭落在第一章後及末 16 秒留給 Studio 結束畫面。`music --dry-run` 目前依賴 TTS 時間軸，尚無報價。

首次正式 `tts` 在**未生成首個音檔**時 exit 4，回覆「Gemini 語音暫時忙碌或達到用量上限，請稍後重試」；工作目錄目前只有 `approvals.json`，媒體帳本顯示 S63 **US$0.00**。需在服務可用後重跑相同 `tts`；再逐句 `check-audio`、處理需重唸句、完成音訊審核，才啟動整集插圖生成。不能把本次 dry-run 或網站服務狀態當作已生成聲音、插圖或成片。

04:35 UTC 左右隔了約三分鐘再次跑完全相同的 `tts`，仍在產生首句前 exit 4，回覆相同；沒有音檔或媒體帳本支出。這兩次失敗不足以區分短暫壅塞與 Gemini 當日額度耗盡；若是後者，skill 所記夏令重置時間為 **07:00 UTC**，可在 07:05 UTC 之後再試，並在每次有新診斷或狀態變化時才重試。不得以備用聲音暗中改掉頻道固定聲線。

另一位未參與撰稿的查核者另寫 [成片 QA 可讀的 `verify-1.md`](../../docs/videos/curio-s63/verify-1.md)：19 個來源／範圍群組涵蓋 127 句、6 張資訊卡及上架文案，18 組在出版文本的說話人限定內 CONFIRMED，0 個仍在旁白引用的 NOT FOUND，1 組是編輯語句 OUT OF SCOPE。報告逐一說明家人後續、選民比例和法律結果的證據界線，並綁上述同一 R8 三檔雜湊；`factsChecks` 可讀且通過。它記錄 `claims.md`、`research.md` 舊導言仍寫「R8 待審」；為維持獨立覆核和正式盲評的檔案雜湊，不修改已凍結的 `claims.md`，當前結論以 R8 正式回條為準。

## Notes

R4 [正式雙人盲讀合併審核](../../docs/videos/curio-s63/review/r4-formal-merge-audit.md)為 **12／13 HOLD**：A 否決 `payoffs` 與 `no_recap`，B 只否決 `no_recap`；官方逐題 OR 與 CLI 重播共同只擋 `s63103` 的重複接收者資訊。作者須另凍結 R5，並取得新的獨立史料／畫面審核及兩位未讀 R4 的正式盲讀，才可解鎖付費媒體。

Brown's narrative has the wife's and children's forced sale in August 1848, but does not explicitly date his own escape. The book's hymn is signed 1849-09-01, while the cited title page lacks a printed publication year; do not infer a publication year or an escape day from that signature. Exact 27 hours and 3 ft 1 in × 2 ft × 2 ft 6 in are Samuel J. May's appended speech extract, not Brown's stopwatch/measurement. The book was written by Charles Stearns from Brown's statement; it is not Brown's autograph diary. The source is accessible at pinned GITenberg revision `a92658e80effa4cce03bb19c13e96ffaaae5fa2b`; NPS and other sites tested through this cloud proxy returned CONNECT 403, so unviewed pages are not used as evidence. No paid voice, image or music has been requested for S63.

2026-10-22 同聲線語音已恢復：127句、13:37.13時間軸、52.60秒濃縮開場。check-audio進行中；精確證據r8-tts-reset-recovery-20261022，未稱QA通過／人耳核准，未進插圖。

## 最新製作檢查點（2026-10-22，台北）

前述R4／R8暫停記錄為歷史狀態。最新R9獨立來源查核通過，新雙讀者各13／13；127句旁白已生成，13:41.07，正文12:42.43，開場52.83秒。主辨識接受126／127句、0旗標；s63028保留供應商拒絕，由離線SenseVoice及另一查核者重跑確認內容相符。跨供應商機器證據127句，不宣稱主辨識器127句通過或站主親聽。詳見review/r9-s63028-independent-asr-audit.md與r9-cross-provider-audio-production-decision.md。首九景正在生成，尚待原圖驗收；121景插圖＋judge整集上限US$4.91，每景最多三次實際圖。PR #1665尚非成片；配樂／合成／QA／字幕／Shorts仍待做。
