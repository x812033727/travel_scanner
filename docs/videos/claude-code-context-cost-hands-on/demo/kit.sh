#!/usr/bin/env bash
# Builds the ship-kit plugin from the seed's neutral file names: the same six files the plugins
# video loaded (a manifest, one skill with its template, one agent, one hook and its script).
#
#   bash <seed>/kit.sh <folder>
#
# The seed keeps every part under a name Claude Code does not look for (parts/manifest.json,
# parts/release-prep.skill.md, parts/hooks.plugin.json ...), so a copy of the seed inside a
# repository is neither a plugin nor a marketplace. This script puts them where a plugin's parts
# go: <folder>/.claude-plugin/plugin.json, skills/release-prep/SKILL.md and template.md,
# agents/log-scout.md, hooks/hooks.json and scripts/guard.mjs.
#
# It refuses to build inside a git repository. The check is made on the file system (a .git
# entry in the folder or in any folder above it), so it starts no git command. It also refuses
# (exit 5) a folder that already holds something it did not build: never point it at a folder
# of your own.
set -u
dest="${1:?folder to build the plugin in}"
seed="$(cd "$(dirname "$0")" && pwd)"

probe="$dest"
while [ ! -d "$probe" ]; do probe="$(dirname "$probe")"; done
probe="$(cd "$probe" && pwd)"
while :; do
  if [ -e "$probe/.git" ]; then
    echo "refused: the plugin folder is inside a git repository." >&2
    exit 4
  fi
  [ "$(dirname "$probe")" = "$probe" ] && break
  probe="$(dirname "$probe")"
done

# The folder is deleted and rebuilt. One that exists, is not empty and is not a plugin folder
# this script built is somebody's own: refuse, delete nothing.
if { [ -d "$dest" ] && [ -n "$(ls -A "$dest" 2>/dev/null)" ] && [ ! -f "$dest/.claude-plugin/plugin.json" ]; } || { [ -e "$dest" ] && [ ! -d "$dest" ]; }; then
  echo "refused: the plugin folder exists and was not built by this script. Nothing was deleted." >&2
  exit 5
fi

rm -rf "$dest"
mkdir -p "$dest/.claude-plugin" "$dest/skills/release-prep" "$dest/agents" "$dest/hooks" "$dest/scripts"
cp "$seed/parts/manifest.json" "$dest/.claude-plugin/plugin.json"
cp "$seed/parts/release-prep.skill.md" "$dest/skills/release-prep/SKILL.md"
cp "$seed/parts/release-prep.template.md" "$dest/skills/release-prep/template.md"
cp "$seed/parts/log-scout.agent.md" "$dest/agents/log-scout.md"
cp "$seed/parts/hooks.plugin.json" "$dest/hooks/hooks.json"
cp "$seed/parts/guard.mjs" "$dest/scripts/guard.mjs"
