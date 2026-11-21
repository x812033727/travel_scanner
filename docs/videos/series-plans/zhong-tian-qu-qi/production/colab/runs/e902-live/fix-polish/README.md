# 第 2 集真人版 fix-polish：上架前精修的重拍提示詞（A＋B 共 8 鏡）

2026-11-21。依據：`review-zt/consolidated/retakes.json`（e002 的 A、B）、完整審片報告 `review-zt/reports/e002-full.txt`、
畫格條 `review-zt/ep/e002/review/shots/`、`x/`；分鏡 `docs/videos/zhong-tian-qu-qi-e002-r2/script.md`（c01–c40 與〈2026-11-06 審稿後的修改〉）。
只寫提示詞與 spec，沒有送出任何工作。種子 9029101、9029102，960×544 Ref2VA，每鏡兩支，共 16 支、108 秒。

**base 怎麼找的**：`_live-e902/.../picks.json` 沒有 `motion_from` 欄位，改從每鏡 `draft` 的路徑讀出資料夾與種子（d1、fix1、fix3），
提示詞就是同資料夾 `prompts/ref-sNN-SEED.txt`。d1 同一鏡兩個種子的提示詞相同。

**整集共用的改法**
- 秦霜的刀：舊寫法 `one old chopping knife with a narrow iron blade as long as a forearm, a thick back…` 每次都長成劍或長刀（s21、s24 有護手長鞘；s06、s17 是大彎刀）。
  第 2 集裡唯一畫對的是 s23（短寬、裸刃插在腰帶上）。新句：`one old firewood cleaver, a short wide squared iron blade one foot long and as wide as her palm, with a thick dark back, a bright edge and a short wooden handle wrapped in black cloth, its bare blade pushed through the right side of her wide leather belt, the short black handle up at her right hip`。
  只用正面寫法，沒有寫 sword、scabbard、hand guard（審片改寫句裡的 `no sword, no scabbard, no hand guard` 是否定名詞，沒照抄）。
