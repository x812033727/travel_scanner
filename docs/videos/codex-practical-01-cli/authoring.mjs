// Authoring source for the lesson-01 teaching cards. No model/provider calls.
// This writes only video.json and script.md beside this file.
import { createHash } from 'node:crypto';
import { writeFileSync } from 'node:fs';
const scenes = [];
const source = '01 CLI session-01 · 2026-10-11';
const lab = '01 五檔教材 · 作者提供';
function card(id, template, data, text, claims = [], chapter) {
  const capacity = template === 'bullets' ? data.items.length : template === 'steps' ? data.steps.length
    : template === 'table' ? data.rows.length : template === 'compare' ? 2
    : template === 'stats' ? data.stats.length : template === 'terminal' ? data.output.length : 0;
  scenes.push({ id, ...(chapter ? { chapter } : {}), template, data, claims,
    lines: text.map((text, i) => ({ // Retain the reviewed line identity when the listener clarifies its wording.
      id: id === 'baseline-before-change' && i === 2 ? '346cca' : createHash('sha256').update(id + ':' + text).digest('hex').slice(0, 6),
      text, ...(i < capacity ? { reveal: 1 } : {}) })) });
}
function list(id, title, items, text, claims = [], chapter, src = lab) {
  card(id, 'bullets', { title, items, source: src }, text, claims, chapter);
}
function table(id, title, columns, rows, text, claims = [], chapter, src = lab) {
  card(id, 'table', { title, columns, rows, source: src }, text, claims, chapter);
}
function code(id, code, caption, text, claims = [], chapter) {
  card(id, 'code', { code, caption }, text, claims, chapter);
}

card('first-verdict', 'stats', { title: '同一份起點，先留下基線', stats: [
  { value: '2', label: '測試通過' }, { value: '1', label: '測試失敗' },
  { value: '0', label: 'Codex 修改的檔案' }], source }, [
  'Codex 已經讀完專案，測試卻還有一個失敗。',
  '這次我們保留失敗，先把它變成能核對的基線。',
  '知道原本哪裡沒做，才看得出下一次改對了沒。'], ['C01','C02'], '先把現況看清楚');
card('project-promise', 'title', { title: '讀懂待辦網站，再決定下一步', subtitle: 'Codex 實作 01 · CLI｜真實 exec 檢查紀錄', tag: '同一專案，持續做成任務與週報工具' }, [
  '你可能已經會把需求交給 Codex，卻很難判斷結果。',
  '這個系列用同一個小網站，把判斷的方法做完整。'], ['C03']);
list('what-to-deliver', '這一輪的交付物', ['五份檔案的用途與界線', '實際測試、失敗位置、尚未驗證', '下一輪的目標、範圍與驗收'], [
  '今天交的是一份檢查報告，還不是新增功能。',
  '報告要指得出檔案，也要留下真的執行過的結果。',
  '最後把問題收斂成下一輪能驗收的小任務。'], ['C03'], '準備可以重做的起點');
list('unpack-all', '先解開完整教材', ['取得 codex-practical-01-materials.zip', '完整解壓：start／reference／challenge', '進入 start，不先複製 reference'], [
  '下載本課教材，完整解壓到新的練習資料夾。',
  '先進入起始資料夾，保留參考答案作為最後對照。',
  '混用不同課的起點，測試數和問題都會跟著改變。'], ['C03']);
table('folder-roles', '三個資料夾，三種用途', ['資料夾','用途'], [
  ['start','這次實際檢查的五檔起點'], ['reference','作者參考實作，供最後核對'], ['challenge','換一個情境，自行交檢查報告']], [
  '起始資料保留一個還沒完成的篩選功能。',
  '參考資料由作者提供，不是這輪模型改出的成果。',
  '換題練習則留給你重做，看看方法是否真的學會。'], ['C03','C04']);
code('environment-commands', 'codex --version\nnode --version\npy --version', '環境核對指令｜在 PowerShell 輸入', [
  '先確認終端機能找到 Codex、測試工具和網頁伺服器。',
  '版本先記下來，出現差異時才有線索。'], ['C05']);
