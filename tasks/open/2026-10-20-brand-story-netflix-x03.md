---
id: 2026-10-20-brand-story-netflix-x03
title: 製作 Netflix 郵寄 DVD 轉串流品牌故事 X03
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-x03-remediation
claimed_at: 2026-10-20T18:08:15Z
created_at: 2026-10-20T10:42:12Z
completed_at:
branch: codex/brand-story-netflix-x03
depends_on: []
scope:
  - docs/videos/story-everyday-netflix-x03
  - tasks/open/2026-10-20-brand-story-netflix-x03.md
---

# Netflix X03：郵寄 DVD 還在成長時，為何開出電腦即看？

## Why

站主要求品牌故事逐支製作並在完成後開 PR。X03 是既有二十集之外的補充題，與 C01 Crocs、C02 特百惠、X01 Adobe Creative Cloud、X02 Domino’s 的核心反轉不同；本集只追 Netflix 從郵寄 DVD 與線上即看並行，到把串流列為核心策略、最後結束寄片的可查時間線。另一系列的 Blockbuster 拒買 Netflix 題講的是 2000 年收購談判，不是本集主線。

## Definition of done

- [x] 四份 SEC 原始申報支撐六章主線與逐句史實；完成本輪畫面提示詞／公開說明修訂後，須按**新** `video.json` 雜湊重做來源與兩位敘事讀者收據及 `lint`。
- [ ] 在單支 US$25 硬上限內，完成至少八分鐘正文、30–60 秒濃縮開場、MiniMax `image-01` 插圖、配樂、5 秒片頭、21 秒片尾、1080p 試片與可關閉的繁中字幕。
- [ ] 完成音訊、畫面、格式、成本與來源 QA，交付上架包；正式品牌素材與 YouTube 可點片尾連結仍依站主／Studio 流程驗證。

## Steps

- [x] 建立四份 SEC 原件筆記、題材去重、製作簡報和六章 Treatment（X03 pipeline 第一階段）。
- [x] 請獨立查核者複核原件引文、訂戶／寄送／觀看／營收單位與六章因果，留下綁定最終逐句稿內容的收據。
- [x] 寫繁中逐句稿、場景提示詞、至少八組伏筆、數字卡與 YouTube 文案，綁定定稿 SHA 做來源審查和盲讀。
- [ ] 在付費前跑整片 TTS、圖片和配樂乾跑，將語音、轉錄、查核、插圖、評審、重做、音樂和稅費合計守在 US$25 內。
- [ ] 生成媒體、檢查旁白、合成概念試片與字幕，完成整檔 QA、交接和 PR。

## How to verify

前製先核對 [`source-notes.md`](../../docs/videos/story-everyday-netflix-x03/source-notes.md) 的 SEC 連結、引文、年末訂戶數與不同計量範圍，並審閱 [`brief.md`](../../docs/videos/story-everyday-netflix-x03/brief.md) 及 [`treatment.md`](../../docs/videos/story-everyday-netflix-x03/treatment.md)。定稿後才建立 `video.json`、跑 `node tools/video/cli.mjs lint --slug story-everyday-netflix-x03` 和影片工具的付費乾跑；媒體完成後核對音訊、字幕、影格、解碼、台帳，並跑 `npm run test:docs-videos`、`npm run check:tasks`。

## Notes

2026-10-20：本分支從 `origin/main` 建立；**X03 pipeline 第一階段**完成來源筆記、brief 與六章 Treatment。第一階段當時尚無完整逐句劇本、獨立查核收據、付費呼叫、媒體或上架核准。四份 Netflix SEC 10-K 已唯讀開啟並回 HTTP 200；2007 年寄出 DVD 總片數比 2006 年增 20%，但每名平均付費訂戶每月租片數下降，不能把後者歸因串流。2007 年末約 750 萬訂戶不可寫成 2007 年一月推出即看時的數量；2010 年「多數訂戶各自透過串流看的內容多於 DVD」不是營收占比；2023 年美國寄片收入與全球串流收入不能當相同市場分母比較。頻道即時影片清單在此雲端仍不可讀，僅能按儲存庫既有題庫去重。

