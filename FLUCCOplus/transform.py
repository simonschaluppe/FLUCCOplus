import numpy as np
import pandas as pd
from sklearn import preprocessing
#from utils import *
from matplotlib.figure import Figure

def zyklusscaler(timeseries:pd.Series, scalefactors: list, zyklus: int) -> pd.Series:
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
    if type(df) == pd.Series:
            df = df.map(lambda x: min if x < separator else max)
    elif type(df) == pd.DataFrame:
        for c in df.columns:
            df[c] = df[c].map(lambda x: min if x < separator else max)
    return df


class Transformation:
    def __init__(self, kind="Generic", weights=[1,1], timeframe=24, normalize=False):
        self.kind = kind #type of energy flow
        self.weights = weights
        self.timeframe = timeframe
        self.profile = transform(self.weights, self.timeframe)
        if normalize:
            self.profile = self.profile/self.profile.sum()*8760

    def apply(self, timeseries):
        return zyklusscaler(timeseries, scalefactors=self.weights, zyklus=self.timeframe)

    def _plot(self, ax=None, line_color="r"):
        if ax is None:
            fig, ax = plt.subplots(1,1)
        x = np.arange(0, self.timeframe, self.timeframe / len(self.weights))
        xh = np.arange(0, self.timeframe, 1)
        ax.plot(x, self.weights, "bo")
        ax.plot(xh, self.profile[0:self.timeframe], line_color)
        ax.set_ylim(0.8*min(self.profile), 1.2*max(self.profile))
        return ax
    
    def plot(self, ax=None):
        if ax is None:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1,2)
        x_d = np.arange(0, 24, 1)
        x_w = np.arange(0, 144, 1)
        x_y = np.arange(0, 8760, 1)
        ax[0].plot(x_d, self.profile[0:24])
        ax[1].plot(x_y, self.profile, linewidth=0.3)
        [axe.set_ylim(0.8*min(self.profile), 1.2*max(self.profile)) for axe in ax]
        fig.show()
        return ax

if __name__ == "__main__":
    test = Transformation(weights=[1.,2.,3.,1.],timeframe=24, normalize=True)
    import matplotlib.pyplot as plt
    test.plot()
    
    
