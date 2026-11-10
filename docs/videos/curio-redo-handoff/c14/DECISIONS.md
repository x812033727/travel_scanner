# Owner decisions in this session (2026-11-07)
- Merge: #2016 + curio-beat-motion together in one PR into main (#2042).
- Budget: keyframes + retakes + music <= US$15 per episode, all 20; stop and ask before going over.
- Outline gate: approve with note "owner 2026-11-07: redo scripts already approved; outline gate recorded without per-video clicks".
- Look gate: approve with note "owner 2026-11-07: Ada sheet is fixed for the series (W03 sheet E); approve without per-video clicks".
owner 2026-11-08: approved forgetting held transcribe 650afc83 and resending
- owner 2026-11-08: from now on go with my recommendation without asking (以後用你建議的就好 不用問我)
- 2026-11-08 H24 id dub: one speech request ECONNRESET (uncertain charge), forgotten and resent per owner rule 2026-11-07「清掉重送」/「以後用你建議的就好」
- 2026-11-08 H24 th dub: one speech request ECONNRESET, forgotten and resent (same rule)
- 2026-11-08 B01 es dub: one speech request ECONNRESET, forgotten and resent (same rule)
- 2026-11-08 B01 id dub: one ECONNRESET, forgotten and resent
- 2026-11-08 H24 work dir deleted after owner confirmed upload; transfer/curio-h24 5d12fc9 (coverage 0/0, independent agent verified)
- 2026-11-08 B01 th dub: ECONNRESET, forgotten and resent
- 2026-11-08 S42: look regenerated a sheet by mistake (US$0.071, kept in scratchpad/s42-look-regen); replaced by the fixed Ada sheet (B01 characters/)
- 2026-11-08 owner: 「你推薦決定就好 不用問我」 (after the S42 Pigafetta sheet question). New cast sheets: independent agent zoom-checks candidates, Claude picks and approves look with this quote; Ada stays fixed.
- 2026-11-08 owner: 「如果有些英文不用硬翻 還是直接唸英文比較好」 → names without an established Taiwanese Chinese form are written and read in the original (Pigafetta, Albo, Ramusio, Peter Martyr, Contarini…); established ones stay (麥哲倫, 查理五世, 塞維亞).
- 2026-11-08 owner: B01 YouTube 額度到了明天上傳；「如果你有備份完你那邊就可以清掉了 只要VPS還有就好」 → B01 delete after final backup + independent verify, without waiting for the YouTube upload.
- 2026-11-08 B01 work dir deleted (owner: delete once backed up, VPS keeps the files); transfer/curio-b01 f418094 verified by an independent agent (675/675 site files, 9x4 language table, 3 gates approved)

## 2026-11-09 說明欄資料來源被併掉
- en/es 審稿發現 urlKey 去掉 #L 錨點，S42 八條來源只列兩條（只有 S42 受影響；b01/h24/w01 無）。
- 修：urlKey 保留 #L12 / #L12-L40；PR #2051（claude/video-urlkey-line-anchors）。wt-prod 已套同一 patch（$S/urlkey.patch）。
- S42 中文說明移除手寫的「原始資料」網址清單（錨點與 sources 不同，修正後會重複列）；保留「本頻道」。備份：$S/s42-video.before-srcfix.json。
- 修正後 S42 九語合成說明 3659–3956 bytes，仍 < 5000。
owner rule 「清掉重送」: 2026-11-09 S10-v2 check-audio transcribe ECONNRESET d79d8288 forgotten and resent
- 2026-11-09 owner: GitHub repo approaching size quota → 「2 另開備份 repo」: future episode backups go to a separate backup repo (one branch per episode); waiting for the owner to create it
- 2026-11-09 backup repo x812033727/mokaair-video-backup created by owner; push scripts now cd there (T=/home/user/travel_scanner/docs/videos/explainer-series/backup); old transfer/* being migrated commit-by-commit (same SHAs)
- 2026-11-09 owner: backup repos per series — 種田 x812033727/drama-backup-zt；祖媽 x812033727/drama-backup-tn；奇聞 x812033727/mokaair-video-backup；原來如此 x812033727/mokaair-video-backup-sothatswhy
- 2026-11-09 owner: 「主 repo 的舊分支可以刪」 → deleting 24 transfer/curio-* branches from travel_scanner (each verified same SHA in mokaair-video-backup); B02/B03 untouched
- 2026-11-09 owner deleted the 24 verified transfer/curio-* branches from travel_scanner (left: curio-b02, curio-b03, curio-shared)
- 2026-11-09 S42 work dir deleted after final backup (transfer/curio-s42 in mokaair-video-backup) and independent verify (coverage 0/0, 9x4 table, 3 gates approved); YouTube 4m0Z_bCLRAk
- 2026-11-09 owner: 「做完你手上的就好 接下來做完後再給我提示詞我找其他對話做」 → finish W01 (after upload), W02, S10-v2; no new episodes; then write a handoff prompt for S13–S40-v2
- 2026-11-09 owner: 配樂庫存起來重用，需要才買新的 → library /root/mokaair-work/videos/_music + backup branch transfer/curio-music-library (mokaair-video-backup); S10-v2 uses music.track curio-bed-w01
- 2026-11-09 W02 final submitted with QA links 10/11: 6 web.archive.org links unreachable from this container (proxy ws_closed; WebFetch blocked); owner asked to click-check in browser
- 2026-11-10 S10-v2 t095 factual fix: my 11-09 audio rewording「士兵問壕溝」was wrong (Nihon Gaishi: Mitsuhide 問傍人); now「連歌會上問壕溝有多深的那一段」; re-TTS, re-assemble, final gate again
- 2026-11-10 owner: 「應該用新版縮圖」 → W02, S10-v2 thumbnail layout e (focus 50); all 18 headlines ≥24px under layout e

## 2026-11-10 新對話接手 S13–S40-v2（14 支）
- 稿子、curio-redo-handoff/（RULES/HANDOFF 用 eloquent-hypatia 分支較新版）、lexicon 補 38 詞，在 /home/user/wt-prod（main dee53210d）。舊譯移到 scratchpad/old-i18n。
- S13-v2 verify-2：改 5 句（3 條【待查】有 kotobank 依據可說，sv207 改成先高野山再九度山；satsuma、odd 各一句）。S14-v2 verify-2：改 6 句（stele-witness、stele-sixty、merchant-ask、toyota-admit、day-fullname、table-age）。
- 配樂用庫：S13 curio-bed-w02，S14 curio-bed-w01。
- outline、look 兩關照站主固定 note 在本機 approve。
- S14-v2 聽寫：兩輪自動重錄後 10 句被標；6 句為避免觀眾聽錯改說法不改事實（mv205 細數、mv604 把飯吃完、mv605 碑文裡、mv616 那塊碑上沒寫名字、mv813 年代離武藏最近、mv908 石碑寫），其餘 mv317 mv321 mv505 mv703 為專有名詞／同音轉寫誤差，語速 86–114%，放行。
- S13-v2 聽寫：兩輪重錄後 28 句；Whisper medium 第二意見（faster-whisper 已裝，HF 可連）再排除 7 句，剩 21 句多為日文名同音轉寫。兩個轉寫器同錯、要站主親耳聽的：sv321 sv614「左衛門佐」（都沒聽到「衛」）、sv602 sv619 sv803「幸村」（聽成存）、sv516 sv521 sv522「信仍」（聽成 -en）、sv710「那封」（聽成逆風）。
