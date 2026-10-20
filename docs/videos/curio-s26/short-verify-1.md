# S26 單支來源精華短片：開畫前查核

2026-10-20 初查時，長片 `video.json` SHA-256 為 `bd87f62f4c571e02c00447d93ce69e4c5caecd7a13a53cd3f477cc5babab9264`；當時 `shorts.json` SHA-256 為 `5309edd11497db09c332f8ae6badcfc1107ec0c09679c4ee954d07293fe6f759`。更早的長片 SHA `62cd30fb3bc2cfa261e97fa43783ab4c12abf501dcb66fbecb573535c973d116`、Short SHA `89a25e4f0a32ac73970a24ebb84b4d68b16c30b122c64724ad7f25b059e892d5` 也僅為舊草案；這四個 SHA 均不能綁定目前成品。短片只講一件事：卡爾 1841 年提到歸給瑪麗・安東尼的名言，同句仍標「不論真假」。更早的盧梭引文只稱「一位偉大的公主」，不能藉此替皇后署名作證。

七景均指向現有 `shot` ID：`ma070`（1841 年存疑語氣）、`ma065`（卡爾轉述並批評報紙建議）、`ma096`（以布里歐修話諷刺建議）、`ma071`（「人們歸給」及「不論真假」）、`ma072`（卡爾未自稱親聞）、`ma031`（盧梭匿名公主）、`ma075`（兩份文字保持分開）。對應固定來源為 `research.md` 的 K，1841 年 11 月第 5499–5512 行，以及 R-FR 約第 186–190 行與 R-EN 第 9700–9706 行。短片不宣稱卡爾是最初署名者、不把兩份文字畫成同一份現場證詞，也不推斷皇后絕未說過此話。

候選為一支 `from-episode` 精華，7 景、8 句、140 個字元；預估約 33–40 秒，實際 25–55 秒須待日後頻道語音量測。現行單支 Curio 規則的 `episodeShortsProblems` 與逐支 `validate` 均回傳零問題；所有 shot ID 存在。獨立審查者對初查版**精確 SHA** `89a25e4f…` 的來源歸屬、七景與長度預估覆核 **PASS**；報紙明標為卡爾的轉述，標題沒有暗示他是名言作者。

**初查當時尚未付費或出片**：當時 S26 圖像尚未生成，不能通過 `from-episode --check` 的關鍵影格雜湊綁定。這是舊版狀態；現行檢查見下段。

2026-10-20 第二版更新（現為歷史紀錄）：獨立定點來源覆核指出原 `ma072` 標題「他沒有親耳聽見」超出卡爾原文，已僅改為「卡爾未稱親聞」；修後 `shorts.json` 精確 SHA `5309edd11497db09c332f8ae6badcfc1107ec0c09679c4ee954d07293fe6f759` 獨立覆核 **PASS**（`/tmp/s26-short-source-addendum.md`）。當時 `from-episode --slug curio-s26 --check` 回傳 **1 Short valid、七張圖全部 SHA 相合**；所選 manifest SHA `5d2ef215180433525b523e6d82a7622e95b92febee3179ac48d050c818c53490`，七景原生尺寸均無史料／人物硬傷。`ma031` 主體偏左，直式 9:16 自動中心裁切可能只見空白文件，建片後須看實際裁圖。這一版當時尚未出片。

## 現行七幕精華與成片綁定

2026-10-20。現行長片 `video.json` SHA-256 為 `bb524cc7846a17a102d8b8c50322061977cdc897b097b7473c5b22e9edd77996`；現行 `shorts.json` SHA-256 為 `d9f59d6c925ec637a6696a5941da9df5332a1922370b4a98461c36a2e1684850`。後者以已核對的長片逐句原音改為七幕八句，畫面依序使用 `ma001 / ma096 / ma071 / ma007 / ma030 / ma031 / ma075`。第三幕畫面 `ma071` 配長片已核 `ma002` 問句；獨立讀者覆查這七幕文字、固定 K41／R-FR／R-EN、畫面與聲音來源層級無硬傷。`from-episode --slug curio-s26 --check` 重新通過 **1 Short valid、七圖 SHA 均相合**。

本機成品 `script.json` SHA-256 `13bfa382e792b8c98fc811134bc4dc383e88ceae2497da6c671a1c179c8c43a7`，`verify.json` 綁此 SHA 與四項固定史料結論；MP4 SHA-256 `ec20dd8b44897237c679712352ffb7fba738fec90f5dff979c6c339bbea592b8`。八段旁白沿用七句長片原 WAV，`ma007` 在原有停頓切成兩句字幕；後半段原樣本作 −1 dB PCM 增益以通過真峰值限制，沒有重錄或改字。`check-audio` 八句皆過、零旗標。四語字幕各八 cue 時碼相同。實際直式成片的 `ma031` 人物遭中心裁掉、保留空白書頁與來源標題；列為構圖 WATCH，未見假字或來源反轉。詳細 QA 與尚待補的真實 YouTube 長片 URL，見 [short-delivery.md](short-delivery.md)。
