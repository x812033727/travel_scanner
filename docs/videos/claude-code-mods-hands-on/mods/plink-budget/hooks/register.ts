import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

// The host stopped answering SSH after about 40 connections
// in one session (2026-09-04), so the budget stops short.
const LIMIT = 30
const WARN_AT = 20

// plink in command position: a bare or quoted path to it,
// followed by an option
const PLINK = /(^|[\s"'/\\;&|(])plink(\.exe)?["']?\s+-/i

const count = atom(
  { plugin: 'plink-budget', key: 'count' } as const,
  0,
)

const refusal = (used: number) =>
  `plink-budget: this session has already opened ${used} ` +
  `SSH connections (limit ${LIMIT}); the host may lock SSH ` +
  'out after too many. Put the remaining remote commands ' +
  'into one script and tell the person, who can type ' +
  '/plink reset.'

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'plink',
      description: '這個 session 開了幾次 SSH 連線',
    })

    return next(e)
  })

  on('command.run', { command: 'plink' }, async ($, e) => {
    if (e.args.trim() === 'reset') {
      await update($, count, () => 0)
      $.ui.status(undefined)

      return { text: 'SSH 連線次數已歸零' }
    }

    const used = await read($, count)
    const text =
      `這個 session 已經開了 ${used} 次 SSH 連線，` +
      `上限 ${LIMIT} 次`

    return { text }
  })

  for (const tool of ['Bash', 'PowerShell'] as const) {
    on('tool.call', { tool }, async ($, e, next) => {
      if (!PLINK.test(e.command)) {
        return next(e)
      }

      const used = await read($, count)

      if (used >= LIMIT) {
        return { deny: refusal(used) }
      }

      await update($, count, n => n + 1)
      $.ui.status(`plink ${used + 1}/${LIMIT}`)

      if (used + 1 === WARN_AT) {
        $.ui.toast(`SSH 連線已經 ${WARN_AT} 次，上限 ${LIMIT} 次`)
      }

      return next(e)
    }).catch(($, e, next) =>
      next.called
        ? next(e)
        : { deny: 'plink-budget: counter failed; not run.' },
    )
  }
}
