#!/usr/bin/env bash
# Install ffmpeg from the Ubuntu archive, falling back to the main mirror when the runner's own one crawls.
#
# GitHub's runners point apt at azure.archive.ubuntu.com. On 2026-10-26 that mirror served
# packages at tens of KB/s on some runners (13.5 MB libflite1 in four to six minutes), so one
# install outlasted the 20-minute video-tests job twice before any test ran, while a sibling
# job on another runner installed the same packages in under a minute. Each attempt here gets
# a deadline well inside the job (a healthy install takes under a minute); the second and
# third go to archive.ubuntu.com instead.
#
# The pipeline's ffmpeg lookup (tools/video/assemble/ffmpeg.mjs) wants libx264; a build without
# it fails here, by name, instead of as six ToolMissing test failures.
set -euo pipefail

apt_options=(-o Acquire::Retries=3 -o Acquire::http::Timeout=30)
for attempt in 1 2 3; do
  if [ "$attempt" -gt 1 ]; then
    # A deadline can land mid-unpack; finish what dpkg started before trying again.
    sudo dpkg --configure -a || true
    sudo sed -i 's#http://azure\.archive\.ubuntu\.com/ubuntu#http://archive.ubuntu.com/ubuntu#g' \
      /etc/apt/sources.list.d/*.sources /etc/apt/sources.list 2>/dev/null || true
  fi
  if timeout 90 sudo apt-get "${apt_options[@]}" update \
    && timeout 240 sudo apt-get "${apt_options[@]}" install -y --no-install-recommends ffmpeg; then
    break
  fi
  if [ "$attempt" = 3 ]; then exit 1; fi
  sleep $((attempt * 10))
done

ffmpeg -hide_banner -version | sed -n 1p
encoders=$(ffmpeg -hide_banner -encoders)
if ! grep -qw libx264 <<<"$encoders"; then
  echo "::error::the installed ffmpeg has no libx264 encoder"
  exit 1
fi
