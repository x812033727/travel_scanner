# 第 39 集真人版 fix3：REVIEW 2「剪接救不了」的三鏡（s32、s39、新鏡 s40b）

fix3 準備代理 2026-11-25 寫。依據：`../cut-notes.md` REVIEW 2〈剪接救不了、建議重拍的〉第 1–3 條、`../cut-review.md` 問題 5（s39 群眾消失、套繩在地上、近乎定格）、
問題 6（s40 結尾沒有人回頭看許硯）、問題 18（s32 小禾像興奮在笑）、協調者的交辦（s39 保留 fix1 的直立長槍，不改橫槍）、`../picks-final.tsv`、
`../fix1/{plan.md,mkspec.py,mkjobs.py}`、聖經 `r2-bible-e031-e040.md`（第 31 條畫外視線、第 34 條群眾每人一種衣色年紀、跪拍到膝）、任務檔第 34 集 fix4（背影鏡的寫法）。
成片（REVIEW 2 後）：`/root/mokaair-work/videos/_live-e939/zhong-tian-qu-qi-e939-dh/cut/e939-live.mp4`。
**本代理沒有送 Colab**、沒用 RunPod、沒付費圖、沒有新圖（s40b 用現有的 `set-gucang-wai-l1`）；只做了 DRY／PRECHECK。
**repo 規則（main #2224，2026-11-25）**：docs/videos 底下不 commit 圖、聲音、影片；本輪只 commit 文字檔（`mkspec.py`、`spec.json`、`mkjobs.py`、`plan.md`）。

## 重拍清單（3 鏡 6 支、34 秒）

種子 **9391501／9391502**（93912xx 開門圖 Qwen、93913xx fix1、93914xx fix2 與它的 Qwen 都用過）。

| 鏡 | 秒 × 支 | 基底（照送出的工作與提示詞，sha256 核對） | 問題 | 改什麼（英文原句在 `mkspec.py`） |
|---|---|---|---|---|
| s32 | 6 × 2 | d1 9391101（成片用的那支） | 小禾說「我沒看見臉」時像興奮、在笑（203.0–204.0 露齒）；d1 的 `scared and trying hard to remember` 畫成急著回想的亮臉 | 只改臉：`frightened`、眼睛睜大含淚、眉頭往中間皺起、嘴唇發抖、聲音小而抖、肩膀縮起＋NOSMILE；動作結尾再寫一次「到最後一格都害怕、嘴唇發抖」。圖、構圖（半坐靠枕、頭在畫右的枕頭那頭、兩手抱草兔子）、比帽簷與下巴繩的手勢、說話句（剪接用片中原聲對嘴）、**慢推鏡**（跟成片那支同一個構圖）、6 秒都照 d1 |
| s39 | 6 × 2 | fix1 9391302（成片用的那支） | 田頭的村民整批不見、套繩整條在地上（d1 的 `the slack neck rope crossing soft in the lower foreground` 就是它）、六段 0.45–0.6 秒靜止像照片配嘴 | 前景左緣與左下角：s36 十人裡的四個（炭灰瘦中年、深橄欖綠胖五十歲、深灰配舊靛藍頭巾的中年婦人、本色麻短衣頭巾的寬背四十歲），**只見後腦與肩、虛焦、擠在畫緣、面向她**；拿掉地上那條繩，寫「麻繩套在他脖子上拉緊成套索、從第一格到最後一格、繩尾垂在胸前」；刁七在畫右、離前景四人遠（膝蓋不被擋），兩膝著地全身照 fix1；她的視線改成「朝前景左邊那四個村民」（不再是畫外，拿掉『那一側只有空地與水田』）；人數句「六個人、前景四人只見背影」寫兩次；動作加「前景四人整支挪腳、往刁七那邊傾、有人轉頭跟旁邊的人」與「刁七嚥一下口水、抬眼看她一下又垂下」；鞋句加「其他人深色布鞋」；**fix1 的長槍（直立、完整、槍頭在上、全長在框裡）與固定鏡照留** |
| s40b（新鏡） | 5 × 2（用 1.5–2 秒） | 工作欄位取 d1 s36 9391101（同一張穀倉前整張圖）；提示詞整段在 `mkspec.py` 寫好 | 結尾沒有人回頭看許硯，讀成「他說完了」不是「全村都看許硯」 | 穀倉前整張圖 `set-gucang-wai-l1`（不送任何人像）：中遠景、腰以上，s36 那六個村民（白髮小髻灰長袍老人、炭灰瘦中年、舊靛藍十五歲少年、深橄欖綠胖五十歲、深灰配靛藍頭巾婦人、本色麻短衣頭巾寬背四十歲）**背對鏡頭**站成一排面向穀倉；畫右下緣那條踩實的土路（圖上的土埂，往村子的路）空著；鏡頭中段六人**同時轉頭看向畫右下緣的路**、肩膀跟著轉，之後一直朝右到最後一格，仍背對鏡頭、最多露一點頰邊；**不點名許硯、不寫他的人**（第 40 集第一鏡才入鏡）；沒人說話；人數句兩次；「never the mood.」分隔句放在場景句（照 fix1 s38）；固定鏡；同一個清晨低角度暖陽 |

