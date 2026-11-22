# 第 22 集真人版 fix-polish 第五輪（第二波 s14 再拍，2026-11-22）

第 4 輪 s14 兩支（9229401、9229402）跟現行片段一樣：唐小棠珍珠簪單髻、長粉帶垂到胸前，獨立挑片判 RETAKE（`round4/review-picks.tsv`）。
原因是正面定妝照 `tangxiaotang-portrait-l1` 本身就是這個髮型，第 4 輪拿掉 angle-a、改字都修不掉。協調者決定照系列聖經改設計，不需要站主點頭：
`r2-bible-e021-e030.md` 拍法第 3 條（唐小棠的鏡從背後拍、雙丸子頭粉緞帶），`r2-bible-e031-e040.md` 也記了正臉會畫成單髻。
種子 9229501、9229502；1 鏡 2 支 12 秒 → `runpod/live/fixp5/`。base 仍是成片現用的 `d1/prompts/ref-s14-9221102.txt`。

| 鏡 | 錯在哪 | 改了什麼設計 | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- |
| s14 | 唐小棠全集唯一的臉是單髻插花長粉帶，前後鏡背影是雙丸子；第 4 輪仍一樣 | 低角度中景，過唐小棠背影（右前景，正背對、頭不轉、兩顆高丸子各一條短粉緞帶、後頸露出）拍桌子對面的小禾；小禾說台詞（模型原聲）；唐小棠不說話，唯一動作是伸筷子把一大塊滷肉放進小禾碗裡 | 拿掉 `tangxiaotang-portrait-l1`，改送背影 `tangxiaotang-back-shuangji-e922-w2`（現行 `s15-t1.mp4` 第 2 秒裁，來源見 refs-live README）；小禾定妝照與桌面場景圖照舊 | 構圖跟下一鏡 s15（同樣過她的背影拍小禾）很像，兩鏡連著會像同一個機位，靠低角度、景別稍寬與夾肉的動作區分；稿子的「甜笑、眼角紅」從背後看不到；背影圖右邊帶一盞燭，可能多畫一盞燈 |

## 三個檢查

- `polish-build.py 22 5`：0 錯，1 鏡 2 支 12 秒。
- `preflight-prompts.py …/fixp5/colab-jobs.json`：0 error、0 warning。
- `h3r.sh check --manifest …/fixp5/colab-jobs.json`：0 error、0 warning。
