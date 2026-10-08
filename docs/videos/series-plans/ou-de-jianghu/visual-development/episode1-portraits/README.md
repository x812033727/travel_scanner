# 《偶的江湖》首集九人畫像

**2026-10-09 更新：**目前 27 張獨立視圖以 [finalized-views-receipt.json](finalized-views-receipt.json) 為準，沈歸鶴全身改 v3、半身改 v2，概念改 v5。統一圖庫在 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/final-art/20261009/gallery.html`；下列 2026-10-08 圖庫與收據保存歷史，不再是最新入口。原生尺寸已按身份／服裝參照用途作編輯處置，沒有放大或宣稱最終影片尺寸通過。人物圖的微小手邊掛飾不可用作扇拓撲依據，扇結構以 construction-details v3 與 personal-prop-states v3 為準。個別圖像仍待站主正式採用。

2026-10-08。依使用者選擇的「保留目前華麗古裝與細緻人物風格」，已從九人概念延伸出 **27 張獨立視圖：每人正面頭像、3/4 半身、完整全身各一張**。殷無聲、燕迴、洛青衍半身的指尖裁切已改為 v2，保留三張舊版，因此這階段共 30 個 PNG。另有前一階段 14 個概念 PNG，分開保存。

27 張均為分別生成的單角色視圖，已逐圖實看及核對來源；不是拼板裁切。共同風格已接受，個別圖像與微小服飾細節尚待採用。半身／全身的原生尺寸低於 [製作清單](../production-list.md) 的建議，沈、姬兩張半身也較建議比例窄長，仍需記錄最終輸出選擇。

## 最新獨立視圖包

圖冊：`<VIDEO_WORKDIR>/ou-de-jianghu-e001/portraits/20261008/gallery.html`。可依角色篩選、點圖放大；只展示 27 張目前候選，三張舊版保存在同目錄。

- [獨立視圖交付清單](independent-views.md)：九人版本、原生尺寸與後續製作順序。
- [independent-views-receipt.json](independent-views-receipt.json)：30 檔 SHA-256、尺寸、版本、27 張目前候選、角色來源與接受狀態。
- [independent-view-prompts.json](independent-view-prompts.json)：30 次完整提示及參照圖 SHA。
- [三主角審查](independent-main-review.md)、[六配角與三張 v2 覆核](independent-supporting-review.md)：實圖結果與可見範圍。
- [圖冊與包裝驗證](independent-views-verification.json)：檔案完整性及瀏覽器載入、篩選、放大、手機版檢查。

## 前一階段：概念圖冊與資料

媒體與可放大的圖冊保存在 repo 外：`<VIDEO_WORKDIR>/ou-de-jianghu-e001/art-direction/20261008/gallery.html`。同目錄保留全部 PNG 與生成提示。路徑是媒體索引，不是 repo 相對連結。

- [media-receipt.json](media-receipt.json)：14 檔的 SHA-256、尺寸、原生成檔名、版本、來源 12 檔的 SHA 與接受範圍。
- [prompts.json](prompts.json)：新增六人的完整提示與風格參照。前三人的提示、修訂與方向接受見 [美術定調](../art-direction/README.md)。
- [correction-prompts.json](correction-prompts.json)：沈v3、洛v2、殷v2的局部修訂提示與來源版本。
- [review.md](review.md)：新增六人的獨立視覺審查；前三人見 [定調審查](../art-direction/review.md)。

以下九張概念是獨立視圖的來源，概念階段共 14 個 PNG（九張修訂候選、五張歷史版本），皆為 1536 × 1024。

| 角色 | 概念來源檔名 | 基底造型與後續細節 |
| --- | --- | --- |
| 沈歸鶴 | `shen-guihe-concept-v3.png` | 白冠單羽、白銀鶴紋與淡藍腰帶。白紙扇已合攏；冠、衣紋与扇子局部仍待固定母版。 |
| 姬無霜 | `ji-wushuang-concept-v2.png` | 銀髮黑銀鳳冠、黑紫霜蕨紋。補清楚手足、袖口與冠鏈；左眼霜花不可鏡像。 |
| 寂聞 | `ji-wen-concept-v1.png` | 蓮冠、金紅袈裟、左臂三圈念珠。與其他人統一皮膚及明暗畫法。 |
| 包三錢 | `bao-sanqian-concept-v1.png` | 歪髻、後推草帽、赭褐補丁袍、三枚方孔錢。固定帽位、錢串與錢袋連接。 |
| 殷無聲 | `yin-wusheng-concept-v2.png` | 左頰舊疤、炭灰束腕與右肩背劍。髮環及可見劍柄護手已改素面，白邊收窄、雙手下垂；完整劍鞘待側後／背面核查。 |
| 燕迴 | `yan-hui-concept-v1.png` | 歪裂銅冠、鏽褐破袍、缺左袖、右肩單彎刀紅纓。補不被刀與袖遮住的持物參照。 |
| 聶孤鐵 | `nie-gutie-concept-v1.png` | 灰髮、左眼白翳、鐵箍與黑皮圍裙、鏽紅半袍、單把鍛造鉗。固定舊傷圖樣與鉗子結構。 |
| 玄門長老 | `xuanmen-elder-concept-v1.png` | 白髮長鬚、深青道冠、雲松紋與左臂拂塵。固定道冠、拂塵支點與袍層。 |
| 洛青衍 | `luo-qingyan-concept-v2.png` | 海綠象牙白波紋袍、白貝扣與半束髮。珊瑚冠已改為低矮橫向；後續固定冠枝與衣紋母版。 |

角色身份依 [cast.json](../../production/cast.json)、[cast-notes.md](../../production/cast-notes.md) 和 [character-design.md](../character-design.md)。殷無聲保持閉口，沒有以台詞替代手勢；燕迴缺的是角色左袖；聶孤鐵白翳在角色左眼。姬無霜與洛青衍的頸後記號不在中性畫像常露。不畫說書人肖像，也未提前公開匿名黑風的真身面孔。

## 接續製作

1. 從 27 張已實看的視圖固定個別採用臉、冠飾、主紋與掛飾母版；優先補殷的完整劍鞘與各道具連接。姬的雙手、雙鞋已在獨立視圖補清楚，三張半身裁切也已修正。
2. 依實際動畫與展示用途確定最終輸出尺寸、畫幅與留白，記錄採用圖 SHA 與接受範圍。保留原生圖，未將放大圖片當成新增原生細節。
3. 接續動畫參照任務，補左右側、背面、表情、手勢、道具與服層。角色多視圖須由同一造型延伸，避免每個角度重新設計。
4. 外部圖片匯入能力完成後，再經正常 look、judge、choice 和來源綁定；最後用連續三鏡測轉頭、冠鏈、衣袖及持物穩定性。

本輪完成九人獨立視圖候選；逐圖採用、動畫參照、正常 look 核准與動態測試仍在原任務清單追蹤。內建 imagegen 沒有回傳本輪帳單，因此收據不宣稱免費或成本為零。
