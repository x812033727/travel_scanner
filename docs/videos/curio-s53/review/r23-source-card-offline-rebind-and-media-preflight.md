# S53 R23｜南公園來源卡離線圖單重綁與下一景媒體預檢

2026-10-22 UTC。依 [R23 非作者來源與畫面紙審](r23-s53018-source-card-independent-paper.md) **PASS**，將私人工作區的 14 張既收圖安全綁到 R23 的分鏡版本；此步沒有購圖、judge 或聲音呼叫。

## 凍結與重綁

`video.json` SHA-256 `2b5d0bfd85a581cac1e08ac8c155a9e8f89969634cc98e1c5300fe3457c7720e`，`claims.md` SHA `a276b8561f713f6160fe8fd4d68c79f0c85640ce0f4db2cf031d81f99e3c278e`，未改的 `script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。舊私人 manifest SHA `96ef6a6d67c03fd37f86963f819f5bdbafce8c72fbb9f04d0bb983b371a04ef5`，`visual_hash=133eba68d1a96469`；R23 目標 `visualHash=14dade824c0840b3`，`look_hash=98a370ae40badbaf` 不變。

操作前要求 `STOP` 在位、jobs 空、ledger 不變，先驗原圖檔 SHA 與既有 14 筆圖單條目。舊 manifest 獨占備份為 `/workspace/.video-work/curio-s53/rebind-backups/r22-manifest-before-r23-source-card.json`，備份 SHA 等於上述舊 SHA。只修改 `visual_hash`，原子取代再讀回；新私人 manifest SHA-256 **`b8e3159267747d1ea80b70276d79cbf70cfb6c497fdbcd2cd516978e1a4eaca1`**、權限 600。前後 14 個 `shots` 條目逐項相同，選圖實檔各自仍等於條目 SHA，[R22 清單](r22-s53010-card-s53018-offline-manifest-rebind.md)可追。對這 14 景跑 `keyframeProblems` 為 **0 問題**。`s53010`、`s53018`、尚未畫的 `s53085` 均無圖單條目；沒有把 R22 退件圖重新接回。舊 contact sheet 引用仍為空。

第一次腳本嘗試在匯入常數時失敗，尚未寫入；第二次腳本的寫後 ledger 預期雜湊有筆誤，觸發自動復原，重查 manifest 與舊 SHA 完全相同。修正筆誤後第三次完整寫後驗證 **PASS**。最終 ledger SHA 仍 `dc7aaf8ca062b7680113bde534ce7d1cbdc218ab5567626f0365f6fa39dfc01f`（US$0.4725／36 image／35 judge／0 預約）、jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`（空），`STOP` 在位，整集上限 US$4.78。

## 下一景即時預檢

下一個未畫 `shot` 為 `s53023`。台詞問公園廣場能否長期容納救災小屋；來源為 [1913 年調查 G L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)，指出公園與廣場僅臨時使用。其未改提示詞是 1906 年廣場中匿名救濟工作者查看空白公園街區圖，旁有救濟小屋草圖；它沒有聲稱具名個案、真實地圖圖樣或永久使用權。R5 全景來源／書面畫面紙審 PASS，R23 沒改此景。先前在 image-01 未恢復前只讀預檢失敗，現在 `keyframes --shot s53023 --takes 1 --dry-run` 退出 0，回報 image-01 可用、1K 圖約 US$0.01。`media-status --json` 回報可用 images 10,060／30,000、judge 8,526／30,000；此預檢沒有付費。

下一步限 `s53023` **一張原生圖與一次 judge**，直接看未裁原圖及所選圖，遇第一張人工 REJECT 即停。每次付費前須重新核上述 R23 雜湊、14 KEEP、帳本／jobs／`STOP`；不能再畫 `s53010` 或 `s53018` 第四張。此回不代表完整分鏡、網站卡、人耳、配樂或成片核准。
