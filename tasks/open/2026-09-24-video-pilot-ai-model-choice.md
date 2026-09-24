---
id: 2026-09-24-video-pilot-ai-model-choice
title: 影片產線 T6：試作影片〈AI 模型怎麼挑〉
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-24T06:12:08Z
created_at: 2026-09-24T00:41:17Z
completed_at:
branch: claude/video-pilot-audio
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

- [x] 站主的一次性設定：後台填好 Azure 金鑰與區域；權杖改用配對取得（#717），2026-09-24 代理跑 `login`、站主按「允許」。
- [x] 用 `audition` 讓站主比較頻道聲音，選定後寫進 `docs/videos/README.md` 的聲音表。2026-09-24 第一輪 7 個 Azure 聲音：站主選 Ava（多語）+5%，但嫌「語調太平、像在念稿」；第二輪 Gemini 5 個聲音，選 **Sulafat**（#725 之後）。
- [x] 企劃代理 → 站主選大綱。2026-09-24 選 A（三個問題的判斷框架），站主觀點照草稿；核准已綁定 `brief.md` 的雜湊。
- [x] 撰稿代理（sonnet）→ 查核代理（opus，換人）→ 聽眾優先審稿。
  - 撰稿：157 句、2,939 字。
  - 查核第 1 輪：37 條，改 4 條。
  - 站主決定成本表的旗艦改用 Claude Opus 5.5 重算。
  - 查核第 2 輪（換人）：33 條，改 1 條，不需第 3 輪。
  - 聽眾審稿：章節拆回 8 章，另修 5 句。
- [ ] 價格類事實在錄製當天重新查官方頁（文章是 2026-09-19 的數字）。
- [x] tts（Sulafat，157 句，約 10 分鐘）。
- [x] 旁白檢查：站主 2026-09-24 決定「正確與否給 Jev 判斷」，不自己試聽 → `check-audio`（#732、#736）。2026-09-25 結果 157 句全數通過，0 句被標。
- [ ] 站主核准旁白（`approve --gate audio`）→ render → assemble → CC → package。
- [ ] 站主上傳、確認。

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-model-choice
node tools/video/cli.mjs status --slug ai-model-choice --workdir <VIDEO_WORKDIR>
```

## Notes

- 營利政策的對策：至少一段用當天官方定價實算三種流程的成本，不只是念重點。
- **上架前要處理（查核第 2 輪提出）**：說明欄、片尾與 2fhy 都說完整算式在來源文章裡，但文章還是 Opus 5 的數字（0.03／0.0114／0.1004）。可以更新文章的成本段（走 content-pipeline），或在說明欄加一句「文章的表用 Claude Opus 5、算法相同」。待站主決定。
- 2026-09-25 分支改為 `claude/video-pilot-audio`：`claude/video-pilot` 被 worktree video-skill 佔著，那邊沒有 commit 的 Sulafat 改動（`video.json` 的 voice、`README.md` 的聲音表）已原樣搬過來、單獨一個 commit。
- **旁白檢查的過程（2026-09-24〜25）**：
  - 第一輪 157 句，Jev 標了 28 句。其中 8 句是轉寫把字寫成同音字（它／他、級聯／吉蓮），5 句是聲音自己加的語氣詞。站主選擇**保留語氣詞**，工具因此改成同音字與語氣詞不送 Jev（票 `2026-09-24-check-audio-accepts-same-sound-characters`）。
  - 其餘 15 句逐句重錄兩輪，剩 4 句一再出錯：句尾單獨的「答」被聽成「打」，「單一旗艦」「分三步走」也一樣。這 4 句改寫成「先回答」「各回答一次」「單一旗艦模型」「分三個步驟」，改寫後比較好聽懂。再重錄一次後全數通過。
  - 四輪重錄共 473 字，檢查時 Jev 大約呼叫 25 次。
  - 另外有 3 句 Gemini 連續幾次都轉寫失敗，隔天才成功（#736 之後錯誤訊息會帶狀態碼）。
- 2026-09-24 claude-opus-5-5 認領。第一次真合成的數字：101 字樣稿、7 個聲音，共 1,282 計費字元；Ava 原速 19.9 秒，約每分鐘 300 字，比工具估計的 250 字快。8–12 分鐘的片要 2,400–3,400 字旁白。之後 `DEFAULT_CPM` 或 `video.json` 應該能依聲音設定語速，否則 lint 的長度估計會偏長。
