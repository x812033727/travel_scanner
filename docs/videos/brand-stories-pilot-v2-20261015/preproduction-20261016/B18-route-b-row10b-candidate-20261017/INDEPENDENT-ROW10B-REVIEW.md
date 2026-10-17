# B18 Row10b：獨立來源、口播及工人路由審查

- 審查日：2026-10-17；審查者：Codex `/root/b18_script_scene_alignment/b18_route_b_plan_review`，未撰寫本候選。
- **結論：離線 row 設計 PASS，P1 0、P2 0；正式採用與影片製作仍 HOLD。** 這只核新 row 和未實作的逐景路由是否與來源、已審第三版口播相容；不是完整章稿、`review-candidate.json`、正式 verifier、TTS、媒體或站主看片收據。
- 本候選最後位元組：`B18.json` SHA-256 `6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc`；`routing-amendment.json` `2e6af7afc91a0ac05794a0f683309cd967895604a77e7897dbe122d1bc948399`；`delta.json` `c7910ad4010f4f989dfa53922d364499526470efffe7b01b4b1e91de6f40e9db`；`verification.json` `1456894dcf57f40da4fa5e15994104d33622254ca7e5ccd00493691220b2898e`；`README.md` `91914a896b10f01069ee7a6cd5005712b2341c21a690353678a3025f533a4274`；`build.mjs` `7690de977636258d98685e43035f07e4b52139c424d19b0e95d084e68ca6c2c9`；`sha256.json` `ebe6b6634e5726939e0f2c7e6bf49708330b81e602de8ba9436a6c8ac9d3bd0b`。Canonical story SHA-256 `fbcff4985abae065811ff41cb234ac4190fd22cc8129e03f43048d5dd42af665`。
- 固定對照：父版 row `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681`；第三版全文 `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1`，全文審稿 `603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4`。原 12-fact Route B 設計與 [schema 補充收據](../B18-fullscript-route-b-plan-20261017/INDEPENDENT-PLAN-REVIEW-ADDENDUM.md)、前一個 Row10 HOLD 收據分開保留，不當成本版 PASS。

## 來源與敘事核對

1. **五處改動與十筆上限。** 只改 `chapters[hook].point`、`chapters[turn].point`、`must_verify[4].claim`、`sources[2].supports`、`sources[3].supports`；`must_verify` 仍為十筆。直接呼叫 `storyProblems` 得零問題、canonical story SHA 與本包相同；`build.mjs --check` 讀回 `PASS_OFFLINE_ROW_SCHEMA_ONLY_HOLD`。舊 row 收據綁舊 story SHA，不能沿用。
2. **法院時間線仍有限界。** [法院官方判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)理由 P8 L476–495 記獲授權使用餐台及「元禄寿司」標示的**訴外元祿**於 1967 年開仙台直營首店、東京錦糸町連鎖首店；P10 L574–578 記特定第 579776 號實用新案 1972 年屆滿及其後已有與原告無關的多家公司經營。新 fact 4 把這兩段同來源的事實列成一條限定的時間線，清楚區分訴外公司與原告、特定權利與所有權利。工人不能直接讀 PDF；新的正式 row reviewer-only 清單必須為 `[4]`，並按本版 story SHA 重新審查。
3. **後場與盤色分路。** `must_verify[9]` 與父版逐字相同，只含[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的後場製作、直線送盤，仍為 `attributed:true`；第三版全文 T04 已口播「發明協會記錄」。盤色／裝飾分價只加進來源 [2] 的 `supports` 和 `turn.point`，T06 原文不唸來源，沒有再被複合 fact 9 強制口播歸屬。[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)原文同頁確有盤色或裝飾分價；`plan.mjs` 將來源 `[2]` 的 `archive` 列入 `PRIMARY_KINDS`，獨立重算 `claimSupported({sources:[2]})` 為 true。來源卡是觀眾可見的補充出處；真正的正式查核仍須靠逐景 claim `source:2, fact:null` 與來源段落，不能只靠卡片字樣。
4. **未實作的 t18。** `routing-amendment.json` 把歷史設計的 `t18→fact 11` 改為未來 T06 `turn-s088` 的盤色 claim、`source:2, fact:null` 及非朗讀來源卡；`t3` 則改路由至新 fact 4。`turn-s088` 在目前父版仍是座位問句的 `shot`，舊 `t18` 仍在 `turn-s092`、指 fact 7；本包沒有假稱兩者已改好。**必須在正式章稿進 verifier 前就把 t18 的 scene／source／fact 與句子一同改寫。** `story.mjs` 的 `checkedRows` 對已有 ID 若收到 `fact:null` 會回退到前一筆的 fact，因此不能指望 verifier 直接把舊 t18 的 fact 7 清成 null。正式改稿後需核對 source 卡採用支援的 title／後製方式、可讀性、插圖占比、卡片連續數和說話時間；卡片不是模型插畫中的可讀文字。

## 本收據不解鎖的關卡

本版仍無獨立的正式 row `review-candidate.json`；舊 85 景和 65 筆主張位元組未變，所有舊主張仍 `UNCHECKED`。新版 85 景／88 句改寫、t18 實際 `fact:null` 讀回、逐章 verifier／listener／narrative、與固定全文逐字對位、TTS／Jev、MiniMax 圖片、繁中 CC、聲畫 QA、成片與站主看片均未完成。沒有主機寫入、付費呼叫、匯入、上傳或發布。任一上列受審 SHA 改變，本收據須重新出具。
