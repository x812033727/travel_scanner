# B18 Row10b：最終位元組獨立審查補充收據

- 日期：2026-10-17；審查者：Codex `/root/b18_script_scene_alignment/b18_route_b_plan_review`。
- 這是追加收據，不改寫 `INDEPENDENT-ROW10B-REVIEW.md`。原收據 SHA-256 `957b34461c0ff9f4b8964d4a9908f20f18ec6239aaca25ca42cef2e9735efac6` 綁定修改前的路由／驗證／說明／產生器，只保留為歷史審查，**不能作為現版 PASS**。
- **現版結論：離線 row 與路由設計 PASS，P1 0、P2 0；正式 row 採用、章稿驗證、工人及媒體製作仍 HOLD。** `build.mjs --check` 回傳 `PASS_OFFLINE_ROW_SCHEMA_ONLY_HOLD`，十筆 `must_verify`、舊 85 景、舊 65 筆 claim；這是離線一致性檢查，不是已完成逐景查核。

## 本次釘住的最終輸入

| 檔案／對照 | SHA-256 |
| --- | --- |
| `B18.json` | `6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc` |
| `routing-amendment.json` | `0a6e9e01ef763b895ba985f8dcc1f4e6b16c416e7faba4996e594f0124acdee4` |
| `delta.json` | `c7910ad4010f4f989dfa53922d364499526470efffe7b01b4b1e91de6f40e9db` |
| `verification.json` | `1cff6ce7c2ad9c74591ea782ef536e1b6058b349ee8f70c83b252affcaf7d9ce` |
| `README.md` | `3a9d02fba4592a55a9f3f6f14d0d64124fe9e25443cae717a27360dc8a16bba4` |
| `build.mjs` | `0885f9bdfa7271accceb59b418545e73a6d0987524daab0789ad51a19890e844` |
| `sha256.json` | `c28d2df085ceebd8bdc8b19534f55bd9a3ef22b436753c57973ee8412e931fdd` |
| canonical story | `fbcff4985abae065811ff41cb234ac4190fd22cc8129e03f43048d5dd42af665` |
| 受審第三版全文／審稿收據 | `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1` ／ `603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4` |

## 追加審查結果

1. 作者新增的 `t18.pre_verifier_chapter_write_required` 精確要求正式 `turn` 章稿先存 `scene=turn-s088, source=2, fact=null, verdict=UNCHECKED`，再進 verifier；`post_verifier_persisted_readback_required` 要求讀回同一場景、來源與 `fact:null`，並確認非朗讀來源字卡存在。`build.mjs` 對兩項要求與 T06 場景歸屬均有斷言，`verification.json` 對三項實作／QA 仍明列 `false`，沒有冒充完成。
2. 這個順序有實際工人依據：`tools/video/automation/story.mjs` 的 `checkedRows` 對 verifier 回傳的 `fact:null` 會用既存 claim 的 fact 回退；目前舊 `t18` 是 `turn-s092, source=1, fact=7`。因此只在 verifier 答案中改 `fact:null` 會錯誤回到 fact 7。預先保存新章稿及 verifier 後的持久化讀回是必要關卡；此包尚未執行。
3. 其他實質設計不變：法院 fact 4 僅把官方判決中的 1967 年訴外元祿授權展店與特定第 579776 號權利 1972 年期滿串為有限法律時間線；fact 9 仍只涵蓋發明協會所載後場直線送盤，與受審 T04 口播歸屬一致。T06 盤色句留在來源 `[2]` 支持及將來獨立 `fact:null` claim，配不朗讀來源字卡，沒有迫使受審 T06 口播來源名稱。法院與發明協會原文、`archive` 主來源分類、十筆 schema 的審查結論與前一收據相同；本次重核最後輸入未改動這些 row／全文位元組。
4. 舊 65 筆逐景 claim 仍全為 `UNCHECKED`，舊 row 審查因 canonical story SHA 更新而失效。正式落地前仍要對新 row 獨立審查，產生並核對後繼章稿／逐景 claim，完成 t18 寫入與讀回、T06 來源卡、verifier／listener／敘事、受審全文逐字對位與片長；不得用此 PASS 代表影片可製作或可上線。

本補充只驗最終離線候選與修正後的必要關卡。未做主機寫入、付費呼叫、影片匯入、上傳或發布；任何受審輸入 SHA 改變，須再出新收據。
