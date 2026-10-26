# 原創縮圖subject與卡片視覺核對

[SVG](thumbnail-subject.svg)由[原創generator](generate-thumbnail-subject.py)確定性產生，再用ffmpeg/librsvg生成[PNG](thumbnail-subject.png)供原生thumbnail asset讀取。[來源與SHA](thumbnail-subject-provenance.json)記錄完整生成命令；原創素材CC0，沒有第三方圖片／官方UI／商標。

40列是本例真實回覆的顯示數，省略只表示沒顯示；圖內欄線是標明「原創示意」的簡化圖，不冒充40筆逐列截圖。下方是同一份配送表按條件查詢後另存的完整結果，可用CSV／Parquet重開核對；未放480／1200等後段答案。原始[預覽](../public-run/runlogs/agent-preview.stdout.txt)與[公開命令核對](../public-run/public-run-results.json)留存。

input-columns只移除與title相同的optional key，標題、五欄原名／中文意思與來源一字不變。原生重新capture該卡與thumbnail均0layout，其餘63state內容鍵與PNG SHA完全一致；沒有全片組裝、音訊或付費。root待看路徑在[視覺delta收據](../reviews/visual-only-source-delta.json)。
