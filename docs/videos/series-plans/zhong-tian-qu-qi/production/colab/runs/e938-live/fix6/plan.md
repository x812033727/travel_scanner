# 第 38 集真人版 fix6：付費修馬鞍與 s22（兩階段：先 Qwen 改圖、挑圖，再跑 H3）

fix6 準備代理 2026-11-24 寫。站主：品質優先、有問題就修；協調者：免費的辦法都試過了，這次付費修，由協調者跑。
依據：`../fix4/review-picks.tsv`（s22 兩支又回到柵前／嵌柵，沿用 fix2 9381401）、`../fix5/review-picks.tsv`（s29 s30 s32 的鞍改字也換不掉：送的馬圖是光背馬，H3 每次畫成高鞍頭、亮鋼馬鐙的西式鞍；s32 兩支都推到隊長半身）、
`../picks-final.tsv`、第 38 集 Qwen 三輪的經驗（`../qwen/{jobs.json,step2/,step3/}`、PREP.md §7：**搬東西會失敗，加東西做得好**）、`minimax-h3-colab` skill（`h3.sh images`、first_frame 模式、`fit_first_frame.sh`）。
**本代理沒有送 Colab、沒 commit**；只寫好檔案、跑檢查與 DRY。

## 順序（一定照這個順序）

| 步 | 指令 | 做什麼 | 產出 |
|---|---|---|---|
| 1a | `STEP=a bash <S>/e938f6-qwen.sh` | Qwen：在光背棗紅馬圖上**只加鞍、鐙、肚帶** | `qwen6/a/prop-zaohongma-an-9381801.png`、`-9381802.png` |
| 1a' | 人挑（下面「挑圖要看什麼」） → `STEP=pick-a PICK=<seed> bash <S>/e938f6-qwen.sh` | 裝成 `refs-live/prop-zaohongma-an-l1.png`（另存 `fix6/qwen/PICK-horse-<seed>.png`）；**手動在 `refs-live/README.md` 第 38 集那段補一句**（來源、種子、md5） | 新馬圖 |
| 1b | `STEP=b bash <S>/e938f6-qwen.sh` | Qwen：在空的城門圖 `-zha3` 上**只加一人一馬、在柵的遠側**（image 2 阿令定妝照、image 3 剛裝好的配鞍馬） | `qwen6/b/s22-ff-9381803…9381806.png` |
| 1b' | 人挑 → `STEP=pick-b PICK=<seed> bash <S>/e938f6-qwen.sh` | 存 `fix6/qwen/PICK-s22-ff-<seed>.png`，`fit_first_frame.sh` 裁到 H3 草稿畫布 960×544 → `<live>/fix6/first-frames/s22-ff.png` | s22 首格 |
| 2 | `bash <S>/e938f6.sh` | 用挑好的兩張圖重建 jobs（`mkspec.py`＋`mkjobs.py`）、檢查、送 H3：s29 s30 s32（參照模式、新馬圖）＋s22（首格模式） | `<live>/fix6/out/` 8 支 |

`<S>` = `/tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad`，`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live`。
兩支腳本都**不設帳號**（`COLAB_ACCOUNT_SLOT`／`COLAB_ACCOUNT_HOLDER`／`PATH` 由外部設好，先 `accounts.py claim`）、`REL` 可覆寫（slot a 預設 `colab-release-A.sh`）、`SESSION` 預設 `zt-live3`（fix4／fix5 還在跑就換 session 或等）。
1a 與 1b 是兩次開機（1b 要等 1a 挑完）；也可以 1a 跑完先不釋放、挑完接著跑 1b，省一次開機（腳本每步都會釋放，要省就手動）。

## 第一階段：Qwen 改圖（`qwen/`）

