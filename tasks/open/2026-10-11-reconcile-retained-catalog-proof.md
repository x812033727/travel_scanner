---
id: 2026-10-11-reconcile-retained-catalog-proof
title: 逐 ID 對帳封存的 181 筆目錄證據缺口，保留真正未結案項
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T13:46:05Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-reconcile-retained-catalog-proof.md
---

## Why

原分支 `codex/content-review-resolution` HEAD `9cd24e2be787925be58eb55418c4d9b6333fa049` 保存已套用且獨立核對的 2026-09-09 finite review：189 筆中僅 8 筆新增有證據的狀態決定，留下 181 個 `keep_pending` IDs（154 店家、22 文章、5 影片）。原票 `2026-09-08-remaining-189-catalog-proof` 未隨同證據包進入共享主線；目前未找到這個 exact ID cohort 的後續逐筆結案收據。181 是歷史封存集合，絕不是 2026-10-11 正式站仍待審數。後續補資料、地圖與訂位操作可能已處理其中部分，必須先排除，不能重播原操作。

## Done when

- [ ] 從下列精確 ID 集合建立 181/181 對帳表；每列含類型、當前存在與狀態、最新相關 audit/來源證據、核對時間及歷史缺件是否已補足。已完成、已刪除、被替代與仍待證據分別有可追溯結論；無讀取權限的列明確標「尚未核對」。
- [ ] 對剩餘真正缺件逐列寫下可執行的下一步，或引用已存在任務和認領者。文章／影片核對原文、語言與實質內容；店家核對 exact branch 身分、精準地圖與耐久座標來源。無法取得證據就記具體限制，不能把看不到頁面當成拒絕理由。
- [ ] 已有相同 ID 的 open/done 票先引用，不重複開研究票；新增修正或正常審核如有必要，另立新的有限 manifest/窄 scope，保留原 applied manifest 與稽核歷史。
- [ ] 原分支證據包和舊票的去向已保全且列在本票；對帳完成不自動等於剩餘商品已發布。

## Steps

- [ ] 唯讀擷取 `git show 9cd24e2be787925be58eb55418c4d9b6333fa049:docs/catalog-content-reviews/2026-09-09-remaining-proof.json`，核對只選 `decision=keep_pending` 的 154+22+5 個 IDs；不得把原 189 件或後來的全佇列數當成本票 cohort。
- [ ] 在目前主線與共享票逐 ID 搜尋後續收據，尤其 `2026-09-12-food-merchant-enrichment`、`2026-09-06-naver-maps-key`、`2026-09-07-merchant-style-discovery` 和後续訂位／CatchTable 票；相同 IDs 僅對帳和引用，不接管其 claims。
- [ ] 以允許的唯讀來源取得每列現在的狀態、相關審核紀錄及來源，不執行 POST/PATCH 或重播 `2026-09-09-final-proof-decisions`。沒有權限則保留具體讀取缺件，不推論目前 pending。
- [ ] 將唯一剩餘 proof 工作及已有工作的對應關係記入本票；只在確實需要新的實作／審核時拆票。

## Verification

精確覆蓋 181 個不同 IDs，分類數 154/22/5；下列 ID 集合的 compact sorted-key JSON SHA-256 為 `92a8958eb7b6e656a9f527a0280452fbde3f2f4a584121f760d7a29dd67c78b9`。歷史 JSON 文字 SHA-256 為 `5818b278bf606d21894607f11ff4a25b528f6b5fe3a4aed6f12f7b7e836c2c7a`，原 manifest 的獨立核對時間為 `2026-09-09T00:32:02.029875+00:00`，fingerprint `caa2e9a336f89d4f07ed6b078409a705c624938e53933d81a4ee0313fdc2e0d6`。對帳前後正式資料與原 applied audits 均不變；任何「已完成」判定須有對應該 ID 的後續正面證據。

## Notes

證據原路徑：`docs/catalog-content-reviews/2026-09-09-remaining-proof.json`、`docs/catalog-content-reviews/2026-09-09-remaining-proof-result.md`、原 `tasks/open/2026-09-08-remaining-189-catalog-proof.md`，皆可用上列 HEAD 唯讀取回。scratch 完整抽取（包含每筆歷史缺件）：`C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/catalog-retained-proof-cohort.json`；最終分支證據在同目錄 `catalog-audit.json` 與 `catalog-evidence.json`。主線 PR #408 的 296 店家／311 訂位 review 是另一 scope；只能逐 ID 交叉引用，不能當成本票文章、影片、座標證據全部結案。

