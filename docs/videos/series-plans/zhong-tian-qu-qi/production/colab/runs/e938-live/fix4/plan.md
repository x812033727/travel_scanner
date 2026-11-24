# 第 38 集真人版 fix4 重拍計畫（REVIEW 3：s09、s17、s22）

REVIEW 3 代理 2026-11-24 寫。依據：`../review3-plan.md`（兩份審片合併，B 節）、`../cut-review.md`（審 1）、`../cut-review-2.md`（審 2）、
`../fix3/{mkspec.py,mkjobs.py,plan.md}`。**沒有送 Colab**、沒用 RunPod、沒付費圖、沒 commit；只做 DRY 與檢查。

## 為什麼只重拍這三鏡

剪接（裁切、換種子、改剪點、混音）修得掉的都已經在 REVIEW 3 的新版剪好（`../review3-plan.md` A 節）。剩下剪接救不了、又是一般觀眾一眼看得到的：

| 鏡 | 問題（誰提的） | 為什麼剪接救不了 |
| --- | --- | --- |
| **s09** | 床上沒有小禾（審 2 必修 M1）：兩人中間只有光禿的床尾 | 床夾在秦霜與許硯中間，裁不掉；d1 另一支 9381101 床也是空的、還多一桿長槍（看圖在 scratchpad `e938c/r3/g2.jpg` 第一排） |
| **s17** | 秦霜帶笑（審 1 該改 3；審 2 認為可接受） | 片中 c0.8–1.6、c3.3 都在笑，台詞 5 秒、笑在句子中間，剪不掉；d1 9381101 背景有一匹沒人騎的馬（挑片已退） |
| **s22** | 馬嵌在拒馬柵裡（審 2 必修 M2）：橫木從馬胸、斜木從馬腿中間穿過 | 這支是唯一地理對的（鏡頭→柵→馬→城牆）；d1 兩支、fix1 9381301、fix2 9381402 都是馬在柵前（地理反）。裁切只留小門那一側也會留下橫在馬頸前的木條 |

不重拍、照接受的（理由在 `../review3-plan.md`）：s20 正面跑、s29/s30/s32 西式鞍、s19 布偶熊、s01 頭在左、s08 咧嘴、s18 走出院門（已剪短）、s25 腰後柵木。

## 重拍清單（3 鏡 6 支、38 秒）

種子 **9381601／9381602**；秒數照底稿的工作（＝BUY）。底稿是**現在剪接用的那一支實際送出的工作與提示詞**（`mkjobs.py` 核 sha256；送圖、加在最後的長槍圖／馬圖與它們的句子都照舊，張數不變、表頭不動），每個替換在底稿裡剛好一次。運鏡照底稿（s09、s17 慢推；s22 固定）。

| 鏡 | 底稿 | 秒 × 支 | 改什麼（英文原句在 `mkspec.py`） | 錄音／對嘴 |
|---|---|---|---|---|
| s09 | d1 9381102 | 8 × 2 | 兩人中間、許硯身後的床上寫「粉被蓋著睡著的小女孩、頭在枕上、從第一格到最後一格都看得到」（照 fix1 s12 9381302 拍成的寫法）；人數句改成「站著的只有秦霜與許硯，床上睡著小女孩」 | 片中原聲（秦霜）；剪接照原剪點 2.0–8.0、rubberband 約 0.81 → 205 Hz |
| s17 | d1 9381102 | 6 × 2 | `not smiling` 換成「serious and wary：瞇眼、眉平、嘴角平穩不動」＋NOSMILE | 片中原聲；剪點要把整句「那是…不是剛學的」包進去（d1 是 1.0–6.4） |
| s22 | fix2 9381401 | 5 × 2 | 馬在柵**遠側再兩個馬身**、柵腳與馬蹄之間一條空的石板地、每根橫木與木樁都在馬前面、沒有一根碰到牠；人數句加「馬離柵很遠」 | 無台詞；剪接照 1.25–4.25 |

## 檔案與指令（2026-11-24，全部跑過、0 錯）

```
cd docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e938-live/fix4
python3 -I mkspec.py                                    # 3 shots -> spec.json (19 s per seed, 38 s)；每個替換在底稿裡剛好一次
python3 -I mkjobs.py <live>/fix4                        # scan 0；colab-jobs.json 6 支、38 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix4/colab-jobs.json                           # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix4/colab-jobs.json    # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix4/colab-jobs.json   # 0／0
bash <scratchpad>/e938f4/scan4.sh                       # 否定名詞／會長字的名詞／掛著的東西／舊字：全 0
DRY=1 bash <scratchpad>/e938f4.sh                       # rc 0（帳號 A 的 COLAB_ACCOUNT_SLOT=a＋PATH 也 rc 0；REL 不存在時 rc 2）
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live`。`mkjobs.py` 自己帶完整掃描（照 fix3 的 mkjobs：否定名詞、分隔句各一次、
鬍渣／柴刀／劍／桌／燈／跳躍字、笑字、點名畫外人、必在與必去的句子、台詞、運鏡、送圖與編號句、表頭），任何一項不過就 exit 1；`e938f4.sh` 送前再跑一次。

