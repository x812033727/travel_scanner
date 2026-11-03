---
id: 2026-11-03-ai-host-lipsync-pilot
title: AI 主持人導覽 Shorts 小樣：原創角色對嘴，比較兩到三條 lip-sync 路線
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-03T01:09:58Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/pilots/ai-host-lipsync
---

# AI 主持人導覽 Shorts 小樣：原創角色對嘴，比較兩到三條 lip-sync 路線

## Why

站主 2026-11-03 問能不能做「真人感的 vlog」、用 AI 主持人。現有產線做不到：旁白有了（Gemini 台灣口音 TTS），片段有了（RunPod／Colab 的 MiniMax H3、Hailuo、Kling），但**沒有對嘴**——`docs/videos/DRAMA.md` 與 animation 系列 skill 都寫「產線沒有對嘴」，露臉說話的鏡頭被評成 B 級風險（`.agents/skills/animation-preproduction/references/shot-risk.md` 的 `speech.visible-mouth`），收據一律寫 `lip_sync_verified: false`；自動影片的插圖規則也不畫真人臉（`.agents/skills/youtube-video/references/visuals.md:32`）。要不要把「主持人說話的畫面」做進產線，取決於現成的 lip-sync 路線做出來的嘴型、表情、角色一致性與成本，所以先做一支小樣比較，不先寫程式。

界線（和站主說過的）：AI 主持人是**導覽員**，講站上查核過的攻略內容，不假裝親身去過（不說「我昨天去吃了」）；親身經驗的 vlog 感由站主實拍的畫面或人工錄製路線提供。角色是原創的，不像任何真人，不用真人照片或真人聲音當參考。上架勾「變造或合成內容」。

## Definition of done

- [ ] 一個原創主持人的設定圖（正面、三分之四側、半身，固定臉、髮型、服裝），存在 `docs/videos/pilots/ai-host-lipsync/character/`，附提示詞與生成工具。
- [ ] 從一篇已上線的 Mokaair 旅遊攻略改寫一段約 45–55 秒的導覽口播稿（不寫第一人稱的親身經歷），用產線的 Gemini 聲音合成同一份旁白。
- [ ] 同一張設定圖加同一段旁白，跑兩到三條對嘴路線（候選：Kling lip-sync、RunPod pod 上的開源說話頭像模型、HeyGen／Hedra 類商用服務；實際跑哪幾條寫進 Notes），每條產出一支主持人 A-roll。
- [ ] `docs/videos/pilots/ai-host-lipsync/ledger.csv` 每支一列：路線、模型或方案、輸入解析度與秒數、輸出寬高與 fps、成本（點數或美元）、生成時間、浮水印、嘴型同步（逐句看）、表情與眨眼、臉的一致性、手與身體、恐怖谷感、備註。
- [ ] 至少一支合成成 9:16 Shorts（主持人 A-roll 加 H3 或站主素材的 B-roll、繁中 CC），交站主看。
- [ ] `docs/videos/pilots/ai-host-lipsync/README.md` 寫結論：推薦哪條路線、一分鐘成本、能不能做長片、要進產線還需要什麼（例如 `lipsync` 階段、對嘴驗收、角色一致性檢查），並另開對應的 tools／api 票。

## Steps

- [ ] 0. 站主確認方向：純 AI 導覽員，或站主實拍加 AI 主持人串場；以及願意試哪些付費路線、預算上限。
- [ ] 1. 選一篇攻略、寫口播稿、合成旁白。
- [ ] 2. 畫角色設定圖（伺服器的 MiniMax image-01 或 RunPod 的 Qwen 首格），站主核可。
- [ ] 3. 逐條路線跑對嘴、記 ledger；每條送出前先寫好預算，不超過上限。
- [ ] 4. 挑最好的一支合成 Shorts。
- [ ] 5. 寫 README 結論、開後續票（本票不改 `tools/` 與 skill）。

## How to verify

```bash
npm run check:tasks
ls docs/videos/pilots/ai-host-lipsync/
```

站主實際看完 Shorts 小樣與 ledger，在 README 記下決定。

## Notes

- 2026-11-03 開票。產線現況：`.agents/skills/animation-production/references/providers-and-plans.md` 提到社群 MCP（github.com/199-mcp/mcp-kling）有 `create_lipsync`，扣 Kling 開發者 API 的資源包，未試過。RunPod 路線（`minimax-h3-runpod` skill）目前只跑 H3，pod 上能不能跑別的 ComfyUI 工作流要先查。
- YouTube 對大量產製、不真實內容有營利限制；「AI 導覽員講查核過的內容」的定位與「假裝親身經驗」差很多，結論裡要寫清楚。
