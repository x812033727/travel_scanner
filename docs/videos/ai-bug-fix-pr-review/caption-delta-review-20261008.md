# 四語字幕差異獨立覆核 — 2026-10-08

- 影片：`ai-bug-fix-pr-review`。
- 覆核人：`agent_offline_audio`；獨立於本輪 source 修正與四語 merge 的執行者。
- 範圍：五句來源修正 × 四語，合計 **20 條 delta 語意覆核**；另外對每語全部 **133 條**進行 ID、來源雜湊及完整 entry 保留檢查。其餘 128 條沒有在本輪重新逐語語意審閱。
- 結論：**20/20 語意 PASS，四語 133/133 source hash current，無 delta 語意 blocker**。這是 draft caption text 的覆核，不是 timed CC、配音／音訊 QA、owner 語言選擇或上架核准。
- 機械檢查時間：`2026-10-07T23:53:25.501Z`，本輪只讀 Node 程序實際 exit 0；讀取後再次驗證原／現來源及八份 locale bytes 的完整 SHA 相同。首次舊 pin 檢查因 source 從 `f6c2622c…` 改為 `cc5c51a7…` 而 exit 1，未用該結果宣告通過；本報告綁最終 `7cddf570…`。

## 檔案與版本綁定

`<repo>` 指此輪 managed checkout；`<private>` 指此輪操作證據目錄。這些代號不包含使用者主機路徑。

原始 bytes 來自 `<private>/source-repair/20261007T234441233150Z/`；snapshot receipt 完整 SHA256 為 `92e1a7e9eb5ed52d22e17208c06ffbf028ffb643528ed786b275e52d128051b7`（2634 bytes）。

| 檔案 | 原完整 SHA256 | 現完整 SHA256 | bytes 原 → 現 |
| --- | --- | --- | --- |
| video.json | `a17181e2c1058d0582d5968bc2fa143668f86ab5af4f424f5af18a4114a04741` | `7cddf570305b4afa8d87833aec8fac92ab3469648674fd6d17d085fd0dffe0d4` | 28843 → 28840 |
| en | `c0064fae6261ad39dea7fcad54a495717ade705486a63f701d02dc9b8c690aa0` | `c665271bc455acad57f27d727b1e34778c11973c4ee965d0dd372e276550d5cd` | 19187 → 19247 |
| ja | `7150aff3bd7ae19e15fbc36a6b5adf0631ef68a6ba38d0ca84a5985d5a6b7f17` | `7bfd43d8fc6c24aa6019d2e56200ee995e81f2c24c63de808eca680867674aa2` | 20599 → 20757 |
| ko | `184c08dea8662fc3b7aef22ae5a830e04988b1838f3fe1f9db31c0f74c0e8b17` | `7011243d495915a7e6e5fb6ed4a4aafd32f15c0500ff3708f5cc0e138589e4bd` | 21496 → 21597 |
| zh-CN | `00109871b89faec3a95b1aaa65d876b9baba8e2e8dce62bb15ef54e661ecd579` | `b65113db230c2bf87c478afe2f981aece3f59a31d6d98b595667d3a513cac688` | 18839 → 18854 |

現稿路徑為 `<repo>/docs/videos/ai-bug-fix-pr-review/video.json` 與 `i18n/{en,ja,ko,zh-CN}.json`。原稿有 28 場景、133 句；現稿仍是 28 場景、同序的 133 個唯一 ID。本表綁完整 source 檔案，包括本輪旁白、字卡及官方來源查核日期等修改；並不宣稱整份 source 僅有五個 JSON 欄位改動。

目前 `claims.md`：`a0e439c36cd833291827c993c64e2ecd8d495fc83228b950fa93c3e7b434c983`（3613 bytes）。它明示歷史 CLI 原始歸屬缺證，以及相對頻率主張已縮為可能發生的審查風險。

## 原生只讀 freshness 與保留檢查

只 import 既有模組的純函式；沒有呼叫 native CLI、寫入 translation hash 或執行 provider：

| 模組／函式 | 實際模組完整 SHA256 |
| --- | --- |
| `tools/video/core/schema.mjs`：`eachLine`、`textHash` | `d810ca82a8ef459faea23efa0afcbf1029d08521cb50c09e157bb19598ac172f` |
| `tools/video/core/translations.mjs`：`sourceHashes`、`metadataStatus`、`thumbnailStatus` | `92145323271592349e1a11d3ee4aafccc24c7ed418ed7ee331ec5b5bf49c86e4` |

