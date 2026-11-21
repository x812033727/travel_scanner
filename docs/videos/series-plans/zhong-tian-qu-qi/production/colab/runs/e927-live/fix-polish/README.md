# 第 27 集真人版 fix-polish：上架前重拍 s06、s07、s08

2026-11-21。依 `review-zt/consolidated/retakes.json` 的 e027 A／B 三鏡（C 級的 s17、s23、s30 不在這一批）與 `reports/e027.txt` 表 1–3。
base 都是 d1（`picks.json` 的 `motion_from: d1`；d1 兩個種子的提示詞逐字相同，取選中那支的檔）。台詞照稿子原句，三鏡都是模型原聲，說話的人照樣露嘴說。
參考圖全部沿用 base（四張定妝照／場景圖都是平臉、嘴閉著，不需要換）。種子 9279101、9279102；秒數照 base：8＋6＋6，兩個種子共 40 秒草稿。

三鏡共同的改法：場景句裡的封條從 `crossed over them` 改成 `pasted flat on the wood corner to corner in one big X, glued down along their whole length`，並在每鏡把門板與封條寫進該人身後的畫左（d1 的 s07 變兩條垂紙、s08 變「人」字或兩組）。
全部只用正面描述：三支提示詞沒有任何 smile／grin／laugh 字（fix3 的寫法），不能笑的臉逐部位寫，並寫到「until the last frame」。

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- | --- |
| s06 | A | 許硯被當面嘲笑卻整鏡微笑（3 fps 22 格都笑） | `d1/prompts/ref-s06-9271102.txt`（8 秒） | 景別 `low-angle medium shot … framed from the waist up` → `low-angle medium close two-shot … from the chest up, heads in the upper third`（臉大，表情撐得住）；許硯 `still and cold, not smiling: jaw set, lips pressed shut` → 眉壓低往中間皺、眼瞇起盯著魏少卿的臉、嘴角往下拉平、嘴抿成一條細直線、咬肌繃住、下巴平；魏少卿 `mocking: a thin lazy smile` → 抬下巴、挑一邊眉、半垂眼從鼻尖往下看（拿掉同框的笑字，避免傳染給許硯）；扇尖寫明在許硯**左**肩、扇子長約一前臂；動作句加「每敲一下他下顎繃得更緊、眼睛一直盯著魏少卿、嘴角到最後一格都往下」 | 無 | 魏少卿沒有笑字後，他的「拖長音冷笑」只剩抬下巴、挑眉與原聲語氣，可能偏平（稿子「本鏡可以笑」不是必須）。沒照審片句的「從畫右晃進來、收扇、敲兩下」：一鏡一個動作，只拍敲兩下（同 base 與稿子〈真人版的改動〉） |
| s07 | B | 扇子整鏡還搭在肩上沒撥開；封條變兩條鬆垂的白紙 | `d1/prompts/ref-s07-9271101.txt`（6 秒） | `Xu Yan pushes the fan off his shoulder with the back of his right hand as he speaks` → 開口前一記：右手橫過胸口、用手背把扇子從左肩一下揮開，那隻拿扇的手往右下甩出畫、他的手放回身側、之後整鏡左肩上沒有扇子，再說完整句；前景人加 `the back of his head toward us the whole shot`（d1 兩支轉出半張臉和山羊鬍）；許硯 `steady and cold, not smiling: level eyes …` → 眉壓低、盯著對方、下顎繃、嘴角拉平；身後加門板與貼平的 X 封條 | 無 | 揮扇放在說話前，草稿的台詞起點可能晚 1 秒左右，6 秒應放得下（錄音 a06 4.20 秒），剪點要重量。扇子出畫後模型可能又把那隻手帶回來，挑片時看 2 秒以後的左肩 |
| s08 | A | 賴三叉腰咧嘴大笑著說，不擦手、不冒汗、不心虛 | `d1/prompts/ref-s08-9271102.txt`（6 秒） | `framed from the waist up … both hands already gripping the hem of his apron` → `framed from mid-thigh up`、駝背聳肩、**手肘夾緊肋骨**、兩手從第一格就併在肚子前抓著灰圍裙前襟（d1 抓「下襬」兩側就成了叉腰）；`guilty and jumpy, not smiling: brows twitching, eyes darting` → 眉往上往中間皺、額頭與鬢角冒汗、眼睛左右亂飄、嘴角往下繃、嘴只微微開合地嘀咕；動作句 → 整鏡兩手在肚子前的圍裙上用力來回擦、手肘夾在肋旁、嘴角到最後一格往下繃（接 s09 擦手揚粉）；拿掉站著時讀不出來的 `limping on his left foot`；身後加門板與 X 封條 | 無 | **沒加圍觀的人**：審片句要三四個圍觀者，但稿子 2026-11-17 獨立審稿的必改是「s08 拿掉圍觀的人與黑衣人」（無定妝照的群眾易長成第二個賴三），維持一個人；「街上空無一人」這半條沒修，接受或由站主決定。也沒加審片句的前景疊門板（場景圖沒有，維持 base 的長櫃） |

## 檢查（2026-11-21）

```
python3 -I _scripts/polish-build.py 27            -> e927: 3 shots, 6 drafts, 40 s
python3 -I _scripts/preflight-prompts.py …/fixp/colab-jobs.json  -> 0 error(s), 0 warning(s)
h3r.sh check --manifest …/fixp/colab-jobs.json    -> 0 error(s), 0 warning(s)
```

輸出：`~/mokaair-work/videos/zhong-tian-qu-qi-e927-dh/runpod/live/fixp/`（`prompts/ref-sNN-927910{1,2}.txt`、`retake.json`、`colab-jobs.json`）。沒有送出任何工作。

## 挑片時要看的

- s06：許硯每 0.5 秒裁臉看嘴角（尤其魏少卿說話的中段與鏡尾）；扇子敲在左肩、敲兩下；胸上景別頭頂沒被推出畫。
- s07：揮扇是否一下揮開、扇子之後不再回到肩上；前景人只有後腦、沒有鬍子；台詞起點與片中原聲完整。
- s08：兩手一直在肚子前擦、沒上腰；嘴角往下、不咧嘴；汗；封條是一個貼平的 X。
