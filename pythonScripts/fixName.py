#!/usr/bin/env python

import os
import sys
import glob
import pandas as pd

files = sorted(glob.glob("*-HDWM.csv"))
stations = pd.read_csv('stations.csv')

for file in files:
    data = pd.read_csv(file)
    data.drop('name',axis=1, inplace=True)
    df = pd.merge(data, stations, how='left', on=['lat', 'lon'])
    df.to_csv(file, index=False)
    pass
