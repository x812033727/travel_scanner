---
id: 2026-10-19-curio-s26-marie-antoinette-brioche-attribution
title: Curio S26 Marie Antoinette brioche attribution episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s26
claimed_at: 2026-10-19T19:10:41Z
created_at: 2026-10-19T19:10:38Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s26
---

# Curio S26 Marie Antoinette brioche attribution episode

## Why

站主要求在 S34 之後依推薦持續製作 S 軸歷史影片。S26 的常見問句「沒有麵包就吃蛋糕，瑪麗皇后真的說過嗎？」需要把盧梭《懺悔錄》的匿名「公主」、法文 *brioche*、瑪麗・安東尼的生平，以及十九世紀已帶懷疑語氣的歸屬文字分開核對；題庫的寫作年份不能逕當成已證事實。

## Definition of done

- [x] `docs/videos/curio-s26` 有估 8.7 分鐘劇本、固定來源筆記、逐句事實表、83 張靜圖分鏡。
- [ ] 獨立史料覆核與確切雜湊盲讀：第七輪舊稿 13/13 通過；逐句語音檢查後改了 13 句，**現行確切新版待重讀**，媒體品管與成片待完成。

## Steps

- [x] 檢查 S26 無其他活躍認領、遠端 PR 或 main 既有落地，建立窄 scope。
- [x] 固定盧梭法文摘錄與完整英譯、Campan 生年／赴法記錄、Karr 1841 與 1843 年文字；標示一手敘述和後來轉述的界線。
- [x] 完成 brief、research、claims、video.json、script.md；獨立史料讀者已完成初次與增量覆核。
- [x] 首次全新盲讀完成 11/13；針對長段落失去懸念、糕點店岔線修稿，見 `verify-3.md`。
- [x] 第二次全新盲讀 10/13；連同獨立增量史料覆核指出的過度推論與畫面暗示，一次作結構修訂，見 `verify-4.md`。
- [x] 第三次全新盲讀 9/13；再修重複、章首與流程式句子，見 `verify-5.md`。
- [x] 第四次全新盲讀 12/13，固定原件及新增句史料覆核通過；刪去兩處真重複並收窄哺乳詞義，見 `verify-6.md`。
- [x] 第五次全新盲讀 12/13，刪相鄰的國王承諾重述；婦人不能哺乳明確歸於自述，見 `verify-7.md`。
- [x] 第六次全新盲讀 12/13，刪卡爾布里歐修引語的重述；修兩處馬車旁人群畫面，見 `verify-8.md`。
- [x] 本次精確雜湊由第七位新讀者判 13/13，固定來源再核通過；見 `verify-9.md`。
- [ ] 完成 84 句語音、`check-audio` 重錄，實測正文至少 8 分鐘後再排插圖；舊稿合成正文 8:24.03，兩輪語音檢查標記 24→13，現行新版待重讀及受影響句重錄；共享 MiniMax 圖像額度由根代理協調。
- [ ] 跑文件測試、記錄最後交接。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s26`；`node tools/video/cli.mjs narrative --slug curio-s26`；`npm run test:docs-videos`；`npm run check:tasks`。

## Notes

與其他集共用 `codex/curio-s34-endurance-20261019`，本票只改 `docs/videos/curio-s26`。早期原件可讀 GitHub 固定提交：TEI 對《懺悔錄》法文摘錄、GITenberg 完整英譯、Campan 回憶錄、Karr《Les Guêpes》。Karr 1841 年稱名言「真假未定」，1843 年又提其找到一部 1760 年書將話歸給托斯卡納公爵夫人；後者只可稱「Karr 自述」，尚未獨立找到該書。盧梭原文未指名瑪麗；不能把題庫的約 1765 年寫作日期或匿名公主身分寫成已證。

第七輪受審稿 narrative hash `15270e565c5bca98`、`script.md` SHA-256 `acadd5d68adc18b4063cc54957436dfa2880b2ce1b4684675feccf3d9a50fab3`，84 句、83 張靜圖、估 8.6 分鐘；lint 0 錯 0 警告。早稿獨立史料覆核見 `verify-1.md`、`verify-2.md`；前六次全新盲讀在逐步修稿中得 11/13、10/13、9/13、12/13、12/13、12/13，原始阻擋及源流分見 `verify-3.md` 至 `verify-8.md`。第七次確切雜湊 13/13，固定來源相符，見 `verify-9.md`。outline／script 關卡均依站主的持續製作委託記錄代理核准，明示站主未逐篇審讀；**舊稿語音實測已達 8 分鐘但品質未過，插圖支出仍為 US$0.00**。

上段是第七次盲讀時的舊稿紀錄。現行措辭修復稿 SHA-256 `1847738eb6cb8410b3034e4147bde198dca73355062b3679755946c40926e3ea`、narrative hash `8e432e5b4d5ef1e2`，84 句、83 靜圖，lint 0/0；舊稿語音實測正文 504.03 秒。第二輪語音檢查仍有 13 句標記，詳見 `verify-10.md`。現行稿的盲讀、來源差分、重錄與語音審核都未通過，故插圖支出仍 US$0.00。
