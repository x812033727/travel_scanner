# 榜單前 40 名短劇的漫劇改編企劃包（2025 前 20 ＋ 2026 1–10 月前 20）

站主（2026-10-28）要把 2025 全年與 2026 年 1–10 月紅果熱度前 20 名的短劇，各改編成一部
**原創**漫劇，每部都照《種田娶妻打天下》（[`../zhong-tian-qu-qi/`](../zhong-tian-qu-qi/README.md)）
的規格做，只有兩處不同：

| 規格 | 種田娶妻打天下 | 這 40 部 |
| --- | --- | --- |
| 規模 | 5 季 × 60 集 = 300 集，每季 6 篇章 × 10 集 | 同 |
| 單集 | 50–180 秒，篇章末 ≥ 120 | **90–180 秒**，篇章末 ≥ 120 |
| 鉤子 | 每集 3 個（前 3 秒、中段、結尾）彼此不同 | **每集 3–5 個**：同樣的三個，加可選的 `extra_hooks`（0–2 句），全部彼此不同 |
| 題材 | 穿越＋系統＋多妻＋種田 | **保留各劇自己的題材**（萌寶、重生、豪門、玄幻、年代……），只學它的套路結構 |

原創規則與原企劃一致：只學原劇的**套路**（人設結構、金手指形式、爽點類型、鉤子節奏）；人名、
世界、劇情、台詞全部原創，每部 README 都有「參考劇與原創聲明」。

## 目錄

```
rankings.json        40 筆：年份、名次、原劇名、平台、熱度、來源、原創劇名、進度
lib/validate.mjs     共用檢查器：node lib/validate.mjs <plan-dir> [--season N]
lib/build.mjs        共用產生器：node lib/build.mjs <plan-dir> [--check]
lib/validate.test.mjs
<year>-<rank>-<slug>/
  README.md          一句話、類型、規模、參考劇與原創聲明、季表、等站主決定
  reference.md       原劇的套路拆解（基本資料、前提、人設結構、金手指、爽點、鉤子節奏、要換掉的）
  plan.json          形狀同 zhong-tian-qu-qi/plan.json；episode_seconds 90–180、hooks_per_episode 3–5
  setting.json       世界、金手指規則與代價、15–20 位人物（真人外貌提示詞）、12 條謎團、調性、不黃標、顏值、畫面
  outline.json       5 季 × 6 篇章
  season-01.json … season-05.json   逐集細綱，欄位照 zhong-tian-qu-qi/authoring.md
  setting.md / outline.md / season-NN.md / episodes.csv   由 lib/build.mjs 產生，不手改
```

`lib/` 是把 `zhong-tian-qu-qi/validate.mjs` 與 `build.mjs` 一般化：目錄當參數，秒數與鉤子數從該目錄
的 `plan.json` 讀（沒有就用 50–180、3 個的舊規則），其餘規則一字不改；用它跑 `../zhong-tian-qu-qi`
結果和原檔一致。`zhong-tian-qu-qi/` 本身不動。

## 兩份榜單

數字單位是萬。2025 的來源是 DataEye《2025 年微短劇行業數據報告》第 32 頁的紅果 1–12 月峰值熱度
TOP20（同系列合併成一筆，去重後 16 部，第 17–20 名照同報告第 19 頁的 DataEye 熱力值榜補）。
**2026 沒有官方的 1–10 月累計榜**：這是把 DataEye 月報（4、5、6、9 月）、新浪 5/12 破億盤點、塔猴
7、9、10 月的紅果快照合併去重後排的；1、2、10 月沒有完整月榜，5 月只有日均熱度，兩種口徑不能直接比。
《十八歲太奶奶駕到》兩年都上榜，只列在 2025。每筆的來源網址在 `rankings.json`。