每個 ID 均以原生 `textHash(line.text)` 與 locale `lines[id].source_hash` 比較，並確認翻譯文字存在；沒有手算或注入逐句 source hash。完整檔案 SHA256 是 bytes 識別，與原生 12 位 source hash 的用途分開。

| locale | ID coverage／唯一 | current caption hashes | exact changed entries | 未改完整 entries | metadata freshness | 縮圖文字 |
| --- | --- | --- | --- | --- | --- | --- |
| en | 133/133，無多缺 ID | 133/133 | 下列五句 | 128 | title、description、tags、6 chapters 均 current；0 orphan | missing，既有 |
| ja | 133/133，無多缺 ID | 133/133 | 下列五句 | 128 | 同上 | missing，既有 |
| ko | 133/133，無多缺 ID | 133/133 | 下列五句 | 128 | 同上 | missing，既有 |
| zh-CN | 133/133，無多缺 ID | 133/133 | 下列五句 | 128 | 同上 | missing，既有 |

四語實際變更集合都精確是 `v40017,v40021,v40022,v4e3002,v40109`；每個改動 entry 只有 `text` 與 `source_hash` 改變。以記憶體中的現稿副本，把五個 entry 換回 snapshot entry 後，**整份 locale JSON 與 snapshot deep-equal**。因此另外 128 個完整 entry、title、description、tags、chapters、thumbnail 欄位的存在／內容、全部 `source_hashes` 及其餘 metadata 均保持不變。此逆比對只在記憶體完成，沒有回寫檔案。

原生 metadata source hashes 為 title `60dfbe8e4887`、description `c8e4e57628d7`、tags `02ae8ee95e1b`；chapters：opening `405e76fd08bc`、why-green `9a325a577386`、gate-one `b13802d92b87`、gate-two `718420424dc5`、gate-three `6afcb2caf84a`、three-gates `4147b69644f1`。四語沒有各自 thumbnail 文字及 thumbnail source hash；此既有 optional 缺口未被補造。

## 五句來源差異

| ID | snapshot 來源 | 現來源 | 原生 current source hash |
| --- | --- | --- | --- |
| v40017 | 接下來看 AI 真正交出的修補。 | 接下來看一份可以重跑的本地修補。 | `edba64b1db7d` |
| v40021 | 我用自己寫的分攤函式，讓 Claude Code 依照題目修改。 | 這份本地分攤範例，留下了程式和測試的完整差異。 | `d72eea6dcdf1` |
| v40022 | 它改了程式和測試，工具自寫九個測試都通過。 | 修補後的九個測試重跑全過，稍後再做事後驗收。 | `05bf5c03119c` |
| v4e3002 | 在函式裡，AI 把平均四捨五入換成基本分與餘數。 | 這份修補把平均四捨五入，換成基本分與餘數。 | `b7100231e2ac` |
| v40109 | 尤其輸入驗證最容易在重寫時被無意刪掉。 | 輸入驗證也可能在重寫時被無意刪掉。 | `6161cda31b6f` |

## 20 條逐項語意判定

