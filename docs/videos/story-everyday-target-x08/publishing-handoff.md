# X08 Target Canada｜成片與發布交接

目前有 v14 前製材料及 135 句 Sulafat 旁白；14 句已選擇性重錄，工具重查 135／135 句後仍有 **9 個 Jev 旗標，音訊維持 HOLD**。原始 `match:false` 有 17 句，不能當作最終旗標數；[逐句音訊收據](reviews/audio-qa-v14-selective-redo.md)只有轉錄及 Jev 文字判斷，**沒有人耳聽音或音訊核准**。實測濃縮開場 46.367 秒、實質正文 607.833 秒、純旁白 671.600 秒，長度關卡已達標。尚無圖片、正式剪輯、音樂、繁中 CC、`final.mp4`、縮圖、上傳包、YouTube 影片 ID 或可點的影片連結。已配對的影片工具可由此雲端存取，正式工人仍須確認站主選定的 5 秒片頭、21 秒片尾原檔可讀。這份 repo 文件不能當成成片。

## 從鎖稿到影片

1. v13 同版[來源差異審查](reviews/source-audit-v13-independent.md)與兩位[敘事盲讀合議](reviews/combined-v13-independent.md)已 PASS；v14 只改五處畫面提示詞，[獨立視覺差異審查](reviews/visual-v14-independent.md)已 PASS，實際圖像仍待驗。v14 主片 `video.json` SHA-256 `7a9010968d9fa96abb8bf9df73d79287951ea5a79f01a3596c435a7d9e3216aa`；兩支 `shorts.json` SHA-256 `463fd550cb6b57e79cbf260de183bd77b9ce9b4498389f12eb6df3287bd74a5f`。改動已審文字、卡片或鏡頭後重審受影響內容；`lint` 零錯誤及警告才進媒體。Shorts 每句必須來自鎖版長片或重做同等查核。
2. 從 [全項預算表](production-quote.md) 取得當期單價、最壞合理次數及稅費；整支長片與兩支 Shorts 總計 **US$25** 內才可啟動付費工具。v14 開場 46.367 秒、實質正文 607.833 秒已達 **30–60 秒／至少 8 分鐘**長度關卡，但九個音訊旗標仍須有音訊存取權的人實聽，或有據重錄、重查後再申請音訊核准；不得把工具轉錄或 Jev 通過當成人耳驗收。不靠靜音、慢播、頻道 CTA、片頭或片尾湊秒。
3. 依 `format: drama`、MiniMax `image-01`、精確 `look: {"preset":"cute-mystery"}` 生成匿名插畫並做畫面審查。圖像提示詞不含 `Target`、`Zellers`、`Brian Cornell`、商標、可讀字、真人長相或仿真財報；日期、店數、比率、美元和「公司當時判斷」用原生卡明寫口徑。尤其不能畫成 2015-01-15 當日全部鎖門、所有貨架空無一物，或把非現金減損畫成現金搬出銀行。
4. 以 [BRANDING.md](../BRANDING.md) 正式 pin 的 **5 秒片頭**、**21 秒 v4 片尾**合成：長片次序是第一章濃縮開場 → 5 秒片頭 → 第 2–6 章正文與三句結尾口播 → 21 秒固定片尾。片尾口播要回答開頭、問一個與故事相連的留言題、給訂閱的理由；不念下支影片名。正文配一首輕快、好奇、微懸疑、無人聲音樂。合成後輸出**可關閉繁中 CC**，不燒字幕，核對音畫、標題、縮圖大字 `Target`、數字卡口徑、格數、響度與費用總帳，再做成片 QA 與上傳包。
5. 成片核准後，以 [兩支 Shorts 候選](shorts-script.md) 對照最終主片行 ID 和影格，重用已有素材製作 9:16 `from-episode`；逐支量 25–55 秒並查字幕安全區、口播事實與額外成本。若主片改稿，重映射並重查，不沿用已失效的時間碼或審查雜湊。

## 真正可點的片尾與相關影片

- 21 秒片尾的最後 **17 秒** 是結束畫面底；至少覆蓋最後 16 秒的可點元素須由 **YouTube Studio** 設定。依 [BRANDING.md](../BRANDING.md) 的現行規格，在 Studio「片尾」→「從影片匯入」選既有範本 `oxEtlA8GWas`，將「最符合觀眾喜好」影片｜訂閱｜「最新上傳」影片三個元素的開始時間拉到**全片結尾前 17 秒（片尾第 4 秒）**，並在預覽和上架後實點確認兩個影片連結及訂閱。動畫只畫位置，**不能自行產生可點連結**；範本 ID 也不是本集新片 ID。
- 長片通過成片／上架核准並真的上傳後，記錄 YouTube 回傳的本集影片 ID 和 URL。兩支 Shorts 上架後，各自在 Studio 的「相關影片」設成本集**已公開的真實長片**，並實點驗證。上傳前不填假的網址或把企劃 URL 稱作播放連結。
- 長片說明欄應列出 [FY2013 10-K](https://www.sec.gov/Archives/edgar/data/27419/000002741914000014/tgt-20140201x10k.htm)、[2014 Q2](https://www.sec.gov/Archives/edgar/data/27419/000002741914000025/a2014q2ex-99.htm)、[2014 Q3](https://www.sec.gov/Archives/edgar/data/27419/000002741914000033/a2014q3ex-99.htm)、[2015-01-15 原公告](https://www.sec.gov/Archives/edgar/data/27419/000002741915000005/exhibit99atargetcorporatio.htm)、[FY2014 10-K](https://www.sec.gov/Archives/edgar/data/27419/000002741915000012/tgt-20150131x10k.htm)和[2015 Q1 10-Q](https://www.sec.gov/Archives/edgar/data/27419/000002741915000018/tgt-20150502x10xq.htm)。SEC URL 是可用的**資料來源連結**，不是影片播放連結。

交接時保存最終長片與 Shorts JSON 的 SHA、來源／敘事／視覺審查與[音訊 QA 收據](reviews/audio-qa-v14-selective-redo.md)、九個旗標的實聽或重錄複查結果、乾跑估價和實際費用、TTS／`ffprobe` 的開場與正文長度、正式品牌 pin、成片 QA、`final.mp4`／上傳包 SHA、長片和 Shorts 真實 YouTube URL、Studio 片尾與 Shorts 相關影片實點結果。任何項目未完成，就維持「待製作／待上架」，不宣稱影片已完成或可觀看。
