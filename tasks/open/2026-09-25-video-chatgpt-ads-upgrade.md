---
id: 2026-09-25-video-chatgpt-ads-upgrade
title: 影片：ChatGPT 開始有廣告了，免費版、Go、Plus 要不要升級
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-25T01:23:37Z
created_at: 2026-09-25T01:22:59Z
completed_at:
branch: claude/video-batch-2
depends_on: []
scope:
  - docs/videos/chatgpt-ads-upgrade
---

# 影片：ChatGPT 開始有廣告了，免費版、Go、Plus 要不要升級

## Why

2026-09-24 熱門話題研究的第一名：ChatGPT 廣告 9 月 24 日在台灣上線（OpenAI 9/23 公告），受影響的是免費版與 Go 的使用者。站主 2026-09-25 選了這個題目與大綱 A（判斷方法框架）。企劃書在 `docs/videos/chatgpt-ads-upgrade/brief.md`，來源文章 `ai-free-vs-paid-plans-2026`。

## Definition of done

- [ ] `docs/videos/chatgpt-ads-upgrade/` 有 `brief.md`、`video.json`、`claims.md`、`verify-1.md`（必要時 `verify-2.md`），`lint` 零錯誤。
- [ ] 旁白通過 `check-audio`，站主核准旁白、看完成片（`approvals.json` 三筆，雜湊與成品一致）。
- [ ] 站主在 Studio 上傳成私人，影片 ID 寫回 `video.json`。

## Steps

- [x] 企劃代理寫 brief，站主選大綱（2026-09-25，選項 A）。
- [x] 撰稿（sonnet）→ 查核（opus，換人）→ 聽眾優先審稿，2026-09-25 完成。新詞已併進共用的 `docs/videos/lexicon.json`。
  - 查核第 1 輪改了 21 個事實，最主要是改用官方台幣價；第 2 輪換人查，0 個要改。
  - 聽眾審稿：
    - 五處說「開關」的地方改成中文介面的「無廣告」。官方流程是「變更方案」加上確認，不是撥動式開關。
    - 步驟字卡和旁白改用中文介面名稱「設定 → 廣告控制功能」，英文名稱只放在字卡的說明。
    - 97p6、228y 這兩句預測標成「我的判斷」。
    - wjbn 不再推測官方有沒有把握。
    - 開場的 wuun 加上「付費方案裡」，避免聽起來和 kvw2 矛盾。
    - 刪掉過期的方案階梯圖場景：圖在另一篇文章裡，還寫台灣以美元計價，而且型號是舊的。
    - 開場刪兩句重複的，其他地方刪兩句。
  - lint 0 錯誤，約 11.8 分鐘。
- [ ] tts → check-audio → 核准旁白 → render → assemble → CC → package。
- [ ] 站主截一張 ChatGPT「設定 → 廣告控制功能」的畫面，存成 `docs/videos/chatgpt-ads-upgrade/screenshot-ad-controls.png`（代理不登入站主帳號）。目前的腳本沒有用到截圖，這步可以不做。
- [x] ~~Go 與 Plus 的台灣台幣價格只有登入後看得到~~：2026-09-25 起，未登入從台灣開定價頁就直接顯示 NT$270／NT$690（含 5% 稅，還在陸續推出中），片中改用這兩個官方價。

## How to verify

```bash
node tools/video/cli.mjs lint --slug chatgpt-ads-upgrade
node tools/video/cli.mjs status --slug chatgpt-ads-upgrade
```

## Notes

- 2026-09-25 claude-opus-5-5 認領；分支 `claude/video-batch-2`，疊在試作片分支 `claude/video-pilot-audio` 上（要用它的 `docs/videos/lexicon.json`）。
- **brief 的站主觀點有三個前提被官方來源推翻**（兩輪查核都提到，腳本已照事實寫，brief 沒改，因為核准綁著它的雜湊）：
  - 「免費開關效果跟付錢買 Go 一樣」：Go 可能有廣告，無廣告選項是真的沒有。
  - 「官方用一條線隔開」：官方沒有這樣寫。
  - 「要自己加 5% 稅」：台灣的台幣價已經含稅。
  - 要改 brief 的話，改完要重新核准大綱。
- 會過期的事實：台幣價（還在陸續推出中）、台銀匯率 31.855（2026-09-25 13:45）、「這禮拜」（以 2026-09-23 公告為準）。錄音前再查一次。
