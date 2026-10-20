# build-video-json.py: the generator that wrote video.json from demo/ (run from the lab folder the runs were made in;
# LAB and ROOT at the top point at that folder and the repo; ids.txt is the output of `cli.mjs ids --count 170`;
# numbers.json holds the measured numbers copied from demo/results/tally.txt). Kept as a record of how the cards were cut.
# build.py: assemble docs/videos/skills-one-year-monthly-report/video.json from the run results.
import json, sys, pathlib, re
ROOT = pathlib.Path('/home/user/travel_scanner')
V = ROOT / 'docs/videos/skills-one-year-monthly-report'
LAB = pathlib.Path('<LAB>')
N = json.load(open(pathlib.Path(__file__).with_name('numbers.json'), encoding='utf-8'))
IDS = open(pathlib.Path(__file__).with_name('ids.txt'), encoding='utf-8').read().split()
_i = 0
def nid():
    global _i; _i += 1; return IDS[_i - 1]
def L(text, **kw):
    d = {'id': nid(), 'text': text}; d.update(kw); return d
def lines_of(path, a, b):
    rows = open(path, encoding='utf-8').read().rstrip('\n').split('\n')
    return '\n'.join(rows[a - 1:b])
SKILL = LAB / 'skills/good/monthly-report/SKILL.md'
VAGUE = LAB / 'skills/vague/monthly-report/SKILL.md'
SCRIPT = LAB / 'skills/good/monthly-report/scripts/sum.mjs'
TEMPLATE = LAB / 'skills/good/monthly-report/template.md'
PASTE = LAB / 'prompts/paste.txt'
TODAY = '2026-10-20'
RUN = f'實際跑過 {TODAY}｜Claude Code 2.1.304'
scenes = []
def S(id, template, data, lines, chapter=None, claims=None):
    s = {'id': id}
    if chapter: s['chapter'] = chapter
    s['template'] = template; s['data'] = data
    if claims: s['claims'] = claims
    s['lines'] = lines; scenes.append(s); return s

# ---------- 1 開場濃縮 ----------
S('open', 'title', {'tag': 'Skill 滿一年', 'title': '12 個字，\n**一份月結報表**', 'subtitle': '同一句話、三種做法各跑三次，Skill 贏在哪'},
  [L('十月一號，小店九月的銷售紀錄十二筆，躺在一個資料夾裡。', emotion='壓低放慢，像在講一件剛發生的事'),
   L('我打了十二個字：九月的業績幫我整理一下。'),
   L('Claude 的第一步，是呼叫 monthly-report 這個 Skill。', emotion='「第一步」後停半拍'),
   L('它跑了一支腳本，寫出四個區段的報表，最後一行是總營收八萬五千兩百九十元。'),
   L('去年這個時候，同一件事我每個月要貼三百四十六個字的規則。', emotion='放慢，帶一點無奈')],
  chapter='12 個字叫出一份月結報表', claims=['c1', 'c2'])
S('ask', 'chat', {'title': '同一句話，Skill 那一次', 'messages': [
    {'side': 'right', 'name': '我', 'text': '九月的業績幫我整理一下。'},
    {'side': 'left', 'name': 'Claude', 'text': '報表已寫到 reports/2026-09.md，總營收 85,290 元'}]},
  [L('但同一句話，什麼都不給它，會得到什麼？', reveal=1, emotion='問句上揚，留著'),
   L('我把 description 改成一句廢話，再跑三次。', reveal=1, emotion='壓低'),
   L('還有一份開頭引號沒關的 SKILL.md，丟給驗證指令。'),
   L('Skill 到底是什麼，怎麼寫一個讓 Claude 自己接手的？', emotion='問句上揚，收住')],
  claims=['c1'])

