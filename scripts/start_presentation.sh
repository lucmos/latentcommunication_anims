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

manim-slides present $(sed -e 's/\s\+/ /g'  "$1")
