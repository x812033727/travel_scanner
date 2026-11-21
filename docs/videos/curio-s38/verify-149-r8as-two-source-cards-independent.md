# S38 R8as PF053／058 來源卡獨立紙面覆核

**PASS（來源、差異及卡片限制）。** 審閱者 `/root/s38_pf021_last_paper`，不同於verify148作者。

直接比對Git HEAD與現檔，只有PF053、PF058的template/data改動，逐字符合verify148；其餘完整場景、112個spoken line物件、其他camera與look皆相同。兩張卡原shot camera隨模板移除，未改其他鏡位。script官方重產且台詞不變；claims未改。

## 固定來源

重讀 `/tmp/s38-r8j-pepys-4200.txt` D3 L65955–65973：

- PF053「金錢與銀器／佩皮斯親自押送」：L65956–65959明記清晨送車、money and plate、自己穿night-gown乘車；plate在財產語境指金銀器皿，中文銀器符合既有查核句。卡片不新增財物數額、誰運送或後來結果。
- PF058「塔丘 → 碼頭／箱子由人扛送」：L65967–65970記we did carry them (myself some) over Tower Hill，接著下到停於next quay的lighter。箭頭準確概括路徑，沒有把塔丘當目的地或聲稱船已航行。箱子沿用原台詞與已查核畫面中的家當容器，是搬運示意，不聲稱原文逐字指定所有物品皆箱裝。

正文111景中96張shot、15張卡，插圖比例86.49%；最大連續卡片3張，符合70%／最多3張門檻。PF053及058兩側均有shot，未形成額外連卡問題。獨立官方lint：**0 errors / 0 warnings**。

PF053與PF058各3次actual用盡、0剩餘，不得第四張。PF060仍1actual且machineFAIL、最多另2次，未修改該景。STOP與jobs狀態不由本票改動；本次只寫紙面驗收，不改媒體、manifest、ledger或git，沒有付費。

## 凍結檔案

- `video.json` SHA-256：`d17513ffdae191e3d3d382c0fa17f8c04f40ff8e7f5359e585af0537c9a8fab7`
- `script.md` SHA-256：`7d96b532b4c28838094cea6de4cc931d43f13d421f61aec26270b9e97e5f9f5e`
- `claims.md` SHA-256：`b1a86f5161280e48027cfb6ba1716a8a9eaf0136326a0b4120477507a3c6b02e`
