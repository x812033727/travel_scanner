# 第一集正常 runtime 候選接入收據（2026-10-09）

九張最新版全身圖已離線接入正常工作目錄，全部仍是待 judge、待選用候選。這份收據只更新本次接入狀態；原始畫像與隔離 staging 收據保留其歷史狀態。素材／v4 與 Hailuo 預算的正式採用由主控另綁決策收據；本次工具沒有寫入 look 核准或 plan 開拍鎖定。

- 工作目錄：`<VIDEO_WORKDIR>/ou-de-jianghu-e001`；CLI `--workdir` 傳入其上一層 base，未套錯雙層 slug。
- `runtime_candidates_integrated: true`、`owner_adoption_recorded_here: false`、`budget_authorization_recorded_here: false`、`look_approved: false`、`plan_locked: false`。
- 27 次 CLI：9 dry-run、9 import、9 exact-rerun，全部 exit 0；整個 characters 樹重跑後位元組相同。
- `fetch_attempts: 0`；`paid_requests: 0`；未帶 `--judge`、未 choose／approve／review-push／review-pull。global fetch 與 CLI fetch 均在程序內禁止。
- 啟動時無 LEASE／STOP、characters／keyframes／clips／approvals／media；持有本程序專屬 lease 後才寫入，每次命令前重查，完成後明確 release 並確認 LEASE 消失。
- 每人恰一候選 n=1；`judge=null`、`suggested=null`、`needs_review=true`；沒有 choice／approvals／付費帳本／series-store 寫入。

## 綁定與核對

| 證據 | SHA-256／值 |
| --- | --- |
| v4 video.json | `cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17` |
| 正式 repo video.json | `82d221350032c02b3b2f8943e72e63795be36e221c45067acf5bd9a751d20443` |
| look_hash（v4 與 repo 相同） | `9b3e6914dbc8d109` |
| 正常 characters/manifest.json | `cf37aa3541380f13b864d3c01560e533fc176e7c5d85f472560408e85f7406b6` |
| 全 characters 樹索引 | `79a7b1f92f1f27e8c927246f82ee576c3c68339e4d399ae02a0d5376384c922b` |
| 27 次命令紀錄 | `03470b5b351780504d0cfb5114ad8f77efd66039d530bb53f3ed2f00884aceaf` |

12 份正典來源逐檔重新算 SHA-256，完整清單見同名 JSON 的 `source_files`；畫像收據、原圖、所有原參照圖及 v4 文件也重新算 hash 並前後核對。九張原生 PNG 均為 1024 × 1536，未改圖或放大。v4 與 repo 的 look_hash 和九個 sheetKey 相同，只證明角色基底契約相容，不等於 v4 劇本／plan 已正式採用。

| 角色 ID | 接入版本 | 原圖 SHA-256 | source sidecar SHA-256 |
| --- | --- | --- | --- |
| shen-guihe | shen-guihe-full-body-v3 | `f92406c0e73a7458e012a1487a60cd966b128192f776ddd272028cbd3724ccac` | `f964a4ed3ddda9857786ed5d324c2ac254d88c8040a2810ebe7145ca843cfdca` |
| ji-wushuang | ji-wushuang-full-body-v1 | `6ed68b1de7db15559e4b9d57c84ba92c0ffff80bf1e59970c82677d4915ecec3` | `3d1d54b11375f21ce567ef1d2842bf120e8aad228cc9fa751bc7132d756ae886` |
| ji-wen | ji-wen-full-body-v1 | `8a60b9ce8f83534542d002caedc0102d65255137d9eca99190091565e3ed9a35` | `cb88c8b5aa2c91261570bfb23cf569cc87f78ffa524b8b7cee022211ca89279d` |
| bao-sanqian | bao-sanqian-full-body-v1 | `625174d287f29d8fda2791f8193a89c26476a121bea7b1d80aa52fbc9e43afd9` | `61b5cf282e9fc6acba339b6c2d3d5170ce848ef77660f5d9f02a19c9b04501a6` |
| yin-wusheng | yin-wusheng-full-body-v1 | `ccf625f6813518032435c4a462a1203e6128691afda10516fe9dbcf95e5972ea` | `c1777de700a1b50a6469a30158f6be60b91c7e49209b4feb2a287bda9ac28fac` |
| yan-hui | yan-hui-full-body-v1 | `5cf0a08166ecbb00a7f1a484c4bc7c8ec16ab772f5ad61f1f8390c44792caa21` | `41de788f0ca4bb1ddfdc6788d00a8544a66ef3788030e9ef058fbbb83ad41afb` |
| nie-gutie | nie-gutie-full-body-v1 | `866e1e8cb75e7fabd7ebdc7ae2deca88938b79fc05f864a9c708d31d5d597115` | `c2f414cb80d7b5fe9e2a3b54599f5198b679870443df2bf49553d80d508f6318` |
| xuanmen-elder | xuanmen-elder-full-body-v1 | `564e79297979b1c7bb49b3fba39d8c3e590a2fc6bae246fa37b01837ac61667d` | `984fb9e2493ce88508f99484e565b39db249aa1f3d9dc6bb9361b64f08001606` |
| luo-qingyan | luo-qingyan-full-body-v1 | `9b3991c06ec0ae39acedaec6332a698d7209a75bbb3e5b245e79b6b3da96aeef` | `11d36ae8695d037dd83df65c09bf4925397ad4aea7afc19d3bee16de64120092` |

## 保留的關卡

主控在接入前已傳達使用者正式採用 146 份素材、v4、Hailuo 本期 26980.8 點及小樣 316.8 點；正式決策由主控另記。本收據不重寫原始收據的歷史 pending 值。使用者明確不授權 API 扣款，look 留待實際判圖；本工具沒有執行 judge、選用、核准或 plan 寫入。後續必須用真實 judge 結果走正常選用與 look 審核，不能把本次候選接入或人工實圖覆核寫成 judge。既有八張 staging 圖仍同版；沈歸鶴這次接入 full-body-v3，舊 staging 的 v1 保留不動。

## 重查

在 repo 根目錄以可用 Node 執行 `node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/prepare-runtime-look-20261009.mjs --check --media-base "<VIDEO_WORKDIR>"`。此模式只讀核對來源、原圖、sidecar、manifest、完整候選樹、27 筆命令與本收據；若後續正常 judge 或來源更新導致改變，它會失敗提示歷史收據已非目前狀態。

外部完整收據：`<VIDEO_WORKDIR>/ou-de-jianghu-e001/adoption/20261009/receipts/runtime-look-preparation-20261009.json`；命令紀錄：`<VIDEO_WORKDIR>/ou-de-jianghu-e001/adoption/20261009/logs/runtime-look-commands.json`。
