import { readFileSync } from 'node:fs';
const path = process.argv[2] ?? 'config/settings.shared.json';
const allowed = new Set(['permissions', 'env', 'hooks']);
try {
  const config = JSON.parse(readFileSync(path, 'utf8'));
  if (!config || Array.isArray(config) || typeof config !== 'object') throw new Error('設定必須是物件');
  const unknown = Object.keys(config).filter(key => !allowed.has(key));
  if (unknown.length) throw new Error('本課程設定範本未允許：' + unknown.join(', '));
  if (config.permissions) for (const key of ['allow','deny','ask']) {
    const value = config.permissions[key];
    if (value !== undefined && (!Array.isArray(value) || value.some(v => typeof v !== 'string'))) throw new Error('權限必須是字串清單');
  }
  console.log(JSON.stringify({ok:true,scope:'course-template-only'}));
} catch(error) { console.error(error.message); process.exitCode = 2; }
