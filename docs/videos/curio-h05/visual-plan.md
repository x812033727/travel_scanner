# H05｜A 版視覺製作前清單

2026-10-12。依已選 A〈從河岸贖金，倒追失蹤的人〉、[brief](brief.md)、[歷史研究](research-history.md)、[鈔票研究](research-money-science.md)、[素材查核](research-assets.md)及系列 [look](../history-curiosity/look.md)整理。企劃 SHA：`b384685061f457187f4ba3c189ebc7c99dfa275607853f397c2e8ec5f5df2803`。本文件是預檢方案，沒有生成或審看本集 AI 圖；完整稿尚待交接，以下 pilot 名稱不是已存在的 scene ID。

## 路線與畫面分工

- 僅繁中；沿用選定第 3 版系列 look、MiniMax `image-01` 情境插圖與原生投影片。提示詞只寫景別、物件、空間與光線，畫風放在 `look`；不新增手繪 SVG 或其他生成模型。
- AI 插圖承擔場域與物件氣氛；三張原始檔案照承擔物證；原生 `stats`、`steps`、`compare` 等卡片承擔數字、年份、研究層次與限制。情境插圖不能冒充現場照片、顯微觀察或原作者數據。
- 正文目標 10–11 分鐘、至少 8 分鐘；每 5–8 秒有內容上的畫面變化。白天河岸、機場、明亮文件桌至少占一半，情境插圖目標約 60–70%。這些是企劃目標，實測比例／時長待 TTS 和時間軸，未宣告通過。
- 每張一個主體、至多一個動作；物件近景不塞人物全身服裝。以有限正面物件構成取代 `no/without` 禁物清單。空景尤其查石頭、包裹、窗戶是否長出眼睛、手腳或吉祥物。
- 不描繪近代當事人的臉；背影不補心理或表情。人物不是每章必加的配額。本集優先物件、空座椅與場域，避免為符合通用「表情」規則而虛構肖像。

## 三張 pilot 建議

全稿凍結後選對應現有 shot，沿用該景旁白與 camera；下列是構圖草案，不直接套入來源檔。三張分別驗空景、歷史室內物件、現代研究情境，均不含可辨識臉。

| 暫名／預期位置 | 正面提示詞草案 | 像素驗收重點 |
| --- | --- | --- |
| P1 `pilot-river-day`／開場或1980河岸章 | Wide shot of a broad sandy riverbank in soft overcast daylight. A gently curving strip of damp sand fills the foreground, broad calm river water fills the middle distance, and a low wooded bank lies across the water. Small scattered pebbles rest on the sand. The scene consists of sand, pebbles, river water and the low distant tree line. | 讀成寬河與低河岸，不是海灘浪潮、峽谷、峭峰或都市碼頭；空景沒有擬人石頭或隱藏角色。泛用場域示意，不標成精確 Tena Bar 現場復原。 |
| P2 `pilot-cabin-object`／1971航班章 | Close-up of a closed plain leather briefcase resting on a fabric-upholstered passenger seat inside a 1971 airliner cabin. The case has a simple handle and two small metal latches. The seat cushion, armrest and a rounded cabin wall with an oval window surround it. Soft afternoon light enters from the window. | 關閉公事包是主要物件，扣件不似眼睛；機艙物件合理，沒有現代座椅螢幕、手機或品牌假字。不能看見炸彈內部，不能把公事包內容當作已驗證爆裂物。 |
| P3 `pilot-research-desk`／2020研究章 | Medium shot of a research desk in diffuse daylight. A laboratory microscope stands beside a closed plain specimen box and a blank notebook on a wooden worktop. A simple wall and one window form the background. The microscope, specimen box and notebook occupy the central area. | 顯微鏡是合理儀器而非多鏡頭機器人；文件與盒面不長可讀結果；沒有鈔票、顯微影像或偽造研究數據。只作泛用研究情境，不聲稱是作者實驗室或本集重做試驗。 |

Pilot 必須另看 actual selected 像素並綁檔案 SHA；judge 分數不能代替材質、科學與場域判讀。物證照片無須透過 pilot 重畫。

