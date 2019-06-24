#!/usr/bin/python3

import pandas as pd
import re

class NMap:
    def __init__(self, d):
        self.descr = d
    def get(self, data = None):
        d = pd.read_csv(self.descr)
        df = pd.DataFrame(columns=['ip', 'dn', 'mac', 'company'])
        if data != None:
            with open(data) as fp:
                line = fp.readline()
                print(line)
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

        return df

if __name__ == "__main__":
    n = NMap("/home/petrum/scripts/mac-addresses.csv")
    print(n.get("/home/petrum/scripts/nmap-sample1.txt"))



