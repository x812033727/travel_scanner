# 新版交稿檢查教學：獨立內容與事實查核

查核日期：2026-10-09（Asia/Taipei）
Reviewer：codex-review-own-video
Overall verdict：PASS
適用影片：claude-code-mods-delivery-check-tutorial

本結論允許進入旁白與教學卡片製作。範圍是完整原稿、63 場畫面資料、127 句旁白、官方來源與原生核心操作收據；不是音訊、畫面像素、完整成片或所有原生操作驗收。

## 受查來源與雜湊

| 檔案 | SHA-256 |
| --- | --- |
| [video.json](video.json) | 877df97db4c2423f5a4ed2074644a9907d8c3ea5df503f4bea57a8ae84d7a992 |
| [script.md](script.md) | 9f056de802c522be59b95d2d1abb904129e8138b26079b84a2c4e646f01890a6 |

逐句比對結果：JSON 與 script 的旁白 127／127 相同，零差異。open-check 指令使用正常雙引號，沒有多餘反斜線。寫出本報告前再次讀取來源雜湊，仍與上述版本一致。

## 逐項主張

| ID | Verdict | 類型 | 查核依據及限制 |
| --- | --- | --- | --- |
| c1 | CONFIRMED | fact | Mod 是擴充 Claude Code 介面或行為的外掛；影片以自訂小功能解釋，沒有誤稱換模型。[官方概覽](https://code.claude.com/docs/en/plugins/mods/overview) |
| c2 | CONFIRMED | fact | 終端教學門檻 2.1.287 以上符合官方文件；本例 2.1.293 有既存版本證據。不能將終端門檻擴大套用到所有其他入口。[建立指南](https://code.claude.com/docs/en/plugins/mods/create) |
| c3 | CONFIRMED | fact | --plugin-dir 可載入本機目錄供一次 session 使用；本片沒有宣稱完成常駐安裝。[建立指南](https://code.claude.com/docs/en/plugins/mods/create) |
| c4 | CONFIRMED | fact | plugin validate 分析 manifest 與 hooks 原始碼，不執行 Mod；通過不等於功能、內容或全部案例正確。片中指令是指引，沒有偽造新版成功輸出。[建立指南](https://code.claude.com/docs/en/plugins/mods/create) |
| c5 | CONFIRMED | fact | Mod 使用使用者權限；自行啟動的程序位於 Claude Code 指令沙盒之外。旁白沒有將沙盒說成全面保護。[安全文件](https://code.claude.com/docs/en/plugins/security) |
| c6 | CONFIRMED | source inspection | 重讀 v2 程式確認：資料夾 stat 後使用單層 fs.list 比對固定名稱；不讀文件內容、不寫檔、不呼叫模型。evidence-scope 已清楚說明因果。[官方檔案能力](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network) |
| c7 | CONFIRMED | owner-reported native evidence, bounded | 原生收據支持兩份存在／封面缺少，補入提供的封面檔後，由站主按鈕刷新得到三份存在、時間更新。影片已說明是結果整理，沒有操作錄影；沒有聲稱 Claude 生成了該封面檔。 |
| c8 | CONFIRMED | teaching example and source inspection | 路徑存在不能證明內容合格；空白檔、同名資料夾及錯名的判讀與程式一致。空白、錯名等未被標成全部完成原生 UI 實測。 |
| c9 | CONFIRMED | source inspection, bounded | 原始碼只在指令開啟或按鈕觸發時重新查詢，重畫畫面不讀檔。關閉面板不等於卸載；關閉與停止載入仍標待原生驗證，未冒稱已操作成功。 |
| c10 | CONFIRMED | opinion | 一次提示與固定面板依工作頻率選擇，屬合理教學建議與情境比較；沒有性能、成本或通用優越性的保證。CONFIRMED 指此意見已明確界定且未偽裝成測量結果。 |

上列四份官方頁面在本次查核中透過瀏覽工具讀取。HTTP status：not recorded；瀏覽工具未提供原始 HTTP 狀態碼，本報告不補造 HTTP 200 或連結檢查收據。

## 核心證據界線

c7 收據：`owner-v2-workflow-completed-20261009.json`（保存在外部 demo-evidence；公開範圍見[核心驗證紀錄](../claude-code-mods-no-sandbox-before-install/demo/delivery-verification.md)）。
SHA-256：c0205ecc69704785fa947c142de1fd2d836e61278818b2301afe5b93212dcb2e

收據綁定 runtime commit：4ef14abd3a7f57d46cb85dd5cd0b57ec47c35d7a。

本次重新核對的程式位於 repository 相對路徑 docs/videos/claude-code-mods-no-sandbox-before-install/demo/delivery-check/hooks/：

| 檔案 | SHA-256 |
| --- | --- |
| register.mjs | 35da89a85e27cdb7f615b3f02b10d9013bafa8ed6e1fbf655571503d401bc18c |
| delivery-logic.mjs | b4e8a3aea970870b7f65ec5fa98451aa474be6481c1c0b3fb9a321c7b7b4d1e8 |

站主回報的面板時間為 UTC 2026-10-08T19:43:10.592Z 與 2026-10-08T19:44:43.888Z；影片結果表換成台灣時間 2026-10-09 03:43:10 與 03:44:43，換算正確。兩份原始材料雜湊未變。

這些證據只支持核心缺件、加入提供的封面檔及按鈕刷新。沒有操作截圖或錄影，不支持 Claude 已生成封面檔，也不表示空白、錯名、權限拒絕、課程版 Mod、關閉、重載或所有原生案例都已完成。普通 Node 檢查不替代原生 UI 操作證據。

## 教學與旁白結論

原先計數器課缺乏實用目的的問題已改善。新版依序提供：

1. 交稿缺件造成的具體問題。
2. 完整材料、精確檔名與資料夾位置。
3. 可直接使用的完整程式及可選生成需求。
4. 查缺件、加入封面材料、手動刷新與核對結果。
5. 讀取名稱清單、比對固定名稱的簡明原因。
6. 空白、錯名、位置錯誤與無法檢查的排錯。
7. 一次提示和固定面板的選擇，以及日期修改的內容驗收。
8. 有完整材料與答案的課程檔案練習。

課程版 Mod 已明確界定為延伸需求設計，沒有把尚未實作的第二個 Mod 當成已完成案例。觀眾能完成檔案與內容判讀練習，不必先成功生成新程式。

旁白沒有延續舊版大量 hooks、事件與 next 術語。畫面資料和旁白意思一致，沒有發現阻擋製作的技術誤述或超出實測範圍的成功宣稱。這是讀稿的聽眾視角覆核，尚未聽到實際合成旁白。

## 製作時仍需完成

- 教材與完整範例須有觀眾實際可取得的連結；目前稿件中的教材連結仍是交付條件。
- 8 分鐘以上及單一靜態狀態的時間，須以合成音訊與時間軸驗收；文字估時不是實測片長。
- 長提示詞、完整材料的字級與裁切仍須看實際渲染。
- 本審查沒有聽取旁白、觀看成片或執行 Claude，不能當成完整影片核准。

本次查核及存檔未修改 repository、未付費、未重試被拒的操作。此檔為本次新片 production 來源的獨立查核報告，不是先前被拒的 directory-list assessment，也沒有寫入該被拒路徑。

## 增量覆核：v2 畫面文字與教材連結

查核日期：2026-10-09（Asia/Taipei）
Reviewer：codex-review-own-video
Incremental verdict：PASS

本次只覆核相對 production/video-v1.json 與 production/script-v1.md 的文字／metadata 變更；原審稿正文保留。基準兩檔雜湊分別為 877df97db4c2423f5a4ed2074644a9907d8c3ea5df503f4bea57a8ae84d7a992、9f056de802c522be59b95d2d1abb904129e8138b26079b84a2c4e646f01890a6。

### 本次通過的來源

| 檔案 | SHA-256 |
| --- | --- |
| video.json | 0e2c780f36a78d2a030c09224aac9d11f4e2ec2c1c7bfe93c4b9d7fced8273c3 |
| script.md | 30713d8f0b73808c7579b8eb9a9d5d323a200d0fd8eb2233ad8a77be1c5c71e0 |

再次逐項比較：63 場，127 句；所有旁白 line 物件（包含文字、ID、emotion、reveal）及 voice 設定與基準相同。新版 script 與新版 JSON 的 127 句旁白完全對應，沒有旁白變更。

### 變更結論

| 變更 | Verdict | 核對結果 |
| --- | --- | --- |
| folder-map 教材目錄提示 | CONFIRMED | JSON 與 script 現均為「教材連結內 delivery-check」，對應教材 materials 根目錄的實際結構。初次增量覆核發現 JSON 仍留 demo/ 前綴，作者修正後已重新讀回；此結論只綁定上列最終雜湊。 |
| open-check 輸入位置提示 | CONFIRMED | 改為「在 Claude 對話框輸入」，與既有旁白及 /deliverables 指令的使用位置一致；指令本身沒有變更。 |
| observed-timestamps 原檔欄位 | CONFIRMED | 「原來兩檔」改為「另行核對原檔」，更清楚表達內容未變是另行比對的結果，沒有誤稱面板閱讀了文章內容。既有時間及狀態資料不變。 |
| 完整教材 metadata 連結 | CONFIRMED | URL 綁定本地已存在的 commit b8269244d7fb75bbb2b20cccf4baa31fefb7c8fc，指向 docs/videos/claude-code-mods-delivery-check-tutorial/materials。git ls-tree 及 git show 已核對該 commit 內的材料樹與 README；包含完整 delivery-check 四個程式檔、起始副本、完整封面素材、課程材料及 EXERCISES.md。此項只確認本地提交內容與連結指向一致。 |

c1–c10 原主張與適用界線不變，繼續採用原表的 CONFIRMED 結論；c10 仍是 opinion。本次變更沒有新增原生操作、媒體驗收或模型生成成功的主張。

### 公開連結仍待讀回

教材連結：
https://github.com/x812033727/travel_scanner/tree/b8269244d7fb75bbb2b20cccf4baa31fefb7c8fc/docs/videos/claude-code-mods-delivery-check-tutorial/materials

本次覆核沒有對此公開 URL 執行 HTTP 讀回。Public URL accessibility：not verified；HTTP status：not recorded。不能用本地 commit 及材料存在，推論遠端 push 已完成、網址公開可訪問或觀眾已能下載。發布前仍須由統籌完成推送後的公開連結讀回。

本次 PASS 僅涵蓋上述可核對的文字與 metadata 變更。未重跑 Claude、未付費、未聽旁白、未看新成片，原報告的音訊／畫面／片長／其餘原生驗收限制全部保留。

## 增量覆核：10 句等義口播改寫

2026-10-09（Asia/Taipei）｜Reviewer：codex-review-own-video｜Verdict：PASS。

本次綁定 video.json SHA-256：4406dfc66cfc14f8210a58b75259334f2164664f960090150fde1d3e260b52be；script.md SHA-256：48d007da2ab431a9ddb1283c9ad90727debfa382f6e6f7d2931bec70cfee3b44。

獨立遞迴比對與基準 video-before-audio-rewrite.json（0e2c780f36a78d2a030c09224aac9d11f4e2ec2c1c7bfe93c4b9d7fced8273c3）的差異：只有下列 10 個 line.text 改變，均與受查 audio-rewrite-proposal.json（af84d10baf4bc043480cb438b6f88ab676f3c9e5c5655c825627f74c2c5bae8d）一致。127 個唯一 ID 及排列、voice、畫面 data、emotion、reveal、其他所有 JSON 欄位均未變。新版 script 的 127 句旁白與新版 JSON 全部一致。

| Line ID | Verdict | 語意查核 |
| --- | --- | --- |
| vuyd | CONFIRMED | 保留把固定交稿規則放入介面的用途。 |
| xxbi | CONFIRMED | 保留刻意缺件才能檢查缺件能力的原因。 |
| zqcz | CONFIRMED | 保留從檔案總管複製完整練習路徑的步驟。 |
| pnba | CONFIRMED | 仍限定站主回報的主案例缺封面結果。 |
| rizx | CONFIRMED | 保留先核對證據、不要猜原因的排錯安排。 |
| udkx | CONFIRMED | 仍是手動存入提供的封面材料，不冒稱模型生成。 |
| drfn | CONFIRMED | 保留報名方式必須由主辦人確認的內容缺口。 |
| wvrt | CONFIRMED | 保留實際檢查與只列清單的差別，以及人工核對替代步驟。 |
| xnzi | CONFIRMED | 保留具體「圖書館」錯誤答案反例；未把課程版 Mod 說成已完成。 |
| 3vtm | CONFIRMED | 保留補件後重查、閱讀內容及交給負責者確認的順序。 |

結論：10 句等義改寫沒有新增數字、承諾或實測範圍，原 c1–c10 及證據界線保持有效。本次只確認文字及同步結果；重新合成後的發音、ASR、片長、畫面與成片仍需重新驗收。

教材公開讀回補充：統籌的 production/materials-public-readback.json 記錄 2026-10-08T20:24:09.1848504Z 對既有 commit 固定教材 URL 取得 HTTP 200，containsReadme=true；本覆核者已讀該收據，但沒有自行重發 HTTP 請求。此前「公開連結仍待讀回」是當時狀態，後續已由統籌取得上述讀回證據。
