#!/bin/sh
set -eu
umask 077
# Only loopback ports are published by compose; reach noVNC through an SSH tunnel.
# VNC is additionally password-protected. The password is read from a mounted file.
test -s /run/secrets/vnc_password
mkdir -p /tmp/uploader
Xvfb :99 -screen 0 1440x1000x24 -nolisten tcp &
XVFB_PID=$!
# Wait for the X socket before starting its clients.
tries=0
until xdpyinfo -display :99 >/dev/null 2>&1; do
  tries=$((tries + 1))
  if [ "$tries" -ge 30 ]; then kill "$XVFB_PID"; exit 1; fi
  sleep 1
done
openbox >/dev/null 2>&1 &
WM_PID=$!
x11vnc -display :99 -passwdfile /run/secrets/vnc_password -forever -shared -rfbport 5900 -localhost -quiet >/dev/null 2>&1 &
VNC_PID=$!
websockify --web=/usr/share/novnc 0.0.0.0:6080 127.0.0.1:5900 >/dev/null 2>&1 &
WEB_PID=$!
node src/main.mjs &
APP_PID=$!
cleanup() {
  kill -TERM "$APP_PID" 2>/dev/null || true
  wait "$APP_PID" 2>/dev/null || true
  kill "$WEB_PID" "$VNC_PID" "$WM_PID" "$XVFB_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT
wait "$APP_PID"
