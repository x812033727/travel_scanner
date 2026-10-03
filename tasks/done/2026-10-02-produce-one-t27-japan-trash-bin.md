---
id: 2026-10-02-produce-one-t27-japan-trash-bin
title: Produce one T27 Japan trash-bin survey episode
status: done
priority: P2
area: docs
owner: codex-t27-production
claimed_at: 2026-10-02T12:46:05Z
created_at: 2026-10-02T12:42:27Z
completed_at: 2026-10-02T16:03:22Z
branch: codex/sothatswhy-t27-pilot
depends_on:
  - 2026-10-02-video-render-settled-layout
scope:
  - docs/videos/sothatswhy-t27/
---

# Produce one T27 Japan trash-bin survey episode

## Why

站主在完成 T26 後指定「做下一個」。依第二季順序製作 T27，將垃圾桶疑問聚焦於官方旅客調查能回答的範圍，完成可審閱的繁中長片。

## Definition of done

- [x] 原創六章旁白與 SVG 插畫經獨立查核及聽眾審稿。
- [x] 正常台灣口音旁白正文及成片實測各至少 480 秒，繁中 CC 可開關。
- [x] 正常語音、成片 11 項 QA、上架包 4 項檢查通過，核准綁定目前檔案雜湊。
- [x] 完整成片及上架包保存在 repo 外，後台同集有實際附件及核准收據。
- [x] 完成來源、畫面、時間軸及交付紀錄，草稿 PR 僅在以上工作全部完成後建立。

## Steps

- [x] 官方來源及調查題目、分母、多選條件查核。
- [x] 大綱、腳本、原創畫面製作及獨立覆核。
- [x] TTS 額度預檢、正常合成與逐句語音檢查。
- [x] 合成、字幕、實際影片抽查及正常 QA。
- [x] 後台上架包與交付證據完成。

## How to verify

使用 tools/video/cli.mjs 的 lint、tts --dry-run、check-audio、render、assemble、captions、qa、package 與正常 review-push／review-pull；另以 ffprobe、實際成片解碼與原始 WAV 核對 >=480 秒、原創 SVG 畫面語義及 CC 對時；check:tasks、git diff --check。

## Notes

最終交付完成於 2026-10-02 UTC／2026-10-03 Asia/Taipei：純講述 533.270 秒、正文格線 673.233333 秒、實際完整成片 688.200 秒／20,644 frames。137 句語音零被標，130 原創 SVG／137 正常畫面，三項視覺修正閉環；全部 still 與 15 張 actual-final samples 獨立看過，完整音畫解碼及當前 SHA 通過。normal QA 11/11、package 4/4、outline/audio/final/publish 四關皆 approved/current。

final SHA256 `3894c35e2cd5860d0b834c1ba02578986600c15e1e4ce53d59d0b95f1e993016`；metadata SHA256 `0b391df71413e3ea5ef4307b4984d332dd81174e43af5fc98b92e4ed0abe79d3`。後台 GET 讀回 final review `cab3a243-7d28-433e-bca1-a0a4de07e247`、publish review `2922dac4-fd3a-438c-9614-128ddadd1cc2`，九個附件與本機實檔雜湊逐一一致；YouTube ID null、on_youtube=false、語言選擇 pending／ready_to_upload=false。站主完整播放、聽音、CC 播放器驗收及額外語言選擇不以機械檢查代替，本票只交付本次繁中媒體，不包含上傳、公開或額外語言生成。

來源及所有精確綁定文字收據保留；末稿只改寫 63kr 一句，事實未變，正常 audio approval 重新取得。HTTP 502 的一次付費 POST 結果／費用不確定，成功產出與請求收據全保留，沒有把它描述為未計費；有界恢復及單句改寫詳見 production-record.md。完整實片時間戳偏差及初次 null-output 量化警告保存在 final-runtime-review，沒有冒稱所有 PTS 等於格線或刪掉失敗證據。

本分支已安全接到 main `acb935fb461e34ee110b725b742179cc22d67770`。本機 channel current／舊安裝素材不存在，首輪無書擋 body 已保存 history；本集僅透過私有 work base、唯一 junction 及正常 assemble --adopt-branding 套用已核准系列 11.9 秒 intro／3 秒 outro，成功後正常工具才写 pin，137 段畫面全重用，無新 TTS。全域 registry 及其他影片未動。最後 PR 碰撞前檢讀38worktrees、34個+branches、39remoteheads、9openPR及主線，T27 scope 零競爭／既存PR，主線沒有本集；最後提交前再次檢查。

正式文字證據：production-record、delivery-proof、branding-adoption、visual-review、runtime-audit、final-runtime-review；大型媒體只放 repo 外。本票已結案；Windows 在 done copy 寫入後留下相同 open body，協調者核對 id／owner／body 相符後將 open 副本移至 repo 外本次證據目錄保存，check:tasks 通過且看板只保留 done。本次草稿 PR 不合併或部署。

新 managed worktree sothatswhy-t27，起初疊在 T26 PR #1128 的已測 renderer 修正上。12:54:44Z GitHub 顯示帳號端已合併第一集（merge 9e84872429be5267b08be0cffcd1b6f6aca2de13，十項 CI 全過）；root 沒有執行 ready／merge／deploy。比較兩棵樹完全一致後，第二集分支已移至該最新 main，只交第二集差異。原來如此事務所第二季有效企劃 T27 為旅客調查題，採官方 2026-04-28 公告及原始 PDF；17.2% 為最多被選的困難項目，43.7% 為未遇困難，題目為多選，不能畫成整體互斥比例或推論全日本街頭數量與歷史起因。只製作此集繁中；站主仍控制每集額外語言及 YouTube 上傳／公開。媒體在 C:/Users/x8120/mokaair-work/videos/sothatswhy-t27，不修改全域設定或 uploader，不對未知付費 POST 盲目重試。