2026-10-20：**X03 pipeline 第二階段完成文字稿與免費乾跑。** `video.json` SHA-256 `b65241c55c35f6692cac89e3af4e5aa651b6664025c33890e497846346e722a4`，80 句、六章、10 組伏筆、65 張插圖場景、12 張後製資料卡和一張 `outro`；免費估時 9.1 分鐘，開場 51 秒。獨立 SEC 查核 PASS；盲讀 A 13/13、盲讀 B 12/12 必答通過，收據見 `docs/videos/story-everyday-netflix-x03/reviews/`。`lint` 0 錯誤 0 警告，`test:docs-videos` 236/236，`check:tasks` 通過。2022 SEC 年報只用來辨明筆記裡的美國 DVD 收入口徑；2023 美國 DVD／全球串流營收未進影片。**付費呼叫 US$0，尚無配音、插圖、音樂、字幕、片頭片尾檔或成片；下一關先給 65 張 MiniMax 插圖、80 句語音、轉錄、評審、配樂和重做等做 US$25 全額報價，再進媒體製作與 QA。**

2026-10-20 14:15 UTC：X02 達美樂本機試片的草稿 PR #1620 已開，本票由 `codex-gpt6-netflix-x03` claim 並開始 X03。唯讀預檢重新核對五份 SEC 原件的 SHA 與全部 80 句來源，無阻擋性史實錯誤；但 `nx0404`、`nx0503`、`nx0523` 等提示詞可能誤畫統計分母或授權費用，螢幕／卡片可能生出假片名，正在付費前修稿。公開說明另有未直接列原件的 2023 年 DVD 收入口徑句，將刪除。修稿會改 `video.json` SHA，舊來源與雙盲讀收據不能用於新稿核准。獨立手稿詞庫 bootstrap 工具已在本分支本機實作並通過工具測試；尚未對真實 X03 `--apply`、沒有任何媒體工作目錄或付費生成。待新稿審查收據建立，先唯讀乾跑並審核 US$25 預算，再啟動媒體。

2026-10-20 14:35 UTC：現行稿 SHA-256 `647b73fdb22a2452ad2817ca5554689db5801af0e97996913e7e73c1694b2fb9` 已取得來源與兩位獨立敘事 PASS，`lint` 0 錯誤／0 警告；詞庫審查收據與安全乾跑後 `--apply` 回 `bootstrapped:true`。首輪 TTS 實際合成 78 次、2,305 計費字元，量得 16,396 影格／9:06.53，濃縮開場 50.03 秒、之後口播 8:16.50；`tts --dry-run` 已回 0 句待生成。65 張 MiniMax 插畫加評審乾跑首輪約 US$0.88、每鏡最多三次約 US$2.63；552 秒單曲乾跑約 US$0.08。站點單片 US$200 限額不替代本集 US$25；語音、逐句轉錄、複查與稅費未拆帳，不能把媒體台帳 US$0.00 當總費用。逐句轉錄仍在進行，尚未生成插畫、配樂或成片。

