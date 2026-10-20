# X04 Beats｜零付費前製估算與乾跑

`video.json` SHA-256：`53483afc8fbc219ee6b10a356f29f8a5202319888a2f7e47a3e048de8a544ae5`。2026-10-20 在獨立 X04 worktree 本機執行；本文件只報已跑過的零付費步驟，沒有生成或購買媒體。本集累計實花 **US$0.00**，正式全片硬上限 **US$25**，其中須包含圖片重試與評審、語音、配樂、轉錄、複查及稅費。兩句時序修訂已經[新來源複核](reviews/verify-bootstrap-final.md)與兩份獨立[敘事 A](reviews/blind-a-bootstrap-final.md)／[敘事 B](reviews/blind-b-bootstrap-final.md)綁定；前版審查保留原 SHA，不冒充現稿核准。

| 項目 | 本機結果 | 實花 |
| --- | --- | ---: |
| `lint --slug story-everyday-beats-x04` | 0 errors／0 warnings；67 句、54 張插圖、13 張資料卡、14 個回收鉤子；估正文 8.2 分鐘、濃縮開場 00:54；lint 計費字元粗估 5,733 | US$0.00 |
| `keyframes --dry-run --takes 3` | MiniMax `image-01` ready，1K；54 張插圖一輪工具估約 US$0.73，三輪最多約 US$2.19；只是圖片請求估算，尚未加其他服務及稅費 | US$0.00 |
| 獨立審查後手工詞庫釘選 | [結構化收據](reviews/lexicon-bootstrap.json)綁現稿、`series.json` 與三份獨立證據；唯讀 admission 7／7 PASS，對**全新空工作區**執行手工 bootstrap，釘選詞庫 SHA-256 `26084f8968d1bf068ba16687ab32bbec04ab5207c4f45f50facd4dd6e22d7f9e`，交易 `229ed338-0cbd-4bd6-a3b5-58ab33223229`。沒有虛構工人章稿或 `auto.json` | US$0.00 |
| `tts --dry-run` | 已解開詞庫門檻：**67 次待合成、1,964 計費字元**；這是工具的實際請求規劃量，不是美元報價。共用權杖的唯讀站台狀態查詢因環境網路白名單不含 `mokaair.com` 而失敗，尚未送出語音請求 | US$0.00 |
| `music --dry-run` | 缺少與現稿綁定的 `timeline.json`；須在 TTS 後以實際長度乾跑。先以單曲約 US$0.08 作暫算，不能當成實際報價 | US$0.00 |

圖片至多 54×3＝162 次候選加同數量畫面評審，工具粗估 **US$2.19**；再暫列配樂約 **US$0.08**，目前可見媒體最高情境約 **US$2.27**。此數**不含**未報價語音、轉錄、模型複查、重做、稅費與供應商差額，不能證明 US$25 整集硬上限已有完整餘額。下一個付費階段前須取得或保守計入這些成本並設逐階段停止點；現階段繼續零付費。估時只計 `video.json` 口播，**未**把概念 5 秒片頭與 21 秒片尾灌入 8 分鐘門檻。8.2 分鐘是文字模型估值，距最低要求不遠；正式 TTS 後須以量測的旁白時間軸確認至少 8 分鐘。若不足，先補有 SEC 原件支持的新內容並重新做來源及敘事審查，不能靠延長停頓、空鏡或動畫補時。

本機手工詞庫工作區已建立，但正式工人章稿與原頻道動畫仍不可用；此時沒有可驗收的旁白、插畫、音樂、SRT、MP4 或 YouTube 可點連結。手工 bootstrap 工具仍在 Netflix X03 分支，X04 後續需先取得該工具的已審實作；動畫及連結的具體交接見 [publishing-handoff.md](publishing-handoff.md)。
