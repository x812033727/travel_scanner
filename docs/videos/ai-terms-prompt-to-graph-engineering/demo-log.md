# 示範紀錄：ai-terms-prompt-to-graph-engineering

2026-10-03，在 repo `x812033727/travel_scanner`（git 50cfb03b，Node v22.22.0）由撰稿代理自己執行；這份是影片第 5、6、7 章「我們自己的產線」示範的證據，`lint-terminal`、`ledger-stats`、`our-loop`、`our-graph` 四張卡的內容都從這裡抄。沒有呼叫任何 AI 模型，沒有花錢，沒有任何產品介面的畫面。

## 一、檢查工具（lint）的七次執行

稿子由一支產生 `video.json` 的腳本寫出（撰稿 scratchpad 的 `_tools/build_video.py`，不進 repo；`video.json` 是定稿）。`--demo-english` 會在 `ch5-card` 的旁白放進英文詞「Harness」，用來示範字典關卡；其餘是稿子本身的檢查。每次都是 `node tools/video/cli.mjs lint --slug ai-terms-prompt-to-graph-engineering`，結束碼與輸出的前幾行逐字抄錄（警告逐條列出的那幾次只抄摘要行與錯誤行，完整輸出在 scratchpad 的 `lint-run-N.txt`）。

| # | 用途 | 時間（UTC） | 結束碼 | 摘要行 |
| --- | --- | --- | --- | --- |
| 1 | 故意放英文詞的測試（第 1 版稿） | 2026-10-03T14:32:25Z | 1 | `ai-terms-prompt-to-graph-engineering: 1 errors, 0 warnings` |
| 2 | 稿子本身，第 1 次 | 2026-10-03T14:32:25Z | 1 | `ai-terms-prompt-to-graph-engineering: 1 errors, 0 warnings` |
| 3 | 故意放英文詞的測試（補上 look 之後） | 2026-10-03T14:33:10Z | 1 | `ai-terms-prompt-to-graph-engineering: 3 errors, 30 warnings` |
| 4 | 稿子本身，第 2 次 | 2026-10-03T14:33:11Z | 1 | `ai-terms-prompt-to-graph-engineering: 2 errors, 30 warnings` |
| 5 | 稿子本身，第 3 次（拆短 16 張 shot、縮短單狀態卡片、改光線用語之後） | 2026-10-03T14:38:42Z | 0 | `ai-terms-prompt-to-graph-engineering: 0 errors, 2 warnings` |
| 6 | 故意放英文詞的測試（近定稿；terminal 卡抄的是這一次） | 2026-10-03T14:42:36Z | 1 | `ai-terms-prompt-to-graph-engineering: 1 errors, 1 warnings` |
| 7 | 稿子本身，改字後覆核（定稿） | 2026-10-03T14:42:36Z | 0 | `ai-terms-prompt-to-graph-engineering: 0 errors, 1 warnings` |

### 第 1 次：故意放英文詞的測試（第 1 版稿）

```
ai-terms-prompt-to-graph-engineering: 1 errors, 0 warnings
ERROR look: illustrations need a look: name a preset such as "riso-teal" (docs/videos/ILLUSTRATED.md)
```

### 第 2 次：稿子本身，第 1 次

```
ai-terms-prompt-to-graph-engineering: 1 errors, 0 warnings
ERROR look: illustrations need a look: name a preset such as "riso-teal" (docs/videos/ILLUSTRATED.md)
```

### 第 3 次：故意放英文詞的測試（補上 look 之後）

```
ai-terms-prompt-to-graph-engineering: 3 errors, 30 warnings
ERROR scenes[33].lines[0] (i8vp): "Harness" is not in docs/videos/lexicon.json: add how to say it, or null once it sounds right
ERROR scenes[41] (lint-terminal).data: tool_version is required: the version of the tool that printed the output, as it reports it (for example 2.1.285 (Claude Code)), one line of at most 40 columns
ERROR scenes[18] (ruler-check): about 12.4 s of narration; a shot is at most 12 s (the clip models stop at 10), split it
（30 條 WARN 省略：16 張 shot 超過 10 秒、單狀態卡片超過 8 秒、「daylight」出現在 27／47 張圖、平均 6.7 秒換一張、估計 11.5 分）
Estimate: 11.5 min, 112 lines, 2506 spoken units
```

### 第 4 次：稿子本身，第 2 次

```
ai-terms-prompt-to-graph-engineering: 2 errors, 30 warnings
ERROR scenes[41] (lint-terminal).data: tool_version is required: the version of the tool that printed the output, as it reports it (for example 2.1.285 (Claude Code)), one line of at most 40 columns
ERROR scenes[18] (ruler-check): about 12.4 s of narration; a shot is at most 12 s (the clip models stop at 10), split it
（30 條 WARN 省略：16 張 shot 超過 10 秒、單狀態卡片超過 8 秒、「daylight」出現在 27／47 張圖、平均 6.7 秒換一張、估計 11.5 分）
Estimate: 11.5 min, 112 lines, 2504 spoken units
```

### 第 5 次：稿子本身，第 3 次（拆短 16 張 shot、縮短單狀態卡片、改光線用語之後）

```
ai-terms-prompt-to-graph-engineering: 0 errors, 2 warnings
WARN  scenes (lint-terminal state 2): stays on screen about 8.5 s; a picture changes at least every 8 s: split the shot, reveal one item per sentence, or put an illustration here (estimated; the final gate measures the synthesized timeline)
WARN  scenes: about 11.9 minutes; the target is 9-11
Estimate: 11.9 min, 120 lines, 2554 spoken units
```

