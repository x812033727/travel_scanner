#!/bin/sh
# Renders an SVG with a taller window so the bottom 88px that headless chromium hides in render_svg stay visible.
# usage: render_tall.sh <svg> <png>
SVG="$1"; PNG="$2"
TMP=$(mktemp -d)
printf "<!doctype html><meta charset='utf-8'><style>html,body{margin:0;padding:0;background:#fff}svg{display:block;width:1600px;height:900px}</style>" > $TMP/r.html
cat "$SVG" >> $TMP/r.html
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1600,1000 --screenshot="$PNG" "file://$TMP/r.html" >/dev/null 2>&1
rm -rf $TMP
