# 四语字幕与 metadata 当前完整审核：AI 修好 Bug 就能合并？三个 PR 检查点

查核日：2026-10-08，Asia/Taipei；当前补充覆核 reviewer：caption_final_peer，独立于缩句提案者及翻译作者。

**结果：READY CURRENT FULL584 DRAFT WITH NATIVE TIMED CC CHECK，584 个节点（532字幕、52metadata）PASS，0未解修正。** 当前范围是583项保留上轮完整584审核PASS且精确不变，1项ja/v4e3002缩句新独立语意重读；实际五语字幕纯原生技术检查全0 problems。这不是正式语言核准、owner播放验收或发布。

上轮完整584 closure已在6个实质修正后完成；其中578语意PASS来自同日fresh second review的全稿独立覆核，6项由caption_final_peer独立重读。该完整584报告和原fresh审查物件保持不可变。本次没有重新语意审读583个未动节点，而是逐条核对原文／译文、全object和full-file hashes精确保留。

上游fresh reviewers：en/zh-CN = finish_blind_secondary；ja = finish_blind_secondary/fresh_ja_review；ko = finish_blind_secondary/fresh_ko_review。各 reviewer独立于该轮24处先前修正的作者／提案者。
当前 supplement开始UTC：2026-10-08T04:17:28.127700+00:00；完成UTC：2026-10-08T04:17:31.532174+00:00。


## 目前完整版本與 native freshness

| 檔案 | bytes | 完整 SHA256 | 範圍 |
| --- | ---: | --- | --- |
| `<repo>/docs/videos/ai-bug-fix-pr-review/video.json` | 39172 | `4608bffb664b8d5a99667daae019184750b73fdaefe32256b08c0494f88c6cca` | 繁中来源：133 句／47 場 |
| `<repo>/docs/videos/ai-bug-fix-pr-review/claims.md` | 4553 | `8173695736493aa0f44e544d56354d898009c659d0180cf21dc8e3210c5eb809` | 主张与证据范围 |
| `<repo>/docs/videos/ai-bug-fix-pr-review/verify-4.md` | 107607 | `255a7b05fa89c8785b52e71fbd26e6060f7ec2352b3b990b77e04cd65d781a9d` | 350 繁中来源 leaf 完整事实覆核；不是当前外语译文版本 |
| `<repo>/docs/videos/ai-bug-fix-pr-review/i18n/en.json` | 19245 | `27a9932e3fed585cb1277843acc9e2a4630fbf906436b27dbb622fd688b97770` | 133 字幕＋13 metadata，native source hashes current |
| `<repo>/docs/videos/ai-bug-fix-pr-review/i18n/ja.json` | 21011 | `b3a8bda7c75920ecb3d24198a33cae0a083dfb58cd891a61f0678edc7f0db65d` | 133 字幕＋13 metadata，native source hashes current |
| `<repo>/docs/videos/ai-bug-fix-pr-review/i18n/ko.json` | 21829 | `5f5c909bce1f1c48c32aa51fc456c7d2b0bfd1a66fe1a36b31ca839bba52812a` | 133 字幕＋13 metadata，native source hashes current |
| `<repo>/docs/videos/ai-bug-fix-pr-review/i18n/zh-CN.json` | 18854 | `b65113db230c2bf87c478afe2f981aece3f59a31d6d98b595667d3a513cac688` | 133 字幕＋13 metadata，native source hashes current |

原生純函式读取结果：validateVideo 0 errors；四语各 133 个 source_hash 有效，合计 **532/532 current**；title、description、ordered tags 与 6 chapter source_hashes 全部 current，无 orphan ID 或 chapter。buildSheet/mergeSheet 的全 object roundtrip 深等、0 problems；没有写入翻译文件、运行制作 CLI、重新产生媒体或发出请求。
每语 metadata 13 项：1 title、1 description、5 ordered tags、6 chapter titles。四语完整檔、繁中來源、claims、verify4、lexicon 与证据入口在本覆核前后全 SHA/bytes CAS 一致。Native six-repair CLOSED0 的修复前全文与 fresh-review frozen snapshot bytes 精确相同；回退已授权 6 个 text 值后全 object 深等，其他 578 节点及所有 source-hash fields 保留。
英文标题实际原生 codepoint 长度为 55，低于 100，且无 angle brackets。先前私有 peer note 手写为52的附带字数已在新私有 closure 更正；旧证据不改，草稿文本没改。

## 可验证官方来源与取得时间

这次读取与核对已保存的 HTTP raw body、headers、visible text 完整 bytes/hash；没有重新请求官网，也没有把保存状态写成新的 HTTP 观察。UTC 取得时间对应 2026-10-08 台北日。

### github-review

- Source title：GitHub pull request review quickstart。
- URL：[https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart)。
- Final URL：[https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart)。
- 保存 HTTP status：200；observed UTC：2026-10-07T23:48:59.994139+00:00；source checked_on：2026-10-08。
- `<private>/independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1/github-review.body`：135493 bytes；完整 SHA256 `eb717cc3208ff89ee55fbd6dd8902b7040708b2a2b81956269ca3af53af82ec2`；本次重验匹配。
- `<private>/independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1/github-review.headers`：1775 bytes；完整 SHA256 `079dd2e01695aadec41910b7b25a4352931f56a6a0f0980a9c08cf6b4fccc52a`；本次重验匹配。
- `<private>/independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1/github-review.visible-text.txt`：4051 bytes；完整 SHA256 `e9561c377f094c0f21a3df582a65d556c96b04ecfbaa78b7e01f36bee4d55200`；本次重验匹配。

GitHub 文档用于变更行评论、要求修改、核准等审查机制；Claude CLI 文档只用于工具背景，不证明保留 patch 的历史作者、CLI 命令、结果 JSON、退出码或费用。

### claude-cli

