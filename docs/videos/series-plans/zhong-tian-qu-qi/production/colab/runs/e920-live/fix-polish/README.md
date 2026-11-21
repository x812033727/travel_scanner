# 第 20 集真人版 fix-polish：上架前精修的重拍提示詞（A＋B 共 5 鏡）

2026-11-21。依據：`review-zt/consolidated/retakes.json`（e020 的 A：s01、s37b、s33；B：s10、s15）、完整審片報告 `review-zt/reports/e020.txt`（第二節第 2–6 項）、
畫格條 `review-zt/ep/e020/review/shots/`、`x/m_s10_12_34.jpg`；分鏡 `docs/videos/zhong-tian-qu-qi-e020-r2/script.md`（〈真人版的改動〉〈審稿後的修改〉）。
只寫提示詞與 spec，沒有送出任何工作。種子 9209101、9209102，960×544 Ref2VA，每鏡兩支，共 10 支、58 秒。

**base 怎麼找的**：`_live-e920/zhong-tian-qu-qi-e920-dh/picks.json` 的 `seed` 與 `motion_from`：s01（d1，9201102）、s10（d1，9201101）、s15（d1，9201102）、
s33（fix1，9201201）、s37b（fix1，9201201），提示詞在 `runpod/live/<motion_from>/prompts/ref-sNN-SEED.txt`（d1 這幾鏡沒有不帶種子的 `ref-sNN.txt`）。
提示詞用 scratchpad 的小程式從 base 逐句替換（每個舊句在 base 裡恰好出現一次），不是重打。

**整集共用的寫法**：只用正面描述；冷臉、怕的臉逐部位寫，加「到最後一格都不笑」；說話的人臉朝對方；一鏡一個身體動作；道具寫用身體比的大小；
不引用台詞片段（只在說話句出現一次原句）。秦霜腰帶照稿子空著（「不拍兵器」），本次五鏡都沒有柴刀。

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊 → 新，簡述） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- | --- |
| s01 | A | 開場第一句整句咧嘴笑（0.4–1.0 露齒、1.3–2.0 抿嘴笑、3.1 又笑） | `d1/prompts/ref-s01-9201102.txt`（6 秒） | 表情 `certain and steady: brows level, eyes warm and firm` → `grave and resolute`：眉壓低往中間、眼睛定在她身上、下顎咬緊、句間嘴抿成直線、嘴角往下＋`no smile at any moment, not even at the end of the shot, until the last frame`；右掌第一格撐在瓦上；「抬手、放膝、坐直、然後才說」→ 開口時同一個慢動作把手收到膝上坐直；說話句加「低聲、篤定」與每個字都眉低下顎緊；收尾「眼睛看她」→ 嘴閉成直線、眉仍壓低、整張臉凝重到最後；畫右緣寫成只有暗瓦與夜空（d1 兩支前 2 秒右緣露出唐小棠的臉） | 照 base（只送 `xuyan-angle-a-l1`，正經的那張） | 肩上的破洞亮（審片附帶提到）沒處理：外衣句照 base，改了怕跟 s02、s03 不連戲。音量是模型原聲，「低聲」只是盡量；剪接仍要照審片〈請站主聽〉降。 |
| s37b | A | 唯一的臉：西式飾板牆、算盤比肩寬（約 17 檔）、珍珠簪＋垂胸長緞帶、大袖對襟加抹胸、臉偏 CG | `fix1/prompts/ref-s37b-9201201.txt`（6 秒） | 背景 `the plain white panelled wall`（panelled 長成護牆板）→ 白灰泥牆、直立深色木柱、一角空的深色木架；算盤 `long flat … as long as her forearm … long narrow … long row of rods` → `small flat gold abacus only as long as her hand from wrist to fingertips`、短一排桿、兩手蓋住兩個短邊、抱在胸口正中、「畫面裡唯一一把」，櫃檯放到畫框下緣外（fix1 前段櫃面上多一把）；外貌句拿掉 `pearl pins`、`flowing sleeves` → `close-fitting sleeves`；衣服加「兩片前襟交疊闔上」；加門口來的冷藍暮光、`real skin texture`；結尾加到最後一格不笑 | 照 base（定妝照、角度 a、`prop-jinsuanpan-l1`）。沒加鋪子黃昏圖：近景送整間鋪子會拉成全景（d1 前段就是全身遠景） | 兩張定妝照本身就有珍珠簪與長緞帶，文字可能壓不過（站主曾接受長緞帶）；換掉圖會丟臉，沒換。算盤改小跟 `review3-plan.md` 寫給第 21 集 c01 的「前臂長的大把」衝突：若這鏡換上新片，第 21 集 c01 也要改成手掌長。臉的 CG 感只能靠挑片。 |
| s33 | A | 2.5 秒起轉正、眼睛直視鏡頭說「二牛…」，臉型變寬像另一個演員；句子切成五段；後景阿令深色裙圍裙紅桶；櫃檯後空 | `fix1/prompts/ref-s33-9201201.txt`（6 秒） | 構圖「許硯單獨、右前景櫃檯近端空著」→ 畫右緣櫃檯近端後面加唐小棠的背影（只有兩顆粉緞帶丸子與一邊粉肩、整鏡背對，照 d1 s31／s32 的背影句，不點名、不送圖），大門寫在他身後左邊；他四分之三側臉朝畫右對她說前半句、點一下頭，後半句「越過左肩轉頭、側臉朝畫左身後的大門」喊，側臉留到最後；拿掉 `straightens up`（一鏡一個轉頭）；說話句加「一口氣說完」；阿令 `plain grey-white cotton dress` → 從脖子到腳踝的米白長布裙、`unpainted pale wooden bucket`；人數改「恰好三人」並逐一點出兩個年輕女子的差別 | 照 base（許硯定妝照、角度 a、`set-xuji-pu-eve-l1`） | 加唐小棠背影是審片改寫句要的（給他視線的對象），但 d1 正是在這個位置畫出第二個阿令；兩個不點名的年輕女子靠衣色髮型分，挑片要逐格看分身。斷成五段是模型原聲的節奏，提示詞只能寫「一口氣」。 |
| s10 | B | 擠滿人的店一刀變空店；秦霜站店中央對左牆紙架喊、平掌揮向架子；不在門檻、不是低角度 | `d1/prompts/ref-s10-9201101.txt`（6 秒） | 構圖「門口幾個人的背影」→ 從人群背後腰高的低角度：前景左右五六個宋代衣著客人的背與肩、中間留空隙；秦霜站在大門中間門洞、門檻內一步、背對我們四分之三；她看的方向 `profile to screen left toward the street outside the doorway at the left`（模型讀成店裡左牆）→ 側臉朝畫左、看門外左邊門洞外街上的六個深藍灰宋代短打年輕人（照 s11 的寫法）；表情加眉壓低、瞇眼盯著他們、到最後不笑；動作「踏上門檻＋揮手＋旁人退後」→ 右靴重重踏上石門檻、平掌往門外朝他們一揮，收在手仍伸向街上（拿掉旁人退後） | 照 base（`qinshuang-portrait-l1`、`set-xuji-pu-l1` 早上原圖） | 背對四分之三＋側臉，嘴只看得到一半，原聲對嘴要挑片時看；前景人群可能擋住她。二牛本人沒寫進畫面（六個年輕人只寫深藍灰，避免多一個沒圖的點名人物）。 |
| s15 | B | 門外街與馬車像 3D 遊戲、只有一匹馬；3.5 秒後燈籠變四盞 | `d1/prompts/ref-s15-9201102.txt`（5 秒） | 「the location shown in <Picture 1> is the set」→ 圖只當近處的地面；門柱、對街、馬車全用實拍質感寫（實地拍攝、底片顆粒、磨舊的門柱、風化的白灰牆、磨舊石板、刮痕的黑漆木車、厚布簾、真的馬毛與呼氣）；`two black horses` → `exactly two black horses harnessed side by side`；燈籠 → 「整個畫面恰好兩盞」，對街屋簷寫 `bare edges`；動作改成兩匹馬先走進門洞、車輪在石板上轉，出畫時仍恰好兩盞；補上 `…never the mood. ` 分隔句（base 沒有，polish-build 要求恰好一次） | `set-xuji-pu-l1` → **`set-xuji-pu-floor-pm-l1`**（午後地磚光條裁切）。整間鋪子圖門洞外那條街本身就是平塗的 CG 街，d1 照著放大；稿子〈審稿後的修改〉要的 pm 調色版也是同一條街，所以不送整間 | 拿掉鋪子圖後，門柱與格子板只靠文字，可能跟 s14、s16 的門洞長得不一樣；地磚圖可能讓畫面下半太多地面。兩支都不行的退路仍是審片的「剪到 2.2 秒＋馬蹄、低音開大」。 |

