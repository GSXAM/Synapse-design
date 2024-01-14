#!/bin/csh
#
tr -s ' ' < $1 | tr ' ' '\n' | sort | uniq > $1.index
