#!/usr/bin/env bash
# Builds one variant of the ship-kit plugin from the seed's neutral file names.
#
#   bash <seed>/kit.sh <variant> <folder>
#
# The seed keeps every part under a name Claude Code does not look for (parts/manifest.json,
# parts/release-prep.skill.md, parts/hooks.plugin.json ...), so a copy of the seed inside a
# repository is neither a plugin nor a marketplace. This script puts them where a plugin's parts
# go: <folder>/.claude-plugin/plugin.json, skills/release-prep/SKILL.md and template.md,
# agents/log-scout.md, hooks/hooks.json and scripts/guard.mjs.
#
# variant     what differs from "good"
# good        nothing: manifest, one skill with its template, one agent, one hook and its script
# stale       hooks/hooks.json is the project's hook settings, unchanged: its script path still
#             starts at the project (${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.mjs)
# badjson     the manifest has a comma too many
# noname      the manifest has no "name"
# hookpath    the manifest adds "hooks": "./hooks/extra.json", a file that does not exist
# minimal     the manifest is only {"name": "ship-kit"}
# typo        the manifest has a key spelled "hook"
# nowrap      hooks/hooks.json is the event map without the outer "hooks" key
# noscript    scripts/guard.mjs is missing
# badagent    agents/log-scout.md has a quote that is never closed in its frontmatter
# inside      skills/ sits inside .claude-plugin/
# nomanifest  there is no .claude-plugin/ at all
#
# It refuses to build inside a git repository.
set -u
variant="${1:?variant, for example good}"
dest="${2:?folder to build the plugin in}"
seed="$(cd "$(dirname "$0")" && pwd)"

probe="$dest"
while [ ! -d "$probe" ]; do probe="$(dirname "$probe")"; done
if [ "$(git -C "$probe" rev-parse --is-inside-work-tree 2>/dev/null)" = "true" ]; then
  echo "refused: the plugin folder is inside a git repository." >&2
  exit 4
fi

rm -rf "$dest"
mkdir -p "$dest/.claude-plugin" "$dest/skills/release-prep" "$dest/agents" "$dest/hooks" "$dest/scripts"
cp "$seed/parts/manifest.json" "$dest/.claude-plugin/plugin.json"
cp "$seed/parts/release-prep.skill.md" "$dest/skills/release-prep/SKILL.md"
cp "$seed/parts/release-prep.template.md" "$dest/skills/release-prep/template.md"
cp "$seed/parts/log-scout.agent.md" "$dest/agents/log-scout.md"
cp "$seed/parts/hooks.plugin.json" "$dest/hooks/hooks.json"
cp "$seed/parts/guard.mjs" "$dest/scripts/guard.mjs"

case "$variant" in
  good) ;;
  stale) cp "$seed/parts/hooks.project.json" "$dest/hooks/hooks.json" ;;
  badjson) cp "$seed/broken/manifest.badjson.txt" "$dest/.claude-plugin/plugin.json" ;;
  noname) cp "$seed/broken/manifest.noname.json" "$dest/.claude-plugin/plugin.json" ;;
  hookpath) cp "$seed/broken/manifest.hookpath.json" "$dest/.claude-plugin/plugin.json" ;;
  minimal) cp "$seed/broken/manifest.minimal.json" "$dest/.claude-plugin/plugin.json" ;;
  typo) cp "$seed/broken/manifest.typo.json" "$dest/.claude-plugin/plugin.json" ;;
  nowrap) cp "$seed/broken/hooks.nowrap.json" "$dest/hooks/hooks.json" ;;
  noscript) rm "$dest/scripts/guard.mjs"; rmdir "$dest/scripts" ;;
  badagent) cp "$seed/broken/log-scout.badyaml.agent.md" "$dest/agents/log-scout.md" ;;
  inside) mv "$dest/skills" "$dest/.claude-plugin/skills" ;;
  nomanifest) rm -r "$dest/.claude-plugin" ;;
  *) echo "unknown variant: $variant" >&2; exit 2 ;;
esac
