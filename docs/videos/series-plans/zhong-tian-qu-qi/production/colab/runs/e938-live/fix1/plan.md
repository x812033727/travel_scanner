# 第 38 集真人版 fix1 重拍計畫

合併兼 fix1 準備代理 2026-11-23 寫。依據：`../review-picks-a.tsv`（RETAKE s01 s05 s22 s27）、`../review-picks-b.tsv`（RETAKE s01 s05 s11 s12 s14 s15 s15b s27）、
合併結果 `../picks-merged.tsv`（40 鏡裁決、剪點與備案；6 個種子分歧鏡 s02 s09 s13 s17 s30 s37 合併代理自己逐格看過，草稿在 scratchpad `e938f1/`）、
`../{PREP.md,spec.json,mkspec.py}`、聖經 `r2-bible-e031-e040.md`（第 41 條馬、第 42 條病房）、範本第 37 集 `../../e937-live/fix1`。
**本代理沒有送 Colab**（付費執行由協調者跑）、沒用 RunPod、沒付費圖、沒 commit、沒動第 37 集以前；只做了 DRY／PRECHECK。

## 重拍清單（10 鏡 20 支、118 秒）

種子 **9381301／9381302**（9381201／9381202 是協調者 Qwen 改圖用過的）。秒數全照 d1＝BUY。
基底是 d1 9381101 實際送出的工作與提示詞（`mkjobs.py` 核 sha256、`../spec.json` 每條 d1 修改都在基底裡）。
**PREP §6 的提醒（retake 不會自動加圖）**：本輪不經 `retake.py`，直接沿用 d1 工作的 `reference_images`，而 d1 已經是 `prep938.sh`／`check938.py` 加過圖的版本——
s12 的長槍、s20 s22 s27 的棗紅馬、s27 的隊長定妝照都在最後、句子接在場景句後、表頭重編（`mkjobs.py` 與 `check938f1.py` 斷言）；唐小棠背影鏡不在本輪。
官道與城門的潭字移除、clear-air、鞋句都跟著 d1 基底。十鏡都改**固定鏡**（`The camera holds a static shot.`）；風格句仍是 `with the look of a feature film`、沒有 cinema camera；
許硯沒有鬍渣字；門照圖寫關著；`only` 句與人數句各一次（共兩次）；柴刀、劍、刀刃、桌、燈都不寫；跪拍到膝；馬照第 41 條（一匹、不寫躍起、去程右往左）；不寫告示板、招牌、石碑。

