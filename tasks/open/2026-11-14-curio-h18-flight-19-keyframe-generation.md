---
id: 2026-11-14-curio-h18-flight-19-keyframe-generation
title: Curio H18 Flight 19: keyframe generation, render, assemble, and publish
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-14T16:42:10Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-h18-flight-19
---

# Curio H18 Flight 19: keyframe generation, render, assemble, and publish

## Why

奇聞檔案局 H18《百慕達三角頭號證據：1945 年 6 架飛機為何同一晚消失？》（Flight 19）已完成稿子、獨立查核、盲讀委員會（第五輪通過）、zh-TW Sulafat 旁白、Gemini Lyria 配樂、八語翻譯與審稿、八語 MiniMax 配音（零溢出）、Drive 雲端硬碟備份（`H18/製作檔/curio-h18-flight-19`）。依站主指示先不做影像，影像與成片合成留待本票接續完成。

## Definition of done

- [ ] 影像製作：內建 `generate_image`（劇場級動畫光影 × 厚塗水粉質感，Charles Taylor 角色外觀鎖定，ImagePaths 參照）＋ `keyframes import --provider external --usd 0` 匯入（嚴格禁止 MiniMax 生圖）。
- [ ] 2x-zoom 四格放大獨立審圖（審查角色一致性、解剖、年代與風格）。
- [ ] 畫面渲染（`render`）。
- [ ] 音畫合成（`assemble`）。
- [ ] 繁中字幕與多語系字幕（`captions`）。
- [ ] 品質審查（`qa`）與上架包製作（`package`）。
- [ ] 提交後台 gate 並正式發布。

## Steps

1. 角色設定：產製 Charles Taylor 中尉人物設定圖並鎖定。
2. 逐鏡分鏡生圖：使用 `generate_image` 產生 76 鏡關鍵影格，跑 `keyframes import --provider external --usd 0`。
3. 渲染與合成：`node tools/video/cli.mjs render` 與 `node tools/video/cli.mjs assemble`。
4. 字幕與封裝：`captions`、`qa`、`package`。
5. 備份與推送到後台。

## How to verify

```bash
cd apps/web && npm run check:tasks
node tools/video/cli.mjs lint docs/videos/curio-h18-flight-19
```

## Notes

- 雲端備份位置：Google Drive `AI/備份/AI劇/奇聞檔案局/H18/製作檔/curio-h18-flight-19/`（資料夾 ID: `1dGjoosUoNX5N_OJC6IgP2lQQp_JF6bYy`），內含完整 788MB 壓縮檔 `curio-h18-workdir.tar.gz` 及個別音訊檔案。
- 工作區位置：`/home/antigravity/mokaair-work/videos/curio-h18-flight-19`。
- 本集不使用字卡或卡片，全片 76 鏡均為插圖（插圖比例 100%）。