**s40b 怎麼接進成片**：它是 s40 之後的新鏡（剪接決定放在 s40 收尾或片尾），挑完片後在 `../picks-final.tsv` 的 s40 下一列加
`s40b	fix3	<挑中的種子>	<start>	<end_before>	<note>`（source 寫 `fix3`，片源 `/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/fix3/out/s40b-<種子>.mp4`），
剪接表與組片的鏡頭清單也要加 s40b（沒有台詞、沒有錄音；音效是群眾倒放人聲加一聲回頭的衣料聲，重音照 REVIEW 2 #6 的 reveal-hit 挪到 s40b）。
精修（refine）若要做：s40b 不在 `hailuo/clips-dh-e939.json` 裡（`check939f3.py` 對它跳過 clips-dh 的檢查），要另外補一條沒有人像的精修開頭（照 s19／s03 的 `NOPERSON_REFINE` 做法）。

## 檔案與指令（2026-11-25，全部跑過、0 錯）

```
python3 -I mkspec.py                                    # 3 shots -> spec.json (17 s per seed, 34 s)；每個 replace 在基底提示詞裡剛好一次
python3 -I mkjobs.py <live>/fix3                        # scan 0；colab-jobs.json 6 支、34 秒
python3 -I <scratchpad>/tools/check939f3.py <live>/fix3 # check939.py 的逐鏡斷言（tools/mkcheck939f3.py 從 e939prep/check939.py 改 19 處生成：s40b 加進 FULL 與穀倉前、
                                                        #   s39 不再是畫外視線、s32 留推鏡、s39 s40b 固定鏡、加 fix3 逐鏡斷言），通過
python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json                          # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix3/colab-jobs.json   # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix3/colab-jobs.json  # 0／0
bash <scratchpad>/e939f3/scan.sh                        # prep939 的否定名詞／會長字的名詞／掛著的東西／舊字：全 0（`hanging` 改 `falling down over his chest`）
DRY=1 bash <scratchpad>/e939f3.sh                       # rc 0（另測 GPU=A100＋COLAB_ACCOUNT_SLOT=a＋PATH 帳號 A：release 自動換 colab-release-A.sh）
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live`。
`e939f3.sh`：`COLAB_GPU=${GPU:-G4}`、`SESSION` 預設 `zt-live3`、**不設帳號**（外部設定，或包在 `acctA-run.sh` 裡）、`REL` 可覆寫；送前重跑 mkspec／mkjobs 與上面全部檢查；
**單輪**（`h3_detached.py` 跳過已有 mp4 的工作，重跑就是續跑）；跑完 `ONLY_SELF=1 bash $REL $SESSION`。

**估價**：34 秒 × 約 0.043 CU／秒（第 37 集 fix1 實際）≈ 1.5 CU，加開機，約 **1.5–2.5 CU、0.2–0.3 小時（G4）**。以跑之前的餘額為準；剩約 100 CU 時先問站主。

**跑的指令**（協調者；先確認 `zt-live3` 上沒有別的集在跑）：
```
bash /tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/acctA-run.sh bash /tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/e939f3.sh
# 帳號 B：外部設好 B 的 PATH 後直接 bash .../e939f3.sh；GPU=A100、SESSION=zt-live2 可覆寫
```

## 送出後挑片要看的

- s32：整支害怕、嘴唇發抖、不笑也不露齒；頭在畫右的枕頭那頭、半坐抱草兔子；手勢（頭頂比帽簷、下巴比繩）還在；嘴形對得上片中原聲。
- s39：前景左緣、左下角有村民的後腦與肩（不是空地）；套索在刁七脖子上、地上沒有一整條繩；刁七全身兩膝看得見；長槍整支直立、槍頭在上；整支有在動（前景挪動、刁七嚥口水抬眼），沒有定格。
- s40b：六人都背對鏡頭、同時轉頭往畫右下的路看、沒有人正面對鏡頭、沒有人說話；穀倉與水田照 s36、清晨暖陽；中段轉頭前後各留得下 1.5–2 秒。
- 結果與選擇寫在 `review-picks.tsv`；s32 s39 取代 `../picks-final.tsv` 那兩列（d1 9391101／fix1 9391302 留作備案），s40b 照上面加一列。
