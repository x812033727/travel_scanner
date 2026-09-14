"""Build reproducible starter, deliberate-bug and reference archives."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
LAB = Path(__file__).with_name("lab")
OUT = ROOT / "apps/web/public/tutorials/claude-code"

FILTER = '''
export function filterTodos(items, mode) {
  if (mode === 'active') return items.filter(item => !item.completed);
  if (mode === 'completed') return items.filter(item => item.completed);
  return items;
}
export function loadTodos(raw) {
  try {
    const value = JSON.parse(raw);
    if (!Array.isArray(value)) return [];
    const seen = new Set();
    return value.filter(item => {
      if (!item || typeof item.id !== 'string' || !item.id || seen.has(item.id)
          || typeof item.title !== 'string' || !item.title.trim() || item.title.length > 100
          || typeof item.completed !== 'boolean') return false;
      seen.add(item.id);
      return true;
    }).map(item => ({ id: item.id, title: item.title, completed: item.completed }));
  } catch { return []; }
}
'''

FILTER_TEST = '''
test('篩選保持原始資料與順序', () => {
  const items = [{ id: 'a', title: 'A', completed: false }, { id: 'b', title: 'B', completed: true }];
  assert.deepEqual(filterTodos(items, 'active').map(x => x.id), ['a']);
  assert.deepEqual(filterTodos(items, 'completed').map(x => x.id), ['b']);
  assert.equal(filterTodos(items, 'all'), items);
  assert.equal(items.length, 2);
});
test('損壞的儲存資料不會讓頁面停止運作', () => {
  assert.deepEqual(loadTodos('not json'), []);
  assert.deepEqual(loadTodos('{}'), []);
  assert.deepEqual(loadTodos('[null, {"id": 1}]'), []);
  const valid = { id: 'a', title: 'A', completed: false };
  assert.deepEqual(loadTodos(JSON.stringify([valid, valid])), [valid]);
});
'''


def variants():
    starter = {str(path.relative_to(LAB)).replace('\\', '/'): path.read_text(encoding='utf-8')
               for path in LAB.rglob('*') if path.is_file()}
    complete = dict(starter)
    complete['model.js'] += FILTER
    app = complete['app.js'].replace('removeTodo }', 'removeTodo, filterTodos, loadTodos }')
    app = app.replace('let items = [];', '''let items = [];
let storageAvailable = true;
try { items = loadTodos(localStorage.getItem('mokaair-todos')); } catch { storageAvailable = false; }
let mode = 'all';
document.querySelectorAll('[data-filter]').forEach(button => {
  button.addEventListener('click', () => { mode = button.dataset.filter; render(); });
});''')
    app = app.replace('for (const item of items)', 'for (const item of filterTodos(items, mode))')
    app = app.replace('  list.replaceChildren();', '''  list.replaceChildren();
  try { localStorage.setItem('mokaair-todos', JSON.stringify(items)); } catch { storageAvailable = false; }
  document.querySelectorAll('[data-filter]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === mode)));''')
    app = app.replace(" : '目前沒有待辦。';", " : '目前沒有待辦。';\n  if (!storageAvailable) message.textContent += ' 本次資料無法保存，重新整理後可能清空。';")
    complete['app.js'] = app
    complete['index.html'] = complete['index.html'].replace('<!-- 篩選功能在第 33 篇加入；起始版列出所有項目。 -->', '''<nav class="filters" aria-label="待辦篩選">
      <button type="button" data-filter="all" aria-pressed="true">全部</button>
      <button type="button" data-filter="active" aria-pressed="false">未完成</button>
      <button type="button" data-filter="completed" aria-pressed="false">已完成</button>
    </nav>''')
    complete['tests/model.test.mjs'] = complete['tests/model.test.mjs'].replace('removeTodo }', 'removeTodo, filterTodos, loadTodos }') + FILTER_TEST
    broken = dict(starter)
    broken['model.js'] = broken['model.js'].replace('item.id === id ?', 'item.id !== id ?')
    broken['README.md'] += '\n這是第 34 篇的刻意錯誤材料：勾選會改到其他項目；首次 npm test 預期失敗。請在複本中練習修正。\n'
    return {'starter': starter, 'bug-toggle': broken, 'complete': complete}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, files in variants().items():
        with ZipFile(OUT / (name + '.zip'), 'w') as archive:
            for filename, content in sorted(files.items()):
                info = ZipInfo(f'{name}/{filename}', date_time=(2026, 9, 14, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, content.encode('utf-8'))
        print(f'{name}: {len(files)} files')


if __name__ == '__main__':
    main()
