#!/usr/bin/env bash
#
ROOT=`dirname "$0"`
PUBLIC_STATIC="$ROOT/static/public"

dependencies=( \
"bootstrap", \
"xterm", \
"jquery", \
"popper"
)

[ -e ./static/public/ ] && rm -rf ./start

for p in $dependencies ; do npm install $p; done
for p in $dependencies ; do mkdir -p $PUBLIC_STATIC/$p; done


