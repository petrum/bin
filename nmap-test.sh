#!/bin/bash

./nmap2.py --ago 10 --loop 1 -v \
    -d /home/petrum/scripts/mac-addresses.csv \
    test1.csv test2.csv
