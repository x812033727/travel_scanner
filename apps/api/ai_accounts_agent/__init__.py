"""Host agent that logs the root Claude Code and Codex CLIs into subscription accounts.

It runs as a systemd service next to the deployment agent and answers a fixed set of
HMAC-signed requests on a Unix socket that only the API container can open. See
``ops/ai-accounts/README.md`` for the install steps and the trust boundary.
"""
