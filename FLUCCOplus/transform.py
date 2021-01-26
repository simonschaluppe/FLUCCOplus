

from sklearn import preprocessing

from FLUCCOplus.config import *

@log
def transform(points:np.ndarray, hour_scale=8760): #output dimension is always 8760 hours
    """returns the trigonometric polynomial fitting a given set of support points"""

    h = hour_scale #hours of periodic timeframe

    N = len(points) #Number of support points
    x = np.arange(0, h, h/N, dtype=np.float64) #position of support points
    y = points  # support points of the scaler

    sum = np.fft.rfft(y) # calculate trigonometric polynomial of given support points (discrete fourier transform (dft))
    added_zeros = np.zeros(int((h-N)/2))
    padded_sum = np.concatenate([sum, added_zeros])

    scaler = np.fft.irfft(padded_sum) * h / N #for given hour timescale
    reps = int(np.ceil(9000 / h)) #how often does the signal repeat in a year(9000 instead of 8760 to account for rounding

    return np.concatenate([scaler] * reps)[:8760] # copies the signal reps times and returns only the full year


@logg
def normalize(self, dataframe=None, columns=None):
    """
    :return dataframe (normalized):
    """
    df = self.df if dataframe is None else dataframe

    if columns is None:
        columns = self.vars + self.pps + self.pcs + self.cops
    print(columns)

    x = df[columns].values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    ndf = pd.DataFrame(x_scaled, columns=df[columns].columns, index=df.index)
    return ndf


#%%
