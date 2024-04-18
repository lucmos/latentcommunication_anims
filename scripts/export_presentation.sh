#!/usr/bin/env bash


if [ $# -ne 1 ]
  then
    echo "Provide exactly one file containing whitespace separated slide names"
    exit 1
fi


if [ ! -f "$1" ]; then
    echo "File not found: "\'"$1"\'
    exit 1
fi

manim-slides convert \
    -ccontrols=false \
    -cprogress=true \
    -cshow_slide_number=false \
    -coverview=true \
    -ctouch=true \
    -cview_distance=6 \
    -cmobile_view_distance=4  \
    -chide_cursor_time=1000 \
    $(sed -e 's/\s\+/ /g'  "$1") \
    index.html

