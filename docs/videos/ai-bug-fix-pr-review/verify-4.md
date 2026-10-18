# 第四輪完整來源查核：AI 修好 Bug 就能合併？

查核日：2026-10-08，Asia/Taipei。Reviewer：agent_offline_audio，獨立於 cadence 候選作者與套用者。本 reviewer 只在 repo 新增本報告。

**結果：目前文字 VERIFIED，0 未解事實缺口。** 完整覆核已套用稿的 350 項 leaf 值：133 句旁白、201 項 visual-data 字串、7 項 metadata、3 項縮圖、6 項章節。判定為 CONFIRMED 164、OUT OF SCOPE（編輯／教學判斷）186、NOT FOUND 0；47 場宣告的 visual／reveal／highlight 語意時機 PASS。所有繼承內容亦重新讀取，並非只審 delta，也沒有因「純視覺」自動接受新增可見字詞。

本結論限來源文字與宣告時機，不是音訊、實際 glyph／layout、player、成片 QA、owner 聽感、approval、upload 或 publication。原始歷史 Claude CLI 命令／JSON／exit／費用缺證仍保留，沒有藉由本地 replay 或檔名宣告工具作者。

## 目前正式版本綁定

Final source：video.json，39172 bytes；完整 SHA256 4608bffb664b8d5a99667daae019184750b73fdaefe32256b08c0494f88c6cca。
Current claims：claims.md，4553 bytes；完整 SHA256 8173695736493aa0f44e544d56354d898009c659d0180cf21dc8e3210c5eb809。
Before source：7cddf570305b4afa8d87833aec8fac92ab3469648674fd6d17d085fd0dffe0d4，28840 bytes；133 句、28 場景、261 項 leaf。新稿 47 場景、133 句、350 項 leaf；六章節身分／文字及全部 top-level metadata／縮圖／sources 未動。
舊完整第三輪 verify-3-20261008.md：64320 bytes；SHA256 94eb37845906c4b370640eb464d81603ae196175a04e83d0d291932eb5a402bd；它綁 before7cdd，不能單獨作新4608完整查核。

私有候選完整審查已在套用之前封存且保持原 bytes：

- <private>/private-cadence-review/complete-candidate-review-20261008T011228443801Z-51ac527c-1d8a-41cb-9cb3-71b5aca29cac.json：337817 bytes；SHA256 18cc9e53c534461cf94fdd549d49f958e2b852d3fee47839f914ae7b704de05d。
- 同 prefix .md：103347 bytes；SHA256 283b9c00af407e0aa329e5866e49e67b174db901857db76853f6efb6d93acc79。
- 候選 closure：5276641958aa0a35a9a3549b78aecf36c758be33a8359c542cc47ede0c18cb9b。
- 完整 mechanical／133 raw WAV binding：321403174887d5830c7f5db2c284745b8ad20864ac56376efd2bca3ed7770732。

實際套用收據：<private>/recovery-audit/cadence-adoption-20261008T011621832539Z-3de655fd-c81e-4273-93b9-7206fefa2d75/receipt.json；完整 SHA256 8b03e250f2df3398de9821549924374756ade2f3fc3e45d0ca14e22677327921；記錄 2026-10-08T01:19:19.758719+00:00 已套用 4608、133 spoken entries unchanged、47 scenes／88 states，provider0；收據當時 audio_qa_passed=false、owner_acceptance=false。

本報告建立時 2026-10-08T01:26:47.284122+00:00 重新讀 source 與新版 claims；source bytes 正好等於已完整覆核候選。新版 claims 另記實際主旁白與初輪 flags 的作業狀態，明示非最終音訊／成片／owner 核准；其 hash 不再冒用候選審查時舊 claims hash。

原稿全261 extraction objects（number／where／value／kind／scene）精確等同 fresh-round3/current-extraction-final.json，SHA39c950ffe4d80d9177527da4e67508c25ed0523e1badf08f63fb372afc701a79。新稿350全部逐項審查，其中57個新 visual leaf 字串 occurrences 不在原261同kind值，亦逐項核對其已有旁白、實際 patch、需求與 replay。Code highlight未刪除原完整code／caption；新增文字未引入新產品版本、價格、執行者歸因或核准。

本 reviewer 未要求新增事實修正：fact edits0。從已審候選轉為已套用正式稿時，只更新版本狀態／source與claims綁定；以下完整350逐項表格及47場 notes與原私有報告保持相同。

來源位置：<repo> 指 checkout；<private> 指本輪私有證據目錄。Demo檔名位於 <repo>/docs/videos/ai-bug-fix-pr-review/demo/；CHALLENGE 位於相鄰 ai-coding-tools-same-task/demo/；四語位於本片 i18n/。官方 raw／headers／visible text、actual stdout／stderr 與 replay receipt 位於 <private>/independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1/。這些 logical paths 不公開主機／使用者路徑。

## 機械、metadata與實際媒體binding

完整133 spoken lineobjects（只排除reveal）、ID及次序不變；native linekeys全相同，staleTakes0，cache與oldtimeline全WAVfullSHA匹配。所有topfields、6chapterid/label、metadata/thumbnail/source_checked_on深等。Pure candidate17881frames／596.033333秒、88states、max13.0秒；19新scene依原生增加13.3秒，不是低速播放。舊actual17482frames／582.733333秒，不能把候選推算寫成原生完成。

實際舊audio完整技術收據4abffa6520b1e6cc2ddd459cb982ae3d21e3ec0256845c917ce53d16fd7df787；133WAV和重建旁白bytes相同。oldtimeline4f93c1952c63aa9f0729bd8970694713ca2d1b6c692835556390d50c943005b9；narrationbeea8a9c22c970a02124d1cc196f37edcddc43cdf18f5ac9e12c1bbbc8f527bd。Candidate speechHash2343b0c92135e5fa與舊e1bbfc917180620f不同，需正常native重建及重新binding aggregate；本review不執行。

原生visibility=count-totalReveals+reveal，已逐47scene查初始與新項，code全內容/caption保留只換highlight。實際字卡render及readability另由後續實物檢查，不從此公式推定。

