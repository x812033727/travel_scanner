# 2026-09-29 文章分批發布確認方案

狀態：**方案已備妥；尚未授權部署、匯入、發布或新的正式站操作。** 本文件只列待確認範圍、固定證據與執行門檻。完成本方案任務不代表六張原文章發布任務及 Batch003 剩餘工作完成。

## 盤點與數量

正式站快照時間為 **2026-09-29 10:14:43 台灣時間**，host HEAD `717e16280977fb5e024947bde000adbe0fe4d752`。這是已完成的四鎖、PostgreSQL repeatable-read/read-only 盤點；前後 HEAD 和容器相同。本方案未重新連線正式站或改內容包。私人稽核證據檔 `production-inventory.json` 的 SHA-256 為 `ca2ef0aa181c9bd60f13bdeb35371fd02bbe3b25f78ccd6cfa6574040d74a17a`；下表持久化本次需要的公開文章資料。

| 批次 | 文章 | 尚缺目標文件 | 待發布繁中修正 | 候選狀態 |
| --- | ---: | ---: | ---: | --- |
| Batch003 | 5 | 4 | 0 | 四篇已五語發布；onsen 四語尚需重綁、圖與審稿 |
| Batch036 marketing | 4 | 16 | 0 | 16 譯文／48 圖已合併；Pair A 額外 metadata 問題未結 |
| Batch036 measurement | 4 | 16 | 4 | 原文修正已合併；16 譯文缺目前來源綁定的完整發布證據 |
| Batch040 | 4 | 16 | 3 | 16 譯文／48 圖在 #953、#954 |
| Batch041 | 4 | 16 | 1 | 16 譯文／48 圖已隨 #940、#941 合併；來源審查／修正門檻仍保留 |
| 合計 | 21 | **68** | **8** | **48** 份已有審稿候選、**20** 份仍需製作或重綁 |

68 = 17 篇 × `en, ja, ko, zh-CN`，不含另列的 8 份 zh-TW 修正。#953、#954 兩支未合併 PR 持有 16 份目標文件與 48 圖；已合併 marketing 與 Batch041 合計32份／96圖，共有48份／144圖的候選證據。這是 GitHub 相依狀態更新，正式數量仍來自上述歷史快照；候選不表示已部署、正式匯入或公網驗收。

## T1／T2 本機候選準備

[候選凍結與驗證紀錄](article-localization/releases/p1-20260929-t1-t2/README.md)
已備妥：4篇、16份目標文件、48張語系圖片，另保留4份繁中及12張原圖。
公開 `evidence.json` 固定候選 manifest、內容／圖片／原審稿收據與工具雜湊。
完整性及5種竄改拒絕共6項通過；隔離 SQLite 匯入1項通過，確認逐波僅新增8份
譯文、保留既有資料及重跑無變更。這是合成資料驗證，仍欠路線B交易 guard、
同映像 PostgreSQL 排演與新的正式操作同意；T2 summary 審稿也仍保留。

## 逐篇發布清單

以下「來源 SHA」均是 GuideDocument 驗證、model_dump(mode=json)，再以 UTF-8、sorted keys、compact separators 計算的 SHA-256，對應 document_hash；不是 pack 原始位元組 SHA。21 個本機 pack 的原始 SHA 和正規化文件 SHA 已逐一對到快照。8 篇需修正者的 live 舊 SHA 在下一節。

所有21篇均 active/published、發布指標有效、無到期隱藏。除 Batch003 個別版本外，其他 zh-TW 均 v4、article v2。以下「四語」固定為 `en, ja, ko, zh-CN`。