# ---------- 2 三種做法 ----------
S('score', 'table', {'title': '同一句話、同一個資料夾，三種做法各 3 次',
    'columns': ['做法', '打的字', 'Skill 被呼叫', '寫了報表檔', '六個檢查點'],
    'rows': [['什麼都不給', '12', '0／3', '0／3', '0／6、0／6、0／6'],
             ['規則貼進對話', str(N['paste_chars']), '0／3', '3／3', '6／6、6／6、6／6'],
             ['寫成 Skill', '12', '3／3', '3／3', '6／6、6／6、6／6']],
    'highlight': 2, 'source': f'{RUN}｜各 3 次'},
  [L('什麼都不給的三次，一個報表檔都沒有寫。', reveal=1, emotion='揭曉，短句'),
   L('它在對話裡回了一份自己排的表，淨營收倒是算對了。'),
   L('規則貼進對話的三次，六個檢查點全中。', reveal=1),
   L('寫成 Skill 的三次，一樣六個全中，而且三次都是它自己呼叫的。', reveal=1, emotion='「自己」加重')],
  chapter='三種做法各跑三次：零、六、六', claims=['c3'])
S('typed', 'stats', {'title': '每個月要打幾個字，開場多帶幾個 token', 'stats': [
    {'value': '12 字', 'label': 'Skill：每個月打的字'},
    {'value': f"{N['paste_chars']} 字", 'label': '貼規則：每個月打的字'},
    {'value': f"+{N['tok_s']}", 'label': 'Skill：第一個請求多出的 token', 'note': f"什麼都不給是 {N['tok_b']:,}"},
    {'value': f"+{N['tok_p']}", 'label': '貼規則：第一個請求多出的 token'}],
    'source': f'{RUN}｜串流第一個回應的 usage'},
  [L('差別先看兩個數字：每個月打十二個字，還是三百多個字。', reveal=2),
   L(f"開場多帶的 token，Skill 是{N['tok_s_zh']}個，貼規則是{N['tok_p_zh']}個。", reveal=2, emotion='數字一個一個講')],
  claims=['c4'])
S('bare-reply', 'quote', {'kicker': '什麼都不給的那一次，它的回覆開頭', 'quote': N['bare_quote'], 'source': f'{RUN}｜{N["bare_quote_run"]} 的回覆'},
  [L('什麼都不給的三次，它每次都想自己寫一支 Python 腳本。'),
   L('腳本沒有被預先核准，它就改成手算，這次都算對了。', emotion='平實'),
   L('回來的表多了占比和退貨率，沒有人要求，每次長得也不一樣。'),
   L('規則貼進去也全中，那 Skill 到底贏在哪？', emotion='問句上揚，收住')],
  claims=['c5'])

# ---------- 3 腳本 ----------
S('how', 'compare', {'title': '同一句要求，算數是誰算的',
    'left': {'heading': '貼規則、什麼都不給', 'points': ['六次都是手算，這次都對', '其中四次先想寫 Python 跑', '沒有預先核准，被擋下']},
    'right': {'heading': '寫成 Skill', 'points': ['呼叫 monthly-report', '跑資料夾裡的 sum.mjs', '數字照腳本算的填']},
    'verdict': '腳本跟著資料夾走，規則貼不出腳本', 'source': f'{RUN}｜各 3 次'},
  [L('貼規則和什麼都不給的六次，數字全是手算的。', reveal=1),
   L('其中四次先想寫一支 Python 跑，沒被核准，才改成手算。'),
   L('Skill 那一邊，三次都是呼叫它，跑資料夾裡那支算數的腳本。', reveal=1),
   L('每一次的費用都在兩到七美分之間，貼規則那一邊最貴的一次七美分。'),
   L('規則我可以貼，腳本貼進對話是跑不起來的。', emotion='「跑不起來」放慢')],
  chapter='貼規則也全中，Skill 贏在帶得走的腳本', claims=['c5', 'c6'])
S('run-script', 'terminal', {'title': 'Skill 那一次跑的腳本（輸出節錄前幾行）',
    'command': 'node .claude/skills/monthly-report/scripts/sum.mjs data/2026-09.csv',
    'output': ['{\n  "total": 85290,\n  "items": [\n    {\n      "item": "咖啡豆 200g",\n      "amount": 31200\n    },'],
    'ran_on': TODAY, 'tool_version': 'Node.js v22.22.0'},
  [L('這支腳本讀那十二筆，算總營收、品項小計、退貨、大筆交易。', reveal=1),
   L('總營收八萬五千兩百九十，是它算的，不是模型心算的。', emotion='「它算的」加重')],
  claims=['c6'])
