# 種田娶妻 第 31 集起的共用素材

雲端 session 的工作資料夾（`~/mokaair-work/videos`）不會留下來，也不跨帳號；這些是每集都要、又重做不出一樣結果的檔，
所以放在 repo 裡給每個對話共用（站主 2026-10-30）。站台的媒體庫是快取（`video_media_keep_days`，沒有工作引用就清掉），
不能拿來存。

| 路徑 | 是什麼 | 從哪來 |
| --- | --- | --- |
| `refs-dh/*-portrait-t1.png`、`refs-dh/set-*-t1.png` | 角色定妝照與場景圖（Ref2VA 的 `<Picture N>`） | 第 31–32 集 session 在 Colab 上用 Qwen-Image-Edit 畫的（票 `2026-10-28-31-colab-h3`、`2026-10-29-32-40-colab-ref2va`） |
| `refs-dh/angles/<id>-angle-*.png` | 角度臉，從第 1–30 集的海螺首格裁的 | 同上 |
| `music/cue-tension.mp3`、`cue-suspense.mp3`、`cue-comedy.mp3` | 第 33 集起的三段配樂（各約 2 分鐘） | 2026-10-30 `music-zt.mjs` 經站台 Lyria 3.5 生成，slug `zhong-tian-qu-qi-e033`。第 31、32 集的原版沒有留下 |
| `season1-thumb.png` | 每集匯入用的季封面 | 站台第 30 集 final 審核的 `thumbnail.png`（`review-files --slug zhong-tian-qu-qi-e030 --gate final`） |

`SHA256SUMS` 是每個檔的雜湊；`sha256sum -c SHA256SUMS`（在這個資料夾裡）核對。音效不在這裡：`hailuo/local/sfx-synth.sh` 隨時重新合成。

## 還原到工作資料夾

工具讀的是 `<VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/` 與每集的 `music/`：

```bash
A=docs/videos/series-plans/zhong-tian-qu-qi/production/assets
V=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
mkdir -p "$V/_series/zhong-tian-qu-qi" "$V/zhong-tian-qu-qi-compilations"
cp -r "$A/refs-dh" "$V/_series/zhong-tian-qu-qi/"
cp -r "$A/music" "$V/_series/zhong-tian-qu-qi/"
cp "$A/season1-thumb.png" "$V/zhong-tian-qu-qi-compilations/"
bash docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/sfx-synth.sh
mkdir -p "$V/zhong-tian-qu-qi-eNNN-dh/music" && cp "$V/_series/zhong-tian-qu-qi/music/"cue-*.mp3 "$V/zhong-tian-qu-qi-eNNN-dh/music/"   # 每集，rec.sh 之前
```

新畫的定妝照或場景圖（例如第 39 集的黎明官道）畫好就加進 `refs-dh/`、重算 `SHA256SUMS` 並提交，下一個對話才拿得到。
