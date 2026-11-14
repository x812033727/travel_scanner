# C04 來源 renderer 與後台分類

來源 `video.json.category=explainer` 只保留既有資料字卡的 renderer 相容性；`series.json.kind=story`、品牌故事新規則及後台 `story` 分類仍然適用。分類嘗試因原生卡片契約失敗，未採用；完整失敗稿與證據保存於 [story-category-attempt](history/story-category-attempt/)。

目前 source 已逐位還原為 `8549eb766873b65cb3453d03edfb5c2d151a3a9209578f3383cdc321c9620a75`，共圖計畫為 `666ce7c8ac4f41efa1c65c7d57ac0cf5a638a170558bca3b216abbe37240def2`。[還原收據](render-backend-classification.json)列出原 archive、各檔SHA及原獨立 verify 的精確複製來源；沒有新寫 PASS 或核准。

後續正常 report 由 runtime 代理先查證省略可選 `category` 是否保留既有後台 `story`，再用合法 report API 更新。這不是改來源類別、管理員路由或付費保護繞過；本任務沒有呼叫API。

實際 clean 國際主片仍須完整相符 QA 與當前 final 核准，之後才符合配音關卡。renderer 的 `explainer`、後台語言旗標及此還原，均不代表 clean 成片、實圖共用、配音或上傳資格。
