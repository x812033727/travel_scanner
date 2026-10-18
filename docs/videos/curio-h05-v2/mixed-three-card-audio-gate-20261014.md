# H05 v2｜三張來源卡接入後的旁白時間軸

日期：2026-10-14。`open-threat`、`open-tail`、`open-boy` 已改為[原創 SVG 來源卡](visual-recovery-three-native-cards-20261014.md)，line IDs／口播／場景順序未改。獨立盲審使用的純稿 payload SHA-256 `10ff38b065127285268ee21a027cb21088f7b33e023c328520bc693abf94fcab`；主製作代理確認 11／11 通過，正式 `review/narrative.json` 已匯入，narrative hash 為 `25c823ca2e556693`。本文件記音訊重綁與其後的核准讀回。

## 改前快照與離線核對

快照在外部 `_receipts/mixed-three-cards-audio-before-20261014T040549Z/`，`snapshot.json` SHA-256 `77c153eae26d74b7a64fbd3f7cfab25494edbe8f119e7db8910c229dd8fbaa3e`。121 個檔案逐一複製及比對 SHA，含當時 `video.json`、`script.md`、時間軸、核准、盲審、轉錄、manifest、帳本、旁白總檔及 108 句 WAV。刷新前無專案或上層 `STOP`，無 `LEASE`；媒體帳本 US$0.1755，該步無新費用。

新版 `video.json` SHA-256 `d9f63fe9b019228f21ec02cb0b8029956ae8beed314342a9e841c77c5b2e9bba`，speech hash `0b7b642f114d257f` 與前版相同。Measured dry-run 仍為 16,204 影格／108 句；58 個 shot 占 9,053 影格（55.8689%），108 個畫面狀態最長 7.8 秒、平均 5.0 秒；cadence、章節與素材檢查均無問題，`lint` 零錯誤及零警告。

## 僅用快取重建

`tts --refresh-evidence` 的防護先確認 0 stale takes；工具回報 **0 requests synthesized、0 billable characters、102 requests reused**。正式 `timeline.json` SHA-256 由 `db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee` 更新為 `e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9`，僅三個場景的 template 跟著新版腳本改為 diagram；全部句子音檔 SHA／sample count、影格起訖與全片 16,204 影格不變。`narration.wav` SHA-256 仍為 `f0ce6fff529dfb60a72c0e7b4479938d48f6f476ca5961b7ea2190ba15f6feac`；核准檔與媒體帳本亦未變。

既有 `review/check.json` 的 108／108 句均可依各句 WAV SHA 重用，原 12 個標記也仍是同一批音檔。因沒有新的語音 take，不再做一次外部轉錄或 Jev 呼叫。驗證細節在 `refresh-verification.json`（SHA-256 `2fc0ebd763efe651a1baa7c0c1f8bb4fc62d4d5f07b0ba727a085f42319ffc95`）。

## 後台音訊關卡

`review-push --gate audio` 已為新時間軸送卡，回覆 **pending**；其紀錄 `review-push-audio.log` SHA-256 `c7530fe2eabd86ec97591f3a25e1b9f5eb0a6df105853af9d32602a27f9f0e1c`。緊接的一次 `review-pull --gate audio` 回 exit 3、`audio: waiting for the owner`；舊三筆音訊核准都綁舊時間軸，不能沿用。當時沒有代站主核准，也沒有生成已另獲窄範圍授權的 `night-clouds` 圖；當時的下一關是站主在 `/admin/videos` 審新音訊卡，再讀回本時間軸的核准。

站主其後在 `/admin/videos` 核准。主製作代理執行 `review-pull --slug curio-h05-v2 --gate audio` exit 0；正式 `approvals.json` 新列的 `gate=audio`、`file=timeline.json`、`sha256=e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9`、`approved_at=2026-10-14T04:07:53.585Z`，核准檔 SHA-256 `4c9eeb731bf165350a5b4b2f4f2e5b916ad5702a12338ea286be7803f5d29a0a`。上段 pending 是送審當時狀態；現行音訊關卡已核准讀回。
