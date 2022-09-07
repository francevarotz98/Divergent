#!/bin/bash

echo "[i] out file tcpdump:$1"
cmd="sudo tcpdump -vv -i lo \"src net 192.168.0.0/16 and (port $2)\" -w $1 > /dev/null 2>&1"
eval $cmd