| ID | locale | 現來源 | 實際現翻譯 | 判定 | notes |
| --- | --- | --- | --- | --- | --- |
| v40017 | en | 接下來看一份可以重跑的本地修補。 | Next, let us look at a local patch we can rerun. | PASS | local、rerun 與本地可重跑一致，未保留 AI 提交歸因。 |
| v40017 | ja | 接下來看一份可以重跑的本地修補。 | 次は、再実行できるローカルの修正を見ます。 | PASS | ローカル／再実行 保留範圍及可重跑性，語句自然。 |
| v40017 | ko | 接下來看一份可以重跑的本地修補。 | 다음은 다시 실행할 수 있는 로컬 수정안을 보겠습니다. | PASS | 로컬 수정안／다시 실행 保留本地修補與重跑，沒有工具作者宣稱。 |
| v40017 | zh-CN | 接下來看一份可以重跑的本地修補。 | 接下来看一份可以重跑的本地修补。 | PASS | 保留本地與可重跑；修補不再歸因 AI。 |
| v40021 | en | 這份本地分攤範例，留下了程式和測試的完整差異。 | This local bill-splitting example retains the complete diff of the code and tests. | PASS | bill-splitting 符合分攤情境；code and tests／complete diff 兩類完整差異均保留。 |
| v40021 | ja | 這份本地分攤範例，留下了程式和測試的完整差異。 | このローカルの分配例には、コードとテストの完全な差分が残っています。 | PASS | 分配例、コードとテスト、完全な差分 齊全；沒有 Claude 作者聲明。 |
| v40021 | ko | 這份本地分攤範例，留下了程式和測試的完整差異。 | 이 로컬 분배 예제에는 코드와 테스트의 전체 변경 내용이 남아 있습니다. | PASS | 분배 예제 與上下文分攤一致；程式及測試的完整變更均保留。 |
| v40021 | zh-CN | 這份本地分攤範例，留下了程式和測試的完整差異。 | 这份本地分摊示例，保留了程序和测试的完整差异。 | PASS | 本地分攤範例與程式、測試的完整差異均保留。 |
| v40022 | en | 修補後的九個測試重跑全過，稍後再做事後驗收。 | All nine tests passed again after the patch. We will run the post-hoc acceptance tests later. | PASS | nine／passed again 明確保留 9 項重跑；later／post-hoc 區別後續事後驗收。 |
| v40022 | ja | 修補後的九個測試重跑全過，稍後再做事後驗收。 | 修正後の九つのテストは再実行ですべて通りました。後ほど事後の受け入れテストを行います。 | PASS | 九つ／再実行／後ほど／事後 保留數量、重跑與後續驗收順序。 |
| v40022 | ko | 修補後的九個測試重跑全過，稍後再做事後驗收。 | 수정 후 아홉 개 테스트를 다시 실행해 모두 통과했습니다. 잠시 후 사후 인수 테스트도 실행합니다. | PASS | 아홉 개／다시 실행／잠시 후／사후 保留 9 項與後續事後驗收；並非預先盲測。 |
| v40022 | zh-CN | 修補後的九個測試重跑全過，稍後再做事後驗收。 | 修补后的九个测试重跑全过，稍后再做事后验收。 | PASS | 九項重跑全過與稍後事後驗收分開；沒有『工具自寫』歸因。 |
| v4e3002 | en | 這份修補把平均四捨五入，換成基本分與餘數。 | This patch replaces rounding the average with a base share and a remainder. | PASS | rounding the average → base share and remainder 與保留 patch 演算法相符。 |
| v4e3002 | ja | 這份修補把平均四捨五入，換成基本分與餘數。 | この修正では、平均の四捨五入を基本の配分額と余りの計算に置き換えています。 | PASS | 平均の四捨五入 → 基本の配分額と余り 相符；置き換え指此修補，未指 AI。 |
| v4e3002 | ko | 這份修補把平均四捨五入，換成基本分與餘數。 | 이 수정안은 평균을 반올림하는 방식 대신 기본 몫과 나머지를 계산합니다. | PASS | 平均四捨五入改用基本 몫／나머지，與實際 base、remainder 相符。 |
| v4e3002 | zh-CN | 這份修補把平均四捨五入，換成基本分與餘數。 | 这份修补把平均四舍五入，换成基本份额与余数。 | PASS | 基本份額及餘數正確，沒有把餘數等同再次四捨五入。 |
| v40109 | en | 輸入驗證也可能在重寫時被無意刪掉。 | Input validation may also be accidentally removed during a rewrite. | PASS | may also／accidentally／during a rewrite 保留可能性與非故意，刪除頻率比較。 |
| v40109 | ja | 輸入驗證也可能在重寫時被無意刪掉。 | 入力検証も、書き直す際に誤って削除されることがあります。 | PASS | ことがあります／誤って 保留可能發生的風險，不宣稱最容易或本次實際刪除。 |
| v40109 | ko | 輸入驗證也可能在重寫時被無意刪掉。 | 입력 검증도 코드를 다시 작성할 때 실수로 삭제될 수 있습니다. | PASS | 될 수 있습니다／실수로 保留可能性、非故意與重寫情境，沒有相對頻率。 |
| v40109 | zh-CN | 輸入驗證也可能在重寫時被無意刪掉。 | 输入验证也可能在重写时被无意删掉。 | PASS | 可能／無意／重寫 保留；沒有『尤其容易』的相對頻率主張。 |

