# 五支新版完整影片交付紀錄

2026-10-12 13:59:53 UTC 核對：實際交付索引 **5/5 通過，無待修正錯誤**。

完整影片與四語素材的 `DELIVERY-INDEX.md` 位於目前的本機交付目錄；完成上傳、
後台連結與備份核對後如清理 C 槽，可依 [VPS 還原說明](RESTORE-FROM-VPS.md)
取回同一份索引及成片。

| 影片 | 新片頭秒數 | 全長秒數 | Studio 片尾開始秒數 |
| --- | ---: | ---: | ---: |
| 羅阿諾克 curio-h02 | 41.567 | 721.900 | 705.900 |
| 51 區 curio-u02 | 47.833 | 753.933 | 737.933 |
| 通古斯 curio-h03 | 43.367 | 736.500 | 720.500 |
| 麥田圈 curio-l08 | 44.700 | 739.400 | 723.400 |
| 瑪麗賽勒斯特 curio-h01 | 45.267 | 737.733 | 721.733 |

每片包含 1080p / 30fps MP4、繁中／英／日／韓四份 CC、英／日／韓三份完整
WAV、四語標題說明與章節、縮圖及片尾設定。整批共五支成片、20 份 CC、
15 份補充配音及 20 份標題說明文字；大型媒體保留在外部交付目錄。

影片結構為新濃縮旁白、5 秒頻道片頭、原片第二章起的正文、21 秒配樂片尾。
配樂沿用站主選定的 Golden Hour — Telecasted，各語言說明保留音樂署名。
可點擊片尾元素需於新影片上傳後在 Studio 匯入 `oxEtlA8GWas` 範本，
安排在最後 **16 秒**：最適合觀眾、訂閱、最新上傳。

## 驗證

- 五支均完成整片影音解碼、正確影格數與聲音樣本數、音量／峰值、字幕範圍
  與四語共同時間軸檢查。
- 保留正文的影像封包及四語 PCM 與來源一致，合成前後來源雜湊未變。
- 五支均有與最終成片及圖片雜湊綁定的有限畫面抽查。U02 已改用完整顯示
  1998／2013 兩欄的第 316 格；H03 日文發音、L08 繁中措辭修訂均經新音訊檢查。
- 20 軌新片頭通過音訊關卡；原始 ASR 旗標及精確音檔綁定的第二意見均保留。
  語音收據見 [PRODUCTION-NOTES.md](PRODUCTION-NOTES.md)。
- docs-video 套件 209/209 通過（bundled Node 24.19）；本批 speech／retake／revision
  測試 16/16 通過，另有實際 FFmpeg 合成 smoke 通過。系統 Node 24.13 的原生
  child-process crash 及 bundled runtime 成功紀錄均保留。

## 最終 MP4 SHA256

| 影片 | SHA256 |
| --- | --- |
| curio-h02 | `1dbebfe0f224aef5cd1c5e1c9092553ff66b39678d2e9daafe5b8f0e15a2f8c0` |
| curio-u02 | `19933d6b22373dcfcf58d18debbd5e0403672ccc12c50f1136228d2ca47cf263` |
| curio-h03 | `1d9a1991a24c7082c518543127598861f96d026cb89c3ab9ff17ced3768d30eb` |
| curio-l08 | `5cd592ac04bfc880e43a955bc2a40f2ffceaf82ca785492a3591fc108899aa07` |
| curio-h01 | `4b6a4ba7d44437ba768c7b8eb9a974f914a908ab2b28cca8850668d2e1efff25` |

外部 `final-delivery-receipt.json` 的 SHA256：
`d10e37fafa8fcea0e7448d88b927fd7c2babe032452d33b49f443f87b8870311`。
該收據綁定成片、QA、抽格覆核記錄，以及交付索引 SHA256
`ce874497c3a4509559668bd1a2b2bec832d6a6449ab003b4204eb2c1f675f2de`。

## 狀態與原片註記

本批完成使用者指定的「新版完整影片，之後重新上傳」。五支新版影片已在
Studio 讀回為私人、完整時長且處理完成；四語 CC 與三個可點擊片尾元素已核對。
英／日／韓 15 條音軌已提交，Studio 仍顯示處理中；目前沒有公開發布的授權或
站主完整試播／聽驗的確認。新版後台專案已匯入，但新 YouTube ID 尚待連結，
詳見
[STUDIO-AND-BACKEND-LINKAGE.md](STUDIO-AND-BACKEND-LINKAGE.md)。
U02 英文 Studio 說明另做最小精簡，最終 4,970 UTF-8 bytes，reload 後與外部
sidecar 完全一致；凍結的上傳包未修改，繁中後台資料亦未重匯。

H01 原日文正文保留 `117/118 native clear + 1 exact owner-accepted mtua`
既有資格，沒有改稱全正文 native PASS。正文與既有標題沿用原片；H01 結尾
重建推論的確定語氣、U02 2013 解密範圍，以及共用片尾文件的舊 17 秒建議，
各有獨立後續任務，沒有修改原片或接管其他製作工作。

## 2026-10-13 路徑可攜性與收據

為排除公開儲存庫中的個人主目錄路徑，四份片頭規格移除可由 `--sources`
推得的 `source_doc` 欄位；工具預設改用目前使用者的主目錄，文件範例改用
`<home>` 或相對路徑。未變動影片、字幕、音軌或既有審查收據。規格新舊
SHA-256 對照及續跑限制見 [PORTABILITY.md](PORTABILITY.md)。舊版四份規格
原始位元已保存在外部備份收據目錄，並由備份作業複製到 VPS，4/4 SHA-256
比對一致；既有審查與修訂收據仍綁定舊版雜湊，沒有重綁。

本次檢查：`repo-hygiene` 3/3、Curio 專屬測試 16/16、`check:tasks` 均通過；
實際 FFmpeg 合成 smoke 通過，產出 1,740 格與四語共同時間軸。完整
`test:docs-videos` 在 Windows 系統 Node 24.13 為 214/215：唯一失敗是未修改的
`imported-long-languages/runner.test.mjs` 另啟 Node 時退出 3221226505，沒有
stderr；單獨重跑同樣失敗。WSL Ubuntu 可啟動，但未裝 Node，故無 POSIX
複驗結果。這不改寫上方 2026-10-12 bundled Node 的歷史測試紀錄。
