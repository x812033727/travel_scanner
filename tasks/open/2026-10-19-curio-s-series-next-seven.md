---
id: 2026-10-19-curio-s-series-next-seven
title: Extend the Curio history video production queue to twenty episodes
status: in-progress
priority: P3
area: docs
owner: codex-gpt6-history-series
claimed_at: 2026-10-19T21:20:00Z
created_at: 2026-10-19T21:20:00Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s20
  - docs/videos/curio-s21
  - docs/videos/curio-s22
  - docs/videos/curio-s24
  - docs/videos/curio-s25
  - docs/videos/curio-s27
  - docs/videos/curio-s36
---

# Extend the Curio history video production queue to twenty episodes

## Why

站主在原先約十支之外要求更多歷史系列影片，並授權依建議持續製作。現有本線十三支為 S02、S03、S04、S05、S06、S07、S08、S19、S23、S26、S28、S30、S34；S01、S09、S18 另有工作者認領，不在本票重做。先增加七個各自可獨立製作的候選集，使本線有二十支的明確範圍。

## Proposed next seven

| 集數 | 暫定問題 | 查核起點與風險 |
| --- | --- | --- |
| S20 | 蒙娜麗莎失竊時，畢卡索為何被問話？ | 1911–1913 年報刊與審訊記錄；區分畢卡索、阿波里奈爾與真正竊賊。 |
| S21 | 鬱金香狂熱到底有多瘋？ | 當代成交與契約紀錄、近代經濟史研究；避免把「沒有經濟影響」說滿。 |
| S22 | 維京人何時到過北美？ | 蘭塞奧茲牧草地考古與 1021 年年輪測年論文；分開「在場年份」與首次抵達。 |
| S24 | 阿基米德真的喊過 Eureka 嗎？ | 維特魯威文本及寫作年代；傳說與實驗可行性分層。 |
| S25 | 牛頓的蘋果有打到頭嗎？ | 斯圖克利回憶與牛頓手稿；分開掉落故事與撞頭插畫。 |
| S27 | 維京人的頭盔有角嗎？ | 館藏實物、十九世紀舞台造型；不能從少數出土物概括所有戰士。 |
| S36 | 波士頓真的被糖漿淹過嗎？ | 1919 年事故報告、審訊與當代報刊；傷亡和速度等數字逐一查來源。 |

這些只是題目卡，尚未完成來源重開或腳本簽核。先挑可直接取得一手資料的一題做完整前製；若來源無法核對，保留記錄並換題。每支依 `curio-episode` 流程通過獨立讀稿、逐句史料、語音、插圖、成片與上架包關卡。

## Definition of done

- [ ] 七題各有來源可重開的研究或明確停拍理由，避免照候選題卡直接旁白。
- [ ] 可製作的各集有獨立劇本、來源對照、盲讀及真實媒體品質記錄。
- [ ] 完成影片有 1080p 成片、字幕、封面、QA 和 Private 上架包；影片公開上架由站主另行操作。

## How to verify

逐集檢查研究中引用的原文、`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs status --slug <slug>` 與實際上架包；`npm run check:tasks`。
