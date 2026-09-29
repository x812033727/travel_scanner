# Batch041 keyword／title 摘要修正版

這是兩篇五語內容的本機修正與審稿紀錄，尚未合併、部署或發布。
原發布票 `2026-09-28-release-reviewed-batch041-keyword-and-title` 繼續保留。

## 修正範圍

`seo-keyword-research`、`seo-title-writing` 的 zh-TW、zh-CN、en、ja、ko 原先
都以普通段落起頭。現在把原第二段的三句原文改為首個 summary，原第一段完整移到
摘要後。每語32個區塊，索引2以後的30個區塊、字詞、事實、metadata、來源查閱日期
及30個既有圖片檔均不變。這次沒有重新查核時效資訊，也未刷新 `checked_on`。

另修正 intake 的日文自我指涉判斷：日本語「本文」表示正文，不應被中文的
`本文/這篇` 規則算入。僅 ja 選用 `本記事/この記事/本稿`；上限、manifest override
與其餘 reader-first、summary、站內連結檢查維持有效。其他四語沿用原有 matcher。
這仍是文字啟發式規則，逐語審稿是另一道檢查。

## 來源與審稿

基底為 main `8be1cf9bcaddd697df99e505e33f562b010cfbd0`；兩包與 #940 原審稿內容
及初版 T2 凍結包相同。原候選 manifest
`d2e3fc9a7346b7e8345bcce13a0db7771be0bcffd79e4b0ed4adba49dcde5ab0`
保持不動。此修正版會改變兩個 pack、兩份來源及八份譯文雜湊，不能沿用舊候選
的發布綁定；原圖片及未變正文的既有審稿保留，新摘要結構另行獨立覆核。

## 修正版雜湊

私人 correction manifest SHA-256：
`881263f264eb1e1a7e2ce0c7a22d382f465b2099802fcfe64899b661a1131927`。
它固定 exact Git 原始內容、兩輪審稿、候選 bytes 與30圖雜湊；沒有保存正式版本更新收據。

| 內容包 | 修正前 raw SHA-256 | 修正後 raw SHA-256 |
| --- | --- | --- |
| `seo-keyword-research` | `5dff294b42067bb0cf5015d12d1d8264d436defee3fa7e4068b5736949264e6b` | `7cbab986c23384002c88a7ba0562fad0a8cfd11e436df2b93d0b4e91a64e79b9` |
| `seo-title-writing` | `f35ee83ce3df05e8dc82743ba2832df8e73dedab56ad3a74c3b0a3914efdd447` | `84545118cf04b661f245d86d882b88e3644fdaeb4978ccc07512bb3e9969f31d` |

以下為 GuideDocument normalized document hash，定義同 `document_hash`。

| slug／語系 | 修正前 | 修正後 |
| --- | --- | --- |
| `seo-keyword-research`／zh-TW | `4c59ec325c0e7cefe55a6cf62a58d9cba9860f2f0638f9bdfcfb5bb6bcd07929` | `00b3f0c5941156f9905c2f98e4964eb8ff94fba9e7b454d9edb055014166fe06` |
| `seo-keyword-research`／zh-CN | `a13df2f8839ecae45b1c70b1ba2612ff78968fc7801b71e77eebb614a582e400` | `3723eb11687bf7d1701f16bb9ed6b3ff080ffd4a6423092bd8a783397b3fc8f6` |
| `seo-keyword-research`／en | `eedfae3dc174cf65ae7797d51ab510524e375d5da9126ad386b93a5ba870abe7` | `7309f68d8fce02b14a5f1334aaff24961d0ba286b9023a13c10487338d2cd48c` |
| `seo-keyword-research`／ja | `6b1e3ff00e4c2a0b9bdde951ee8f7d88852232aa59eebfd5dfecc6ea57df13b3` | `d719c4bc84394bf70179cafe742044294f21939313670f5fff5bcf8e91ebb836` |
| `seo-keyword-research`／ko | `a8b76c00a289f20fa3d07197b4c3386e1c153c302c3e145981690e1351598ca9` | `7b4a2d71bb31865cc38ac1d96266e7c2af38a4a2484a59312926b29763b337fd` |
| `seo-title-writing`／zh-TW | `c35deec9315196507dcbaeb8b0e1e347a339e35ecba692a1c4a9baafc621e361` | `b2636ff3d05a40138d395a24d59cd730ba24103bc7b85856f38839bb2de785e7` |
| `seo-title-writing`／zh-CN | `c4804819e9c99ff10577900e8c149f85b1cbc7e86af4fe1988b1a65559663f94` | `6f18986ee0a6db83fa11c2f3ee299c5a31dd920ef1310f54f6f6319edef0bfcb` |
| `seo-title-writing`／en | `49479ee491b2c8c72316b159d4639a631a41b073acdc2c71ec8ef5ab00a80387` | `1cf311b04444a7038c098457f33808c28c0264dfd46a869f7654f423776ca1fa` |
| `seo-title-writing`／ja | `b73ef38377e499082fd6cb1eea5ba67c66b88b0c89ab0ede8dccb96d74644fb3` | `e465fb9ac6e706fb44e1ad318707e72752cc401f15bf4cc6528c279e85f9d8d9` |
| `seo-title-writing`／ko | `82d41007b995431184f6d524da41a6bc75806d6c8a974d00b0fee306ee6d2776` | `53e215befd5fca1a7cb71be9bf374d04ee631f0d909974ea532f972ba36662a8` |

