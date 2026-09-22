#!/usr/bin/env bash
# Land one pull request under strict branch protection.
#
#   bash .agents/skills/task-board/scripts/merge-when-green.sh <pr-number> [max-rounds]
#
# Run it from the worktree that has the PR branch checked out. Each round: rebase onto
# origin/main, push with a lease, wait for the checks, read every check-run of the exact head
# (never `gh pr checks --watch | tail`), and squash-merge with --match-head-commit so a head
# somebody pushed meanwhile is refused rather than merged untested. `strict` protection means
# another merge can put the branch BEHIND again, so it retries up to max-rounds (default 3).
# It stops on a rebase conflict (fix by hand, rerun) and never uses --admin or --auto.
set -euo pipefail

pr="${1:?usage: merge-when-green.sh <pr-number> [max-rounds]}"
rounds="${2:-3}"
required="api web containers full-stack-smoke"

branch=$(gh pr view "$pr" --json headRefName -q .headRefName)
current=$(git rev-parse --abbrev-ref HEAD)
if [ "$current" != "$branch" ]; then
  echo "PR #$pr is on '$branch' but this worktree is on '$current'; check out the branch first" >&2
  exit 2
fi

for round in $(seq 1 "$rounds"); do
  git fetch -q origin main
  if ! git rebase origin/main; then
    git rebase --abort
    echo "round $round: rebase conflict; resolve it by hand, then rerun" >&2
    exit 3
  fi
  git push --force-with-lease origin "$branch"
  head=$(git rev-parse HEAD)
  echo "round $round: head $head pushed, waiting for checks"
  sleep 45
  gh pr checks "$pr" --watch --interval 30 >/dev/null 2>&1 || true

  failed=""
  pending=""
  for name in $required; do
    row=$(gh api "repos/{owner}/{repo}/commits/$head/check-runs?check_name=$name" \
      -q '[.check_runs[] | "\(.status)/\(.conclusion)"] | join(" ")')
    case " $row " in
      *" completed/success "*) ;;
      *" completed/"*) failed="$failed $name" ;;
      *) pending="$pending $name" ;;
    esac
  done
  if [ -n "$failed" ]; then
    echo "round $round: required checks failed:$failed" >&2
    echo "read them with: gh api repos/{owner}/{repo}/commits/$head/check-runs -q '.check_runs[] | \"\\(.name)\\t\\(.status)\\t\\(.conclusion)\"'" >&2
    exit 4
  fi
  if [ -n "$pending" ]; then
    echo "round $round: still pending:$pending (rerun when they finish)" >&2
    exit 5
  fi

  state=$(gh pr view "$pr" --json mergeStateStatus -q .mergeStateStatus)
  case "$state" in
    CLEAN|HAS_HOOKS|UNSTABLE)
      gh pr merge "$pr" --squash --match-head-commit "$head"
      final=$(gh pr view "$pr" --json state -q .state)
      echo "PR #$pr: $final"
      [ "$final" = "MERGED" ] && exit 0
      exit 6
      ;;
    BEHIND|DIRTY|UNKNOWN)
      echo "round $round: mergeStateStatus=$state, main moved; rebasing again"
      ;;
    *)
      echo "round $round: mergeStateStatus=$state; stopping" >&2
      exit 7
      ;;
  esac
done
echo "gave up after $rounds rounds; main keeps moving, rerun later" >&2
exit 8
