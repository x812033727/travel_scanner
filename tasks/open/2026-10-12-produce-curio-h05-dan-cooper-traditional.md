---
id: 2026-10-12-produce-curio-h05-dan-cooper-traditional
title: Produce Curio H05 Dan Cooper Traditional Chinese video
status: in-progress
priority: P2
area: docs
owner: codex-curio-h05
claimed_at: 2026-10-12T09:38:25Z
created_at: 2026-10-12T09:38:05Z
completed_at:
branch: codex/curio-h05-production-20261012
depends_on: []
scope:
  - docs/videos/curio-h05
---

# Produce Curio H05 Dan Cooper Traditional Chinese video

## Why

H04 繁中上傳包交付後，站主要求「繼續」。沿既有歷史懸案題庫接續 H05 Cooper 案，維持僅繁中，以機票、贖金與調查紀錄區分已知事件、推測及仍未解的去向。

## Definition of done

- [x] 三案企劃完成、當天一手來源刷新，所選大綱有本次雜湊核准。
- [x] 腳本經獨立事實及聽眾覆核，圖片權利與出處可追溯。
- [ ] 正文及成片各至少8分鐘；旁白、分鏡、字幕及成片通過原生關卡或站主核准。
- [ ] 僅繁中上傳包完成、原生檢查與正式站 consumer 回讀一致；未驗證項目明列。

## Steps

- [x] 查分支、worktree、遠端、PR與題庫，確認沒有其他 H05 製作；正式站GET404。
- [x] 從origin/main開獨立分支並認領窄範圍，讀回當前頻道立場。
- [x] 更新歷史、研究與素材來源，完成三案送審。
- [x] 撰稿、lint、獨立事實及聽眾審稿。
- [ ] 合成及逐句檢查旁白、製作與實看插圖／字卡。
- [ ] 合成、繁中CC、QA、核准、上傳包與consumer驗證。

## How to verify

Bundled Node 執行 tools/video/cli.mjs 的 lint、tts/keyframes --dry-run、check-audio、render、assemble、captions、qa、package、review-push/review-pull。保存來源／產物SHA及exit receipts，逐張實看採用畫面、獨立字幕覆核、原生正式站 consumer verify_files 回讀。文件跑適用docs-videos檢查及 tools/tasks.mjs check。

## Notes

- 媒體工作區在repo外：C:/Users/x8120/mokaair-work/videos/curio-h05。只做繁中，語言選擇不重問。
- H04 交付保留在既有草稿PR #1460與獨立工作區；不修改其他聊天的H02／H03語言工作。
- H05題卡 checked／ADOPT_WITH_CHANGES。當天刷新優先FBI、FAA與期刊原文，不把2016不再主動調查說成破案或完全結案；生死是推測、領帶DNA不宣稱屬於劫機者本人。
- 不提出在世嫌疑人的罪行結論，不製作真人漫畫臉、炸彈內部、航空操作或劫機操作教學。情境插圖不冒充1971照片。
- YouTube上傳、公開、merge與部署未授權；交付上傳包即本製作票範圍。

- 原生Jev於09:47:37 UTC自動核准A，review 47f37652-00b8-4fec-a322-8f9a729af7e8；brief SHA b384685061f457187f4ba3c189ebc7c99dfa275607853f397c2e8ec5f5df2803，native push/pull exit0與GET200一致。完整稿及付費媒體仍待製作。
- 10:11 UTC：完整稿SHA 007bd144…經24主張／105景／129句的獨立事實及聽眾覆核，0未解；原生lint、兩種dry-run及docs-videos 199／199通過。TTS開始，實際時間軸、逐句讀音、生成圖與播放器仍待驗證。
