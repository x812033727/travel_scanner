#!/bin/bash
# run.sh <locale>: build dub.<locale>.json and run the real dub, showing the tail
D=$(dirname "$0"); python3 $D/mk.py $1 || exit 1
cd /home/user/travel_scanner && bash docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub.sh 048 $1 2>&1 | grep -v "^    at\|^Node\|^$\|throw new\|^ *^\|^file:" | tail -14