table('recorded-versions', '這次錄製的版本', ['工具','實際值'], [
  ['Codex CLI','0.162.0-alpha.17.2'], ['Node.js','v24.13.0']], [
  '畫面是本次實跑版本，不是所有人的指定安裝版本。',
  '你可以用自己的版本跟做，先以本機說明核對參數。'], ['C05'], undefined, source);
code('correct-folder', 'Set-Location "你的教材路徑\\start"\nGet-Location\nGet-ChildItem -Name', '跟做指令｜把第一行路徑換成你的 start', [
  '切到起始資料夾，確認目前位置，再列出檔案。',
  '如果只看到資料夾，通常還在教材外層。'], ['C03']);
table('five-file-contract', '本課起點只有這五份主要檔案', ['檔案','負責'], [
  ['index.html','頁面結構'], ['style.css','畫面樣式'], ['app.js','瀏覽器事件、呈現與保存'],
  ['core.mjs','資料規則'], ['core.test.mjs','三個核心測試']], [
  '核對這五個名字，確認拿到本課相同的起點。',
  '本課瀏覽器程式的副檔名是這個，不要自行換名。',
  '先有一致的材料，後面的結果才比得起來。'], ['C06']);
list('baseline-before-change', '先保留原本的狀態', ['教材 manifest 可核對來源', '本次五檔前後 SHA-256 一致', '這一輪沒有提交修改'], [
  '本次檢查前後，五份檔案的內容雜湊一致。',
  '這讓我們能區分檢查報告和已經改好的專案。',
  '你練習時也保留起點，別靠記憶猜原本的樣子。'], ['C02'], undefined, source);

list('boundary-question', '讀專案，先問責任在哪裡', ['哪裡決定資料規則？', '哪裡把按鈕接到規則？', '哪裡負責把結果顯示出來？'], [
  '不用一開始就看懂每一行，先找出責任的分界。',
  '同一個症狀可能來自資料，也可能來自畫面事件。',
  '知道分界，下一輪才不會把整個專案一起改掉。'], ['C06'], '讀出五份檔案的界線');
code('html-module', '<script type="module" src="app.js"></script>', 'index.html:23｜session-01 起點原文', [
  '這行把頁面接到瀏覽器程式，檔名必須對得上。',
  '它使用模組載入，所以開啟方式也影響測試。'], ['C06','C07']);
list('html-structure', '頁面提供可操作的入口', ['新增表單與輸入欄位', '三種篩選選單與任務清單', '計數、提示與練習資料重設'], [
  '頁面檔提供表單和清單的位置，還有篩選選單。',
  '有選單不代表篩選做完，它只是使用者操作的入口。',
  '真正決定清單內容的規則，還要往程式裡找。'], ['C06']);
list('css-responsibility', '樣式檔處理外觀', ['版面與小螢幕排列', '完成項目的刪除線', '鍵盤焦點的外框'], [
  '樣式檔控制排列、完成效果和焦點外框。',
  '它不能證明資料是否被正確保存，也不負責篩選。',
  '畫面看起來正常，核心規則仍可能有缺口。'], ['C06']);
table('core-versus-browser', '資料規則和瀏覽器程式分開', ['核心 core.mjs','瀏覽器 app.js'], [
  ['新增、切換、刪除、篩選','監聽表單、勾選、按鈕'],
  ['資料編碼與解碼','讀寫 localStorage'],
  ['回傳資料結果','依結果重畫清單']], [
  '核心處理資料規則，瀏覽器程式接住操作。',
  '編碼資料和真的寫入瀏覽器儲存，是不同的責任。',
  '所以核心測試通過，不能直接等於整個網站通過。'], ['C06','C08']);
code('render-boundary', 'const shown = visibleTasks(tasks, filter.value);', 'app.js:22｜session-01 起點原文', [
  '這行把目前資料和選單值交給篩選函式。',
  '畫面使用回傳的清單，決定哪些任務要出現。'], ['C06']);
code('save-boundary', 'localStorage.setItem(key, encodeTasks(tasks));', 'app.js:16 的呼叫摘錄｜完整行含 try/catch', [
  '保存的資料由核心編碼，再由瀏覽器寫入。',
  '只有這個瀏覽器來源的儲存區會收到它。'], ['C06','C09']);
