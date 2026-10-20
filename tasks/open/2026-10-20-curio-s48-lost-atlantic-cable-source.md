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

2026-10-20 R5 作者限縮修訂：依正式 R4 FAIL 修正短暫斷訊與當年抓鉤兩條問答，`atl047` 改問能否上船並回收到接頭斷裂，`atl054` 換成 Russell 有記的備索再試，`atl085/086` 消除計數重述且章首接慢收動作，刪除重述岸端回訊的 `atl096`。企劃、逐句主張及重生劇本同步；[verify-5.md](../../docs/videos/curio-s48/verify-5.md)凍結五檔及兩份原文 SHA、CLI 隔離旁白 JSON SHA、來源／提示詞語義差分和作者自查。`lint` 0 errors／0 warnings，102/102 逐句一致，325 單位／分估正文 8:42.6。**仍須另一人對 R5 精確版獨立史料／書面畫面差分、兩位真正全新隔離讀者盲評**；R4 FAIL 不因作者改稿而自動撤銷，未做站台、Jev、TTS、購圖、插畫或組片。

2026-10-20 R5 [獨立來源／書面畫面差分](../../docs/videos/curio-s48/review/r5-source-independent.md)：精確五檔與 Russell／Field 原文 SHA 均核對，102/102 句按 ID、順序、字面一致。**史料文字 HOLD、書面畫面 PASS**。新 `atl054` 的「斷索後」把 Russell R4029–4034 的轉環銷釘頭斷裂混說成索本體斷裂；應改「接頭斷後」或「轉接鐵件斷後」，同步三檔並重凍結、重審新精確版本。兩張新提示詞可由原文支持。R4 敘事 FAIL 仍需兩位全新隔離讀者重評，未進媒體製作。

2026-10-20 R6 作者按 R5 HOLD 限縮修訂：`atl054` 的「斷索後」改成「接頭斷後」，同步 `video.json`、重生 `script.md`、`claims.md` 口播及限制；其餘旁白、提示詞、景序未改。[verify-6.md](../../docs/videos/curio-s48/verify-6.md)凍結 R6 五檔 SHA 與新官方盲讀 JSON SHA。`lint` 0 errors／0 warnings，102/102 句一致，325 單位／分估正文 8:42.8。**下一步須另一人覆核 R6 精確稿，再找兩位全新隔離讀者重評敘事**；R5 來源 HOLD 與 R4 敘事 FAIL 不由作者自行撤銷，仍無站台、語音、插畫或成片。

2026-10-20 另一位審稿者完成 R6 [獨立史料／書面畫面差分](../../docs/videos/curio-s48/review/r6-source-independent.md)：固定 Russell R4008–4013 與 R4029–4045 分別記先前鐵索斷裂但被止動器抓住、稍後轉環銷釘頭斷裂而鉤與餘索落海；R6 `atl054` 的「接頭斷後」符合後一事故，**來源 PASS、書面畫面 PASS**。五檔與兩份原文 SHA 已核；102/102 句一致，所有提示詞未變，`lint` 0 errors／0 warnings。此 PASS 只綁 R6 精確稿；仍須兩位全新隔離讀者評敘事，R4 正式敘事 FAIL 尚未撤銷，未進媒體製作。

2026-10-20 R6 [正式隔離雙盲敘事關卡](../../docs/videos/curio-s48/review/r6-official-panel.md)：兩份原始回答、原始 payload 及 `panelVerdict`／`mergePanelVerdicts` 完整結果均已封存。payload 與現行 CLI 輸出逐位元相同，五檔 SHA 仍與上列獨立來源／畫面 PASS 相同。A **12/13**，只對必答 `no_spoiler` 答 No，認為 `[atl002]` 提早交代深海中的纜線；B **13/13**，認為開場停在回收場景與待解問題。無共同 No，依固定規則合併 **13/13 PASS**，分歧原樣保留。此結論只放行 R6 精確文字的敘事關卡；Jev、網站大綱／劇本決策、TTS、插畫、配樂及成片仍未做。

