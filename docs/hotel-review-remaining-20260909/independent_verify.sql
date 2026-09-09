-- Anonymous SQL diagnostics for hotel-review-remaining-20260909.
-- v2: AdminAuditLog.metadata_json is PostgreSQL JSON, not JSONB. Normalize
-- before JSON operators/comparisons; text extraction still returns TEXT.
-- Original failed preflight SQL/output must be retained separately.
-- Run this SAME file before/after/replay, retaining all output. Required psql vars:
-- phase=before|after|after-replay; expected_count=final manifest decisions (1..125);
-- expected_approved=actual successful option reviews (0..105);
-- expected_edits=successful new-URL option edits (0..expected_approved);
-- scope_json=JSON array of ONLY {"kind":"option|product","id":"UUID"} from manifest.
-- Before apply, expected outcomes may be the plan; after apply use actual receipts.
-- No URLs, evidence, credentials, emails, ciphertext, or message bodies are printed.
-- All product changes are forbidden by THIS independent verification contract.
-- Products count 60; options count 360; initial approved membership is pinned,
-- not selected by mutable current status: 40 products + 255 options = 295.
-- Fingerprints are full-row comparison MD5s, NOT authorization or operator SHA.
-- Compare protected_groups / historical audit hashes to the before output.
\set ON_ERROR_STOP on
\if :{?phase}
\else
SELECT 1 / 0 AS missing_phase;
\endif
\if :{?expected_count}
\else
SELECT 1 / 0 AS missing_expected_count;
\endif
\if :{?expected_approved}
\else
SELECT 1 / 0 AS missing_expected_approved;
\endif
\if :{?expected_edits}
\else
SELECT 1 / 0 AS missing_expected_edits;
\endif
\if :{?scope_json}
\else
SELECT 1 / 0 AS missing_scope_json;
\endif
\set baseline_at '2026-09-08 21:18:03.737914+00:00'
\set baseline_hash 'c938d83913645ac6a7651eca0e705621b33b40bb235905392c54917492bdb03d'
\set tag 'hotel-review-remaining-20260909'
\set root_id '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'
\set approved_product_ids '0f922904-6306-42ad-900e-bbb2402f4deb,145e7bbb-df82-4bf9-8290-f5be7f9161a9,177996ee-887e-48b8-9ade-240e47675438,2263bc8e-be0a-4163-b2ad-6f3a7c049983,287f69b8-95f4-4e05-817a-e13b4d5310b4,29a7720d-11c2-46ae-abe2-001cd69ac301,32e00e1e-5976-46dd-90f2-bda4c44c1b2c,352d2cf2-2a1b-48a4-ad94-3bfaa1a88303,3a08719d-5a3a-4a87-8df4-f81da9a16c0c,3d531f0f-1a58-4bd7-9311-22125f489742,535688c6-4370-4550-9a66-d35c4f907eef,6431e10f-dde0-471d-ab5f-0dfbefcda2f6,68646c86-2aed-4bd6-a453-29450ab50d6c,6b6f2564-93f4-4aff-aa97-bfe34d456cad,6dde791e-5b13-450f-b743-0e66411af7da,70eec2a6-582f-4c9d-9414-0eec588e85fd,85bf59b8-1c01-4b0d-aa7b-138129b615b2,87ac9f12-2b00-48b1-897e-bf66c5aeb616,89873ccf-5a45-467d-b2c9-dd32c2b6a0df,90cc1cf8-30bd-4498-be0c-56f8fd9f5ee6,911db160-e332-41c6-95f6-3fa89d9a711d,940ceac6-8726-4be9-b00f-f5809dbc0f0b,98c3b936-3470-45b3-b0dc-50353830f2df,a5336bb9-321b-40a0-9d87-cf9d1e6d9d9b,a725fc3d-60bc-4f4b-9ca5-00a87ee6af6a,ad6930f9-64e2-4298-b90f-ad24fae50060,b1afc011-53e2-4cab-b277-1ad8ffbc0af9,b79582da-592f-4a33-aa22-6457cf815094,c70a6326-4302-4394-afb4-ff7a018272a5,c74448b6-1fa7-426e-b5af-17b7d0953382,c934905c-8857-4dfc-963e-9d19e13cd16e,ca55d588-a5dd-4dd9-9c84-72c5e687c48f,e5a8c571-961a-4dea-b36f-43624c85db82,e94492db-9582-4457-b47f-4b44f3112fbb,ee355d59-44c5-478d-a3eb-2c9053febe24,ef29cc9a-331d-4e8f-9fd0-ea30cdcecc5d,f4dc5d28-5de4-4e81-b79f-f8471f1e4863,f73ce087-d361-4f74-8bac-45ed71d5c1ce,fc4ab21a-29df-41c3-acd7-961d3a8fbdd2,fdf201c6-8838-41bd-a9ef-5bdd8f69ad24'
\set approved_option_ids '003c2d18-bbb7-4626-8dab-523f3636869e,02673f9c-4e1c-4aca-9a87-9da1cfcd9f1c,0340e85e-42c7-45f7-91f8-178de9597fd5,037243cc-e506-4ec7-a8d1-43abb828f21f,03d141b8-18bb-4eb8-b04f-60b82c47a25d,03df0967-cada-44aa-9c56-d644ea48716e,04b51b83-700d-43ae-b693-6c892151cd0a,06402d25-6a6a-4f26-8aa7-e06b1234a880,07330eec-282a-4f8c-8ecc-c173fb77dd0c,09eae396-5314-4592-a11e-c257a78b8992,09f6e61b-ff11-4907-9fbc-1d97462fd663,0a7ff9de-a455-4e57-9c90-c3867329bcbf,0ab5ef69-1983-4bd3-a3f5-4244222bcda6,0ae874c3-39bd-4d50-a99c-972b8a5ae81e,0b5fdf65-ddc1-4f09-aeb5-b217e99eaee1,0b8d8e3e-36a3-4c0b-80fd-d23f527ad345,0cdc165e-5b3b-405c-b549-0e5f01ef5fd6,0fd5478c-78a3-4cfb-be12-1c3808c21ebc,10508f3b-79c6-458e-9a45-297496c229b5,12a4900e-2624-4932-a785-0ffa45dcdb02,13054029-6360-4277-8450-7600d6024703,14fa1772-1050-41d1-b40d-87eb004bd254,1715489e-3d34-4009-bf03-3e464c00e6d5,1756e8bb-d91e-42ea-8d0a-5dbbab725ecf,180844c8-c83e-4aa3-90a5-7a6d17f358a2,18ca5278-acf4-41db-967f-8cea1b247a71,1a252781-62f1-4ce1-b216-694bc3cc63a5,1acb421d-8859-43b2-a31d-a0e8a54dc928,1acd2432-987d-4a9b-ba97-33a8e435e892,1bc2ccde-a724-4077-a7cd-9121959ba655,1be7ac66-3205-4cc5-81af-38d9fbbd00ba,1cf185d2-e015-41ac-88ca-00ee55fbcf03,1f942ff0-4d9a-45ca-ae78-9f5dd12ae455,1fb5ce93-a359-4e62-9144-2b1cc15b89a2,224dffcd-9fb9-4371-aa50-97189d2f25e8,22a1645e-4fb3-4eae-a91b-6c6a01b87cd2,2447ca52-01ed-5edf-9b12-1eca6450c7ab,25c1b1d8-1b5d-4a1e-9561-646c991600eb,2712c97b-ad7a-44e4-a8ec-b6ec94d4c5ae,279c9958-acf4-5ae4-aa38-df383a7c7ca3,27eb102d-cb4c-50b6-9976-57a87cfb0d1d,29656832-a29f-465c-aaf8-cae4c339613a,2997aa94-f717-469e-90e8-91e6238375c4,2af4cdf3-c4b4-5cc0-a6c3-14069d54e9bb,2c82339b-0a07-4f4c-b083-b4a38acaede9,2d142178-60cb-404c-8bae-63aa938dbf74,2d90f696-3da9-4572-99e3-a659b41e1017,2e3ad995-c4ff-44f2-9e1b-59a59d3e93a2,2ebbbe05-04a9-4b14-8747-79a4c3ca0de9,2fd75ef7-d8fe-4bea-a682-b2db24ad587e,2ff150eb-5bdd-4b0f-9c60-9696f98d4a55,3027e80b-fc5d-4bc5-97fd-9f21e6f3cdcd,31b17c88-f69b-4671-8b5a-68c99dd9bf62,325269df-e6e3-47e1-91e3-c4ae08f8453c,3266382c-cadf-4df4-954a-5b6735cd952c,32947818-bbb6-4bad-beac-18465e8fb0b4,32981540-acd2-48d6-9f37-450e2e18eb34,33cd1c97-5f2d-44c1-b8e6-4778a9e70b21,3678bebc-9166-4830-b846-c707f940c8e9,37077846-829f-4afc-bfe2-01c94acc6ac1,377a5b5f-df98-422c-8138-9103783e2db9,3808a373-0fe9-4054-8c26-9aff87cb979a,3a3fc414-1e46-426f-9cd5-4e23153cbba6,3afd61bc-e374-46f9-9f87-c4cf49569fa4,3b4e7e4c-a99d-4788-95e3-bcab65b339b6,3ba7e8b5-6667-43aa-ad73-23e40c05d121,3c15c159-2e53-4a78-846b-de63d06dfa0c,3c16bfa9-a0a4-4609-8ef2-127563d46ab5,3d48221c-b5a4-4800-a076-02cf10a364a3,3d4a2875-de67-4e41-86d2-3b7fcd819da9,3e4d561c-d0c9-4a14-8c22-f08635fc85f5,4045f37e-444a-4785-88b1-e6cdcd69afa9,4057e9ce-b353-437a-b2c8-3097222c8fb4,406e1594-5de0-4a01-965b-0fd7cbb29caa,40df8e4f-d119-4a6c-889b-dbcaa43cf282,41fba9ac-0423-495d-be06-ec943031d84f,43721237-040b-47e2-b6ed-446dd4030df0,438d060f-fa69-4fdd-b8f8-2c635c345a84,442f45ca-8b5a-483c-857f-2100975ea741,44d41899-9bb9-499f-a5d1-7a4676a2e499,45416cf8-bac4-4b30-83dd-f450ad7773ff,463f2c0a-12e5-46e8-b3d1-6e1c81c8bfb2,467a0157-2d62-4355-8513-904c1242ee16,4684d23b-a65b-409c-934f-1ca66bfd78bb,46f7993d-4af3-4659-b1f7-6e32b34d02d3,481be31b-86ce-4068-b464-0087353c21ff,4a67b50a-4a40-4a55-a26f-8e7b592cd8ee,4adab3dc-8cd4-4998-ba0c-f88152b2242a,4c06ddea-f526-4d5a-811a-18fa679db91b,4c538ceb-18ef-4d49-839f-6cb82322de83,4c7a6720-54d0-47ad-a9a3-3b14af04b8f3,51fc28c7-db15-4cc3-aaec-67be3261b968,53811838-0547-4b46-8ef4-6c5538853ca9,54c431e4-5578-411d-82a2-9e40923361b8,55853130-59d2-49e3-a064-0201f8df804a,55a8962a-805f-4b6f-9f14-43c15089f869,56327f30-feb0-4992-8fad-d91798b960c6,579764ea-26a3-415a-89eb-4a0e50c582b2,58ba0ac4-2fb7-4b87-bbf6-472c0df03bad,5a23b490-18ed-465f-aa4e-3be06089b335,5c01831e-2e59-4ee4-959f-44180f2d8071,5c926f67-f6ba-4d9d-9501-5f3bc037a68d,5cf89cd2-b9fd-4d10-aa2d-de2ca25a17f7,5db0b61d-90fa-4870-93a8-674ce72ec2a8,60ec6688-75a6-4782-a2bd-1a93660b1a17,644bd3d2-12ba-4ee7-9061-2ee0fbd629a6,648c4341-b60e-4780-a463-6733de26a8ba,661cdc12-9cb7-4c1e-99af-a2a28bb5232f,68411f9a-fc8b-4132-b5fb-6f0221f711fa,68d500d9-94f7-45b5-8c05-da04b475bf57,692c3ff2-8f47-40a7-b57e-e39ae0661d47,6957bfea-4982-459e-b71a-f4351a107b78,6982de70-7703-4e3a-82cd-1b40e26dda97,69d8b040-e631-46e9-aeb0-00b04367d898,6a2411a7-372e-44eb-8a67-458917da05f4,6af4e94a-7e49-4bf7-80d5-ef1897f0c4bb,6cf28949-c58b-4088-994c-880014a00c89,6d7b7332-e87a-4e25-b405-184d9b4d8293,711badb9-7b4b-4602-92d7-191231d0287b,7380ce11-d500-4263-a309-f864e58162d5,741bbf90-898a-42d0-86c2-ce5afd5001cb,74c844f7-3624-4e26-978d-cb80d72f8556,76646f09-1235-4c63-a5e2-3baeba09fd7c,76b12ee7-f02f-463b-9729-122818cb3dc9,771bbcbd-fffb-47b7-8389-490d121bb287,777a0f1d-f066-40f3-82ad-46f0f561ff67,77d57d1e-33ce-40b2-a221-7f6c16194cbe,78b718b2-ea44-47cf-adeb-8c10feee6ff4,78e00bad-b47c-5fba-ad7f-42fed82e4749,7c5f1310-9fad-469d-9100-ec87500fd643,7d5f839c-2fcb-4021-b745-eacdb5e3378a,7dc9e9eb-a3e5-4172-a8aa-b98c1fd104a8,8139b739-b19d-4769-b336-c131419b8ffb,837e69b7-aa5e-477f-b380-90b315d179fd,8399554e-0097-4538-94ad-0d66f0e7f695,847b20f2-99fd-4a02-914c-4148ee4feb45,8726d3be-4304-4abd-9c2c-1ff8736f8fe7,894a022a-0bfb-4976-92ce-562df3f750d7,896be894-67ca-4a94-972b-c17446810c27,897df2fc-6ca6-4987-8aad-c4230b546d8d,89c11cf5-0ed9-48f1-8496-90a7972daa58,8d5f3a67-29be-4c54-8095-3f9ce514fed7,8db458f5-78eb-4a43-978a-2793bafe3bde,90b7a1de-f2e1-4390-afe9-b90784758bea,935bbce0-f79f-425b-be5d-9365039e02c9,93d7012c-2dd4-4a15-af28-b60d91348825,94208dea-57d0-5426-a1be-e2931ce5f181,94b16b18-a2ac-44bd-9a20-dffcd47afa88,95b9862e-7f7e-4f82-b37a-35e36618d687,96260701-8215-49bb-87dd-1478ebdfe6c2,97063551-145a-4836-bd07-f61ac2720c39,98c4d502-9301-4c8c-8c89-90819af6b2c9,994d3ce1-1ed1-474e-9349-f6197ce5aafa,9975c9f3-b98d-44f4-9b89-16ee4a13f162,9c020165-3328-4e31-af2b-90dbef98afef,9c6a9603-2acc-470a-b0bb-5ceb1b525548,9e5078c4-1283-43b3-b236-d721e01bbe36,9edbde9d-913a-4ce8-a81f-b81d29934943,9f57d1ce-ed2a-4b28-8b00-a62a2cc9c224,a1029789-ab2d-4f7c-93ef-42c24bf30219,a28b052e-ca1d-4420-83f2-4b8e237049cd,a32ac29d-d586-4e91-bbb8-f7c6fa0498db,a40752ba-b5bc-498a-9700-dc42b9799a02,a414a1fb-63ba-4e38-aa6c-370fdab74060,a4730a7d-9bc9-48f3-ae30-6c6f4253565f,a4d22691-5824-449d-995f-579fda742a0e,a5be3edd-5fa6-40fe-87ff-21942f8c11db,a659fd94-8cc5-4d54-98c6-2099c30891fc,a6a6a118-83a2-438b-aae3-2c3bd3afab0a,a789b1c7-46c7-42a2-916d-099bad5f18de,a8f294f3-a944-4bd4-a34b-ab0ef59fe59e,a93430c5-36ad-4023-ab80-f674d0325e56,b0c20080-76ad-4b1b-9a4d-657654387ecd,b2abb31a-1a7f-423c-a88b-c550badce271,b2eee839-6ba2-42a1-8dad-c74b6244f7a6,b3c9743c-774b-485b-aa01-61024e0d32c6,b447d6e8-a5ce-4a70-8e3f-bc4bac16c995,b5fa82ed-896c-487e-99ec-e4e36df8496f,b625a281-5916-4a1f-bf1b-9a5c589bb309,b68d4d8c-7647-4001-9883-b4df9e7c6d40,b712edcc-85f8-4456-b2eb-8e1ec2d57de1,b78336ce-4066-443e-978f-caa5a90c5028,ba807e07-e30a-4a9a-bad2-c2a4a3002b98,bf0203d2-ae5c-4085-8ab1-2be98047fd75,bfa28a04-e3e0-4bf2-a81e-80dd0f5c3de0,c6902909-c521-4ef4-9e1d-0c8e9a904d02,c6f9ae48-0fae-451b-a930-f43feddac5d7,c75606de-1030-4474-bd61-36ce08782962,c9f5a980-3e11-4624-8117-2686f528a6b0,ca8807cf-8bf2-4cda-a80e-2beafae1805a,ca99705a-b740-4dd7-a3d3-b33503dfd9d6,cc0d8398-1d6a-4f10-89de-448c7694ce20,cdfbf190-becf-4103-a74a-3b107ebbccb4,ce37fe1a-e52f-4177-8efb-59790fe662e8,cef042b9-5f49-4199-ac83-3f8f28e4f918,cffed808-67e9-4b29-b7dd-343a1c2f9f36,d1e4951c-6fa9-41e8-8a1b-beaa4a7eb0c5,d2271918-ecd6-478f-ab2c-3e4a6d576a1a,d268b025-3d88-4fa5-8941-8392d4363a64,d269ceff-0dcd-43bf-915c-c2f033c26a5e,d280e943-ca49-485d-a4b9-8f90462a0845,d2c5d850-2bf0-4d47-9fd8-28fff108b924,d46b0528-6178-4753-812c-0bb684eb4eae,d47ec0f3-d6fd-4124-9a59-ef4efdff6980,d57fe330-7b68-4fe6-8fac-11ca336bfc69,d5c927bb-4d10-4941-96cb-bf7689f59db2,d5dddc98-3941-493c-85a9-3b63855628cc,d677d8f6-a084-4219-b590-cc42f98158c6,d78a4f4f-66e0-4ff4-b695-ab9742bf96ae,d79a7fff-b43f-4ec5-a2ad-a7855ff335ff,d9c27b3b-b4b0-4147-b35d-b99a2b263ae9,db4ecb6f-c90b-4db7-88a1-5906717b609c,dc1e4e17-0dc5-4b74-b01b-84ec91a1a9df,dd3d94bf-67d1-4679-a092-06d676a1f21e,de780f6f-b863-490a-98f2-4b481da601dd,deb86d4e-9351-4762-838e-32cfd5485e13,df31affa-0971-4330-90a1-8a918e71db6c,e0d9e872-550f-435f-8496-10c2c3826107,e13237ea-4640-47fb-8b4c-8cf40606e99d,e2960e7e-635d-4c2e-8480-567c5577a572,e2ce0d9d-687f-43eb-b0d6-b1774f58f474,e3d07ec6-fea5-4cd3-9bde-d6edc830f00a,e4b7fedd-848d-4972-9660-6b02364dd5ae,e6a8cc92-9899-4d2d-a9fd-521909b61be6,e74e0fa5-bd96-467d-80bd-42dc7ac10224,e7c85c8a-07e5-49dd-8b21-420ebcbad47a,e8603a34-3bcc-4262-be1e-19533c94899f,e8a1d3d3-dde2-4d53-815d-b789f34f06fa,e9fe4cc7-c7fd-4e53-8634-44afdb2c7ef8,ea3b7303-f0c0-4677-b38a-37431d3a8d7b,ea56b3b2-85ae-4ed5-a6a8-57983d9a2509,ea7626cd-3640-4e07-bdf8-0d6e19dc1b60,eb52fcf2-8c30-4291-9dd7-4695fd0e5672,ec50cedf-c5bb-4ba1-bc1a-51038eebe2c6,ecb895e9-c8da-4883-b489-6a2ded17ebfb,ed7ed57b-d83e-4535-be02-baa9e293bef7,ed9a0781-1db1-4b89-a759-9c1fb5594cc3,edc6dcfc-7b6a-4c91-b988-738cf943a40b,eef268cc-63ed-44cc-a05d-f563153796b5,f0f56103-0b4b-4e56-8c44-5cdcee9f0b22,f1250e32-e4be-456c-971b-48b0fa41e476,f16574e7-801b-4a2e-8495-5981655b7ff6,f3ed1561-3046-4647-8c90-0ab634d5c7e2,f41083d2-b516-472c-bd51-0277849ca79c,f448cf9a-fe52-499b-81c8-7114f014cf11,f6adfaca-de6e-45e8-a83f-894e6c4cfc39,f80f116e-6c0f-4956-843d-a359161c2c86,f99f1717-b792-4c1c-ae4b-362e5f27677e,fa78cab4-8f24-40d9-a563-5dc49e58b5b2,facc53e1-9162-4b82-8a4a-35582d69af3e,fbff5aa0-6b40-48dd-a4ce-727ae37c9fee,fce8c987-64f5-403d-ab85-568a3162daa8,fd09af44-8571-44ea-a34e-5f6b3c4be9f6,fe51f041-3f5e-433f-a87c-a2b4708d6f37,fef9bfb7-5911-4f0b-a2b4-4d1095659026'
\set baseline_pending '[{"kind":"product","id":"028e3657-62f8-4636-9033-ee80ad8fc7f1","version":1,"status":"pending"},{"kind":"product","id":"0a47515c-1b5a-4750-9790-1b7969048e30","version":1,"status":"pending"},{"kind":"product","id":"1be1bb97-fbc4-4d9b-b2b9-3744ee473953","version":1,"status":"pending"},{"kind":"product","id":"1e9c0de8-e648-44c0-a4c4-0fb175893d7e","version":1,"status":"pending"},{"kind":"product","id":"434dec94-7909-4556-863a-bee68788b642","version":1,"status":"pending"},{"kind":"product","id":"4938181e-0007-4143-aa0c-4b5ed44f4f8b","version":1,"status":"pending"},{"kind":"product","id":"50f2d47d-24fe-4b07-85a2-3e1c7671e452","version":1,"status":"pending"},{"kind":"product","id":"58d5fd90-1c15-4ff9-b1f7-63c1b3d08494","version":1,"status":"pending"},{"kind":"product","id":"6e824f93-a049-4a32-9df4-fe17dc4d3974","version":1,"status":"pending"},{"kind":"product","id":"71374dce-0786-413b-aafd-b63c7d9a3786","version":1,"status":"pending"},{"kind":"product","id":"758907f4-4870-421e-bf6c-6243cdcc30c4","version":1,"status":"pending"},{"kind":"product","id":"7ee4a065-04fa-4b46-a436-b84ff48528ca","version":1,"status":"pending"},{"kind":"product","id":"7f1b1d18-215a-4ae8-939b-c106ce224d6f","version":1,"status":"pending"},{"kind":"product","id":"9cd0788a-a853-4755-bbd4-3e6f64ac0c57","version":1,"status":"pending"},{"kind":"product","id":"a124dc1e-7f75-44ff-b12d-080da031b3b9","version":1,"status":"pending"},{"kind":"product","id":"ab8d3a45-10b9-477d-a523-07fc7e2036db","version":1,"status":"pending"},{"kind":"product","id":"c1a9d2e5-52ef-418c-aa6b-8a1e9ac1e51f","version":1,"status":"pending"},{"kind":"product","id":"cd720a2b-1db8-4970-9c8f-ddffd505f963","version":1,"status":"pending"},{"kind":"product","id":"e4334b4e-be69-4a48-8d8b-57186d9244c1","version":1,"status":"pending"},{"kind":"product","id":"ed85936a-f890-4a82-80b5-dfdfa63c971a","version":1,"status":"pending"},{"kind":"option","id":"00307d02-975e-4b2f-8843-df7000cd7c50","version":1,"status":"pending","url_null":true},{"kind":"option","id":"03883bc5-7553-4fd5-a021-9149370cf3a2","version":1,"status":"pending","url_null":true},{"kind":"option","id":"050877e8-6f0d-4ee1-81b6-2bcd9d21ebc7","version":1,"status":"pending","url_null":true},{"kind":"option","id":"058bc0c8-a0df-4ed9-9855-cb088ae76288","version":2,"status":"pending","url_null":false},{"kind":"option","id":"08f0183c-6d74-493d-8402-9a0eb4d76243","version":1,"status":"pending","url_null":true},{"kind":"option","id":"12371d73-601e-4351-b472-1c0fc68be7ad","version":1,"status":"pending","url_null":true},{"kind":"option","id":"14983e9d-dcdb-4d43-af50-399c51b1c644","version":1,"status":"pending","url_null":true},{"kind":"option","id":"159bc0b2-5bc7-481e-ba8f-b79bd121e76a","version":1,"status":"pending","url_null":true},{"kind":"option","id":"1765a844-3e15-40ae-af45-033bd3767680","version":1,"status":"pending","url_null":true},{"kind":"option","id":"1a23cbe8-1cd1-4a1d-932a-f3955f567ee4","version":1,"status":"pending","url_null":true},{"kind":"option","id":"1b42c2de-969e-43bf-9dc2-25c824d938d6","version":1,"status":"pending","url_null":true},{"kind":"option","id":"1eb77c39-ad06-4348-8a81-b6937bd1de5d","version":1,"status":"pending","url_null":true},{"kind":"option","id":"2025853a-e016-4b35-b9c1-f44b03c4a0d7","version":1,"status":"pending","url_null":true},{"kind":"option","id":"2156ce3c-3c4c-4822-a307-098bf4e2c06d","version":1,"status":"pending","url_null":true},{"kind":"option","id":"2279dc5a-7f1f-41b2-ad31-6326ebb24bd9","version":1,"status":"pending","url_null":true},{"kind":"option","id":"2489b4c4-c513-4cef-be6d-b803ab8b7ffb","version":1,"status":"pending","url_null":true},{"kind":"option","id":"298dd0c5-9786-45b4-b5a5-db049f0a297f","version":1,"status":"pending","url_null":true},{"kind":"option","id":"2c41cd84-0813-42cf-8a54-003bc6f0cff4","version":1,"status":"pending","url_null":true},{"kind":"option","id":"305f394d-7963-4d03-af74-406ff496a7cf","version":1,"status":"pending","url_null":true},{"kind":"option","id":"35b15018-b498-4135-81b2-946d9777b785","version":1,"status":"pending","url_null":true},{"kind":"option","id":"3d10dc70-0cc8-4f5a-9206-f6c1f6a95317","version":1,"status":"pending","url_null":true},{"kind":"option","id":"4196aaf9-59f9-43eb-b72d-655946344d96","version":1,"status":"pending","url_null":true},{"kind":"option","id":"42a3558d-bb99-4312-abe8-e06e080c09a3","version":1,"status":"pending","url_null":true},{"kind":"option","id":"469f672a-4230-43e1-95c7-75cfc759a3ee","version":1,"status":"pending","url_null":true},{"kind":"option","id":"47832850-bc24-42f7-a0c2-5abf24dd8200","version":1,"status":"pending","url_null":true},{"kind":"option","id":"494e0fb1-0812-4914-82b8-829cedbdf1c0","version":1,"status":"pending","url_null":true},{"kind":"option","id":"4d2c8a10-e5d1-4334-8bd4-6f4e05c3dbe8","version":1,"status":"pending","url_null":true},{"kind":"option","id":"4e1ee548-4abd-47ec-b971-9ec2a700e1b9","version":1,"status":"pending","url_null":true},{"kind":"option","id":"4ed42b59-20e6-4426-8bd4-941ed18e932b","version":1,"status":"pending","url_null":true},{"kind":"option","id":"504edda5-ffc2-4888-93be-37380242386c","version":1,"status":"pending","url_null":true},{"kind":"option","id":"52778715-5952-4ca9-9136-eadce58933c0","version":1,"status":"pending","url_null":true},{"kind":"option","id":"52c1c7c2-9660-459b-94a9-fe3a0b58a3d9","version":1,"status":"pending","url_null":true},{"kind":"option","id":"545a7eaf-00c9-45a0-b6c2-c1622c210260","version":1,"status":"pending","url_null":true},{"kind":"option","id":"5d6e1f99-b13a-44e6-8f7d-c7f1035f4058","version":1,"status":"pending","url_null":true},{"kind":"option","id":"5d76bb7d-4b7f-4d11-bad8-f5b1fac90cda","version":1,"status":"pending","url_null":true},{"kind":"option","id":"5e832165-9b06-45f3-88c3-ed4c991ea9ff","version":1,"status":"pending","url_null":true},{"kind":"option","id":"64ee9069-11b6-410f-9143-c48f5ff6155b","version":1,"status":"pending","url_null":true},{"kind":"option","id":"65ce14ea-44c2-4c3e-b388-a2c818b1b5df","version":1,"status":"pending","url_null":true},{"kind":"option","id":"67c82463-cb0c-4ce8-b53c-3f11a7cffad3","version":1,"status":"pending","url_null":true},{"kind":"option","id":"6ddd5137-9ffe-4649-b6d5-cb33389b3cf8","version":1,"status":"pending","url_null":true},{"kind":"option","id":"6f5246ab-96fd-4dfc-aa25-f4cf8ca308a8","version":1,"status":"pending","url_null":true},{"kind":"option","id":"709186f5-c0bf-413b-ac21-d9a8ac6121a0","version":1,"status":"pending","url_null":true},{"kind":"option","id":"7189583a-865d-4ec6-a4f0-3adcab3b1132","version":1,"status":"pending","url_null":true},{"kind":"option","id":"72b94170-a4ad-4604-910d-b1220e1dc541","version":1,"status":"pending","url_null":true},{"kind":"option","id":"78166961-ffd7-47c0-9852-7eee48f03b91","version":1,"status":"pending","url_null":true},{"kind":"option","id":"7985f2ef-b3e8-48e9-9a85-a844adbc4905","version":1,"status":"pending","url_null":true},{"kind":"option","id":"7c0adcfd-3f12-47f4-ac34-9cccd9b940d4","version":1,"status":"pending","url_null":true},{"kind":"option","id":"7c8322b4-cc11-4ee2-bf74-69a1886c7410","version":1,"status":"pending","url_null":true},{"kind":"option","id":"7c9eae8d-992c-465e-b635-1fd64262193c","version":2,"status":"pending","url_null":false},{"kind":"option","id":"823126b6-3621-43fb-8a9f-40a5568bb3f9","version":1,"status":"pending","url_null":true},{"kind":"option","id":"83554f6b-a045-4a89-ab61-27f077e42d58","version":1,"status":"pending","url_null":true},{"kind":"option","id":"853b4a8c-35fd-4585-9ed7-29a8ed1a1e55","version":1,"status":"pending","url_null":true},{"kind":"option","id":"87068fe2-4ced-4dba-89bb-160f9bb7c9c0","version":1,"status":"pending","url_null":true},{"kind":"option","id":"89755631-5f45-4f15-a404-02312ac1564f","version":1,"status":"pending","url_null":true},{"kind":"option","id":"8c736856-6c85-4bf1-806b-cce55e6e97f8","version":1,"status":"pending","url_null":false},{"kind":"option","id":"8d3953f1-90db-47e9-a06e-aee655c0afad","version":1,"status":"pending","url_null":true},{"kind":"option","id":"90621e6c-4556-40a6-b08e-6b81b467dfbb","version":1,"status":"pending","url_null":true},{"kind":"option","id":"911e0a24-6dd1-4432-adbd-debfbbb77c52","version":1,"status":"pending","url_null":true},{"kind":"option","id":"93d82747-9209-4d79-88e8-ed51e280e934","version":1,"status":"pending","url_null":true},{"kind":"option","id":"952a280b-b3d0-465a-a141-8390783df7e6","version":1,"status":"pending","url_null":true},{"kind":"option","id":"9901400f-29ec-46a9-86d9-a60672839f87","version":1,"status":"pending","url_null":true},{"kind":"option","id":"9ef5afdd-65d5-4c19-b650-bed9de4b75ae","version":1,"status":"pending","url_null":true},{"kind":"option","id":"9ff42733-c0b7-4978-94c8-5c43b49ac625","version":1,"status":"pending","url_null":true},{"kind":"option","id":"a0d899c1-986e-4713-bfec-51f8dec84c90","version":1,"status":"pending","url_null":false},{"kind":"option","id":"a3c846cd-b509-4dbe-a4eb-f19b388e6268","version":1,"status":"pending","url_null":true},{"kind":"option","id":"a5ec8292-a714-45e6-8360-09914bb787a6","version":1,"status":"pending","url_null":true},{"kind":"option","id":"a6c60862-2199-486d-bc3c-5b77e4decf12","version":1,"status":"pending","url_null":true},{"kind":"option","id":"a767702a-1e93-49c2-ab9f-e4b51e47c43d","version":1,"status":"pending","url_null":false},{"kind":"option","id":"b4a2e4da-e250-4892-b159-a7066d2c6c6a","version":1,"status":"pending","url_null":true},{"kind":"option","id":"b4f48443-244b-4370-a281-94f69ff00d37","version":1,"status":"pending","url_null":false},{"kind":"option","id":"b6194681-cb1c-4421-8418-cb09781046f8","version":1,"status":"pending","url_null":true},{"kind":"option","id":"bb5f25c1-ca5c-4a58-99d4-f03b52625004","version":1,"status":"pending","url_null":true},{"kind":"option","id":"bc4916c6-8db8-4aab-b1c3-4e82f6edbe34","version":1,"status":"pending","url_null":true},{"kind":"option","id":"bcb4aa32-4f64-4a88-a8c0-d9f02763a38f","version":1,"status":"pending","url_null":true},{"kind":"option","id":"be895634-8120-42ad-8424-9f39d1cc59df","version":1,"status":"pending","url_null":true},{"kind":"option","id":"bf9172d0-5aef-4b36-a1b8-4d4588a8d1f6","version":1,"status":"pending","url_null":true},{"kind":"option","id":"c05f72cb-8597-491e-9b53-da8f64f6a4bf","version":1,"status":"pending","url_null":true},{"kind":"option","id":"c2cdad33-1ef5-4891-88df-18f4f935e07b","version":1,"status":"pending","url_null":true},{"kind":"option","id":"c59c981f-bf73-4f33-9e79-09c670114a71","version":1,"status":"pending","url_null":true},{"kind":"option","id":"ccc4b5e3-15d1-45c5-b0b4-160842d80b69","version":1,"status":"pending","url_null":false},{"kind":"option","id":"cdadf8ea-a85f-417e-89e6-ff70a660cd85","version":1,"status":"pending","url_null":false},{"kind":"option","id":"ce3c41de-25a7-494e-a8e7-681b40d61b71","version":1,"status":"pending","url_null":true},{"kind":"option","id":"cfa7e834-e904-45da-9d4a-a90bbfcb0945","version":1,"status":"pending","url_null":true},{"kind":"option","id":"d1e93ed9-480d-41ba-9ce6-5de4e9d139f1","version":1,"status":"pending","url_null":true},{"kind":"option","id":"d55df51d-b401-468a-8149-bec50508b4c2","version":1,"status":"pending","url_null":true},{"kind":"option","id":"d5af74c6-0456-4f3b-8e44-52781e7f6abe","version":1,"status":"pending","url_null":true},{"kind":"option","id":"dfb3fe0e-7026-4a86-af7f-ea56c967353d","version":1,"status":"pending","url_null":true},{"kind":"option","id":"e5da18b7-0b5e-4e1d-8c38-d76d8b795ac8","version":1,"status":"pending","url_null":true},{"kind":"option","id":"e7a7e8f4-fb78-43e6-abf1-7d53ce62ef5b","version":1,"status":"pending","url_null":true},{"kind":"option","id":"ea0253d6-170e-4b24-8d30-565900321233","version":1,"status":"pending","url_null":true},{"kind":"option","id":"ec0b9313-17c7-454c-801d-4e77f9bb0556","version":1,"status":"pending","url_null":true},{"kind":"option","id":"ed45fd97-d9e7-433e-8ed2-98ad28d3f868","version":1,"status":"pending","url_null":true},{"kind":"option","id":"ee94fca7-7a70-4894-b05a-09f4092c811d","version":1,"status":"pending","url_null":true},{"kind":"option","id":"efef0014-bb15-46cc-a8c3-5ab5c5de9dd9","version":1,"status":"pending","url_null":true},{"kind":"option","id":"f44ffd7a-f544-4b90-9de4-55f5c0583ce7","version":1,"status":"pending","url_null":true},{"kind":"option","id":"f4865301-ce56-442c-b336-5370142f9b49","version":1,"status":"pending","url_null":true},{"kind":"option","id":"f4e39d22-ad77-4a25-bd0e-8cd73d996b44","version":2,"status":"pending","url_null":false},{"kind":"option","id":"f4f26da8-cfa0-42c0-b2a3-01bf6d34bc4d","version":1,"status":"pending","url_null":true},{"kind":"option","id":"f62855b8-50a7-4c2f-9ddf-aa1a78948141","version":1,"status":"pending","url_null":true},{"kind":"option","id":"f8391277-3692-4ba2-9b29-89794931e864","version":1,"status":"pending","url_null":true},{"kind":"option","id":"fa1dcd2e-db55-4c4f-bac1-009bdacca6b6","version":1,"status":"pending","url_null":true},{"kind":"option","id":"fac9680a-a241-4827-8b9e-70ef8758f760","version":1,"status":"pending","url_null":true},{"kind":"option","id":"fadcb9a0-278b-485d-ba9c-969b6d37ffae","version":1,"status":"pending","url_null":false},{"kind":"option","id":"fc367f21-cc02-4999-a159-1f0ecb662faa","version":1,"status":"pending","url_null":true},{"kind":"option","id":"ff023c57-7f7c-460f-9523-a55805fa42e0","version":1,"status":"pending","url_null":false}]'

BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SET LOCAL TIME ZONE 'UTC';

-- All variables enter SQL via psql SQL-literal quoting, never raw interpolation.
-- Invalid JSON, integer text, duplicate/unknown/previously-approved UUIDs fail closed.
WITH scope AS (
    SELECT * FROM jsonb_to_recordset(:'scope_json'::jsonb) AS x(kind text, id text)
), pending AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_pending'::jsonb)
        AS x(kind text, id text, version integer, status text, url_null boolean)
)
SELECT (
    :'phase' IN ('before', 'after', 'after-replay')
    AND :'expected_count'::integer BETWEEN 1 AND 125
    AND :'expected_approved'::integer BETWEEN 0 AND 105
    AND :'expected_edits'::integer BETWEEN 0 AND :'expected_approved'::integer
    AND (SELECT count(*) FROM scope) = :'expected_count'::integer
    AND (SELECT count(*) FROM scope) =
        (SELECT count(DISTINCT (kind, id)) FROM scope)
    AND NOT EXISTS (
        SELECT 1 FROM scope s LEFT JOIN pending b USING (kind, id) WHERE b.id IS NULL
    )
    AND NOT EXISTS (
        SELECT 1 FROM jsonb_array_elements(:'scope_json'::jsonb) e
        WHERE jsonb_typeof(e) <> 'object' OR e - ARRAY['kind', 'id'] <> '{}'::jsonb
            OR jsonb_typeof(e->'kind') IS DISTINCT FROM 'string'
            OR jsonb_typeof(e->'id') IS DISTINCT FROM 'string'
    )
    AND :'expected_approved'::integer <= (SELECT count(*) FROM scope WHERE kind = 'option')
) AS inputs_valid
\gset
\if :inputs_valid
\else
SELECT 1 / 0 AS invalid_verification_inputs;
\endif