2026-10-20 14:50 UTC：兩輪逐句語音複核後，針對 12 句疑詞與容易誤聽的關鍵事實改寫 `nx0306`、`nx0307`、`nx0408`、`nx0411`、`nx0414`、`nx0415`、`nx0419`、`nx0420`、`nx0501`、`nx0514`、`nx0606`、`nx0618`；詳見 `reviews/audio-review.md`，不把 ASR 轉錄當成人耳核准。新 `video.json` SHA-256 `ea72bdc99073e672a69e4c9c6df32ff1942654caaef86fa827e7ee34ee5aec99` 已取得新一輪獨立來源與兩位敘事 PASS，結構化 `reviews/audio-revision-review.json` 將前後稿與三份新證據綁定；原詞庫 bootstrap 收據仍如實綁前稿，供不可變交易追溯。新 TTS `timeline.json` SHA-256 `e69b87e5e617e51025a26652d47c4412b324dba754f1dfb7a5cd7b39951e1ef8`，16,541 影格／9:11.37 口播，其中濃縮開場 1,501 影格／50.03 秒、其後 501.33 秒。新配樂乾跑 557 秒、約 US$0.08；65 張插畫首輪／三次估算仍約 US$0.88／US$2.63。新稿音訊逐句複核與人耳驗聽、插畫、配樂及本機試片 QA 尚待完成，US$25 全額仍須核實。

2026-10-20 15:00 UTC：初次插畫批次在 7 次候選圖生成後中止，媒體台帳可見約 US$0.08，仍計入本集 US$25。逐鏡預檢針對擬人化道具、假字與標誌、無原件支持的相對規模暗示，只改 **25 幅 shot 提示詞**；現行 `video.json` SHA-256 `4ba2b46746b6bc83960cdf45aa557ba408f280a8e9c4086d27ff99cafd638d8b` 已取得 `reviews/source-review-visual-revision.md`、`reviews/visual-prompt-review.md` 的文字 PASS，`reviews/visual-prompt-revision.json` 綁定新舊 SHA 和兩份證據。旁白、資料卡、音訊 key 均未改，`timeline.json` SHA 仍為 `e69b87e5e617e51025a26652d47c4412b324dba754f1dfb7a5cd7b39951e1ef8`（16,541 影格／9:11.37；開場 50.03 秒、其後 501.33 秒）。依現稿重新出圖每鏡最多兩次估新增不超過約 US$1.75，第三次僅針對確有缺陷的鏡頭；557 秒配樂乾跑仍約 US$0.08。舊詞庫及音訊修訂收據保留原本雜湊，不冒充現稿核准；實際影格、音訊與成本仍待 QA，尚無成片核准。

2026-10-20 15:07 UTC：第二輪在另 **5 次候選圖**後中止；最新稿只在 `4ba2b467…` 上新增全域 `look.style`，使純物件鏡頭不得擬人化、人物僅在鏡頭明示時出現。現行 `video.json` SHA-256 `08c931bb000f373fbf5778d02b0703ef1a8b5144c665bfa30afda7c44ed3e5ac`，獨立 `reviews/source-review-style-amendment.md`、`reviews/visual-prompt-style-amendment.md` 及第四層 `reviews/visual-style-amendment.json` 均綁此 SHA；原詞庫、音訊、25 鏡提示詞三層收據保留歷史雜湊。畫風單張試作未見擬人臉，但光碟護套與回郵袋合併，未達完整構圖驗收；全批仍須逐張 QA。先前兩次中止及新畫風單張試作合計工具可見約 **US$0.18**；557 秒配樂已生成，可見 US$0.08，故完整插畫批次開始時工具台帳為 **US$0.26**，不等於全片供應商帳單。完整插畫批次正在生成；語音時間軸仍為 `e69b87e5…` 的 16,541 影格，音訊、插畫、配樂混音及成片 QA 尚待完成，不宣稱正式資產核准。

2026-10-20 15:47 UTC：四個隔離插畫批次已合併回本集工作區，65/65 鏡有可雜湊追溯的選圖，原始候選圖與模型評審保留；合併收據為 `review/keyframe-merge-f4622a12aa55.json`。媒體台帳可見 **US$1.7135**（122 張候選圖、121 次評審、一首配樂、零保留工單），仍缺語音、轉錄、其他複查與稅費完整帳單，不能宣稱整集 US$25 已核實。80 句音訊機械證據與 12 張資料卡已核對，仍待必要的人耳驗聽。人眼視覺審查發現假字、道具和 2006 年提前出現播放鍵等問題；正以 48 項雜湊綁定的安全概念圖候選清單做來源／視覺雙審，原選圖與評審不得覆寫，替換鏡頭仍為 `needs_review`。目標交付 5 秒概念片頭、21 秒概念片尾、9:37.37 預期長度的 1080p 未核准試片、繁中 SRT／VTT、縮圖及完整 QA；兩個可點影片元素與訂閱鈕仍要在正式 YouTube Studio 上傳後設置和實測。

