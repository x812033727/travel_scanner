#!/usr/bin/env bash
# after the e906 drafts (chain906): the e905 s39 retake, then wait for the picks file (st1/out has 40) and refine e905, then stop
cd /home/user/travel_scanner
while pgrep -f chain906.sh >/dev/null; do sleep 30; done
KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 905 fix1
echo "=== s39 retake done $(date -u +%T)"
A=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e905-dh/runpod/a
for i in $(seq 1 60); do [ -f "$A/st2-go" ] && break; sleep 60; done
[ -f "$A/st2-go" ] || { echo "=== no picks after 60 min, stopping pod"; bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh stop; exit 0; }
NO_UPSCALE=1 bash .agents/skills/minimax-h3-runpod/scripts/route_a_st23.sh 905 9050000 $(cat "$A/st2-go")
echo "=== chain done $(date -u +%T)"
