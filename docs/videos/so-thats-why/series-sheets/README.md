# 原來如此事務所的系列設定圖

站主核准的角色設定圖，工具在每一集自動沿用（`tools/video/media/series-store.mjs`，[`docs/videos/SERIES.md`](../../SERIES.md)）。

- 所長 `chief`：P02 站主選的那張（P05、P14 沿用）。
- 小問 `kid`：2026-11-06 拿掉筆記本之後的新設定（P14 選的 F）。

工具讀的是工作目錄裡的 `_series/sothatswhy/characters/`（預設 `/root/mokaair-work/videos/_series/sothatswhy/characters/`）。
雲端容器是暫時的，這裡放一份備份；新的 session 開工前先還原：

```bash
mkdir -p /root/mokaair-work/videos/_series/sothatswhy
cp -r docs/videos/so-thats-why/series-sheets/characters /root/mokaair-work/videos/_series/sothatswhy/
```

每一集的 `build_scenes.py` 都要在 `video.json` 寫 `"series": {"slug": "sothatswhy", "episode": N, "chapter": 1}`，
`look` 才會從這裡沿用，不重畫。角色的 `appearance` 一改，就會重畫那個角色（設定圖的鍵是外觀描述加畫風）。
