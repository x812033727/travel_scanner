# S38 PF038 原生額度用盡後引文卡作者說明

作者 `/root/s38_pf021_last_paper`。待 root 獨立覆核，未呼叫任何付費服務。

PF038 第三／最後原生圖因3D畫風評審失敗，已沒有第四次額度。採一句中文譯文卡：**「早上收進的家當，又往更遠處搬」**，出處標示坎寧街往倫巴底街及更遠處，1666-09-02。它是原文壓縮翻譯，不是逐字中文記錄。與 PF033「家當裝上車，也背在人身上」的搬運方式不同，此卡呈現同日再次搬遷。

## 固定來源

`/tmp/s38-r8j-pepys-4200.txt`，D2c L65888–65893；直接引文基礎：

- L65891: removing goods from one burned house to another. They now removing
- L65892: out of Canning-streets (which received goods in the morning) into
- L65893: Lumbard-streets, and further;

## 範圍與檢查

可逆完整場景 old/new 位於 `verify-135-r8ao-pf038-card-author-diff.json`。僅 PF038 由 shot 轉 big（原 shot 的 camera/visual 欄位隨模板移除），除 root 指定的 PF040 camera 葉節點外，其他場景完整物件與其他 camera 不變。112個 spoken line 物件與 HEAD 完全相同。官方 `script --slug curio-s38` 已重產，只有 PF038 標題類型與 narrative footer 變化，speech footer不變。claims僅新增本卡來源註記。

Lint 最終結果：**0 errors / 0 warnings**。依 root 指定，額外只改 PF040 camera `track left` → `pull back`；可逆 diff 已列此唯一附加葉節點，中斷 drift/track 同類連續。PF039 已付 cached 圖的 prompt／camera 完全不變。

27筆 KEEP、manifest、ledger、cached PF039、STOP均未修改，未執行 git 或購買媒體。PF039仍保留既有一次實際原生圖。

## 檔案綁定

- `video.json` SHA-256：`3a95717b90909fdbd3eeabadbdc09cb344e7ba8ca53c1884d3ceb4f76193294b`
- `script.md` SHA-256：`035c8792c44590b6c1e2fcc8cff72bd235ef1ac8002b9c5219bbff03622a71bd`
- `claims.md` SHA-256：`b1a86f5161280e48027cfb6ba1716a8a9eaf0136326a0b4120477507a3c6b02e`
