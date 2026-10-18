// Pure data helpers: no Claude API, Node imports, file access, or side effects.
export const TARGETS = Object.freeze([
  Object.freeze({ name: 'article.md', purpose: '文章' }),
  Object.freeze({ name: 'sources.md', purpose: '資料依據' }),
  Object.freeze({ name: 'cover-brief.md', purpose: '封面需求' }),
]);

const CONTROL = /[\u0000-\u001f\u007f]/;
const WINDOWS_ABSOLUTE = /^[A-Za-z]:[\\/]/;

export function parseDirectoryArg(raw) {
  if (typeof raw !== 'string') return invalid('請提供資料夾完整路徑。');
  let directory = raw.trim();
  if (!directory) return { ok: true, directory: null };

  const quote = directory[0];
  if (quote === '"' || quote === "'") {
    if (directory.length < 2 || directory.at(-1) !== quote) {
      return invalid('路徑的引號沒有成對；請重新複製完整路徑。');
    }
    // Command args are raw text, not shell syntax: preserve every backslash.
    directory = directory.slice(1, -1);
    if (directory.includes(quote)) return invalid('請只提供一個完整路徑。');
  }
  return validateDirectory(directory);
}

function validateDirectory(directory) {
  if (!directory || CONTROL.test(directory) || /[<>]/.test(directory)) {
    return invalid('請把提示欄位換成實際路徑，且不要包含換行或控制字元。');
  }
  if (/^[\\/]{2}/.test(directory)) {
    return invalid('這個範例只接受本機完整路徑，不接受網路或裝置路徑。');
  }
  if (!WINDOWS_ABSOLUTE.test(directory) && !directory.startsWith('/')) {
    return invalid('需要完整路徑，例如 C:\\練習資料夾 或 /Users/you/delivery-practice。');
  }
  if (directory.includes('"')) return invalid('請只提供一個完整路徑，並檢查引號。');
  return { ok: true, directory };
}

function invalid(error) {
  return { ok: false, directory: null, error };
}

export function targetPath(directory, name) {
  if (typeof name !== 'string' || !name || name === '.' || name === '..' ||
      /[\\/]/.test(name) || CONTROL.test(name)) {
    throw new Error('Target must be one file name.');
  }
  const parsed = typeof directory === 'string' ? validateDirectory(directory) : invalid('Invalid path.');
  if (!parsed.ok || parsed.directory === null || parsed.directory !== directory) {
    throw new Error('Target directory must be an explicit absolute path.');
  }
  if (WINDOWS_ABSOLUTE.test(directory)) {
    const separator = directory.includes('\\') ? '\\' : '/';
    return directory.replace(/[\\/]+$/, '') + separator + name;
  }
  // Backslashes are ordinary POSIX filename characters, not separators.
  return directory.replace(/\/+$/, '') + '/' + name;
}

export function classifyStat(stat) {
  if (!stat || !['file', 'dir', 'other'].includes(stat.kind)) {
    return unknown('狀態回傳格式無法辨識；請核對目前版本。');
  }
  return {
    status: 'exists',
    label: '路徑存在，內容待審閱',
    detail: '本次只核對路徑，不判斷內容、品質或是否為一般檔案。',
  };
}

export function classifyListedTarget(entries, directory, name) {
  // Validate the whole successful listing before treating absence as evidence.
  // A rejected call must never be replaced with an empty array by the caller.
  if (!Array.isArray(entries) || entries.some((entry) =>
    !entry || typeof entry.name !== 'string' || !entry.name ||
    entry.name === '.' || entry.name === '..' || /[\/\u0000]/.test(entry.name) ||
    !['file', 'dir', 'other'].includes(entry.kind))) {
    return unknown('資料夾清單格式無法辨識；請核對目前版本。');
  }
  targetPath(directory, name);
  const entry = entries.find((item) => item.name === name);
  if (entry) return classifyStat(entry);
  // Path spelling alone cannot tell us whether this filesystem folds case.
  // Neither claim missing nor imply the requested spelling works in this case.
  if (entries.some((item) => item.name.toLowerCase() === name.toLowerCase())) {
    return unknown('找到大小寫不同的檔名；請核對約定檔名。');
  }
  return { status: 'missing', label: '缺少', detail: '本次成功讀取的資料夾清單中沒有這個檔名。' };
}

export function classifyStatError(error) {
  // Folder diagnostics only. Child absence comes from a successful listing.
  // Never guess codes from messages: a permission error can mention ENOENT.md.
  const code = error && typeof error.code === 'string' ? error.code : null;
  if (code === 'ENOENT') {
    return { status: 'missing', label: '缺少', detail: '找不到這個指定路徑。' };
  }
  if (code === 'EACCES' || code === 'EPERM') {
    return unknown('存取遭拒；請核對資料夾與存取權限。');
  }
  if (code === 'ENOTDIR') return unknown('路徑中有一段不是資料夾；請核對完整路徑。');
  return unknown('無法取得可判讀的狀態；請核對資料夾、存取權限及版本。');
}

function unknown(detail) {
  return { status: 'unknown', label: '無法檢查', detail };
}

export function formatCheckedAt(milliseconds) {
  if (typeof milliseconds !== 'number' || !Number.isFinite(milliseconds)) return null;
  const date = new Date(milliseconds);
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
}
