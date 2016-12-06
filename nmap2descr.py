#!/usr/bin/python

import pandas as pd
import sys
import fileinput
import re
import commands
import argparse
import logging

def info(*args):
  res = ''
  for s in args:
    res += str(s)
  logging.info(res)

parser = argparse.ArgumentParser(description='It parses the nmap output in a Pandas dataframe')
parser.add_argument('-s', '--short', action='store_true', help='Short view', required=False)
parser.add_argument('-d', '--descriptions', help='The decription file', required=False)
parser.add_argument('-u', '--unexpected', action='store_true', help='Show unexpected devices', required=False)
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose', required=False)

args = parser.parse_args()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-5s %(message)s', datefmt='%Y%m%d %H:%M:%S', level=logging.DEBUG if args.verbose else logging.WARNING)

pd.set_option('display.expand_frame_repr', False)

d = pd.DataFrame(columns=['mac', 'descr', 'expected'])
if args.descriptions:
    d = pd.read_csv(args.descriptions)
    d['mac'] = d['mac'].str.upper()

info(d)
nmap = pd.DataFrame(columns=['ip', 'dn', 'mac', 'company'])

code, myMac = commands.getstatusoutput("ifconfig | grep HWaddr | head -n 1 | sed 's/.*HWaddr \\(.*\\)/\\1/g'")
info(code, myMac)

for line in sys.stdin:
    line = line.rstrip()
    n = re.search('Nmap scan report for (.*) \((.*)\)', line)
    if n:
        info(n.group(1), n.group(2))
        nmap.loc[len(nmap)] = [n.group(2), n.group(1), None, None]
    else:
        n = re.search('Nmap scan report for (.*)', line)
        if n:
            nmap.loc[len(nmap)] = [n.group(1), None, None, None]

    m = re.search('MAC Address: (.*) \((.*)\)', line)
    if m:
        info(m.group(1), m.group(2))
        last_index = len(nmap) - 1
        nmap.loc[last_index]['mac'] = m.group(1)
        nmap.loc[last_index]['company'] = m.group(2)
info(nmap)
noMac = nmap.mac.isnull()
nmap.ix[noMac, 'mac'] = myMac.upper().rstrip()
info(nmap)

nmap['n'] = nmap.ip.str.split('.', expand=True)[3].astype(int)
info(nmap)
df = pd.merge(nmap, d, how='left', left_on='mac', right_on='mac').sort_values(by='n')
del df['n']

header = ['ip', 'dn', 'descr'] if args.short else df.columns
if not args.descriptions:
    header = [x for x in header if x not in ['expected', 'descr']]

print df[header]

if args.unexpected:
    print df[df.expected != 1].T