SELECT 'snapshot' AS section, :'phase' AS phase, transaction_timestamp() AS captured_at,
       current_setting('transaction_isolation') AS isolation_level,
       current_setting('transaction_read_only') AS read_only,
       :'baseline_at'::timestamptz AS baseline_at, :'baseline_hash' AS baseline_hash;

SELECT 'inventory_totals' AS section,
       (SELECT count(*) FROM travel_service_products WHERE kind = 'hotel') AS hotel_products,
       (SELECT count(*) FROM hotel_booking_options o
        JOIN travel_service_products p ON p.id = o.product_id WHERE p.kind = 'hotel') AS hotel_options,
       (SELECT count(*) FROM travel_service_products
        WHERE kind = 'hotel' AND status = 'approved') AS approved_products,
       (SELECT count(*) FROM hotel_booking_options o
        JOIN travel_service_products p ON p.id = o.product_id
        WHERE p.kind = 'hotel' AND o.status = 'approved') AS approved_options,
       60 AS expected_hotel_products, 360 AS expected_hotel_options,
       40 AS expected_approved_products,
       255 + CASE WHEN :'phase' = 'before' THEN 0 ELSE :'expected_approved'::integer END
           AS expected_approved_options;

SELECT 'hotel_products' AS section, destination_id AS city, status, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(p)::text), '' ORDER BY id), '')) AS rows_md5
FROM travel_service_products p WHERE kind = 'hotel'
GROUP BY destination_id, status ORDER BY destination_id, status;

