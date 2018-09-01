#!/usr/bin/env python

import os
import glob
import datetime
import argparse
import pandas as pd
import numpy as np
import math
import colorlover as cl
import plotly.graph_objs as go
from plotly.offline import plot
import random

def angulo(o,p):
    aux = abs(o - 360 - p)
    aux2 = abs(o - p)
    aux3 = abs(p - 360 - o)
    df_angulo = pd.DataFrame({"a":aux,"b":aux2,"c":aux3})
    return df_angulo.min(axis=1)

def Mean_Bias_speed(p, o):
    bias = p - o
    return sum(bias)/len(bias)

def Mean_Bias_dir(p, o):
    bias = angulo(o, p)
    return sum(bias)/len(bias)

def Mean_Error_speed(p, o):
    gross = abs(p - o)
    return sum(gross)/len(gross)

def Mean_Error_dir(p, o):
    gross = abs(angulo(o, p))
    return sum(gross)/len(gross)

def RMSE_speed(p, o):
    rmse = (p - o)**2
    rmse = sum(rmse)/len(rmse)
    return math.sqrt(rmse)

def RMSE_dir(p, o):
    rmse = (angulo(o, p))**2
    rmse = sum(rmse)/len(rmse)
    return math.sqrt(rmse)

def wind_bft(wind_speed):
    """Convert wind from metres per second to Beaufort scale"""
    BEAUFORT_SCALE_MS = np.array(
        '0.3 1.5 3.4 5.4 7.9 10.7 13.8 17.1 20.7 24.4 28.4 32.6'.split(),
        dtype='float64')
    BEAUFORT_SCALE_DESCRIPTION = np.array(['Calma', 'Ventolina', 'Flojito', 'Flojo', 'Bonancible', 'Fresquito', 'Fresco', 'Frescachón', 'Temporal', 'Temporal fuerte', 'Temporal duro', 'Temporal muy duro', 'Temporal huracanado '])
    if wind_speed is None:
        return None
    else:
        return BEAUFORT_SCALE_DESCRIPTION[np.digitize(wind_speed, BEAUFORT_SCALE_MS)]

def wind_cat(wind_dir):
    """Convert wind from metres per second to Cardinal direction"""
    DIRECTIONS_CATEGORICAL = np.array(
        'N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW N'.split())
    DIRECTIONS_NUMERICAL = np.arange(11.25, 372, 22.5)
    if wind_dir is None:
        return None
    else:
        return DIRECTIONS_CATEGORICAL[np.digitize(wind_dir, DIRECTIONS_NUMERICAL)]

def wind_rose_plot(df_wind_rose):
    data = []
    wind_rose = pd.DataFrame({'wind_dir_cat': np.array('N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW'.split()), 'wind_dir': [0]*16})
    i = 0
    bfs = df_wind_rose.groupby('wind_speed_bfs')
    color = cl.scales[str(df_wind_rose.wind_speed_bfs.unique().shape[0]+1)]['qual']['Set1']
    for bfs_wind, group_bfs in bfs:
        df1 = pd.DataFrame({'wind_dir_cat': group_bfs.wind_dir_cat.value_counts().index, 'wind_dir': group_bfs.wind_dir_cat.value_counts().values})
        df2 = pd.merge(wind_rose, df1, how='left', on='wind_dir_cat').fillna(0)
        data.append(go.Area(t=df2.wind_dir_cat, r=df2.wind_dir_y.fillna(0), marker=dict(color=color[i]), name=bfs_wind))
        i += 1
    layout_windrose = dict(title='Rosa de los vientos de ' + df_wind_rose.model_name.iloc[0].title() + 'en ' + df_wind_rose.name.iloc[0].title(), orientation=270, barmode='stack',)
    plot(dict(data=data, layout=layout_windrose), filename=df_wind_rose.model_name.iloc[0].title()+ '_'+ df_wind_rose.name.iloc[0].title() + 'windrose.html', auto_open=False, image='png', image_filename=df_wind_rose.model_name.iloc[0].title()+ '_'+ df_wind_rose.name.iloc[0].title())


