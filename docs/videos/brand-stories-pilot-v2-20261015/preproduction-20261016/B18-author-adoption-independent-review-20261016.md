# PR #1518 作者六章採用路徑獨立唯讀審查

日期：2026-10-16。範圍：PR #1518 `feat(video): adopt hash-pinned author chapters for brand stories`，只看程式、測試、B18 離線候選；未呼叫正式機、供應商或付費 API，未修改 PR 工作樹。

## 版本與佔用

- PR URL：`https://github.com/x812033727/travel_scanner/pull/1518`；head `b8695951d8f3de44416c589848013747f95378e8`，base／merge-base `4dc42bd020670c4a97a8b8cf199048267731c3b6`。審查時遠端 main `0e0eadc007b57360d3c243880fc46f3946d85d46`；PR `BEHIND`，23 個舊 head checks SUCCESS、draft。
- 工作樹 `<adoption-worktree>`，branch `codex/story-author-chapters-20261016`，`git status --short --branch` 乾淨。票 `tasks/open/2026-10-16-adopt-hash-pinned-author-chapters-for.md` 仍是 `in-progress`，owner `codex-brand-author-adoption`；有已登記工作樹與在用認領。Git 無法證明原編輯者已退出；本會話不直接修改 #1518 或接手票。
- B18 候選在另一工作樹 `<repo>/docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-authored-chapters-candidate/`，尚無採用路徑要求的 `author-package/manifest.json` 或正式 worker／review 收據。該包 `input-pins.json` 指向舊 `tools/video/automation/story.mjs` SHA `f9825a7ce9649111d3e49ab33a2846a8be61111dd2cb2df40db3b68b974676f3`；本 PR 檔案 SHA 為 `8c942a9a59f8e5970946f3b6a0f57c23d25f903ba064c159560e4a0bc0d50ca2`，必須重作 head-bound 整合證據。

## 確認有效的部分

- `tools/video/automation/story.mjs:836-949` 在首次 writer 前核對 slug、六章與當下 `series.json` 的 SHA-256、scene/line/claim ID 與來源／fact 索引界線、全部 `UNCHECKED`，原位元組安裝後標記六章待查；不經 `readChapterAnswer`，故初次保留 title 卡與原 line。錯誤 package 進 `STOPPED_HOLD`，不落回 writer。
- `story.mjs:1208-1222,1431-1509,1518-1550,967-1009` 路由接上六次 `verifier:story`、六次 `listener:story`、全片敘事 panel；A01/B18 另有綁五份文件與真 panel 收據的獨立實稿 review gate，位於 TTS 前。作者稿長度／畫面自動 writer 修正被 `story.mjs:1591,1665` 停住。
- 直接用本 PR 的 `composeStory` 對 B18 六章及保存的 `series.json` 做唯讀合稿，得到 96 scenes／77 shots／19 title cards，`doc.scenes` 與 B18 離線合稿相等；本 PR 的 `lintVideo` 加 `cuteStoryVisualProblems` 配 B18 保存字典 fixture 為 0 errors。這只證資料形狀與第一次合稿，未證正式 checker、媒體或成片。
- 本機曾試 `node --test --test-name-pattern='hash-pinned author|authored last chapter|changed author hashes|authored pronunciation' tools/video/automation/story.test.mjs`：Windows runner 在檔案層以 exit 1 結束，沒有逐案診斷；直接匯入 `story.mjs` 成功。故本報告不宣稱這四案本機 PASS；GitHub 上 23 個 SUCCESS 屬該舊 head 的 CI 證據。

## 阻擋點與最小修正

### P1：採用後的 series 漂移仍可進付費查核（#1518 新增路徑缺口）

`story.mjs:937-942` 記錄 `author_adoption.series_sha256`；但 `1179-1182` 採用後跳過 preflight，`1208-1209` 直接到 `checkChapter`，後者在 `1432` 呼叫 `seriesInfo`，而 `seriesInfo` 在 `528-530` 重讀當前 `series.json`。只要在採用後改一個仍有效的 `plan.sources[0].supports`，下次步驟就會以漂移後企劃讀頁並呼叫 `verifier:story` (`1439-1451`)，沒有與保存 SHA 比較。初次 pin 不能代表後續查核的來源未變。

最小修正：在任何作者稿後續步驟、尤其 `sourcesPayload`／`automation.stage` 前核對 `series.json` 實際 SHA 與 `state.story.author_adoption.series_sha256`；漂移時用專用 `story_author_plan_drift` 停住，編輯後需要新 package／審核綁定。回歸測試放 `tools/video/automation/story.test.mjs`：採用後修改合法 `supports`，下一個 `step()` 應 STOPPED_HOLD，`site.calls.run` 的 verifier/writer 為 0。

### P1：作者 claims 可消失，仍被標記查完（#1518 preflight 與既有 checker／QA 的組合缺口）

`story.mjs:886-887,905-914` 允許每章 `claims: []`；僅驗現有列的索引界線，沒有數量／coverage。既有 `checkChapter` 在 `1452-1458` 只要求模型回 `claims` 陣列，`checkedRows` (`1409-1427`) 可用空陣列清掉全部初始主張，0 個 CHANGED 便設 `checked: true`，六章後 `1464-1468` 寫 `verify-1.md`。`tools/video/qa/facts.mjs:56-63` 只檢查 NOT FOUND 是否仍被場景引用，對「沒有主張」回 PASS；已用純函式呼叫重現 `{"ok":true,"detail":"verify-1.md marks no claim NOT FOUND"}`。B18 候選原有 65 個 UNCHECKED 主張，這條路徑不能默許消失。