SELECT 'hotel_options' AS section, p.destination_id AS city, o.provider,
       o.status, o.discovery_status, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(o)::text), '' ORDER BY o.id), '')) AS rows_md5
FROM hotel_booking_options o JOIN travel_service_products p ON p.id = o.product_id
WHERE p.kind = 'hotel'
GROUP BY p.destination_id, o.provider, o.status, o.discovery_status
ORDER BY p.destination_id, o.provider, o.status, o.discovery_status;

-- These full-row fingerprints MUST be identical before/after/replay.
-- Include non-hotel rows as additional protection, not merely the 420 baseline rows.
WITH scope AS (
    SELECT * FROM jsonb_to_recordset(:'scope_json'::jsonb) AS x(kind text, id text)
), protected AS (
    SELECT 'all_hotel_products_unchanged' AS bucket, p.id::text AS id, to_jsonb(p) AS row_data
    FROM travel_service_products p WHERE kind = 'hotel'
    UNION ALL
    SELECT 'initial_approved_products_40', p.id::text, to_jsonb(p)
    FROM travel_service_products p
    WHERE p.id::text = ANY(string_to_array(:'approved_product_ids', ','))
    UNION ALL
    SELECT 'initial_approved_options_255', o.id::text, to_jsonb(o)
    FROM hotel_booking_options o
    WHERE o.id::text = ANY(string_to_array(:'approved_option_ids', ','))
    UNION ALL
    SELECT 'all_non_scope_hotel_options', o.id::text, to_jsonb(o)
    FROM hotel_booking_options o JOIN travel_service_products p ON p.id = o.product_id
    WHERE p.kind = 'hotel' AND NOT EXISTS (
        SELECT 1 FROM scope s WHERE s.kind = 'option' AND s.id = o.id::text
    )
    UNION ALL
    SELECT 'all_non_hotel_products', p.id::text, to_jsonb(p)
    FROM travel_service_products p WHERE p.kind <> 'hotel'
    UNION ALL
    SELECT 'all_non_hotel_options', o.id::text, to_jsonb(o)
    FROM hotel_booking_options o JOIN travel_service_products p ON p.id = o.product_id
    WHERE p.kind <> 'hotel'
), buckets(bucket, expected_rows) AS (VALUES
    ('all_hotel_products_unchanged', 60), ('initial_approved_products_40', 40),
    ('initial_approved_options_255', 255),
    ('all_non_scope_hotel_options', 360 - (SELECT count(*)::integer FROM scope WHERE kind = 'option')),
    ('all_non_hotel_products', NULL::integer), ('all_non_hotel_options', NULL::integer)
)
SELECT 'protected_groups' AS section, b.bucket, count(p.id) AS rows,
       b.expected_rows,
       CASE WHEN b.expected_rows IS NULL THEN NULL ELSE count(p.id) = b.expected_rows END AS count_matches,
       md5(coalesce(string_agg(md5(p.row_data::text), '' ORDER BY p.id)
           FILTER (WHERE p.id IS NOT NULL), '')) AS rows_md5