| 檔 | 內容 |
|---|---|
| `jobs-a.json` | 2 支：`prop-zaohongma-an-9381801`、`-9381802`；image 1＝`refs-live/prop-zaohongma-l1.png`（光背馬）；1312×736、latent image1、LoRA off（照 e938 qwen 三輪） |
| `horse-saddle.txt`／`negative-horse-saddle.txt` | 「保持一切（機位、毛色、鬃尾、頭、轡頭與韁、姿勢四蹄、灰背景、光）**只加背上的鞍具**：低平舊鞍、暗褐皮面繃在素木框上、前鞍橋低而圓、後緣低、皮面暗而啞；下面一塊摺起的深褐布、四周露出一掌寬；一條暗皮肚帶；近側一隻暗色無光的鐵鐙、掛在暗皮帶上」。負面：西式鞍、鞍角、高前橋高後橋、鍍鉻、亮鋼、銀飾、花紋、流蘇、騎手、第二匹馬、換姿勢、換毛色、換背景 |
| `jobs-b.json` | 4 支：`s22-ff-9381803`…`-9381806`；image 1＝`set-chengmen-ye2-zha3-l1`（空城門、柵在前景：fix2 9381401 就是從這張畫的，**本身就是「清掉」之後的底**，所以不必先從 fix2 的首格把嵌柵的馬擦掉），image 2＝`aling-portrait-l1`，image 3＝`prop-zaohongma-an-l1`（1a' 裝的） |
| `s22-ff.txt`／`negative-s22-ff.txt` | 「保持一切（機位、左邊往外開的小門與火把、磚牆、前景下方的齊腰拒馬柵、石板、月光與火光）**只加一人一馬、在柵的遠側**：image 3 的馬連鞍、側面站定、頭朝左、在柵與城牆之間的路上、**離柵兩個馬身、柵腳與馬蹄之間一條空的石板地**、四蹄著地、在畫面右半；柵的上橫木與木樁在牠前面、離鏡頭更近、**碰不到馬**；image 2 的女子側坐在鞍上、側臉朝左、冷靜、嘴閉」。負面：馬在柵前、馬在柵裡、木樁穿過馬、馬碰柵、跳、揚蹄、馬在小門邊、第二匹馬、第二個人、守軍、笑、西式鞍、柵被搬走 |

`check_images_manifest.py`：jobs-a 0／0；jobs-b 0／0（新馬圖還沒有時，DRY 用光背馬當替身檢查）。

### 挑圖要看什麼

**1a 馬鞍（2 張挑 1）**
- 鞍：低、平、舊、暗褐皮面、看得出木框；**前鞍橋低而圓、沒有往上翹的鞍角、後橋也低**；下面一塊摺起的深色布。
- 鐙：暗色鐵或木、**不反光**；不要亮鋼、鍍鉻、銀邊；只有近側一隻也可以。
- 馬沒被改：毛色、鬃尾、頭與轡頭、四蹄位置、站姿、灰背景都跟 `prop-zaohongma-l1` 一樣（兩張並排比）；沒有多出騎手、第二匹馬、花紋布。
- 都不行：照原提示詞換兩個種子（9381807／9381808）再跑一次 1a；仍不行就交協調者（可改寫成「只加一塊摺起的深色布墊鞍＋暗鐵鐙」的更簡單版本）。

**1b s22 首格（4 張挑 1）**
- 地理：**鏡頭 → 柵（前景）→ 一條空石板 → 馬 → 城牆**；柵的上橫木與木樁全部在馬前面、**沒有一根穿過或碰到馬身**；柵腳與馬蹄之間看得到空的石板地（約兩個馬身）。
- 馬：一匹、側面、頭朝左、四蹄著地、在畫面右半、離小門遠；鞍是新圖的低平暗鞍。
- 人：只有一個女子、在鞍上、側臉朝左、灰白衣、木簪、不笑；臉大致像阿令（遠景、小，可接受）；沒有守軍、沒有第二個人。
- 城門沒被改：小門與火把在左、柵的位置與形狀、磚牆、月光照舊；沒有字、燈籠、招牌。
- 都不行：換 9381807–9381810 再跑一次 1b；或改成兩步（先只加馬、再加人）。

## 第二階段：H3（`mkspec.py` → `spec.json`、`mkjobs.py`）

| 鏡 | 模式 | 底稿 | 種子 | 秒 | 改什麼 |
|---|---|---|---|---|---|
| s29 | 參照 | d1 9381101（剪接現用） | 9381811／9381812 | 5 | 馬圖換成 `prop-zaohongma-an-l1`（同一個位置、張數不變、表頭不動）；鞍不再用文字形容，改成「its low flat old saddle … **exactly as in its picture**」，馬圖句改成「exactly its saddle, the folded dark cloth under it and its dark iron stirrup **as the picture shows them**」（拿掉 `with the saddle written above`）；運鏡照 d1 慢推 |
| s30 | 參照 | d1 9381101 | 9381811／9381812 | 6 | 同 s29；a27 對嘴 |
| s32 | 參照 | d1 9381101 | 9381811／9381812 | 6 | 同 s29；**固定鏡**＋構圖句寫死「held this wide from the first frame to the last, all nine people and the horse inside the frame the whole shot」（fix5 兩支都推到隊長半身）；九人一馬、隊長定妝照照舊在最後；a29 對嘴 |
| s22 | **首格** | fix2 9381401 的文字 | 9381821／9381822 | 5 | 一張圖：1b' 挑好、裁成 960×544 的首格；提示詞以 `<Picture 1>` 為錨（首格照原樣：小門與火把、前景的柵、柵後兩個馬身的空石板、馬與女子、城牆），動作照 fix2：第一格已勒住、原地不動、甩頭踏前蹄、四蹄著地、空石板一直空著、嘴閉、NOSMILE、固定鏡。**不點名阿令**（首格模式沒有她的定妝照，preflight 會警告；臉由首格決定） |

