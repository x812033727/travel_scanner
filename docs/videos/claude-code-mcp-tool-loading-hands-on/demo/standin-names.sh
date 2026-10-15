#!/usr/bin/env bash
# A stand-in for claude that m-checks.sh uses to test the record's replacements. It starts no
# session and calls no model: it writes eight lines to stderr that spell this machine's home
# folder, user name and host name in the forms a real error message could carry, one made-up
# address, and the account's address when the shell holds one. Nothing is written into this
# file: every name is read from the environment when it runs, and m-checks.sh prints only how
# many lines of the record still carry one (0 is the answer).
user="$(basename "$HOME")"
mixed="$(cygpath -m "$HOME" 2>/dev/null || printf '%s' "$HOME")"
back="$(cygpath -w "$HOME" 2>/dev/null || printf '%s' "$HOME")"
{
  echo "home $HOME"
  echo "mixed $mixed"
  echo "back $back"
  echo "url file:///$mixed/somewhere"
  echo "upper ${user^^} and lower ${user,,}"
  echo "host ${HOSTNAME:-no-host-name} and ${COMPUTERNAME:-no-host-name}"
  echo "address someone@example.com"
  echo "account ${CLAUDE_CODE_USER_EMAIL:-nobody@example.org}"
} >&2
