# ai-proofreading-terminology 查核第二輪（2026-10-05）

第二輪查核者，不是撰稿者，也不是第一輪查核者。所有來源今天重新抓取，存放在
`_tools/ai-proofreading-terminology/v2/`。curl 用 `-sSL`、規定的 UA，先剝掉 `<!-- -->` 再讀，
文字由 `v2/totext.py` 抽出。github.com 經代理仍回 403，改讀 raw.githubusercontent.com（200），
並用 WebFetch 確認 github.com 的 repo 頁與 TWPhrases.txt 頁可以打開、內容一致。

格式：主張｜判定（ok / fixed / softened）｜來源

## A1. 第一輪改過的事實（全部重查）

- 摘要「台灣寫軟體、列印，大陸寫軟件、打印」｜ok｜簡編本附錄 ID=54，抓了第 1 到 7 頁：軟體＝軟件、列印＝打印；修訂本「數據」：經由調查或實驗得到的數值，沒有標大陸用法
- 品質列：大陸語詞「品質／質量」｜ok｜附錄第 1 頁「品質｜品質／質量」
- 表格 caption 加上 OpenCC 台灣詞庫｜ok｜TWPhrases：軟件→軟體；視頻→影片 視訊（raw 與 WebFetch 結果一致）
- 質量「可指物體內所含物質的量」｜ok｜修訂本 ID=113680，第 3 義是「物體內所含物質的量」；第 2 義是「專指事物的品質。今大陸地區沿用之」
- Editor「易混淆或形音相近的錯字」｜ok｜docx：「我再你家門前」列在「易混淆錯字」，「以經」列在「形音相近錯字」
- Editor「要用 Microsoft 365 帳號登入才會偵測」｜ok｜docx 第 3 行：「需使用Microsoft 365帳號登入才會偵測」
- OpenCC --ambiguities 只有原生 CLI 支援｜ok｜README 第 110–111 行（npm CLI）與第 154–156 行（Python CLI）。第二輪改寫了句子，見 C
- 「OpenCC 不是逐字替換，而是先查詞庫」｜ok｜README：基於詞庫的確定性轉換；DESIGN_PRINCIPLES：詞組表優先於單字表
- 法律黑線「差異預設顯示在第三份新文件裡」｜ok｜zh-TW 頁：「根據預設，Word 會在新文件中顯示比較結果」，也可以改成顯示在原始或修訂文件
- 「AI 不一定知道你要台灣用語」｜ok（第一輪軟化後是建議語氣，不算事實主張）｜—

## A2. 第一輪無法確認的項目

- Editor 語言表的 ● 與 ◌｜**已解決**｜頁面仍然沒有圖例，但表格前的注記寫「Japanese writing refinements ... (**) are not yet available in the desktop Word app」，而 Japanese 的 Writing refinements 格是「● **」。可見 ● 代表有提供，這項功能只是桌面版還沒有。所以 Chinese (Traditional) 的 ◌／●／◌ 就是只有文法檢查（Chinese (Simplified) 也一樣）。正文不改
- Editor guidance docx 的日期是 2020-09-03｜ok，維持原判｜今天抓的支援頁裡，Chinese (Traditional) 的 Download details 仍連到同一個 docx（22,704 bytes，core.xml 的 created／modified 都是 2020-09-03）。正文另外加上「截至 2026 年 10 月」標示資料時間（見 B）
- github.com 回 403｜照舊處理｜raw.githubusercontent.com 回 200；WebFetch 打開 github.com 的 repo 頁與 TWPhrases.txt 頁，看到的內容相同
- Word 追蹤修訂頁混用「檢閱」與「校閱」｜ok｜zh-TW 頁寫「在 [檢閱 ] 索引標籤上，選取 [追蹤 > 追蹤修訂 ]」，同一頁另一段寫 [校閱 ]；法律黑線頁寫 [校閱]。台灣版 Office 的索引標籤是「校閱」，維持原樣
- 詞庫沒收的詞退回單字預設對應｜ok｜DESIGN_PRINCIPLES 第 116 行：「詞組表的優先級高於單字表」；README 中 `amb.t` 是 default candidate。DESIGN_PRINCIPLES 仍然只記在 notes.md（sources 已有 20 筆）
- 正文長度｜**已處理**｜第一輪是 2,607 字。第二輪縮短導讀段，又刪掉 Python／npm 那句，加上其他修改後是 **2,598 字**（intake_check），落在 2,200–2,600 之內
- 站內連結｜ok｜三個 slug 都在 apps/api/app/guides/content/，kind=life；連結文字與對方標題相符

## A3. 其餘主張抽查（verify-1.md 的清單，從第 2 行起每隔三行取一行）

取第 2、5、8、11、14、17、20、23、26、29、32、35、38、41、44、47、50、53 行。第 2、5 行已在 A1 查過。

