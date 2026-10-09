import { expect, test } from 'claude-code/testing'

test('adds pipefail when a check is piped into tail', async (
  $,
  on,
) => {
  const seen: string[] = []
  on('tool.call', (_$, e) => {
    seen.push(String(e.command))

    return { result: 'ok' }
  })

  const lint = 'npm run lint:web | tail -20'
  const merge = 'git merge origin/main 2>&1 | tail -5'
  await $.tool.call({ tool: 'Bash', command: lint })
  await $.tool.call({ tool: 'Bash', command: merge })

  expect(seen).toEqual([
    `set -o pipefail; ${lint}`,
    `set -o pipefail; ${merge}`,
  ])
})

test('leaves every other command as written', async ($, on) => {
  const seen: string[] = []
  on('tool.call', (_$, e) => {
    seen.push(String(e.command))

    return { result: 'ok' }
  })

  const untouched = [
    'npm run lint:web',
    'git log --oneline | tail -5',
    'npm run test:web | head -40',
    'set -o pipefail; npm run typecheck:web | tail -20',
  ]
  for (const command of untouched) {
    await $.tool.call({ tool: 'Bash', command })
  }

  expect(seen).toEqual(untouched)
})
