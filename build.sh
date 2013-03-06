#!/bin/bash -e

# 
# Essentially a make script, but since we don't want to bother making
# if a package is already available to Python, this seems reasonable.
# 
# For each dependency in dependencies.txt, download .tar.gz, build,
# and install to the repo root, only if missing, only if dependency
# cannot be imported by Python
# 
# ./build.sh             download all necessary files
# ./build.sh clean       remove all installed files
# ./build.sh clean all   combination of above two commands
# 

python=python3
repo=$(pwd)
depFile="$repo/dependencies.txt"
lib="$repo/lib"

clean() {
  echo "Cleaning Repository"
  rm -rf "$lib" $(cat "$depFile" | cut -d$'\t' -f 1)
}

wgetFile() {
  echo "$2" | wget -nc -nv -i - > $1.wget.output 2>&1
}

installPyLib() {
  mkdir -p "$lib"
  cd "$lib"
  
  wgetFile $1 $2
  
  compFile=$(basename $2)
  tar -xzf $compFile
  cd $(echo $compFile | sed 's`.tar.gz``')
  
  patch="$repo"/patches/"$1".diff
  if [ -e "$patch" ]
  then
    echo Applying patch to $1
    patch -p0 -i "$patch"
  fi
  
  echo Building $1
  $python setup.py build > build.output
  echo Adding $(ls build/lib) to project
  echo Alternatively run '`'cd '"'"$(pwd)"'";' $python setup.py install'`' to install library
  mv build/lib/* "$repo"
   
  cd "$repo"
}

#
# Script
#

_all=$(cat "$depFile" | cut -d$'\t' -f 1)
depend=""

while [ $# -ne 0 ]
  do
    if echo $_all | grep $1 > /dev/null
    then
      depend="$depend $1"
    elif [[ $1 == 'clean' ]]
    then
      clean='clean'
    elif [[ $1 == 'all' ]]
    then
      depend=$_all
      break
    fi
    
    shift
done

depend=$(echo $clean $depend | xargs)

if [ -z "$depend" ]
then
  depend=$_all
fi

if [ -d "$lib" ] && ! echo $depend | grep 'clean' > /dev/null
then
  echo Lib directory already exists
  echo "  $0 clean"
  echo To trigger clean build
  echo
fi

for dep in $depend
do
  if [[ $dep == 'clean' ]]
  then
    clean
  else
    source=$(cat "$depFile" | grep '^'$dep | cut -d$'\t' -f 2)
    if $python -c "import $dep" > /dev/null 2>&1
    then
      echo $dep already installed
    else
      echo Installing $dep from $source
      installPyLib $dep $source
    fi
    echo
  fi
done
