# B18 Row10c／Phase 4 路由獨立修訂審查

2026-10-17；審查者 Codex `/root/b18_row10b_formal_offline_review_1017`。我未撰寫 Row10c 產生器或改動受審輸入。**結論：本次路由修訂的離線設計 PASS，P1 0、P2 0；正式章稿、匯入與製片仍 HOLD。** 本結論只驗下列精確位元組和路由契約，不是 worker 實際保存、verifier、最終說明欄或媒體的通過收據。

## 固定輸入

| 受審檔案／資料 | SHA-256 |
| --- | --- |
| 本目錄 `sha256.json` | `4222dbc887f3d9caf2e6299f48127f1f373fa58e5cf93a7dc36fcd95216f9e32` |
| 本目錄 `build.mjs` | `e92a6e0678e85d0f982def535df5912d6165ef3fdc715bfd0426b98c4228083a` |
| 本目錄 `routing-amendment.json` | `12dd4b6e043293fa0c3106782f2af1e60c901719d6250c034a2cc0ad72cf190c` |
| 本目錄 `B18.json`＝Row10b `B18.json` | `6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc` |
| canonical `storyHash` | `fbcff4985abae065811ff41cb234ac4190fd22cc8129e03f43048d5dd42af665` |
| Phase 4 `sha256.json` | `efdf3994152db18892d70c35f6ae10ba3f1d4a9076078922a8a988ee0bbd7422` |
| Phase 4 `B18.md` | `73236441aebc92e804436fd9371a3044a27e5decdd7438905459ef214023768f` |
| Phase 4 獨立全文審稿 | `52172dd22d2a0d349bea7ff7568cbaa2aecef5ab61d2929ad82048df967d745e` |

Row10b 的[獨立六來源／十事實審查](../B18-row10b-offline-source-review-20261017/README.md)只對該 canonical 企劃 row 判 `verdict:pass`，`reviewer_only:[4]`；Row10c 逐位元組沿用同一 row，來源結論沒有延伸到逐景或成片。`build.mjs --check` 重建後得到 `PASS_OFFLINE_ROW_PHASE4_ROUTE_SHAPE_ONLY_HOLD`、10 項 fact、95 景／65 筆 `UNCHECKED` 主張；Phase 4 的 `verify-worker.mjs` 得 `OFFLINE_WORKER_SHAPE_ONLY_HOLD`。兩者都只是離線形狀檢查。

## 修訂核對

1. **來源呈現條款已對齊。** 舊 Row10b `routing-amendment.json` 的 `t18.visual_source_card` 與 `post_verifier_persisted_readback_required.source_card_present:true/source_card_not_spoken:true` 是為了第三版 T06 沒有口播來源而設。Row10c 不再要求那張卡。受審 Phase 4 的 `turn-s088` 是無文字的 `shot`，兩句旁白連續說出「發明協會的沿革」與「用盤子的顏色或裝飾區分價位」；對應 [發明協會原頁](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) 的沿革段。94 個 shot 加末景 `outro` 不須塞入不支援的 `title` 卡，也不要求 MiniMax 畫可讀來源字。
2. **逐景證據路由保留。** `t18` 仍是獨立的 `turn-s088/source:2/fact:null/UNCHECKED`，沒有併到 `must_verify[9]` 的後場直線送盤 `attributed:true` 事實。`t3` 仍以來源 3 路由到法院專屬 fact 4；`reviewer_only:[4]` 不變。先前 12 項設計的 fact 10、11 沒有偷加到十項上限之外。
3. **順序與持久化要求保留。** `pre_verifier_chapter_write_required` 仍指定先把 `t18` 的場景、來源 2、`fact:null`、`UNCHECKED` 寫入真章稿；`post_verifier_persisted_readback_required` 要求 verifier 後再讀回同一景與 `fact:null`，並核對可聽來源歸屬。這處理了 `checkedRows()` 對 verifier-only `fact:null` 回退舊 fact 7 的風險；目前離線 `turn.json` 並非正式主機的保存收據。
4. **完整 URL 是後續成片資料檢查。** `final_description_source_url_required` 等於 row 的 `sources[2].url`，即發明協會沿革完整網址。`verification.json` 將 `final_description_source_url_present` 正確留為 `false`；沒有把未產生的說明欄說成已驗證。
5. **企劃與來源不變。** Row10c `B18.json` 原始 SHA 與 Row10b 完全相同；`delta.json` 的 `row_changed_paths:[]` 可用位元組比對重現。新稿口播與 Phase 4 獨立全文審稿的 SHA 已釘住；任何其中一檔改動須重新審查本路由。Row10c 不修改 active `episodes/B18.json`、active review、`stories.json` 或 worker code。

未解鎖：正式匯入包、worker B18 參考稿與部署、真實章稿 prewrite/postreadback、65 筆逐景 verifier 判定、listener／narrative、最終說明欄 URL、TTS 9–11 分鐘、Jev、MiniMax 成像及連續三鏡樣片、繁中 CC、成片 QA 和站主看片。此審查未作主機寫入、付費呼叫、匯入、合併部署、上傳或發布。
