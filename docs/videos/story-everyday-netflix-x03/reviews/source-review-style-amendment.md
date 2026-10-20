# X03 Netflix｜全片畫風補充的獨立來源審查

**判定：PASS，僅限 `look.style` 的來源與敘事風險。** 本收據接續[視覺提示詞審查](source-review-visual-revision.md)及其不可變的[修訂收據](visual-prompt-revision.json)，由前稿 `video.json` SHA-256 `4ba2b46746b6bc83960cdf45aa557ba408f280a8e9c4086d27ff99cafd638d8b` 接到現稿 `08c931bb000f373fbf5778d02b0703ef1a8b5144c665bfa30afda7c44ed3e5ac`。這次在既有 `cute-mystery` preset 之上加入英文全域畫風描述：維持台灣 YouTube 解說卡通的扁平色彩、深色線條與原配色；只有明確要求人物的鏡頭才畫大頭小身人物；純物件鏡頭的光碟、信封、電腦及郵袋不可長出臉、四肢或吉祥物特徵。此條件不增添 Netflix 的歷史主張。

獨立機械核對：現稿 80 句的顯示文字、`say`、句 ID、所屬場景與順序計算值 `displayedNarrationSha256` 仍是 `787ae902895422b416537ad01da8b25eed0b0f763ae325ab9af884c2d1c48fcf`，與不可變視覺修訂收據一致；`speechHash` 仍是 `a3d7c9b185b3b334`，與已量測 `timeline.json` 一致。刪除現稿新增的 `look.style` 後，排除靜圖提示詞的完整文件 SHA-256 為 `493079bd898700009f2d40978ba9e020972754454dae92896885e72989230747`，與前次視覺修訂收據相同；因此在非鏡頭提示詞欄位中，**只有 `look.style` 變動**。現行 `drafts/lines.txt`、`video.json` 與 `source-matrix.md` 的 80 句文字與來源代號逐項一致，12 張資料卡及 3 句原生片尾仍與儲存庫 HEAD 相同。

這項畫風規則有助於把申報資料的示意道具維持為無標誌物件，不把擬人光碟或虛構角色誤當史料。它不應遮掉鏡頭指定的兩條交付路徑、三片上限示意或郵寄道具；最終構圖仍需逐鏡檢查。`scene-nx0102` 的單張試作在工具評審中 `passed: true`，但評審也指出光碟套與回郵袋被合成一個物件，故**不能以此推論全批 65 張合格**，也不能把技術評審當成人工畫面批准。後續圖片仍按選圖雜湊、造假字樣、年代道具與數字口徑逐張覆核；本收據不批准語音、配樂、字幕或成片。
