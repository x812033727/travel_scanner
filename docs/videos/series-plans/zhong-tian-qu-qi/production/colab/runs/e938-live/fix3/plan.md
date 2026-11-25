# 第 38 集真人版 fix3 重拍計畫（s25、s26 照城門地理重拍）

fix3 準備代理 2026-11-24 寫。依據：協調者的 fix3 指示與 `../fix2/review-picks.tsv`（s22 選 fix2 9381401 剪 1.250–4.250、s27 選 fix2 9381401 0–0.5 秒＋fix1 9381302 0–0.75 秒、s01 沿用 fix1）、
`../{spec.json,mkspec.py}`、`../fix1/mkjobs.py`。**本代理沒有送 Colab**、沒用 RunPod、沒付費圖、沒 commit、沒動第 37 集以前；只做 DRY／PRECHECK。

## 為什麼重拍

fix2 s22 9381401 第一次把城門地理拍對了：**鏡頭在小門這一側 → 拒馬柵在前景 → 馬在柵後 → 城牆**。d1 選定的兩鏡跟這個反了：
- s25-9381102：柵在阿令身後、柵後直接是城牆，她變成站在柵離城牆的那一側。
- s26-9381101：隊長身後是柵；從阿令那一側拍過去，柵應該在他前面，他在柵的小門那一側。

## 重拍清單（2 鏡 4 支、24 秒）

種子 **9381501／9381502**；秒數照 d1＝BUY（各 6 秒）；錄音 a24 3.68 秒、a25-p85 3.08 秒放得下（d1 的剪點長度 4.0–5.6 秒）。
基底是 **d1 9381101** 實際送出的工作與提示詞（`mkjobs.py` 核 sha256、`../spec.json` 每條 d1 修改都在）：s25 的馬圖、s26 的隊長定妝照照舊在最後、句子跟著（張數不變，表頭不動）；
官道與城門的潭字移除、clear-air 都跟著。只換送的場景圖，換成兩張新的免費裁切。固定鏡、不笑（NOSMILE）、台詞照原鏡、說話對象照 d1 在畫外不點名；第 41 條照舊（一匹馬、不寫躍起）。

| 鏡 | 秒 × 支 | 送圖 | 改什麼（英文原句在 `mkspec.py`） |
|---|---|---|---|
| s25 | 6 × 2 | `aling-portrait`、`aling-angle-a`、**`set-chengmen-ye2-zhahou-l1`**（換掉 `-lu`）、`prop-zaohongma` | 從柵的這一側隔著柵拍：齊腰拒馬柵**橫過整個畫面下緣、比馬離鏡頭近**；阿令與馬在柵後、城牆根的路上；上橫木從她下方的馬胸前過去，人和馬整鏡都在柵後；身後只有緊貼在馬後的長城牆（拿掉「她來時的路」）；畫左那一側只寫木樁與暗牆（拿掉「火光照的柵」）；隊長仍在畫左外、不點名；NOSMILE；固定鏡 |
| s26 | 6 × 2 | **`set-chengmen-ye2-zhamen-l1`**（換掉 `-qiang`）、`duizhang-portrait` | 從路那一側（阿令那一側）隔著柵拍：柵**橫過整個畫面下緣、在他前面、比他離鏡頭近**，木樁整鏡擋在他與鏡頭之間；他**站在柵的小門那一側、緊貼在木樁後**，上橫木在他腰的高度；身後是往外開的小門（畫左）、火光磚牆與鐵架上的火把（沒人拿）；同一張臉、同一頂盔（d1 的定妝照句照舊）；矛往畫右外短戳；NOSMILE；固定鏡 |

### 兩張新的免費裁切（`kong_e938.sh` 同一套做法）

- `set-chengmen-ye2-zhahou-l1` = `640:360:640:300`（md5 0c909c3）：柵橫過畫面下半、長城牆緊貼在後、左緣一點火光牆角。接 fix2 s22 `-zha3` 的右半，同一個方向。
- `set-chengmen-ye2-zhamen-l1` = `560:315:420:300`（md5 5a322d9）：柵橫過畫面下部，後面是往外開的小門、火把與火光磚牆。這是反打用的背景：隊長前面是柵、後面是小門，觀眾讀得出他在柵的小門那一側，鏡頭在阿令那一側。

做法：兩行 `c "$G" …` 加在 `kong_e938.sh` 最後，都是 crop＋lanczos 1312×736＋bitexact。跑兩次逐位元相同；原有 16 張重建仍跟 refs-live 逐位元相同。
`refs-live/README.md` 第 38 集那段加一句；scratchpad `prep938.sh` 的比對清單加了 `zhahou`、`zhamen`。付費圖沒做。

**剪接提醒**：s23 選定的 1102 隊長也在柵後（柵在他前面），跟 fix3 s26 一致；s24 年輕守軍、s28 不受影響。

## 檔案與指令（2026-11-24，全部跑過、0 錯）

```
python3 -I mkspec.py                                    # 2 shots -> spec.json (12 s per seed, 24 s)；每個替換在 d1 提示詞裡剛好一次
python3 -I mkjobs.py <live>/fix3                        # scan 0；colab-jobs.json 4 支、24 秒
python3 -I <scratchpad>/tools/check938f3.py <live>/fix3 # mkcheck938f3.py 從 check938f1.py 再改 6 處生成（新裁切、柵在前、阿令／隊長的位置），通過
python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json                          # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix3/colab-jobs.json   # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix3/colab-jobs.json  # 0／0
bash <scratchpad>/e938f1/scan3.sh                       # prep938 的否定名詞／會長字的名詞／掛著的東西／舊字：全 0
DRY=1 bash <scratchpad>/e938f3.sh                       # rc 0（帳號 A 的 COLAB_ACCOUNT_SLOT=a＋PATH 也 rc 0；REL 不存在時 rc 2）
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live`。`check938f1.py`、`check938f2.py` 重新生成後，對 fix1、fix2 仍通過。
`e938f3.sh` 照 `e938f2.sh` 的寫法：G4、`SESSION` 預設 `zt-live3`、帳號由外部設定、`REL` 可覆寫、送前再跑檢查、兩輪補缺、跑完釋放。

**估價**：4 支 24 秒，照秒數比例約 1.0 CU，加開機約 **1.2–1.6 CU、約 10–15 分鐘**。

## 送出後挑片要看的

- s25：柵在前景下緣、阿令與馬在柵後、城牆緊貼在後；她朝畫左外說、不笑；只有一匹馬、沒有別人。
- s26：柵在他前面、橫過下緣；他身後是小門與火把；同一張臉、同一頂紅纓盔；不笑；矛往畫右外。
- 結果寫在 `review-picks.tsv`，取代 `../picks-merged.tsv` 的 s25、s26 兩列（d1 選擇留作備案）。