FROM buckets b LEFT JOIN protected p USING (bucket)
GROUP BY b.bucket, b.expected_rows ORDER BY b.bucket;

-- Per-target row fingerprints allow hold receipts to be compared with BEFORE rows,
-- even though the set of current receipts is empty before the first apply.
WITH scope AS (
    SELECT * FROM jsonb_to_recordset(:'scope_json'::jsonb) AS x(kind text, id text)
), rows AS (
    SELECT 'product' AS kind, p.id::text AS id, p.status, p.version, to_jsonb(p) AS row_data
    FROM travel_service_products p WHERE p.kind = 'hotel'
    UNION ALL
    SELECT 'option', o.id::text, o.status, o.version, to_jsonb(o)
    FROM hotel_booking_options o JOIN travel_service_products p ON p.id = o.product_id
    WHERE p.kind = 'hotel'
)
SELECT 'scope_row_fingerprints' AS section, s.kind, s.id, r.status, r.version,
       md5(r.row_data::text) AS row_md5,
       a.metadata_json::jsonb->>'outcome' AS receipt_outcome
FROM scope s LEFT JOIN rows r USING (kind, id)
LEFT JOIN admin_audit_logs a ON a.action = 'hotel_catalog_evidence_review'
    AND a.target = :'tag' || ':' || s.kind || ':' || s.id
