---
id: 2026-09-26-video-dubs-worker
title: Video dubs: the worker synthesizes, shortens, checks and packages the tracks, and qa reports them
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-26T17:59:41Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-dubs-command
  - 2026-09-26-video-dubs-check-language
  - 2026-09-26-video-dubs-setting
  - 2026-09-26-video-dubs-captions-package
scope:
  - tools/video/automation
  - tools/video/qa
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
  - .claude/skills/youtube-video/references/prompts/caption-translate.md
  - .claude/skills/youtube-video/references/prompts/caption-review.md
---

# Video dubs: the worker synthesizes, shortens, checks and packages the tracks, and qa reports them

## Why

前四張票做出指令、檢查、每支影片的語言選擇與上傳包之後，主機工人要自己把配音做完，站主只在 Studio 上傳檔案（`docs/videos/DUBS.md`、`HANDS-OFF.md`）。站主 2026-09-27 的要求是每支影片先只出繁體中文，之後由站主在影片頁勾選要加的語言，勾了才做。塞不下的句子要交給翻譯模型縮短、被 Jev 標記的句子要重錄，兩輪不成就跳過那個語系，不能卡住整支影片。

## Definition of done

- [ ] 工人每一輪從既有的影片清單（`GET /video/videos`，`ProjectSummary.dub_locales`）看每支影片勾了哪些語系；成片已核准、而且有勾了還沒做（沒有當前音軌、也沒有跳過紀錄）的語系時，對那幾個語系跑：
  - `dub --locale <那幾個>`；結束碼 1 → 翻譯階段的「縮短」模式，只給 `fit.json` 列的句子與 `max_chars`（數字、專有名詞、說法不能改，字幕跟著用縮短後的句子）→ `i18n-merge` → 再 `dub`，每個語系最多 2 輪；
  - `check-audio --locale` → Jev 標記 → `dub --redo`，最多 2 輪；
  - 仍不行的語系寫 `dubs/<locale>/skipped.json`（原因），繼續往下，不 block；
  - 之後跑 `captions`（有配音的語系改用配音時間軸）；上傳包已經打包過就再跑一次 `package`；
  - 送一筆 gate `dubs` 的審核：附上做好的音軌檔（role `dub_<locale>`），payload `{ locales: { en: { file, status: "ready" }, ja: { status: "skipped", reason } } }`，summary 列出語系；站主核准表示已上傳。再勾新的語系就再送一筆。
  - 把 `dub:<locale>` 放進回報的 checklist，清單頁看得到進度。
- [ ] 沒勾語言的影片，流程和現在一個位元組都不差（測試）；配音不擋「確認上架」。
- [ ] `qa` 多一項 `dubs`：勾了的每個語系，不是有一條當前而且檢查過的音軌，就是有跳過的原因；跳過的算過、細節列成警告，缺的算沒過。
- [ ] 翻譯提示 `caption-translate.md` 說明 `max_chars` 與縮短模式，`caption-review.md` 檢查預算；`.claude/skills` 複本同步。
- [ ] `AUTOMATION.md`：工人的一輪多一段「配音」、輪數常數、成本連到 DUBS.md。
- [ ] `automation.test.mjs` 用假的 runner 走：一次成功、縮短一輪後成功、兩輪後跳過、沒勾語言不跑、已做過的語系不重做。

## Steps

- [ ] `flow.mjs` 的配音段與兩個迴圈；`prompts.mjs` 的縮短模式。
- [ ] `qa` 的 `dubs` 項。
- [ ] 提示詞與複本；`AUTOMATION.md`。
- [ ] 測試；主機上對一支已核准的影片勾 en，看它跑完。

## How to verify

```bash
npm run test:tools
```

主機：在 `/admin/videos` 對一支成片已核准的影片勾 en 並儲存，等工人日誌出現配音那一段；影片頁多一張 `dubs` 卡片，附件裡有 `en.m4a`；`qa.json` 的 `dubs` 項是 ok。

## Notes

- 工人在容器裡跑 `tools/video`，ffmpeg 是 `assemble` 用的那一個；要用 `--format mp3` 時先確認容器的 ffmpeg 有 libmp3lame。
- 每條音軌約 28 MB（m4a），送審的分段上傳與 `video_review_max_total_bytes` 要夠。
- 伺服器的 Gemini 月額度（`video_speech_gemini_monthly_character_limit`，預設 300,000 字元）先調高再勾語言：四條配音一支約 20,600 字元。
- 2026-09-29 (claude-opus-5-5): claimed by mistake (`tasks claim` has no `--dry-run`) and released without changes. What the season's videos 5 and 6 taught about each step this task automates is in `docs/videos/DUBS.md` §聲音會唸錯的地方: the shortening rounds need the measured rates, and inner-zero numbers in ja/ko are linted. Two further points. `check-audio --second-opinion` can clear Gemini's false flags before `dub --redo`. A zh-TW line that is too dense for the English and Japanese dubs is better given a longer `pause_after_ms` before the audio gate than cut in every language.
