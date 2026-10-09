import type { Register } from 'claude-code'

// A pipeline's exit code is its last command's, so
// `npm run lint | tail` exits 0 when lint fails. Only tail is
// handled: head closes the pipe early, and pipefail would turn
// a pass into exit 141.
const CHECKS = [
  'npm\\s+(run\\s+)?(lint|test|typecheck|check)[\\w:-]*',
  'npx\\s+(tsc|eslint|vitest|playwright)',
  'pytest',
  'ruff',
  'mypy',
  'tsc',
  'git\\s+(merge|rebase|pull)',
]
const CHECK = new RegExp(`\\b(${CHECKS.join('|')})\\b`)
const INTO_TAIL = /\|\s*tail\b/
const ALREADY_SAFE = /pipefail|PIPESTATUS/

export const register: Register = on => {
  on('tool.call', { tool: 'Bash' }, ($, e, next) => {
    const isMasked =
      CHECK.test(e.command) &&
      INTO_TAIL.test(e.command) &&
      !ALREADY_SAFE.test(e.command)

    if (!isMasked) {
      return next(e)
    }

    $.ui.toast('pipe-guard：加上 pipefail，tail 遮不住失敗')

    const command = `set -o pipefail; ${e.command}`

    return next({ ...e, command })
  })
}
