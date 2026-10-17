#!/usr/bin/env python3

"""Build a byte-exact guarded candidate for the captured host deploy script.

This builder never writes the production host script. Its output is a reviewed
candidate; installation needs a separate named host-write approval and live
source hash readback. The source must be the independently captured LF-only
script at ORIGINAL_SHA256, not a similarly named local file.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
from pathlib import Path

ORIGINAL_SHA256 = "c8bb3559f6b7e25e11c3bdf207c2f8dabd28835119c78494b3c9ad8bb75bd64f"
GUARD_MARKER = "A01_EXACT_MAIN_AND_ENV_GUARD_V1"


def replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise ValueError(
            f"expected one source anchor, got {source.count(old)}: {old[:50]!r}"
        )
    return source.replace(old, new, 1)


def build(raw: bytes) -> bytes:
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA256:
        raise ValueError("captured host script SHA-256 drift")
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise ValueError("captured host script must be LF-only")
    source = raw.decode("utf-8")
    source = replace_once(
        source,
        "IGNORE_HOLD=0\n",
        "IGNORE_HOLD=0\n"
        "# A01_EXACT_MAIN_AND_ENV_GUARD_V1: opt-in, immutable cutover inputs.\n"
        'EXPECTED_MAIN_SHA=""\nEXPECTED_ENV_SHA256=""\n'
        'EXPECTED_REDIS_URL_SHA256=""\nEXPECTED_HOLD_SHA256=""\nPINNED_ENV_FILE=""\n'
        "cleanup_pinned_env() {\n"
        '  [[ -z "$PINNED_ENV_FILE" ]] || rm -f -- "$PINNED_ENV_FILE"\n'
        "}\n"
        "trap cleanup_pinned_env EXIT\n",
    )
    source = replace_once(
        source,
        "    --ignore-hold) IGNORE_HOLD=1 ;;\n",
        "    --ignore-hold) IGNORE_HOLD=1 ;;\n"
        "    --expected-main-sha=*)\n"
        "      EXPECTED_MAIN_SHA=${1#*=}\n"
        "      [[ $EXPECTED_MAIN_SHA =~ ^[0-9a-f]{40}$ ]] || { echo 'invalid expected main SHA' >&2; exit 2; } ;;\n"
        "    --expected-env-sha256=*)\n"
        "      EXPECTED_ENV_SHA256=${1#*=}\n"
        "      [[ $EXPECTED_ENV_SHA256 =~ ^[0-9a-f]{64}$ ]] || { echo 'invalid expected env SHA' >&2; exit 2; } ;;\n"
        "    --expected-redis-url-sha256=*)\n"
        "      EXPECTED_REDIS_URL_SHA256=${1#*=}\n"
        "      [[ $EXPECTED_REDIS_URL_SHA256 =~ ^[0-9a-f]{64}$ ]] || { echo 'invalid expected Redis URL SHA' >&2; exit 2; } ;;\n"
        "    --expected-hold-sha256=*)\n"
        "      EXPECTED_HOLD_SHA256=${1#*=}\n"
        "      [[ $EXPECTED_HOLD_SHA256 =~ ^[0-9a-f]{64}$ ]] || { echo 'invalid expected hold SHA' >&2; exit 2; } ;;\n",
    )
    source = replace_once(
        source,
        'done\n\nmkdir -p "$LOG_DIR"\n',
        "done\n"
        "if [[ -n $EXPECTED_MAIN_SHA || -n $EXPECTED_ENV_SHA256 || -n $EXPECTED_REDIS_URL_SHA256 ]]; then\n"
        "  [[ -n $EXPECTED_MAIN_SHA && -n $EXPECTED_ENV_SHA256 && -n $EXPECTED_REDIS_URL_SHA256 ]] || { echo 'expected SHA flags must be paired' >&2; exit 2; }\n"
        "fi\n"
        "if [[ -n $EXPECTED_HOLD_SHA256 ]]; then\n"
        '  [[ -n $EXPECTED_MAIN_SHA && -n $EXPECTED_ENV_SHA256 && -n $EXPECTED_REDIS_URL_SHA256 && $IGNORE_HOLD -eq 1 ]] || { echo "expected hold requires pinned deploy and --ignore-hold" >&2; exit 2; }\n'
        'fi\n\nmkdir -p "$LOG_DIR"\n',
    )
    source = replace_once(
        source,
        'HOLD=""\n[[ -f "$HOLD_FILE" ]] && HOLD=',
        'if [[ -n "$EXPECTED_HOLD_SHA256" ]]; then\n'
        '  [[ -f "$HOLD_FILE" && ! -L "$HOLD_FILE" ]] || fail "pinned A01 hold missing"\n'
        '  actual_hold=$(sha256sum -- "$HOLD_FILE") || fail "pinned A01 hold unreadable"\n'
        '  [[ "${actual_hold%% *}" == "$EXPECTED_HOLD_SHA256" ]] || fail "pinned A01 hold changed"\n'
        "fi\n"
        'HOLD=""\n[[ -f "$HOLD_FILE" ]] && HOLD=',
    )
    source = replace_once(
        source,
        'PENDING=$(pending_releases)\n[[ -n "$PENDING" ]] && HOLD=',
        "PENDING=$(pending_releases)\n"
        '[[ -z "$EXPECTED_HOLD_SHA256" || -z "$PENDING" ]] || fail "another staged release appeared"\n'
        '[[ -n "$PENDING" ]] && HOLD=',
    )
    source = replace_once(
        source,
        'compose() { docker compose -f "$COMPOSE_FILE" --profile "$PROFILE" --profile news --profile video "$@"; }\n',
        "assert_pinned_env() {\n"
        '  [[ -z "$EXPECTED_ENV_SHA256" ]] && return 0\n'
        '  [[ -f "$PINNED_ENV_FILE" && ! -L "$PINNED_ENV_FILE" ]] || fail "pinned env snapshot missing"\n'
        '  [[ "${RUNTIME_ENV_FILE:-}" == "$PINNED_ENV_FILE" ]] || fail "runtime env path changed"\n'
        "  local actual\n"
        '  actual=$(sha256sum -- "$PINNED_ENV_FILE")\n'
        '  [[ "${actual%% *}" == "$EXPECTED_ENV_SHA256" ]] || fail "pinned env snapshot changed"\n'
        "}\n"
        "compose() {\n"
        '  if [[ -n "$PINNED_ENV_FILE" ]]; then\n'
        "    assert_pinned_env\n"
        '    docker compose --env-file "$PINNED_ENV_FILE" -f "$COMPOSE_FILE" --profile "$PROFILE" --profile news --profile video "$@"\n'
        "  else\n"
        '    docker compose -f "$COMPOSE_FILE" --profile "$PROFILE" --profile news --profile video "$@"\n'
        "  fi\n"
        "}\n",
    )
    source = replace_once(
        source,
        "}\n\n# Repair modes an earlier git run may already have left behind.",
        "}\n"
        "assert_pinned_redis_config() {\n"
        '  [[ -z "$EXPECTED_REDIS_URL_SHA256" ]] && return 0\n'
        "  if ! compose config --format json 2>/dev/null | python3 -c "
        "'import hashlib,json,sys; d=json.load(sys.stdin); e=sys.argv[1]; snap=sys.argv[2]; "
        's=d["services"]; required=("api","video-ai-worker"); '
        'names=tuple(n for n,v in s.items() if "REDIS_URL" in v.get("environment",{})); '
        'paths=lambda x:[v.get("path") if isinstance(v,dict) else v for v in x]; '
        'ok=set(required).issubset(names) and all(hashlib.sha256(s[n]["environment"]["REDIS_URL"].encode()).hexdigest()==e '
        'and ("env_file" not in s[n] or paths(s[n]["env_file"])==[snap]) for n in names); '
        "sys.exit(0 if ok else 1)' "
        '"$EXPECTED_REDIS_URL_SHA256" "$PINNED_ENV_FILE"; then\n'
        '    fail "rendered API or video AI worker Redis URL drifted"\n'
        "  fi\n"
        "}\n\n# Repair modes an earlier git run may already have left behind.",
    )
    source = replace_once(
        source,
        'REMOTE_SHA=$(git rev-parse "origin/$BRANCH")\n',
        'REMOTE_SHA=$(git rev-parse "origin/$BRANCH")\n'
        'if [[ -n "$EXPECTED_MAIN_SHA" ]]; then\n'
        '  [[ "$REMOTE_SHA" == "$EXPECTED_MAIN_SHA" ]] || fail "fetched main SHA changed; refusing deploy"\n'
        '  [[ -f .env && ! -L .env ]] || fail "host env source missing or symlink"\n'
        "  actual_env=$(sha256sum -- .env)\n"
        '  [[ "${actual_env%% *}" == "$EXPECTED_ENV_SHA256" ]] || fail "host env source changed; refusing deploy"\n'
        "  PINNED_ENV_FILE=$(mktemp /run/mokaair-a01-deploy-env.XXXXXXXX)\n"
        '  cat -- .env > "$PINNED_ENV_FILE"\n'
        '  chmod 600 "$PINNED_ENV_FILE"\n'
        "  assert_pinned_env\n"
        '  export RUNTIME_ENV_FILE="$PINNED_ENV_FILE"\n'
        "fi\n",
    )
    for old, new in (
        ('"HEAD..origin/$BRANCH"', '"HEAD..$REMOTE_SHA"'),
        ('"origin/$BRANCH..HEAD"', '"$REMOTE_SHA..HEAD"'),
        ('git log -1 "origin/$BRANCH"', 'git log -1 "$REMOTE_SHA"'),
        (
            'git diff --name-only HEAD "origin/$BRANCH"',
            'git diff --name-only HEAD "$REMOTE_SHA"',
        ),
        (
            'git diff --name-status HEAD "origin/$BRANCH"',
            'git diff --name-status HEAD "$REMOTE_SHA"',
        ),
        (
            'git diff --quiet HEAD "origin/$BRANCH"',
            'git diff --quiet HEAD "$REMOTE_SHA"',
        ),
        ('git diff HEAD "origin/$BRANCH"', 'git diff HEAD "$REMOTE_SHA"'),
        ('git merge --ff-only "origin/$BRANCH"', 'git merge --ff-only "$REMOTE_SHA"'),
    ):
        if old not in source:
            raise ValueError(f"missing immutable ref anchor: {old}")
        source = source.replace(old, new)
    source = replace_once(
        source,
        "trap 'rm -f -- \"$VIDEO_STAGE_DRAIN_READY_FILE\"' EXIT",
        "trap 'rm -f -- \"$VIDEO_STAGE_DRAIN_READY_FILE\"; cleanup_pinned_env' EXIT",
    )
    source = replace_once(
        source,
        '  compose up --build -d || fail "$why, and the rollback rebuild also failed - MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"',
        "  assert_pinned_redis_config\n"
        '  compose up --build -d || fail "$why, and the rollback rebuild also failed - MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"',
    )
    source = replace_once(
        source,
        "if ! compose up --build -d; then",
        "assert_pinned_redis_config\nif ! compose up --build -d; then",
    )
    if source.count(GUARD_MARKER) != 1:
        raise ValueError("guard marker count drift")
    return source.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--patch-output", type=Path)
    args = parser.parse_args()
    raw = args.capture.read_bytes()
    candidate = build(raw)
    if args.output.exists():
        if args.output.read_bytes() != candidate:
            raise ValueError("existing candidate output differs")
    else:
        args.output.write_bytes(candidate)
    if args.patch_output is not None:
        diff = "".join(
            difflib.unified_diff(
                raw.decode("utf-8").splitlines(keepends=True),
                candidate.decode("utf-8").splitlines(keepends=True),
                fromfile="deploy-travel-scanner.sh.live-c8bb3559",
                tofile="deploy-travel-scanner.sh.expected-main-env-hold",
            )
        )
        if args.patch_output.exists():
            if args.patch_output.read_bytes() != diff.encode("utf-8"):
                raise ValueError("existing patch output differs")
        else:
            args.patch_output.write_bytes(diff.encode("utf-8"))
    print(f"original_sha256={ORIGINAL_SHA256}")
    print(f"candidate_sha256={hashlib.sha256(candidate).hexdigest()}")


if __name__ == "__main__":
    main()
