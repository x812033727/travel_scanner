# 第 9 集真人版 fix-polish 第 4 輪（第二波，W2）：s26

種子 9099401／9099402，960×544 Ref2VA，2 支、12 秒草稿（成片只用約 3.5 秒）。

| 鏡 | 錯在哪（現行成片） | base | 改了什麼設計 | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s26 | 166.04–169.54：握刀的手粗、青筋，像中年男人；刀是雙刃尖匕首，跟第一波修好的 s30 不同 | `fix2/prompts/ref-s26-9091301.txt`（picks：fix2 9091301，end-before 3.5） | 改用道具圖鎖手與刀：新 s30 阿令左手握刀那一格裁成 `prop-bishou-w2`；刀照圖寫死（尖刃一掌半長、中間一道脊、小深色銅護手、深色木柄比手掌略長），手寫纖細、皮膚光滑、指節小；拿掉 not curved／no guard／no other blade 等否定句；只做「手指收緊一次、指節微白」 | **新 `prop-bishou-w2`**（`clips/s30-t5.mp4` 第 0.5 秒裁）＋ `set-xujia-lingfang-l1` | 道具圖裡刀是斜向上、在她腰前，這鏡要平指許硯領口，可能照圖畫成斜的；圖裡有腰帶與衣身，可能畫出半個身體 |


檢查（2026-11-22）：`polish-build.py 9 4`、`preflight-prompts.py fixp4/colab-jobs.json`、`h3r.sh check` 都 0 錯 0 警告。沒有送出、沒有改 `polish-build.py`。
