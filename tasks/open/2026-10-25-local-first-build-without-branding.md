---
id: 2026-10-25-local-first-build-without-branding
title: Local first builds silently omit channel bookends when no package is installed
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-25T21:16:06Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/assemble/cli.mjs
  - docs/videos/branding-release
---

# Local first builds silently omit channel bookends when no package is installed

## Why

2026-10-25第三支claude-formal-verification-255的首次assemble明確加adopt-branding/intro-after-condensation時，原生工具在編碼前拒絕：no current branding package is installed for this video。本producer的/workspace/work/videos沒有_branding/current.json，也沒有正式intro/outro素材；同機既有DNS與ForTy成片亦無branding.json。官方v4素材指紋與本地缺少素材是兩回事，不能把旁白outro卡當作已裝正式頻道動畫。

拿掉adopt參數的一般first-build會回傳null並繼續合成，QA的brandingCurrent對兩端皆null可通過。這可讓缺正式片頭片尾的成片被誤稱符合全套新規則。2026-10-04的bookend audit已記錄相同缺default原因，本票補上本次可重現的本機防呆及待補素材項。沒有修改shared toolcode或正式站。

## Definition of done

- [ ] 新長片缺branding package時有明確可見的未完成項，不能把缺素材當全套規則已完成。
- [ ] 以正常可用管道取得／驗證站主正式片頭片尾，再安裝到本producer；不假冒v4、不使用未授權音樂或管理員私有路由。
- [ ] 依真正目前final／approval／YouTube身分決定各片採用或換版，保留原音訊、縮圖和舊收據；若換版，更新成片SHA、各CC／M4A時間軸、metadata／package及後臺讀回。
- [ ] 原始本地單元／整合測試涵蓋missing-default與正常installed-default；不部署、不自動公開影片。

## Evidence and current work

- 第三片首次explicit-adoption失敗log：/workspace/work/ai-tech-next/formal-assemble.log，編碼前失敗，沒有重做TTS／ASR。
- sourcee6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f、speech8028c7320d9cab29，105／105音檢通過；其後正常assemble主體僅供候選審看，不因此聲稱有頻道動畫。
- third main、八語與下一支內容製作照常前進，本票保持open、不把待補項清掉。
- 正式v4片頭原始SHA50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d／150frames；片尾00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396／630frames，來源僅repo既有release紀錄，未聲稱本機有其bytes或已安裝。