def wind(observed, modeled_path, path_plot):

    statistics = [['DataSet','Mean Bias Vel.', 'Mean Bias Dir.', 'Mean Error Vel.', 'Mean Error Dir.', 'RMSE Vel', 'RMSE Dir']]

    observed = pd.read_csv(observed, parse_dates=['date'])
    observed['o_wind_speed'] = observed['wind_speed']
    observed['o_wind_dir'] = observed['wind_dir']
    aux = observed['date'] + datetime.timedelta(hours=3)
    observed['date'] = aux
    modeled_list = [modeled_path+'/' + modeled for modeled in sorted(os.listdir(modeled_path))]
    DATA_RANGE = pd.read_csv(modeled_list[0], parse_dates=['date'])
    DATA_RANGE_DATE = DATA_RANGE.date.drop_duplicates()
    observed = observed[observed.date.isin(DATA_RANGE_DATE)]
    observed['model_name'] = observed['name']
    modeled = pd.DataFrame()
    model_name = []
    for model in modeled_list:
        df = pd.read_csv(model, parse_dates=['date'])
        name, waste = os.path.basename(model).split(".")
        model_name.append(name)
        df['model_name'] = name
        modeled = modeled.append(df)
        pass
    modeled['p_wind_speed'] = modeled['wind_speed']
    modeled['p_wind_dir'] = modeled['wind_dir']

    observed['wind_dir_cat'] = wind_cat(observed.o_wind_dir)
    modeled['wind_dir_cat'] = wind_cat(modeled.p_wind_dir)
    observed['wind_speed_bfs'] = wind_bft(observed.o_wind_speed)
    modeled['wind_speed_bfs'] = wind_bft(modeled.p_wind_speed)
    N = observed.groupby('name')

    os.chdir(path_plot)

    color = cl.scales[str(len(modeled_list)+1)]['qual']['Set1']
    for name, group in N:
        i = 0
        trace_speed = []
        trace_dir = []
        df_wind_rose_1 = group[group.name == name]
        #wind_rose_plot(df_wind_rose_1[['wind_speed_bfs', 'wind_dir_cat', 'model_name', 'name']])
        o_date = group[group.name == name].date
        o_speed = group[group.name == name].o_wind_speed
        o_dir = group[group.name == name].o_wind_dir
        trace_speed.append(go.Scatter(x=o_date, y=o_speed, mode='lines+markers', name='Observado', line=dict(color=color[i])))
        trace_dir.append(go.Scatter(x=o_date, y=o_dir, mode='lines+markers', name='Observado', line=dict(color=color[i])))
        i += 1
        for model in model_name:
            p_date = modeled[(modeled.name == name) & (modeled.model_name == model)].date
            p_speed = modeled[(modeled.name == name) & (modeled.model_name == model)].p_wind_speed
            p_dir = modeled[(modeled.name == name) & (modeled.model_name == model)].p_wind_dir
            df_wind_rose_2 = modeled[(modeled.name == name) & (modeled.model_name == model)]
            #wind_rose_plot(df_wind_rose_2[['wind_speed_bfs', 'wind_dir_cat', 'model_name', 'name']])
            trace_speed.append(go.Scatter(x=p_date, y=p_speed, mode='lines+markers', name=model, line=dict(color=color[i])))
            trace_dir.append(go.Scatter(x=p_date, y=p_dir, mode='lines+markers', name=model, line=dict(color=color[i])))
            i += 1
            statistics.append([name+' '+model,Mean_Bias_speed(p_speed.values, o_speed.values), Mean_Bias_dir(p_dir.values, o_dir.values), Mean_Error_speed(p_speed.values, o_speed.values), Mean_Error_dir(p_dir.values, o_dir.values), RMSE_speed(p_speed.values, o_speed.values), RMSE_dir(p_dir.values, o_dir.values)])

        layout_speed = dict(title='Velocidad en el tiempo ' + name.title(),
                            xaxis=dict(title='Tiempo'), yaxis=dict(title='V [m/s]'), plot_bgcolor='rgb(229,229,229)',)
        #plot(dict(data=trace_speed, layout=layout_speed), filename=name +
             #'speed.html', auto_open=False, image='png', image_filename=name)
        layout_dir = dict(title='Dirección en el tiempo ' + name.title(),
                          xaxis=dict(title='Tiempo'), yaxis=dict(title='Grados '), plot_bgcolor='rgb(229,229,229)',)
        #plot(dict(data=trace_dir, layout=layout_dir), filename=name +
             #'direction.html', auto_open=False, image='png', image_filename=name)
        df_statistics = pd.DataFrame(statistics[1:], columns=statistics[0])
        df_statistics.to_latex("statistics.csv",index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='csv to wind plots', description='plot data')
    parser.add_argument('-o', help='path to csv with observed data')
    parser.add_argument(
        '-m', help='path to csv(s) with modeled data')
    parser.add_argument('-d', help='path to place plots', default=os.getcwd())
    parser.add_argument
    args = parser.parse_args()
    wind(args.o, args.m, args.d)
