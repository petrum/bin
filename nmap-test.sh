#!/bin/bash

./nmap.py /home/petrum/scripts/nmap-sample1.txt /home/petrum/scripts/nmap-sample2.txt
sudo nmap -sP 192.168.1.1/24 | ./nmap.py
