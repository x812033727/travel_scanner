---
id: 2026-09-24-video-pilot-ai-model-choice
title: 影片產線 T6：試作影片〈AI 模型怎麼挑〉
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-24T00:41:17Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-skill-automated
scope:
  - docs/videos/ai-model-choice
  - docs/videos/lexicon.json
  - docs/videos/README.md
---

# 影片產線 T6：試作影片〈AI 模型怎麼挑〉

## Why

第一支試作影片〈AI 模型怎麼挑〉，由已發布的 `ai-workflow-cost-quality-latency`（成本、品質、延遲怎麼取捨）改寫，8–12 分鐘，Mokaair 品牌。用它把整條全自動產線從企劃跑到站主在 Studio 以私人狀態看完，找出工具與規則的缺口。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `docs/videos/ai-model-choice/` 有 `brief.md`（含站主觀點與觀眾看完能做到的事）、`video.json`、`claims.md`、`verify-1.md`（必要時 `verify-2.md`）。
- [ ] `docs/videos/lexicon.json` 收錄這支用到的術語唸法。
- [ ] 站主選過大綱、聽過旁白、看完全片（`approvals.json` 有三筆，雜湊與成品一致）。
- [ ] 站主在 Studio 上傳成私人；章節出現在進度條上。
- [ ] 實際耗時、TTS 字數、截圖與編碼時間記在 Notes，給下一支估時間。

## Steps

- [ ] 站主的一次性設定（`.agents/skills/youtube-video/references/automated.md` §一次性設定）：後台填 Azure 金鑰與區域、連線測試、建立影片工具權杖，站主自己跑 `node tools/video/cli.mjs login`。
- [ ] 用 `audition` 讓站主比較頻道聲音（曉臻、雲哲、曉雨，以及 Ava、Andrew 講台灣國語），選定後寫進 `docs/videos/README.md` 的聲音表。
- [ ] 企劃代理 → 站主選大綱。
- [ ] 撰稿代理（sonnet）→ 查核代理（opus，換人）→ 聽眾優先審稿。
- [ ] 價格類事實在錄製當天重新查官方頁（文章是 2026-09-19 的數字）。
- [ ] tts → 試聽 → render → assemble → package。
- [ ] 站主上傳、確認。

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-model-choice
node tools/video/cli.mjs status --slug ai-model-choice --workdir <VIDEO_WORKDIR>
```

## Notes

- 營利政策的對策：至少一段用當天官方定價實算三種流程的成本，不只是念重點。