`v40022` 的「九個」指修補後 `fare.test.mjs` 裡的九項測試，與稍後四項事後驗收分開；本輪實際 replay 是 9+4=13/13，不能把九項翻譯改成十三項。事後驗收是在保留修補之後建立，不能稱為預先規劃的盲測。各語未增加作者、已合併 PR 或正式站事故聲明。

`v40109` 描述可能發生的審查風險，沒有相對頻率或此次刪除事實主張；保留的 patch 實際仍含原輸入 guards。四語均保留此可能性，不暗示本例 guards 已被刪。

## Metadata 的教學情境範圍

現 source 題名「AI 修好 Bug 就能合併？三個 PR 檢查點」與縮圖「AI 修補審查」提出教學情境。四語 description 都說明這是本地可重跑例子、不是正式站事故或已合併 PR，沒有指稱此次 patch 的工具作者。現 metadata 未出現 Claude 作者歸因。

既有 en title 是「AI Fixed the Bug. Can You Merge? Three PR Review Gates」：首句為陳述式，應連同後續疑問及 description 的本地教學範圍理解；它不是此次 patch 確由 AI 產生的 provenance。ja／ko／zh-CN 題名也保留 AI 修補後是否可合併的教學問句。本輪只讀取 metadata 的範圍與歸因表述，沒有重寫或宣告所有既有 metadata 已重新逐語完整送審。

## 可驗證來源清單及適用範圍

本輪沒有重新抓網頁、重新跑 demo 或呼叫付費模型。以下是已存在且這次實際讀取並驗證 bytes SHA 的證據。

### 本地保留 patch 與實際 replay

- `<repo>/docs/videos/ai-bug-fix-pr-review/demo/claude.patch`：`3d793faef18e5508fe7825d57158a24a60c1c18c62c0ed75672ac2b99ca1db1a`（2738 bytes）。
- 起點 `fare.mjs`：`53a822df2b194a252cff62e52b2a0d7418d593537d54b13e054cb794eafc4665`（424 bytes）；`fare.test.mjs`：`3ec607b3f151af05ed49d4f2b5597e9bd5ff15c043794aa08d39083092a3ca19`（322 bytes）；事後 `acceptance.test.mjs`：`236c499487e47419157ee7d35bf443ccd95859fa95e0b07cbc6ae3e79302a1ba`（1115 bytes）。
- `<private>/independent-verify/demo-replay-20261007T233114391508Z-5b7d5205-106d-4a4f-a68b-123c9dbb53e6/receipt.json`：`e601250c60d5e1df02effb9f19fccfb2a1f59e87578e181d01bc9a42c7cfe516`（23815 bytes）。實際 2026-10-07 23:31 UTC 閉合：起點 2/2 exit 0，起點驗收 1/4 exit 1，套 patch exit 0，修補後 13/13 exit 0。
- 同目錄 `patched-thirteen-tests.stdout.txt`：`ed88c9e8aca41975fa97424a81d06735a9b1760d984b210940b9bb9cbf61ca93`（758 bytes）；`patched-samples.stdout.txt`：`4ffc88928323a8ccaeb311dda86ec45d6d7cbe9a22b40680dc1a5cd6be2ef2a0`（94 bytes）。

replay 收據綁當時原 source `a17181e2…`；本輪比對現存 demo 輸入與收據 SHA 相同，因此可以支持本輪字幕的保留修補行為。不是宣稱已重新合成／驗收整支新版影片。patch 實際把 `Math.round(totalCents / people)` 改成 `Math.floor` 基本份額及整數餘數；樣本 `100/3 → [34,33,33]`、`2/3 → [1,1,0]`。它修改程式及測試兩個檔案；資料及 replay 證明結果，**檔名 claude.patch、歷史 comparison.md、重排輸出截圖都不能單獨證明 Claude 或 AI 作者歸屬**。原始歷史 CLI 命令、JSON、exit provenance 未找到，此缺口保留。

### 兩份官方 HTTP 200 metadata／審查參考

