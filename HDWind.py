#!/usr/bin/env python
"""
CSV data to windini_N.asc
"""
import os
import shutil
import pandas as pd
import argparse

HDWM_OPT = os.environ['HDWM_OPT']
HDWM_OPT_DATA = os.environ['HDWM_OPT_DATA']
OUTPUT = os.environ['OUTPUT']
OUTPUT_FILE = os.environ['OUTPUT_FILE']


def run(path_datos, path_stations):
    """dataframe in csv format, datum WGS84, epsg:4326:
        header: date,lat,lon,name,wind_dir,wind_speed
    """
    data = pd.read_csv(path_datos, parse_dates=['date'])
    stations = pd.read_csv(path_stations)
    HEIGHT = 10
    data['height'] = HEIGHT
    data = data.sort_values('date')
    N = data.groupby('date')
    hdwind = pd.DataFrame()

    for name, group in N:
        with open('windini_0.asc', 'w') as f:
            f.write('ReferenceSystem 1' + '\n')
            f.write('InputPoints ' + str(len(group)) + '\n')
            for index, input_data in group.iterrows():
                f.write(
                    str(input_data.lat) + ' ' + str(input_data.lon) + ' ' +
                    str(input_data.height) + ' ' + str(input_data.wind_speed) +
                    ' ' + str(input_data.wind_dir) + '\n')

            f.write('OutputLayers 1' + '\n' + '10' + '\n')
            f.write('OutputPoints ' + str(stations.shape[0]) + '\n')
            for station in stations.itertuples():
                f.write(
                    str(station.lat) + ' ' + str(station.lon) + ' ' +
                    str(10) + '\n')
        os.remove(HDWM_OPT_DATA + '/windini_0.asc')
        shutil.move('windini_0.asc', HDWM_OPT_DATA)
        os.system(HDWM_OPT + "/HDWM")
        df = pd.read_csv(OUTPUT_FILE)
        df['date'] = name
        df = pd.merge(df, stations, how='left', on=['lat', 'lon'])
        hdwind = hdwind.append(df)
    hdwind.to_csv('laSerena_WRF-HDWM.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='data-HDWind-data', description='input data to HDWind model and output data')
    parser.add_argument('-d', default=os.getcwd(), help='dir to input data csv ')
    parser.add_argument('-s', help='csv with stations data: lon,lat,name')
    args = parser.parse_args()
    run(args.d, args.s)
