# S38 R8al PF033 來源字卡獨立紙審

2026-10-22 UTC。審者 `/root/s38_pf021_last_paper`，未撰寫此字卡或claims附註。結論：**PAPER PASS**。沒有媒體、creative檔案修改、manifest／ledger變更或Git提交；本票不代表新原圖、站主聽審或成片已驗收。

現稿video SHA-256 **`10e8aeedddfd6572ed3ab1d8390b9a5e50b85f73749f4315761ddd74cbc08853`**，script `2be40fda932ec6881f9f9cc1cb504bbe3705157f0c0e8a15cf74f1044c8e0314`，claims `65d2d3c70735495fb4c9e42806a414fc5dba90a67c4aa3eaaae4a9f12c30e464`。verify127作者差分SHA `9d07fcc4aa64ca3a8d1cbbe41b342115fa676985603024264efed8646ff24198`。

## 固定來源與中文譯文

重開固定Pepys日記1666年9月2日條目L65856–65860，全文SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。他記沿Watlingstreet行走，人人負載物品離開、有人連病人及床搬走，L65860直接寫 `goods carried in carts and on backs`。字卡 **「家當裝上車，也背在人身上」** 忠實呈現車載與人背兩種搬運；沒有加入物件數量、撤離成功、特定家庭或火勢結果。`佩皮斯日記・中文譯文`及`街上的搬運人潮・1666．09．02`明確標出翻譯、脈絡與日期，不冒充原手稿或錄音。既定旁白「沿街有人背著包，車上也堆滿要搬的家當。」仍與同段來源相容。

作者記錄PF033第一張有現代道路漆線而退件、後兩張因攝影背景機器FAIL，故三張耗盡後改來源卡。帳本核實PF033已有三張ready原生image；**沒有第四張放行**。這張來源卡只放史料譯句，不把未通過的圖片升格成已驗收。

## 改動與沿用證明

verify127的old／new完整場景與稿件逐字相符；把現PF033反填old、維持原JSON格式序列化，逐位元組復原前稿video SHA `5b2ba6712bbff7b021265864d2182a483c2387db592ac6f83b794b84c3f93fe9`。唯一場景改動是PF033由shot轉big；其112句中的原台詞與emotion不變，其他111個完整場景物件不變。

verify125原十九景中，除PF033轉卡外的**十八個石地prompt逐字相同**，繼續承接verify126的地面增量PASS；PF035–PF111剩餘77個完整場景亦未新增差異。全片展平112個口播ID／文字與前稿相同；script112行旁白與Git HEAD逐字相同，並逐句等於現video。script新SHA只是官方重新產稿後補PF033`（big）`標題及刷新雜湊頁腳，沒有聲音文字改稿。claims只補本卡來源與退件界線。

正式lint exit0，**0 errors／0 warnings**；正文101shot／111非outro場景（91.0%插圖），最長連卡仍3，不違反系列來源卡比例／連續上限。未把未通過圖像或來源卡當作插圖計數。

## KEEP與真實付費狀態

只讀active manifest SHA `140ac1da1f3dfc4b1feda1eb537c29488c355087d215fdbd1615db43c285fad9`，24個KEEP完整場景與前稿相等、選用實檔SHA逐張吻合、judge PASS且無needs_review。STOP在位、jobs空；PF033失敗入選條目已隔離，本審沒有移動它。

Ledger SHA `fc723b59614509fa6760656806b5ef59ba48512e02cbe385b52dbafcf44582b8`：實付US$1.2310／86image／85judge／1music，舊US$0.0035 reservation保留。PF033實際3張；**PF035實際1張ready快取圖、尚待judge**，不能叫作零次未畫。PF036–PF111才是76個零次新景。PF035必須從原快取接回，最多再買兩張，不得因新visual hash重設三張上限。

按現價剩餘PF035快取圖一次judge＋最多兩個新image／judge、其餘76景各三試，上界US$3.115；加已付及reservation為 **US$4.3495 < US$4.58**。本票支持在STOP下保留24個KEEP條目／實檔、安全離線重綁現稿、驗即時模型／價格／餘額／dry-run及快取key後，依原整集授權續做PF035–PF111有界流程。舊來源卡與耗盡景不重開，KEEP只吃快取，不另逐張請使用者授權。這仍是紙審PASS，未自行解除STOP或宣稱整集完成。
