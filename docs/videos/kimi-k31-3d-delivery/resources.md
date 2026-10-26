# 原創3D交付檢查教具

[下載完整教具ZIP](downloads/kimi-3d-demo.zip)（1,218,511bytes；約1.16MiB）。

固定版本公開下載：[原創教具ZIP（commit 1738c946）](https://raw.githubusercontent.com/x812033727/travel_scanner/1738c9460205627a73b05917790af6ac89812e12/docs/videos/kimi-k31-3d-delivery/downloads/kimi-3d-demo.zip)。已於2026-10-27 02:16:15 Asia/Taipei實際完整下載，HTTP 200、1,218,511bytes，SHA-256與本地原檔一致。公開下載檔的31項內容另經CRC與30筆 `SHA256SUMS.txt` 雜湊核對；見[完整HTTP讀回](receipts/production/resource-supplement/public-kit-HTTP-readback.json)及[公開ZIP逐檔驗證](receipts/production/resource-supplement/public-kit-archive-verification.json)。

這是本片自行製作的墊圈、刻意填孔對照、檢查程式與離線檢視頁。它們不是Kimi生成或實際匯出的檔案，也沒有拿去列印；填孔對照不能當成模型失誤。官方消息與這份教材的來源不同。

下載後解壓縮，在解壓縮目錄開啟 `demo/index.html` 即可離線檢視、旋轉及切換剖面；不需帳號、套件、CDN或網路。中性開場畫面是 `demo/intro.html`。原創檔案依包內CC0授權提供，官方文字、商標和權重不在此授權內。

用Python 3標準函式庫重跑：

```sh
cd demo
python3 check.py --stl ring.stl --spec spec.json
python3 check.py --stl filled.stl --spec spec.json
```

程式exit0表示完成計算；請讀JSON的 `accepted_for_this_limited_spec` 與各項 `checks`。完整步驟與適用座標見 [教材說明](demo/README.md)。

實際公開下載的ZIP另已解壓至全新隔離目錄，依上述兩行指令重跑；[原創教具公開下載重現紀錄](receipts/production/resource-supplement/public-kit-reproduction.json)保留實際結果。

本例檢查封閉邊、方向、外部尺寸、體積和33條固定孔軸射線。STL本身沒有毫米單位，本包由外部規格指定mm。名義孔徑16mm的64段多邊形，實際最小淨空約15.980727mm；若新需求是最小淨空至少16mm，有孔教具也不符合，原程式沒有實作這條新增門檻。檢查結果不等於任意孔形、公差、自交、壁厚、材料、承重、切片、列印或製造認證。

ZIP包含30份已凍結的原創檔案，另加 `SHA256SUMS.txt`，共31項。ZIP中的2026-10-26 00:00是固定封裝中繼資料，不是觀測或錄製時間。

SHA-256：

```text
aa049f3c71407d5c9728f493dad7c79c8fce2116f85be9d71746077e3ce31b21
```

[逐檔封裝驗證](receipts/production/download-kit-verification.json)保存原始檔雜湊與位元組數。這份教具的下載不代表成片、字幕、語音已交付後台。

## 字幕文字檔

繁中加八語的[實際SRT與VTT](captions/narration-timed/README.md)另附於文件。它們跟隨本片繁中旁白與正式片頭尾時間；保留47項閱讀速度注意事項，沒有聲稱外語配音已完成或通過音檢。

上述公開下載連結已完整讀回，並加入[九語說明更新稿](description-drafts/README.md)。可下載[九語完整JSON](description-drafts/metadata9-draft.json)及[可直接閱讀的完整TXT](description-drafts/resource-metadata9-draft.txt)。它們是尚未採用的更新稿；目前後台九語metadata仍維持原值，正式上架包前須經正常流程採用與重審。教具或更新稿可下載不代表外語配音、語言批次、成片核准或上架包已完成。

台北2026-10-27 02:35，下載連結與九語完整說明更新稿已作為單一參考附件送到[本片後台](https://mokaair.com/zh-TW/admin/videos?video=kimi-k31-3d-delivery)；同一筆待審的14個附件均經正常工具完整下載與逐檔SHA核對。[實際交付收據](receipts/production/resource-supplement/actual-backend-resource-delivery.json)保留結果；九語metadata原值仍未替換，稿件仍是尚未採用的參考。
