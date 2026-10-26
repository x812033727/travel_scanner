# ForTy：海外參考與本片製作映射

2026-10-25。沿用本日已核對的六片，沒有補搜湊數；本輪沒有觀看影片或量鏡頭，只有題目、索引、章節／逐字稿文字觀察。完整數據與快照矛盾保留在 `reference-study-20261025.md`。**沒有找到可核對的ForTy直接熱門影片，不能說本題本週已爆紅。**

| 既有候選（研究用意譯） | 時窗／第三方點閱快照 | 對ForTy的實際關係與用途 |
| --- | --- | --- |
| [Matthew Berman：Kimi K3.1](https://www.youtube.com/watch?v=5sEVvu4mQ8g) | 10/24，7日內；Jukebox10/25約102K／約21h，約615K訂閱 | 不同主題，只保留候選稽核；不借它的案例證明ForTy |
| [Matt Wolfe：11件AI突破](https://www.youtube.com/watch?v=umGZrkyTRtw) | 10/21，7日內；Trari本session10/25早先134,641，首日87,087，約1.02M訂閱；重開redirect失敗 | 科研題的間接線索。已讀逐字稿討論研究演示與限制，可啟發追問資料如何支持結論；不是ForTy報導 |
| [Two Minute Papers：DeepMind生命科學訪談](https://www.youtube.com/watch?v=Wkaw03p3BrM) | 10/07，30日內；YT Pro Analytics頁標10/22約153.7K，約1.84M訂閱；搜尋快取154.4K不同 | AlphaGenome、非ForTy。摘要有研究者參與，只借「追原始研究」的研究方法 |
| [Two Minute Papers：Gemini 4 Argon](https://www.youtube.com/watch?v=LWxX6vvHfrc) | 10/19，7日內；同頁10/22約206.8K，搜尋快取221.6K不同 | 不同模型題；題目提供「主張與結果要拆開」的編輯問題，不能當已觀察的剪輯手法 |
| [Two Minute Papers：DeepSeek記憶](https://www.youtube.com/watch?v=4fLVq6HJsKc) | 10/11，30日內；同頁10/22約328.9K，搜尋快取330.7K不同 | 不同機制題；單一機制的題目範圍可借鑑，沒有觀看其圖解與鏡頭 |
| [Y Combinator：形式化證明與漏洞](https://www.youtube.com/watch?v=X7oI4Umt3DU) | 索引10/17，30日內；沒有可靠點閱、訂閱或片長快照 | 不同研究題，僅章節文字可查；不納入「熱門」或ForTy需求證據 |

數字都不是即時YouTube API；Berman／Wolfe／Two Minute Papers的上架年齡、規模及長講座／一般長片不同，不能按總觀看排序，點閱／訂閱也不是CTR。單次或衝突快照無法推出成長曲線，不能推論某種手法造成高觀看。

## 本片新增證據與原創映射

主問題：**同樣呈現為一個森林類別的像素，怎麼讀出不同程度的模型支持？** 正向收穫是會讀一格真實ForTy資料、算出第六類與分類，並對並列最大值作正確判斷。時長依完整製作規格決定，不靠重述補滿。

| 參考層級／借的方式 | 自己新增的證據 | 本片原創畫面／旁白設定 | 驗收 |
| --- | --- | --- | --- |
| Wolfe逐字稿中的科研線索與演示限制；文字層 | 官方2020 COG實際兩個ROI，另有獨立解碼核對 | 開場直接比較A分數0.992與B並列0.344；明列本片argmax/tie慣例，展示實際衍生圖 | 對照 `forty-demo/README.md`、兩份ROI JSON、`independent-results.json`；不是官方App截圖 |
| AlphaGenome訪談摘要提示追到原始研究；文字層 | DeepMind文章＋Google catalog＋Figshare版本日期 | 短時間交代本週介紹及2017–2025早期序列，再把本次2020示範年份放在畫面 | 不把5/22已公開的基準圖叫本週首發；不稱本次測到年度變化 |
| DeepSeek題目的單一機制範圍；編輯推論 | 真實五band與公式Other=250−sum；A實際值[0,248,0,0,0]→Other2 | 依輸入、加總、用250扣除總和、除250、比較最大值順序，旁白逐步可跟算 | A六分數為[0,.992,0,0,0,.008]；旁白和畫面同步，不只閃算式 |
| Gemini題目啟發把結果與解釋拆開；編輯推論 | B實際值[0,86,0,1,77]→Other86；第2、第6類同0.344 | 第二例讓「最大值＝唯一答案」的直覺遇到實際並列；解釋本片NumPy取第一個的慣例 | 不聲稱官方獨立類別圖使用相同tie規則；B是刻意選最低最大分數，不是隨機精度抽樣 |
| 全部參考不提供本片原始畫面 | 官方未校準說明、類別F1與資料來源 | 用一段回收分數、地面真相、資料年份與採用範圍，來源放字卡／說明欄 | 0.344不能說34.4%正確率；不把2020分類當現況、因果或法規結論 |

本片獨有的資訊增益是**真實且可重做的資料→六分數→並列處理**。不是翻譯海外腳本、重製縮圖或下載他人整片。來源與時間戳服務證據，不能整段旁白反覆報出處。

## 交製作時保持的界線

- 真實ROI讀自2020；2017–2025是本週新聞介紹的早期序列，本次沒有成功取得其像素／年度App操作。App目前只見一般底圖，不能冒稱ForTy overlay成功。
- A固定座標附近、B刻意從已下載block挑低分並列點；二者不是地面標註，不估整體或單點正確率。B本片圖採第一個argmax，不替官方作tie保證。
- 來源資料CC BY4.0；依 `forty-demo/README.md` 列Neumann等、DOI與裁切／殘差／argmax改作。這不授權衛星底圖或文章其他圖像。
- 主來源： [DeepMind10/22](https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/)、[Google catalog](https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection)、[Figshare API](https://api.figshare.com/v2/articles/32288616)、[正式論文](https://www.nature.com/articles/s41597-026-08299-5)。Nature全文取得有限，不能說已逐頁讀完。

沒有實際觀看參考影片，故沒有任何剪點、音效、運鏡或留存量測；所有畫面順序與計算呈現都是本片原創製作設定。
