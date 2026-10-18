---
id: 2026-10-11-integrate-retained-video-source-fixes
title: Integrate retained video peak, locale QA and Mandarin boundary fixes into current main
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-11T14:19:00Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-integrate-retained-video-source-fixes.md
  - tools/video/assemble/branding-smoke.mjs
  - tools/video/assemble/branding.mjs
  - tools/video/assemble/branding.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

## Why

2a98 的三項 source 修補與本地 done 收據尚未落進主線。frozen main 1f183e4d1f3bb493b5412ca242f2cbb98da4f9bf 仍直接 concat branding audio、未選語言的 QA 仍走 readLanguages 全語要求、Mandarin matcher 仍只有行尾 closing-particle 候選。原三張票只存在 2a98，本地 done 不等於 main 整合完成。

原始 source 在 codex/stalled-videos-completion-20261008，HEAD b9940f18c1dfed8b493ceb9778df4c845728d4e2。現有 Draft PR #1387 https://github.com/x812033727/travel_scanner/pull/1387 已承載這三項修補，snapshot HEAD 382f26428786500a8e59d87ed04d8ccdf5c7e300；branding 3 檔與 Mandarin 2 檔對 2a98 完全相同，QA 2 檔是後續相容修訂。因此本票是完成現有 PR 或原 owner 的 current-main successor 的獨立整合驗收，不是另開第二個重複實作/PR。docs-only recovery 母票不能代替此 source scope。

## Definition of done

- [ ] 在當時最新 main 核對 active claims、PR #1387/head 與其 worktree，與原 owner 協調；保留 2a98 dirty 檔、已付費/UNKNOWN receipt、Mods STOP、原 claims。不要在 2a98 reset/rebase，也不要整檔覆蓋主線。
- [ ] 只相容整合下列 7 個產品/測試檔的三個 semantic delta；當前主線四語政策（#1413 移除 zh-CN）、STOP/lease、失去 policy 的 final guard、paid recovery/receipt/source 驗證保持。若 #1387 已 merged，核對同義實作與驗收後直接結案，不再重做。
- [ ] Branding 在 audio concat 後使用 unity-gain、latency-compensated、4x oversampling 的 -2 dBFS limiter 與 AAC headroom。真實離線 AAC regression 能重現原 0 dBTP 並證明修補後通過原 peak gate；選定 body bytes、video frames、精確 PCM samples、body/outro phase、CC/chapter offsets 不變。原 programme loudness、duration/body/final minima 與普通 assembly/QA 音訊門檻保持。
- [ ] owner 未選語言時，只要求 narration locale 與 mandatory zh-TW 的 captions/metadata；QA 不建立 languages.json、不替 owner 選語言。明選 metadata-only en 不要求 en CC；明選 en CC 缺件要只在 caption item 失敗，未選 ja/ko 不被強制要求。選擇後仍用 current-main captionLocalesOf/metadataLocalesOf 與四語規則，英文 narration 仍要求 en 加 zh-TW。
- [ ] Mandarin 比對在刪標點前，只對 heard transcript 增加 clause-boundary closing-particle 候選，支援中文及 ASCII 標點前的新增 耶/餒。intended script 不改。lexical 氣餒/气馁/好耶 仍有意義，只可容許再新增的 氣餒耶/好耶餒；數字、否定、名詞、缺少 intended 字、leading/interior particles 仍拒絕。原 raw/end-only 與非中文行為不變。
- [ ] 重用既有 cached tgby 的 primary/secondary transcripts 做 zero-provider regression，兩個皆 same-sound；htb5/ew6e/kr2g/yqpn/bc5q 五個原 flags 仍不通過。不得因 matcher 改動宣告 owner 聽音/影片/語言 acceptance。
- [ ] 由未撰寫 source 的 reviewer，以整合後最新 main baseline 重新審查 duration-bound QA 2 檔及 check.test.mjs，保留所有既有 review 增量，只增加本次真正獨立的 increment/bindings。不要把 2a98 舊 review.json 蓋掉 current-main receipt。long-form check/review tests 與 task checks 通過，最後讀回實際 merged main 的 source/receipt/hash。
- [ ] source 整合證據、local test、main merged、production deployment、owner listening、upload/publication 分開記；本票結案不表示後三者完成。原三票的 localdone 記錄保留其作者/範圍/原始證據。

