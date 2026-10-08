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
