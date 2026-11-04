# sothatswhy-p05-down-jacket 製作紀錄

企劃：[`brief.md`](brief.md)（形式沿用 P02 定案：[`../so-thats-why/dialogue-pilot-20261103/README.md`](../so-thats-why/dialogue-pilot-20261103/README.md)、
評分表 [`SCORECARD.md`](../so-thats-why/dialogue-pilot-20261103/SCORECARD.md)）。查核來源：[`claims.md`](claims.md)。範本：[`../sothatswhy-p02-cloud-rain/`](../sothatswhy-p02-cloud-rain/)。

## 稿子怎麼產生

整份 `video.json`（scenes、loops、角色、聲音、youtube、縮圖、sources）都由 [`build_scenes.py`](build_scenes.py) 產生：
`python3 build_scenes.py` 直接改寫同一個資料夾的 `video.json`，再 `node tools/video/cli.mjs lint --slug sothatswhy-p05-down-jacket`、
`node tools/video/cli.mjs script --slug sothatswhy-p05-down-jacket` 重產 [`script.md`](script.md)。改台詞或提示詞改這支檔再重產，
不要只改 `video.json`，不然下次重產會被蓋掉。

- **角色與聲音**：`chief`、`kid` 兩個物件與 `voice` 跟 P02 逐字相同，P02 已核准的設定圖（所長 E、小問 B）直接沿用；改任何一個字，設定圖與所有關鍵影格都會過期。
- **運鏡凍結在 [`cameras.json`](cameras.json)**（P02 的教訓：運鏡照順序輪流指派，一張改成卡片後面全部位移、快取全失效）。
  `build_scenes.py` 先讀它，只有新鏡頭才從輪替裡拿下一個運鏡並寫回。之後把鏡頭改成卡片或刪掉，其他鏡頭的 `camera` 不會變；
  不要刪 `cameras.json`（插圖畫好以後刪掉就會整集重畫）。
- **提示詞的寫法**（P02 四輪重畫學到的，都寫進產生器）：動作在前、長相在後（`kid()`、`chief()` 把 `KIDDESC`／`CHIEFDESC` 接在最後）；
  所長一律 waist-up medium shot 或 head-and-shoulders close-up、素牆（`chief()` 有斷言）；小問雙手在做動作，不拿筆記本；
  機制特寫由小問拿放大鏡看（羽絨、溫度計、保溫瓶剖面）；兩個角色不同框；不寫海報、白板、招牌、書背；物件不畫臉。
  主線物件是同一件 `a puffy coral-orange down jacket`（`JACKET`）：不用 teal（lint 當成畫風字）、不跟小問的藏青外套與芥末帽撞色；
  小問不穿上它（設定圖的藏青外套會打架），只抱、摸、包、拿。
- **自我檢查**（lint 不管 `sothatswhy-` 的系列規則，所以產生器自己印）：插圖占比、連續卡片 ≤ 3、鏡頭 ≤ 12 秒、小問一句 ≤ 15 字、
  所長一句 ≤ 25 字、每 45 秒內有一個問句或伏筆、沒有三個同運鏡連在一起。

## 2026-11-04

- **撰稿**：7 章（開場＋5 章＋收尾）、176 句、108 張插圖、8 張卡片（插圖 93%，連續卡片最多 2 張）、`loops` 21 個全部回收。
  小問約 24% 字數（35% 句數），每句 ≤ 15 字；所長每句 ≤ 25 字；每章結尾停在小問的一個問題上，所長每章至少一句「你」。
  lint 估 10.4 分鐘（2,178 字），0 錯誤、17 警告；純字數照 4.5 字／秒算約 8.1 分鐘正文，P02 實錄比 lint 估計長約 6%。
- **數字只用 claims.md 的可用說法**：大人安靜坐著「大約一百瓦左右」（不說小問是一百瓦：小朋友「少一些，但也一直在放」）、
  發抖「好幾倍」、鋼鐵比木頭「快上百倍」、水比空氣「大約二十幾倍」。冰塊只說「很多學校課堂都會做這個比較，包起來的融得比較慢」，
  不給時間與溫度；畫面上用羽絨衣包冰塊是想像實驗。保溫瓶說「擋回去很多」「瓶口沒有真空，熱還是會慢慢溜」，不說完全擋住；
  風寒說的是露出的皮膚，溫度計不會因為風變低。沒用：80–100 瓦範圍、濕衣服失去九成保暖力、25 倍、ILO 的「壓住處較冷」（未讀到原文）、產品史。
- **brief.md**：lint 要求標題是「## 站主觀點」，原本是「## 站主觀點（草稿）」，只改了這一個標題（內容不動）才能 0 錯誤。
- **已知不改的警告**（同 P02）：有角色的影片套漫劇的 `craft` 節奏警告（鏡頭中位數、句長、insert、wide、motion.look 等），解說不為消警告切碎；
  「black」「yellow」「wear」出現在每張插圖，是每張都要重述角色長相；開場約 50 秒（片頭後第 2 句就是第一個問題，P02 也是 45 秒）。
- **下一步**：另一個代理逐主張查核（`verify-1.md`）→ 兩位新讀者盲評 `narrative` → 站主看 `script.md` → 旁白 → 插圖整集一次報價。
