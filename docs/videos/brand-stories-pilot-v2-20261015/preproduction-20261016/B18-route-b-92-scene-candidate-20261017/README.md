# B18 Route B Phase 2：92 鏡離線草案（HOLD）

**這是隔離候選，不是可匯入、可製作或可覆蓋現用 B18 的章稿。** 它只讀第三版受審全文 `../B18-spoken-source-cadence-candidate-20261017/B18.md`（SHA-256 `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1`）；現用 `scripts/B18.md` 的凍結版本不作輸入。Row10b、舊 flow 與 25 段對位設計均被 `build.mjs` 雜湊釘住。沒有呼叫模型、TTS、圖像或正式主機，也沒有把任何 `UNCHECKED` 改為通過。

## 可重跑的離線結果

在儲存庫根目錄執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-92-scene-candidate-20261017/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-92-scene-candidate-20261017/verify-worker.mjs
```

第一行得到 `PASS_OFFLINE_92_SCENE_DRAFT_HOLD`：六章 92 鏡，沿用舊 85 鏡並新加 `origin-s020b`、`engine-s046b`、`turn-s068b`、`turn-s080b`、`turn-s072b`、`now-s095b`、`now-s098b`。25 段受審口播依序完全覆蓋，去除空白後與全文一致；7 個新增鏡頭均為具體插畫提示。舊 65 個 claim ID 全在，65/65 仍為 `UNCHECKED`。`paragraph-coverage.json` 與 `claim-coverage.json` 記逐段、逐 claim 路線；`sha256.json` 釘住輸入、生成器及六章輸出。

第二行確認可愛插畫靜態門檻：73/92 鏡是插畫（79.35%，高於 70%），19 張字卡、連續字卡至多 2 張。**正式 writer 門檻仍 HOLD**：`tools/video/automation/story.mjs` 的 `readChapterAnswer` 實測在 origin 第三鏡返回 `scenes[2] is a "title": a story's scene is a shot (the last chapter ends with an outro card)`。目前最後一鏡 `now-s103` 也是 `shot`，尚未設計 worker 的末尾 `outro`。離線的 deterministic line IDs 也不是正式 writer 發給模型的 IDs。

| 對位 | 離線內容 | 還要核對 |
| --- | --- | --- |
| H02 第三問 → T04 | 後場製作、直線送到客席；hook 與 T04 都保留 fact 9 路線 | `attributed:true` 的可聽歸屬；不能把 h7 改成 `fact:null` 來通關 |
| T01 1967 | 法院 PDF P8 L476–495 的受授權訴外公司仙台直營／東京連鎖展店；t3 → source 3／fact 4 | 1967 句跨 turn-s068／s068b，須獨立核書面來源、口播與卡片節拍；不能畫成原告自己開兩家直營 |
| T02 1972 | 第 579776 號**特定**實用新案期滿；與其他權利、商標分開 | 法院 P10 L574–578；fact 4 仍 reviewer-only |
| T06 多價盤 | `turn-s088` 為發明協會來源字卡；t18 已在章稿中先存 `source:2, fact:null, verdict:UNCHECKED` | 此為 10 項 must_verify 以外的獨立主張；正式 verifier **之前**須先存章稿，之後讀回 `fact:null` 和非口播來源卡，防止 `checkedRows` 回退舊 fact 7 |
| N01 兩件實物 | 1985 年堺東店輸送機與另存早期板片分開畫 | 不能當 1958 年同一原機 |

### 必須由獨立審稿確認的可聽歸屬

以下都保留對應 `must_verify`，未以 `fact:null` 隱藏。正式 verifier 若要求每次重唸來源，而受審全文沒有那句，應 **HOLD 並重審口播／規則**，不得逕行通過。

| ID | 受審口播的精確文本 | source／fact | HOLD 原因 |
| --- | --- | --- | --- |
| h7 |「後來有店把師傅留在後場，盤子又怎麼從後場送到客席？」| 2／9 | H02 未口播「發明協會」，且本句是預告問題；需確認 attributed fact 的場景適用性。 |
| i1 |「一到轉角，帶子擠在一起，盤子掉下來。」| 0／3 | H02 已唸 J-Net21，但 I01 沒再唸；核跨章可聽歸屬。 |
| i5 |「一片片扇形板排在一起，讓帶子沿著吧台角落轉向」| 0／3 | I03 同段稍後才唸 J-Net21；核來源名與主張的先後。 |
| e9 |「一九七〇年，大阪萬博。」| 0／6 | E05 沒唸發明協會；fact 6 的 attributed 路線是否可由 T01 回收需核。 |
| n7 |「早期那些扇形板，說明當年的轉角怎麼被解開。」| 0／3 | N02 回顧 I03；該章未再唸 J-Net21。 |

有 9 筆 claim 文字跨兩景，且 7 景量字超過 42 個可見字；精確 ID 與文字在 `paragraph-coverage.json`。這些是 **分鏡密度與逐景 verifier 對位風險**，不是測過可播放的時間。T01 的法院 1967 事實及 E01 首店資料也在跨景清單，須獨立審查如何讓一景主張對得到該景旁白，或再調鏡頭／文字。既有 25 段全文不得為通過機械檢查而擅改。

### 片長、卡片與預算 HOLD

受審全文有 2,667 個漢字／阿拉伯數字，若以每分鐘 300 字**粗估**，正文約 8 分 53 秒；加 5 秒片頭、21 秒片尾僅約 9 分 19 秒。worker 目標是 9–11 分鐘，**必須以實際 TTS 和剪輯時間軸量測**。新增七鏡只重新分配畫面，不能當作增加七段口播或保證片長。

MiniMax image-01 本地目錄標價每張 US$0.0035；七張新鏡頭一次生成的**增量目錄價**約 US$0.0245，未含重試、合成、TTS、音樂、稅費，也非帳單或付費授權。若把 19 張字卡全部改成新插畫，另增 19 張約 US$0.0665；整體較舊 66 張插畫多 26 張約 US$0.091（同樣僅圖片目錄價）。

**shot-only 可執行替代路線評估：** 若 19 張字卡對敘事不是必需，可另做 92 個 `shot` 的候選，畫面不要求 AI 畫文字；來源進合法的 `plan.sources`／逐景 claim 欄及影片說明。可是 Row10b 對 t18 特別要求可讀回的**非口播來源卡**，只改為書面來源欄不能自動滿足；須先獨立審查可關閉 CC／後製合法來源卡或改口播一句「發明協會記載……」，後者要重新獨立審稿並更新凍結全文收據。現在的 19 卡草案和 shot-only 想法均不可逕送 worker。

## 採用前的門檻

1. 獨立逐段聽讀／來源／視覺審查本候選與原第三版全文，特別審上列 5 個歸屬、9 筆跨景 claim、T01 法院 P8 和 T06 發明協會。**本目錄目前沒有獨立 Phase 2 審查收據。**
2. 選定可由 `readChapterAnswer` 接受的 19 張卡處理方式、末尾 `outro`、正式 writer line IDs；重新檢查 hook→payoff 與至少 70% 插畫。
3. Row10b 若要正式採用，需對實際企劃／章稿另做審稿、保存 t18 `fact:null` 再跑 verifier，讀回 source 2 與非口播來源卡；65 筆逐景 claim 仍需真查核。
4. TTS 實測 9–11 分鐘、逐景 6–12 秒、音訊與片尾／可點連結；預算及任何付費製作走既有核准流程。現在無 TTS、圖片或成片。

保留所有既有審稿、現用資料與上線狀態；本草案沒有採用或發布宣稱。
