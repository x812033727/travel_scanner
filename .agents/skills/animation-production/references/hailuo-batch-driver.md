# Hailuo 網頁批次驅動：一次做五集的 3D 國漫短劇（種田娶妻路線）

《種田娶妻打天下》第 1–20 集（2026-10-16～10-18）在 Claude 桌面版內建瀏覽器、窗格隱藏的情況下，用頁面裡的驅動程式一次送一整批首格與片段，每集 30–47 鏡、每鏡一張首格加一支 4 秒片段，約 2,300–3,200 點。這份寫**換一個帳號、換一個 agent（Claude 或 Codex）接手時，從零開始怎麼做、哪些坑已經踩過**。一鏡一鏡手動送、帶收據與變更單的長片做法在 `hailuo-episode-operations.md`；兩份不衝突，短劇用這份。

工具與工作清單都在 `docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/`（下稱 `H/`），本機腳本在 `H/local/`，系列細節與歷史在 `H/README.md`。素材在 repo 外：`<VIDEO_WORKDIR>/zhong-tian-qu-qi-eNNN-dh/`（`VIDEO_WORKDIR`，沒設時用 `H/local/rec.sh` 裡寫的預設），收據 `<VIDEO_WORKDIR>/zhong-tian-qu-qi-receipts.jsonl`。

## 一、站主定下的規則（每集都適用）

- 3D 國漫 CG 畫風、16:9；女角火辣漂亮但不露、不血腥；說話的鏡頭一定看得到嘴在動（`production/storyboard-rules.md`）。
- 每集開場與結尾之外，中段還要 2–3 個以上鉤子（約每 20–25 秒一個）。
- 字幕一律軟字幕 CC，不燒進畫面；系統面板已在畫面上的系統台詞，CC 不重複。
- 英日韓配音與 CC **要等站主確認繁中版之後才做**，先做會白花。
- 有問題照代理的建議走，不用每件事都問；花錢超過預算、改已確認的東西才問。
- 上架：後台一集一個匯入（「教學影片」分頁，category `drama`）；YouTube 五集合一支、一季拍完整季合一支，標題「種田娶妻打天下 第1–5集 | CC字幕」；封面一季一張、不放字、所有語言共用。

## 二、新帳號從零開始

1. **登入**：請站主在內建瀏覽器登入海螺（代理不輸密碼）。換帳號前先確認舊帳號沒有沒下載的東西：所有 `c:` 片段與 `aN-` 首格都要在收據裡。
2. **開四個分頁**（都在 `hailuoai.video`）：
   - 圖片頁 `create/image-generation`：首格與參考圖。
   - 影片頁 `create/image-to-video`：片段驅動。
   - 一個空分頁：開作品詳情頁撈掉出清單的片段。
   - 視需要再一個圖片分頁：單張重畫。
3. **載入頁面程式**：先 commit、push，再從 GitHub raw 用該次 commit 的 sha 抓，存進 localStorage 方便重載後再用。
   ```js
   const base = 'https://raw.githubusercontent.com/<owner>/<repo>/<sha>/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/';
   localStorage.ztbase = base;
   // 影片頁
   localStorage.hailuodhsrc = await (await fetch(base + 'hailuo-dh.js')).text(); eval(localStorage.hailuodhsrc);
   // 圖片頁
   localStorage.hailuodhimgsrc = await (await fetch(base + 'hailuo-dh-img.js')).text(); eval(localStorage.hailuodhimgsrc);
   ```
4. **影片頁的設定**：新帳號預設是「全能參考、5s、21:9」，要改成「起始/結束幀、自動、2K、4s」，底欄顯示 `1 48 創建`（4 秒 × 12 點）。
   - 模式：`__yzv.react(__yzv.leaf('全能參考'))`，再 `__v2.pick('起始/結束幀')`。
   - 時長與比例：點 `__yzv.leaf('5s')` 打開設定面板；面板裡的選項是頁面上**最後一組**同名葉節點，例如 `[...].filter(e => e.textContent.trim() === '4s').at(-1)`，再用 `__yzv.react(el, 6)` 點下去。
   - 改完用 `__yz.bar()` 與 `__yzv.chips()` 讀回確認。設定**每次重新整理都會被重設**，重載後一定要重設。