| 2025 | 原劇 | 熱度 | 目錄 | 2026 | 原劇 | 熱度 | 目錄 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 十八歲太奶奶駕到，重整家族榮耀 | 20164 | `2025-01-tai-nainai` | 1 | 萬妖圖錄傳 | 13700 | `2026-01-wanyao-tulu` |
| 2 | 夫人她專治不服 | 12567 | `2025-02-furen-bufu` | 2 | 穿書富家妯娌，我和閨蜜齊上陣 | 13203 | `2026-02-fujia-zhouli` |
| 3 | 盛夏芬德拉 | 12347 | `2025-03-shengxia-fendela` | 3 | 糟糕，和閨蜜一起穿越後把反派玩壞了 | 12428 | `2026-03-guimi-chuanyue` |
| 4 | 家裡家外 | 11989 | `2025-04-jiali-jiawai` | 4 | 少夫人來自東北 | 11884 | `2026-04-shaofuren-dongbei` |
| 5 | 千金謀 | 11334 | `2025-05-qianjin-mou` | 5 | 紅糖薑汁 | 11840 | `2026-05-hongtang-jiangzhi` |
| 6 | 金屋藏驕 | 10716 | `2025-06-jinwu-cangjiao` | 6 | 糯糯下山，師兄們都慌了 | 11400 | `2026-06-nuonuo-xiashan` |
| 7 | 念念有詞 | 10031 | `2025-07-niannian-youci` | 7 | 隱身侍衛 | 11243 | `2026-07-yinshen-shiwei` |
| 8 | 老公請和我戀愛吧 | 9943 | `2025-08-laogong-lianai` | 8 | 錯嫁有喜 | 10803 | `2026-08-cuojia-youxi` |
| 9 | 荒年全村啃樹皮，我有系統滿倉肉 | 9893 | `2025-09-huangnian-xitong` | 9 | 八零辣妻，揣著四寶撩夫 | 10799 | `2026-09-baling-laqi` |
| 10 | 半熟老公 | 9817 | `2025-10-banshu-laogong` | 10 | 豪門月嫂，一不小心成了全家白月光 | 10715 | `2026-10-haomen-yuesao` |
| 11 | 雲渺（我修仙多年強億點怎麼了） | 9730 | `2025-11-yunmiao` | 11 | 那年冬至 | 10654 | `2026-11-nanian-dongzhi` |
| 12 | 朝陽似我 | 9590 | `2025-12-zhaoyang-siwo` | 12 | 曼陀羅 | 10638 | `2026-12-mantuoluo` |
| 13 | 馴野 | 9575 | `2025-13-xun-ye` | 13 | **done**：5 季 300 集，validate 零錯誤 | 10509 | `2026-13-zhouyi-jiye` |
| 14 | 只為佔有你 | 9305 | `2025-14-zhiwei-zhanyou` | 14 | 姐，他真是我姐夫 | 9588（日均） | `2026-14-jiefu` |
| 15 | 幸得相遇離婚時 | 9298 | `2025-15-xingde-xiangyu` | 15 | 時光和你都很美 | 9359（日均） | `2026-15-shiguang-heni` |
| 16 | 傅爺的小青梅又颯又美 | 9240 | `2025-16-fuye-qingmei` | 16 | 掃黑 | 9216 | `2026-16-saohei` |
| 17 | 小小球神不好惹（補位，熱力值） | 9074 | `2025-17-qiushen` | 17 | 重生！醜小鴨逆襲成了萬人迷 | 8922 | `2026-17-chouxiaoya` |
| 18 | 人面桃花長相憶（補位） | 6768 | `2025-18-renmian-taohua` | 18 | 拆CP不成，反成爸媽心尖寵 | 8386（日均） | `2026-18-chai-cp` |
| 19 | 好孕甜妻被鑽石老公寵上天（補位） | 6059 | `2025-19-haoyun-tianqi` | 19 | 大唐憨婿之我姐姐是太子妃 | 8264 | `2026-19-datang-hanxu` |
| 20 | 家庭煮夫（補位） | 5945 | `2025-20-jiating-zhufu` | 20 | 發配邊關，罪妻開荒養出戰神 | 8251 | `2026-20-fapei-bianguan` |

## 進度

一部一張看板票（`tasks/open/2026-10-28-top40-<目錄名>.md`），scope 只有那部的目錄，所以多個 session
可以同時各寫一部。每部的進度寫在 `rankings.json` 的 `status`（reference → setting → outline → s01 … s05 → done）
與它的票裡；下表由人更新。