2026-10-20 R6 [全稿 Jev 政策與站台劇本卡](../../docs/videos/curio-s48/review/r6-policy.md)：五檔 SHA 未漂移。先以 `review-push --report-only` 建立 S48 站台 row，讀回 `category=explainer`、`format=drama`、審核卡 0 件；再對完整 3,096 字元旁白做**一次**無重試 `policyRequest({ doc, brief })`，`questions=explainer`、**PASS**（stance .73、demo 不適用、advice .01、sponsored .13），匿名回條及防重送私有紀錄均留存。`review-push --gate script` 送出精確 R6 劇本；站台讀回 1 張 `hand_pushed=true`、`status=pending` 的劇本卡，SHA `ddf43a0f76cef45f378d3d34c4a1050d7391eaf11bf2faf8f8f3f3f0833e3c5f`，**未獲網站或站主核准**。大綱卡、TTS、插畫、配樂與成片均未執行。

2026-10-20 R6 [配音實測與音訊 HOLD](../../docs/videos/curio-s48/verify-7.md)：五檔精確 SHA 未變；本機委派選擇大綱 A 與劇本，不冒稱站台核准。Gemini Sulafat 首合成 102 句、2,896 billable characters；官方 `check-audio` 22 flagged。兩輪只重唸當輪受標句（22／634 字元、13／364 字元），每輪重新完整覆核，旗標降到 **9**，仍以結束碼 1 未過。最終旁白實測開場 54.77 秒、正文 10:48.30、含片尾 11:57.20；完整首版、兩輪 WAV／時間線、原樣檢查與旗標、受標單句備份及雜湊留在私有工作目錄。兩輪額度已用完，**在音訊 HOLD 停手，未畫圖、配樂、組片或推送音訊核准**；待九句聽感／措辭／發音字典覆核後再接手。

2026-10-20 R7 作者依兩輪重唸後仍有的九句旗標作[最小聽感改稿與精確凍結](../../docs/videos/curio-s48/verify-8.md)：只改 `atl029/040/049/054/059/066/090/095/099` 九個口播，與 `claims.md` 同步並重生 `script.md`；`atl054→atl056` 增一條問答伏筆，所有畫面提示詞與其餘 93 句不變。五檔 SHA、逐句差分、固定史料界線和只讀盲讀 payload SHA 均在 verify-8；`video.json` SHA `143026c1d2306a31ee54ff8970d6f79a353983682f4c756a9fe0575c6a164168`，`lint` 0 errors／0 warnings、102/102 句 ID 唯一且主張同文。325 單位／分估開場 45.27 秒、正文 8:49.27；尚無 R7 實測時長。**R6 的來源／書面畫面、雙盲、政策、網站卡與音訊結果皆不能移轉為 R7 放行**；須由另一人重核九句及新問答、兩位全新隔離讀者重評，之後重跑全稿政策和站台精確稿流程，才可重新合成改句並完整音檢。作者未發動新付費呼叫，仍未插畫、配樂、組片或成片。

2026-10-20 R7 [獨立史料／書面畫面差分](../../docs/videos/curio-s48/review/r7-source-independent.md)：固定 Russell／Field 原文及 R7 五檔 SHA 均核對；九句改詞、新 `atl054→atl056` 的推定搜尋帶回收均有原文支持，**史料文字 PASS、書面畫面 PASS**。`video.json` 只改九句文字並增一條伏筆，99 個插圖提示詞未改；102/102 句按 ID、順序、字面與 `claims.md` 同步，`script.md` 的 99 句正文加三句片尾相符，`lint` 0 errors／0 warnings。這只放行 R7 精確稿的來源與書面畫面；**仍須兩位全新隔離讀者重評敘事，再處理 R7 政策／站台、改句 TTS 與完整音檢**。目前 R6 音訊 HOLD 不移轉，尚未買圖、配樂或組片。
