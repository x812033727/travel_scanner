---
id: 2026-10-20-curio-s48-lost-atlantic-cable-source
title: Curio S48 lost Atlantic cable source-audited episode preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T14:19:58Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s48
---

# Curio S48 lost Atlantic cable source-audited episode preproduction

## Why

站主請持續製作不重複的新歷史長片。S48 聚焦 1865 年大東號把大西洋電報電纜遺失海底、1866 年回頭鉤起並接通的單一事件鏈；與既有 S38 倫敦大火、S43 達爾文、S45–S47 人物題及題庫的海難題不同。1865 年船上記者日記與 1892 年後出的 Field 家族敘事須分清見證層次，尤其不能把每次抓到繩索就說成已接通。

## Definition of done

- [x] 固定兩份可重開全文與 SHA，按原文行號列事實、數字、歧義與畫面界線。
- [x] A／B 企劃與推薦方案、30–60 秒濃縮開場、保守至少 8 分鐘的時序劇本、逐句主張與畫面提示可供獨立覆核。
- [x] `lint` 0 error，檔案雜湊與未完成關卡留在交接；未經獨立來源／雙盲、站台與影音驗收不稱完成影片。

## Steps

- [x] 對照題庫及既有 S 集；從 GITenberg 固定 Russell 1865 現場書與 Field 1892 年後出敘事。
- [x] 寫來源錨點、企劃、可愛畫面劇本、逐景主張並重生 `script.md`。
- [x] 執行 lint／一致性與估時，記錄精確 SHA 後釋出本票。

## How to verify

