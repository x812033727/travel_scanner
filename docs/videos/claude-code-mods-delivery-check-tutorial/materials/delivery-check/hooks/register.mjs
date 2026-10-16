import {
  TARGETS,
  parseDirectoryArg,
  targetPath,
  classifyListedTarget,
  classifyStatError,
  formatCheckedAt,
} from './delivery-logic.mjs';

const PANE = 'delivery-check';
let generation = 0;
let state = initialState();

function initialState() {
  return { directory: null, rows: [], checkedAt: null, checking: false, notice: '' };
}

// Keep $ calls in this file and spell them in full for Claude's static analysis.
// The imported helpers receive only data, never $ or one of its namespaces.
async function refresh($) {
  const directory = state.directory;
  if (!directory) return;
  const request = ++generation;
  state = { directory, rows: [], checkedAt: null, checking: true, notice: '' };
  $.ui.invalidate('ui.render');

  try {
    const folder = await $.fs.stat(directory);
    if (request !== generation) return;
    if (folder?.kind !== 'dir') {
      state = { ...state, checking: false, notice: '指定路徑不是資料夾；請重新指定。' };
      $.ui.invalidate('ui.render');
      return;
    }
  } catch (error) {
    if (request !== generation) return;
    const result = classifyStatError(error);
    state = {
      ...state,
      checking: false,
      notice: result.status === 'missing'
        ? '找不到指定資料夾；請核對完整路徑。尚未檢查三個交稿路徑。'
        : '資料夾無法檢查。' + result.detail,
    };
    $.ui.invalidate('ui.render');
    return;
  }

  let rows;
  try {
    // A successful directory listing establishes missing names without
    // depending on whether the host preserves errno fields across the bridge.
    const entries = await $.fs.list(directory);
    rows = TARGETS.map((target) => ({
      ...target,
      path: targetPath(directory, target.name),
      ...classifyListedTarget(entries, directory, target.name),
    }));
  } catch {
    // In particular, a denied/failed listing is not an empty directory.
    rows = TARGETS.map((target) => ({
      ...target,
      path: targetPath(directory, target.name),
      status: 'unknown',
      label: '無法檢查',
      detail: '無法讀取資料夾清單；請核對資料夾、存取權限及版本。',
    }));
  }
  if (request !== generation) return;

  let checkedAt = null;
  try {
    checkedAt = formatCheckedAt(await $.clock.now());
  } catch {
    // Keep the check results, but never invent a completion timestamp.
  }
  if (request !== generation) return;
  state = {
    directory,
    rows,
    checkedAt,
    checking: false,
    notice: checkedAt === null ? '未取得檢查時間；以上結果不可當成即時監看。' : '',
  };
  $.ui.invalidate('ui.render');
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    generation += 1;
    state = initialState();
    await $.command.register({
      name: 'deliverables',
      description: '手動檢查文章、資料依據和封面需求的路徑',
      argumentHint: '"資料夾完整路徑"',
    });
    return next(e);
  });

  on('session.end', async ($, e, next) => {
    generation += 1;
    state = initialState();
    $.ui.invalidate('ui.render');
    return next(e);
  });

  on('command.run', { command: 'deliverables' }, async ($, e) => {
    const request = ++generation;
    const parsed = parseDirectoryArg(e.args);
    if (!parsed.ok) {
      // Cancel pending work and clear old results so an invalid new target
      // cannot leave a convincing-looking snapshot of the previous folder.
      state = { ...initialState(), notice: parsed.error };
    } else if (parsed.directory !== null) {
      state = { ...initialState(), directory: parsed.directory };
    } else if (!state.directory) {
      state.notice = '請輸入 /deliverables "資料夾完整路徑"，先指定要查哪裡。';
    }

    // The pinned declaration returns void. Do not infer visibility from its result.
    await $.ui.open({ id: PANE, title: '交稿檢查', focus: true, closeOnEscape: true });
    if (request !== generation) return {};
    $.ui.invalidate('ui.render');
    if (parsed.ok && state.directory) await refresh($);
    // No text/context, prompt submission, model call, or fall-through command.
    return {};
  });

  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    if (e.requestId !== PANE) return next(e);
    const { Box, Text, Button } = $.ui.resolve(e);
    const children = [
      Text({ children: ['交稿檢查 v2'] }),
      Text({ children: ['檢查資料夾：' + (state.directory ?? '尚未指定')] }),
      Text({ children: ['上次檢查（UTC）：' + (state.checkedAt ?? '尚未完成或未取得時間')] }),
    ];
    if (state.checking) children.push(Text({ children: ['正在檢查指定路徑……'] }));
    if (state.notice) children.push(Text({ children: [state.notice] }));
    for (const row of state.rows) {
      children.push(Text({ children: [row.name + '（' + row.purpose + '）：' + row.label] }));
      if (row.status === 'unknown') children.push(Text({ children: [row.detail] }));
    }
    if (state.directory) {
      children.push(Button({
        key: 'refresh',
        label: '重新檢查',
        onPress: async () => { await refresh($); },
      }));
    }
    children.push(Text({ children: ['路徑檢查不判斷內容品質；畫面只保留上次查詢結果。'] }));
    children.push(Button({
      key: 'close',
      label: '關閉面板',
      onPress: async () => { await $.ui.close({ id: PANE }); },
    }));
    return Box({ flexDirection: 'column', children });
  });
}
