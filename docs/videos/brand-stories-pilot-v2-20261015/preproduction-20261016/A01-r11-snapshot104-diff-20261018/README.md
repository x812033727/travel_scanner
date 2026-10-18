# A01 r11 與 104 鏈舊快照：唯讀銜接差異，HOLD

這份隔離資料只比較兩份**已保存在本機**的輸入：2026-10-17 的 A01 `snapshot-104` 與 [r11 編輯候選](../A01-editorial-candidate-20261018-r11/README.md)。r11 可作唯讀銜接比對基準；[獨立審查更正附錄](../A01-editorial-candidate-20261018-r11/independent-full-review-addendum-20261018.md)已將其正式事實關卡列為 `HOLD_P1_N14`。`build.mjs` 不連主機、資料庫、後台或供應商；`--write` 只更新本目錄的 `report.json`，`--check` 完全唯讀。報告不包含快照原文、模型回覆、主機路徑或憑證，報告狀態固定為 `OFFLINE_DIFF_ONLY_HOLD`。

## 釘選與重跑

- r11 `manifest.json` SHA-256：`39bcc9e69c4d89eea044e145abb592c587183796e92bb13646c83f82511d289a`；原獨立全文複審 SHA-256：`2ed2f086af582ea75dde7abfdf43fb032d3fa7da2feb3917b249c7c890d774ac`，原結論 `PASS_OFFLINE_WITH_P2_NOTES`。更正附錄 SHA-256：`ed0c8932dbe71440cce9e7a3e6d55ec791ef2785010b53f282357c52ceddf1d7`；原結論**不得用作正式事實關卡 PASS**，目前為 `HOLD_P1_N14`。
- 舊快照既有獨立驗證為 **104 鏈**，tip `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`。本包另釘選外部 `verified-review104.json` 原始位元組 SHA-256 `29ddbe75e849f09fed508b3c1405fd533445aa8adee337539cb11ea9287460aa`、儲存庫舊讀回收據 SHA-256 `70f7ea78a198c7ae593d3668c52f6ffea3ec7316072f0d35df04ffd63a7ae3d1`，以及快照 **254 檔**相對路徑與逐檔內容的清單 SHA-256 `827361fe4f8d89cbc3c211af5df91de1bbcb09ae8b4ffd6acf534b4465dfd6d3`。任何檔案數、路徑、位元組、審查或來源 tip 漂移即停；此檢查不重新驗證主機出處或當下狀態。

在本機儲存庫根目錄，把參數設為**本機絕對路徑**，不要將快照或私有路徑提交：

```powershell
$a01Snapshot = '<absolute local immutable snapshot-104 directory>'
$a01Verified = '<absolute local verified-review104.json>'
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261018-r11/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-r11-snapshot104-diff-20261018/build.mjs --check --snapshot $a01Snapshot --verified $a01Verified
```

`report.json` 是完整的逐章 scene／line／claim ID 增刪與變動、跨章句子移動、公開來源 URL 集合差異及釘選。主張比較會解開舊六章 `source` 的 0 起算索引，對照舊公開來源 URL、原文、查核日期、場景、審查狀態；r11 每筆則從 `claims.md` 與逐鏡引用讀取，再和 `source-map.json` 對照。找不到來源、重複 ID、Markdown 列與鏡頭／來源對不上時會停止；唯一無來源的 active `n14` 依更正附錄明列 `HOLD_P1_N14`，不默認沿用舊審稿。舊六章與舊合稿的場景 ID 全部對得上；扣除合稿正常增加的 `chapter`、`claims` 衍生欄位，場景正文差異為 **0**。這只證明舊快照內部可比較，不表示 r11 可以直接覆蓋它。

## 本次找到的銜接差異

| 項目 | 104 鏈快照 | r11 候選 |
| --- | ---: | ---: |
| 場景／口播句 | 79／108 | 65／77 |
| hook／origin／idea／engine／turn／now 場景 | 8／17／15／10／23／6 | 5／9／9／13／14／15 |
| `video.json` 正文目標 | 9–11 分鐘 | 7–8 分鐘 |
| 系列及舊 `auto.json` 目標 | 各 10 分鐘 | 系列仍 10 分鐘，未修改舊 auto |
| 公開 `video.sources` | 13 筆 | 17 筆，恰等於 r11 **有來源**主張的網址集合；`n14` 無來源 |

