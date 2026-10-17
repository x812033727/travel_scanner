# A01 詞典重設候選：獨立程式審查（2026-10-16）

**結論：PASS，僅限離線提案與 80→81 筆本機快照過渡檢查。正式環境維持 HOLD。** 本審查沒有寫入正式機、建立第 81 筆事件、核准影片、啟動模型或媒體製作。這份文件也不是程式所需的 `independent-review.json` 或站主的正式機寫入核准。

## 凍結版本與方法

| 檔案 | SHA-256 |
| --- | --- |
| `rebaseline.mjs` | `3fc95650b906d265c23e1d103db4ef58c21dbed3f2edb311c7e50dfb694136dd` |
| `rebaseline.test.mjs` | `d6ee383b7fe3c08beffaf515f5ecc2e186cfa8026a6ad2d1f71def9d474cc84d` |
| `README.md` | `2ebda1e3859bffa8a52a8868a8df8ad12ee9adc63f65faf0a9e090f63c40be4d` |

我逐段讀取候選程式與原 `A01-host-inspect-candidate/inspect.mjs`，重跑 `node --check rebaseline.mjs`（exit 0）及 `node --test rebaseline.test.mjs`（**12/12 PASS，exit 0**）。新增負例涵蓋章稿只有 `say` 命中、`video.json` 只有 `say` 命中，以及 `video.json` 無 `say` 時的 `text` 命中；三者均拒絕提案。檢查前後三檔 SHA 一致。

## 固定快照讀回

我以 `A01-live-readback-20261016.md` 記載的 **06:24 UTC** 本機解開快照，搭配保留的舊版 `A01-round10-candidate/evidence/round9-lexicon.json`，唯讀重跑 `--snapshot`。原封存 tar 的記錄 SHA-256 為 `3ec1f7d2ade117456f875dab1b2eae8fa3f2d2d6372020bc49f1f50806b12676`；本次重跑驗證的是解開後的本機檔案，未重新向主機擷取。

- 提案 exit 0；`plan_sha256` 仍為 `3ca62cfa4386c43dd0d45a6554fa3df63ddceb51f23bd48e9a9de9c2ab693f58`，來源組合雜湊從 `cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b` 指向 `2a54ed212c1d876664e17f73fc39f8a20b1ddddccb6c877de54c694c5634501a`。
- 原 80 筆索引清單釘選 `ada7ff1859788310fcda7ca35da052a2c4f1009b2c9058454b0e1b4d74d3614f` 與鏈尾索引 `c7ddb6b5796605c08b3c47c305864eddf28e5246ee6ad8426c3601637ecdc9a4` 保持一致。除詞典外，來源圖各欄均須與鏈尾相同。
- 舊、新詞典位元組分別符合固定 SHA `ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9` 與 `835e09df378d0c1b542b89c3fc44b2583b201217679267bce1146c638187d9c1`；295→297 詞條，僅增加 `pull: null`、`request: null`。
- 修正版同時掃六章與 `video.json`，依實際 TTS 選擇 `line.say ?? line.text` 檢查兩詞；固定快照的兩組各 92 條旁白、`say` 均為 0、命中均為 0。再以與當時部署 commit 相同的四個相關程式檔，在本機比較舊、新詞典：`speechHash` 均為 `361cd8ee38800ef2`，63 筆 TTS request 的 key 與 body 逐項相同。這是該固定快照在相同程式下「配音請求不變」的離線證據，不是正式機實際試播或供應商執行結果。

## 過渡檢查與邊界

程式先要求原檢查器在固定 80 筆鏈、安裝收據、歷史索引與鏈尾釘選通過後，**僅**因 `SOURCE_DRIFT_FROM_TIP` 拒絕快照；再核對唯一詞典差異。擬議第 81 筆索引以原鏈尾來源雜湊為 `before`、新來源雜湊為 `after`，綁定外部審查與 record-only 收據的原始 bytes SHA。過渡驗證要求前後快照分開、恰好 81 個事件 ID、舊稽核及安裝收據 bytes 不變、新事件／收據目錄只有預期檔案、來源圖與新索引清單／鏈尾釘選相符。測試覆蓋偽造舊鏈或新索引、偽造審查／收據、重複事件、並發詞典或歷史資料變動及部分寫入；均維持 HOLD。

**正式環境尚缺：** 新鮮且可證明來源的完整不可變主機快照；真正獨立審查者核對精確計畫與詞典寫入來源；外部驗證審查者及操作人身分、站主對這筆 A01 稽核與 record-only 收據的限縮寫入核准；STOP／LEASE／工作／US$25 帳本等即時前檢；經審查的安全追加程序與寫後第二次主機讀回；將正式檢查器的 80 筆要求及新釘選升級為 81 筆。程式中的姓名和 `owner_approval_ref` 字串本身不能驗證身分或授權。共用詞典仍可再次漂移，須另行處理穩定的每片來源綁定。A01 敘事 PASS、確切實稿審查、部署競態與付費製作關卡亦未由本審查解除。
