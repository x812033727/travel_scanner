## 2026-10-31 新規則改稿現況

正文 3,100 字、125 句、113 景，lint 估 13 分。查核 `verify-2.md` 有條件通過，問題已全改。

**盲評還不算過**：五輪，最後兩位其他十二題都是，但 `no_recap` 兩位都答否（`panel/merged.json` 記著），每次指的是不同句，都已改，改完沒有再讀，因為額度快到了。下一步：再找一位讀者讀一次，`no_recap` 答是就過。三位讀者都說第六章（n087–n098）信件細節最可能離開。

# S43 寫稿紀錄

## 2026-10-31 新規則改稿

- 字數：正文 3,114 字，含片尾 3,214 字。
- lint：0 錯誤、3 警告，估計 13.5 分（開場約 59 秒）。三條警告都是 `adult`／`year`／`naturalist` 在提示詞裡太常出現：來自逐字沿用的舊提示詞（舊稿為了不讓達爾文畫成小孩，每張都寫「22-year-old adult naturalist」），不改；新提示詞沿用同樣寫法。
- `loops` 21 個，每個都回收；「你」34 次；「還記得」4 句（n023、n043、n079、n116，另有 `n049`「你記得第三條吧」）；明說的前向鉤子 1 句（`n020`「第四條你先記住」）。
- 章節（8 章）：一封邀請信到家，他想去，回信卻是拒絕／父親沒說不行，只是勸到他自己寫下拒絕／四條變八條，舅舅一條一條回答，再駕車三十英里／位子還在，他叮嚀姊姊別講，中午船長的信就到了／五分鐘前空出來的位子，和船長最難聽的實話／名字都上了名冊，他還是不肯點頭／兩次被吹回來，出海後兩人在巴西吵翻／幾小時後的道歉，和他很熟以後才聽到的鼻子。
- 畫面：110 張插圖、6 張卡片（open-promise、sense-card、note-card、settled-card、gale-card、nose-card）。沿用 81 景／新提示詞 22 景；另外 7 景是逐字複製的提示詞（open-letter、captain-empty、list-smile、doubt-berth、quarrel、king-again、captain-doubt），不用再畫。舊景的 `id`、`data.prompt`、`camera` 一字沒改，不少舊景換了配的旁白。新提示詞：open-nose、captain-rage、priest、off-to-maer、shooting、father-smile、mrs-henslow、llama、captain-confess、gig、captain-king、bahia、captain-praise、darwin-retort、packed、gunroom、apology、captain-dawn、boss、lavater、job-seeker、elder-nose。
- 沒用到的舊景 15 張：dn003、dn005、dn011、dn012、dn016、dn018、dn019、dn020、dn021、dn023、dn032、dn044、dn069、dn076b、dn077a。
- 舊紀錄（舊分支 `verify-7.md`）寫到兩輪試圖共 6 張（第二輪是 `dn008`、`dn082`、`dn087a`），本機沒有檔案。同一份紀錄寫 `dn008`、`dn082` 人物偏孩童或畫風不過，未 KEEP；兩景這次仍照規定沿用，畫的時候要再看一次。還沒跑 `tts`、`keyframes`、`music`。
- 查核：三份固定版本重新下載，SHA-256 與 `research.md` 相符。N01–N41 寫在 `research.md` 末節，原文字串由腳本逐一比對，行號也是腳本定位的。

**還沒解決的事**

- 盲評 `narrative` 還沒跑，查核結論要另一個代理覆核（尤其 N35 巴伊亞那段、`n040` 的先後、`n048`「位子還在」）。
- `claims.md` 末節列了兩份來源對不上的地方：自傳說「當晚」回絕、信是隔天；清單與打獵的先後。旁白都避開了，查核時請再看一次。
- 巴伊亞那段談到奴隸制，畫面只有船長與達爾文兩人，沒有畫被奴役的人；政策審時請再看一次。
- 第 4 章的詹尼斯與亨斯洛太太那段是這集最接近岔題的地方；它回收父親的第三條。如果盲評兩位都說岔題，先壓這裡（`n051`–`n052b`）。
- 標題已講「放棄了兩次」，開場預告 `o009` 只說「又會逼他做決定」。如果盲評說開場被標題講掉，標題後半換成「1831 年的信一個字都沒提」。

（舊的 2026-10-20 審查紀錄在分支 `origin/codex/curio-s34-endurance-20261019` 的同一資料夾 `verify-*.md`、`review/`，沒有帶過來。）
