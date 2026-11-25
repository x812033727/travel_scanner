# 第 38 集真人版 fix2 重拍計畫

fix2 準備代理 2026-11-23 寫。依據：`../fix1/review-picks.tsv`（fix1 挑片：RETAKE s01 s22 s27，reason 裡的 fix2 英文草稿）、協調者的 fix2 指示、
`../fix1/{mkspec.py,mkjobs.py,plan.md}`、fix1 成片 `/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/fix1/out/`（s22 s27 合併代理也抽格看過）。
**本代理沒有送 Colab**、沒用 RunPod、沒付費圖、沒 commit、沒動第 37 集以前；只做 DRY／PRECHECK。

## 重拍清單（3 鏡 6 支、32 秒）

種子 **9381401／9381402**。秒數照 d1＝BUY（s01 6、s22 5、s27 5）。
基底是 **fix1 9381301** 實際送出的工作與提示詞（`mkjobs.py` 核 sha256、`../fix1/spec.json` 每條修改都在基底裡）；fix1 本身建在 d1 9381101 上，
所以 d1 的加圖（s22 s27 的棗紅馬、s27 的隊長定妝照，在最後、句子跟著、表頭重編）、潭字移除、clear-air、鞋句、固定鏡都跟著。fix2 的每個替換在 fix1 提示詞裡剛好一次。

| 鏡 | 秒 × 支 | fix1 的問題 | 改什麼（英文原句在 `mkspec.py`） |
|---|---|---|---|
| s01 | 6 × 2 | 1301 多一個坐在床後的許硯（三人）；1302 枕頭在左、第一格額頭沒有濕布。原因：「他跪在枕頭那頭的畫右」與「枕頭在畫右」搶同一個位置 | 他改跪在**床的中段、枕頭左邊**（`in the middle of the frame just left of the pillow`）；構圖句加「她的頭在畫右的枕頭上、腳朝畫左」；拿掉「第二塊濕布」，改成**他的右手掌第一格就按在她額頭那塊濕布上**、她的頭在他手後清楚可見；動作只寫「用手掌把布輕輕抹平」、同一個位置一直跪著；加 `he is the only man in the room, and nobody sits on the bed or stands behind it`，連同 only two people、one child **各寫兩次** |
| s22 | 5 × 2 | 兩支都是馬走到小門邊才停，柵從馬身中間穿過（橫木在馬胸腹後、木樁在腿前） | 換更低更近的新免費裁切 **`-zha3`**（柵在前景下半）；低機位、柵 `running large across the lower half of the frame … nearer to the camera than the horse`；馬**在畫面右半、離小門至少三個馬身、第一格就已勒住**、整鏡站在原地不走（`stays on the same spot from the first frame to the last and does not walk`）；**柵的上橫木在馬胸前、交叉木樁在四條腿前**；阿令冷、嘴抿成一線、NOSMILE；甩頭、前蹄原地踏、四蹄在地 |
| s27 | 5 × 2 | 1302 0–0.75 秒最好（馬從右緣進來、在柵的遠側朝柵衝），0.875 秒起整個跳過柵；隊長一直站著、沒有撲 | 同 `-zha3` 與柵在前的句子；馬第一格**還小、還遠、在右緣、離柵一打步**、交叉木樁在牠腿前；**這一鏡只跑一半距離就剪**（`closes only half of that distance, still well short of the stakes`）、碰不到柵、**前蹄每一步都不高過膝**（不寫 forelegs／lifting／over the barrier，`check938` 擋這些字）；隊長**第一格就往畫左撲**（`already throwing himself to the left from the first frame`），落在小門旁的石板上側躺 |

### 接戲（協調者：要接得上 d1 的 s26 與 s27b-9381101）

