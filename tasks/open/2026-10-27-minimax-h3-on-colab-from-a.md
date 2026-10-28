---
id: 2026-10-27-minimax-h3-on-colab-from-a
title: MiniMax H3 on Colab from a Claude Code cloud session: shared skill, token pairing, bootstrap
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-27T17:06:56Z
completed_at:
branch: claude/minimax-h3-colab-skill
depends_on: []
scope:
  - .agents/skills/minimax-h3-colab
  - .claude/skills/minimax-h3-colab
  - tools/minimax-h3-colab.test.mjs
---

# MiniMax H3 on Colab from a Claude Code cloud session: shared skill, token pairing, bootstrap

## Why

The owner asked (2026-10-27) whether the Codex recipe from kocpc's article
(https://www.kocpc.com.tw/archives/670501: install `killkli/minimax-h3-colab-skill`, pair the
Colab CLI with Google OAuth2, let the agent upload images and a prompt to a Colab GPU, run
MiniMax H3 there and download the MP4) can be driven from a Claude Code cloud session instead,
with a "token pairing" so the agent controls Colab. Three things stood in the way: the upstream
skill installs only into `~/.codex/skills` (Claude Code reads `.claude/skills` here); a cloud
session has no browser and a fresh container every time, so the CLI's one-time OAuth2 pairing
and its saved token do not survive; and nothing said how a clip made this way enters the drama
pipeline.

## Definition of done

- [x] A shared skill `minimax-h3-colab` (canonical under `.agents/skills`, byte-identical
      entrypoint under `.claude/skills`) that both harnesses load, passing `tools/skills.test.mjs`.
- [x] A fresh browserless shell can be made ready with one command: the Colab CLI (pinned
      0.7.5) and the upstream skill (pinned commit, cloned, not vendored: it has no licence
      file) are installed, the token is restored from the environment secret
      `COLAB_CLI_TOKEN_JSON`, and the pairing is proven by `colab usage` printing the balance
      (exit 4 otherwise).
- [x] The pairing itself can be done from inside a cloud session: a helper keeps the CLI's
      sign-in process alive in the background, prints the URL, takes the code the owner pastes
      later, and exports the saved token as one line for the secret.
- [x] Offline tests with a fake `colab` cover the helper, the token and verify steps and the
      runner wrapper (`tools/minimax-h3-colab.test.mjs`).
- [x] The references say how a Colab clip reaches `clips import` (provider `external`,
      note `route=colab-h3`, CU receipts), and which works cannot take it (any with a
      production profile; 1344×768 is not native 1080p).
- [ ] One real pairing and one real clip (owner's Google account and compute units; this
      session has neither): fill the "not tried" rows of `cloud-pairing.md` §4 (does `colab new`
      and the WebSocket `exec` pass the cloud proxy, A100 usage rate, cold start, CU per 5-second
      clip) and record them there.

## Steps

- [x] Read the article, the upstream repo at `0a0d3b9c`, and google-colab-cli 0.7.5's `auth.py`
      (remote copy-paste OAuth flow via `sdk.cloud.google.com`, token at
      `~/.config/colab-cli/token.json`, scopes include `cloud-platform`).
- [x] `scripts/pair.py` (headless pairing), `scripts/bootstrap.sh` (install | token | verify),
      `scripts/h3.sh` (wrapper over upstream `runner.py`), two references, SKILL.md and its copy.
- [x] Verified in this container: `uv tool install google-colab-cli==0.7.5` through the proxy,
      the OAuth URL prints without a browser, `colab.research.google.com` and
      `accounts.google.com` are reachable, `bootstrap.sh install` and `verify` behave.
- [ ] Owner: pair once (route A or B in `cloud-pairing.md` §3), store `COLAB_CLI_TOKEN_JSON`,
      approve the first paid batch; agent: run the three-shot pilot and record the numbers.
- [ ] Follow-up, outside this scope: add the skill to the list in `AGENTS.md` (that file was in
      the active scope of `2026-10-14-curio-episodes-keep-the-series-look` when this was claimed).

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh install && bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh verify   # exit 4 until paired
```

With a paired account: `bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage` prints the
balance as JSON; a `single --mode first_frame` run downloads an MP4 with video and audio streams.

## Notes

- The "token pairing" is the Colab CLI's own OAuth2 refresh token, not anything of Claude's:
  pair once, `pair.py export`, store as the cloud environment's secret `COLAB_CLI_TOKEN_JSON`.
  The environment's setup script cannot read secrets, so `bootstrap.sh token` runs in-session.
- The token carries `cloud-platform` scope. Pair with a Google account that has the Google AI
  Pro/Ultra subscription and no GCP projects or billing; revoke under the account's third-party
  access ("Google Cloud SDK") to invalidate a leaked one.
- What runs on Colab is ComfyUI with Turbo LoRAs (Ref2VA: the official 4-step LoRA;
  first_frame: a community v4 Turbo LoRA), output up to 1344×768 at 24 fps with an AAC track,
  4–15 requested seconds (frames align to 17k+5). It is not the MiniMax API's H3 nor Hailuo's web
  H3, so none of the `providers-and-plans.md` measurements apply; the pilot has to look.
- Quota per the article (not measured here): Google AI Pro gives 200 CU a month, about 1 CU per
  12-second clip. The A100 high-RAM hourly rate is whatever `colab usage` prints.
- Running the upstream unit tests here was refused by the session's permission classifier
  ("code from external"); `h3.sh test` runs them where a person allows it.
- The classifier also means a cloud session may be asked for permission on the first
  `bootstrap.sh install` (it installs a tool and clones a repository).

### 2026-10-27: tooling landed, ticket handed back (claude-fable-5-1-minimax-h3-colab)

PR #1894 merged with everything above except the two items that need the owner's Google
account and compute units (the real pairing and the first paid clip), so the ticket goes back to
`open` instead of `done`: whoever runs the first real batch ticks them and fills the "not tried"
rows of `cloud-pairing.md` §4. The AGENTS.md follow-up still waits on the active scope of
`2026-10-14-curio-episodes-keep-the-series-look`.
