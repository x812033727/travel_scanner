---
id: 2026-10-19-curio-s34-endurance
title: Curio S34 Endurance new history episode
status: done
priority: P2
area: docs
owner: codex-gpt6-s34
claimed_at: 2026-10-19T17:09:06Z
created_at: 2026-10-19T17:09:01Z
completed_at: 2026-10-19T20:06:56Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s34
---

# Curio S34 Endurance new history episode

## Why

站主 2026-10-19 要一支新的歷史影片，明確選擇「另做新題目」；S01、S09、S18 已由另一位工作者認領。從奇聞檔案局 S 軸題庫選 S34 堅忍號，做一支史料可核、約十分鐘的單線故事。

## Definition of done

- [x] 原始史料與獨立覆核支撐年份、人數、數字和引句，不把另一支羅斯海支隊算進「28 人全員生還」。
- [x] 站主選定大綱與劇本；`video.json`、`script.md` 通過系列 lint 與盲評。
- [x] 旁白逐句核對、整集插圖、分鏡、配樂與成片 QA 完成；一項業配模型判斷有人工覆核紀錄。
- [x] 交付繁中上架包，由站主決定是否及何時上架。

## Steps

- [x] 檢查同題認領，建立窄 scope；避開 S01／S09／S18 與 `topics.json`。
- [x] 查核薛克頓《South!》原文，建立企劃與逐句來源，請第二位讀者獨立覆核。
- [x] 寫 A 案大綱與完整可審劇本，檢查鉤子、畫面、片長和系列規格。
- [x] 送劇本關卡，待站主選擇及核准後製作媒體。
- [x] 預覽旁白與整集圖數／最高花費，取得整集授權。
- [x] 完成逐句語音查核；音訊審核頁送後台，站主委託下留本機核准紀錄。
- [x] 完成插圖、配樂、成片品管與交付。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s34`；`node tools/video/cli.mjs script --slug curio-s34`；`npm run test:docs-videos`；外加逐句事實對照與獨立讀者盲評。成片另需 `status`、`check-audio`、`qa`、`package` 與站主的審核紀錄。

## Notes

- 2026-10-19：`topics.json` 的 S34 題目卡是**未查核候選**。草案的「1914 年被冰困並壓沉」與原書不同：1914 年啟航，1915 年 1 月被困、10 月 27 日棄船、11 月 21 日沉沒。「最近有人住的地方在一千多公里外」也沒有充分依據。題庫檔被 S01／S09／S18 試片票認領，本票只改 `curio-s34` 目錄；後續更新題庫需另行協調。
- 《South!》Standard Ebooks 固定版 `233aa69e707ecc348ceef2eb1c167ada6a28ac24` 在 `/tmp/curio-s34-south` 可讀。直接開書站與多數博物館網站被此環境網路政策擋住，因此以可開的原始文本核對；缺來源的 2022 沉船發現與徵人廣告不進旁白。
- 主機 S 軸支援任務 `2026-10-18-curio-host-route-knows-the-s` 尚未完成；先以本機 `format: drama` 準備可審稿，媒體階段要核對後台分類與關卡。
- 2026-10-19：站主選 A 案並核准最後 94 句劇本，`outline` 與 `script` 本機關卡有雜湊紀錄。第二位史料覆核覆蓋 94／94 句；兩位獨立盲讀者各通過 13／13 題，系列 lint 0 errors、0 warnings。`npm run test:docs-videos` 236 passed。站台裝置配對成功，語音 Gemini Sulafat dry-run 94 句／2,162 計費字元；MiniMax 插圖 dry-run 90 張、最多 3 次／張，站台報價上限約 US$3.65，站主已一次核准此上限。媒體保存在 `/workspace/.video-work/curio-s34`，權杖留在本機私密憑證檔，沒有進 repo。
- 2026-10-19：語音辨識共促成 12 句口語改寫，其中 `ed090` 最後再次簡化；獨立讀者盲評最後稿 13／13 通過、史料對照仍無重大出入，`lint` 0／0，已重記 `script` 雜湊。94 句 Gemini Sulafat 旁白實長 09:29；`check-audio` 80 句逐字相符、7 句同音或語助詞差異、7 句模型判可用、0 未解標記。音訊審核頁送後台；站主授權持續製作的本機紀錄不代表人工試聽。90 張插圖提示詞已獨立預審並修正六處史實／生成風險，整集 `keyframes --takes 3` 正在依 US$3.65 授權上限生成。媒體日誌 `/tmp/curio-s34-keyframes.log`，工作檔 `/workspace/.video-work/curio-s34`。
- 2026-10-19：90 張 MiniMax 插圖全部通過，第一輪四景未過已簡化提示詞重畫；另抽看聯絡表後，將「蓋帆布」與「翻救生艇搭屋頂」兩張畫面改得更貼旁白。全片畫面成本約 **US$1.80／US$3.65 核准上限**。分鏡審核送後台，本站主廣泛委託下記本機核准，不代表站主逐張親看。正生成配樂，後續還須 render、clips、assemble、captions、QA 與上架包。媒體在 `/workspace/.video-work/curio-s34`，不進 Git。
- 2026-10-19：成片 `final.mp4` 1920×1080、09:29.8、165.5 MB，SHA-256 `c694898370ea…`；93 段畫面合成，-14 LUFS，配樂底聲 -33 LUFS，繁中字幕 97 段。實花 MiniMax＋Lyria **US$1.8755**，低於站主核准的插圖上限。`qa` 11 項有 10 項通過：畫面節奏最長 10.6 秒、12 條說明連結全可開、縮圖／事實／字幕／音量等均通過。唯一未過 `policy`：Jev 將片尾「訂閱奇聞檔案局」評為業配 0.41（門檻 0.30）；逐句查閱旁白後確認沒有第三方商品、付費服務、贊助或購買引導，屬本頻道一般訂閱呼籲。已將原始 QA 與成片送至後台，依站主本回合持續委託記本機成片核准，備註清楚說明人工覆核與站主未親自觀看；後台成片審核仍待站主檢視。`package` 檢查 4／4 通過，繁中上架包在 `/workspace/.video-work/curio-s34/upload`，不進 Git；英文／日文／韓文尚未勾選製作。
- 2026-10-19：繁中上架包已推送後台 `publish` 審核，狀態 pending；站主按 `UPLOAD.md` 自行決定是否、何時在 YouTube Studio 以私人影片上傳。此票的可交付製作工作已完成。
