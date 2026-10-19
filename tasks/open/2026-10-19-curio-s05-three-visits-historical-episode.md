---
id: 2026-10-19-curio-s05-three-visits-historical-episode
title: Curio S05 Three Visits historical episode
status: in-progress
priority: P2
area: docs
owner: codex-s05
claimed_at: 2026-10-19T17:59:22Z
created_at: 2026-10-19T17:59:20Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s05
---

# Curio S05 Three Visits historical episode

## Why

站主授權持續製作新的歷史系列影片。S05「三顧茅廬，還是諸葛亮自己上門？」是尚未製作的 S 軸候選，適合接在 S34 等已啟動題目之後；需要把〈出師表〉、陳壽正文、裴注引《魏略》與小說場面分清，才不會把真正存在的古籍異說說成「三顧是假的」。本票只認領 `docs/videos/curio-s05`，不碰共用題庫。

## Definition of done

- [x] 固定可追溯的古籍轉錄、查核主要敘述和小說增飾，寫成約 8.1 分鐘可審的故事與分鏡。
- [x] `video.json` 與 `script.md` 通過奇聞檔案局 lint；逐句主張可追到史料層級。
- [ ] 獨立盲讀修改後的最終稿通過 13 題；更新過的旁白再做逐句聽辨；插圖、配樂、成片與上架包完成。

## Steps

- [x] 檢查同題資料與分支、認領窄 scope，選 A 案史料追查線。
- [x] 核讀固定《三國志》卷 35 與《三國演義》37／38 回，建立 `brief.md`、`research.md`。
- [x] 完成 `video.json`、`script.md`、`claims.md`，修到 0 lint errors／warnings。
- [x] 收取第一位盲讀者 13 題回饋，修正重述、問題回收、章名與章節銜接。
- [ ] 請全新讀者盲讀劇本雜湊 `d36f3aba…`；通過後恢復已暫停的插圖與語音關卡。
- [ ] 完成媒體與交付，並在同一 PR 將票結案。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s05`（0 errors、0 warnings）；`node tools/video/cli.mjs script --slug curio-s05`；`node tools/video/cli.mjs narrative --slug curio-s05` 加新讀者的 `--answers`；`npm run test:docs-videos`（236 passed）；`npm run check:tasks`（既有其他 scope 的警告不影響本票）。後續另跑語音、插圖、QA、上架包關卡。

## Notes

- 2026-10-19：固定《三國志》轉錄 commit `10a0b1ab3019d8821262f7402366d14fb4aaa102`，小說轉錄 commit `761813427eb5685c395804493f9fbd7ad8dc7d`；詳細原文見 `docs/videos/curio-s05/research.md`。本次暫存 `/tmp/s05-sanguozhi`、`/tmp/s05-sanguoyanyi` 僅供核讀，不依賴暫存交接。
- 《三國志》正文與〈出師表〉都寫劉備三顧；裴注引《魏略》說諸葛亮北行見劉備，且稱《九州春秋》同說。裴本人依〈出師表〉反駁。《三國演義》的風雪、晝寢是更晚的小說場面；不可說「三顧只有小說才有」，也不可把裴注引文當裴認可。
- A 案成稿 113 句／94 張 still／2 張文字卡／片尾，估 9.1 分鐘；`narrative` 內容指紋 `bde3ee6c3e80beb1`，lint 0／0。第一位獨立盲讀者提出四類問題（章節預告、章末承接、荊州問題未回收、重述及末章名），已針對最新版全部修正。仍需另一位盲讀者重新給 13 題判定後，才提交劇本關卡與付費媒體。
- `npm run test:docs-videos` 236 passed；`npm run check:tasks` validated 2070 files，警告均屬其他舊票或重疊 scope。原稿、口語稿各已付費製作旁白並通過當時的 113/113 語音比對；第三輪盲讀指出末段證據問題，故再修兩句並刪一張重複插圖。現稿 `script.md` SHA-256 `449ca0f7a131285669001520f34f5623e2c16ba85c36796023584625cc4aed91`，112 句／93 張插圖、估 9.1 分鐘，lint 0／0；新稿尚待全新盲讀、再合成改過的兩句與語音複查。已畫並通過第一張插圖，整集畫圖在盲讀前暫停，恢復時會重用此圖；先前整集報價 94 張、最多 US$3.81，現稿張數更少。每次 `approve` 均記下使用者委派而非聲稱站主親讀或親聽。
- 2026-10-19 新嚴格盲讀對上段舊稿評為 **10/13**，失敗項為 `chapters_link`、`no_recap`、`no_detour`。現已刪除隆中細節與魚水旁支，讓《魏略》章末問題直接引出裴查〈出師表〉，又讓小說等待引出陳壽長談的記錄問題；移走過早與重複的天氣判斷。現稿 `script.md` SHA-256 `6db96fb4dfce61ef0eddd457f2870c4af410736198bb7561fcce4a94914262e9`，101 句、86 張 still、2 張文字卡、1 片尾，估 8.3 分鐘，lint 0 errors／0 warnings；逐句 claims 覆蓋 101/101。**此前所有敘事核准、TTS 與聽辨只屬舊稿，不能沿用於現稿。** 未啟動新媒體工作，待另一名未讀研究筆記的讀者重評。
- 2026-10-19 第二位全新盲讀者評舊版 `6db96fb4…` 為 **11/13**，僅 `chapters_link` 和 `no_recap` 不過。依回饋刪重複 `eg019` 場景與 `eg112` 句，讓小說章末 `eg091` 問長談有無逐字紀錄、下一章 `eg092` 立即回答，`eg093` 說明證據界線。現稿 SHA-256 `b4189b4854c1491ff7e7ab06c72527230a19b663881382a21c367dac9e752f84`，99 句／85 張 still／2 張文字卡／1 片尾，估 8.1 分鐘，lint 0／0；claims 覆蓋 99/99。待第三位未讀前兩份查核的讀者評現稿；舊稿 TTS 不可沿用。
- 2026-10-19 第三位全新盲讀者評 `b4189b48…` 為 **12/13**，唯一不足是 `visit-017` 緊接 `visit-016` 重複「三次才見」。已將 `eg017` 改為徐庶「臥龍」推薦往劉備求策的前進節拍，並使該鏡改畫諸葛亮準備談策，不再用三個行程籤重述次數。現稿 SHA-256 `d2b973ae3a7e3ad338657fa3175d59828b9bd3b1333429a7c29ad5a86d5c4874`；99 句／85 張 still，估 8.1 分鐘、lint 0／0，待第四位全新盲讀。
- 2026-10-19 第四名來源隔離讀者對 `d2b973ae…` 判為 **6/12 必答題**，較前一位讀者嚴格，具體指出開場問題太抽象、首章收尾未引徐庶、《九州春秋》問法與回答不完全對應，以及尾聲重述拜訪方向。現稿把 `eg005`–`eg007` 寫成樊城目的地、牛尾飾物開談、徐庶推薦後的劉備反應三個未解時刻；`eg007` 直接引新野，`eg058` 直接問裴是否抄《九州春秋》完整對話，移除 `visit-079`，`eg094` 只新增傳記未記語氣的界線。現稿 SHA-256 `d36f3abaec7f76cfffb229b8fc0e2682a6d2f2165d94c1ed93d3aa5978dad944`，98 句／84 張 still／2 張文字卡／片尾，估 8.1 分鐘，lint 0／0、claims 98/98；固定史料段 `卧龍也`、`亮乃北行見備`、`結毦`、`九州春秋所言亦如之`、`計將安出` 均已抽查。待另一名獨立讀者評此雜湊，未恢復媒體。