## 全稿與實圖高風險清單

| 風險 | 必查畫面／修正方向 |
| --- | --- |
| 727 機尾階梯 | 出口位於機尾腹部，不在機側；機尾、機身與階梯需能讀成同一結構。只呈空景與概念位置，不補開門步驟、飛行配置或跳傘技術；畫不清時改用原生文字關係卡，不能以錯誤飛機圖定案。 |
| 未知跳傘經過 | 不生成確切離機姿勢、降落位置、是否開傘、落水、埋錢或死亡畫面。雨夜只是敘事場域，不畫成已知完整路線。 |
| 1971／1980／2020 混用 | 售票桌、機艙與舊文件沒有智慧型手機、平板、現代安檢及座椅娛樂螢幕。現代研究桌可以有研究儀器，但不要沿剪接暗示它在1971年已使用。日期由卡片顯示。 |
| 河岸與錢的路線 | 白天低河岸不能變海岸、聚落或高山河谷；不得畫已確定的漂流線、入水點或埋藏者。推定落區與發現地以原生卡片區分，不能把約30公里畫成實證運輸距離。 |
| 男孩背影 | 若旁白需要，只用單一、泛化、合理兒童比例的後背視角與一個靜止姿態。不要一張同時挖沙、拾錢、展示、奔跑；不畫可辨識的 Brian Ingram 臉、幼兒身體或成人手臂。發現動作若難以清楚呈現，拆成沙地空景與原件。 |
| 貨幣與可讀文字 | 鈔票面額、序號、Dan Cooper 名字只能來自核准原檔或原生文字卡。生成圖限封閉包裹、空白紙面、普通物件；不讓模型補鈔票、票券、航空商標或公文印章。 |
| 領帶與 DNA | 原件照片是領帶證據；不能搭「身分吻合」勾號、某人剪影或血緣樹使觀眾以為 DNA 已確認劫機者。來源不充分時不把可見飾件當作 clip-on 構造證據。 |
| 矽藻與科學證據 | 以原生卡片分開單張原鈔、現代對照、觀察及作者季節推論。不要生成顯微照片、假 Asterionella／Fragilaria、元素譜或研究曲線；本版沒有採用論文圖表。若日後新增原論文圖，須另登記圖號、原圖權利與是否含第三方素材。 |
| 比例與總數 | 四具傘是要求數，不畫成跳下時全部背在身上；36是獲釋乘客數，不用畫面人頭湊數。5,800美元是尋回部分，不能藉多捆道具暗示全數贖金。 |
| 縮圖與結尾 | 以物件／河岸為主，不用嫌疑人臉、生成鈔票、已破案或已證實死亡的圖章；文字不承諾已找出完整入河路線。 |

## 三段可檢驗的卡片

1. **名字對照**：原件姓名欄 → 購票用名 Dan Cooper／案件通稱 D.B. Cooper → 真實身分未確認。原件只放大版面顯示，不修補手寫字。
2. **2.9% 實算**：先辨識分子「尋回 5,800 美元」與分母「交付 200,000 美元」，再顯示 `5,800 ÷ 200,000 × 100 = 2.9%`，最後落在「找到部分錢 ≠ 知道人在哪裡」。不作通膨換算，也不把剩下97.1%當作已確定仍留某地的錢。既有計算收據 `_audit/recovered-ransom-calculation.json` SHA `610941f45724dd5d214b4d1f6c8f692a4d870e49488e66bbbcab9b3757cfad2c` 已讀回；數值為29/1000及2.9%。
3. **研究的三層**：樣本「一張原鈔的數個小片」→ 觀察／現代對照 → 作者推測較符合五月至六月浸水。相鄰卡保留「年份、入河方式、抵岸與埋入完整過程、人的身分和生死未由此確認」；不得把季節推論畫成1972年的確定日期。本集卡片是資料整理，不是新生成的科學證據。

正式 render 後逐個 reveal 看完整字、分子分母、繁中、來源與揭露；各狀態須對應當時旁白。照片卡另核檔名與實際 SHA、完整物件邊緣、姓名欄、署名及運鏡末端裁切；源圖原始位元組不變。