- 斧頭（s19、s21、s22）：`the one wood axe, a pale wooden handle as long as an arm and one wedge-shaped dark iron head with a single cutting edge on one side and a flat blunt back on the other`，跟 s17 的單刃斧一樣。
- 錄音鏡（s22、s30）維持錄音：說話的人背對、嘴不入鏡，畫面上其他人嘴閉著；拿掉 base 裡引用的台詞片段（「妳哥嘛」「太狠了吧」），免得模型照著開口。

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- | --- |
| s19 | A | 單手一刀不成立：左手握斧柄、刀舉出畫面上緣後沒再回來、木頭自己裂開 | `fix3/prompts/ref-s19-9021401.txt`（6 秒） | 側面、只拍肩膀以下、斧柄朝鏡頭外 → 膝高低角度全景、靴到頭頂上方都在畫內、頭上留大片空；斧頭寫成照 s17 的單刃斧，斧柄斜向畫左、柄尾擱在木墩左緣、離她遠；柴刀第一格就舉在右肩上方、整把在畫內；動作加「腰一擰、只用右手一刀、刀身一路看得到」，斧頭從中間掉進泥地；左拳從第一格到最後一格插腰；冷臉逐部位寫 | 照 base（秦霜定妝照、院子 l2） | 全景時秦霜的臉小，冷臉可能看不清；模型仍可能讓左手去碰斧柄（斧柄已移到離她最遠的一邊）。base 的剪點是 start 2.2，新片劈下應在前 2 秒，挑片時重量 |
| s24 | A | 腰間是有護手、黑長鞘的劍 | `fix1/prompts/ref-s24-9021201.txt`（6 秒） | 只換刀的描述（窄刃一前臂長 → 短寬方頭、裸刃插腰帶右邊、黑布柄在右胯），結尾「the knife stays in her belt」→「the short wide cleaver stays in her belt at her right hip」；台詞、轉身、回頭斜眼、NOSMILE 不動 | 照 base | 定妝照沒有刀，刀完全靠文字；第二輪還像劍的話照 WRITING 第十一節改設計（讓刀在身體另一側不入鏡） |
| s21 | B | 秦霜腰前長刀長鞘；小禾拖的是雙刃斧 | `d1/prompts/ref-s21-9021102.txt`（6 秒） | 刀描述換新句；斧頭「a dark iron head」→ 單刃楔形、平鈍斧背；「the iron head hanging at her knees」→「the single-edged iron head…」；結尾加「the cleaver in her belt」；運鏡照 base（固定） | 照 base | 審片改寫句要秦霜「把柴刀插回腰帶」（分鏡 c21），沒寫：一鏡兩人各一個動作，插刀這個動作最容易把刀畫成長鞘；改成第一格就插在腰帶上、她抱胸不動。s19 結尾刀在她手上、s21 已在腰帶，中間由剪接帶過 |
| s22 | B | 秦霜錄音在講，動嘴的是小禾；秦霜背對 | `d1/prompts/ref-s22-9021102.txt`（6 秒） | 拿掉「小禾噘嘴」「on 「妳哥嘛」… 憋笑」→「嘴唇整鏡抿著不動，只用眉眼演：斧頭被拿走時眉往下、眼睛跟著斧頭、肩膀垮一下，再抬眼、眼睛彎起來」；「Qin Shuang crouches」→ 第一格已單膝蹲好（轉換動作不放開頭）；木屑寫在辮子上；刀、斧換新句 | 照 base | 審片建議改成秦霜四分之三側臉說話（變成原聲鏡），但這鏡是錄音，照 brief「錄音鏡維持嘴閉著或背對」沒改。若站主要看到秦霜的臉，要改成原聲：提示詞加她的台詞，聲音也換成片段原聲 |
| s03 | B | 台詞「三位姑娘」畫面只有兩位；紅紙卷握在手上沒塞腰帶 | `d1/prompts/ref-s03-9021101.txt`（8 秒） | 加阿令的外貌錨句（`<Picture 8>`）與位置：井邊最後一個、低頭看地、袖子蓋手腕、嘴閉；「beyond them A-ling stays off screen」→「exactly three women in a row…」＋「Exactly one Qin Shuang, one Tang Xiaotang and one A-ling; only these 4 people」；紅紙「右手拿著」→ 第一格就直插在腰帶左邊、兩手空著（塞的動作放開頭會被跳過）；中景 → 膝上中遠景、頭上留空；跟拍 → 固定鏡（四人同框跟拍容易把阿令推出畫）；場景句縮短（字數 990）；刀換新句 | 加 `aling-portrait-l1.png`（第 8 張），場景圖改第 9 張；共 9 張 | preflight `four`（4 個有名字的人）保留：台詞就是對三位說，三位都要在畫面上，第 1 集 s38 三人同框也接得上。風險是分身或阿令抬頭直視；阿令只給一張定妝照、站最遠、低頭。剪接後要重看 s03 的 crop（base 有 `880:495:0:25`）與紅紙在 s05、s13b 仍握在手上的不連戲（不在這次範圍） |
| s30 | B | 唐小棠走出院門、站到錢員外身邊對他笑；閉嘴側臉時錄音還在講 | `d1/prompts/ref-s30-9021101.txt`（8 秒） | 跟拍 → 固定鏡（跟拍把她帶到錢員外身邊）；構圖寫錢員外在院門口、隔五大步空地；唐小棠開頭在左框外，走進來停在許硯右邊、並肩、留到最後一格，整鏡背對、臉朝錢員外；拿掉「on 「太狠了吧」」改成單純的時刻描述 | 照 base | 她整鏡背對，觀眾看不到「不笑」的臉，但這是錄音鏡，背對最保險；審片要的四分之三側臉同樣需要改成原聲鏡，沒改 |
| s01 | B | 全片第一格是現代黃銅掛鎖、鉸鏈手銬、現代鑰匙 | `d1/prompts/ref-s01-9021101.txt`（6 秒） | 「square iron padlock」「key」→ 宋代鐵匠打的兩個粗黑鐵環＋短鐵鍊，一根圓頭長鐵栓橫穿兩環；趙捕頭的手捏住鐵栓頭、一拉抽出，鐵環連鍊掉在畫面下方泥地、留到最後；袖口寫 Song-dynasty；勒痕、舊疤、拉袖照 base | 照 base | 分鏡寫「鑰匙插進鎖孔一轉」，這裡改成抽鐵栓：只要寫 lock、key 模型就畫掛鎖與現代鑰匙（審片改寫句的 bar lock＋flat key 同樣有這個風險）。動作意思一樣（官府的人卸下鐵鐐），台詞是畫外錄音，不受影響；站主若堅持鑰匙要再議 |
| s06 | B | 換了地方（柴牆、花田）、木柴不連戲（淺色方柴 → s07 深色帶皮圓木）、秦霜右手握大菜刀、許硯沒往後跳 | `d1/prompts/ref-s06-9021101.txt`（8 秒） | 場景句「the woodpile and the bamboo fence behind」（長成一整面柴牆）→ 同一個院子：踏石、屋牆與屋門、門邊一小堆圓柴、右後的井；木柴「pale split log in her right hand」→ 一根深色帶皮圓木、雙手低握（兩手都在木頭上，刀才不會跑到手上）、雙手低拋；結尾加「her hands come back empty」；刀換新句 | 照 base | 審片改寫句要她從柴堆抽一根再丟（兩個動作），沒寫：轉換動作放開頭會被跳過，維持 base 的「木頭第一格已在手上」 |

## 檢查（2026-11-21）

```bash
cd /home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs
python3 -I _scripts/polish-build.py 2          # e902: 8 shots, 16 drafts, 108 s
python3 -I _scripts/preflight-prompts.py /root/mokaair-work/videos/zhong-tian-qu-qi-e902-dh/runpod/live/fixp/colab-jobs.json
cd /home/user/zt-work && bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest /root/mokaair-work/videos/zhong-tian-qu-qi-e902-dh/runpod/live/fixp/colab-jobs.json
```

- `polish-build.py 2`：0 錯，8 鏡、16 支、108 秒。
- `preflight-prompts.py`：0 error、2 warning，都是 s03 的 `four`（兩個種子各一條）：保留，理由見上表。
- `h3r.sh check`：0 error、0 warning。
- 另外掃過新提示詞：sword、scabbard、padlock、key、lock、handcuff、knife、pout、giggle 都沒有；兩個分隔字串各一次。

## 拍完要看

- s19：每 0.25 秒一格看左手有沒有離開胯、刀身有沒有出畫、斧頭是不是完整掉下；劈開那一下的時間，重對 `zhongtian-sfx-chop-wood` 與 reveal-hit。
- s21、s22、s24、s03、s06：秦霜腰間是不是短寬柴刀（放大到腰）。
- s22：小禾的嘴整鏡閉著；s30：唐小棠有沒有走到錢員外那邊、有沒有轉出側臉。
- s03：數人頭（剛好一個秦霜、一個唐小棠、一個阿令），阿令有沒有抬頭直視。
- s01：鐵環、鐵栓的樣子沒有現代感；鐵環落地留在畫面裡（審片缺的「鐵鍊落泥地」音效放 c4 左右）。
