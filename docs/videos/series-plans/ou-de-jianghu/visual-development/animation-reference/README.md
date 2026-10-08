# 第一集九人動畫參照包

沿用站主選定的「華麗古裝與細緻人物風格」，補成可審閱的 **74 張新參照＋9 張沿用正面全身**。每人六個方向（正、背、左右側、左右3/4）、六表情板、三組動作階段板、服裝／手／冠／識別物细節；另有九人色彩尺度板與剪影板。每個板面只算一個 PNG，不把格子當獨立圖。

- [媒體清冊、尺寸與SHA](media-receipt.json)
- [完整生成與修訂提示](prompts.json)
- [逐人製作審查](review.md)
- [另一位審查者的實圖抽驗與修訂複看](../handoff/character-reference-independent-review.md)
- [原27張畫像](../episode1-portraits/independent-views.md)
- [正式匯入能力與隔離pending驗證](../import-contract/README.md)

本機圖冊在 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/animation-reference/20261008/gallery.html`，原圖皆保留在同目錄，imagegen 的初始輸出亦未刪除。清冊列明每個最新 key、原生尺寸、歷史版本與12份正典來源 SHA。`build-receipt.mjs <首集媒體目錄>` 可重新核對原件並生成圖冊。

**這是2D／I2V參照候選包，尚未代表個別圖像正式採用、分層骨架、3D模型或動畫通過。** `proposed_reference_set_complete=true` 表示用途齊備；`animation_reference_ready=false` 保留正式採用與製作驗收的區別。既有九張正面母圖已真實匯入新的隔離pending工作區，但没有judge、choice或owner approval。

## 使用規則

1. 先以正面頭像辨臉、全身母圖辨服裝，再看角度與細節；表情板是臉部近景，裁去部分冠頂不取代完整冠圖。
2. 左右一律指角色本人，不能水平翻圖替代不對稱衣袖、霜花、眼傷或持物手。
3. 燕迴右3/4採垂刀中性姿態：穿袖右手持刀、裸左臂放下。它不是其餘扛刀姿態的精確轉台中間格。
4. 殷無聲表情與動作保持閉口、不以說話嘴型表演。月牙、金印及黑風另在受控場景道具卡，不能常駐普通定妝。
5. 髮長、冠鏈及刺繡仍有生成透視差異；此包供設計約束，逐鏡關鍵影格仍要核對。尺度板只是相對高度提案，不設定正典公分數。
6. 多數全身原生為1024×1536；先前2048長邊是編輯建議，這次沒有用放大冒充原生達標。細節特寫要用局部參照，不能把隊列小臉當特寫母圖。

多圖並不因放進資料夾就自動被模型讀到。原生look目前每角色採一张基底圖，其他參照需按當鏡用途提供；實際request參照SHA、關鍵影格與三鏡小樣仍依[開拍包](../episode-plan/preproduction-package-v3.md)驗證。