S('exec-quote', 'quote', {'kicker': 'Skill 公開那一天就寫明的用途',
    'quote': 'Skills can include executable code for tasks where traditional programming is more reliable than token generation.',
    'translation': '技能可以帶可執行的程式碼，給那些寫程式比讓模型生成更可靠的工作',
    'source': 'Anthropic｜Introducing Agent Skills｜2025-10-16'},
  [L('二〇二五年十月十六號公開那一天，用途就寫在公告裡：帶著程式碼走。', reveal=1),
   L('所以那個資料夾裡，到底有什麼？', emotion='問句上揚，收住')],
  claims=['c7'])

# ---------- 4 三個檔 ----------
S('tree', 'terminal', {'title': 'Skill 資料夾裡的三個檔', 'command': 'find .claude/skills -type f | sort',
    'output': ['.claude/skills/monthly-report/SKILL.md\n.claude/skills/monthly-report/scripts/sum.mjs\n.claude/skills/monthly-report/template.md'],
    'ran_on': TODAY, 'tool_version': 'sort (GNU coreutils) 9.4'},
  [L('一個資料夾、三個檔：說明、腳本、範本。', reveal=1, emotion='一個一個數')],
  chapter='資料夾裡的三個檔：SKILL.md、腳本、範本', claims=['c8'])
S('skill-head', 'code', {'title': 'SKILL.md 的開頭四行', 'language': 'yaml', 'code': lines_of(SKILL, 1, 4), 'highlight': [3],
    'caption': 'SKILL.md 17 行裡的第 1–4 行；全檔在說明欄的 demo 資料夾'},
  [L('開頭三行夾在兩條橫線裡：一個名稱，一句描述。'),
   L('亮起來的這一行，是 Claude 判斷要不要接手的依據。', emotion='放慢，一字一字'),
   L('寫它做什麼，還有你提到哪些字的時候用。'),
   L('名稱那一行不寫也行，會用資料夾的名字；描述一行就夠。')],
  claims=['c9'])
S('skill-body', 'code', {'language': 'markdown', 'code': lines_of(SKILL, 7, 17), 'highlight': [3, 4, 10, 11],
    'caption': 'SKILL.md 的第 7–17 行：五條規則，就是以前每個月貼的那一段'},
  [L('正文是五條規則，就是我以前每個月貼的那一段。'),
   L('亮起來的第二條，叫它先跑腳本，數字一律用腳本算的。'),
   L('最後那一條把回覆的最後一行釘死，之後每個月都長一樣。', emotion='「釘死」加重'),
   L('正文一旦被讀進對話，這一輪之後都還在，不用再讀一次。')],
  claims=['c9'])
S('template-a', 'code', {'language': 'markdown', 'code': lines_of(TEMPLATE, 1, 8), 'caption': 'template.md 16 行裡的第 1–8 行'},
  [L('範本就是報表長什麼樣：標題、總營收、品項排行。')], claims=['c10'])
S('template-b', 'code', {'language': 'markdown', 'code': lines_of(TEMPLATE, 9, 16), 'caption': 'template.md 的第 9–16 行'},
  [L('退貨明細和要注意的事，是老闆每個月真的會看的兩塊。'),
   L('那範本裡缺的這些數字，誰來填？', emotion='問句上揚，留著')], claims=['c10'])
S('script-a', 'code', {'language': 'javascript', 'code': lines_of(SCRIPT, 9, 14), 'caption': 'sum.mjs 26 行裡的第 9–14 行：每一筆的金額'},
  [L('腳本的這幾行，把每一筆的數量乘上單價。'),
   L('這一步模型手算也會；要它每個月都算對，我寧願交給腳本。', emotion='「我寧願」是意見')], claims=['c11'])
S('script-b', 'code', {'language': 'javascript', 'code': lines_of(SCRIPT, 15, 24), 'highlight': [9, 10], 'caption': 'sum.mjs 的第 15–24 行：總營收、品項小計、退貨、大筆交易'},
  [L('這幾行算總營收和品項小計，再挑出退貨和超過一萬元的交易。'),
   L('一萬元這個門檻寫在腳本裡，不靠模型每個月記得。', emotion='「不靠模型」加重')],
  claims=['c11'])