| 鏡 | 秒 × 支 | 誰標的 | 問題（d1） | 改什麼（英文原句在 `mkspec.py`） |
|---|---|---|---|---|
| s01 | 6 × 2 | A、B、協調者 | 1101 房間左右反（枕頭在左）、蹲坐不跪、濕布在胸口、蠟燭點著；1102 床上兩個小禾 | 機位低、正對床，「枕頭在畫右、床尾在畫左」；水盆從前景搬到床尾左邊（不擋膝）；`the only child in the bed`＋`little Xiaohe, the only child, lying alone in the bed`（人數句與 only 句兩次）；第一格「濕布已經蓋在額頭上」，他右手拿第二塊擰好的在額頭上方一掌，動作只寫蓋上抹平、一直跪著；`both his knees and both his shins flat on the floorboards, his whole body from his head to his feet inside the frame`；白天蠟燭「熄著、燭芯黑冷、窗光是房裡唯一的光」；固定鏡 |
| s05 | 6 × 2 | A、B | 兩支枕頭邊一張小桌、一根點著的蠟燭（傍晚） | 近景拿掉蠟燭句；背景只寫「粉枕頭填滿她頭兩邊、深色床頭、素白灰牆」；固定鏡 |
| s11 | 6 × 2 | B、協調者；A 選 1102 | 身後枕頭那頭的床入鏡、枕頭是空的；1101 燭火點著 | 拿掉蠟燭句；身後虛焦「床上睡著一個八歲、兩條小辮的女孩，額頭摺好的濕布」；人數句 `exactly two people`＋`Only these 2 people`（她虛焦）；她不動地睡著；固定鏡 |
| s12 | 8 × 2 | B、協調者；A 選 1101 | 床整張入鏡而且空；1101 左緣多一個灰衣人、1102 門開著＋第二個秦霜 | 拿掉過肩的許硯肩膀（多出來的人就是它）、她對畫右外的人說話；阿令**點名並加送 `aling-portrait-l1`（第 2 張，表頭 4 張）**：門內、背靠關著的木板門、腰以上、不笑；右後虛焦床尾、粉被蓋著睡著的小女孩；`exactly two people standing in the room, Qin Shuang and A-ling`＋`Only Qin Shuang and A-ling stand in the frame`；固定鏡 |
| s14 | 6 × 2 | B、協調者；A 選 1102 | 身後床頭與枕頭、床空；1101 笑、鞭子交出去又回到手上 | 身後虛焦床上睡著的女孩；三人（前景阿令後腦、他、虛焦的她）；NOSMILE；「她握住鞭柄、鞭子跟著她的手走，他的右手空著垂下到最後一格」；固定鏡 |
| s15 | 6 × 2 | B、協調者；A 選 1101 | 身後的床與空枕頭（文字只寫牆與窗，圖是床） | 身後寫成「窗下的床、睡著的女孩、枕頭在右」；兩人句兩次；她不動地睡著；固定鏡 |
| s15b | 6 × 2 | B、協調者；A 選 1101 | 同 s15；1101 淡笑；1102 床上小炕桌兩根蠟燭 | 同 s15；NOSMILE（`lips pressed shut in one flat line`）；固定鏡 |
| s20 | 5 × 2 | 合併代理（協調者列評估） | 兩支都是小跑，1101 2 秒後站住、1102 3 秒後幾乎停（全集唯一一個官道狂奔） | 第一格就是 flat-out gallop、腿伸長、鬃尾平飛；「整個畫面從右緣狂奔到左緣、不減速、片尾到左緣」；固定側面低機位 |
| s22 | 5 × 2 | A、協調者；B 選 1101 | 馬站在柵**靠鏡頭這一側**，小門直接在馬面前 | 送新的免費裁切 **`set-chengmen-ye2-zha2-l1`**；照圖寫地理：鏡頭在小門這一側、小門在柵的這一側、柵從火把腳下橫過畫面中段到右緣、**柵擋在馬與小門之間**、馬在柵的另一邊（沿著城牆根那條路）三步外勒住、腿從交叉的木樁間看得到（地理寫兩次）；甩頭、前蹄原地踏、四蹄在地；固定鏡 |
| s27 | 5 × 2 | A、B、協調者 | 馬沿柵平行小走、柵在遠側；隊長在小門前不動 | 同 s22 機位與兩句地理；馬第一格就在柵的另一邊全速衝、從右緣進來朝畫左直衝柵與城牆相接處、側面、頭低鬃飛；**剪在離柵兩步、四蹄著地**（沒有 lifting／forelegs）；隊長在**柵的小門這一側**、柵的近端火把旁，往畫左一撲（接 s27b 1101：馬落在小門這一側、隊長跌在柵近端）；固定鏡 |

### 為什麼 s22／s27 這樣寫（城門的地理）

`set-chengmen-ye2-l1`（付費 Qwen 9381215）上，柵從小門右邊那支火把腳下起、往右下伸到畫框右緣；小門在柵的**鏡頭這一側**，路（`s27b` 原句「the road running back along the wall toward the right」）在柵後沿城牆根往右遠去。
d1 把馬寫成「on the road side of the barrier」，模型就把馬放到前景石板地上，柵在馬身後、小門開在馬面前。照這張圖唯一說得通的寫法是：**馬在柵的遠側（城牆根的路上），小門與鏡頭在近側**——
柵就擋在馬與小門之間，s27b 1101「馬已落在小門這一側、隊長跌在柵的近端」也剛好接上（s27b 不重拍）。
- **s27 改成側面不是側後**：側後要鏡頭在路那一側、背對我們看小門，現有的圖都是從小門這一側拍的，免費裁切做不出反打；聖經第 41 條「只拍側面與側後」側面也可以。要真的側後，得付費畫一張反打的城門圖（Qwen 約 0.5–1 CU），先看 fix1。
- **新裁切 `-zha2`**：`kong_e938.sh` 加一行 `c "$G" set-chengmen-ye2-zha2-l1 1000:562:312:174`（同一套 `crop`＋lanczos 1312×736＋bitexact，跑兩次逐位元相同，md5 523e0fb），比 `-zha`（800:450）寬，
  柵的遠側到牆根留得下一匹全身的馬、整個衝刺在畫面裡；`kong_e938.sh` 原有的 14 張重建仍跟 refs-live 逐位元相同。`prep938.sh` 的比對清單加了 `zha2`，`refs-live/README.md` 第 38 集那段加一句。

### 病房的蠟燭與床（協調者「同樣檢查其他病房近景的蠟燭句」）

