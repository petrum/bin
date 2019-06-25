#!/bin/bash

./nmap.py -d /home/petrum/scripts/mac-addresses.csv /home/petrum/scripts/nmap-sample1.txt /home/petrum/scripts/nmap-sample2.txt
./nmap.py /home/petrum/scripts/nmap-sample1.txt /home/petrum/scripts/nmap-sample2.txt
sudo nmap -sP 192.168.1.1/24 | ./nmap.py -d /home/petrum/scripts/mac-addresses.csv
sudo nmap -sP 192.168.1.1/24 | ./nmap.py