在 repo 根目錄跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s48 --json`、`npm run check:tasks`；前者只驗靜態關卡，片長要等 TTS 實測。原始來源檔為 `/tmp/s48-russell-atlantic-telegraph.txt` 及 `/tmp/s48-field-atlantic-telegraph.txt`，其 SHA 記於 `research.md`。

## Notes

S48 前製由此票持有，僅寫 `docs/videos/curio-s48`；與其他代理的 S33／S43／S45／S46／S47 範圍無衝突。1858 年已有短暫跨洋電報，不能把 1866 年說成首次跨洋通信。Russell 是 1865 年隨船報導者；Henry M. Field 的 1898 印本（1892 版權）是後出家族敘事，雖引用船員與原始日記，不能整書當 1866 當日船上逐字紀錄。站主的常設推薦偏好只允許本機選 A，網站關卡仍待真正審核。

前製候選已封存於 `docs/videos/curio-s48/verify-1.md`；`lint` 為 0 errors／0 warnings，103 句主張表逐句文字一致，325 單位／分估正文 8:37.6。這只完成本票的前製範圍，獨立查核、兩位盲讀、站台決策、音畫與影片仍待後續票認領。

2026-10-20 獨立查核者重新下載兩份固定原文並核 SHA，判 R1 [史料與書面畫面 HOLD](../../docs/videos/curio-s48/review/r1-source-independent.md)。`atl080` 把目視共五分鐘誤寫成斷後再五分鐘；`atl095` 混合 Dudley 和另一段《Spectator》見證；研究 P10 把船上儲存線圈檢查誤置於海底拖鉤；`atl099` 的「測出」過強；多個電流計／海底纜線提示詞會畫出來源不支持的器具和視角。修成 R2 後重新固定 hash、獨立差分及兩位新盲讀；未修前不得配音或買圖。

2026-10-20 R2 精準修訂已寫入 `docs/videos/curio-s48/verify-2.md`，逐條回應 R1 的 `atl080/095/099`、P10 與 `atl003/024/029/076/096` 畫面問題；另把 `atl057/094` 口播作來源層級修正，P14/P16 分行段。五檔 exact SHA、103/103 句一致性、325 單位／分開場 44.5 秒及正文 8:40.6、`lint` 0 errors/0 warnings 已記錄。**仍等另一人對 R2 的獨立差分及兩位新盲讀**；R1 HOLD 不由作者自行撤銷，未做站台／音圖／影片。

R2 交接前再縮緊 `atl076`：提示詞只正面描繪抓鉤索、渾濁海面與瞭望者，不提舊線，減少生圖模型提早畫出電纜的風險；唯一改變的五檔雜湊是 `video.json`，新 SHA 已在 `verify-2.md`。

2026-10-20 另一人對最新精確 R2、兩份固定原文及 R1 HOLD 清單做[獨立差分覆核](../../docs/videos/curio-s48/review/r2-source-independent.md)，判 **史料 PASS、書面畫面 PASS**：五分鐘為斷前總目視、Dudley 船上與《Spectator》愛爾蘭端分層、脆線是船上線圈、搜尋帶只按航位推估，書面提示詞不提早顯露海底線或畫針式電流計。此 PASS 綁 `video.json` SHA `431f19fcf13bc325df7de65678fcc6d34368becb946a722ca931e9a3786032f3` 等 verify-2 五檔；兩位全新讀者敘事盲讀、站台、音畫仍待。

2026-10-20 兩位全新、互相隔離的讀者在精確 R2 上回報 8/13、10/13；共同 No 的 `no_spoiler`、`chapters_link`、`no_recap` 使[合併敘事正式 FAIL](../../docs/videos/curio-s48/review/r2-narrative-merged-reported.md)。原始逐題 JSON 未保存，共享檔只如實記轉述摘要。作者已作 R3 精準修訂：[verify-3.md](../../docs/videos/curio-s48/verify-3.md) 凍結五檔 SHA，記錄破梗、章節橋接、重複結尾、真正新 payoff、來源行號及自查。R3 `lint` 0 errors／0 warnings、103/103 逐句一致、325 單位／分正文 8:45.8；仍須**另一人獨立史料／書面畫面差分與兩名全新讀者盲讀**，R2 PASS 不移轉，未做 TTS、買圖、動畫、組片或站台核准。

2026-10-20 另一人的 R3[獨立來源審稿回報摘要](../../docs/videos/curio-s48/review/r3-source-independent-reported.md)為**來源 HOLD、書面畫面 PASS**：Field 將 1866 年第二線抵岸寫成「Saturday, September 7」，但 9 月 7 日實為星期五；Russell 的 1,186 `miles` 此處未明定陸英里或海里。原始審稿全文未留，共享收據只據轉交結論記錄。作者已做 R4 小幅修訂：[verify-4.md](../../docs/videos/curio-s48/verify-4.md) 將抵岸改「九月初」、放線門檻改「超過一千海里」並交代兩種解讀皆成立，凍結五檔 SHA；`lint` 0 errors／0 warnings、103/103 句一致、325 單位／分正文 8:45.4。**R4 尚待另一人獨立來源／書面畫面差分和兩名全新盲讀**；無站台、TTS、插畫或組片成果。

2026-10-20 R4：另一位製作人重開固定 Russell／Field 原文，按 1866-09-07 星期矛盾及 1,186 miles 單位歧義核對精確新版，判[史料／書面畫面差分 PASS](../../docs/videos/curio-s48/review/r4-source-independent.md)。R4 只說「九月初」「超過一千海里」，並公開換算與來源限制；仍須兩名真正全新讀者對 R4 敘事盲讀，Jev、網站與付費媒體未做。

2026-10-20 R4 正式隔離雙盲：此前兩個看過 brief／claims 的 R4 首讀保留為編輯意見；另用 CLI 只含旁白與 13 題的 JSON 給兩位全新讀者，A、B 各 11/13，均判必答 `payoffs`、`no_recap` No，合併[正式敘事 FAIL](../../docs/videos/curio-s48/review/r4-official-panel.md)。主要是 `atl026→027` 承諾無法交代的故障原因、`atl005→054` 鉤物問答含糊，以及 `atl050→054`、`atl095→096` 事實重述。R5 修後須重跑獨立來源／畫面及真正新隔離盲讀；未進語音或付費媒體。
