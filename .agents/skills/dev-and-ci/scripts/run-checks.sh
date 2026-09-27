#!/usr/bin/env bash
# Run the repository's checks by group, one log per check, and report every exit code.
#
# Why this exists: a check piped through `| tail` reports tail's exit status, so a failing
# lint or typecheck reads as a pass unless its error happens to be in the lines printed.
# Each check here writes its whole output to a file and the script prints `exit=N` for it,
# then a summary, and exits non-zero when anything failed.
#
# Usage (from anywhere inside the worktree):
#   bash .agents/skills/dev-and-ci/scripts/run-checks.sh [web] [api] [tools]   # default: all
#   CHECK_LOG_DIR=/some/dir bash .../run-checks.sh web                          # keep the logs there
#
# The groups mirror AGENTS.md "Checks before you push" and the web/api jobs of ci.yml. The
# API group runs without RUN_INTEGRATION_TESTS, so integration tests skip here and only CI
# runs them.
set -u
# On Windows the API venv prints Han text only with this set; elsewhere it is harmless.
export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"

root="$(git rev-parse --show-toplevel)" || exit 2
log_dir="${CHECK_LOG_DIR:-$(mktemp -d)}"
# A redirect into a directory that does not exist skips the command entirely.
mkdir -p "$log_dir" || exit 2

groups=("$@")
[ "${#groups[@]}" -eq 0 ] && groups=(web api tools)

failed=()
summary=()

run() {
  # run <name> <dir> <command...>
  local name="$1" dir="$2"
  shift 2
  local log="$log_dir/$name.log"
  (cd "$root/$dir" && "$@") > "$log" 2>&1
  local code=$?
  echo "$name exit=$code  ($log)"
  summary+=("$name=$code")
  [ "$code" -ne 0 ] && failed+=("$name")
  return 0
}

for group in "${groups[@]}"; do
  case "$group" in
    web)
      [ -d "$root/node_modules" ] || echo "WARNING: no node_modules in this worktree; run npm ci at its root first"
      run lint-web . npm run -s lint:web
      run check-i18n . npm run -s check:i18n
      run typecheck-web . npm run -s typecheck:web
      run test-web . npm run -s test:web
      ;;
    api)
      run ruff apps/api uv run ruff check .
      run mypy-app apps/api uv run mypy app
      run mypy-tests apps/api uv run mypy tests
      run pytest apps/api uv run pytest -q -p no:cacheprovider
      ;;
    tools)
      run test-tools . npm run -s test:tools
      run check-tasks . npm run -s check:tasks
      ;;
    *)
      echo "unknown group: $group (use web, api or tools)"
      exit 2
      ;;
  esac
done

echo "summary: ${summary[*]}"
echo "logs: $log_dir"
if [ "${#failed[@]}" -gt 0 ]; then
  echo "FAILED: ${failed[*]}"
  exit 1
fi
echo "all passed"