list('data-not-server', '目前沒有帳號與伺服器資料庫', ['資料保存在這個瀏覽器來源', 'CLI 測試不會自動讀到網頁的資料', '重新整理與保存必須另外檢查'], [
  '這是本機練習網站，沒有帳號和伺服器資料庫。',
  '終端機的核心測試，也不會自動取得網頁儲存的任務。',
  '要確認保存，得真的在瀏覽器重新整理再看結果。'], ['C06','C08','C09']);
table('evidence-levels', '兩種驗證，各回答一件事', ['核心測試','瀏覽器操作'], [
  ['資料規則符合斷言嗎？','事件與模組真的能運作嗎？'],
  ['輸入是否被意外改動？','重新整理後資料還在嗎？']], [
  '核心測試能快速定位規則，但範圍只到測試寫的地方。',
  '瀏覽器操作則檢查載入、事件和保存是否接起來。',
  '把兩種證據分開，才不會誤把半套驗收當成完成。'], ['C08']);

card('prompt-contract', 'steps', { title: '把檢查要求写成明確契約', steps: [
  {title:'目的',detail:'理解起點，不修改'}, {title:'動作',detail:'讀五檔，實跑既有測試'},
  {title:'證據',detail:'結果、位置、未驗證項'}, {title:'交付',detail:'報告與下一輪任務'}], source:'baseline-prompt.txt · session-01' }, [
  '提示不用寫得玄，先把目的和動作講清楚。',
  '再指定要留下什麼證據，避免只收到一段心得。',
  '最後要求下一輪任務，讓報告能接到真正的工作。'], ['C10'], '把提示變成可驗收的要求');
code('prompt-readonly', '這是教學的待辦網站起始材料。只讀檢查，不要修改任何檔案，\n也不要修正故意保留的測試失敗。', '原始提示第 1 段｜僅為卡片換行', [
  '先把只讀和保留失敗寫明，這輪只建立基線。',
  '如果模型順手修掉問題，後面就少了可比較的起點。'], ['C10']);
code('prompt-file-map', '請列出五份主要檔案的用途，\n以及資料操作和瀏覽器介面的界線。', '原始提示第 2 段｜僅為卡片換行', [
  '要求用途還不夠，還要它說明兩層之間的界線。',
  '你得到的應該是責任地圖，不只是檔名清單。'], ['C10']);
code('prompt-execute', '實際執行 node --test core.test.mjs，\n記下通過數、失敗數、失敗測試名稱與退出碼。', '原始提示第 3 段｜僅為卡片換行', [
  '這段指定實際執行，不接受讀完程式後猜測結果。',
  '測試名稱和退出碼能幫你回頭找到真正的問題。'], ['C10']);
code('prompt-separate-proof', '讀取失敗測試和對應程式，\n指出觀察到的現況與仍需驗證的假說，\n不要把假說寫成實測事實。', '原始提示第 4 段｜僅為卡片換行', [
  '讀程式推論出的行為，和操作看到的行為要分開。',
  '報告寫得肯定，不會讓沒有做過的測試突然成立。'], ['C10']);
code('prompt-next-task', '最後給下一個任務的目標、修改範圍和驗收條件；\n這一次只交檢查報告。', '原始提示最後一段｜僅為卡片換行', [
  '報告最後要能交棒，下一輪才有清楚的起終點。',
  '完整提示在教材裡，這幾張卡是原文分段。'], ['C10']);
code('save-prompt', 'Get-Content ..\\baseline-prompt.txt -Raw |\n  codex exec --sandbox read-only --skip-git-repo-check `\n    -C . --output-last-message ..\\baseline-answer.md -', 'PowerShell 跟做命令｜不是錄製的完整原始 argv', [
  '從起點把附上的提示送入一次執行，最後回覆另存檔案。',
  '畫面保留命令，方便你重做後比較自己的報告。'], ['C11']);
