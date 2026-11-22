# 第 14 集真人版第四波重拍（round6，2026-11-22）

依據 `review-zt/WAVE2-BRIEF.md` 的寫法與禁止事項，加上 `ROUND2-BRIEF.md`「同一個錯再出現就改設計」。種子 9149601、9149602；1 鏡 2 支 12 秒 → `runpod/live/fixp6/`。沒有送出任何工作。base `fixp5/prompts/ref-s12-9149502.txt`，圖照 base（`aling-portrait-l1`、`angles/aling-angle-a-l1`、`set-xujia-zoulang-l1`）。

| 鏡 | 錯在哪 | 改了什麼設計 | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- |
| s12 | 「京城」三次都念錯：d1 9141101「清晨」、round5 兩支「清城／青城」（`../round5/review-picks.tsv`）；拼音提示沒用 | 不再對嘴：改成阿令右肩後的過肩背影（她在畫右半、頭背對鏡頭到最後一格、最多看到左耳緣），朝畫外左的許硯；她不說話、嘴閉著，台詞改鋪錄音 `audio/zq914a12.wav`（4.64 秒）。保留 9149502 的好處：背影寫清楚半披髮（頭頂高髻橫插一根木簪、下半長髮直垂到腰）、燭光勾出髮緣與右肩；畫左半是虛焦的走廊，只寫木樑、灰泥牆、兩點燭火、一盞圓紙燈籠。一個動作：頭微偏向畫左的他並停住；冷用肩頸寫（肩平穩、頸直繃、背挺、手垂身側不動）。鏡長 8 → 6 秒（錄音前後各約 0.7 秒；背影越長越容易轉頭） | 無 | 模型可能讓她轉頭露側臉或嘴動（Ref2VA 自己出聲）：挑片看嘴是否入鏡、有沒有出聲，草稿音軌剪接時整段換成錄音；定妝照是正面與 3/4，背影的髻與簪位置靠角度圖推；畫右半的身體可能被畫得太大蓋住燈籠 |

## 接戲（現行成片 `_live-e914/.../cut/e914-live.mp4`，final.log）

- s11（50.67，`s11-t5`）、s13（59.96，`s13-t5`）都是許硯近景、臉朝畫右，身後燭光土牆與走廊燈籠；阿令在 s12 朝畫左看他，軸線不變。

## 剪接表要改

- s12 改 `voice_off` 鋪 `audio/zq914a12.wav`，拿掉 s12 的 `clip_af 0.88`；草稿原聲（環境聲以外）不要留。

## 檢查

```
python3 -I _scripts/polish-build.py 14 6                         -> e914: 1 shots, 2 drafts, 12 s
python3 -I _scripts/preflight-prompts.py …/fixp6/colab-jobs.json -> 0 error(s), 0 warning(s)
h3r.sh check --manifest …/fixp6/colab-jobs.json                  -> 0 error(s), 0 warning(s)
```
