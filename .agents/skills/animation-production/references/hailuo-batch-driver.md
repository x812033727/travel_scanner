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
| 手多了一隻（第 7 集孫掌櫃） | 生成瑕疵 | 看 `sheet.png` 抓。重畫首格時提示詞加 "exactly two arms and two hands"，存成 t2，再重拍片段 |
| 角色聲音太像、女角聽起來像男生 | 聲音挑錯 | 先錄樣本給站主聽，確認後才整季重錄。Gacrux 是女聲 |
| `rm` 帶變數路徑被安全檢查擋下 | 防誤刪 | 寫成 `"${W:?}/${id:?}.wav"` |
| Bash heredoc 裡的反斜線被吃掉 | Bash 工具會少一層跳脫 | 含正則的腳本先用 Write 寫成檔再跑 |
| `python -I` 印中文出錯 | Windows 主控台 cp1252 | 直接寫成 UTF-8 檔案，不要印到 stdout |
| 匯入後台只上傳 720p 預覽 | `tools/video/cli.mjs import` 的設計 | YouTube 由站主在 Studio 手動上傳，多語音軌也只能在 Studio 手動加 |
| 後台「漫劇」分頁看不到這些集 | 那個分頁只收站上自動產線的作品，建劇會觸發自動企劃 | 照站主決定用「教學影片」分頁、category `drama` |

## 六、收工

- 每集要過的檢查：`audit.mjs` 沒有缺漏、`sheet.png` 看過、`final.log` 沒有長凍格。手機版用 SendUserFile 傳給站主（超過 30 MB 要另壓一份）。
- 記憶與交接：在 `H/README.md` 補這一批學到的事；這份 skill 只寫通用的做法與坑。
