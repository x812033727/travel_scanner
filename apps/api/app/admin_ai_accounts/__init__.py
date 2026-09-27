"""Admin routes for the host's Claude Code and Codex subscription accounts.

The host agent in ``apps/api/ai_accounts_agent`` owns the CLIs and their logins; these
routes only relay fixed operations to it over its Unix socket and record them in the
admin audit log. No token or credential ever passes through here.
"""