- 傍晚近景 s05、s11 拿掉蠟燭句（`check938f1.py` 斷言兩鏡沒有 `candle`）：這兩鏡送的是 `-kong-xi-zhen`（枕頭那頭），矮凳不在框裡，寫了就長出桌與燭（d1 s05 兩支、s11 1101、s06 1102 都點著）。
- 其他病房近景這輪不重拍、不改：s03 s06 s10 的 d1 選定支蠟燭都熄著、在左；剪接不用處理。
- 夜裡 s12 s14 s15 s15b 留「矮凳上那一朵火」：d1 這幾鏡的選定支都只有一朵、在床尾矮凳（唯一的暖光），寫了沒出錯；s15b 1102 的兩朵火＋炕桌是那一支自己的問題。
- 床上的女孩：s11 s14 s15 s15b 寫「a little girl of eight with two little pigtails asleep in it … her eyes shut」（`asleep in the bed` 至少兩次），**不點名、不送小禾的圖**——虛焦的背景人物送臉部圖反而會把她拉成焦點；s12 只看得到床尾，寫粉被蓋著睡著的小身形。

**不重拍、剪接處理**（`../picks-merged.tsv`）：s03（哄孩子帶笑，剪在餵藥那段）、s18（馬走出院門不是衝；8 秒兩支、H3 騎馬加速不保證，剪接靠馬蹄聲）、
s24（B 記盔後黑纓、A 記沒有；背影、小）、s26（柵在他身後、跟 s23 不一致；中景，柵讀成背景；fix1 s27 與 s27b 隊長都在柵的小門這一側，跟本鏡一致）。
s04、s16 收尾改用 B 的較早剪點避開笑；s37 起點 0.5（量過原聲 0.75 秒起）。

## 檔案與指令（2026-11-23，全部跑過、0 錯）

```
python3 -I mkspec.py                                    # 10 shots -> spec.json (59 s per seed, 118 s)；每個 replace 在 d1 提示詞裡剛好一次
python3 -I mkjobs.py <live>/fix1                        # scan 0；colab-jobs.json 20 支、118 秒
python3 -I <scratchpad>/tools/check938f1.py <live>/fix1 # check938.py 的逐鏡斷言（mkcheck938f1.py 從 check938.py 改 22 處生成），通過
python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json                          # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json   # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix1/colab-jobs.json  # 0／0
bash <scratchpad>/e938f1/scan.sh                        # prep938 的否定名詞／會長字的名詞／掛著的東西／舊字：全 0（NOSMILE 的 no smile 照第 37 集 fix1 放行）
DRY=1 bash <scratchpad>/e938f1.sh                       # rc 0（另測 COLAB_ACCOUNT_SLOT=a＋PATH 帳號 A：release 自動換 colab-release-A.sh；REL 可覆寫）
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live`。
`e938f1.sh`：G4、`SESSION` 預設 `zt-live3`、**不設帳號**（`COLAB_ACCOUNT_SLOT`／`COLAB_ACCOUNT_HOLDER`／`PATH` 由外部設定）、`REL` 可覆寫（預設：slot a → `colab-release-A.sh`，否則 `colab-release.sh`）、
送前再跑 `check938f1.py`、preflight、`check_manifest`；兩輪補缺；跑完 `ONLY_SELF=1 bash $REL $SESSION`。

**估價**：照第 37 集 fix1（20 支 118 秒，實際 5.03 CU、約 40 分鐘），本輪同樣 20 支 118 秒，約 **0.5 小時、4.5–6 CU**。d1 跑完後餘額 181.39 CU（`e938d1-A-run.log`），以跑之前的數字為準。

## 送出後挑片要看的

- s01：一個孩子、枕頭在右、雙膝與小腿著地全身入鏡、第一格額頭已有濕布、蠟燭熄、只有兩人。
- s05：枕頭兩邊沒有桌與燭火。s11 s14 s15 s15b：身後床上有睡著的女孩（虛焦）、她不會醒來看鏡頭；s14 不笑、鞭子交出去不回來；s15b 不笑。
- s12：門關著、阿令在門內門邊、只有秦霜與阿令兩個站著的人、床上有人、沒有過肩的第三人。
- s20：全速、不停、右往左。
- s22：馬在柵的另一邊、柵在馬與小門之間、甩頭踏步、四蹄在地。s27：馬在柵的另一邊全速衝、剪在柵前兩步、沒有起跳、隊長在小門這一側往旁一撲；接 s27b 1101。
- 結果與選擇寫在 `review-picks.tsv`；`../picks-merged.tsv` 的 RETAKE 列與 s20 的 d1 選擇由它取代（d1 選擇與暫用剪點留作備案）。
