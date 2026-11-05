# 種田娶妻 第 31 集起的共用素材

雲端 session 的工作資料夾（`~/mokaair-work/videos`）不會留下來，也不跨帳號；這些是每集都要、又重做不出一樣結果的檔，
所以放在 repo 裡給每個對話共用（站主 2026-10-30）。站台的媒體庫是快取（`video_media_keep_days`，沒有工作引用就清掉），
不能拿來存。

| 路徑 | 是什麼 | 從哪來 |
| --- | --- | --- |
| `refs-dh/*-portrait-t1.png`、`refs-dh/set-*-t1.png` | 角色定妝照與場景圖（Ref2VA 的 `<Picture N>`） | 第 31–32 集 session 在 Colab 上用 Qwen-Image-Edit 畫的（票 `2026-10-28-31-colab-h3`、`2026-10-29-32-40-colab-ref2va`） |
| `refs-dh/angles/<id>-angle-*.png` | 角度臉，從第 1–30 集的海螺首格裁的 | 同上 |
| 第 43–60 集的新圖（2026-11-01 起）：`refs-dh/chuzhifu-portrait-t1.png`；`set-haoshe`、`set-mifeng-fang`、`set-shuyuan-zhai`、`set-zhou-jie`、`set-bangfang`、`set-zhoufu-tang`、`set-zhoufu-houtang`、`set-zhou-kezhan-yuan`、`set-beidu-qiantan`、`set-hetan`、`set-liaowangtai`、`set-cundao`、`set-jiusi`（各 `-t1.png`）；定妝照 `chengshanzhang`、`fengxuezheng`、`weixun`、`dutie`、`dengyasi`、`lengtie`、`changgonggong`（各 `-portrait-t1.png`；常公公第二步多畫了鬍子，再以那張為 image 1、`latent: image1` 剃掉） | 定妝照與場景圖 | Colab Qwen-Image-Edit-2509（`h3.sh images --detached`，`lora: false`、20 步、CFG 4、空白 latent），票 `2026-10-31-zhong-tian-paint-e042-e060-refs`。場景圖的 image 1 是 `set-shuyuan-t1.png`、1920×1088；定妝照的 image 1 是 `zhaobutou-portrait-t1.png`、1248×1664（3:4 胸像，跟海螺時期的定妝照同構圖）；褚知府以外分兩步畫（先畫對人，再裁胸像、以趙捕頭為 image 2 重畫），見 `lessons.md` §9。提示詞、seed 與每一輪的取捨在 `production/colab/runs/refs-e042-e060/`。PNG 內嵌 ComfyUI 的 prompt（`tEXt` 的 `prompt` 欄）可以讀回完整設定 |
| `music/cue-tension.mp3`、`cue-suspense.mp3`、`cue-comedy.mp3` | 第 33 集起的三段配樂（各約 2 分鐘） | 2026-10-30 `music-zt.mjs` 經站台 Lyria 3.5 生成，slug `zhong-tian-qu-qi-e033`。第 31、32 集用的是另一組同名 cue，2026-11-04 從 `transfer/zt-e031-e032-media` 取回，放在 `music/e031-e032/` |
| 第 42 集的新圖：`refs-dh/xudalang-portrait-t1.png`、`zhouyuanwai-portrait-t1.png`、`innkeeper-portrait-t1.png`、`registrar-portrait-t1.png`、`set-zhou-kezhan-t1.png`、`set-gongyuan-t1.png` | 許大郎、周員外、客棧掌櫃、貢院書吏的定妝照，州城客棧與貢院報名處的場景圖。第 42 集已用這六張做片，後面連戲的集數要用同一張 | 2026-11-01 在 RunPod 上用 Qwen-Image-Edit 畫的（route A session）；seed 依序 420012、420012、420000、420000、420012、420011。已知瑕疵：許大郎的斗笠偏大、周員外的帽子比瓜皮帽高、客棧角落留著幾個像酒瓶的東西 |
| 第 43 集的新圖：`refs-dh/xunkao-portrait-t1.png`、`weijiapu-portrait-t1.png` | 巡考（s27）、魏家家僕（s21；第 47 集唐小棠截他的信時還會出現）的定妝照。書吏 s15、s17 沿用第 42 集的 `registrar-portrait-t1.png` | 2026-11-01 雲端 session 在 RunPod 上用 Qwen-Image-Edit 畫的（`h3r.sh images`，20 步、CFG 4、空白 latent、1248×1664）。image 1 用書吏定妝照時兩人都抄了書吏的臉與山羊鬍；改用**場景圖** `set-haoshe-t1.png` 當 image 1（只取畫質，提示詞寫「not its place」）後臉才各自不同。巡考第一次是立領盤扣（清代、民國的樣子），改寫 round-collared yuanlingpao 才對。seed：巡考 430301、家僕 430202。各輪的 manifest 在 `production/colab/runs/e043/refs/` |
| 第 44–60 集的配角定妝照（2026-11-01）：`refs-dh/` 的 `xunbing`（巡兵，e044）、`shuliqi`（書吏妻，e045）、`yayi`（衙役，e046、e050、e051）、`weiguanjia`（魏管家，e048）、`baobang`（報榜人，e049）、`tongpan`（通判，e052）、`zhifufuren`（知府夫人，e052）、`xinchai`（信差，e055）、`shaonian`（少年，e056）、`jinjuntongling`（禁軍統領，e060），各 `-portrait-t1.png`。第 50 集的掌櫃 `zhanggui` 沿用第 42 集的 `innkeeper-portrait-t1.png`（同一間州城客棧） | 沒有定妝照的配角會變卡通（lessons §8）；`colab/runs/eNNN/extras.json` 用 `_scripts/extras_patch.py` 把它們接進片段 | RunPod Qwen-Image-Edit，image 1 用場景圖 `set-haoshe-t1.png`（第 43 集的做法），seed 440100／440101；書吏妻、信差第一輪是立領盤扣，第二輪寫交領繫帶（440200、440201）。manifest 在 `colab/runs/refs-e044-e060/` |
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
