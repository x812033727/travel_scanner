# B18 Row10b 獨立企劃來源審查候選

2026-10-17；審查者 Codex `/root/b18_row10b_formal_offline_review_1017`。**結論：Row10b 企劃來源離線 PASS，整體 Phase 4 採用 HOLD（整合 P2 一項）。** 本目錄只保存隔離的 `reviews/B18.json` 形狀候選，不是正式匯入、工人逐章查核、付費製作或成片審核收據。

## 固定的受審版本

| 對象 | SHA-256 |
| --- | --- |
| `../B18-route-b-row10b-candidate-20261017/B18.json` | `6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc` |
| Row canonical `storyHash` | `fbcff4985abae065811ff41cb234ac4190fd22cc8129e03f43048d5dd42af665` |
| `../B18-route-b-phase4-candidate-20261017/B18.md` | `73236441aebc92e804436fd9371a3044a27e5decdd7438905459ef214023768f` |
| `../B18-route-b-phase4-candidate-20261017/sha256.json` | `efdf3994152db18892d70c35f6ae10ba3f1d4a9076078922a8a988ee0bbd7422` |
| `../B18-route-b-phase4-full-editorial-review-20261017.md` | `52172dd22d2a0d349bea7ff7568cbaa2aecef5ab61d2929ad82048df967d745e` |

`review-candidate.json` 使用 `plan.mjs` 的 `REVIEW_KEYS`：`id`、`reviewed`、`reviewer`、`story_sha256`、`verdict:pass`、`sources_opened:6`、`changes:[]`、短 `notes`、`reviewer_only:[4]`。`reviewer_only` 應放在審查收據，不直接加到原始 row；編譯器才會把它投影到 `must_verify[4]`。舊 active 收據綁的是 `d0a9e19d…`，對本版失效。

## 六個來源與十筆事實

直接重新開啟六個原 URL，按 0 起算的來源索引核對：