S('layers', 'steps', {'title': 'Skill 分三層進到對話', 'steps': [
    {'title': '開機', 'detail': '只讀名稱與描述'}, {'title': '用到', 'detail': '才讀正文那五條'}, {'title': '執行', 'detail': '用到哪個附檔才打開哪個'}],
    'source': 'Claude Code skills 頁；agentskills.io｜2026-10-20'},
  [L('Skill 分三層進到對話。開機時 Claude 只拿到名稱和描述。', reveal=1),
   L('它判斷用得上，才讀正文那五條。', reveal=1),
   L('範本和腳本，用到哪一個才打開哪一個。', reveal=1),
   L(f"這就是開場只多{N['tok_s_zh']}個 token 的原因。", emotion='「只多」輕一點')],
  claims=['c12'])
S('where', 'screencast', {'title': '官方頁：Skill 放哪裡，誰載得到', 'caption': 'Claude Code 文件｜skills｜Choose where skills load｜2026-10-20 擷取',
    'steps': [{'action': 'goto', 'url': 'https://code.claude.com/docs/en/skills#where-skills-live'},
              {'action': 'wait', 'selector': '#where-skills-live'},
              {'action': 'capture', 'focus': '#where-skills-live', 'zoom': 1.3}]},
  [L('放哪裡，決定誰載得到。'),
   L('家目錄底下的，你每個專案都有；專案裡的，跟著 repo 交給同事。', emotion='指著畫面')],
  claims=['c13'])
S('where-table', 'table', {'title': '同一個資料夾，放哪裡', 'columns': ['位置', '路徑', '誰載得到'],
    'rows': [['個人', '~/.claude/skills/', '這台機器的每個專案'], ['專案', '.claude/skills/', '開在這個 repo 的每個 session'],
             ['外掛', '<plugin>/skills/', '外掛啟用的地方'], ['Codex', '.agents/skills/', 'OpenAI 的 Codex，同一種 SKILL.md']],
    'highlight': 1, 'source': 'Claude Code 與 OpenAI Codex 的 skills 頁｜2026-10-20'},
  [L('這支放在專案裡，月報跟著店的資料夾走。', reveal=1),
   L('外掛裡的那一份，哪裡啟用外掛，哪裡就有。', reveal=1),
   L('寫好了，我怎麼知道它這一次真的用了？', emotion='問句上揚，收住')],
  claims=['c13'])

# ---------- 5 怎麼確認 ----------
S('call', 'code', {'title': '串流裡的第一筆工具呼叫', 'language': 'json', 'code': '{\n  "name": "Skill",\n  "input": {\n    "skill": "monthly-report",\n    "args": "九月"\n  }\n}',
    'caption': f'{RUN}｜claude -p 的 stream-json｜s1、s2、s3 都是這一筆'},
  [L('它回我說照規則做了，這不算證據。', emotion='平實'),
   L('我看紀錄：串流裡第一筆工具呼叫就是 Skill，點名了這個資料夾。'),
   L('連「九月」兩個字都當參數帶了進去，三次都一樣。', emotion='「三次都一樣」放慢'),
   L('用斜線直接叫的那一次剛好相反：紀錄裡沒有這筆呼叫。'),
   L(f"正文直接展開進對話，第一個請求多帶了{N['tok_x_zh']}個 token。")],
  chapter='不用問它：看紀錄裡那一筆呼叫', claims=['c14'])
S('check', 'steps', {'title': '三個地方對一次', 'steps': [
    {'title': '串流', 'detail': '名稱是 Skill 的那一筆呼叫'}, {'title': '畫面', 'detail': '/skills 的清單裡有它'}, {'title': '磁碟', 'detail': '報表檔在、最後一行對'}],
    'source': '第 2 步是官方 skills 頁的做法；這次沒有開畫面'},
  [L('不開畫面的時候，看串流。', reveal=1),
   L('開著畫面的時候，用清單指令看它在不在。', reveal=1),
   L('最後看磁碟：報表檔在不在，最後一行對不對。', reveal=1)],
  claims=['c14', 'c15'])
S('trigger-quote', 'quote', {'quote': 'Seeing a skill trigger tells you Claude found it, not that it did what you intended.',
    'translation': '看到 Skill 被觸發，只代表 Claude 找到它，不代表它做了你要的事',
    'source': 'Claude Code 文件｜skills｜Evaluate and iterate｜2026-10-20'},
  [L('被呼叫，只代表它找到了；做對沒有，要看檔案。', reveal=1, emotion='「找到了」停半拍'),
   L('那如果我把描述那一行寫壞呢？', emotion='問句上揚，收住')],
  claims=['c16'])