ORDER BY s.kind, s.id;

SELECT 'root_actor_provenance' AS section, count(*) AS matching_roots,
       count(*) FILTER (WHERE r.mode = 'review_pending') AS review_pending_roots,
       count(*) FILTER (WHERE u.is_active) AS active_actors,
       count(*) FILTER (WHERE EXISTS (
           SELECT 1 FROM admin_audit_logs a
           WHERE a.action = 'catalog_review_requested'
             AND a.target = 'catalog-review:' || :'root_id'
             AND a.actor_user_id = r.actor_user_id
       )) AS authenticated_request_audits
FROM catalog_review_runs r JOIN users u ON u.id = r.actor_user_id
WHERE r.id = :'root_id'::uuid;

WITH receipts AS (
    SELECT a.* FROM admin_audit_logs a WHERE action = 'hotel_catalog_evidence_review'
        AND target LIKE :'tag' || ':%'
), scope AS (
    SELECT * FROM jsonb_to_recordset(:'scope_json'::jsonb) AS x(kind text, id text)
), root_actor AS (
    SELECT actor_user_id FROM catalog_review_runs WHERE id = :'root_id'::uuid
)
SELECT 'receipt_totals' AS section, :'expected_count'::integer AS expected_final_rows,
       CASE WHEN :'phase' = 'before' THEN 0 ELSE :'expected_count'::integer END AS expected_now_rows,
       count(*) AS rows, count(DISTINCT target) AS distinct_targets,
       count(*) - count(DISTINCT target) AS duplicate_targets,
       count(DISTINCT actor_user_id) AS distinct_actors,
       count(*) FILTER (WHERE actor_user_id = (SELECT actor_user_id FROM root_actor)) AS root_actor_rows,
       count(*) FILTER (WHERE actor_user_id IS NULL) AS null_actor_rows,
       count(*) FILTER (WHERE metadata_json::jsonb->>'tag' IS DISTINCT FROM :'tag'
          OR metadata_json::jsonb->>'root_run_id' IS DISTINCT FROM :'root_id'
          OR metadata_json::jsonb->>'baseline_hash' IS DISTINCT FROM :'baseline_hash') AS invalid_provenance_rows,
       count(*) FILTER (WHERE NOT EXISTS (
           SELECT 1 FROM scope s WHERE s.kind = metadata_json::jsonb->>'kind'
               AND s.id = metadata_json::jsonb->>'target_id'
               AND receipts.target = :'tag' || ':' || s.kind || ':' || s.id
       )) AS non_scope_receipt_rows,
       count(*) FILTER (WHERE metadata_json::jsonb->>'outcome' = 'approved') AS approved_rows,
       count(*) FILTER (WHERE metadata_json::jsonb->>'outcome' = 'approved'
           AND metadata_json::jsonb->'option_patch' IS NOT NULL
           AND metadata_json::jsonb->'option_patch' <> 'null'::jsonb) AS approved_edit_rows,
       md5(coalesce(string_agg(md5(to_jsonb(receipts)::text), '' ORDER BY id), '')) AS rows_md5
