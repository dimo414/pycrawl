#!/bin/bash -e

python=python3
repo=$(pwd)
lib="$repo/lib"

mkdir -p "$lib"
pushd "$lib" >/dev/null

echo Downloading dependencies:
cat "$repo/dependencies.txt" | wget -nv -i - > wget.output

for gz in *.tar.gz
do
  tar -xzf $gz
  rm $gz
done

for proj in "$lib"/*
do
  if [ -d "$proj" ]
  then
    pushd "$proj" >/dev/null
    echo Building $(basename "$(pwd)")
    $python setup.py build > build.output
    echo Adding $(ls build/lib) to project
    mv build/lib/* "$repo"
    popd >/dev/null
  fi
done

popd >/dev/null
