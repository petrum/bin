#!/usr/bin/python3

import pandas as pd
import re
import sys
import argparse
import logging

pd.set_option('display.expand_frame_repr', False)

class NMap:
    def __init__(self, d = None):
        self.descr = d
    def get(self, data = None):
        df = pd.DataFrame(columns=['ip', 'dn', 'mac', 'company'])
        if data != None:
            with open(data) as fp:
                lines = fp.readlines()
        else:
            lines = sys.stdin.readlines()
        for line in lines:
            #print(line)
            if not line:
                break
            n = re.search('Nmap scan report for (.*) \((.*)\)', line)
            if n:
                df.loc[len(df)] = [n.group(2), n.group(1), None, None]
            else:
                n = re.search('Nmap scan report for (.*)', line)
                if n:
                    df.loc[len(df)] = [n.group(1), None, None, None]
            m = re.search('MAC Address: (.*) \((.*)\)', line)
            if m:
                last_index = len(df) - 1
                df.loc[last_index]['mac'] = m.group(1)
                df.loc[last_index]['company'] = m.group(2)
        if self.descr != None:    
            d = pd.read_csv(self.descr)
            df = pd.merge(df, d, how='left', left_on='mac', right_on='mac')
            df = df[df.mac.notnull()]
        df.set_index('ip', inplace=True)
        return df

def main():
    parser = argparse.ArgumentParser(description='It parses the nmap output in a Pandas dataframe')
    parser.add_argument('-d', '--descriptions', help='The decription file', required=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose', required=False)
    parser.add_argument('tests', nargs=argparse.REMAINDER, action="store")
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-5s %(message)s', datefmt='%Y%m%d %H:%M:%S', level=logging.DEBUG if args.verbose else logging.WARNING)
    n = NMap(args.descriptions)
    if args.tests != None:
        for test in args.tests:
            print(n.get(test))
    else:
        print(n.get())

if __name__ == "__main__":
    main()
    




