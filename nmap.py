#!/usr/bin/python3

import pandas as pd
import re

pd.set_option('display.expand_frame_repr', False)

class NMap:
    def __init__(self, d):
        self.descr = d
    def get(self, data = None):
        d = pd.read_csv(self.descr)
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
        res = pd.merge(df, d, how='left', left_on='mac', right_on='mac')
        res = res[res.mac.notnull()]
        res.set_index('ip', inplace=True)

        return res

if __name__ == "__main__":
    n = NMap("/home/petrum/scripts/mac-addresses.csv")
    print(n.get("/home/petrum/scripts/nmap-sample1.txt"))
    print(n.get("/home/petrum/scripts/nmap-sample2.txt"))




