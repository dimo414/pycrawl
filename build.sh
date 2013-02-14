#!/bin/bash -e

python=python3
repo=$(pwd)
lib="$repo/lib"

if [ -d "$lib" ]
then
  echo Lib directory already exists
  echo "  rm -rf $lib"
  echo To download dependancies again
  echo
fi

echo Checking dependencies:
cat "$repo/dependencies.txt" | while read -r line
do
  dep=$(echo "$line" | cut -d$'\t' -f 1)
  source=$( echo "$line" | cut -d$'\t' -f 2)
  if $python -c "import $dep" > /dev/null 2>&1
  then
    echo $dep already installed
  else
    echo Downloading $dep from $source
    
	mkdir -p "$lib"
	pushd "$lib" >/dev/null
    echo $source | wget -nv -i - >> wget.output 2>&1
    popd > /dev/null
  fi
done

if [ ! -d "$lib" ] # no files downloaded
then
  exit 0
fi

pushd "$lib" >/dev/null

for gz in $(ls | grep '.*\.tar\.gz')
do
  tar -xzf $gz
  rm $gz
done

for proj in *
do
  if [ -d "$proj" ]
  then
    pushd "$proj" >/dev/null
    echo
    echo Building $(basename "$(pwd)")
    $python setup.py build > build.output
    echo Adding $(ls build/lib) to project
    echo Alternatively run '`'cd "$(pwd)"';' $python setup.py install'`' to install library
    rm -rf "$repo/$(ls build/lib)"
    mv build/lib/* "$repo"
    popd >/dev/null
  fi
done

popd >/dev/null
