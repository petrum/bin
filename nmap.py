#!/usr/bin/python

import pandas as pd

class NMap:
    def __init__(self, d):
        self.descr = d
    def get(self):
        dDf = pd.read_csv(self.descr)
        return dDf

if __name__ == "__main__":
    n = NMap("/home/petrum/scripts/mac-addresses.csv")
    print n.get()



