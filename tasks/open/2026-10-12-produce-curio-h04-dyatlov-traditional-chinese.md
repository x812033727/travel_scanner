---
id: 2026-10-12-produce-curio-h04-dyatlov-traditional-chinese
title: Produce Curio H04 Dyatlov Traditional Chinese video
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-12T04:45:10Z
completed_at:
branch: codex/curio-h04-production-20261012
depends_on: []
scope:
  - docs/videos/curio-h04
---

# Produce Curio H04 Dyatlov Traditional Chinese video

## Why

站主在 H03 繁中交付完成後要求「繼續」。接續已查核題庫 H04 佳特洛夫事件，維持只出繁體中文，以帳篷、足跡、1959 年文件和雪板模型講清楚證據與推測的差別。

## Definition of done

- [x] 三案企劃送審且所選大綱有當前雜湊核准。
- [x] 繁中腳本經獨立事實與聽眾審稿，來源和圖片授權可追溯。
- [ ] 正文與成片均達 8 分鐘，旁白、分鏡、字幕與成片通過既有關卡或站主核准。
- [ ] 繁中上傳包完成、原生檢查通過，正式站讀回一致；未驗證項目據實記錄。

## Steps

- [x] 查分支、worktree、遠端與 PR，確認 H04 無人製作；正式站 GET 404。
- [x] 新建獨立分支並認領窄範圍；讀回當前頻道立場。
- [x] 刷新一手來源與圖片授權，完成三案並送審。
- [x] 撰稿、lint、獨立事實查核與聽眾審稿。
- [x] 合成旁白並逐句檢查、製作及審看插圖與字卡。
- [ ] 合成、繁中 CC、QA、核准與上傳包驗證。

## How to verify

以 bundled Node 執行 `tools/video/cli.mjs` 的 `lint`、`tts --dry-run`、`check-audio`、`keyframes --dry-run`、`render`、`assemble`、`captions`、`qa`、`package` 與 `review-push/review-pull`；逐階段保存外部工作區 exit receipt 與 SHA。修改的 repo 文件跑 `tools/tasks.mjs check` 及適用的影片文件檢查。

## Notes

- repo 外媒體：`C:/Users/x8120/mokaair-work/videos/curio-h04`。`_audit/preflight-{reviews,settings}.json` 保存 2026-10-12 唯讀預檢。
- 只製作繁中長片；不重新詢問語言。沒有 YouTube 上傳、公開、merge 或部署授權。
- H03 已交付且其分支/PR #1456 保留；不修改 H03 來源或媒體，也不干涉其他聊天的語言工作。
- H04 原題卡仍需製作查核：帳篷切口的「兩處/三條」各文件不同；首批發現日 26/27 日不同；不敘述確切當夜氣溫、切口數或「找到帳篷隔天」。
- 在世檢察官懲處/離職與驗屍細節不進本片。2022 年考察只表達作者報告，不能當作 1959 年事件重演。
- 當前大綱 SHA `32bf76ed25e862e3e7c9e0bf8d1d369a2f9ad625a270c5518ed0919592f32a63`；review `d76bc11e-0d58-4983-b7d2-378d18e17bd2` 已由站主於 `2026-10-12T05:19:58.330973Z` 核准 A。2026-10-12 05:22 UTC 原生 review-pull exit 0 並 GET 200 回讀一致。
- 已有共用修正票 `2026-10-10-outline-pick-demo-exempts-explainers`，本集不擴張scope修改門檻、不重問付費judge以碰運氣。
- A 案完整稿 100 景／119 句已經獨立事實與聽眾覆核 PASS，0 未解必修；三張文書裁切已實看與清權。兩份覆核綁最終 video SHA `98b2fe192185644dd7a36a3deac8c4f8c9314a54486cedf1ff23cdd85dfae2f8`。docs-videos 199 tests passed。
- 119句旁白經三輪局部重錄與四句口語修正，逐句機器檢查0 flagged；正文604.0667秒、最長狀態7.7333秒。audio review `f28e20d8-8c02-4b9b-8af9-a50b8494b847` 已自動核准，2026-10-12 06:41 UTC原生pull及GET200讀回一致。真人完整播放仍待成片審看。
- 兩次轉寫答案遺失分別取得站主單筆一次重試授權，均已成功；Windows rename EPERM另依confirmed原件核對恢復，0重買。詳情與收據索引在PRODUCTION.md。
- 帳篷、弱層插圖小樣實看可保留；7張原創向量示意已實看並整合，舊足跡take保留。65張情境插圖主批次製作中；正式字卡及成片尚未完成。最新文件測試199 passed／0 failed。
- 08:02 UTC來源更新為 `3f2fdb0864afaa199e994f47bb180c6662e2e46efcc74da2c307e4268353e5e0`：現為60張AI情境插圖、12張已實看的原創SVG、3張授權文書裁切。speech/timeline不變。13項材料性畫面問題以4張SVG及9張窄範圍修圖處理；完整候選及修正收據保留在外部 `_audit/science-repairs-integration/`。08:04文件檢查199 passed／0 failed。正式render、assemble、繁中字幕與final review接續完成。
- 08:46:30 UTC assemble exit0；正文604.0667秒、成片ffprobe 612.100秒／18,362格，final SHA `262b2018a767cd7c1bdee9ff51cd54534e14e4199ec169ca9eb2b9a203ea3d86`。60/60 AI目前圖與12/12 SVG已有實看證據；57正式字卡狀態hash均與已審預覽一致，另實看37張代表轉場。獨立成片組裝稽核0材料性阻擋；保留一格容器時間差備註。
- 繁中119 cues完成，`_audit/caption-wrap-applied/receipt.json`證明10處僅換行、文字／時間不變；原生QA 11/11、15個連結可讀，綁目前final SHA。證據索引與完整SHA見PRODUCTION.md。本次只勾媒體製作步驟，成片核准與上傳包DoD仍開放。
- 08:52:19 UTC正式站GET200讀回分鏡review `3ba806bc-0250-4f10-9b96-35ee1c664de6` approved（08:25:59 UTC），同一 `9fe70948…` content SHA；大綱／旁白亦approved。final push隨後exit0，final review `0825f526-228e-4ad5-98de-efd02394c4bc` 於08:52:37 UTC建立，綁目前final SHA；08:52:46原生pull exit3、08:52:49 GET200均確認成片pending。只等成片及三張保留圖審看，不重問語言／分鏡；上傳包DoD保留。
- IAB連接逾時、Chrome使用者工作階段不可用，連續播放／完整聽音／播放器CC均 `NOT_RUN`。08:53:36本機播放器僅HTTP Range206及VTT200確認，UI結果未確認，不等於播放驗收。未做YouTube上傳、公開、merge或部署。
