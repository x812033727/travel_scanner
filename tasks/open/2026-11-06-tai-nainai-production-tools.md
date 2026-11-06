---
id: 2026-11-06-tai-nainai-production-tools
title: 祖奶奶今年十八 製作工具：script.md 轉 video.json 與 Colab 片段清單
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5
claimed_at: 2026-11-06T16:02:33Z
created_at: 2026-11-06T16:02:25Z
completed_at:
branch: claude/intelligent-gates-9n92xm
depends_on:
  - 2026-11-06-tai-nainai-screen-test
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools
  - docs/videos/tai-nainai-e001/video.json
  - docs/videos/tai-nainai-e001/brief.md
  - docs/videos/tai-nainai-e001/shots-en.json
---

# 祖奶奶今年十八 製作工具：script.md 轉 video.json 與 Colab 片段清單

## Why

第一季 60 集的分鏡在 `docs/videos/tai-nainai-eNNN/script.md`（中文、六欄表），但配音、匯入、剪接要 `video.json`，Colab 片段要 Ref2VA manifest。
《種田》的 `video.json` 是撰稿腳本直接寫的、`script.md` 從它產生；這部反過來，`script.md` 是源頭，所以要一支轉換工具。
站主 2026-11-06 試鏡後定走真人（3D 不行），照建議先做工具與定妝照重畫。

## Definition of done

- [ ] `production/tools/` 能把一集的 `script.md` 解析成結構化的鏡頭與台詞，加上逐鏡英文正文（`shots-en.json`，以中文那一列的雜湊綁定），產生 `video.json` 與 Ref2VA 第一段 manifest。
- [ ] 第 1 集跑通：`node tools/video/cli.mjs lint --slug tai-nainai-e001` 零錯，manifest 過 `h3.sh check`。

## Steps

- [x] `parse_script.py`：場頭（場景圖、燈、時間）、鏡頭六欄、台詞（說話人、語氣、心裡話、畫外、答在／因為標記）。
- [x] 說話人對 `cast.json` 的角色與路人 id。
- [x] `shots-en.json` 格式與第 1 集 27 鏡的英文正文。
- [x] `compile.py`：`video.json`、`brief.md`、Ref2VA manifest；中文列改了而英文沒跟上就停。
- [ ] 試鏡學到的：燈的分數各一張祠堂場景圖、景別要準的鏡走首格路線。

## How to verify

```bash
node tools/video/cli.mjs lint --slug tai-nainai-e001
```

## Notes

- 2026-11-06 第 1 集跑通：`compile.py 1` 產生 27 鏡、19 句、6 個角色的 `video.json`，`lint` 0 錯；`--manifest --placeholders` 兩份 Ref2VA manifest 過 `h3.sh check`。
  lint 剩 12 個 craft 警告是分鏡本身的節奏（鏡長中位數 4.6 秒、台詞中位數 16 字、78% 的鏡只有看與呼吸），跟 bible 的「台詞一句 10–24 字」（站主 2026-11-05 規格）互相衝突，交站主決定，工具不改。
- 參考圖的檔名規則：`<id>-portrait-t1.png`、換裝 `<id>-<look>-t1.png`、場景 `set-<場景>-t1.png`，祠堂有燈的分數時先找 `set-<場景>-lamp<N>-t1.png`。重畫定妝照時照這個名字存。

- 全季六欄表 1,438 列 `cNN`、另有少數 `cNNa/b` 拆鏡；另一種三欄表（鏡｜估計秒數｜要買）是長鏡清單，不是鏡頭。
