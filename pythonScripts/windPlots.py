#!/usr/bin/env python

import os
#import datetime
import argparse
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import random


def wind(observed, modeled_list, path_plot):


    observed = pd.read_csv(observed,parse_dates=['date'])
    observed.rename(columns = {'wind_speed':'o_wind_speed', 'wind_dir':'o_wind_dir'}, inplace=True)
    #aux = observed['date'] + datetime.timedelta(hours=3)
    #observed['date'] = aux

    modeled = pd.DataFrame()
    model_name = []
    for model in modeled_list:
        df = pd.read_csv(model, parse_dates=['date'])
        name, waste = os.path.basename(model).split(".")
        model_name.append(name)
        df['model_name'] = name
        modeled = modeled.append(df)
        pass

    modeled.rename(columns = {'wind_speed':'p_wind_speed', 'wind_dir':'p_wind_dir'}, inplace=True)

    N = observed.groupby('name')

    trace = []

    os.chdir(path_plot)
    for name, group in N:
        trace.append(go.Scatter(x = group[group.name == name].date, y = group[group.name == name].o_wind_speed, mode = 'lines+markers', name = 'Observado', line = dict(color = ('#1DE9B6'))))
        for model in model_name:
            trace.append(go.Scatter(x = modeled[(modeled.name==name) & (modeled.model_name==model)].date, y = modeled[(modeled.name==name) & (modeled.model_name==model)].p_wind_speed, mode = 'lines+markers', name = model, line = dict(color = ("#%06x" % random.randint(0, 0xFFFFFF)))))
        layout = dict(title = 'Velocidad en el tiempo ' + name.title(), xaxis = dict(title = 'Tiempo'), yaxis = dict(title = 'V [m/s]'),)
        plot(dict(data=trace,layout=layout), filename=name, image='png')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='csv to wind plots', description='plot data')
    parser.add_argument('-o', help='path to csv with observed data')
    parser.add_argument('-m', nargs='+', help='path(s) to csv(s) with modeled data')
    parser.add_argument('-d', help='path to place plots', default=os.getcwd())
    parser.add_argument
    args = parser.parse_args()
    wind(args.o, args.m, args.d)
