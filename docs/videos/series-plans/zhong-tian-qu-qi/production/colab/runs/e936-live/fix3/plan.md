# 第 36 集真人版 fix3：s02 用付費開門圖重拍

第 36 集前置代理 2026-11-21 寫。依據：協調者 2026-11-21 的指示（站主同意、協調者跑了開門圖，選 9361202 → `assets/refs-live/set-cunkou-zha2-kai-l1.png`，約 1.3 CU，餘額 223.00）、
`writer-tools/e036-r2/review-independent.md`（必改 1、建議 2）、`../picks-merged.tsv`（s02 目前用 d1 9361101，start 1.000 end-before 6.583）、範本 `../fix1/`、`../fix2/`。
沒用 RunPod、付費圖、站台 TTS；沒 commit。

## 為什麼重拍

d1 的 s02 是付費圖還沒有時的免費繞法：送 `-zha2-wai2`（畫面裡沒有門扇），門口在畫左外、人從左緣走進來——**觀眾看不到「門開了」**（稿子 c02 的鉤子）。
開門圖挑定後 `r2.py` 設 `KAI = True`，s02 換成 `S02_KAI`：從門裡看兩扇門往內推開、跟籬笆垂直、門閂靠左門柱，八個流民穿過門口朝鏡頭走來，守門兩人各在一扇門邊拿火把，許硯在門口右邊側身，前排老人作揖。

## 一支、兩個種子、12 秒

| 鏡 | 種子 | 秒 | 圖 | 寫法 |
|---|---|---|---|---|
| s02 | 9361231、9361232 | 6（= `r2.py` BUY） | 許硯 l1、`set-cunkou-zha2-kai-l1` | 基底是 `KAI = True` 那一版 d1 提示詞（`prep936.sh` 在隔離的工作資料夾 scratchpad `e936kaiprep/` 跑過，0 錯；其他 39 鏡的提示詞跟送出的 d1 逐位元相同，只有 s02 不同），sha256 核過；再照 fix1 的習慣：**固定鏡**、結果先寫（兩扇門從第一格到最後一格都推開著、十一人到最後一格）、每張臉 NOSMILE、作揖放在鏡頭中段、其他人繼續走過。火把點名（必改 2）照 d1 |

`mkjobs.py` 掃描 0（推鏡、cinema camera、`wai2`、門口在畫外的舊句、open、會長字或掛著的東西、笑字、否定名詞、分隔句各一次、圖、秒數）；`preflight-prompts.py`、`check_manifest.py`、`h3r.sh check` 都 0／0。

```
python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/fix3     # 2 jobs, 12 s, scan 0
bash <scratchpad>/e936f3.sh   # 查別的 driver 與 session → zt-live3 G4 → 兩輪補缺 → ONLY_SELF=1 colab-release.sh zt-live3 → sessions / usage
```

## 狀態（2026-11-21）

**沒有送出**：送之前 `colab sessions` 沒有 session、沒有別的 driver、餘額 223.00 CU、assignments 0；`e936f3.sh` 的呼叫**被 Claude Code 的自動權限擋下**（判定為不想要的動作；昨天開門圖那一次也一樣），照規則不繞過。
要協調者跑 `bash <scratchpad>/e936f3.sh`（或給前置代理加允許 `e936f3.sh` 的權限）。估約 0.3–0.5 CU（第 36 集 fix1 18 支 124 秒約 3 CU 等比）。

## 跑完之後（挑片與精修）

1. 一人挑（寫明），兩支並排每 0.25 秒抽格，跟目前的 d1 9361101（scratchpad `e936prep/s02-d1-sheet.jpg`，1.0–6.583 秒）比：
   門整鏡推開著、門口看得到外面；十一人、人數不增加（d1 的備註：3.73 秒起畫左人變多）；四支火把在點名的四人手上、老人兩手空著作揖；許硯不笑、不看鏡頭；
   守門兩人拿火把；沒有字、沒有多出來的門或牌子。寫 `review-picks.tsv`（`shot	choice	reason`，choice 是種子或 `KEEP`）。
2. 比 d1 好才換：`SESSION=zt-live3 PREP=1 PRECHECK_ONLY=1 ONLY=s02 bash <scratchpad>/e936refine.sh`（讀檔順序已含 `fix3/review-picks.tsv`，`SRC` 表 `123` = fix3），
   再 `SESSION=zt-live3 ONLY=s02 bash <scratchpad>/e936refine.sh`；核 `.seed` = 挑的種子、1312×736、格數等於草稿，抽格跟草稿並排看。跑完 `ONLY_SELF=1` 釋放、核 assignments 0、未記名 VM 手動釋放。
