# B18 六章完整逐字稿：離線候選

**HOLD。** [`B18.md`](B18.md)是可讀的新版完整口播候選，並非正式工人已採用的 `story/chapters/`、`video.json` 或已審核的稿。它依[來源歸屬旁白候選](../B18-attributed-narration-candidate-20261017/README.md)的 row、六章與來源界線另寫；父版 canonical story SHA-256 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`，父版 row SHA-256 `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681`。父版自身仍未採用，65 筆逐景主張仍全是 `UNCHECKED`。

舊 [`scripts/B18.md`](../../scripts/B18.md) SHA-256 `5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724` 和[舊全文審稿](../../scripts/reviews/B18.md) SHA-256 `1583b36311fde688a49f70aa546bb1c30b53ab294afeb1119bb576c73a479cdb`保持原樣，當作歷史資料。舊稿的 1978 年期滿說法與[法院判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)對特定第 579776 號 1972 年期滿的認定不合；本版口播只說判決可支持的窄範圍，沒有以一項權利推斷所有權利、商標或市場變化的唯一原因。道頓堀展店年份有來源分歧，也不口播年份。

| 章節 | 主要改寫 | 來源界線 |
| --- | --- | --- |
| 開場與起點 | 約 25 秒濃縮片頭前的三問；早期 20 日圓立食店與送盤瓶頸 | [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| 點子 | 轉角堵帶、盤子掉落；撲克牌／名片兩版本分別歸屬；1957 試作 | 同上；板片不畫成可考證事故照片 |
| 生意 | 1958 首店 50 日圓、道頓堀只說後來展店、1962 實用新案、萬博 300 日圓桶裝套組 | [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)、[法院](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)；價格不混時代 |
| 轉折 | 萬博曝光與加盟展店分開；法院只認定特定權利；後場直線、1980 旁通裝置、1986 ㄇ字型店 | [法院](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)、[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)、[石野官方年表](https://www.ishino-group.com/history/)；不同店型不是同一台機器逐年改裝 |
| 現在 | 2021 年第 112 號機械遺產：1985 堺東店機器與另存早期板片 | [日本機械學會](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)；不說是 1958 首店原機 |

[`check.mjs`](check.mjs)只在此候選目錄寫 `verification.json`。它驗證父版與舊稿雜湊、六章與 25 段口播各自有來源註、三個開場懸念回收、相關年份與禁止口播說法、片頭片尾 cue 和末段三句；字數是計數，不是 TTS 實測。請執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-attributed-narration-candidate-20261017/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-fullscript-candidate-20261017/check.mjs --check
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-fullscript-candidate-20261017/check.mjs
```

`verification.json`的 `OFFLINE_SCRIPT_STRUCTURE_ONLY_HOLD`只代表上述機械條件。本稿將父版 `h5/i1/i5/i6/i7/n7` 的來源歸屬落在 H02／I01／I03／I04／N02 的完整口播；它是獨立寫成的說書稿，**不是與工程六句逐字相同的可套用 patch**。後續若採用，須在正式章稿對齊全文、按新 row 重做來源審核與整份逐字稿審查，不能引用父版或舊版的審稿 PASS。現行工人規格的 hook 預算是 30 秒內，`STORY.md` 的舊設計則寫 30–60 秒；本稿歷史語速估開場 25 秒、正文 8 分 47 秒，片頭片尾合計約 9 分 13 秒。這些都不是本稿的 TTS 或成片實測。

聽眾審稿還要判斷多次口播 `J-Net21` 是否打斷故事節奏，TTS／Jev 要實測它的日英混合念法。要調整任何一處歸屬用語，需同步修改工程章稿並重做文字查核，不得只把字卡來源當作配音觀眾也聽得到的歸屬。

離線獨立讀稿對 `B18.md` SHA-256 `41d3e8d321bdfbb94fefb8039df3713303e5380779ede982165d1d0f1596dfa6` 未找到 P1 史實錯誤；這是候選字稿的唯讀篩查，**不是正式全文審稿收據**。它仍指出三項採用前風險：不同文件對開場長度有 30 秒內與 30–60 秒兩種規格；五處口播 J-Net21 可能觸發出處過密的警告並影響聽感；歷史語速估的正文只比 8 分鐘下限長 47 秒，實際 TTS 若較快可能不足。後續不能以此篩查或字數估計代替工人關卡。

仍需正式工人逐章 verifier／listener／narrative、TTS 實測、插圖、繁中 CC、聲畫 QA、成片審核和站主決定是否上傳。此包沒有主機寫入、模型或媒體付費呼叫、匯入、合併、部署或發布。