FROM receipts;

SELECT 'receipt_outcomes' AS section, metadata_json::jsonb->>'kind' AS kind,
       metadata_json::jsonb->>'requested_decision' AS requested_decision,
       metadata_json::jsonb->>'outcome' AS outcome,
       coalesce(metadata_json::jsonb->>'guard_code', '(none)') AS guard_code,
       count(*) AS rows,
       count(*) FILTER (WHERE metadata_json::jsonb->>'outcome' = 'hold'
           AND (metadata_json::jsonb->>'before_hash' IS DISTINCT FROM metadata_json::jsonb->>'after_hash'
             OR metadata_json::jsonb->>'before_version' IS DISTINCT FROM metadata_json::jsonb->>'after_version'))
           AS changed_hold_rows
FROM admin_audit_logs WHERE action = 'hotel_catalog_evidence_review'
    AND target LIKE :'tag' || ':%'
GROUP BY 2, 3, 4, 5 ORDER BY 2, 3, 4, 5;

-- Approved existing URL => +1 version and one normal review.
-- Approved previously-null URL => +2 versions, one edit and one review.
-- Hold => +0 versions and zero normal edit/review audits.
WITH receipts AS (
    SELECT a.*, a.metadata_json::jsonb AS m FROM admin_audit_logs a
    WHERE action = 'hotel_catalog_evidence_review' AND target LIKE :'tag' || ':%'
), pending AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_pending'::jsonb)
        AS x(kind text, id text, version integer, status text, url_null boolean)
), joined AS (
    SELECT r.*, b.version AS baseline_version, b.url_null,
           o.version AS live_version, o.status AS live_status,
           o.url AS live_url, o.evidence_url AS live_evidence_url,
           (SELECT count(*) FROM admin_audit_logs a
            WHERE a.target = r.m->>'target_id'
                AND a.action = 'travel_services.hotel_option_edit'
                AND a.created_at >= :'baseline_at'::timestamptz) AS edit_audits,
           (SELECT count(*) FROM admin_audit_logs a
            WHERE a.target = r.m->>'target_id'
                AND a.action = 'travel_services.hotel_option_review'
                AND a.created_at >= :'baseline_at'::timestamptz) AS review_audits
    FROM receipts r LEFT JOIN pending b ON b.kind = r.m->>'kind' AND b.id = r.m->>'target_id'
    LEFT JOIN hotel_booking_options o ON o.id::text = r.m->>'target_id' AND r.m->>'kind' = 'option'
)
SELECT 'receipt_version_audit_guards' AS section,
       count(*) FILTER (WHERE baseline_version IS NULL
           OR (m->>'before_version')::integer IS DISTINCT FROM baseline_version) AS invalid_baseline_version,
       count(*) FILTER (WHERE m->>'outcome' NOT IN ('approved', 'hold')
           OR m->>'outcome' IS NULL) AS unknown_outcomes,
       count(*) FILTER (WHERE m->>'kind' = 'product' AND m->>'outcome' <> 'hold') AS forbidden_product_mutations,
       count(*) FILTER (WHERE m->>'kind' = 'option' AND (
           live_version IS DISTINCT FROM (m->>'after_version')::integer
           OR (m->>'outcome' = 'hold' AND (
               live_status IS DISTINCT FROM 'pending'
               OR live_version IS DISTINCT FROM baseline_version
               OR edit_audits <> 0 OR review_audits <> 0))
           OR (m->>'outcome' = 'approved' AND (
               live_status IS DISTINCT FROM 'approved' OR live_url IS NULL
               OR live_version IS DISTINCT FROM baseline_version + CASE WHEN url_null THEN 2 ELSE 1 END
               OR edit_audits <> CASE WHEN url_null THEN 1 ELSE 0 END
               OR review_audits <> 1
               OR (url_null AND (
                   m->'option_patch'->>'url' IS DISTINCT FROM live_url
                   OR m->'option_patch'->>'evidence_url' IS DISTINCT FROM live_evidence_url))
               OR (NOT url_null AND m->'option_patch' IS NOT NULL
                   AND m->'option_patch' <> 'null'::jsonb)))
       )) AS option_version_or_audit_errors
