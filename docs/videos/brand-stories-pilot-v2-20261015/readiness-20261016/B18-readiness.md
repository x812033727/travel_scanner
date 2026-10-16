# B18 製作準備唯讀核對

2026-10-16。範圍：既有稿件／收據／工人輸入／最新規格的準備度，沒有重新做全文事實審查。只產生 Temp 報告，未動 repo、主機、付費服務或批准收據。

## 已完成而可沿用

- 完整旁白 `scripts/B18.md` SHA **5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724** 與 `scripts/reviews/B18.md` 的獨立文字事實／敘事收據吻合，2026-10-15 審者為另一位 Codex。
- 企劃 canonical story SHA **f9be8cd707c30ac0260543f89bd5ce22960a3b5582d83c233fcce0db1633df23** 與 `episodes/reviews/B18.json` 相符；storyProblems、reviewProblems、seriesProblems 都為空。
- 本機 `stories.json` 的 B18 列與來源列＋審稿 notes 的預期編譯結果深比較一致，series 也一致；沒有重寫 compiled file。
- 本機 `tools/video/automation/story.mjs` 的 PILOT_SCRIPT_REFERENCES 仍指向這份 B18 凍結稿。它要求獨立檢查實際章檔、合併稿與 narrative 收據；已有文字 PASS 不能直接當工人 PASS。

**結論：不需要另寫一篇 B18 全新逐字稿。最小工作是讓工人輸入與視覺分鏡忠實接上這份已審全文。**

## 真正缺口

| ID | 現況 | 最小補齊 |
| --- | --- | --- |
| G1 | 既有 worker hook 與舊 treatment 是「轉角／1958 怎麼守生意／1978」；已審 H02 是「轉角＋1958／1970 萬博／1978」。 | 以已審稿作參照，做最小 row delta 或正式章稿轉換 manifest，明確保留三個預告順序。改 row 就重綁 row review，不動凍結全文與其 hash。 |
| G2 | 108 格＝91 插畫＋17 卡是章節排程，另只有八個代表 prompt。 | 展開完整逐鏡原文切片／ID／來源／用途／camera／prompt；重建 24 段原文完全相同，再跑離線結構與 shot_reading。無須硬湊另一個鏡數。 |
| G3 | 文字回收完整，但沒有同圖 cache／實際圖片綁定。 | H02 三個問句分別配 I01、E05、T02 的同一張圖，正式補 scene IDs 與完整請求身分；生成後保留同檔 SHA。 |
| G4 | 9:06 用舊試作 300 字／分；本片未實錄。 | 保留估值的來源，另列同口徑估算；等 TTS 實測再判 9–11 分鐘工人範圍，不能因估算先改全文或填空白。 |
| G5 | 舊 README／treatment／shot-plan 還寫兩支 US$25、要餘額證明、未審草稿或舊 PR 部署狀態。 | 下次 repo 文件整合時記錄最新狀態；依 owner 訂閱豁免不再問餘額。B18 仍須獨立明確授權；新報價每片 US$5 是提案。 |

這些缺口屬既有 pilot 工作，不需要重複開五集工作；請協調者記入既有試作票，報告本身不越過唯讀 scope 修改任務檔。

## 三組同圖的最小設計方向

1. **H02 第一句 → I01**：一般化工坊人物查看彎角處的一只盤子；同圖在 I01「開場那個會卡住的轉角」回來，扇形解法留 I03，1957／1958 結果留 I04／E01。開場圖不先畫出解法。
2. **H02 第二句 → E05**：一般化展覽餐檯、單人與一只壽司桶。日期與 300 日圓由後製在正文才顯示，不把首店 50 日圓餐盤混在其中。
3. **H02 第三句 → T02**：一般化經營者查看空白權利資料夾與壽司盤；不用偽造證書、商標或新招牌提前洩漏答案。

這只是可供分鏡作者落地的概念對位，**不是已完成的三組 scene/prompt 或圖片綁定**，沒有產圖。完整分鏡要讓每組前後 prompt/camera、模型、seed、size、negative、cast/reference 相同，最後指向同一張通過的圖片與 SHA。N03 三句尾聲也要求同圖；若切成多鏡以符合時長 lint，仍可共用一個 asset。

**v3 報價仍保守按 91 張不同插畫計，不先算成 88 張。** 舊 108 格是否已預留回收或尾聲共用沒有逐鏡證據，不能重複扣圖。角色設定圖只沿用一個 sushi-chef cast，縮圖用既有圖後製，clip=0。

## 片長口徑與報價提醒

獨立重取 24 個 blockquote 原文及其製作註 ID：舊漢字／數字計數 **2728**；同後五集排除標點／符號／空白的計數 **2729**。只讀敘事段，不把製作註、來源或掛鉤表算進正文。

| 方法 | 完整六章正文（含 hook） | 加 26 秒動畫 |
| --- | ---: | ---: |
| 原收據：300 漢字／數字每分鐘 | 545.60 秒 | 571.60 秒 |
| 同五集：250 計數單位每分鐘 | 654.96 秒 | 680.96 秒 |
| 同五集：230 計數單位每分鐘 | 711.91 秒 | 737.91 秒 |

目前工人對 10 分鐘 cute-mystery 的實際正文範圍是 **540–660 秒**（story.mjs lengthBand），全長 QA 另有正文至少 480 秒。慢端估值超過 660，不代表現在已實測失敗；舊實測語速也不能當本片速度。v3 費用計價用 600 秒，不是已證明的 B18 上限；正式聲音出來後需重新核用量。這不足以推翻 US$5 提案，但不能用 9:06 舊推算保證片長與費用。