S('cta', 'cta', {'kicker': '說明欄的文章', 'title': '技能、專案、個人指令、MCP 怎麼分', 'sub': 'Claude Skills 是什麼：把重複流程包成可重用的技能'},
  [L('技能跟專案、個人指令怎麼分工，說明欄那篇文章有一張表。')], claims=['c17'])

# ---------- 6 description 與 validate ----------
S('vague-head', 'code', {'title': '把描述換成一句廢話', 'language': 'yaml', 'code': lines_of(VAGUE, 1, 4), 'highlight': [3], 'caption': '正文 13 行一個字不動，只改第 3 行'},
  [L('我把描述換成一句專案維護用的說明，正文一個字不動。', emotion='壓低')],
  chapter='描述寫成廢話照樣被呼叫；驗證指令抓的是另一種錯', claims=['c18'])
S('vague-score', 'table', {'title': '描述是廢話的那一份，3 次', 'columns': ['次數', 'Skill 被呼叫', '跑了腳本', '六個檢查點'],
    'rows': [['v1', '有', '有', '6／6'], ['v2', '有', '有', '6／6'], ['v3', '有', '有', '6／6']],
    'source': f'實際跑過 {TODAY}｜描述只有「專案維護用的說明。」'},
  [L('三次，它三次都來接，三次都全中。', reveal=3, emotion='揭曉，短句')], claims=['c18'])
S('name-big', 'big', {'kicker': 'monthly-report 對上了「業績整理」', 'text': '名字就對上了', 'sub': '被呼叫，不是描述寫對的證據'},
  [L('救它的是名字：monthly-report，對上了業績整理這句話。'),
   L('所以被呼叫，不能當成描述寫對的證據。', emotion='「不能」加重'),
   L('描述還是照正道寫：做什麼、什麼時候用，放進你真的會講的詞。'),
   L('描述有上限，連同補充的觸發句一共一千五百三十六個字元，超過會被截掉。')],
  claims=['c18', 'c19'])
S('validate-a', 'terminal', {'title': '引號沒關的那一份（輸出節錄）', 'command': 'claude plugin validate .claude/skills',
    'output': ['× Found 1 error:\n\n  > frontmatter: YAML frontmatter failed to parse: YAML Parse error:\nUnexpected EOF. At runtime this skill loads with empty metadata (all\nfrontmatter fields silently dropped).\n\n× Validation failed'],
    'ran_on': TODAY, 'tool_version': '2.1.304 (Claude Code)'},
  [L('換另一種錯：描述的引號沒關。驗證指令直接報錯。', reveal=1),
   L('它還講了後果：執行時這個 Skill 會載入成空的開頭，描述整個掉了。', emotion='放慢')],
  claims=['c20'])
S('validate-b', 'terminal', {'title': '欄位名打錯一個字母的那一份（輸出節錄）', 'command': 'claude plugin validate .claude/skills',
    'output': ['‼ Found 1 warning:\n\n  > description: No description in frontmatter. A description helps users and\nClaude understand when to use this skill.\n\n√ Validation passed with warnings'],
    'ran_on': TODAY, 'tool_version': '2.1.304 (Claude Code)'},
  [L('欄位名打錯一個字母，它只警告，結束碼還是零；加嚴格模式才擋。', reveal=1)],
  claims=['c20'])
S('fix-order', 'bullets', {'title': 'Skill 沒被呼叫，照這個順序查', 'items': ['描述裡有沒有你會說的詞', '問它有哪些 Skill 可用，清單裡在不在', '換個說法再要求一次', '用斜線直接叫它', '跑 validate 看開頭有沒有壞'],
    'source': 'Claude Code skills 頁｜Skill not triggering'},
  [L('沒被呼叫，先查描述有沒有你會說的詞，再問它有哪些 Skill 可用。', reveal=2),
   L('換個說法再試，或者用斜線直接叫它。', reveal=2),
   L('最後跑驗證指令，開頭壞掉它會直接說。', reveal=1)],
  claims=['c21'])