table('command-flags', '命令上這幾個位置要對', ['位置','作用'], [
  ['--sandbox read-only','以只讀限制執行'], ['-C .','使用目前起點目錄'],
  ['--output-last-message','保存最後報告'], ['末尾的 -','從標準輸入讀提示']], [
  '只讀限制是執行設定，不只是文字裡拜託模型。',
  '目前目錄必須是起點，報告則保存在起點外面。',
  '教材不是版本庫，所以這個命令明確略過版本庫檢查。'], ['C11'], undefined, 'Codex CLI 官方 reference · 2026-10-11');
list('recording-is-real', '本次真實執行留下了什麼', ['原始提示與完整執行參數', '24 筆事件及工具輸出', '最後報告、版本、時間與雜湊'], [
  '本次錄製保留原始提示、執行參數和事件紀錄。',
  '後面終端卡片是從實際輸出重現，不是假裝螢幕錄影。',
  '個人路徑不放進畫面，完整紀錄另行保存。'], ['C01','C12'], undefined, source);
card('report-first-line', 'quote', { quote:'只讀檢查已完成，未修改任何檔案，也未修正刻意保留的失敗。', source:'session-01/answer.md · 真實回覆摘錄', kicker:'模型回覆，要接著核對' }, [
  '模型回覆說沒有改檔，我們再用檔案雜湊核對。',
  '這次兩邊一致，才有依據把基線保留下來。'], ['C02','C12']);
table('two-exit-codes', '成功結束的是哪一層？', ['程序','退出碼與意義'], [
  ['Codex exec','0：這輪報告完成'], ['node --test','1：既有測試有失敗']], [
  '這裡有兩個退出碼，回答的是兩個不同問題。',
  '模型完成檢查，可以成功結束，同時報告測試失敗。',
  '不要看到外層成功，就把網站也寫成已經完成。'], ['C01'], undefined, source);

card('baseline-test', 'terminal', { title:'真實測試輸出摘錄／重新排版', command:'node --test core.test.mjs', output:[
  'ℹ tests 3\nℹ suites 0', 'ℹ pass 2\nℹ fail 1', 'ℹ cancelled 0\nℹ skipped 0\nℹ todo 0'],
  ran_on:'2026-10-11', tool_version:'Node.js v24.13.0', prompt:'>' }, [
  '這是模型真的執行過的測試，完整輸出保留在事件裡。',
  '總共三個測試，兩個通過，一個失敗，內層退出碼是一。',
  '起點預期就是這個結果，失敗不代表操作做錯。'], ['C01'], '讀懂測試失敗的意思');
table('three-tests', '三個測試的範圍', ['範圍','本次結果'], [
  ['新增、修剪文字、輸入限制','通過'], ['切換、篩選、刪除的組合','失敗於未完成篩選'],
  ['版本資料編解碼與錯誤輸入','通過']], [
  '新增資料和編解碼測試通過，問題集中在中間這組。',
  '它包含好幾個斷言，並不只有單一動作。',
  '所以還要找到實際停住的位置，不能只看測試名稱。'], ['C13']);
table('failure-location', '先讀預期和實際', ['欄位','內容'], [
  ['位置','core.test.mjs:17'], ['情境','兩筆任務，把 a 設為完成'],
  ['預期','未完成篩選只留下 b'], ['實際','a 和 b 都出現']], [
  '測試建立兩筆任務，再把第一筆設成完成。',
  '未完成篩選應該只留下第二筆，實際卻留下兩筆。',
  '這個差異，比一句篩選壞了更能指引下一步。'], ['C13'], undefined, source);
code('unfinished-function', 'export function visibleTasks(tasks, filter) {\n  return tasks;\n}', 'core.mjs:17–19｜session-01 起點原文', [
  '對應函式目前直接回傳全部任務，沒有使用篩選條件。',
  '這是教材刻意留下的實作位置，不是隨機製造的錯誤。'], ['C13']);
list('observed-not-guessed', '此刻已觀察到', ['未完成篩選包含了已完成任務', '對應函式忽略 filter', '測試停在第 17 行的斷言'], [
  '這三件事有測試輸出和程式內容支持。',
  '先把已觀察到的事講清楚，不急著猜其他功能。',
  '後續修改也要對著這些證據確認，不能只換個說法。'], ['C13'], undefined, source);
