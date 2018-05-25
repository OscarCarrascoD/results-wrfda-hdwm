#!/usr/bin/env python

import os
#import datetime
import argparse
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
import random

COLOR_OBSERVED = ["#f7fbff", "#e1edf8", "#cbdff1", "#acd0e6", "#82bbdb", "#59a2cf", "#3587c1", "#1b6ab0", "#094d96", "#08306b"]
COLOR_MODELED = ["#f7f4f9", "#e9e3f0", "#d7c2df", "#cca1ce", "#d57cbd", "#e34fa0", "#e01f78", "#c20d52", "#93003e", "#67001f"]
DIRECTIONS_CATEGORICAL = np.array('N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW N'.split())
DIRECTIONS_NUMERICAL = np.arange(11.25, 372, 22.5)


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

    observed['wind_dir_cat'] = DIRECTIONS_CATEGORICAL[np.digitize(observed.o_wind_dir, DIRECTIONS_NUMERICAL)]
    modeled['wind_dir_cat'] = DIRECTIONS_CATEGORICAL[np.digitize(observed.p_wind_dir, DIRECTIONS_NUMERICAL)]
    N = observed.groupby('name')

    trace_speed = []
    trace_dir = []

    os.chdir(path_plot)
    for name, group in N:
        colorplot_o = random.choice(COLOR_OBSERVED)
        COLOR_OBSERVED.remove(colorplot_o)
        trace_speed.append(go.Scatter(x = group[group.name == name].date, y = group[group.name == name].o_wind_speed, mode = 'lines+markers', name = 'Observado', line = dict(color = colorplot_o)))
        trace_dir.append(go.Scatter(x = group[group.name == name].date, y = group[group.name == name].o_wind_dir, mode = 'lines+markers', name = 'Observado', line = dict(color = colorplot_o)))

        for model in model_name:
            colorplot_m = random.choice(COLOR_MODELED)
            COLOR_MODELED.remove(colorplot_m)
            trace_speed.append(go.Scatter(x = modeled[(modeled.name==name) & (modeled.model_name==model)].date, y = modeled[(modeled.name==name) & (modeled.model_name==model)].p_wind_speed, mode = 'lines+markers', name = model, line = dict(color = colorplot_m)))
            trace_dir.append(go.Scatter(x = modeled[(modeled.name==name) & (modeled.model_name==model)].date, y = modeled[(modeled.name==name) & (modeled.model_name==model)].p_wind_dir, mode = 'lines+markers', name=model, line = dict(color=colorplot_m)))

        layout_speed = dict(title = 'Velocidad en el tiempo ' + name.title(), xaxis = dict(title = 'Tiempo'), yaxis = dict(title = 'V [m/s]'),)
        plot(dict(data=trace_speed,layout=layout_speed), filename=name+'.html', auto_open=False, image='png', image_filename=name)
        layout_dir = dict(title = 'Dirección en el tiempo ' + name.title(), xaxis = dict(title = 'Tiempo'), yaxis = dict(title = 'Grados '),)
        plot(dict(data=trace_speed,layout=layout_dir), filename=name+'.html', auto_open=False, image='png', image_filename=name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='csv to wind plots', description='plot data')
    parser.add_argument('-o', help='path to csv with observed data')
    parser.add_argument('-m', nargs='+', help='path(s) to csv(s) with modeled data')
    parser.add_argument('-d', help='path to place plots', default=os.getcwd())
    parser.add_argument
    args = parser.parse_args()
    wind(args.o, args.m, args.d)