## 來源與最新格式

已有全文收據逐段覆核 [0] J-Net21、[1] 日本機械學會、[2] 發明協會；[3] 維基只作參照。row 的 sources.checked 仍為 2026-09-28，但兩份獨立收據明列 2026-10-15 重開。這次沒有重新打開來源或建立 source-body hash，不聲稱當前工人可讀性已驗；正式製作時檢查 reader 頁面擷取與必要段落即可，不須無故重做全部文字審查。

完整稿新增的 1960 第二店、300 日圓萬博壽司桶、1971／1974 給茶、後來直線帶／採購／盤色／八〇年代店型均已在全文收據覆核；正式章稿須逐條帶來源主張表，不能因 row 的十條 must_verify 沒有逐項寫出而遺漏歸屬。兩種薄片靈感分來源、20／50／300 日圓分年代、實用新案分類、1985 機器與另存早期板片、2022 實績與2023 當時估計的限制照舊。

series 已是 target_minutes=10、image-01、exact cute-mystery、stills；目前 composeStory 強制 subtitles.burn_in=false，輸出分類 story。未生成的 B18 video.json 仍須實際讀回確認可關閉繁中 CC，不能從本機程式推論正式成片已正確。片頭在首章後 5 秒；末尾三句後 21 秒片尾；最後 16 秒結束畫面可點性等另行授權上傳後驗。

## 接下來的最短路徑

1. 免費整理 G1 的輸入／參考對位，以及 G2/G3 完整逐鏡表；保持全文原文與 ID。必要 row delta 獨立覆核。
2. A01 完成帳本、聲畫與站主驗收後，才按明確 B18 授權及可執行的全片上限前檢。這次不假設 US$5 或 US$25 已獲 B18 授權。
3. 正式六章 writer/verifier/listener、合併稿、narrative panel 和獨立 reference review 各按實際檔案 hash 完成；不由本報告簽 script-review.json。
4. TTS／發音／實測片長、插畫評審與同圖 hash、可關閉 CC、完整影片 QA、站主看片、另行授權上傳與片尾點擊驗證。

正式狀態未從主機查讀；本機 repo 未見 B18 v2 的正式 video.json 只代表本機缺該產物，不表示主機一定不存在。

## 精確檔案索引

下列均以 repository_root 為基準。詳盡欄位、三組概念對位、章別計數及已審新事實對照見 B18-readiness.json。

| 相對檔案 | SHA-256 |
| --- | --- |
| docs/videos/brand-stories-pilot-v2-20261015/scripts/B18.md | `5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724` |
| docs/videos/brand-stories-pilot-v2-20261015/scripts/reviews/B18.md | `e05236ae3f66c4a5780abd431d8e8d21e95ad929978e472cef2defafb4ee31d8` |
| docs/videos/brand-stories-pilot-v2-20261015/episodes/B18.json | `2150ff1b5a3a25d99ffadbe617ee746e42c93b3e24ef814a64d05f8149b00565` |
| docs/videos/brand-stories-pilot-v2-20261015/episodes/reviews/B18.json | `3a7bb438fc9ad1717d2d7fd902a4b238d85804fa394328b54730ead05d986834` |
| docs/videos/brand-stories-pilot-v2-20261015/stories.json | `3a87dff10ed597c68b01588244e5bd3443dfa69af13d97fbd8e411a81d32cd01` |
| docs/videos/brand-stories-pilot-v2-20261015/series.json | `b2cdb40dd5c6b9e7723ae76fd5fb9992ca66fc0baebabc4ae0f5caabdb38502b` |
| docs/videos/brand-stories-pilot-v2-20261015/B18-shot-plan.md | `7c890e609d46d8536408045d84dc462bf363840fd679265ebbb76bd2e6843929` |
| docs/videos/brand-stories-pilot-v2-20261015/B18-conveyor-belt-sushi.md | `d8b88934f1bb2aa1d24f6053d3e5ff780dd5937f4f424e6cebd89e69b05bf298` |
| docs/videos/brand-stories-pilot-v2-20261015/README.md | `2164925a36a72e87f6dae1f1cfab035618fe3d55d951ff1f53aea487e5e43a99` |
| docs/videos/brand-stories-pilot-v2-20261015/build.mjs | `aca63359b111c6082aeb93f6ccbed75351d62dec65474a478cbbc7f1529d2162` |
| tools/video/automation/story.mjs | `f9825a7ce9649111d3e49ab33a2846a8be61111dd2cb2df40db3b68b974676f3` |
| tools/video/core/narrative.mjs | `0b9dce18b4df77d1872297ed5e971b19f74ce6b1245a661c2d91c50966565926` |
| tools/video/story-plans/plan.mjs | `5ec625989c2aa9f86ea837b6c03f189554746618825292ad1c30fad1b6988de5` |
| .agents/skills/youtube-video/references/story.md | `957d5859811bc161f661ec14f5cacf1e7e4ed81e34745c62f367ba2d2def5806` |
| .agents/skills/youtube-video/references/script-writing.md | `57c71ae9aebb453c90ca618cf7c208416b01f4082fd100ef4b28d307ade74a0c` |
| .agents/skills/curio-episode/SKILL.md | `57c34a1e088e407c8102d4e28cb836e040baaaa94dc16dddec09e57ba7b3b12f` |
| docs/videos/long-form/README.md | `dd639c0c85595881d1bda64541d28f29e8d90f1067e541c08eb28dc9c4543c3b` |
