# run.sh <locale> : regenerate dub json and run the real dub
S=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/e054-dub-agent
cd /home/user/travel_scanner && python3 $S/gen.py $1 && bash docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub.sh 054 $1 2>&1 | grep -v '^long?' | grep -v -E '^\s+at |^Node|throw new|^\s+\^|dub-track.mjs:65' | tail -20
