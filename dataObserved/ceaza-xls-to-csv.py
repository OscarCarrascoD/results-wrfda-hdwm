#!/usr/bin/env python

import os
import argparse
import glob
import pandas as pd


def data(path_datos, path_stations, name_csv):
    os.chdir(path_datos)
    stations = pd.read_csv(path_stations)
    files_xlsx = sorted(glob.glob("*.xls"))
    df = pd.DataFrame()

    for f in files_xlsx:
        data = pd.read_excel(f, skiprows=4, skip_footer=4, header=None,
                             parse_dates=[0], usecols=[0, 2, 6],
                             names=['date', 'wind_speed', 'wind_dir'])
        data = data.dropna()
        name, waste = f.split(".")
        data['name'] = name
        data = pd.merge(data, stations, how='left', on='name')
        data['lat'] = data['lat'].apply(lambda x: f'{x:.6f}')
        data['lon'] = data['lon'].apply(lambda x: f'{x:.6f}')
        if name_csv is None:
            data.to_csv(name + '.csv', index=False)
        else:
            df = df.append(data)

    if name_csv is not None:
        df.to_csv(name_csv + '.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='xls-to-csv', description='xls(s) to csv(s)')
    parser.add_argument('-d', default=os.getcwd(), help='dir with xls(s)')
    parser.add_argument('-s', help='csv with stations data: lon,lat,name')
    parser.add_argument(
        '-n', action="store", help='if used, one csv will be generated. Otherwise for each xls one csv will be generated')
    parser.add_argument

    args = parser.parse_args()
    data(args.d, args.s, args.n)