table('assertions-after-failure', '同一個測試，後段沒有跑到', ['斷言位置','本次狀態'], [
  ['第 16 行：原始資料未被改動','已執行並通過'], ['第 17 行：未完成篩選','已執行並失敗'],
  ['第 18–20 行：已完成、刪除等','本輪未執行到']], [
  '前一行確認原始資料未被改動，這個斷言通過了。',
  '下一行失敗後，同一個測試裡的後段就沒有跑到。',
  '因此不能把後面的刪除功能也宣稱這輪驗證過。'], ['C13'], undefined, source);
card('hypothesis-versus-fact', 'compare', {title:'這時候，網頁行為仍是推論', left:{heading:'程式推論',points:['畫面篩選可能仍顯示全部']}, right:{heading:'本輪模型實測',points:['只執行核心測試','沒有啟動瀏覽器']}, source:'session-01/answer.md · 真實回覆'}, [
  '讀程式可以推論畫面篩選也會有問題。',
  '可是這輪模型沒有開瀏覽器，推論還不是實際操作結果。',
  '接著用網頁操作，把這個缺口補成另一份證據。'], ['C08','C12']);

code('http-start-command', 'py -m http.server 4173 --bind 127.0.0.1', '跟做指令｜在 start 目錄啟動，另開瀏覽器', [
  '保持終端機開著，用本機伺服器提供這個資料夾。',
  '網址和檔案目錄要一起對，才是在測相同的網站。'], ['C14'], '把程式推論接到瀏覽器證據');
card('http-url', 'big', {text:'http://127.0.0.1:4173/', kicker:'瀏覽器網址列', sub:'目前終端機：start｜停止伺服器：Ctrl+C'}, [
  '瀏覽器打開畫面上的網址，別把命令貼到網址列。',
  '練習結束回終端機停止伺服器，資料仍留在瀏覽器。'], ['C14','C09']);
card('file-versus-http', 'compare', { title:'雙擊 HTML，換了載入方式', left:{heading:'雙擊檔案',points:['file://','模組載入受到檔案來源限制']}, right:{heading:'本機伺服器',points:['http://127.0.0.1:4173/','透過相同來源載入模組']}, source:'MDN Modules · 2026-10-11'}, [
  '雙擊頁面會走檔案網址，和本機網頁來源不同。',
  '這個起點使用模組，應該透過伺服器測試。',
  '如果只有外觀出現卻不能新增，先核對開啟方式。'], ['C07','C14']);
table('file-failure-observed', '這次真的看見了載入方式的差異', ['入口','作者另外實跑的觀察'], [
  ['file:// 起點','2 個錯誤，觀察到跨來源限制'],
  ['本機 HTTP 起點','可新增、完成並重新整理保存']], [
  '作者另外用檔案網址打開起點，觀察到兩個載入錯誤。',
  '改用本機網頁來源後，再操作新增、完成和重新整理。',
  '這個排錯先修正開啟方式，不需要先改程式湊成功。'], ['C07','C14','C15'], undefined, 'Edge browser/receipt.json · 2026-10-11');
card('browser-filter-method', 'steps', {title:'用同一個情境核對篩選', steps:[
  {title:'新增兩筆',detail:'讀專案、做網站'}, {title:'完成第一筆',detail:'留下另一筆未完成'},
  {title:'選未完成',detail:'起點目前仍顯示兩筆'}], source:'Edge browser/receipt.json · 2026-10-11'}, [
  '在起點新增兩筆，勾選第一筆，再切成未完成篩選。',
  '作者另外用瀏覽器實跑，起點仍顯示兩筆。',
  '這份網頁證據支持剛才的推論，但來源要分開標示。'], ['C15']);
table('author-reference-compare', '作者參考版，用來看驗收的樣子', ['驗證','start／reference'], [
  ['核心測試','2 通過 1 失敗／3 通過'], ['未完成篩選','顯示 2 筆／顯示 1 筆'],
  ['來源','原始教材／作者參考實作']], [
  '參考版的三個核心測試通過，未完成篩選只留下另一筆。',
  '它是作者參考實作，不能當成這輪模型的修改成果。',
  '先看到正確結果的形狀，才知道下一輪要驗什麼。'], ['C04','C16']);