| 批次／slug | 已發布／本次待發布 | repo 繁中來源 SHA-256 | 候選內容／資產 |
| --- | --- | --- | --- |
| Batch003 / `japan-hotel-room-plan-guide` | 五語已發布；繁中 v6、四語 v2；不重發 | `a4da2f0d10fca0045571733bb7713407d2741e7bee3f84560956c8573e1d135e` | [內容包](../apps/api/app/guides/content/japan-hotel-room-plan-guide.json)；快照五語全文與 repo 相同 |
| Batch003 / `japan-luggage-forwarding-guide` | 五語已發布；繁中 v6、四語 v2；不重發 | `d768c6e3c1e35a4e20f42bea41241424cce763c0038148f4c43e1de361078b8b` | [內容包](../apps/api/app/guides/content/japan-luggage-forwarding-guide.json)；快照五語全文與 repo 相同 |
| Batch003 / `japan-onsen-ryokan-guide` | 僅繁中 v8；待四語 | `66c6ecf6f37010ea0f5cc514e541950c3543183f17496ddfe3c57fd837102a8d` | [內容包](../apps/api/app/guides/content/japan-onsen-ryokan-guide.json)；**四語完整候選／資產 manifest 未備齊** |
| Batch003 / `japan-restaurant-reservation-etiquette` | 五語已發布；繁中 v4、四語 v2；不重發 | `3cb3295fdd677e421d6f31cc1cfc4740a4e6dc8175635c928b2589bd74206069` | [內容包](../apps/api/app/guides/content/japan-restaurant-reservation-etiquette.json)；快照五語全文與 repo 相同 |
| Batch003 / `japan-station-locker-guide` | 五語已發布；繁中 v6、四語 v2；不重發 | `e7be75fe82319ed5e0818ef4c0d5ab2040ab94aaaa7dc8ec2c9ee7fa06d6dd9a` | [內容包](../apps/api/app/guides/content/japan-station-locker-guide.json)；快照五語全文與 repo 相同 |
| Batch036-marketing / `marketing-plan-small-business` | 僅繁中 v4；待四語 | `1f556287a76e6352278f7a53601c6cb425201f2db1be6fe75d7f4f72943f6403` | [內容包](../apps/api/app/guides/content/marketing-plan-small-business.json)；[#908](https://github.com/x812033727/travel_scanner/pull/908) 已合併；[12 圖](../apps/web/public/guides/marketing-plan-small-business) |
| Batch036-marketing / `paid-vs-organic-marketing` | 僅繁中 v4；待四語 | `5e1a8e1569da09bc78c46a3dfc8e465550ecebf9722b21be6756023e80ff8f16` | [內容包](../apps/api/app/guides/content/paid-vs-organic-marketing.json)；[#908](https://github.com/x812033727/travel_scanner/pull/908) 已合併；[12 圖](../apps/web/public/guides/paid-vs-organic-marketing) |
| Batch036-marketing / `marketing-mix-models` | 僅繁中 v4；待四語 | `cf9325d203eae0940db98bf6cdc8efcf691667b405a9f396e6e4f16bce937725` | [內容包](../apps/api/app/guides/content/marketing-mix-models.json)；[#907](https://github.com/x812033727/travel_scanner/pull/907) 已合併；[12 圖](../apps/web/public/guides/marketing-mix-models) |
| Batch036-marketing / `brand-tone-vibe-marketing` | 僅繁中 v4；待四語 | `1e43ef74156c751df615cf65d3da529fd50b5dae4ee83486e7f697e68116f728` | [內容包](../apps/api/app/guides/content/brand-tone-vibe-marketing.json)；[#907](https://github.com/x812033727/travel_scanner/pull/907) 已合併；[12 圖](../apps/web/public/guides/brand-tone-vibe-marketing) |
| Batch036-measurement / `ga4-site-measurement` | 僅繁中 v4；待四語 | `b4720887a084a76bf4bf8cbe217a7a7197e55c403b06b91c17e1dde6f6e12390` | [內容包](../apps/api/app/guides/content/ga4-site-measurement.json)；**四語完整候選／資產 manifest 未備齊** |
| Batch036-measurement / `ga4-sessions-engagement` | 僅繁中 v4；待四語 | `ff73406a61ffefba2be42cd6d6a4d1435a6090b3fd04e220f6641b8108ec89cc` | [內容包](../apps/api/app/guides/content/ga4-sessions-engagement.json)；**四語完整候選／資產 manifest 未備齊** |
| Batch036-measurement / `google-search-console-workflow` | 僅繁中 v4；待四語 | `5e8a510cbcf7c180559db1b8a04cef77d7e83ff85a9211910b049e4586127cc8` | [內容包](../apps/api/app/guides/content/google-search-console-workflow.json)；**四語完整候選／資產 manifest 未備齊** |
| Batch036-measurement / `utm-link-conventions` | 僅繁中 v4；待四語 | `286e4b6bb93e3a1237487f1d5d6d8efa128f7cffcbd992f154731a73e88d4be7` | [內容包](../apps/api/app/guides/content/utm-link-conventions.json)；**四語完整候選／資產 manifest 未備齊** |
| Batch040 / `affiliate-marketing-basics` | 僅繁中 v4；待四語 | `c893c8eafcb6b941454590103fbac8359c0db4d29d03e1597a788acac56fc0ce` | [#953 pack](https://github.com/x812033727/travel_scanner/blob/0bbf0d74e55e4a1089009abee8525e025c894f88/apps/api/app/guides/content/affiliate-marketing-basics.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/0bbf0d74e55e4a1089009abee8525e025c894f88/apps/web/public/guides/affiliate-marketing-basics) |
| Batch040 / `ecommerce-product-seo` | 僅繁中 v4；待四語 | `25fe33ce82acaf264b19525ae192c3ca880891b8eebda6b28ef5435fffc9b2ee` | [#954 pack](https://github.com/x812033727/travel_scanner/blob/6922a5a20d92778863178ddeaab7808962170e6f/apps/api/app/guides/content/ecommerce-product-seo.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/6922a5a20d92778863178ddeaab7808962170e6f/apps/web/public/guides/ecommerce-product-seo) |
| Batch040 / `independent-store-marketplace` | 僅繁中 v4；待四語 | `7cf113f88ce54b02f4e0b096584107bf7fb69093b8d5dd74829222a7d6d03985` | [#953 pack](https://github.com/x812033727/travel_scanner/blob/0bbf0d74e55e4a1089009abee8525e025c894f88/apps/api/app/guides/content/independent-store-marketplace.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/0bbf0d74e55e4a1089009abee8525e025c894f88/apps/web/public/guides/independent-store-marketplace) |
| Batch040 / `zero-click-search-strategy` | 僅繁中 v4；待四語 | `2c0660c39def2c8b42aeac4ce1da4c0960d76eb99a48018298d7626a25307902` | [#954 pack](https://github.com/x812033727/travel_scanner/blob/6922a5a20d92778863178ddeaab7808962170e6f/apps/api/app/guides/content/zero-click-search-strategy.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/6922a5a20d92778863178ddeaab7808962170e6f/apps/web/public/guides/zero-click-search-strategy) |
| Batch041 / `seo-keyword-research` | 僅繁中 v4；待四語 | `4c59ec325c0e7cefe55a6cf62a58d9cba9860f2f0638f9bdfcfb5bb6bcd07929` | [#940 pack](https://github.com/x812033727/travel_scanner/blob/91219fda72e401003ba6f069b59db30559845f06/apps/api/app/guides/content/seo-keyword-research.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/91219fda72e401003ba6f069b59db30559845f06/apps/web/public/guides/seo-keyword-research) |
| Batch041 / `seo-title-writing` | 僅繁中 v4；待四語 | `c35deec9315196507dcbaeb8b0e1e347a339e35ecba692a1c4a9baafc621e361` | [#940 pack](https://github.com/x812033727/travel_scanner/blob/91219fda72e401003ba6f069b59db30559845f06/apps/api/app/guides/content/seo-title-writing.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/91219fda72e401003ba6f069b59db30559845f06/apps/web/public/guides/seo-title-writing) |
| Batch041 / `on-page-seo-workflow` | 僅繁中 v4；待四語 | `4916a8cc37818e40960e39a28243f2bc8c62f5f07457745ea70f59505a924479` | [#941 pack](https://github.com/x812033727/travel_scanner/blob/4d425bd28344bbfab32af805a53e21b811836cf4/apps/api/app/guides/content/on-page-seo-workflow.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/4d425bd28344bbfab32af805a53e21b811836cf4/apps/web/public/guides/on-page-seo-workflow) |
| Batch041 / `image-seo-workflow` | 僅繁中 v4；待四語 | `e359a3d9f84fb59983424ec12a82369839d88c5570b1845e0c3c5af5345e433d` | [#941 pack](https://github.com/x812033727/travel_scanner/blob/4d425bd28344bbfab32af805a53e21b811836cf4/apps/api/app/guides/content/image-seo-workflow.json)；[12 圖](https://github.com/x812033727/travel_scanner/blob/4d425bd28344bbfab32af805a53e21b811836cf4/apps/web/public/guides/image-seo-workflow) |

onsen 的繁中修正已發布：v8、來源 SHA 如表，pack 位元組 SHA `febd82c4b31ef49e7a625efc4174e4174e6c5f8c4716bdd4e85997a2e6f985aa`，與 #588 修正版一致。不能算第九份待修正來源。四語預定落點為其內容包的 en/ja/ko/zh-CN 與 `apps/web/public/guides/japan-onsen-ryokan-guide/` 中由新 artifact manifest 指定的資產；**目前沒有合格的新 manifest 或可直接發布的四語圖檔清單**。舊稿需依已修正來源重綁並重審。已完成四篇的 bundle manifest `099aec1b983a418f288998840c1548b51c90ab3f8e496c5ba702dac281d8186b` 不涵蓋 onsen，不可沿用。

## 八份繁中修正：十二處錯誤站內連結

已用相應 merge commit 的 parent 內容重建舊稿，確認其 normalized SHA 等於 live 快照。差異只把 ArticleInline 改成相同可見文字的 TextInline；沒有改段落、來源、root metadata 或原圖。表內為零起算 RFC 6901 pointer。

| 波次／slug | 來源 PR | live 舊 SHA → repo 新 SHA | 精確操作 |
| --- | --- | --- | --- |
| S1 / `ga4-sessions-engagement` | [#902](https://github.com/x812033727/travel_scanner/pull/902) | `88d0f3c1803879d39a8e7dcc142b92dcdcdd1c1398450a4d7550d8b4a22ec0d2` → `ff73406a61ffefba2be42cd6d6a4d1435a6090b3fd04e220f6641b8108ec89cc` | `/blocks/8/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}` |
| S1 / `ga4-site-measurement` | [#902](https://github.com/x812033727/travel_scanner/pull/902) | `cbcfe4cdd261a10fbfaa2249a8baa7f91d09e413c96af087c304438e98e7a921` → `b4720887a084a76bf4bf8cbe217a7a7197e55c403b06b91c17e1dde6f6e12390` | `/blocks/12/inlines/1`：`{"type":"article","text":"參數","kind":"life","slug":"ai-term-model-parameters"}` → `{"type":"text","text":"參數"}`<br>`/blocks/13/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}` |
| S1 / `google-search-console-workflow` | [#902](https://github.com/x812033727/travel_scanner/pull/902) | `3170ef7dd3a419f96e23731bf7ca9570ed0c59f380327c9627cff39432544734` → `5e8a510cbcf7c180559db1b8a04cef77d7e83ff85a9211910b049e4586127cc8` | `/blocks/12/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}`<br>`/blocks/21/inlines/1`：`{"type":"article","text":"參數","kind":"life","slug":"ai-term-model-parameters"}` → `{"type":"text","text":"參數"}` |
| S1 / `utm-link-conventions` | [#902](https://github.com/x812033727/travel_scanner/pull/902) | `c10ea735007d5fe11ea95147984add5b40beff6ee45be075669019454c51ed08` → `286e4b6bb93e3a1237487f1d5d6d8efa128f7cffcbd992f154731a73e88d4be7` | `/blocks/1/inlines/1`：`{"type":"article","text":"參數","kind":"life","slug":"ai-term-model-parameters"}` → `{"type":"text","text":"參數"}`<br>`/blocks/21/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}` |
| S2 / `affiliate-marketing-basics` | [#930](https://github.com/x812033727/travel_scanner/pull/930) | `d8b48acf8b07e6d2175a68bd58ed20bbbb5233bdbf3f91dbf48f089a26e44e32` → `c893c8eafcb6b941454590103fbac8359c0db4d29d03e1597a788acac56fc0ce` | `/blocks/17/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}` |
| S2 / `ecommerce-product-seo` | [#930](https://github.com/x812033727/travel_scanner/pull/930) | `4113bffff6500ce1136fc7cc085978d22ba6d32acbfbb2d889c2ffb06e7c6ffd` → `25fe33ce82acaf264b19525ae192c3ca880891b8eebda6b28ef5435fffc9b2ee` | `/blocks/1/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}`<br>`/blocks/12/inlines/1`：`{"type":"article","text":"參數","kind":"life","slug":"ai-term-model-parameters"}` → `{"type":"text","text":"參數"}` |
| S2 / `zero-click-search-strategy` | [#930](https://github.com/x812033727/travel_scanner/pull/930) | `b27d1f15ec07653f055a9008d177fbc80c93675cc7b92ea37d1396f9bb8069c5` → `2c0660c39def2c8b42aeac4ce1da4c0960d76eb99a48018298d7626a25307902` | `/blocks/11/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}` |
| S3 / `image-seo-workflow` | [#934](https://github.com/x812033727/travel_scanner/pull/934) | `0f9bbddbf9ec3c9a236c93b0e666e03a211e947988a92a5950b4cac99dbd93b0` → `e359a3d9f84fb59983424ec12a82369839d88c5570b1845e0c3c5af5345e433d` | `/blocks/16/inlines/1`：`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}` → `{"type":"text","text":"標記"}` |

S1 = measurement 4篇／7處；S2 = Batch040 3篇／4處；S3 = Batch041 image-seo 1篇／1處。原文發布後重新匯出來源版本及 published SHA，再把翻譯綁定到新正式版本。repo 已修正不表示 live 已修正。

## PR 與審稿收據

2026-09-29 本機準備時唯讀重查 GitHub：**#940、#941 已合併；#953、#954 仍為 OPEN、isDraft=false**。本方案沒有合併或改其狀態，也沒有宣稱這些合併已部署。下方審稿證據仍固定原 review head，不以 merge SHA 偷換審稿版本；PR 更新／rebase 後要重新核對。

| PR | 現況／用途 | merge SHA 或目前 head SHA |
| --- | --- | --- |
| [#588](https://github.com/x812033727/travel_scanner/pull/588) | MERGED；onsen 繁中已發布 | `8264c01a77f1044c9b8e756addaaa997bbc1c58a` |
| [#592](https://github.com/x812033727/travel_scanner/pull/592) | MERGED；Batch003 其餘四篇已五語發布 | `ac860f386e2f30dd68dcfff59a66d57272d8fc34` |
| [#902](https://github.com/x812033727/travel_scanner/pull/902) | MERGED；measurement 繁中修正 | `3f22a60f06570ba269e8c5568cdabb10e4c5720e` |
| [#907](https://github.com/x812033727/travel_scanner/pull/907) | MERGED；marketing Pair B，8譯文／24圖 | `3c48ccd91e4a34fba139f107cca2f6fba9da9658` |
| [#908](https://github.com/x812033727/travel_scanner/pull/908) | MERGED；marketing Pair A，8譯文／24圖 | `22c86ec81f02b8d3c7fe179e954d5cb90e23be65` |
| [#930](https://github.com/x812033727/travel_scanner/pull/930) | MERGED；Batch040 繁中修正 | `d68ab5db9a417f8f764b8bb9b39ace058c350e68` |
| [#934](https://github.com/x812033727/travel_scanner/pull/934) | MERGED；Batch041 image-seo 繁中修正 | `7654e7b5ed14f3e3a118d7a271c887d4c9b1e977` |
| [#940](https://github.com/x812033727/travel_scanner/pull/940) | MERGED；Batch041 keyword／title，8譯文／24圖 | `ef2b3fb98bf7eb9c848c6c46258291c0355fb135` |
| [#941](https://github.com/x812033727/travel_scanner/pull/941) | MERGED；Batch041 on-page／image，8譯文／24圖 | `4dc3bd4812451762885c73ab96ce88a719069f0b` |
| [#953](https://github.com/x812033727/travel_scanner/pull/953) | OPEN；Batch040 affiliate／store，8譯文／24圖 | `0bbf0d74e55e4a1089009abee8525e025c894f88` |
| [#954](https://github.com/x812033727/travel_scanner/pull/954) | OPEN；Batch040 ecommerce／zero-click，8譯文／24圖 | `6922a5a20d92778863178ddeaab7808962170e6f` |

marketing 的逐文件與逐圖證據：[Pair A](article-localization/batch036-marketing-pair-a-evidence.md)、[Pair B](article-localization/batch036-marketing-pair-b-evidence.md)。舊證據中的 CI pending 是當時狀態；合併狀態以上表為準。其 JSON canonical hash 與本文件的 GuideDocument normalized hash 定義不同，不能混比。

四份私人工作区 final-peer-qa 收據都已重算 SHA，並對到下列固定 head 的公開證據。每份含兩個 pack SHA、五語 normalized document SHA、24個資產 SHA；附件目標表固定本次讀取的32份文件。

| PR | 公開證據 | 私人工作區內相對收據名 | 收據 SHA-256 |
| --- | --- | --- | --- |
| [#940](https://github.com/x812033727/travel_scanner/pull/940) | [review evidence](https://github.com/x812033727/travel_scanner/blob/91219fda72e401003ba6f069b59db30559845f06/docs/article-localization/batch041-pair-a-evidence.md) | `batch041-pair-a/final-peer-qa/review-hashes.json` | `91c3801224784c30fc93f2236e86cf2525358ea63ffa6e15a3292c81853f8adb` |
| [#941](https://github.com/x812033727/travel_scanner/pull/941) | [review evidence](https://github.com/x812033727/travel_scanner/blob/4d425bd28344bbfab32af805a53e21b811836cf4/docs/article-localization/batch041-pair-b-evidence.md) | `batch041-pair-b/final-peer-qa/review-hashes.json` | `bdc30cbe2ee0e51d5cc08504028ae13df8f26633e1c2753cff9a091a073f441e` |
| [#953](https://github.com/x812033727/travel_scanner/pull/953) | [review evidence](https://github.com/x812033727/travel_scanner/blob/0bbf0d74e55e4a1089009abee8525e025c894f88/docs/article-localization/batch040-pair-a-evidence.md) | `batch040-pair-a/final-peer-qa/review-hashes.json` | `0590025b81b3e5b18a658169e9746452f29e7a710cdd83ecaad1abb6c4bc91b0` |
| [#954](https://github.com/x812033727/travel_scanner/pull/954) | [review evidence](https://github.com/x812033727/travel_scanner/blob/6922a5a20d92778863178ddeaab7808962170e6f/docs/article-localization/batch040-pair-b-evidence.md) | `batch040-commerce-search-pair-b/final-peer-qa/review-hashes.json` | `10090e34f05628d40c4cc9c12b57f0ce9844e32711c354819ce87e4bbcf38785` |

### Pair A 額外待處理問題

`paid-vs-organic-marketing` 的 /sources/1 標題「Google 搜尋中心：廣告與自然搜尋結果的區別」對到 `https://developers.google.com/search/docs/fundamentals/do-i-need-seo`；/sources/2 是 `https://support.google.com/google-ads/answer/2567043?hl=zh-Hant`。原審稿已註記標題不符與固定繁中 URL。建議 Pair A 八份先保留，完成版本化的來源 metadata 修正、受影響四語同步／重審與新 hash，再提出**額外來源更正**確認；不能夾入上列八份 inline 更正。marketing-plan 本身沒有同樣問題，站主可選擇先獨立發布其四語。Pair B 不受此問題牽連。

## 建議波次與每批允許變化

各列獨立 allowlist、dry-run 和發布後收據。可先準備及審查；正式步驟仍逐步取得站主明確同意。前一列完成不自動批准下一列。

| 順序 | 範圍 | 預期變化 | 開始條件 |
| --- | --- | --- | --- |
| 0 | 本機 manifest、guard driver、同映像隔離排演 | 正式站0寫入 | 固定各波 slug/locale/來源/目標/圖 hash；補齊缺件 |
| S1 | measurement 四篇，只 zh-TW | 4來源更新；目標語系0新增 | #902在選定映像；僅表列7處 diff |
| S2 | affiliate、ecommerce、zero-click，只 zh-TW | 3來源更新；目標語系0新增 | #930；僅表列4處；store不在此波 |
| S3 | image-seo，只 zh-TW | 1來源更新；目標語系0新增 | #934；僅表列1處 |
| T1 | marketing mix、brand-tone，各四語 | 8 locale create／發布；繁中不變 | #907及圖在映像；來源無漂移 |
| T2 | Batch041 keyword、title，各四語 | 8 locale create／發布；繁中不變 | #940已合併；兩篇原文summary審查、exact-head CI、排演仍須完成 |
| T3 | Batch040 affiliate、store，各四語 | 8 locale create／發布；繁中不變 | S2 affiliate完成；#953合併、rebind、排演 |
| T4 | Batch040 ecommerce、zero-click，各四語 | 8 locale create／發布；繁中不變 | S2完成；#954合併、rebind、排演 |
| T5 | Batch041 on-page、image，各四語 | 8 locale create／發布；繁中不變 | S3完成；#941合併、rebind、排演 |
| T6 | marketing plan、paid-vs-organic，各四語 | 8 locale create／發布；額外來源修正另計 | metadata修正另行確認、受影響文件重審 |
| T7 | measurement 四篇，各四語 | 16 locale create／發布；繁中不變 | S1後新基準、16份翻譯／圖／獨立審稿及內容PR |
| T8 | Batch003 onsen，各四語 | 4 locale create／發布；繁中內容不變 | 修正版來源重綁、4份翻譯／圖／審稿、新bundle與內容PR |

T1–T5共40份已有審稿候選但仍有門檻；T6另8份候選；T7–T8為未備齊20份。版本號由服務決定，不預造發布後 v5／v6。

## 執行步驟與停止／回復條件

依據：[article-localization](../.agents/skills/article-localization/SKILL.md)、[content-pipeline](../.agents/skills/content-pipeline/SKILL.md)、[四鎖與hold](../ops/release/README.md)、[publisher](article-localization/publish_bundle.py)、[source correction](article-localization/source_correction.py)、[管理服務](../apps/api/app/guides/admin_service.py)。

1. **本機準備**：選定波次，固定 pack／資產／審稿 hash及部署提交，必要CI在該提交通過。8份來源更正需由上表加 fresh snapshot 製作完整 source-correction receipt（舊draft／published全文、版本、hash、可見性、pointer）；此表不能代替正式收據。未選locale全文保留。
2. **隔離排演**：以同API映像和隔離PostgreSQL測 dry-run、交易內來源與版本guard、編輯衝突、撤稿／隱藏／到期、失敗後同state續跑及回復。#940、#941、#953、#954 的既有證據沒有成功排演收據；skipped或environment unavailable不算通過。來源單獨發布及路線B scoped import的guard driver尚待製備／審查／排演，不能只用CLI dry-run替代。onsen沿用路線A；既有路線B批次可用受guard保護的scoped import。
3. **正式fresh preflight**：取得指定步驟同意後，核对當時HEAD、映像、四鎖、hold、release state，以及allowlist各篇article/locale版本、draft/published hash、active/status/expiry和缺語系列；任何來源、資產、可見性或缺列狀態漂移就停該波，不覆蓋編輯。這份盤點不代替未來preflight。
4. **備份／部署**：第一個資料寫入前做pg_dump -Fc，pg_restore --list驗證並記dump SHA。只在映像缺所需內容或程式時部署批准SHA。多階段driver於持四鎖時acquire hold，每段verify，所有階段成功後clear；失敗／回復保留hold。不得覆寫別人的hold或在內容階段之間另跑一般部署。
5. **dry-run與diff**：完整指定slug和locale。S1/S2/S3只允許4/3/1份zh-TW更新；T波只允許指定缺語系create，taxonomy不得意外改變。比較正規化正文及表列更正，保存實際返回值，不捏造成功数量。apply前重跑dry-run和已批准收據一致，寫入交易內再驗來源／版本。
6. **發布**：A路線固定同bundle、baseline、manifest SHA、deployed-root、actor及state-dir，dry-run → drafts → publish-articles → publish-hubs；本次沒有hub時不得新增其他文章。失敗用同state對帳。B路線下方CLI僅為呼叫形狀，外層必須補交易內guard與durable receipt。不要把整波當天然全有全無，逐篇記錄完成量，失敗即停。
7. **核對／公網驗收**：published pointer／版本／body hash對批准manifest；未選語系、來源及root狀態不變。再dry-run應unchanged。經批准links rebuild/check，檢查同語系文章連結不連私人草稿。最終17篇五語共85頁、桌機＋手機共170個檢視組合：h1、全文、圖片位元組／缺字／溢出、canonical、hreflang、連結、sitemap各分頁。分批先驗當時已公開語系，全數完成再驗85頁矩陣；HTTP200或有資料列都不等於完成。
8. **回復**：依前後版本收據界定已寫入範圍。新目標locale用expected_version撤回，只作用於本波新發布列，保留revision/audit，不刪文章或資料列。繁中回復先restore_revision到原正文，再以正確expected_version publish_locale；restore_revision只改draft，不會自動恢复公開正文。後續有人編輯則停，不強覆蓋。回復必須先排演並取得正式步驟同意；整庫restore只作另行批准的災難回復。
9. **紀錄／結案**：在對應releases/<batch>/存去識別README／evidence（部署／manifest SHA、逐篇版本/hash、審稿鏈、公網圖證、失敗／回復）。私人快照、actor和備份位置留私人目錄。原發布票只有整張驗收完成才結案。

路線B的T1呼叫形狀（**尚未執行；不能跳過外層guard**）：

```bash
python -m app.cli guides-import --slug marketing-mix-models --slug brand-tone-vibe-marketing --locale en --locale ja --locale ko --locale zh-CN --dry-run
# 僅在批准的driver內，再次檢查來源／版本／hold且dry-run一致後：
python -m app.cli guides-import --slug marketing-mix-models --slug brand-tone-vibe-marketing --locale en --locale ja --locale ko --locale zh-CN --publish --actor-email <ACTIVE_ADMIN_EMAIL>
```

路線A命令形狀（占位值需由該波完整artifact補齊）：

```bash
python publish_bundle.py --bundle <BUNDLE> --baseline <BASELINE> --manifest-sha256 <SHA256> --deployed-root <APP_ROOT> --state-dir <STATE> --actor-id <ADMIN_UUID> dry-run
# 其他參數不變，依序改phase為drafts、publish-articles、publish-hubs。
```

**publisher相依限制**：當下publish_holds必須對所有公開內容階段生效，不能沿用舊參考文件「bundle不讀holds」而繞過。修正目前在 **PR #966**，同PR還含startup token guard；正式API/web盤點的token未設定，所以PR應保持draft，不能直接合併／部署。需先完成經批准的設定處理並合併／選定release版本，或另行審查獨立publisher修正；執行前驗證實際部署程式。解除兩個過時Singapore hold不批准本表發布。

## 需要補齊或確認

| 項目 | 本次狀態／下一步 |
| --- | --- |
| 批次順序 | 建議S1–S3後T1–T5；T6待metadata，T7–T8待新候選；站主可只同意部分波次準備 |
| Pair A | 建議先修paid-vs-organic；是否先獨立發布marketing-plan四語需站主決定，新增來源更正另計 |
| 部署SHA、映像digest、fresh CI | 未選定；不能把盤點host HEAD／PR head當已批准部署值 |
| 各波baseline、manifest SHA、來源收據、guard driver | 尚未形成可執行release artifact；需本機製備、獨立審查、排演再確認 |
| 同映像隔離排演 | #940、#941、#953、#954均未有完成證據，合併不代替排演；必須補齊 |
| measurement16份／onsen4份 | 缺新來源綁定、完整圖manifest、逐語審稿及內容PR；沒有可核准的最終target SHA |
| 正式preflight、備份、actor、發布及瀏覽器證據 | 尚未執行；正式每一步待站主明確同意，當時取得值 |

本方案完成表示精確清單、證據與門檻可供確認；沒有宣布68份可立即一次發布。

## 附錄：48份已有候選的目標文件雜湊

均為GuideDocument正規化SHA：marketing從repo計算，其餘從上述釘住SHA的review receipt讀取。安裝／合併／rebase後需重算；來源或metadata改動要重審受影響稿，不能沿用本表批准新稿。

| slug | locale | SHA-256 | 持有位置 |
| --- | --- | --- | --- |
| `marketing-plan-small-business` | `en` | `f91360e9c4d8f68fa92e8b220f12bcc8a45a84b27e3e4a41750bd5c474f3c335` | 已合併repo |
| `marketing-plan-small-business` | `ja` | `ab953256e587644b716bdc6d9df3d6f6e547902a4cab58ff37819478a902dabf` | 已合併repo |
| `marketing-plan-small-business` | `ko` | `3403fe90d885faf4c054dd02f7a05e31d6835358fc801174cabfc7425fb37a89` | 已合併repo |
| `marketing-plan-small-business` | `zh-CN` | `1a7ed503b7e11a2fc7275da3ddb5e554efddb87beae344d2d2b21e178a456792` | 已合併repo |
| `paid-vs-organic-marketing` | `en` | `f40be0cb197bdfc97e484b029b23e689dbad1b9e923d9b079b55fbbd4bc27cdf` | 已合併repo |
| `paid-vs-organic-marketing` | `ja` | `d38f3343354ff4073b16480ef09850415cfdb074a0078fe6f0bc107747d4cd00` | 已合併repo |
| `paid-vs-organic-marketing` | `ko` | `ea1cd0608228020ccdcd683a97e555e2eaddb90ac38a0add7875abd4f16ab097` | 已合併repo |
| `paid-vs-organic-marketing` | `zh-CN` | `2148930e6becb9baa3709dddd8dd1761352a678a9e4d52ca4dca8fe04e0dc41f` | 已合併repo |
| `marketing-mix-models` | `en` | `373a0509f37ab7a87abf760a20707b6fbabb8d16add2ec16caa7f4cc955a8551` | 已合併repo |
| `marketing-mix-models` | `ja` | `a4394674ae748c9de956a3edfe5eac35ea76d142da48f4e28e8c95c9d3462384` | 已合併repo |
| `marketing-mix-models` | `ko` | `1b83cd2e4005d1a2cf8ca2a270a0fc022283c4801b894304590de7316138468b` | 已合併repo |
| `marketing-mix-models` | `zh-CN` | `5ca07548800feb23a11c71e5f918ade7efb02b87acf203051cbdf856319b296c` | 已合併repo |
| `brand-tone-vibe-marketing` | `en` | `56159ebd2e52b00c09f64282b19de33e75d361d243f343a5a926188c7ef23e3a` | 已合併repo |
| `brand-tone-vibe-marketing` | `ja` | `5fce4e8124d6b1655ac980f8f04954490540ed9fda702e9b1b9d996153af205b` | 已合併repo |
| `brand-tone-vibe-marketing` | `ko` | `0f53faacc291720b831a97ec238f13c1f9a2f02a3f54b96d8624e179fa0b10cc` | 已合併repo |
| `brand-tone-vibe-marketing` | `zh-CN` | `9eb16f372750eab74df7d59dc850dd73bcd55839c063d06f9af7d6ae515591ff` | 已合併repo |
| `seo-keyword-research` | `en` | `eedfae3dc174cf65ae7797d51ab510524e375d5da9126ad386b93a5ba870abe7` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `seo-keyword-research` | `ja` | `6b1e3ff00e4c2a0b9bdde951ee8f7d88852232aa59eebfd5dfecc6ea57df13b3` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `seo-keyword-research` | `ko` | `a8b76c00a289f20fa3d07197b4c3386e1c153c302c3e145981690e1351598ca9` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `seo-keyword-research` | `zh-CN` | `a13df2f8839ecae45b1c70b1ba2612ff78968fc7801b71e77eebb614a582e400` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `seo-title-writing` | `en` | `49479ee491b2c8c72316b159d4639a631a41b073acdc2c71ec8ef5ab00a80387` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `seo-title-writing` | `ja` | `b73ef38377e499082fd6cb1eea5ba67c66b88b0c89ab0ede8dccb96d74644fb3` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `seo-title-writing` | `ko` | `82d41007b995431184f6d524da41a6bc75806d6c8a974d00b0fee306ee6d2776` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `seo-title-writing` | `zh-CN` | `c4804819e9c99ff10577900e8c149f85b1cbc7e86af4fe1988b1a65559663f94` | [#940](https://github.com/x812033727/travel_scanner/pull/940) |
| `on-page-seo-workflow` | `en` | `fdedd7db594797846c46614ec1c570a6c0aa81f3ef0ed3e114afc858e015e912` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `on-page-seo-workflow` | `ja` | `93af5cae9e98710541935b067c0379677f5719d6665323493ca61ad0a2857049` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `on-page-seo-workflow` | `ko` | `e29c3c2e5789283a02ae9bc5ae3547854d77da406a666786223c6f7658419162` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `on-page-seo-workflow` | `zh-CN` | `531dfef338314b32f95ec078da92c0f5ec2ee3fafa39ab1d036269dfcdc3af2e` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `image-seo-workflow` | `en` | `9254857df9bb2dc059e2762dafa5558831315d0599df753e388c32f98c20ad6e` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `image-seo-workflow` | `ja` | `89af3e12f925071f0b291e503f81e34f26c7768023aa0bc5f4229ccdf92d957a` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `image-seo-workflow` | `ko` | `9ed7ce44b430a7077e1102de5d6cc57e6d612291089afe521cba793468b5102c` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `image-seo-workflow` | `zh-CN` | `f7c90be51532375c3ff018c55773b66365513d8383891b10c6c3f7438dc29bd7` | [#941](https://github.com/x812033727/travel_scanner/pull/941) |
| `affiliate-marketing-basics` | `en` | `59d903bf04ff70a43be15338b550d4acd07ae187cddd55a407f1c99edef32346` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `affiliate-marketing-basics` | `ja` | `81defe39a0b72d6c8713d4cbcee63f653156d081af487ecb880f25f4b2f41d26` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `affiliate-marketing-basics` | `ko` | `2fde2eaabb5806bd943b0764a36964820e6593b798f5dda07a891890457a62ef` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `affiliate-marketing-basics` | `zh-CN` | `e641651be4ae027a4438fe0280e0143ca56ac2b2d0c661dbf3c0c90b8ab2a4ab` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `independent-store-marketplace` | `en` | `d5ff72f6812047ca05a76b0bd219524ead5b977a524d960bb163e0c5fa8cc39d` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `independent-store-marketplace` | `ja` | `88abca048b9b07fb816ce88b627cc2c0004d25d30b52d30c0a75853fcc7084d5` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `independent-store-marketplace` | `ko` | `2deecc52e3e944025ce4a50e5e68703805f80a88425f4c5e486cba78086b4687` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `independent-store-marketplace` | `zh-CN` | `1d8d659551cd1f322a886dc798cd62b481191fe52be6bb87ac74bbf6029e5102` | [#953](https://github.com/x812033727/travel_scanner/pull/953) |
| `ecommerce-product-seo` | `en` | `179dc082f7f70b3e1b4564294f9db0550622cd31fb8ca9528c12b62077bca67a` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
| `ecommerce-product-seo` | `ja` | `9a79b3ec62b053726580b079eab62212a56d4c5ee9776fca5b83c0ef01f1f0bc` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
| `ecommerce-product-seo` | `ko` | `2a841f12c410eed7c1a8685ee3e20beb076c3b100c4dab123feb138a1f62326f` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
| `ecommerce-product-seo` | `zh-CN` | `0527e40fa3057a329d10c236a63c609e41f87c64595f678c74698dd6fc5e5b23` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
| `zero-click-search-strategy` | `en` | `dece135cba2abc5c915191270ca53c6d4e5a482f46e54ef3f3b61b5e91b2944a` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
| `zero-click-search-strategy` | `ja` | `ecb208f3c894ae38f33a55b83f123d60c2ab1814e244eecd396b3846ff63dc71` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
| `zero-click-search-strategy` | `ko` | `666904c88ba0bad06c37019ae8bae120e8fcb35fd861645b016be2c0153d9d56` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
| `zero-click-search-strategy` | `zh-CN` | `c77001eeffe00f95626783157b2e9808a2a8ebfcc0ec4fbad7c0222573caaf67` | [#954](https://github.com/x812033727/travel_scanner/pull/954) |
