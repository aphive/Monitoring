#!/bin/bash

# This script will pull the number of Asterisk Peers
# and output the results ready for graphing.
# eg. Hints:10
# author: Computero
# ver: 1.0

hints=`sudo asterisk -rx "show hints" | grep -c "1$"`

if [ $hints -gt -1 ]; then
    echo Hints:$hints
fi