保存目錄：`<private>/independent-verify/official-sources-20261008-11fe7b04-8a93-4f91-b123-5d2e7a7e390c/`。兩份收據都是實際 HTTP 200、0 redirects；UTC 日期為 2026-10-07，台灣查核日期為 2026-10-08，與現 source `checked_on` 一致。

| 來源 | 實際 HTTP 200 觀察時間 UTC | raw body bytes／完整 SHA256 | response receipt 完整 SHA256 | scope |
| --- | --- | --- | --- | --- |
| [GitHub PR review quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) | 2026-10-07T23:27:59.8780648+00:00 | 135493／`eb717cc3208ff89ee55fbd6dd8902b7040708b2a2b81956269ca3af53af82ec2` | `926a63c8c7f288fc14e8eca71b2beb27378d5e9b409d0f33cea420a5fc86b7de` | 支援對差異留言、要求修改或核准。三關方法是本片編輯建議；官方文件不證明示例已合併／已上線。 |
| [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) | 2026-10-07T23:28:00.6654476+00:00 | 539070／`3fc10d61d4b7f2bda629691065750698e0671839012c0ff01365ce722b6e979e` | `2391400f33b5f19240fd6ae87b14c01cb83ddd107cc6d9da09570931873365d3` | 支援目前 CLI 的 print／JSON／permission 選項說明；不證明 9/27 原始 CLI 呼叫、工具作者或費用。 |

檔案為 `github-review-quickstart.hop-00.body`、`github-review-quickstart.response.json` 及 `claude-cli-reference.hop-00.body`、`claude-cli-reference.response.json`。解析文字 SHA 分別為 `639fcfdcb92ccbf13b4e9958daa88abb4dc09b65d906a15b68f50a7382d91ee1` 與 `d594649a9b9bc6dccbd73396e1f4834eb226d5164a262a052302914af65508b0`。官方頁面是定義／流程參考，沒有把本地實際結果外包成官方證實。

## 完整 ID coverage

以下為原生 `eachLine` 讀出的現 source 次序；原 snapshot 同序，四語 key set 精確等於這 133 個唯一 ID：

```text
v40000 v40001 v40002 v40003 v40007 v40008 v40009 v40010 v40011 v4e1000 v4e1001 v4e1002
v4e1003 v40014 v40015 v40016 v40017 v40018 v40021 v40022 v40023 v40024 v40025 v40028
v40029 v40030 v40031 v40032 v40035 v40036 v40037 v40038 v40039 v40040 v4e2000 v4e2001
v4e2002 v4e2003 v40042 v40043 v40044 v40045 v40046 v40049 v40050 v40051 v40052 v40053
v40056 v40057 v40058 v40059 v40060 v40063 v40064 v40065 v40066 v40067 v4e3000 v4e3001
v4e3002 v4e3003 v40070 v40071 v40072 v40073 v40074 v40075 v4e4000 v4e4001 v4e4002 v4e4003
v40077 v40078 v40079 v40080 v40081 v40084 v40085 v40086 v40087 v40088 v40091 v40092
v40093 v40094 v40095 v40098 v40099 v40100 v40101 v40102 v40103 v4shot0 v4shot1 v4e5000
v4e5001 v4e5002 v4e5003 v40105 v40106 v40107 v40108 v40109 v40112 v40113 v40114 v40115
v40116 v40119 v40120 v40121 v40122 v40123 v4e6000 v4e6001 v4e6002 v4e6003 v40126 v40127
v40128 v40129 v40130 v40133 v40134 v40135 v40136 v40137 v40140 v40141 v40142 v40143
v40144
```

## 交接限制與剩餘缺口

- 本輪接受範圍是 20 條 draft caption delta；全 133 條 hash current 只是機械來源匹配，不代表另外 128 條本輪已逐語重審。
- 四語 metadata bytes 保留、原生 freshness current；四語 localized thumbnail 文字仍 missing。沒有補造 owner 的 selected languages。
- 遠端未選語言的狀態是 root 本輪既有讀取背景，這份 caption review 沒有再呼叫遠端 API；本地四語草稿存在不等於 owner 選取、匯入或核准。
- 此輪未執行 provider、native stage、ASR、配音、render、timed CC、upload 或 publish；沒有新增付費。舊成片與音訊收據的有限搜尋缺口仍存在，不能以本報告推定從未付費，亦不能宣告目前媒體包已完成。
