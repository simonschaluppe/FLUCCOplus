import numpy as np
import pandas as pd
from sklearn import preprocessing
from FLUCCOplus.utils import *
from matplotlib.figure import Figure


def zyklusscaler(timeseries, scalefactors: list, zyklus: int) -> pd.Series:
    """
        Transforms a timeseries by the defined scalefactors over the cycle
        param: zyklus: self-defined period. It can be 24 (daily) or 8760 (monthly) hour
               scalefactors: self-defined weights.
    """
    if len(timeseries) > 8760:
        timeseries.drop(timeseries.tail(8761).index, inplace=True)
    else:
        pass

    timeseries_scaled = np.multiply(timeseries, transform(scalefactors, zyklus))
    ratio = timeseries.sum() / timeseries_scaled.sum()
    timeseries_scaled = timeseries_scaled * ratio

    return pd.Series(timeseries_scaled, index=timeseries.index)


def transform(support_points: list, hour_scale: int = 8760):
    """
    returns the trigonometric polynomial fitting
    a given set of support points

    output dimension is always 8760 hours
    """

    h = hour_scale  # hours of periodic timeframe
    points = np.array(support_points)
    N = len(points)  # Number of support points
    x = np.arange(0, h, h / N, dtype=np.float64)  # position of support points
    y = points  # support points of the scaler

    sum = np.fft.rfft(
        y)  # calculate trigonometric polynomial of given support points (discrete fourier transform (dft))
    added_zeros = np.zeros(int((h - N) / 2))  # fill the higher frequency fourier coefficients
    padded_sum = np.concatenate([sum, added_zeros])

    scaler = np.fft.irfft(padded_sum) * h / N  # for given hour timescale
    reps = int(
        np.ceil(9000 / h))  # how often does the signal repeat in a year(9000 instead of 8760 to account for rounding

    return np.concatenate([scaler] * reps)[:8760]  # copies the signal reps times and returns only the full year


def plot(scaler, support_points, hour_scale=8760, view_scale=1.5):
    p, h = support_points, hour_scale

    x = np.arange(0, h, h / len(p))
    xh = np.arange(0, 8760, 1)

    fig = Figure()
    ax = fig.add_subplot()
    a, b = 0, int(h * view_scale)
    ax.plot(x[a:b], p[a:b], "bo")
    ax.plot(xh[a:b], scaler[a:b], "r")
    return fig


# @logg
# def normalize(self, dataframe=None, columns=None):
#     """
#     :return dataframe (normalized):
#     """
#     df = self.df if dataframe is None else dataframe
#
#     if columns is None:
#         columns = self.vars + self.pps + self.pcs + self.cops
#     print(columns)
#
#     x = df[columns].values  # returns a numpy array
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(x)
#     ndf = pd.DataFrame(x_scaled, columns=df[columns].columns, index=df.index)
#     return ndf


def normalize(dataframe, columns=None):
    """
    :return dataframe (normalized):
    """
    df = dataframe

    if columns is None:
        columns = df.columns

    x = df[columns].values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    ndf = pd.DataFrame(x_scaled, columns=df[columns].columns, index=df.index)
    return ndf


def discretize(df, separator:float, min=0., max=1.):
    """
    :param df: Dataframe with continous signals
    :param separator: Value by which to separate the signal in 2 categories
    :param min: the resulting value of the area below the separator
    :param max: the resulting value of the area above the separator
    :return: Sparated dataframe with dsicrete values (only min and max)
    """
    for c in df.columns:
        df[c] = df[c].map(lambda x: min if x < separator else max)
    return df

def signaleigenschaften(df, separator:float):
    disc = discretize(df=df, separator=separator)
    anzahl = pd.DataFrame()
    sig = disc.where(disc > 0)
    sig = pd.DataFrame(sig)
    anzahl = sig.count()
    df_step = pd.DataFrame()
    df_not = pd.DataFrame()
    for separator in df.columns:
        df_step[separator] = df[separator].shift(1).ne(df[separator]).where(df[separator] == 1).cumsum()
        df_not[separator] = df[separator].shift(1).ne(df[separator]).where(df[separator] == -1).cumsum()

    df_desc = pd.DataFrame()
    df_desc["Zeitraum mit Signal [h]"] = anzahl
    df_desc["Nicht-Signal-Zeitraum [h]"] = len(df) - anzahl
    df_desc["Anzahl Signal-Perioden"] = df_step.max()
    df_desc["Durchschnittliche Dauer Signal [h]"] = (
                df_desc["Zeitraum mit Signal [h]"] / df_desc["Anzahl Signal-Perioden"])
    df_desc["Durchschnittliche Dauer Nicht-Signal [h]"] = df_desc["Nicht-Signal-Zeitraum [h]"] / df_desc[
        "Anzahl Signal-Perioden"]

    return df_desc

#    df_desc = pd.DataFrame()
 #   df_desc["Zeitraum mit Signal [h]"] = anzahl18[cut]
  #  df_desc["Nicht-Signal-Zeitraum [h]"] = 8760 - anzahl18[cut]
   # df_desc["Anzahl Signal-Perioden"] = df18_step.max()
    #df_desc["Durchschnittliche Dauer Signal [h]"] = (
     #           desc18["Zeitraum mit Signal [h]"] / desc18["Anzahl Signal-Perioden"])
    #desc18["Durchschnittliche Dauer Nicht-Signal [h]"] = desc18["Nicht-Signal-Zeitraum [h]"] / desc18[
     #   "Anzahl Signal-Perioden"]