Metadata及縮圖為AI修補教學問句/建議；description明確本地可重跑、非正式事故/非已合併。沒有重引Claude作者。Brief歷史Claude歸因不能當原始CLI證據。

## 來源清單與scope

- fare.mjs: 424B；完整SHA 53a822df2b194a252cff62e52b2a0d7418d593537d54b13e054cb794eafc4665
- fare.test.mjs: 322B；完整SHA 3ec607b3f151af05ed49d4f2b5597e9bd5ff15c043794aa08d39083092a3ca19
- acceptance.test.mjs: 1115B；完整SHA 236c499487e47419157ee7d35bf443ccd95859fa95e0b07cbc6ae3e79302a1ba
- claude.patch: 2738B；完整SHA 3d793faef18e5508fe7825d57158a24a60c1c18c62c0ed75672ac2b99ca1db1a
- claude-acceptance-output.txt: 355B；完整SHA a74c7a10e44941233f10f52b22477c8f2be317d4a06b566f93e3be0c8bfbba1e
- claude-acceptance.png: 45733B；完整SHA a0ab2d33e04606260f4c1a118013826a94f09db68c816b53527407bce699427a
- brief.md: 2226B；完整SHA 511afa8537ca1807ccc84aa25019e0a055349ba1168bcf9f8dd73f2738d749c4
- 候選審查當時 claims.md: 3613B；完整SHA a0e439c36cd833291827c993c64e2ecd8d495fc83228b950fa93c3e7b434c983；目前 claims.md: 4553B；完整SHA 8173695736493aa0f44e544d56354d898009c659d0180cf21dc8e3210c5eb809
- verify-3-20261008.md: 64320B；完整SHA 94eb37845906c4b370640eb464d81603ae196175a04e83d0d291932eb5a402bd
- CHALLENGE.md: 475B；完整SHA 80a2ad6b1f3dd7bc6f6e819bc87007e21b2570ee53a683ece0b508b77895655a
- en.json: 19247B；完整SHA c665271bc455acad57f27d727b1e34778c11973c4ee965d0dd372e276550d5cd
- ja.json: 20757B；完整SHA 7bfd43d8fc6c24aa6019d2e56200ee995e81f2c24c63de808eca680867674aa2
- ko.json: 21597B；完整SHA 7011243d495915a7e6e5fb6ed4a4aafd32f15c0500ff3708f5cc0e138589e4bd
- zh-CN.json: 18854B；完整SHA b65113db230c2bf87c478afe2f981aece3f59a31d6d98b595667d3a513cac688

第三輪actual replay receipt 37edaa812e09584cbbb2df55342df27c98915420e88fcf7a8b6e854e50236d69：已讀stdout並重驗全SHA，舊2/2 exit0、舊事後1/4 exit1、修補9+4=13/13 exit0。100/3舊[33,33,33]新[34,33,33]、2/3舊[1,1,1]新[1,1,0]、新2/5[1,1,0,0,0]；10020組不是全safe integer形式化證明。完整patch只改fare.mjs/test且原guards保留。本review沒有rerun。

