#!/bin/bash

python=python3
repo=$(pwd)
lib=$repo/lib

mkdir -p $lib
pushd $lib

wget -i $repo/dependancies.txt

for gz in *.tar.gz
do
  tar -xzf $gz
  rm $gz
done

for proj in $lib/*
do
  pushd $proj
  $python setup.py build
  echo Adding $(ls build/lib) to project
  mv build/lib/* $repo
  popd
done

popd