table('browser-additional-checks', '另外檢查了哪些網頁行為', ['檢查','兩版觀察'], [
  ['重新整理','任務和完成狀態保留'], ['同名任務刪除','只刪選定的身分'],
  ['標記字串','當成文字顯示'], ['390 像素寬','沒有水平溢出']], [
  '網頁檢查還包括重新整理和同名任務刪除。',
  '同一個標題可以有不同身分，刪除必須對到那一筆。',
  '這些觀察補上介面證據，並不擴大核心測試的範圍。'], ['C15']);
list('storage-check-scope', '壞掉的儲存資料，先保留', ['兩版皆顯示無法讀取的提示', '原始損壞資料沒有被覆寫', '重設只處理練習專用資料'], [
  '作者也檢查損壞的儲存資料，兩版都保留原值。',
  '重設練習只處理專用資料，不該清空其他網站資料。',
  '遇到保存問題先看提示，別直接用清空全部代替診斷。'], ['C15'], undefined, 'Edge browser/receipt.json · 2026-10-11');
list('same-origin-for-reload', '保存檢查，要用同一個來源', ['同一個協定、主機、連接埠', '新增、完成，再重新整理', '換來源時不要當成資料遺失'], [
  '重新整理測試要留在同一個來源，連接埠也要相同。',
  '換了網址或連接埠，瀏覽器可能使用另一個儲存區。',
  '那時看不到任務，不足以證明保存函式有問題。'], ['C09']);

table('next-task-goal', '下一輪任務：只完成篩選', ['欄位','要求'], [
  ['目標','全部／未完成／已完成'], ['範圍','core.mjs 的 visibleTasks'],
  ['保留','既有測試與瀏覽器檔案']], [
  '下一輪把目標限定在三種篩選，不順手重做頁面。',
  '修改範圍指向一個函式，其餘檔案先保留。',
  '這樣結果不對時，也比較容易找到造成差異的地方。'], ['C17'], '把報告交成下一輪任務');
table('next-task-acceptance', '驗收不能只寫「正常」', ['情境','應該看到'], [
  ['兩筆，一筆完成，選全部','兩筆，順序不變'], ['選未完成','只有未完成那筆'],
  ['選已完成','只有完成那筆'], ['空清單','空清單，不出錯']], [
  '寫出具體情境：兩筆裡一筆完成，三種篩選各看到什麼。',
  '再把空清單列進去，避免只做出剛好成功的示範。',
  '驗收說得清楚，模型和你才是在回答同一個問題。'], ['C17']);
list('invariants', '這次修改不該造成的差異', ['不改原始資料', '不重排原有順序', '篩選不改總數或保存內容'], [
  '篩選決定顯示哪些任務，不該偷偷改掉原始資料。',
  '順序、總數和保存內容，也不是這個任務要變動的東西。',
  '把這些限制寫入驗收，就能攔住看似方便的額外修改。'], ['C17']);
code('next-prompt-suggestion', '完成 core.mjs 的 visibleTasks 三種篩選。\n只修改該函式，不改測試與瀏覽器檔案。\n重跑既有測試，再逐項記錄網頁驗收與未驗證項。', '下一輪提示建議｜本輪沒有執行這段', [
  '這段是下一輪可用的任務提示，本次只交報告。',
  '真正修改時，依同一套驗收重新跑，別提前填成功。'], ['C17']);
table('deliverable-status', '報告裡，把狀態寫完整', ['證據','本課狀態'], [
  ['模型檢查','完成，沒有改檔'], ['模型內執行測試','2 通過 1 失敗'],
  ['作者參考測試與網頁核對','另有實跑紀錄'], ['下一輪模型修補','本輪未執行']], [
  '模型檢查、作者對照和下一輪任務，各自寫清楚。',
  '不要把參考程式通過，寫成模型已經完成修補。',
  '把狀態講準，才知道真正還缺哪一個動作。'], ['C01','C04','C15','C16','C17']);