5. **圖片頁**：輸出張數要是 1（`__yz.one()`；重載可能變回 4 張 × 80 點），比例由 `__zt.go` 自己設 16:9。
6. **點數**：從頁面文字讀，`document.body.innerText.match(/\n([\d,]{4,})\n/)`。一集估價由 `gen-dh.mjs` 印出；送整批之前先確認餘額夠。

## 三、一批五集的流程

1. **分鏡**：一集派一個子代理平行寫。提示樣板與檢查指令見 `H/README.md`「第 16–20 集」一節：照 e015 的五個檔案結構，固定的場景片語，鉤子標成【鉤子N】，三個檢查（`lint`、`drama_craft_check.mjs`、`shot_reading.mjs --route hailuo`）都要過。新角色先加進 `production/cast.json`（英文外貌與 Gemini 聲音，挑還沒用過的聲音），也要加進 `gen-dh.mjs` 的 `DH`、`EN`、`NAMED`。新場景在 `gen-dh.mjs` 的 `SET` 加一條片語對應。
2. **參考圖**：新角色定妝照與新場景寫成 `refs-dh-jobs-N.json`，在圖片頁 `__zt.go(id + '-t1', prompt, 0, aspect)` 一張一張送。
3. **工作清單**：`node H/gen-dh.mjs docs/videos/zhong-tian-qu-qi-e016/video.json H/local/empty-lock.json 16 H/ff-dh-e016.json H/clips-dh-e016.json（第 16 集；別集照改數字）`。檢查每張首格都配到一張 `dh-set-*`；沒配到的表示提示詞沒用固定場景片語。
4. **錄音**：`bash H/local/rec.sh NNN`（Gemini 聲音，要先 `node tools/video/cli.mjs login`）。
5. **配樂表**：`H/edit-dh-eNNN.json`，可照上一集複製。音效名稱來自 `sfx_dirs` 的音效庫，另有合成的 `river`、`rain`、`underwater`、`ding`。
6. **commit、push**，把 `localStorage.ztbase` 換成新的 sha。
7. **首格**（圖片頁）：
   ```js
   localStorage.ztffdh16 = await (await fetch(localStorage.ztbase + 'ff-dh-e016.json')).text();
   void __zt.drive([16, 17, 18, 19, 20], 300);
   ```
   - 完成的圖：`__zt.newdl()` 列出，貼給 `bash H/fetch-dh.sh` 下載，再 `__zt.markdl([...])`。
   - `newdl` 會順便把 `edhN-sNN-t1` 別名寫進 `zturls`，影片頁就是靠這個知道首格好了。
8. **片段**（影片頁）：
   - 把每集的 `clips-dh-eNNN.json` 換成 `ztmiddhN`，鍵從 `aN-sNN` 改成 `sNN`。
   - `localStorage.dhq` 放 `["16:s01", …]`，然後 `void __dhq.run()`。
   - 驅動只送首格已經好了的鏡頭。完成的片：`__dhq.clipsdone()` 列出，下載後 `__dhq.markc([...])`。
9. **組片**：一集全部片段到齊後跑 `bash H/local/asm.sh NNN`，要看兩樣東西：
   - `sheet.png`：手、臉、多餘的人。
   - `final.log`：`held` 超過約 0.5 秒，表示台詞比片段長、畫面會凍格。
10. **總檢查**：`node H/local/audit.mjs`，逐集列出缺的首格、片段、錄音，以及成片比素材舊的地方。
11. **匯入後台**：`node H/local/prep-import.mjs 16 17 …`，再逐一跑 `node tools/video/cli.mjs import --from <VIDEO_WORKDIR>/zhong-tian-qu-qi-import/zhong-tian-qu-qi-eNNN`。
12. **合集**：`node H/compile-dh.mjs 1 5 <out.mp4>`。只改了某一集時，刪掉那一集的 part 再用 `REUSE=1` 重跑。

## 四、打氣迴圈

窗格隱藏時，只有正在被工具呼叫的分頁會往前跑。所以要輪流對兩個分頁呼叫：一次最多 4–5 個動作，每段 sleep 不超過 18–20 秒，否則單次呼叫會撞上 45 秒逾時。

```js
// 圖片頁：撐著、列出完成的圖
await __job2.sleep(15000); [JSON.parse(localStorage.ztlog).slice(-2).join(' | '), __zt.newdl().join('\n')]
// 影片頁：撐著、看門狗、完成的片、掉出清單的、重複的
await __v3zt.sleep(15000); [__wd(), __dhq.log.slice(-2).join('\n'), __dhq.clipsdone().join('\n'), __lost().join(' | '), __dups()]
```

