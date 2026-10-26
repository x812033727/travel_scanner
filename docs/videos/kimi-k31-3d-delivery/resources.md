# 原創3D交付檢查教具

[下載完整教具ZIP](downloads/kimi-3d-demo.zip)（1,218,511bytes；約1.16MiB）。

這是本片自行製作的墊圈、刻意填孔對照、檢查程式與離線檢視頁。它們不是Kimi生成或實際匯出的檔案，也沒有拿去列印；填孔對照不能當成模型失誤。官方消息與這份教材的來源不同。

下載後解壓縮，在解壓縮目錄開啟 `demo/index.html` 即可離線檢視、旋轉及切換剖面；不需帳號、套件、CDN或網路。中性開場畫面是 `demo/intro.html`。原創檔案依包內CC0授權提供，官方文字、商標和權重不在此授權內。

用Python 3標準函式庫重跑：

```sh
cd demo
python3 check.py --stl ring.stl --spec spec.json
python3 check.py --stl filled.stl --spec spec.json
```

程式exit0表示完成計算；請讀JSON的 `accepted_for_this_limited_spec` 與各項 `checks`。完整步驟與適用座標見 [教材說明](demo/README.md)。

本例檢查封閉邊、方向、外部尺寸、體積和33條固定孔軸射線。STL本身沒有毫米單位，本包由外部規格指定mm。名義孔徑16mm的64段多邊形，實際最小淨空約15.980727mm；若新需求是最小淨空至少16mm，有孔教具也不符合，原程式沒有實作這條新增門檻。檢查結果不等於任意孔形、公差、自交、壁厚、材料、承重、切片、列印或製造認證。

ZIP包含30份已凍結的原創檔案，另加 `SHA256SUMS.txt`，共31項。ZIP中的2026-10-26 00:00是固定封裝中繼資料，不是觀測或錄製時間。

SHA-256：

```text
aa049f3c71407d5c9728f493dad7c79c8fce2116f85be9d71746077e3ce31b21
```

[逐檔封裝驗證](receipts/production/download-kit-verification.json)保存原始檔雜湊與位元組數。這份教具的下載不代表成片、字幕、語音已交付後台。

## 字幕文字檔

繁中加八語的[實際SRT與VTT](captions/narration-timed/README.md)另附於文件。它們跟隨本片繁中旁白與正式片頭尾時間；保留47項閱讀速度注意事項，沒有聲稱外語配音已完成或通過音檢。

本提案的教具ZIP連結是repo文件中的資源；目前後台九語說明尚未附上它的公開URL。正式上架包前仍須補入真正可用的公開連結，按正常流程重審metadata，不能因本地ZIP存在就聲稱說明已完成交付。
