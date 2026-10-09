import { expect, test } from 'claude-code/testing'

const PLINK = '"/c/Program Files/PuTTY/plink.exe"'
const SSH = `${PLINK} -batch -load <saved-session> "id"`
const bash = (command: string) => ({ tool: 'Bash', command })

test(
  'counts plink connections and leaves other commands alone',
  async ($, on) => {
    on('tool.call', () => ({ result: 'ok' }))

    await $.tool.call(bash(SSH))
    await $.tool.call(bash('git status'))
    await $.tool.call(bash('grep plink notes.md'))
    await $.tool.call({
      tool: 'PowerShell',
      command: 'plink.exe -batch -load <saved-session> "id"',
    })

    const answer = await $.command.run({
      command: 'plink',
      args: '',
    })
    expect(answer.text).toBe(
      '這個 session 已經開了 2 次 SSH 連線，上限 30 次',
    )
  },
)

test(
  'refuses the connection past the limit, ' +
    'and /plink reset lifts it',
  async ($, on) => {
    let ran = 0
    on('tool.call', () => {
      ran += 1

      return { result: 'ok' }
    })

    for (let i = 0; i < 30; i += 1) {
      await $.tool.call(bash(SSH))
    }
    expect(ran).toBe(30)

    const refused = await $.tool.call(bash(SSH))
    expect(ran).toBe(30)
    const said = String(refused.deny ?? refused.text)
    expect(said).toContain('plink-budget')

    await $.command.run({ command: 'plink', args: 'reset' })
    await $.tool.call(bash(SSH))
    expect(ran).toBe(31)
  },
)
