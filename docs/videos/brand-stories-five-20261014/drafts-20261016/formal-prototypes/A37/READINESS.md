# A37 正式章節格式原型 r2

**只完成本機格式準備，存在真實字典錯誤，尚不能交工作者製作。** 無外部 API、主機操作、付費媒體、repo 修改或 production PASS。

## 原文與來源界線

- 原完整稿仍是48段／2152編輯字數，SHA 63e6277c85cc573556651f686cbf7722d602c620265e7730a9f3f32b7d016d09，逐段重建成功，原檔沒有改寫。
- 此次正式形狀使用已獨立接受的 active 分鏡48段／2136字，只包含既有 I03、E10、T01a 三處來源限縮。active narration SHA 6ac46a8cc8b78a96903cf30cb2a81de2b06467726511535e58ff3f996d916cce。沒有新增任何旁白修改；兩種 SHA 不混用。
- I03 不復活「戰爭帶來的壓力」；E10 只說官方紀錄中的國家隊球鞋，不說密切合作；T01a 只比較旋入式鞋釘結構，不把 PUMA 的天候回憶套在 Adidas。私人分裂起因、1936 Owens、1954 唯一勝因與中場換釘均未新增。
- 2009 是後來的員工／管理者等混隊活動，700是支持者，不是兄弟生前和解。7比5和混隊結果仍依原順序出現。
- 30 CIDs 對應75列正式形狀 claim，全部 UNCHECKED。來源多候選及 must_verify 多候選各自保留 null；完整候選和限制在 mapping。原 row review 的 reviewer_only[0] 指既有 must_verify 主張的人工證據限制，不是所有新章稿已核准。

## 已完成的格式轉換

- 48個 active 原段逐字切成90個唯一ID片段，86鏡；UTF-16切片完整、無遺漏、無重疊、無重排，未加 say 或 pause。
- 72插畫／14卡、69個預定不同插畫。14卡皆原生 title，原 text→title、scope→subtitle、source→tag，cc_safe=true；沒有杜撰scope。官方 template 與 HTML visibleText 保字檢查通過，尚無像素／手機可讀性驗收。
- 10組 loop 的完整 setup／payoff 段落窗均保留。r1 曾把第一組 H03＋O08 的 scalar setup 放在 O08，導致工具只數到兩個開場預告；r2 僅改為原 H03 最後片段 a370005，O08 留在 sidecar 作再提醒。原 loops、全部 scenes／claims／文字和 payoff 不變。loop-anchor-delta.json 與 previous-attempt 保存真實修正及先前報告。
- 三組共圖為 S004→S024、S005→S040、S006→S082。prompt／camera／key 逐字保留；合成同 seed 請求的 cache key 相同，仍須正式產圖後比較 accepted 檔案 SHA，不能以 sidecar key 當成已共圖。
- 官方 composeStory 與 advanceStory 的離線 relint 分支實際執行；shot_reading 72鏡／0 traps，cute gate 0 errors。模型、媒體、外部 API、正式主機和 repo 寫入皆0。

## 真實待處理事項

1. **字典仍有24處／9種詞錯誤：** Adidas、HISTORY、RUDA、PUMA、Adolf、Dassler、SUPER、ATOM、BRASIL。保存的 A29 同一 lexicon fixture 未加入假讀音或 null；這不是正式站最新字典讀取。需正式讀音及音訊驗收。
2. **章稿採用入口有缺口。** origin／idea／engine／turn／now 的 readChapterAnswer 拒絕 title；hook 雖接受卻會丟掉 native claim ID／verdict／notes。compose 能合成不表示既有普通 row 匯入會採用作者章稿；它仍會叫 writer。需精確雜湊綁定的安全採用流程，不能直接用這些檔案冒充已裝入。
3. **兩項敘事警告仍保留：** 03:47–06:21為154秒、06:21–08:22為121秒沒有工具偵測到 open loop。其餘 craft warnings 一併保留，共24 warnings；此包不改旁白以消警告，也不把旁白故事擅改成角色對話。
4. **估時不是實測。** 六章含hook、排除branding，純旁白依230–250編輯字／分鐘估512.64–557.22秒。官方預設timeline582.267秒含90片段各300ms、85鏡間各700ms、最後1500ms與frame rounding；不拿間隔補片長。實際TTS、節奏、至少8分鐘gate與片長需在真音訊後確認。
5. **計數差異不是刪字。** 2136編輯計數與官方2055相差81：官方不算4個「〇」，Latin字詞各算2單位比逐字少79，但官方會多算2個片假名區間的「・」標點；即4＋79－2＝81。所有旁白字串仍完整一致。
6. **圖片、卡片與cast尚未製作。** title HTML 保字不是像素QA；圖片沒有產生。原兩個一般化人物cast留在plan，未擅自綁鏡或產出真人肖像。image_asset_key不是原生scene欄位；data.source只可切clip，不能用於still共圖。

## 檔案與界線

- chapters/：六章正式schema形狀候選；全部claim待查。
- mapping.json：原稿與active兩種段落、既有三處限縮、切片、CID／source／fact、loops完整窗、原卡和共圖對照。
- compose-lint-evidence.json、card-adapter-evidence.json、shot-reading-evidence.json：實際本機工具證據。
- input-pins.json：48個repo來源hash；output-pins.json：初次r2工具產物hash；handoff-pins.json：本次完整交付hash。
- loop-anchor-delta.json／previous-attempt/：初次scalar轉換問題及窄修正；初次候選仍留在外部工作封存，未覆寫。

5秒片頭放hook之後，21秒片尾放全部旁白之後；繁中CC保持可關閉。實際來源checker、listener、narrative、pilot、TTS、圖片、renderer、owner看片與上傳均未由本包完成。