最小修正：作者 package 至少要求具審核清單綁定的每項初始 claim；checker 回覆必須對所有原 claim ID 給出明確 verdict 或帶理由的剔除記錄，缺列/空列 STOP，不把未知判決改作已完成。用 `story.test.mjs` 測六章空 claims 的 package、以及 65 項中少一項／回空 checker 結果皆不產生 `verify-1.md`；`qa/facts.test.mjs` 測空主張報告不構成事實 PASS。此 checker/QA 問題原已存在，#1518 讓外部作者稿進入該路徑，風險擴大。

### P1：B18 共圖沒有媒體身份契約（#1518 未涵蓋的正式採用阻擋）

B18 `mapping.json` 的 `image_reuse` 指定 `hook-s004 → idea-s023`、`hook-s005 → engine-s055`、`hook-s006 → turn-s077`，三組原 prompt/camera 相同但 `actual_same_file_verified=null`；`end_visual_reuse` 指定 `now-s101/101b/102/103` 同一張圖、不同運鏡，其實際同檔也為 null。六章 `chapters/*.json` 的 native shot `data` 沒有 `image_asset_key`；該鍵只在 sidecar。`story.mjs:718-720` 只將 scene data 合到 `video.json`，沒有讀 sidecar。`tools/video/media/keyframes.mjs:584-633,683,712` 逐 `scene.id` 產生／選定圖片；`tools/video/assemble/drama.mjs:151-157` 亦按 `scene.id` 取 `keyframes.shots[id]`。`tools/video/media/stages.mjs:283-304` 的 request cache key 包含完整 composed prompt（其中有 camera，見 `keyframes.mjs:558`）與 seed/ref/model 等；前三組在相同條件可能碰巧重用，沒有強制選定 SHA 相同；結尾四鏡 camera 不同，request key 不同，不能藉快取保證同圖。

最小修正：把已審 sidecar 的 `shot → canonical shot` 對應綁進 author manifest／runtime，核對來源先於別名、沒有循環、prompt/視覺意圖與受審對應吻合。keyframes 只生成 canonical 的選定圖片，別名 manifest 記錄同一已接受 file/sha256 與 `reuse_of`，各鏡仍保留自己的 camera/motion；來源變更時別名一同失效。測試 `media/look-keyframes.test.mjs` 驗三組及結尾四鏡選定 SHA 完全相同、只支付 canonical 圖、漂移 fail closed；`assemble/drama.test.mjs` 驗同 SHA 下的四種運鏡仍各自輸出。真正媒體產出後需保存接受圖片 SHA 與實看片尾節奏，不能以同 prompt 充當實際共圖證據。

### P1：title 來源卡在 checker patch 後可靜默消失（既有 patch 與 #1518 作者卡相容缺口）

第一次合稿確實保留 19 張 title 卡。但 `story.mjs:1453` 的 checker `applyPatch` 未用 `mayDrop` 限制；`applyPatch` 在 `1387-1401` 可刪一張卡的唯一旁白 line，接著把沒有 line 的 scene 整個移除。B18 九組來源疊字移到 title 卡，卡片消失可能連同來源歸屬消失；目前測試只 assert 採用當刻的 `doc.scenes[1].template === "title"` (`story.test.mjs:916-923`)，沒有 checker/listener 後的原卡集合檢查。

最小修正：作者稿的受審卡片 ID/內容建立保護清單；checker 要刪最後一條卡片 line 時先 STOP 到編輯審查，或出具明確卡片移除變更單；在每次 relint 與 pilot receipt 前核對保留集。回歸測試讓 checker 回 `{drop:[<某來源卡唯一 line id>]}`，不得默默得到少一張卡的 `video.json`。

### 整合／付費邊界

此 manifest 僅有 local `series_sha256` 加六章 SHA，沒有 B18 `input-pins`、`mapping`、獨立審稿收據、編譯 row SHA 的可信綁定。B18 候選尚未生成並由獨立 reviewer 確認與**正式 start 後實際** `series.json` 相符的 manifest；離線候選的 series hash 不是 live worker 的證據。`story.mjs:954-969` 對 `story-five-*` 回 null，五支沒有 A01/B18 的 frozen editorial／independent actual-script 收據；普通 verifier/listener/narrative 仍在，但不能拿它們代替外部作者稿與正式成稿對齊。此 PR 沒有新增五支的逐片付費限額或發布授權；#1518 的 CI 與 adopted 狀態也不等於任何片獲准花費、已完成或可上傳。

最小整合測試：用 B18 **實際候選包**（96鏡／65 claims／11 loops／19 cards）與新 worker head 建完整 manifest，在隔離環境演練 `draftStory → adopt → checker → listener → narrative → pilot receipt gate`，斷言採用前 0 writer/paid、claims 不掉、title/source cards 不掉、source/hash drift STOP、末尾及 hook 共圖 alias 保持；每片獨立成本與批准紀錄另由主控審核。五支則逐片提供相同的來源／獨立實稿審查與付費界線，再跑同類整合測試。

## Verdict

**HOLD：#1518 目前 head 可證明「六章初次原樣合入」，不能宣稱 B18 可正式採用，更不能據此啟動 B18 或後五支付費製作。** 在上述資料漂移、claims 保全、共圖身份、卡片存續與真 B18 head-bound 演練完成之前，不建議合併／部署此採用路徑。PR 綠燈只對舊 head/base 生效；修正後需要重測並重新獨立審查。票與工作樹仍由 `codex-brand-author-adoption` 佔用，先協調原 owner，避免跨工作樹改其檔案。