## Steps

- [ ] 先對帳 PR #1387 是否已包含全部三項；以該 PR 的當前 owner/worktree 和 current-main 差異決定原分支續整合或其單一 successor，不複製另一組 source 工作。
- [ ] 7 產品/測試檔固定為 tools/video/assemble/branding-smoke.mjs、branding.mjs、branding.test.mjs；tools/video/qa/cli.mjs、qa.test.mjs；tools/video/tts/check.mjs、check.test.mjs。另 2 檔只供獨立 duration receipt：docs/videos/long-form/review.md 與 review.json。
- [ ] 用離線 FFmpeg synthetic bookends 與 cached transcript fixtures 驗證；測試輸出寫 repo 外。不呼叫 ASR/TTS/Jev/生成、不啟動正式 worker、不動 STOP/approval/owner language choices、不上傳、不部署。
- [ ] 通過獨立 review 與 required CI 後，依正常 task-board PR 流程讀回實際 main 整合結果；docs-only 2026-10-08-stalled-production-video-completion 只記 current cohort/remaining production 與本票連結。

## How to verify

    node --test tools/video/assemble/branding.test.mjs tools/video/assemble/assemble.test.mjs tools/video/assemble/drama.test.mjs tools/video/compile/compile.test.mjs
    node tools/video/assemble/branding-smoke.mjs --assets <offline-synthetic-assets> --workdir <outside-repo-evidence>
    node --test tools/video/qa/qa.test.mjs tools/video/qa/duration.test.mjs
    node --test --test-name-pattern='comparison|same-sound|Taiwanese particles|closing particles|outside Chinese|zh-CN keeps' tools/video/tts/check.test.mjs
    node tools/video/long-form/cli.mjs check
    node --test tools/video/long-form/review.test.mjs
    node tools/tasks.mjs check
    git diff --check

執行現在受影響的 full suite/required CI，不能把歷史 full Windows tts suite 的 EPERM 當全部 green，也不要把舊失敗直接當當前失敗；若仍失敗，記真實 exit code 與原因，與 #1379/#1391 owner 協調其已存在 atomic/path 修補。

## Notes

原 localdone ID：2026-10-08-video-branding-true-peak、2026-10-08-video-qa-undecided-languages、2026-10-08-video-audio-closing-particle-boundaries。原舊 source baseline edcce347a3f97841f84f8788d81f16e51c34a3e6；QA source commit ed827033、Mandarin source eccafa3c7、獨立 duration receipts 52cfd7eea/b9940f18c。這些是歷史版本證據，不能取代 current-main 相容驗收。

既有 branding smoke 在 <home>/mokaair-work/handoff/branding-peak-20261008/smoke/evidence.json：540 frames/18 s、864000 samples/channel、decoded peak -2 dBTP、retained body SHA 相同、quiet body PCM 遠離 seams 差最多 1 unit、CC 5000–15000 ms/chapters 不變。原 real AAC regression 是 576000 samples/channel、0 → -1.9 dBTP。synthetic overall -15.1 LUFS 不是 production loudness acceptance。

原 branding.mjs SHA256 1d5c89b5e54ebfee67fae5fececa7b4e8d5e1dba7dd145dca6e459bfe5d4658c；原 check.test.mjs receipt SHA256 42f9bdbcb3b4454fb9d945f3899da36bcc3d70c045d31196f0c931a692f906d1。Mandarin 離線證據在 <home>/mokaair-work/stalled-video-completion-20261008/embedding-audio/particle-offline-recheck.json。

本輪僅恢復共享待辦；没有接管source任務、修改原worktree、model/provider request或正式站操作。

原始保留分支／核對HEAD：
- `codex/stalled-videos-completion-20261008@b9940f18c1dfed8b493ceb9778df4c845728d4e2`。
- `codex/stalled-video-reviewed-fixes-20261008@382f26428786500a8e59d87ed04d8ccdf5c7e300`。

本票保持 open、未認領。此輪僅恢復共享追蹤與具體驗收，不改原owner/claim/HOLD/STOP/UNKNOWN；已完成實作與現存媒體不重做。新票在本draft PR，尚未合併至main；續作先查main與active scope，不從歷史收據推論當前正式狀態。
