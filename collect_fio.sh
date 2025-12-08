#!/bin/bash

# Output in Gigabits per second
grep "iops" $1  | tr -d " " | tr "," " " | awk '{print $3}' | tr -d 'avg=' | tr -d ',' | awk -v sz=8388608 '{s += $1} END {print s*sz*8/1e9;}'


# Original collect. Catting into grep couldn't be me.
##!/bin/bash
#
#config=$1
#io_size=$2
#ssd=$3
#STATS_PATH=/home/midhul/membw-eval
#
#cat $STATS_PATH/$config.fio$ssd.txt  | grep "iops        :" | tr -d ' ' | tr ',' ' ' | awk '{print $3}' | tr -d 'avg=' | tr -d ',' | awk -v sz=$io_size '{s += $1} END {print s*sz*8/1e9;}'