兩次審查均接受10份摘要，0項待改；審稿收據仍保留原始狀態及其 before/proposed hash 綁定。

| 私人審稿收據 | SHA-256 |
| --- | --- |
| `proposal-review.json` | `9fab5203baa17309f65d03350d62cf0a36ae2c01bce83bd6197c27d5a1a91892` |
| `independent-editorial-review.json` | `359e84cc1c56562a06ca18abe9f892872985182dd700c11ce52521e93d47cba4` |

## 本機檢查

- 實際 repo 的兩篇×五語 strict intake：10/10 exit 0，未使用
  `--no-reader-first`、自訂 manifest 或提高次數限制；工具與兩包的執行前後 hash 一致。
- 仍有41個非阻擋提醒：10個沒有批次 manifest、10個自製 hero 沒有來源標題可查重、
  8個語系 SVG 檔名未被舊計數規則辨識、5個既有查證措辭、8個摘要的一般數量詞。
  所有被引用圖檔存在；本次沒有把提醒當成新事實重寫文章。
- 兩包 lint：0 errors；仍有8個譯文站內連結提醒。原發布票已保留實際公開目標
  語系與相關閱讀文字的核對，未先行新增未驗證的公網連結。
- 工具回歸測試在舊 matcher 上9 failed／12 passed，修正後21 passed；安裝進 repo
  後與 content-pack／content-links 一起測為33 passed／5 skipped。5項略過是缺隔離
  PostgreSQL；沒有把 SQLite 成功當成正式庫驗收。
- scoped Ruff、測試檔 mypy 通過；共享技能契約6項通過。獨立程式覆核未發現問題。

私人 strict intake 收據 SHA-256：
`86a3c2e7be672794934784e12302a5b9d8ab23953852c44bec2de5183e4a1843`。
程式 SHA-256（UTF-8/LF）：
`e2866986620549b13e1a78d7d3e1625df15cbff9a61f4ea6123b08e99eefee2b`；
21個回歸測試的檔案 SHA-256：
`eea358f2ddf7a9d21d4d3401d60a99b53114ea828a71dd60442a4ec0da5e44c3`。

## 離線預覽

兩篇×五語×桌機／手機共20個案例全部通過：摘要在 hero 前呈現、原首段完整保留、
無頁面水平溢出，40次圖片載入成功、0個網路請求及0個頁面錯誤。獨立覆核者查看
涵蓋20個案例的摘要／首段圖與另三張首屏；未聲稱逐張看完整篇長截圖。手機較長的
前言會讓摘要延伸到下一屏，仍可正常捲動閱讀。

摘要使用從 repository 讀取的實際 SummaryCard JSX，由 React 靜態渲染；外層頁面
與樣式是 standalone 近似。這不是 Next.js route 測試或正式站驗收。

私人最終結構與目視驗收收據 SHA-256：
`fd14fad3667cac7dd7cc3979ad026cf28de3e516b1e35f36ed944f801d4a3791`；
自動瀏覽器收據 SHA-256：
`f9107d7836bf68ef09afade7cc151fda4bc7d31dc4ed86d9dd971bbcb7089415`。
自動收據保留當時「目視待審」狀態，後續目視結果另存在上述最終收據，沒有覆寫歷史。

## 發布交接

1. 先審查及合併這個獨立修正 PR。這不等於同意正式部署或匯入。
2. 按站主逐步同意重新取得正式 zh-TW 版本／雜湊，將**兩份來源摘要修正**列成
   獨立、更小的來源更新 allowlist。歷史 v4 只供對照；不得拿它直接覆蓋目前資料。
3. 用交易內 source/version/visibility guard、備份與可持久化紀錄發布來源修正，
   取得新的來源收據後，才重綁八份翻譯、審稿與同一批24張語系圖。
4. 建立明確版本的新 T2 候選；完成指定 API 映像與隔離 PostgreSQL 排演、正式
   preflight、獨立同意與五語公網驗收。SQLite 合成資料及 standalone preview
   都不替代這些步驟。

本文件不解除任何發布 hold；原凍結包、歷史正式快照及舊審稿收據仍各自保留。
