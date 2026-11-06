# 《恁祖媽今年18》的共用參考圖

雲端 session 的工作資料夾不會留下來，所以每集都要、又重畫不出一樣結果的定妝照與場景圖放在這裡（照《種田》`production/assets/README.md` 的做法）。
`SHA256SUMS` 核對：在 `refs/` 裡跑 `sha256sum -c SHA256SUMS`。檔名就是 `tools/compile.py --manifest --refs` 找參考圖的規則。

| 檔 | 是什麼 | 從哪來 |
| --- | --- | --- |
| `refs/yuetang-18-portrait-t1.png` | 十八歲月棠基本款（月白立領布衫、一條辮子在右肩前）胸像，全季的主臉 | 2026-11-06 Colab Qwen-Image-Edit，`tools/refs.py portraits`，第一輪 t2（seed 620001），灰底當 image 1 |
| `refs/yuetang-18-shouyi-t1.png` | 十八歲月棠的 `shouyi`（壽衣） | 以上一張為 image 1、`latent: image1`，只換衣服（第二輪 t3，seed 622000）：臉跟基本款同一張 |
| `refs/yuetang-96-portrait-t1.png` | 九十六歲月棠 | 以十八歲基本款為 image 1 畫老（第二輪 t2，seed 622011）；看起來七十多歲，是模型的上限 |
| `refs/fubo-portrait-t1.png` | 福伯 | 第一輪 t2（seed 620005）；t1 畫成中山裝，不用 |
| `refs/meifeng-portrait-t1.png` | 林美鳳基本款 | 試鏡第一輪 `r1-meifeng-b`（seed 611004）；半身，不是胸像 |
| `refs/set-shenjia-citang-lamp1-t1.png`、`lamp3-t1.png` | 祠堂，燈 1、燈 3 | 第一輪 `lamp1-t1`（格局對、但是白天）為 image 1、`latent: image1` 改成夜裡與燈的分數（seed 622020、622021）。窗口還有一道光，當月光用 |
| `refs/set-shenjia-zhengting-t1.png` | 正廳 | 試鏡第一輪 `r1-set-zhengting-a`（seed 611010）；落地鐘的鐘面看得到（bible 要轉開），近景避開 |

每一輪的 manifest、提示詞與進度檔在 `production/screen-test/runs/`（`<R>`、`<W>` 是工作資料夾）。
還沒畫（bible〈先畫順序〉第 1 批）：建業、建邦、小滿、阿凱與各人的換裝，院子、迴廊、穿堂、臨街外觀，長明燈、老藥櫃、報信鈴、銀印戒與第 1 集的特寫道具。

還原到工作資料夾：

```bash
mkdir -p ${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/tai-nainai/refs
cp docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/assets/refs/*.png ${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/tai-nainai/refs/
```
