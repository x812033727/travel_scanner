# Installed by ops/ai-accounts/install.sh as /etc/profile.d/mokaair-ai-accounts.sh.
#
# In an interactive root shell, `claude`, `codex` and `agy` use the account marked as
# default on /admin/ai-accounts. The account is resolved when the command starts, so a
# session keeps its account even if the default changes while it runs. `claude-a` … `agy-e`
# pick one explicitly. Scripts that call the CLIs by path, and shells that never read this
# file, get account A through the /root/.claude, /root/.codex and
# /root/.gemini/antigravity-cli links.
if [ "$(id -u)" = 0 ] && [ -d /var/lib/mokaair-ai-accounts ]; then
  _mokaair_ai_slot() {
    _mokaair_ai_value=$(cat "/var/lib/mokaair-ai-accounts/default-$1" 2>/dev/null || true)
    case "$_mokaair_ai_value" in
      a | b | c | d | e) printf '%s' "$_mokaair_ai_value" ;;
      *) printf 'a' ;;
    esac
  }
  claude() {
    CLAUDE_CONFIG_DIR="/var/lib/mokaair-ai-accounts/claude-$(_mokaair_ai_slot claude)" \
      command claude "$@"
  }
  codex() {
    CODEX_HOME="/var/lib/mokaair-ai-accounts/codex-$(_mokaair_ai_slot codex)" \
      command codex "$@"
  }
  # Each Antigravity account is a home of its own; see mokaair-ai-cli.
  agy() {
    HOME="/var/lib/mokaair-ai-accounts/agy-$(_mokaair_ai_slot agy)" \
      DBUS_SESSION_BUS_ADDRESS="unix:path=/dev/null/mokaair-no-keyring" \
      command agy "$@"
  }
fi
