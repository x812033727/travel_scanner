import {readFileSync,writeFileSync,mkdirSync,readdirSync,existsSync,mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,join,dirname} from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';
const repo=resolve(dirname(fileURLToPath(import.meta.url)),'../..');
export const sourceRoot=join(repo,'docs/videos/codex-practical-series/materials/source');
const read=name=>readFileSync(join(sourceRoot,name),'utf8');
const lessons=[
  ['確認目前專案與基準','確認路徑、檔案地圖、執行既有測試；把失敗當作觀察，不先改程式。','只讀五個專案檔與 core.test.mjs；交檔案地圖與原始測試結果。','completed 篩選仍是錯的，辨認 actual/expected。','reference 是作者先寫好的完整版本，不代表你已修好 start。'],
  ['把需求變成 Plan','把搜尋需求寫成案例、檔案範圍、驗收及還原計畫，保持程式不變。','只改 docs/task-brief.md、docs/plan.md。先列澄清，再交可審閱計畫；不實作。','需求把搜尋描述為模糊的「更好用」，以具體輸入/輸出補足。','以 Read/read、空白查詢、中文與組合篩選鎖定案例。'],
  ['篩選與搜尋','實作三種篩選及忽略大小寫、首尾空白的標題搜尋。','只改 core.mjs；先執行既有及 feature 測試，保存順序、ID、原始資料。','搜尋省略 trim，輸入「  Read 」找不到。','visibleTasks 先用 query.trim().toLocaleLowerCase()，再用 filter 返回新陣列。'],
  ['AGENTS 與檔案規則','把專案規則放入可被核對的檔案，不把設定檔當自動測試。','只改 AGENTS.md、docs/data-contract.md；記錄載入範圍並對照現有資料契約。','附了一份要求以 title 識別資料的候選規則，指出衝突。','規則須以 ID 區分同名項目；驗證命令與結果另記。'],
  ['重現同名刪除故障','建立同名不同 ID 的最小案例，修正刪錯兩筆的問題。','只改 core.mjs；先以兩筆 Read 重現，再使 identity 測試通過。','三筆同名任務只刪指定 ID，其他仍存在。','removeTask 必須比較 task.id 與傳入 id，不找 title 再刪整群。'],
  ["寫會抓出問題的測試","抓出 All 原地 reverse、順序改變等原測試沒有測到的錯。","只改 tests/meaningful.test.mjs、core.mjs；start 是 TODO 測試，新需求斷言由你新增，先失敗再修正，不刪原測試。","對凍結輸入呼叫 All；另以混合完成/同名的 Active 確認未顯示任務不變。","freeze + 順序預期都要驗證，All 不能 tasks.reverse()；既有綠燈與 TODO 不代表此需求已驗。"],
  ["審查 diff 與交付","既有核心測試可綠，仍靠 diff 與真實 DOM 操作抓出文字被解析為 HTML。","先只讀 app.mjs、core.mjs 與既有測試，寫 docs/review.md；修復只改 app.mjs，不改既有測試。","標題為 <img src=x> 應是文字；真正瀏覽器驗 DOM，儲存與其他功能仍保留。","title.textContent 保留文字；核心測試未涵蓋 DOM，不用 keyword 測試代替畫面證據。"],
  ['Git、PR 說明與還原','在獨立練習庫做分支、選擇性暫存、PR 說明、revert。','讀 docs/git-lab.md；用 node git-lab.mjs 在暫存庫跑流程，不 push。','工作目錄和 staged 檔案不同時，先分清再還原指定路徑。','保留獨立 CSS 註記；PR 說明列需求、修改及實際檢查；未提交 GitHub。'],
  ["JSON、CSV 與週報","核對作者提供的 IO 接線，補整批驗證、v1->v2 日期轉換與 CLI 週報契約。","只改 core.mjs、report.mjs，可新增 tests/data-boundary.test.mjs；保留既有測試，非法列不得半批寫入。日期按台北 +08。","固定跨日資料應算在台北 10 月 11 日，而非 UTC 10 月 10 日。","固定週報 5/2/1/1；舊完成時間 null；非法 CSV 整批拒絕，quoted CRLF 原樣保留。"],
  ['響應式與鍵盤操作','修正 900px 最小寬度，實際檢查 390/1280px 與 Tab 焦點。','只改 style.css、index.html；Node 測試之外還需記錄真實瀏覽器觀察。','超長無空白標題也不能撐寬頁面。','移除固定最小寬度，使用換行與 overflow-wrap；保留 label 和 focus-visible。'],
  ['有證据的重構','把 report CLI 的重複統計收回 weeklyReport，而不改輸出。','只改 report.mjs；先保存輸出，再以同一固定資料比對。','把錯誤日期順序傳到 CLI 必須維持相同失敗行為。','report CLI 只解析參數、讀檔、呼叫核心及輸出，不重新實作日期算法。'],
  ['接手與上下文','核對 handoff 的舊假說，記錄已驗證及尚未驗證的事。','只改 docs/handoff.md；重新讀來源和跑檢查，不直接照筆記修 bug。','先前筆記聲稱本週完成 3 項；目前真值是 2。','交接寫輸入版本、實際命令、exit code、真值和下一步；不要捏造執行。'],
  ['可重用驗收 Skill','建立本專案可觸發的 verify-delivery，明確輸入與停止條件。','只改 .agents/skills/verify-delivery/SKILL.md；驗收不得趁機改功能。','練習缺檔與 NOT RUN；原測試不准重寫成綠燈。','frontmatter 的 name/description 寫使用情境；命令、真值與人工檢查均可照做。'],
  ['唯讀 MCP','啟動本機 stdio MCP，列資源、讀取週報、拒絕寫入。','讀 mcp-server.mjs、docs/mcp-lab.md；測試只碰虛構 fixture。','要求 write_task 或 ../../ 路徑必須拒絕，fixture 雜湊不變。','固定 URI practice://tasks、practice://weekly-report；工具 list_tasks/read_weekly_report。'],
  ['隔離 worktree','用兩個工作樹分別交付介面說明與 --compact 週報功能，再整合。','讀 docs/worktree-lab.md；A 只改 index.html；B 只改 report.mjs、tests/report-compact.test.mjs；整合前看 diff。','兩個分支改同一句介面說明，重現衝突後保留雙方需求；CSS KEEP-MY-NOTE 仍留原 checkout。','A 加入「搜尋會與目前狀態篩選一起套用。」；B 增加 --compact 單行 JSON 加 LF，預設 pretty、5/2/1/1 與來源不變。'],
  ['分工與獨立分析','派兩個代理分別分析資料測試與畫面，合併有證據的發現。','用 docs/subagent-lab.md 的提示；分析僅讀檔、提可重現問題，不同時改核心。','兩份分析意見不同時用測試/原文裁決，不以票數決定。','主代理先定輸入/輸出/範圍，再獨立驗證建議；未跑代理需明示。'],
  ["排程／批次週報","App 實際設定排程，CLI 一次 exec 保留紀錄並驗證來源真值。","CLI 先 node exec-run.mjs --dry-run；支援 --input、--from、--to，真跑需登入與 native codex。App 讀 docs/app-schedule.md。","新 run 改為台北2026-10-12..18，完成0/unknown1；另用缺檔 input 留失敗收據且不呼叫provider。錯數3/timeout是補充驗證器案例。","每次新 run；status/input 保存實際參數與來源hash，verify獨立計算；缺檔preflight_failed、舊run保留、不自動重跑。"],
  ["封存、CI 與還原專題","從 TODO scaffold 自行實作日期封存，再完成預覽、備份、CI 例子與還原。","只改 core.mjs、archive.mjs、restore.mjs、.github/workflows/practice.yml，可新增 tests/archive-boundary.test.mjs；不改既有測試，來源不覆寫。","cutoff 相等可封存；unknown/pending 保留；壞備份不得產生新結果。","先 preview old 一筆，apply 到新目錄備份與結果，restore 到新檔核對原文。"],
];
const procedures=[
  ['完整解壓本包；在 start 核對五個檔名、Get-Location/pwd、node --version。','執行 node --test core.test.mjs，記錄3 tests/2 pass/1 fail及exit1。','讀 core.test.mjs 第17行的 Active預期[b]與實際[a,b]，對照visibleTasks。','目前位置為 start；照 ../baseline-prompt.txt 送出只讀檢查，將模型報告與自己測試分開保存。','在另一個终端機用本機HTTP預覽新增Read/Build、勾選Read、reload；未操作寫NOT RUN。','到reference再跑同一命令；challenge找出Completed失敗與start不同。','只交檔案地圖、已知缺口及第03課的函式範圍/驗收，不改實作。'],
  ['在start跑node --test，確認本課資料是v1、程式保持不變。','讀docs/task-brief.md，把更好用拆成Read/read、空白、中文、狀態交集的例子。','在Codex進Plan，先問會改變規格的問題，寫輸入與完成條件。','把順序、同名ID、儲存值保留列為限制；只列core與新測試為下一輪範圍。','把步驟、測試、人工驗收與還原寫入docs/plan.md；本課不實作。','用challenge的模糊需求再寫一份計畫；最後才比對作者reference。'],
  ['跑node --test，保存現有篩選與搜尋失敗。','讀index選單與app事件，確認控制項已存在，修改範圍為core。','先寫三種filter、trim/case/中文、空查詢與同名ID的預期。','只實作visibleTasks，返回新清單、保留順序及原資料。','同一測試重跑到綠，再用HTTP畫面檢查搜尋與篩選交集。','challenge輸入「  Read 」重現trim缺口，再說明修正理由。'],
  ['先讀當前v1資料契約及core，不把候選規則當正確來源。','將只改指定檔、ID識別、原測試保留、無依賴與真實檢查寫入AGENTS.md。','在本課新聊天確認Codex實際讀到的規則範圍，保留真正回覆。','用docs/rules-review.md覆核title唯一的候選說法，指出與兩筆Read衝突。','跑node --test；規則檔改善不等於已執行瀏覽器或功能修復。','輸出規則的用途、載入範圍、此次檢查與NOT RUN。'],
  ['建立三筆同名Read但ID a/b/c，指定刪b；先寫預期[a,c]。','跑tests/identity.test.mjs，確認錯版依title把同名全部刪掉。','讀removeTask與app傳入id，將錯誤限定到刪除條件。','只改core的ID比較；同一重現與全部node --test都重跑。','HTTP畫面確認刪其中一筆仍留下另一筆，未操作不得記PASS。','challenge使用完成狀態不同的三筆同名項目，仍只刪指定ID。'],
  ["先跑start既有測試：可綠但meaningful只有TODO，不能宣稱已驗All原地reverse。","在tests/meaningful.test.mjs自己寫[a,b,c]顺序、原輸入與Object.freeze斷言。","只加測試，先跑出真正失敗；保留原測試/輸出，不倒轉預期或刪斷言。","再修core使All保序且不修改輸入；各filter空清單一起核對。","重跑同一回歸與完整node --test，解釋新測試抓的是使用者要求。","challenge用混合完成/同名的Active核對未顯示任務不變；作者強案例不冒充這輪學生撰寫。"],
  ["先跑既有Node核心，綠燈仍沒有DOM驗收。","讀候選app的title.innerHTML，對照需求只要標題文字。","HTTP新增<img src=x>，核對img元素與可見文字，保存修前故障。","列问题到docs/review.md；只改app回textContent，保持事件/ID/儲存。","重跑核心；HTTP另驗literal文字、reload及同名刪除，未跑UI記NOT RUN。","最後核對必要diff；不新增keyword字串測試冒充DOM驗收。"],
  ['先讀docs/git-lab.md，確認是獨立練習庫、不含正式遠端。','跑node git-lab.mjs，讀當次真的Git結果；腳本在暫存庫完成並清理。','手動另建全新庫，提交baseline，建立codex/title-practice分支。','改index標題並留獨立CSS註記，只stage index；對照cached與worktree差異。','提交index後revert；核對歷史3 commits、原標題恢復且CSS註記保留。','寫docs/pull-request.md包含問題、修改與實際驗證；未開PR明示。'],
  ['讀v1/v2契約、fixtures/legacy-v1.json與UTC完成時間；未知維持null。','執行node --test，重現本課把台北日期誤當UTC造成的週報錯數。','整批驗證JSON/CSV，再合併；用invalid.csv證明原清單不會半批變動。','修台北+08日曆邊界，10月10日22:00Z應算10月11日。','跑node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11；核對5/2/1/1。','HTTP匯入固定JSON、匯出CSV再讀回；重複ID整批拒絕。'],
  ['先跑Node資料測試，然後真正開HTTP；它們不是畫面驗收。','把視窗調390px，觀察main的900px min-width造成水平溢出。','只修CSS/必要HTML，保留label、button與focus-visible。','在390px和1280px實際檢查長標題、搜尋、匯入表單、Tab與刪除後焦點。','把結果填入docs/browser-acceptance.md；沒跑的格保持NOT RUN。','challenge加長中文與無空白字串，不能撐寬畫面。'],
  ['保存report CLI對固定資料的原JSON輸出及exit code。','讀report.mjs的重複統計，找出核心已有weeklyReport。','把CLI保留參數、读檔、呼叫核心與輸出；不重複日期算法。','同一fixture與日期跑重構前後，逐欄比對結果。','以日期倒序、非法文件、已存在輸出檢查失敗行為與來源保留。','最後跑node --test並交只含report範圍的diff。'],
  ['讀docs/handoff.md的完成3項假說，不先改來源。','讀fixtures及契約，跑report得到5/2/1/1；確認UTC22:00跨台北日期。','用同一資料跑node --test，保存版本與實際exit code。','把「已驗證、假說、未驗證、下一步」分欄寫新handoff。','在獨立新聊天只給目前檔案與交接，要求重新核對而非信任舊數字。','challenge說明為何不能把boundary日期改成符合舊筆記。'],
  ['讀本課驗收清單，確認技能只適用Small Steps交付檢查。','在.agents/skills/verify-delivery/SKILL.md寫name/description、輸入、命令、真值與停止條件。','從本專案新聊天呼叫verify-delivery，保存實際讀到的技能與檢查。','要求只驗收、不修功能，PASS/FAIL/NOT RUN都有來源與命令。','用另一個缺core的空練習目錄測缺檔回報，不改全域技能。','最後比對作者reference：是否能照做、是否偷偷重寫測試。'],
  ['先跑node --test tests/mcp.test.mjs，證明stdio、只讀清單與拒絕寫入。','讀docs/mcp-lab.md，用node mcp-server.mjs啟動；輸入initialize/resources/list/read請求。','確認URI兩項與tool兩項，read_weekly_report回5/2/1/1。','用當前Codex MCP入口註冊本課絕對server路徑並讀回；未連成功明示。','真正經MCP讀fixture或report，保存工具結果；要求write_task與外部路徑應拒絕。','核對fixture原文/雜湊不變，停止本課server。'],
  ['複製整課到全新Git練習庫，提交baseline；不在正式庫操作。','依docs/worktree-lab.md建立practice-ui與practice-report兩路，記錄各自路徑/分支/狀態。','A只改index.html加入可見篩選說明；B只改report.mjs並新增tests/report-compact.test.mjs。','B先寫單行/預設pretty/數字與來源不變的測試，再實作--compact；兩路各跑node --test。','主庫留KEEP-MY-NOTE，證明新worktree不帶入未提交註記且原檔保留。','逐路只暫存指定檔再提交；回主庫cherry-pick並實測新介面與兩種報表輸出。','challenge兩路改同一句UI說明，保留衝突輸出、手動保留雙方需求再驗收；乾淨且保存成果才移除明確工作樹。'],
  ['先讀docs/subagent-lab.md，寫輸入、只讀範圍與兩份獨立輸出路徑。','A分析資料/測試/日期；B分析HTML/互動/CSS/storage，兩者不得改core。','在App或CLI可用入口實際派發；沒有入口用獨立聊天並正確標示。','將真實結果存analysis-data/UI，不複製作者示例冒充代理結果。','主代理重現每個可操作問題；舊claim3以fixture真值2裁決。','Browser沒跑的結果保持NOT RUN；只採納已核對發現。'],
  ["先手動執行report CLI得到5/2/1/1；固定期間不是今天動態本週。","CLI先node exec-run.mjs --dry-run，核對argv/schema/input/from/to及modelInvoked=false。","已登入才用node exec-run.mjs --run run-01；新目錄保留status/input/prompt/schema/events/final/stderr。","node verify-result.mjs run-01核對退出、完成turn、實際參數及目前來源hash，再獨立計算真值。","變式用--from 2026-10-12 --to 2026-10-18和新run ID；另以--input fixtures/missing.json留preflight_failed收據、不呼叫provider。","App依docs/app-schedule建立週報、讀回設定、核對第一次結果；練習後停用並讀回。","錯數3/timeout的synthetic測試只驗證器單元教學，不冒充模型；不自動重跑。"],
  ['讀資料契約，先寫completed且已知日期<=cutoff、unknown/pending保留、輸入不變的案例。','start 的 archiveTasks 是 TODO/throw scaffold；跑 node --test 保留 archive-not-implemented，自己實作新功能。','驗證cutoff格式、驗資料、按ID保持順序分類；不要讀reference後整包覆蓋。','preview：node archive.mjs fixtures/tasks.json --cutoff 2026-10-04T15:59:59.999Z --out archive-run。確認old一筆/retained4/unknown1且無寫入，再加--apply。','核對backup.json原文、archived/retained/receipt；用restore.mjs還原到新檔並逐byte比較。','在自己的練習repo採用CI例子，真的push跑完才記CI PASS；未執行記NOT RUN。','challenge另保留unknown誤封存缺陷；再測cutoff equality、壞備份與既有輸出，來源和舊結果都保留。'],
];
const transferExercises={
  1:{prompt:'主變式：不讀前一輪報告，用全新 start/reference 重跑同一 node --test core.test.mjs，解釋差異並交第03課範圍。另做 challenge：只讀診斷 Completed 失敗，不實作。',answer:'主變式真相：start 3 tests/2 pass/1 fail/exit1，停第17行 Active，actual[a,b]、expected[b]；reference 3 pass/0 fail/exit0。challenge 也是2/1/exit1，但 Active 通過，停第18行 Completed，actual[b]、expected[a]；第19–20行未跑到。下一輪只實作 visibleTasks、保留既有測試與瀏覽器檔案；三filter/空清單/順序/輸入不變及HTTP另外驗收，01本身不修功能。'},
  3:{prompt:'保留教材 challenge 的「  Read 」trim 缺口。課綱補充：新增 id=report-a「寫報告」未完成、report-b「報告校對」已完成、lunch「買午餐」未完成；查詢「 報告 」分別用 All/Active/Completed，先預測 IDs/count，再加自己的Unicode斷言及實際畫面。',answer:'教材trim案例：feature測試資料 a=Read完成、b=Build未完成、c=Read完成；「  READ 」+Completed 應[a,c]、2項，Active應[]。課綱中文變式：「 報告 」+All=[report-a,report-b]/2；Active=[report-a]/1；Completed=[report-b]/1。lunch不匹配，原三筆資料、ID、完成狀態與順序均不变；xyz無結果但不刪資料，空查詢依狀態顯示。只有core綠燈時UI仍NOT RUN。'},
  5:{prompt:'教材挑戰：三筆同名Read，ID a/b/c，只有b完成；刪b應保留a/c。課綱補充：a/b同名「寫報告」、a未完成/b完成、c「買午餐」未完成；搜尋「報告」+Active，刪畫面中的a，再回All；不要把畫面位置當原始索引。',answer:'教材identity真相：removeTask(input,b)回[a,c]，原input仍[a,b,c]且b.completed=true。課綱篩選後刪除：visibleTasks(input,active,報告)只回[a]；以該項id=a呼叫removeTask(input,a)，回[b,c]，b仍同標題且completed=true，c不變、順序仍b先c後。原input仍[a,b,c]。若刪a/b兩筆則是title身分缺陷；禁止同名不是修復。瀏覽器仍需另做此操作與reload。'}
};
function put(root,name,body){const target=join(root,name);mkdirSync(dirname(target),{recursive:true});writeFileSync(target,name.endsWith('.md')?body.toString().trimEnd()+'\n':body);}
function files(root){return readdirSync(root,{withFileTypes:true}).flatMap(item=>item.isDirectory()?files(join(root,item.name)).map(name=>item.name+'/'+name):[item.name]);}
function replaceFunction(body,name,replacement){const begin=body.indexOf('export function '+name+'(');if(begin<0)throw new Error('Missing '+name);let end=body.indexOf('\nexport function ',begin+1);if(end<0)end=body.length;return body.slice(0,begin)+replacement+'\n'+body.slice(end);}
const featureTests=`import test from 'node:test';import assert from 'node:assert/strict';import {visibleTasks} from '../core.mjs';
const tasks=[{id:'a',title:'Read',completed:true},{id:'b',title:'Build',completed:false},{id:'c',title:'Read',completed:true}];
test('feature: trim case-insensitive search combined with filters',()=>{assert.deepEqual(visibleTasks(tasks,'completed','  READ ').map(t=>t.id),['a','c']);assert.deepEqual(visibleTasks(tasks,'active','read'),[]);});
test('feature: Unicode and empty query preserve order',()=>{const input=[{id:'z',title:'寫週報',completed:false},...tasks];assert.deepEqual(visibleTasks(input,'all','週報').map(t=>t.id),['z']);assert.deepEqual(visibleTasks(input,'all','').map(t=>t.id),['z','a','b','c']);});\n`;
const identityTest=`import test from 'node:test';import assert from 'node:assert/strict';import {removeTask} from '../core.mjs';
test('identity: delete exactly one same-title ID',()=>{const tasks=[{id:'a',title:'Read',completed:false},{id:'b',title:'Read',completed:true},{id:'c',title:'Read',completed:false}];assert.deepEqual(removeTask(tasks,'b').map(t=>t.id),['a','c']);assert.equal(tasks.length,3);});\n`;
const meaningfulTest=`import test from 'node:test';import assert from 'node:assert/strict';import {visibleTasks} from '../core.mjs';
test('meaningful: All keeps order',()=>{const tasks=[{id:'a',title:'A',completed:false},{id:'b',title:'B',completed:true}];assert.deepEqual(visibleTasks(tasks,'all').map(t=>t.id),['a','b']);assert.deepEqual(tasks.map(t=>t.id),['a','b']);});
test('meaningful: frozen input is not changed',()=>{const tasks=Object.freeze([Object.freeze({id:'a',title:'A',completed:false}),Object.freeze({id:'b',title:'B',completed:true})]);assert.deepEqual(visibleTasks(tasks,'all'),tasks);});\n`;
function copyBaseline(root,variant){for(const name of files(join(sourceRoot,'baseline-'+variant)))put(root,name.replace(/\.fixture$/,''),readFileSync(join(sourceRoot,'baseline-'+variant,name)));}
function createSnapshot(root,id,variant){
  mkdirSync(root,{recursive:true});
  if(id===1){copyBaseline(root,variant==='reference'?'expected':variant==='challenge'?'broken':'start');return;}
  for(const name of files(sourceRoot)){
    if(name.startsWith('baseline-') || name.endsWith('.fixture'))continue;
    if(id<9 && (name.startsWith('fixtures/') || name.startsWith('tests/') || ['core.mjs','core.test.mjs','report.mjs','archive.mjs','restore.mjs','mcp-server.mjs','exec-run.mjs','verify-result.mjs'].includes(name) || name.startsWith('.github/')))continue;
    if(id<14 && (name==='mcp-server.mjs'||name==='tests/mcp.test.mjs'))continue;
    if(name==='tests/report-compact.test.mjs' && (id<15 || (id===15 && variant!=='reference')))continue;
    if(id<17 && (['exec-run.mjs','verify-result.mjs','tests/automation.test.mjs'].includes(name)))continue;
    if(id<18 && (name==='archive.mjs'||name==='restore.mjs'||name==='tests/report.test.mjs'||name.startsWith('.github/')))continue;
    if(id<13 && name.startsWith('.agents/'))continue;
    if(id<4 && name==='AGENTS.md')continue;
    put(root,name,readFileSync(join(sourceRoot,name)));
  }
  if(id<9){
    put(root,'index.html',read('index.html').replace('v2 重設寫入空文件，保留舊 v1 與其他儲存鍵。','重設僅移除本教材專用儲存鍵，其他儲存鍵保留。'));
    let core=read('baseline-expected/core.mjs.fixture');
    if(id>=3)core=replaceFunction(core,'visibleTasks',`export function visibleTasks(tasks, filter='all', query='') {
  const needle=String(query).trim().toLocaleLowerCase();
  return tasks.filter(task=>(filter==='active'?!task.completed:filter==='completed'?task.completed:true) && task.title.toLocaleLowerCase().includes(needle));
}`);
    put(root,'core.mjs',core);put(root,'core.test.mjs',read('baseline-expected/core.test.mjs.fixture'));
    if(id>=3)put(root,'tests/feature.test.mjs',id===6&&variant==='start'?featureTests.replace(/test\('feature: Unicode[^\n]*\n?/,''):featureTests);
    if(id>=5)put(root,'tests/identity.test.mjs',identityTest);
    if(id>=6)put(root,'tests/meaningful.test.mjs',id===6&&variant==='start'?"import test from 'node:test';\ntest.todo('TODO: add All order, original input and frozen input regression before fixing core');\n":meaningfulTest);
    put(root,'fixtures/tasks.json',JSON.stringify({version:1,tasks:JSON.parse(read('fixtures/tasks.json')).tasks.map(({id,title,completed})=>({id,title,completed}))},null,2)+'\n');
  }
  put(root,'lesson-config.mjs',`export const lesson=${id};\nexport const features={search:${id>=3},data:${id>=9},archive:${id>=18}};\nexport const storageKey='mokaair-codex-practical-v${id>=9?2:1}';\n`);
  if(id<15 || (id===15 && variant!=='reference')){
    put(root,'index.html',readFileSync(join(root,'index.html'),'utf8').replace('<p id="filter-hint">搜尋會與目前狀態篩選一起套用。</p>\n',''));
    if(id>=9)put(root,'report.mjs',read('report-basic.mjs.fixture'));
  }
  if(id<9){
    put(root,'README.md',`# Small Steps 第 ${id} 課專案\n\n作者編寫的獨立練習複本，未聲稱是模型執行成果。只有本機 HTML/CSS/JavaScript，無 npm、登入、後端。\nNode22+：node --test。Windows：py -m http.server 4173 --bind 127.0.0.1；macOS/Linux：python3 -m http.server 4173 --bind 127.0.0.1。瀏覽 http://127.0.0.1:4173，Ctrl+C 停止。不要雙擊 HTML。\n\nindex.html 是頁面，app.mjs 是互動，core.mjs 是資料操作，storage.mjs 是儲存失敗 adapter。資料為 v1：id/title/completed，ID 唯一、同名標題允許。儲存鍵 mokaair-codex-practical-v1；暫存資料損毀時原值保留。第9課才教 completedAt、JSON/CSV 匯入匯出与 CLI 週報，這份複本尚無那些入口。\n\n從本課外層 README.md、prompts.md、acceptance.md 讀任務；解答另在 answers.md。\n`);
    put(root,'docs/data-contract.md','# 本課 v1 資料契約\n文件 version=1；每項 id/title/completed。ID 唯一，title 可同名且須1..100非空白字元，completed是真正布林。\n篩選、搜尋、刪除以 ID 保持資料與順序；不可以title當唯一值。不得刪測試、改成含糊成功條件。\n儲存鍵 mokaair-codex-practical-v1，資料損毀時原值保留，禁止 localStorage.clear()。\n');
    put(root,'docs/handoff.md','# 本課複本交接\n本複本尚未執行檢查。先確認資料夾、讀 v1 契約和 core.mjs，再跑 node --test。\n不要把作者預期當实际結果；紀錄 PASS/FAIL/NOT RUN 及命令/退出碼。\n');
  }else if(id<18){const body=read('README.md'),begin=body.indexOf('## 封存與還原'),end=body.indexOf('## 人工瀏覽器');put(root,'README.md',body.slice(0,begin)+body.slice(end));}
  if(id<15 || (id===15 && variant!=='reference')){
    const body=readFileSync(join(root,'README.md'),'utf8'),begin=body.indexOf('## 單行週報'),end=body.indexOf('\n## ',begin+1);
    if(begin>=0)put(root,'README.md',body.slice(0,begin)+(end>=0?body.slice(end):''));
    if(id>=9)put(root,'docs/data-contract.md',readFileSync(join(root,'docs/data-contract.md'),'utf8').replace('第15課的 --compact 只改 JSON 呈現：單行加LF；預設仍兩空格pretty，日期規則和數字不變。\n',''));
  }
  const defective=variant!=='reference';
  let core=readFileSync(join(root,'core.mjs'),'utf8');
  if(defective&&id===3)core=variant==='start'?replaceFunction(core,'visibleTasks','export function visibleTasks(tasks,filter,query) { return tasks; }'):core.replace('String(query).trim().toLocaleLowerCase()','String(query).toLocaleLowerCase()');
  if(defective&&id===5)core=replaceFunction(core,'removeTask',`export function removeTask(tasks,id) { const title=tasks.find(task=>task.id===id)?.title; return tasks.filter(task=>task.title!==title); }`);
  if(defective&&id===6)core=core.replace("return tasks.filter(task=>", "if(filter==='all' && !query) return tasks.reverse();\n  return tasks.filter(task=>");
  if(defective&&id===9)core=core.replace("return utc - 8 * 60 * 60 * 1000;","return utc; // EXERCISE: this UTC boundary is wrong for Taipei calendar dates.");
  if(id===18 && variant==='start')core=replaceFunction(core,'archiveTasks',`export function archiveTasks(tasks, cutoff) {
  // TODO: validate cutoff and source; return ordered archived/retained without mutation.
  // Only completed tasks with a known UTC completedAt <= cutoff may be archived.
  throw new Error('archive-not-implemented');
}`);
  if(id===18 && variant==='challenge')core=core.replace('task.completed && task.completedAt !== null && task.completedAt <= cutoff','task.completed && (task.completedAt === null || task.completedAt <= cutoff)');
  put(root,'core.mjs',core);
  if(defective&&id===7){let app=readFileSync(join(root,'app.mjs'),'utf8');put(root,'app.mjs',app.replace('title.textContent=task.title','title.innerHTML=task.title'));}
  if(defective&&id===10)put(root,'style.css',read('style.css')+'\n/* EXERCISE: intended mobile defect */\nmain{min-width:900px}\n');
  if(defective&&id===11){let report=read('report-basic.mjs.fixture');report=report.replace('const result = weeklyReport(tasks, options.from, options.to);',`// EXERCISE: duplicate the implementation here; consolidate without changing output.
  const boundary=date=>{if(typeof date!=='string'||!/^\\d{4}-\\d{2}-\\d{2}$/.test(date))throw new Error('calendar-date');
    const utc=Date.parse(date+'T00:00:00.000Z');if(!Number.isFinite(utc)||new Date(utc).toISOString().slice(0,10)!==date)throw new Error('calendar-date');return utc-8*60*60*1000;};
  const begin=boundary(options.from),end=boundary(options.to)+86400000;
  if(begin>=end)throw new Error('date-order');
  const result={revision:'weekly-report-v2',timezone:'Asia/Taipei',weekStart:options.from,weekEnd:options.to,total:tasks.length,
    completedInWeek:tasks.filter(t=>t.completed&&t.completedAt&&Date.parse(t.completedAt)>=begin&&Date.parse(t.completedAt)<end).length,
    pending:tasks.filter(t=>!t.completed).length,unknownCompleted:tasks.filter(t=>t.completed&&t.completedAt===null).length};`);put(root,'report.mjs',report);}
  writeLessonArtifacts(root,id,variant);
}
function writeLessonArtifacts(root,id,variant){
  const reference=variant==='reference';
  if(id===2){put(root,'docs/task-brief.md',reference?'# 任務需求\n搜尋首尾空白及大小寫都忽略；中文可找；與狀態篩選交集。只規劃，不修改程式。\n':'# 任務需求\n搜尋要更好用。請先將模糊需求轉成可驗收案例，不修改程式。\n');put(root,'docs/plan.md',reference?'# 作者參考計畫\n1. 先讀 core/app/index 及現有測試。\n2. 只修改 visibleTasks，保留 ID/順序。\n3. 新增 query；以 Read/read、空查詢、中文、active+Read 驗收。\n4. 先保存原版和失敗；完成後 Node + 瀏覽器；不加入框架。\n':'# 計畫待填\n請列問題、輸入/輸出案例、檔案範圍、驗收與还原。\n');}
  if(id===4)put(root,'docs/rules-review.md',reference?'# 規則覆核\n以 ID 區分資料，title 可重複。已核對原始碼；尚未執行模型。\n':'# 待覆核候選規則\n候選說法：「title 可當唯一識別碼」。找出與資料契約的衝突再修規則。\n');
  if(id===7)put(root,'docs/review.md',reference?'# 作者覆核參考\n候選 innerHTML 超出需求、會把任務文字解析成元素；改回 textContent。Node 需重跑，瀏覽器 literal-markup 測試另記。\n':'# 覆核待填\n先列候選 diff 的需求、風險、案例，再修正。不能只寫「tests pass」。\n');
  if(id===8){put(root,'docs/git-lab.md',gitInstructions);put(root,'git-lab.mjs',gitScript);put(root,'docs/pull-request.md',reference?'# PR 描述作者範例（尚未提交 GitHub）\n更正示範頁標題；只提交 index.html，獨立 CSS 註記保留在工作目錄。驗證分支、staged diff 及 Node；revert 保留歷史。\n':'# PR 描述待填\n問題、最後行為、實際測試、未驗證事項。請先在 isolated Git lab 做出可審查改動。\n');}
  if(id===10)put(root,'docs/browser-acceptance.md','# 瀏覽器驗收記錄\n390px: NOT RUN\n1280px: NOT RUN\nTab 焦點: NOT RUN\n同名 ID/重新整理/匯入拒絕: NOT RUN\n填入實際觀察與日期，不能將作者 CSS 當已錄影。\n');
  if(id===12)put(root,'docs/handoff.md',reference?'# 作者交接參考，不是本複本執行紀錄\n來源 fixtures/tasks.json v2，已知真值 total5/completedInWeek2/pending1/unknown1。跨日 UTC22:00 屬次日台北。\n本複本已執行：無。請重新跑 node --test、report CLI，再填入實際 exit code。瀏覽器與產品 UI 尚未測。\n':'# 過時交接（刻意練習）\n未驗證說法：本週完成應是 3。有人說把 boundary 日期往前調就會符合。\n請先讀資料契約重新驗證，不能照筆記更改來源。\n');
  if(id===13&&!reference)put(root,'.agents/skills/verify-delivery/SKILL.md','---\nname: verify-delivery\ndescription: TODO define project and trigger\n---\n# 驗收技能待完成\nTODO: inputs, checks, stopping rules, PASS/FAIL/NOT RUN。不得重寫測試。\n');
  if(id===14)put(root,'docs/mcp-lab.md',mcpInstructions);
  if(id===15){put(root,'docs/worktree-lab.md',worktreeInstructions);
    put(root,'docs/worktree-result.md',reference?'# 作者參考交付範圍，非工作樹實跑紀錄\nA：index.html 的 filter-hint 可見提示。B：report.mjs --compact 與 tests/report-compact.test.mjs。\n預設pretty JSON不變，compact單行JSON加LF，兩者真值5/2/1/1、來源不變。\n本複本尚未執行Git、模型或HTTP；須按worktree-lab真正建立、核對、提交與整合。\n':'# 工作樹結果待填\n各路cwd/branch/status、授權diff、test實際exit、commit、整合輸出、HTTP、KEEP-MY-NOTE、衝突及還原。未執行項目NOT RUN。\n');
  }
  if(id===16){put(root,'docs/subagent-lab.md',subagentInstructions);
    put(root,'docs/analysis-data.md',reference?'# 作者分析參考，不是代理输出\n契约：同名ID、原順序、整批拒絕非法資料、未知時間保留。固定fixture5/2/1/1。旧交接「3」與來源不符，應重跑report而不改日期。当前複本 Node 檢查尚未執行。\n':'# 資料代理分析待填\n輸入、預期、實際觀察、重現命令、檔案、未驗證。沒有執行代理就明示。\n');
    put(root,'docs/analysis-ui.md',reference?'# 作者分析參考，不是代理输出\n原始碼使用textContent、label、focus-visible、專用儲存鍵。這些是可讀到的設計，不能當瀏覽器實測。390px/1280px/Tab/reload/損毀值：NOT RUN。應另用實際瀏覽器验证。\n':'# 畫面代理分析待填\n每項附真實觀察或NOT RUN，不能用原始碼推測冒充畫面證據。\n');
  }
  if(id===17){put(root,'docs/app-schedule.md',scheduleInstructions);put(root,'docs/batch-run.md',batchInstructions);}
  if(id===18)put(root,'docs/capstone.md','# 封存交付\nstart 的 archiveTasks 是尚未實作的 TODO/throw scaffold；自己按契約完成新功能。archive/restore CLI 是作者提供接線，不是模型成果。challenge 另有 unknown 誤封存缺陷。\n先檢查 unknown、pending、cutoff equality、backup restore、CLI rerun、來源原文與輸入不變。\n先 preview，再 apply 到新目錄。CI YAML 是可執行範例，未實際 push/檢查前記 NOT RUN。\n驗收來源 fixture：archived=[old]、retained4、unknown1，還原後原文與五項資料都相同。\n');
  put(root,'AUTHORSHIP.md','# 素材來源\n此複本由教材作者建構，含刻意故障或作者參考解答。未聲稱由某次 Codex、代理、MCP、排程或 CI 真實執行產生。\n');
}
const gitInstructions=`# 獨立 Git 練習\n\n執行 node git-lab.mjs；腳本只在作業系統新建的暫存庫操作，不碰目前庫、不設遠端、不 push。輸出是當次實際 Git 狀態。\n手動重現時將本資料夾複製到全新目錄：\n\n\`\`\`text\ngit init -b main\ngit config user.name Practice\ngit config user.email practice@example.test\ngit add index.html style.css core.mjs core.test.mjs app.mjs\ngit commit -m "practice baseline"\ngit switch -c codex/title-practice\n\`\`\`\n修改 index.html 標題；獨立在 style.css 留 KEEP-MY-NOTE。只 git add index.html，核對 git diff 和 git diff --cached。\ncommit 標題改動後先保存 CSS 註記，用 git revert HEAD 做逆向提交；原始碼回到原題但歷史保留。\n只在此 isolated lab 可依實驗要求 git restore -- style.css；真專案先保存與辨認所有權。不要 git reset --hard。\nPR 描述存在 docs/pull-request.md；建立文字檔不等於已開 PR。\n`;
const gitScript=`import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,copyFileSync,rmSync} from 'node:fs';import {tmpdir} from 'node:os';import {join} from 'node:path';import {spawnSync} from 'node:child_process';import assert from 'node:assert/strict';
const container=mkdtempSync(join(tmpdir(),'small-steps-git-')),lab=join(container,'repo');mkdirSync(lab);const config=join(container,'empty.config');writeFileSync(config,'');const env={...process.env,GIT_CONFIG_GLOBAL:config,GIT_CONFIG_NOSYSTEM:'1',GIT_TERMINAL_PROMPT:'0'};for(const key of Object.keys(env))if(key.startsWith('GIT_')&&!['GIT_CONFIG_GLOBAL','GIT_CONFIG_NOSYSTEM','GIT_TERMINAL_PROMPT'].includes(key))delete env[key];
const git=(...args)=>{const run=spawnSync('git',args,{cwd:lab,env,encoding:'utf8'});if(run.status!==0)throw new Error(run.stderr||'Git unavailable');return run.stdout.trim();};
try{for(const name of ['index.html','style.css','core.mjs','core.test.mjs','app.mjs'])copyFileSync(new URL(name,import.meta.url),join(lab,name));git('init','-b','main');git('config','user.name','Practice');git('config','user.email','practice@example.test');git('add','.');git('commit','-m','practice baseline');git('switch','-c','codex/title-practice');const html=readFileSync(join(lab,'index.html'),'utf8');writeFileSync(join(lab,'index.html'),html.replace('完成一件事，留下證據。','完成一件事，核對結果。'));writeFileSync(join(lab,'style.css'),readFileSync(join(lab,'style.css'),'utf8')+'\\n/* KEEP-MY-NOTE */\\n');git('add','index.html');assert.equal(git('diff','--cached','--name-only'),'index.html');assert.equal(git('diff','--name-only'),'style.css');git('commit','-m','update practice title');git('revert','--no-edit','HEAD');assert.equal(readFileSync(join(lab,'index.html'),'utf8'),html);assert.equal(git('diff','--name-only'),'style.css');assert.equal(git('remote'),'');console.log(JSON.stringify({isolated:true,branch:git('branch','--show-current'),commits:Number(git('rev-list','--count','HEAD')),stagedOnly:'index.html',notePreserved:true,reverted:true,remote:false},null,2));}finally{rmSync(container,{recursive:true,force:true});}\n`;
const mcpInstructions=`# 本機唯讀 MCP\n\nnode --test tests/mcp.test.mjs 會真正啟動 stdio 子程序並驗 JSON-RPC，但不代表已連入 Codex。\n手動協定檢查：啟動 node mcp-server.mjs，輸入每行一個 JSON：\n\n\`\`\`json\n{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"practice","version":"1"}}}\n{"jsonrpc":"2.0","id":2,"method":"resources/list"}\n{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read_weekly_report","arguments":{"from":"2026-10-05","to":"2026-10-11"}}}\n\`\`\`\nURI: practice://tasks、practice://weekly-report；工具 list_tasks(noargs)、read_weekly_report(from,to)。write_task 与任意路徑會拒絕。stdout 只輸出協定；Ctrl+C 停止。\n連到 Codex 時，用你版本的 MCP 設定介面註冊 command=node、args=[絕對 mcp-server.mjs 路徑]；CLI 可在確認當前 help 後用 codex mcp add small-steps -- node ABSOLUTE_SERVER_PATH。只在錄製用設定環境示範，讀回列表，再實際讀資源；教材沒有替你安裝全域設定。\n`;
const worktreeInstructions=`# Worktree：介面與報表分開交付

本課 start 尚無新提示或 --compact；reference 是作者完整實作，不是工作樹或模型執行紀錄。從 start 複製全部檔案到全新的 practice-worktree，開終端機在其根目錄操作。下列 ../ 路徑必須尚不存在；若已有練習請換新名稱，不覆寫。不要在正式 repository 照做。

\`\`\`text
git init -b main
git config user.name Practice
git config user.email practice@example.test
git add .
git commit -m "practice baseline"
git worktree add ../practice-ui -b codex/filter-hint
git worktree add ../practice-report -b codex/report-compact
git worktree list
git -C ../practice-ui status --short
git -C ../practice-report status --short
\`\`\`

在原 practice-worktree 的 style.css 手動加 /* KEEP-MY-NOTE */，保持未提交。兩個工作樹的 style.css 不應有此字，原檔仍有；先用 Get-Location/pwd、git branch --show-current、git status --short 核對自己在哪一份。

路線 A 的 Codex 任務：只改 index.html，在搜尋與狀態工具列下方加入可見文字「搜尋會與目前狀態篩選一起套用。」。作者使用 p#filter-hint。維持既有 label、搜尋接線、窄螢幕與資料行為。用真正 HTTP 畫面核對文字及390px；Node測試不證明文字可見。

路線 B 的 Codex 任務：只改 report.mjs，並新增 tests/report-compact.test.mjs。加入無值的 --compact 旗標；stdout 及 --out 都是單行 JSON，加一個尾端 LF。沒有此旗標時維持原兩空格 pretty JSON。固定資料仍 total5/completedInWeek2/pending1/unknownCompleted1；來源不變，既有輸出仍拒絕覆寫。新測試先證明 compact 未實作，再驗預設與 compact 等值、行數、來源保留、重複旗標拒絕。

各路完成後在自己的資料夾跑 node --test，再只暫存授權檔案。以下仍從主 practice-worktree 執行：

\`\`\`text
git -C ../practice-ui diff
git -C ../practice-ui add index.html
git -C ../practice-ui diff --cached --name-only
git -C ../practice-ui commit -m "add filter explanation"
git -C ../practice-report diff
git -C ../practice-report add report.mjs tests/report-compact.test.mjs
git -C ../practice-report diff --cached --name-only
git -C ../practice-report commit -m "add compact weekly report"
git cherry-pick codex/filter-hint
git cherry-pick codex/report-compact
git diff --name-only
git show --stat HEAD
node --test
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11 --compact
\`\`\`

成功條件：A commit 只有 index.html；B commit 只有 report.mjs 及新測試；main 有可見提示與兩種格式，數字相同，未提交的 style.css 註記仍在原工作樹。以 HTTP 真正檢查整合頁面；未跑記 NOT RUN。把整合 commit hashes 與原文輸出另記，不把作者 reference 當這次代理結果。

挑戰：從完成主任務的 main 建兩個新分支，故意改相同的 p#filter-hint 文字：

\`\`\`text
git worktree add ../practice-conflict-a -b codex/conflict-a
git worktree add ../practice-conflict-b -b codex/conflict-b
\`\`\`

A 改為「搜尋會與目前狀態篩選一起套用；首尾空白會被忽略。」；B 改為「搜尋會與目前狀態篩選一起套用；搜尋不會刪除任務。」。兩路各只 git add index.html，提交後：

\`\`\`text
git -C ../practice-conflict-a add index.html
git -C ../practice-conflict-a commit -m "explain trimmed search"
git -C ../practice-conflict-b add index.html
git -C ../practice-conflict-b commit -m "explain retained tasks"
git cherry-pick codex/conflict-a
git cherry-pick codex/conflict-b
git status --short
\`\`\`

第二次應停止於 index.html 內容衝突，這是預期失敗。先保存輸出，再讀雙方需求，把衝突標記改成一句保留兩項意思的提示：「搜尋會與目前狀態篩選一起套用；首尾空白會被忽略，搜尋不會刪除任務。」。只 git add index.html，再 git cherry-pick --continue。重新 node --test、兩格式與HTTP驗收；style.css 註記仍不提交。若決定停止未完成的這次挑選，用 git cherry-pick --abort；不要 reset --hard。

還原：若只完成主任務且尚未做文案挑戰，可在主練習庫 git revert --no-edit codex/report-compact，再 git revert --no-edit codex/filter-hint；核對逆向提交與原 CSS 註記保留。若有後續文案改動，先讀歷史及 diff 再選回復範圍，或保留整份成果、從本包 start 複製全新副本。

清理：先 git worktree list 核對絕對路徑，保存成果並確認各支工作樹 git status --short 是空。只對本課明確路徑執行 git worktree remove ../practice-ui、../practice-report、../practice-conflict-a、../practice-conflict-b；沒有做挑戰就不執行其兩條。原 main 的註記保留。是否刪分支依成果是否仍需要決定。
`;
const subagentInstructions=`# 獨立分析練習\n\n以下是可照貼的提示，沒有預先製造代理回覆。把結果另存 docs/analysis-data.md、docs/analysis-ui.md。\n\n代理 A：只讀 core.mjs、core.test.mjs、fixtures、tests；檢查同名ID、immutability、非法整批匯入、台北跨日、未知時間。每個發現給輸入、預期、目前結果、檔案與證據，禁止改檔。\n代理 B：只讀 index.html、app.mjs、style.css、storage.mjs；檢查文字呈現、键盤焦點、390px布局、reload与损毁storage。可執行獨立瀏覽器驗收；未跑的項目標 NOT RUN，禁止改檔。\n主代理：先讀兩份結果，重現可操作發現；不以兩票同意代替驗證；只將確認問題列成後續任務。\nApp／CLI 依你當前版本的子代理入口派發。若入口不可用，可在兩個獨立聊天手動派發並標示為「獨立聊天分析」；不能標示已用了未驗證的子代理功能。\n`;
const scheduleInstructions=`# App 週報排程\n\n先在這個本機練習專案手動執行 report.mjs 確認真值，再透過 App 的排程入口建立本課專案週報。建立後讀回名稱、專案、時區 Asia/Taipei、時間和提示。教材沒有替你建立任何排程。\n\n提示可照貼：每次只讀 fixtures/tasks.json，使用 Asia/Taipei 的包含整天日期 2026-10-05 至 2026-10-11，執行 node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11；在全新 runs/run-ID 路徑保存結果，回報 total/completedInWeek/pending/unknownCompleted。若輸入沒有變更且無錯誤則保持安靜；完成第一次執行、失敗、需我處理時通知。禁止改來源。\n\n第一次實際執行後核對輸入版本、命令、exit code、結果與固定真值；App 設定成功不等於已跑過。停止練習時在 App 暫停或刪除本課建立的排程，讀回確認。不能宣稱主機關閉時仍能執行。\n`;
const batchInstructions="# CLI 一次性批次\n\nnode exec-run.mjs --dry-run 只列 argv/schema 與實際 input/from/to，不讀來源、不用模型。可加 --input FILE、--from DATE、--to DATE；預設 fixtures/tasks.json、2026-10-05 到 2026-10-11，日期為包含整天的台北日曆。\n\nnode exec-run.mjs --run run-01 會建立全新資料夾，先驗來源與日期，再真正呼叫 codex exec；須先完成登入與額度核對。Windows 若需要可加 --codex NATIVE_CODEX_EXE，不執行 .cmd/.bat wrapper。input 必須位於本課專案內，CLI 不會讀 localStorage。\nnode verify-result.mjs run-01 對照 input.json/status.json 的实际 input/from/to/timezone/sourceSha256，確認來源未變，再独立計算真值；不相信模型 JSON 的日期或數字。\n\n次週主變式：\nnode exec-run.mjs --dry-run --from 2026-10-12 --to 2026-10-18\nnode exec-run.mjs --run run-next-week --from 2026-10-12 --to 2026-10-18\nnode verify-result.mjs run-next-week\n預期 total5/completedInWeek0/pending1/unknownCompleted1。第二條是真模型請求，沒跑須記 NOT RUN；dry-run 和 synthetic 單元測試不能替代它。\n\n缺檔失敗演練（確定性、沒有provider呼叫）：\nnode exec-run.mjs --run run-missing --input fixtures/missing.json --from 2026-10-12 --to 2026-10-18\n預期 exit1，run-missing/status.json state=preflight_failed、modelInvoked=false、errorCode=ENOENT，保留 input/prompt/schema、空 events.jsonl、stderr，沒有 final.json。先確定此檔本來不存在，不刪正常fixture來湊錯誤。恢復後只用新 run ID，舊run拒覆寫。\n\n120秒 timeout、launch_failed、缺 turn.completed、錯數都拒絕；所有真實 events/stderr 保留、不自動重試。模型啟動後的 modelInvoked 表示runner已嘗試呼叫CLI，不等於API成功或完成。synthetic events只在單元測試臨時資料夾，明標非模型證據。\n";
export function materializeLesson(value,destination){
  const id=Number(value);if(!Number.isInteger(id)||id<1||id>18)throw new Error('Lesson must be 1..18');
  const root=resolve(destination);if(existsSync(root))throw new Error('Destination already exists: '+root);mkdirSync(root,{recursive:true});
  const [title,goal,scope,challenge,answer]=lessons[id-1];
  const meta={id,title,authorship:'author-built teaching reference; no model execution claim',snapshots:['start','reference','challenge'],
    startDirectory:'start',referenceDirectory:'reference',challengeDirectory:'challenge',testCommand:id===1?'node --test core.test.mjs':'node --test',
    intentionalFailures:[3,5,9,18].includes(id)?['start','challenge']:id===1?['start','challenge']:id===6?['challenge']:[],
    manualChecks:id===7?['literal-markup-in-real-DOM']:id===10?['390px','1280px','Tab focus']:[],steps:procedures[id-1],transferExercise:transferExercises[id]?.prompt??null,expectedReport:id>=9?JSON.parse(read('fixtures/truth.json')):null};
  for(const variant of meta.snapshots)createSnapshot(join(root,variant),id,variant);
  if(id===1)put(root,'baseline-prompt.txt',readFileSync(join(repo,'tools/codex-practical/baseline-prompt.txt')));
  put(root,'lesson.json',JSON.stringify(meta,null,2)+'\n');
  const legacy=id===1;
  put(root,'README.md',`# ${String(id).padStart(2,'0')} ${title}\n\n${goal}\n\n本包獨立起步，不必沿用上一課改檔。start 是練習起點；reference 是作者參考；challenge 是遷移練習。解答在 answers.md，先獨立做完才讀。所有模型、瀏覽器、MCP、排程與 CI 結果必須另記，參考檔不等於實測。\n\n## 啟動與檢查\n\n在選定 snapshot 內開終端機，先核對 Get-Location（PowerShell）或 pwd。Node22+、Python3，不需 npm。\n\n\`\`\`text\n${meta.testCommand}\n\`\`\`\n\nWindows: py -m http.server 4173 --bind 127.0.0.1\nmacOS/Linux: python3 -m http.server 4173 --bind 127.0.0.1\n瀏覽 http://127.0.0.1:4173；Ctrl+C 停止。不要雙擊 HTML。\n\n${legacy?'01 start 原始測試預期 2 PASS/1 FAIL；reference 3 PASS；challenge 2 PASS/1 FAIL。五個程式檔是既有 Small Steps 教材逐 byte 複本，儲存鍵 mokaair-codex-todo-v1。':`本課 start/challenge ${meta.intentionalFailures.length?'有刻意故障，測試預期非零；不准刪測試。':'可啟動，任務差異在文件或人工驗收，不等於作業已完成。'} reference Node 檢查應全過。儲存鍵 mokaair-codex-practical-v${id>=9?2:1}。`}\n\n## 任務範圍\n\n${scope}\n\n## 一步一步完成\n\n${meta.steps.map((step,index)=>`${index+1}. ${step}`).join('\n')}\n\n## 挑戰\n\n${challenge}\n\n${id>=9?'固定來源 fixtures/tasks.json: total5、completedInWeek2、pending1、unknownCompleted1。`node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`。台北 +08 日曆；CLI 不會自動讀瀏覽器 localStorage。':''}\n\n## 還原\n\n先匯出虛構資料或保留檔案，重新複製本包 start 到新的練習資料夾；不覆寫你做過的版本。不要清除其他網站儲存、改正式庫、以未執行的圖或命令當證據。\n`);
  const appPreparation=legacy?'讀者先在完整教材包外層讀 README.md 與 acceptance.md，將本課目標、修改範圍和驗收要求貼到 App 聊天，再選 start 專案。start 只有原始五檔；不要求模型讀取其中不存在的 README 或 acceptance。\n\n':'';
  const appReview=legacy?'依讀者提供的需求核對工作路徑與五個檔案，列出基準及差距；本課只讀，不改程式。':'先確認工作路徑與檔案，讀 README/acceptance，列出基準及差距再動手。';
  put(root,'prompts.md',`# 可照貼提示\n\n## App\n\n${appPreparation}在本課獨立練習專案使用 ${scope} 目標是：${goal}。${appReview}所有未跑檢查寫 NOT RUN，不能改原始輸入來湊答案。\n\n## CLI\n\n从本課 snapshot 開 codex；貼入：${scope} 目標是：${goal}。先讀檔、確認範圍、保存基準。測試命令 ${meta.testCommand}。輸出實際命令/exit code/diff/未驗證；不得聲稱 App、瀏覽器或 CI 操作。\n\n## 遷移\n\n不讀 answers，處理 challenge：${challenge} 先寫預期，再讓案例證明結果。\n`);
  put(root,'acceptance.md',`# 完成條件\n\n- 能說出本課問題、輸入、允許改動和成功條件。\n- 保留開始版本與真正測試結果；故障課先失敗再修正。\n- ${goal}\n- ${challenge}\n- ${meta.testCommand} 回傳實際狀態；reference 應全過，01 start 故障由原測試看出。\n- 瀏覽器步驟另記 PASS/FAIL/NOT RUN；不能把靜態原始碼或 Node 綠燈當已看畫面。\n- 交付只有授權路徑 diff，來源、舊輸出与其他儲存鍵保留。\n- 独立完成 challenge 后再比對答案。\n`);
  put(root,'answers.md',`# 作者參考解答（不是模型紀錄）\n\n${answer}\n\n對照 reference 的檔案。不要整包覆盖 start 後聲稱已完成實作。先用自己寫的驗收案例判斷，再讀解答。\n\n${id>=9?'固定報表：total=5，completedInWeek=2，pending=1，unknownCompleted=1；2026-10-10T22:00Z 算台北10月11日。封存 cutoff2026-10-04T15:59:59.999Z 只選 old，一筆；保留四筆包含 unknown/pending。':''}\n`);
  if(transferExercises[id]){
    const exercise=transferExercises[id];
    for(const name of ['README.md','prompts.md','acceptance.md'])put(root,name,readFileSync(join(root,name),'utf8')+'\n## 固定變式與補充案例\n\n'+exercise.prompt+'\n');
    put(root,'answers.md',readFileSync(join(root,'answers.md'),'utf8')+'\n## 逐項預期真相\n\n'+exercise.answer+'\n');
  }
  if(id===9)for(const name of ['README.md','prompts.md'])put(root,name,readFileSync(join(root,name),'utf8')+'\n本包 IO/匯入 UI 接線是作者提供 scaffold；本課模型任務是核對並補資料驗證、日期與週報契約，不得把原接線說成這輪模型新增。\n');
  if(id===6)put(root,'README.md',readFileSync(join(root,'README.md'),'utf8').replace('本課 start/challenge 有刻意故障，測試預期非零；不准刪測試。','本課 start 既有測試可綠，但 meaningful 是 TODO；自己新增需求斷言先紅、修後綠。challenge 有強案例與故障，預期非零；不准刪測試。'));
  if(id===7)put(root,'README.md',readFileSync(join(root,'README.md'),'utf8')+'\n本課既有 Node 測試可綠；unsafe innerHTML 要以 diff 加真正 HTTP/DOM 的 literal markup 操作驗收。沒有 source-keyword 守衛來替代瀏覽器。\n');
  if(id===11)put(root,'acceptance.md',readFileSync(join(root,'acceptance.md'),'utf8')+'\n重構前後：合法期間10-05..11輸出逐byte相同；2026-02-30..03-08均exit1/calendar-date；錯誤日期順序10-11..05均exit1/date-order。不以重構名義悄悄改錯誤行為。\n');
  return {...meta,path:root};
}
export function materializeAll(destination){const root=resolve(destination);if(existsSync(root))throw new Error('Destination already exists');mkdirSync(root,{recursive:true});return lessons.map((_,index)=>materializeLesson(index+1,join(root,String(index+1).padStart(2,'0'))));}
export function writeLessonGuides(destination){
  const scratch=mkdtempSync(join(tmpdir(),'codex-guides-')),target=resolve(destination);
  try{const all=materializeAll(join(scratch,'lessons'));for(const meta of all){const output=join(target,String(meta.id).padStart(2,'0'));for(const name of ['lesson.json','README.md','prompts.md','acceptance.md','answers.md'])put(output,name,readFileSync(join(meta.path,name)));if(meta.id===1)put(output,'baseline-prompt.txt',readFileSync(join(meta.path,'baseline-prompt.txt')));const docs=join(meta.path,'reference/docs');if(existsSync(docs))for(const name of files(docs).filter(name=>name.endsWith('.md')))put(output,'workflow/'+name,readFileSync(join(docs,name)));}return all.map(meta=>({id:meta.id,path:join(target,String(meta.id).padStart(2,'0'))}));}
  finally{rmSync(scratch,{recursive:true,force:true});}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){try{const[id,out]=process.argv.slice(2);if(!id||!out)throw new Error('Usage: node tools/codex-practical/labs.mjs 01 NEWDIR OR all NEWDIR');console.log(JSON.stringify(id==='all'?materializeAll(out):materializeLesson(id,out),null,2));}catch(error){console.error(error.message);process.exitCode=1;}}
