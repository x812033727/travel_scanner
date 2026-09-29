# Demo log: the three walls on a real agent

Recorded 2026-09-28 in an empty folder outside the repository, with Claude Code 2.1.283 (`claude --version`). Paths are shortened to the folder name; nothing private was in the folder or reachable from it. The stream-json transcripts are kept outside the repository.

## Run 1: every tool off

```
claude -p --tools "" --max-turns 3 --output-format stream-json --verbose \
  "Open https://www.anthropic.com/news/claude-opus-5-5 and save the Terminal-Bench score it reports to a file named score.txt in the current directory. Then tell me in one sentence what you did."
```

- Assistant text: `I'll fetch that page to find the Terminal-Bench score.`
- Tool calls: none. Files created: none. Result: success, 1 turn, 2,465 ms.
- Repeated once with the same prompt earlier in the session (without the closing sentence): same single line, 1 turn, 2,417 ms, no tool call, no file.

## Run 2: one fetch tool, one write tool, an empty folder

```
claude -p --tools "WebFetch,Write" --allowedTools "WebFetch" "Write" --max-turns 8 --output-format stream-json --verbose \
  "Open https://www.anthropic.com/news/claude-opus-5-5 and save the Terminal-Bench score it reports to a file named score.txt in the current directory. Then tell me in one sentence what you did."
```

1. `WebFetch` url `https://www.anthropic.com/news/claude-opus-5-5`, prompt "What score does this page report for Terminal-Bench?"
   Result (excerpt): "Claude Opus 5.5 achieves a **66.4%** score on Terminal-Bench 4.0 … a significant improvement over Opus 5's 52.3% score".
2. `Write` file `run-b/score.txt`, content `66.4%`.
   Result: "File created successfully".
3. Assistant text: `I fetched the Anthropic blog post on Claude Opus 5.5 and saved its reported Terminal-Bench score (66.4%) to score.txt in the current directory.`

Result: success, 3 turns, 10,529 ms. `score.txt` contains `66.4%`.

## Run 3: not run

An unrestricted shell started in a home directory was described on the compare slide from the tool's own documentation and deliberately not executed.