- 8 Google 文件的拼字與文法建議只支援英、西、法、德、葡、義文｜ok｜57859 的 hl=zh-Hant 第 22 行；hl=en 第 25 行內容相同
- 11 軟體／軟件｜ok｜附錄
- 14 程式／程序｜ok｜附錄「程式｜程序」
- 17 只換字形會留下「軟件」｜ok｜STCharacters：软→軟，「件」不在表中；STPhrases 沒有「软件」
- 20 程序在台灣指辦事的規則次序｜ok｜修訂本 ID=124548 只有一個義項：「辦事的一定規則次序」
- 23 質量當品質講是大陸地區沿用｜ok｜ID=113680
- 26 干：乾、幹、干｜ok｜Unihan U+5E72 kTraditionalVariant：乾 干 幹；STCharacters：幹 乾 干 榦
- 29 复：復、複、覆｜ok｜Unihan U+590D：复 復 複 覆；STCharacters：復 複 覆
- 32 例詞 18 條｜ok｜STPhrases 逐條比對全部吻合（面条→麪條、这里→這裏，再經 TWVariants 麪→麵、裏→裡）
- 35 OpenCC 不使用大型語言模型、結果穩定可預期｜ok｜README 第 29–30 行
- 38 s2t 轉成 OpenCC 標準繁體，不等於台灣用字｜ok｜DESIGN_PRINCIPLES 第 3、11 行；README 配置清單
- 41 台灣詞庫：數據→資料／數據、視頻→影片／視訊｜ok｜TWPhrases
- 44 英文字母與阿拉伯數字用半形｜ok｜docx「建議使用半形拉丁字母」「建議使用半形數字」
- 47 Google 文件建議模式：右上角編輯圖示 → 建議｜ok｜6033474 第 26–27 行
- 50 callout（頭發、皇後）｜ok｜措辭是「可能」，當示意用
- 53 站內連結｜ok｜見 A2

另外順手核對了：附錄的其他四列（資料＝數據、影片＝視頻、列印＝打印、品質）、Unihan 发／后／台／面／里、Copilot FAQ 三句（第 125、126、135 行）、標點手冊的引號說明、樂詞網首頁（學術名詞、雙語詞彙、辭書）。結果都吻合。

## 第二輪的事實修正

1. **風格表「異體字」列的例子**：原本寫「例如公布或公佈」，依據是修訂本 ID=75132。但修訂本「公布」有兩個義項，「也作「公佈」」只掛在第 2 義（向公眾揭示某種事實）。第 1 義「把法律或命令公告周知」只收「公布」，所以這個例子會讓讀者在公告法令的語境也選「公佈」。例子改成「雇主或僱主」：修訂本 ID=71572 只有一個義項，並寫「也作「僱主」」。sources 裡同一筆換成 ID=71572，總數仍是 20。Editor 的「異體字選字」也舉了僱主→雇主，可以互相印證。
2. **「這類詞轉換工具不會動」**：原句講的是所有轉換工具，能查證的只有 OpenCC 的詞表（STPhrases 與 TWPhrases 都沒有质量、土豆的詞組條目）。改成「這類詞 OpenCC 的台灣詞庫不會替換」。

## B. 合規檢查（辦公效率批次）

- 實測：沒有實測結果、分數或「實測」字樣。「結果穩定可預期」是 OpenCC README 自己的說法，有出處。
- 廠商功能與日期：Editor、Google 文件、Copilot 的段落原本沒有日期。第 5 段加上「截至 2026 年 10 月」，兩張表的 caption 原本就有日期。（compliance）
- 法規：沒有引用任何法條。標點與用語只引教育部的辭典與手冊。
- 提示詞：已經標成「校稿提示詞範本」，前一句改為「可以用下面的提示詞範本校稿」，不宣稱有效。（compliance）
- 人工檢查：提示詞要求只列建議、標出待確認、不改數字與人名；後面接追蹤修訂或建議模式逐條接受，加上七項人工終校清單與 callout。每個 AI 產出旁邊都有人工步驟。
- 工具推薦：沒有說哪個工具比較好。Editor 只當成「規則型工具能抓哪些錯」的參考，依據是它自己的說明檔。Google 的限制照它的說明頁寫。
- 能力描述：「聊天式 AI 能做規則做不到的事」是沒有出處的能力保證，改成「聊天式 AI 可以拿來檢查規則管不到的地方」，當作用法建議。（compliance）

## C. 讀者優先與用字

- 「本文」「這篇」出現 0 次。沒有描述研究過程的句子。caption 的「查證於 2026 年 10 月」是日期標示，和圖上的 2026 對得上，保留。
- 外文術語：Word、Microsoft Editor、Copilot、Unicode、OpenCC 第一次出現都附了中文說明。原句「Python 與 npm 版的命令列工具不支援這個選項」裡的 Python、npm 沒有中文，改寫成「OpenCC 原生的命令列工具才有標出歧義的選項（--ambiguities）」。範圍一樣（只有原生 CLI 支援），也去掉了沒有中文的術語。（style）
- 導讀段「以下依序說明……」原本把六件事列成流水帳，縮短成四項。（style／長度）
- 開頭第一段第一句就回答了問題：AI 抓得到表面錯誤，抓不到事實、數字與專有名詞。
- 用字是台灣用法。軟件、數據、視頻、質量、用戶都是刻意舉的例子。沒有驚嘆號，也沒有「總結來說」這類贅詞。
- 正文 2,598 字。

## 圖

重新渲染了 hero.png 與 diagram-1.png 並逐張看過：沒有文字溢出、重疊或空白過多的地方，箭頭旁的標籤也沒有壓到線。圖解唯一的數字是 2026。hero 只有一行 52px 的字，沒有 logo、臉孔或遞增長條。這一輪沒有改圖。

## 檢查結果

- `pack_cli ingest --dry-run`：dry run: nothing written（通過）
- `intake_check.py`：RESULT PASS（0 failures），body_length=2598。唯一的 WARN 是自繪 hero 沒有標題可以查重，和第一輪相同。
