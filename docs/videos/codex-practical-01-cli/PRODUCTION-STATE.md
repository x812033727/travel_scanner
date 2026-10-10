# CLI 01 試製狀態

2026-10-11（Asia/Taipei）。狀態：`assembly_in_progress`。

主稿60張卡、162短行，lint估算14.3分鐘／3174 spoken units，0 errors／0 warnings；正文最少 8 分鐘及目標12–18分鐘仍須合成後實量。`authoring.mjs` 為卡片原稿，執行只寫同目錄 video.json/script.md，無模型／媒體／後台調用。

已綁定：真實只讀 exec、原始提示、24事件、完整最後回覆、工具版本與hash；五檔無變更證據；作者另跑的reference3/0及Edge網站13項檢查。這些都不表示本輪模型修補或原生App操作。

已完成：

1. build-05／build-06 的18教材ZIP重建一致；本片五檔與教材完全一致。獨立代理完成主案例／變式重做，保留預期基準失敗。
2. [verify-1.md](verify-1.md) 的20項主張通過，綁定目前稿件hash。這是影片稿件查核，仍不等於人類新手學習驗收。
3. file://失敗與HTTP網站修復有作者Edge證據；另外保留真正執行 `py -u -m http.server 4173 --bind 127.0.0.1`、HTTP200、回應hash與關閉自有程序的收據。
4. 本機首課ZIP與完整manifest已交付；公開下載入口尚未發布。影片未冒稱有公開教材連結。
5. outline已核准並讀回；TTS額度dry-run後合成繁中Sulafat旁白。原29句被標，首次局部重錄後13句；本機Whisper確認8句，再重錄5句後只剩1句。未撰稿的聽眾審稿將「跟做」改成同義的「練習」，只重錄21字。現在正文13分27秒，162句全部檢查：121逐字符合、28同音／語助詞、3句Jev通過、10句由第二轉寫確認，0 flags；audio已自動核准並讀回實際timeline hash。這是機械轉寫關卡，不冒稱站主已聽過。
6. 60張卡／136狀態／1445影格引用已渲染；[verify-media.md](verify-media.md) 的獨立靜態查核通過。终端明標「真實測試輸出摘錄／重新排版」，沒有冒充TUI錄影。

正在合成；尚缺繁中CC、成片實長與11項QA、上傳包及站主播放／跟做。沒有上傳或公開發布。App另列 `pending_capture`，native computer API在当前文字工作階段不可用；CLI與網站證據不能替代。

媒體與原始紀錄：`C:/Users/x8120/mokaair-work/codex-practical-series/media/codex-practical-01-cli`、同系列 `runs`。Windows confirmed journal rename EPERM僅從hash一致的完整已知provider回覆恢復本地紀錄，保留原sent、tmp及收據，未重送原請求。另一套本機辨識遇到UTF-8輸出問題，已用 `PYTHONUTF8=1` 重跑，沒有修改或降低檢查門檻。

## 可複製的作者本機檢查

```powershell
node docs/videos/codex-practical-01-cli/authoring.mjs
node tools/video/cli.mjs lint --slug codex-practical-01-cli
```

請勿以單一lint成功替代獨立学习者、事實審稿或完整媒體關卡。