table('failure-wrong-directory', '找不到測試檔，先核對目錄', ['看見的問題','先做的事'], [
  ['找不到 core.test.mjs','列出目前目錄檔案'], ['只有 start／reference','進入 start 再執行']], [
  '如果找不到測試檔，先列出目前目錄，不急著叫模型補檔。',
  '教材外層和起點目錄不同，回到正確位置再跑。',
  '路徑問題修好以前，測試結果無法代表這份專案。'], ['C18'], '卡住時，先縮小問題');
table('failure-auth-or-quota', '模型沒有執行，和測試失敗分開', ['情況','處理'], [
  ['尚未登入','依官方登入流程處理'], ['額度或服務錯誤','保留訊息，不填成測試結果'],
  ['沒有工具執行紀錄','要求明確列出未執行項']], [
  '如果登入或額度卡住，模型可能根本沒有檢查專案。',
  '保留錯誤訊息，報告標成未執行，不填成測試失敗。',
  '能讀回覆還不夠，還要確認有相對應的執行紀錄。'], ['C19'], undefined, 'Codex troubleshooting · 2026-10-11');
table('failure-test-code', '測試退出碼 1，保留完整上下文', ['需要留下','原因'], [
  ['執行命令與日期','確認是同一次測試'], ['測試名與失敗位置','找到斷言'],
  ['預期與實際','知道差在哪裡']], [
  '測試失敗時，保留命令和失敗位置，不只截紅色訊息。',
  '預期和實際能幫你確認，是資料差異還是環境問題。',
  '本課已知有一個待實作位置，先解讀再決定要不要改。'], ['C13','C18']);
list('failure-web-start', '頁面能看，按鈕卻沒反應', ['先核對是否 file://', '改用本機伺服器網址', '再看模組與事件，不先改樣式'], [
  '如果看得到頁面，按鈕卻沒反應，先看網址開頭。',
  '先用本機伺服器重做，再決定是不是程式問題。',
  '只看到外觀正常，不能證明瀏覽器程式已經載入。'], ['C07','C18']);
table('failure-port-in-use', '連接埠已占用，不要混到另一份網站', ['選擇','要一起改'], [
  ['停止自己原本的練習伺服器','再於這份 start 啟動'], ['改用其他本機連接埠','命令、網址與保存來源']], [
  '如果連接埠被占用，先確認是不是自己的上一個練習。',
  '換連接埠也可以，但網址要一起改，保存來源也會換。',
  '瀏覽器若還開著舊站，測到的就不是這份起點。'], ['C09','C14','C18']);

card('transfer-task', 'steps', {title:'換題：自己重做一次兩版比較', steps:[
  {title:'準備',detail:'start、reference 各用全新副本'}, {title:'情境',detail:'分別執行相同的核心測試'},
  {title:'交付',detail:'說明差異，寫第 03 課的窄範圍交接'}], source:'01 變式 · 獨立練習'}, [
  '現在不看前面的報告，自己重做一次兩版比較。',
  '各用全新副本跑同一個命令，先寫預測，再看結果。',
  '最後說明差異，交出第三課能接手的範圍和驗收。'], ['C20'], '把方法用到自己的問題');
list('transfer-what-to-look-for', '換題時，要找的證據', ['哪份副本跑出哪個退出碼？', '哪個檔案和斷言解釋差異？', '已驗證、推論、未執行能分開嗎？'], [
  '先把每份目錄和退出碼對上，別只抄最後的數字。',
  '再用檔案和斷言解釋，為什麼只有起點有這個紅燈。',
  '沒有操作過的那一層，就老實列入尚未驗證。'], ['C20']);
list('report-self-check', '交出去以前，自己讀一次', ['檔案用途能指回來源', '每個實測都有命令、結果、版本', '下一輪範圍與驗收可直接照做'], [
  '交報告前，逐句確認它能不能指回來源和操作。',
  '如果只有感覺正常，就再補一個能核對的具體結果。',
  '下一輪任務能直接照做，才算把這次檢查交完整。'], ['C10','C20']);
card('outro', 'bullets', {title:'有基線，下一次修改才看得懂', items:['五檔責任地圖','2 通過 1 失敗的基線','有範圍、有驗收的下一輪任務'], source:'01 CLI · 本課交付'}, [
  '這次留下五檔責任地圖，以及兩個通過、一個失敗的基線。',
  '你最常遇到的是工作目錄、測試判讀，還是網頁開啟問題？',
  '訂閱後，接著用同一專案，把需求收斂成能驗收的任務。'], ['C01','C03']);