2026-10-11 分支續查；共享票比對基線為 main `73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b` 的全部 389 張 open 票，未找到同義任務（詳 `C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/catalog-open-task-check.json`）。本票只追蹤唯讀對帳與保全，初始 scope 僅含本票檔案，結果直接記在本票。任何程式、資料或其他證據檔修改須另開窄 scope 票並先核對所有者；不釋放或覆寫任何原 claims、owner、scope。未發布、未公開、舊票仍在 open、當前主線較新，均不能單獨證明現在仍 pending。這次開票不授權正式資料寫入、重播舊 batch、付費呼叫、部署或發布。

### 歷史 merchant IDs（154）

```text
0181ec5c-0143-457b-8090-73f232178c25
0299e3f7-fc78-479e-9e7e-31c66d6be476
03fd0c86-e0a0-4827-8c8d-b1f7e55a2bff
040b647a-c014-40f8-9228-88e572be0341
08d6c559-42a2-44d6-87d4-c537729cc723
0ae25e81-8099-458f-b499-f7f60e49ee47
0b134656-bbb2-4c36-bc2c-6b35c7ef95b7
0d23757a-72e3-4005-ac3b-e03bbf4c299d
0d273ace-605d-4241-a31f-b50901a84991
0e9b5728-b9ea-47b2-a509-80e2cf780276
104ef733-f89b-4fc6-b7b0-d607d651831b
11b1055a-90c5-4290-80a9-7af59775adea
12703a93-0f13-4507-88b7-8d4b9dc91305
12e01b0c-cf7b-4b5d-8147-12c1a1bb7316
13439174-4cc4-4d33-9df5-78dd5439cbf0
13594705-5c51-4fb3-8ed9-a918df917d34
14617b42-f478-4e29-9777-74daa9921543
15f8ce00-ad14-45f9-abf4-df3373e21c48
1976c249-cd88-43ce-ab17-5067c4c191fb
1b4f86de-2908-4dcb-8cb8-bfd811548939
1b8bfe6c-16fd-415c-a447-7fe1e9644273
1b9ac05c-eb25-4931-8bc1-d248ce3232ad
1c07c8cb-e413-411d-a89c-df8a5eba5aa5
1e053375-aa20-4acb-8dd1-af4b17f6d940
20690c69-ae0d-4315-ab3d-dc28fa992ee4
213996aa-7dcd-4431-b65e-e1f138fe48c5
23d0b22b-d98e-45b3-bb7e-42306120f7a1
28248e3a-3ed9-4464-84fd-b48136070557
29732d41-650b-4931-9c85-beeb5445cc80
2e2d4339-c0d8-47ff-b9b0-d3ceae6f41c5
2ec13495-f550-4403-983d-e8062ea99764
30de73e4-a1e2-4e05-a25a-837967d4c1eb
319e3834-81f2-489a-b693-560e6000ab7f
353561c3-51c1-4626-b0af-ad106a744c02
35b24cc0-aa86-48eb-9c98-638d120e6214
365defab-21b0-4925-8c43-330de98575f9
36d3a1e7-9634-4320-aa5f-650de1b2c142
39058365-5996-4bb6-be27-a4da2be21b9b
3a6a2117-cc18-42f5-8642-8c602776bfac
3b2ac2ed-9a87-42c1-aaa5-8be0dcae3d2e
3c0e02b5-c41e-4d2a-af6d-105fa0471a85
3d1e594e-5b87-42fb-9eba-189c75aa31fd
3dede7b9-f3a6-4ad8-a0b1-f9e545cee066
3e64087d-648c-4c8b-b6b7-34cc89470544
40396a97-d56b-498a-968e-ce9452e65468
4216ce16-eaff-4f92-9484-c2675b0bdb3a
4219396c-4abb-4b97-a7c5-03cee4997e79
421f2385-dc28-4887-a245-4ae2ef0020a8
429beb9d-906b-4922-b690-311a5037c23b
42a58bea-9007-4d5d-a463-cb15da666410
4399bd0b-872c-4be0-8672-987130997fae
447594a2-64b5-42e3-8346-f65ef8a43e8d
455a02b1-a062-42d8-838b-3f948d48bac4
47c8cb1f-1c23-442b-b8f3-380ea1426e9a
4c34e5b8-2f07-40b1-82fd-87d0fcb5cef1
4c5c9bfb-1c64-4e7c-aafd-1c214843ee56
4e8ea37a-95c2-4181-842c-ce57198620bc
5122104f-09da-4460-a607-49ce7de4679f
516efd3f-bcb1-42fd-8f3f-427fb8d2695c
573cb1e1-a359-4e54-adab-b43504506295
575f4d18-3f44-46ae-bc36-df28a6f649b4
5a6897b8-9541-496d-bdf8-38cd3fd418ba
5b1c54c4-b235-46f3-b8cc-c6f25815ae34
5d1471ed-e25f-44b9-b77b-d60f710046ac
5d699761-1348-4651-b9b5-82bc7dbd382d
5de652cd-4e5e-46fe-90a0-f8591bb2d44b
5e721a01-e324-4897-865a-2a8b5dcaeee0
62f6a4ff-631f-4768-84a7-2e62d32409c1
631512de-270d-408f-bb6d-bf1bb2939b09
632a9614-e2d4-4a06-a716-a079ef84e442
63806c4c-5b7d-4728-adfb-512534d2ac3e
66aa13cc-7032-43ac-8f15-abf4a942ec6d
68e2afd0-1bf3-4c23-90ae-f17082fa2f55
6adeac55-6071-4668-83a9-826286b689c7
6b81e58e-9f52-4bbd-8a1e-69a15d92de77
6ecb64bc-5240-4817-b5e4-0bad84acf68b
7191d929-bc2d-44c4-a067-6c23724c3611
75e9efb4-3924-405d-b4d0-3aeeb2990641
797688e7-527a-4434-b587-eb2cb72d7200
7a3a83e5-9ff0-4ce0-b9d8-2f3d5a144be5
812ba40c-6124-459c-bb68-fcbf0044f1f4
849c081b-7b76-4658-8bc8-3f00d7345be8
84cdbb66-3564-4493-969b-f826d9864168
85c452ab-1b43-4fb3-bee0-0b2a9dc5145a
88a060c8-5669-41eb-811f-df5b63701768
89c6cd87-637b-414c-9615-de0d6beab124
8b244f82-abe6-4662-bf75-0e94cba6e66d
8c069b33-f6cd-4308-8b4f-15b33a76929d
8eda5dfa-9bc6-43a8-a5a1-df303ad940aa
8eeaad83-6a77-4122-94a9-b29ef8838af2
9034a7dc-d91e-4e99-a606-716a7d7f6e89
9079da1b-e4ee-459a-bb72-788a7b60cd40
90e25d52-61a7-4a3e-89fa-a8d875da913b
91096102-bf14-41d9-8fe6-be16ebf564c3
92f0cef1-ec28-4ea1-9623-37f0dc913af5
94fef879-744c-47b9-a711-dc875b44c736
95019845-606a-4ebd-9c57-79e3d6e80950
95370017-9eba-4dba-8923-03649a652dda
95ebdcd0-b440-4f69-8006-960b25921b89
99024e8d-c802-4b89-a89b-51b592db5b85
9c05ea3f-a830-444b-989c-0ae07b001443
9ecbc73e-7b9d-4c1c-868b-a608f8f58a3c
a1d031a8-228d-4277-801a-8f059cb0c194
a4d4b2c5-2686-43e9-a837-d9e322ca2a1c
a5a85163-ce80-49f2-a840-12b87cb86ea1
a96a103c-1679-4c95-86b7-b2de4737e195
aa6fe82c-628a-4cab-b983-f8aafe475d5a
ae860e9a-6130-4938-81e4-fd1efaed9dc6
aed709f3-9dd4-4d31-8948-a287aa5442bc
af0d4a86-095f-4d95-a8f5-1fbdb906a360
af446c42-e733-4c7d-bba5-ec17302c8af4
afed30ea-7c05-4c6c-b1d2-f655f9f6a02f
b61989ed-c12d-43fa-9240-da120f2651ce
b732eff2-432a-4cb5-8da3-452d4a8541b6
b79d66d3-35d2-480f-9005-aeda91a92fe2
b8cd6398-6672-4538-9eb0-98f0d366380f
ba83ce21-151b-4265-b5af-adece9eb27e9
bb195c02-be71-4329-8b9c-7f1081a85994
bb4b8533-46d7-4c5b-8ac2-645c6af2dc44
bc486787-f1b3-42b7-837f-23d017424d92
bfaa43df-d070-4e26-84bf-327d55321d25
c1470b06-cd6a-4f93-800a-b767db4e11ef
c1730cdb-2519-481d-b1f5-2d39b8653b22
c1bda07d-6352-4c58-a6e7-45bfa50244f5
c1e79d99-33fc-4533-9626-3e53d0b43102
c41ae39a-34e0-412e-8efe-e969d7055dbc
c56f4794-885e-4138-a442-d3196b69e9a8
c6bf3fac-662b-4324-bb17-34cd68377518
c73fe181-514e-447d-9876-3ec4c42543ab
c80974d5-4c51-43ec-aab6-46cac6d72bc6
c8b2fae3-c6ac-4ed2-ab55-9f95c5c66c42
ca5cfda1-2ed8-44e4-9dca-182374323181
cbe297ca-920c-4246-a04c-5e0b30bfc27b
ccb33486-9b22-41b8-adb3-9ae825f3a8b3
cd8c71a1-c4aa-4a9c-99a3-69c41d83477e
cdb76d98-41e6-4137-b85b-4c1c816b664d
cfaf72c3-1af8-40e8-b8d1-09e112cf95ba
d19a7510-07c8-47a3-9d16-5f082ec84e93
d3fb819a-95dc-40f3-856e-99399b758009
d48791b6-a96d-4625-8176-5d7cc52413a7
d54f09af-14d9-47d1-a2c4-3f6f905b8daf
df804358-9355-4a63-8fe3-6a99dd796148
e052eca9-83d2-4773-b587-1593bea024c7
e4057193-d3ab-4766-9129-6ab55b412905
e669c10c-2bf7-4d93-b58c-4f948eb23572
ed634aaa-fd3d-4614-9b87-31c780b8feaf
ee1198a1-5d3c-438b-98de-781c1cf53659
eea1a953-04e0-4527-9497-d65300ac5ce1
f0422609-a3e6-49b4-baef-04ebad18d207
f7d04a96-363d-4816-8a5f-82dad42339dd
f82fae10-53d2-447b-90f9-bd4971aba12f
fc940f39-f83e-4fb1-b4ed-cb1adb03b66b
feb0c080-ec12-44b6-9ece-3f129e8a18a6
feed4397-743a-4d75-b520-b17bd04cf06f
```