畫布照草稿 960×544（跟 d1 一樣，之後精修到 1312×736）；首格先 `fit_first_frame.sh` 裁到 960×544，`mkjobs.py` 用 ffprobe 斷言尺寸一致（check_manifest 也擋）。
一份 manifest 混兩種模式：`h3_detached.py` 每支讀自己的 `inference_mode`（first_frame 送 `H3_INPUT_IMAGE`）。

### 檢查（2026-11-24，全部 0 錯）

第二階段要讀挑好的圖，現在還沒有，所以 DRY 用**替身**跑完整條路（`STANDIN=1`：光背馬當新馬圖、fix2 9381401 的第一格當首格，輸出到 `<live>/fix6-dry`，不碰 `<live>/fix6`）：

```
STEP=a DRY=1 bash <S>/e938f6-qwen.sh              # check_images_manifest 0/0；rc 0
STEP=b DRY=1 bash <S>/e938f6-qwen.sh              # 替身馬；0/0；rc 0
DRY=1 STANDIN=1 bash <S>/e938f6.sh                # mkspec + mkjobs（scan 0）、check938f6.py、preflight 0/0、check_manifest 0/0、h3r 0/0；rc 0
DRY=1 bash <S>/e938f6.sh                          # 圖還沒挑：rc 2，印出要先跑哪一步（正確行為）
bash <S>/e938f1/scan6.sh                          # 否定名詞／會長字的名詞／掛著的東西／舊字：全 0
```

帳號 A（`COLAB_ACCOUNT_SLOT=a`＋`PATH`）兩支腳本 DRY 都 rc 0、release 自動換 `colab-release-A.sh`；`REL` 不存在時 rc 2。`check938f1/f2/f3/f5` 重新生成後對 fix1～fix5 仍通過。
`tools/check938f6.py` 由 `tools/mkcheck938f6.py` 從 `check938f1.py` 改 8 處生成（只查 s29 s30 s32：新馬圖在原位、鞍句指向圖、s32 固定鏡且寫死全景）；s22 的首格工作由 `mkjobs.py` 自己掃（一張圖、尺寸、`<Picture 1>`、必在／必去句、運鏡、笑字、西式鞍字）。

## 挑片（第二階段跑完）

- s29 s30 s32：鞍要跟新馬圖一樣（低平暗鞍、暗鐙），**三鏡規則照舊**（三鏡都有可用的一支才一起換，否則都留 d1）；s32 九人一馬整鏡都在、沒有推近；s30 a27、s32 a29 對嘴。
- s22：柵在前、空石板、馬在後、整鏡不走、四蹄著地、不笑；首格的地理有沒有在動作裡守住（馬往前走到柵就不行）。退路：fix2 9381401 c1.25–4.25。
- 選中的改 `../picks-final.tsv`（source `fix6`），再精修。

## 估價

| 項目 | CU |
|---|---|
| 1a 馬鞍 2 張（G4 一次開機、模型載入約 8 分鐘＋每張約 30 秒） | 1.5–2.5 |
| 1b s22 首格 4 張（同上） | 1.5–2.5 |
| 第二階段 8 支 44 秒（每秒 0.043＋開機） | 2.2–2.8 |
| 精修選中的四鏡（約 22 秒、約 530 格 × 0.0032＋開機；可跟 fix4／fix5 的精修同一批） | 2.0–2.5 |
| **合計** | **約 7–10 CU** |

（參考：第 38 集 Qwen 三輪共 8.45 CU；第 37 集第一輪重拍 118 秒 5.03 CU。）若 1a 或 1b 要重跑一次，各加 1.5–2.5 CU。餘額剩約 100 CU 時先問站主。
