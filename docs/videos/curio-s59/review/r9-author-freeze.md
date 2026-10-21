# S59 R9｜重聽疑問回收與片末回呼，作者凍結

2026-10-21 UTC。**作者預檢完成，待全新獨立史料／書面畫面覆核及兩位隔離敘事盲讀；付費媒體 HOLD。** [R8 正式合票](r8-merge-policy/summary.md)固定 OR 12／13，唯一未過 payoffs：兩位都指出 s59059 問錫箔磨損是否妨礙旁人重聽，後文沒有直接回答。B 另指出 s59108 重複機械原理卻沒有點名回呼；這一題在 R8 正式 OR 由 A 通過，本輪作者也作一處窄幅清理。

| 凍結創作檔 | R9 SHA-256 |
| --- | --- |
| research.md | 39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d |
| brief.md | 9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3 |
| claims.md | 54e6c2f1d8fb533161ed48980ef1043faf6716c70999576507de9d6a735da747 |
| video.json | a0f986b5f1f578f6170b62ad24e17775b87ef4d3eb463104de9975a84928e4e6 |
| script.md | 6c28555d04104c676f76414479f038f426893f940a183e2518e3e9abac22cc09 |

[結構化差分](r9-author-structured-diff.json) SHA-256 a99c3380fe38c57b2ff7845f11c98eb82f525c660465c25540da22bb43fec72e。兩個 video.json 台詞葉節點與兩個逐句表台詞欄逆換後，R8 的 video、claims 和工具生成 script 原始 SHA 全部精確復原；research、brief、所有 prompt 和卡片資料未變。visualHash 仍是 3e39a4b9868072e1；narrativeHash 從 755facc75e73fc89 改為 2b1c46b809933014。

- s59059 現直接回答：錫箔上的痕多次播放後會變淺，旁人雖可重聽，聲音會漸糊；結尾把新困難接到搖柄上的手。這是 [D6955–6976](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6955-L6976) 的同段觀察，沒有將磨損或轉速指定為杜蒙塞爾巴黎初試失敗的原因。
- s59108 用「還記得箔上的壓痕嗎？」點名回呼 s59052 的機械路徑，並把針與薄片的回放振動扣回開場腹語疑問；沒有再宣稱回放音質恆定或巴黎當天實行書中另述的電話檢驗。[D6935–6953](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6935-L6953) 提供回放機理，[D6999–7025](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6999-L7025) 提供腹語疑慮與重試。

script CLI 重生 script.md，110 句、100 張 shot、10 張 big、12 組伏筆；正文扣除開場九句與末兩句為 2,626 漢字，以每分鐘 325 漢字最快估算 8.08 分鐘，全片工具估 13.37 分鐘。lint 0 error／0 warning，docs-video tests 236／236，check:tasks exit 0（其他長期認領警告）。這些只是形式與作者檢查，不能替代新獨立判讀；R8 票與史料收據對 R9 失效。沒有付費呼叫。
