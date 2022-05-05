import pandas as pd

import  FLUCCOplus.utils as utils
import FLUCCOplus.config as config
import FLUCCOplus.web as web
from pathlib import Path

PEEXCEL_PATH = config.DATA_PROCESSED / Path("peexcel_normalized.csv")
WEB_PATH = config.DATA_PROCESSED / Path("WEB_normalized.csv")
SPOT_PATH = config.DATA_PROCESSED / Path("DrexelCO2/Signale_CO2mix_SpotMarket.xlsx")
MANUTZ_PATH = config.DATA_PROCESSED / Path("MANutz/maxnutz_normalized.csv")

def load_peexcel():
    return pd.read_csv(PEEXCEL_PATH, index_col=0, parse_dates=True)


def load_web(year=None):
    df = web.read(WEB_PATH, decimal=",")
    if year:
        df = df[df.index.year==year]
    return df


def load_spotprice(year=None):
    import numpy as np
    dates = np.arange(f"{year}-01-01", f"{year+1}-01-01 00:00", dtype="datetime64[h]")
    df = pd.read_excel(SPOT_PATH, index_col=(0))
    df.index = dates
    return df

def load_pypsa_avg(year=None):
    utils.maxnutz()
    import numpy as np
    dates = np.arange(f"{year}-01-01", f"{year+1}-01-01 00:00", dtype="datetime64[h]")
    df = pd.read_csv(MANUTZ_PATH, sep=";", decimal=",", index_col=(0))
    df.index = dates
    return df


def signaleigenschaften(df_desc):
    df_desc = pd.DataFrame()
    df_desc["Zeitraum mit Signal [h]"] = anzahl18[cut]
    df_desc["Nicht-Signal-Zeitraum [h]"] = 8760 - anzahl18[cut]
    df_desc["Anzahl Signal-Perioden"] = df18_step.max()
    df_desc["Durchschnittliche Dauer Signal [h]"] = (
                desc18["Zeitraum mit Signal [h]"] / desc18["Anzahl Signal-Perioden"])
    desc18["Durchschnittliche Dauer Nicht-Signal [h]"] = desc18["Nicht-Signal-Zeitraum [h]"] / desc18[
        "Anzahl Signal-Perioden"]

