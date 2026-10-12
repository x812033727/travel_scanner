# H05 製作紀錄

2026-10-12。站主要求在H04交付後「繼續」，接續既有歷史懸案題庫H05，沿用僅繁中。本次製作範圍為成片與上傳包。

## 當前狀態

- 題庫H05原有checked／ADOPT_WITH_CHANGES；本次重新讀取FBI、FAA、2020期刊全文及三張物證圖的來源／權利。三份當日研究已落地，圖片原檔已下載及實看，尚未完成成片呈現。
- 三案企劃及獨立規劃覆核完成，0未解必修。原生Jev選A「從河岸贖金，倒追失蹤的人」：符合立場0.92、有示範0.95、建議0.01，正式站自動核准。不是承接H04的舊核准。
- outline review `47f37652-00b8-4fec-a322-8f9a729af7e8`，建立及核准時間 `2026-10-12T09:47:37.209200Z`；brief SHA `b384685061f457187f4ba3c189ebc7c99dfa275607853f397c2e8ec5f5df2803`。`review-push-2026-10-12T09-47-33-209Z`、`review-pull-2026-10-12T09-47-59-872Z`均exit0，`reviews-2026-10-12T09-48-01.756Z.json` GET200讀回approved／choice=A。
- 完整A案稿已取代初始企劃登錄稿；修正版video SHA `007bd144583905a61774bf0c7e92ac389431018bc955c2a0335cea759f984768`、claims SHA `4c1ab06a23eb749d757d56a214f2e2ac02597c84df0bab44cf1c96e900acce76`。105景、129句、2403口說單位。覆核已修正案發五週年、D.B.口說、研究推論圖解和兩次揭示的對拍，刪除五景同義補句；正式獨立覆核報告已綁定新版。
- 原生lint於10:07:48 UTC通過（0 errors；3個空景構圖詞頻率提醒），估11分31秒、127狀態最多7.5秒、插圖估60.43%；這些仍是估算。`tts --dry-run`：127請求／2701計費字元，Sulafat ready。`keyframes --dry-run`：74鏡、MiniMax image-01 ready、1K、0超出prompt預算，約US$1單輪／US$3最多三輪。以上預檢無付費；插圖、render、assemble或上傳包仍未製作。
- docs-videos檢查199／199通過，0 skipped（`_audit/docs-videos.log`）。這項檢查不等於音訊、圖片或播放器審看。
- `verify-1.md`（SHA `25efe7d0bf042483f2b498679f6c6b463f9a0f84c64053bdc39ec76834a93441`）及 `listener-review.md`（SHA `63cb8c1e0cbed238d707cebb03222dabb9b7359a6c2034b135892882a925931b`）均綁定上述修正版，0未解必修。24主張全部覆核；只有五週年一組事實變更，不觸發第二事實輪。TTS於10:11 UTC開始，尚在合成，未宣稱音訊核准。

## 規格與界線

- 製作目標正文10–11分鐘，正文及成片各至少8分鐘，實際長度依合成時間軸及ffprobe；不灌停頓補時。
- 本機插圖投影片，系列既有畫風、MiniMax image-01、Gemini Sulafat；字幕只做可開關繁中CC。人物只用無臉背影與剪影，生成圖不畫金額／鈔票序號／航空品牌或炸彈內部。
- 本次settings GET200：slides_image_model=image-01，slides_max_usd_per_video=80，auto_pick_outline=true，slides_auto_approve_storyboard=true，無指定音樂／音效素材。每次付費階段先原生dry-run，以當前提示、可沿用素材與供應商實際回應為準。
- 在世嫌疑人不入稿；生死與DNA歸屬不下定論。2016不再主動調查不叫破案／完全結案，公開卷宗不等於重新啟動案件。
- 只出繁中是已有站主指示；`languages.json`先保存空額外語言及未落地的backend決定時間，不偽填時間。成片核准後再以已有指示保存正式站選擇，不重問語言。
- H04媒體與PR #1460保留；不修改其他聊天的H02／H03語言工作。YouTube上傳、公開、PR合併及部署未授權。

## 來源、實算與素材

- [歷史刷新](research-history.md)：18項主張，FBI各頁同一機構不算多份獨立證據。
- [科學研究](research-money-science.md)：只分析一張原鈔，五月／六月屬浸水季節推論，不定年份、抵岸日、身分或全部贖金路線。
- [素材權利](research-assets.md)：機票、贖金陳列與領帶3張原件。2400×1369、1400×921、768×616；權利及SHA已記錄。沒有把後來拍攝的原件照片標成1971或1980當時攝影。
- 原件不編修，依bytes SHA複製至外部 `stock/`；`_audit/plan-preflight.json`保存完整下載／複製綁定。原件與情境插圖分開標示，領帶只在框內呈現，不以像素猜構造。
- 實算 `_audit/recovered-ransom-calculation.json`：FBI公布5,800／200,000美元＝2.9%；整數比例29／1000，沒有通膨換算。此比例不推出其餘錢的去向、人身分、生死或搬運者。

## 持久證據

媒體／工具工作區在repo外：`C:/Users/x8120/mokaair-work/videos/curio-h05`。`_audit/preflight-{reviews,settings}.json`保存GET404無既有H05製作及GET200當前頻道立場。所有圖片、WAV、影片、收據與候選留在外部；repo只放來源、規劃及查核文字。
