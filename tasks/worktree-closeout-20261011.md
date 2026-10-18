# Codex C 槽收尾與待辦

更新：2026-10-12T00:59:00.265549+08:00。尚未合併內容統一放入 [PR #1450](https://github.com/x812033727/travel_scanner/pull/1450)，維持 draft。

本輪已刪 **3 個舊工作目錄**、先前 **14 個已结案翻譯資料根**，以及 **2 個完整新聞／翻譯資料根**。移除原檔邏輯大小合計 **28.670 GiB**；先前工作目錄與小批次的主壓縮備份 **1.004 GiB** 留在 C 本機。

這是檔案邏輯大小，不是 NTFS 配置容量；扣主備份的差值尚不含小型證據／報告與保護中的暫存 checkout，也不歸因其他聊天的磁碟變動。備份在 C 本機，沒有聲稱外部或異機備份。

## 新聞與翻譯：依最新指示整根刪除、不新增備份

使用者最後明確要求「幫我將新聞與翻譯的都刪除」，接著指定「新聞與翻譯不用備份」，因此這兩根包含未完資料一併刪除，不新增完整備份。精確範圍只限下表的兩個 C 槽資料根；其他翻譯批次、repo、Claude、《偶的江湖》及正式站不包含在這次整根授權。

| 完整資料根 | 實際刪除 | 檔案 | 原檔 GiB |
| --- | --- | ---: | ---: |
| `<home>\.codex\news-review` | 已清理 | 43073 | 16.487 |
| `<home>\.codex\article-localization-release\all-missing-20261007` | 已清理 | 49849 | 9.684 |

資料刪除不代表產品工作已完成。新聞 66 個未完候選、wave6 的 17 篇未發布文章，以及既有 source、review、錯誤／未知請求、hold、checkpoint 和發布證據隨整根一併刪除；原任務與 owner 不擅自結案或釋出。續作須從仍存的 Git、既有局部備份、正式站與其他來源重新整理，不能承諾完整還原已刪資料。

完整資料根未備份；整根備份草稿從未執行。刪除前重核精確路徑與所有祖先、完整檔案數及位元組、無 reparse，逐檔排他開啟確認無讀寫占用，再重查 CWD／排程／程序引用。沒有聲稱對這次 92,922 檔做內容 SHA 備份或完整還原。刪除收據：`codex-closeout-20261011/full-data-cleanup-receipt.json`。

## 工作目錄

| 目錄 | 結果 | GiB | 證據與下一步 |
| --- | --- | ---: | --- |
| article-locales-wave4 | 已清理 | 0.858 | #1401 已合併；完整工作檔、Git 歷史及 index 已備份，確認未使用後移除。 |
| fc2e | 已清理 | 0.623 | 使用者明確不再使用；研究、環境及所有未提交／ignored 檔已備份。原 metadata 槽已由新 a18a 使用；保留新 owner 的 metadata。 |
| batch006-final-close（Batch034） | 已清理 | 0.546 | 使用者明確不再使用；結案副本與兩份本機任務 metadata 已備份。 |
| 4e16 | 保留 | 1.263 | 32 篇發布收據集中 #1450；合併後再查使用狀態。Decrypt 原票已恢復共享 open。 |
| pr-merge-watch | 保留 | 0.897 | missing-entry 保留修正及回歸集中 #1450；合併後重查原 staged 17 檔與使用狀態。 |
| b136 | 保留 | 0.660 | 凍結 collector 實際 import 此目錄 helper；保留，待現任 owner 釋出依賴或完成合法 successor adoption。 |

五份原 worktree 共 98,587 個檔案已完整保存，包括未提交、ignored、原始 index、狀態及 Git metadata。Git 歷史復原需舊 `retained64-followup-20261011/completed-codex.bundle` 加上新增量 bundle。原來源 repo 不作唯一的 restore object store；ZIP 全 blob SHA、Git graph 及十個 restore fixture 已驗證。

wave4 移除後，原多根執行器因來源證據超過時效停止，沒有續刪。fc2e／Batch034 改成單根重新完整 SHA、排他讀取及 owner／process／automation／ref 守衛；原失敗收據與各次新收據全部保留。

## 原已結案翻譯批次

batch026-wordpress-operations、batch018-web-basics 與 batch012-selection 內 12 個 Otaru／Sapporo 子根已清理，10,904 檔共 506,492,629 bytes。三組完整備份 11,662 檔逐一解壓 SHA 核對；batch012 父根、47 個 top-level、690 個 independent-review、21 個 qa-tool-check-jeju 保留，758 檔共 34,675,770 bytes 刪後原 SHA 不變。

原先為五個新聞 prepared 及 c30 prospective 所做的 827 檔小批次備份也保留；這六個副本後來納入整根處理，不重複計算已刪容量。c30 先前 Windows 目錄 st_size 的 0／4096 表示差異及失敗收據完整保留，沒有將 raw fingerprint 失敗冒稱成功。

## 共享 PR 內容與驗證

- #1401 已在 2026-10-11 15:37:22 UTC 合併，合併前 exact-head 四個必要檢查與其他檢查成功；沒有重複發布內容。
- #1373 的九份 docs、四張 release done 票與全域進度原 bytes 集中 #1450，19 路徑獨立核對通過；總票 stale claim 修正為 open／unclaimed，全域補語系仍未完成。
- tidy 對網站最新 200 筆列表缺片的情況保留資料，等目前狀態出現後再判斷保留期限。五個新增回歸覆蓋空列表、200 筆、dry-run、實際清理與重新出現。沒有執行正式影片素材清理。
- Decrypt 原始分類票恢復共享 open／unclaimed，保留 Nano Banana／TikTok 兩候選 snapshots；沒有重跑候選。
- b136 四原件、獨立還原與 12 個離線案例完成，實際 helper 依賴仍在，維持 open。

驗證：tidy 40 pass／1 個既有 Windows symlink skip；docs-video 199 pass；longform 473 plans pass。完整 tools suite 為 2,246 tests：2,224 pass、9 fail、13 skip，exit 1；九個失敗已有 Windows FFmpeg、C: ESM、lease、slash、speech journal EPERM 票追蹤。卡住的自有 automation test child 經確認後停止，該檔未完整跑完；沒有宣稱全 suite 綠燈。

## 續作清單（資料已刪，須從仍存來源重新整理）

- 新聞去重 589 個候選，2026-10-11 16:14:35 UTC 正式資料庫 READ ONLY 對帳：397 published／101 rejected／25 duplicate／46 manual_review／19 needs_redraft／1 failed。未完 66 個全部映射既有票，原 520 cohort 剩餘 52 个是其中子集，不重複加總。397 published 均有五語版本指針，本輪未重新 GET 全部公開頁。
- [news-held-cohort-recovery](open/2026-10-10-news-held-cohort-recovery.md)、[resolve-current-news-review-and-redraft](open/2026-10-07-resolve-current-news-review-and-redraft.md)：保留原 owner。66 項中 20 個無 Guide、46 個已有草稿；逐項對照本機 `news/pending66-existing-task-map.json`。CFTC 接續官方 HTTP403 source gate；Sanders／Glasses 校正 claim 12／14 navigation；XRPL5186 先更新 Source／Evidence／Guide／history／RQ／CP seals，再沿原流程處理已審提案。
- [article-five-language-completion](open/2026-09-14-article-five-language-completion.md)：保留原 claim；wave4 13 篇／52 翻譯、wave5 12 篇／48 翻譯已有發布收據，不使用舊未發布交接當現況。
- [article-missing-locales-completion](open/2026-10-07-article-missing-locales-completion.md)：open／unclaimed，刷新正式站缺口後續做，不把舊 862／3448 當目前數字。
- [release-wave3-travel-and-life-article](done/2026-10-07-release-wave3-travel-and-life-article.md)：本 PR #1450 恢復同 ID 的 done 版本；核對的 origin/main `6b5370b6fd661a8733392b79c2458bea9c70a7fb` 仍是舊 open 版本，待本 PR 合併整合。wave3 已有實際發布與公開頁驗收，不重複發布。
- [localize-reviewed-web-design-wave6](open/2026-10-09-localize-reviewed-web-design-wave6.md)：#1409 merged 只證明內容整合，原 review owner 保留。本機 release／審查工作資料隨整根刪除；已合併的 repository 內容包仍在，接續先核對哪些來源可由 main／PR 重建。原 localize owner 依 merge 收據修正過時 checklist；正式發布沿原 release 票，不重做已整合的內容。
- [release-localized-web-design-wave6](open/2026-10-09-release-localized-web-design-wave6.md)：17 篇仍待發布；先由仍存內容包與收據重建來源及 release state，再修正 merge-v1／實際 merge-v2 綁定及未證實的背景結果，完成 85 頁／170 views／255 媒體與 ledger 驗收；不能直接重放舊 helper。

## 仍保留的暫存目錄與限制

`localization-receipts-closeout` 內一份新建重複 open 票被自動核准審查拒絕刪除，回覆只有 `blocked by policy`。`tidy-capped-list-guard` 的 archive_worktree 因 pinned task/workspace 保護拒絕。兩個目錄均保留，沒有換工具繞過，也沒有取消聊天釘選。

Claude、《偶的江湖》、原影片、正式站內容、HOLD 與 provider 控制未更動。新聞正式資料庫只有唯讀對帳；沒有新聞 Save／翻譯發布、部署或新的付費生成。

Git metadata 補充：fc2e 的舊 Gitdir 在刪除當下已移除；刪後独立覆核時，該槽位目前由其他聊天的新 a18a worktree 使用；檔案 mtime 不當成實際重用時間證明。fc2e 的原 path／ref／registry binding 仍不存在；新的 a18a metadata 保留，沒有當成殘留刪除。
