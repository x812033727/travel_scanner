# usage: crop.sh in out w h x y
ffmpeg -v error -y -i "$1" -vf "crop=$3:$4:$5:$6,scale=iw*3:ih*3" "$2"