- Source title：Claude Code CLI reference。
- URL：[https://code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference)。
- Final URL：[https://code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference)。
- 保存 HTTP status：200；observed UTC：2026-10-07T23:49:01.108852+00:00；source checked_on：2026-10-08。
- `<private>/independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1/claude-cli.body`：539027 bytes；完整 SHA256 `918f104b0dd820eb969918624984175941b8bc2992abf2a66080bba51115a15a`；本次重验匹配。
- `<private>/independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1/claude-cli.headers`：2689 bytes；完整 SHA256 `fdf976d985ea6cdc165b72498872883c412b808f044d9509cbb33ea31b33fa61`；本次重验匹配。
- `<private>/independent-verify/fresh-round3-20261007T234850429195Z-64f9b074-0fdd-4d05-8bae-7f4882e725f1/claude-cli.visible-text.txt`：39844 bytes；完整 SHA256 `db92da1399e695d3a051eb70a46290fd391abe4a21c197582096aeb54d7fbc65`；本次重验匹配。

GitHub 文档用于变更行评论、要求修改、核准等审查机制；Claude CLI 文档只用于工具背景，不证明保留 patch 的历史作者、CLI 命令、结果 JSON、退出码或费用。

## 本地示例与其他来源全文 pins

| logical source | bytes | full SHA256 |
| --- | ---: | --- |
| `<repo>/docs/videos/ai-bug-fix-pr-review/demo/fare.mjs` | 424 | `53a822df2b194a252cff62e52b2a0d7418d593537d54b13e054cb794eafc4665` |
| `<repo>/docs/videos/ai-bug-fix-pr-review/demo/fare.test.mjs` | 322 | `3ec607b3f151af05ed49d4f2b5597e9bd5ff15c043794aa08d39083092a3ca19` |
| `<repo>/docs/videos/ai-bug-fix-pr-review/demo/acceptance.test.mjs` | 1115 | `236c499487e47419157ee7d35bf443ccd95859fa95e0b07cbc6ae3e79302a1ba` |
| `<repo>/docs/videos/ai-bug-fix-pr-review/demo/claude.patch` | 2738 | `3d793faef18e5508fe7825d57158a24a60c1c18c62c0ed75672ac2b99ca1db1a` |
| `<repo>/docs/videos/ai-bug-fix-pr-review/demo/claude-acceptance-output.txt` | 355 | `a74c7a10e44941233f10f52b22477c8f2be317d4a06b566f93e3be0c8bfbba1e` |
| `<repo>/docs/videos/ai-bug-fix-pr-review/demo/claude-acceptance.png` | 45733 | `a0ab2d33e04606260f4c1a118013826a94f09db68c816b53527407bce699427a` |
| `<repo>/docs/videos/ai-coding-tools-same-task/demo/CHALLENGE.md` | 475 | `80a2ad6b1f3dd7bc6f6e819bc87007e21b2570ee53a683ece0b508b77895655a` |
| `<repo>/docs/videos/ai-bug-fix-pr-review/brief.md` | 2226 | `511afa8537ca1807ccc84aa25019e0a055349ba1168bcf9f8dd73f2738d749c4` |
| `<repo>/docs/videos/lexicon.json` | 3406 | `862d277aaf4359e9e07b5f3281f59eabb240f5ea3227c174f692cf2d0237f675` |

这些示例属于本地可重跑分摊案例。实际 replay 证据由 verify-3/verify-4 和保存 stdout/stderr 支持：旧原两测试2/2成功，旧事后验收1/4成功且预期exit1，保留修补原测试9/9与事后4/4共13/13。性质测试覆盖10020组合，不是全safe integer形式化证明。本次只读代码、patch和保存证据，没有重新运行测试。claude-acceptance.png是保存输出重排，不是原终端截图。文件名和通过的测试均不证明历史AI/Claude作者；需求、diff、回归三关是本片编辑方法。

## 审核收据与保留范围

| evidence | bytes | full SHA256 |
| --- | ---: | --- |
| `<private>/private-language-review/fresh-second-review-2026-10-08T031301567Z-979bec98-b98b-455f-8845-ae6638646616/all-four-fresh-second-review.json` (fresh complete second review) | 414859 | `efc81e440d28497a36e77f62a2a844e024bace48aa6aab7f69d21400d1573c4b` |
| `<private>/private-language-review/fresh-second-review-2026-10-08T031301567Z-979bec98-b98b-455f-8845-ae6638646616/required-fixes.json` (required six fixes) | 7099 | `2ee089c62d2d94f795f2faa5c456fc1d53c4518027fd7d64d770c6ad6ff86fc2` |
| `<private>/private-language-review/native-repair2-2026-10-08T03-29-50-921Z-29018d46-5f86-4934-830b-d89ba3131457/receipt.json` (native exact six repair CLOSED0) | 25978 | `c601285665e45cf76ddbe3143aa3638061bcb7e9780e65ab2fffc663bb82d4ed` |

正式 owner GET 保存 HTTP200于 2026-10-08T03:59:06.475Z；response 15165B SHA256 `6ade85c56ca08dd9a7df09b9b662545428b3f40690dcbf8f4587a1b1b4ffd890`。owner decided_at=2026-10-08T03:46:07.866448Z，en/ja/ko/zh-CN 的 metadata、captions 全true，dub 全false；local languages.json fullSHA256 `5ee5e220b6dc659d7062cc3695e76e6c4492478fd5bb69c0a605ec0c5d5c1d96`。本 reviewer 只核对已选择的部件，没有写入选择或核准。实际五语 SRT/VTT 已经原生重产，纯函数逐bytes核对与native checkCues全0 problems；这只表示字幕技术检查，不是配音听感、owner Studio/playback接受或发布。四语仍缺可选thumbnail words，原生保留本片繁中缩图；不冒充外语缩图验收。

下表现在保留583个原full584 PASS的精确相同 source/translation 与判定来源；仅ja/v4e3002为本次新重读CPS缩句，原full584与此前fresh review保留不动。所有行当前文本直接来自上述完整source/draft hashes。


## 日文阅读速度修正与当前 closure

本次 supplement 完成UTC：2026-10-08T04:17:31.532174+00:00。当前584条仍为PASS，范围 **583 原full584语意PASS精确保留＋1新独立语意重读**。前述6处属于上轮完整584 closure的历史审核，本轮未冒称重读其余583条。

ja/v4e3002：この修正では、平均の四捨五入を基本の配分額と余りの計算に置き換えています。 → この修正では、平均の四捨五入を基本の配分額と余りに置き換えます。。37→32 codepoints；去除的「計算」不是繁中原文独立条件。原文平均四舍五入换成基本分与余数、邻句输入guard保留及本地diff范围都不变。native captions-only worksheet/merge CLOSED0，只改此一个text值；反向替回后JA全object与原0b264完整档深等。

在同一原生 presentation timeline 重建旧JA，可重现 `cue 65 (v4e3002): 8.4 characters a second, above 8`；新实际JA/SRT/VTT与纯原生serialization逐bytes相等，全部五语0 reading/width/overlap problems。未调音速、未拉长line speech window、未修改主旁白/成片，不宣称听过外语声音。

| locale | actual cues | native problems | SRT full SHA256 | VTT full SHA256 |
| --- | ---: | ---: | --- | --- |
| zh-TW | 133 | 0 | `cf6f0a76af69e8fb2170a696165bc52cb18df74c303b7e2c0b69d96d20b97944` | `65e0b6b4381eee00f3b7a34a61096f2b584da2fd6a2734728f7648da9f3e1351` |
| en | 134 | 0 | `354cac5870b44931794a1dbccc4fb975f2bc1c326db0ac7c84077e1f4077e8bc` | `ecffdba2bfe2a41c4819b1a4da4a5a5e7dc4dae1971f7cdf7551c753a9c228a4` |
| ja | 139 | 0 | `17e3a94f568928d6be850f5d0b9c15a3a9e0531d7089e4a2cfb2288268c6b43e` | `bafc50a1f0c1b47aeeed9db10dccef843cc51379c6e91eb819be66cc43f3f3ca` |
| ko | 160 | 0 | `53410115f147b3c60b52aa6ddf773ec70b6abae01403fa3fc610d44fb09f34a1` | `848b7c09b7dac2793f790ea03c461e934b05fcd913fbce068b4590af32a738b4` |
| zh-CN | 133 | 0 | `4adb2f25a6f83f4b4cd83802c126cd2e2e28daa4d91ff0555db19c18d8133db2` | `27a381b4255eb4cd04452f494a31e046fa6df7df1bea95fdc54c63cb9c4186c3` |

- 旧完整584 private report：`4cee2c8b671bae11757e8dfbff5d95ab2d0a6f699fd6a9a5e4e0a9c3ab10a84d`，保存不改。
- 独立语意proposal：`b19235b3380333b4e1f4743a2221c0661d30ad37cb609295eec5fe0906479f35`。
- 本次native one-node repair CLOSED0 receipt：`f6cce2e8418ae9ed881ca0ba2a480bec34cad1380fa4870923aeee9aa26faf74`。
- 本次actual recaptions CLOSED0 receipt：`e2c17fbcb8b54f0d8cb7ea52fb8b6f0fa4a31ef26e0ee0a19ab71f8b83003aee`。
- 本次完整current584 private closure：`3ab79e9bf21ab81e129aa6097647d60eba182fb86a6022243fe8ffe36b09639e`。

## 完整 584 项当前逐节点审查表

| locale | id | kind | 繁中原文 | 当前译文 | 结果 | 判定范围 | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| en | v40000 | caption | 三個人分一百分，舊測試全綠，結果卻只分出九十九。 | Three people split 100 cents. Old tests passed, but the shares totaled 99. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100分/3人的99分實際缺額與舊測試通過均保留。 |
| en | v40001 | caption | AI 送來一份修補程式，你會直接合併嗎？ | AI sent a patch. Would you merge it right away? | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI送來修補後的合併提問保留，未新增特定工具作者。 |
| en | v40002 | caption | 我帶你看需求、差異與回歸，三道關都要過。 | We'll check requirements, diff, and regression. All three must pass. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求、差異、回歸三關及帶領檢查的敘述保留。 |
| en | v40003 | caption | 我們先從那一分為什麼消失開始。 | First, let us see how that one cent disappeared. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 一分缺額的因果引子保留，沒有更換幣別。 |
| en | v40007 | caption | 第一個舊測試，只檢查能整除的金額。 | The first old test only covered an evenly divisible amount. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一個舊測試只覆蓋可整除金額的範圍保留。 |
| en | v40008 | caption | 人數不合法也會擋，兩個結果都是綠色。 | The invalid count was also rejected. Both tests were green. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非法人數被擋及兩項舊測試綠燈均維持實際結果語氣。 |
| en | v40009 | caption | 不整除的路徑沒人問，所以錯誤藏得好好的。 | No test covered a remainder, so the bug stayed hidden. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 未涵蓋餘數路徑造成缺陷未被發現的因果保留。 |
| en | v40010 | caption | 這次示範是真正執行的檔案，不是想像案例。 | This demo uses files we actually ran, not an imagined example. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 實際執行本地檔案與想像案例的區別保留。 |
| en | v40011 | caption | 它證明程式照舊測試運作，沒有證明帳算對。 | It shows the code passed old tests, not that the accounting was right. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 通過舊測試不等於分帳正確的證據限制保留。 |
| en | v4e1000 | caption | 這是起始專案真的跑過的兩個測試。 | These are the two tests we actually ran on the starter project. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 起始專案真正執行兩項測試的時態与數量保留。 |
| en | v4e1001 | caption | 第一個測一百二十分，三人平均分。 | The first splits 120 cents equally among three people. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 120分/3人平均分的數字與操作順序保留。 |
| en | v4e1002 | caption | 第二個測零人時要拋出錯誤。 | The second expects an error for zero people. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 零人應拋錯的斷言條件保留。 |
| en | v4e1003 | caption | 它們全綠，只能證明這兩件事，不能代表餘數正確。 | Both pass, but neither tells us whether remainders are handled. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩项通過不能證實餘數處理正確的限制保留。 |
| en | v40014 | caption | 分一百分給三個人，原始程式回三個三十三。 | For 100 cents and three people, the starter returned 33, 33, and 33. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原程式100分/3人回33、33、33的實際結果保留。 |
| en | v40015 | caption | 這不是顯示格式的問題，總和真的少了一分。 | That is not a display issue; the total really is one cent short. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 缺一分是總和問題而非顯示問題的因果保留。 |
| en | v40016 | caption | 如果少掉的一分錢會記入帳務，就算測試全綠也不能合併。 | If the missing cent affects accounts, green tests still cannot justify a merge. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 帳務影響仍是如果條件，未說本例已有正式帳務事故。 |
| en | v40017 | caption | 接下來看一份可以重跑的本地修補。 | Next, let us look at a local patch we can rerun. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 接著看可重跑本地修補的轉場與範圍保留。 |
| en | v40018 | caption | 這個失敗結果已寫進可重跑的驗收檔案。 | The failure is captured in a repeatable acceptance test file. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 失敗案例已被收入可重跑驗收檔案的實際時態保留。 |
| en | v40021 | caption | 這份本地分攤範例，留下了程式和測試的完整差異。 | This local bill-splitting example retains the complete diff of the code and tests. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地分攤例保留程式與測試完整差異，未新增Claude作者歸因。 |
| en | v40022 | caption | 修補後的九個測試重跑全過，稍後再做事後驗收。 | All nine tests passed again after the patch. We will run the post-hoc acceptance tests later. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補後九項測試已通過、後續再做事後驗收的順序與時態保留。 |
| en | v40023 | caption | 這不是正式站的事故，也不是已合併的真實 PR。 | This was no production incident or real merged PR. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非正式站事故、非已合併真實PR的兩項限制保留。 |
| en | v40024 | caption | 它是可以公開重跑的一份本地修補案例。 | It is a local patch that anyone can rerun. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地修補可供重跑的含義保留，未聲稱已部署或合併。 |
| en | v40025 | caption | 所以它適合用來練審查，卻不能代表產品事故。 | It is useful for review practice, not evidence of a product incident. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 適合審查練習而不代表產品事故的範圍保留。 |
| en | v40028 | caption | 第一關，不要先看 AI 說它完成了什麼。 | Gate one: do not start with AI's completion message. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一關先不依賴AI完成訊息的編輯建議保留。 |
| en | v40029 | caption | 先把需求寫成你可以算得出來的條件。 | Write requirements as conditions you can calculate yourself. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求寫成可自行算出的條件的建議保留。 |
| en | v40030 | caption | 這題要保留輸入規則，不能只修一個範例。 | The fix must preserve input rules, not just repair one example. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 必須保留輸入規則、不可只修一例的契約保留。 |
| en | v40031 | caption | 也不能悄悄把分配規則改成另一種做法。 | It must not silently change how the shares are assigned. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不能偷偷更換分配规则的限制保留。 |
| en | v40032 | caption | 第一關的答案，應該能不靠工具自己口述。 | You should be able to state this first gate without the tool. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一關內容應能不用工具自行口述的意思保留。 |
| en | v40035 | caption | 第一條，結果長度要和人數一樣。 | First, the output length must equal the number of people. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 輸出長度等於人數的第一條件保留。 |
| en | v40036 | caption | 第二條，所有人的份額加總，必須等於原來金額。 | Second, all shares must add up to the original amount. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 份額總和等於原金额的第二條件保留。 |
| en | v40037 | caption | 第三條，任何兩人最多只差一分。 | Third, any two shares may differ by at most one cent. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 任意兩份額最多相差一分的上界保留。 |
| en | v40038 | caption | 第四條，有餘數時，前面的人先分到。 | Fourth, when cents remain, earlier people get them first. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 餘數先配給前方位置的順序規則保留。 |
| en | v40039 | caption | 四條放在一起，才描述完整的分攤行為。 | Together, those four rules define the full allocation. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四條合起來定義分攤行為的含義保留。 |
| en | v40040 | caption | 如果只補一百除三，還會漏掉其他金額。 | Fixing only 100 divided by three would miss other amounts. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只修100/3會漏其他金額的反事實風險保留。 |
| en | v4e2000 | caption | 只測一百分除三，還可能把規則寫死在特例上。 | Testing only 100 ÷ 3 may leave the rule hard-coded to that case. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只測100/3可能寫死特例的可能性語氣保留。 |
| en | v4e2001 | caption | 再代入兩分給三個人，正確是前兩位各一分。 | Try two cents among three people: the first two should get one each. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2分/3人前兩人各1分的需求值保留。 |
| en | v4e2002 | caption | 第三位拿零分，總和仍是兩分。 | The third gets zero, and the total remains two cents. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三人0分、總和仍2分的數字與順序保留。 |
| en | v4e2003 | caption | 這組資料會立刻露出四捨五入重複分配的問題。 | That case quickly exposes duplicate allocations caused by rounding. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四捨五入導致重複分配的因果關係保留。 |
| en | v40042 | caption | 還有原本就存在的輸入檢查。 | The starter also had input validation. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原有輸入檢查先前存在的含義保留。 |
| en | v40043 | caption | 總額不能是負數、小數或超過安全整數。 | The amount cannot be negative, fractional, or beyond a safe integer. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 拒絕負數、小數、超安全整數範圍三類金額保留。 |
| en | v40044 | caption | 人數只能是一到一百之間的安全整數。 | The count must be a safe integer from 1 through 100. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 人數為1至100的安全整數，上下界和整數性保留。 |
| en | v40045 | caption | 修補若刪掉這些檢查，就算範例變對也不能過關。 | A patch that removes those checks fails, even if this example works. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若刪檢查即使範例成功仍不得通過的條件保留。 |
| en | v40046 | caption | 它們不是額外加分題，而是修補前就有的規則。 | They are existing rules, not optional extra credit. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原有規則並非額外加分的意思保留。 |
| en | v40049 | caption | 把一百分除以三，理想結果是三十四、三十三、三十三。 | For 100 cents and three people, expect 34, 33, and 33. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100分/3人的34、33、33需求結果保留。 |
| en | v40050 | caption | 這組數字同時檢查總和與餘數順序。 | That checks both the total and the remainder order. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同時檢查總和與餘數順序的兩重目的保留。 |
| en | v40051 | caption | 只測每個人差不多，還是不夠。 | Checking only that each share is close is not enough. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只看份額接近仍不足的限制保留。 |
| en | v40052 | caption | 需求契約先寫清楚，才有審查的尺。 | Write the contract first to give the review a measuring stick. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先清楚寫需求契約才有審查準則的比喻保留。 |
| en | v40053 | caption | 換成兩分三人，正確順序也是一、一、零。 | For two cents and three people, the order is 1, 1, 0. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2分/3人的1、1、0順序保留。 |
| en | v40056 | caption | 第二關，打開實際差異，不只讀工具的完成訊息。 | Gate two: open the actual diff, not just the completion message. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二關打開實際差異而非只讀完成訊息的建議保留。 |
| en | v40057 | caption | 先確認它只改到預期的程式和測試。 | First, check that it changed only the expected code and tests. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 確認只有預期程式與測試改動的範圍保留。 |
| en | v40058 | caption | 接著把新增邏輯代入一百分除三的例子。 | Then trace 100 divided by three through the new logic. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 把100/3代入新邏輯的操作保留。 |
| en | v40059 | caption | 最後看它有沒有刪掉原來的保護條件。 | Finally, check that the original protections remain. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 最後確認原保護條件仍在的檢查目的保留。 |
| en | v40060 | caption | 文字摘要可能遺漏細節，差異本身才是檢查對象。 | A text summary can miss details. Review the diff itself. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 摘要可能漏細節、須檢查實際差異的可能性與因果保留。 |
| en | v40063 | caption | 這份修補先算每人最少要拿多少。 | This patch first computes the minimum share for each person. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補先求每人基本最低份額的算法意義保留。 |
| en | v40064 | caption | 再算剩下幾分，要補給幾位前面的人。 | Then it finds how many cents remain for earlier people. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 再計算餘數及前方補配位置的意義保留。 |
| en | v40065 | caption | 總額一百，分給三人，各拿三十三，還剩一分錢。 | Split 100 cents three ways: 33 each, with one cent left. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100分給3人各33分、剩1分的數字保留。 |
| en | v40066 | caption | 第一位多拿一分，其餘兩位維持三十三。 | The first gets one more; the others stay at 33. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人多1分、另兩人維持33的顺序保留。 |
| en | v40067 | caption | 用兩分三人再代一次，就能看到前兩位各多一分。 | Trace two cents among three people: the first two each get one cent. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2分給3人前兩人各獲1分的需求行為保留。 |
| en | v4e3000 | caption | 完整差異顯示，函式前兩段輸入檢查仍然保留。 | The full diff shows the function's first two input checks remain. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 完整差異中前兩段輸入檢查仍保留的實際描述保留。 |
| en | v4e3001 | caption | 非法金額和非法人數，仍會在分配前被擋。 | Invalid amounts and counts are still rejected before allocation. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非法金額和人數於分配前被擋的顺序保留。 |
| en | v4e3002 | caption | 這份修補把平均四捨五入，換成基本分與餘數。 | This patch replaces rounding the average with a base share and a remainder. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 平均四捨五入改成基本份額加餘數的算法差異保留。 |
| en | v4e3003 | caption | 這是這份本地差異的範圍，不替其他檔案背書。 | That is the scope of this local diff, not a claim about other files. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只代表這份本地差異、不為其他檔背書的範圍保留。 |
| en | v40070 | caption | 我在差異裡先找原有驗證，這次沒有被刪掉。 | I checked the original validations in the diff; they remain. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱確認原驗證未被刪除的實際結果保留。 |
| en | v40071 | caption | 再看檔案清單，只有程式和測試被修改。 | The file list shows only the code and tests changed. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 檔案清單只有程式與測試改動的實際範圍保留。 |
| en | v40072 | caption | 新增測試涵蓋不整除、零金額和非法輸入。 | New tests cover remainders, zero amount, and invalid inputs. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新增測試覆蓋不整除、零額、非法輸入三類保留。 |
| en | v40073 | caption | 這些都是看得見的證據，不是工具的口頭保證。 | That is visible evidence, not just the tool's word. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可見證據而非工具口頭保證的意思保留。 |
| en | v40074 | caption | 如果它順手改了部署或帳務設定，應該另外討論。 | If it also changed deployment or billing settings, discuss that separately. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 部署或帳務改動仍是如果條件，須另議而非宣稱本例發生。 |
| en | v40075 | caption | 新增測試也要看斷言，不只看測試名稱。 | Read test assertions, not just test names. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需讀斷言而非只看測試名稱的建議保留。 |
| en | v4e4000 | caption | 新增測試不能只看名字，要看它到底斷言什麼。 | For new tests, check exactly what their assertions verify. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新增測試需辨認實際斷言內容的意思保留。 |
| en | v4e4001 | caption | 這份修補測到一百分除三，是三十四、三十三、三十三。 | This patch tests that 100 split three ways yields 34, 33, 33. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補測試100/3得到34、33、33的實際斷言保留。 |
| en | v4e4002 | caption | 也測到兩分分五人，前兩位各一分，其餘拿零。 | It also tests two cents among five: 1, 1, then zeros. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補測試2分/5人前兩1分其餘0的實際斷言保留。 |
| en | v4e4003 | caption | 這兩組一起看，比只看測試數量更有意義。 | Those cases matter more than the raw count of tests. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩組具体案例比純數量更有證據力的編輯建議保留。 |
| en | v40077 | caption | 這裡展示的是本地修補，不是假裝已有人核准的 PR。 | This is a local patch, not a PR someone has already approved. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地修補非已有人核准的真實PR，未虛構正式核准。 |
| en | v40078 | caption | 真正的專案還要看相關模組、型別與維運影響。 | Real projects also need module, type, and operational review. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 真實專案應擴看模組、型別、維運三類影响保留。 |
| en | v40079 | caption | 如果這段程式連著付款系統，範圍會更大。 | The scope grows if this function connects to payments. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 連付款系統時才擴大範圍的條件保留。 |
| en | v40080 | caption | 影片示範的方法，可以帶進真正的審查流程。 | You can carry this demo method into real reviews. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 方法可帶入真實審查的編輯建議保留。 |
| en | v40081 | caption | 我把這個範圍明確標出，避免觀眾以為是真實核准。 | I label this scope clearly so no one mistakes it for real approval. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱標示範圍以免誤認核准的意圖保留。 |
| en | v40084 | caption | 第三關，把修補放進另外寫的事後驗收。 | Gate three: run the patch against a separate, later acceptance suite. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三關使用另外於事後寫成的驗收，未改稱事前盲測。 |
| en | v40085 | caption | 工具自己寫的測試有用，但不能是唯一標準。 | Tool-written tests help, but cannot be the only standard. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 工具自寫測試只能是部分標準，未歸因特定歷史工具。 |
| en | v40086 | caption | 好的驗收測試，應該先在舊版程式重現這個錯誤。 | A good acceptance test should first reproduce this bug in the old code. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 好的驗收應先在舊碼重現同一缺陷的建議順序保留。 |
| en | v40087 | caption | 所以我先拿舊碼跑同一份事後驗收。 | So I ran the same later acceptance suite against the old code first. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱已先用舊碼跑同一事後驗收的實際順序保留。 |
| en | v40088 | caption | 理想順序是先讓驗收能重現舊錯，再評估新修補。 | Ideally, first reproduce the old failure, then assess the new patch. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 理想先重現舊錯、再評估新修補的編輯建議保留。 |
| en | v40091 | caption | 舊碼雖然兩個原測試全過，事後四類只過一類。 | The old code passed both original tests but only one of four later groups. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 舊2/2通過、事後4類只過1類的對照數字保留。 |
| en | v40092 | caption | 這證明新驗收能抓到我們要修的缺陷。 | That shows the new suite catches the defect we meant to fix. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新驗收捕捉欲修缺陷的證據含義保留，未擴成完全正確。 |
| en | v40093 | caption | 換成修補後，四類事後驗收全通過。 | The patch then passed all four later acceptance groups. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補四類事後驗收全部通過的實際結果保留。 |
| en | v40094 | caption | 這才是比較有力的紅燈到綠燈證據。 | That is stronger red-to-green evidence. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 紅到綠證據比較有力的相對編輯判斷保留。 |
| en | v40095 | caption | 這一步能排除只檢查舊有整除案例的假安全感。 | It counters the false comfort of old exact-division tests. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 避免只看整除舊例造成假安心的目的保留。 |
| en | v40098 | caption | 驗收不是只寫一百除三。 | Acceptance covers more than 100 ÷ 3. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 驗收不僅是100/3单例的範圍保留。 |
| en | v40099 | caption | 我還把零到五百的總額，搭配一到二十人跑過。 | I also ran amounts from 0 to 500 with 1 to 20 people. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱已跑總額0至500、1至20人的范围保留。 |
| en | v40100 | caption | 每組都檢查總和，並確認最大差距不超過一分。 | Each case checks the total and a maximum gap of one cent. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 每組總和及最大差額不超1分的兩項斷言保留。 |
| en | v40101 | caption | 這種性質檢查，能抓到你沒想到的餘數組合。 | These property checks catch remainder combinations you may miss. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 性質檢查可抓未想到餘数组合的功能保留。 |
| en | v40102 | caption | 實際回圈涵蓋大量組合，但仍不是形式化證明。 | The loop covers many cases, but it is not a formal proof. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 大量組合仍不是形式化證明的限制保留。 |
| en | v40103 | caption | 超出測試範圍的風險，要再根據業務補案例。 | Add business-specific cases for risks beyond this test range. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 超出範圍風險需按業務補例的建議保留。 |
| en | v4shot0 | caption | 這是同一份修補在本機跑出的驗收輸出。 | This is local acceptance output from the same patch. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同一修補在本機實際執行的驗收輸出，未稱原始錄影或正式站。 |
| en | v4shot1 | caption | 四項綠燈有紀錄，但還要對照需求與完整差異。 | Four green groups are recorded, but still compare the full diff and contract. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四類绿灯有紀錄但仍需對照完整差異與需求的限制保留。 |
| en | v4e5000 | caption | 回圈跑每組數字時，不只看總額。 | For every case in the loop, I checked more than the total. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回圈逐组不只看總額的檢查範圍保留。 |
| en | v4e5001 | caption | 它還比對輸出長度，確認沒有漏掉任何人。 | It also checks output length so nobody is omitted. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 檢查輸出長度以避免漏人的目的保留。 |
| en | v4e5002 | caption | 再找最大和最小份額，差距不能超過一。 | It compares largest and smallest shares; the gap must be at most one. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 最大与最小份额差距不超1，維持分攤單位与上界。 |
| en | v4e5003 | caption | 這三個斷言對每組資料都成立，才算這關通過。 | All three assertions must hold for each case to pass this gate. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 每組三項斷言都成立才過关的全稱條件保留。 |
| en | v40105 | caption | 零金額要回傳每人零分，不能拋出莫名錯誤。 | A zero amount must give everyone zero, not throw a strange error. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 零額每人应为0且不应无故抛错的契约保留。 |
| en | v40106 | caption | 負數、小數或超大總額，仍然要被拒絕。 | Negative, fractional, or huge amounts must still be rejected. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 负数、小数、超大总额仍需拒绝的回归要求保留。 |
| en | v40107 | caption | 零人、超過一百人和小數人數也是一樣。 | The same goes for zero, over 100, or fractional people counts. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 0人、超100人、小数人数三类非法输入保留。 |
| en | v40108 | caption | 回歸的意思，就是修新 Bug 也守住舊契約。 | Regression testing checks that the bug fix preserves the old rules. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回归明确是测试旧契约未被新Bug修补破坏，非统计回归或重跑泛称。 |
| en | v40109 | caption | 輸入驗證也可能在重寫時被無意刪掉。 | Input validation may also be accidentally removed during a rewrite. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 输入验证可能意外被删的可能性保留，未恢复缺证的相对频率主张。 |
| en | v40112 | caption | 把需求、程式差異和回歸測試一起看。 | Review the requirements, code diff, and regression tests together. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求、程序差异、回归测试三类证据合看保留。 |
| en | v40113 | caption | 需求契約告訴你什麼叫修好。 | The requirement contract defines what fixed means. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求契约界定何为修好的意思保留。 |
| en | v40114 | caption | 差異讓你知道實際改了哪些檔、哪些行。 | The diff shows which files and lines actually changed. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 差异说明实际修改的文件和行，未省去具体范围含义。 |
| en | v40115 | caption | 回歸則證明新舊規則至少在測試範圍內成立。 | Regression tests show old and new rules hold within the tested range. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回归只证明在测试范围内成立，保留有限证明范围。 |
| en | v40116 | caption | 只缺一道關，審查紀錄就不完整。 | Miss a gate, and the review record is incomplete. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 缺一关导致记录不完整的编辑方法保留。 |
| en | v40119 | caption | 我會在審查紀錄裡放三件事。 | I put three things in the review record. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人称安排三项审查记录的意思保留，未制造正式PR记录。 |
| en | v40120 | caption | 第一，需求有哪些明確的驗收條件。 | First, the explicit acceptance conditions. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 首项明确验收条件的记录范围保留。 |
| en | v40121 | caption | 第二，實際差異只改了哪些地方。 | Second, the actual scope of the diff. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二项记录实际差异的改动范围保留。 |
| en | v40122 | caption | 第三，哪個測試先紅、修補後又如何變綠。 | Third, which test failed before and passed after the patch. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三项记录测试先失败后成功的顺序保留。 |
| en | v40123 | caption | 這三項可以寫進 PR 描述，讓審查者快速重跑。 | Put those in the PR description so others can rerun the check. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可写入PR描述供他人重跑的建议保留，未称已有真实PR。 |
| en | v4e6000 | caption | 最後把那個原本失敗的案例寫在審查摘要裡。 | Include the original failing case in the review summary. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 摘要记下原失败案例的建议保留。 |
| en | v4e6001 | caption | 附上完整差異，不只貼兩行好看的核心程式。 | Attach the full diff, not just two attractive core lines. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 提供完整差异而非仅两行核心代码的范围保留。 |
| en | v4e6002 | caption | 再列出重跑指令與通過的測試範圍。 | List rerun commands and the range of tests that passed. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 列出重跑命令和通过的测试范围的建议保留。 |
| en | v4e6003 | caption | 下一位審查者不必相信口頭報告，能自己驗證。 | The next reviewer can verify it instead of trusting a verbal report. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 后继审查者可独立验证而非只信口头报告的因果保留。 |
| en | v40126 | caption | 這個小型示範雖然通過驗收，仍不能代替真實業務判斷。 | This small demo passed acceptance, but cannot replace business judgment. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 小型验收通过仍不能代替业务判断的限制保留。 |
| en | v40127 | caption | 需求若一開始寫錯，測試也可能跟著綠錯方向。 | If the requirement was wrong, tests may pass for the wrong behavior. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若需求错误则测试可能错向通过的条件和可能性保留。 |
| en | v40128 | caption | 還要有人看改動範圍、資料影響和回滾方式。 | Someone must review scope, data impact, and rollback options too. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需人检查范围、数据影响、回滚三个领域保留。 |
| en | v40129 | caption | 負責合併的人，得對這個判斷負責。 | The person merging must own that judgment. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 合并者应承担判断责任的含义保留。 |
| en | v40130 | caption | 合併不是模型替團隊作的事，而是負責者作的決定。 | Merging is a responsible human decision, not a model's decision. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 模型不代替团队负责者决定合并的责任归属保留。 |
| en | v40133 | caption | 在 GitHub 的正式流程裡，審查者可以對變更行留言。 | In GitHub's formal flow, reviewers can comment on changed lines. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | GitHub审查者可评论变更行，产品拉丁拼写和能力范围保留。 |
| en | v40134 | caption | 也可以要求修改，或在看過證據後核准。 | They can request changes or approve after reading the evidence. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 要求修改或阅证后批准，两种选择和证据顺序保留。 |
| en | v40135 | caption | 這裡不替任何真實 PR 點核准。 | We are not approving any real PR here. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本示范不对真实PR执行批准，未虚构实际动作。 |
| en | v40136 | caption | 重點是讓下一位審查者找到同一份證據。 | The point is to let the next reviewer find the same evidence. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下一位审查者找到相同证据的目的保留。 |
| en | v40137 | caption | 影片畫面展示規則，不會用別人的 PR 當裝飾。 | The video shows the rule, not someone else's PR as decoration. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 画面展示规则而不拿他人PR当装饰的范围保留。 |
| en | v40140 | caption | 回到開頭：AI 修好 Bug，測試綠了，能直接合併嗎？ | Back to the start: AI fixed the bug and tests are green. Merge? | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI修好与绿灯是否足以合并仍是结尾反问，非自动授权。 |
| en | v40141 | caption | 先過需求、差異、回歸這三道關，再由人作最後判斷。 | Check requirements, diff, and regression; then a person decides. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 三关之后仍由人最后决定的顺序保留。 |
| en | v40142 | caption | 這次的起始碼、修補和測試，要放在一起核對。 | Keep the starter, patch, and tests together for this example. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 起始码、修补、测试要共同核对的证据集合保留。 |
| en | v40143 | caption | 拿你下一個小修補照著試一次，比背規則更有用。 | Try this on your next small fix instead of memorizing a rule. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 用下一份小修补练习比单背规则更有用的编辑建议保留。 |
| en | v40144 | caption | 這個小練習之後，再把同一方法用到較大的改動。 | Then carry the method from this exercise into larger changes. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先小练习再较大改动的顺序保留。 |
| en | title | metadata | AI 修好 Bug 就能合併？三個 PR 檢查點 | If AI Fixes a Bug, Can You Merge? Three PR Review Gates | PASS | 原full584 PASS＋精确不变；保留原判定来源 | The conditional If AI Fixes a Bug matches the source question and does not assert that the preserved patch was historically authored by AI. The three review gates are the episode teaching method. Adjacent description preserves the rerunnable local-demo scope and denies production-incident/merged-PR claims. Natural searchable English title, 55 codepoint characters by the native read-only result, below 100, no angle brackets. |
| en | description | metadata | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。 | The two original tests passed, but splitting 100 cents allocated only 99. Follow a real patch and test run to learn how to review requirements, the diff, and regression before merging.<br>This is a rerunnable local demo, not a production incident or a merged PR. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 说明保留旧两项通过、100分少到99、需求/差异/回归与本地非事故非合并PR限制。 |
| en | tags:0 | metadata | AI code review | AI code review | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI code review 搜寻词拉丁字母名称保持。 |
| en | tags:1 | metadata | PR review | PR review | PASS | 原full584 PASS＋精确不变；保留原判定来源 | PR review 搜寻词与来源保持。 |
| en | tags:2 | metadata | Bug fix | bug fix | PASS | 原full584 PASS＋精确不变；保留原判定来源 | Bug fix 为普通技术搜寻词，大小写规范不新增产品名。 |
| en | tags:3 | metadata | 程式碼審查 | code review | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 程式码审查用目标语言自然技术用语。 |
| en | tags:4 | metadata | 回歸測試 | regression testing | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回归测试采用明确技术用语，不误译为统计回归。 |
| en | chapter:opening | metadata | 綠燈也會漏 | Green Tests Can Miss Bugs | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 开场章节保留绿灯仍可能漏掉缺陷的含义。 |
| en | chapter:why-green | metadata | 綠燈不等於正確 | Green Is Not Correctness | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二章节保留绿灯不等于正确的证据限制。 |
| en | chapter:gate-one | metadata | 第一關：需求契約 | Gate 1: The Requirements | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一关章节保留需求契约/约束检查含义。 |
| en | chapter:gate-two | metadata | 第二關：讀差異 | Gate 2: Read the Diff | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二关章节保留直接阅读实际差异的含义。 |
| en | chapter:gate-three | metadata | 第三關：跑回歸 | Gate 3: Run Regression | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三关章节保留执行回归测试的含义。 |
| en | chapter:three-gates | metadata | 合併前的決定 | The Merge Decision | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 收束章节保留合并前最后由责任者判断的主题。 |
| ja | v40000 | caption | 三個人分一百分，舊測試全綠，結果卻只分出九十九。 | 100セントを3人で分けると99セント。元のテストは全件成功です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100/3 舊碼只得99分及原測試全過兩項均保留；次序重排不改因果。 |
| ja | v40001 | caption | AI 送來一份修補程式，你會直接合併嗎？ | AIが修正パッチを出しました。すぐマージしますか。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI 出修補後能否直接合併仍是教學問句，未歸因本地 patch 作者。 |
| ja | v40002 | caption | 我帶你看需求、差異與回歸，三道關都要過。 | 要件、差分、回帰を一緒に確認します。3つとも通る必要があります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 三關要件、差分與回歸均保留；一起確認保持講者引導語氣。 |
| ja | v40003 | caption | 我們先從那一分為什麼消失開始。 | まず、消えた1セントの原因から見ます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 消失1セント的原因與先從此處開始均保留。 |
| ja | v40007 | caption | 第一個舊測試，只檢查能整除的金額。 | 元の最初のテストは、割り切れる金額だけを確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一個原測試只驗整除金額，與120/3原斷言一致。 |
| ja | v40008 | caption | 人數不合法也會擋，兩個結果都是綠色。 | 人数が不正なら止めるテストも成功しています。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不合法人數被擋且該測試成功；も與開頭全件成功連接另一個綠燈。 |
| ja | v40009 | caption | 不整除的路徑沒人問，所以錯誤藏得好好的。 | 割り切れない場合を誰も問わず、バグが隠れました。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 未詢問不整除路徑使缺陷藏住的因果保留，限本例。 |
| ja | v40010 | caption | 這次示範是真正執行的檔案，不是想像案例。 | 架空の例ではなく、実際に動かしたファイルです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 實際執行檔案與非架空案例的區分完整保留。 |
| ja | v40011 | caption | 它證明程式照舊測試運作，沒有證明帳算對。 | 元のテストに通っただけで、計算の正しさは未確認です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 僅符合原測試、尚未證明計算正確的限制保留。 |
| ja | v4e1000 | caption | 這是起始專案真的跑過的兩個測試。 | これは出発点のプロジェクトで実行した2件のテストです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 起始專案實際執行2件測試，數量與實測語態一致。 |
| ja | v4e1001 | caption | 第一個測一百二十分，三人平均分。 | 1件目は120セントを3人で均等に分けます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 120セント、3人、均等分配皆與原測試一致。 |
| ja | v4e1002 | caption | 第二個測零人時要拋出錯誤。 | 2件目は人数がゼロなら例外を出すか調べます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 零人須產生例外的第二件测试條件一致。 |
| ja | v4e1003 | caption | 它們全綠，只能證明這兩件事，不能代表餘數正確。 | 両方成功しても、余りの処理までは証明できません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩件都成功仍不證明餘數處理，限制未弱化。 |
| ja | v40014 | caption | 分一百分給三個人，原始程式回三個三十三。 | 100セントを3人に分けると、元のコードは33ずつ返します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100セント分3人、原碼各33的數字和原碼主體一致。 |
| ja | v40015 | caption | 這不是顯示格式的問題，總和真的少了一分。 | 表示の問題ではなく、合計が本当に1セント足りません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非顯示問題而合計少1セント，否定及真實缺額保留。 |
| ja | v40016 | caption | 如果少掉的一分錢會記入帳務，就算測試全綠也不能合併。 | その1セントが会計に関わるなら、全テストが通ってもマージできません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 会計に関わるなら保留假設條件，不把教學例說成實際帳務事故。 |
| ja | v40017 | caption | 接下來看一份可以重跑的本地修補。 | 次は、再実行できるローカルの修正を見ます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下一步看可再執行的本地修正，範圍與時態一致。 |
| ja | v40018 | caption | 這個失敗結果已寫進可重跑的驗收檔案。 | この失敗は再実行できる検証ファイルにも記録しました。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 失敗已記入可再執行檢證檔案，保持已完成語態。 |
| ja | v40021 | caption | 這份本地分攤範例，留下了程式和測試的完整差異。 | このローカルの分配例には、コードとテストの完全な差分が残っています。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地分攤例留下完整程式與測試差分，未增加工具作者。 |
| ja | v40022 | caption | 修補後的九個測試重跑全過，稍後再做事後驗收。 | 修正後の九つのテストは再実行ですべて通りました。後ほど事後の受け入れテストを行います。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 9件重跑全過與稍後事後驗收均保留；43字為兩句，無已產生cue或配音預算可判超標。 |
| ja | v40023 | caption | 這不是正式站的事故，也不是已合併的真實 PR。 | 本番環境の事故でも、マージ済みの実際のPRでもありません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本番事故與已合併真PR兩項否定完整保留。 |
| ja | v40024 | caption | 它是可以公開重跑的一份本地修補案例。 | 公開して再実行できるローカルの修正例です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可公開重跑的本地修補例，未轉成已正式發布。 |
| ja | v40025 | caption | 所以它適合用來練審查，卻不能代表產品事故。 | レビューの練習には使えますが、製品事故の代表例ではありません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 適合審查練習但不代表產品事故的適用範圍保留。 |
| ja | v40028 | caption | 第一關，不要先看 AI 說它完成了什麼。 | 第1関門。AIの完了報告より先に見るものがあります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先於AI完了報告確認其他事項，保持第一關的建議順序。 |
| ja | v40029 | caption | 先把需求寫成你可以算得出來的條件。 | 自分で計算して確かめられる要件を書き出します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 將需求寫成可自行計算檢證的條件，動作與主體保留。 |
| ja | v40030 | caption | 這題要保留輸入規則，不能只修一個範例。 | 入力規則を守り、1例だけ直して終わりにしません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留輸入規則且不可只修單一例子的要求完整。 |
| ja | v40031 | caption | 也不能悄悄把分配規則改成另一種做法。 | 分配の規則を黙って別の方式に変えてもいけません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不可默默換分配方式，否定及規則類別一致。 |
| ja | v40032 | caption | 第一關的答案，應該能不靠工具自己口述。 | 第1関門の答えは、ツールなしで説明できるはずです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 應不依靠工具自行說明，應然語氣保留。 |
| ja | v40035 | caption | 第一條，結果長度要和人數一樣。 | 1つ目。出力配列の長さは人数と同じです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 輸出配列長度等於人數，未改成金額長度。 |
| ja | v40036 | caption | 第二條，所有人的份額加總，必須等於原來金額。 | 2つ目。全員の取り分の合計が元の金額に一致。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 全員份額總和等於原金額；條件清單的短句終止不構成語體誤譯。 |
| ja | v40037 | caption | 第三條，任何兩人最多只差一分。 | 3つ目。任意の2人の差は最大1セント。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 任意2人最大差1セント，量詞與上限一致。 |
| ja | v40038 | caption | 第四條，有餘數時，前面的人先分到。 | 4つ目。余りは先頭の人から順に受け取ります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 餘數由前面的人順序收到，順序契約保留。 |
| ja | v40039 | caption | 四條放在一起，才描述完整的分攤行為。 | 4条件を合わせて、分配の動作が決まります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 4條合併才描述分配行為，條數與完整性意涵保留。 |
| ja | v40040 | caption | 如果只補一百除三，還會漏掉其他金額。 | 100を3で割る例だけなら、別の金額を見落とします。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只處理100/3仍遺漏其他金額的條件與限制一致。 |
| ja | v4e2000 | caption | 只測一百分除三，還可能把規則寫死在特例上。 | 100を3で割るだけでは、特例を固定しても通ります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 單一100/3特例即使硬編也可能通過，未說實際修補硬編。 |
| ja | v4e2001 | caption | 再代入兩分給三個人，正確是前兩位各一分。 | 2セントを3人に分けると、先頭2人は1ずつです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2セント分3人、前2人各1，與契約正確輸出一致。 |
| ja | v4e2002 | caption | 第三位拿零分，總和仍是兩分。 | 3人目はゼロで、合計は2セントです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第3人0、合計2セント皆一致。 |
| ja | v4e2003 | caption | 這組資料會立刻露出四捨五入重複分配的問題。 | この例なら、丸めによる重複分配がすぐ分かります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 丸め描述本例四捨五入的上位處理，與畫面及後文四捨五入一致，未引入不同演算法。 |
| ja | v40042 | caption | 還有原本就存在的輸入檢查。 | 元からある入力チェックも確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 既有輸入檢查仍須確認，未稱新增規則。 |
| ja | v40043 | caption | 總額不能是負數、小數或超過安全整數。 | 総額は負数、小数、安全整数の上限超えを拒否します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 負數、小數、超過安全整數上限均拒絕，三類一致。 |
| ja | v40044 | caption | 人數只能是一到一百之間的安全整數。 | 人数は1から100までの安全な整数だけです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 人數為1至100的安全整數，端點與安全整數要求保留。 |
| ja | v40045 | caption | 修補若刪掉這些檢查，就算範例變對也不能過關。 | 修正でこの検証が消えたら、例が正しくても不合格です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若刪掉驗證，即使例子正確仍不合格，條件及否定一致。 |
| ja | v40046 | caption | 它們不是額外加分題，而是修補前就有的規則。 | 追加課題ではなく、元からあった規則です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 規則原已存在而非附加題，時間範圍保留。 |
| ja | v40049 | caption | 把一百分除以三，理想結果是三十四、三十三、三十三。 | 100を3で分ける正解は34、33、33です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100/3正確34、33、33，所有數字與次序一致。 |
| ja | v40050 | caption | 這組數字同時檢查總和與餘數順序。 | 合計と余りを渡す順番を同時に確認できます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同時檢查合計和餘數順序，兩項完整。 |
| ja | v40051 | caption | 只測每個人差不多，還是不夠。 | 各人の金額が近いかだけでは足りません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只看各人金額接近不足，限制一致。 |
| ja | v40052 | caption | 需求契約先寫清楚，才有審查的尺。 | 要件を先に明確にして、レビューの物差しにします。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求先明確作為審查尺，日文物差し保持比喻。 |
| ja | v40053 | caption | 換成兩分三人，正確順序也是一、一、零。 | 2セントを3人なら、順に1、1、0です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2セント、3人、1/1/0順序完整。 |
| ja | v40056 | caption | 第二關，打開實際差異，不只讀工具的完成訊息。 | 第2関門。完了報告だけでなく実際の差分を開きます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 打開實際差分且不僅完了報告，第二關對象一致。 |
| ja | v40057 | caption | 先確認它只改到預期的程式和測試。 | 想定したコードとテストだけが変わったか確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 確認只有預期程式與測試改動，only範圍完整。 |
| ja | v40058 | caption | 接著把新增邏輯代入一百分除三的例子。 | 新しいロジックに100を3で割る例を当てはめます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新增邏輯代入100/3，對象與數字一致。 |
| ja | v40059 | caption | 最後看它有沒有刪掉原來的保護條件。 | 元の保護条件を削っていないかも見ます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原保護條件是否刪除仍是確認問題，未直接斷言被刪。 |
| ja | v40060 | caption | 文字摘要可能遺漏細節，差異本身才是檢查對象。 | 要約では細部が抜けることがあります。確認するのは差分そのものです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 摘要可能漏細節、檢查差分本身，可能性及對象一致。 |
| ja | v40063 | caption | 這份修補先算每人最少要拿多少。 | この修正は、まず一人あたりの最低額を計算します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先算每人最低額，對應base計算且不歸因工具。 |
| ja | v40064 | caption | 再算剩下幾分，要補給幾位前面的人。 | 次に余ったセントを先頭の何人に配るか決めます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 再算餘數分給前幾人，對應remainder與i比較。 |
| ja | v40065 | caption | 總額一百，分給三人，各拿三十三，還剩一分錢。 | 100セントを3人に分けると、各33セントで1セント余ります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100セント、3人、各33、餘1完全一致。 |
| ja | v40066 | caption | 第一位多拿一分，其餘兩位維持三十三。 | 最初の人が1多く、残り2人は33のまま。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 首位多1、其餘2人維持33；清單式短句保留數值。 |
| ja | v40067 | caption | 用兩分三人再代一次，就能看到前兩位各多一分。 | 2を3で分けても、先頭2人が1ずつ受け取ります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2/3時前2人各1，base0下的額外1與最終1等價。 |
| ja | v4e3000 | caption | 完整差異顯示，函式前兩段輸入檢查仍然保留。 | 差分全体を見ると、関数冒頭の2つの入力検証は残っています。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 完整差分中函式前2段驗證仍在，数量與實際保留語態一致。 |
| ja | v4e3001 | caption | 非法金額和非法人數，仍會在分配前被擋。 | 不正な金額や人数は、分配前に拒否されます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不合法金額、人數在分配前拒絕，條件及先後完整。 |
| ja | v4e3002 | caption | 這份修補把平均四捨五入，換成基本分與餘數。 | この修正では、平均の四捨五入を基本の配分額と余りに置き換えます。 | PASS | 本次新独立重读CPS缩句 | PASS: both state that this retained patch replaces rounding of the average with the base allocated amount and remainder. Removing 計算 does not drop a source clause; the zh-TW source names the base and remainder rather than adding an explicit calculation clause. PASS: 平均、四捨五入、基本の配分額 and 余り stay unchanged and name the same arithmetic concepts. No product or company name changes. PASS: neither current nor proposed line adds, drops or changes a number. Neighboring two input guards remain separate. PASS: この修正では anchors the statement to this patch. 置き換えます is natural polite nonpast narrative here, not an instruction or a future promise. No historical AI authorship or approval is introduced. PASS: v4e3001 still says invalid amount/people are rejected before allocation; v4e3003 still limits the evidence to this local diff, so the change of allocation logic does not imply removal of input checks or validation of other files. PASS: concise natural Japanese; removes redundant 計算 and aspect without adding ambiguity. This is a textual assessment, not a measured cue-fit pass. |
| ja | v4e3003 | caption | 這是這份本地差異的範圍，不替其他檔案背書。 | これはこの差分の話で、他のファイルは保証しません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只討論此本地差分，不為其他檔案保證，範圍否定保留。 |
| ja | v40070 | caption | 我在差異裡先找原有驗證，這次沒有被刪掉。 | 元の入力検証が削られていないと、差分で確認しました。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 差分確認原輸入驗證未刪的已完成觀察一致。 |
| ja | v40071 | caption | 再看檔案清單，只有程式和測試被修改。 | 変更ファイルはコードとテストだけでした。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 変更ファイル僅程式與測試，與patch兩檔範圍一致。 |
| ja | v40072 | caption | 新增測試涵蓋不整除、零金額和非法輸入。 | 追加テストは余り、ゼロ金額、不正入力を扱います。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 追加測試含餘數、零金額及不合法輸入，三類保留。 |
| ja | v40073 | caption | 這些都是看得見的證據，不是工具的口頭保證。 | 口頭の保証ではなく、確認できる証拠です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可查證的證據對照口頭保證，未偷換為自動核准。 |
| ja | v40074 | caption | 如果它順手改了部署或帳務設定，應該另外討論。 | デプロイや会計設定まで変われば、別途協議します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若改部署或會計設定需另議，条件形維持假設，未說此次有改。 |
| ja | v40075 | caption | 新增測試也要看斷言，不只看測試名稱。 | テスト名だけでなく、実際のアサーションを読みます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | アサーション是日文程式測試的恰當用語，且不只看測試名的要求完整。 |
| ja | v4e4000 | caption | 新增測試不能只看名字，要看它到底斷言什麼。 | 追加テストは名前だけでなく、アサーションで何を確認するか見ます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | Name-only checking remains insufficient; the repaired sentence asks what the programming assertion actually verifies. アサーション matches v40075 and the visible assert.deepEqual examples. The added 名前だけでなく keeps the source not-only condition, with no new factual claim. |
| ja | v4e4001 | caption | 這份修補測到一百分除三，是三十四、三十三、三十三。 | 100を3で分け、34、33、33になると確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100/3等於34/33/33是讀取現存測試的確認，不是假設新補測；數字完整。 |
| ja | v4e4002 | caption | 也測到兩分分五人，前兩位各一分，其餘拿零。 | 2を5人に分け、先頭2人が1、他はゼロと確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2分5人前2位各1其餘0，與實際patch斷言一致。 |
| ja | v4e4003 | caption | 這兩組一起看，比只看測試數量更有意義。 | 2例を読む方が、テスト件数だけより意味があります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 一起讀2例較單看件數有意義，保留編輯建議而非量測。 |
| ja | v40077 | caption | 這裡展示的是本地修補，不是假裝已有人核准的 PR。 | これはローカルの修正で、承認済みPRではありません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地修正、非核准PR的界線完整，未宣稱已有人批准。 |
| ja | v40078 | caption | 真正的專案還要看相關模組、型別與維運影響。 | 実案件では周辺モジュール、型、運用面も見ます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 真實案件的模組、型、運用影響三項保留。 |
| ja | v40079 | caption | 如果這段程式連著付款系統，範圍會更大。 | 決済システムにつながるなら、確認範囲は広がります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 決済系統接續なら為假設；審查範圍擴大，不宣稱已整合付款。 |
| ja | v40080 | caption | 影片示範的方法，可以帶進真正的審查流程。 | この動画の方法は実際のレビューにも持ち込めます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 示範方法可帶入真實審查，未把示範變成正式審查操作。 |
| ja | v40081 | caption | 我把這個範圍明確標出，避免觀眾以為是真實核准。 | 実際に承認した例と誤解されないよう範囲を示します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 明示範圍避免觀眾誤認已真實承認，防誤解目的保留。 |
| ja | v40084 | caption | 第三關，把修補放進另外寫的事後驗收。 | 第3関門。修正を別に書いた事後の検証にかけます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 另寫事後検証作第三關，未混淆既有2件或patch9件。 |
| ja | v40085 | caption | 工具自己寫的測試有用，但不能是唯一標準。 | ツール自身のテストも有用ですが、それだけでは不十分です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 工具自寫測試有用但不足，泛稱限制而非本patch作者證明。 |
| ja | v40086 | caption | 好的驗收測試，應該先在舊版程式重現這個錯誤。 | よい受け入れテストは、まず旧コードでこのバグを再現します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先在舊碼重現錯誤的受入測試建議保留。 |
| ja | v40087 | caption | 所以我先拿舊碼跑同一份事後驗收。 | そこで同じ事後検証を旧コードでも実行しました。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同一份事後檢證在舊碼也實際執行，第一人稱日文可省略但完成語態保留。 |
| ja | v40088 | caption | 理想順序是先讓驗收能重現舊錯，再評估新修補。 | まず旧バグを再現し、その後で新修正を評価します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先舊bug再新修補的建議順序完整，沒有改成預先盲測紀錄。 |
| ja | v40091 | caption | 舊碼雖然兩個原測試全過，事後四類只過一類。 | 旧テスト2件は成功し、事後検証は4種中1種だけ成功しました。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 旧2件成功、事後4種僅1種成功，數量與差異完整。 |
| ja | v40092 | caption | 這證明新驗收能抓到我們要修的缺陷。 | 新しい検証が狙った欠陥を捉える証拠です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新検証捕捉目标缺陷的證據與因果保留。 |
| ja | v40093 | caption | 換成修補後，四類事後驗收全通過。 | 修正後は、事後検証の4種類がすべて成功。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修正後事後4類全過，與9件patch測試未混用。 |
| ja | v40094 | caption | 這才是比較有力的紅燈到綠燈證據。 | これが、失敗から成功へ変わった強い証拠です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 紅轉綠為較有力證據的比較語意保留，非全面正確保證。 |
| ja | v40095 | caption | 這一步能排除只檢查舊有整除案例的假安全感。 | 割り切れる旧例だけを見る安心感を取り除けます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只看整除舊例的安心感應被排除，保留來源的審查限制。 |
| ja | v40098 | caption | 驗收不是只寫一百除三。 | 検証は100を3で割る例だけではありません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 验收不止100/3，否定與數值完整。 |
| ja | v40099 | caption | 我還把零到五百的總額，搭配一到二十人跑過。 | 総額0から500、人数1から20も組み合わせました。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 已組合總額0到500、人數1到20，端點及已做語態一致。 |
| ja | v40100 | caption | 每組都檢查總和，並確認最大差距不超過一分。 | 毎回合計と、最大差が1セント以下か確かめます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 每組合計與最大差不大於1セント兩項檢查完整。 |
| ja | v40101 | caption | 這種性質檢查，能抓到你沒想到的餘數組合。 | 性質を確認すれば、想定外の余りも拾えます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 性質確認能找出未想過的餘數組合，未聲稱窮盡全範圍。 |
| ja | v40102 | caption | 實際回圈涵蓋大量組合，但仍不是形式化證明。 | 多くの組み合わせを試しても、形式的な証明ではありません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 試大量組合仍非形式證明，保留关键限制。 |
| ja | v40103 | caption | 超出測試範圍的風險，要再根據業務補案例。 | 範囲外のリスクには業務に応じた例を追加します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 測試範圍外按業務補例，未變成無條件完整安全。 |
| ja | v4shot0 | caption | 這是同一份修補在本機跑出的驗收輸出。 | 同じ修正をローカルで検証した実際の出力です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同一修補在本機検証的實際輸出，不引入Claude作者或原始終端截圖宣稱。 |
| ja | v4shot1 | caption | 四項綠燈有紀錄，但還要對照需求與完整差異。 | 4項目の成功記録と、要件・差分を照らします。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 4項成功記錄仍須對照要件與差分，數字及證據限制保留。 |
| ja | v4e5000 | caption | 回圈跑每組數字時，不只看總額。 | ループ内では、各組み合わせで合計以外も見ます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 迴圈逐組不只看合計，保留追加檢查引導。 |
| ja | v4e5001 | caption | 它還比對輸出長度，確認沒有漏掉任何人。 | 出力の長さと人数を比べ、漏れがないか確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 比輸出長度與人數避免漏人，與實際length斷言一致。 |
| ja | v4e5002 | caption | 再找最大和最小份額，差距不能超過一。 | 最大額と最小額を比べ、差は1以下です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 最大最小份額差不超1，兩端及界線一致。 |
| ja | v4e5003 | caption | 這三個斷言對每組資料都成立，才算這關通過。 | 3つのアサーションが毎回成立して初めて通過します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | The three programming assertions must hold for every dataset before the gate passes. 3つのアサーション consistently uses the established technical term. 毎回 is clear in the adjacent per-dataset checks of sum, output length and max/min share. 成立して初めて retains the required-condition relationship and does not turn examples into formal proof. |
| ja | v40105 | caption | 零金額要回傳每人零分，不能拋出莫名錯誤。 | ゼロ金額なら全員にゼロ。意味不明な例外は出しません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 零金額每人零，且不產生莫名例外，未改成零人。 |
| ja | v40106 | caption | 負數、小數或超大總額，仍然要被拒絕。 | 負数、小数、上限を超える総額は引き続き拒否します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 負數、小數、超上限總額仍拒絕，三類與既有规则一致。 |
| ja | v40107 | caption | 零人、超過一百人和小數人數也是一樣。 | 人数ゼロ、101人以上、小数の人数も同じです。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 零人、101以上、小數人數等价原超100，邊界與拒絕延續一致。 |
| ja | v40108 | caption | 回歸的意思，就是修新 Bug 也守住舊契約。 | 回帰確認では、バグ修正後も元の契約を守ります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回帰確認保留修bug仍守舊契約的回歸測試意涵，非統計回歸。 |
| ja | v40109 | caption | 輸入驗證也可能在重寫時被無意刪掉。 | 入力検証も、書き直す際に誤って削除されることがあります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 誤刪入力検証是可能風險，可能形未改成已發生或最高頻率。 |
| ja | v40112 | caption | 把需求、程式差異和回歸測試一起看。 | 要件、コード差分、回帰テストをまとめて見ます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 要件、程式差分與回帰テスト三者同看，術語意涵一致。 |
| ja | v40113 | caption | 需求契約告訴你什麼叫修好。 | 要件は、何をもって修正完了とするかを示します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 要件說明何謂修好，未用模型自報作尺。 |
| ja | v40114 | caption | 差異讓你知道實際改了哪些檔、哪些行。 | 差分は、実際にどのファイルと行が変わったかを示します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 實際改動檔與行兩項完整。 |
| ja | v40115 | caption | 回歸則證明新舊規則至少在測試範圍內成立。 | 回帰テストは、試した範囲で新旧の規則を確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回帰テスト只在試過範圍確認新旧規則，範圍限制保留。 |
| ja | v40116 | caption | 只缺一道關，審查紀錄就不完整。 | どれか欠けると、レビューの記録は不十分です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 任一道欠缺即審查記錄不足，三關關係一致。 |
| ja | v40119 | caption | 我會在審查紀錄裡放三件事。 | レビュー記録には3点を残します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 講者將留3項審查記錄，第一人稱可省略且數字完整。 |
| ja | v40120 | caption | 第一，需求有哪些明確的驗收條件。 | 1つ目。要件の具体的な受け入れ条件。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第1項具體受入條件完整；列舉片語不構成叙述語體滑移。 |
| ja | v40121 | caption | 第二，實際差異只改了哪些地方。 | 2つ目。実際の差分で変えた場所。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第2項差分實際改哪裡，保留限定對象。 |
| ja | v40122 | caption | 第三，哪個測試先紅、修補後又如何變綠。 | 3つ目。どのテストが失敗し、修正後に成功したか。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第3項哪測試先失敗、修後成功，紅綠語意與先後一致。 |
| ja | v40123 | caption | 這三項可以寫進 PR 描述，讓審查者快速重跑。 | PR説明に書けば、次の人もすぐ再実行できます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 3項可写入PR描述讓下一審查者重跑，PR Latin拼寫與可行語氣一致。 |
| ja | v4e6000 | caption | 最後把那個原本失敗的案例寫在審查摘要裡。 | 最後に、元の失敗例をレビュー要約へ残します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原失敗例寫入摘要的建議完整。 |
| ja | v4e6001 | caption | 附上完整差異，不只貼兩行好看的核心程式。 | 見栄えのよい2行だけでなく、差分全体を添えます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 完整差分、不只好看的2行，完整性要求與数字一致。 |
| ja | v4e6002 | caption | 再列出重跑指令與通過的測試範圍。 | 再実行コマンドと、通ったテスト範囲も示します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 重跑指令及通過範圍兩項均保留。 |
| ja | v4e6003 | caption | 下一位審查者不必相信口頭報告，能自己驗證。 | 口頭報告を鵜呑みにせず、自分で検証できます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下一審查者无需信口頭報告可自驗，主体承前文未改為信任模型。 |
| ja | v40126 | caption | 這個小型示範雖然通過驗收，仍不能代替真實業務判斷。 | この小規模な実演は検証を通りましたが、実際の業務判断の代わりにはなりません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 示範已過驗證仍不能代業務判斷，既成结果與限制完整。 |
| ja | v40127 | caption | 需求若一開始寫錯，測試也可能跟著綠錯方向。 | 要件が最初から誤っていれば、テストも誤った方向で通ることがあります。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若需求先錯，測試也可能朝錯誤方向通過，条件與可能性保留。 |
| ja | v40128 | caption | 還要有人看改動範圍、資料影響和回滾方式。 | 変更範囲、データへの影響、戻し方も人が確認します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 人確認範圍、資料影響與回復方式，三項均保留。 |
| ja | v40129 | caption | 負責合併的人，得對這個判斷負責。 | マージ担当者がその判断に責任を持ちます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 合併担当者負責判斷，責任主体一致。 |
| ja | v40130 | caption | 合併不是模型替團隊作的事，而是負責者作的決定。 | マージはモデルではなく、担当者が決めます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 由担当者決定而非模型，未改成模型可替團隊合併。 |
| ja | v40133 | caption | 在 GitHub 的正式流程裡，審查者可以對變更行留言。 | GitHubの正式な流れでは、変更行にコメントできます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | GitHub正式流程可在变更行留言，保存官方文件支援且名稱exact。 |
| ja | v40134 | caption | 也可以要求修改，或在看過證據後核准。 | 修正依頼も、証拠を見たうえでの承認もできます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可要求修正或見證據後承認，三關編輯建議未说成GitHub硬規則。 |
| ja | v40135 | caption | 這裡不替任何真實 PR 點核准。 | ここでは実際のPRを承認していません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 此處沒承認真PR，完成否定與本地範圍保留。 |
| ja | v40136 | caption | 重點是讓下一位審查者找到同一份證據。 | 次の人も同じ証拠にたどり着けることが大切です。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同じ証拠にたどり着ける is the natural construction for the next reviewer being able to reach the same evidence; the surrounding lines are about review traceability. It adds no approval, publication or real-PR operation. 次の人 is contextually the next reviewer. |
| ja | v40137 | caption | 影片畫面展示規則，不會用別人的 PR 當裝飾。 | 画面は規則の説明用で、他人のPRを飾りにはしません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 畫面只説明規則，不用他人PR裝飾，否定與範圍一致。 |
| ja | v40140 | caption | 回到開頭：AI 修好 Bug，測試綠了，能直接合併嗎？ | 最初の問いです。AIが直し、テストが緑なら即マージ？ | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 開頭問題的重述仍为問句，非工具作者或已合併的事实宣稱。 |
| ja | v40141 | caption | 先過需求、差異、回歸這三道關，再由人作最後判斷。 | 要件、差分、回帰を確認し、最後は人が判断します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 三關後最後由人判斷，回帰在前文已定義為回帰テスト。 |
| ja | v40142 | caption | 這次的起始碼、修補和測試，要放在一起核對。 | 出発点のコード、修正、テストを一緒に照合します。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本次起始碼、修補、測試三者一起照合，對象完整。 |
| ja | v40143 | caption | 拿你下一個小修補照著試一次，比背規則更有用。 | 次の小さな修正で試す方が、暗記より役立ちます。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下個小修補實作比背誦有用，為原編輯建議而非新增成效事實。 |
| ja | v40144 | caption | 這個小練習之後，再把同一方法用到較大的改動。 | その後、より大きな変更にも同じ方法を使いましょう。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 小練習後才用至較大改動，順序與勸勉語氣一致。 |
| ja | title | metadata | AI 修好 Bug 就能合併？三個 PR 檢查點 | AIがバグを直したらマージしていい？PRで確認する3つのこと | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI/PR Latin字樣正確、3關數量完整，36字內且無尖括號；問句保留。 |
| ja | description | metadata | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。 | 元の2つのテストはすべて成功したのに、100セントを分けると合計は99セントでした。開発者は実際の修正とテストをたどり、マージ前に要件・差分・回帰を確認する方法を学べます。<br>これは再実行できるローカルの例で、本番環境の事故やマージ済みのPRではありません。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原2測試成功、100變99、本地可重跑及非事故／非已合併PR完整保留；沒有作者歸因。 |
| ja | tags:0 | metadata | AI code review | AIコードレビュー | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI代码审查術語自然日文AIコードレビュー，AI拼寫正確。 |
| ja | tags:1 | metadata | PR review | PRレビュー | PASS | 原full584 PASS＋精确不变；保留原判定来源 | PRレビュー是自然檢索詞，PR拼寫不變。 |
| ja | tags:2 | metadata | Bug fix | バグ修正 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | Bug作一般技術詞自然譯為バグ修正，未當官方产品名改写。 |
| ja | tags:3 | metadata | 程式碼審查 | コードレビュー | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 程式碼審查自然譯コードレビュー，與tags:0相容。 |
| ja | tags:4 | metadata | 回歸測試 | 回帰テスト | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回歸測試譯回帰テスト，與正文明确用語一致。 |
| ja | chapter:opening | metadata | 綠燈也會漏 | 緑のテストにも見落としがある | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 綠色測試也有遺漏意涵完整，短章節名自然。 |
| ja | chapter:why-green | metadata | 綠燈不等於正確 | テスト成功と正しさは別 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 成功與正確不等同的對照完整。 |
| ja | chapter:gate-one | metadata | 第一關：需求契約 | 第1関門：要件の確認 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求契約以要件確認表達，與正文四條完整需求關係一致。 |
| ja | chapter:gate-two | metadata | 第二關：讀差異 | 第2関門：差分を読む | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二關讀差分，序數及動作一致。 |
| ja | chapter:gate-three | metadata | 第三關：跑回歸 | 第3関門：回帰テスト | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三關回帰テスト，明確為回歸測試而非統計分析。 |
| ja | chapter:three-gates | metadata | 合併前的決定 | マージ前の判断 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 合併前判斷，時間及決策意涵完整。 |
| ko | v40000 | caption | 三個人分一百分，舊測試全綠，結果卻只分出九十九。 | 세 명이 100센트를 나누는데 기존 테스트는 통과해도 합계는 99입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留三人、100 cents、舊測試通過與合計99的矛盾；99的cent單位可由同句前文承接。 |
| ko | v40001 | caption | AI 送來一份修補程式，你會直接合併嗎？ | AI가 수정 패치를 냈습니다. 바로 병합하시겠습니까? | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留AI交來修補後是否直接合併的教學問句，未把特定保留patch作者說成已查證。 |
| ko | v40002 | caption | 我帶你看需求、差異與回歸，三道關都要過。 | 요구 사항, 변경 내역, 회귀 검증을 함께 봅니다. 세 단계 모두 통과해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求、差異與回歸三關及全部須通過均在；一起檢視的敘述保留教學邀請。 |
| ko | v40003 | caption | 我們先從那一分為什麼消失開始。 | 먼저 1센트가 어디서 사라졌는지 보겠습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留從消失的1 cent開始查問題的順序。 |
| ko | v40007 | caption | 第一個舊測試，只檢查能整除的金額。 | 첫 번째 기존 테스트는 나누어떨어지는 금액만 확인합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 첫 번째/기존及只能整除的限制準確，並未聲稱所有金額受測。 |
| ko | v40008 | caption | 人數不合法也會擋，兩個結果都是綠色。 | 잘못된 인원수도 막습니다. 두 테스트 모두 통과합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留非法人數被擋與兩個測試通過，與舊測試檔相符。 |
| ko | v40009 | caption | 不整除的路徑沒人問，所以錯誤藏得好好的。 | 나머지가 생기는 경우는 검사하지 않아 오류가 숨어 있었습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 未檢查餘數路徑造成錯誤藏住的因果成立，過去式符合舊測試範圍。 |
| ko | v40010 | caption | 這次示範是真正執行的檔案，不是想像案例。 | 이 시연에는 실제로 실행한 파일을 씁니다. 가상 사례가 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 實際執行的檔案及非想像例子的對照保留，未擴張成正式產品事故。 |
| ko | v40011 | caption | 它證明程式照舊測試運作，沒有證明帳算對。 | 기존 테스트대로 동작한다는 증거지 정산이 맞다는 증거는 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 區分舊測試能證明的動作與不能證明的帳目正確性。 |
| ko | v4e1000 | caption | 這是起始專案真的跑過的兩個測試。 | 시작 프로젝트에서 실제 실행한 두 테스트입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留起始專案及確實執行的兩個測試，沒有降成假設。 |
| ko | v4e1001 | caption | 第一個測一百二十分，三人平均分。 | 첫째는 120센트를 세 명에게 똑같이 나누는 경우입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 120 cents、三人及平均分三要素正確。 |
| ko | v4e1002 | caption | 第二個測零人時要拋出錯誤。 | 둘째는 인원이 0일 때 오류를 던지는지 봅니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二測試、人數0及拋出錯誤均保留。 |
| ko | v4e1003 | caption | 它們全綠，只能證明這兩件事，不能代表餘數正確。 | 두 테스트는 그 두 가지만 증명합니다. 나머지 처리가 맞는지는 증명하지 못합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩個測試只能證明那兩件事，不能證明餘數處理，限制未遺漏。 |
| ko | v40014 | caption | 分一百分給三個人，原始程式回三個三十三。 | 원본 코드는 100센트를 세 명에게 33, 33, 33으로 줍니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100 cents分三人得到33/33/33準確，原始程式身分清楚。 |
| ko | v40015 | caption | 這不是顯示格式的問題，總和真的少了一分。 | 표시 형식의 문제가 아닙니다. 합계가 정말 1센트 부족합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非顯示格式錯誤、總和真的少1 cent均保留。 |
| ko | v40016 | caption | 如果少掉的一分錢會記入帳務，就算測試全綠也不能合併。 | 회계에 영향을 줄 1센트라면 테스트가 다 통과해도 병합하면 안 됩니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 使用조건 -라면保留帳務影響的假設，沒有宣稱本例已發生帳務事故。 |
| ko | v40017 | caption | 接下來看一份可以重跑的本地修補。 | 다음은 다시 실행할 수 있는 로컬 수정안을 보겠습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留接下來、可重跑與本地修補，沒有產品作者或已合併聲明。 |
| ko | v40018 | caption | 這個失敗結果已寫進可重跑的驗收檔案。 | 이 실패 사례는 다시 실행할 수 있는 검증 파일에 담았습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 已寫入可重跑驗收檔案是完成狀態，검증 파일符合此處保存案例的語境。 |
| ko | v40021 | caption | 這份本地分攤範例，留下了程式和測試的完整差異。 | 이 로컬 분배 예제에는 코드와 테스트의 전체 변경 내용이 남아 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地分配例、程式與測試的完整變更均保留，未引用檔名作Claude作者證據。 |
| ko | v40022 | caption | 修補後的九個測試重跑全過，稍後再做事後驗收。 | 수정 후 아홉 개 테스트를 다시 실행해 모두 통과했습니다. 잠시 후 사후 인수 테스트도 실행합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 九個測試已重跑全過採完成式，事後驗收是接下來步驟；九與四未混合。 |
| ko | v40023 | caption | 這不是正式站的事故，也不是已合併的真實 PR。 | 운영 사이트 사고도, 실제로 병합된 PR도 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同時排除正式站事故與已合併真實PR，PR拼写未變。 |
| ko | v40024 | caption | 它是可以公開重跑的一份本地修補案例。 | 공개적으로 재실행할 수 있는 로컬 수정 사례입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 公開重跑及本地修補案例的范围保留。 |
| ko | v40025 | caption | 所以它適合用來練審查，卻不能代表產品事故。 | 검토 연습에는 좋지만 제품 사고를 대표하지는 않습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 適合審查練習、不能代表產品事故的因果与限定均在。 |
| ko | v40028 | caption | 第一關，不要先看 AI 說它完成了什麼。 | 첫 단계에서는 AI의 완료 보고부터 읽어서는 안 됩니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一關及不先讀AI完成報告的指示清楚，AI拼寫保留。 |
| ko | v40029 | caption | 先把需求寫成你可以算得出來的條件。 | 먼저 직접 계산할 수 있는 조건으로 요구 사항을 적습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先寫成可自行計算的需求條件，未加入工具能力或強制官方流程。 |
| ko | v40030 | caption | 這題要保留輸入規則，不能只修一個範例。 | 입력 규칙을 지켜야지 예제 하나만 고치면 안 됩니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留輸入規則、不僅修一例兩個要點一致。 |
| ko | v40031 | caption | 也不能悄悄把分配規則改成另一種做法。 | 분배 규칙을 슬쩍 다른 방식으로 바꿔서도 안 됩니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不得悄悄改分配方式的否定與規則範圍保留。 |
| ko | v40032 | caption | 第一關的答案，應該能不靠工具自己口述。 | 첫 단계의 답은 도구 없이도 직접 설명할 수 있어야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一關、無工具及能自己口述均有對應。 |
| ko | v40035 | caption | 第一條，結果長度要和人數一樣。 | 첫째, 결과의 길이는 인원수와 같아야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一條輸出長度等於人數，沒有把人數改成金額。 |
| ko | v40036 | caption | 第二條，所有人的份額加總，必須等於原來金額。 | 둘째, 모든 사람의 몫을 더하면 원래 금액이어야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二條所有份額加總等於原金額，未弱化成約等於。 |
| ko | v40037 | caption | 第三條，任何兩人最多只差一分。 | 셋째, 두 사람의 몫 차이는 최대 1센트입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 任何兩人差距最多1 cent準確，최대保留上限。 |
| ko | v40038 | caption | 第四條，有餘數時，前面的人先分到。 | 넷째, 나머지는 앞쪽 사람부터 받습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第四條餘數先給前面的人，順序不顛倒。 |
| ko | v40039 | caption | 四條放在一起，才描述完整的分攤行為。 | 네 조건이 모여야 분배 동작을 온전히 설명합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四個條件一起才完整描述分配行為，네條件數量準確。 |
| ko | v40040 | caption | 如果只補一百除三，還會漏掉其他金額。 | 100을 3으로 나누는 경우만 고치면 다른 금액을 놓칩니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只修100/3會漏其他金額的條件和風險保留。 |
| ko | v4e2000 | caption | 只測一百分除三，還可能把規則寫死在特例上。 | 100을 3으로 나누는 것만 검사하면 그 특수 사례에 맞춰 규칙을 고정해 버릴 수 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 검사하면 retains the only-test-100/3 condition. 그 특수 사례에 맞춰 규칙을 고정해 버릴 수 있습니다 explicitly keeps the undesirable possibility of hardcoding the rules to that single special case. The next 2-cent/3-person example illustrates the broader requirement; the repaired line does not say hardcoding necessarily occurred or that the patch is already accepted. |
| ko | v4e2001 | caption | 再代入兩分給三個人，正確是前兩位各一分。 | 2센트를 세 명에게 나누면 앞의 두 명이 1센트씩 받습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2 cents給三人，前兩位各1 cent，順序與金額準確。 |
| ko | v4e2002 | caption | 第三位拿零分，總和仍是兩分。 | 셋째는 0센트, 합계는 여전히 2센트입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三位0 cent、總和仍2 cents均保留。 |
| ko | v4e2003 | caption | 這組資料會立刻露出四捨五入重複分配的問題。 | 이 사례는 반올림으로 중복 분배하는 오류를 바로 드러냅니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 這組資料揭露反覆四捨五入造成重複分配的問題，沒有變成只顯示格式錯誤。 |
| ko | v40042 | caption | 還有原本就存在的輸入檢查。 | 기존에 있던 입력 검사도 지켜야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留既有輸入檢查的存在與應維持之語境。 |
| ko | v40043 | caption | 總額不能是負數、小數或超過安全整數。 | 총액은 음수나 소수, 안전한 정수 범위를 넘는 값이면 안 됩니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 負數、小數及超出安全整數範圍全部拒絕，與Number.isSafeInteger相符。 |
| ko | v40044 | caption | 人數只能是一到一百之間的安全整數。 | 인원수는 1부터 100까지의 안전한 정수여야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 人數必須為1至100的安全整數，兩端與整數條件保留。 |
| ko | v40045 | caption | 修補若刪掉這些檢查，就算範例變對也不能過關。 | 이 검사를 지웠다면 예제가 맞아도 통과시킬 수 없습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若刪掉驗證即使範例正確仍不得過關，假設和否定清楚。 |
| ko | v40046 | caption | 它們不是額外加分題，而是修補前就有的規則。 | 추가 점수 문제가 아니라 수정 전부터 있던 규칙입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不是額外加分，而是修補前存在的規則；前後時間不錯置。 |
| ko | v40049 | caption | 把一百分除以三，理想結果是三十四、三十三、三十三。 | 100센트를 세 명에게 나누면 34, 33, 33이 정답입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100 cents分三人正確34/33/33，數字與順序未改。 |
| ko | v40050 | caption | 這組數字同時檢查總和與餘數順序。 | 합계와 나머지를 주는 순서를 함께 검사하는 사례입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同時檢查加總和餘數分配顺序，沒有遺漏第二項。 |
| ko | v40051 | caption | 只測每個人差不多，還是不夠。 | 각자의 금액이 비슷한지만 확인하면 부족합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 僅確認每人金額差不多仍不足，each-person語義保留。 |
| ko | v40052 | caption | 需求契約先寫清楚，才有審查的尺。 | 요구 사항을 먼저 명확히 해야 검토 기준이 생깁니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求先明確後有檢視尺度的因果，以검토 기준自然表達。 |
| ko | v40053 | caption | 換成兩分三人，正確順序也是一、一、零。 | 2센트를 세 명에게 나눠도 순서는 1, 1, 0입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2 cents、三人、1/1/0與正確順序都保留。 |
| ko | v40056 | caption | 第二關，打開實際差異，不只讀工具的完成訊息。 | 둘째 단계는 완료 보고가 아니라 실제 변경 내역을 엽니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二關須讀實際變更而不只完成摘要，語義不變。 |
| ko | v40057 | caption | 先確認它只改到預期的程式和測試。 | 예상한 코드와 테스트만 수정했는지 먼저 확인합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只改預期程式和測試的範圍限制清楚。 |
| ko | v40058 | caption | 接著把新增邏輯代入一百分除三的例子。 | 새 로직에 100센트를 세 명에게 나누는 사례를 대입합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新邏輯代入100 cents給三人的例子，數字與步驟保留。 |
| ko | v40059 | caption | 最後看它有沒有刪掉原來的保護條件。 | 기존의 보호 조건을 삭제하지 않았는지도 봅니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 確認是否刪去原有保護條件，沒有直接指控本patch已刪除。 |
| ko | v40060 | caption | 文字摘要可能遺漏細節，差異本身才是檢查對象。 | 요약에는 빠진 내용이 있을 수 있습니다. 변경 자체를 봐야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 摘要可能漏細節，因此要讀變更本身，可能性與因果未改。 |
| ko | v40063 | caption | 這份修補先算每人最少要拿多少。 | 이 수정안은 먼저 각자의 기본 몫을 계산합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先算基本份額對應Math.floor所給每人最低份額，未翻成平均四捨五入。 |
| ko | v40064 | caption | 再算剩下幾分，要補給幾位前面的人。 | 그다음 남은 센트를 앞의 몇 명에게 줄지 계산합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 剩餘cent與前面幾人得到額外份額的兩個計算保留。 |
| ko | v40065 | caption | 總額一百，分給三人，各拿三十三，還剩一分錢。 | 100센트를 셋이 나누면 33씩 받고 1센트가 남습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100 cents、三人、每人33、餘1 cent均正確。 |
| ko | v40066 | caption | 第一位多拿一分，其餘兩位維持三十三。 | 첫째가 1센트를 더 받고, 나머지 둘은 33센트입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一位多1 cent，其餘兩位33 cents，數字與角色無誤。 |
| ko | v40067 | caption | 用兩分三人再代一次，就能看到前兩位各多一分。 | 2센트를 세 명에게 대입하면 앞의 둘이 1센트씩 받습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 以2 cents給三人再代入，前兩位各1 cent；基礎份額為0的語境成立。 |
| ko | v4e3000 | caption | 完整差異顯示，函式前兩段輸入檢查仍然保留。 | 전체 변경 내역에서 함수 시작 부분의 두 입력 검사가 그대로 남아 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 전체 변경 내역에서 states what the complete diff shows. 함수 시작 부분의 두 입력 검사 locates both guards inside the beginning of the function, matching fare.mjs and the preserved patch. 그대로 남아 있습니다 retains the unchanged-guard claim. The following line still says illegal amount/people are rejected before allocation. |
| ko | v4e3001 | caption | 非法金額和非法人數，仍會在分配前被擋。 | 잘못된 금액과 인원수는 여전히 분배 전에 거부합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不合法金額、人數仍在分配前被拒絕，先後與持續性保留。 |
| ko | v4e3002 | caption | 這份修補把平均四捨五入，換成基本分與餘數。 | 이 수정안은 평균을 반올림하는 방식 대신 기본 몫과 나머지를 계산합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 平均四捨五入改為基本份額與餘數，對應patch兩個新計算。 |
| ko | v4e3003 | caption | 這是這份本地差異的範圍，不替其他檔案背書。 | 이 로컬 변경의 범위일 뿐, 다른 파일까지 보증하지는 않습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 此本地差異的范围及不能替其他檔案保證兩層限制都保留。 |
| ko | v40070 | caption | 我在差異裡先找原有驗證，這次沒有被刪掉。 | 변경 내역에서 기존 검사를 먼저 찾았고 삭제되지 않았습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 確實查看舊檢查且本次未刪，past tense與保留patch相符。 |
| ko | v40071 | caption | 再看檔案清單，只有程式和測試被修改。 | 파일 목록도 확인했습니다. 코드와 테스트만 바뀌었습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 程式與測試兩類檔案被改，실제完成語氣未降成假設。 |
| ko | v40072 | caption | 新增測試涵蓋不整除、零金額和非法輸入。 | 새 테스트는 나머지, 0센트, 잘못된 입력을 다룹니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新增測試涵蓋餘數、0 cents、非法輸入，三類都在。 |
| ko | v40073 | caption | 這些都是看得見的證據，不是工具的口頭保證。 | 눈으로 확인할 수 있는 증거이지 도구의 말뿐인 보증이 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可見證據與工具口頭保證的區別清楚，未增添工具作者。 |
| ko | v40074 | caption | 如果它順手改了部署或帳務設定，應該另外討論。 | 배포나 회계 설정까지 바꿨다면 따로 논의해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若改到部署或會計設定應另議，-다면保留假設。 |
| ko | v40075 | caption | 新增測試也要看斷言，不只看測試名稱。 | 새 테스트는 이름뿐 아니라 단언 내용도 봐야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 測試名稱以外也須讀斷言，단언與相關三句使用一致。 |
| ko | v4e4000 | caption | 新增測試不能只看名字，要看它到底斷言什麼。 | 새 테스트는 이름만 보지 말고 실제로 무엇을 단언하는지 확인해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新測試不能只看名稱而要確認實際斷言，沒有把數量當驗收。 |
| ko | v4e4001 | caption | 這份修補測到一百分除三，是三十四、三十三、三十三。 | 100센트를 세 명에게 34, 33, 33으로 나누는지 봅니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100 cents給三人34/33/33與實際patch assertion相符。 |
| ko | v4e4002 | caption | 也測到兩分分五人，前兩位各一分，其餘拿零。 | 2센트를 다섯 명에게 나눠 앞의 둘은 1씩, 나머지는 0인지 봅니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2 cents給五人，前兩位各1，其餘0，與patch的1/1/0/0/0一致。 |
| ko | v4e4003 | caption | 這兩組一起看，比只看測試數量更有意義。 | 테스트 개수보다 이 두 사례를 함께 보는 편이 유용합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩個案例合看比只數測試有用，建議未改成產品量測結論。 |
| ko | v40077 | caption | 這裡展示的是本地修補，不是假裝已有人核准的 PR。 | 여기서는 승인된 PR인 척하지 않고 로컬 수정안을 보여줍니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地修補與不得裝成已核准PR的界線明確，PR原拼寫保留。 |
| ko | v40078 | caption | 真正的專案還要看相關模組、型別與維運影響。 | 실제 프로젝트라면 관련 모듈, 타입, 운영 영향도 봐야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 實際專案另看模組、型別與營運影響，範圍沒有遺漏。 |
| ko | v40079 | caption | 如果這段程式連著付款系統，範圍會更大。 | 이 코드가 결제 시스템과 연결된다면 검토 범위는 더 커집니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 付款系統連接是條件式，沒有聲稱本示範已整合付款系統。 |
| ko | v40080 | caption | 影片示範的方法，可以帶進真正的審查流程。 | 영상의 방법을 실제 검토 과정에도 적용할 수 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 影片方法可用於真實審查，是可用性建議而非已執行真實PR。 |
| ko | v40081 | caption | 我把這個範圍明確標出，避免觀眾以為是真實核准。 | 실제 승인 사례로 오해하지 않도록 범위를 명시했습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 明示範圍以免誤當真實核准，過去式符合本片已標明範圍。 |
| ko | v40084 | caption | 第三關，把修補放進另外寫的事後驗收。 | 셋째 단계는 별도로 작성한 사후 검증에 수정안을 넣습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三關是另寫的事後驗收，沒有誤說修補前已獨立盲測。 |
| ko | v40085 | caption | 工具自己寫的測試有用，但不能是唯一標準。 | 도구의 자체 테스트는 유용하지만 유일한 기준은 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 工具自有測試有用但不應為唯一基準，一般性建議不證明這份patch作者。 |
| ko | v40086 | caption | 好的驗收測試，應該先在舊版程式重現這個錯誤。 | 좋은 사후 검증은 먼저 기존 코드에서 이 버그를 재현해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 好驗收應先對旧碼重現錯誤，first與should皆保留。 |
| ko | v40087 | caption | 所以我先拿舊碼跑同一份事後驗收。 | 그래서 같은 사후 검증을 기존 코드에 먼저 실행했습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同一份事後驗收已先在旧碼執行，明確完成式。 |
| ko | v40088 | caption | 理想順序是先讓驗收能重現舊錯，再評估新修補。 | 먼저 기존 오류를 재현하고 그다음 새 수정안을 평가합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先重現舊錯再評新修補，步驟順序保留。 |
| ko | v40091 | caption | 舊碼雖然兩個原測試全過，事後四類只過一類。 | 기존 테스트 2개는 통과했지만 사후 검증 4종 중 1종만 통과했습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩個舊測試通過及事後四類只過一類，2、4、1均準確。 |
| ko | v40092 | caption | 這證明新驗收能抓到我們要修的缺陷。 | 새 검증이 고치려는 결함을 잡아낸다는 뜻입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新驗收能抓到待修缺陷的结論保留，未增添全域正確證明。 |
| ko | v40093 | caption | 換成修補後，四類事後驗收全通過。 | 수정안으로 바꾼 뒤 사후 검증 4종이 모두 통과했습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補後事後四類全部通過，完成式与4/4相符。 |
| ko | v40094 | caption | 這才是比較有力的紅燈到綠燈證據。 | 그것이 더 강한 실패에서 통과로의 전환 증거입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 由失敗到通過是更有力證據，保留比較建議而非工具性能排名。 |
| ko | v40095 | caption | 這一步能排除只檢查舊有整除案例的假安全感。 | 기존의 나누어떨어지는 사례만 검사한 데서 오는 잘못된 안도감을 없앱니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 排除僅測既有整除案例造成的假安全感，案例范围保留。 |
| ko | v40098 | caption | 驗收不是只寫一百除三。 | 사후 검증은 100을 3으로 나누는 사례뿐이 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 事後驗收不只100/3，否定語意未變。 |
| ko | v40099 | caption | 我還把零到五百的總額，搭配一到二十人跑過。 | 금액 0부터 500까지, 인원수 1부터 20까지 조합했습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 已組合金額0至500與人數1至20，端點和實際完成式保留。 |
| ko | v40100 | caption | 每組都檢查總和，並確認最大差距不超過一分。 | 각 조합의 합계와 최대 몫 차이가 1센트 이하인지 봅니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 逐組檢查總和與最大份額差距不超1 cent，兩個條件及上限準確。 |
| ko | v40101 | caption | 這種性質檢查，能抓到你沒想到的餘數組合。 | 이런 성질 검사는 미처 생각 못 한 나머지 조합도 찾습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 性質檢查能找出未預想到的餘數組合，未聲稱所有可能輸入已涵蓋。 |
| ko | v40102 | caption | 實際回圈涵蓋大量組合，但仍不是形式化證明。 | 반복문으로 많은 조합을 봤지만 형식적 증명은 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 實際回圈看過多組但不是形式化證明，完成語氣和限制完整。 |
| ko | v40103 | caption | 超出測試範圍的風險，要再根據業務補案例。 | 테스트 범위 밖 위험에는 업무에 맞는 사례를 더해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 測試範圍以外風險需按業務補案例，未誤稱已補全。 |
| ko | v4shot0 | caption | 這是同一份修補在本機跑出的驗收輸出。 | 같은 수정안을 로컬에서 실행한 검증 출력입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同一份修補在本機執行的驗收輸出，沒有把重排圖片稱原始终端截圖。 |
| ko | v4shot1 | caption | 四項綠燈有紀錄，但還要對照需求與完整差異。 | 검증 4종의 통과 기록도 요구 사항과 전체 변경에 대조해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四類通過仍需與需求及完整差異對照，4與完整限制保留。 |
| ko | v4e5000 | caption | 回圈跑每組數字時，不只看總額。 | 반복문은 각 숫자 조합에서 합계만 보지 않습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 每組數字不只檢查總額，否定未反轉。 |
| ko | v4e5001 | caption | 它還比對輸出長度，確認沒有漏掉任何人。 | 결과 길이를 비교해 빠진 사람이 없는지도 봅니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 比對結果長度以免漏人，實際長度assert保留。 |
| ko | v4e5002 | caption | 再找最大和最小份額，差距不能超過一。 | 최대 몫과 최소 몫의 차이도 1을 넘지 않아야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 最大最小份額差不得超1，与actualassert相符。 |
| ko | v4e5003 | caption | 這三個斷言對每組資料都成立，才算這關通過。 | 각 조합에서 이 세 단언이 모두 성립해야 통과입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 每組都須三個斷言成立才通過，三與all兩個條件準確。 |
| ko | v40105 | caption | 零金額要回傳每人零分，不能拋出莫名錯誤。 | 총액이 0이면 모두에게 0을 돌려줘야지 엉뚱한 오류를 내면 안 됩니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 總額0則每人0、不可無故拋錯，return與throw對照清楚。 |
| ko | v40106 | caption | 負數、小數或超大總額，仍然要被拒絕。 | 음수, 소수, 지나치게 큰 총액도 계속 거부해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 負數、小數與過大總額仍拒絕，三類及持續規則保留。 |
| ko | v40107 | caption | 零人、超過一百人和小數人數也是一樣。 | 인원수 0, 100 초과, 소수도 마찬가지입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 0人、超100人、非整數人數同樣拒絕，0和100門檻未改。 |
| ko | v40108 | caption | 回歸的意思，就是修新 Bug 也守住舊契約。 | 회귀 검증은 새 버그를 고치면서 기존 규칙도 지키는 겁니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回歸檢查保護既有規則的意思正確，회귀 검증用語一致；겁니다是正式禮貌語尾縮寫。 |
| ko | v40109 | caption | 輸入驗證也可能在重寫時被無意刪掉。 | 입력 검증도 코드를 다시 작성할 때 실수로 삭제될 수 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 重寫時可能誤刪輸入驗證，가능성 -수 있습니다未誇大成最常發生。 |
| ko | v40112 | caption | 把需求、程式差異和回歸測試一起看。 | 요구 사항, 변경 내역, 회귀 테스트를 함께 확인해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求、變更、回歸測試要合看，三類證據清楚。 |
| ko | v40113 | caption | 需求契約告訴你什麼叫修好。 | 요구 사항은 무엇이 수정 완료인지 알려줍니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求界定何謂修好，以수정 완료呈現完成標準而非工具保證。 |
| ko | v40114 | caption | 差異讓你知道實際改了哪些檔、哪些行。 | 변경 내역은 실제로 바뀐 파일과 줄을 보여줍니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 差異顯示實際變更檔案與行，兩個对象均在。 |
| ko | v40115 | caption | 回歸則證明新舊規則至少在測試範圍內成立。 | 회귀 검증은 테스트 범위에서 새 규칙과 기존 규칙을 확인합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回歸只在測試範圍確認新舊規則，범위限制未丟失。 |
| ko | v40116 | caption | 只缺一道關，審查紀錄就不完整。 | 한 단계라도 빠지면 검토 기록이 불완전합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 缺任一關則紀錄不完整，any與不足語意完整。 |
| ko | v40119 | caption | 我會在審查紀錄裡放三件事。 | 저는 검토 기록에 세 가지를 넣습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱저는及將放三件事均明確，保留編輯建議立場。 |
| ko | v40120 | caption | 第一，需求有哪些明確的驗收條件。 | 첫째, 요구 사항의 명확한 검증 조건입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一項明確驗收條件，검증 조건符合前文後設驗收語境。 |
| ko | v40121 | caption | 第二，實際差異只改了哪些地方。 | 둘째, 실제 변경이 어디에만 적용됐는지입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二項實際變更僅到哪些地方，어디에만保留範圍限定。 |
| ko | v40122 | caption | 第三，哪個測試先紅、修補後又如何變綠。 | 셋째, 어느 테스트가 먼저 실패했고 수정 후 통과했는지입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三項哪個測試先失败、修補後通過，先後方向完整。 |
| ko | v40123 | caption | 這三項可以寫進 PR 描述，讓審查者快速重跑。 | PR 설명에 쓰면 다음 검토자가 빨리 다시 실행할 수 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 三項可放PR描述讓審查者快速重跑，PR拼寫與可重跑目的保留。 |
| ko | v4e6000 | caption | 最後把那個原本失敗的案例寫在審查摘要裡。 | 마지막으로 처음 실패한 사례를 검토 요약에 넣습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 最後把原先失敗案例放入審查摘要，沒有變成只寫成功結果。 |
| ko | v4e6001 | caption | 附上完整差異，不只貼兩行好看的核心程式。 | 보기 좋은 핵심 두 줄 말고 전체 변경 내역을 붙입니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 要附完整差異而非只貼兩行核心，2與完整范围保留。 |
| ko | v4e6002 | caption | 再列出重跑指令與通過的測試範圍。 | 재실행 명령과 통과한 테스트 범위도 적습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 重跑命令及通過測試範圍都列出，未只要求命令。 |
| ko | v4e6003 | caption | 下一位審查者不必相信口頭報告，能自己驗證。 | 다음 검토자는 말만 믿지 않고 직접 확인할 수 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下一位可自己驗證而非信口頭報告，能力與對比保留。 |
| ko | v40126 | caption | 這個小型示範雖然通過驗收，仍不能代替真實業務判斷。 | 이 작은 시연은 검증을 통과했지만 실제 업무 판단을 대신할 수 없습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 小型示範已通過驗收但不可代替真實業務判斷，两個語意及完成式都在。 |
| ko | v40127 | caption | 需求若一開始寫錯，測試也可能跟著綠錯方向。 | 요구 사항부터 틀렸다면 테스트도 잘못된 방향으로 통과할 수 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求錯會讓測試沿錯誤方向通過的假設及可能性保留。 |
| ko | v40128 | caption | 還要有人看改動範圍、資料影響和回滾方式。 | 변경 범위, 데이터 영향, 되돌리는 방법도 사람이 봐야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 人仍需看變更範圍、資料影響與回滾，三個方面都在。 |
| ko | v40129 | caption | 負責合併的人，得對這個判斷負責。 | 병합 책임자가 그 판단을 책임져야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 合併責任者對判斷負責，沒有移轉給模型。 |
| ko | v40130 | caption | 合併不是模型替團隊作的事，而是負責者作的決定。 | 병합은 모델이 대신하지 않습니다. 책임자가 결정합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 模型不代為合併、責任人決定，團隊語境可由上下文承接，決策責任未丟失。 |
| ko | v40133 | caption | 在 GitHub 的正式流程裡，審查者可以對變更行留言。 | GitHub 정식 절차에서는 변경된 줄에 검토 댓글을 달 수 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | GitHub變更行可留言，GitHub正確拼寫，與保存官方來源支持的流程一致。 |
| ko | v40134 | caption | 也可以要求修改，或在看過證據後核准。 | 수정을 요청하거나 증거를 보고 승인할 수도 있습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可要求修改或看到證據後批准，兩種動作及證據條件保留。 |
| ko | v40135 | caption | 這裡不替任何真實 PR 點核准。 | 여기서는 실제 PR을 승인하지 않습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 這裡不批准實際PR，否定與範圍完整。 |
| ko | v40136 | caption | 重點是讓下一位審查者找到同一份證據。 | 핵심은 다음 검토자가 같은 증거를 찾게 하는 겁니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下一位可找到同一證據，같은保留一致性；겁니다維持禮貌敘述。 |
| ko | v40137 | caption | 影片畫面展示規則，不會用別人的 PR 當裝飾。 | 영상에는 규칙을 보여주며 남의 PR을 장식으로 쓰지 않습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 畫面示規則、不用他人PR裝飾，兩項都保留。 |
| ko | v40140 | caption | 回到開頭：AI 修好 Bug，測試綠了，能直接合併嗎？ | 처음 질문입니다. AI가 버그를 고쳐 테스트도 통과했다면 바로 병합해도 됩니까? | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回到AI修bug測試通過能否直接合併的教學問句，未聲稱本patch已查證AI作者。 |
| ko | v40141 | caption | 先過需求、差異、回歸這三道關，再由人作最後判斷。 | 요구 사항, 변경, 회귀 검증을 거친 뒤 사람이 최종 판단합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求、差異、回歸三關後由人最終判斷，順序及責任完整。 |
| ko | v40142 | caption | 這次的起始碼、修補和測試，要放在一起核對。 | 이번 시작 코드, 수정안, 테스트를 한데 놓고 대조해야 합니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 開始碼、修補、測試三者合核對，未要求只信其中一者。 |
| ko | v40143 | caption | 拿你下一個小修補照著試一次，比背規則更有用。 | 다음 작은 수정에 직접 적용해 보십시오. 규칙을 외우는 것보다 낫습니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下一次小修補實際練習比背規則有用，보십시오保留正式禮貌指示。 |
| ko | v40144 | caption | 這個小練習之後，再把同一方法用到較大的改動。 | 그 연습 뒤에는 더 큰 변경에도 같은 방법을 사용하십시오. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先小練習再較大改動使用同方法，順序及same-method語意保留。 |
| ko | title | metadata | AI 修好 Bug 就能合併？三個 PR 檢查點 | AI가 버그를 고쳤다면 바로 병합할까? PR 검토 3단계 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 31個字元、不超100、無尖括號；AI與PR拼寫正確，保留合併問句與三階段檢視主題。 |
| ko | description | metadata | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。 | 기존 테스트 두 개는 모두 통과했지만 100센트를 나눴더니 합계는 99센트뿐이었습니다. 실제 수정과 테스트를 따라가며 병합 전에 요구 사항, 변경 내역, 회귀 여부를 확인하는 방법을 배웁니다.<br>이 시연은 로컬에서 다시 실행할 수 있는 사례이며, 운영 사이트의 사고나 이미 병합된 PR이 아닙니다. | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 保留兩測試全過卻100/99、實際修補/測試、需求/差異/回歸及本地非正式事故/非已合併PR全部限定；過去式正確。 |
| ko | tags:0 | metadata | AI code review | AI 코드 리뷰 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI原拼寫及code review以本地常用코드 리뷰呈現，符合可搜尋通用詞。 |
| ko | tags:1 | metadata | PR review | PR 리뷰 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | PR原拼寫與리뷰為常用搭配，無錯誤產品或模型名。 |
| ko | tags:2 | metadata | Bug fix | 버그 수정 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | Bug為通用術語버그，수정對應fix；不是產品名稱轉写。 |
| ko | tags:3 | metadata | 程式碼審查 | 코드 검토 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 程式碼審查以코드 검토表達，語意準確且可搜尋。 |
| ko | tags:4 | metadata | 回歸測試 | 회귀 테스트 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 회귀 테스트為回歸測試的常用韓文術語，與內文回歸検증不矛盾。 |
| ko | chapter:opening | metadata | 綠燈也會漏 | 테스트가 통과해도 놓치는 것 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 測試通過仍會漏東西，保留綠燈隱喻的教學意思。 |
| ko | chapter:why-green | metadata | 綠燈不等於正確 | 통과가 정답은 아닙니다 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 通過不等於正確，章節名清楚且未宣稱本測試失敗。 |
| ko | chapter:gate-one | metadata | 第一關：需求契約 | 1단계: 요구 사항 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一階段需求事項，契約在此是需求條件集合，以요구 사항自然保留主題。 |
| ko | chapter:gate-two | metadata | 第二關：讀差異 | 2단계: 변경 내역 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二階段讀實際變更，章節短題保留diff語義。 |
| ko | chapter:gate-three | metadata | 第三關：跑回歸 | 3단계: 회귀 테스트 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三階段回歸測試，테스트保留跑驗收的行為與術語。 |
| ko | chapter:three-gates | metadata | 合併前的決定 | 병합 전 최종 판단 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 合併前最終判斷對應合併前決定，沒有變成已合併狀態。 |
| zh-CN | v40000 | caption | 三個人分一百分，舊測試全綠，結果卻只分出九十九。 | 三人分100分，旧测试全绿，结果却只分出99分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100分/3人的99分實際缺額與舊測試通過均保留。 |
| zh-CN | v40001 | caption | AI 送來一份修補程式，你會直接合併嗎？ | AI 交来一份补丁，你会直接合并吗？ | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI送來修補後的合併提問保留，未新增特定工具作者。 |
| zh-CN | v40002 | caption | 我帶你看需求、差異與回歸，三道關都要過。 | 我带你检查需求、代码差异和回归，这三关都要过。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求、差異、回歸三關及帶領檢查的敘述保留。 |
| zh-CN | v40003 | caption | 我們先從那一分為什麼消失開始。 | 先从那1分为什么不见了说起。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 一分缺額的因果引子保留，沒有更換幣別。 |
| zh-CN | v40007 | caption | 第一個舊測試，只檢查能整除的金額。 | 第一项旧测试只检查能够整除的金额。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一個舊測試只覆蓋可整除金額的範圍保留。 |
| zh-CN | v40008 | caption | 人數不合法也會擋，兩個結果都是綠色。 | 人数不合法也能拦住，两项测试都是绿灯。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非法人數被擋及兩項舊測試綠燈均維持實際結果語氣。 |
| zh-CN | v40009 | caption | 不整除的路徑沒人問，所以錯誤藏得好好的。 | 没人测试不能整除的情况，所以错误藏了起来。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 未涵蓋餘數路徑造成缺陷未被發現的因果保留。 |
| zh-CN | v40010 | caption | 這次示範是真正執行的檔案，不是想像案例。 | 这次示例用的是真实运行过的文件，不是想象的案例。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 實際執行本地檔案與想像案例的區別保留。 |
| zh-CN | v40011 | caption | 它證明程式照舊測試運作，沒有證明帳算對。 | 它只能证明代码通过旧测试，不能证明分账正确。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 通過舊測試不等於分帳正確的證據限制保留。 |
| zh-CN | v4e1000 | caption | 這是起始專案真的跑過的兩個測試。 | 这是起始项目实际跑过的两项测试。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 起始專案真正執行兩項測試的時態与數量保留。 |
| zh-CN | v4e1001 | caption | 第一個測一百二十分，三人平均分。 | 第一项测试120分由三人平分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 120分/3人平均分的數字與操作順序保留。 |
| zh-CN | v4e1002 | caption | 第二個測零人時要拋出錯誤。 | 第二项检查人数为零时会报错。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 零人應拋錯的斷言條件保留。 |
| zh-CN | v4e1003 | caption | 它們全綠，只能證明這兩件事，不能代表餘數正確。 | 两项都绿，只能证明这两点，不能说明余数处理正确。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩项通過不能證實餘數處理正確的限制保留。 |
| zh-CN | v40014 | caption | 分一百分給三個人，原始程式回三個三十三。 | 100分分给三人，原代码返回33、33、33。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原程式100分/3人回33、33、33的實際結果保留。 |
| zh-CN | v40015 | caption | 這不是顯示格式的問題，總和真的少了一分。 | 这不是显示格式问题，总额真的少了1分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 缺一分是總和問題而非顯示問題的因果保留。 |
| zh-CN | v40016 | caption | 如果少掉的一分錢會記入帳務，就算測試全綠也不能合併。 | 如果少掉的1分钱会影响账务，测试全绿也不能合并。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 帳務影響仍是如果條件，未說本例已有正式帳務事故。 |
| zh-CN | v40017 | caption | 接下來看一份可以重跑的本地修補。 | 接下来看一份可以重跑的本地修补。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 接著看可重跑本地修補的轉場與範圍保留。 |
| zh-CN | v40018 | caption | 這個失敗結果已寫進可重跑的驗收檔案。 | 这个失败案例已写进可重复运行的验收文件。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 失敗案例已被收入可重跑驗收檔案的實際時態保留。 |
| zh-CN | v40021 | caption | 這份本地分攤範例，留下了程式和測試的完整差異。 | 这份本地分摊示例，保留了程序和测试的完整差异。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地分攤例保留程式與測試完整差異，未新增Claude作者歸因。 |
| zh-CN | v40022 | caption | 修補後的九個測試重跑全過，稍後再做事後驗收。 | 修补后的九个测试重跑全过，稍后再做事后验收。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補後九項測試已通過、後續再做事後驗收的順序與時態保留。 |
| zh-CN | v40023 | caption | 這不是正式站的事故，也不是已合併的真實 PR。 | 这不是真实生产事故，也不是已合并的 PR。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非正式站事故、非已合併真實PR的兩項限制保留。 |
| zh-CN | v40024 | caption | 它是可以公開重跑的一份本地修補案例。 | 这是一份能公开重跑的本地修复案例。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地修補可供重跑的含義保留，未聲稱已部署或合併。 |
| zh-CN | v40025 | caption | 所以它適合用來練審查，卻不能代表產品事故。 | 适合练习代码审查，却不能当成产品事故。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 適合審查練習而不代表產品事故的範圍保留。 |
| zh-CN | v40028 | caption | 第一關，不要先看 AI 說它完成了什麼。 | 第一关，先别看 AI 声称完成了什么。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一關先不依賴AI完成訊息的編輯建議保留。 |
| zh-CN | v40029 | caption | 先把需求寫成你可以算得出來的條件。 | 先把需求写成自己也能算清楚的条件。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求寫成可自行算出的條件的建議保留。 |
| zh-CN | v40030 | caption | 這題要保留輸入規則，不能只修一個範例。 | 这道题要保留输入规则，不能只修一个例子。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 必須保留輸入規則、不可只修一例的契約保留。 |
| zh-CN | v40031 | caption | 也不能悄悄把分配規則改成另一種做法。 | 也不能悄悄换掉原来的分配规则。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 不能偷偷更換分配规则的限制保留。 |
| zh-CN | v40032 | caption | 第一關的答案，應該能不靠工具自己口述。 | 第一关的答案，不靠工具口述也应该说得清。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一關內容應能不用工具自行口述的意思保留。 |
| zh-CN | v40035 | caption | 第一條，結果長度要和人數一樣。 | 第一，输出数组长度要等于人数。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 輸出長度等於人數的第一條件保留。 |
| zh-CN | v40036 | caption | 第二條，所有人的份額加總，必須等於原來金額。 | 第二，所有人的份额加起来必须等于原金额。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 份額總和等於原金额的第二條件保留。 |
| zh-CN | v40037 | caption | 第三條，任何兩人最多只差一分。 | 第三，任意两人的份额最多差1分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 任意兩份額最多相差一分的上界保留。 |
| zh-CN | v40038 | caption | 第四條，有餘數時，前面的人先分到。 | 第四，有余数时，排在前面的人先拿到。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 餘數先配給前方位置的順序規則保留。 |
| zh-CN | v40039 | caption | 四條放在一起，才描述完整的分攤行為。 | 这四条放在一起，才完整描述分账规则。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四條合起來定義分攤行為的含義保留。 |
| zh-CN | v40040 | caption | 如果只補一百除三，還會漏掉其他金額。 | 只修100除以3，还会漏掉其他金额。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只修100/3會漏其他金額的反事實風險保留。 |
| zh-CN | v4e2000 | caption | 只測一百分除三，還可能把規則寫死在特例上。 | 只测100除以3，也可能把规则写死在这个特例。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只測100/3可能寫死特例的可能性語氣保留。 |
| zh-CN | v4e2001 | caption | 再代入兩分給三個人，正確是前兩位各一分。 | 再试2分分给三人，前两人应该各拿1分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2分/3人前兩人各1分的需求值保留。 |
| zh-CN | v4e2002 | caption | 第三位拿零分，總和仍是兩分。 | 第三人拿0分，总和仍是2分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三人0分、總和仍2分的數字與順序保留。 |
| zh-CN | v4e2003 | caption | 這組資料會立刻露出四捨五入重複分配的問題。 | 这组数据很快就能暴露四舍五入造成的重复分配问题。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四捨五入導致重複分配的因果關係保留。 |
| zh-CN | v40042 | caption | 還有原本就存在的輸入檢查。 | 还要保留起始代码已有的输入检查。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原有輸入檢查先前存在的含義保留。 |
| zh-CN | v40043 | caption | 總額不能是負數、小數或超過安全整數。 | 总额不能是负数、小数，也不能超过安全整数范围。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 拒絕負數、小數、超安全整數範圍三類金額保留。 |
| zh-CN | v40044 | caption | 人數只能是一到一百之間的安全整數。 | 人数只能是1到100之间的安全整数。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 人數為1至100的安全整數，上下界和整數性保留。 |
| zh-CN | v40045 | caption | 修補若刪掉這些檢查，就算範例變對也不能過關。 | 补丁如果删掉这些检查，就算示例正确也不能通过。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若刪檢查即使範例成功仍不得通過的條件保留。 |
| zh-CN | v40046 | caption | 它們不是額外加分題，而是修補前就有的規則。 | 它们不是加分项，而是修复前就有的规则。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 原有規則並非額外加分的意思保留。 |
| zh-CN | v40049 | caption | 把一百分除以三，理想結果是三十四、三十三、三十三。 | 100分分给三人，正确结果是34、33、33。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100分/3人的34、33、33需求結果保留。 |
| zh-CN | v40050 | caption | 這組數字同時檢查總和與餘數順序。 | 这组数同时检查总和与余数分配顺序。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同時檢查總和與餘數順序的兩重目的保留。 |
| zh-CN | v40051 | caption | 只測每個人差不多，還是不夠。 | 只看每个人分得差不多，还不够。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只看份額接近仍不足的限制保留。 |
| zh-CN | v40052 | caption | 需求契約先寫清楚，才有審查的尺。 | 先写清需求约束，审查才有依据。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先清楚寫需求契約才有審查準則的比喻保留。 |
| zh-CN | v40053 | caption | 換成兩分三人，正確順序也是一、一、零。 | 换成2分分给三人，正确顺序也是1、1、0。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2分/3人的1、1、0順序保留。 |
| zh-CN | v40056 | caption | 第二關，打開實際差異，不只讀工具的完成訊息。 | 第二关，打开实际代码差异，别只读工具的完成消息。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二關打開實際差異而非只讀完成訊息的建議保留。 |
| zh-CN | v40057 | caption | 先確認它只改到預期的程式和測試。 | 先确认它只改了预期中的代码和测试。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 確認只有預期程式與測試改動的範圍保留。 |
| zh-CN | v40058 | caption | 接著把新增邏輯代入一百分除三的例子。 | 再把100除以3代入新逻辑。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 把100/3代入新邏輯的操作保留。 |
| zh-CN | v40059 | caption | 最後看它有沒有刪掉原來的保護條件。 | 最后看它有没有删掉原来的保护条件。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 最後確認原保護條件仍在的檢查目的保留。 |
| zh-CN | v40060 | caption | 文字摘要可能遺漏細節，差異本身才是檢查對象。 | 文字摘要可能遗漏细节，要审查差异本身。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 摘要可能漏細節、須檢查實際差異的可能性與因果保留。 |
| zh-CN | v40063 | caption | 這份修補先算每人最少要拿多少。 | 这份补丁先算出每人至少拿多少。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補先求每人基本最低份額的算法意義保留。 |
| zh-CN | v40064 | caption | 再算剩下幾分，要補給幾位前面的人。 | 再算剩下几分，该补给前面几个人。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 再計算餘數及前方補配位置的意義保留。 |
| zh-CN | v40065 | caption | 總額一百，分給三人，各拿三十三，還剩一分錢。 | 总额100分，三人各拿33分，还剩1分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 100分給3人各33分、剩1分的數字保留。 |
| zh-CN | v40066 | caption | 第一位多拿一分，其餘兩位維持三十三。 | 第一人多拿1分，另两人仍是33。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人多1分、另兩人維持33的顺序保留。 |
| zh-CN | v40067 | caption | 用兩分三人再代一次，就能看到前兩位各多一分。 | 再代入2分分给三人，就能看到前两人各多拿1分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 2分給3人前兩人各獲1分的需求行為保留。 |
| zh-CN | v4e3000 | caption | 完整差異顯示，函式前兩段輸入檢查仍然保留。 | 完整代码差异显示，函数前两段输入检查仍然保留。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 完整差異中前兩段輸入檢查仍保留的實際描述保留。 |
| zh-CN | v4e3001 | caption | 非法金額和非法人數，仍會在分配前被擋。 | 非法金额和人数，仍会在分配前被拦住。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 非法金額和人數於分配前被擋的顺序保留。 |
| zh-CN | v4e3002 | caption | 這份修補把平均四捨五入，換成基本分與餘數。 | 这份修补把平均四舍五入，换成基本份额与余数。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 平均四捨五入改成基本份額加餘數的算法差異保留。 |
| zh-CN | v4e3003 | caption | 這是這份本地差異的範圍，不替其他檔案背書。 | 这只是本地差异的范围，不代表其他文件也没问题。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 只代表這份本地差異、不為其他檔背書的範圍保留。 |
| zh-CN | v40070 | caption | 我在差異裡先找原有驗證，這次沒有被刪掉。 | 我先找原有校验，这次没有被删除。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱確認原驗證未被刪除的實際結果保留。 |
| zh-CN | v40071 | caption | 再看檔案清單，只有程式和測試被修改。 | 再看文件清单，只有代码和测试被修改。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 檔案清單只有程式與測試改動的實際範圍保留。 |
| zh-CN | v40072 | caption | 新增測試涵蓋不整除、零金額和非法輸入。 | 新测试涵盖不能整除、零金额和非法输入。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新增測試覆蓋不整除、零額、非法輸入三類保留。 |
| zh-CN | v40073 | caption | 這些都是看得見的證據，不是工具的口頭保證。 | 这些是看得见的证据，不是工具口头保证。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可見證據而非工具口頭保證的意思保留。 |
| zh-CN | v40074 | caption | 如果它順手改了部署或帳務設定，應該另外討論。 | 如果它顺手改了部署或账务设置，就得另行讨论。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 部署或帳務改動仍是如果條件，須另議而非宣稱本例發生。 |
| zh-CN | v40075 | caption | 新增測試也要看斷言，不只看測試名稱。 | 看新增测试，还要看断言，不只看测试名。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需讀斷言而非只看測試名稱的建議保留。 |
| zh-CN | v4e4000 | caption | 新增測試不能只看名字，要看它到底斷言什麼。 | 新增测试不能只看名字，要看它实际断言了什么。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新增測試需辨認實際斷言內容的意思保留。 |
| zh-CN | v4e4001 | caption | 這份修補測到一百分除三，是三十四、三十三、三十三。 | 这份补丁测试100分分给三人，结果是34、33、33。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補測試100/3得到34、33、33的實際斷言保留。 |
| zh-CN | v4e4002 | caption | 也測到兩分分五人，前兩位各一分，其餘拿零。 | 还测试2分分给五人：前两人各1分，其余为0。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補測試2分/5人前兩1分其餘0的實際斷言保留。 |
| zh-CN | v4e4003 | caption | 這兩組一起看，比只看測試數量更有意義。 | 两组放在一起，比只看测试数量更有意义。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 兩組具体案例比純數量更有證據力的編輯建議保留。 |
| zh-CN | v40077 | caption | 這裡展示的是本地修補，不是假裝已有人核准的 PR。 | 这里展示的是本地补丁，不是冒充已获批准的 PR。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本地修補非已有人核准的真實PR，未虛構正式核准。 |
| zh-CN | v40078 | caption | 真正的專案還要看相關模組、型別與維運影響。 | 真正的项目还得看相关模块、类型和运维影响。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 真實專案應擴看模組、型別、維運三類影响保留。 |
| zh-CN | v40079 | caption | 如果這段程式連著付款系統，範圍會更大。 | 如果这段代码连接支付系统，审查范围会更大。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 連付款系統時才擴大範圍的條件保留。 |
| zh-CN | v40080 | caption | 影片示範的方法，可以帶進真正的審查流程。 | 视频示范的方法，可以用到真正的代码审查。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 方法可帶入真實審查的編輯建議保留。 |
| zh-CN | v40081 | caption | 我把這個範圍明確標出，避免觀眾以為是真實核准。 | 我明确标注示例范围，避免观众误以为是真实批准。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱標示範圍以免誤認核准的意圖保留。 |
| zh-CN | v40084 | caption | 第三關，把修補放進另外寫的事後驗收。 | 第三关，把补丁放进另写的事后验收测试。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三關使用另外於事後寫成的驗收，未改稱事前盲測。 |
| zh-CN | v40085 | caption | 工具自己寫的測試有用，但不能是唯一標準。 | 工具自写的测试有用，但不能是唯一标准。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 工具自寫測試只能是部分標準，未歸因特定歷史工具。 |
| zh-CN | v40086 | caption | 好的驗收測試，應該先在舊版程式重現這個錯誤。 | 好的验收测试，应先在旧代码上复现这个错误。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 好的驗收應先在舊碼重現同一缺陷的建議順序保留。 |
| zh-CN | v40087 | caption | 所以我先拿舊碼跑同一份事後驗收。 | 所以我先用旧代码运行同一份事后验收。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱已先用舊碼跑同一事後驗收的實際順序保留。 |
| zh-CN | v40088 | caption | 理想順序是先讓驗收能重現舊錯，再評估新修補。 | 理想顺序是先复现旧错误，再评估新补丁。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 理想先重現舊錯、再評估新修補的編輯建議保留。 |
| zh-CN | v40091 | caption | 舊碼雖然兩個原測試全過，事後四類只過一類。 | 旧代码虽然两项原测试全过，事后4类只过1类。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 舊2/2通過、事後4類只過1類的對照數字保留。 |
| zh-CN | v40092 | caption | 這證明新驗收能抓到我們要修的缺陷。 | 这说明新验收能抓到我们要修的缺陷。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 新驗收捕捉欲修缺陷的證據含義保留，未擴成完全正確。 |
| zh-CN | v40093 | caption | 換成修補後，四類事後驗收全通過。 | 换成补丁后，事后4类验收全部通过。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 修補四類事後驗收全部通過的實際結果保留。 |
| zh-CN | v40094 | caption | 這才是比較有力的紅燈到綠燈證據。 | 这才是更有力的从红灯到绿灯的证据。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 紅到綠證據比較有力的相對編輯判斷保留。 |
| zh-CN | v40095 | caption | 這一步能排除只檢查舊有整除案例的假安全感。 | 它能消除只测原有整除案例带来的虚假安全感。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 避免只看整除舊例造成假安心的目的保留。 |
| zh-CN | v40098 | caption | 驗收不是只寫一百除三。 | 验收不只测100除以3。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 驗收不僅是100/3单例的範圍保留。 |
| zh-CN | v40099 | caption | 我還把零到五百的總額，搭配一到二十人跑過。 | 我还跑了0到500分的总额，搭配1到20人。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人稱已跑總額0至500、1至20人的范围保留。 |
| zh-CN | v40100 | caption | 每組都檢查總和，並確認最大差距不超過一分。 | 每组都检查总和，并确认最大差额不超过1分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 每組總和及最大差額不超1分的兩項斷言保留。 |
| zh-CN | v40101 | caption | 這種性質檢查，能抓到你沒想到的餘數組合。 | 这种性质检查能抓到意料之外的余数组合。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 性質檢查可抓未想到餘数组合的功能保留。 |
| zh-CN | v40102 | caption | 實際回圈涵蓋大量組合，但仍不是形式化證明。 | 实际循环覆盖很多组合，但仍不是形式化证明。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 大量組合仍不是形式化證明的限制保留。 |
| zh-CN | v40103 | caption | 超出測試範圍的風險，要再根據業務補案例。 | 超出测试范围的风险，还得按业务补充案例。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 超出範圍風險需按業務補例的建議保留。 |
| zh-CN | v4shot0 | caption | 這是同一份修補在本機跑出的驗收輸出。 | 这是同一份补丁在本机跑出的验收输出。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 同一修補在本機實際執行的驗收輸出，未稱原始錄影或正式站。 |
| zh-CN | v4shot1 | caption | 四項綠燈有紀錄，但還要對照需求與完整差異。 | 有4项绿灯的记录，但还要对照需求和完整差异。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 四類绿灯有紀錄但仍需對照完整差異與需求的限制保留。 |
| zh-CN | v4e5000 | caption | 回圈跑每組數字時，不只看總額。 | 循环跑每组数据时，不只检查总额。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回圈逐组不只看總額的檢查範圍保留。 |
| zh-CN | v4e5001 | caption | 它還比對輸出長度，確認沒有漏掉任何人。 | 还核对输出长度，确认没有漏掉任何人。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 檢查輸出長度以避免漏人的目的保留。 |
| zh-CN | v4e5002 | caption | 再找最大和最小份額，差距不能超過一。 | 再看最大和最小份额，差距不能超过1分。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 最大与最小份额差距不超1，維持分攤單位与上界。 |
| zh-CN | v4e5003 | caption | 這三個斷言對每組資料都成立，才算這關通過。 | 三项断言在每组数据上都成立，这关才算通过。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 每組三項斷言都成立才過关的全稱條件保留。 |
| zh-CN | v40105 | caption | 零金額要回傳每人零分，不能拋出莫名錯誤。 | 零金额时每个人都应拿到0，不能莫名报错。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 零額每人应为0且不应无故抛错的契约保留。 |
| zh-CN | v40106 | caption | 負數、小數或超大總額，仍然要被拒絕。 | 负数、小数或过大的总额，仍要被拒绝。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 负数、小数、超大总额仍需拒绝的回归要求保留。 |
| zh-CN | v40107 | caption | 零人、超過一百人和小數人數也是一樣。 | 人数为零、超过100或不是整数，也一样要被拒绝。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 0人、超100人、小数人数三类非法输入保留。 |
| zh-CN | v40108 | caption | 回歸的意思，就是修新 Bug 也守住舊契約。 | 回归的意思，是修新 Bug 时也要守住旧规则。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回归明确是测试旧契约未被新Bug修补破坏，非统计回归或重跑泛称。 |
| zh-CN | v40109 | caption | 輸入驗證也可能在重寫時被無意刪掉。 | 输入验证也可能在重写时被无意删掉。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 输入验证可能意外被删的可能性保留，未恢复缺证的相对频率主张。 |
| zh-CN | v40112 | caption | 把需求、程式差異和回歸測試一起看。 | 把需求、代码差异和回归测试放在一起看。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求、程序差异、回归测试三类证据合看保留。 |
| zh-CN | v40113 | caption | 需求契約告訴你什麼叫修好。 | 需求约束告诉你什么叫修好。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需求契约界定何为修好的意思保留。 |
| zh-CN | v40114 | caption | 差異讓你知道實際改了哪些檔、哪些行。 | 代码差异让你知道实际改了哪些文件、哪些行。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 差异说明实际修改的文件和行，未省去具体范围含义。 |
| zh-CN | v40115 | caption | 回歸則證明新舊規則至少在測試範圍內成立。 | 回归测试说明新旧规则至少在测试范围内成立。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回归只证明在测试范围内成立，保留有限证明范围。 |
| zh-CN | v40116 | caption | 只缺一道關，審查紀錄就不完整。 | 少一道关，审查记录就不完整。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 缺一关导致记录不完整的编辑方法保留。 |
| zh-CN | v40119 | caption | 我會在審查紀錄裡放三件事。 | 我会在审查记录里放三件事。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一人称安排三项审查记录的意思保留，未制造正式PR记录。 |
| zh-CN | v40120 | caption | 第一，需求有哪些明確的驗收條件。 | 第一，需求有哪些明确的验收条件。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 首项明确验收条件的记录范围保留。 |
| zh-CN | v40121 | caption | 第二，實際差異只改了哪些地方。 | 第二，实际差异只改了哪些地方。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二项记录实际差异的改动范围保留。 |
| zh-CN | v40122 | caption | 第三，哪個測試先紅、修補後又如何變綠。 | 第三，哪个测试先红，修复后又怎样变绿。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三项记录测试先失败后成功的顺序保留。 |
| zh-CN | v40123 | caption | 這三項可以寫進 PR 描述，讓審查者快速重跑。 | 把这三项写进 PR 描述，审查者就能快速重跑。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 可写入PR描述供他人重跑的建议保留，未称已有真实PR。 |
| zh-CN | v4e6000 | caption | 最後把那個原本失敗的案例寫在審查摘要裡。 | 最后，在审查摘要里写明原本失败的案例。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 摘要记下原失败案例的建议保留。 |
| zh-CN | v4e6001 | caption | 附上完整差異，不只貼兩行好看的核心程式。 | 附上完整差异，别只贴两行好看的核心代码。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 提供完整差异而非仅两行核心代码的范围保留。 |
| zh-CN | v4e6002 | caption | 再列出重跑指令與通過的測試範圍。 | 再列出重跑命令和通过的测试范围。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 列出重跑命令和通过的测试范围的建议保留。 |
| zh-CN | v4e6003 | caption | 下一位審查者不必相信口頭報告，能自己驗證。 | 下一位审查者能亲自验证，不必相信口头报告。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 后继审查者可独立验证而非只信口头报告的因果保留。 |
| zh-CN | v40126 | caption | 這個小型示範雖然通過驗收，仍不能代替真實業務判斷。 | 这个小示例虽然通过验收，仍不能代替真实业务判断。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 小型验收通过仍不能代替业务判断的限制保留。 |
| zh-CN | v40127 | caption | 需求若一開始寫錯，測試也可能跟著綠錯方向。 | 如果一开始需求写错，测试也可能沿着错方向通过。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 若需求错误则测试可能错向通过的条件和可能性保留。 |
| zh-CN | v40128 | caption | 還要有人看改動範圍、資料影響和回滾方式。 | 还得有人检查改动范围、数据影响和回滚方式。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 需人检查范围、数据影响、回滚三个领域保留。 |
| zh-CN | v40129 | caption | 負責合併的人，得對這個判斷負責。 | 负责合并的人，要对这个判断负责。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 合并者应承担判断责任的含义保留。 |
| zh-CN | v40130 | caption | 合併不是模型替團隊作的事，而是負責者作的決定。 | 合并不是模型替团队决定，而是责任人的决定。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 模型不代替团队负责者决定合并的责任归属保留。 |
| zh-CN | v40133 | caption | 在 GitHub 的正式流程裡，審查者可以對變更行留言。 | 在 GitHub 的正式流程中，审查者能对改动行留言。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | GitHub审查者可评论变更行，产品拉丁拼写和能力范围保留。 |
| zh-CN | v40134 | caption | 也可以要求修改，或在看過證據後核准。 | 也可以要求修改，或看过证据后批准。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 要求修改或阅证后批准，两种选择和证据顺序保留。 |
| zh-CN | v40135 | caption | 這裡不替任何真實 PR 點核准。 | 这里不批准任何真实 PR。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 本示范不对真实PR执行批准，未虚构实际动作。 |
| zh-CN | v40136 | caption | 重點是讓下一位審查者找到同一份證據。 | 重点是让下一位审查者找到同一份证据。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 下一位审查者找到相同证据的目的保留。 |
| zh-CN | v40137 | caption | 影片畫面展示規則，不會用別人的 PR 當裝飾。 | 视频画面展示规则，不拿别人的 PR 当装饰。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 画面展示规则而不拿他人PR当装饰的范围保留。 |
| zh-CN | v40140 | caption | 回到開頭：AI 修好 Bug，測試綠了，能直接合併嗎？ | 回到开头：AI 修好 Bug、测试绿了，能直接合并吗？ | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI修好与绿灯是否足以合并仍是结尾反问，非自动授权。 |
| zh-CN | v40141 | caption | 先過需求、差異、回歸這三道關，再由人作最後判斷。 | 先过需求、差异、回归三关，再由人作最终判断。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 三关之后仍由人最后决定的顺序保留。 |
| zh-CN | v40142 | caption | 這次的起始碼、修補和測試，要放在一起核對。 | 这次的起始代码、补丁和测试，要放在一起核对。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 起始码、修补、测试要共同核对的证据集合保留。 |
| zh-CN | v40143 | caption | 拿你下一個小修補照著試一次，比背規則更有用。 | 拿下一个小修复照着试，比死记规则更有用。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 用下一份小修补练习比单背规则更有用的编辑建议保留。 |
| zh-CN | v40144 | caption | 這個小練習之後，再把同一方法用到較大的改動。 | 做完这个小练习，再把方法用到更大的改动。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 先小练习再较大改动的顺序保留。 |
| zh-CN | title | metadata | AI 修好 Bug 就能合併？三個 PR 檢查點 | AI 修好 Bug 就能合并？三个 PR 审查要点 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 标题保留AI/Bug/PR、合并疑问及三个检查关概念；小于100字符且无角括号。 |
| zh-CN | description | metadata | 原本兩個測試全綠，分攤一百分卻只分出九十九分。開發者可以跟著實際修補與測試，學會在合併前檢查需求、差異與回歸。<br>示範是本地可重跑案例，並非正式站事故或已合併 PR。 | 原有两项测试都通过，100分分账却只分出99分。开发者可以跟着实际补丁和测试，学习合并前如何检查需求、代码差异和回归。<br>示例是可以在本机重跑的案例，不是生产事故，也不是已合并的 PR。 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 说明保留旧两项通过、100分少到99、需求/差异/回归与本地非事故非合并PR限制。 |
| zh-CN | tags:0 | metadata | AI code review | AI code review | PASS | 原full584 PASS＋精确不变；保留原判定来源 | AI code review 搜寻词拉丁字母名称保持。 |
| zh-CN | tags:1 | metadata | PR review | PR review | PASS | 原full584 PASS＋精确不变；保留原判定来源 | PR review 搜寻词与来源保持。 |
| zh-CN | tags:2 | metadata | Bug fix | Bug fix | PASS | 原full584 PASS＋精确不变；保留原判定来源 | Bug fix 为普通技术搜寻词，大小写规范不新增产品名。 |
| zh-CN | tags:3 | metadata | 程式碼審查 | 代码审查 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 程式码审查用目标语言自然技术用语。 |
| zh-CN | tags:4 | metadata | 回歸測試 | 回归测试 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 回归测试采用明确技术用语，不误译为统计回归。 |
| zh-CN | chapter:opening | metadata | 綠燈也會漏 | 绿灯也会漏掉 Bug | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 开场章节保留绿灯仍可能漏掉缺陷的含义。 |
| zh-CN | chapter:why-green | metadata | 綠燈不等於正確 | 测试通过不等于正确 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二章节保留绿灯不等于正确的证据限制。 |
| zh-CN | chapter:gate-one | metadata | 第一關：需求契約 | 第一关：需求约束 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第一关章节保留需求契约/约束检查含义。 |
| zh-CN | chapter:gate-two | metadata | 第二關：讀差異 | 第二关：读代码差异 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第二关章节保留直接阅读实际差异的含义。 |
| zh-CN | chapter:gate-three | metadata | 第三關：跑回歸 | 第三关：跑回归测试 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 第三关章节保留执行回归测试的含义。 |
| zh-CN | chapter:three-gates | metadata | 合併前的決定 | 合并前怎么决定 | PASS | 原full584 PASS＋精确不变；保留原判定来源 | 收束章节保留合并前最后由责任者判断的主题。 |
