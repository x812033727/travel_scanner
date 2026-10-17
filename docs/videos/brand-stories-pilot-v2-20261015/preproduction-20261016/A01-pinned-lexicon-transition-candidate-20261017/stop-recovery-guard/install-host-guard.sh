#!/usr/bin/env bash
# Candidate only. --check is read-only; --install needs exact site-owner approval.
set -euo pipefail
case "${1:---check}" in
  --check|--install) mode="${1:---check}" ;;
  *) echo 'usage: install-host-guard.sh --check|--install' >&2; exit 2 ;;
esac
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
volume=/var/lib/docker/volumes/travel_scanner_video_work/_data
stop="$volume/story-rolling-suitcase-v2/STOP"
unit='mokaair-a01-review@.service'
helpers=(a01_stop_guard.py a01_phase_runner.py a01_phase_recover.py)
[[ "$(id -u)" == 0 ]] || { echo 'root required' >&2; exit 1; }
[[ "$(docker volume inspect travel_scanner_video_work --format '{{.Mountpoint}}')" == "$volume" ]] || {
  echo 'named volume mountpoint changed; stop and review' >&2; exit 1;
}
[[ -f "$stop" && ! -L "$stop" ]] || { echo 'A01 project STOP missing or not regular' >&2; exit 1; }
# This revision deliberately has no site-wide docker.service dependency. Refuse
# an older boot-hook install so a reviewer can reconcile it explicitly.
[[ ! -e /etc/systemd/system/mokaair-a01-stop-restore.service ]] || {
  echo 'unexpected older Docker boot guard; inspect before installing' >&2; exit 1;
}
created=()
temps=()
for name in "${helpers[@]}"; do
  source_file="$source_dir/$name"; target="/usr/local/sbin/$name"
  [[ -f "$source_file" && ! -L "$source_file" ]] || { echo "candidate file missing: $name" >&2; exit 1; }
  if [[ -e "$target" || -L "$target" ]]; then
    [[ -f "$target" && ! -L "$target" ]] && cmp -s "$source_file" "$target" || {
      echo "installed helper differs: $target" >&2; exit 1;
    }
  fi
done
[[ -f "$source_dir/$unit" && ! -L "$source_dir/$unit" ]] || {
  echo "candidate unit missing: $unit" >&2; exit 1;
}
if [[ -e "/etc/systemd/system/$unit" || -L "/etc/systemd/system/$unit" ]]; then
  [[ -f "/etc/systemd/system/$unit" && ! -L "/etc/systemd/system/$unit" ]] &&
    cmp -s "$source_dir/$unit" "/etc/systemd/system/$unit" || {
      echo "installed unit differs: $unit" >&2; exit 1;
    }
fi
for name in "${helpers[@]}" "$unit"; do sha256sum "$source_dir/$name"; done
printf 'A01 guard precheck: STOP present, volume pinned, mode=%s\n' "$mode"
if [[ "$mode" == --check ]]; then
  echo 'READ ONLY: no installation performed'
  exit 0
fi
rollback() {
  local result=$?
  trap - EXIT
  for target in "${temps[@]}"; do rm -f -- "$target"; done
  if (( result != 0 )); then
    echo 'A01 guard install failed; removing only files created by this invocation' >&2
    for target in "${created[@]}"; do rm -f -- "$target"; done
    systemctl daemon-reload || true
    echo 'STOP stayed present. Read back files and unit before any phase.' >&2
  fi
  exit "$result"
}
trap rollback EXIT
install_new() {
  local source_file=$1 target=$2 mode=$3 temporary
  temporary="$(mktemp "${target}.a01-install.XXXXXXXX")"
  temps+=("$temporary")
  install -m "$mode" "$source_file" "$temporary"
  cmp -s "$source_file" "$temporary"
  # Hardlink creation refuses an unexpected existing target and publishes a
  # complete copy atomically. A SIGKILL may leave the complete file to inspect.
  ln -- "$temporary" "$target"
  created+=("$target")
  rm -f -- "$temporary"
}
for name in "${helpers[@]}"; do
  target="/usr/local/sbin/$name"
  if [[ ! -e "$target" ]]; then
    install_new "$source_dir/$name" "$target" 0700
  fi
done
if [[ ! -e "/etc/systemd/system/$unit" ]]; then
  install_new "$source_dir/$unit" "/etc/systemd/system/$unit" 0644
fi
systemd-analyze verify "/etc/systemd/system/$unit"
systemctl daemon-reload
for name in "${helpers[@]}"; do cmp -s "$source_dir/$name" "/usr/local/sbin/$name"; done
cmp -s "$source_dir/$unit" "/etc/systemd/system/$unit"
[[ "$(systemctl show mokaair-a01-review@validate.service -p FragmentPath --value --no-pager)" == "/etc/systemd/system/$unit" ]]
echo 'Phase unit and helpers installed/read back. No boot dependency; incomplete manifest refuses any phase.'
trap - EXIT