- d1 s26 1101：隊長站在柵的**小門這一側**（柵在他身後）、矛放平——fix2 s27 他第一格就在柵的小門這一側近端撲出去，位置一致。
- d1 s27b 1101：第一格馬已落在**小門這一側**、塵土、隊長**跌在柵的近端**、3 秒撐起——fix2 s27 的結尾是他側躺在小門旁的石板上、馬還在柵的遠側，中間的跳躍交給剪接與馬蹄聲（聖經第 41 條）。
- 提醒剪接（fix1 挑片已記）：d1 s25 選定的 1102 阿令在柵的**前面**（柵在她身後），跟「馬在柵的遠側」本來就不一致。

### 新裁切 `set-chengmen-ye2-zha3-l1`（免費）

fix1 的 `-zha2`（1000:562:312:174）牆根就貼在柵後面，模型找不到柵後放馬的地方，就讓柵穿過馬身。只改字很可能再穿一次，所以照協調者的「額外」再做一張：
`kong_e938.sh` 加一行 `c "$G" set-chengmen-ye2-zha3-l1 780:438:396:298`（同一套 crop＋lanczos 1312×736＋bitexact；跑兩次逐位元相同，md5 c2b0115；原有 15 張重建仍跟 refs-live 逐位元相同）。
這張更低、更近：小門與火把在左、柵大大地橫過畫面下半（在我們這一側）、柵後是牆根與右邊一點暗地。`refs-live/README.md` 第 38 集那段加一句；scratchpad `prep938.sh` 的比對清單加了 `zha3`。
付費重畫城門圖沒有做（協調者：先不要）。若 fix2 仍穿柵或仍跳：s22 用 d1 1101 的空鏡、s27 用 fix1 1302 的 0–0.75 秒加馬蹄聲（`../fix1/review-picks.tsv` 的暫用剪點），再請站主決定要不要付費畫一張柵在前景、遠側有路的城門圖。

**s01 剪接**：不要左右翻轉畫面（交領會變左衽），fix1 挑片已記。

## 檔案與指令（2026-11-23，全部跑過、0 錯）

```
python3 -I mkspec.py                                    # 3 shots -> spec.json (16 s per seed, 32 s)；每個替換在 fix1 提示詞裡剛好一次
python3 -I mkjobs.py <live>/fix2                        # scan 0；colab-jobs.json 6 支、32 秒
python3 -I <scratchpad>/tools/check938f2.py <live>/fix2 # mkcheck938f2.py 從 check938f1.py 再改 6 處生成（s01 中段、只有一個男人；s22 s27 柵在前；s27 半程、隊長第一格撲），通過
python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json                          # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix2/colab-jobs.json   # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix2/colab-jobs.json  # 0／0
bash <scratchpad>/e938f1/scan2.sh                       # prep938 的否定名詞／會長字的名詞／掛著的東西／舊字：全 0
DRY=1 bash <scratchpad>/e938f2.sh                       # rc 0（帳號 A 的 COLAB_ACCOUNT_SLOT=a＋PATH 也 rc 0，release 自動換 colab-release-A.sh；REL 可覆寫）
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live`。`check938f1.py` 重新生成後對 fix1 仍通過。
`e938f2.sh` 照 `e938f1.sh`：G4、`SESSION` 預設 `zt-live3`、帳號由外部設定、`REL` 可覆寫、送前再跑 `check938f2.py`／preflight／`check_manifest`、兩輪補缺、跑完釋放。

**估價**：6 支 32 秒，照第 37 集第一輪重拍（118 秒 5.03 CU）按秒數約 1.4 CU，加開機約 **1.5–2 CU、約 15 分鐘**。

## 送出後挑片要看的

- s01：一個許硯、一個孩子；他跪在床中段、雙膝與小腿著地；枕頭與她的頭在畫右；第一格他的手掌就在她額頭的布上；蠟燭熄。
- s22：馬在畫右半、柵的遠側、離門三個馬身、從頭到尾不走；柵的橫木與木樁擋在馬前；她不笑。
- s27：馬從遠處朝柵衝、半程就剪、沒有跳；隊長第一格就往左撲、側躺在小門旁。
- 結果寫在 `review-picks.tsv`；取代 `../fix1/review-picks.tsv` 的 s01 s22 s27 三列（fix1 的暫用剪點留作備案）。