| 索引 | 原始來源 | 本次查到的範圍 |
| --- | --- | --- |
| 0 | [中小企業基盤整備機構 J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) | 1947 立食店四貫 20 日圓、1948 吹田啤酒廠、轉角掉盤與撲克牌版本、1957 試作、1958 開店、律師警告及後來加盟店獨立；同文 1978 權利說法與法院特定權利認定衝突。 |
| 1 | [日本機械學會機械遺產 112](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html) | 1958 年 4 月布施首店；1985 年製、堺東店當時仍在用的機器，與元祿產業另存的早期魚鱗／三日月板分列。 |
| 2 | [發明協會迴轉壽司沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) | 立食店四貫 20、名片扇形版本、1958 約 20 坪及四貫 50、1962 實用新案、萬博表彰與約 240 家、後場製作和直線送盤、盤色／裝飾區分價格。其 1978 版本只列分歧。 |
| 3 | [日本法院官方判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) | 理由 P8 L466–469 登記號；P8 L476–495 指獲授權的訴外元祿於 1967 年在仙台開直營首店、東京錦糸町開連鎖首店；P10 L574–578 僅認第 579776 號實用新案於 1972 年期滿，之後有與原告無關業者。工人讀不到 PDF 文字，故 fact 4 為 reviewer-only。 |
| 4 | [石野集團／北日本カコー年表](https://www.ishino-group.com/history/) | 1980 大型店旁通裝置、1986 ㄇ字型輸送帶店是兩個年份與設備節點；1971 已販售附給茶裝置的輸送帶。 |
| 5 | [石野集團介紹](https://www.ishino-group.com/group/) | 集團介紹將整合給茶裝置寫成 1974；和同集團年表的 1971 記述有差異，本版只作 caveat，不作口播事實。 |

| `must_verify` | 結論與限定 |
| --- | --- |
| 0 | PASS：1958 年 4 月首店由 0／1 支持；約 20 坪、四貫 50 日圓由 2 支持，和舊立食店 20 日圓分開。 |
| 1 | PASS：1948 吹田工廠及送瓶啟發由 0 支持；未指名啤酒公司。 |
| 2 | PASS：先前四貫 20 日圓與人手瓶頸由 0／2 支持；不移作 1958 首店價。 |
| 3 | PASS：0 的撲克牌、2 的名片版本分開歸屬；1957 試作與轉角掉盤見 0。`attributed:true` 保留。 |
| 4 | PASS，`reviewer_only:[4]`：僅引 3 的法院認定；1967 係被授權訴外公司，1972 係特定第 579776 號權利；不能外推所有權利或唯一展店原因。 |
| 5 | PASS：0 報導律師警告和部分加盟店獨立；仍以該報導歸屬，沒有擴大成全國禁令。 |
| 6 | PASS：1970 萬博出店 0／2；表彰和約 240 家屬 2，不把 0 的約 250 家混入。`attributed:true` 保留。 |
| 7 | PASS：1 清楚分開 1985 店內機器和另存的早期板片；非首店原機。 |
| 8 | PASS：4 支持 1980 旁通裝置與 1986 ㄇ字型店；不推斷同一家店的連續改裝。 |
| 9 | PASS：2 支持後場製作／直線送盤，`attributed:true` 適用這整筆 fact；Phase 4 T04 口播已有發明協會歸屬。盤色分價只在來源 2 的 `supports` 與章節規劃，不混入 fact 9。 |

Row10b `build.mjs --check` 回 `PASS_OFFLINE_ROW_SCHEMA_ONLY_HOLD`、10 facts；本候選 `check.mjs` 驗 `storyProblems=[]`、`reviewProblems=[]`、`storyHash`、六來源數、`reviewer_only:[4]`、Phase 4 受審檔案 SHA，以及編譯時的 800 字 caveats 限制。這些是離線格式與來源審查，不會把 65 筆 `UNCHECKED` 改成 `CONFIRMED`。

## Phase 4 整合仍 HOLD：P2 一項

Row10b 的 [`routing-amendment.json`](../B18-route-b-row10b-candidate-20261017/routing-amendment.json) 對 `t18` 明定 `visual_source_card`，且 `post_verifier_persisted_readback_required` 要求 `source_card_present:true`、`source_card_not_spoken:true`。這是當時第三版 T06 **沒有口播來源**的補救條件。受審 Phase 4 [`B18.md`](../B18-route-b-phase4-candidate-20261017/B18.md) 已在 T06 口播「發明協會的沿革」，製作註則把完整出處放在註與說明欄；[`turn-s088`](../B18-route-b-phase4-candidate-20261017/remapped-chapters/turn.json) 是 `shot`，94 個插畫鏡頭加 `now-outro` 沒有原生來源字卡。Phase 4 已有 `t18=turn-s088/source:2/fact:null/UNCHECKED` 的**離線**形狀，但沒有滿足舊路由收據的來源卡讀回條款。不能把先前 Row10b 設計 PASS 或 Phase 4 全文 PASS 當成此整合條款已通過。

最小修正選項：另立受審路由修訂，把 `t18` 的非朗讀卡要求改為 **T06 可聽發明協會歸屬 + 正式影片說明欄完整來源 URL**，保留 `source:2/fact:null` 的逐景主張、正式 verifier 前寫入、verifier 後持久化讀回與 `UNCHECKED` 起始狀態。這維持 Phase 4 的 shot-only worker 形狀，不用把可讀文字塞進 MiniMax 插畫。修訂必須獨立審查；本收據沒有替它簽核。若仍要畫面內來源卡，須另行證明 worker 支援的卡片型別、畫面可讀性和插畫占比，重審變動分鏡。

其他後續關卡：Row10b 實際匯入包與 A01 企劃列不變性、正式工人 B18 script reference 更新及 CI／部署、真實六章 writer/verifier/listener/narrative、65 個 claim 判定、t18 正式讀回、TTS 9–11 分鐘、Jev、MiniMax 真圖及連續三鏡小樣、繁中 CC、成片 QA 與站主看片；B18 付費尚未核准。本目錄未做主機寫入、付費、匯入、部署、上傳或發布。