`e938f4.sh` 照 `e938f3.sh`：G4、`SESSION` 預設 `zt-live3`、帳號由外部設定（`COLAB_ACCOUNT_SLOT`／`COLAB_ACCOUNT_HOLDER`／`PATH`，先 `accounts.py claim`）、
`REL` 可覆寫（slot a 預設 `colab-release-A.sh`）、送前檢查、兩輪補缺、跑完只釋放自己的 session。

**估價**：6 支 38 秒；照第 37 集第一輪重拍的實數（118 秒 5.03 CU＝每秒 0.043）約 1.6 CU，加開機 **約 1.8–2.3 CU、15–20 分鐘**。
精修另計（下節）約 **2.3–3.0 CU**。fix4＋精修合計 **約 4–5.5 CU**。餘額剩約 100 CU 時先問站主。

## 送出後挑片要看的、重拍不成的退路

| 鏡 | 挑片要看 | 退路（兩支都不行時） |
|---|---|---|
| s09 | 床上看得到小禾（被子下的身形、頭在枕上），整鏡都在；門關著；只有一桿長槍；秦霜攔胸、不笑；許硯不笑、嘴閉著 | **現用 d1 9381102 c2.0–8.0 照舊**（床尾空著、說得過去是小禾在出框的枕頭那頭）；或在 s09 前後插 s12 那種床上有她的鏡頭不可行（沒有），所以接受並列為已知瑕疵 |
| s17 | 整鏡不笑、瞇眼警覺；句子整句在片中、對嘴；身後沒有空馬；長槍一桿 | **現用 d1 9381102 c1.0–6.4 照舊**（審 2 認為輕笑配「看穿了」說得通）；或改用秦霜錄音 a18-p85 鋪在 s16 尾＋s17 從 c3.6 起（不笑的那段、約 2.0 秒，但只剩句尾對嘴），不建議 |
| s22 | 柵在前景、馬在柵後**有空隙**、沒有木條穿過馬身；四蹄在地、不走；不笑；只有一匹馬、一個人 | **現用 fix2 9381401 c1.25–4.25 照舊**（地理對、馬嵌在柵裡），或放大約 1.4 倍只留小門與火把、馬頭頸（木條仍橫在馬頸前，比較不顯眼）。不換 d1／fix2 9381402（地理反） |

挑片寫 `review-picks.tsv`（同 fix1–fix3 的欄位），選中的再進精修。

## 精修（refine）怎麼做

精修只送草稿與它的第一格（refine.py 沒有參考圖），所以照 `e938refine.sh` 的做法、**只送有換的鏡**：

1. 挑定後，把 `../picks-final.tsv` 的 s09、s17、s22 三列改成 fix4 選中的種子與剪點（source `fix4`）；**同時把 `../review3-trims.tsv` 的剪點也寫進 picks-final**
   （s02 s16 s17 s18 s27b 的新剪點；s34 改 `d1 9381101 1.750 3.750`、s36 改 `d1 9381102 1.250 5.000`）：`PREP=1` 會照 picks-final 重寫 `picks.json`，沒寫進去的 REVIEW 3 剪點會被蓋掉。
2. `tools/heads938.py` 的頭句照舊適用（s09 兩人＋床上睡著的小禾；s17 秦霜；s22 阿令與馬）；s09 要加進「床上睡著的小禾」那組（現在是 s11 s12 s14 s15 s15b）。
3. `PREP=1 PRECHECK_ONLY=1 bash <scratchpad>/e938refine.sh`（0 錯：picks＝picks-final＋s27c2、草稿逐位元、motion_from＝source、提示詞與掃描）。
   refine-prep 要認得 `fix4` 這一輪（fix1–fix3 已經走過同一條路；不認得就照 fix3 的做法補一行來源目錄）。
4. 送：`SESSION=zt-live2 ONLY=s09,s17,s22,s34,s36 bash <scratchpad>/e938refine.sh`（**s34、s36 不必重拍**：REVIEW 3 已換成 d1 另一支，現在剪接用的是草稿畫面放大，一起精修就好）。
   五支約 723 格，照第 37 集每格 0.0032 CU 約 2.3 CU，加開機約 2.3–3.0 CU、約 15–20 分鐘。
5. `python3 <scratchpad>/e938refine-verify.py`（`.seed`＝picks、1312×736、格數同草稿），草稿／精修並排看過；舊精修移到 `refined/old/`。
6. 剪接：`e938cut.sh` 的 `--draft-picture s34,s36` 拿掉、want 表與種子表照新的 picks 改，重跑；s09／s17 換片後重量片中原聲音高（秦霜目標約 205 Hz，`mkov938.py` 的 `AF`），s17 的 `voice_skip` 看新片的雜音。
