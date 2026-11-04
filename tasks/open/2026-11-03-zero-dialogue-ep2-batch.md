---
id: 2026-11-03-zero-dialogue-ep2-batch
title: 零台詞四系列第 2–5 集（共 16 集）：產線與成片
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-03T15:34:37Z
created_at: 2026-11-03T15:34:36Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/wangjia-couple-e02
  - docs/videos/raccoon-mischief-e02
  - docs/videos/influencer-piglet-e02
  - docs/videos/shechu-hell-e02
  - docs/videos/zero-dialogue-series-ideas/production
  - docs/videos/wangjia-couple-e03
  - docs/videos/wangjia-couple-e04
  - docs/videos/wangjia-couple-e05
  - docs/videos/raccoon-mischief-e03
  - docs/videos/raccoon-mischief-e04
  - docs/videos/raccoon-mischief-e05
  - docs/videos/influencer-piglet-e03
  - docs/videos/influencer-piglet-e04
  - docs/videos/influencer-piglet-e05
  - docs/videos/shechu-hell-e03
  - docs/videos/shechu-hell-e04
  - docs/videos/shechu-hell-e05
---

# 零台詞四系列第 2 集（新髮型、吊燈、雪國、年度簡報）：產線與成片

## Why

站主 2026-11-03：四個系列的 EP1 做完後，每個系列繼續做下一集；照推薦直接決定、依序做完。

## Definition of done

- [x] 四集的 `video.json`、`brief.md`（lint 0 錯誤），由 `docs/videos/zero-dialogue-series-ideas/production/make_episode.py` 從各集 spec 產生。
- [x] 第 3–5 集 12 份 spec（`production/gen_specs.py` 產生，每份 lint 0 錯誤）。站主 2026-11-03：每系列 5 集、共 20 集。
- [ ] Colab 首格、H3 直式片段（`run_episode.sh`：一張一張跑、每張逾時強制重試）。
- [ ] 剪接成片（`edit.py`）、站主看過。

## How to verify

```bash
for s in wangjia-couple-e02 raccoon-mischief-e02 influencer-piglet-e02 shechu-hell-e02; do node tools/video/cli.mjs lint --file docs/videos/$s/video.json; done
```

## Notes

- 配樂沿用各系列 EP1 的那首（同系列聽起來一致，也不用再付）；音效沿用 EP1 的，加上每集 spec 的 `sfx_extra`（ffmpeg 合成）。
- 每一鏡一個主角，笑點那一格寫成角色本身在做（EP1 的教訓）。
- 第 2 集四支成片（2026-11-03）：新髮型 13.5 s（s05、s06 片段後半自己換景，剪短）、吊燈 17.2 s（s01 模型把吊燈畫成完好，裁掉天花板）、雪國 15.6 s（成品照片段 1 秒就換景，改用首格慢推；裁掉模型畫的雜誌名）、年度簡報 14.6 s。
- `edit.py` 會自動在片段中途的硬切換景之前剪掉（scene > 0.4）；鏡頭慢慢移走的那種偵測不到，要看片。
- 第 3–5 集（2026-11-03／04）：等妳出門 13.8 s；電視 15.6 s；仙境瀑布 14.4 s（成品照假刊名「FADCCA」裁掉）；主管巡視 15.8 s（s06 陰影被畫成黑球，只用後半）；凌晨三點打電動 14.4 s；時鐘 15.2 s；櫻花雨 14.4 s（假刊名用 delogo 遮掉、成品照改首格慢推）；申請加薪 15.2 s；搶被子 13.4 s；盆栽 15.2 s；螢火蟲之夜 14.0 s（成品照後半變形，剪短）。
- 網美小豬成品照一直出現假刊名，原因是 spec 寫了「like a magazine cover」，模型真的畫封面；e05 拿掉後就沒有了。之後網美小豬的成品照不要寫雜誌封面。
- 2026-11-04 01:3x 容器重啟，排程中斷；社畜地獄 e05 的首格已存在，重跑 `run_episode.sh` 從片段接續。
- 2026-11-04 品管：三組加一位獨立審片人逐格掃描 20 支。最常見：人類手指（黃金獵犬、小豬最常見）、辦公室背景的人影、插入特寫多一隻手、片段中途換角色、成品照假刊名。四輪重畫共約 35 鏡（提示詞加「四肢是毛茸茸動物爪、沒有人類手指」「身後就是一面牆、沒有隔間」，並避免在提示詞寫出不該出現的物件名稱，例如寫「原本掛時鐘的地方」反而畫出時鐘），其餘用剪短、整鏡拿掉、首格靜止、裁切、delogo 處理。最終 20 支都通過審片，9.8–18.0 s、1080x1920、30 fps、-13.5～-14.9 LUFS。
- 之後的 spec 寫法：角色要拿東西時改成「放在胸口／桌上」；辦公室場景直接寫「身後一面牆」；不要寫「像雜誌封面」；插入特寫只寫物件本身，不寫「一隻手伸進來」。

## 2026-11-04 品管紀錄

- 20 集都過了四道關卡（`production/QA.md`），包括站主要求的笑點審核。兩位審片人在四輪之後都判「笑點有畫出來」，好笑 3–4。
- 每集的判定、接受的已知問題與修正都在 `production/QA-2026-11-04.md`。重剪用 `recut.py`，補畫用 `redo3.py`、`redo4.py`；`edit.py` 新增 hold、reverse、push、lights_out、music_off、box。
- 還沒做：上架（`shorts import` 的工具缺口在另一張票 2026-11-03-shorts-import-zero-dialogue）。