## 檢查（2026-11-21）

```bash
cd /home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs
python3 -I _scripts/polish-build.py 20          # e920: 5 shots, 10 drafts, 58 s
python3 -I _scripts/preflight-prompts.py /root/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/runpod/live/fixp/colab-jobs.json
cd /home/user/zt-work && bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest /root/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/runpod/live/fixp/colab-jobs.json
```

- `polish-build.py 20`：0 錯，5 鏡、10 支、58 秒。
- `preflight-prompts.py`：0 error、0 warning。
- `h3r.sh check`：0 error、0 warning。
- 另外掃過新提示詞：smile／grin 只出現在 `no smile at any moment…`；pearl、forearm、long gold、sword、knife、cleaver 都沒有；`panelled` 只剩 s10、s33 的鋪子場景句（照 base，全景與鋪子圖一致）；`warm` 只用在光；台詞原句各只出現一次；兩個分隔字串各一次。

## 拍完之後要看的

- s01：逐 0.5 秒看嘴角（尤其 0.4–1.0、1.3–2.0、3.1 秒相對位置與句尾）；右緣有沒有唐小棠。
- s37b：算盤大小與數量（前 1 秒左下角）、牆、髮飾；挑定後重做封面（審片第 3 項）。
- s33：畫面裡是不是恰好兩個年輕女子、後角那個有沒有出門；後半句是不是側臉朝大門、沒有轉正。
- s10：她是不是在門檻上、揮手方向是不是門外；前景人群有沒有擋到臉。
- s15：馬的數量、燈籠數量、門柱樣子能不能接 s14／s16。
