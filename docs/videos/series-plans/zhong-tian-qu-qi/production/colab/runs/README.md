# 每一集實際跑過的清單與提示詞（第 33 集起）

站主 2026-10-31：「不要我用其他對話他還要跟我要參考圖片跟資料那些的。」這裡是每一集在 Colab 上**實際送出**的東西，從工作資料夾
`<VIDEO_WORKDIR>/zhong-tian-qu-qi-eNNN-dh/colab/a/` 原樣複製（只收文字：manifest、提示詞、紀錄；不收影片與首格圖）。

為什麼要留：`ref2manifest.mjs` 與 `cast.json` 之後還會改，重跑它產生的提示詞不一定是當時用的那一份；重抽時手改的提示詞（例如第 37 集
s29「全程怒容、不笑」、s37「寬刃單刃彎刀」）也只在這裡。要重拍某一鏡、或查某一鏡為什麼長這樣，以這裡為準。

| 位置 | 是什麼 |
| --- | --- |
| `eNNN/st1/` | 第一段（Ref2VA 960×544 草稿）的 manifest `ref-eNNN-partK.json` 與 `prompts/ref-sNN.txt`、`run.log` |
| `eNNN/retakeK/` | 重抽的 manifest 與改過的提示詞（seed 在 manifest 裡） |
| `eNNN/st2/` | 第二段（refine σ0.5、10 步、1312×736）的 manifest 與 `prompts/sNN.txt`；`input_video` 指出用的是哪一份草稿 |
| `eNNN/takes.tsv` | 每一鏡最後用的草稿（第一段或哪一次重抽）、第二段 seed、出自哪份 manifest（第二段做完才有） |
| `eNNN/*.log`、`*.sh` | 該集第二、三段的紀錄與當時的腳本 |
| `_scripts/` | 這個 session 排程用的腳本（`st1.sh`、`st23.sh`、`mk-st2.py`、各集的 chain 與單鏡重抽）；整理過的版本在 `../route-a/` |

manifest 裡的參考圖路徑是工作資料夾的絕對路徑；對應的圖在 `../../assets/refs-dh/`（同檔名，`SHA256SUMS` 可核對）。


每集的 `cut/` 是剪接時的紀錄：`final.log`（每鏡用哪個 take、在成片的起點與長度、在哪裡切開），`dub-<語言>.log`（八語配音逐句的長度與加速倍率）。`e031/first-frames/` 是第 31 集小樣的 9 張首格（路線 B，成片沒有用）。從工作資料夾原樣複製（2026-11-04）。

每集的 `dub/<語言>/fit.json` 是八語配音對進剪接的方式：每句的開始時間、空檔長度、原長、加速倍率與結果。有了它和雲端 `recordings/` 的原始錄音，修一句配音時只要重做那一句，不必整條重對。從工作資料夾 `segments-v4/dub-<語言>/` 原樣複製（2026-11-05）。