已看實際claude-acceptance.png：4testnames、4pass/0fail與保存txt一致；圖661.8585ms是保留輸出重排，非本輪duration或原始terminal。檔名不證明AI/Claude作者。
- [github-review](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart)：actualHTTP200 at 2026-10-07T23:48:59.994139+00:00；raw135493B SHA eb717cc3208ff89ee55fbd6dd8902b7040708b2a2b81956269ca3af53af82ec2；text SHA e9561c377f094c0f21a3df582a65d556c96b04ecfbaa78b7e01f36bee4d55200；官方流程參考；GitHub 支援變更行留言、要求修改及核准。Claude CLI 只支援現行參考背景，不能證明歷史工具作者、命令、JSON、exit 或費用。
- [claude-cli](https://code.claude.com/docs/en/cli-reference)：actualHTTP200 at 2026-10-07T23:49:01.108852+00:00；raw539027B SHA 918f104b0dd820eb969918624984175941b8bc2992abf2a66080bba51115a15a；text SHA db92da1399e695d3a051eb70a46290fd391abe4a21c197582096aeb54d7fbc65；官方流程參考；GitHub 支援變更行留言、要求修改及核准。Claude CLI 只支援現行參考背景，不能證明歷史工具作者、命令、JSON、exit 或費用。

## 全47scene逐項時機

| scene | IDs | 判定與notes |
| --- | --- | --- |
| opening | v40000,v40001 | PASS：舊2/2綠但100/3總和99有實際probe；AI問句是教學假設，不是本patch作者證據。 |
| opening-gates | v40002,v40003 | PASS：v40002同句列三關，三項同時可見；編輯方法不是GitHub強制規則。 |
| why-green | v40007,v40008 | PASS：舊檔僅整除和零人兩測試；2測試不代表需求完整。 |
| why-green-missing | v40009,v40010,v40011 | PASS：v40009換卡，未測不整除限定舊兩測試；非全產品頻率聲明。 |
| old-test-code | v4e1000,v4e1001 | PASS：完整四行保留；highlight1/2對應120/3及第一assert，實際baseline存在。 |
| old-test-code-part2 | v4e1002,v4e1003 | PASS：v4e1002起highlight3/4對應零人RangeError；全四行仍在。 |
| bug-example | v40014,v40015 | PASS：100/3 baseline[33,33,33]總和99；highlight1/2呼叫及輸出一致。 |
| bug-example-part2 | v40016 | PASS：v40016是假設帳務風險；highlight3少一分，非正式帳務事故。 |
| bug-example-part3 | v40017,v40018 | PASS：v40017預告下個修補，舊失敗圖作回顧；v40018已有acceptancefile，未叫舊碼已修好。 |
| patch-source | v40021,v40022,v40023,v40024,v40025 | PASS：v40021/22/23/24逐項diff、9重跑、非正式事故/合併、可重跑；9不混13，無Claude歸因。 |
| gate-one | v40028,v40029 | PASS：需求章節兩句是審查建議。 |
| gate-one-rules | v40030,v40031,v40032 | PASS：v40030/31/32逐項輸入、分配、口述；與CHALLENGE和原guards相符。 |
| contract | v40035,v40036,v40037,v40038,v40039,v40040 | PASS：初顯長度；v40036/37/38依序總和/差額/順序；四條CHALLENGE一致。 |
| small-remainder | v4e2000,v4e2001 | PASS：2/3新[1,1,0]有probe；v4e2000預告第二例、v4e2001解釋，不錯置結果。 |
| small-remainder-total | v4e2002,v4e2003 | PASS：左起始[1,1,1]總和3、右需求[1,1,0]總和2，實際probe成立。 |
| inputs | v40042,v40043,v40044,v40045,v40046 | PASS：先總額、v40044顯1..100、v40045顯保留；人數安全整數由旁白明示，卡不取消限定。 |
| contract-case | v40049,v40050 | PASS：100/3新[34,33,33]總和100與餘數順序一致；舊99正確。 |
| contract-case-check | v40051,v40052,v40053 | PASS：差不多不足、尺是比喻；v40053才加2/3，probe及契約相符。 |
| gate-two | v40056,v40057 | PASS：讀diff不只摘要是審查方法，無模型性能宣稱。 |
| gate-two-reading | v40058,v40059,v40060 | PASS：v40058/59/60代入、guards、檔案；第三項回顧差異，未另造新增檔案。 |
| diff-core | v40063,v40064 | PASS：完整四行保留，highlight1/2是base/remainder，與patch等價換行。 |
| diff-core-part2 | v40065,v40066 | PASS：highlight3/4是Array.from；100=33*3+1，首位34其餘33。 |
| diff-core-part3 | v40067 | PASS：highlight2/4餘數條件；2/3 base0 remainder2，前兩位1。 |
| validation-stays | v4e3000,v4e3001,v4e3002,v4e3003 | PASS：初顯兩guards，v4e3002揭只換分配；原patch未刪guards，不背書其他檔案。 |
| diff-check | v40070,v40071,v40072,v40073,v40074,v40075 | PASS：v40070/71/72/74依序guards/兩檔/新assert/另議部署帳務；最後是如果建議非本次部署修改。 |
| test-assertions | v4e4000,v4e4001 | PASS：完整四行assert；highlight1/2的100/3新結果存在實際patch。 |
| test-assertions-part2 | v4e4002,v4e4003 | PASS：v4e4002 highlight3/4；2/5[1,1,0,0,0]存在patch，不以數量代需求。 |
| not-real-pr | v40077,v40078 | PASS：本地patch範圍保留；沒有把真實PR核准當證據。 |
| not-real-pr-scope | v40079,v40080,v40081 | PASS：付款系統是如果條件；依序方法與非核准，未宣稱付款整合驗收。 |
| gate-three | v40084,v40085 | PASS：明說事後驗收；工具自寫測試是泛稱限制，不證明這9项作者。 |
| gate-three-replay | v40086,v40087,v40088 | PASS：v40086/87/88舊碼重現、同份事後驗收、評估修補；理想順序非預先盲測。 |
| red-first | v40091,v40092,v40093,v40094,v40095 | PASS：先左2/2和1/4，v40093才右9和4/4；總13是9+4，來源不混。 |
| property | v40098,v40099 | PASS：全8行code；highlight1/2對0..500、1..20，caption明示改寫且省略lengthcheck。 |
| property-part2 | v40100,v40101 | PASS：highlight4/5/6是sum和max-min；實際10020組具assert。 |
| property-part3 | v40102,v40103 | PASS：highlight1/2/5/6對範圍和條件；旁白保留非形式化證明與業務風險。 |
| test-output | v4shot0,v4shot1 | PASS：實際檢視PNG/txt四名稱、4/4及旧durations一致；明示輸出重排，非原terminal或本輪時長。 |
| property-check | v4e5000,v4e5001,v4e5002,v4e5003 | PASS：先總額、v4e5001/2顯長度和差額；實際每組三檢查，節錄省length不代表原檔缺。 |
| inputs-test | v40105,v40106,v40107,v40108,v40109 | PASS：零金额每人0，非法總額/人數及保護依句揭露；v40109僅可能風險，非頻率。 |
| three-gates | v40112,v40113 | PASS：編輯方法與brief立場一致，非官方機械規則。 |
| three-gates-evidence | v40114,v40115,v40116 | PASS：差異後回歸，只說測試範圍成立，非全域證明。 |
| review-summary | v40119,v40120,v40121,v40122,v40123 | PASS：v40119 title-only，v40120/21/22逐條需求、兩檔、紅綠，圖句一致。 |
| review-record | v4e6000,v4e6001,v4e6002,v4e6003 | PASS：v4e6000/1/2逐項失敗案例、完整diff、指令範圍，是可重跑建議。 |
| limits | v40126,v40127,v40128,v40129,v40130 | PASS：初title-only；v40127需求、v40128同時範圍/回滾、v40129負責者，不宣稱QA核准。 |
| github | v40133,v40134 | PASS：官方capture支持變更行留言、要求修改、核准；不說影片真實操作。 |
| github-evidence | v40135,v40136,v40137 | PASS：v40135/36/37逐項不核准/可追溯/不用他人PR，保持本地範圍且無帳號資料。 |
| outro | v40140,v40141 | PASS：AI修好回到教學問句；人判斷，沒有本patch工具歸因。 |
| outro-practice | v40142,v40143,v40144 | PASS：v40142/43/44一起核對、練小修補、再較大改動；較有用是建議非測量。 |

## 全350候選leaf逐項

| # | where | actual current value | verdict | evidence |
| --- | --- | --- | --- | --- |
| 1 | youtube.title | AI 修好 Bug 就能合併？三個 PR 檢查點 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 2 | youtube.description | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 3 | youtube.tags[0] | AI code review | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 4 | youtube.tags[1] | PR review | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 5 | youtube.tags[2] | Bug fix | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 6 | youtube.tags[3] | 程式碼審查 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 7 | youtube.tags[4] | 回歸測試 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 8 | thumbnail.data.tag | AI 修補審查 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 9 | thumbnail.data.headline | 測試綠了？<br>**先過 3 關** | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 10 | thumbnail.data.sub | 需求／差異／回歸 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 11 | opening.chapter | 綠燈也會漏 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 12 | opening.data.tag | AI 修補審查 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 13 | opening.data.title | 測試全綠，還少一分 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 14 | opening.data.subtitle | 合併前先過三道關 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 15 | v40000.text | 三個人分一百分，舊測試全綠，結果卻只分出九十九。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 16 | v40001.text | AI 送來一份修補程式，你會直接合併嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 17 | opening-gates.data.title | 合併前的三道關 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 18 | opening-gates.data.items[0] | 需求契約 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 19 | opening-gates.data.items[1] | 實際差異 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 20 | opening-gates.data.items[2] | 回歸測試 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 21 | v40002.text | 我帶你看需求、差異與回歸，三道關都要過。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 22 | v40003.text | 我們先從那一分為什麼消失開始。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 23 | why-green.chapter | 綠燈不等於正確 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 24 | why-green.data.kicker | 第一個畫面 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 25 | why-green.data.text | 2 個測試通過 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 26 | why-green.data.sub | 但不代表需求被測完 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 27 | v40007.text | 第一個舊測試，只檢查能整除的金額。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 28 | v40008.text | 人數不合法也會擋，兩個結果都是綠色。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 29 | why-green-missing.data.kicker | 沒被測到的路徑 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 30 | why-green-missing.data.text | 不整除的案例 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 31 | why-green-missing.data.sub | 綠燈不能證明帳算對 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 32 | v40009.text | 不整除的路徑沒人問，所以錯誤藏得好好的。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 33 | v40010.text | 這次示範是真正執行的檔案，不是想像案例。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 34 | v40011.text | 它證明程式照舊測試運作，沒有證明帳算對。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 35 | old-test-code.data.title | 綠燈實際測了什麼 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 36 | old-test-code.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 37 | old-test-code.data.code | assert.deepEqual(splitFareCents(120, 3),<br>  [40, 40, 40]);<br>assert.throws(() => splitFareCents(100, 0),<br>  RangeError); | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 38 | old-test-code.data.caption | 原本只有整除和非法人數兩題 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 39 | v4e1000.text | 這是起始專案真的跑過的兩個測試。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 40 | v4e1001.text | 第一個測一百二十分，三人平均分。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 41 | old-test-code-part2.data.title | 綠燈實際測了什麼 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 42 | old-test-code-part2.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 43 | old-test-code-part2.data.code | assert.deepEqual(splitFareCents(120, 3),<br>  [40, 40, 40]);<br>assert.throws(() => splitFareCents(100, 0),<br>  RangeError); | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 44 | old-test-code-part2.data.caption | 原本只有整除和非法人數兩題 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 45 | v4e1002.text | 第二個測零人時要拋出錯誤。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 46 | v4e1003.text | 它們全綠，只能證明這兩件事，不能代表餘數正確。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 47 | bug-example.data.title | 漏掉的案例 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 48 | bug-example.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 49 | bug-example.data.code | splitFareCents(100, 3)<br>// 原本得到 [33, 33, 33]<br>// 總和 99，少了 1 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 50 | bug-example.data.caption | 起始程式與事後測試實際輸出 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 51 | v40014.text | 分一百分給三個人，原始程式回三個三十三。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 52 | v40015.text | 這不是顯示格式的問題，總和真的少了一分。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 53 | bug-example-part2.data.title | 漏掉的案例 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 54 | bug-example-part2.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 55 | bug-example-part2.data.code | splitFareCents(100, 3)<br>// 原本得到 [33, 33, 33]<br>// 總和 99，少了 1 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 56 | bug-example-part2.data.caption | 起始程式與事後測試實際輸出 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 57 | v40016.text | 如果少掉的一分錢會記入帳務，就算測試全綠也不能合併。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 58 | bug-example-part3.data.title | 漏掉的案例 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 59 | bug-example-part3.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 60 | bug-example-part3.data.code | splitFareCents(100, 3)<br>// 原本得到 [33, 33, 33]<br>// 總和 99，少了 1 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 61 | bug-example-part3.data.caption | 起始程式與事後測試實際輸出 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 62 | v40017.text | 接下來看一份可以重跑的本地修補。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 63 | v40018.text | 這個失敗結果已寫進可重跑的驗收檔案。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 64 | patch-source.data.title | 這份示範的來源 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 65 | patch-source.data.items[0] | 程式和測試的完整差異 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 66 | patch-source.data.items[1] | 修補測試9項重跑全過 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 67 | patch-source.data.items[2] | 非正式站事故／非已合併PR | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 68 | patch-source.data.items[3] | 可公開重跑的本地修補 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 69 | v40021.text | 這份本地分攤範例，留下了程式和測試的完整差異。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 70 | v40022.text | 修補後的九個測試重跑全過，稍後再做事後驗收。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 71 | v40023.text | 這不是正式站的事故，也不是已合併的真實 PR。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 72 | v40024.text | 它是可以公開重跑的一份本地修補案例。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 73 | v40025.text | 所以它適合用來練審查，卻不能代表產品事故。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 74 | gate-one.chapter | 第一關：需求契約 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 75 | gate-one.data.title | 先問：修的是哪個需求？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 76 | v40028.text | 第一關，不要先看 AI 說它完成了什麼。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 77 | v40029.text | 先把需求寫成你可以算得出來的條件。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 78 | gate-one-rules.data.title | 需求包括原有規則 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 79 | gate-one-rules.data.items[0] | 保留輸入規則 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 80 | gate-one-rules.data.items[1] | 保留分配規則 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 81 | gate-one-rules.data.items[2] | 驗收條件能自己口述 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 82 | v40030.text | 這題要保留輸入規則，不能只修一個範例。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 83 | v40031.text | 也不能悄悄把分配規則改成另一種做法。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 84 | v40032.text | 第一關的答案，應該能不靠工具自己口述。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 85 | contract.data.title | 需求契約四條 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 86 | contract.data.steps[0].title | 長度 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 87 | contract.data.steps[0].detail | 每人一個整數金額 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 88 | contract.data.steps[1].title | 總和 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 89 | contract.data.steps[1].detail | 加起來等於原金額 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 90 | contract.data.steps[2].title | 差額 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 91 | contract.data.steps[2].detail | 最多相差一分 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 92 | contract.data.steps[3].title | 順序 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 93 | contract.data.steps[3].detail | 餘數先給前面的人 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 94 | v40035.text | 第一條，結果長度要和人數一樣。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 95 | v40036.text | 第二條，所有人的份額加總，必須等於原來金額。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 96 | v40037.text | 第三條，任何兩人最多只差一分。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 97 | v40038.text | 第四條，有餘數時，前面的人先分到。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 98 | v40039.text | 四條放在一起，才描述完整的分攤行為。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 99 | v40040.text | 如果只補一百除三，還會漏掉其他金額。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 100 | small-remainder.data.kicker | 再代一組 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 101 | small-remainder.data.text | 2 分給 3 人 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 102 | small-remainder.data.sub | 正確結果：1、1、0 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 103 | v4e2000.text | 只測一百分除三，還可能把規則寫死在特例上。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 104 | v4e2001.text | 再代入兩分給三個人，正確是前兩位各一分。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 105 | small-remainder-total.data.title | 2分分給3人 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 106 | small-remainder-total.data.left.heading | 起始程式 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 107 | small-remainder-total.data.left.points[0] | 1、1、1 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 108 | small-remainder-total.data.left.points[1] | 總和3 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 109 | small-remainder-total.data.right.heading | 需求結果 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 110 | small-remainder-total.data.right.points[0] | 1、1、0 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 111 | small-remainder-total.data.right.points[1] | 總和2 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 112 | v4e2002.text | 第三位拿零分，總和仍是兩分。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 113 | v4e2003.text | 這組資料會立刻露出四捨五入重複分配的問題。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 114 | inputs.data.title | 原有輸入規則也算契約 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 115 | inputs.data.items[0] | 總額：非負安全整數 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 116 | inputs.data.items[1] | 人數：1到100 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 117 | inputs.data.items[2] | 原有輸入檢查要保留 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 118 | v40042.text | 還有原本就存在的輸入檢查。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 119 | v40043.text | 總額不能是負數、小數或超過安全整數。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 120 | v40044.text | 人數只能是一到一百之間的安全整數。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 121 | v40045.text | 修補若刪掉這些檢查，就算範例變對也不能過關。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 122 | v40046.text | 它們不是額外加分題，而是修補前就有的規則。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 123 | contract-case.data.title | 一個例子，看四個條件 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 124 | contract-case.data.left.heading | 原本 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 125 | contract-case.data.left.points[0] | 33、33、33 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 126 | contract-case.data.left.points[1] | 總和 99 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 127 | contract-case.data.right.heading | 需求 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 128 | contract-case.data.right.points[0] | 34、33、33 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 129 | contract-case.data.right.points[1] | 總和 100 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 130 | v40049.text | 把一百分除以三，理想結果是三十四、三十三、三十三。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 131 | v40050.text | 這組數字同時檢查總和與餘數順序。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 132 | contract-case-check.data.title | 總和與順序一起看 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 133 | contract-case-check.data.items[0] | 每人差不多還不夠 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 134 | contract-case-check.data.items[1] | 需求契約是審查的尺 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 135 | contract-case-check.data.items[2] | 2分給3人：1、1、0 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 136 | v40051.text | 只測每個人差不多，還是不夠。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 137 | v40052.text | 需求契約先寫清楚，才有審查的尺。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 138 | v40053.text | 換成兩分三人，正確順序也是一、一、零。 | CONFIRMED | E1/E2/E3; exact challenge, input guards and private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 139 | gate-two.chapter | 第二關：讀差異 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 140 | gate-two.data.title | 逐行看它改了什麼 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 141 | v40056.text | 第二關，打開實際差異，不只讀工具的完成訊息。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 142 | v40057.text | 先確認它只改到預期的程式和測試。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 143 | gate-two-reading.data.title | 直接檢查實際差異 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 144 | gate-two-reading.data.steps[0].title | 代入 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 145 | gate-two-reading.data.steps[0].detail | 100分給3人 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 146 | gate-two-reading.data.steps[1].title | 保護 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 147 | gate-two-reading.data.steps[1].detail | 原輸入條件保留 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 148 | gate-two-reading.data.steps[2].title | 差異 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 149 | gate-two-reading.data.steps[2].detail | 直接看檔案變更 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 150 | v40058.text | 接著把新增邏輯代入一百分除三的例子。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 151 | v40059.text | 最後看它有沒有刪掉原來的保護條件。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 152 | v40060.text | 文字摘要可能遺漏細節，差異本身才是檢查對象。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 153 | diff-core.data.title | 修補的核心四行 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 154 | diff-core.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 155 | diff-core.data.code | const base = Math.floor(totalCents / people);<br>const remainder = totalCents - base * people;<br>return Array.from({ length: people }, (_, i) =><br>  i < remainder ? base + 1 : base); | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 156 | diff-core.data.caption | 從本地修補差異節錄 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 157 | v40063.text | 這份修補先算每人最少要拿多少。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 158 | v40064.text | 再算剩下幾分，要補給幾位前面的人。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 159 | diff-core-part2.data.title | 修補的核心四行 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 160 | diff-core-part2.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 161 | diff-core-part2.data.code | const base = Math.floor(totalCents / people);<br>const remainder = totalCents - base * people;<br>return Array.from({ length: people }, (_, i) =><br>  i < remainder ? base + 1 : base); | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 162 | diff-core-part2.data.caption | 從本地修補差異節錄 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 163 | v40065.text | 總額一百，分給三人，各拿三十三，還剩一分錢。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 164 | v40066.text | 第一位多拿一分，其餘兩位維持三十三。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 165 | diff-core-part3.data.title | 修補的核心四行 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 166 | diff-core-part3.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 167 | diff-core-part3.data.code | const base = Math.floor(totalCents / people);<br>const remainder = totalCents - base * people;<br>return Array.from({ length: people }, (_, i) =><br>  i < remainder ? base + 1 : base); | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 168 | diff-core-part3.data.caption | 從本地修補差異節錄 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 169 | v40067.text | 用兩分三人再代一次，就能看到前兩位各多一分。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 170 | validation-stays.data.title | 新邏輯前面的檢查還在 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 171 | validation-stays.data.items[0] | 總額先驗證 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 172 | validation-stays.data.items[1] | 人數先驗證 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 173 | validation-stays.data.items[2] | 只替換分配算法 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 174 | v4e3000.text | 完整差異顯示，函式前兩段輸入檢查仍然保留。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 175 | v4e3001.text | 非法金額和非法人數，仍會在分配前被擋。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 176 | v4e3002.text | 這份修補把平均四捨五入，換成基本分與餘數。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 177 | v4e3003.text | 這是這份本地差異的範圍，不替其他檔案背書。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 178 | diff-check.data.title | 差異裡的檢查與範圍 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 179 | diff-check.data.items[0] | 輸入驗證保留嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 180 | diff-check.data.items[1] | 有改題目以外的檔嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 181 | diff-check.data.items[2] | 新測試在驗什麼？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 182 | diff-check.data.items[3] | 部署／帳務設定要另外討論 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 183 | v40070.text | 我在差異裡先找原有驗證，這次沒有被刪掉。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 184 | v40071.text | 再看檔案清單，只有程式和測試被修改。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 185 | v40072.text | 新增測試涵蓋不整除、零金額和非法輸入。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 186 | v40073.text | 這些都是看得見的證據，不是工具的口頭保證。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 187 | v40074.text | 如果它順手改了部署或帳務設定，應該另外討論。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 188 | v40075.text | 新增測試也要看斷言，不只看測試名稱。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 189 | test-assertions.data.title | 新測試要讀斷言 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 190 | test-assertions.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 191 | test-assertions.data.code | assert.deepEqual(splitFareCents(100, 3),<br>  [34, 33, 33]);<br>assert.deepEqual(splitFareCents(2, 5),<br>  [1, 1, 0, 0, 0]); | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 192 | test-assertions.data.caption | 這兩個斷言存在實際修補測試 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 193 | v4e4000.text | 新增測試不能只看名字，要看它到底斷言什麼。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 194 | v4e4001.text | 這份修補測到一百分除三，是三十四、三十三、三十三。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 195 | test-assertions-part2.data.title | 新測試要讀斷言 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 196 | test-assertions-part2.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 197 | test-assertions-part2.data.code | assert.deepEqual(splitFareCents(100, 3),<br>  [34, 33, 33]);<br>assert.deepEqual(splitFareCents(2, 5),<br>  [1, 1, 0, 0, 0]); | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 198 | test-assertions-part2.data.caption | 這兩個斷言存在實際修補測試 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 199 | v4e4002.text | 也測到兩分分五人，前兩位各一分，其餘拿零。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 200 | v4e4003.text | 這兩組一起看，比只看測試數量更有意義。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 201 | not-real-pr.data.kicker | 範圍說明 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 202 | not-real-pr.data.text | 本地 patch | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 203 | not-real-pr.data.sub | 沒有真實 PR 審核紀錄 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 204 | v40077.text | 這裡展示的是本地修補，不是假裝已有人核准的 PR。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 205 | v40078.text | 真正的專案還要看相關模組、型別與維運影響。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 206 | not-real-pr-scope.data.title | 這份示範的適用範圍 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 207 | not-real-pr-scope.data.items[0] | 連付款系統時要擴大審查 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 208 | not-real-pr-scope.data.items[1] | 方法可帶入真實審查 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 209 | not-real-pr-scope.data.items[2] | 本地示範不等於核准 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 210 | v40079.text | 如果這段程式連著付款系統，範圍會更大。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 211 | v40080.text | 影片示範的方法，可以帶進真正的審查流程。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 212 | v40081.text | 我把這個範圍明確標出，避免觀眾以為是真實核准。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 213 | gate-three.chapter | 第三關：跑回歸 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 214 | gate-three.data.title | 測試要能抓到原本的錯 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 215 | v40084.text | 第三關，把修補放進另外寫的事後驗收。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 216 | v40085.text | 工具自己寫的測試有用，但不能是唯一標準。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 217 | gate-three-replay.data.title | 把同一份事後驗收放回舊碼 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 218 | gate-three-replay.data.steps[0].title | 重現 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 219 | gate-three-replay.data.steps[0].detail | 先抓到原來的錯 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 220 | gate-three-replay.data.steps[1].title | 舊碼 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 221 | gate-three-replay.data.steps[1].detail | 跑同一份事後驗收 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 222 | gate-three-replay.data.steps[2].title | 修補 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 223 | gate-three-replay.data.steps[2].detail | 再評估新修補 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 224 | v40086.text | 好的驗收測試，應該先在舊版程式重現這個錯誤。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 225 | v40087.text | 所以我先拿舊碼跑同一份事後驗收。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 226 | v40088.text | 理想順序是先讓驗收能重現舊錯，再評估新修補。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 227 | red-first.data.title | 先紅、再綠 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 228 | red-first.data.left.heading | 舊碼 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 229 | red-first.data.left.points[0] | 2 個舊測試通過 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 230 | red-first.data.left.points[1] | 事後 4 類只過 1 類 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 231 | red-first.data.right.heading | 修補 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 232 | red-first.data.right.points[0] | 修補測試 9 項通過 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 233 | red-first.data.right.points[1] | 事後 4 類全通過 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 234 | v40091.text | 舊碼雖然兩個原測試全過，事後四類只過一類。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 235 | v40092.text | 這證明新驗收能抓到我們要修的缺陷。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 236 | v40093.text | 換成修補後，四類事後驗收全通過。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 237 | v40094.text | 這才是比較有力的紅燈到綠燈證據。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 238 | v40095.text | 這一步能排除只檢查舊有整除案例的假安全感。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 239 | property.data.title | 不只測一組數字 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 240 | property.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 241 | property.data.code | for (let total = 0; total <= 500; total += 1) {<br>  for (let people = 1; people <= 20; people += 1) {<br>    const shares = splitFareCents(total, people);<br>    const sum = shares.reduce((a, b) => a + b, 0);<br>    assert.equal(sum, total);<br>    assert.ok(Math.max(...shares) - Math.min(...shares) <= 1);<br>  }<br>} | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 242 | property.data.caption | 驗收邏輯節錄（畫面改寫、省略長度檢查） | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 243 | v40098.text | 驗收不是只寫一百除三。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 244 | v40099.text | 我還把零到五百的總額，搭配一到二十人跑過。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 245 | property-part2.data.title | 不只測一組數字 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 246 | property-part2.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 247 | property-part2.data.code | for (let total = 0; total <= 500; total += 1) {<br>  for (let people = 1; people <= 20; people += 1) {<br>    const shares = splitFareCents(total, people);<br>    const sum = shares.reduce((a, b) => a + b, 0);<br>    assert.equal(sum, total);<br>    assert.ok(Math.max(...shares) - Math.min(...shares) <= 1);<br>  }<br>} | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 248 | property-part2.data.caption | 驗收邏輯節錄（畫面改寫、省略長度檢查） | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 249 | v40100.text | 每組都檢查總和，並確認最大差距不超過一分。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 250 | v40101.text | 這種性質檢查，能抓到你沒想到的餘數組合。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 251 | property-part3.data.title | 不只測一組數字 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 252 | property-part3.data.language | javascript | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 253 | property-part3.data.code | for (let total = 0; total <= 500; total += 1) {<br>  for (let people = 1; people <= 20; people += 1) {<br>    const shares = splitFareCents(total, people);<br>    const sum = shares.reduce((a, b) => a + b, 0);<br>    assert.equal(sum, total);<br>    assert.ok(Math.max(...shares) - Math.min(...shares) <= 1);<br>  }<br>} | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 254 | property-part3.data.caption | 驗收邏輯節錄（畫面改寫、省略長度檢查） | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 255 | v40102.text | 實際回圈涵蓋大量組合，但仍不是形式化證明。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 256 | v40103.text | 超出測試範圍的風險，要再根據業務補案例。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 257 | test-output.data.title | 事後驗收的實際輸出 | CONFIRMED | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 258 | test-output.data.image | docs/videos/ai-bug-fix-pr-review/demo/claude-acceptance.png | CONFIRMED | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 259 | test-output.data.caption | 同一示範的本地修補；原始輸出重排，4／4 通過 | CONFIRMED | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 260 | v4shot0.text | 這是同一份修補在本機跑出的驗收輸出。 | CONFIRMED | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 261 | v4shot1.text | 四項綠燈有紀錄，但還要對照需求與完整差異。 | CONFIRMED | E1/E3/E4; exact retained output and inspected reflow PNG; no historical provider attribution Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 262 | property-check.data.title | 性質測試逐組查三件事 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 263 | property-check.data.steps[0].title | 總額 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 264 | property-check.data.steps[0].detail | 各份額加總不變 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 265 | property-check.data.steps[1].title | 人數 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 266 | property-check.data.steps[1].detail | 輸出長度相同 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 267 | property-check.data.steps[2].title | 差距 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 268 | property-check.data.steps[2].detail | 最大與最小最多差一 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 269 | v4e5000.text | 回圈跑每組數字時，不只看總額。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 270 | v4e5001.text | 它還比對輸出長度，確認沒有漏掉任何人。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 271 | v4e5002.text | 再找最大和最小份額，差距不能超過一。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 272 | v4e5003.text | 這三個斷言對每組資料都成立，才算這關通過。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 273 | inputs-test.data.title | 再保護原本沒壞的地方 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 274 | inputs-test.data.items[0] | 零金額：每人零分 | CONFIRMED | Stored code/patch/tests and already-closed fresh round3 replay; current bytes and actual outputs verified. |
| 275 | inputs-test.data.items[1] | 總額非法輸入 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 276 | inputs-test.data.items[2] | 人數非法輸入 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 277 | inputs-test.data.items[3] | 原有輸入驗證要保留 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 278 | v40105.text | 零金額要回傳每人零分，不能拋出莫名錯誤。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 279 | v40106.text | 負數、小數或超大總額，仍然要被拒絕。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 280 | v40107.text | 零人、超過一百人和小數人數也是一樣。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 281 | v40108.text | 回歸的意思，就是修新 Bug 也守住舊契約。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 282 | v40109.text | 輸入驗證也可能在重寫時被無意刪掉。 | OUT OF SCOPE | Editorial possible omission risk; no relative frequency. Actual patch retains guards. |
| 283 | three-gates.chapter | 合併前的決定 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 284 | three-gates.data.title | 三道關缺一不可 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 285 | v40112.text | 把需求、程式差異和回歸測試一起看。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 286 | v40113.text | 需求契約告訴你什麼叫修好。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 287 | three-gates-evidence.data.title | 把證據放在一起 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 288 | three-gates-evidence.data.steps[0].title | 差異 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 289 | three-gates-evidence.data.steps[0].detail | 改了哪些檔與行 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 290 | three-gates-evidence.data.steps[1].title | 回歸 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 291 | three-gates-evidence.data.steps[1].detail | 在測試範圍內成立 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 292 | v40114.text | 差異讓你知道實際改了哪些檔、哪些行。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 293 | v40115.text | 回歸則證明新舊規則至少在測試範圍內成立。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 294 | v40116.text | 只缺一道關，審查紀錄就不完整。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 295 | review-summary.data.title | 準備合併時記下證據 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 296 | review-summary.data.steps[0].title | 需求 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 297 | review-summary.data.steps[0].detail | 總和、差額、順序、輸入 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 298 | review-summary.data.steps[1].title | 差異 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 299 | review-summary.data.steps[1].detail | 兩個預期檔案 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 300 | review-summary.data.steps[2].title | 測試 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 301 | review-summary.data.steps[2].detail | 舊碼紅、修補綠 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 302 | v40119.text | 我會在審查紀錄裡放三件事。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 303 | v40120.text | 第一，需求有哪些明確的驗收條件。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 304 | v40121.text | 第二，實際差異只改了哪些地方。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 305 | v40122.text | 第三，哪個測試先紅、修補後又如何變綠。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 306 | v40123.text | 這三項可以寫進 PR 描述，讓審查者快速重跑。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 307 | review-record.data.title | 交給審查者的最小證據 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 308 | review-record.data.items[0] | 失敗案例與需求 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 309 | review-record.data.items[1] | 完整差異 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 310 | review-record.data.items[2] | 重跑指令與測試結果 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 311 | v4e6000.text | 最後把那個原本失敗的案例寫在審查摘要裡。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 312 | v4e6001.text | 附上完整差異，不只貼兩行好看的核心程式。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 313 | v4e6002.text | 再列出重跑指令與通過的測試範圍。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 314 | v4e6003.text | 下一位審查者不必相信口頭報告，能自己驗證。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 315 | limits.data.title | 仍要人判斷的地方 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 316 | limits.data.items[0] | 需求本身正確嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 317 | limits.data.items[1] | 改動範圍完整嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 318 | limits.data.items[2] | 風險與回滾可接受嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 319 | limits.data.items[3] | 最後由負責者判斷 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 320 | v40126.text | 這個小型示範雖然通過驗收，仍不能代替真實業務判斷。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 321 | v40127.text | 需求若一開始寫錯，測試也可能跟著綠錯方向。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 322 | v40128.text | 還要有人看改動範圍、資料影響和回滾方式。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 323 | v40129.text | 負責合併的人，得對這個判斷負責。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 324 | v40130.text | 合併不是模型替團隊作的事，而是負責者作的決定。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 325 | github.data.kicker | 真實團隊流程 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 326 | github.data.text | 留下可追溯的審查 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 327 | github.data.sub | 看差異、留言、要求修改或核准 | CONFIRMED | E5; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 328 | v40133.text | 在 GitHub 的正式流程裡，審查者可以對變更行留言。 | CONFIRMED | E5; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 329 | v40134.text | 也可以要求修改，或在看過證據後核准。 | CONFIRMED | E5; https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 330 | github-evidence.data.title | 留下同一份證據 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 331 | github-evidence.data.items[0] | 示範不核准真實PR | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 332 | github-evidence.data.items[1] | 讓下一位審查者追溯 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 333 | github-evidence.data.items[2] | 不用別人的PR裝飾畫面 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 334 | v40135.text | 這裡不替任何真實 PR 點核准。 | CONFIRMED | E1/E3; exact local baseline/patch/test artifacts and independent private replay Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 335 | v40136.text | 重點是讓下一位審查者找到同一份證據。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 336 | v40137.text | 影片畫面展示規則，不會用別人的 PR 當裝飾。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 337 | outro.data.title | AI 修好 Bug，就能合併嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 338 | outro.data.cta | 拿三關清單檢查你的下一個修補 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 339 | outro.data.lines[0] | 需求契約 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 340 | outro.data.lines[1] | 實際差異 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 341 | outro.data.lines[2] | 回歸測試 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 342 | v40140.text | 回到開頭：AI 修好 Bug，測試綠了，能直接合併嗎？ | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 343 | v40141.text | 先過需求、差異、回歸這三道關，再由人作最後判斷。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 344 | outro-practice.data.title | 拿下一份修補試一次 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 345 | outro-practice.data.items[0] | 起始碼、修補、測試放在一起 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 346 | outro-practice.data.items[1] | 小修補先練三道關 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 347 | outro-practice.data.items[2] | 再用到較大改動 | OUT OF SCOPE | Editorial method, question, hypothetical scope, label or recommended practice; not measured vendor/product fact. |
| 348 | v40142.text | 這次的起始碼、修補和測試，要放在一起核對。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 349 | v40143.text | 拿你下一個小修補照著試一次，比背規則更有用。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |
| 350 | v40144.text | 這個小練習之後，再把同一方法用到較大的改動。 | OUT OF SCOPE | ED; brief and explicitly proposed three-gate editorial method Actual current value independently reread with artifact/context; inherited wording is not automatic acceptance. |


## 本輪限制與交接

- 本報告是目前文字 VERIFIED；完整350表不是部分抽樣或僅delta，57新增visible字詞亦已核對。
- 文中17881frames／596.033333秒／max13秒是候選當時以actual133clip lengths作的純函式預測；後續原生 refresh 及成片的實際時長、timeline／narration／checks 必須各自另有閉合收據。不能由這份文字報告宣告媒體重建已成功。
- Source拆場與reveal改变speechHash／場間隔。Linekeys與133原WAV全SHA同值可以復用；舊 aggregate／timeline／旁白／ASR stage／final approval不能自動當新稿current。
- Native plan47 groups不是provider呼叫數或整集費用。先前288 billable只是一輪continuation摘要，第一輪abort的總費用未知；本報告不補造費用。
- 原生首輪13flags及正在準備的真正第二轉寫由root正常流程處理；這份文字報告不改音訊、ASR cache、Jev分數、flags或owner核准。沒有把查核假疑點當錯音，也沒有音訊通過宣稱。
- 原私有候選報告保留未套用時的狀態與全部bytes；正式 source 已實際4608，但未完成的音訊／成片／player／owner驗收仍明確分開。
- 本輪没有provider、HTTP、模型／ASR、native CLI／stage呼叫、source／claims／i18n或媒體寫入；repo唯一變更為verify-4.md，私有closure另記source與輸出SHA。