S('switch-off', 'code', {'title': '反過來：不要它自己接手', 'language': 'yaml', 'code': '---\nname: deploy\ndescription: Deploy the application to production\ndisable-model-invocation: true\n---\n\n{ "skillOverrides": { "deploy": "off" } }',
    'highlight': [4, 7], 'caption': '上面是 SKILL.md 的開頭，下面是設定檔的一行；官方 skills 頁的例子｜引用'},
  [L('反過來，用太多的時候有兩個開關。'),
   L('開頭加一行關掉模型自己呼叫，它就只能由你用斜線叫。'),
   L('不想改檔案，在設定裡把它關掉也行。'),
   L('寫好的資料夾，怎麼帶走？', emotion='問句上揚，收住')],
  claims=['c22'])

# ---------- 7 帶走 ----------
S('keep', 'steps', {'title': '留下來、帶走', 'steps': [
    {'title': '進版控', 'detail': '.claude/skills/ 跟著 repo'}, {'title': '移除', 'detail': '刪掉資料夾'},
    {'title': 'Claude 應用程式', 'detail': '上傳，開頭只收六個欄位'}, {'title': 'Codex', 'detail': '放進 .agents/skills/'}],
    'source': 'Claude Code、Claude 說明中心、Codex 的 skills 頁'},
  [L('留下來很簡單：資料夾進版控，刪掉就是移除。', reveal=2),
   L('同一個資料夾上傳到 Claude 應用程式也能用，開頭只收六個欄位。', reveal=1),
   L('這支只用了兩個，剛好都在裡面。'),
   L('應用程式那邊要先打開程式碼執行，技能那一頁才會出現。'),
   L('放進 Codex 讀的那個資料夾，同一份檔就能用。', reveal=1)],
  chapter='留下來、帶走、換成你自己的那一段', claims=['c23', 'c24'])
S('allowed', 'quote', {'kicker': '貼規則那一邊被擋下的 Python，在 Skill 裡有解',
    'quote': 'allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)',
    'translation': '開頭多這一行：替自己資料夾裡的腳本預先核准，跑的時候不用再問',
    'source': 'Claude Code 文件｜skills｜string substitutions｜引用'},
  [L('還記得貼規則那一邊被擋下的 Python 嗎？', emotion='問句上揚'),
   L('Skill 的開頭可以替自己的腳本預先核准，跑的時候不用再問。', reveal=1),
   L('這支沒有寫這一行；腳本跑得了，是因為那次的核准清單本來就有它。', emotion='平實')],
  claims=['c25'])
S('practice', 'chat', {'title': '換成你的那一段', 'messages': [
    {'side': 'right', 'text': '把你每個月重貼的規則，貼進 SKILL.md 的正文'},
    {'side': 'left', 'text': '開頭補名稱和描述，跑一次驗證指令'},
    {'side': 'right', 'text': '用一句不提名字的話叫它，看紀錄有沒有那一筆'}]},
  [L('練習只有三步：把你每個月貼的那一段，放進正文。', reveal=1),
   L('開頭補名稱和描述，跑一次驗證。', reveal=1),
   L('用一句不提名字的話叫它，紀錄裡要有那一筆呼叫。', reveal=1)],
  claims=['c9', 'c14'])

# ---------- 8 結尾 ----------
S('closing', 'outro', {'title': '一個資料夾、三行開頭、12 個字', 'cta': '你每個月重貼的那一段是什麼？留言告訴我',
    'lines': ['什麼都不給 0／6、貼規則 6／6、Skill 6／6，各 3 次', '描述寫成廢話照樣被呼叫：名字對上了', '腳本跟著資料夾走，規則貼不出腳本']},
  [L('Skill 就是一個資料夾、三行開頭，加上你本來就在貼的那段規則，三次全中。', emotion='放穩，一句講完'),
   L('你每個月重貼的那一段是什麼？留言告訴我。', emotion='問句上揚'),
   L('每一支都這樣跑給你看，訂閱就不會漏掉。')],
  chapter='一個資料夾、三行開頭、十二個字', claims=['c3'])

