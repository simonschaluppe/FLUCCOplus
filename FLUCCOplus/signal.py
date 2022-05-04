import pandas as pd


import FLUCCOplus.config as config
import FLUCCOplus.web as web
from pathlib import Path

PEEXCEL_PATH = config.DATA_PROCESSED / Path("peexcel_normalized.csv")
WEB_PATH = config.DATA_PROCESSED / Path("WEB_normalized.csv")


def load_peexcel():
    return pd.read_csv(PEEXCEL_PATH, index_col=0, parse_dates=True)


def load_web(year=None):
    df = web.read(WEB_PATH, decimal=",")
    if year:
        df = df[df.index.year==year]
    return df


def load_spotprice():
    print("Needs to be implemented: loads the drexelco2s signals")
    return None

def load_pypsa_avg():
    print("Needs to be implemented: loads the rolling average signals from MAx Nutz MA with PyPSA")
    return None