### 第 6 次：故意放英文詞的測試（近定稿；terminal 卡抄的是這一次）

```
ai-terms-prompt-to-graph-engineering: 1 errors, 1 warnings
ERROR scenes[40].lines[0] (mymk): "Harness" is not in docs/videos/lexicon.json: add how to say it, or null once it sounds right
WARN  scenes: about 11.9 minutes; the target is 9-11
Estimate: 11.9 min, 120 lines, 2552 spoken units
```

### 第 7 次：稿子本身，改字後覆核（定稿）

```
ai-terms-prompt-to-graph-engineering: 0 errors, 1 warnings
WARN  scenes: about 11.9 minutes; the target is 9-11
Estimate: 11.9 min, 120 lines, 2550 spoken units
```

稿子本身的三次（第 2、4、5 次）：第 1 次缺 `look`、第 2 次 `tool_version` 還是佔位字串加一張 12.4 秒的 shot、第 3 次零錯誤；第 7 次是把 `lint-terminal` 最後一句縮短、`our-loop` 填入實際次數之後的覆核，仍為零錯誤。`our-loop` 卡因此寫「前兩次被擋下，第三次才歸零；共跑 7 次，含 2 次故意放錯的測試」。

## 二、`lint-terminal` 卡抄的是第 6 次

`command`：`node tools/video/cli.mjs lint --slug ai-terms-prompt-to-graph-engineering`（69 欄）。`output` 兩段：第一段是摘要行，第二段是錯誤行；錯誤行 127 欄，照終端機在第 80 欄斷行成兩行（版型一行最多 80 欄）。`ran_on` 2026-10-03；`tool_version`「50cfb03b (tools/video, git)」——工具沒有 `--version`，用 repo 的 git 短碼。

```
ai-terms-prompt-to-graph-engineering: 1 errors, 1 warnings
ERROR scenes[40].lines[0] (mymk): "Harness" is not in docs/videos/lexicon.json: 
add how to say it, or null once it sounds right
```

## 三、`status` 的輸出（第 7 章「產線是一張圖」）

對已經做到查核階段的試片 `ai-term-token` 跑一次，14 個步驟一步一個勾選框，「Next」是下一個指令：

```
# status --slug ai-term-token, 2026-10-03T14:32:25Z, git 50cfb03b
ai-term-token  (work directory: /root/mokaair-work/videos/ai-term-token)
  [x] brief
  [ ] outline approved: not approved yet
  [x] script passes lint
  [x] fact-checked
  [ ] narration synthesized: timeline.json has no current audio evidence; run tts to refresh cached takes, then review the narration again
  [ ] narration approved: nothing to approve yet
  [ ] keyframes drawn
  [ ] storyboard approved: nothing to approve yet
  [ ] frames rendered
  [ ] video assembled
  [ ] captions written
  [ ] final video approved: nothing to approve yet
  [ ] upload package
  [ ] on YouTube

Next: ask the owner to choose the outline (a question with options), then node tools/video/cli.mjs approve --slug ai-term-token --gate outline
```

這支影片自己在第 7 次 lint 之後的 `status`：`[x] brief`、`[x] script passes lint`，`[ ] outline approved`（等站主或 Jev 挑大綱）、`[ ] fact-checked`（等查核）。

## 四、`ledger-stats` 卡的三個數字

```
apps/api/app/video_automation/schemas.py:242: slides_max_usd_per_video: int = Field(default=20, ge=0, le=10_000)
apps/api/app/video_automation/models.py:141: "slides_max_usd_per_video": 20,
tools/video/automation/flow.mjs:72: export const MAX_REPLANS = 2;
tools/video/automation/automation.test.mjs:2304: assert.equal(MAX_REWRITE_ROUNDS, 2);
```

同一天在 main 分支的 raw 檔確認（`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，都回 200）：`schemas.py` 含 `slides_max_usd_per_video: int = Field(default=20`、`flow.mjs` 含 `MAX_REPLANS = 2`、`docs/videos/HANDS-OFF.md` 含「自動品管 11 項全過」。20 美元是後台設定的**預設值**，站主可以在 `/admin/videos` 的設定分頁改；字卡的 note 寫「後台設定的預設值」。

## 五、核准綁雜湊（`wax-seal`）

出處是 skill 主文與 `automated.md`：「核准綁定檔案雜湊：稿子或旁白改了，舊的核准自動失效，後面的指令會以結束碼 3 拒絕，要重新 review-push」；`docs/videos/HANDS-OFF.md`「核准綁定檔案雜湊，檔案改過就要重新送審」。這次沒有實際觸發結束碼 3（還沒有任何核准可以失效），旁白只說機制，不說「我們試過」。

## 六、沒做的事

- 沒有呼叫任何模型、沒有 `tts`、沒有 `keyframes`、沒有 `review-push`；本機沒有金鑰也沒有配對權杖。
- 沒有改 `docs/videos/lexicon.json`：旁白沒有英文名詞。
- 沒有改 `docs/videos/ai-terms/terms.json` 與系列 README（那個資料夾在另一張票的 scope 裡）；這一集要登記進名詞庫，由持有該 scope 的人補一列 `status: planned` 或一段「總覽集」說明。

