// runner: one place for what is hidden before anything is printed or written into the repository.
// Paths become <lab>, <plugin>, <logs>, <seed>, <work>, <home>; the user and host names (whole
// words, any case) become <user> and <host>; long ids become <uuid>, toolu_<id>, agent-<id>,
// req_<id>; Claude Code's own project-folder slug becomes <project-slug>.
import { homedir, hostname, userInfo } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
export const WORK = join(here, '..', '..');
export const SEED = join(WORK, '_tools', 'seed');
export const RUNNER = here;
export const LOGS = join(WORK, 'run', 'logs');
export const LAB = join(WORK, 'run', 'lab');
export const KIT = join(WORK, 'run', 'ship-kit');
export const DRY = join(WORK, 'run', 'dry');

const esc = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
// Every way one folder is written: C:\\a\\b (inside JSON text), C:\a\b, C:/a/b, /c/a/b, and
// either case of the drive letter.
export const spellings = (path) => {
  if (!path) return [];
  const forward = String(path).replaceAll('\\', '/').replace(/\/$/, '');
  const drives = /^[A-Za-z]:/.test(forward)
    ? [forward[0].toUpperCase() + forward.slice(1), forward[0].toLowerCase() + forward.slice(1)] : [forward];
  const out = [];
  for (const each of drives) {
    out.push(each.replaceAll('/', '\\\\'), each.replaceAll('/', '\\'), each);
    if (/^[A-Za-z]:/.test(each)) out.push(`/${each[0].toLowerCase()}${each.slice(2)}`);
  }
  return [...new Set(out)];
};

export function makeMask(extra = []) {
  // Longest first: <lab>, <plugin>, <logs> and <seed> lie inside <work>, which lies inside <home>.
  const pairs = [...extra, [join(DRY, 'lab'), '<dry>/lab'], [join(DRY, 'ship-kit'), '<dry>/ship-kit'], [DRY, '<dry>'],
    [LAB, '<lab>'], [KIT, '<plugin>'], [LOGS, '<logs>'], [RUNNER, '<runner>'], [SEED, '<seed>'], [WORK, '<work>'], [homedir(), '<home>']]
    .filter(([path]) => path);
  const user = new RegExp(`\\b${esc(userInfo().username)}\\b`, 'gi');
  const host = new RegExp(`\\b${esc(hostname())}\\b`, 'gi');
  return (text) => {
    // The transcript of a background subagent lies in Claude Code's own temporary folder below
    // the home directory: the whole path is left out.
    let shown = String(text ?? '').replace(/(output_file:? ?"?)[^\s"]+\.output/g, '$1<a file in Claude Code\'s temporary folder, not shown>');
    for (const [path, mark] of pairs) for (const each of spellings(path)) shown = shown.split(each).join(mark);
    return shown
      .replace(/[A-Za-z]--Users-[A-Za-z0-9-]+/g, '<project-slug>')
      .replace(user, '<user>').replace(host, '<host>')
      .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<uuid>')
      .replace(/toolu_[0-9A-Za-z]{6,}/g, 'toolu_<id>')
      .replace(/agent-[0-9a-f]{6,}/g, 'agent-<id>')
      .replace(/(agentId:? ?"?)[0-9a-f]{8,}/g, '$1<id>')
      .replace(/([\\/]tasks[\\/]+)[0-9a-z]{8,}(\.output)/g, '$1<id>$2')
      .replace(/req_[0-9A-Za-z]{10,}/g, 'req_<id>');
  };
}

export const BUILT_IN_AGENTS = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
// The same list the seed's tally.mjs and runner/models.mjs carry.
export const SHIPPED_SKILLS = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides', 'init', 'security-review', 'keybindings-help']);
export const OUR_SKILL = /^(ship-kit:)?release-prep$/;
export const OUR_AGENT = /^(ship-kit:)?log-scout$/;
export const skillName = (value) => {
  const skill = String(value ?? '').replace(/^\//, '');
  return OUR_SKILL.test(skill) || SHIPPED_SKILLS.has(skill) ? skill : '(another skill)';
};
export const agentName = (value) => (!value ? '(no type given)' : OUR_AGENT.test(value) || BUILT_IN_AGENTS.has(value) ? value : '(another agent)');
export const readStream = (text) => text.split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((line) => line.type !== 'rate_limit_event');
