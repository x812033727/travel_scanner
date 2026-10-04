---
id: 2026-09-29-video-pilot-jev-decision-model
title: Pilot the first illustrated storytelling video: Jev, the model that only decides
status: done
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-29T09:14:25Z
completed_at: 2026-10-03T23:46:23Z
branch:
depends_on:
  - 2026-09-29-video-storytelling-prompts
scope:
  - docs/videos/jev-decision-model-explained
  - docs/videos/ILLUSTRATED.md
---

# Pilot the first illustrated storytelling video: Jev, the model that only decides

## Why

計畫的每個數字（成本、節奏、judge 一次過的比例、站主審片分鐘數）都是估的；第一支插圖說書影片要拿真實數字，並與 Gary Chen 的參考片（`2mtn-Qp59y4`，同題）並排比較。現有 10 支的資料夾都在別的票的 scope 裡，所以新開一支。

## Definition of done

- [ ] `docs/videos/jev-decision-model-explained/`：brief（站主觀點、觀眾看完能做到的事、每個數字在當天官方頁查核：TypeSafe AI 的 Jev、193.6×／444.6×、RLCD、輸出 token 免費、每百萬輸入 token 約 US$0.042、Diogo Almeida）→ video.json（說書式、shot 每 5–8 秒）→ 旁白 → 插圖（Flash、自動核准）→ 合成 → CC → qa → 上架包。
- [ ] 驗收：鉤子 ≤20 秒；≥2 個「你以為…其實…」；每章結尾是問題；無狀態 >8 秒、平均 ≤6 秒、share ≥ 0.5；shot 溶接、章節硬切、單狀態卡片漂移；床 ≤ −24 LUFS、成片 −14 LUFS；音效不搶戲；畫面無燒錄字；媒體花費 ≤ US$15。
- [ ] `ILLUSTRATED.md` 的數字表：插圖張數、重做次數、judge 一次過比例、分鐘數、站主審成片分鐘數、費用。
- [ ] 站主看過並決定 10 支舊片重做（`restyle`＋加圖）或照舊上架。

## Steps

- [ ] 在 `/admin/videos` 發起投影片影片，題目「爆紅的 Jev 不聊天只做決定：快 200 倍、便宜 400 倍是真的嗎？」。
- [ ] 走完全自動路線，每一步記數字。
- [ ] 寫回 `ILLUSTRATED.md`。

## How to verify

`node tools/video/cli.mjs status --slug jev-decision-model-explained` 依序出現 keyframes drawn → storyboard approved → frames rendered → music generated → video assembled → final video approved；`qa` 的 pace 項印最長、平均、share；`media-status` 印帳本。

## Notes

站主第 0 期要先做（2026-09-29 第 1–8 期都已落地，不再需要過渡期的做法）：

1. 部署後到 `/admin/videos` 設定分頁：
   - 教學分頁的 Gemini 語音 `style` 貼 `tools/video/automation/register.mjs` 的 `STORY_VOICE_STYLE`（新安裝已是預設；既有的資料列要自己貼）。
   - 「投影片影片的插畫」區塊：打開「替投影片影片畫插圖」；模型維持 gemini-3.1-flash-image；單支上限 20（或 15）；「judge 全過時自動核准投影片的分鏡」維持開；填「授權配樂檔名」（例如 `bed.mp3`）與「音效組資料夾」（例如 `studio-a`）。
   - 說書規則已在提示詞裡（`REGISTER_RULES`），常設指示不必再貼；要加頻道自己的口頭禪才貼。
2. 工人主機的 `<VIDEO_WORKDIR>/_music/<檔名>`（mp3／m4a／wav／flac）與 `<VIDEO_WORKDIR>/_sfx/<組名>/{stamp,whoosh,pop}.*` 加 `manifest.json`（`{"source":…,"license":…,"sounds":{"stamp":{"file":"stamp.wav"},"whoosh":{…},"pop":{…}}}`），格式見 `docs/videos/ILLUSTRATED.md` §配樂與音效。
3. 在「影片」分頁發起一支投影片影片（題目如上）；工人會自己走 keyframes → storyboard（自動核准）→ render → music（檢查你的檔）→ assemble → 品管 → 上架包；插圖成本估 US$5–8（60–75 張 × US$0.077，含 judge）。
4. 舊的 10 支要改口吻：`node tools/video/cli.mjs restyle --slug <slug>`（先 `--dry-run` 看現況）；要加插圖則要撰稿重寫成有 `shot` 的稿（另開票；它們的資料夾仍在別的 in-progress 票的 scope 裡）。

- **Merged into the AI terms episode, 2026-10-03 (owner's decision).** This pilot is not
  produced as its own video. The owner chose to make the same launch post an episode of
  「AI 名詞十分鐘」 instead: `docs/videos/ai-term-system-one-model/` (brief, demo, notes),
  produced by `2026-10-03-ai-term-system-one-model-video`. What moved there: the role of
  first illustrated storytelling pilot, the acceptance criteria above, the `ILLUSTRATED.md`
  numbers table, the side-by-side observation against `2mtn-Qp59y4`, the owner's decision on
  the 10 older videos, and the phase-0 setup notes. What was dropped on purpose, because the
  series does not say it: the price per million tokens, free output, 193.6× / 444.6×, RLCD,
  the founder, and the 「爆紅…快 200 倍、便宜 400 倍」 title. The comparison with
  `2mtn-Qp59y4` becomes "same subject, different angle", not a point-by-point match.
  `docs/videos/jev-decision-model-explained/` was never created. The two `ILLUSTRATED.md`
  rows that name this ticket are updated by the episode's production task, because that file
  is held by `2026-10-03-illustrated-slides-round-2-a-family` (review) today.
