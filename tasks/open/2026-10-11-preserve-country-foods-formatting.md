---
id: 2026-10-11-preserve-country-foods-formatting
title: 保全 country-foods 工作樹的 17 個格式修改並確認所有者處置
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-10-11T13:46:06Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-preserve-country-foods-formatting.md
---

## Why

原分支 `codex/country-foods-map-links` HEAD `a8736021c98f38a71e5f57555766d4cb86cc893e` 的產品已由 PR #56 replacement branch 合併，merged commit `803b84601340d024fcdfe4fb326e086aa2a4e9c3` 為目前主線祖先；migration renumber 0020→0022 的完整 upgrade/downgrade AST 等價，其餘產品亦有正面落地證據。checkout `C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanner-foods-maps` 仍有 17 個未提交 Python 路徑。完整工作 diff 及逐檔 AST 證明這 17 個修改目前只涉及格式，但產品已完成不能當作所有者放棄這些 bytes，也不能因此 reset／刪工作樹。

## Done when

- [ ] 17 個路徑、原 HEAD 與所有未提交 bytes 已有可回讀的保全檔、完整 patch、SHA-256 manifest；保存來源時間與 restore／roundtrip 結果。
- [ ] 再核對當前 worktree status 與 HEAD；如新增／更動檔案，另記新快照，絕不套用本票舊「formatting-only」結論去丟棄新內容。
- [ ] 找到原 owner/task 與未釋放 claims，記錄 owner 對保留、另票整合或明確捨棄的意圖；沒有 owner 明確 disposition 就維持原工作樹及 branch 原狀。
- [ ] 若 owner 要整合，另開限確切檔案的票與正常檢查；若要清理，先核對保全可還原再由根任務依既有授權處理。本票只記處置證據，不自行 reset／清理，也不釋放原 claims。

## Steps

- [ ] 唯讀記錄 `C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanner-foods-maps` 的 HEAD/status、17-file完整 diff／bytes 與原 blob 身分；將保全置於工作樹外，不修改原 index 或檔案。
- [ ] 逐檔讀 HEAD 與 working bytes 做 Python AST 比對，將格式等價與 byte 差異分別記錄；檔案變動時重新判定。
- [ ] 先保存 patch 和每檔 bytes，使用獨立 scratch 複本 roundtrip 驗證 SHA-256；不得在原 checkout 試 restore。
- [ ] 在本票引用 owner 意圖及具體 disposition。此處置須涵蓋全部 17 路徑，不能因 PR #56 已合併而推論未提交修改可以丟棄。

## Verification

2026-10-11 初始封存為 17/17 AST-equivalent；每檔 bytes SHA-256 清單在下方。完整 manifest `C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/catalog-country-dirty-byte-manifest.json`；語意比對 `catalog-semantic-proofs.json` 的 `workingASTEquivalent`。最後仍需新鮮 status/HEAD 與 bytes 比對，並以 scratch restore 驗證內容，原 checkout/index、branch、owner/claims 均維持不變直到明確處置。

## Notes

來源分支產品完成證據及保護理由見 `C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/catalog-audit.json`。這不是重做 foods/map-links 產品的票。未提交的格式 bytes 未發布，也不代表主線產品未完成；單憑內容可逆或 AST 等價仍不能代 owner 決定捨棄。

2026-10-11 分支續查；共享票比對基線為 main `73c84ca7f5e75004dfb78c36b7bf7a971da8ca0b` 的全部 389 張 open 票，未找到同義任務（詳 `C:/Users/x8120/.codex/scratch/uncertain-branches-followup-20261011/catalog-open-task-check.json`）。本票只追蹤唯讀對帳與保全，初始 scope 僅含本票檔案，結果直接記在本票。任何程式、資料或其他證據檔修改須另開窄 scope 票並先核對所有者；不釋放或覆寫任何原 claims、owner、scope。未發布、未公開、舊票仍在 open、當前主線較新，均不能單獨證明現在仍 pending。這次開票不授權正式資料寫入、重播舊 batch、付費呼叫、部署或發布。

### 需保全的 exact 17 路徑與 working-byte SHA-256

- `apps/api/app/alerts/monitor.py` — `219b3c3722417d7cbb4f890a901a7dd22953e6f04439a6958ada7f1be051e9fd`
- `apps/api/app/alerts/router.py` — `f519f82ce9955e283e39d336b50c6233b842ed6c4b1746034e9905ca722911a5`
- `apps/api/app/auth/router.py` — `5b84051f19e736792b8514cbd86db729cbc825b85859ec3e3553dbee3cd40634`
- `apps/api/app/crawlers/back_to_back.py` — `f9f4512473713592bb755a6b3d94ff48430b9614fb09c96692c89bffae078881`
- `apps/api/app/crawlers/router.py` — `f21adbcd84b911012326cd352829c7b37ae673d4181bb73874357ed952f18983`
- `apps/api/app/flights/router.py` — `78e58ab8467cb27d00adb04d17ce77bcaf3d3940334f7f7c84cd313d1f6aa34a`
- `apps/api/app/line/client.py` — `70f2793f589729073240a79170beb393e3bdf2b8a99fdd467bde4c651f0bac22`
- `apps/api/app/problems.py` — `29387fc6f0f782bc95ca16b3c6c21dd1fbe73dd04046da735589b43fdd902e61`
- `apps/api/app/providers/booking.py` — `e8bf790a4c2dcc9fbda8e0c3bb53395d2e8e95956922ddd62926badb4dbd01cf`
- `apps/api/app/providers/google_travel_impact.py` — `7e0455f98a74403a762bdfc792531fba9e4465cb9c7c4f55b1608bb59415373a`
- `apps/api/app/providers/live_back_to_back.py` — `0a4a504fad9ffa59a4dd9b54d6490a05be411c7b8f093d67f4f37b1243dd7ec7`
- `apps/api/app/providers/usage_meter.py` — `c3faa9c254746536e882e2d8eaa35c4f6d785e717308588594353267903ef217`
- `apps/api/app/trips/route_planner.py` — `b00263e6db573f7d20f78725c1755f8af02791203987847249634da6ff396a8d`
- `apps/api/app/trips/route_tasks.py` — `a9358b0bb3be6e5363c52108772e69f5e4a892383cd646d82da8b61cef817f4b`
- `apps/api/app/trips/routing.py` — `8788944a8089c4fc974a58144b0d24eb6b67378af7739bd6152406b700a1c069`
- `apps/api/app/usage/service.py` — `b6568fabf900e4003940f3a4eaa0e2f4479623aaf44a8ee1c6f10991e31d15ae`
- `apps/api/app/weather/google.py` — `2c302d595cee044eb398c51b69579700cd82c3e1ce59b11515c771d4245409b0`

本票保持 open、未認領；建票只恢復待辦，不釋出原分支 owner 或授權接管現有工作目錄。續作時依 task-board 核對認領、main 與本票 scope；正式站寫入、合併／部署與付費生成維持各自原有授權。

本票 scope 僅含這份對帳紀錄：以唯讀調查及可查核結論完成交接。需要產品、資料或原工作目錄修改時另開並認領窄 scope 票，不以本票直接處置。