# loops
def lid(scene, idx): return [s for s in scenes if s['id'] == scene][0]['lines'][idx]['id']
loops = [
    {'setup': lid('ask', 0), 'payoff': lid('score', 0), 'what': '什麼都不給的三次會得到什麼'},
    {'setup': lid('ask', 1), 'payoff': lid('vague-score', 0), 'what': '描述改成廢話還會不會被呼叫'},
    {'setup': lid('ask', 2), 'payoff': lid('validate-a', 0), 'what': '引號沒關的那一份驗證怎麼說'},
    {'setup': lid('bare-reply', 2), 'payoff': lid('how', 2), 'what': 'Skill 比貼規則多做到的事'},
    {'setup': lid('exec-quote', 1), 'payoff': lid('tree', 0), 'what': '資料夾裡有什麼'},
    {'setup': lid('where-table', 2), 'payoff': lid('call', 1), 'what': '怎麼知道它真的用了'},
    {'setup': lid('trigger-quote', 1), 'payoff': lid('vague-score', 0), 'what': '描述寫壞會怎樣'},
    {'setup': lid('switch-off', 3), 'payoff': lid('keep', 0), 'what': '資料夾怎麼帶走'},
]
doc = {
  'schema_version': 1, 'slug': 'skills-one-year-monthly-report', 'format': 'slides', 'category': 'tutorial',
  'source_guide': 'claude-skills-explained', 'target_minutes': [8, 12],
  'voice': {'provider': 'gemini', 'name': 'Sulafat',
            'style': '標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。',
            'performance': '這一支是照著紀錄講的實作：像把一個三個檔的資料夾和十三次的紀錄攤在朋友面前，一格一格對給他看，穩、清楚、不嚇人。開場壓低放慢；計分表三列各停半拍；講到手算與腳本的差別放慢；「名字就對上了」是全片最亮的一句；章末的問句輕輕收。'},
  'youtube': {'category_id': 28, 'made_for_kids': False, 'default_language': 'zh-TW',
    'title': 'Skill 滿一年了還在重貼規則？12 個字叫出月結報表，背後一個資料夾',
    'description': ('同一句 12 個字的要求、同一個只有一份 CSV 的資料夾，「什麼都不給」「規則貼進對話」「寫成 Skill」各跑三次，再把 description 改成一句廢話跑三次：Skill 跟貼規則到底差在哪，Claude 有沒有用它怎麼看，沒被用到先查什麼。\n'
      '給每個月都有一件固定格式的事要交給 Claude 的人：月報、週報、貼文改寫、客訴回覆。會打指令的人與不會的人都看得懂，資料夾的寫法上傳到 Claude 應用程式也一樣。\n\n'
      '想照著做：練習資料夾、兩個版本的 Skill、三份要求、跑的腳本、每一次的結果與逐筆紀錄都在 https://github.com/x812033727/travel_scanner/tree/main/docs/videos/skills-one-year-monthly-report/demo （逐筆紀錄是同一個資料夾的 runlog.txt）\n\n'
      '你會學到：\n'
      '・一個 Skill 資料夾的三個檔：SKILL.md（開頭三行加五條規則）、scripts/sum.mjs（26 行的算數腳本）、template.md（報表的四個區段）\n'
      f"・計分（各 3 次）：什麼都不給 0／6（連檔案都沒有寫）、貼規則 6／6、Skill 6／6；打的字 12 對 {N['paste_chars']}；開場多帶的 token ＋{N['tok_s']} 對 ＋{N['tok_p']}\n"
      '・貼規則與什麼都不給的六次全是手算（四次先想寫 Python 跑、沒被預先核准）；Skill 的三次跑的都是資料夾裡的腳本\n'
      '・不用問 Claude：串流裡第一筆工具呼叫就是 Skill，輸入是 {"skill": "monthly-report", "args": "九月"}\n'
      '・description 改成「專案維護用的說明。」照樣三次被呼叫、三次 6／6：名字對上了，所以被呼叫不是描述寫對的證據\n'
      '・claude plugin validate：引號沒關的那一份報錯、結束碼 1，並說執行時會載入成空的 metadata；欄位名打錯的只警告、結束碼 0，加 --strict 才是 1\n\n'
      '照著打的時候\n'
      '・先把 demo 複製到任何 git 儲存庫以外的地方。run.sh 每次從 seed 重建資料夾，再把 skills/good（或 skills/vague）複製到 .claude/skills/，把 prompts 裡的那一份當要求送進不開畫面的 claude -p。\n'
      f"・旗標：--model sonnet --permission-mode default --tools \"Read,Glob,Grep,Edit,Write,Bash,Skill\" --allowedTools \"Read,Glob,Grep,Edit,Write,Bash(node *),Bash(mkdir *),Bash(cat *),Bash(ls *)\" --output-format stream-json --verbose --no-session-persistence --setting-sources project --strict-mcp-config --max-turns 40 --max-budget-usd 1。node 在預先核准的清單裡、python3 不在，所以 Skill 帶的腳本跑得了、模型自己寫的 Python 跑不了；Skill 可以用 allowed-tools 替自己的腳本預先核准（片中引用官方頁，這支沒有寫）。\n"
      '・專案的 .claude/settings.json 關掉內建與帳號同步的 Skill；三個內建外掛的 Skill 關不掉，每一臂都一樣。\n'
      f"・每跑一次都用掉你的額度；這十三次每次回報約 {N['cost_min']} 到 {N['cost_max']} 美元。\n\n"
      '怎麼跑的\n'
      '・Linux 容器、Claude Code 2.1.304、Node v22.22.0，2026-10-20。十三次 session 都是 --model sonnet、不開畫面；主線三臂各 3 次、描述含糊 3 次、斜線 1 次。\n'
      '・沒有觀察的：任何互動式的畫面（/skills、/context、/skill-doctor、斜線選單、Claude 應用程式的 Customize 頁）；其他模型與作業系統；Claude 應用程式或 Codex 實際載入同一個資料夾（只引用官方頁的位置與欄位規則）；allowed-tools 預先核准的效果；手算會不會算錯（這次六次都對）。\n'
      '・試跑那一輪把腳本和範本放在專案資料夾裡，什麼都不給的那一次自己找到它們、做到五步；正式那一輪才把它們搬進 Skill 資料夾（runlog-pilot.txt）。'),
    'tags': ['Claude Skill', 'Agent Skills', 'SKILL.md', 'Claude Skills 教學', 'Claude Code', 'Skill 是什麼', 'Claude Code skill 沒觸發', 'skill description', 'Codex skills', 'Mokaair'],
    'video_id': None},
  'thumbnail': {'template': 'thumb', 'data': {'tag': 'Skill 滿一年', 'headline': '12 字\n**一份報表**', 'sub': '同一句話三種做法各 3 次：\n0／6、6／6、6／6', 'capture': 'where'}},
  'sources': [
    {'title': 'Extend Claude with skills｜Claude Code Docs', 'url': 'https://code.claude.com/docs/en/skills', 'checked_on': TODAY},
    {'title': 'Plugin commands reference｜Claude Code Docs', 'url': 'https://code.claude.com/docs/en/plugins/cli-reference', 'checked_on': TODAY},
    {'title': 'Introducing Agent Skills｜Anthropic', 'url': 'https://www.anthropic.com/news/skills', 'checked_on': TODAY},
    {'title': 'Agent Skills Overview｜agentskills.io', 'url': 'https://agentskills.io/', 'checked_on': TODAY},
    {'title': 'Using skills in Claude｜Claude Help Center', 'url': 'https://support.claude.com/en/articles/12512180-using-skills-in-claude', 'checked_on': TODAY},
    {'title': 'Skills｜OpenAI Developers (ChatGPT and Codex)', 'url': 'https://developers.openai.com/codex/skills', 'checked_on': TODAY},
    {'title': 'Run Claude Code programmatically｜Claude Code Docs', 'url': 'https://code.claude.com/docs/en/headless', 'checked_on': TODAY},
  ],
  'assets': [], 'subtitles': {'burn_in': False}, 'scenes': scenes, 'loops': loops,
}
# checks
chars = 0
for s in scenes:
    for l in s['lines']:
        n = len(l['text']); chars += n
        if n > 40: print('LONG', s['id'], n, l['text'])
cues = sum(1 for s in scenes for l in s['lines'] if l.get('emotion'))
total = sum(len(s['lines']) for s in scenes)
print(f'{len(scenes)} scenes, {total} lines, {chars} chars, {cues} cues ({cues/total:.0%}), ids used {_i}')
for s in scenes:
    if s['template'] == 'code':
        for ln in s['data']['code'].split('\n'):
            if len(ln) > 64: print('CODE LONG', s['id'], len(ln))
        if len(s['data']['code'].split('\n')) > 16: print('CODE LINES', s['id'])
json.dump(doc, open(V / 'video.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open(V / 'video.json', 'a', encoding='utf-8').write('\n')