| 目錄 | 原創劇名 | 進度 |
| --- | --- | --- |
| `2025-01-tai-nainai` | 祖奶奶今年十八 | **done**：5 季 300 集逐集細綱齊，validate 零錯誤 |
| `2026-01-wanyao-tulu` | 百妖食單 | **done**：5 季 300 集逐集細綱齊，validate 零錯誤 |
| `2025-02-furen-bufu` | 少奶奶不好惹 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-02-fujia-zhouli` | 我們穿進了自己審的稿 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-03-shengxia-fendela` | 合約到期前 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-03-guimi-chuanyue` | 我和我媽穿去亡國 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-04-jiali-jiawai` | 海風吹進門 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-04-shaofuren-dongbei` | 租來的女朋友不想退租 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-05-qianjin-mou` | 她的當鋪不談愛 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-05-hongtang-jiangzhi` | 薑茶要趁熱 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-06-jinwu-cangjiao` | 她養的小白臉是世界冠軍 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-06-nuonuo-xiashan` | 小糰糰找哥哥 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-07-niannian-youci` | 我老公不說話，但我話很多 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-07-yinshen-shiwei` | 保鏢只想吃飽 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-08-laogong-lianai` | 醒來八年後，我老公是我死對頭 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-08-cuojia-youxi` | 傻姑娘嫁對了人 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-09-huangnian-xitong` | 全村餓肚子，我家飄肉香 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-09-baling-laqi` | 鐵漢的便當太太 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-10-banshu-laogong` | 契約第七條：不談感情 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-10-haomen-yuesao` | 住進唐家的治療師 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-11-yunmiao` | 茶館老闆娘活了兩千歲 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-11-nanian-dongzhi` | 冬至那天我嫁給了倒數的人 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-12-mantuoluo` | 瀾港的帳，一筆都不能是他給的 | **done**：5 季 300 集，validate 零錯誤 |
| `2026-13-zhouyi-jiye` | 四樓的燈整夜都亮 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-12-zhaoyang-siwo` | 晨光落在第七張圖 | outline；五季細綱代理撰寫中 |
| `2025-13-xun-ye` | 她簽下的那個搬家工 | **done**：5 季 300 集，validate 零錯誤 |
| `2025-14-zhiwei-zhanyou` | 他只是我的光替 | outline；五季細綱代理撰寫中 |
| `2025-16-fuye-qingmei` | 八歲那年，我管過首富 | outline；五季細綱代理撰寫中 |
| `2025-18-renmian-taohua` | 他站在我身後三步 | outline；五季細綱代理撰寫中 |
| `2026-14-jiefu` | 預報說我會嫁給他 | outline；五季細綱代理撰寫中 |
| `2026-17-chouxiaoya` | 重生後，我裁掉了她的濾鏡 | outline；五季細綱代理撰寫中 |
| `2025-17-qiushen` | 球王回來時九歲 | outline；五季細綱代理撰寫中 |
| `2025-15-xingde-xiangyu` | 婚約到他判刑那天為止 | outline；五季細綱代理撰寫中 |
| `2026-15-shiguang-heni` | 退婚前，我先把大神追到手 | outline；五季細綱代理撰寫中 |
| `2026-16-saohei` | 潮汐帳 | outline；五季細綱代理撰寫中 |
| `2026-18-chai-cp` | 我媽十八歲，我十七歲 | outline；五季細綱代理撰寫中 |
| `2026-19-datang-hanxu` | 全京城都說我憨，只有我姊不信 | outline；五季細綱代理撰寫中 |
| `2025-19-haoyun-tianqi` | 我兒子在戶政門口徵爸爸 | outline；五季細綱代理撰寫中 |
| `2026-20-fapei-bianguan` | 半袋糧認下的媳婦，把邊關種綠了 | outline；五季細綱代理撰寫中 |
| `2025-20-jiating-zhufu` | 三年期滿，我收回岳家的風光 | outline；五季細綱代理撰寫中 |
| 其餘 0 部 | 未定 | reference（套路拆解） |

## 每部怎麼做

1. 讀 `reference.md`，決定要保留哪些套路、換掉什麼。
2. 取 3 個原創劇名候選寫進 README，先用第一個。
3. `plan.json` → `setting.json` → `outline.json`，每一步用 `lib/validate.mjs` 擋結構。
4. `season-01.json` 起逐季寫，一季一次 `--season N`；寫完就 `lib/build.mjs`、commit、push、在票裡記進度。
5. 五季齊、整體 validate 零錯誤、`build --check` 乾淨 → 票 done，更新 `rankings.json` 與上表。

## 檢查

```bash
node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/<dir>
node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/<dir> --check
node --test docs/videos/series-plans/top40-2025-2026/lib/validate.test.mjs
npm run check:tasks
```

`validate.mjs` 只檢查結構與規則，不能證明真人看了會不會停不下來；每部第一篇章上架後要用留存曲線驗證。