- `__wd`、`__lost`、`__dups` 不在 `hailuo-dh.js` 裡，存在 `localStorage.ztloopsrc`，重載後要再 `eval` 一次。
  - `__wd`：最後一筆 log 超過 240 秒就重啟 `__dhq.run()`。
  - `__lost`：列出還沒完成、但已經不在清單上的片段。
  - `__dups`：同一鏡被送兩次的卡片。
- 換一批集數時，要把三個 helper 裡寫死的集數一起改：
  - `__lost` 裡的 `/^c:a(1[6-9]|20)-/`；
  - `__dups` 與 `localStorage.ztdetsrc` 裡的 `[16,17,18,19,20]`。

## 五、已經踩過的坑

| 現象 | 原因 | 做法 |
| --- | --- | --- |
| 同一鏡被送了 6 次 | `reconcile` 把集數寫死成 1–10 集，第 11 集的卡片對不上，驅動以為沒送過 | 已改成讀所有 `ztmiddhN`；排隊中的重複卡按「取消」會退點 |
| 新一集第 1 鏡的卡片一直對不上 | 冷開場重複上一集最後一鏡，兩鏡的提示詞前 300 字相同；卡片上看得到的文字又被截斷 | `reconcile` 改取最長相同前綴（c68001f24）；同分時不對，手動把卡號寫進 `ztcmapdh` |
| 首格標籤可能貼錯 | 同場景的鏡頭提示詞開頭一樣，只比前 60 字會撞 | `__zt.desc` 讀卡片 React 資料裡的完整提示詞，比前 400 字 |
| 影片頁連續 abort、上傳一直沒反應（`__v2.up()` 一直是空的） | 分頁跑久了狀態壞掉，圖片上傳無聲失敗 | 重新整理分頁，再 `eval(localStorage.hailuodhsrc)` 與 `eval(localStorage.ztloopsrc)`，重設模式與 4s，然後重跑 `__dhq.run()`。重載後 `__dhq.log` 會清空 |
| 首格送出後 `fresh: []`、30 秒後重試 | 圖片與影片共用排隊上限，排滿時建立會無聲失敗（不扣點） | 正常現象，驅動會自己重試。真的懷疑重複時，用完整提示詞搜卡片確認 |
| 片段完成了卻不在 `clipsdone()` 裡 | 排隊 40–55 分鐘，完成時已被擠出建立頁的 30 張清單；首格卡片也會出現在影片頁的清單裡，擠得更快 | `__lost()` 給卡號，在空分頁開 `my-work-detail/ai-video/<卡號>`，跑 `eval(localStorage.ztdetsrc)` 讀無浮水印網址；被彈回首頁表示還沒算完 |
| 下載到有浮水印的片 | 卡片 `<video>` 的 `video_raw_….mp4` 是浮水印版 | 只用 `downloadURLWithoutWatermark`（`clipsdone`、`ztdetsrc` 給的就是這個） |
| 驅動停在上傳那一步不寫 log | 隱藏窗格節流 | 看門狗 `__wd()` 每輪呼叫一次；最後一筆是 `queue empty` 時不會重啟 |
| 單次工具呼叫逾時（45 秒） | 一次 sleep 太久或動作太多 | sleep ≤ 18–20 秒、一批 ≤ 4–5 個動作；逾時後頁面裡的腳本還在跑，先讀狀態再決定 |
| 成片有一段凍格 1–2 秒 | 台詞比 4 秒片段長，片段慢放到 1.35 倍還不夠 | 用 6 秒重拍那一鏡：設定改 6s（底欄 `1 72 創建`），`ztmiddhN` 那鏡的秒數改 6，手動 `__v3zt.upload` 加 `__v3zt.go`，存成 `sNN-t2.mp4`（組片取最後一個 take）。拍完改回 4s |
| 「紅色的手」被畫成像流血（第 18 集賴三沾到薑黃加草木灰的染料） | 只寫 red palm，模型會畫成濕的紅色液體 | 首格整批出來後先排成一張總覽圖檢查；提示詞寫 "stained a flat dry orange-vermilion colour like powdered dye or paint, matte and dry, no liquid, no drips, no wound"。影片已經送出的話，趁還在排隊時按「取消」（會退點），刪掉 `ztcmapdh` 與 `ztcidh` 裡的那一筆，把鏡頭移到 `dhq` 最前面，讓驅動用新首格重送 |
| 手多了一隻（第 7 集孫掌櫃） | 生成瑕疵 | 看 `sheet.png` 抓。重畫首格時提示詞加 "exactly two arms and two hands"，存成 t2，再重拍片段 |
| 角色聲音太像、女角聽起來像男生 | 聲音挑錯 | 先錄樣本給站主聽，確認後才整季重錄。Gacrux 是女聲 |
| `rm` 帶變數路徑被安全檢查擋下 | 防誤刪 | 寫成 `"${W:?}/${id:?}.wav"` |
| Bash heredoc 裡的反斜線被吃掉 | Bash 工具會少一層跳脫 | 含正則的腳本先用 Write 寫成檔再跑 |
| `python -I` 印中文出錯 | Windows 主控台 cp1252 | 直接寫成 UTF-8 檔案，不要印到 stdout |
| 匯入後台只上傳 720p 預覽 | `tools/video/cli.mjs import` 的設計 | YouTube 由站主在 Studio 手動上傳，多語音軌也只能在 Studio 手動加 |
| 後台「漫劇」分頁看不到這些集 | 那個分頁只收站上自動產線的作品，建劇會觸發自動企劃 | 照站主決定用「教學影片」分頁、category `drama` |
| 分頁連同步的 JS 都逾時、截圖也逾時 | 分頁開太久（卡片列表很長）整頁凍住，重新整理也救不回 | 關掉那個分頁、開新分頁到同一頁重新注入；localStorage 是同源共用，紀錄都還在 |
| 送出後 log 是 `"fresh":[]`，下一輪又送同一鏡 | 卡片還沒出現在列表就判定沒送成 | 對帳（`reconcile`）通常會在下一輪補上對應；看到沒對應的新卡號就是重複，能取消就取消 |
| 某鏡送出超過兩小時都沒結果，列表上也找不到 | 早就失敗、失敗卡被擠出列表 | 刪掉那鏡的 `ztcmapdh`／`ztcidh` 對應、`unshift` 回 `dhq` 重送 |
| 列表外已經做完的片 | 卡片被擠出建立頁的清單 | 不用導頁：`fetch('/zh-Hant/my-work-detail/ai-video/<卡號>')` 的 HTML 裡就有 `moss/prod/<路徑>-0_*.mp4`（無浮水印），組成 `label 2 <路徑>` 給 `fetch-dh.sh` |
| 組片在某鏡 `Stray % near ''` 失敗 | 系統面板文字有「%」，drawtext 當成展開符號 | assemble-v4 的 drawtext 已加 `expansion=none` |
| 成片裡手心的染料看起來像血 | 紅色、濕亮、前景失焦 | 能裁就先免費裁掉；要重拍就寫「dry matte orange-vermilion dye powder, no liquid」 |
| 重拍改過提示詞的鏡，驅動說 `already` 不送 | 舊卡還在列表上，reconcile 用最長前綴把舊卡對到同一個 label | 把舊卡在 `ztcmapdh` 改成 `x:old-<label>`，直接 `__oneOrig(id)` 送，再把新卡號手寫進 `ztcmapdh` |
| 兩鏡提示詞一字不差（例：e24 s15 與 e15 s11），一直重送 | reconcile 遇到並列的最佳前綴就不對應 | 手寫 `ztcmapdh`；寫分鏡時避免完全相同的反應鏡描述 |
| 舊集數重拍找不到首格網址 | 換帳號或清掉 localStorage 後 `zturls` 沒了，只有早期的 `ff-urls-dh.txt` | 用 `__zt.go('aN-sNN-t5', …)` 重畫首格（`newdl` 會把 `edhN-sNN-t1` 別名指到新圖） |
| 重拍的片段被舊片蓋掉 | `fetch-dh.sh` 一律存成 `sNN-t1.mp4` | 重拍的片自己 curl 成 `sNN-t2/t5.mp4`；assemble 取排序最後的 take |
| 成片檢查只看幾格看不出換臉、陌生人、低領 | 縮圖太小 | 每鏡取 35%／80% 兩格做檢查圖，分給子代理逐鏡比對分鏡與定妝照，可疑的再抽大圖 |
| 新帳號的 localStorage 是空的，`__wd`／`__lost`／`__dups`／`__rec` 都不見了 | 這些 helper 以前只存在頁面裡 | 已收進 `H/hailuo-dh-loop.js`（`localStorage.zteps` 設這批集數）；舊帳號 CDN 上的參考圖新帳號照樣抓得到，`refs-dh-urls.json` 直接沿用 |
| 新帳號影片頁選不到「自動」比例 | 還沒上傳圖時「自動」的 onClick 是空的 | 直接選 16:9（首格本來就是 16:9） |
| 女角的領口還是低、或立領下是透紗 | 固定外貌只寫 ruqun，模型畫成齊胸襦裙 | 外貌寫明「high stand-up mandarin collar fastened at the throat … thick opaque silk with nothing sheer」；首格整批出來先抽女角近景看領口 |
| 重拍的片段一直被對回舊卡 | 提示詞跟舊卡一樣，reconcile 照前綴把舊卡對回原鏡 | 在頁面 `ztmiddhN` 那鏡的 `[Shot 1] ` 後面加一句開頭（例如服裝、道具的說明），重算前 16 碼 sha；舊卡改 `x:old-`，刪 `ztdlc`／`ztcidh`／`__sentAt` 的那筆，本機舊檔移到 `clips/old/` |
| 失敗卡（狀態 3、5）讓那鏡永遠不重送 | 失敗卡也帶原提示詞，reconcile 把它對回原鏡 | `hailuo-dh-loop.js` 包了 reconcile：失敗卡自動改 `x:fail-` 並放回佇列 |
| 首格與片段排隊互卡、送出常常 `fresh:[]` | 圖片與影片共用約 10–16 個同時進行的上限 | 正常；驅動失敗後的等待在頁面改短（8 秒＋重新整理＋4 秒），送得比較快。一批五集約 7–8 小時 |
| 影片頁跑約 1.5–2 小時後點數不再變、log 出現 abort | 上傳無聲卡死 | 重新整理後一行 `await eval(localStorage.ztrebootsrc)` 重建（模式、4s、16:9、縮短的等待、`__st`／`__dl`／`__p`） |
| 借用的音效庫被別的製作刪掉，組片時 `ENOENT …sound-library` | 音效庫在《偶的江湖》工作區 | `bash H/local/sfx-synth.sh` 合成本劇自己的音效到 `<VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/sfx`，剪輯表 `sfx_dirs` 指過去 |
| 封條、紙張上的紅色印記被看成血；帳本特寫出現看得懂的假字 | 模型自己加紅印、寫字 | 提示詞寫「plain clean white paper … no red marks, no stamps」「tiny abstract ink dashes … no recognisable characters」 |
| 改了角色外貌文字，重畫的圖還是露胸 | 參考立繪本身就是那套衣服，模型照圖不照字 | 先重畫參考立繪（同一張臉、新服裝，用舊立繪當參考圖），產生器改參考新立繪，再重畫鏡頭 |
| 標成 `visual: "still"` 的鏡只重畫首幀，成片沒變 | 3D 版成片那幾鏡其實用片段（`final.log` 寫 `sNN-t1.mp4`） | 重做前先看 `final.log` 用的是 `.mp4` 還是 `.png`；用片段的鏡要一起補拍 |
| 兩個圖片分頁同時畫，畫出重複的圖 | 兩邊跑同一份清單 | 清單照參考圖排序後切成兩半，各跑一半（`hailuo-dh-redo.js` 的 `__redoSplit`） |
| 隱藏的圖片分頁跑一陣子後不再前進，log 沒有新的 OK | 背景分頁的計時器被節流到停住 | 把那個分頁的 `__ztstop` 設成 true，重新載入後再 `drive` 剩下的 |
| 修「像血的紅手」，染料畫到不該染的人手上 | 提示詞只寫「手上的染料」，沒說是誰的手 | 指名誰的手乾淨、誰的手有乾的霧面橘色染料 |
| 重拍舊集數的片早就算好，卻一直沒被收回 | `__lost()` 只看 `zteps` 目前批次的集數，舊集數的卡掉出清單時不會列出 | 送出超過一小時還沒回的重拍，直接 `await __rec(["c:aN-sNN", ...])` 從詳情頁撈 |

## 六、收工

- 每集要過的檢查：`audit.mjs` 沒有缺漏、`sheet.png` 看過、`final.log` 沒有長凍格。手機版用 SendUserFile 傳給站主（超過 30 MB 要另壓一份）。
- 記憶與交接：在 `H/README.md` 補這一批學到的事；這份 skill 只寫通用的做法與坑。
