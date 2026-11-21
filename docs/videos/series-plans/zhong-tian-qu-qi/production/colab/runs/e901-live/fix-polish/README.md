# 第 1 集真人版 fix-polish：上架前精修重拍（2026-11-21）

站主 2026-11-21 決定審片列 A、B 的鏡全部重拍。第 1 集在 `review-zt/consolidated/retakes.json` 有 7 鏡，全是 B（濃縮版報告沒寫原因，
原因是看畫格條 `review-zt/ep/e001/review/shots/sNN.jpg`、證據格 `x/`、`e901-live/review-picks.tsv` 與 `fix*/review-picks.tsv`、`cut-review-2.md` 後補上的）。

- 種子 9019101、9019102；960×544 Ref2VA；7 鏡 14 支，共 96 秒。
- base：`picks.json` 每鏡 `draft` 所在的資料夾（d1、fix1、fix4）裡、同種子的 `prompts/ref-sNN-SEED.txt`。第 1 集的 d1 提示詞檔名也帶種子，`st1*` 不用找。
- 產生：`python3 -I ../../_scripts/polish-build.py 1` → `~/mokaair-work/videos/zhong-tian-qu-qi-e901-dh/runpod/live/fixp/`。
- 只送 B 級（沒有 A）。台詞一字沒改；s13、s04、s08b 與 s14 前段是錄音或系統聲，畫面上維持嘴閉、臉埋或背對。

