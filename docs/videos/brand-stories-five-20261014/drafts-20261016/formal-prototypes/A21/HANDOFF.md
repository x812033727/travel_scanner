# A21 免費 formal prototype

狀態：AUTHOR_FORMAT_PROTOTYPE_ONLY。這是既有分鏡轉正式資料格式的本機原型；沒有真正 verifier/listener/narrative、沒有批准稿件或付費、沒有 host 狀態或上傳授權。

## 輸入與轉換

- 來源：repo `docs/videos/brand-stories-five-20261014/drafts-20261016/storyboards/A21`、正式 compiled stories 的 A21 row 及現有 series。53 個來源檔案全部重算 hash 不變。
- 沿 A16 的原型轉換器及 A37 r2 的原稿／adaptation 保全方式，新增 A21 的精確 pins、33 CID→10 must_verify 項映射與 H04 scalar loop 選擇。generator 是作者映射，仍需獨立核對，沒有自簽內容 PASS。
- 原稿 47 段完整保存在 mapping.original_frozen_paragraphs；active 47 段完整保存在 mapping.active_paragraphs。唯一既有 adaptation 是 T06 主詞改為「稅務機關」，after SHA `75c7cc7af952bdc4fda1ed3ace1f3221187aca074c3cf40e8372ae51cf1ab397`；逐字沿用已審版本，其餘 46 段相同。既有 adaptation 原狀及 root 真正獨審文件都附在 mapping，不改舊文件內的 pending 歷史字樣。
- compiled row 比 episodes/A21.json 多的只有 caveats 後面拼接既有 row review.notes；程式逐值驗證其餘欄相同。使用 compiled row 原樣，沒有刪掉查核限制。
- 89 鏡→89 native scenes，103 line，逐 UTF-16 片段與全文串接完全一致。沒有新增旁白或停頓。
- 97 native claims 全為 UNCHECKED。原段若跨鏡，每列保留原段主張及所屬 source CID；多來源／多事實對應留 null，全部候選索引和 scope 放 sidecar，不擅自縮成單一來源。來源 0–5 與 must_verify 0–9 沒有重排。
- 11 張卡片以 native `title` 的 title/subtitle/tag 分別保留 text/scope/source。所有原始字元與換行在 scene.data 保留；HTML 文字檢查只把換行映射成 renderer 的 `<br>`。尚未做像素排版驗收。
- 78 插畫 prompt/camera/visual 不變；三組開場共圖在 synthetic seed=1 的實際 prompt/cache-key 計算相同。image_asset_key 仍在 sidecar，原生 schema 不直接接受該欄；實際 accepted file/hash 尚未產生，不能把 request 相同當最終圖片相同。
- 繁中字幕 burn_in=false。voice 使用既有 A29 原型 fixture 作離線編譯，沒有當作 A21 試音核准。music 在 synthetic fixture 關閉；正式 branding 資產／時長／連結尚未綁定。

## 8 個 loops 的 scalar 適配

完整原 setup/payoff 陣列、每個原段／line ID 都保存在 mapping.loops。native 只能放一個 setup/payoff ID，所以一般使用完整窗口末句；H04 的兩個法院預告須分清：

- 2007：H03 `a210005` → E07 結束 `a21001p`。
- 2008：H04 **第一句**「隔年，高等法院換了讀法；」`a210006` → T04 結束 `a21001z`，不能取 H04 後面的 2009 句。
- 2009：H04/H05 的完整窗口以 H05 的問題 `a210008` → N01 結束 `a210026`。
- 其他原 loops 均依原窗口適配，沒有新增鉤子、改旁白或丟掉原陣列。這是待獨立審核的格式選擇，不宣稱敘事 panel 通過。

## 真實本機結果

正式 `advanceStory(..., 'script passes lint')` 的離線 relint 分支與 `composeStory` 二次合成完全一致；會回報 origin/idea/engine/turn/now 未通過 lint。Synthetic state 只為執行 relint，寫在標明非主機狀態的 observation：六章 checked/listened=false、check_rounds=0、verified/listener_done=false。未建立 auto.json、verify-1.md、narrative 或 script-review 收據。

- 17 個 lexicon errors：Fredric、Baur、Harold、Hawley、Regular、Pringles、Dippers、Warren、HMRC、Sensations、Poppadoms（重複出現逐筆保留）。沒有填假發音或 null 來消掉錯誤。
- 7 warnings 全文見 compose-lint-evidence.json：generic/face/window 重複提示；136 秒、108 秒無新掛鉤窗口；「二〇〇九年」出現三次；12 tags 只取前10。沒有為這次格式測試改稿。
- cuteStoryVisualProblems=0；官方 shot_reading：78 shots、0 traps。
- 89 scenes、103 lines、97 UNCHECKED claims、33 CIDs、8 loops、11 cards、3 reuse pairs。
- 正式 estimateTimeline：正文 **620.233 秒（10:20）**，hook 45.767 秒、最長鏡9.567秒。六章估45.767／81.033／99.9／143.233／86.7／163.6秒。這含預設句／鏡間隙，沒有手動補停頓，不能當 TTS。
- 原編輯口徑2283字，250/230 cpm 純旁白估547.92／595.565秒；正式 spokenUnits 為2187，差異含英文按詞及「〇」的計數方式，逐段記錄在 evidence，沒有默改原稿數字。
- 無 fetch/stage/API/media 呼叫、無 repo／host 寫入。

## 實際格式限制

既有 `readChapterAnswer` writer-answer normalizer 只接受 shot 與尾章 outro，**會拒絕這裡5章的 title 卡**；hook 雖接受，也不是 lossless（會處理 claim IDs/verdict/note）。正式 compose/schema 允許卡片與真實字典錯誤是另一回事。因此這包不能冒充普通 writer JSON 回答直接餵進 worker，也沒有在本任務實作安裝器。必須以另外受審、保留資料與失效化關卡的匯入方式處理。

正式製作仍缺字典試音、獨立映射審核、真實事實／聽稿／敘事檢查、實錄長度、完整報價和付費授權、圖片驗收和共圖 hash、branding／CC、播放檢查及 owner 驗收。本包不修改既有報價。

## 檔案與執行紀錄

- generator：`build-A21-formal-prototype.mjs`，SHA `eeb294833b0c10828eb651aaaa0893684ac0d4596a554355b04b066dd365a3ea`。
- mapping：`a599e4898a74f5f52f446a7c023d3f53d5d161a374d19679075223fe312ad5cf`。
- compose-lint-evidence：`ca9c97b2d0cf343252eeb4bd70b61aa7fc0cdf34ce869ce9f6f49d75cd9c798a`。
- synthetic video：`6921eb1ebe05dee5e1a3d64e7e2bd9224a85189b7332886f5e5049778da6b6f8`。
- 初次額外 raw-row=compiled-row assertion 揭露正常 caveats review-note 差異，改為驗證精確拼接，沒有改 row。
- 初次 card 檢查把含換行字串直接拿去比去掉 `<br>` 的 visibleText，兩卡 false negative；只修比較器的換行正規化。原失敗輸出與原 generator 保存在 `pre-card-check-attempt/`，正式結果位於本目錄頂層。沒有刪掉或覆寫原稿／原分鏡。
- generator 目前刻意拒絕覆寫已存在輸出；不要在這個已完成資料夾重跑。重現須使用新的隔離目錄並保留相同輸入 pins。