FROM joined;

WITH actions(action, kind, expected_final) AS (VALUES
    ('travel_services.product_edit', 'product', 0),
    ('travel_services.product_review', 'product', 0),
    ('travel_services.hotel_option_edit', 'option', :'expected_edits'::integer),
    ('travel_services.hotel_option_review', 'option', :'expected_approved'::integer)
), targets AS (
    SELECT id::text AS target, 'product' AS kind FROM travel_service_products WHERE kind = 'hotel'
    UNION ALL
    SELECT o.id::text, 'option' FROM hotel_booking_options o
    JOIN travel_service_products p ON p.id = o.product_id WHERE p.kind = 'hotel'
), scope AS (
    SELECT * FROM jsonb_to_recordset(:'scope_json'::jsonb) AS x(kind text, id text)
), root_actor AS (
    SELECT actor_user_id FROM catalog_review_runs WHERE id = :'root_id'::uuid
), scoped AS (
    SELECT a.*, x.kind FROM admin_audit_logs a
    JOIN actions x ON x.action = a.action JOIN targets t ON t.target = a.target AND t.kind = x.kind
    WHERE a.created_at >= :'baseline_at'::timestamptz
)
SELECT 'normal_service_audits_since_baseline' AS section, x.action,
       CASE WHEN :'phase' = 'before' THEN 0 ELSE x.expected_final END AS expected_rows,
       count(a.id) AS rows,
       count(a.id) = CASE WHEN :'phase' = 'before' THEN 0 ELSE x.expected_final END AS count_matches,
       count(a.id) FILTER (WHERE a.actor_user_id = (SELECT actor_user_id FROM root_actor)) AS root_actor_rows,
       count(a.id) FILTER (WHERE a.actor_user_id IS DISTINCT FROM
           (SELECT actor_user_id FROM root_actor)) AS invalid_actor_rows,
       count(a.id) FILTER (WHERE NOT EXISTS (
           SELECT 1 FROM scope s WHERE s.kind = x.kind AND s.id = a.target
       )) AS non_scope_rows,
       md5(coalesce(string_agg(md5(to_jsonb(a)::text), '' ORDER BY a.id)
           FILTER (WHERE a.id IS NOT NULL), '')) AS rows_md5
FROM actions x LEFT JOIN scoped a ON a.action = x.action
GROUP BY x.action, x.expected_final ORDER BY x.action;

-- All pre-baseline audit rows are immutable, including prior normal route audits.
-- Capturing every action hash detects changed/deleted historic rows outside hotels.
SELECT 'all_historical_audits' AS section, action, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(a)::text), '' ORDER BY id), '')) AS rows_md5
FROM admin_audit_logs a WHERE created_at < :'baseline_at'::timestamptz
GROUP BY action ORDER BY action;

WITH expected(tag, expected_rows, expected_md5) AS (VALUES
    ('hotel-review-all-20260908', 290, 'd31bf5777d5dff64c86693fa74a24324'),
    ('hotel-review-followup-20260909', 67, '120f42a19572275eca89a0b5994c8344')
), fingerprints AS (
    SELECT e.*, count(a.id) AS rows, count(DISTINCT a.target) AS distinct_targets,
           md5(coalesce(string_agg(md5(to_jsonb(a)::text), '' ORDER BY a.id)
               FILTER (WHERE a.id IS NOT NULL), '')) AS rows_md5
    FROM expected e LEFT JOIN admin_audit_logs a
      ON a.action = 'hotel_catalog_evidence_review' AND a.target LIKE e.tag || ':%'
    GROUP BY e.tag, e.expected_rows, e.expected_md5
)
SELECT 'previous_batch_receipts' AS section, *,
       rows = expected_rows AND distinct_targets = expected_rows AND rows_md5 = expected_md5 AS unchanged
FROM fingerprints ORDER BY tag;

SELECT 'travel_service_config' AS section, id, version,
       md5(data::jsonb::text) AS data_md5, md5(to_jsonb(c)::text) AS row_md5
FROM travel_service_config c ORDER BY id;

-- Hash ciphertext but never print it. Stable settings exclude health observations.
SELECT 'provider_configs' AS section, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(c)::text), '' ORDER BY id), '')) AS full_rows_md5,
       md5(coalesce(string_agg(md5((to_jsonb(c) - ARRAY[
           'created_at', 'updated_at', 'last_tested_at', 'last_test_status', 'last_test_message'
       ])::text), '' ORDER BY id), '')) AS stable_settings_md5
FROM provider_configs c;

SELECT 'travel_service_brands_all' AS section, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(b)::text), '' ORDER BY id), '')) AS rows_md5
FROM travel_service_brands b
UNION ALL
SELECT 'travel_service_offers_hotel', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(o)::text), '' ORDER BY o.id), ''))
FROM travel_service_offers o JOIN travel_service_products p ON p.id = o.product_id WHERE p.kind = 'hotel'
UNION ALL
SELECT 'destination_affiliate_offers_hotel', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(o)::text), '' ORDER BY id), ''))
FROM destination_affiliate_offers o WHERE module = 'hotel'
UNION ALL
SELECT 'hotel_booking_clicks_all', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(c)::text), '' ORDER BY id), ''))
FROM hotel_booking_clicks c
UNION ALL
SELECT 'affiliate_clicks_hotel', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(c)::text), '' ORDER BY id), ''))
FROM affiliate_clicks c WHERE service_type = 'hotel' OR module = 'hotel'
ORDER BY section;

COMMIT;