| 鏡 | 審片問題（現在那支） | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s04 | 氣泡像兩顆黏在鼻孔與嘴上的金屬玻璃球；頭髮仍是整齊髮髻 | `d1/…/ref-s04-9011102.txt`，6 秒 | 構圖：補「臉在畫面中間、閉眼、嘴閉著」，「long black hair loose」→「髮髻在水裡散開、髮絲飄在臉頰額頭旁」。動作：「a burst of silver bubbles」→「一串很多顆豌豆大小、像河水裡真正空氣的透明小氣泡，從嘴往上晃過鼻子額頭出畫，後面還跟著一串」；手往上抓照舊，改成「同時」 | 不換 | 外貌錨句與三張圖都是束髮，文字壓不過圖（教訓：髮型照圖畫），髮絲可能還是只散幾縷 |
| s08b | 看起來沒濕：袍子乾、髮髻整齊、沒有滴水；景別偏全身 | `d1/…/ref-s08b-9011101.txt`，8 秒 | 構圖：「soaked through … water dripping from the ends of his hair」→「胸上中近景；像剛從河裡撈上來：袍子吸水變深石板藍、濕布發亮貼在肩胸手臂上、濕髮發亮貼在額頭臉頰、河水從臉頸流下、下巴與髮梢滴水」。動作：「looks down at his soaked sleeves … turns them over」→「低頭看濕袖，再把兩手舉到胸前慢慢翻成掌心朝上，兩邊袖口流下一道水、指尖滴水；眉頭因困惑皺起、嘴一直抿著」 | 不換 | 三張許硯圖都是乾的，濕度可能仍不夠；胸上景別讓翻掌心時手要舉進畫面 |
| s13 | 草兔畫成稻草球；小禾側臉露出（台詞是錄音）；許硯沒退半步 | `d1/…/ref-s13-9011102.txt`，6 秒 | 構圖：兔子「a small straw-woven rabbit, plaited from pale yellow straw」→「巴掌大、淡黃稻草編的兔子，兩隻直立的草耳、圓草頭、兩顆深色種子做的眼睛，塞在腰帶前面」。動作：「face buried … hidden to the end」→「整張臉壓進他袍子前面，此後到最後一格只看得到後腦與紅繩辮子」、兔子留在腰帶；「he rocks back half a step」→「被撞得退半步、低頭看她頭頂、眉毛驚訝地抬起」；二牛「留在門邊半身、嘴閉著」 | 不換 | 一鏡三人、多拍（跑、抱、退步）；畫格條裡屋子已對，主要賭兔子的樣子 |
| s14 | 身後是開著的門與屋外村景、木柱，不是分鏡的「只有土牆和水缸」；兔子像布偶玩具 | `fix1/…/ref-s14-9011201.txt`，10 秒 | 場景句：「the plank door on screen left, a big clay water vat on screen right」→「門在左牆、水缸靠後牆」；構圖加「鏡頭面向屋子後牆」、小禾「背對鏡頭」，「behind them only the earthen wall」→「身後只有光禿的土磚牆與靠牆的大圓陶水缸，被斜照的晨光照著」；兔子同 s13 寫死。動作：前四秒「lips stay closed」→「嘴抿著」，加「眉頭放鬆」；說話句補「turned toward her … eyes on the top of her head」（gaze 規則） | 不換（`set-xujia-wu-l1` 本來就只有牆、窗、桌、缸，沒有門） | 門的位置只寫在場景句，模型若又把門畫在畫左背景就仍會看到屋外；現片 3.5 秒開口、到 9.2 秒，10 秒夠 |
| s23 | 趙捕頭第一格正面對鏡頭露齒笑；阿令開頭抬頭直視鏡頭；秦霜、阿令並排 | `fix4/…/ref-s23-9011502.txt`，6 秒 | 構圖：趙捕頭加「身體轉向畫左、四分之三側面，對著畫外左的許硯」；兩女「一前一後排成一列：秦霜在前、多半步、眼睛看畫外左的許硯；阿令在她後面一整步、半個人藏在秦霜肩後、從第一格起下巴收到胸前、看腳下的土、頭頂朝鏡頭」，「iron shackles … short iron chain」→「iron cuffs … short hanging iron chain」。動作：「gives a cold smirk … sweeping his arm」→ 說話句補 gaze，冷臉逐部位寫（一邊嘴角往上抿成一條細線、細眼往旁斜、眉低而硬），「說完才往旁邊跨一大步，露出院門口的兩人」；拿掉甩手臂與「兩手空著」，秦霜只寫「下巴抬著」 | 不換 | 秦霜柴刀依定案接受（拿在手上也算過）；阿令有三張圖都是平視的胸像，第一格低頭靠文字 |
| s28 | 紅紙是手掌大的長方小紅箋、上面有一直行一直行的深色字（例如 187.4 秒）；前後鏡 s21、s29 是一大張空白紅紙 | `fix4/…/ref-s28-9011501.txt`，6 秒 | 改成審片建議的過肩鏡：「low-angle close-up of Constable Zhao wearing exactly one … cap … opened red paper gripped in his right fist at his chest」→「稍低角度、從許硯背後的過肩近景：左前景是許硯的左肩與束髮後腦、背對鏡頭；趙捕頭在畫右、離他一臂、帽上留空、身體四分之三轉向許硯、細眼斜著盯許硯、嘴角下撇、左手拿著連鞘佩刀；右手垂在身側的一大張紅紙，報紙那麼大、比肩寬，朝鏡頭那面整片均勻空白的紅」；身後「天空與秋枝」→「竹籬笆與掛紅果的禿柿子樹映著亮天」；「He is the only person」→「Only these 2 people」。動作：說話句補 gaze，「his right fist keeping hold of the red paper」→「那張大紅紙仍從右手垂著打開」，「leans … off screen left」→「斜眼瞪著往許硯探身」，補「許硯背對鏡頭不動、看不到嘴」。header 改成 5 張圖、加許硯錨句（照 s22） | 加 `xuyan-portrait-l1`、`xuyan-angle-a-l1`、`xuyan-angle-b-l1`（同 s22），共 5 張 | 紙上長字是這集反覆出的錯，只能靠「blank」「均勻的紅」；紙垂在身側比握在胸前不容易被拿近看。過肩讓許硯入畫，分鏡原本是趙捕頭單人低角度近景（審片改寫句要過肩，照審片） |
| s32 | 唐小棠一路正面走向鏡頭、對鏡頭喊；趙捕頭往院子裡走而不是出院門 | `d1/…/ref-s32-9011102.txt`，6 秒 | 構圖：「full shot through the yard gate in the foreground」→「從院子裡斜拍：鏡頭站在柴堆旁，斜看向畫右開著的院門，小轎停在院門外的巷子」；唐小棠加「臉朝畫外左的許硯一行人」；趙捕頭「在院門口往巷子走出去」。動作：說話句補 gaze（四分之三側臉、眼睛越過鏡頭左邊看他們、never looking into the lens）與「甜、明亮的中音域說話聲，興奮但放鬆」；「walking briskly in through the gate」→「往畫左快步走進院門、朝畫外左的人高高揮手」；「strides past her … leaves the frame」→「從她肩旁走出院門進巷子、從畫右出畫」 | 不換 | 跟拍運鏡可能把鏡頭轉到她正面；聲音音高（s32 356 Hz 對 s34 約 210 Hz）只能用文字試，挑片時要量 |

## 三個檢查（2026-11-21）

- `polish-build.py 1`：0 錯，7 鏡 14 支 96 秒。
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error、0 warning。第一次跑 s23 有 `unpictured Xu Yan` 與 `four`（「eyes on Xu Yan, never looking」那句沒寫 off screen，被算成畫面上的人），改成「eyes on him」後清掉。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error、0 warning。

## 挑片時看

- s04：氣泡是不是一串小氣泡、有沒有黏在臉上；第 0 格是不是就是臉。
- s08b：濕不濕（袍子顏色、頭髮、滴水）；兩句都嘴閉。
- s13、s14：兔子有沒有耳朵和臉、在不在小禾腰帶上；s14 身後有沒有門與屋外；s14 前 4 秒嘴閉。
- s23：阿令第 0 格起低頭；趙捕頭有沒有對鏡頭笑。s28：紙的大小與有沒有字（放大看）、許硯有沒有轉頭露臉。s32：她有沒有看鏡頭、趙捕頭往哪走、音高。