const doc = { schema_version:1, slug:'codex-practical-01-cli', format:'slides', category:'tutorial',
  target_minutes:[12,18],
  voice:{provider:'gemini',name:'Sulafat',style:'Relaxed, conversational tech explainer talking to a friend, in Taiwan Mandarin with a natural Taiwanese accent. Natural rise and fall in intonation, light emphasis on key words, never flat or like reading a script. Medium-brisk pace.'},
  youtube:{category_id:27,made_for_kids:false,default_language:'zh-TW',
    title:'Codex 實作 01 CLI：讀懂專案與測試，別把「跑完」當成「做對」',
    description:'用同一個待辦網站起點，實際讓 Codex CLI 執行只讀檢查：讀五份檔案、跑核心測試、解讀兩個通過與一個失敗，再把問題寫成有範圍、有驗收的下一輪任務。\n\n本片以教學卡片重現真實 exec 事件與工具輸出；不是原生 App 或 TUI 螢幕錄影。模型這輪沒有修改程式，也沒有啟動瀏覽器。網站操作與 reference 的三個通過測試是作者另外執行的參考驗證，來源分別標示。\n\n跟做材料：codex-practical-01-materials.zip，完整解壓後依 README 進入 start。reference 是作者提供的參考實作；challenge 是換題練習。教材取得連結需在交付套件完成後補入。\n\n實跑日期：2026-10-11（台灣時間）。Codex CLI 0.162.0-alpha.17.2；核心測試 Node.js v24.13.0。版本可能不同，執行前用本機 --help 核對。',
    tags:['Codex','Codex CLI','實作教學','測試','待辦網站'],video_id:null},
  thumbnail:{template:'thumb',data:{headline:'**跑完≠做對**',tag:'CODEX 實作 01 CLI'}},
  sources:[
    {title:'Codex CLI',url:'https://learn.chatgpt.com/docs/codex/cli',checked_on:'2026-10-11'},
    {title:'Codex CLI reference',url:'https://learn.chatgpt.com/docs/cli/reference',checked_on:'2026-10-11'},
    {title:'Codex non-interactive mode',url:'https://learn.chatgpt.com/docs/non-interactive-mode',checked_on:'2026-10-11'},
    {title:'Codex best practices',url:'https://learn.chatgpt.com/docs/learn/best-practices',checked_on:'2026-10-11'},
    {title:'Codex troubleshooting',url:'https://learn.chatgpt.com/docs/reference/troubleshooting',checked_on:'2026-10-11'},
    {title:'Python http.server',url:'https://docs.python.org/3/library/http.server.html',checked_on:'2026-10-11'},
    {title:'MDN JavaScript modules',url:'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules',checked_on:'2026-10-11'},
    {title:'MDN localStorage',url:'https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage',checked_on:'2026-10-11'}],
  assets:[], subtitles:{burn_in:false}, scenes };
writeFileSync(new URL('./video.json', import.meta.url), JSON.stringify(doc,null,2)+'\n');
const script=['# Codex 實作 01 CLI：讀懂專案與測試', '',
  '作者來源稿｜教學卡片重現真實 exec 檢查紀錄；當前實測與驗收狀態見 PRODUCTION-STATE.md。',
  '旁白及字幕以 video.json 為單一來源。本檔由 authoring.mjs 同步產生。', ''];
for (const scene of scenes) {
  script.push(`## ${scene.id}${scene.chapter ? '｜'+scene.chapter : ''}`, '',
    `畫面：${scene.template}｜依據：${scene.claims.join('、')}`, '');
  for (const line of scene.lines) script.push(`- ${line.id}｜${line.text}`);
  script.push('');
}
writeFileSync(new URL('./script.md', import.meta.url), script.join('\n').trimEnd()+'\n');
console.log(JSON.stringify({scenes:scenes.length,lines:scenes.reduce((n,s)=>n+s.lines.length,0)}));
