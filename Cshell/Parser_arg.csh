#!/bin/csh

# $1 $2 $n
# $argv[1] $argv[2] $argv[n]
# $argv[2-] $argv[2+] $argv[n+] $argv[n-]
# $argv[*]
set name = "$1"
echo "The name is: $name"
echo "The name is: $argv[1]"
echo $2
echo $3
echo $4
echo $#argv

set path = `pwd`/*_a*
echo $path
echo $path:h
echo $path:t
echo $path:r
echo $path:e

pushd $path
