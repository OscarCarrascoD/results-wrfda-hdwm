#!/usr/bin/env python

import os
import sys
import glob
import pandas as pd

def data(path, name_csv):
    os.chdir(path)
    files_xlsx = sorted(glob.glob("*.xls"))
    df = pd.DataFrame()

    for f in files_xlsx:
        data = pd.read_excel(f, skiprows=4, skip_footer=4, header=None,
                             parse_dates=[0], usecols=[0, 2, 6],
                             names=['date', 'wind_speed', 'wind_dir'])
        data = data.dropna()
        data['name'], waste = f.split(".")
        df = df.append(data)

    df.to_csv(name_csv + '.csv', index=False)

if __name__ == "__main__":
    files_path = sys.argv[1]
    name_csv = sys.argv[2]
    data(files_path, name_csv)
