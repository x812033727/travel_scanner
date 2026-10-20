---
id: 2026-10-20-blackberry-x09
title: 製作 BlackBerry 品牌故事 X09 前製包
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-blackberry-x09
claimed_at: 2026-10-20T17:52:57Z
created_at: 2026-10-20T17:52:54Z
completed_at:
branch: codex/brand-story-blackberry-x09
depends_on: []
scope:
  - docs/videos/story-everyday-blackberry-x09
---

# 製作 BlackBerry 品牌故事 X09 前製包

## Why

站主要持續做與奇聞檔案局相同規則的原創品牌故事，逐集完成後開 PR。BlackBerry 的 2017 KEYone 是一個可由 SEC 原件查核的反常故事：手機仍有品牌名，但公司把後續硬體開發與銷售責任交由夥伴承擔。本票建立 X09 獨立前製，避免將授權轉型寫成一天全停售、把自有設備收入誤當 KEYone 銷量，或把專利授權收入誤寫成手機授權成果。

## Definition of done

- [x] 完成六章一線繁中 Treatment、來源矩陣、30–60 秒開場、實質正文稿、可機讀主片與兩支 `from-episode` Shorts。
- [x] 五份 SEC 原件、110 句主片與 8 張原生卡、兩支 Shorts 的同版獨立來源審查 PASS：`reviews/source-audit-v7-independent.md` 綁定 v7 主片與 Shorts SHA。
- [x] 兩位獨立敘事盲讀對同版主片 SHA 的合併必答題 PASS；A 11/12、B 12/12，唯一分歧是 `no_recap`，沒有兩人都答否的必答題。Lint 0 錯誤／0 警告，稿面鉤子節奏合格。
- [ ] 向主代理交付 draft PR、全部驗證與待製作清單；正式 TTS 時長、付費媒體、官方動畫、成片 QA 與 YouTube Studio 可點連結仍需另行完成，不能稱此 PR 是成片。

## Steps

- [x] 對已核准百題、C01–C20、X01–X08 查重；以獨立工作樹做第九題。
- [x] 讀五份 SEC HTML 原件並留 URL 與 SHA，寫 FY2015、FY2017、FY2018 庫存退出與 FY2020 手機授權條款的限制。
- [x] 編成 110 句、99 插畫景、8 卡、19 loops；長片 lint 0/0；Shorts 稿面 38–50 秒。
- [x] 用配對影片工具對舊版做免費乾跑；v7 為 110 句、本機約 2,565 個 `say` 字元與 99 插畫景。舊版每圖報價只供估算，v7 仍須重新乾跑當期報價與額度。
- [ ] 同版新來源審查與兩位盲讀合併 PASS 後，重跑文件／任務檢查、推送並開 draft PR。

## How to verify

`node docs/videos/story-everyday-blackberry-x09/compose-video.mjs`、`node docs/videos/story-everyday-blackberry-x09/compose-shorts.mjs`；重建檔案的 SHA 必須和同版審查收據相同。`node tools/video/cli.mjs lint --file docs/videos/story-everyday-blackberry-x09/video.json`、`npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。兩位盲讀收據須列 13 題、行 ID 與同一主片 SHA；合併判定依兩位**都**答否才退回。

## Notes

2026-10-20：五份 SEC 原件下載 SHA 見 `source-notes.md`。FY2017 截於 2017-02-28；KEYone 由 TCL 宣布，預計 FY2018 Q1 供應。v1、v2 來源審查只對各自舊主片 SHA 有效；v2 兩位獨立盲讀都指出主線與結尾 QNX 岔題，故依 FY2018 原件重構。當前主片 SHA `774c84a401b0c08112ec89073d12d9b1a14cb924a40684fc8235c0e70a4ecf27`；Shorts SHA `6341e807ec1c2b06562faaa2b38a65bd90e4dcfe679b5f4bbbec98d2c61e7214`；同版 v7 來源 PASS、雙盲合併 PASS。v7 圖像 99 景依舊單價粗估三次上限 US$4.01，實際報價和全項 US$25 預算仍待重新乾跑。站點同月新配樂額度暫無；正式 5 秒片頭、21 秒 v4 片尾與 Studio 管理入口未在此工作區裝設。專集 lexicon 已以交易鎖在 `story-lexicon/`，沒有產生音訊／圖片；媒體或任何出刊連結仍待後續。

v4 的獨立來源差異審查 PASS，但兩位 v4 敘事盲讀都指出章節承接、開頭「為何」未回收與結尾重述；因此 v5 重新安排章首事件、收束區域及機型名單、以收入縮小與庫存風險作有界推論。v5 獨立來源差異審查 PASS，但兩位 v5 盲讀都指出三組舊數字重述與產品、地域岔路；v6 因此保留每組第一次登場，刪去地域與平台點名。v6 獨立來源審查發現 FY2018 百分比混用調整後／GAAP 分母，盲讀 A 則指出庫存重述、尾段數字清單和 Short 2 原因對比不足。v7 用同一 GAAP 分母重新換算占比，收束尾段帳目，並在 Short 2 口播區分 FY2016→17 需求／機型老化與 FY2018 授權轉型。v7 來源審查 PASS；敘事 A 對 FY2017 原因回扣一題判否、B 全部判是，故按兩位都否才退的規則合併 PASS。舊審查只作歷史紀錄。