舊公開來源與 r11 有 **8 筆保留、9 筆新增、5 筆移除**；保留的 8 筆還有標題或查核日期變化。全片有 **50 個保留的口播句 ID**，其中 **25 個換章、26 個換鏡、33 個改字**；逐章刪加不能被誤讀為全片新句。場景內容變化先扣除合稿增添的 `chapter`、`claims` 欄位，主張改動另在主張欄列示。

**19 個全片保留的主張 ID 無一可視為原樣沿用**：依原文、來源、查核日、鏡頭及狀態逐欄比對，17 個改了主張文字，`h6`、`o27` 換了可解析的來源 URL，`n14` 在前後兩版皆**沒有來源 URL／查核日期**，須另行查核或刪修。其餘保留 ID 即使字相同，審查狀態也由舊 `PLAN`／`CONFIRMED` 改為 r11 `PENDING`，不可移植舊判定。`i35` 是新增主張，`t7`、`n16` 是保留 ID 但內容已改；`report.json` 列全數 ID、逐欄變化與跨章位置。來源 URL 綁定只是結構檢查，不等於已實地查證來源。

更重要的是，r11 的 `series.plan.sources` 仍有 **23 筆**：7 筆未被 r11 播出主張引用，且**缺少** Plath 2024 年校友刊第 17 頁的 1988 年第一人稱來源。現行本機 `tools/video/automation/story.mjs` 的 `composeStory` 會直接把整份 `plan.sources` 寫回 `video.sources`。因此重合稿會讓 7 筆無關來源回流、使一筆真實引用缺席；詳見 `report.json` 的精確 URL 集合。r11 `candidate/` 只有合稿／系列／詞典／腳本／主張表，**沒有六個 `story/chapters/*.json`**，不能當成正式機章稿安裝包。

## 下一步採用順序與停止條件

1. 先取得**新的正式機唯讀** A01 全鏈與六章、衍生檔、release／worker、STOP／LEASE、所有未決 journal、階段與媒體工作、完整 US$25 帳本；再做獨立二次讀回。若鏈數、tip、章稿或工作狀態不同於預期，保留現況，重新做對照。2026-10-17 的 104 鏈及較早的舊 tar 不能代替今天的證據。
2. 在隔離分支製作**新的、重新雜湊的修稿與六章來源轉換候選**：先限定 `n14` 的樓梯情境、補上可查來源與編者推論標記，核對主張表、企劃來源、影片來源索引及場景引用，再交獨立查核者做新的正式事實複審；更正附錄未建立 r12，亦未預先核准任何改寫。從新鮮正式六章與 r11 65 鏡逐 ID 對照，明列退役、保留與新增場景／主張，以及保留 ID 但改字／改來源／換章的情形；依序重組 `hook`、`origin`、`idea`、`engine`、`turn`、`now`。保留全部歷史稽核事件與既有失敗結果，將變更後的 chapter checked／listened／narrative 狀態交正式 worker 重新查核，不把 r11 的 `PENDING` 當成已查核。候選需固定前後來源與每個檔案雜湊，獨立審查後才可設計主機交易。
3. 另處理**來源重併**：在企劃與正式 worker 的公開來源規則中保留 17 筆實際引用，補足 1988 年第一人稱來源，避免 7 筆無關企劃來源回流；此程式檔案不在本包修改範圍。再處理 A01 專屬 420–480 秒正文關卡，並以受審的來源事件明確處置舊 `[9,11]` 持久設定。系列及 B18／後五集的十分鐘規格不跟著改。
4. 只有新的事實複審通過，且正式來源、六章、查核／listener／敘事實際結果全數核對通過後，第二讀者才能判斷是否寫正式 `story/reviews/script-review.json`。原 r11 `PASS_OFFLINE_WITH_P2_NOTES` 不可移作 `factual_claims: PASS`。真 TTS 片長、盲聽、插畫聯絡表、成片與站主看片是後續獨立關卡。

本包**不**建立正式審稿收據，不解除 STOP，不清除舊 audit／未知工作，不匯入影片、不購買旁白或圖片，也不授權合併、部署、B18／後五支或 YouTube 上傳。
