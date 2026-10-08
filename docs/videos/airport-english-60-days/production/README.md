# 機場英文 60 天：正式重製來源

這一版接續 [完整稽核](../AUDIT.md) 的修正。**60 集教學文字已重修及獨立覆核；
正式 60 支影片尚未完成。** 本目錄沒有成片、正式音軌或製作核准，歷史樣片也沒有
被改標為新成品。原始來源與稽核紀錄保持不變。

## 交付規格

- 60 集，每集最終 **600 秒**，包含實際採用的頻道片頭片尾。
- 英文常駐畫面、英文預設語音；繁中、簡中、日文、韓文各自可選 CC。
- 四語替代音軌只翻譯教學引導與測驗，角色對話複用經查核的英文原音。
- 1920×1080、30 fps；H.264 High、CRF18、2 B frames、2 秒 closed GOP、BT.709、faststart。
- AAC-LC、48 kHz、立體聲、384 kbps 目標；兩次 loudnorm，−14 LUFS／−1 dBTP 目標。
- 本工作不包含 YouTube 上傳、公開或排程。

## 已完成及其證據

| 工作 | 證據與驗收範圍 |
| --- | --- |
| 60 集五語來源、180 題明確答案證據 | `lessons/dayNN.json`；`reviews/verify-day01.md`、`verify-02-21.md`、`verify-22-41.md`、`verify-42-60.md` |
| 旅運事實及安全表述 | `reviews/claims-review.json`／`.md`；23 組主張、24 份當日取得的官方來源；虛構航班與櫃檯不當作即時資訊 |
| 五語共用教學指示 | `reviews/verify-shared-instructions.md`；跟讀允許暫停，保留英文畫面，不宣稱關閉英文字幕 |
| 正式製作來源 | 每集 `video.json`、`brief.md`、`claims.md`、四語 `i18n/`、字幕分段及混合音軌規劃；`prepare-report.json` 記錄官方 lint |
| 畫面排版預檢 | `reviews/layout-preflight.json`；21 張最長／代表字卡經官方 renderer 檢查，英文最多 3 行、字體至少 60 px；不是全片實看 |
| 60 張正式版型縮圖預檢 | `reviews/thumbnail-preflight.json`；修短兩個溢出標題後全數通過，JPEG 留在外部媒體工作目錄 |
| 播放器修正 | `reviews/player-validation.json`；實際 Chromium 測試 CC 切集、失敗音軌回英文、靜音、倍速、拖曳及手機版面 |

獨立文字覆核綁定內容 SHA-256。生成版本另由逐集 `verify-1.md` 與
`review-binding.json` 連結到真實覆核及來源；它們不代替正式音訊、成片或發布核准。
單元測試中的語音、核准及媒體 fixture 只供測試，不能複製進正式工作目錄。

## 尚未完成

正式 Sulafat 合成、逐句轉寫／Jev 查核、音訊核准、實測時長調整、1080p30 成片、
實際 CC 對時、四語完整音軌、最終 11 項 QA、上架包 4 項 QA，以及完整 60 集預覽。
目前文字估算的正文長度約 539–623 秒，**不等於已達成 600 秒成片**；不能用任意
空白、慢速播放或額外循環補時。需要依實際語音與品牌素材調整有教學目的的節奏。

已確認的外部前置條件：

1. 此環境沒有影片工具權杖；需依倉庫 `youtube-video` skill 的第 9 條，以官方
   `login` 配對連結由站主在後台允許。不要把金鑰或權杖貼入對話或 Git。
2. 本機尚無正式品牌素材。倉庫最新已查到的頻道啟用紀錄是
   [v2 CC 片頭](../../branding-release/2026-10-01-channel-branding-cc-activation.md)，
   當時為 5 秒片頭及 3 秒片尾；必須取得目前實際素材與 pin、核對 SHA 及格數，
   不能用這份歷史紀錄冒充現場量測。

## 繼續製作

實際命令與安全邊界見 [產線工具說明](../../../../tools/video/airport_english/README.md)。
所有工作音訊、影片、核准及上架包存放在 repository 外，來源與媒體目錄分開。
先完成 Day01 的正式合成、聽音、排版、時長與關卡，再將通過的流程跑完其餘 59 集。

播放器採用本機 HTTP 啟動；不宣稱 ES module 可直接用 `file://` 開啟。
原先公開的 Day01 樣片連結不代表這次正式重製版本，舊 ZIP 也未被當作新交付。
