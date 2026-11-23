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

| `refs/jianye-portrait-t1.png`、`jianbang-portrait-t1.png`、`xiaoman-portrait-t1.png`、`akai-portrait-t1.png` | 建業、建邦、小滿（制服）、阿凱（警察制服）胸像 | 2026-11-06 第一批（`refs-r2` round 1，各兩張選 t1；seed 623000、623002、623004、623006） |
| `refs/jianbang-home-t1.png`、`xiaoman-home-t1.png` | 建邦、小滿的 `home` | 以上面的胸像為 image 1、`latent: image1` 只換衣服（round 2，seed 624002、624003）；小滿是全身坐姿 |
| `refs/yuetang-18-huiyi-1948-t1.png` | 十八歲月棠民國三十七年的樣子（照片道具用） | 以十八歲基本款為 image 1 換裝（round 2，seed 624006） |
| `refs/yuetang-18-hand-wrinkle-t1.png` | `wrinkle`／`yaoju` 的右手背老人紋插鏡參考 | round 2（seed 624100）：右手背一片老人紋，戒指只在左手 |
| `refs/set-shenjia-yuanzi-t1.png`、`set-shenjia-huilang-t1.png` | 院子、迴廊 | round 1（院子 t1 seed 623100；迴廊原 t2 seed 623103） |
| `refs/prop-*.png` | 長明燈、老藥櫃、報信鈴、銀印戒、小銅油壺、備用銅鑰匙、祠堂插鎖、茶盤茶杯 | round 1，各一張（seed 623200 起） |
| `refs/xiaoman-damp-t1.png`、`yuetang-18-white-strand-t1.png`、`set-shenjia-chuantang-t1.png`、`set-shenjia-jiewai-t1.png`、`prop-fubo-yaoshichuan-t1.png` | 小滿 `damp`、月棠 `white-strand`、穿堂、臨街外觀、福伯的鑰匙串 | 2026-11-06 重畫（`refs-r3`，seed 625002、625003、625010、625012、625020）。白髮比一指寬粗一些，先用 |
| `refs/qianlaoban-`、`yuqin-`、`jiangmubai-`、`gaojingli-`、`zhiyuan-`、`zhixing-`、`hexiaoyang-`、`lindao-portrait-t1.png` | 第一章要的八個角色（bible〈先畫順序〉第 2 批） | `refs-r4`，各兩張選一（seed 626000 起）。玉琴（輪椅）、知遠、林導畫成全身、臉小，要重畫胸像 |
| `refs/set-shenjia-fanting-`、`chufang-`、`shufang-`、`xiaomanfang-`、`set-gongche-`、`set-gaozhong-xiaomen-t1.png` | 飯廳、廚房、書房、小滿房、公車、高中側門 | `refs-r4`（seed 626100 起）；公車與校門的提示詞另寫成白天、空的，不寫乘客與學生 |
| `refs/set-shenjia-citang-lamp4-t1.png`、`lamp5-t1.png` | 祠堂燈 4、燈 5 | 以燈 1 那張為 image 1、`latent: image1` 只改燈（seed 626200、626201），格局跟燈 1、燈 3 一樣 |
| `refs/zhiyuan-portrait-t1.png`、`yuqin-portrait-t1.png`、`lindao-portrait-t1.png` | 知遠、玉琴、林導重畫的胸像（取代 `refs-r4` 那三張全身） | 2026-11-07 `refs-r5`：`refs.py` 的胸像濾掉 jeans、sneakers、wheelchair、tall 等字之後重畫（知遠 t1 seed 627000、玉琴 t1 seed 627002、林導 t2 seed 627005；林導 t1 的相機背帶上有字，不用）。知遠仍是半身，臉夠大 |
| `refs/meifeng-home-t1.png` | 林美鳳 `home` | `refs-r5` t2（seed 627101），以基本款為 image 1、`latent: image1`。寫「house robe」兩次都畫成 V 領，改寫「扣到頂的緞面睡衣式上衣＋同色寬褲」，`cast.json` 與 shots-en 跟著改；畫出來是小翻領，不是立領 |
| `refs/jianye-home-t1.png` | 建業 `home` | `refs-r5` t2（seed 627103）。外貌改成「frown line … same colour as the rest of his skin」並明寫 no scar，兩張裡仍有一張（t1）畫成紅色刀疤 |
| `refs/yuetang-18-hand-faintline-t1.png` | `faint-line` 的右手背淺紋插鏡參考 | `refs-r5` t2（seed 627105）：以 `hand-wrinkle-t1` 為 image 1、`latent: image1`，只把老人紋淡成一道淺紋，戒指不動；第一次（從灰底畫、`latent: empty`）多畫了一枚戒指 |
| `refs/zhiyuan-shirt-t1.png`、`zhiyuan-coat-t1.png` | 知遠 `shirt`、`coat` | `refs-r6`（`refs.py looks`，以上面的知遠胸像為 image 1；shirt t1 seed 627200、coat t1 seed 627202）；t2 的臉偏掉 |

每一輪的 manifest、提示詞與進度檔在 `production/screen-test/runs/`（`<R>`、`<W>` 是工作資料夾）。
第 1 批（bible〈先畫順序〉）與第一章要的參考圖到 `refs-r6` 都齊了。

還原到工作資料夾：

```bash
mkdir -p ${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/tai-nainai/refs
cp docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/assets/refs/*.png ${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/tai-nainai/refs/
```