2026-10-20 16:11 UTC：本機概念試片已交付 `/workspace/brand-story-preview/netflix-x03/`。最後 49 鏡安全概念圖替換有來源／視覺檢查與 SHA 綁定收據，原圖及評審未覆寫；49 鏡仍標 `needs_review`。整檔技術 QA **PASS**：H.264 1920×1080／30 fps，17,321 影格／577.367 秒（9:37.37），完整音畫解碼與連續 PTS、92 句繁中 SRT／VTT 位元組一致、−14 LUFS／−1 dBFS 真峰值；MP4 SHA-256 `28237f52f5deacd7bbe1ea2c90cf2616cc48d1e57cb296c65c407e587b8cd728`。概念旁檔保持 `approved:false`、`official_branding:false`；[QA 原始結果](../../docs/videos/story-everyday-netflix-x03/reviews/local-preview-qa-result.json)與[審閱紀錄](../../docs/videos/story-everyday-netflix-x03/reviews/local-preview-qa.md)已入包。票仍開著：尚缺站主 49 鏡與人工聽審、正式 5 秒片頭與 21 秒片尾、語音／轉錄／稅費全額結算，以及 YouTube Studio 兩個影片元素與訂閱元素實點驗證；本地動畫上的框線不能點擊。

2026-10-20 視覺規格補查：見[逐鏡複核](../../docs/videos/story-everyday-netflix-x03/reviews/visual-triage-20261020.md)。49 鏡替代圖中 **23 鏡由本機 SVG 製成 PNG**，使實際 MiniMax 插圖最多 **42／77＝54.5%**；現稿另有自訂 `look.style`，會覆蓋固定 `cute-mystery` 預設。故本機試片僅供概念審看，按既定規格需移除畫風覆寫並在新媒體工作區重製 **65 鏡 MiniMax 圖**。嚴格故事正文實測 **8:00.70**，僅多門檻 0.70 秒；重配音不能加快後直接沿用長度判定。另缺兩支 25–55 秒 `from-episode` Shorts。65 鏡三次乾跑估最多 **US$2.63**，現有可見台帳 US$1.7135，但語音／轉錄／稅費未拆帳，尚不能確認全片 US$25 內；此輪未啟動任何付費重製。正式視覺、成本、Shorts 與上架關卡均仍未完成。

2026-10-20 18:08 UTC：協調者指派新的 X03 修復代理接手本票與現有 #1621 草稿 PR；原持有代理已結束、工作樹乾淨，故使用 `claim --force` 接手，沒有碰其他 session 工作區。已把固定畫風候選及兩支來源對照 Shorts 放在隔離的 [`remake/`](../../docs/videos/story-everyday-netflix-x03/remake/readiness.md)；候選主片 SHA `4ba2b467…` **逐位元組等於**先前由獨立來源／視覺複查 PASS 的 25 鏡修訂版，只從現行概念稿移除 `/look/style`。65/77＝84.4% 只是在 65 鏡都重畫為真正 MiniMax 時的目標；Shorts 157／166 字僅粗估 37.7／39.8 秒，媒體與獨立盲讀仍待做。舊 MP4、當前 `video.json` 和所有原始收據保留；因完整供應商成本未知，沒有付費重畫、不能宣稱同規格成片。下一步先核清全額預算，再以新工作區出圖、實測正文和 Shorts、驗聽及正式品牌／可點連結。
