#!/usr/bin/python3

import pandas as pd
import re
import sys
import argparse
import logging
import datetime
import subprocess
import time
from subprocess import run, PIPE
import tempfile
import os

pd.set_option('display.expand_frame_repr', False)
pd.set_option('mode.chained_assignment', 'raise')

def sendEmail(to, txt, subject):
    print(subject)
    print(txt)
    if to == None:
        return
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        f.write(txt)
        f.close()
        cmd = "/usr/bin/mail -s '{}' '{}' < '{}'".format(subject, to, tmp.name)
        run(cmd, shell=True)

class NMap:
    def __init__(self, d, t):
        self.descr = d
        self.tests = t
        self.index = 0

    def isDone(self):
        return False if len(self.tests) == 0 else self.index >= len(self.tests)

    def get(self):
        if len(self.tests) > 0:
            df = pd.read_csv(self.tests[self.index])
            self.index = self.index + 1
            return df
        df = pd.DataFrame(columns=['ip', 'dn', 'mac', 'company'])
        cmd = "/usr/bin/sudo /usr/bin/nmap -sP 192.168.1.1/24"
        code, out = subprocess.getstatusoutput(cmd)
        if code != 0:
            logging.error("The '{}' command returned code = {}".format(cmd, code)) 
            sys.exit(-1) 
        #print(out)
        lines = out.splitlines()
        #print(lines)
        for line in lines:
            #print(line)
            #line = line + "\n"
            n = re.search(r'Nmap scan report for (.*) \((.*)\)', line)
            #print(n)
            if n:
                df.loc[len(df)] = [n.group(2), n.group(1), None, None]
            else:
                n = re.search('Nmap scan report for (.*)', line)
                if n:
                    df.loc[len(df)] = [n.group(1), None, None, None]
            m = re.search(r'MAC Address: (.*) \((.*)\)', line)
            #print(m)
            if m:
                last_index = len(df) - 1
                df.loc[last_index]['mac'] = m.group(1)
                df.loc[last_index]['company'] = m.group(2)
        df = df[df.mac.notnull()]
        if self.descr != None:
            d = pd.read_csv(self.descr)
            df = pd.merge(df, d, how='left', left_on='mac', right_on='mac')
        #df.set_index('ip', inplace=True)
        df.loc[df.index, 'ts'] = datetime.datetime.now()
        return df

def main():
    parser = argparse.ArgumentParser(description='It parses the nmap output in a Pandas dataframe')
    parser.add_argument('-d', '--descriptions', help='The decription file', required=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose', required=False)
    parser.add_argument('tests', nargs=argparse.REMAINDER, action="store")
    parser.add_argument('--email', help='The email', required=False)
    parser.add_argument('--ago', help='The ago period in seconds', required=False)
    parser.add_argument('--loop', help='The loop period in seconds', required=False)

    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-5s %(message)s', datefmt='%Y%m%d %H:%M:%S', level=logging.DEBUG if args.verbose else logging.WARNING)
    n = NMap(args.descriptions, args.tests)

    df = n.get()
    df.loc[df.index, 'active'] = True
    loop = 30
    if args.loop:
        loop = int(args.loop)
    ago = 180
    if args.ago:
        ago = int(args.ago)
    while not n.isDone():
        sys.stdout.flush()
        time.sleep(loop)
        df2 = n.get()
        with open("/tmp/nmap-dump-" + str(os.getpid()) + ".txt", "w") as f:
            print(str(df), file=f)
    print(df)
if __name__ == "__main__":
    main()
