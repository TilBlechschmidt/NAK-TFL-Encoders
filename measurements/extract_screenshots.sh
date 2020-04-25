#!/usr/bin/env bash
declare -a arr=(1 7 11 14 19 23 26 32 42)

for file in out/*
do
    for i in "${arr[@]}"
    do
        TIME=$i
        VIDEO=$(basename "$(find "$file" -name "video.*")")

        mkdir -p "$file/screenshots"
        docker run --rm -it -v "$(pwd)/$file":/host opencoconut/ffmpeg -ss $TIME -i /host/$VIDEO -frames:v 1 -qscale:v 2 /host/screenshots/$TIME.jpg
    done
done
