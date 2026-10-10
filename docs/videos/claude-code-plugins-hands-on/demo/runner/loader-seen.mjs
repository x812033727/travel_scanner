// What the debug record and stderr say about plugins, as counts.
// Usage: node loader-seen.mjs <logs>/<name>.debug.txt <logs>/<name>.stderr.txt
// The debug record's format is not documented, so nothing here is scored. Lines that name the
// seed's plugin are printed with every list, every quoted string that is not the seed's and
// every other plugin id emptied; everything else is a number. No name or path of a plugin,
// marketplace, skill or agent that is not the seed's is printed.
import { existsSync, readFileSync } from 'node:fs';

const [debugFile, stderrFile] = process.argv.slice(2);
const linesOf = (file) => (file && existsSync(file) ? readFileSync(file, 'utf8').split('\n').filter(Boolean) : null);
const debug = linesOf(debugFile);
const stderr = linesOf(stderrFile);
const OURS = /ship-kit|release-prep|log-scout|guard\.mjs/;
const count = (lines, pattern) => lines.filter((line) => pattern.test(line)).length;

if (debug === null) {
  console.log('   debug record: no such file');
} else {
  const about = debug.filter((line) => /plugin|marketplace/i.test(line));
  const ids = about.flatMap((line) => line.match(/[a-z0-9][a-z0-9._-]*@(inline|skills-dir|synced|[a-z0-9][a-z0-9._-]*)/gi) ?? []);
  const seeds = ids.filter((id) => id.startsWith('ship-kit@'));
  const others = new Set(ids.filter((id) => !id.startsWith('ship-kit@')));
  console.log(`   debug record: ${debug.length} lines | that say plugin or marketplace: ${about.length} | that name ship-kit: ${count(debug, /ship-kit/)} | that say guard.mjs: ${count(debug, /guard\.mjs/)}`);
  console.log(`   ids of the form name@origin on those lines: the seed's ${seeds.length} (${[...new Set(seeds)].join(', ') || 'none'}) | any other, distinct: ${others.size} (count only)`);
  console.log(`   lines that say: marketplace ${count(debug, /marketplace/i)} | installed_plugins ${count(debug, /installed_plugins/i)} | enabledPlugins ${count(debug, /enabledPlugins/i)} | synced ${count(debug, /synced/i)} | trust ${count(debug, /trust/i)} | --plugin-dir ${count(debug, /plugin-dir/i)} | userSettings ${count(debug, /userSettings/)} | policySettings or managed ${count(debug, /policySettings|managed/i)}`);
  const pairs = {};
  for (const line of debug.filter((each) => /skill|agent|plugin|hook/i.test(each))) {
    for (const pair of line.match(/\b(managed|policy|user|project|local|plugin|built-?in|bundled|flag|cli|inline|session)[a-z]*: ?\d+/gi) ?? []) pairs[pair] = (pairs[pair] ?? 0) + 1;
  }
  console.log(`   "source: number" pairs on lines about skills, agents, plugins or hooks: ${Object.entries(pairs).map(([pair, times]) => `${pair} (x${times})`).join(' | ') || 'none'}`);
  const shown = debug.filter((line) => OURS.test(line) && /plugin|hook/i.test(line)).slice(0, 14);
  console.log(`   the first ${shown.length} lines that name the seed's parts and say plugin or hook (time stamps cut, lists and other names emptied):`);
  for (const line of shown) {
    const text = line.replace(/^\S+ /, '')
      .replace(/\[[^\]]*\]/g, (list) => (OURS.test(list) && list.length < 80 && !/,/.test(list) ? list : '[...]'))
      .replace(/"[^"]*"/g, (quoted) => (OURS.test(quoted) ? quoted : '"..."'))
      .replace(/[a-z0-9][a-z0-9._-]*@(inline|skills-dir|synced|[a-z0-9][a-z0-9._-]*)/gi, (id) => (id.startsWith('ship-kit@') ? id : '<another-plugin>'));
    console.log(`      | ${text.slice(0, 220)}`);
  }
}
if (stderr === null) console.log('   stderr: no such file');
else console.log(`   stderr: ${stderr.length} lines | that say plugin ${count(stderr, /plugin/i)} | trust ${count(stderr, /trust/i)} | hook ${count(stderr, /hook/i)} | warning ${count(stderr, /warn/i)}`);