### 歷史 article IDs（22）

```text
040456ae-7743-479c-b76f-605e41916b8d
1ca13f76-72f1-4545-9812-7cb0d807a296
35919977-5fb0-4f73-9195-fce44d61bc7c
4b4684f5-8368-4651-8009-7d85af075819
53ffa363-1163-4342-97e1-776c85548a9f
54398225-f709-480f-9516-3213cbb5464f
61f270e2-d5e2-48d4-a9a6-7688b57da362
6a8a37a1-9b88-4455-b585-8a6a62e1246c
6c50b83e-1ed3-4001-85dc-f3928290e8c1
737784b7-7116-4fb3-adec-ea08e3642695
7b8149bc-cb49-4e6d-b475-5fd867287e81
8e0556f5-cc4c-4285-ba5c-b7fcf90a2220
9fc67d07-474b-49d9-94e3-28a7296fb994
a1fc621d-672b-412b-9669-be7e044d2dde
b5ebc1f3-f9b2-47e6-abbd-0c7c2bc8e81f
b99921df-6e18-42c5-abe7-bed798f622af
ce5228a7-2246-46ec-a9dd-d9851ab1a2d5
d779a73c-eca1-4bbe-9db5-e8ef3a0ef00f
de56543f-565d-422b-b30f-80dd7472f02b
df8930b2-75f1-4a1a-833f-0e01a314777c
eca50a01-fb8a-4882-9f66-5f7c310eb366
f76afad6-0918-4b7b-a266-0d064fdeffdc
```

### 歷史 video IDs（5）

```text
45f64818-79b6-439d-875b-3fcee3916cd7
84e9ab65-2513-413f-b7a0-25baa0dc39fe
d3ea879f-3a5b-4afe-955a-b75cdbaa440a
d7ae0dd6-c7e7-4246-a4d8-4985059c00df
f2672744-d68c-4b7e-94ab-f0ded7a62edc
```

本票保持 open、未認領；建票只恢復待辦，不釋出原分支 owner 或授權接管現有工作目錄。續作時依 task-board 核對認領、main 與本票 scope；正式站寫入、合併／部署與付費生成維持各自原有授權。

本票 scope 僅含這份對帳紀錄：以唯讀調查及可查核結論完成交接。需要產品、資料或原工作目錄修改時另開並認領窄 scope 票，不以本票直接處置。
