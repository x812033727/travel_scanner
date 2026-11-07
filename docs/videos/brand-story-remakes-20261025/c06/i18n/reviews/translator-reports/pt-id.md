# C06 葡文／印尼文文字翻譯自查

範圍為已凍結中文 R3 的八語文字準備；只填原生工作表 `text`，沒有 merge、SRT、音訊、時長擬合、媒體驗收或獨立 TEXT_PASS。

## 凍結工作表

- `pt.todo.json`：163句、6章、title／description／tags／thumbnail 全填；title 83 Unicode字元；整份 worksheet SHA256 `efb48f35580bb826acf07407bce01caefd1dd01de074cdb1c415fd66b7d879b4`。
- `id.todo.json`：163句、6章、title／description／tags／thumbnail 全填；title 67 Unicode字元；整份 worksheet SHA256 `72bdaba29864612cf9af642d6ac123e3d738d46433aecc9de617107c0571ced8`。

## 完整性與語意自查

- 遞迴移除 `text` 後，與各自不可變的純來源工作表完全相同；id、scene、todo、source、glossary、boundaries 等均未改。163個line ID及順序完整，6個chapter未移動，沒有空白文字。
- 說明欄全部來源網址保持原序、逐字相同；原件英文標題也保留。只翻譯說明正文及「查閱」日期標題。兩語標題均少於100字元。
- 全篇按來源逐句自查，保留你／我視角、疑問、想像場景與跨句承接；不新增歷史心理或公司因果。人名／品牌保留 Cleo McVicker、Noah、Joseph、Kay Zufall、Kutol、Kroger、Rainbow Crafts、The Strong、Fun Factory、Play-Doh、Hasbro。
- 2024數字保留為公司所述「年出貨逾5億罐／容器」；葡文是 remessas anuais de mais de 500 milhões de potes，印尼文是 pengiriman tahunan ... melebihi 500 juta wadah。沒有改成零售銷量、兒童數或當年單年銷售。
- 保留1933訂單、1949接手、1950年代初下滑、1955幼稚園建議、1956品牌／子公司、1957顏色、1960工具／同年5月專利申請、1965年1月核發、2026年7月成人產品各自年代。
- 專利中的包覆／濕熱糊化仍歸於作者解釋；黏結成分為「也容許加入」，不是必需或人人配方；密閉保存最長三年仍是「文本聲稱」並保留上限。乾硬不能揉回亦維持文本語境。
- 成人產品首個系列與噴霧維持數月均保留公司歸因，沒有當作獨立實驗結果。葡文 conservação、印尼文 menjaga hasil karya 指作品保存，而不是聲稱套件原料通用保存年限。
- 拉丁文字檢查沒有殘留中／日／韓／泰腳本；這只證明文字形式，沒有做聲音或實際caption時間檢查。

## 留給獨立覆核的事項

葡文縮圖副標採 `Hasbro (2024): >500 mi de potes`，以常見縮寫 mi 表「百萬」，保留來源／年份／罐數；印尼文 `Klaim 2024: >500 jt wadah` 的 jt 為 juta（百萬）縮寫，wadah 為容器，避免暗示金屬罐。這是手機縮圖的文字方案，尚未以實際字體／版面驗收。葡文 plasticidade、印尼文 plastisitas 是專利段落對「可塑性」的術語；獨立校對可判斷口語易懂程度。沒有可用真實line視窗，因此不聲稱任何配音fit通過。
