
import FLUCCOplus.timeseries as ts

from FLUCCOplus.utils import *

POWER_RATINGS_MW = {
    "Neuhof I": 18.,
    "Neuhof III": 3.,
    "Maustrenk": 14,
    "STERN I": 2,
    "STERN II": 12,
    "STERN III": 6
}

@log
def read(path, **kwargs):#All data in kWh
    """All data in kWh"""
    df = pd.read_csv(path,
                     delimiter=";",
                     index_col="Datetime UCT",
                     parse_dates=["Datetime UCT"],
                     **kwargs
                     )
    return df #All data in kWh

@logg
def start_pipeline(df):
    return df.copy()

@logg
def clean(df):
    """returns a clean em df 15-17"""
    return (df
            .pipe(start_pipeline)
            .drop("UTCOffset", axis=1)
            .drop("Datetime CET", axis=1)
            .fillna(0)
            .astype(float)
            )
@logg
def power(df):
    """returns the powers in MW"""
    return df.resample("H").sum() / 1000

def adjust_outlier(df):
#     for each column
    pass


