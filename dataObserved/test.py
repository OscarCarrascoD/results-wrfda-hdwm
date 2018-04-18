#!/usr/bin/env python

import os
import argparse
import glob
import pandas as pd


def data(path, name_csv):
    print(path)

    if name_csv == None:
        print("VACIO")
    if name_csv is not None:
        print(name_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='xls-to-csv', description='xls(s) to csv(s)')
    parser.add_argument('-d', default=os.getcwd(), help='dir with xls(s)')
    parser.add_argument('-n', action="store", help='if used, one csv will be generated. Otherwise for each xls one csv will be generated')
    parser.add_argument

    args = parser.parse_args()
    data(args.d, args.n)
