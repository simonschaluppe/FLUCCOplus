

from sklearn import preprocessing

from FLUCCOplus.config import *


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